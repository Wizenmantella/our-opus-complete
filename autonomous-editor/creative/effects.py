# creative/effects.py
from moviepy.editor import vfx
import random

def apply_zoom_punch(clip, intensity=1.15):
    """Applies a dynamic zoom-in effect to the center of the clip."""
    # This creates a function that calculates the size at any given time t
    def resize_func(t):
        # A simple parabola that peaks at the clip's midpoint
        return 1 + (intensity - 1) * (1 - 4 * (t / clip.duration - 0.5)**2)

    return clip.fx(vfx.resize, resize_func).set_position(('center', 'center'))

def apply_screen_shake(clip, intensity=10):
    """Applies a screen shake effect by rapidly changing the clip's position."""
    # This creates a function that returns a random position offset at any given time t
    def position_func(t):
        return (random.uniform(-intensity, intensity), random.uniform(-intensity, intensity))

    return clip.set_position(position_func)

def apply_speed_ramp(clip, ramp_points):
    """
    Applies a speed ramp to a clip.
    ramp_points is a list of (time, speed_multiplier) tuples.
    e.g., [(0, 1), (2, 4), (3, 1)] will play normal, speed up to 4x at 2s, then return to normal at 3s.
    """
    print("-> [Creative] Applying speed ramp.")
    # The speedx function in moviepy can take a function of time
    # This requires a more complex implementation to map out the speed curve
    # based on the ramp_points. For now, we'll use a simple constant speed up.
    final_speed = ramp_points[0][1] if ramp_points else 2
    return clip.fx(vfx.speedx, final_speed)

def apply_beat_zoom(clip, beat_timestamps, zoom_intensity=1.2, zoom_duration=0.2):
    """
    Applies quick zoom punches synchronized to detected audio beats.
    This creates audio-reactive visual effects.
    """
    print(f"-> [Creative] Applying beat-synchronized zoom to {len(beat_timestamps)} beats.")
    
    def beat_zoom_func(t):
        # Check if current time is near any beat timestamp
        for beat_time in beat_timestamps:
            if abs(t - beat_time) <= zoom_duration / 2:
                # Apply zoom effect near beat
                beat_progress = abs(t - beat_time) / (zoom_duration / 2)
                zoom_factor = 1 + (zoom_intensity - 1) * (1 - beat_progress)
                return zoom_factor
        return 1.0  # Normal size when not near a beat
    
    return clip.fx(vfx.resize, beat_zoom_func).set_position(('center', 'center'))