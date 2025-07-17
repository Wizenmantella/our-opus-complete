# analysis/audio.py
import whisper
import librosa
import soundfile as sf
import os
from tqdm import tqdm

from project import VideoProject

class AudioAnalyzer:
    """A static class for all audio analysis tasks."""
    
    @staticmethod
    def transcribe(project: VideoProject, model_name: str = "base"):
        """
        Transcribes the audio of the video using Whisper.
        Stores word-level timestamps in the project object.
        """
        print("-> Starting audio transcription...")
        if not project.audio_path:
            raise ValueError("Audio path not set in project.")

        model = whisper.load_model(model_name)
        result = model.transcribe(
            project.audio_path,
            word_timestamps=True,
            verbose=False
        )
        project.transcript = result["segments"]
        print("-> Transcription complete.")

    @staticmethod
    def analyze_beats(project: VideoProject):
        """
        Analyzes the audio to find beat timestamps using Librosa.
        Stores the beat timestamps in the project object.
        """
        print("-> Analyzing audio beats...")
        if not project.audio_path:
            raise ValueError("Audio path not set in project.")

        y, sr = librosa.load(project.audio_path)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_timestamps = librosa.frames_to_time(beats, sr=sr)
        project.beat_timestamps = beat_timestamps.tolist()
        print(f"-> Beat analysis complete. Found {len(beat_timestamps)} beats at ~{tempo:.2f} BPM.")