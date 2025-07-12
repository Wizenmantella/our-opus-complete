#!/usr/bin/env python3
"""
Final Viral Demo - Working viral content creator
"""

import subprocess
import json
import time
from pathlib import Path
import shutil

def create_viral_edits():
    """Create viral edits for all platforms"""
    
    print("🚀 VIRAL CONTENT CREATOR - FINAL DEMO")
    print("=" * 50)
    
    input_video = "raw_content.mp4"
    output_dir = Path("viral_final")
    output_dir.mkdir(exist_ok=True)
    
    results = {}
    
    # 1. TikTok Edit (15 seconds, portrait)
    print("\n📱 Creating TikTok Viral Edit...")
    tiktok_output = output_dir / "tiktok_viral_final.mp4"
    
    tiktok_cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-t", "15",
        "-vf", (
            "crop=ih*9/16:ih,"  # Crop to 9:16
            "drawtext=text='WAIT FOR IT...':fontsize=80:fontcolor=yellow:"
            "borderw=8:bordercolor=black:x=(w-text_w)/2:y=100:"
            "enable='between(t,0,3)',"
            "drawtext=text='This is incredible':fontsize=60:fontcolor=white:"
            "borderw=4:bordercolor=black:x=(w-text_w)/2:y=h-200:"
            "enable='between(t,3,6)',"
            "drawtext=text='Follow for Part 2':fontsize=50:fontcolor=white:"
            "x=(w-text_w)/2:y=h-100:enable='gt(t,12)':"
            "box=1:boxcolor=red@0.8:boxborderw=10"
        ),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        str(tiktok_output)
    ]
    
    result = subprocess.run(tiktok_cmd, capture_output=True)
    if result.returncode == 0:
        print(f"✅ TikTok edit created: {tiktok_output}")
        results["tiktok"] = str(tiktok_output)
    else:
        print("⚠️ TikTok edit failed")
    
    # 2. Instagram Reel (30 seconds, portrait)
    print("\n📸 Creating Instagram Reel...")
    instagram_output = output_dir / "instagram_reel_final.mp4"
    
    instagram_cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-t", "30",
        "-vf", (
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "eq=saturation=1.2,"  # Instagram color boost
            "drawtext=text='THE TRUTH REVEALED':fontsize=70:fontcolor=white:"
            "borderw=6:bordercolor=black:x=(w-text_w)/2:y=100:"
            "enable='between(t,0,3)',"
            "drawtext=text='Share if this helped':fontsize=50:fontcolor=white:"
            "borderw=3:bordercolor=black:x=(w-text_w)/2:y=h-150:"
            "enable='gt(t,25)',"
            "drawbox=x=0:y=h-10:w=w*t/30:h=10:color=purple@0.8:t=fill"  # Progress bar
        ),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        str(instagram_output)
    ]
    
    result = subprocess.run(instagram_cmd, capture_output=True)
    if result.returncode == 0:
        print(f"✅ Instagram Reel created: {instagram_output}")
        results["instagram"] = str(instagram_output)
    else:
        print("⚠️ Instagram Reel failed")
    
    # 3. YouTube Shorts (45 seconds, portrait)
    print("\n📺 Creating YouTube Shorts...")
    youtube_output = output_dir / "youtube_shorts_final.mp4"
    
    youtube_cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-t", "45",
        "-vf", (
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "drawtext=text='THE $1000 SECRET':fontsize=90:fontcolor=yellow:"
            "borderw=10:bordercolor=black:x=(w-text_w)/2:y=100:"
            "enable='between(t,0,3)',"
            "drawtext=text='SUBSCRIBE':fontsize=60:fontcolor=white:"
            "x=(w-text_w)/2:y=h/2:enable='gt(t,40)':"
            "box=1:boxcolor=red@0.9:boxborderw=15"
        ),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        str(youtube_output)
    ]
    
    result = subprocess.run(youtube_cmd, capture_output=True)
    if result.returncode == 0:
        print(f"✅ YouTube Shorts created: {youtube_output}")
        results["youtube"] = str(youtube_output)
    else:
        print("⚠️ YouTube Shorts failed")
    
    # 4. Side-by-side comparison
    print("\n🎬 Creating Viral Showcase...")
    showcase_output = output_dir / "VIRAL_SHOWCASE_COMPLETE.mp4"
    
    # Create a side-by-side comparison if we have at least 2 videos
    existing_videos = [v for v in results.values() if Path(v).exists()]
    
    if len(existing_videos) >= 2:
        # Use first two videos for side-by-side
        showcase_cmd = [
            "ffmpeg", "-y",
            "-i", existing_videos[0],
            "-i", existing_videos[1],
            "-filter_complex", (
                "[0:v]scale=960:1080[v0];"
                "[1:v]scale=960:1080[v1];"
                "[v0][v1]hstack=inputs=2[v];"
                "color=black:s=1920x200[title];"
                "[title]drawtext=text='VIRAL CONTENT SHOWCASE':"
                "fontsize=80:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2[title_text];"
                "[title_text][v]vstack=inputs=2"
            ),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-t", "15",
            str(showcase_output)
        ]
        
        result = subprocess.run(showcase_cmd, capture_output=True)
        if result.returncode == 0:
            print(f"✅ Showcase created: {showcase_output}")
            results["showcase"] = str(showcase_output)
        else:
            print("⚠️ Showcase creation failed")
    
    # 5. Generate report
    print("\n📊 Generating Report...")
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "videos_created": list(results.keys()),
        "viral_techniques": [
            "Hook text optimization",
            "Platform-specific formatting",
            "Call-to-action overlays",
            "Color grading",
            "Progress indicators",
            "Engagement prompts"
        ],
        "platforms": {
            "tiktok": {
                "duration": "15s",
                "format": "9:16 (1080x1920)",
                "hook": "WAIT FOR IT...",
                "cta": "Follow for Part 2"
            },
            "instagram": {
                "duration": "30s",
                "format": "9:16 (1080x1920)",
                "hook": "THE TRUTH REVEALED",
                "features": ["Color boost", "Progress bar"]
            },
            "youtube": {
                "duration": "45s",
                "format": "9:16 (1080x1920)",
                "hook": "THE $1000 SECRET",
                "cta": "SUBSCRIBE"
            }
        }
    }
    
    report_path = output_dir / "viral_analytics.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # 6. Copy to Desktop
    if "showcase" in results and Path(results["showcase"]).exists():
        desktop_path = Path.home() / "Desktop" / "Videos" / "VIRAL_CONTENT_FINAL.mp4"
        shutil.copy2(results["showcase"], desktop_path)
        print(f"\n✅ Showcase copied to: {desktop_path}")
    
    # Show summary
    print("\n" + "=" * 50)
    print("📁 CREATED FILES:")
    for name, path in results.items():
        if Path(path).exists():
            size = Path(path).stat().st_size / 1024 / 1024
            print(f"  • {name}: {size:.1f} MB")
    
    print(f"\n📊 Report: {report_path}")
    print("=" * 50)
    
    return results

if __name__ == "__main__":
    # Check for input
    if not Path("raw_content.mp4").exists():
        print("❌ Please run create_real_demo_video.py first")
    else:
        create_viral_edits()