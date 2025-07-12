#!/usr/bin/env python3
"""
Test Ultimate Viral Video Editor
Demonstrates complete viral video creation pipeline
"""

import asyncio
from pathlib import Path
import sys

# Import our viral editor
from ultimate_viral_editor import (
    UltimateViralEditor, 
    ViralVideoConfig, 
    ViralPlatform, 
    ViralTemplate
)

async def test_viral_editor():
    """Test the viral video editor with different templates"""
    
    print("🚀 TESTING ULTIMATE VIRAL VIDEO EDITOR")
    print("=" * 70)
    
    # Find test video
    test_videos = [
        "/Users/darriushart/Desktop/DOG AND BOY.mp4",
        "/Users/darriushart/Desktop/Video's/test_video.mp4"
    ]
    
    input_video = None
    for video in test_videos:
        if Path(video).exists():
            input_video = video
            break
    
    if not input_video:
        print("❌ No test video found!")
        return
    
    print(f"📹 Using test video: {input_video}")
    
    # Create output directory
    output_dir = Path("/Users/darriushart/Desktop/Video's/viral_outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize editor
    editor = UltimateViralEditor()
    
    # Test different viral styles
    test_configs = [
        {
            "name": "TikTok Podcast Style",
            "config": ViralVideoConfig(
                platform=ViralPlatform.TIKTOK,
                template=ViralTemplate.PODCAST_CLIPS,
                duration=30.0,
                music_sync=True,
                auto_captions=True,
                hook_style="explosive",
                engagement_overlays=True
            ),
            "output": str(output_dir / "tiktok_podcast_viral.mp4")
        },
        {
            "name": "Instagram Motivational",
            "config": ViralVideoConfig(
                platform=ViralPlatform.INSTAGRAM_REEL,
                template=ViralTemplate.MOTIVATION,
                duration=30.0,
                music_sync=True,
                auto_captions=True,
                hook_style="urgent",
                transition_intensity=0.9,
                engagement_overlays=True
            ),
            "output": str(output_dir / "instagram_motivation_viral.mp4")
        },
        {
            "name": "YouTube Tutorial",
            "config": ViralVideoConfig(
                platform=ViralPlatform.YOUTUBE_SHORTS,
                template=ViralTemplate.TUTORIAL,
                duration=45.0,
                music_sync=False,
                auto_captions=True,
                hook_style="mystery",
                engagement_overlays=True
            ),
            "output": str(output_dir / "youtube_tutorial_viral.mp4")
        }
    ]
    
    # Process each style
    for test in test_configs:
        print(f"\n{'='*70}")
        print(f"🎬 Creating: {test['name']}")
        print(f"{'='*70}")
        
        try:
            result = await editor.create_viral_video(
                input_video=input_video,
                config=test["config"],
                output_path=test["output"]
            )
            
            if result["success"]:
                print(f"\n✅ Success! Created: {test['output']}")
                print(f"⏱️  Processing time: {result['processing_time']:.1f}s")
                print(f"📊 Viral score: {result['viral_score'] * 100:.1f}%")
                
                # Print report
                report = result["report"]
                print("\n📋 Viral Video Report:")
                print(f"  • Platform: {report['platform']}")
                print(f"  • Template: {report['template']}")
                print(f"  • Duration: {report['duration']}s")
                print(f"  • Viral moments: {report['viral_moments_found']}")
                print(f"  • Face coverage: {report['face_coverage']}")
                print(f"  • Motion score: {report['average_motion_score']:.1f}")
                print(f"  • Estimated engagement: {report['estimated_engagement_rate']}")
                
            else:
                print(f"\n❌ Failed to create {test['name']}")
                
        except Exception as e:
            print(f"\n❌ Error creating {test['name']}: {e}")
    
    print("\n" + "="*70)
    print("🎉 VIRAL VIDEO TESTS COMPLETE!")
    print(f"📁 Check outputs in: {output_dir}")
    print("="*70)
    
    # Show feature summary
    print("\n✨ VIRAL FEATURES DEMONSTRATED:")
    print("  ✅ Explosive hook intros (3 styles)")
    print("  ✅ Dynamic animated captions (6 styles)")  
    print("  ✅ Beat-synced cuts and effects")
    print("  ✅ Viral transitions (10 types)")
    print("  ✅ Engagement overlays and CTAs")
    print("  ✅ Platform-specific optimization")
    print("  ✅ Progress bars and countdowns")
    print("  ✅ Emoji reactions and animations")
    print("  ✅ Speed ramping and time effects")
    print("  ✅ Professional color grading")
    
    print("\n🚀 This system can create viral videos like:")
    print("  • MrBeast style with big text and energy")
    print("  • Alex Hormozi podcast clips with captions")
    print("  • Gaming highlights with effects")
    print("  • Quick tutorials with step counters")
    print("  • Motivational content with power zooms")
    print("  • Reaction videos with split screens")
    
    print("\n💡 The AI automatically:")
    print("  • Detects the best moments")
    print("  • Adds hooks to grab attention")
    print("  • Syncs edits to music beats")
    print("  • Optimizes for each platform")
    print("  • Maximizes engagement potential")


async def create_single_viral_video(video_path: str, style: str = "tiktok_podcast"):
    """Create a single viral video with specified style"""
    
    editor = UltimateViralEditor()
    
    # Style presets
    styles = {
        "tiktok_podcast": ViralVideoConfig(
            platform=ViralPlatform.TIKTOK,
            template=ViralTemplate.PODCAST_CLIPS,
            duration=30.0,
            music_sync=True,
            auto_captions=True,
            hook_style="explosive"
        ),
        "instagram_motivation": ViralVideoConfig(
            platform=ViralPlatform.INSTAGRAM_REEL,
            template=ViralTemplate.MOTIVATION,
            duration=30.0,
            music_sync=True,
            auto_captions=True,
            hook_style="urgent"
        ),
        "youtube_gaming": ViralVideoConfig(
            platform=ViralPlatform.YOUTUBE_SHORTS,
            template=ViralTemplate.GAMING,
            duration=60.0,
            music_sync=True,
            auto_captions=True,
            hook_style="explosive",
            transition_intensity=1.0
        )
    }
    
    config = styles.get(style, styles["tiktok_podcast"])
    output_path = f"/Users/darriushart/Desktop/Video's/viral_{style}_{Path(video_path).stem}.mp4"
    
    print(f"🎬 Creating {style} viral video...")
    
    result = await editor.create_viral_video(
        input_video=video_path,
        config=config,
        output_path=output_path
    )
    
    if result["success"]:
        print(f"\n✅ Viral video created: {output_path}")
        print(f"📊 Viral score: {result['viral_score'] * 100:.1f}%")
    else:
        print("\n❌ Failed to create viral video")
    
    return result


if __name__ == "__main__":
    # Check if specific video provided
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        style = sys.argv[2] if len(sys.argv) > 2 else "tiktok_podcast"
        asyncio.run(create_single_viral_video(video_path, style))
    else:
        # Run full test suite
        asyncio.run(test_viral_editor())