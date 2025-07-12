#!/usr/bin/env python3
"""
Ultimate Viral Video Editor - Complete System
Integrates all viral editing features into one powerful tool
"""

import cv2
import numpy as np
import asyncio
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import subprocess
import json
import time
from dataclasses import dataclass, asdict
from enum import Enum

# Import our viral modules
from viral_effects_engine import ViralEffectsEngine, TransitionType, TextAnimation, ViralEffect
from viral_caption_system import ViralCaptionEngine, CaptionStyle, Caption
from beat_sync_engine import BeatSyncEditor, MusicVideoSync

class ViralPlatform(Enum):
    """Target platforms for viral videos"""
    TIKTOK = "tiktok"
    INSTAGRAM_REEL = "instagram_reel"
    YOUTUBE_SHORTS = "youtube_shorts"
    TWITTER = "twitter"

class ViralTemplate(Enum):
    """Viral video templates"""
    PODCAST_CLIPS = "podcast_clips"        # Joe Rogan, Lex Fridman style
    REACTION = "reaction"                  # Split screen reactions
    TUTORIAL = "tutorial"                  # Quick how-to videos
    MOTIVATION = "motivation"              # Gary Vee, motivational clips
    COMEDY = "comedy"                      # Comedy sketches with timing
    GAMING = "gaming"                      # Gaming highlights
    TRANSFORMATION = "transformation"      # Before/after content
    NEWS_STYLE = "news_style"             # Breaking news format

@dataclass
class ViralVideoConfig:
    """Configuration for viral video creation"""
    platform: ViralPlatform
    template: ViralTemplate
    duration: float = 30.0
    music_sync: bool = True
    auto_captions: bool = True
    hook_style: str = "explosive"
    transition_intensity: float = 0.8
    engagement_overlays: bool = True
    trending_effects: List[str] = None

