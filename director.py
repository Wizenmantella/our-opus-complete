# director.py
import random
from project import VideoProject
from config import STYLE_PROFILES

class Director:
    """
    The AI Director makes creative decisions and generates an 'edit plan'.
    """
    def __init__(self, project: VideoProject):
        self.project = project
        self.style = STYLE_PROFILES[project.style_name]
        self.edit_plan = []

    def generate_edit_plan(self):
        """
        Analyzes the project data and style profile to create a detailed
        list of editing actions.
        """
        print("-> The Director is generating the edit plan...")

        # 1. Hook & Retention Overlays
        if self.style.get("use_hook_text", False):
            self.edit_plan.append({
                'time': 0, 
                'action': 'add_overlay', 
                'type': 'hook_text', 
                'text': "YOU WON'T BELIEVE THIS", 
                'duration': 3
            })
        
        if self.style.get("use_progress_bar", False):
            self.edit_plan.append({
                'time': 0, 
                'action': 'add_overlay', 
                'type': 'progress_bar', 
                'duration': self.project.clip.duration
            })

        # 2. Captions
        self.edit_plan.append({
            'time': 0, 
            'action': 'add_captions', 
            'style': 'word_by_word'
        })

        # 3. Beat-synced Effects
        effect_frequency = self.style.get("effect_frequency", 0.5)
        allowed_effects = self.style.get("allowed_effects", [])
        
        for i, beat_time in enumerate(self.project.beat_timestamps):
            if random.random() < effect_frequency and allowed_effects:
                effect_type = random.choice(allowed_effects)
                self.edit_plan.append({
                    'time': beat_time,
                    'action': 'apply_effect',
                    'type': effect_type,
                    'duration': 0.3
                })

        # 4. Scene-based Transitions
        transition_frequency = self.style.get("transition_frequency", 0.3)
        allowed_transitions = self.style.get("allowed_transitions", [])
        
        for scene_time in self.project.scene_timestamps:
            # Find nearby beats for better sync
            nearby_beats = [beat for beat in self.project.beat_timestamps 
                          if abs(beat - scene_time) < 0.2]
            
            if nearby_beats and random.random() < transition_frequency and allowed_transitions:
                transition_type = random.choice(allowed_transitions)
                sync_time = min(nearby_beats, key=lambda x: abs(x - scene_time))
                
                self.edit_plan.append({
                    'time': sync_time,
                    'action': 'apply_transition',
                    'type': transition_type,
                    'duration': 0.5
                })

        # 5. Emphasis-based Effects (on ALL CAPS words)
        if self.project.transcript:
            for segment in self.project.transcript:
                for word_info in segment.get('words', []):
                    word = word_info.get('word', '')
                    if word.isupper() and len(word) > 2:
                        self.edit_plan.append({
                            'time': word_info['start'],
                            'action': 'apply_effect',
                            'type': 'screen_shake',
                            'duration': 0.3
                        })

        # 6. Engagement Text at Key Moments
        high_energy_beats = [beat for i, beat in enumerate(self.project.beat_timestamps) if i % 16 == 0]
        engagement_texts = ["FIRE!", "INSANE!", "AMAZING!", "WOW!", "INCREDIBLE!"]
        
        for i, beat_time in enumerate(high_energy_beats[:5]):  # Limit to 5
            if beat_time > 3:  # After hook
                text = random.choice(engagement_texts)
                self.edit_plan.append({
                    'time': beat_time,
                    'action': 'add_overlay',
                    'type': 'engagement_text',
                    'text': text,
                    'duration': 2
                })

        # Sort the plan by time
        self.edit_plan.sort(key=lambda x: x['time'])
        self.project.edit_plan = self.edit_plan
        print(f"-> Edit plan generated with {len(self.edit_plan)} actions.")
        
        return self.edit_plan