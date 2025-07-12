# 🚀 Complete Installation Guide - AI Video Editor

## Overview
This guide will help you install **everything** needed to run the AI Video Editor, including system dependencies, Python packages, and QuickTime compatibility fixes.

## 📋 Prerequisites

### macOS (Required for this guide)
- macOS 10.15 or later
- Python 3.8+ (check with `python3 --version`)
- At least 10GB free disk space
- Admin access to install system packages

## 🛠️ Step 1: Install Homebrew (Package Manager)

Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, add Homebrew to your PATH:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## 📦 Step 2: Install System Dependencies

### Essential packages (REQUIRED):
```bash
# Video processing
brew install ffmpeg

# Computer vision
brew install opencv

# Build tools
brew install pkg-config cmake

# Graphics libraries
brew install cairo pango gdk-pixbuf

# Image processing
brew install imagemagick

# Audio processing (for pyaudio)
brew install portaudio

# Python development
brew install python@3.11
```

### Optional but recommended:
```bash
# Additional tools
brew install wget git gh
brew install gifsicle  # For GIF optimization
brew install youtube-dl  # For downloading videos
```

## 🐍 Step 3: Install Python Dependencies

### Create virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### Core dependencies:
```bash
pip install --upgrade pip setuptools wheel

# Essential packages
pip install numpy opencv-python opencv-contrib-python
pip install Pillow moviepy imageio imageio-ffmpeg
pip install scipy scikit-image matplotlib
pip install tqdm colorama rich click

# Audio processing
pip install librosa soundfile pydub
pip install pyaudio  # May need: CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install pyaudio

# Video analysis
pip install imutils

# Async and utilities
pip install aiohttp asyncio python-dotenv pyyaml
```

### AI/ML packages (optional, for advanced features):
```bash
# PyTorch (choose based on your system)
# For Mac with Apple Silicon:
pip install torch torchvision torchaudio

# For Intel Mac:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Other AI packages
pip install transformers sentence-transformers
pip install openai-whisper
```

## 🎬 Step 4: Fix QuickTime Compatibility

QuickTime Player requires specific video codecs. Use these settings when creating videos:

### FFmpeg settings for QuickTime:
```bash
-c:v libx264        # H.264 video codec
-pix_fmt yuv420p    # Compatible pixel format
-profile:v main     # Compatible profile
-level 4.0          # Compatible level
-c:a aac            # AAC audio codec
-movflags +faststart # Optimize for streaming
```

### Convert existing videos:
```bash
# Single video
python3 create_quicktime_video.py /path/to/video.mp4

# All videos in a directory
python3 quicktime_convert.py ~/Desktop/Videos/
```

## 🔧 Step 5: Verify Installation

### Check FFmpeg:
```bash
ffmpeg -version
# Should show version 6.0 or later
```

### Check Python packages:
```python
python3 -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
python3 -c "import moviepy; print('MoviePy: OK')"
python3 -c "import numpy; print(f'NumPy: {numpy.__version__}')"
```

### Test video creation:
```bash
# Create test video
python3 create_quicktime_video.py

# This creates videos in ~/Desktop/Videos/ that work in QuickTime
```

## 🚨 Troubleshooting

### Issue: "command not found: brew"
**Solution**: Homebrew not installed or not in PATH
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```

### Issue: "No module named cv2"
**Solution**: OpenCV not installed properly
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python opencv-contrib-python
```

### Issue: Videos won't play in QuickTime
**Solution**: Wrong codec or pixel format
```bash
# Use the QuickTime converter
python3 create_quicktime_video.py your_video.mp4
```

### Issue: PyAudio installation fails
**Solution**: Install portaudio first
```bash
brew install portaudio
CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install pyaudio
```

## 📝 Quick Start Commands

After installation, you can:

### 1. Create viral content:
```bash
python3 simple_viral_creator.py
```

### 2. Run showcase demo:
```bash
python3 simple_showcase_demo.py
```

### 3. Create QuickTime videos:
```bash
python3 create_quicktime_video.py
```

## 🎯 Complete Installation Script

Run this to install everything automatically:
```bash
python3 install_everything.py
```

## ✅ Installation Checklist

- [ ] Homebrew installed
- [ ] FFmpeg installed (`ffmpeg -version`)
- [ ] OpenCV installed (`brew list opencv`)
- [ ] Python packages installed (`pip list`)
- [ ] QuickTime converter working
- [ ] Test video plays in QuickTime Player

## 🔗 Useful Links

- [Homebrew](https://brew.sh)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [OpenCV Python](https://pypi.org/project/opencv-python/)
- [MoviePy Documentation](https://zulko.github.io/moviepy/)

## 💡 Tips

1. **Virtual Environment**: Always use a virtual environment to avoid conflicts
2. **FFmpeg Path**: Make sure FFmpeg is in your PATH: `which ffmpeg`
3. **QuickTime Codecs**: Always use H.264 video + AAC audio for compatibility
4. **Python Version**: Use Python 3.8+ for best compatibility

## 🎬 Next Steps

1. Test the installation by creating a simple video
2. Try the viral content creator
3. Experiment with different effects and filters
4. Check all videos play correctly in QuickTime Player

---

**Need help?** Check the error messages carefully - they usually indicate what's missing!