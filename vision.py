# vision.py
from scenedetect import detect, ContentDetector
from project import VideoProject

class Vision:
    @staticmethod
    def analyze_scenes(project: VideoProject):
        print("Analyzing scenes...")
        scene_list = detect(project.video_path, ContentDetector())
        # Get timestamps in seconds
        project.scene_cuts = [scene[1].get_seconds() for scene in scene_list]
        print(f"Found {len(project.scene_cuts)} scene cuts")