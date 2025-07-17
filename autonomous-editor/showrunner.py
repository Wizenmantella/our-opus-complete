# showrunner.py
from typing import List, Dict, Any
from project import VideoProject

class Showrunner:
    """
    The strategic brain that understands narrative structure and pacing.
    It creates a high-level "pacing map" to guide the Director.
    This elevates the system from reactive editing to proactive storytelling.
    """
    def __init__(self, project: VideoProject):
        self.project = project

    def create_pacing_map(self) -> List[Dict[str, Any]]:
        """
        Analyzes the video's duration and content to define a narrative arc.
        This replaces random editing with strategic, story-driven decisions.
        """
        print("-> [Showrunner] Designing the narrative arc...")
        duration = self.project.clip.duration
        pacing_map = []

        # Phase 1: The Hook (First 3-5 seconds)
        # Goal: Maximum impact to grab the viewer within the critical retention window
        hook_end = min(duration, 4.0)
        pacing_map.append({
            "phase": "hook",
            "start": 0,
            "end": hook_end,
            "description": "Critical viewer retention window - maximum impact required",
            "style_overrides": {
                "effect_frequency": 0.9,  # High frequency of effects
                "zoom_intensity": 1.20,   # Aggressive zooms
                "shake_intensity": 15,    # More dramatic shake
                "use_hook_text": True,
                "transition_frequency": 0.9
            }
        })

        # Phase 2: The Setup (Early content - build interest)
        setup_end = min(duration * 0.3, 15.0)
        if hook_end < setup_end:
            pacing_map.append({
                "phase": "setup",
                "start": hook_end,
                "end": setup_end,
                "description": "Establish context and build viewer investment",
                "style_overrides": {
                    "effect_frequency": 0.5,
                    "zoom_intensity": 1.10,
                    "shake_intensity": 8,
                    "transition_frequency": 0.4
                }
            })

        # Phase 3: The Climax (Peak intensity moment)
        # For shorter videos, place climax at 60-70% through
        # For longer videos, multiple intensity peaks
        climax_start = duration * 0.6
        climax_end = climax_start + min(duration * 0.15, 8.0)
        
        if climax_start < duration:
            pacing_map.append({
                "phase": "climax",
                "start": climax_start,
                "end": min(climax_end, duration),
                "description": "Peak emotional and visual intensity",
                "style_overrides": {
                    "effect_frequency": 1.0,  # Non-stop effects
                    "zoom_intensity": 1.25,   # Maximum zoom
                    "shake_intensity": 20,    # Intense shake
                    "transition_frequency": 1.0,
                    "use_speed_ramps": True   # Enable speed effects for climax
                }
            })

        # Phase 4: The Resolution (Wind down if video is long enough)
        if duration > 30:  # Only for longer content
            resolution_start = max(climax_end, duration * 0.8)
            pacing_map.append({
                "phase": "resolution",
                "start": resolution_start,
                "end": duration,
                "description": "Controlled wind-down with strategic pacing",
                "style_overrides": {
                    "effect_frequency": 0.3,
                    "zoom_intensity": 1.08,
                    "shake_intensity": 5,
                    "transition_frequency": 0.2
                }
            })

        # Phase 5: The Default (Everything else not covered by specific phases)
        pacing_map.append({
            "phase": "default",
            "start": 0,
            "end": duration,
            "description": "Baseline pacing for standard content",
            "style_overrides": {
                "effect_frequency": 0.4,
                "zoom_intensity": 1.15,
                "shake_intensity": 10,
                "transition_frequency": 0.5
            }
        })
        
        print(f"-> [Showrunner] Narrative map created with {len(pacing_map)} phases.")
        self._log_pacing_strategy(pacing_map)
        return pacing_map

    def _log_pacing_strategy(self, pacing_map: List[Dict[str, Any]]):
        """Logs the strategic decisions for transparency and debugging."""
        print("\n📋 STRATEGIC PACING ANALYSIS:")
        print("-" * 50)
        for phase in pacing_map:
            if phase['phase'] != 'default':
                duration = phase['end'] - phase['start']
                print(f"🎬 {phase['phase'].upper()}: {phase['start']:.1f}s-{phase['end']:.1f}s ({duration:.1f}s)")
                print(f"   Strategy: {phase['description']}")
                print(f"   Effect Frequency: {phase['style_overrides'].get('effect_frequency', 'default')}")
        print("-" * 50)

    def analyze_content_distribution(self) -> Dict[str, Any]:
        """
        Analyzes the distribution of content types throughout the video.
        This could be extended to identify speech vs music vs silence ratios.
        """
        total_duration = self.project.clip.duration
        
        # Calculate speech density (words per minute)
        total_words = sum(
            len(segment.get('words', [])) 
            for segment in self.project.transcript
        )
        speech_density = (total_words / total_duration) * 60 if total_duration > 0 else 0
        
        # Calculate beat density (beats per minute) 
        beat_density = (len(self.project.beat_timestamps) / total_duration) * 60 if total_duration > 0 else 0
        
        # Calculate scene change frequency
        scene_density = (len(self.project.scene_timestamps) / total_duration) * 60 if total_duration > 0 else 0
        
        content_analysis = {
            "speech_density": speech_density,  # Words per minute
            "beat_density": beat_density,      # Beats per minute  
            "scene_density": scene_density,    # Scene changes per minute
            "total_duration": total_duration,
            "content_type": self._classify_content_type(speech_density, beat_density)
        }
        
        print(f"-> [Showrunner] Content Analysis: {content_analysis['content_type']}")
        print(f"   Speech: {speech_density:.1f} WPM | Beats: {beat_density:.1f} BPM | Scenes: {scene_density:.1f} CPM")
        
        return content_analysis

    def _classify_content_type(self, speech_density: float, beat_density: float) -> str:
        """Classifies content to inform strategic decisions."""
        if speech_density > 180:  # Very high speech rate
            return "fast_dialogue"
        elif speech_density > 120:  # Moderate speech rate  
            return "standard_dialogue"
        elif beat_density > 120:  # High beat density
            return "music_driven"
        elif speech_density < 60:  # Low speech rate
            return "atmospheric"
        else:
            return "mixed_content"