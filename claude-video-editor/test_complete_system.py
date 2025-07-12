#!/usr/bin/env python3
"""
Complete System Test - Verifies all components work together
Tests the integration of all 5 evolutionary phases
"""

import asyncio
import sys
from pathlib import Path

# Test imports for all systems
print("Testing imports for complete system...")

try:
    # Phase 1: Viral Editor
    from src.video_ai_editor.viral_effects_engine import ViralEffectsEngine
    print("✅ Phase 1: Viral Effects Engine imported")
except ImportError as e:
    print(f"❌ Phase 1 import failed: {e}")

try:
    # Phase 2: Ultimate Automated Editor
    from src.video_ai_editor.core.ultimate_automated_editor import UltimateAutomatedEditor, CreativeAIDirector
    print("✅ Phase 2: Ultimate Automated Editor imported")
except ImportError as e:
    print(f"❌ Phase 2 import failed: {e}")

try:
    # Phase 3: Hollywood Editor
    from hollywood_editor import HollywoodEditor, Project, ContentType, Platform
    print("✅ Phase 3: Hollywood Editor imported")
except ImportError as e:
    print(f"❌ Phase 3 import failed: {e}")

try:
    # Phase 4: Project Chimera
    from project_chimera import ProjectChimera, PsychologyEngine, GenerativeAestheticsEngine, SocialCortex
    print("✅ Phase 4: Project Chimera imported")
except ImportError as e:
    print(f"❌ Phase 4 import failed: {e}")

try:
    # Phase 5: Autonomous Showrunner
    from autonomous_showrunner import AutonomousShowrunner, DigitalSoul, CognitiveMirror, CulturalZeitgeistEngine
    print("✅ Phase 5: Autonomous Showrunner imported")
except ImportError as e:
    print(f"❌ Phase 5 import failed: {e}")

try:
    # Integration modules
    from chimera_integration import ChimeraHollywoodBridge
    print("✅ Integration: Chimera-Hollywood Bridge imported")
except ImportError as e:
    print(f"❌ Integration import failed: {e}")

print("\n" + "="*50)


