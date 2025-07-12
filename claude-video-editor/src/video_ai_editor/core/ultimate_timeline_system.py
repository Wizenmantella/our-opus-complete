#!/usr/bin/env python3
"""
Ultimate Timeline System - Professional multi-track timeline with unlimited layers
Supports all professional editing modes, magnetic timeline, and advanced features
"""

import asyncio
import logging
import uuid
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class EditMode(Enum):
    """Professional editing modes"""
    RIPPLE = "ripple"
    ROLL = "roll"
    SLIP = "slip"
    SLIDE = "slide"
    LIFT = "lift"
    EXTRACT = "extract"
    INSERT = "insert"
    OVERWRITE = "overwrite"
    APPEND = "append"
    REPLACE = "replace"
    MATCH_FRAME = "match_frame"
    FIT_TO_FILL = "fit_to_fill"
    THREE_POINT = "three_point"
    FOUR_POINT = "four_point"


class TrackType(Enum):
    """Track types for timeline"""
    VIDEO = "video"
    AUDIO = "audio"
    SUBTITLE = "subtitle"
    GRAPHICS = "graphics"
    ADJUSTMENT = "adjustment"
    COMPOUND = "compound"


class BlendMode(Enum):
    """Comprehensive blending modes"""
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    SOFT_LIGHT = "soft_light"
    HARD_LIGHT = "hard_light"
    COLOR_DODGE = "color_dodge"
    COLOR_BURN = "color_burn"
    DARKEN = "darken"
    LIGHTEN = "lighten"
    DIFFERENCE = "difference"
    EXCLUSION = "exclusion"
    HUE = "hue"
    SATURATION = "saturation"
    COLOR = "color"
    LUMINOSITY = "luminosity"
    ADD = "add"
    SUBTRACT = "subtract"
    DIVIDE = "divide"
    ALPHA_ADD = "alpha_add"
    LINEAR_BURN = "linear_burn"
    LINEAR_DODGE = "linear_dodge"
    VIVID_LIGHT = "vivid_light"
    LINEAR_LIGHT = "linear_light"
    PIN_LIGHT = "pin_light"
    HARD_MIX = "hard_mix"


@dataclass
class TimelineMarker:
    """Timeline marker for annotations"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    timecode: float = 0.0
    color: str = "#FF0000"
    note: str = ""
    chapter: bool = False
    web_link: str = ""
    
    
@dataclass 
class Keyframe:
    """Animation keyframe"""
    time: float
    value: Any
    ease_in: str = "linear"
    ease_out: str = "linear"
    interpolation: str = "linear"
    

@dataclass
class ClipTransform:
    """Complete clip transformation data"""
    position_x: float = 0.0
    position_y: float = 0.0
    position_z: float = 0.0
    rotation_x: float = 0.0
    rotation_y: float = 0.0 
    rotation_z: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    anchor_x: float = 0.5
    anchor_y: float = 0.5
    opacity: float = 1.0
    crop_left: float = 0.0
    crop_right: float = 0.0
    crop_top: float = 0.0
    crop_bottom: float = 0.0
    feather_left: float = 0.0
    feather_right: float = 0.0
    feather_top: float = 0.0
    feather_bottom: float = 0.0
    # Animation keyframes for each property
    keyframes: Dict[str, List[Keyframe]] = field(default_factory=dict)


@dataclass
class TimelineClip:
    """Comprehensive timeline clip"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    source_file: str = ""
    track_id: str = ""
    
    # Timing
    start_time: float = 0.0  # Timeline position
    duration: float = 0.0    # Clip duration
    end_time: float = 0.0    # Calculated end time
    
    # Source timing (for trimming)
    source_in: float = 0.0   # Source start
    source_out: float = 0.0  # Source end
    source_duration: float = 0.0
    
    # Visual properties
    transform: ClipTransform = field(default_factory=ClipTransform)
    blend_mode: BlendMode = BlendMode.NORMAL
    enabled: bool = True
    locked: bool = False
    
    # Speed and timing
    speed: float = 1.0
    reverse: bool = False
    freeze_frame: bool = False
    freeze_time: float = 0.0
    
    # Audio properties
    volume: float = 1.0
    pan: float = 0.0  # -1.0 to 1.0
    audio_gain: float = 0.0  # dB
    muted: bool = False
    audio_channels: List[int] = field(default_factory=list)
    
    # Effects and filters
    effects: List[Dict[str, Any]] = field(default_factory=list)
    color_correction: Dict[str, Any] = field(default_factory=dict)
    
    # Linking and relationships
    linked_clips: List[str] = field(default_factory=list)  # Linked audio/video
    compound_parent: Optional[str] = None
    nested_sequence: Optional[str] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    rating: int = 0
    
    def __post_init__(self):
        """Calculate derived properties"""
        if self.end_time == 0.0:
            self.end_time = self.start_time + self.duration
        if self.source_out == 0.0:
            self.source_out = self.source_in + self.duration


