# creative/transitions.py
from moviepy.editor import VideoFileClip, vfx
import numpy as np

def create_glitch_transition(clip, transition_time, duration=0.3):
    """Creates a glitch transition at the specified time."""
    def glitch_effect(get_frame, t):
        if transition_time <= t <= transition_time + duration:
            frame = get_frame(t)
            # Add glitch effects during transition
            progress = (t - transition_time) / duration
            intensity = np.sin(progress * np.pi)  # 0 to 1 to 0
            
            if np.random.random() < intensity * 0.5:
                # Random line displacement
                h, w = frame.shape[:2]
                displaced = frame.copy()
                for _ in range(int(intensity * 10)):
                    y = np.random.randint(0, h)
                    shift = np.random.randint(-int(w * 0.1), int(w * 0.1))
                    if shift != 0:
                        displaced[y] = np.roll(displaced[y], shift, axis=0)
                return displaced
        return get_frame(t)
    
    return clip.fl(glitch_effect)

def create_whip_pan_transition(clip, transition_time, duration=0.4):
    """Creates a whip pan transition effect."""
    def motion_blur_effect(get_frame, t):
        if transition_time <= t <= transition_time + duration:
            frame = get_frame(t)
            # Apply horizontal motion blur
            progress = (t - transition_time) / duration
            blur_intensity = 4 * progress * (1 - progress)  # Peaks in middle
            
            if blur_intensity > 0.1:
                # Simple horizontal blur simulation
                kernel_size = int(blur_intensity * 20) + 1
                if kernel_size > 1:
                    import cv2
                    kernel = np.ones((1, kernel_size)) / kernel_size
                    blurred = cv2.filter2D(frame, -1, kernel)
                    return blurred
        return get_frame(t)
    
    return clip.fl(motion_blur_effect)

def create_zoom_transition(clip, transition_time, duration=0.5):
    """Creates a zoom in/out transition."""
    def zoom_effect(t):
        if transition_time <= t <= transition_time + duration:
            progress = (t - transition_time) / duration
            # Zoom out then in
            zoom_factor = 1.0 + 0.3 * np.sin(progress * np.pi)
            return zoom_factor
        return 1.0
    
    return clip.resize(zoom_effect)