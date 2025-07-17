#!/usr/bin/env python3
"""
Verification script to ensure the Autonomous Editor is properly set up.
Run this before your first edit to check all dependencies and assets.
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def check_mark(status):
    return f"{Colors.GREEN}✓{Colors.ENDC}" if status else f"{Colors.RED}✗{Colors.ENDC}"

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{text}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 8
    print(f"{check_mark(is_valid)} Python version: {version.major}.{version.minor}.{version.micro}")
    return is_valid

def check_directory_structure():
    """Verify all required directories exist."""
    required_dirs = [
        "analysis",
        "creative", 
        "assets",
        "assets/fonts",
        "assets/sfx",
        "assets/overlays"
    ]
    
    all_exist = True
    print("\nDirectory Structure:")
    for dir_path in required_dirs:
        exists = os.path.isdir(dir_path)
        all_exist &= exists
        print(f"  {check_mark(exists)} {dir_path}/")
    
    return all_exist

def check_required_files():
    """Verify all required Python files exist."""
    required_files = [
        "main.py",
        "editor.py",
        "director.py",
        "composer.py",
        "project.py",
        "config.py",
        "requirements.txt",
        "analysis/__init__.py",
        "analysis/audio.py",
        "analysis/vision.py",
        "creative/__init__.py",
        "creative/captions.py",
        "creative/effects.py",
        "creative/overlays.py",
        "creative/transitions.py",
        "assets/__init__.py",
        "assets/asset_manager.py"
    ]
    
    all_exist = True
    print("\nRequired Files:")
    for file_path in required_files:
        exists = os.path.isfile(file_path)
        all_exist &= exists
        print(f"  {check_mark(exists)} {file_path}")
    
    return all_exist

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        version_line = result.stdout.split('\n')[0]
        print(f"{check_mark(True)} FFmpeg: {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{check_mark(False)} FFmpeg: Not installed")
        print(f"  {Colors.YELLOW}→ Install with: brew install ffmpeg{Colors.ENDC}")
        return False

def check_assets():
    """Check for required assets."""
    print("\nAssets:")
    
    # Check for fonts
    font_dir = Path("assets/fonts")
    ttf_files = list(font_dir.glob("*.ttf")) if font_dir.exists() else []
    has_font = len(ttf_files) > 0
    
    if has_font:
        print(f"  {check_mark(True)} Fonts found: {', '.join(f.name for f in ttf_files)}")
    else:
        print(f"  {check_mark(False)} No .ttf fonts found in assets/fonts/")
        print(f"  {Colors.YELLOW}→ Download Montserrat-ExtraBold.ttf from Google Fonts{Colors.ENDC}")
    
    # Check for sound effects
    sfx_dir = Path("assets/sfx")
    required_sfx = ["glitch.mp3", "whoosh.mp3"]
    
    for sfx in required_sfx:
        sfx_path = sfx_dir / sfx
        exists = sfx_path.exists()
        print(f"  {check_mark(exists)} {sfx}")
    
    return has_font

def check_virtual_env():
    """Check if we're in a virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    print(f"\n{check_mark(in_venv)} Virtual environment active")
    
    if not in_venv:
        print(f"  {Colors.YELLOW}→ Create with: python3 -m venv venv{Colors.ENDC}")
        print(f"  {Colors.YELLOW}→ Activate with: source venv/bin/activate{Colors.ENDC}")
    
    return in_venv

def check_torch_mps():
    """Check if PyTorch MPS backend is available (Apple Silicon)."""
    try:
        import torch
        mps_available = torch.backends.mps.is_available()
        if mps_available:
            print(f"{check_mark(True)} Apple Silicon MPS backend available")
        else:
            print(f"{check_mark(False)} MPS not available (Intel Mac or missing PyTorch)")
        return True
    except ImportError:
        print(f"{check_mark(False)} PyTorch not installed")
        print(f"  {Colors.YELLOW}→ Run: pip install -r requirements.txt{Colors.ENDC}")
        return False

def main():
    print_header("AUTONOMOUS EDITOR SETUP VERIFICATION")
    
    # Run all checks
    checks = {
        "Python Version": check_python_version(),
        "Directory Structure": check_directory_structure(),
        "Required Files": check_required_files(),
        "FFmpeg": check_ffmpeg(),
        "Virtual Environment": check_virtual_env(),
        "PyTorch/MPS": check_torch_mps(),
        "Assets": check_assets()
    }
    
    # Summary
    print_header("SUMMARY")
    
    all_passed = all(checks.values())
    
    if all_passed:
        print(f"\n{Colors.GREEN}✓ ALL CHECKS PASSED!{Colors.ENDC}")
        print(f"\nYour Autonomous Editor is ready to forge content!")
        print(f"\nRun your first edit with:")
        print(f"  {Colors.BLUE}python main.py /path/to/video.mp4 --style high_energy_meme{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}✗ Some checks failed.{Colors.ENDC}")
        print(f"\nPlease address the issues above before running the editor.")
        
        failed_checks = [k for k, v in checks.items() if not v]
        print(f"\nFailed checks: {', '.join(failed_checks)}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.ENDC}\n")

if __name__ == "__main__":
    main()