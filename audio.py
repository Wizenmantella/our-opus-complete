# audio.py
import whisper
import librosa
from project import VideoProject

class Audio:
    @staticmethod
    def transcribe(project: VideoProject):
        print("Transcribing audio...")
        model = whisper.load_model("base")
        result = model.transcribe(project.audio_path, word_timestamps=True)
        project.transcript = result
        print("Transcription complete.")

    @staticmethod
    def analyze_beats(project: VideoProject):
        print("Analyzing beats...")
        y, sr = librosa.load(project.audio_path)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        project.beat_times = beat_times.tolist()
        print(f"Beat analysis complete. Tempo: {tempo:.2f} BPM")