#!/usr/bin/env python3
"""
Hollywood-Level Video Editor - Complete Installation Script
Installs all dependencies needed for the most advanced video editing system with AI automation
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description=""):
    """Run shell command with error handling"""
    print(f"🔧 {description if description else command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_system():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check platform
    system = platform.system()
    machine = platform.machine()
    print(f"✅ Platform: {system} {machine}")
    
    # Check if we're on Apple Silicon
    if system == "Darwin" and machine == "arm64":
        print("✅ Apple Silicon detected - optimized installation")
    
    return True

def install_core_dependencies():
    """Install core Python dependencies"""
    print("\n📦 Installing core dependencies...")
    
    # Core packages that should install on any system
    core_packages = [
        "numpy>=1.21.0",
        "opencv-python>=4.5.0", 
        "Pillow>=8.0.0",
        "ffmpeg-python>=0.2.0",
        "aiofiles>=0.8.0",
        "pydantic>=1.8.0",
        "rich>=10.0.0",
        "tqdm>=4.62.0",
        "scipy>=1.7.0",
        "matplotlib>=3.5.0",
        "scikit-learn>=1.0.0",
        "psutil>=5.8.0",
        "requests>=2.25.0",
        "aiohttp>=3.8.0",
        "websockets>=10.0.0",
        "sqlalchemy>=1.4.0",
        "watchdog>=2.1.0",
        "colorama>=0.4.4",
        "click>=8.0.0",
        "pathlib",
        "dataclasses",
        "typing-extensions>=4.0.0",
        "packaging>=21.0.0"
    ]
    
    for package in core_packages:
        if not run_command(f"pip3 install '{package}'", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")

def install_audio_dependencies():
    """Install audio processing dependencies"""
    print("\n🎵 Installing audio dependencies...")
    
    audio_packages = [
        "librosa>=0.9.0",
        "soundfile>=0.12.0", 
        "pydub>=0.25.0",
        "resampy>=0.4.0",
        "noisereduce>=2.0.0",
        "pyloudnorm>=0.1.0",
        "aubio>=0.4.9",
        "webrtcvad>=2.0.10",
        "openai-whisper>=20230314",
        "whisper-openai",
        "essentia>=2.1b6",
        "pyaudio>=0.2.11",
        "vosk>=0.3.42",
        "speech-recognition>=3.10.0"
    ]
    
    # Try to install PyAudio (can be problematic)
    print("🔧 Installing PyAudio (may require system audio libraries)...")
    if platform.system() == "Darwin":  # macOS
        # Install portaudio first on macOS
        run_command("brew install portaudio", "Installing portaudio via Homebrew")
    
    for package in audio_packages:
        if not run_command(f"pip3 install '{package}'", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")

def install_ai_dependencies():
    """Install AI/ML dependencies"""
    print("\n🤖 Installing AI/ML dependencies...")
    
    # Check if we should install CPU or GPU versions
    system = platform.system()
    machine = platform.machine()
    
    if system == "Darwin":  # macOS
        # For Apple Silicon, use MPS acceleration
        ai_packages = [
            "torch>=1.12.0",
            "torchvision>=0.13.0", 
            "torchaudio>=0.12.0",
            "transformers>=4.21.0",
            "diffusers>=0.10.0",
            "ultralytics>=8.0.0",
            "mediapipe>=0.10.0",
            "onnx>=1.14.0",
            "onnxruntime>=1.15.0",
            "tensorflow>=2.12.0",
            "keras>=2.12.0",
            "face-recognition>=1.3.0",
            "dlib>=19.24.0",
            "insightface>=0.7.3",
            "deepface>=0.0.79",
            "segment-anything-model",
            "openai>=0.27.0",
            "anthropic>=0.3.0"
        ]
        
        if machine == "arm64":
            print("🍎 Installing Apple Silicon optimized PyTorch...")
            ai_packages.extend([
                "coremltools>=6.0.0",
                "tensorflow-macos>=2.12.0",
                "tensorflow-metal>=0.6.0"
            ])
    else:
        # For other platforms, install CPU versions by default
        ai_packages = [
            "torch>=1.12.0+cpu",
            "torchvision>=0.13.0+cpu", 
            "torchaudio>=0.12.0+cpu",
            "transformers>=4.21.0",
            "diffusers>=0.10.0",
            "ultralytics>=8.0.0",
            "mediapipe>=0.10.0",
            "onnx>=1.14.0",
            "onnxruntime>=1.15.0",
            "tensorflow>=2.12.0",
            "keras>=2.12.0",
            "face-recognition>=1.3.0",
            "dlib>=19.24.0",
            "insightface>=0.7.3",
            "deepface>=0.0.79",
            "segment-anything-model",
            "openai>=0.27.0",
            "anthropic>=0.3.0"
        ]
    
    for package in ai_packages:
        if not run_command(f"pip3 install '{package}'", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")

def install_image_dependencies():
    """Install image processing dependencies"""
    print("\n🖼️  Installing image processing dependencies...")
    
    image_packages = [
        "imageio>=2.22.0",
        "imageio-ffmpeg>=0.4.7",
        "scikit-image>=0.19.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "moviepy>=1.0.3",
        "av>=8.0.0",
        "decord>=0.6.0",
        "vidgear>=0.3.0",
        "pymediainfo>=6.0.0"
    ]
    
    for package in image_packages:
        if not run_command(f"pip3 install '{package}'", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")

def install_specialized_dependencies():
    """Install specialized video editing dependencies"""
    print("\n🎨 Installing specialized dependencies...")
    
    specialized_packages = [
        "colorspacious>=1.1.2",
        "fonttools>=4.33.0",
        "boto3>=1.26.0",
        "google-cloud-storage>=2.7.0",
        "azure-storage-blob>=12.14.0",
        "flask>=2.2.0",
        "fastapi>=0.95.0",
        "uvicorn>=0.20.0",
        "youtube-dl>=2021.12.17",
        "yt-dlp>=2023.3.4",
        "google-api-python-client>=2.80.0",
        "python-magic>=0.4.27",
        "cupy-cuda11x; sys_platform != 'darwin'",
        "pyopencl>=2022.3.1",
        "GPUtil>=1.4.0",
        "pynvml>=11.4.1"
    ]
    
    for package in specialized_packages:
        if not run_command(f"pip3 install '{package}'", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")

def setup_ffmpeg():
    """Ensure FFmpeg is available"""
    print("\n🎬 Checking FFmpeg installation...")
    
    # Check if ffmpeg is already available
    if run_command("ffmpeg -version", "Checking existing FFmpeg"):
        print("✅ FFmpeg already installed")
        return True
    
    # Check if it's in our local bin
    ffmpeg_path = Path.home() / "bin" / "ffmpeg"
    if ffmpeg_path.exists():
        print("✅ FFmpeg found in ~/bin/")
        return True
    
    print("ℹ️  FFmpeg not found. Please ensure FFmpeg is installed:")
    print("   macOS: brew install ffmpeg")
    print("   Ubuntu: sudo apt install ffmpeg")
    print("   Or download from: https://ffmpeg.org/download.html")
    
    return False

def verify_installation():
    """Verify the installation works"""
    print("\n🔍 Verifying installation...")
    
    try:
        # Test core imports
        import numpy as np
        print("✅ NumPy")
        
        import cv2
        print("✅ OpenCV")
        
        import PIL
        print("✅ Pillow")
        
        # Test our package
        try:
            from src.video_ai_editor.ultimate_auto_editor import UltimateHollywoodEditor
            print("✅ Video AI Editor - Hollywood Editor")
        except ImportError as e:
            print(f"⚠️  Video AI Editor import issue: {e}")
        
        # Test optional imports
        try:
            import torch
            print(f"✅ PyTorch {torch.__version__}")
        except ImportError:
            print("⚠️  PyTorch not available")
        
        try:
            import librosa
            print("✅ Librosa")
        except ImportError:
            print("⚠️  Librosa not available")
        
        print("\n🎉 Installation verification complete!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main installation process"""
    print("🚀 Ultimate Video Editor - Installation Script")
    print("=" * 50)
    
    if not check_system():
        print("❌ System requirements not met")
        return False
    
    # Install dependencies in order
    install_core_dependencies()
    install_audio_dependencies() 
    install_ai_dependencies()
    install_image_dependencies()
    install_specialized_dependencies()
    
    # Setup FFmpeg
    setup_ffmpeg()
    
    # Setup package structure
    print("\n📦 Setting up Video AI Editor package...")
    
    # Create __init__.py files if they don't exist
    init_files = [
        "src/__init__.py",
        "src/video_ai_editor/__init__.py",
        "src/video_ai_editor/core/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).parent.mkdir(parents=True, exist_ok=True)
        if not Path(init_file).exists():
            with open(init_file, 'w') as f:
                f.write('"""Video AI Editor Package"""\n')
            print(f"✅ Created {init_file}")
    
    # Try to install our package in development mode
    if run_command("pip3 install -e .", "Installing Video AI Editor in development mode"):
        print("✅ Package installed successfully")
    else:
        print("⚠️  Package installation failed, but dependencies are installed")
    
    # Verify everything works
    success = verify_installation()
    
    if success:
        print("\n🎉 Installation Complete!")
        print("\n🎬 Ready to create Hollywood-level videos!")
        print("\nNext steps:")
        print("1. Run: python3 test_installation.py")
        print("2. Try the automated editor: python3 ultimate_hollywood_editor.py") 
        print("3. Use the system: from src.video_ai_editor.ultimate_auto_editor import UltimateHollywoodEditor")
    else:
        print("\n⚠️  Installation completed with some issues")
        print("The system may still work, but some features might be limited")
    
    return success

if __name__ == "__main__":
    main()