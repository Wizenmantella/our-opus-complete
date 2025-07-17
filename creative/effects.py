# creative/effects.py
from moviepy.editor import vfx
import numpy as np

def apply_zoom_punch(clip, zoom_intensity=1.1):
    """Applies a quick zoom-in effect."""
    # This is a simplified implementation. A true punch requires more complex keyframing.
    zoomed_clip = clip.fx(vfx.resize, newsize=lambda t: 1 + (zoom_intensity - 1) * (1 - 4 * (t - 0.5)**2))
    return zoomed_clip.set_position(('center', 'center'))

def apply_screen_shake(clip, intensity=5):
    """Applies a screen shake effect."""
    def shake(t):
        import random
        dx = intensity * random.uniform(-1, 1)
        dy = intensity * random.uniform(-1, 1)
        return (dx, dy)
    return clip.set_position(shake)

def apply_rgb_split(clip, strength=5):
    """Applies an RGB split/chromatic aberration effect."""
    # This requires separating channels, which is complex in moviepy.
    # A simpler approach is to overlay slightly shifted color versions.
    # For now, this is a placeholder for a more advanced implementation.
    print("Warning: RGB split effect is a placeholder and not fully implemented.")
    return clip

def apply_speed_ramp(clip, speed_factor=2.0):
    """Applies a speed ramp (fast forward)."""
    return clip.fx(vfx.speedx, factor=speed_factor)

def apply_glitch_effect(clip, intensity=0.5):
    """Applies a digital glitch effect."""
    def glitch_frame(get_frame, t):
        frame = get_frame(t)
        if np.random.random() < intensity:
            # Add some random noise or corruption
            h, w = frame.shape[:2]
            noise = np.random.randint(0, 50, size=(h, w, 3), dtype=np.uint8)
            return np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return frame
    
    return clip.fl(glitch_frame)