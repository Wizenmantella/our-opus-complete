#!/usr/bin/env python3
"""
Viral Caption System - Advanced Animated Subtitles
Creates eye-catching captions like MrBeast, Alex Hormozi, and viral TikToks
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import subprocess
import json
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import re

class CaptionStyle(Enum):
    """Popular viral caption styles"""
    MRBEAST = "mrbeast"  # Bold, colorful, word emphasis
    HORMOZI = "hormozi"  # Black bars, white text, keyword highlights
    TIKTOK = "tiktok"   # Centered, animated per word
    PODCAST = "podcast"  # Two-tone, speaker labels
    GAMING = "gaming"   # Neon, glitch effects
    MOTIVATION = "motivation"  # Bold, gradient backgrounds

@dataclass
class Caption:
    """Individual caption with timing and style"""
    text: str
    start_time: float
    end_time: float
    style: CaptionStyle
    keywords: List[str] = None
    animation: str = "pop"
    position: str = "center"

@dataclass
class WordTiming:
    """Timing for individual words"""
    word: str
    start: float
    end: float
    emphasis: bool = False

class ViralCaptionEngine:
    """Create viral-style animated captions"""
    
    def __init__(self):
        self.style_configs = self._load_style_configs()
        
    def _load_style_configs(self) -> Dict:
        """Load viral caption style configurations"""
        
        return {
            CaptionStyle.MRBEAST: {
                "font": "Arial Black",
                "base_size": 90,
                "emphasis_size": 110,
                "colors": {
                    "primary": "white",
                    "emphasis": "yellow",
                    "background": "black@0.8"
                },
                "box_padding": 20,
                "animation": "bounce_scale",
                "position": "bottom",
                "word_spacing": 1.2
            },
            CaptionStyle.HORMOZI: {
                "font": "Helvetica Bold",
                "base_size": 70,
                "emphasis_size": 85,
                "colors": {
                    "primary": "white",
                    "emphasis": "yellow",
                    "background": "black@0.95"
                },
                "box_padding": 30,
                "animation": "slide_fade",
                "position": "center",
                "black_bars": True
            },
            CaptionStyle.TIKTOK: {
                "font": "Arial",
                "base_size": 60,
                "emphasis_size": 75,
                "colors": {
                    "primary": "white",
                    "emphasis": "red",
                    "background": "black@0.7"
                },
                "box_padding": 15,
                "animation": "word_pop",
                "position": "center",
                "stroke": True
            },
            CaptionStyle.PODCAST: {
                "font": "Arial",
                "base_size": 65,
                "emphasis_size": 65,
                "colors": {
                    "primary": "white",
                    "emphasis": "cyan",
                    "background": "black@0.8",
                    "speaker1": "blue",
                    "speaker2": "green"
                },
                "box_padding": 15,
                "animation": "fade",
                "position": "bottom",
                "show_speaker": True
            },
            CaptionStyle.GAMING: {
                "font": "Arial Black",
                "base_size": 80,
                "emphasis_size": 100,
                "colors": {
                    "primary": "white",
                    "emphasis": "magenta",
                    "background": "black@0.6",
                    "glow": "cyan"
                },
                "box_padding": 15,
                "animation": "glitch_pop",
                "position": "top",
                "effects": ["glow", "glitch"]
            },
            CaptionStyle.MOTIVATION: {
                "font": "Arial Black",
                "base_size": 85,
                "emphasis_size": 105,
                "colors": {
                    "primary": "white",
                    "emphasis": "gold",
                    "background": "gradient",
                    "gradient_start": "red",
                    "gradient_end": "orange"
                },
                "box_padding": 25,
                "animation": "power_scale",
                "position": "center",
                "uppercase": True
            }
        }
    
    def process_caption_text(self, caption: Caption) -> List[WordTiming]:
        """Process caption text into timed words"""
        
        words = caption.text.split()
        duration = caption.end_time - caption.start_time
        word_duration = duration / len(words)
        
        word_timings = []
        current_time = caption.start_time
        
        for word in words:
            # Check if word should be emphasized
            is_emphasis = False
            if caption.keywords:
                # Check if word matches any keyword (case insensitive)
                word_clean = re.sub(r'[^\w\s]', '', word.lower())
                is_emphasis = any(keyword.lower() in word_clean for keyword in caption.keywords)
            
            # Auto-detect emphasis words
            emphasis_patterns = [
                r'\b(NEVER|ALWAYS|MUST|WON\'T|CAN\'T|DON\'T)\b',
                r'\b(MILLION|BILLION|THOUSAND)\b',
                r'\b(FIRST|LAST|ONLY|BEST|WORST)\b',
                r'\b(INSANE|CRAZY|AMAZING|INCREDIBLE)\b'
            ]
            
            if not is_emphasis:
                for pattern in emphasis_patterns:
                    if re.search(pattern, word.upper()):
                        is_emphasis = True
                        break
            
            word_timing = WordTiming(
                word=word,
                start=current_time,
                end=current_time + word_duration,
                emphasis=is_emphasis
            )
            
            word_timings.append(word_timing)
            current_time += word_duration
        
        return word_timings
    
    def create_animated_caption(self, caption: Caption) -> str:
        """Create FFmpeg filter for animated caption"""
        
        style = self.style_configs[caption.style]
        word_timings = self.process_caption_text(caption)
        
        filters = []
        
        # Add black bars for Hormozi style
        if style.get("black_bars"):
            filters.append("split[main][bars]")
            filters.append("[bars]drawbox=x=0:y=ih*0.3:w=iw:h=ih*0.4:color=black@0.95:t=fill[bars_out]")
            filters.append("[main][bars_out]overlay")
        
        # Process each word
        for i, word_timing in enumerate(word_timings):
            word_filter = self._create_word_filter(
                word_timing, 
                style, 
                i, 
                len(word_timings),
                caption.position
            )
            filters.append(word_filter)
        
        # Add overall effects
        if "effects" in style:
            if "glow" in style["effects"]:
                filters.append(self._add_glow_effect(style))
            if "glitch" in style["effects"]:
                filters.append(self._add_glitch_effect())
        
        return ",".join(filters)
    
    def _create_word_filter(self, word_timing: WordTiming, style: Dict, 
                           index: int, total_words: int, position: str) -> str:
        """Create filter for individual word animation"""
        
        # Base properties
        if word_timing.emphasis:
            fontsize = style["emphasis_size"]
            fontcolor = style["colors"]["emphasis"]
        else:
            fontsize = style["base_size"]
            fontcolor = style["colors"]["primary"]
        
        # Calculate position
        x_pos, y_pos = self._calculate_position(position, index, total_words)
        
        # Apply animation based on style
        animation = style["animation"]
        
        if animation == "bounce_scale":
            # MrBeast style - words bounce and scale
            scale_factor = 1.3 if word_timing.emphasis else 1.1
            filter_str = (
                f"drawtext=text='{word_timing.word}':"
                f"fontfile='{style['font']}':"
                f"fontsize={fontsize}*if(between(t\\,{word_timing.start}\\,{word_timing.start + 0.1})\\,{scale_factor}\\,1):"
                f"fontcolor={fontcolor}:"
                f"x={x_pos}:"
                f"y={y_pos}+if(between(t\\,{word_timing.start}\\,{word_timing.start + 0.1})\\,-20\\,0):"
                f"box=1:boxcolor={style['colors']['background']}:"
                f"boxborderw={style['box_padding']}:"
                f"enable='between(t\\,{word_timing.start}\\,{word_timing.end})'"
            )
            
        elif animation == "word_pop":
            # TikTok style - words pop in one by one
            filter_str = (
                f"drawtext=text='{word_timing.word}':"
                f"fontfile='{style['font']}':"
                f"fontsize={fontsize}:"
                f"fontcolor={fontcolor}:"
                f"x={x_pos}:"
                f"y={y_pos}:"
                f"box=1:boxcolor={style['colors']['background']}:"
                f"boxborderw={style['box_padding']}:"
                f"alpha='if(lt(t-{word_timing.start}\\,0.1)\\,(t-{word_timing.start})*10\\,1)':"
                f"enable='between(t\\,{word_timing.start}\\,{word_timing.end})'"
            )
            
        elif animation == "slide_fade":
            # Hormozi style - slide and fade
            filter_str = (
                f"drawtext=text='{word_timing.word}':"
                f"fontfile='{style['font']}':"
                f"fontsize={fontsize}:"
                f"fontcolor={fontcolor}:"
                f"x={x_pos}+if(lt(t-{word_timing.start}\\,0.2)\\,(0.2-(t-{word_timing.start}))*100\\,0):"
                f"y={y_pos}:"
                f"alpha='if(lt(t-{word_timing.start}\\,0.2)\\,(t-{word_timing.start})*5\\,1)':"
                f"enable='between(t\\,{word_timing.start}\\,{word_timing.end})'"
            )
            
        elif animation == "glitch_pop":
            # Gaming style - glitch effect on emphasis
            if word_timing.emphasis:
                filter_str = (
                    f"drawtext=text='{word_timing.word}':"
                    f"fontfile='{style['font']}':"
                    f"fontsize={fontsize}:"
                    f"fontcolor={fontcolor}:"
                    f"x={x_pos}+random(1)*10-5:"
                    f"y={y_pos}+random(2)*10-5:"
                    f"box=1:boxcolor={style['colors']['background']}:"
                    f"boxborderw={style['box_padding']}:"
                    f"enable='between(t\\,{word_timing.start}\\,{word_timing.end})'"
                )
            else:
                filter_str = self._create_basic_word(word_timing, style, x_pos, y_pos)
                
        elif animation == "power_scale":
            # Motivation style - powerful scaling
            scale_factor = 1.5 if word_timing.emphasis else 1.2
            filter_str = (
                f"drawtext=text='{word_timing.word.upper() if style.get('uppercase') else word_timing.word}':"
                f"fontfile='{style['font']}':"
                f"fontsize={fontsize}*if(between(t\\,{word_timing.start}\\,{word_timing.start + 0.15})\\,"
                f"1+(t-{word_timing.start})*{scale_factor*4}\\,1):"
                f"fontcolor={fontcolor}:"
                f"x={x_pos}:"
                f"y={y_pos}:"
                f"box=1:boxcolor={style['colors']['background']}:"
                f"boxborderw={style['box_padding']}:"
                f"enable='between(t\\,{word_timing.start}\\,{word_timing.end})'"
            )
            
        else:
            # Default fade animation
            filter_str = self._create_basic_word(word_timing, style, x_pos, y_pos)
        
        return filter_str
    
    def _create_basic_word(self, word_timing: WordTiming, style: Dict, x: str, y: str) -> str:
        """Create basic word filter"""
        
        fontsize = style["emphasis_size"] if word_timing.emphasis else style["base_size"]
        fontcolor = style["colors"]["emphasis"] if word_timing.emphasis else style["colors"]["primary"]
        
        return (
            f"drawtext=text='{word_timing.word}':"
            f"fontfile='{style['font']}':"
            f"fontsize={fontsize}:"
            f"fontcolor={fontcolor}:"
            f"x={x}:"
            f"y={y}:"
            f"box=1:boxcolor={style['colors']['background']}:"
            f"boxborderw={style['box_padding']}:"
            f"enable='between(t\\,{word_timing.start}\\,{word_timing.end})'"
        )
    
    def _calculate_position(self, position: str, word_index: int, 
                           total_words: int) -> Tuple[str, str]:
        """Calculate word position based on style"""
        
        if position == "center":
            # Center each word
            x = "(w-text_w)/2"
            y = "(h-text_h)/2"
        elif position == "bottom":
            # Bottom with word flow
            words_per_line = 5
            line = word_index // words_per_line
            x = f"(w-text_w)/2 + {(word_index % words_per_line - 2) * 150}"
            y = f"h*0.85 - {line * 100}"
        elif position == "top":
            x = "(w-text_w)/2"
            y = "h*0.1"
        else:
            x = "(w-text_w)/2"
            y = "(h-text_h)/2"
        
        return x, y
    
    def _add_glow_effect(self, style: Dict) -> str:
        """Add glow effect to text"""
        
        glow_color = style["colors"].get("glow", "cyan")
        return f"gblur=sigma=3:steps=1,colorize={glow_color}:0.5"
    
    def _add_glitch_effect(self) -> str:
        """Add glitch effect"""
        
        return "noise=alls=20:allf=t+u"
    
    def create_keyword_highlight_system(self, text: str, keywords: List[str]) -> Dict:
        """Create a system to highlight keywords in captions"""
        
        # Analyze text for keyword placement
        highlighted_text = text
        keyword_positions = []
        
        for keyword in keywords:
            pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                keyword_positions.append({
                    "keyword": keyword,
                    "start": match.start(),
                    "end": match.end(),
                    "original": match.group()
                })
        
        return {
            "text": highlighted_text,
            "keywords": keyword_positions,
            "highlight_filter": self._create_highlight_filter(keyword_positions)
        }
    
    def _create_highlight_filter(self, keyword_positions: List[Dict]) -> str:
        """Create filter to highlight keywords"""
        
        filters = []
        
        for pos in keyword_positions:
            # Create colored box behind keyword
            highlight = (
                f"drawbox=x={pos['start']*20}:y=h*0.8-5:"
                f"w={len(pos['keyword'])*25}:h=40:"
                f"color=yellow@0.5:t=fill"
            )
            filters.append(highlight)
        
        return ",".join(filters)
    
    def create_speaker_labels(self, speaker: str, color: str = "blue") -> str:
        """Create speaker label for podcast-style captions"""
        
        return (
            f"drawtext=text='{speaker}:':"
            f"fontfile='Arial Bold':fontsize=50:"
            f"fontcolor={color}:"
            f"x=50:y=h*0.75:"
            f"box=1:boxcolor=black@0.8:boxborderw=10"
        )


class ViralCaptionProcessor:
    """Process and apply viral captions to videos"""
    
    def __init__(self):
        self.caption_engine = ViralCaptionEngine()
    
    def generate_captions_from_audio(self, audio_file: str) -> List[Caption]:
        """Generate captions from audio (placeholder for speech recognition)"""
        
        # In real implementation, use speech recognition
        # This is a demo with sample captions
        sample_captions = [
            Caption(
                text="This will LITERALLY change your life",
                start_time=0.0,
                end_time=2.5,
                style=CaptionStyle.MRBEAST,
                keywords=["LITERALLY", "change", "life"]
            ),
            Caption(
                text="I spent 30 DAYS testing this method",
                start_time=2.5,
                end_time=5.0,
                style=CaptionStyle.MRBEAST,
                keywords=["30 DAYS", "testing"]
            ),
            Caption(
                text="And the results were INSANE",
                start_time=5.0,
                end_time=7.0,
                style=CaptionStyle.MRBEAST,
                keywords=["results", "INSANE"]
            )
        ]
        
        return sample_captions
    
    def apply_viral_captions(self, input_video: str, output_video: str, 
                            captions: List[Caption], style: CaptionStyle) -> bool:
        """Apply viral captions to video"""
        
        filters = []
        
        for caption in captions:
            caption.style = style  # Override with selected style
            caption_filter = self.caption_engine.create_animated_caption(caption)
            filters.append(caption_filter)
        
        # Build FFmpeg command
        filter_complex = ",".join(filters) if filters else "copy"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-vf", filter_complex,
            "-c:a", "copy",
            "-preset", "fast",
            output_video
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Error applying captions: {e}")
            return False


def demo_viral_captions():
    """Demo viral caption styles"""
    
    print("🎬 Viral Caption System")
    print("\nAvailable Styles:")
    for style in CaptionStyle:
        print(f"- {style.value}: {style.name}")
    
    print("\nCaption Features:")
    print("- Automatic keyword emphasis")
    print("- Word-by-word animations")
    print("- Multiple animation styles")
    print("- Speaker labels for podcasts")
    print("- Glow and glitch effects")
    print("- Smart word positioning")
    
    print("\nExample Caption Configuration:")
    example = {
        "text": "This hack will save you THOUSANDS of dollars",
        "keywords": ["hack", "THOUSANDS", "dollars"],
        "style": "mrbeast",
        "animation": "bounce_scale"
    }
    print(json.dumps(example, indent=2))


if __name__ == "__main__":
    demo_viral_captions()