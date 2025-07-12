#!/usr/bin/env python3
"""
Viral Effects Engine - Modern Social Media Video Effects
Creates trending effects seen in viral TikTok, Instagram, and YouTube videos
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import subprocess
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class TransitionType(Enum):
    """Viral transition types"""
    GLITCH = "glitch"
    WHIP_PAN = "whip_pan"
    ZOOM_PUNCH = "zoom_punch"
    RGB_SPLIT = "rgb_split"
    SPIN = "spin"
    MORPH = "morph"
    FLASH = "flash"
    SHAKE = "shake"
    SLIDE = "slide"
    WARP = "warp"

class TextAnimation(Enum):
    """Text animation styles"""
    TYPEWRITER = "typewriter"
    BOUNCE = "bounce"
    SLIDE_UP = "slide_up"
    FADE_WORDS = "fade_words"
    GLITCH_TEXT = "glitch_text"
    NEON_GLOW = "neon_glow"
    THREE_D_SPIN = "3d_spin"
    WAVE = "wave"
    EXPLOSION = "explosion"

@dataclass
class ViralEffect:
    """Viral effect configuration"""
    name: str
    intensity: float = 1.0
    duration: float = 0.5
    params: Dict = None

class ViralEffectsEngine:
    """Advanced viral video effects engine"""
    
    def __init__(self):
        self.ffmpeg_filters = []
        self.complex_filters = []
        
    def create_hook_intro(self, text: str, style: str = "explosive") -> str:
        """Create viral hook intro with text"""
        
        hooks = {
            "explosive": {
                "font_size": 120,
                "font_color": "yellow",
                "box_color": "red@0.9",
                "animation": "scale=2:2,zoompan=z='if(lte(mod(t,0.5),0.25),2,1)':d=1",
                "shake": "crop=in_w:in_h:sin(t*50)*5:cos(t*50)*5"
            },
            "mystery": {
                "font_size": 100,
                "font_color": "white",
                "box_color": "black@0.8",
                "animation": "fade=in:0:10",
                "blur": "boxblur=10:1:cr=0:ar=0,fade=out:20:10"
            },
            "urgent": {
                "font_size": 110,
                "font_color": "red",
                "box_color": "yellow@0.9",
                "animation": "rotate=PI/4*sin(t*10):c=none",
                "flash": "eq=brightness=sin(t*20)*0.5+1"
            }
        }
        
        hook_style = hooks.get(style, hooks["explosive"])
        
        # Build complex filter for hook
        filters = []
        
        # Animated text
        text_filter = f"drawtext=text='{text}':fontsize={hook_style['font_size']}:fontcolor={hook_style['font_color']}:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor={hook_style['box_color']}:boxborderw=20"
        filters.append(text_filter)
        
        # Add animation
        if "animation" in hook_style:
            filters.append(hook_style["animation"])
        
        # Add shake effect
        if "shake" in hook_style:
            filters.append(hook_style["shake"])
        
        # Add flash effect
        if "flash" in hook_style:
            filters.append(hook_style["flash"])
        
        return ",".join(filters)
    
    def create_transition(self, transition_type: TransitionType, duration: float = 0.5) -> str:
        """Create viral transition effect"""
        
        if transition_type == TransitionType.GLITCH:
            # Digital glitch effect
            return self._glitch_transition(duration)
        
        elif transition_type == TransitionType.WHIP_PAN:
            # Fast horizontal motion blur
            return f"boxblur=luma_radius=50:chroma_radius=50:luma_power=1,rotate=t*10:c=black"
        
        elif transition_type == TransitionType.ZOOM_PUNCH:
            # Quick zoom in/out
            return f"zoompan=z='if(lt(mod(t,{duration}),{duration/2}),1.5,1)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        
        elif transition_type == TransitionType.RGB_SPLIT:
            # Chromatic aberration
            return self._rgb_split_effect(duration)
        
        elif transition_type == TransitionType.SPIN:
            # 360 spin transition
            return f"rotate=2*PI*t/{duration}:c=black"
        
        elif transition_type == TransitionType.FLASH:
            # White flash
            return f"fade=out:st=0:d={duration/2}:c=white,fade=in:st={duration/2}:d={duration/2}:c=white"
        
        elif transition_type == TransitionType.SHAKE:
            # Camera shake
            return f"crop=in_w:in_h:sin(t*100)*20:cos(t*100)*20"
        
        elif transition_type == TransitionType.WARP:
            # Warp/distortion effect
            return f"perspective=x0=sin(t*5)*100:y0=0:x1=W:y1=sin(t*5)*100:x2=0:y2=H:x3=W:y3=H"
        
        else:
            # Default slide
            return f"scale=iw*2:ih*2,crop=iw/2:ih/2:iw/2*t/{duration}:0"
    
    def _glitch_transition(self, duration: float) -> str:
        """Create digital glitch effect"""
        
        # Combination of RGB shift, noise, and displacement
        glitch_filters = [
            # RGB channel shift
            "split[r][g][b]",
            "[r]lutrgb=g=0:b=0,crop=iw:ih:sin(t*100)*10:0[r1]",
            "[g]lutrgb=r=0:b=0,crop=iw:ih:0:cos(t*100)*10[g1]", 
            "[b]lutrgb=r=0:g=0,crop=iw:ih:sin(t*50)*5:sin(t*50)*5[b1]",
            "[r1][g1][b1]merge=3",
            # Add digital noise
            f"noise=alls=20:allf=t+u,eq=brightness=sin(t*50)*0.2"
        ]
        
        return ";".join(glitch_filters)
    
    def _rgb_split_effect(self, duration: float) -> str:
        """Create RGB split/chromatic aberration"""
        
        split_amount = 10
        return (
            f"split=3[r][g][b];"
            f"[r]lutrgb=g=0:b=0,crop=iw:ih:{split_amount}:0[r1];"
            f"[g]lutrgb=r=0:b=0[g1];"
            f"[b]lutrgb=r=0:g=0,crop=iw:ih:-{split_amount}:0[b1];"
            f"[r1][g1]blend=all_mode=screen[rg];"
            f"[rg][b1]blend=all_mode=screen"
        )
    
    def create_text_animation(self, text: str, animation: TextAnimation, 
                            position: str = "center", duration: float = 2.0) -> str:
        """Create animated text overlays"""
        
        # Base text properties
        base_props = {
            "fontsize": 80,
            "fontcolor": "white",
            "box": 1,
            "boxcolor": "black@0.7",
            "boxborderw": 15
        }
        
        # Position calculations
        positions = {
            "center": "x=(w-text_w)/2:y=(h-text_h)/2",
            "top": "x=(w-text_w)/2:y=h*0.1",
            "bottom": "x=(w-text_w)/2:y=h*0.85",
            "left": "x=w*0.1:y=(h-text_h)/2",
            "right": "x=w*0.8:y=(h-text_h)/2"
        }
        
        pos = positions.get(position, positions["center"])
        
        if animation == TextAnimation.TYPEWRITER:
            # Typewriter effect - reveal text character by character
            return f"drawtext=text='{text}':fontsize={base_props['fontsize']}:fontcolor={base_props['fontcolor']}:{pos}:box={base_props['box']}:boxcolor={base_props['boxcolor']}:boxborderw={base_props['boxborderw']}:enable='gte(t,0)':text_shaping=1"
        
        elif animation == TextAnimation.BOUNCE:
            # Bouncing text
            return f"drawtext=text='{text}':fontsize={base_props['fontsize']}:fontcolor={base_props['fontcolor']}:x=(w-text_w)/2:y=(h-text_h)/2+sin(t*5)*20:box={base_props['box']}:boxcolor={base_props['boxcolor']}:boxborderw={base_props['boxborderw']}"
        
        elif animation == TextAnimation.SLIDE_UP:
            # Slide up from bottom
            return f"drawtext=text='{text}':fontsize={base_props['fontsize']}:fontcolor={base_props['fontcolor']}:x=(w-text_w)/2:y=if(lt(t\\,{duration/2})\\,h-(t*2*h/{duration})\\,(h-text_h)/2):box={base_props['box']}:boxcolor={base_props['boxcolor']}:boxborderw={base_props['boxborderw']}"
        
        elif animation == TextAnimation.GLITCH_TEXT:
            # Glitchy text with color shifts
            return f"drawtext=text='{text}':fontsize={base_props['fontsize']}:fontcolor=white:x=(w-text_w)/2+sin(t*100)*5:y=(h-text_h)/2+cos(t*100)*5:box={base_props['box']}:boxcolor={base_props['boxcolor']}:boxborderw={base_props['boxborderw']}"
        
        elif animation == TextAnimation.NEON_GLOW:
            # Neon glow effect
            glow_filter = f"drawtext=text='{text}':fontsize={base_props['fontsize']+4}:fontcolor=cyan:{pos}:alpha=0.5,drawtext=text='{text}':fontsize={base_props['fontsize']}:fontcolor=white:{pos}"
            return glow_filter
        
        elif animation == TextAnimation.WAVE:
            # Wave animation
            return f"drawtext=text='{text}':fontsize={base_props['fontsize']}:fontcolor={base_props['fontcolor']}:x=(w-text_w)/2+sin(t*3)*30:y=(h-text_h)/2+sin(t*3+1)*20:box={base_props['box']}:boxcolor={base_props['boxcolor']}:boxborderw={base_props['boxborderw']}"
        
        else:
            # Default fade in
            return f"drawtext=text='{text}':fontsize={base_props['fontsize']}:fontcolor={base_props['fontcolor']}:{pos}:box={base_props['box']}:boxcolor={base_props['boxcolor']}:boxborderw={base_props['boxborderw']}:alpha='if(lt(t\\,1)\\,t\\,1)'"
    
    def create_speed_ramp(self, start_time: float, end_time: float, 
                         speed_factor: float = 0.5) -> str:
        """Create speed ramping effect (slow-mo to fast)"""
        
        if speed_factor < 1:
            # Slow motion
            return f"setpts={1/speed_factor}*PTS"
        else:
            # Fast forward
            return f"setpts={1/speed_factor}*PTS"
    
    def create_zoom_punch(self, timestamp: float, intensity: float = 1.5) -> str:
        """Create zoom punch effect on beat"""
        
        zoom_duration = 0.2
        return f"zoompan=z='if(between(t\\,{timestamp}\\,{timestamp+zoom_duration})\\,{intensity}\\,1)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=hd1080"
    
    def create_shake_effect(self, intensity: float = 10, duration: float = 0.5) -> str:
        """Create camera shake effect"""
        
        return f"crop=in_w:in_h:sin(t*100)*{intensity}:cos(t*100)*{intensity}"
    
    def create_progress_bar(self, position: str = "bottom", color: str = "red") -> str:
        """Create progress bar overlay"""
        
        bar_height = 8
        if position == "bottom":
            return f"drawbox=x=0:y=h-{bar_height}:w=w*t/duration:h={bar_height}:color={color}:t=fill"
        else:  # top
            return f"drawbox=x=0:y=0:w=w*t/duration:h={bar_height}:color={color}:t=fill"
    
    def create_countdown_timer(self, start_number: int = 3) -> str:
        """Create countdown timer overlay"""
        
        countdown_filters = []
        for i in range(start_number, 0, -1):
            start_time = (start_number - i)
            end_time = start_time + 1
            
            filter_text = f"drawtext=text='{i}':fontsize=200:fontcolor=yellow:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=red@0.8:boxborderw=20:enable='between(t\\,{start_time}\\,{end_time})'"
            countdown_filters.append(filter_text)
        
        return ",".join(countdown_filters)
    
    def create_emoji_reaction(self, emoji: str, position: Tuple[int, int], 
                            animation: str = "bounce") -> str:
        """Create animated emoji overlay"""
        
        # Note: In real implementation, would overlay emoji image
        # This creates a text-based emoji with animation
        
        x, y = position
        
        if animation == "bounce":
            return f"drawtext=text='{emoji}':fontsize=100:x={x}:y={y}+sin(t*5)*20:enable='gte(t\\,0)'"
        elif animation == "grow":
            return f"drawtext=text='{emoji}':fontsize=50+t*50:x={x}:y={y}:enable='between(t\\,0\\,2)'"
        elif animation == "spin":
            return f"drawtext=text='{emoji}':fontsize=80:x={x}+sin(t*5)*20:y={y}+cos(t*5)*20:enable='gte(t\\,0)'"
        else:
            return f"drawtext=text='{emoji}':fontsize=80:x={x}:y={y}:enable='gte(t\\,0)'"
    
    def create_split_screen(self, layout: str = "vertical") -> str:
        """Create split screen effect"""
        
        if layout == "vertical":
            # Side by side
            return "[0:v]scale=iw/2:ih,pad=iw*2:ih[left];[1:v]scale=iw/2:ih[right];[left][right]overlay=w"
        elif layout == "horizontal":
            # Top and bottom
            return "[0:v]scale=iw:ih/2,pad=iw:ih*2[top];[1:v]scale=iw:ih/2[bottom];[top][bottom]overlay=0:h"
        elif layout == "grid":
            # 2x2 grid
            return "[0:v]scale=iw/2:ih/2[tl];[1:v]scale=iw/2:ih/2[tr];[2:v]scale=iw/2:ih/2[bl];[3:v]scale=iw/2:ih/2[br];[tl][tr]hstack[top];[bl][br]hstack[bottom];[top][bottom]vstack"
        else:
            return "[0:v][1:v]hstack"
    
    def create_retention_hook(self, hook_type: str = "question") -> str:
        """Create retention hooks to keep viewers watching"""
        
        hooks = {
            "question": "drawtext=text='Can you spot it?':fontsize=60:fontcolor=yellow:x=(w-text_w)/2:y=h*0.8:box=1:boxcolor=red@0.8:boxborderw=10",
            "wait_for_it": "drawtext=text='WAIT FOR IT...':fontsize=80:fontcolor=white:x=(w-text_w)/2:y=h*0.5:box=1:boxcolor=black@0.8:boxborderw=15:enable='between(t\\,0\\,3)'",
            "part_indicator": "drawtext=text='Part 1/3':fontsize=50:fontcolor=white:x=w*0.85:y=h*0.05:box=1:boxcolor=black@0.7:boxborderw=10",
            "arrow": "drawtext=text='👇':fontsize=100:x=w*0.5:y=h*0.7+sin(t*3)*10:enable='gte(t\\,0)'"
        }
        
        return hooks.get(hook_type, hooks["question"])
    
    def create_viral_filter_chain(self, effects: List[ViralEffect]) -> str:
        """Chain multiple viral effects together"""
        
        filter_chain = []
        
        for effect in effects:
            if effect.name == "glitch":
                filter_chain.append(self.create_transition(TransitionType.GLITCH, effect.duration))
            elif effect.name == "zoom_punch":
                filter_chain.append(self.create_zoom_punch(effect.params.get("timestamp", 0), effect.intensity))
            elif effect.name == "shake":
                filter_chain.append(self.create_shake_effect(effect.intensity, effect.duration))
            elif effect.name == "text":
                filter_chain.append(self.create_text_animation(
                    effect.params.get("text", ""), 
                    effect.params.get("animation", TextAnimation.BOUNCE),
                    effect.params.get("position", "center"),
                    effect.duration
                ))
            elif effect.name == "progress":
                filter_chain.append(self.create_progress_bar())
            elif effect.name == "countdown":
                filter_chain.append(self.create_countdown_timer(effect.params.get("start", 3)))
        
        return ",".join(filter_chain)


class ViralVideoProcessor:
    """Process videos with viral effects"""
    
    def __init__(self):
        self.effects_engine = ViralEffectsEngine()
    
    def apply_viral_edit(self, input_video: str, output_video: str, 
                        effects_config: Dict) -> bool:
        """Apply viral effects to video"""
        
        # Build filter complex from config
        filters = []
        
        # Hook intro
        if effects_config.get("hook"):
            hook_filter = self.effects_engine.create_hook_intro(
                effects_config["hook"]["text"],
                effects_config["hook"]["style"]
            )
            filters.append(hook_filter)
        
        # Text overlays
        if effects_config.get("text_overlays"):
            for text_config in effects_config["text_overlays"]:
                text_filter = self.effects_engine.create_text_animation(
                    text_config["text"],
                    TextAnimation[text_config["animation"]],
                    text_config.get("position", "center"),
                    text_config.get("duration", 2.0)
                )
                filters.append(text_filter)
        
        # Transitions
        if effects_config.get("transitions"):
            for trans in effects_config["transitions"]:
                trans_filter = self.effects_engine.create_transition(
                    TransitionType[trans["type"]],
                    trans.get("duration", 0.5)
                )
                filters.append(trans_filter)
        
        # Speed effects
        if effects_config.get("speed_ramps"):
            for ramp in effects_config["speed_ramps"]:
                speed_filter = self.effects_engine.create_speed_ramp(
                    ramp["start"],
                    ramp["end"],
                    ramp["speed"]
                )
                filters.append(speed_filter)
        
        # Progress bar
        if effects_config.get("progress_bar"):
            filters.append(self.effects_engine.create_progress_bar())
        
        # Retention hooks
        if effects_config.get("retention_hooks"):
            for hook in effects_config["retention_hooks"]:
                hook_filter = self.effects_engine.create_retention_hook(hook["type"])
                filters.append(hook_filter)
        
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
            print(f"Error applying viral effects: {e}")
            return False


def demo_viral_effects():
    """Demo viral effects configuration"""
    
    viral_config = {
        "hook": {
            "text": "YOU WON'T BELIEVE THIS!",
            "style": "explosive"
        },
        "text_overlays": [
            {
                "text": "Wait for it...",
                "animation": "BOUNCE",
                "position": "center",
                "duration": 2.0
            },
            {
                "text": "Mind = Blown 🤯",
                "animation": "GLITCH_TEXT",
                "position": "bottom",
                "duration": 1.5
            }
        ],
        "transitions": [
            {"type": "GLITCH", "duration": 0.3},
            {"type": "ZOOM_PUNCH", "duration": 0.2}
        ],
        "speed_ramps": [
            {"start": 5.0, "end": 7.0, "speed": 0.5},  # Slow motion
            {"start": 10.0, "end": 11.0, "speed": 2.0}  # Fast forward
        ],
        "progress_bar": True,
        "retention_hooks": [
            {"type": "question"},
            {"type": "wait_for_it"}
        ]
    }
    
    return viral_config


if __name__ == "__main__":
    # Demo the viral effects engine
    engine = ViralEffectsEngine()
    
    print("🎬 Viral Effects Engine Initialized")
    print("\nAvailable Effects:")
    print("- Hook Intros: explosive, mystery, urgent")
    print("- Transitions:", [t.value for t in TransitionType])
    print("- Text Animations:", [a.value for a in TextAnimation])
    print("- Retention Hooks: question, wait_for_it, part_indicator, arrow")
    print("\nExample Configuration:")
    print(demo_viral_effects())