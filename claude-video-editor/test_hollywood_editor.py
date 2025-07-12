#!/usr/bin/env python3
"""
Test script for Hollywood Editor - Demonstrates all capabilities
"""

import asyncio
import json
from pathlib import Path
from hollywood_editor import (
    HollywoodEditor,
    ContentType,
    Platform,
    EditDecisionEngine,
    PredictiveViralEngine,
    GenerativeContentEngine,
    AutonomousChannelManager
)

async def test_complete_pipeline():
    """Test the complete Hollywood Editor pipeline"""
    
    print("🎬 HOLLYWOOD EDITOR - COMPLETE CAPABILITY DEMONSTRATION")
    print("=" * 70)
    
    # Test 1: Script Generation
    print("\n1️⃣ TESTING GENERATIVE SCRIPTING")
    print("-" * 40)
    
    content_engine = GenerativeContentEngine()
    
    test_prompts = [
        ("Create a 30-second viral video about the benefits of hydration", ContentType.EDUCATIONAL),
        ("How to make the perfect coffee in 5 steps", ContentType.TUTORIAL),
        ("Top 5 mind-blowing facts about the ocean", ContentType.ENTERTAINMENT),
        ("Why you should start today - motivational message", ContentType.MOTIVATION)
    ]
    
    for prompt, content_type in test_prompts:
        print(f"\nPrompt: {prompt}")
        script = await content_engine.generate_script(prompt, content_type, 30)
        print(f"Generated Script Preview: {script[:200]}...")
        
        # Test keyword extraction
        keywords = content_engine._extract_keywords(script)
        print(f"Keywords: {keywords[:5]}")
    
    # Test 2: Edit Decision Engine
    print("\n\n2️⃣ TESTING EDIT DECISION ENGINE")
    print("-" * 40)
    
    from hollywood_editor import Project
    decision_engine = EditDecisionEngine()
    
    # Create test project
    test_project = Project(
        prompt="Test educational content",
        content_type=ContentType.EDUCATIONAL,
        target_platforms=[Platform.YOUTUBE_SHORTS, Platform.TIKTOK],
        script="This is a test script with multiple sections.",
        source_files=["test1.mp4", "test2.mp4"]
    )
    
    # Generate EDL
    edl = decision_engine.generate_edit_plan(test_project)
    print(f"Generated {len(edl)} edit actions")
    
    for i, action in enumerate(edl[:3]):
        print(f"  Action {i+1}: {type(action).__name__}")
    
    # Test 3: Predictive Viral Engine
    print("\n\n3️⃣ TESTING PREDICTIVE VIRAL ENGINE")
    print("-" * 40)
    
    viral_engine = PredictiveViralEngine()
    
    # Generate variants
    variants = viral_engine.generate_variants(edl, test_project)
    print(f"Generated {len(variants)} viral variants:")
    
    for variant in variants:
        print(f"  • {variant['name']}: Score = {variant['predicted_score']['total']:.2f}")
    
    # Select best
    best_id = viral_engine.select_best_variant(variants, test_project)
    best_variant = next(v for v in variants if v["id"] == best_id)
    print(f"Selected: {best_variant['name']}")
    
    # Test 4: Platform Export Specifications
    print("\n\n4️⃣ TESTING PLATFORM SPECIFICATIONS")
    print("-" * 40)
    
    from hollywood_editor import ExportDeliverySystem
    export_system = ExportDeliverySystem()
    
    print("Platform Export Presets:")
    for platform, preset in export_system.export_presets.items():
        print(f"  • {platform.value}: {preset['resolution']} @ {preset['fps']}fps, {preset['bitrate']} bitrate")
    
    # Test 5: Autonomous Channel Management
    print("\n\n5️⃣ TESTING CHANNEL MANAGEMENT")
    print("-" * 40)
    
    channel_manager = AutonomousChannelManager()
    
    # Test metadata generation
    for platform in [Platform.YOUTUBE, Platform.TIKTOK, Platform.INSTAGRAM_REEL]:
        metadata = channel_manager._generate_platform_metadata(test_project, platform)
        print(f"\n{platform.value} Metadata:")
        print(f"  Title: {metadata['title'][:50]}...")
        print(f"  Tags: {metadata['tags']}")
    
    # Test 6: Complete Pipeline
    print("\n\n6️⃣ TESTING COMPLETE PIPELINE")
    print("-" * 40)
    
    editor = HollywoodEditor()
    
    # Create from prompt only
    print("\nCreating video from prompt...")
    project = await editor.create_masterpiece(
        prompt="Create a 30-second video about why everyone should learn to code",
        content_type=ContentType.EDUCATIONAL,
        target_platforms=[Platform.YOUTUBE_SHORTS, Platform.TIKTOK],
        target_duration=30
    )
    
    print(f"\n✅ Project Status: {project.status.value}")
    print(f"Project ID: {project.project_id}")
    
    if project.script:
        print(f"Generated Script: {project.script[:100]}...")
    
    if project.edit_decision_list:
        print(f"Edit Actions: {len(project.edit_decision_list)}")
    
    if project.viral_variants:
        print(f"Viral Variants: {len(project.viral_variants)}")
    
    if project.output_paths:
        print("Output Files:")
        for platform, path in project.output_paths.items():
            print(f"  • {platform}: {path}")
    
    # Cleanup
    editor.cleanup()
    
    print("\n" + "=" * 70)
    print("✅ HOLLYWOOD EDITOR TEST COMPLETE!")
    print("=" * 70)

