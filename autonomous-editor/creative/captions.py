# creative/captions.py
from moviepy.editor import TextClip, CompositeVideoClip
from typing import List, Dict, Any
from project import VideoProject
from config import CAPTION_STYLE

def generate_caption_clips(project: VideoProject, start_time: float, end_time: float) -> List[TextClip]:
    """
    Generates a list of MoviePy TextClips for word-by-word captions
    that fall within a specific time segment of the video.
    """
    if not project.transcript:
        return []

    caption_clips = []
    for segment in project.transcript:
        for word_info in segment.get('words', []):
            word_start = word_info['start']
            word_end = word_info['end']

            # Check if the word falls within the current clip's timeframe
            if word_start >= start_time and word_end <= end_time:
                word = word_info['word']
                duration = word_end - word_start
                
                # Adjust start time to be relative to the subclip
                relative_start = word_start - start_time

                txt_clip = TextClip(
                    word.upper(),
                    fontsize=CAPTION_STYLE['fontsize'],
                    color=CAPTION_STYLE['highlight_color'],
                    font=CAPTION_STYLE['font'],
                    stroke_color=CAPTION_STYLE['stroke_color'],
                    stroke_width=CAPTION_STYLE['stroke_width']
                ).set_position('center').set_duration(duration).set_start(relative_start)

                caption_clips.append(txt_clip)

    return caption_clips