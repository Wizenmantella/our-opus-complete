# effects.py
import moviepy.editor as mp
import numpy as np

def apply_zoom_punch(clip, start_time, duration=0.2, strength=1.1):
    """Zooms in and out quickly."""
    def zoom_effect(t):
        if start_time <= t <= start_time + duration:
            progress = (t - start_time) / duration
            # Create a punch effect that peaks in the middle
            zoom_factor = 1 + (strength - 1) * np.sin(np.pi * progress)
            return zoom_factor
        return 1.0
    
    return clip.resize(zoom_effect)

def apply_rgb_split(clip, start_time, duration=0.3, strength=5):
    """Creates a chromatic aberration effect."""
    def rgb_split_effect(get_frame, t):
        if start_time <= t <= start_time + duration:
            frame = get_frame(t)
            h, w, c = frame.shape
            
            # Create offset versions
            red_frame = np.zeros_like(frame)
            blue_frame = np.zeros_like(frame)
            
            # Shift red channel right
            if strength < w:
                red_frame[:, strength:, 0] = frame[:, :-strength, 0]
                red_frame[:, :, 1:] = frame[:, :, 1:]  # Keep green and blue
            
            # Shift blue channel left  
            if strength < w:
                blue_frame[:, :-strength, 2] = frame[:, strength:, 2]
                blue_frame[:, :, :2] = frame[:, :, :2]  # Keep red and green
            
            # Blend the effects
            return (frame + red_frame * 0.3 + blue_frame * 0.3) / 1.6
        return get_frame(t)
    
    return clip.fl(rgb_split_effect)

def apply_screen_shake(clip, start_time, duration=0.5, intensity=10):
    """Applies screen shake effect."""
    def shake_effect(get_frame, t):
        if start_time <= t <= start_time + duration:
            frame = get_frame(t)
            h, w = frame.shape[:2]
            
            # Random offset
            offset_x = np.random.randint(-intensity, intensity + 1)
            offset_y = np.random.randint(-intensity, intensity + 1)
            
            # Create transformation matrix
            M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
            
            # Apply transformation
            import cv2
            shaken = cv2.warpAffine(frame, M, (w, h))
            return shaken
        return get_frame(t)
    
    return clip.fl(shake_effect)

def apply_glitch_effect(clip, start_time, duration=0.2):
    """Applies digital glitch effect."""
    def glitch_effect(get_frame, t):
        if start_time <= t <= start_time + duration:
            frame = get_frame(t)
            h, w = frame.shape[:2]
            
            # Random horizontal line displacement
            glitched = frame.copy()
            num_glitches = np.random.randint(3, 8)
            
            for _ in range(num_glitches):
                y = np.random.randint(0, h)
                shift = np.random.randint(-w//10, w//10)
                
                if shift > 0:
                    glitched[y, shift:] = frame[y, :-shift]
                elif shift < 0:
                    glitched[y, :shift] = frame[y, -shift:]
            
            return glitched
        return get_frame(t)
    
    return clip.fl(glitch_effect)