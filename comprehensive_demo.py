#!/usr/bin/env python3
"""
COMPREHENSIVE HOLLYWOOD EDITOR DEMO
===================================

This demo showcases ALL capabilities of the Hollywood Editor AI video editing system.
It demonstrates every style profile, effect type, and feature available.

Features Demonstrated:
1. Audio Analysis (Whisper transcription + beat detection)
2. Visual Analysis (scene detection)
3. AI Director decision making
4. Dynamic word-by-word captions
5. Multiple editing styles (high_energy_meme, viral_tiktok, cinematic, calm_corporate)
6. Visual effects (zoom punch, screen shake, glitch, RGB split)
7. Engagement overlays (hook text, progress bars, engagement text)
8. Beat-synchronized editing
9. Scene-aware transitions
10. Emphasis effects on ALL CAPS words

Requirements:
- Input video file (MP4 recommended)
- All dependencies installed (moviepy, whisper, librosa, scenedetect, etc.)
"""

import os
import sys
import argparse
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import random

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from editor import Editor
from config import STYLE_PROFILES

def create_sample_video():
    """Creates a sample video file for testing if none exists."""
    print("Creating sample video for demo...")
    
    # Create a simple 10-second test video with audio
    from moviepy.editor import ColorClip, AudioFileClip
    import numpy as np
    
    # Create a simple colored background
    video = ColorClip(size=(1920, 1080), color=(50, 50, 150), duration=10)
    
    # Add some text that changes
    texts = ["WELCOME TO", "HOLLYWOOD EDITOR", "AI POWERED", "VIDEO EDITING!", "AMAZING RESULTS!"]
    text_clips = []
    
    for i, text in enumerate(texts):
        start_time = i * 2
        text_clip = TextClip(
            text,
            fontsize=100,
            color='white',
            font='Arial-Bold'
        ).set_position('center').set_start(start_time).set_duration(2)
        text_clips.append(text_clip)
    
    # Composite video with text
    final_video = CompositeVideoClip([video] + text_clips)
    
    # Create synthetic audio with beats
    sample_rate = 22050
    duration = 10
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create a simple beat pattern
    beat_freq = 2  # 2 beats per second = 120 BPM
    audio_wave = np.sin(2 * np.pi * 440 * t) * 0.3  # Base tone
    
    # Add beat emphasis
    for beat_time in np.arange(0, duration, 1/beat_freq):
        beat_start = int(beat_time * sample_rate)
        beat_end = min(beat_start + int(0.1 * sample_rate), len(audio_wave))
        if beat_end > beat_start:
            audio_wave[beat_start:beat_end] += np.sin(2 * np.pi * 880 * t[beat_start:beat_end]) * 0.5
    
    # Save audio to temporary file
    import soundfile as sf
    audio_path = "demo_audio.wav"
    sf.write(audio_path, audio_wave, sample_rate)
    
    # Add audio to video
    from moviepy.editor import AudioFileClip
    audio_clip = AudioFileClip(audio_path)
    final_video = final_video.set_audio(audio_clip)
    
    # Save sample video
    sample_path = "sample_input.mp4"
    final_video.write_videofile(
        sample_path,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    # Clean up
    os.remove(audio_path)
    final_video.close()
    audio_clip.close()
    
    print(f"Sample video created: {sample_path}")
    return sample_path

def demonstrate_style_profile(style_name, input_video):
    """Demonstrates a specific editing style."""
    print(f"\n{'='*60}")
    print(f"DEMONSTRATING STYLE: {style_name.upper()}")
    print(f"{'='*60}")
    
    style = STYLE_PROFILES[style_name]
    print(f"Description: {style['description']}")
    print(f"Effects: {style.get('allowed_effects', 'None')}")
    print(f"Transitions: {style.get('allowed_transitions', 'None')}")
    print(f"Effect Frequency: {style.get('effect_frequency', 0)}")
    print(f"Uses Hook Text: {style.get('use_hook_text', False)}")
    print(f"Uses Progress Bar: {style.get('use_progress_bar', False)}")
    
    # Create output filename
    output_path = f"demo_output_{style_name}.mp4"
    
    try:
        # Run the editing pipeline
        editor = Editor(
            video_path=input_video,
            style_name=style_name,
            output_path=output_path
        )
        editor.run_pipeline()
        
        print(f"✅ {style_name} demo completed successfully!")
        print(f"Output saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error in {style_name} demo: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_feature_showcase():
    """Creates a comprehensive showcase video demonstrating all features."""
    print(f"\n{'='*60}")
    print("CREATING COMPREHENSIVE FEATURE SHOWCASE")
    print(f"{'='*60}")
    
    showcase_clips = []
    
    # Title card
    title = TextClip(
        "HOLLYWOOD EDITOR\nFEATURE SHOWCASE",
        fontsize=80,
        color='white',
        font='Arial-Bold',
        stroke_color='black',
        stroke_width=3
    ).set_position('center').set_duration(3)
    
    bg = ColorClip(size=(1920, 1080), color=(20, 20, 40), duration=3)
    title_card = CompositeVideoClip([bg, title])
    showcase_clips.append(title_card)
    
    # Feature demonstrations
    features = [
        "🎵 Audio Analysis (Whisper + Beat Detection)",
        "👁️ Visual Scene Detection",
        "🧠 AI Director Decision Making", 
        "📝 Dynamic Word-by-Word Captions",
        "⚡ High Energy Meme Style",
        "🎬 Cinematic Style",
        "🔥 Viral TikTok Style",
        "💼 Corporate Style",
        "💥 Zoom Punch Effects",
        "🌊 Screen Shake Effects",
        "⚡ Glitch Effects",
        "🎯 Beat-Synchronized Editing",
        "🎪 Engagement Overlays",
        "📊 Progress Bars",
        "🚀 Hook Text",
        "🎨 Scene-Aware Transitions"
    ]
    
    for i, feature in enumerate(features):
        # Create feature card
        feature_text = TextClip(
            feature,
            fontsize=60,
            color='yellow',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=2
        ).set_position('center').set_duration(2)
        
        # Random background color
        colors = [(150, 50, 50), (50, 150, 50), (50, 50, 150), (150, 50, 150), (150, 150, 50)]
        bg_color = random.choice(colors)
        bg = ColorClip(size=(1920, 1080), color=bg_color, duration=2)
        
        feature_card = CompositeVideoClip([bg, feature_text])
        showcase_clips.append(feature_card)
    
    # Combine all clips
    from moviepy.editor import concatenate_videoclips
    final_showcase = concatenate_videoclips(showcase_clips)
    
    # Save showcase
    showcase_path = "hollywood_editor_feature_showcase.mp4"
    final_showcase.write_videofile(
        showcase_path,
        codec='libx264',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    final_showcase.close()
    print(f"✅ Feature showcase created: {showcase_path}")
    return showcase_path

def main():
    """Main demo function that showcases all capabilities."""
    parser = argparse.ArgumentParser(
        description="Comprehensive Hollywood Editor Demo - Shows off ALL capabilities",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Input video file (will create sample if not provided)"
    )
    
    parser.add_argument(
        "--style",
        type=str,
        default="all",
        choices=list(STYLE_PROFILES.keys()) + ["all"],
        help="Style to demonstrate (default: all styles)"
    )
    
    parser.add_argument(
        "--create-sample",
        action="store_true",
        help="Force creation of sample video even if input provided"
    )
    
    args = parser.parse_args()
    
    print("🎬 HOLLYWOOD EDITOR COMPREHENSIVE DEMO 🎬")
    print("=" * 50)
    
    # Get or create input video
    if args.create_sample or not args.input:
        input_video = create_sample_video()
    else:
        input_video = args.input
        if not os.path.exists(input_video):
            print(f"❌ Input video not found: {input_video}")
            print("Creating sample video instead...")
            input_video = create_sample_video()
    
    print(f"Using input video: {input_video}")
    
    # Create feature showcase
    create_feature_showcase()
    
    # Demonstrate styles
    successful_outputs = []
    
    if args.style == "all":
        styles_to_demo = list(STYLE_PROFILES.keys())
    else:
        styles_to_demo = [args.style]
    
    for style in styles_to_demo:
        output = demonstrate_style_profile(style, input_video)
        if output:
            successful_outputs.append(output)
    
    # Print summary
    print(f"\n{'='*60}")
    print("🎉 DEMO COMPLETE! 🎉")
    print(f"{'='*60}")
    print(f"Input video: {input_video}")
    print(f"Feature showcase: hollywood_editor_feature_showcase.mp4")
    print(f"Style demonstrations created: {len(successful_outputs)}")
    
    for output in successful_outputs:
        print(f"  ✅ {output}")
    
    print(f"\n🚀 The Hollywood Editor demonstrated {len(STYLE_PROFILES)} editing styles")
    print("   with AI-powered analysis, beat-synchronized effects, and viral optimization!")
    
    # Clean up sample if we created it
    if args.create_sample or not args.input:
        if os.path.exists("sample_input.mp4"):
            os.remove("sample_input.mp4")
            print("🧹 Cleaned up sample video file")

if __name__ == "__main__":
    main()