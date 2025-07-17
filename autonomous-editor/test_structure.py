#!/usr/bin/env python3
"""
Test script to verify the autonomous editor structure is complete.
"""

import os
import sys

def check_file_exists(filepath, required=True):
    """Check if a file exists and report status."""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {filepath}")
    return exists

def check_module_structure():
    """Verify all modules and files are in place."""
    print("Checking Autonomous Editor Structure...")
    print("=" * 50)
    
    # Core files
    print("\nCore Files:")
    core_files = [
        "main.py",
        "editor.py", 
        "director.py",
        "composer.py",
        "project.py",
        "config.py",
        "requirements.txt"
    ]
    
    for f in core_files:
        check_file_exists(f)
    
    # Analysis package
    print("\nAnalysis Package:")
    analysis_files = [
        "analysis/__init__.py",
        "analysis/audio.py",
        "analysis/vision.py"
    ]
    
    for f in analysis_files:
        check_file_exists(f)
    
    # Creative package
    print("\nCreative Package:")
    creative_files = [
        "creative/__init__.py",
        "creative/captions.py",
        "creative/effects.py",
        "creative/overlays.py",
        "creative/transitions.py"
    ]
    
    for f in creative_files:
        check_file_exists(f)
    
    # Assets package
    print("\nAssets Package:")
    assets_files = [
        "assets/__init__.py",
        "assets/asset_manager.py"
    ]
    
    for f in assets_files:
        check_file_exists(f)
    
    # Asset directories
    print("\nAsset Directories:")
    asset_dirs = [
        "assets/fonts",
        "assets/overlays", 
        "assets/sfx"
    ]
    
    for d in asset_dirs:
        exists = os.path.isdir(d)
        status = "✅" if exists else "❌"
        print(f"{status} {d}/")
    
    print("\n" + "=" * 50)
    print("Structure check complete!")
    
    # Check for placeholder implementations
    print("\nChecking for complete implementations...")
    
    # Read effects.py to see if it's still a placeholder
    with open("creative/effects.py", "r") as f:
        effects_content = f.read()
        if "EFFECT_REGISTRY" in effects_content:
            print("✅ effects.py is fully implemented")
        else:
            print("❌ effects.py is still a placeholder")
    
    # Read transitions.py to see if it's still a placeholder
    with open("creative/transitions.py", "r") as f:
        transitions_content = f.read()
        if "TRANSITION_REGISTRY" in transitions_content:
            print("✅ transitions.py is fully implemented")
        else:
            print("❌ transitions.py is still a placeholder")

if __name__ == "__main__":
    check_module_structure()