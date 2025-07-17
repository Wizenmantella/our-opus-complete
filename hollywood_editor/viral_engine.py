# In hollywood_editor/viral_engine.py

import uuid
from typing import List, Dict, Any
from copy import deepcopy

# Assuming project.py and actions.py are in the same directory
from .project import Project
from .actions import BaseAction, Cut, AddText

class PredictiveViralEngine:
    """
    Analyzes an Edit Decision List (EDL) to predict its viral potential.
    It can generate variants of the EDL to optimize for engagement.
    """

    def _score_edl(self, edl: List[BaseAction], project: Project) -> Dict[str, float]:
        """
        Scores an EDL based on a set of heuristics for viral potential.
        This is a simplified model. A production system would use a trained ML model.
        """
        score_components = {
            "hook_intensity": 0.0,
            "pacing": 0.0,
            "text_engagement": 0.0,
        }
        
        # 1. Hook Intensity Score (first 3 seconds)
        cuts_in_hook = sum(1 for action in edl if isinstance(action, Cut) and action.start_time < 3)
        score_components["hook_intensity"] = min(cuts_in_hook / 3.0, 1.0) * 40  # Max 40 points

        # 2. Pacing Score (cuts per minute)
        total_cuts = sum(1 for action in edl if isinstance(action, Cut))
        cuts_per_minute = (total_cuts / project.target_duration) * 60
        # Ideal pacing is around 20-30 cuts per minute for short-form content
        if 20 <= cuts_per_minute <= 30:
            score_components["pacing"] = 30  # Max 30 points
        else:
            score_components["pacing"] = max(0, 30 - abs(25 - cuts_per_minute))

        # 3. Text Engagement Score
        text_actions = sum(1 for action in edl if isinstance(action, AddText))
        # Ideal is some text, but not overwhelmingly so
        if 3 <= text_actions <= 10:
            score_components["text_engagement"] = 30 # Max 30 points
        else:
            score_components["text_engagement"] = max(0, 30 - (abs(6 - text_actions) * 5))
            
        total_score = sum(score_components.values())
        score_components["total"] = total_score
        return score_components

    def generate_variants(self, edl: List[BaseAction], project: Project) -> List[Dict[str, Any]]:
        """
        Generates several variants of an EDL to test different editing styles.
        """
        variants = []
        
        # Variant 1: The Original
        original_edl = deepcopy(edl)
        variants.append({
            "id": str(uuid.uuid4()),
            "name": "Original Edit",
            "edl": original_edl,
            "predicted_score": self._score_edl(original_edl, project)
        })

        # Variant 2: Faster Paced Hook
        faster_hook_edl = deepcopy(edl)
        # Simple modification: add an extra quick cut in the first second
        if isinstance(faster_hook_edl[0], BaseAction):
            new_cut = Cut(start_time=0.5, end_time=1.0, source_file="fast_cut_effect.mp4", source_start=0, source_end=0.5)
            faster_hook_edl.insert(1, new_cut)
            variants.append({
                "id": str(uuid.uuid4()),
                "name": "Faster Paced Hook",
                "edl": faster_hook_edl,
                "predicted_score": self._score_edl(faster_hook_edl, project)
            })

        # Variant 3: Text-Heavy
        text_heavy_edl = deepcopy(edl)
        # Simple modification: add more text overlays
        new_text = AddText(start_time=1.0, end_time=3.0, text="WATCH THIS!", font_size=72, position=('center', 'top'))
        text_heavy_edl.insert(2, new_text)
        variants.append({
            "id": str(uuid.uuid4()),
            "name": "Text-Heavy Version",
            "edl": text_heavy_edl,
            "predicted_score": self._score_edl(text_heavy_edl, project)
        })

        return variants

    def select_best_variant(self, variants: List[Dict[str, Any]], project: Project) -> str:
        """
        Selects the best variant based on the predicted total score.
        """
        if not variants:
            return None
            
        best_variant = max(variants, key=lambda v: v["predicted_score"]["total"])
        return best_variant["id"]