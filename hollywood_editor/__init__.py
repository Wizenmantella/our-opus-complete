"""
Hollywood Editor - AI-Powered Video Creation System

Core package for automated video production and viral content creation.
"""

from .project import (
    ContentType,
    Platform, 
    ProjectStatus,
    Project
)
from .content_engine import GenerativeContentEngine
from .edit_engine import EditDecisionEngine
from .actions import BaseAction, Cut, AddText, ApplyLUT, AddAudio
from .export_system import ExportDeliverySystem
from .viral_engine import PredictiveViralEngine
from .channel_manager import AutonomousChannelManager
from .editor import HollywoodEditor

__version__ = "1.0.0"
__author__ = "Hollywood Editor Team"

__all__ = [
    "Project",
    "ContentType",
    "Platform",
    "ProjectStatus",
    "BaseAction",
    "Cut",
    "AddText",
    "ApplyLUT",
    "AddAudio",
    "GenerativeContentEngine",
    "EditDecisionEngine",
    "PredictiveViralEngine",
    "ExportDeliverySystem",
    "AutonomousChannelManager",
    "HollywoodEditor",
]
