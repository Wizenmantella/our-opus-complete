#!/usr/bin/env python3
"""
Beat Sync Engine - Music-Driven Video Editing
Synchronizes cuts, effects, and transitions to music beats
"""

import numpy as np
import subprocess
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import json
import librosa
import librosa.display
import matplotlib.pyplot as plt

class BeatType(Enum):
    """Types of musical beats"""
    KICK = "kick"
    SNARE = "snare"
    HIHAT = "hihat"
    BASS_DROP = "bass_drop"
    BUILD_UP = "build_up"
    BREAK = "break"
    CHORUS = "chorus"

class SyncEffect(Enum):
    """Effects to sync with beats"""
    CUT = "cut"
    ZOOM_PUNCH = "zoom_punch"
    FLASH = "flash"
    SHAKE = "shake"
    GLITCH = "glitch"
    SPEED_RAMP = "speed_ramp"
    COLOR_SHIFT = "color_shift"
    TRANSITION = "transition"

@dataclass
class Beat:
    """Individual beat with properties"""
    timestamp: float
    strength: float
    beat_type: BeatType
    frequency: float = 0.0

@dataclass
class MusicSection:
    """Section of music with characteristics"""
    start_time: float
    end_time: float
    section_type: str  # intro, verse, chorus, bridge, outro
    energy_level: float
    bpm: float

@dataclass
class BeatSyncEdit:
    """Edit synced to beat"""
    beat_time: float
    effect: SyncEffect
    intensity: float
    duration: float
    params: Dict = None