def demonstrate_features():
    """Demonstrate all Hollywood Editor features"""
    
    print("\n🌟 HOLLYWOOD EDITOR FEATURES")
    print("=" * 70)
    
    features = {
        "1. GENERATIVE SCRIPTING": [
            "• AI writes complete video scripts from simple prompts",
            "• Adapts tone and structure based on content type",
            "• Optimizes for platform-specific engagement",
            "• Includes hooks, CTAs, and viral elements"
        ],
        
        "2. AUTOMATED CONTENT SOURCING": [
            "• Extracts keywords from scripts",
            "• Sources relevant stock footage (Pexels API ready)",
            "• Generates AI voiceovers (ElevenLabs ready)",
            "• Future: Generative video AI integration (Sora)"
        ],
        
        "3. EDIT DECISION ENGINE": [
            "• Structured EDL with typed EditAction objects",
            "• Platform-specific optimizations",
            "• Content-aware editing decisions",
            "• Automatic pacing and timing"
        ],
        
        "4. PREDICTIVE VIRAL ENGINE": [
            "• Generates multiple edit variants",
            "• Scores each variant for viral potential",
            "• Considers hook retention, pacing, engagement",
            "• Learns from performance history"
        ],
        
        "5. HOLLYWOOD POLISH": [
            "• Professional color grading",
            "• Film grain for texture",
            "• Audio mastering (EQ, compression, LUFS)",
            "• Platform-specific encoding"
        ],
        
        "6. AUTONOMOUS CHANNEL MANAGEMENT": [
            "• Auto-publishes to YouTube, TikTok, Instagram",
            "• Generates SEO-optimized titles and tags",
            "• Tracks performance metrics",
            "• Analyzes audience feedback",
            "• Updates models based on results"
        ],
        
        "7. UNIFIED ARCHITECTURE": [
            "• Single HollywoodEditor class orchestrates all",
            "• Project state management with tracking",
            "• Async pipeline for efficiency",
            "• Comprehensive error handling"
        ],
        
        "8. PRODUCTION CLI": [
            "• Simple commands for complex operations",
            "• Batch processing support",
            "• Real-time progress tracking",
            "• Performance analytics"
        ]
    }
    
    for category, items in features.items():
        print(f"\n{category}")
        print("-" * 40)
        for item in items:
            print(item)
    
    print("\n📊 CAPABILITY SUMMARY")
    print("-" * 40)
    print("• Input: Simple text prompt")
    print("• Output: Platform-optimized viral videos")
    print("• Process: Fully autonomous from script to publishing")
    print("• Learning: Improves with each video based on performance")
    
    print("\n🚀 This is not just a video editor...")
    print("   It's an autonomous content creation studio!")

def show_example_commands():
    """Show example CLI commands"""
    
    print("\n📟 EXAMPLE COMMANDS")
    print("=" * 70)
    
    examples = [
        {
            "desc": "Create educational video from prompt",
            "cmd": "python main.py create 'Benefits of meditation' --type educational --platform youtube_shorts tiktok"
        },
        {
            "desc": "Create and auto-publish to all platforms",
            "cmd": "python main.py create 'Top 5 productivity hacks' --publish --platform youtube tiktok instagram_reel"
        },
        {
            "desc": "Create from existing video with AI enhancement",
            "cmd": "python main.py create 'Make this viral' --input video.mp4 --type entertainment"
        },
        {
            "desc": "Batch create multiple videos",
            "cmd": "python main.py batch prompts.json --platform youtube_shorts --publish --parallel 3"
        },
        {
            "desc": "Check video performance",
            "cmd": "python main.py performance <project-id>"
        }
    ]
    
    for ex in examples:
        print(f"\n{ex['desc']}:")
        print(f"  $ {ex['cmd']}")
    
    print("\n💡 Create a config file for API keys:")
    print("  $ python main.py config")

if __name__ == "__main__":
    # Run async test
    asyncio.run(test_complete_pipeline())
    
    # Show features
    demonstrate_features()
    
    # Show commands
    show_example_commands()
    
    print("\n✨ Hollywood Editor is ready to revolutionize content creation!")