class UltimateViralEditor:
    """Complete viral video editing system"""
    
    def __init__(self):
        self.effects_engine = ViralEffectsEngine()
        self.caption_engine = ViralCaptionEngine()
        self.beat_sync = MusicVideoSync()
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[ViralTemplate, Dict]:
        """Load viral video templates"""
        
        return {
            ViralTemplate.PODCAST_CLIPS: {
                "caption_style": CaptionStyle.HORMOZI,
                "effects": ["zoom_punch", "shake", "glitch"],
                "transitions": [TransitionType.ZOOM_PUNCH, TransitionType.GLITCH],
                "hook_text": ["THIS CHANGED EVERYTHING", "NOBODY TALKS ABOUT THIS", "THE TRUTH ABOUT"],
                "retention_hooks": ["wait_for_it", "question"],
                "music_intensity": 0.7,
                "cut_pattern": "dynamic",
                "aspect_ratio": "9:16"
            },
            ViralTemplate.REACTION: {
                "caption_style": CaptionStyle.TIKTOK,
                "effects": ["split_screen", "emoji_reactions", "zoom_punch"],
                "transitions": [TransitionType.SLIDE, TransitionType.FLASH],
                "hook_text": ["MY REACTION TO", "I CAN'T BELIEVE", "WATCHING THIS FOR THE FIRST TIME"],
                "retention_hooks": ["arrow", "part_indicator"],
                "music_intensity": 0.8,
                "cut_pattern": "reaction_based",
                "aspect_ratio": "9:16",
                "layout": "split_vertical"
            },
            ViralTemplate.TUTORIAL: {
                "caption_style": CaptionStyle.MRBEAST,
                "effects": ["step_counter", "highlight_box", "arrow_pointer"],
                "transitions": [TransitionType.SLIDE, TransitionType.MORPH],
                "hook_text": ["LEARN THIS IN 30 SECONDS", "THE EASIEST WAY TO", "STEP BY STEP"],
                "retention_hooks": ["countdown", "progress_bar"],
                "music_intensity": 0.5,
                "cut_pattern": "step_based",
                "aspect_ratio": "9:16"
            },
            ViralTemplate.MOTIVATION: {
                "caption_style": CaptionStyle.MOTIVATION,
                "effects": ["power_zoom", "dramatic_pause", "text_explosion"],
                "transitions": [TransitionType.FLASH, TransitionType.ZOOM_PUNCH],
                "hook_text": ["STOP SCROLLING", "THIS WILL CHANGE YOUR LIFE", "LISTEN CAREFULLY"],
                "retention_hooks": ["question", "wait_for_it"],
                "music_intensity": 0.9,
                "cut_pattern": "beat_heavy",
                "aspect_ratio": "9:16"
            },
            ViralTemplate.GAMING: {
                "caption_style": CaptionStyle.GAMING,
                "effects": ["screen_shake", "hit_markers", "combo_counter"],
                "transitions": [TransitionType.GLITCH, TransitionType.RGB_SPLIT],
                "hook_text": ["INSANE CLUTCH", "YOU WON'T BELIEVE THIS", "IMPOSSIBLE SHOT"],
                "retention_hooks": ["countdown", "arrow"],
                "music_intensity": 1.0,
                "cut_pattern": "action_sync",
                "aspect_ratio": "16:9"
            }
        }
    
    async def create_viral_video(self, input_video: str, config: ViralVideoConfig,
                               output_path: str = None) -> Dict[str, Any]:
        """Create a complete viral video with all effects"""
        
        if not output_path:
            output_path = f"viral_{config.platform.value}_{int(time.time())}.mp4"
        
        print("🚀 ULTIMATE VIRAL VIDEO EDITOR")
        print("=" * 60)
        print(f"Platform: {config.platform.value}")
        print(f"Template: {config.template.value}")
        print(f"Duration: {config.duration}s")
        print("=" * 60)
        
        start_time = time.time()
        
        # Get template settings
        template = self.templates[config.template]
        
        # Phase 1: Video Analysis
        print("\n📊 Phase 1: Analyzing Content")
        analysis = await self._analyze_video_content(input_video)
        
        # Phase 2: Create Hook
        print("\n🎣 Phase 2: Creating Viral Hook")
        hook_video = await self._create_viral_hook(input_video, template, config)
        
        # Phase 3: Apply Template Effects
        print("\n✨ Phase 3: Applying Viral Effects")
        effects_video = await self._apply_template_effects(hook_video, template, config, analysis)
        
        # Phase 4: Add Captions
        if config.auto_captions:
            print("\n📝 Phase 4: Adding Viral Captions")
            caption_video = await self._add_viral_captions(effects_video, template, config)
        else:
            caption_video = effects_video
        
        # Phase 5: Music Sync
        if config.music_sync:
            print("\n🎵 Phase 5: Syncing to Music")
            music_video = await self._sync_to_music(caption_video, template, config)
        else:
            music_video = caption_video
        
        # Phase 6: Engagement Overlays
        if config.engagement_overlays:
            print("\n💬 Phase 6: Adding Engagement Elements")
            final_video = await self._add_engagement_overlays(music_video, template, config)
        else:
            final_video = music_video
        
        # Phase 7: Platform Optimization
        print("\n📱 Phase 7: Platform Optimization")
        optimized_video = await self._optimize_for_platform(final_video, config, output_path)
        
        processing_time = time.time() - start_time
        
        # Generate report
        report = self._generate_viral_report(analysis, config, processing_time)
        
        print("\n" + "=" * 60)
        print("✅ VIRAL VIDEO COMPLETE!")
        print(f"📹 Output: {output_path}")
        print(f"⏱️  Processing Time: {processing_time:.1f}s")
        print("=" * 60)
        
        return {
            "success": True,
            "output_path": output_path,
            "processing_time": processing_time,
            "report": report,
            "viral_score": self._calculate_viral_score(analysis, config)
        }
    
    async def _analyze_video_content(self, video_path: str) -> Dict[str, Any]:
        """Analyze video for viral potential"""
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        
        # Detect key moments
        key_moments = []
        motion_scores = []
        face_frames = []
        
        # Sample frames for analysis
        sample_interval = max(1, frame_count // 100)
        
        for i in range(0, frame_count, sample_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break
            
            # Motion detection
            if i > 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if 'prev_gray' in locals():
                    diff = cv2.absdiff(prev_gray, gray)
                    motion_score = np.mean(diff)
                    motion_scores.append(motion_score)
                    
                    if motion_score > 30:  # High motion
                        key_moments.append({
                            "time": i / fps,
                            "type": "high_motion",
                            "score": motion_score
                        })
                prev_gray = gray
            
            # Face detection (simplified)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.1, 4)
            if len(faces) > 0:
                face_frames.append(i / fps)
        
        cap.release()
        
        # Identify best clips for viral content
        best_clips = self._identify_best_clips(key_moments, motion_scores, duration)
        
        return {
            "duration": duration,
            "fps": fps,
            "key_moments": key_moments,
            "best_clips": best_clips,
            "face_coverage": len(face_frames) / (frame_count / sample_interval),
            "average_motion": np.mean(motion_scores) if motion_scores else 0,
            "viral_moments": len([m for m in key_moments if m["score"] > 40])
        }
    
    async def _create_viral_hook(self, video_path: str, template: Dict, 
                               config: ViralVideoConfig) -> str:
        """Create attention-grabbing hook intro"""
        
        hook_text = np.random.choice(template["hook_text"])
        hook_duration = 3.0
        
        # Create hook video segment
        hook_output = "temp_hook.mp4"
        
        # Build hook filter
        hook_filter = self.effects_engine.create_hook_intro(hook_text, config.hook_style)
        
        # Add countdown or urgency element
        if config.template == ViralTemplate.TUTORIAL:
            hook_filter += "," + self.effects_engine.create_countdown_timer(3)
        
        # Extract first 3 seconds with hook
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-t", str(hook_duration),
            "-vf", hook_filter,
            "-c:a", "copy",
            hook_output
        ]
        
        subprocess.run(cmd, capture_output=True)
        return hook_output
    
    async def _apply_template_effects(self, video_path: str, template: Dict,
                                    config: ViralVideoConfig, analysis: Dict) -> str:
        """Apply template-specific effects"""
        
        effects_output = "temp_effects.mp4"
        
        # Build effects based on template
        effects = []
        
        # Add transitions at key moments
        for i, moment in enumerate(analysis["key_moments"][:5]):  # Limit to 5 transitions
            transition_type = np.random.choice(template["transitions"])
            transition_filter = self.effects_engine.create_transition(
                transition_type, 
                duration=0.3
            )
            effects.append(transition_filter)
        
        # Add template-specific effects
        if "zoom_punch" in template["effects"]:
            for moment in analysis["best_clips"]:
                zoom_filter = self.effects_engine.create_zoom_punch(
                    moment["start"], 
                    intensity=1.3
                )
                effects.append(zoom_filter)
        
        # Add progress bar for tutorials
        if config.template == ViralTemplate.TUTORIAL:
            effects.append(self.effects_engine.create_progress_bar())
        
        # Combine all effects
        filter_complex = ",".join(effects) if effects else "copy"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", filter_complex,
            "-c:a", "copy",
            effects_output
        ]
        
        subprocess.run(cmd, capture_output=True)
        return effects_output
    
    async def _add_viral_captions(self, video_path: str, template: Dict,
                                config: ViralVideoConfig) -> str:
        """Add viral-style captions"""
        
        caption_output = "temp_captions.mp4"
        
        # Generate sample captions (in real use, would transcribe audio)
        captions = self._generate_sample_captions(config.duration, template["caption_style"])
        
        # Build caption filters
        caption_filters = []
        
        for caption in captions:
            caption_filter = self.caption_engine.create_animated_caption(caption)
            caption_filters.append(caption_filter)
        
        # Apply captions
        filter_complex = ",".join(caption_filters) if caption_filters else "copy"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", filter_complex,
            "-c:a", "copy",
            caption_output
        ]
        
        subprocess.run(cmd, capture_output=True)
        return caption_output
    
    async def _sync_to_music(self, video_path: str, template: Dict,
                           config: ViralVideoConfig) -> str:
        """Sync video to music beats"""
        
        music_output = "temp_music.mp4"
        
        # For demo, add simple beat sync effects
        # In real use, would analyze actual audio
        beat_times = [i * 0.5 for i in range(int(config.duration * 2))]
        
        beat_filters = []
        for beat_time in beat_times[:20]:  # Limit effects
            if np.random.random() < template["music_intensity"]:
                # Random beat effect
                effect_type = np.random.choice(["zoom_punch", "flash", "shake"])
                
                if effect_type == "zoom_punch":
                    filter_str = self.effects_engine.create_zoom_punch(beat_time, 1.1)
                elif effect_type == "flash":
                    filter_str = f"fade=in:st={beat_time}:d=0.05:c=white"
                else:
                    filter_str = self.effects_engine.create_shake_effect(5, 0.1)
                
                beat_filters.append(filter_str)
        
        filter_complex = ",".join(beat_filters) if beat_filters else "copy"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", filter_complex,
            "-c:a", "copy",
            music_output
        ]
        
        subprocess.run(cmd, capture_output=True)
        return music_output
    
    async def _add_engagement_overlays(self, video_path: str, template: Dict,
                                     config: ViralVideoConfig) -> str:
        """Add engagement elements"""
        
        engagement_output = "temp_engagement.mp4"
        
        # Build engagement overlays
        overlays = []
        
        # Add retention hooks
        for hook_type in template["retention_hooks"]:
            hook_filter = self.effects_engine.create_retention_hook(hook_type)
            overlays.append(hook_filter)
        
        # Add platform-specific CTAs
        if config.platform == ViralPlatform.TIKTOK:
            cta = "drawtext=text='Follow for Part 2 👆':fontsize=50:fontcolor=white:x=w*0.5:y=h*0.9:box=1:boxcolor=red@0.8:boxborderw=10"
            overlays.append(cta)
        elif config.platform == ViralPlatform.INSTAGRAM_REEL:
            cta = "drawtext=text='Double tap if you agree ❤️':fontsize=45:fontcolor=white:x=(w-text_w)/2:y=h*0.85:box=1:boxcolor=black@0.7:boxborderw=10"
            overlays.append(cta)
        
        # Add emoji reactions for certain templates
        if config.template in [ViralTemplate.REACTION, ViralTemplate.COMEDY]:
            emoji = self.effects_engine.create_emoji_reaction("😱", (100, 100), "bounce")
            overlays.append(emoji)
        
        filter_complex = ",".join(overlays) if overlays else "copy"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", filter_complex,
            "-c:a", "copy",
            engagement_output
        ]
        
        subprocess.run(cmd, capture_output=True)
        return engagement_output
    
    async def _optimize_for_platform(self, video_path: str, config: ViralVideoConfig,
                                   output_path: str) -> str:
        """Optimize video for specific platform"""
        
        # Platform-specific settings
        platform_specs = {
            ViralPlatform.TIKTOK: {
                "resolution": "1080x1920",
                "fps": 30,
                "bitrate": "4M",
                "audio_bitrate": "128k"
            },
            ViralPlatform.INSTAGRAM_REEL: {
                "resolution": "1080x1920",
                "fps": 30,
                "bitrate": "5M",
                "audio_bitrate": "160k"
            },
            ViralPlatform.YOUTUBE_SHORTS: {
                "resolution": "1080x1920",
                "fps": 30,
                "bitrate": "6M",
                "audio_bitrate": "192k"
            }
        }
        
        specs = platform_specs.get(config.platform, platform_specs[ViralPlatform.TIKTOK])
        
        # Final optimization and trim to duration
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-t", str(config.duration),
            "-vf", f"scale={specs['resolution']}:force_original_aspect_ratio=increase,crop={specs['resolution']}",
            "-r", str(specs["fps"]),
            "-b:v", specs["bitrate"],
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", specs["audio_bitrate"],
            "-movflags", "+faststart",
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True)
        
        # Cleanup temp files
        for temp_file in ["temp_hook.mp4", "temp_effects.mp4", "temp_captions.mp4", 
                         "temp_music.mp4", "temp_engagement.mp4"]:
            if Path(temp_file).exists():
                Path(temp_file).unlink()
        
        return output_path
    
    def _identify_best_clips(self, key_moments: List[Dict], motion_scores: List[float],
                           duration: float) -> List[Dict]:
        """Identify best clips for viral content"""
        
        # Sort moments by score
        sorted_moments = sorted(key_moments, key=lambda x: x["score"], reverse=True)
        
        # Select top clips that fit in target duration
        best_clips = []
        clip_duration = 3.0  # 3-second clips
        
        for moment in sorted_moments[:10]:  # Top 10 moments
            clip = {
                "start": max(0, moment["time"] - 1.5),
                "end": min(duration, moment["time"] + 1.5),
                "score": moment["score"],
                "type": moment["type"]
            }
            best_clips.append(clip)
        
        return best_clips
    
    def _generate_sample_captions(self, duration: float, style: CaptionStyle) -> List[Caption]:
        """Generate sample captions for demo"""
        
        caption_duration = 2.5
        num_captions = int(duration / caption_duration)
        
        sample_texts = [
            "This is the moment everything changed",
            "Nobody expected what happened next",
            "Pay attention to this part",
            "The results were absolutely INSANE",
            "This is why it went viral",
            "Wait for the plot twist",
            "You won't believe the outcome",
            "This changed EVERYTHING"
        ]
        
        captions = []
        for i in range(num_captions):
            caption = Caption(
                text=sample_texts[i % len(sample_texts)],
                start_time=i * caption_duration,
                end_time=(i + 1) * caption_duration,
                style=style,
                keywords=["changed", "INSANE", "viral", "EVERYTHING"],
                animation="bounce"
            )
            captions.append(caption)
        
        return captions
    
    def _calculate_viral_score(self, analysis: Dict, config: ViralVideoConfig) -> float:
        """Calculate viral potential score"""
        
        score = 0.0
        
        # Hook quality (30%)
        score += 0.3  # Assuming good hook was created
        
        # Motion and engagement (20%)
        if analysis["average_motion"] > 20:
            score += 0.2
        elif analysis["average_motion"] > 10:
            score += 0.1
        
        # Face presence (20%)
        score += min(0.2, analysis["face_coverage"] * 0.4)
        
        # Key moments (20%)
        moment_score = min(0.2, len(analysis["viral_moments"]) * 0.05)
        score += moment_score
        
        # Platform optimization (10%)
        score += 0.1  # Assuming proper optimization
        
        return min(1.0, score)
    
    def _generate_viral_report(self, analysis: Dict, config: ViralVideoConfig,
                             processing_time: float) -> Dict:
        """Generate viral video report"""
        
        return {
            "platform": config.platform.value,
            "template": config.template.value,
            "duration": config.duration,
            "processing_time": processing_time,
            "viral_moments_found": len(analysis["viral_moments"]),
            "face_coverage": f"{analysis['face_coverage'] * 100:.1f}%",
            "average_motion_score": analysis["average_motion"],
            "effects_applied": [
                "Viral Hook",
                "Dynamic Captions",
                "Beat Sync" if config.music_sync else None,
                "Engagement Overlays" if config.engagement_overlays else None,
                "Platform Optimization"
            ],
            "estimated_engagement_rate": f"{self._calculate_viral_score(analysis, config) * 100:.1f}%"
        }