class BeatDetectionEngine:
    """Detect beats and musical features"""
    
    def __init__(self):
        self.sample_rate = 22050
        self.hop_length = 512
        
    def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        """Comprehensive audio analysis for beat sync"""
        
        print(f"🎵 Analyzing audio: {audio_path}")
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=self.sample_rate)
        
        # Beat tracking
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
        beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=self.hop_length)
        
        # Onset detection (for all percussion hits)
        onset_frames = librosa.onset.onset_detect(
            y=y, sr=sr, hop_length=self.hop_length, 
            backtrack=True, units='frames'
        )
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=self.hop_length)
        
        # Spectral analysis for beat classification
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        
        # Energy analysis
        rms_energy = librosa.feature.rms(y=y)[0]
        
        # Detect bass drops and build-ups
        bass_drops = self._detect_bass_drops(y, sr)
        build_ups = self._detect_build_ups(rms_energy, beat_times)
        
        # Segment analysis
        segments = self._analyze_segments(y, sr, beat_times)
        
        # Create beat objects with classification
        classified_beats = self._classify_beats(
            beat_times, onset_times, spectral_centroids, 
            spectral_rolloff, rms_energy, bass_drops
        )
        
        return {
            "tempo": tempo,
            "beat_times": beat_times.tolist(),
            "onset_times": onset_times.tolist(),
            "classified_beats": classified_beats,
            "bass_drops": bass_drops,
            "build_ups": build_ups,
            "segments": segments,
            "energy_profile": rms_energy.tolist(),
            "duration": len(y) / sr
        }
    
    def _detect_bass_drops(self, y: np.ndarray, sr: int) -> List[Dict]:
        """Detect bass drops in audio"""
        
        # Low frequency energy
        y_bass = librosa.effects.remix(y, intervals=[(0, len(y))], align_zeros=False)
        
        # Apply low-pass filter for bass frequencies
        from scipy import signal
        b, a = signal.butter(4, 200 / (sr / 2), 'low')
        y_bass_filtered = signal.filtfilt(b, a, y)
        
        # Calculate bass energy
        bass_energy = librosa.feature.rms(y=y_bass_filtered)[0]
        
        # Find sudden increases in bass energy
        bass_diff = np.diff(bass_energy)
        threshold = np.percentile(bass_diff, 95)
        
        bass_drops = []
        for i, diff in enumerate(bass_diff):
            if diff > threshold:
                time = librosa.frames_to_time(i, sr=sr, hop_length=self.hop_length)
                bass_drops.append({
                    "time": float(time),
                    "intensity": float(diff / threshold),
                    "type": "bass_drop"
                })
        
        return bass_drops
    
    def _detect_build_ups(self, rms_energy: np.ndarray, beat_times: np.ndarray) -> List[Dict]:
        """Detect build-up sections"""
        
        build_ups = []
        window_size = 50  # frames
        
        for i in range(len(rms_energy) - window_size):
            window = rms_energy[i:i + window_size]
            
            # Check for increasing energy
            if all(window[j] <= window[j + 1] for j in range(len(window) - 1)):
                start_time = i * self.hop_length / self.sample_rate
                end_time = (i + window_size) * self.hop_length / self.sample_rate
                
                build_ups.append({
                    "start": float(start_time),
                    "end": float(end_time),
                    "type": "build_up",
                    "energy_increase": float(window[-1] / window[0])
                })
        
        return build_ups
    
    def _classify_beats(self, beat_times: np.ndarray, onset_times: np.ndarray,
                       spectral_centroids: np.ndarray, spectral_rolloff: np.ndarray,
                       rms_energy: np.ndarray, bass_drops: List[Dict]) -> List[Beat]:
        """Classify beats by type"""
        
        classified_beats = []
        
        for beat_time in beat_times:
            # Find nearest frame
            frame = librosa.time_to_frames(beat_time, sr=self.sample_rate, hop_length=self.hop_length)
            
            if frame < len(spectral_centroids):
                centroid = spectral_centroids[frame]
                energy = rms_energy[frame] if frame < len(rms_energy) else 0
                
                # Classify based on frequency content
                if centroid < 200:  # Low frequency - likely kick
                    beat_type = BeatType.KICK
                elif 200 <= centroid < 1000:  # Mid frequency - likely snare
                    beat_type = BeatType.SNARE
                else:  # High frequency - likely hihat
                    beat_type = BeatType.HIHAT
                
                # Check if it's a bass drop
                for drop in bass_drops:
                    if abs(beat_time - drop["time"]) < 0.1:
                        beat_type = BeatType.BASS_DROP
                        break
                
                beat = Beat(
                    timestamp=float(beat_time),
                    strength=float(energy),
                    beat_type=beat_type,
                    frequency=float(centroid)
                )
                
                classified_beats.append(beat)
        
        return classified_beats
    
    def _analyze_segments(self, y: np.ndarray, sr: int, beat_times: np.ndarray) -> List[MusicSection]:
        """Analyze music segments (verse, chorus, etc.)"""
        
        # Use spectral features to detect sections
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        
        # Simple segmentation based on chroma changes
        segments = []
        segment_length = sr * 8  # 8-second segments
        
        for i in range(0, len(y), segment_length):
            start_time = i / sr
            end_time = min((i + segment_length) / sr, len(y) / sr)
            
            # Calculate segment energy
            segment_audio = y[i:i + segment_length]
            segment_energy = np.mean(librosa.feature.rms(y=segment_audio))
            
            # Estimate BPM for segment
            segment_tempo, _ = librosa.beat.beat_track(y=segment_audio, sr=sr)
            
            # Simple classification
            if segment_energy > 0.1:
                section_type = "chorus"
            elif segment_energy > 0.05:
                section_type = "verse"
            else:
                section_type = "intro" if i == 0 else "bridge"
            
            section = MusicSection(
                start_time=float(start_time),
                end_time=float(end_time),
                section_type=section_type,
                energy_level=float(segment_energy),
                bpm=float(segment_tempo)
            )
            
            segments.append(section)
        
        return segments


