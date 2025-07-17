# creative/overlays.py
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, vfx
from config import CAPTION_STYLE

def create_hook_text(text: str, duration: float, screensize: tuple):
    """Creates a large, impactful text overlay for the start of the video."""
    return TextClip(
        text,
        fontsize=100,
        color='white',
        font=CAPTION_STYLE['font'],
        stroke_color='black',
        stroke_width=5
    ).set_position('center').set_duration(duration)

def create_progress_bar(duration: float, screensize: tuple):
    """Creates a progress bar that animates across the screen."""
    w, h = screensize
    bar = ColorClip(size=(1, 20), color=(255, 255, 0)).set_position(('left', 'bottom'))
    animated_bar = bar.fx(vfx.resize, width=lambda t: (t / duration) * w)
    return animated_bar.set_duration(duration)

def create_animated_emoji(emoji: str, duration: float):
    """Creates a pop-up emoji animation."""
    # This requires a font that supports the emoji.
    emoji_clip = TextClip(emoji, fontsize=150).set_duration(duration)
    # Add animation (e.g., pop-in and fade-out)
    return emoji_clip.resize(lambda t: 1 + 0.2 * (1 - 4 * (t - 0.5)**2)).set_opacity(lambda t: min(1, 5 * (duration - t)))

def create_engagement_overlay(text: str, duration: float, position: str = 'center'):
    """Creates engaging text overlays like 'FIRE!' or 'INSANE!'"""
    return TextClip(
        text,
        fontsize=80,
        color='yellow',
        font='Arial-Bold',
        stroke_color='red',
        stroke_width=3
    ).set_position(position).set_duration(duration)