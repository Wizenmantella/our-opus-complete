# analysis/audio.py
import whisper
import librosa
import torch
from project import VideoProject

class AudioAnalyzer:
    """A static class for all audio analysis tasks."""

    @staticmethod
    def transcribe(project: VideoProject, model_name: str = "base", use_advanced: bool = True):
        """
        Transcribes the audio using Whisper to extract word-level truth.
        Leverages Apple Silicon's MPS for GPU acceleration.
        Now with optional advanced processing for Hollywood-level accuracy.
        """
        if use_advanced:
            from analysis.whisper_advanced import AdvancedWhisperProcessor
            processor = AdvancedWhisperProcessor()
            result = processor.advanced_transcribe(project, quality_priority="balanced")
            project.transcript = result["segments"]
            return
            
        # Fallback to basic transcription
        print("-> [Ears] Transcribing audio...")
        if not project.audio_path:
            raise ValueError("Audio path not set in project. Cannot transcribe.")

        device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"-> [Ears] Using device: {device.upper()} for transcription.")
        model = whisper.load_model(model_name, device=device)

        result = model.transcribe(
            project.audio_path,
            word_timestamps=True,
            verbose=False
        )
        project.transcript = result.get("segments", [])
        print("-> [Ears] Transcription complete.")

    @staticmethod
    def analyze_beats(project: VideoProject):
        """
        Analyzes the audio to find its soul: the beat.
        """
        print("-> [Ears] Analyzing audio beats...")
        if not project.audio_path:
            raise ValueError("Audio path not set in project. Cannot analyze beats.")

        y, sr = librosa.load(project.audio_path)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_timestamps = librosa.frames_to_time(beats, sr=sr)
        project.beat_timestamps = beat_timestamps.tolist()
        print(f"-> [Ears] Beat analysis complete. Found {len(beat_timestamps)} beats at ~{tempo:.2f} BPM.")