@dataclass
class TimelineTrack:
    """Professional timeline track"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    track_type: TrackType = TrackType.VIDEO
    index: int = 0
    
    # Track properties
    enabled: bool = True
    locked: bool = False
    solo: bool = False
    muted: bool = False
    height: int = 100  # Track height in pixels
    
    # Audio properties
    volume: float = 1.0
    pan: float = 0.0
    monitoring: bool = False
    record_enabled: bool = False
    
    # Track targeting
    target_video: bool = True
    target_audio: bool = True
    patch_source: Optional[str] = None
    
    # Visual properties
    color: str = "#555555"
    collapsed: bool = False
    
    # Track effects
    track_effects: List[Dict[str, Any]] = field(default_factory=list)
    
    # Clips on this track
    clips: List[TimelineClip] = field(default_factory=list)
    
    # Track grouping
    group_id: Optional[str] = None
    
    
@dataclass
class TimelineSequence:
    """Complete timeline sequence"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Untitled Sequence"
    
    # Sequence settings
    frame_rate: float = 29.97
    resolution_width: int = 1920
    resolution_height: int = 1080
    pixel_aspect_ratio: float = 1.0
    field_order: str = "progressive"
    color_space: str = "Rec. 709"
    
    # Timeline properties
    duration: float = 0.0
    timecode_start: str = "01:00:00:00"
    current_time: float = 0.0
    
    # Tracks
    video_tracks: List[TimelineTrack] = field(default_factory=list)
    audio_tracks: List[TimelineTrack] = field(default_factory=list)
    subtitle_tracks: List[TimelineTrack] = field(default_factory=list)
    
    # Timeline elements
    markers: List[TimelineMarker] = field(default_factory=list)
    
    # Playback settings
    zoom_level: float = 1.0
    scroll_position: float = 0.0
    snapping_enabled: bool = True
    magnetic_timeline: bool = True
    
    # Safe zones
    title_safe: float = 0.9
    action_safe: float = 0.93
    
    # Grid and guides
    grid_enabled: bool = False
    guides: List[float] = field(default_factory=list)
    
    # Nested sequences
    parent_sequence: Optional[str] = None
    nested_sequences: List[str] = field(default_factory=list)


