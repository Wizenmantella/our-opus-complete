#!/usr/bin/env python3
"""
Complete Installation Script - Install everything needed for the AI Video Editor
This script installs all dependencies and fixes video compatibility issues
"""

import subprocess
import sys
import os
from pathlib import Path
import platform

class CompleteInstaller:
    def __init__(self):
        self.system = platform.system()
        self.is_mac = self.system == "Darwin"
        self.errors = []
        self.installed = []
        
    def run(self):
        """Run complete installation"""
        print("🚀 AI VIDEO EDITOR - COMPLETE INSTALLATION")
        print("=" * 60)
        print(f"System: {self.system}")
        print(f"Python: {sys.version}")
        print("=" * 60)
        
        # 1. Check and install Homebrew (macOS)
        if self.is_mac:
            print("\n📦 Checking Homebrew...")
            self.install_homebrew()
        
        # 2. Install system dependencies
        print("\n🔧 Installing System Dependencies...")
        self.install_system_deps()
        
        # 3. Install Python dependencies
        print("\n🐍 Installing Python Dependencies...")
        self.install_python_deps()
        
        # 4. Create QuickTime-compatible conversion script
        print("\n🎬 Creating QuickTime Compatibility Tools...")
        self.create_quicktime_tools()
        
        # 5. Summary
        self.print_summary()
    
    def install_homebrew(self):
        """Install Homebrew if not present"""
        try:
            result = subprocess.run(["brew", "--version"], capture_output=True)
            if result.returncode == 0:
                print("✅ Homebrew already installed")
                self.installed.append("Homebrew")
            else:
                raise FileNotFoundError
        except:
            print("📥 Installing Homebrew...")
            install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            print(f"Please run this command in Terminal:\n{install_cmd}")
            self.errors.append("Homebrew needs manual installation")
    
    def install_system_deps(self):
        """Install system dependencies"""
        if self.is_mac:
            deps = [
                ("ffmpeg", "FFmpeg - Video processing"),
                ("opencv", "OpenCV - Computer vision"),
                ("pkg-config", "Package configuration"),
                ("cairo", "Cairo - Graphics library"),
                ("pango", "Pango - Text rendering"),
                ("gdk-pixbuf", "Image loading"),
                ("libffi", "Foreign function interface"),
                ("imagemagick", "Image manipulation"),
                ("gifsicle", "GIF optimization"),
                ("wget", "File downloader")
            ]
            
            for dep, desc in deps:
                print(f"\n📦 Installing {desc}...")
                try:
                    # Check if already installed
                    check = subprocess.run(["brew", "list", dep], capture_output=True)
                    if check.returncode == 0:
                        print(f"✅ {dep} already installed")
                        self.installed.append(dep)
                    else:
                        # Install
                        result = subprocess.run(["brew", "install", dep], capture_output=True, text=True)
                        if result.returncode == 0:
                            print(f"✅ {dep} installed successfully")
                            self.installed.append(dep)
                        else:
                            print(f"⚠️ Failed to install {dep}")
                            self.errors.append(f"{dep}: {result.stderr}")
                except Exception as e:
                    print(f"⚠️ Error installing {dep}: {e}")
                    self.errors.append(f"{dep}: {str(e)}")
    
    def install_python_deps(self):
        """Install Python dependencies"""
        
        # Core dependencies
        core_deps = [
            "numpy>=1.21.0",
            "opencv-python>=4.5.0",
            "opencv-contrib-python>=4.5.0",
            "Pillow>=9.0.0",
            "moviepy>=1.0.3",
            "imageio>=2.9.0",
            "imageio-ffmpeg>=0.4.5",
            "scipy>=1.7.0",
            "scikit-image>=0.18.0",
            "matplotlib>=3.5.0",
            "tqdm>=4.62.0"
        ]
        
        # AI/ML dependencies
        ai_deps = [
            "torch>=2.0.0",
            "torchvision>=0.15.0",
            "transformers>=4.25.0",
            "sentence-transformers>=2.2.0",
            "openai-whisper",
            "stable-baselines3>=1.6.0"
        ]
        
        # Audio processing
        audio_deps = [
            "librosa>=0.9.0",
            "soundfile>=0.10.0",
            "pydub>=0.25.0",
            "pyaudio>=0.2.11",
            "wave",
            "pedalboard>=0.6.0"
        ]
        
        # Video analysis
        video_deps = [
            "vidstab>=1.7.0",
            "imutils>=0.5.0",
            "dlib>=19.22.0",
            "face-recognition>=1.3.0",
            "mediapipe>=0.9.0"
        ]
        
        # Utilities
        util_deps = [
            "requests>=2.26.0",
            "aiohttp>=3.8.0",
            "asyncio",
            "python-dotenv>=0.19.0",
            "pyyaml>=6.0",
            "colorama>=0.4.0",
            "rich>=12.0.0",
            "click>=8.0.0",
            "typer>=0.4.0"
        ]
        
        all_deps = core_deps + audio_deps + util_deps
        
        print("\n📦 Installing Python packages...")
        
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True)
        
        for dep in all_deps:
            print(f"Installing {dep}...")
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    self.installed.append(dep)
                else:
                    print(f"⚠️ Failed to install {dep}")
                    self.errors.append(f"{dep}: {result.stderr}")
            except Exception as e:
                print(f"⚠️ Error installing {dep}: {e}")
                self.errors.append(f"{dep}: {str(e)}")
        
        # Install AI dependencies separately (they're large)
        print("\n🤖 Installing AI dependencies (this may take a while)...")
        for dep in ai_deps:
            print(f"Installing {dep}...")
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    self.installed.append(dep)
            except subprocess.TimeoutExpired:
                print(f"⚠️ {dep} installation timed out (continuing...)")
            except Exception as e:
                print(f"⚠️ Skipping {dep}: {e}")
    
    def create_quicktime_tools(self):
        """Create QuickTime compatibility tools"""
        
        # Create conversion script
        convert_script = '''#!/usr/bin/env python3
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
'''
        
        # Save conversion script
        convert_path = Path("quicktime_convert.py")
        with open(convert_path, 'w') as f:
            f.write(convert_script)
        
        os.chmod(convert_path, 0o755)
        print(f"✅ Created QuickTime conversion tool: {convert_path}")
        
        # Create fix script for existing videos
        fix_script = '''#!/bin/bash
# Fix all videos for QuickTime compatibility

echo "🎬 Converting all videos to QuickTime format..."

# Convert showcase videos
for video in showcase_output/*.mp4 viral_showcase/*.mp4 viral_final/*.mp4; do
    if [ -f "$video" ]; then
        echo "Converting $video..."
        python3 quicktime_convert.py "$video"
    fi
done

# Convert desktop videos
for video in ~/Desktop/Videos/*.mp4; do
    if [ -f "$video" ]; then
        echo "Converting $video..."
        python3 quicktime_convert.py "$video"
    fi
done

echo "✅ Conversion complete!"
'''
        
        fix_path = Path("fix_all_videos.sh")
        with open(fix_path, 'w') as f:
            f.write(fix_script)
        
        os.chmod(fix_path, 0o755)
        print(f"✅ Created batch fix script: {fix_path}")
    
    def print_summary(self):
        """Print installation summary"""
        
        print("\n" + "=" * 60)
        print("📊 INSTALLATION SUMMARY")
        print("=" * 60)
        
        print(f"\n✅ Successfully installed: {len(self.installed)} packages")
        for item in self.installed[:10]:  # Show first 10
            print(f"  • {item}")
        if len(self.installed) > 10:
            print(f"  ... and {len(self.installed) - 10} more")
        
        if self.errors:
            print(f"\n⚠️ Errors encountered: {len(self.errors)}")
            for error in self.errors[:5]:
                print(f"  • {error}")
        
        print("\n🎬 QUICKTIME COMPATIBILITY")
        print("-" * 40)
        print("To fix videos for QuickTime Player:")
        print("1. Single video: python3 quicktime_convert.py <video.mp4>")
        print("2. All videos:  bash fix_all_videos.sh")
        
        print("\n📝 NEXT STEPS")
        print("-" * 40)
        print("1. Convert existing videos for QuickTime:")
        print("   python3 quicktime_convert.py ~/Desktop/Videos/")
        print("\n2. Install any missing system dependencies:")
        print("   brew install ffmpeg opencv")
        print("\n3. For AI features, install PyTorch:")
        print("   pip3 install torch torchvision")
        
        print("\n✅ Installation complete!")
        print("=" * 60)

def main():
    """Run the installer"""
    installer = CompleteInstaller()
    installer.run()

if __name__ == "__main__":
    main()