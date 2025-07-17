# analysis/vision.py
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images

from project import VideoProject

class VisionAnalyzer:
    """A static class for all video analysis tasks."""

    @staticmethod
    def analyze_scenes(project: VideoProject):
        """
        Analyzes the video to find scene cuts using PySceneDetect.
        Stores the scene cut timestamps in the project object.
        """
        print("-> Analyzing video for scene changes...")
        video = open_video(project.video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector())
        scene_manager.detect_scenes(video, show_progress=True)
        scene_list = scene_manager.get_scene_list()

        # Get timestamps for each scene cut
        scene_timestamps = [scene[1].get_seconds() for scene in scene_list if scene[1].get_seconds() > 0]
        project.scene_timestamps = scene_timestamps
        print(f"-> Scene analysis complete. Found {len(scene_timestamps)} scene cuts.")