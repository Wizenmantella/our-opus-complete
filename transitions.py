# transitions.py
import moviepy.editor as mp
import numpy as np

def create_glitch_transition(clip, transition_time, duration=0.3):
    """Creates a glitch transition at the specified time."""
    def glitch_transition_effect(get_frame, t):
        if transition_time <= t <= transition_time + duration:
            frame = get_frame(t)
            h, w = frame.shape[:2]
            
            # Intensity increases then decreases
            progress = (t - transition_time) / duration
            intensity = np.sin(progress * np.pi)  # 0 to 1 to 0
            
            glitched = frame.copy()
            num_lines = int(intensity * 20)
            
            for _ in range(num_lines):
                y = np.random.randint(0, h)
                shift = np.random.randint(-int(w * 0.3), int(w * 0.3))
                
                if shift > 0 and shift < w:
                    glitched[y, shift:] = frame[y, :-shift]
                elif shift < 0 and abs(shift) < w:
                    glitched[y, :shift] = frame[y, -shift:]
            
            # Random color channel corruption
            if np.random.random() < intensity:
                channel = np.random.randint(0, 3)
                glitched[:, :, channel] = np.roll(glitched[:, :, channel], 
                                                np.random.randint(-10, 11), axis=1)
            
            return glitched
        return get_frame(t)
    
    return clip.fl(glitch_transition_effect)

def create_whip_pan_transition(clip, transition_time, duration=0.4):
    """Creates a whip pan transition effect."""
    def whip_pan_effect(get_frame, t):
        if transition_time <= t <= transition_time + duration:
            frame = get_frame(t)
            
            # Motion blur effect
            progress = (t - transition_time) / duration
            blur_intensity = 4 * progress * (1 - progress)  # Peaks in middle
            
            if blur_intensity > 0.1:
                import cv2
                kernel_size = int(blur_intensity * 30) + 1
                if kernel_size % 2 == 0:
                    kernel_size += 1
                
                # Horizontal motion blur
                kernel = np.zeros((kernel_size, kernel_size))
                kernel[kernel_size // 2, :] = 1.0
                kernel = kernel / kernel_size
                
                blurred = cv2.filter2D(frame, -1, kernel)
                return blurred
            
        return get_frame(t)
    
    return clip.fl(whip_pan_effect)

def create_zoom_transition(clip, transition_time, duration=0.5):
    """Creates a zoom in/out transition."""
    def zoom_transition_effect(t):
        if transition_time <= t <= transition_time + duration:
            progress = (t - transition_time) / duration
            # Zoom out then in
            zoom_factor = 1.0 + 0.3 * np.sin(progress * np.pi)
            return zoom_factor
        return 1.0
    
    return clip.resize(zoom_transition_effect)