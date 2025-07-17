# creative/overlays.py
from moviepy.editor import TextClip, ColorClip, vfx
from config import CAPTION_STYLE

def create_hook_text(text: str, duration: float):
    """Creates a massive, screen-dominating text overlay to hook the viewer."""
    return TextClip(
        text,
        fontsize=100,
        color='white',
        font=CAPTION_STYLE['font'],
        stroke_color='black',
        stroke_width=5
    ).set_position('center').set_duration(duration)

def create_progress_bar(duration: float, screensize: tuple):
    """Creates a retention-boosting progress bar that animates across the screen."""
    w, _ = screensize
    bar = ColorClip(size=(1, 20), color=(255, 255, 0)).set_position(('left', 'bottom'))
    animated_bar = bar.fx(vfx.resize, width=lambda t: (t / duration) * w)
    return animated_bar.set_duration(duration)