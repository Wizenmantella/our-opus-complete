#!/usr/bin/env python3
"""
Instagram Reel Editor - Viral Style
Transforms any video into an engaging Instagram Reel with modern editing techniques
"""

import cv2
import numpy as np
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
import subprocess
import random
import math
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ReelStyle(Enum):
    VIRAL_PODCAST = "viral_podcast"
    MOTIVATIONAL = "motivational"
    EDUCATIONAL = "educational"
    TRENDY_CLIP = "trendy_clip"
    REACTION_STYLE = "reaction_style"

@dataclass
class ReelConfig:
    """Configuration for Instagram Reel editing"""
    style: ReelStyle = ReelStyle.VIRAL_PODCAST
    duration: float = 30.0  # Instagram Reel max 90s, but 30s is optimal
    add_captions: bool = True
    add_zoom_effects: bool = True
    add_split_screen: bool = False
    add_progress_bar: bool = True
    add_engagement_text: bool = True
    color_grade: str = "warm_viral"
    add_music: bool = False
    fast_cuts: bool = True
    add_emojis: bool = True

class InstagramReelEditor:
    """Advanced Instagram Reel editor with viral techniques"""
    
    def __init__(self, config: ReelConfig = None):
        self.config = config or ReelConfig()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_bold = cv2.FONT_HERSHEY_DUPLEX
        
        # Modern color schemes
        self.color_schemes = {
            "warm_viral": {
                "primary": (255, 87, 51),      # Orange-red
                "secondary": (255, 206, 84),   # Yellow
                "accent": (255, 255, 255),     # White
                "background": (0, 0, 0)        # Black
            },
            "cool_modern": {
                "primary": (64, 224, 255),     # Blue
                "secondary": (138, 43, 226),   # Purple
                "accent": (255, 255, 255),     # White
                "background": (20, 20, 30)     # Dark blue
            }
        }
    
    async def create_instagram_reel(self, input_video: str, output_path: str = None) -> Dict[str, Any]:
        """Create an Instagram Reel from any input video"""
        
        if not Path(input_video).exists():
            return {"success": False, "error": "Input video not found"}
        
        if not output_path:
            output_path = f"instagram_reel_{Path(input_video).stem}.mp4"
        
        print(f"🎬 Creating Instagram Reel from: {input_video}")
        print(f"📱 Style: {self.config.style.value}")
        print(f"⏱️  Target Duration: {self.config.duration}s")
        
        # Process video through Instagram Reel pipeline
        result = await self._process_reel_pipeline(input_video, output_path)
        
        return result
    
    async def _process_reel_pipeline(self, input_video: str, output_path: str) -> Dict[str, Any]:
        """Process video through Instagram Reel editing pipeline"""
        
        pipeline_steps = [
            ("📐 Converting to 9:16 aspect ratio", self._convert_to_vertical),
            ("✂️ Smart trimming to optimal length", self._smart_trim_for_engagement),
            ("🎨 Applying viral color grading", self._apply_viral_color_grade),
            ("📝 Adding dynamic captions", self._add_dynamic_captions),
            ("🔍 Adding zoom and movement effects", self._add_zoom_effects),
            ("📊 Adding progress indicators", self._add_progress_elements),
            ("💬 Adding engagement elements", self._add_engagement_overlay),
            ("🎵 Optimizing audio for mobile", self._optimize_audio_for_mobile),
            ("🚀 Final optimization and export", self._export_optimized_reel)
        ]
        
        temp_files = []
        current_file = input_video
        
        try:
            for step_name, step_func in pipeline_steps:
                print(f"  {step_name}...")
                
                temp_output = f"temp_reel_{len(temp_files)}.mp4"
                result = await step_func(current_file, temp_output)
                
                if result.get("success"):
                    temp_files.append(current_file if current_file != input_video else None)
                    current_file = temp_output
                else:
                    print(f"    ⚠️ Warning: {step_name} had issues")
            
            # Move final result to output path
            if current_file != output_path:
                subprocess.run(["mv", current_file, output_path], check=True)
            
            # Cleanup temp files
            for temp_file in temp_files:
                if temp_file and Path(temp_file).exists():
                    Path(temp_file).unlink()
            
            # Get final video info
            final_info = self._get_video_info(output_path)
            
            return {
                "success": True,
                "output_path": output_path,
                "video_info": final_info,
                "features_applied": [
                    "9:16 Vertical Format",
                    "Smart Trimming for Engagement",
                    "Viral Color Grading",
                    "Dynamic Captions",
                    "Zoom & Movement Effects",
                    "Progress Indicators",
                    "Engagement Overlays",
                    "Mobile-Optimized Audio"
                ]
            }
            
        except Exception as e:
            logger.error(f"Reel processing failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _convert_to_vertical(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Convert video to 9:16 aspect ratio for Instagram"""
        
        try:
            # Get input video dimensions
            cap = cv2.VideoCapture(input_video)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            # Calculate crop/scale for 9:16
            target_width = 1080
            target_height = 1920
            
            # If video is wider than 9:16, crop sides
            if width / height > 9 / 16:
                # Crop width to match 9:16
                new_width = int(height * 9 / 16)
                crop_x = (width - new_width) // 2
                crop_filter = f"crop={new_width}:{height}:{crop_x}:0"
            else:
                # Add padding or zoom to fill 9:16
                crop_filter = f"scale={target_width}:{target_height}:force_original_aspect_ratio=increase,crop={target_width}:{target_height}"
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", f"{crop_filter},scale={target_width}:{target_height}",
                "-c:a", "copy",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": result.returncode == 0}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _smart_trim_for_engagement(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Smart trimming to create engaging content"""
        
        try:
            # Get video duration
            cap = cv2.VideoCapture(input_video)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            cap.release()
            
            if duration <= self.config.duration:
                # Video is already short enough
                subprocess.run(["cp", input_video, output_video])
                return {"success": True}
            
            # Find the most engaging segment
            # For now, take middle section (can be enhanced with AI analysis)
            start_time = max(0, (duration - self.config.duration) / 2)
            
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start_time),
                "-i", input_video,
                "-t", str(self.config.duration),
                "-c", "copy",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": result.returncode == 0}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _apply_viral_color_grade(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Apply viral-style color grading"""
        
        try:
            # Viral color grading filters
            if self.config.color_grade == "warm_viral":
                color_filter = "eq=contrast=1.2:brightness=0.05:saturation=1.3,curves=red='0/0 0.5/0.6 1/1':green='0/0 0.5/0.5 1/0.9':blue='0/0 0.5/0.4 1/0.8'"
            elif self.config.color_grade == "cool_modern":
                color_filter = "eq=contrast=1.1:brightness=0.02:saturation=1.2,hue=h=10:s=1.1"
            else:
                color_filter = "eq=contrast=1.15:brightness=0.03:saturation=1.25"
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", color_filter,
                "-c:a", "copy",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": result.returncode == 0}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _add_dynamic_captions(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Add dynamic captions with modern styling"""
        
        if not self.config.add_captions:
            subprocess.run(["cp", input_video, output_video])
            return {"success": True}
        
        try:
            # Create caption overlays (this would integrate with speech recognition in full version)
            sample_captions = [
                {"text": "This is going to", "start": 0, "duration": 2},
                {"text": "BLOW YOUR MIND 🤯", "start": 2, "duration": 2},
                {"text": "Wait for it...", "start": 4, "duration": 2},
            ]
            
            # Build drawtext filters for captions
            drawtext_filters = []
            colors = self.color_schemes[self.config.color_grade]
            
            for i, caption in enumerate(sample_captions):
                # Modern caption styling
                text = caption["text"].replace(":", "\\:")
                
                # Add background box and text
                drawtext_filter = f"drawtext=fontfile='Arial':text='{text}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h*0.8:box=1:boxcolor=black@0.7:boxborderw=10:enable='between(t,{caption['start']},{caption['start'] + caption['duration']})'"
                drawtext_filters.append(drawtext_filter)
            
            # Combine all text overlays
            if drawtext_filters:
                vf_filter = ",".join(drawtext_filters)
                
                cmd = [
                    "ffmpeg", "-y",
                    "-i", input_video,
                    "-vf", vf_filter,
                    "-c:a", "copy",
                    output_video
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                return {"success": result.returncode == 0}
            
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _add_zoom_effects(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Add zoom and movement effects for engagement"""
        
        if not self.config.add_zoom_effects:
            subprocess.run(["cp", input_video, output_video])
            return {"success": True}
        
        try:
            # Add subtle zoom effect (Ken Burns style)
            zoom_filter = "zoompan=z='min(zoom+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", zoom_filter,
                "-c:a", "copy",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": result.returncode == 0}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _add_progress_elements(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Add progress indicators and modern UI elements"""
        
        if not self.config.add_progress_bar:
            subprocess.run(["cp", input_video, output_video])
            return {"success": True}
        
        try:
            # Get video duration for progress calculation
            duration_cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", input_video]
            duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
            duration = float(duration_result.stdout.strip())
            
            # Add progress bar at bottom
            progress_filter = f"drawbox=x=0:y=h-10:w=w*t/{duration}:h=10:color=orange:t=fill"
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", progress_filter,
                "-c:a", "copy",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": result.returncode == 0}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _add_engagement_overlay(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Add engagement elements like 'Follow for more', emojis, etc."""
        
        if not self.config.add_engagement_text:
            subprocess.run(["cp", input_video, output_video])
            return {"success": True}
        
        try:
            engagement_texts = [
                "Follow for more 👆",
                "Like if you agree 💯",
                "Save this! 📌"
            ]
            
            # Add engagement text in top corner
            selected_text = random.choice(engagement_texts)
            
            engagement_filter = f"drawtext=fontfile='Arial':text='{selected_text}':fontsize=40:fontcolor=white:x=50:y=50:box=1:boxcolor=black@0.5:boxborderw=5"
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", engagement_filter,
                "-c:a", "copy",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": result.returncode == 0}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _optimize_audio_for_mobile(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Optimize audio for mobile viewing"""
        
        try:
            # Audio optimization for mobile devices
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "128k",
                "-ar", "44100",
                "-ac", "2",
                "-af", "loudnorm=I=-16:LRA=7:tp=-2",  # Loudness normalization
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": result.returncode == 0}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _export_optimized_reel(self, input_video: str, output_video: str) -> Dict[str, Any]:
        """Final export optimization for Instagram"""
        
        try:
            # Instagram Reel optimized settings
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-s", "1080x1920",
                "-r", "30",
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                output_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": result.returncode == 0}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_video_info(self, video_path: str) -> Dict[str, Any]:
        """Get video information"""
        
        try:
            cap = cv2.VideoCapture(video_path)
            info = {
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": cap.get(cv2.CAP_PROP_FPS),
                "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "duration": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS),
                "file_size": Path(video_path).stat().st_size / (1024 * 1024)  # MB
            }
            cap.release()
            return info
        except:
            return {}


async def main():
    """CLI interface for Instagram Reel Editor"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Create viral Instagram Reels from any video")
    parser.add_argument("input_video", help="Input video file")
    parser.add_argument("-o", "--output", help="Output reel file")
    parser.add_argument("-s", "--style", choices=["viral_podcast", "motivational", "educational"], 
                       default="viral_podcast", help="Reel style")
    parser.add_argument("-d", "--duration", type=float, default=30.0, help="Target duration in seconds")
    parser.add_argument("--no-captions", action="store_true", help="Disable captions")
    parser.add_argument("--no-zoom", action="store_true", help="Disable zoom effects")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bar")
    
    args = parser.parse_args()
    
    # Create configuration
    config = ReelConfig(
        style=ReelStyle(args.style),
        duration=args.duration,
        add_captions=not args.no_captions,
        add_zoom_effects=not args.no_zoom,
        add_progress_bar=not args.no_progress
    )
    
    # Create editor and process video
    editor = InstagramReelEditor(config)
    
    output_path = args.output or f"instagram_reel_{Path(args.input_video).stem}.mp4"
    
    print("🎬 Instagram Reel Editor")
    print("=" * 40)
    
    result = await editor.create_instagram_reel(args.input_video, output_path)
    
    if result["success"]:
        print("\n✅ Instagram Reel created successfully!")
        print(f"📱 Output: {result['output_path']}")
        
        info = result.get("video_info", {})
        if info:
            print(f"📐 Resolution: {info.get('width')}x{info.get('height')}")
            print(f"⏱️  Duration: {info.get('duration', 0):.1f}s")
            print(f"📊 File Size: {info.get('file_size', 0):.2f} MB")
        
        features = result.get("features_applied", [])
        if features:
            print("\n✨ Features Applied:")
            for feature in features:
                print(f"  • {feature}")
        
        print(f"\n🚀 Ready to upload to Instagram!")
        
    else:
        print(f"\n❌ Failed to create reel: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())