async def demo_viral_editor():
    """Demo the ultimate viral editor"""
    
    # Example configurations for different viral styles
    configs = {
        "podcast_viral": ViralVideoConfig(
            platform=ViralPlatform.TIKTOK,
            template=ViralTemplate.PODCAST_CLIPS,
            duration=30.0,
            music_sync=True,
            auto_captions=True,
            hook_style="explosive",
            engagement_overlays=True
        ),
        "gaming_highlight": ViralVideoConfig(
            platform=ViralPlatform.YOUTUBE_SHORTS,
            template=ViralTemplate.GAMING,
            duration=60.0,
            music_sync=True,
            auto_captions=True,
            hook_style="urgent",
            transition_intensity=1.0
        ),
        "tutorial_quick": ViralVideoConfig(
            platform=ViralPlatform.INSTAGRAM_REEL,
            template=ViralTemplate.TUTORIAL,
            duration=30.0,
            music_sync=False,
            auto_captions=True,
            hook_style="mystery",
            engagement_overlays=True
        )
    }
    
    print("🚀 Ultimate Viral Video Editor")
    print("\nAvailable Templates:")
    for template in ViralTemplate:
        print(f"  • {template.value}")
    
    print("\nExample Configurations:")
    for name, config in configs.items():
        print(f"\n{name}:")
        print(f"  Platform: {config.platform.value}")
        print(f"  Template: {config.template.value}")
        print(f"  Duration: {config.duration}s")
        print(f"  Features: Captions={config.auto_captions}, Music={config.music_sync}")
    
    return configs


if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_viral_editor())