async def test_viral_editor():
    """Test Phase 1: Viral Editor"""
    print("\n🎬 Testing Viral Effects Engine...")
    
    try:
        engine = ViralEffectsEngine()
        
        # Test hook creation
        hook_filter = engine.create_hook_intro("TEST THIS!", style="explosive")
        assert "drawtext" in hook_filter
        print("  ✓ Hook creation working")
        
        # Test transition
        transition = engine.create_viral_transition("whip_pan", duration=0.5)
        assert "fps" in transition["filter"]
        print("  ✓ Viral transitions working")
        
        # Test caption system
        captions = engine.create_dynamic_captions("Test caption", highlight_words=["Test"])
        assert len(captions) > 0
        print("  ✓ Caption system working")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def test_ultimate_editor():
    """Test Phase 2: Ultimate Automated Editor"""
    print("\n🤖 Testing Ultimate Automated Editor...")
    
    try:
        editor = UltimateAutomatedEditor()
        ai_director = CreativeAIDirector()
        
        # Test AI Director analysis
        analysis = ai_director.analyze_content_requirements(
            content_type="educational",
            target_audience="young_adults",
            duration=60
        )
        assert "style" in analysis
        print("  ✓ AI Director analysis working")
        
        # Test creative decisions
        decisions = ai_director.make_creative_decisions(
            content_analysis=analysis,
            platform="tiktok"
        )
        assert len(decisions) > 0
        print("  ✓ Creative decision making working")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def test_hollywood_editor():
    """Test Phase 3: Hollywood Editor"""
    print("\n🎭 Testing Hollywood Editor...")
    
    try:
        editor = HollywoodEditor()
        
        # Test project creation
        project = await editor._create_project_state(
            prompt="Test video",
            content_type=ContentType.ENTERTAINMENT,
            target_platforms=[Platform.YOUTUBE]
        )
        assert project.prompt == "Test video"
        print("  ✓ Project creation working")
        
        # Test script generation
        script = await editor.content_engine.generate_script(
            "Test topic",
            ContentType.EDUCATIONAL,
            duration=30
        )
        assert "sections" in script
        print("  ✓ Script generation working")
        
        # Test EDL creation
        edl = editor.edit_engine.create_edit_decision_list(
            script,
            ContentType.EDUCATIONAL,
            style_params={"pacing": "medium"}
        )
        assert len(edl) > 0
        print("  ✓ Edit Decision List working")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def test_project_chimera():
    """Test Phase 4: Project Chimera"""
    print("\n🧬 Testing Project Chimera...")
    
    try:
        chimera = ProjectChimera()
        
        # Test cultural artifact creation
        artifact = await chimera.create_cultural_artifact(
            seed_concept="Test concept",
            target_emotion="contemplative",
            platform="tiktok"
        )
        assert "components" in artifact
        assert "predicted_impact" in artifact
        print("  ✓ Cultural artifact creation working")
        
        # Test psychology engine
        psych_engine = PsychologyEngine()
        tension = psych_engine.analyze_narrative_tension("Test script", duration=30)
        assert len(tension) > 0
        print("  ✓ Psychology engine working")
        
        # Test aesthetics engine
        aesthetics_engine = GenerativeAestheticsEngine()
        aesthetic = aesthetics_engine.generate_aesthetic_from_prompt("test aesthetic")
        assert aesthetic.name != ""
        print("  ✓ Aesthetics generation working")
        
        # Test social cortex
        cortex = SocialCortex()
        trends = await cortex.analyze_real_time_trends("tiktok")
        assert len(trends) > 0
        print("  ✓ Social cortex working")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def test_autonomous_showrunner():
    """Test Phase 5: Autonomous Showrunner"""
    print("\n🌟 Testing Autonomous Showrunner...")
    
    try:
        showrunner = AutonomousShowrunner()
        
        # Test digital soul
        from autonomous_showrunner import PersonaArchetype, ContentPlatform
        persona = showrunner.digital_soul.create_persona(
            name="TestPersona",
            archetype=PersonaArchetype.CREATOR,
            origin_story="Test origin",
            core_values=["test", "values"]
        )
        assert persona.name == "TestPersona"
        print("  ✓ Digital Soul creation working")
        
        # Test cognitive mirror
        insights = showrunner.cognitive_mirror.analyze_audience_feedback(
            [{"platform": "test", "comments": [{"text": "Great video!", "likes": 10}]}]
        )
        assert isinstance(insights, list)
        print("  ✓ Cognitive Mirror working")
        
        # Test zeitgeist engine
        cultural_analysis = await showrunner.zeitgeist_engine.analyze_cultural_discourse(["test"])
        assert "current_zeitgeist" in cultural_analysis
        print("  ✓ Cultural Zeitgeist Engine working")
        
        # Test universe creation
        universe = await showrunner.create_digital_universe(
            universe_name="Test Universe",
            core_theme="Test theme",
            initial_platforms=[ContentPlatform.YOUTUBE_LONG]
        )
        assert universe["name"] == "Test Universe"
        print("  ✓ Universe creation working")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def test_integration():
    """Test system integration"""
    print("\n🔄 Testing System Integration...")
    
    try:
        # Test Chimera-Hollywood Bridge
        bridge = ChimeraHollywoodBridge()
        
        # Test integrated creation
        result = await bridge.create_cultural_video(
            concept="Test integration",
            emotion="contemplative",
            platforms=["tiktok"]
        )
        assert "hollywood_project" in result
        assert "chimera_artifact" in result
        print("  ✓ Chimera-Hollywood integration working")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def run_complete_test():
    """Run all system tests"""
    print("\n" + "╔" + "═"*48 + "╗")
    print("║" + " "*10 + "COMPLETE SYSTEM TEST SUITE" + " "*12 + "║")
    print("╚" + "═"*48 + "╝")
    
    results = {
        "Phase 1 - Viral Editor": await test_viral_editor(),
        "Phase 2 - Ultimate Editor": await test_ultimate_editor(),
        "Phase 3 - Hollywood Editor": await test_hollywood_editor(),
        "Phase 4 - Project Chimera": await test_project_chimera(),
        "Phase 5 - Autonomous Showrunner": await test_autonomous_showrunner(),
        "System Integration": await test_integration()
    }
    
    print("\n" + "="*50)
    print("TEST RESULTS:")
    print("="*50)
    
    all_passed = True
    for phase, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{phase}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*50)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("The complete system is working correctly.")
        print("\nThe evolution is complete:")
        print("  • From viral video editor...")
        print("  • To autonomous cultural creator!")
    else:
        print("⚠️  Some tests failed.")
        print("Please check the error messages above.")
    
    return all_passed


async def show_system_stats():
    """Show system statistics"""
    print("\n📊 SYSTEM STATISTICS:")
    print("="*50)
    
    # Count files
    py_files = list(Path(".").rglob("*.py"))
    total_files = len(py_files)
    
    # Count lines of code
    total_lines = 0
    for f in py_files:
        if f.is_file():
            try:
                total_lines += len(f.read_text().splitlines())
            except:
                pass
    
    print(f"Total Python files: {total_files}")
    print(f"Total lines of code: {total_lines:,}")
    
    # Show major components
    print("\nMAJOR COMPONENTS:")
    components = [
        ("Viral Effects Engine", "src/video_ai_editor/viral_effects_engine.py"),
        ("Ultimate Automated Editor", "src/video_ai_editor/core/ultimate_automated_editor.py"),
        ("Hollywood Editor", "hollywood_editor.py"),
        ("Project Chimera", "project_chimera.py"),
        ("Autonomous Showrunner", "autonomous_showrunner.py")
    ]
    
    for name, path in components:
        p = Path(path)
        if p.exists():
            lines = len(p.read_text().splitlines())
            print(f"  • {name}: {lines:,} lines")
    
    print("\n✨ A complete autonomous content creation ecosystem!")


if __name__ == "__main__":
    # Run tests
    asyncio.run(run_complete_test())
    
    # Show statistics
    asyncio.run(show_system_stats())