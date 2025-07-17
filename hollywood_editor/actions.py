# In hollywood_editor/actions.py

from dataclasses import dataclass
from typing import Tuple

@dataclass
class BaseAction:
    """Base class for all edit actions."""
    start_time: float
    end_time: float

@dataclass
class Cut(BaseAction):
    """Represents cutting to a specific source media file."""
    source_file: str
    source_start: float
    source_end: float

@dataclass
class AddText(BaseAction):
    """Represents adding on-screen text."""
    text: str
    font_size: int = 48
    position: Tuple[str, str] = ('center', 'center') # e.g., ('center', 'bottom')
    color: str = 'white'

@dataclass
class ApplyLUT(BaseAction):
    """Represents applying a color Look-Up Table (LUT)."""
    lut_file: str # e.g., "teal_and_orange.cube"

@dataclass
class AddAudio(BaseAction):
    """Represents adding a background music or sound effect track."""
    audio_file: str
    volume: float = 0.5 # 0.0 to 1.0