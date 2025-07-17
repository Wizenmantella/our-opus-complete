from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import uuid
from typing import List, Dict, Any, Optional

class ContentType(Enum):
    EDUCATIONAL = "Educational"
    TUTORIAL = "Tutorial"
    ENTERTAINMENT = "Entertainment"
    MOTIVATION = "Motivation"
    NEWS = "News"

class Platform(Enum):
    YOUTUBE = "YouTube"
    YOUTUBE_SHORTS = "YouTube Shorts"
    TIKTOK = "TikTok"
    INSTAGRAM_REEL = "Instagram Reel"

class ProjectStatus(Enum):
    PENDING = "Pending"
    SCRIPTING = "Scripting"
    EDITING = "Editing"
    RENDERING = "Rendering"
    COMPLETE = "Complete"
    FAILED = "Failed"

@dataclass
class Project:
    """Represents a single video creation project."""
    prompt: str
    content_type: ContentType
    target_platforms: List[Platform]

    # Optional inputs
    script: Optional[str] = None
    source_files: List[str] = field(default_factory=list)
    target_duration: int = 30

    # Managed by the editor
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: ProjectStatus = ProjectStatus.PENDING
    edit_decision_list: List[Any] = field(default_factory=list)
    viral_variants: List[Dict[str, Any]] = field(default_factory=list)
    output_paths: Dict[str, Path] = field(default_factory=dict)
    voiceover_file: Optional[Path] = None
    voiceover_timestamps: Optional[List[Dict[str, Any]]] = None
