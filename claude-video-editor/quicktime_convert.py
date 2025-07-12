#!/usr/bin/env python3
"""
Convert videos to QuickTime-compatible format
QuickTime prefers H.264 codec with AAC audio
"""

import subprocess
import sys
from pathlib import Path

def convert_to_quicktime(input_path, output_path=None):
    """Convert video to QuickTime-compatible format"""
    
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        return False
    
    if output_path is None:
        output_path = input_path.with_stem(f"{input_path.stem}_quicktime")
    
    print(f"Converting {input_path} to QuickTime format...")
    
    # QuickTime-compatible settings
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-c:v", "libx264",        # H.264 codec
        "-preset", "slow",        # Better quality
        "-crf", "20",            # High quality (lower = better)
        "-pix_fmt", "yuv420p",   # Compatibility pixel format
        "-c:a", "aac",           # AAC audio codec
        "-b:a", "192k",          # Audio bitrate
        "-movflags", "+faststart", # Better streaming
        "-vf", "format=yuv420p",  # Ensure compatibility
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully converted to: {output_path}")
            print(f"✅ This video will play in QuickTime Player")
            return True
        else:
            print(f"❌ Conversion failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def batch_convert(directory):
    """Convert all videos in a directory"""
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    videos = []
    
    for ext in video_extensions:
        videos.extend(Path(directory).glob(f"*{ext}"))
    
    print(f"Found {len(videos)} videos to convert")
    
    for video in videos:
        output = video.with_stem(f"{video.stem}_qt")
        convert_to_quicktime(video, output)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if Path(path).is_dir():
            batch_convert(path)
        else:
            convert_to_quicktime(path)
    else:
        print("Usage: python quicktime_convert.py <video_file_or_directory>")
