# project.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from moviepy.editor import VideoFileClip

@dataclass
class VideoProject:
    """
    A data container for all information related to a single video editing project.
    This object is passed between different modules of the editor.
    """
    video_path: str
    style_name: str
    output_path: Optional[str] = None

    # Core assets, populated during initialization
    clip: Optional[VideoFileClip] = None
    audio_path: Optional[str] = None

    # Analysis results, populated by the analysis modules
    transcript: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    beat_timestamps: Optional[List[float]] = field(default_factory=list)
    scene_timestamps: Optional[List[float]] = field(default_factory=list)

    # The final plan, populated by the Director
    edit_plan: Optional[List[Dict[str, Any]]] = field(default_factory=list)