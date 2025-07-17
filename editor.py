# editor.py
import os
from moviepy.editor import VideoFileClip

from project import VideoProject
from analysis.audio import AudioAnalyzer
from analysis.vision import VisionAnalyzer
from director import Director
from composer import Composer

class Editor:
    """
    The main orchestrator for the video editing pipeline.
    """
    def __init__(self, video_path: str, style_name: str, output_path: str = None):
        if not output_path:
            name, ext = os.path.splitext(video_path)
            output_path = f"{name}_edited{ext}"
        
        self.project = VideoProject(
            video_path=video_path,
            style_name=style_name,
            output_path=output_path
        )

    def _prepare_project(self):
        """Initializes the project by loading the video and extracting audio."""
        print("--- Preparing Project ---")
        self.project.clip = VideoFileClip(self.project.video_path)
        
        audio_path = "temp_audio.wav"
        self.project.clip.audio.write_audiofile(audio_path, codec='pcm_s16le', verbose=False, logger=None)
        self.project.audio_path = audio_path
        print("-> Project prepared successfully.")

    def run_pipeline(self):
        """
        Runs the entire editing pipeline from start to finish.
        """
        try:
            self._prepare_project()

            print("\n--- Phase 1: Analysis ---")
            AudioAnalyzer.transcribe(self.project)
            AudioAnalyzer.analyze_beats(self.project)
            VisionAnalyzer.analyze_scenes(self.project)

            print("\n--- Phase 2: Direction ---")
            director = Director(self.project)
            director.generate_edit_plan()

            print("\n--- Phase 3: Composition & Rendering ---")
            composer = Composer(self.project)
            final_video = composer.build_video()
            composer.render(final_video)

        finally:
            # Clean up temporary files
            if self.project.audio_path and os.path.exists(self.project.audio_path):
                os.remove(self.project.audio_path)
            if self.project.clip:
                self.project.clip.close()
            print("\n--- Pipeline Finished ---")