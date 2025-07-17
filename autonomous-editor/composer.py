# composer.py
import os
from moviepy.editor import (
    CompositeVideoClip,
    AudioFileClip,
    concatenate_videoclips,
    VideoFileClip,
)
from tqdm import tqdm
from project import VideoProject
from creative import captions, overlays, effects, transitions
from config import STYLE_PROFILES
from assets.asset_manager import AssetManager


class Composer:
    """
    The Composer takes the Director's edit plan and assembles the final video
    by processing each segment individually and then concatenating them.
    """

    def __init__(self, project: VideoProject):
        self.project = project
        self.asset_manager = AssetManager()
        self.style = STYLE_PROFILES[project.style_name]

    def build_video(self) -> CompositeVideoClip:
        """
        Executes the edit plan to construct the final video clip.
        """
        print("-> [Assembly] The Composer is building the final video...")
        if not self.project.clip:
            raise ValueError("Project clip not loaded.")

        processed_clips = []
        global_overlays = []

        # First, separate global overlays from segment-based actions
        plan_segments = [
            p for p in self.project.edit_plan if p.get("action") != "add_global_overlay"
        ]
        plan_globals = [
            p for p in self.project.edit_plan if p.get("action") == "add_global_overlay"
        ]

        for action in plan_globals:
            if action["type"] == "hook_text":
                clip = overlays.create_hook_text(action["text"], action["duration"])
                global_overlays.append(clip)
            elif action["type"] == "progress_bar":
                clip = overlays.create_progress_bar(
                    action["duration"], self.project.clip.size
                )
                global_overlays.append(clip.set_start(0))

        # Process each segment from the director's plan
        for segment_plan in tqdm(plan_segments, desc="Composing Segments"):
            try:  # <--- START OF ROBUSTNESS BLOCK
                start = segment_plan["start"]
                end = segment_plan["end"]

                # Cut the original clip to get the current segment
                sub_clip = self.project.clip.subclip(start, end)

                # Apply effects to this segment
                for effect_name in segment_plan.get("effects", []):
                    if effect_name == "zoom_punch":
                        sub_clip = effects.apply_zoom_punch(
                            sub_clip, self.style["zoom_intensity"]
                        )
                    elif effect_name == "screen_shake":
                        sub_clip = effects.apply_screen_shake(
                            sub_clip, self.style["shake_intensity"]
                        )

                # Add captions for this specific segment
                segment_captions = captions.generate_caption_clips(
                    self.project, start, end
                )

                # Composite the captions onto the sub_clip
                if segment_captions:
                    sub_clip = CompositeVideoClip([sub_clip] + segment_captions)

                processed_clips.append(sub_clip)

            except Exception as e:  # <--- CATCH THE FAILURE
                print(f"\n[WARNING] Failed to process segment from {segment_plan['start']:.2f}s to {segment_plan['end']:.2f}s. Error: {e}. Skipping.")
                # Append the original, unprocessed sub_clip to maintain timeline continuity
                try:
                    fallback_clip = self.project.clip.subclip(segment_plan["start"], segment_plan["end"])
                    processed_clips.append(fallback_clip)
                    print(f"-> [Recovery] Using original unprocessed segment as fallback.")
                except Exception as fallback_error:
                    print(f"[ERROR] Complete failure on segment {segment_plan['start']:.2f}s-{segment_plan['end']:.2f}s: {fallback_error}")
                    # Continue without this segment to prevent total failure

        # Concatenate all the processed sub-clips into a single timeline
        if not processed_clips:
             # If no segments were processed, use the original clip
            final_timeline = self.project.clip
        else:
            final_timeline = concatenate_videoclips(processed_clips)

        # Composite the global overlays on top of the final timeline
        final_video = CompositeVideoClip([final_timeline] + global_overlays)

        # Re-attach the original audio to ensure perfect sync
        if self.project.audio_path:
            original_audio = AudioFileClip(self.project.audio_path)
            # Ensure audio does not exceed the final video's duration
            final_audio = original_audio.subclip(0, final_video.duration)
            final_video = final_video.set_audio(final_audio)

        return final_video

    def render(self, final_clip: CompositeVideoClip):
        """
        Renders the final video clip to a file with optimized settings.
        """
        print("-> [Assembly] Rendering final video...")
        if not self.project.output_path:
            raise ValueError("Output path not set.")

        final_clip.write_videofile(
            self.project.output_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            threads=os.cpu_count(),  # Utilize all available CPU cores
            preset="medium",  # A superior balance of speed and quality
        )
        print(f"-> [Assembly] Final video saved to: {self.project.output_path}")