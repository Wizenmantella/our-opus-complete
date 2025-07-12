#!/usr/bin/env python3
"""
Simple Viral Content Creator - Creates viral edits that actually work
"""

import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List
import random

class SimpleViralCreator:
    """Creates viral content with proven techniques"""
    
    def __init__(self):
        self.output_dir = Path("viral_showcase")
        self.output_dir.mkdir(exist_ok=True)
        
        # Viral hooks that work
        self.hooks = [
            "WAIT FOR IT...",
            "THIS CHANGED EVERYTHING",
            "NOBODY EXPECTED THIS",
            "THE SECRET REVEALED",
            "WATCH TILL THE END"
        ]
        
        self.captions = [
            "This is incredible",
            "I can't believe this",
            "Pay attention here",
            "The results are insane",
            "Try this yourself"
        ]
    
    def create_viral_content(self, input_video: str) -> Dict[str, str]:
        """Create viral content for all platforms"""
        
        print("🚀 VIRAL CONTENT CREATOR")
        print("=" * 50)
        
        results = {}
        
        # Create viral versions
        print("\n1️⃣ Creating TikTok Viral Edit...")
        results["tiktok"] = self.create_tiktok_edit(input_video)
        
        print("\n2️⃣ Creating Instagram Reel...")
        results["instagram"] = self.create_instagram_reel(input_video)
        
        print("\n3️⃣ Creating YouTube Shorts...")
        results["youtube"] = self.create_youtube_shorts(input_video)
        
        print("\n4️⃣ Creating Ultimate Showcase...")
        results["showcase"] = self.create_final_showcase(results)
        
        print("\n✅ COMPLETE!")
        return results
    
    def create_tiktok_edit(self, input_video: str) -> str:
        """Create TikTok viral edit"""
        
        output = self.output_dir / "tiktok_viral.mp4"
        hook = random.choice(self.hooks)
        
        # Create filter for TikTok
        filters = []
        
        # 1. Crop to 9:16
        filters.append("crop=ih*9/16:ih")
        
        # 2. Add hook text
        filters.append(
            f"drawtext=text='{hook}':fontsize=80:fontcolor=yellow:"
            f"borderw=8:bordercolor=black:x=(w-text_w)/2:y=h*0.1:"
            f"enable='between(t,0,3)'"
        )
        
        # 3. Add captions
        for i, caption in enumerate(self.captions[:3]):
            start_time = 3 + i * 4
            filters.append(
                f"drawtext=text='{caption}':fontsize=60:fontcolor=white:"
                f"borderw=4:bordercolor=black:x=(w-text_w)/2:y=h*0.8:"
                f"enable='between(t,{start_time},{start_time+3})'"
            )
        
        # 4. Add zoom effect
        filters.append("scale=iw*1.1:ih*1.1,crop=iw/1.1:ih/1.1")
        
        # 5. Add engagement CTA
        filters.append(
            "drawtext=text='Follow for Part 2':fontsize=50:fontcolor=white:"
            "x=(w-text_w)/2:y=h*0.9:enable='gt(t,12)':"
            "box=1:boxcolor=red@0.8:boxborderw=10"
        )
        
        filter_str = ",".join(filters)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-t", "15",
            "-vf", filter_str,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            str(output)
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            print(f"✅ Created: {output}")
        else:
            print(f"⚠️ Error: {result.stderr.decode()[:200]}")
        
        return str(output)
    
    def create_instagram_reel(self, input_video: str) -> str:
        """Create Instagram Reel"""
        
        output = self.output_dir / "instagram_reel.mp4"
        
        filters = []
        
        # 1. Format for Instagram
        filters.append("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")
        
        # 2. Color enhancement
        filters.append("eq=saturation=1.2:brightness=0.05:contrast=1.1")
        
        # 3. Title text
        filters.append(
            "drawtext=text='THE TRUTH REVEALED':fontsize=70:fontcolor=white:"
            "borderw=6:bordercolor=black:x=(w-text_w)/2:y=h*0.1:"
            "enable='between(t,0,3)'"
        )
        
        # 4. Captions with emojis
        emoji_captions = [
            "This is amazing 🔥",
            "Watch carefully 👀", 
            "Mind = Blown 🤯",
            "Try this now 💪",
            "Share if helpful ❤️"
        ]
        
        for i, caption in enumerate(emoji_captions):
            start_time = 3 + i * 5
            filters.append(
                f"drawtext=text='{caption}':fontsize=50:fontcolor=white:"
                f"borderw=3:bordercolor=black:x=(w-text_w)/2:y=h*0.85:"
                f"enable='between(t,{start_time},{start_time+4})'"
            )
        
        # 5. Progress bar
        filters.append(
            "drawbox=x=0:y=h-10:w='w*t/30':h=10:color=purple@0.8:t=fill"
        )
        
        filter_str = ",".join(filters)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-t", "30", 
            "-vf", filter_str,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            str(output)
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            print(f"✅ Created: {output}")
        else:
            print(f"⚠️ Error: {result.stderr.decode()[:200]}")
        
        return str(output)
    
    def create_youtube_shorts(self, input_video: str) -> str:
        """Create YouTube Shorts"""
        
        output = self.output_dir / "youtube_shorts.mp4"
        
        filters = []
        
        # 1. Format for Shorts
        filters.append("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")
        
        # 2. MrBeast style title
        filters.append(
            "drawtext=text='$1000 SECRET REVEALED':fontsize=90:fontcolor=yellow:"
            "borderw=10:bordercolor=black:x=(w-text_w)/2:y=h*0.1:"
            "enable='between(t,0,3)'"
        )
        
        # 3. Chapter markers
        chapters = ["THE SETUP", "THE SECRET", "THE RESULTS"]
        for i, chapter in enumerate(chapters):
            start_time = i * 15
            filters.append(
                f"drawtext=text='{chapter}':fontsize=40:fontcolor=white:"
                f"x=50:y=50:enable='between(t,{start_time},{start_time+2})':"
                f"box=1:boxcolor=black@0.7:boxborderw=5"
            )
        
        # 4. Subscribe reminder
        filters.append(
            "drawtext=text='SUBSCRIBE FOR MORE':fontsize=60:fontcolor=white:"
            "x=(w-text_w)/2:y=h*0.5:enable='gt(t,40)':"
            "box=1:boxcolor=red@0.9:boxborderw=15"
        )
        
        filter_str = ",".join(filters)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-t", "45",
            "-vf", filter_str,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            str(output)
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            print(f"✅ Created: {output}")
        else:
            print(f"⚠️ Error: {result.stderr.decode()[:200]}")
        
        return str(output)
    
    def create_final_showcase(self, videos: Dict[str, str]) -> str:
        """Create final showcase combining all edits"""
        
        output = self.output_dir / "VIRAL_SHOWCASE_FINAL.mp4"
        
        # Create intro
        intro_path = self.output_dir / "intro.mp4"
        intro_cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=black:duration=3:size=1920x1080:rate=30",
            "-vf", "drawtext=text='VIRAL CONTENT SHOWCASE':fontsize=80:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264", "-preset", "fast",
            str(intro_path)
        ]
        subprocess.run(intro_cmd, capture_output=True)
        
        # Create platform title cards
        existing_videos = []
        
        for platform, video_path in videos.items():
            if platform != "showcase" and Path(video_path).exists():
                # Create title card
                title_path = self.output_dir / f"{platform}_title.mp4"
                title_cmd = [
                    "ffmpeg", "-y",
                    "-f", "lavfi", "-i", "color=blue:duration=2:size=1920x1080:rate=30",
                    "-vf", f"drawtext=text='{platform.upper()}':fontsize=100:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
                    "-c:v", "libx264", "-preset", "fast",
                    str(title_path)
                ]
                subprocess.run(title_cmd, capture_output=True)
                
                if Path(title_path).exists():
                    existing_videos.append(str(title_path))
                    existing_videos.append(video_path)
        
        if not existing_videos:
            print("⚠️ No videos to showcase")
            return str(output)
        
        # Create concat file
        concat_file = self.output_dir / "concat.txt"
        with open(concat_file, 'w') as f:
            if Path(intro_path).exists():
                f.write(f"file '{intro_path}'\n")
            for video in existing_videos:
                f.write(f"file '{video}'\n")
        
        # Concatenate
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(output)
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            print(f"✅ Final showcase: {output}")
        else:
            print(f"⚠️ Concat error: {result.stderr.decode()[:200]}")
        
        # Generate report
        self.generate_report(videos)
        
        return str(output)
    
    def generate_report(self, videos: Dict[str, str]):
        """Generate analytics report"""
        
        report = {
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "videos_created": list(videos.keys()),
            "techniques_used": [
                "Viral hooks",
                "Dynamic captions",
                "Platform optimization",
                "Color grading",
                "CTAs",
                "Progress indicators",
                "Emoji integration"
            ],
            "platforms": {
                "tiktok": {
                    "duration": "15s",
                    "format": "9:16 portrait",
                    "features": ["Hook text", "Zoom effect", "Follow CTA"]
                },
                "instagram": {
                    "duration": "30s", 
                    "format": "9:16 portrait",
                    "features": ["Color enhancement", "Emoji captions", "Progress bar"]
                },
                "youtube": {
                    "duration": "45s",
                    "format": "9:16 portrait", 
                    "features": ["MrBeast title", "Chapters", "Subscribe CTA"]
                }
            }
        }
        
        report_path = self.output_dir / "viral_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Report: {report_path}")


def main():
    """Run the viral content creator"""
    
    # Check for input video
    input_video = "raw_content.mp4"
    if not Path(input_video).exists():
        print("❌ No input video found")
        return
    
    # Create viral content
    creator = SimpleViralCreator()
    results = creator.create_viral_content(input_video)
    
    # Show results
    print("\n📁 Created files:")
    for name, path in results.items():
        if Path(path).exists():
            size = Path(path).stat().st_size / 1024 / 1024
            print(f"  • {name}: {Path(path).name} ({size:.1f} MB)")
    
    # Copy to desktop
    showcase_path = Path(results.get("showcase", ""))
    if showcase_path.exists():
        import shutil
        desktop = Path.home() / "Desktop" / "Videos" / "VIRAL_CONTENT_SHOWCASE.mp4"
        shutil.copy2(showcase_path, desktop)
        print(f"\n✅ Copied to: {desktop}")

if __name__ == "__main__":
    main()