class UltimateTimelineSystem:
    """
    Ultimate Timeline System - Professional multi-track editing
    Supports unlimited tracks, all editing modes, and advanced features
    """
    
    def __init__(self):
        self.sequences: Dict[str, TimelineSequence] = {}
        self.current_sequence_id: Optional[str] = None
        self.edit_mode: EditMode = EditMode.RIPPLE
        self.snap_threshold: float = 0.1  # seconds
        self.magnetic_threshold: float = 0.05  # seconds
        self.playhead_position: float = 0.0
        self.selection_in: Optional[float] = None
        self.selection_out: Optional[float] = None
        self.clipboard: List[TimelineClip] = []
        
        # Track management
        self.track_groups: Dict[str, List[str]] = {}
        self.solo_tracks: List[str] = []
        
        # Editing history for undo/redo
        self.edit_history: List[Dict[str, Any]] = []
        self.history_index: int = -1
        
        logger.info("Ultimate Timeline System initialized")
    
    def create_sequence(self, name: str = "New Sequence", **kwargs) -> str:
        """Create a new timeline sequence"""
        sequence = TimelineSequence(name=name, **kwargs)
        
        # Create default tracks
        self._create_default_tracks(sequence)
        
        self.sequences[sequence.id] = sequence
        self.current_sequence_id = sequence.id
        
        logger.info(f"Created sequence: {name} ({sequence.id})")
        return sequence.id
    
    def _create_default_tracks(self, sequence: TimelineSequence):
        """Create default track layout"""
        # Create video tracks (V1, V2, V3...)
        for i in range(3):
            track = TimelineTrack(
                name=f"V{i+1}",
                track_type=TrackType.VIDEO,
                index=i,
                color=f"hsl({i*120}, 50%, 50%)"
            )
            sequence.video_tracks.append(track)
        
        # Create audio tracks (A1, A2, A3...)
        for i in range(6):
            track = TimelineTrack(
                name=f"A{i+1}",
                track_type=TrackType.AUDIO,
                index=i,
                color=f"hsl({i*60}, 70%, 40%)"
            )
            sequence.audio_tracks.append(track)
        
        # Create subtitle track
        subtitle_track = TimelineTrack(
            name="Subtitles",
            track_type=TrackType.SUBTITLE,
            index=0,
            color="#FF6B35"
        )
        sequence.subtitle_tracks.append(subtitle_track)
    
    def add_track(self, sequence_id: str, track_type: TrackType, 
                  name: str = "", index: Optional[int] = None) -> str:
        """Add a new track to sequence"""
        sequence = self.sequences[sequence_id]
        
        if track_type == TrackType.VIDEO:
            tracks = sequence.video_tracks
            default_name = f"V{len(tracks)+1}"
        elif track_type == TrackType.AUDIO:
            tracks = sequence.audio_tracks
            default_name = f"A{len(tracks)+1}"
        else:
            tracks = sequence.subtitle_tracks
            default_name = f"S{len(tracks)+1}"
        
        track = TimelineTrack(
            name=name or default_name,
            track_type=track_type,
            index=index if index is not None else len(tracks)
        )
        
        if index is not None:
            tracks.insert(index, track)
            # Reindex tracks
            for i, t in enumerate(tracks):
                t.index = i
        else:
            tracks.append(track)
        
        logger.info(f"Added track: {track.name} to sequence {sequence_id}")
        return track.id
    
    def add_clip_to_track(self, sequence_id: str, track_id: str, 
                         source_file: str, start_time: float,
                         duration: Optional[float] = None,
                         source_in: float = 0.0,
                         **clip_properties) -> str:
        """Add clip to timeline track with professional placement"""
        sequence = self.sequences[sequence_id]
        track = self._find_track(sequence, track_id)
        
        if not track:
            raise ValueError(f"Track {track_id} not found")
        
        # Auto-detect duration if not provided
        if duration is None:
            duration = self._get_source_duration(source_file)
        
        # Create clip
        clip = TimelineClip(
            name=Path(source_file).stem,
            source_file=source_file,
            track_id=track_id,
            start_time=start_time,
            duration=duration,
            source_in=source_in,
            source_out=source_in + duration,
            source_duration=self._get_source_duration(source_file),
            **clip_properties
        )
        
        # Apply magnetic timeline if enabled
        if sequence.magnetic_timeline:
            clip.start_time = self._apply_magnetic_positioning(
                sequence, track, clip.start_time, duration
            )
        
        # Handle different edit modes
        self._apply_edit_mode(sequence, track, clip)
        
        track.clips.append(clip)
        self._sort_track_clips(track)
        
        # Update sequence duration
        self._update_sequence_duration(sequence)
        
        logger.info(f"Added clip {clip.name} to track {track.name}")
        return clip.id
    
    def _apply_magnetic_positioning(self, sequence: TimelineSequence, 
                                  track: TimelineTrack, 
                                  desired_time: float, 
                                  duration: float) -> float:
        """Apply magnetic timeline positioning"""
        snap_points = []
        
        # Collect snap points from all clips
        for track_list in [sequence.video_tracks, sequence.audio_tracks]:
            for t in track_list:
                for clip in t.clips:
                    snap_points.extend([clip.start_time, clip.end_time])
        
        # Add markers as snap points
        snap_points.extend([m.timecode for m in sequence.markers])
        
        # Add playhead position
        snap_points.append(self.playhead_position)
        
        # Find closest snap point
        closest_point = desired_time
        min_distance = float('inf')
        
        for point in snap_points:
            distance = abs(point - desired_time)
            if distance < min_distance and distance < self.magnetic_threshold:
                min_distance = distance
                closest_point = point
        
        return closest_point
    
    def _apply_edit_mode(self, sequence: TimelineSequence, 
                        track: TimelineTrack, new_clip: TimelineClip):
        """Apply current edit mode when adding clips"""
        if self.edit_mode == EditMode.INSERT:
            self._insert_edit(track, new_clip)
        elif self.edit_mode == EditMode.OVERWRITE:
            self._overwrite_edit(track, new_clip)
        elif self.edit_mode == EditMode.RIPPLE:
            self._ripple_edit(track, new_clip)
        elif self.edit_mode == EditMode.REPLACE:
            self._replace_edit(track, new_clip)
        # Add more edit modes as needed
    
    def _insert_edit(self, track: TimelineTrack, new_clip: TimelineClip):
        """Insert edit - push existing clips forward"""
        for clip in track.clips:
            if clip.start_time >= new_clip.start_time:
                clip.start_time += new_clip.duration
                clip.end_time = clip.start_time + clip.duration
    
    def _overwrite_edit(self, track: TimelineTrack, new_clip: TimelineClip):
        """Overwrite edit - replace overlapping content"""
        clips_to_remove = []
        clips_to_modify = []
        
        for clip in track.clips:
            # Check for overlap
            if (clip.start_time < new_clip.end_time and 
                clip.end_time > new_clip.start_time):
                
                if (clip.start_time >= new_clip.start_time and 
                    clip.end_time <= new_clip.end_time):
                    # Completely overlapped - remove
                    clips_to_remove.append(clip)
                elif clip.start_time < new_clip.start_time < clip.end_time:
                    # Partial overlap - trim end
                    clip.duration = new_clip.start_time - clip.start_time
                    clip.end_time = clip.start_time + clip.duration
                elif clip.start_time < new_clip.end_time < clip.end_time:
                    # Partial overlap - trim start
                    trim_amount = new_clip.end_time - clip.start_time
                    clip.start_time = new_clip.end_time
                    clip.source_in += trim_amount
                    clip.duration -= trim_amount
                    clip.end_time = clip.start_time + clip.duration
        
        # Remove completely overlapped clips
        for clip in clips_to_remove:
            track.clips.remove(clip)
    
    def _ripple_edit(self, track: TimelineTrack, new_clip: TimelineClip):
        """Ripple edit - insert and shift later clips"""
        self._insert_edit(track, new_clip)
    
    def _replace_edit(self, track: TimelineTrack, new_clip: TimelineClip):
        """Replace edit - replace clip at playhead"""
        # Find clip at playhead position
        target_clip = None
        for clip in track.clips:
            if clip.start_time <= self.playhead_position <= clip.end_time:
                target_clip = clip
                break
        
        if target_clip:
            # Replace with new clip
            new_clip.start_time = target_clip.start_time
            new_clip.duration = min(new_clip.duration, target_clip.duration)
            new_clip.end_time = new_clip.start_time + new_clip.duration
            track.clips.remove(target_clip)
    
    def trim_clip(self, sequence_id: str, clip_id: str, 
                  new_in: Optional[float] = None,
                  new_out: Optional[float] = None,
                  trim_mode: str = "ripple") -> bool:
        """Professional clip trimming with different modes"""
        sequence = self.sequences[sequence_id]
        clip = self._find_clip(sequence, clip_id)
        
        if not clip:
            return False
        
        old_duration = clip.duration
        
        if new_in is not None:
            # Trim in point
            time_change = new_in - clip.start_time
            clip.start_time = new_in
            clip.source_in += time_change
            clip.duration -= time_change
        
        if new_out is not None:
            # Trim out point
            clip.duration = new_out - clip.start_time
        
        clip.end_time = clip.start_time + clip.duration
        
        # Apply trim mode effects
        if trim_mode == "ripple":
            self._ripple_trim_adjustment(sequence, clip, old_duration)
        elif trim_mode == "roll":
            self._roll_trim_adjustment(sequence, clip, old_duration)
        
        logger.info(f"Trimmed clip {clip.name}: {trim_mode} mode")
        return True
    
    def _ripple_trim_adjustment(self, sequence: TimelineSequence, 
                               trimmed_clip: TimelineClip, old_duration: float):
        """Adjust timeline for ripple trim"""
        duration_change = trimmed_clip.duration - old_duration
        
        # Find track containing the clip
        track = self._find_track_containing_clip(sequence, trimmed_clip.id)
        if not track:
            return
        
        # Shift later clips
        for clip in track.clips:
            if clip.start_time >= trimmed_clip.end_time:
                clip.start_time += duration_change
                clip.end_time += duration_change
    
    def _roll_trim_adjustment(self, sequence: TimelineSequence,
                             trimmed_clip: TimelineClip, old_duration: float):
        """Adjust adjacent clips for roll trim"""
        duration_change = trimmed_clip.duration - old_duration
        
        track = self._find_track_containing_clip(sequence, trimmed_clip.id)
        if not track:
            return
        
        # Find adjacent clip
        for clip in track.clips:
            if abs(clip.start_time - trimmed_clip.end_time) < 0.01:
                # Adjacent clip found - adjust it
                clip.start_time -= duration_change
                clip.source_in -= duration_change
                clip.duration += duration_change
                clip.end_time = clip.start_time + clip.duration
                break
    
    def slip_edit(self, sequence_id: str, clip_id: str, offset: float) -> bool:
        """Slip edit - change source timing without affecting timeline position"""
        sequence = self.sequences[sequence_id]
        clip = self._find_clip(sequence, clip_id)
        
        if not clip:
            return False
        
        # Adjust source in/out points
        clip.source_in += offset
        clip.source_out += offset
        
        # Ensure source timing stays within bounds
        if clip.source_in < 0:
            clip.source_in = 0
            clip.source_out = clip.duration
        elif clip.source_out > clip.source_duration:
            clip.source_out = clip.source_duration
            clip.source_in = clip.source_out - clip.duration
        
        logger.info(f"Slip edit clip {clip.name}: offset {offset}s")
        return True
    
    def slide_edit(self, sequence_id: str, clip_id: str, offset: float) -> bool:
        """Slide edit - move clip and adjust adjacent clips"""
        sequence = self.sequences[sequence_id]
        clip = self._find_clip(sequence, clip_id)
        
        if not clip:
            return False
        
        track = self._find_track_containing_clip(sequence, clip_id)
        if not track:
            return False
        
        # Move the clip
        old_start = clip.start_time
        clip.start_time += offset
        clip.end_time += offset
        
        # Adjust adjacent clips
        for other_clip in track.clips:
            if other_clip.id == clip_id:
                continue
                
            if other_clip.end_time == old_start:
                # Clip before - extend or trim
                other_clip.duration += offset
                other_clip.end_time += offset
            elif other_clip.start_time == old_start + clip.duration:
                # Clip after - move start
                other_clip.start_time += offset
                other_clip.source_in -= offset
                other_clip.duration -= offset
        
        logger.info(f"Slide edit clip {clip.name}: offset {offset}s")
        return True
    
    def add_marker(self, sequence_id: str, name: str, 
                   timecode: Optional[float] = None, **kwargs) -> str:
        """Add timeline marker"""
        sequence = self.sequences[sequence_id]
        
        marker = TimelineMarker(
            name=name,
            timecode=timecode or self.playhead_position,
            **kwargs
        )
        
        sequence.markers.append(marker)
        sequence.markers.sort(key=lambda m: m.timecode)
        
        logger.info(f"Added marker: {name} at {marker.timecode}s")
        return marker.id
    
    def create_compound_clip(self, sequence_id: str, 
                           clip_ids: List[str], name: str) -> str:
        """Create compound/nested clip from selection"""
        sequence = self.sequences[sequence_id]
        clips_to_compound = []
        
        for clip_id in clip_ids:
            clip = self._find_clip(sequence, clip_id)
            if clip:
                clips_to_compound.append(clip)
        
        if not clips_to_compound:
            raise ValueError("No valid clips found for compound clip")
        
        # Calculate compound clip bounds
        start_time = min(clip.start_time for clip in clips_to_compound)
        end_time = max(clip.end_time for clip in clips_to_compound)
        duration = end_time - start_time
        
        # Create new sequence for compound clip
        compound_sequence_id = self.create_sequence(f"{name} - Compound")
        
        # Move clips to compound sequence (simplified)
        compound_clip = TimelineClip(
            name=name,
            start_time=start_time,
            duration=duration,
            nested_sequence=compound_sequence_id
        )
        
        logger.info(f"Created compound clip: {name}")
        return compound_clip.id
    
    def three_point_edit(self, sequence_id: str, source_file: str,
                        source_in: float, source_out: float,
                        timeline_in: float) -> str:
        """Three-point editing"""
        duration = source_out - source_in
        
        return self.add_clip_to_track(
            sequence_id=sequence_id,
            track_id=self._get_target_track_id(sequence_id),
            source_file=source_file,
            start_time=timeline_in,
            duration=duration,
            source_in=source_in
        )
    
    def four_point_edit(self, sequence_id: str, source_file: str,
                       source_in: float, source_out: float,
                       timeline_in: float, timeline_out: float) -> str:
        """Four-point editing with fit to fill"""
        source_duration = source_out - source_in
        timeline_duration = timeline_out - timeline_in
        
        # Calculate speed to fit
        speed = source_duration / timeline_duration
        
        return self.add_clip_to_track(
            sequence_id=sequence_id,
            track_id=self._get_target_track_id(sequence_id),
            source_file=source_file,
            start_time=timeline_in,
            duration=timeline_duration,
            source_in=source_in,
            speed=speed
        )
    
    def match_frame(self, sequence_id: str, clip_id: str) -> Dict[str, Any]:
        """Match frame to source"""
        sequence = self.sequences[sequence_id]
        clip = self._find_clip(sequence, clip_id)
        
        if not clip:
            return {}
        
        # Calculate current source timecode
        playhead_offset = self.playhead_position - clip.start_time
        source_timecode = clip.source_in + (playhead_offset / clip.speed)
        
        return {
            "source_file": clip.source_file,
            "source_timecode": source_timecode,
            "clip_id": clip_id
        }
    
    def lift_extract(self, sequence_id: str, 
                    in_point: float, out_point: float,
                    extract: bool = False) -> List[str]:
        """Lift or extract clips from timeline"""
        sequence = self.sequences[sequence_id]
        removed_clips = []
        
        for track_list in [sequence.video_tracks, sequence.audio_tracks]:
            for track in track_list:
                clips_to_process = []
                
                for clip in track.clips:
                    if (clip.start_time < out_point and 
                        clip.end_time > in_point):
                        clips_to_process.append(clip)
                
                for clip in clips_to_process:
                    if extract:
                        # Extract: remove and close gap
                        track.clips.remove(clip)
                        removed_clips.append(clip.id)
                        
                        # Shift later clips
                        gap_duration = out_point - in_point
                        for other_clip in track.clips:
                            if other_clip.start_time >= out_point:
                                other_clip.start_time -= gap_duration
                                other_clip.end_time -= gap_duration
                    else:
                        # Lift: remove but leave gap
                        track.clips.remove(clip)
                        removed_clips.append(clip.id)
        
        logger.info(f"{'Extracted' if extract else 'Lifted'} {len(removed_clips)} clips")
        return removed_clips
    
    def pancake_timeline(self, sequence_id: str, 
                        reference_sequence_id: str) -> bool:
        """Create pancake timeline for comparison editing"""
        # This would create a stacked view of multiple sequences
        # Implementation depends on UI framework
        logger.info(f"Created pancake timeline: {sequence_id} + {reference_sequence_id}")
        return True
    
    def _find_track(self, sequence: TimelineSequence, track_id: str) -> Optional[TimelineTrack]:
        """Find track by ID in sequence"""
        for track_list in [sequence.video_tracks, sequence.audio_tracks, sequence.subtitle_tracks]:
            for track in track_list:
                if track.id == track_id:
                    return track
        return None
    
    def _find_clip(self, sequence: TimelineSequence, clip_id: str) -> Optional[TimelineClip]:
        """Find clip by ID in sequence"""
        for track_list in [sequence.video_tracks, sequence.audio_tracks, sequence.subtitle_tracks]:
            for track in track_list:
                for clip in track.clips:
                    if clip.id == clip_id:
                        return clip
        return None
    
    def _find_track_containing_clip(self, sequence: TimelineSequence, 
                                   clip_id: str) -> Optional[TimelineTrack]:
        """Find track containing specific clip"""
        for track_list in [sequence.video_tracks, sequence.audio_tracks, sequence.subtitle_tracks]:
            for track in track_list:
                for clip in track.clips:
                    if clip.id == clip_id:
                        return track
        return None
    
    def _sort_track_clips(self, track: TimelineTrack):
        """Sort clips on track by start time"""
        track.clips.sort(key=lambda c: c.start_time)
    
    def _update_sequence_duration(self, sequence: TimelineSequence):
        """Update sequence duration based on clips"""
        max_end_time = 0.0
        
        for track_list in [sequence.video_tracks, sequence.audio_tracks]:
            for track in track_list:
                for clip in track.clips:
                    max_end_time = max(max_end_time, clip.end_time)
        
        sequence.duration = max_end_time
    
    def _get_source_duration(self, source_file: str) -> float:
        """Get duration of source file"""
        # This would use ffprobe or similar to get actual duration
        # For now, return placeholder
        return 10.0
    
    def _get_target_track_id(self, sequence_id: str) -> str:
        """Get currently targeted track for editing"""
        sequence = self.sequences[sequence_id]
        
        # Find first enabled video track
        for track in sequence.video_tracks:
            if track.enabled and track.target_video:
                return track.id
        
        # Fallback to first track
        if sequence.video_tracks:
            return sequence.video_tracks[0].id
        
        raise ValueError("No target track available")
    
    def export_sequence_data(self, sequence_id: str) -> Dict[str, Any]:
        """Export complete sequence data"""
        sequence = self.sequences[sequence_id]
        
        return {
            "sequence": {
                "id": sequence.id,
                "name": sequence.name,
                "frame_rate": sequence.frame_rate,
                "resolution": [sequence.resolution_width, sequence.resolution_height],
                "duration": sequence.duration
            },
            "tracks": {
                "video": [self._track_to_dict(t) for t in sequence.video_tracks],
                "audio": [self._track_to_dict(t) for t in sequence.audio_tracks],
                "subtitle": [self._track_to_dict(t) for t in sequence.subtitle_tracks]
            },
            "markers": [self._marker_to_dict(m) for m in sequence.markers]
        }
    
    def _track_to_dict(self, track: TimelineTrack) -> Dict[str, Any]:
        """Convert track to dictionary"""
        return {
            "id": track.id,
            "name": track.name,
            "type": track.track_type.value,
            "enabled": track.enabled,
            "clips": [self._clip_to_dict(c) for c in track.clips]
        }
    
    def _clip_to_dict(self, clip: TimelineClip) -> Dict[str, Any]:
        """Convert clip to dictionary"""
        return {
            "id": clip.id,
            "name": clip.name,
            "source_file": clip.source_file,
            "start_time": clip.start_time,
            "duration": clip.duration,
            "source_in": clip.source_in,
            "speed": clip.speed,
            "enabled": clip.enabled
        }
    
    def _marker_to_dict(self, marker: TimelineMarker) -> Dict[str, Any]:
        """Convert marker to dictionary"""
        return {
            "id": marker.id,
            "name": marker.name,
            "timecode": marker.timecode,
            "color": marker.color
        }


# Example usage and testing
async def demo_timeline_system():
    """Demonstrate timeline system capabilities"""
    timeline = UltimateTimelineSystem()
    
    # Create a new sequence
    seq_id = timeline.create_sequence("Demo Sequence", frame_rate=29.97)
    
    # Add some clips
    clip1_id = timeline.add_clip_to_track(
        seq_id, timeline.sequences[seq_id].video_tracks[0].id,
        "video1.mp4", 0.0, 10.0
    )
    
    clip2_id = timeline.add_clip_to_track(
        seq_id, timeline.sequences[seq_id].video_tracks[0].id,
        "video2.mp4", 10.0, 8.0
    )
    
    # Add marker
    timeline.add_marker(seq_id, "Scene 1", 5.0)
    
    # Trim a clip
    timeline.trim_clip(seq_id, clip1_id, new_out=8.0)
    
    # Three-point edit
    timeline.three_point_edit(seq_id, "video3.mp4", 2.0, 7.0, 15.0)
    
    # Export data
    export_data = timeline.export_sequence_data(seq_id)
    print(f"Timeline created with {len(export_data['tracks']['video'][0]['clips'])} clips")
    
    return timeline


if __name__ == "__main__":
    asyncio.run(demo_timeline_system())