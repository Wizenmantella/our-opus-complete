# composer.py
from moviepy.editor import CompositeVideoClip, AudioFileClip
from tqdm import tqdm

from project import VideoProject
from creative import captions, overlays, effects

class Composer:
    """
    The Composer takes the edit plan and assembles the final video.
    """
    def __init__(self, project: VideoProject):
        self.project = project

    def build_video(self):
        """
        Executes the edit plan to create the final video clip.
        """
        print("-> The Composer is building the final video...")
        final_clips = [self.project.clip]

        # Process the edit plan
        for action in tqdm(self.project.edit_plan, desc="Executing Edit Plan"):
            action_type = action['action']
            
            if action_type == 'add_captions':
                caption_clips = captions.generate_caption_clips(self.project, self.project.clip.size)
                final_clips.extend(caption_clips)

            elif action_type == 'add_overlay':
                overlay_type = action['type']
                if overlay_type == 'hook_text':
                    clip = overlays.create_hook_text(action['text'], action['duration'], self.project.clip.size)
                    final_clips.append(clip.set_start(action['time']))
                elif overlay_type == 'progress_bar':
                    clip = overlays.create_progress_bar(action['duration'], self.project.clip.size)
                    final_clips.append(clip.set_start(action['time']))
                elif overlay_type == 'engagement_text':
                    clip = overlays.create_engagement_overlay(action['text'], action['duration'])
                    final_clips.append(clip.set_start(action['time']))

            # Note: Applying effects and transitions directly is complex.
            # A more robust system would slice the main clip and apply effects to those slices.
            # This is a simplified implementation for clarity.
            elif action_type == 'apply_effect':
                effect_type = action['type']
                if effect_type == 'zoom_punch':
                    # Apply zoom punch effect to main clip
                    self.project.clip = effects.apply_zoom_punch(
                        self.project.clip, 
                        zoom_intensity=1.15
                    )
                elif effect_type == 'screen_shake':
                    # Apply screen shake effect
                    self.project.clip = effects.apply_screen_shake(
                        self.project.clip,
                        intensity=8
                    )
                elif effect_type == 'glitch':
                    # Apply glitch effect
                    self.project.clip = effects.apply_glitch_effect(
                        self.project.clip,
                        intensity=0.3
                    )
                print(f"Applied effect {effect_type} at {action['time']} seconds")

            elif action_type == 'apply_transition':
                print(f"Applying transition {action['type']} at {action['time']} (feature in development)")

        # Composite everything together
        final_video = CompositeVideoClip(final_clips, size=self.project.clip.size)
        
        # Re-attach the original audio
        if self.project.audio_path:
            original_audio = AudioFileClip(self.project.audio_path)
            final_video = final_video.set_audio(original_audio)

        return final_video

    def render(self, final_clip):
        """
        Renders the final video clip to a file.
        """
        print("-> Rendering final video...")
        final_clip.write_videofile(
            self.project.output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            threads=8,  # Use multiple threads for faster rendering
            preset='medium'  # A good balance of speed and quality
        )
        print(f"-> Final video saved to: {self.project.output_path}")