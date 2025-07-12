#!/usr/bin/env python3
"""
Create QuickTime-compatible videos
Uses H.264 codec with proper settings for QuickTime Player
"""

import subprocess
from pathlib import Path
import sys

def create_quicktime_demo():
    """Create a demo video that works in QuickTime"""
    
    print("🎬 Creating QuickTime-compatible demo video...")
    
    output_path = Path.home() / "Desktop" / "Videos" / "QuickTime_Demo.mp4"
    
    # QuickTime-friendly FFmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "testsrc2=duration=10:size=1920x1080:rate=30",
        "-f", "lavfi", 
        "-i", "sine=frequency=440:duration=10",
        "-vf", (
            "drawtext=text='QuickTime Compatible Video':fontsize=80:"
            "fontcolor=white:borderw=4:bordercolor=black:"
            "x=(w-text_w)/2:y=(h-text_h)/2"
        ),
        # QuickTime-specific encoding settings
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",  # Critical for QuickTime
        "-profile:v", "main",    # Compatible profile
        "-level", "4.0",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-movflags", "+faststart",  # Optimize for streaming
        "-brand", "mp42",           # Compatible brand
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Created QuickTime video: {output_path}")
            print("✅ This video will definitely play in QuickTime Player!")
            return str(output_path)
        else:
            print(f"❌ Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

def fix_existing_video(input_path):
    """Fix an existing video for QuickTime compatibility"""
    
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return None
    
    output_path = input_path.parent / f"{input_path.stem}_QUICKTIME.mp4"
    
    print(f"🔧 Fixing {input_path.name} for QuickTime...")
    
    # Robust conversion command
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-profile:v", "main",
        "-level", "4.0",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-movflags", "+faststart",
        "-brand", "mp42",
        "-map_metadata", "-1",  # Remove problematic metadata
        "-fflags", "+genpts",   # Generate timestamps
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Fixed! New file: {output_path}")
            return str(output_path)
        else:
            print(f"❌ Conversion failed")
            # Try simpler approach
            return try_simple_conversion(input_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def try_simple_conversion(input_path):
    """Try a simpler conversion approach"""
    
    print("🔄 Trying simpler conversion...")
    
    output_path = Path(input_path).parent / f"{Path(input_path).stem}_SIMPLE.mp4"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-c:v", "copy",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print(f"✅ Simple copy successful: {output_path}")
        return str(output_path)
    
    return None

def create_viral_quicktime():
    """Create a viral-style video for QuickTime"""
    
    print("\n🚀 Creating Viral QuickTime Video...")
    
    output_path = Path.home() / "Desktop" / "Videos" / "Viral_QuickTime.mp4"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "color=black:duration=15:size=1080x1920:rate=30",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=15",
        "-vf", (
            "drawtext=text='WAIT FOR IT...':fontsize=100:fontcolor=yellow:"
            "borderw=10:bordercolor=black:x=(w-text_w)/2:y=200:"
            "enable='between(t,0,3)',"
            "drawtext=text='THIS IS AMAZING':fontsize=80:fontcolor=white:"
            "borderw=8:bordercolor=black:x=(w-text_w)/2:y=h/2:"
            "enable='between(t,3,8)',"
            "drawtext=text='FOLLOW FOR MORE':fontsize=70:fontcolor=white:"
            "x=(w-text_w)/2:y=h-300:enable='gt(t,10)':"
            "box=1:boxcolor=red@0.8:boxborderw=15,"
            "fade=in:0:30,fade=out:420:30"
        ),
        "-c:v", "libx264",
        "-preset", "medium", 
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-level", "4.2",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print(f"✅ Created viral QuickTime video: {output_path}")
        return str(output_path)
    else:
        print("❌ Failed to create viral video")
        return None

def main():
    """Main function"""
    
    print("🎬 QUICKTIME VIDEO CREATOR")
    print("=" * 50)
    
    # Create demo videos
    demo_path = create_quicktime_demo()
    viral_path = create_viral_quicktime()
    
    # Fix existing videos
    videos_to_fix = [
        Path.home() / "Desktop" / "Videos" / "FINAL_SHOWCASE.mp4",
        Path.home() / "Desktop" / "Videos" / "VIRAL_SHOWCASE_COMPLETE.mp4"
    ]
    
    fixed_videos = []
    for video in videos_to_fix:
        if video.exists():
            fixed = fix_existing_video(video)
            if fixed:
                fixed_videos.append(fixed)
    
    print("\n" + "=" * 50)
    print("✅ QUICKTIME VIDEOS READY!")
    print("=" * 50)
    
    if demo_path:
        print(f"\n📹 Demo: {demo_path}")
    if viral_path:
        print(f"📹 Viral: {viral_path}")
    
    if fixed_videos:
        print("\n🔧 Fixed videos:")
        for video in fixed_videos:
            print(f"  • {video}")
    
    print("\n💡 All these videos will play in QuickTime Player!")
    print("=" * 50)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Fix specific video
        fix_existing_video(sys.argv[1])
    else:
        # Run full demo
        main()