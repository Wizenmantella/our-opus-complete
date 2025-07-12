#!/usr/bin/env python3
"""
Hollywood-Level Video Editor - Installation Test Script
Tests all major components to ensure the system is working correctly.
"""

import sys
import traceback
import importlib
from pathlib import Path

def test_import(module_name, description=""):
    """Test importing a module"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description or module_name}")
        return True
    except ImportError as e:
        print(f"❌ {description or module_name}: {e}")
        return False

def test_core_dependencies():
    """Test core dependencies"""
    print("🔍 Testing core dependencies...")
    
    tests = [
        ("numpy", "NumPy"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("ffmpeg", "FFmpeg-Python"),
        ("asyncio", "AsyncIO"),
        ("aiofiles", "AIO Files"),
        ("rich", "Rich"),
        ("tqdm", "TQDM"),
        ("scipy", "SciPy"),
        ("matplotlib", "Matplotlib"),
        ("sklearn", "Scikit-Learn"),
        ("psutil", "PSUtil"),
        ("requests", "Requests"),
        ("aiohttp", "AIO HTTP"),
        ("websockets", "WebSockets"),
        ("sqlalchemy", "SQLAlchemy"),
        ("watchdog", "Watchdog"),
        ("colorama", "Colorama"),
        ("click", "Click")
    ]
    
    passed = 0
    for module, desc in tests:
        if test_import(module, desc):
            passed += 1
    
    print(f"Core dependencies: {passed}/{len(tests)} passed")
    return passed == len(tests)

def test_audio_dependencies():
    """Test audio processing dependencies"""
    print("\n🎵 Testing audio dependencies...")
    
    tests = [
        ("librosa", "Librosa"),
        ("soundfile", "SoundFile"),
        ("pydub", "PyDub"),
        ("resampy", "Resampy"),
        ("noisereduce", "NoiseReduce"),
        ("pyloudnorm", "PyLoudnorm"),
        ("aubio", "Aubio"),
        ("webrtcvad", "WebRTC VAD"),
        ("whisper", "OpenAI Whisper"),
        ("speech_recognition", "Speech Recognition")
    ]
    
    passed = 0
    for module, desc in tests:
        if test_import(module, desc):
            passed += 1
    
    print(f"Audio dependencies: {passed}/{len(tests)} passed")
    return passed >= len(tests) * 0.8  # 80% pass rate

def test_ai_dependencies():
    """Test AI/ML dependencies"""
    print("\n🤖 Testing AI/ML dependencies...")
    
    tests = [
        ("torch", "PyTorch"),
        ("torchvision", "TorchVision"),
        ("torchaudio", "TorchAudio"),
        ("transformers", "Transformers"),
        ("diffusers", "Diffusers"),
        ("ultralytics", "Ultralytics"),
        ("mediapipe", "MediaPipe"),
        ("onnx", "ONNX"),
        ("onnxruntime", "ONNX Runtime"),
        ("tensorflow", "TensorFlow"),
        ("keras", "Keras"),
        ("face_recognition", "Face Recognition"),
        ("deepface", "DeepFace"),
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic")
    ]
    
    passed = 0
    for module, desc in tests:
        if test_import(module, desc):
            passed += 1
    
    print(f"AI/ML dependencies: {passed}/{len(tests)} passed")
    return passed >= len(tests) * 0.7  # 70% pass rate

def test_image_dependencies():
    """Test image processing dependencies"""
    print("\n🖼️ Testing image dependencies...")
    
    tests = [
        ("imageio", "ImageIO"),
        ("skimage", "Scikit-Image"),
        ("seaborn", "Seaborn"),
        ("plotly", "Plotly"),
        ("moviepy", "MoviePy"),
        ("av", "PyAV"),
        ("pymediainfo", "PyMediaInfo")
    ]
    
    passed = 0
    for module, desc in tests:
        if test_import(module, desc):
            passed += 1
    
    print(f"Image dependencies: {passed}/{len(tests)} passed")
    return passed >= len(tests) * 0.8  # 80% pass rate

def test_specialized_dependencies():
    """Test specialized dependencies"""
    print("\n🎨 Testing specialized dependencies...")
    
    tests = [
        ("colorspacious", "Colorspacious"),
        ("fonttools", "FontTools"),
        ("boto3", "Boto3"),
        ("flask", "Flask"),
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("yt_dlp", "YT-DLP"),
        ("magic", "Python Magic"),
        ("GPUtil", "GPUtil")
    ]
    
    passed = 0
    for module, desc in tests:
        if test_import(module, desc):
            passed += 1
    
    print(f"Specialized dependencies: {passed}/{len(tests)} passed")
    return passed >= len(tests) * 0.6  # 60% pass rate

def test_hardware_acceleration():
    """Test hardware acceleration capabilities"""
    print("\n⚡ Testing hardware acceleration...")
    
    acceleration_available = []
    
    # Test PyTorch GPU support
    try:
        import torch
        if torch.cuda.is_available():
            print("✅ CUDA available")
            acceleration_available.append("CUDA")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("✅ Metal Performance Shaders (MPS) available")
            acceleration_available.append("MPS")
        else:
            print("⚠️ GPU acceleration not available (CPU only)")
    except ImportError:
        print("❌ PyTorch not available")
    
    # Test OpenCL
    try:
        import pyopencl as cl
        platforms = cl.get_platforms()
        if platforms:
            print("✅ OpenCL available")
            acceleration_available.append("OpenCL")
    except ImportError:
        print("⚠️ OpenCL not available")
    
    # Test CUDA directly
    try:
        import cupy as cp
        print("✅ CuPy available")
        acceleration_available.append("CuPy")
    except ImportError:
        print("⚠️ CuPy not available")
    
    if not acceleration_available:
        print("⚠️ No GPU acceleration detected - system will use CPU")
    else:
        print(f"✅ Hardware acceleration: {', '.join(acceleration_available)}")
    
    return True

def test_video_editor_components():
    """Test the video editor components"""
    print("\n🎬 Testing Video Editor components...")
    
    try:
        # Test main editor
        from src.video_ai_editor.ultimate_auto_editor import UltimateHollywoodEditor
        print("✅ Ultimate Hollywood Editor")
        
        # Test core systems
        from src.video_ai_editor.core.hardware_acceleration_system import HardwareAccelerationSystem
        print("✅ Hardware Acceleration System")
        
        from src.video_ai_editor.core.advanced_ai_analysis_engine import AdvancedAIAnalysisEngine
        print("✅ AI Analysis Engine")
        
        from src.video_ai_editor.core.professional_audio_system_complete import ProfessionalAudioSystem
        print("✅ Professional Audio System")
        
        from src.video_ai_editor.core.multicam_360_video_system import MulticamAnd360VideoSystem
        print("✅ Multicam and 360° Video System")
        
        from src.video_ai_editor.core.media_management_collaboration_system import MediaManagementSystem
        print("✅ Media Management System")
        
        from src.video_ai_editor.core.export_delivery_system import ExportDeliverySystem
        print("✅ Export and Delivery System")
        
        from src.video_ai_editor.core.advanced_masking_rotoscoping_system import AdvancedMaskingRotoscopingSystem
        print("✅ Advanced Masking and Rotoscoping System")
        
        print("✅ All core components loaded successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Video Editor component import failed: {e}")
        print("Traceback:")
        traceback.print_exc()
        return False

def test_ffmpeg():
    """Test FFmpeg availability"""
    print("\n🎬 Testing FFmpeg...")
    
    import subprocess
    
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg: {version_line}")
            return True
        else:
            print("❌ FFmpeg command failed")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg command timed out")
        return False
    except Exception as e:
        print(f"❌ FFmpeg test error: {e}")
        return False

def test_system_resources():
    """Test system resources"""
    print("\n💾 Testing system resources...")
    
    try:
        import psutil
        
        # Memory
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        print(f"📊 Total Memory: {memory_gb:.1f} GB")
        
        if memory_gb < 8:
            print("⚠️ Warning: Less than 8GB RAM detected")
        elif memory_gb < 16:
            print("✅ Adequate memory for basic editing")
        else:
            print("✅ Excellent memory for professional editing")
        
        # CPU
        cpu_count = psutil.cpu_count()
        print(f"🔧 CPU Cores: {cpu_count}")
        
        if cpu_count < 4:
            print("⚠️ Warning: Less than 4 CPU cores")
        elif cpu_count < 8:
            print("✅ Adequate CPU for basic editing")
        else:
            print("✅ Excellent CPU for professional editing")
        
        # Disk space
        disk = psutil.disk_usage('.')
        disk_free_gb = disk.free / (1024**3)
        print(f"💽 Free Disk Space: {disk_free_gb:.1f} GB")
        
        if disk_free_gb < 10:
            print("⚠️ Warning: Less than 10GB free space")
        elif disk_free_gb < 100:
            print("✅ Adequate space for small projects")
        else:
            print("✅ Excellent space for large projects")
        
        return True
        
    except ImportError:
        print("❌ PSUtil not available for system resource check")
        return False

def create_test_video():
    """Create a simple test video to verify the system works"""
    print("\n🎥 Creating test video...")
    
    try:
        import numpy as np
        import cv2
        from pathlib import Path
        
        # Create a simple test video
        output_path = Path("test_output.mp4")
        
        # Video properties
        width, height = 640, 480
        fps = 30
        duration = 3  # seconds
        total_frames = fps * duration
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        if not writer.isOpened():
            print("❌ Could not create video writer")
            return False
        
        # Generate frames
        for frame_num in range(total_frames):
            # Create a colorful gradient frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add gradient effect
            for y in range(height):
                for x in range(width):
                    frame[y, x] = [
                        int(255 * x / width),  # Red gradient
                        int(255 * y / height),  # Green gradient
                        int(255 * (frame_num / total_frames))  # Blue changes over time
                    ]
            
            # Add frame number text
            cv2.putText(frame, f"Frame {frame_num}", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            writer.write(frame)
        
        writer.release()
        
        if output_path.exists():
            print(f"✅ Test video created: {output_path}")
            print(f"📄 File size: {output_path.stat().st_size / 1024:.1f} KB")
            return True
        else:
            print("❌ Test video was not created")
            return False
            
    except Exception as e:
        print(f"❌ Test video creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Hollywood-Level Video Editor - Installation Test")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Core Dependencies", test_core_dependencies()))
    test_results.append(("Audio Dependencies", test_audio_dependencies()))
    test_results.append(("AI/ML Dependencies", test_ai_dependencies()))
    test_results.append(("Image Dependencies", test_image_dependencies()))
    test_results.append(("Specialized Dependencies", test_specialized_dependencies()))
    test_results.append(("Hardware Acceleration", test_hardware_acceleration()))
    test_results.append(("Video Editor Components", test_video_editor_components()))
    test_results.append(("FFmpeg", test_ffmpeg()))
    test_results.append(("System Resources", test_system_resources()))
    test_results.append(("Test Video Creation", create_test_video()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("🎬 Your Hollywood-level video editing system is ready!")
        print("\nNext steps:")
        print("1. Try: python3 ultimate_hollywood_editor.py")
        print("2. Import: from src.video_ai_editor.ultimate_auto_editor import UltimateHollywoodEditor")
    elif passed >= total * 0.8:
        print("\n✅ SYSTEM MOSTLY FUNCTIONAL")
        print("🎬 Your video editing system should work with most features!")
        print("⚠️ Some advanced features may be limited due to missing dependencies")
    else:
        print("\n⚠️ SYSTEM NEEDS ATTENTION")
        print("❌ Several critical components are missing")
        print("📋 Please review the failed tests and install missing dependencies")
    
    return passed >= total * 0.8

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)