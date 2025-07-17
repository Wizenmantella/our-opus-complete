# creative/captions.py
from moviepy.editor import TextClip, CompositeVideoClip
from typing import List, Dict, Any
from config import CAPTION_STYLE
from project import VideoProject

def generate_caption_clips(project: VideoProject, screensize: tuple) -> List[TextClip]:
    """
    Generates a list of MoviePy clips for word-by-word captions.
    """
    if not project.transcript:
        return []

    caption_clips = []
    for segment in project.transcript:
        for word_info in segment.get('words', []):
            word = word_info['word']
            start = word_info['start']
            end = word_info['end']
            duration = end - start

            # Create the text clip for this word
            txt_clip = TextClip(
                word.upper(),
                fontsize=CAPTION_STYLE['fontsize'],
                color=CAPTION_STYLE['highlight_color'],
                font=CAPTION_STYLE['font'],
                stroke_color=CAPTION_STYLE['stroke_color'],
                stroke_width=CAPTION_STYLE['stroke_width']
            ).set_position('center').set_duration(duration).set_start(start)

            caption_clips.append(txt_clip)

    return caption_clips

def create_word_highlight_caption(word: str, start_time: float, duration: float) -> TextClip:
    """Creates a single highlighted word caption."""
    return TextClip(
        word.upper(),
        fontsize=CAPTION_STYLE['fontsize'],
        color=CAPTION_STYLE['highlight_color'],
        font=CAPTION_STYLE['font'],
        stroke_color=CAPTION_STYLE['stroke_color'],
        stroke_width=CAPTION_STYLE['stroke_width']
    ).set_position('center').set_duration(duration).set_start(start_time)