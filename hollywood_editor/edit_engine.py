# In hollywood_editor/edit_engine.py

import os
from pathlib import Path
import random
from typing import List

# Assuming project.py and actions.py are in the same directory
from .project import Project
from .actions import BaseAction, Cut, AddText, ApplyLUT, AddAudio
# Import the content engine to use its keyword extraction
from .content_engine import GenerativeContentEngine

class EditDecisionEngine:
    """
    Analyzes a project's script and generates an Edit Decision List (EDL),
    which is a sequence of actions to create the final video.
    """

    def __init__(self):
        # We need an instance of the content engine to extract keywords
        self.content_engine = GenerativeContentEngine()

    def _find_matching_footage(self, keyword: str, all_footage: List[Path]) -> Path:
        """Finds the best footage for a given keyword."""
        matches = [p for p in all_footage if keyword.lower() in p.name.lower()]
        return random.choice(matches) if matches else None

    def generate_edit_plan(self, project: Project) -> List[BaseAction]:
        """
        Creates an EDL from a project using intelligent keyword-based footage selection.
        If word-level timestamps are available, creates dynamic word-by-word subtitles.
        """
        if not project.script:
            print("Warning: No script found in the project. Cannot generate an edit plan.")
            return []

        edl: List[BaseAction] = []
        current_time = 0.0

        # --- Step 1: Scan for available stock footage ---
        stock_footage_dir = Path("./stock_footage")
        if not stock_footage_dir.exists():
            print(f"Warning: Stock footage directory not found at {stock_footage_dir}")
            available_footage = []
        else:
            available_footage = list(stock_footage_dir.glob("*.mp4")) + list(stock_footage_dir.glob("*.mov"))

        if not available_footage:
            print("Warning: No stock footage found. Video will be black.")
            # Fallback to hardcoded list if no footage is found
            available_footage = [Path(f"stock_footage_{i}.mp4") for i in range(10)]

        # --- Step 2: Extract keywords from the script ---
        keywords = self.content_engine._extract_keywords(project.script)
        print(f"Extracted keywords for footage selection: {keywords}")

        # --- Step 3: Create footage cuts ---
        # Simple logic: split script by lines to create scenes
        script_lines = [line.strip() for line in project.script.split('\n') if line.strip()]

        # Estimate duration per line
        if not script_lines:
            return []
        duration_per_line = project.target_duration / len(script_lines)

        # Create footage cuts based on script lines
        for i, line in enumerate(script_lines):
            start_time = current_time
            end_time = current_time + duration_per_line

            # Intelligent Cut Selection
            # Find a relevant keyword for this line of the script
            line_keyword = next((kw for kw in keywords if kw in line.lower()), None)

            selected_footage_path = None
            if line_keyword:
                selected_footage_path = self._find_matching_footage(line_keyword, available_footage)

            # Fallback to a random clip if no match is found
            if not selected_footage_path and available_footage:
                selected_footage_path = random.choice(available_footage)

            if selected_footage_path:
                cut_action = Cut(
                    start_time=start_time,
                    end_time=end_time,
                    source_file=str(selected_footage_path),
                    source_start=0.0, # Start from the beginning of the stock clip
                    source_end=duration_per_line
                )
                edl.append(cut_action)

            current_time = end_time

        # --- Step 4: Create text overlays ---
        # Check if we have word-level timestamps for dynamic subtitles
        if project.voiceover_timestamps:
            print("Using word-level timestamps for dynamic subtitles.")
            for word_data in project.voiceover_timestamps:
                word = word_data['word']
                start = word_data['start']
                end = word_data['end']

                text_action = AddText(
                    start_time=start,
                    end_time=end,
                    text=word.upper(), # Make subtitles stand out
                    font_size=72,
                    position=('center', 'center'),
                    color='yellow' # Highlight color
                )
                edl.append(text_action)
        else:
            # Fallback to line-by-line text if no timestamps
            print("No word timestamps available. Using line-by-line subtitles.")
            current_time = 0.0
            for line in script_lines:
                start_time = current_time
                end_time = current_time + duration_per_line

                text_action = AddText(
                    start_time=start_time + 0.5, # Add text slightly after the cut
                    end_time=end_time - 0.5,
                    text=line,
                    font_size=52,
                    position=('center', 'center')
                )
                edl.append(text_action)

                current_time = end_time

        # 3. Add audio - prioritize voiceover if it exists
        if project.voiceover_file and project.voiceover_file.exists():
            voiceover_action = AddAudio(
                start_time=0.0,
                end_time=project.target_duration,
                audio_file=str(project.voiceover_file),
                volume=1.0  # Voiceover should be at full volume
            )
            edl.insert(0, voiceover_action)
        else:
            # Fallback to background music if no voiceover was generated
            music_action = AddAudio(
                start_time=0.0,
                end_time=project.target_duration,
                audio_file="background_music.mp3",
                volume=0.3
            )
            edl.insert(0, music_action)

        # 4. Apply a consistent color grade over the entire video
        lut_action = ApplyLUT(
            start_time=0.0,
            end_time=project.target_duration,
            lut_file="cinematic_look.cube"
        )
        edl.insert(0, lut_action) # Add LUT at the beginning as well

        print(f"Generated an intelligent EDL with {len(edl)} actions.")
        return edl
