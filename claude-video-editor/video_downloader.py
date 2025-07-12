#!/usr/bin/env python3
"""
Video Downloader Helper
Downloads videos from various platforms for processing
"""

import subprocess
import sys
from pathlib import Path
import re

def install_yt_dlp():
    """Install yt-dlp if not available"""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        print("✅ yt-dlp is already installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing yt-dlp...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
            print("✅ yt-dlp installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install yt-dlp")
            return False

def download_video(url: str, output_dir: str = "/Users/darriushart/Desktop/Video's") -> str:
    """Download video from URL"""
    
    if not install_yt_dlp():
        return None
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Extract video ID for filename
    video_id = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})', url)
    if video_id:
        filename = f"downloaded_video_{video_id.group(1)}.%(ext)s"
    else:
        filename = "downloaded_video.%(ext)s"
    
    output_template = str(output_path / filename)
    
    print(f"📥 Downloading video from: {url}")
    print(f"📁 Saving to: {output_path}")
    
    try:
        cmd = [
            "yt-dlp",
            "--format", "best[height<=720]",  # Limit to 720p for faster processing
            "--output", output_template,
            "--no-playlist",
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Find the downloaded file
            downloaded_files = list(output_path.glob("downloaded_video*"))
            if downloaded_files:
                downloaded_file = downloaded_files[-1]  # Get the most recent
                print(f"✅ Video downloaded: {downloaded_file}")
                return str(downloaded_file)
            else:
                print("❌ Downloaded file not found")
                return None
        else:
            print(f"❌ Download failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        return None

def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Download videos for editing")
    parser.add_argument("url", help="Video URL to download")
    parser.add_argument("-o", "--output-dir", default="/Users/darriushart/Desktop/Video's",
                       help="Output directory")
    
    args = parser.parse_args()
    
    downloaded_file = download_video(args.url, args.output_dir)
    
    if downloaded_file:
        print(f"\n🎬 Ready to edit! Run:")
        print(f"python3 instagram_reel_editor.py '{downloaded_file}'")
    else:
        print("\n❌ Download failed. Please try a different URL or method.")

if __name__ == "__main__":
    main()