class BeatSyncEditor:
    """Create beat-synchronized edits"""
    
    def __init__(self):
        self.beat_detector = BeatDetectionEngine()
        self.effect_mappings = self._create_effect_mappings()
    
    def _create_effect_mappings(self) -> Dict[BeatType, List[SyncEffect]]:
        """Map beat types to appropriate effects"""
        
        return {
            BeatType.KICK: [SyncEffect.CUT, SyncEffect.ZOOM_PUNCH, SyncEffect.FLASH],
            BeatType.SNARE: [SyncEffect.SHAKE, SyncEffect.TRANSITION, SyncEffect.GLITCH],
            BeatType.HIHAT: [SyncEffect.COLOR_SHIFT, SyncEffect.SPEED_RAMP],
            BeatType.BASS_DROP: [SyncEffect.ZOOM_PUNCH, SyncEffect.GLITCH, SyncEffect.FLASH],
            BeatType.BUILD_UP: [SyncEffect.SPEED_RAMP, SyncEffect.COLOR_SHIFT],
            BeatType.BREAK: [SyncEffect.TRANSITION, SyncEffect.GLITCH],
            BeatType.CHORUS: [SyncEffect.CUT, SyncEffect.ZOOM_PUNCH]
        }
    
    def create_beat_sync_edits(self, audio_analysis: Dict, video_duration: float) -> List[BeatSyncEdit]:
        """Create edit decisions based on beat analysis"""
        
        edits = []
        
        # Process classified beats
        for beat in audio_analysis["classified_beats"]:
            # Skip beats beyond video duration
            if beat.timestamp > video_duration:
                continue
            
            # Select appropriate effect based on beat type
            possible_effects = self.effect_mappings.get(beat.beat_type, [SyncEffect.CUT])
            effect = np.random.choice(possible_effects)
            
            # Calculate effect intensity based on beat strength
            intensity = min(beat.strength * 2, 1.0)
            
            # Create edit
            edit = BeatSyncEdit(
                beat_time=beat.timestamp,
                effect=effect,
                intensity=intensity,
                duration=0.1 if effect != SyncEffect.TRANSITION else 0.5,
                params=self._get_effect_params(effect, beat)
            )
            
            edits.append(edit)
        
        # Add special edits for bass drops
        for drop in audio_analysis["bass_drops"]:
            if drop["time"] <= video_duration:
                edit = BeatSyncEdit(
                    beat_time=drop["time"],
                    effect=SyncEffect.ZOOM_PUNCH,
                    intensity=min(drop["intensity"], 1.0),
                    duration=0.3,
                    params={"zoom_amount": 1.5 + drop["intensity"] * 0.5}
                )
                edits.append(edit)
        
        # Add speed ramps for build-ups
        for buildup in audio_analysis["build_ups"]:
            if buildup["start"] <= video_duration:
                edit = BeatSyncEdit(
                    beat_time=buildup["start"],
                    effect=SyncEffect.SPEED_RAMP,
                    intensity=0.8,
                    duration=buildup["end"] - buildup["start"],
                    params={"speed_factor": 0.5, "ramp_type": "exponential"}
                )
                edits.append(edit)
        
        # Sort edits by time
        edits.sort(key=lambda x: x.beat_time)
        
        return edits
    
    def _get_effect_params(self, effect: SyncEffect, beat: Beat) -> Dict:
        """Get parameters for specific effect"""
        
        params = {}
        
        if effect == SyncEffect.ZOOM_PUNCH:
            params["zoom_amount"] = 1.2 + beat.strength * 0.3
            params["zoom_duration"] = 0.1
            
        elif effect == SyncEffect.SHAKE:
            params["shake_intensity"] = 5 + beat.strength * 15
            params["shake_frequency"] = 50
            
        elif effect == SyncEffect.GLITCH:
            params["glitch_intensity"] = beat.strength
            params["glitch_type"] = "digital" if beat.beat_type == BeatType.SNARE else "analog"
            
        elif effect == SyncEffect.COLOR_SHIFT:
            params["hue_shift"] = beat.frequency / 1000 * 180  # Map frequency to hue
            params["saturation_boost"] = 1.2
            
        elif effect == SyncEffect.SPEED_RAMP:
            params["speed_factor"] = 0.5 if beat.strength < 0.5 else 2.0
            params["ramp_type"] = "linear"
            
        elif effect == SyncEffect.FLASH:
            params["flash_color"] = "white"
            params["flash_opacity"] = beat.strength
            
        return params
    
    def generate_ffmpeg_filters(self, edits: List[BeatSyncEdit], video_duration: float) -> str:
        """Generate FFmpeg filter string for beat-synced edits"""
        
        filters = []
        
        for edit in edits:
            if edit.effect == SyncEffect.ZOOM_PUNCH:
                zoom = edit.params.get("zoom_amount", 1.3)
                filter_str = (
                    f"zoompan=z='if(between(t\\,{edit.beat_time}\\,{edit.beat_time + edit.duration})\\,"
                    f"{zoom}\\,1)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                )
                filters.append(filter_str)
                
            elif edit.effect == SyncEffect.SHAKE:
                intensity = edit.params.get("shake_intensity", 10)
                filter_str = (
                    f"crop=in_w:in_h:"
                    f"if(between(t\\,{edit.beat_time}\\,{edit.beat_time + edit.duration})\\,"
                    f"sin(t*100)*{intensity}\\,0):"
                    f"if(between(t\\,{edit.beat_time}\\,{edit.beat_time + edit.duration})\\,"
                    f"cos(t*100)*{intensity}\\,0)"
                )
                filters.append(filter_str)
                
            elif edit.effect == SyncEffect.FLASH:
                opacity = edit.params.get("flash_opacity", 0.8)
                filter_str = (
                    f"fade=enable='between(t\\,{edit.beat_time}\\,{edit.beat_time + 0.05})':"
                    f"s=in:d=0.05:alpha=0:c=white"
                )
                filters.append(filter_str)
                
            elif edit.effect == SyncEffect.GLITCH:
                filter_str = (
                    f"rgbashift=rh=if(between(t\\,{edit.beat_time}\\,{edit.beat_time + edit.duration})\\,5\\,0):"
                    f"gh=if(between(t\\,{edit.beat_time}\\,{edit.beat_time + edit.duration})\\,-5\\,0)"
                )
                filters.append(filter_str)
                
            elif edit.effect == SyncEffect.COLOR_SHIFT:
                hue = edit.params.get("hue_shift", 30)
                filter_str = (
                    f"hue=h=if(between(t\\,{edit.beat_time}\\,{edit.beat_time + edit.duration})\\,"
                    f"{hue}\\,0)"
                )
                filters.append(filter_str)
        
        return ",".join(filters) if filters else "null"


class MusicVideoSync:
    """Main class for music-video synchronization"""
    
    def __init__(self):
        self.beat_editor = BeatSyncEditor()
    
    def sync_video_to_music(self, video_path: str, audio_path: str, 
                           output_path: str, sync_intensity: float = 0.8) -> bool:
        """Sync video edits to music beats"""
        
        print("🎵 Syncing video to music beats...")
        
        # Extract audio if needed
        if not audio_path:
            audio_path = self._extract_audio(video_path)
        
        # Analyze audio
        audio_analysis = self.beat_editor.beat_detector.analyze_audio(audio_path)
        
        # Get video duration
        video_duration = self._get_video_duration(video_path)
        
        # Create beat-synced edits
        edits = self.beat_editor.create_beat_sync_edits(audio_analysis, video_duration)
        
        # Filter by intensity
        edits = [e for e in edits if e.intensity >= (1 - sync_intensity)]
        
        print(f"  📍 Found {len(audio_analysis['beat_times'])} beats")
        print(f"  🎯 Creating {len(edits)} synchronized edits")
        print(f"  💥 Detected {len(audio_analysis['bass_drops'])} bass drops")
        
        # Generate filters
        filters = self.beat_editor.generate_ffmpeg_filters(edits, video_duration)
        
        # Apply edits
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-vf", filters,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  ✅ Beat-synced video created: {output_path}")
                
                # Save edit decision list
                self._save_edit_decisions(edits, output_path.replace('.mp4', '_edits.json'))
                
                return True
            else:
                print(f"  ❌ Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  ❌ Processing error: {e}")
            return False
    
    def _extract_audio(self, video_path: str) -> str:
        """Extract audio from video"""
        
        audio_path = video_path.replace('.mp4', '_audio.wav')
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "22050", "-ac", "1",
            audio_path
        ]
        
        subprocess.run(cmd, capture_output=True)
        return audio_path
    
    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration"""
        
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            return float(data["format"]["duration"])
        except:
            return 30.0  # Default fallback
    
    def _save_edit_decisions(self, edits: List[BeatSyncEdit], output_path: str):
        """Save edit decisions for review"""
        
        edit_data = []
        for edit in edits:
            edit_data.append({
                "time": edit.beat_time,
                "effect": edit.effect.value,
                "intensity": edit.intensity,
                "duration": edit.duration,
                "params": edit.params
            })
        
        with open(output_path, 'w') as f:
            json.dump({
                "edits": edit_data,
                "total_edits": len(edit_data),
                "effects_used": list(set(e.effect.value for e in edits))
            }, f, indent=2)
        
        print(f"  📄 Edit decisions saved: {output_path}")


def demo_beat_sync():
    """Demo beat sync capabilities"""
    
    print("🎵 Beat Sync Engine Demo")
    print("\nCapabilities:")
    print("- Automatic beat detection")
    print("- Beat classification (kick, snare, hihat)")
    print("- Bass drop detection")
    print("- Build-up detection")
    print("- Music section analysis")
    print("- Synchronized effects:")
    for effect in SyncEffect:
        print(f"  • {effect.value}")
    
    print("\nExample beat-synced edits:")
    example_edits = [
        {"time": 0.5, "effect": "zoom_punch", "beat": "kick"},
        {"time": 1.0, "effect": "shake", "beat": "snare"},
        {"time": 2.5, "effect": "glitch", "beat": "bass_drop"},
        {"time": 4.0, "effect": "speed_ramp", "beat": "build_up"}
    ]
    print(json.dumps(example_edits, indent=2))


if __name__ == "__main__":
    demo_beat_sync()