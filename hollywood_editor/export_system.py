# In hollywood_editor/export_system.py

from pathlib import Path
from typing import List, Dict, Any

# MoviePy is used for the actual video rendering
from moviepy.editor import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeAudioClip,
)
from moviepy.video.fx.all import colorx

# Assuming project.py and actions.py are in the same directory
from .project import Project, Platform
from .actions import BaseAction, Cut, AddText, ApplyLUT, AddAudio


class ExportDeliverySystem:
    """
    Renders the final video based on an Edit Decision List (EDL)
    and handles platform-specific export settings.
    """

    def __init__(self):
        """Initializes with presets for different platforms."""
        self.export_presets: Dict[Platform, Dict[str, Any]] = {
            Platform.YOUTUBE_SHORTS: {
                "resolution": (1080, 1920),
                "fps": 30,
                "bitrate": "8000k",
                "codec": "libx264",
            },
            Platform.TIKTOK: {
                "resolution": (1080, 1920),
                "fps": 30,
                "bitrate": "8000k",
                "codec": "libx264",
            },
            Platform.INSTAGRAM_REEL: {
                "resolution": (1080, 1920),
                "fps": 30,
                "bitrate": "8000k",
                "codec": "libx264",
            },
            Platform.YOUTUBE: {
                "resolution": (1920, 1080),
                "fps": 30,
                "bitrate": "12000k",
                "codec": "libx264",
            },
        }

    def render_video(
        self, project: Project, edl: List[BaseAction], platform: Platform
    ) -> Path:
        """
        Renders a video for a specific platform using the provided EDL.

        This is a simplified rendering pipeline. A production system would
        handle errors, temporary files, and more complex effects.

        Args:
            project: The project object.
            edl: The Edit Decision List to execute.
            platform: The target platform for which to render.

        Returns:
            The path to the final rendered video file.
        """
        print(f"Starting render for {platform.value}...")
        preset = self.export_presets[platform]
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{project.project_id}_{platform.value}.mp4"

        # Separate actions by type
        cuts = [action for action in edl if isinstance(action, Cut)]
        texts = [action for action in edl if isinstance(action, AddText)]
        audios = [action for action in edl if isinstance(action, AddAudio)]
        luts = [action for action in edl if isinstance(action, ApplyLUT)]

        # --- Video Clip Assembly ---
        # In a real system, you'd need to have the source footage available.
        # We'll create placeholder clips for now.
        video_clips = []
        for cut in cuts:
            # Placeholder: create a black clip if the source file doesn't exist
            # In a real implementation, you would have downloaded stock footage here.
            try:
                clip = VideoFileClip(cut.source_file).subclip(
                    cut.source_start, cut.source_end
                )
            except Exception as e:
                print(f"Warning: Could not find {cut.source_file} (error: {e}). Using black clip.")
                duration = cut.end_time - cut.start_time
                clip = VideoFileClip("placeholder.mp4", audio=False).set_duration(duration)
            video_clips.append(clip)
        
        if not video_clips:
            print("Error: No video clips to render.")
            return None

        final_video = concatenate_videoclips(video_clips)

        # --- Text Overlay ---
        text_clips = []
        for text_action in texts:
            txt_clip = (
                TextClip(
                    text_action.text,
                    fontsize=text_action.font_size,
                    color=text_action.color,
                    size=final_video.size, # Use the main video's size
                    method="caption",
                )
                .set_position(text_action.position)
                .set_duration(text_action.end_time - text_action.start_time)
                .set_start(text_action.start_time)
            )
            text_clips.append(txt_clip)

        # --- New Audio Assembly Logic ---
        audio_tracks = []
        for audio_action in audios:
            try:
                audio_clip = AudioFileClip(audio_action.audio_file).volumex(audio_action.volume)
                audio_tracks.append(audio_clip)
            except Exception as e:
                print(f"Warning: Could not load audio file {audio_action.audio_file} (error: {e})")
        
        if audio_tracks:
            # Mix all audio tracks together
            final_audio = CompositeAudioClip(audio_tracks)
            final_video.audio = final_audio.set_duration(final_video.duration)


        # --- Effects ---
        if luts:
            # Apply the first LUT found in the plan
            lut_action = luts[0]
            try:
                final_video = final_video.fx(colorx.lut, lut_file=lut_action.lut_file)
            except Exception as e:
                print(f"Warning: Could not apply LUT {lut_action.lut_file} (error: {e})")

        # --- Composition ---
        # Combine video and text clips
        final_clip = CompositeVideoClip([final_video] + text_clips)

        # --- Final Render ---
        print(f"Writing final video to {output_path}...")
        final_clip.write_videofile(
            str(output_path),
            fps=preset["fps"],
            codec=preset["codec"],
            bitrate=preset["bitrate"],
            threads=4,
            preset="medium",
            logger='bar' 
        )
        print("✅ Render complete.")
        return output_path