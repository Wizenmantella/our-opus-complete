# overlays.py
import moviepy.editor as mp

def create_hook_text(text, duration=3, fontsize=70):
    """Creates a large, impactful text overlay for the beginning."""
    return mp.TextClip(text.upper(), 
                      fontsize=fontsize, 
                      color='white', 
                      font='Arial-Bold', 
                      stroke_color='black', 
                      stroke_width=3)\
        .set_position('center')\
        .set_duration(duration)\
        .set_start(0)

def create_progress_bar(video_duration, height=8):
    """Creates a bar that animates across the bottom of the screen."""
    def progress_bar_frame(t):
        progress = min(t / video_duration, 1.0)
        # Create a simple colored bar
        import numpy as np
        # Assuming 1920x1080 resolution
        width = 1920
        bar_width = int(width * progress)
        
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        if bar_width > 0:
            frame[:, :bar_width] = [255, 107, 107]  # Red color
        
        return frame
    
    return mp.VideoClip(progress_bar_frame, duration=video_duration)\
        .set_position(('center', 'bottom'))

def create_beat_flash(beat_times, video_duration):
    """Creates white flashes on beat times."""
    def flash_effect(t):
        # Check if we're close to a beat
        for beat_time in beat_times:
            if abs(t - beat_time) < 0.05:  # 50ms window
                return [255, 255, 255]  # White flash
        return [0, 0, 0]  # Transparent
    
    return mp.VideoClip(lambda t: flash_effect(t), duration=video_duration)\
        .set_opacity(0.3)

def create_word_captions(transcript, fontsize=50):
    """Creates word-by-word captions from transcript."""
    if not transcript or 'segments' not in transcript:
        return []
    
    captions = []
    for segment in transcript['segments']:
        if 'words' in segment:
            for word_info in segment['words']:
                word = word_info['word'].strip()
                start = word_info['start']
                end = word_info['end']
                duration = end - start
                
                caption = mp.TextClip(word.upper(),
                                    fontsize=fontsize,
                                    color='white',
                                    font='Arial-Bold',
                                    stroke_color='black',
                                    stroke_width=2)\
                    .set_position('center')\
                    .set_start(start)\
                    .set_duration(duration)
                
                captions.append(caption)
    
    return captions

def create_engagement_text(text, start_time, duration=2):
    """Creates engaging text overlays like 'FIRE!' or 'INSANE!'"""
    return mp.TextClip(text,
                      fontsize=60,
                      color='yellow',
                      font='Arial-Bold',
                      stroke_color='red',
                      stroke_width=3)\
        .set_position(('right', 'top'))\
        .set_start(start_time)\
        .set_duration(duration)\
        .crossfadein(0.3)\
        .crossfadeout(0.3)