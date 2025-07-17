# director.py
import random
from typing import List, Dict, Any
from project import VideoProject
from config import STYLE_PROFILES
from analysis.sentiment import analyze_sentiment, get_creative_intent

class Director:
    """
    The AI Director. It analyzes the project data and style profile to
    generate a detailed, time-ordered 'edit plan'. This is the creative core.
    It now follows a high-level pacing_map from the Showrunner for strategic decisions.
    """
    def __init__(self, project: VideoProject, pacing_map: List[Dict[str, Any]] = None):
        self.project = project
        self.base_style = STYLE_PROFILES[project.style_name]
        self.pacing_map = pacing_map or []
        self.edit_plan = []

    def _get_style_for_time(self, time: float) -> Dict[str, Any]:
        """Gets the correct style overrides for a given timestamp based on pacing map."""
        # Start with the base style
        current_style = self.base_style.copy()
        
        # Layer on phase-specific overrides
        for phase in self.pacing_map:
            if phase['start'] <= time < phase['end']:
                # The 'default' phase is a fallback
                if phase['phase'] == 'default':
                    current_style.update(phase['style_overrides'])
                # More specific phases override the default
                elif phase['phase'] != 'default':
                    current_style.update(phase['style_overrides'])
                    # Give priority to non-default phases
                    if phase['phase'] in ['hook', 'climax']:
                        break
        return current_style

    def generate_edit_plan(self):
        """
        Constructs the final edit plan by creating a timeline of segments.
        """
        print("-> [Brain] The Director is generating the edit plan under Showrunner's strategic guidance...")
        if not self.project.clip:
            raise ValueError("Project clip not loaded.")

        # 1. Gather all significant timestamps
        cut_points = {0, self.project.clip.duration}
        cut_points.update(self.project.scene_timestamps)
        
        # Add beat-based cut points based on frequency
        if self.project.beat_timestamps:
            for i, beat_time in enumerate(self.project.beat_timestamps):
                if i % 4 == 0: # Consider every 4th beat a potential cut point
                    cut_points.add(beat_time)

        # 2. Create a sorted list of unique timestamps to define segments
        sorted_cuts = sorted(list(cut_points))

        # 3. Create segments and apply rules
        for i in range(len(sorted_cuts) - 1):
            start_time = sorted_cuts[i]
            end_time = sorted_cuts[i+1]
            duration = end_time - start_time

            if duration < 0.2: # Ignore very short segments
                continue

            segment_plan = {
                "start": start_time,
                "end": end_time,
                "duration": duration,
                "effects": [],
                "overlays": [],
                "transition": None
            }

            # MOTIVATED DECISION: Analyze segment content for emotional context
            segment_text = " ".join(
                word_info['word'] 
                for segment_data in self.project.transcript 
                for word_info in segment_data.get('words', []) 
                if start_time <= word_info['start'] < end_time
            )
            
            # Get sentiment-based creative intent
            sentiment = analyze_sentiment(segment_text)
            creative_intent = get_creative_intent(sentiment)
            
            # STRATEGIC DECISION: Get dynamic style based on pacing map
            segment_style = self._get_style_for_time(start_time)
            
            # Apply effects based on emotional content AND strategic pacing
            effective_frequency = segment_style['effect_frequency'] * creative_intent['effect_multiplier']
            
            if sentiment["intensity"] > 0 or sentiment["energy"] > 0:
                # Guarantee intense effects for emotionally charged content
                for recommended_effect in creative_intent['recommended_effects']:
                    if recommended_effect in segment_style.get('allowed_effects', []):
                        segment_plan["effects"].append(recommended_effect)
            elif random.random() < effective_frequency:
                # Fallback to strategic style-based randomness for neutral content
                effect = random.choice(segment_style.get('allowed_effects', []))
                if effect:
                    segment_plan["effects"].append(effect)
            
            # Rule: Apply transitions at scene changes with strategic pacing
            transition_frequency = segment_style.get('transition_frequency', self.base_style['transition_frequency'])
            if start_time in self.project.scene_timestamps and random.random() < transition_frequency:
                transition = random.choice(segment_style.get('allowed_transitions', []))
                if transition:
                    segment_plan["transition"] = transition

            self.edit_plan.append(segment_plan)

        # Rule: Add global overlays (Hook & Progress Bar)
        if self.style.get("use_hook_text", False):
            self.edit_plan.insert(0, {'action': 'add_global_overlay', 'type': 'hook_text', 'text': "YOU WON'T BELIEVE THIS", 'duration': 3})
        if self.style.get("use_progress_bar", False):
            self.edit_plan.insert(0, {'action': 'add_global_overlay', 'type': 'progress_bar', 'duration': self.project.clip.duration})

        self.project.edit_plan = self.edit_plan
        print(f"-> [Brain] Edit plan generated with {len(self.edit_plan)} actions/segments.")