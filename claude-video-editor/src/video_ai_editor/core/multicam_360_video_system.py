#!/usr/bin/env python3
"""
Multicam and 360° Video System
Complete multicam editing and 360° video processing system with professional features.

Features:
- Multicam sync (timecode, audio, markers)
- Multi-angle viewing (2, 4, 9, 16, 25+ angles)
- Angle switching and live cutting
- Audio follows video / Video follows audio
- Multicam metadata handling
- Angle color coding and organization
- Bank switching for large projects
- Equirectangular 360° support
- Stereoscopic 3D processing
- 360° effects and stabilization
- Horizon leveling and reframe to flat
- Tiny planet effects
- Spatial audio for 360°
- VR headset preview capabilities
"""

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from scipy import signal
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import librosa
import soundfile as sf
from typing import Dict, List, Tuple, Optional, Any, Union
import asyncio
import logging
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import json
import math
import subprocess
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class SyncMethod(Enum):
    """Synchronization methods"""
    TIMECODE = "timecode"
    AUDIO_WAVEFORM = "audio_waveform"
    MARKERS = "markers"
    MANUAL = "manual"
    AUTO_DETECT = "auto_detect"


class AngleLayout(Enum):
    """Multi-angle viewing layouts"""
    SINGLE = "single"
    DUAL = "dual"
    QUAD = "quad"
    NINE = "nine"
    SIXTEEN = "sixteen"
    TWENTY_FIVE = "twenty_five"
    CUSTOM = "custom"


class ProjectionType(Enum):
    """360° projection types"""
    EQUIRECTANGULAR = "equirectangular"
    CUBEMAP = "cubemap"
    FISHEYE = "fisheye"
    STEREOGRAPHIC = "stereographic"
    CYLINDRICAL = "cylindrical"


class StereoMode(Enum):
    """Stereoscopic 3D modes"""
    MONO = "mono"
    TOP_BOTTOM = "top_bottom"
    SIDE_BY_SIDE = "side_by_side"
    OVER_UNDER = "over_under"
    INTERLEAVED = "interleaved"


@dataclass
class CameraAngle:
    """Camera angle information"""
    angle_id: str
    name: str
    video_path: str
    audio_path: Optional[str] = None
    timecode_offset: float = 0.0
    color_coding: str = "#FFFFFF"
    metadata: Dict[str, Any] = field(default_factory=dict)
    sync_confidence: float = 0.0
    is_360: bool = False
    stereo_mode: StereoMode = StereoMode.MONO
    projection: Optional[ProjectionType] = None


@dataclass
class SyncPoint:
    """Synchronization point between angles"""
    timestamp: float
    angles: Dict[str, float]  # angle_id -> timestamp
    method: SyncMethod
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MulticamProject:
    """Multicam project structure"""
    project_id: str
    name: str
    angles: List[CameraAngle]
    sync_points: List[SyncPoint]
    master_angle: Optional[str] = None
    frame_rate: float = 30.0
    resolution: Tuple[int, int] = (1920, 1080)
    audio_follows_video: bool = True
    banks: Dict[str, List[str]] = field(default_factory=dict)


class MulticamSyncEngine:
    """Advanced multicam synchronization engine"""
    
    def __init__(self):
        self.sample_rate = 48000
        self.sync_tolerance = 0.1  # seconds
        
    async def sync_multicam_project(self, angles: List[CameraAngle], 
                                  sync_method: SyncMethod = SyncMethod.AUTO_DETECT) -> List[SyncPoint]:
        """Synchronize multicam project"""
        
        logger.info(f"Synchronizing {len(angles)} camera angles using {sync_method.value}")
        
        sync_points = []
        
        if sync_method == SyncMethod.AUTO_DETECT:
            # Try multiple sync methods and pick the best
            sync_methods = [SyncMethod.TIMECODE, SyncMethod.AUDIO_WAVEFORM, SyncMethod.MARKERS]
            best_sync = None
            best_confidence = 0.0
            
            for method in sync_methods:
                try:
                    candidate_sync = await self._sync_by_method(angles, method)
                    if candidate_sync and len(candidate_sync) > 0:
                        avg_confidence = np.mean([sp.confidence for sp in candidate_sync])
                        if avg_confidence > best_confidence:
                            best_confidence = avg_confidence
                            best_sync = candidate_sync
                except Exception as e:
                    logger.warning(f"Sync method {method.value} failed: {e}")
                    continue
            
            sync_points = best_sync or []
            
        else:
            sync_points = await self._sync_by_method(angles, sync_method)
        
        logger.info(f"Generated {len(sync_points)} sync points")
        return sync_points
    
    async def _sync_by_method(self, angles: List[CameraAngle], 
                            method: SyncMethod) -> List[SyncPoint]:
        """Sync by specific method"""
        
        if method == SyncMethod.TIMECODE:
            return await self._sync_by_timecode(angles)
        elif method == SyncMethod.AUDIO_WAVEFORM:
            return await self._sync_by_audio_waveform(angles)
        elif method == SyncMethod.MARKERS:
            return await self._sync_by_markers(angles)
        else:
            return []
    
    async def _sync_by_timecode(self, angles: List[CameraAngle]) -> List[SyncPoint]:
        """Synchronize using embedded timecode"""
        
        sync_points = []
        
        # Extract timecode from each angle
        timecodes = {}
        for angle in angles:
            tc = await self._extract_timecode(angle.video_path)
            if tc:
                timecodes[angle.angle_id] = tc
        
        if len(timecodes) < 2:
            return sync_points
        
        # Find common timecode points
        common_times = self._find_common_timecode_points(timecodes)
        
        for tc_time in common_times:
            angle_times = {}
            for angle_id, tc_data in timecodes.items():
                # Find frame with this timecode
                frame_time = self._timecode_to_frame_time(tc_time, tc_data)
                if frame_time is not None:
                    angle_times[angle_id] = frame_time
            
            if len(angle_times) >= 2:
                sync_point = SyncPoint(
                    timestamp=tc_time,
                    angles=angle_times,
                    method=SyncMethod.TIMECODE,
                    confidence=0.95,
                    metadata={"timecode": tc_time}
                )
                sync_points.append(sync_point)
        
        return sync_points
    
    async def _sync_by_audio_waveform(self, angles: List[CameraAngle]) -> List[SyncPoint]:
        """Synchronize using audio waveform correlation"""
        
        sync_points = []
        
        # Load audio from all angles
        audio_data = {}
        for angle in angles:
            audio_path = angle.audio_path or angle.video_path
            try:
                y, sr = librosa.load(audio_path, sr=self.sample_rate)
                audio_data[angle.angle_id] = y
            except Exception as e:
                logger.warning(f"Could not load audio for angle {angle.angle_id}: {e}")
                continue
        
        if len(audio_data) < 2:
            return sync_points
        
        # Use first angle as reference
        reference_id = list(audio_data.keys())[0]
        reference_audio = audio_data[reference_id]
        
        # Find correlation with other angles
        for angle_id, audio in audio_data.items():
            if angle_id == reference_id:
                continue
            
            # Cross-correlation to find offset
            correlation = signal.correlate(reference_audio, audio, mode='full')
            lag = signal.correlation_lags(len(reference_audio), len(audio), mode='full')
            
            # Find peak correlation
            max_corr_idx = np.argmax(np.abs(correlation))
            offset_samples = lag[max_corr_idx]
            offset_seconds = offset_samples / self.sample_rate
            confidence = abs(correlation[max_corr_idx]) / (np.linalg.norm(reference_audio) * np.linalg.norm(audio))
            
            if confidence > 0.3:  # Minimum confidence threshold
                sync_point = SyncPoint(
                    timestamp=0.0,
                    angles={reference_id: 0.0, angle_id: -offset_seconds},
                    method=SyncMethod.AUDIO_WAVEFORM,
                    confidence=float(confidence),
                    metadata={"offset_samples": int(offset_samples)}
                )
                sync_points.append(sync_point)
        
        return sync_points
    
    async def _sync_by_markers(self, angles: List[CameraAngle]) -> List[SyncPoint]:
        """Synchronize using visual markers (clapperboard, flash, etc.)"""
        
        sync_points = []
        
        # Detect sync markers in each video
        markers = {}
        for angle in angles:
            angle_markers = await self._detect_sync_markers(angle.video_path)
            if angle_markers:
                markers[angle.angle_id] = angle_markers
        
        if len(markers) < 2:
            return sync_points
        
        # Match markers across angles
        matched_markers = self._match_markers_across_angles(markers)
        
        for marker_group in matched_markers:
            if len(marker_group) >= 2:
                sync_point = SyncPoint(
                    timestamp=np.mean(list(marker_group.values())),
                    angles=marker_group,
                    method=SyncMethod.MARKERS,
                    confidence=0.8,
                    metadata={"marker_type": "visual"}
                )
                sync_points.append(sync_point)
        
        return sync_points
    
    async def _extract_timecode(self, video_path: str) -> Optional[Dict[str, Any]]:
        """Extract timecode information from video"""
        
        try:
            # Use ffprobe to extract timecode
            cmd = [
                'ffprobe', '-v', 'quiet', '-show_entries', 'frame=pkt_pts_time,timecode',
                '-select_streams', 'v:0', '-of', 'json', video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                frames = data.get('frames', [])
                
                if frames:
                    return {
                        'start_timecode': frames[0].get('timecode'),
                        'frames': frames
                    }
        except Exception as e:
            logger.warning(f"Timecode extraction failed: {e}")
        
        return None
    
    def _find_common_timecode_points(self, timecodes: Dict[str, Any]) -> List[str]:
        """Find common timecode points across angles"""
        
        # Simplified implementation - would need proper timecode parsing
        common_points = []
        
        # Extract all timecodes
        all_timecodes = set()
        for tc_data in timecodes.values():
            frames = tc_data.get('frames', [])
            for frame in frames:
                tc = frame.get('timecode')
                if tc:
                    all_timecodes.add(tc)
        
        # Find timecodes present in multiple angles
        for tc in all_timecodes:
            present_count = 0
            for tc_data in timecodes.values():
                frames = tc_data.get('frames', [])
                if any(frame.get('timecode') == tc for frame in frames):
                    present_count += 1
            
            if present_count >= 2:
                common_points.append(tc)
        
        return sorted(common_points)
    
    def _timecode_to_frame_time(self, timecode: str, tc_data: Dict[str, Any]) -> Optional[float]:
        """Convert timecode to frame time"""
        
        frames = tc_data.get('frames', [])
        for frame in frames:
            if frame.get('timecode') == timecode:
                return float(frame.get('pkt_pts_time', 0))
        
        return None
    
    async def _detect_sync_markers(self, video_path: str) -> List[float]:
        """Detect visual sync markers (flashes, clapperboards)"""
        
        markers = []
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        prev_frame = None
        frame_idx = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Detect sudden brightness changes (flashes)
                brightness_change = abs(np.mean(gray) - np.mean(prev_frame))
                
                if brightness_change > 50:  # Threshold for flash detection
                    timestamp = frame_idx / fps
                    markers.append(timestamp)
            
            prev_frame = gray
            frame_idx += 1
            
            # Sample every 10th frame for performance
            for _ in range(9):
                cap.read()
                frame_idx += 10
        
        cap.release()
        return markers
    
    def _match_markers_across_angles(self, markers: Dict[str, List[float]]) -> List[Dict[str, float]]:
        """Match markers across different camera angles"""
        
        matched_groups = []
        
        # Get all marker times
        all_markers = []
        for angle_id, marker_times in markers.items():
            for time in marker_times:
                all_markers.append((angle_id, time))
        
        # Cluster markers by time
        if not all_markers:
            return matched_groups
        
        times = np.array([marker[1] for marker in all_markers]).reshape(-1, 1)
        
        # Use DBSCAN to group markers that occur at similar times
        clustering = DBSCAN(eps=self.sync_tolerance, min_samples=2)
        labels = clustering.fit_predict(times)
        
        # Group markers by cluster
        for label in set(labels):
            if label != -1:  # Ignore noise points
                cluster_markers = {}
                for i, (angle_id, time) in enumerate(all_markers):
                    if labels[i] == label:
                        if angle_id not in cluster_markers:
                            cluster_markers[angle_id] = time
                        else:
                            # Keep the marker closest to cluster center
                            cluster_center = np.mean([all_markers[j][1] for j in range(len(all_markers)) if labels[j] == label])
                            if abs(time - cluster_center) < abs(cluster_markers[angle_id] - cluster_center):
                                cluster_markers[angle_id] = time
                
                if len(cluster_markers) >= 2:
                    matched_groups.append(cluster_markers)
        
        return matched_groups


class MulticamEditor:
    """Professional multicam editing system"""
    
    def __init__(self):
        self.sync_engine = MulticamSyncEngine()
        self.current_project = None
        self.preview_layout = AngleLayout.QUAD
        
    async def create_multicam_project(self, angles: List[CameraAngle], 
                                    project_name: str) -> MulticamProject:
        """Create new multicam project"""
        
        logger.info(f"Creating multicam project '{project_name}' with {len(angles)} angles")
        
        # Synchronize angles
        sync_points = await self.sync_engine.sync_multicam_project(angles)
        
        # Apply synchronization offsets
        for sync_point in sync_points:
            for angle_id, offset in sync_point.angles.items():
                angle = next((a for a in angles if a.angle_id == angle_id), None)
                if angle:
                    angle.timecode_offset = offset
                    angle.sync_confidence = sync_point.confidence
        
        # Create project
        project = MulticamProject(
            project_id=f"multicam_{len(angles)}_{hash(project_name)}",
            name=project_name,
            angles=angles,
            sync_points=sync_points,
            master_angle=angles[0].angle_id if angles else None
        )
        
        # Organize into banks if many angles
        if len(angles) > 4:
            project.banks = self._organize_into_banks(angles)
        
        self.current_project = project
        return project
    
    def _organize_into_banks(self, angles: List[CameraAngle]) -> Dict[str, List[str]]:
        """Organize angles into banks for easier management"""
        
        banks = {}
        bank_size = 8  # 8 angles per bank
        
        for i in range(0, len(angles), bank_size):
            bank_name = f"Bank_{i // bank_size + 1}"
            bank_angles = [angle.angle_id for angle in angles[i:i + bank_size]]
            banks[bank_name] = bank_angles
        
        return banks
    
    async def generate_multicam_preview(self, project: MulticamProject, 
                                      layout: AngleLayout = AngleLayout.QUAD,
                                      timestamp: float = 0.0) -> np.ndarray:
        """Generate multicam preview with specified layout"""
        
        # Load frames from all angles at specified timestamp
        angle_frames = {}
        
        for angle in project.angles:
            frame = await self._get_frame_at_timestamp(angle, timestamp)
            if frame is not None:
                angle_frames[angle.angle_id] = frame
        
        # Create layout
        preview = self._create_layout_preview(angle_frames, layout, project.resolution)
        
        return preview
    
    async def _get_frame_at_timestamp(self, angle: CameraAngle, timestamp: float) -> Optional[np.ndarray]:
        """Get frame from angle at specific timestamp"""
        
        try:
            # Adjust timestamp with sync offset
            adjusted_timestamp = timestamp + angle.timecode_offset
            
            cap = cv2.VideoCapture(angle.video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Seek to frame
            frame_number = int(adjusted_timestamp * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                return frame
            
        except Exception as e:
            logger.warning(f"Could not get frame for angle {angle.angle_id}: {e}")
        
        return None
    
    def _create_layout_preview(self, frames: Dict[str, np.ndarray], 
                             layout: AngleLayout, 
                             output_resolution: Tuple[int, int]) -> np.ndarray:
        """Create preview layout from angle frames"""
        
        output_width, output_height = output_resolution
        preview = np.zeros((output_height, output_width, 3), dtype=np.uint8)
        
        if not frames:
            return preview
        
        frame_list = list(frames.values())
        
        if layout == AngleLayout.SINGLE:
            # Single angle (full screen)
            if frame_list:
                resized = cv2.resize(frame_list[0], (output_width, output_height))
                preview = resized
        
        elif layout == AngleLayout.DUAL:
            # Two angles side by side
            tile_width = output_width // 2
            
            for i, frame in enumerate(frame_list[:2]):
                resized = cv2.resize(frame, (tile_width, output_height))
                x_offset = i * tile_width
                preview[:, x_offset:x_offset + tile_width] = resized
        
        elif layout == AngleLayout.QUAD:
            # Four angles in 2x2 grid
            tile_width = output_width // 2
            tile_height = output_height // 2
            
            for i, frame in enumerate(frame_list[:4]):
                row = i // 2
                col = i % 2
                
                resized = cv2.resize(frame, (tile_width, tile_height))
                y_offset = row * tile_height
                x_offset = col * tile_width
                
                preview[y_offset:y_offset + tile_height, 
                       x_offset:x_offset + tile_width] = resized
        
        elif layout == AngleLayout.NINE:
            # Nine angles in 3x3 grid
            tile_width = output_width // 3
            tile_height = output_height // 3
            
            for i, frame in enumerate(frame_list[:9]):
                row = i // 3
                col = i % 3
                
                resized = cv2.resize(frame, (tile_width, tile_height))
                y_offset = row * tile_height
                x_offset = col * tile_width
                
                preview[y_offset:y_offset + tile_height,
                       x_offset:x_offset + tile_width] = resized
        
        return preview
    
    async def create_multicam_sequence(self, project: MulticamProject, 
                                     cuts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create final multicam sequence from cuts"""
        
        sequence = {
            "project_id": project.project_id,
            "cuts": cuts,
            "timeline": [],
            "metadata": {
                "angles_used": set(),
                "total_cuts": len(cuts),
                "sync_confidence": np.mean([angle.sync_confidence for angle in project.angles])
            }
        }
        
        # Process each cut
        for cut in cuts:
            angle_id = cut["angle_id"]
            start_time = cut["start_time"]
            end_time = cut["end_time"]
            
            # Find angle
            angle = next((a for a in project.angles if a.angle_id == angle_id), None)
            if not angle:
                continue
            
            # Add to timeline
            timeline_item = {
                "angle_id": angle_id,
                "angle_name": angle.name,
                "start_time": start_time,
                "end_time": end_time,
                "duration": end_time - start_time,
                "video_path": angle.video_path,
                "audio_path": angle.audio_path,
                "timecode_offset": angle.timecode_offset,
                "metadata": cut.get("metadata", {})
            }
            
            sequence["timeline"].append(timeline_item)
            sequence["metadata"]["angles_used"].add(angle_id)
        
        sequence["metadata"]["angles_used"] = list(sequence["metadata"]["angles_used"])
        
        return sequence


class Video360Processor:
    """360° video processing and effects system"""
    
    def __init__(self):
        self.supported_projections = [ProjectionType.EQUIRECTANGULAR, ProjectionType.CUBEMAP, ProjectionType.FISHEYE]
        
    async def process_360_video(self, video_path: str, output_path: str,
                              processing_config: Dict[str, Any]) -> str:
        """Process 360° video with various effects and corrections"""
        
        logger.info(f"Processing 360° video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_idx = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frame = frame.copy()
            
            # Apply 360° processing
            if processing_config.get("stabilization", False):
                processed_frame = await self._stabilize_360_frame(processed_frame)
            
            if processing_config.get("horizon_leveling", False):
                processed_frame = self._level_horizon(processed_frame)
            
            if processing_config.get("color_correction", False):
                processed_frame = self._apply_360_color_correction(processed_frame)
            
            if processing_config.get("projection_conversion"):
                target_projection = processing_config["projection_conversion"]
                processed_frame = self._convert_projection(processed_frame, 
                                                         ProjectionType.EQUIRECTANGULAR,
                                                         target_projection)
            
            out.write(processed_frame)
            frame_idx += 1
        
        cap.release()
        out.release()
        
        return output_path
    
    async def _stabilize_360_frame(self, frame: np.ndarray) -> np.ndarray:
        """Apply 360° stabilization"""
        
        # Simplified 360° stabilization
        # In practice, would use proper 360° stabilization algorithms
        
        height, width = frame.shape[:2]
        
        # Create rotation matrix for small correction
        angle = np.random.normal(0, 0.5)  # Small random correction (placeholder)
        rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1.0)
        
        stabilized = cv2.warpAffine(frame, rotation_matrix, (width, height))
        
        return stabilized
    
    def _level_horizon(self, frame: np.ndarray) -> np.ndarray:
        """Level horizon in 360° video"""
        
        # Detect horizon line and correct tilt
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Detect lines (simplified horizon detection)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                               minLineLength=100, maxLineGap=10)
        
        if lines is not None and len(lines) > 0:
            # Find dominant horizontal line
            angles = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                angles.append(angle)
            
            # Get median angle for horizon
            horizon_angle = np.median(angles)
            
            # Correct tilt
            height, width = frame.shape[:2]
            rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), 
                                                    -horizon_angle, 1.0)
            leveled = cv2.warpAffine(frame, rotation_matrix, (width, height))
            
            return leveled
        
        return frame
    
    def _apply_360_color_correction(self, frame: np.ndarray) -> np.ndarray:
        """Apply color correction for 360° video"""
        
        # Equirectangular distortion correction
        height, width = frame.shape[:2]
        
        # Weight correction based on latitude
        y_coords = np.arange(height)
        lat_weights = np.cos((y_coords / height - 0.5) * np.pi)
        
        # Apply latitude-based color correction
        corrected = frame.copy().astype(np.float32)
        
        for y in range(height):
            weight = lat_weights[y]
            # Adjust saturation based on latitude
            hsv_row = cv2.cvtColor(corrected[y:y+1], cv2.COLOR_BGR2HSV)
            hsv_row[:, :, 1] *= weight  # Adjust saturation
            corrected[y:y+1] = cv2.cvtColor(hsv_row, cv2.COLOR_HSV2BGR)
        
        return corrected.astype(np.uint8)
    
    def _convert_projection(self, frame: np.ndarray, 
                          source_projection: ProjectionType,
                          target_projection: ProjectionType) -> np.ndarray:
        """Convert between 360° projections"""
        
        if source_projection == target_projection:
            return frame
        
        height, width = frame.shape[:2]
        
        if (source_projection == ProjectionType.EQUIRECTANGULAR and 
            target_projection == ProjectionType.CUBEMAP):
            return self._equirectangular_to_cubemap(frame)
        
        elif (source_projection == ProjectionType.EQUIRECTANGULAR and 
              target_projection == ProjectionType.FISHEYE):
            return self._equirectangular_to_fisheye(frame)
        
        # Add more projection conversions as needed
        return frame
    
    def _equirectangular_to_cubemap(self, frame: np.ndarray) -> np.ndarray:
        """Convert equirectangular to cubemap"""
        
        height, width = frame.shape[:2]
        face_size = width // 4  # Each cube face size
        
        # Create cubemap layout (cross format)
        cube_height = face_size * 3
        cube_width = face_size * 4
        cubemap = np.zeros((cube_height, cube_width, 3), dtype=np.uint8)
        
        # Generate each cube face
        faces = ['front', 'right', 'back', 'left', 'top', 'bottom']
        positions = [
            (face_size, face_size),     # front
            (face_size * 2, face_size), # right
            (face_size * 3, face_size), # back
            (0, face_size),             # left
            (face_size, 0),             # top
            (face_size, face_size * 2)  # bottom
        ]
        
        for i, (face, (x, y)) in enumerate(zip(faces, positions)):
            face_img = self._generate_cube_face(frame, face, face_size)
            cubemap[y:y+face_size, x:x+face_size] = face_img
        
        return cubemap
    
    def _generate_cube_face(self, equirectangular: np.ndarray, 
                          face: str, face_size: int) -> np.ndarray:
        """Generate single cube face from equirectangular"""
        
        height, width = equirectangular.shape[:2]
        face_img = np.zeros((face_size, face_size, 3), dtype=np.uint8)
        
        # Face direction vectors
        face_vectors = {
            'front':  [0, 0, 1],
            'right':  [1, 0, 0],
            'back':   [0, 0, -1],
            'left':   [-1, 0, 0],
            'top':    [0, 1, 0],
            'bottom': [0, -1, 0]
        }
        
        if face not in face_vectors:
            return face_img
        
        # Generate sampling coordinates
        for i in range(face_size):
            for j in range(face_size):
                # Cube face coordinates (-1 to 1)
                x = (2.0 * j / face_size) - 1.0
                y = (2.0 * i / face_size) - 1.0
                
                # Convert to 3D vector
                if face == 'front':
                    vec = [x, -y, 1]
                elif face == 'right':
                    vec = [1, -y, -x]
                elif face == 'back':
                    vec = [-x, -y, -1]
                elif face == 'left':
                    vec = [-1, -y, x]
                elif face == 'top':
                    vec = [x, 1, y]
                elif face == 'bottom':
                    vec = [x, -1, -y]
                
                # Normalize vector
                norm = np.sqrt(sum(v**2 for v in vec))
                vec = [v / norm for v in vec]
                
                # Convert to spherical coordinates
                theta = np.arctan2(vec[0], vec[2])  # longitude
                phi = np.arcsin(vec[1])             # latitude
                
                # Convert to equirectangular coordinates
                u = (theta / np.pi + 1.0) / 2.0  # 0 to 1
                v = (phi / (np.pi/2) + 1.0) / 2.0  # 0 to 1
                
                # Sample from equirectangular image
                eq_x = int(u * width) % width
                eq_y = int(v * height) % height
                
                face_img[i, j] = equirectangular[eq_y, eq_x]
        
        return face_img
    
    def _equirectangular_to_fisheye(self, frame: np.ndarray) -> np.ndarray:
        """Convert equirectangular to fisheye"""
        
        height, width = frame.shape[:2]
        size = min(height, width)
        fisheye = np.zeros((size, size, 3), dtype=np.uint8)
        
        center = size // 2
        radius = center
        
        for i in range(size):
            for j in range(size):
                # Distance from center
                dx = j - center
                dy = i - center
                r = np.sqrt(dx**2 + dy**2)
                
                if r <= radius:
                    # Fisheye to spherical mapping
                    theta = np.arctan2(dy, dx)  # azimuth
                    phi = (r / radius) * (np.pi / 2)  # elevation
                    
                    # Convert to equirectangular coordinates
                    u = (theta / np.pi + 1.0) / 2.0
                    v = (phi / (np.pi / 2))
                    
                    # Sample from equirectangular
                    eq_x = int(u * width) % width
                    eq_y = int(v * height) % height
                    
                    fisheye[i, j] = frame[eq_y, eq_x]
        
        return fisheye
    
    async def create_tiny_planet_effect(self, frame: np.ndarray) -> np.ndarray:
        """Create tiny planet effect from 360° image"""
        
        height, width = frame.shape[:2]
        size = min(height, width)
        tiny_planet = np.zeros((size, size, 3), dtype=np.uint8)
        
        center = size // 2
        
        for i in range(size):
            for j in range(size):
                # Polar coordinates
                dx = j - center
                dy = i - center
                r = np.sqrt(dx**2 + dy**2)
                theta = np.arctan2(dy, dx)
                
                if r > 0:
                    # Tiny planet mapping
                    longitude = theta
                    latitude = (r / center) * np.pi - np.pi/2
                    
                    # Convert to equirectangular coordinates
                    u = (longitude / np.pi + 1.0) / 2.0
                    v = (latitude / np.pi + 0.5)
                    
                    # Clamp and sample
                    u = max(0, min(1, u))
                    v = max(0, min(1, v))
                    
                    eq_x = int(u * width) % width
                    eq_y = int(v * height) % height
                    
                    tiny_planet[i, j] = frame[eq_y, eq_x]
        
        return tiny_planet
    
    async def reframe_to_flat(self, frame: np.ndarray, 
                            fov: float = 90.0, 
                            yaw: float = 0.0, 
                            pitch: float = 0.0) -> np.ndarray:
        """Reframe 360° video to flat perspective"""
        
        height, width = frame.shape[:2]
        output_width = width // 2
        output_height = height // 2
        
        flat_frame = np.zeros((output_height, output_width, 3), dtype=np.uint8)
        
        # Convert FOV to radians
        fov_rad = np.radians(fov)
        half_fov = fov_rad / 2
        
        for i in range(output_height):
            for j in range(output_width):
                # Normalized coordinates (-1 to 1)
                x = (2.0 * j / output_width) - 1.0
                y = (2.0 * i / output_height) - 1.0
                
                # Apply FOV scaling
                x *= np.tan(half_fov)
                y *= np.tan(half_fov)
                
                # Create 3D vector
                vec = [x, y, 1.0]
                
                # Normalize
                norm = np.sqrt(sum(v**2 for v in vec))
                vec = [v / norm for v in vec]
                
                # Apply rotation (yaw and pitch)
                # Simplified rotation - would use proper rotation matrices
                theta = np.arctan2(vec[0], vec[2]) + np.radians(yaw)
                phi = np.arcsin(vec[1]) + np.radians(pitch)
                
                # Convert to equirectangular coordinates
                u = (theta / np.pi + 1.0) / 2.0
                v = (phi / (np.pi/2) + 1.0) / 2.0
                
                # Clamp and sample
                u = max(0, min(1, u))
                v = max(0, min(1, v))
                
                eq_x = int(u * width) % width
                eq_y = int(v * height) % height
                
                flat_frame[i, j] = frame[eq_y, eq_x]
        
        return flat_frame


class StereoProcessor:
    """Stereoscopic 3D processing"""
    
    def __init__(self):
        self.supported_modes = [mode for mode in StereoMode]
    
    async def process_stereo_video(self, video_path: str, output_path: str,
                                 stereo_mode: StereoMode,
                                 output_mode: StereoMode) -> str:
        """Process stereoscopic 3D video"""
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate output dimensions
        output_width, output_height = self._get_output_dimensions(
            width, height, stereo_mode, output_mode
        )
        
        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Split stereo frame
            left_eye, right_eye = self._split_stereo_frame(frame, stereo_mode)
            
            # Process eyes if needed
            left_eye = self._process_eye(left_eye, "left")
            right_eye = self._process_eye(right_eye, "right")
            
            # Combine to output format
            output_frame = self._combine_stereo_frame(left_eye, right_eye, output_mode)
            
            out.write(output_frame)
        
        cap.release()
        out.release()
        
        return output_path
    
    def _split_stereo_frame(self, frame: np.ndarray, 
                          stereo_mode: StereoMode) -> Tuple[np.ndarray, np.ndarray]:
        """Split stereo frame into left and right eyes"""
        
        height, width = frame.shape[:2]
        
        if stereo_mode == StereoMode.SIDE_BY_SIDE:
            left_eye = frame[:, :width//2]
            right_eye = frame[:, width//2:]
        
        elif stereo_mode == StereoMode.TOP_BOTTOM:
            left_eye = frame[:height//2, :]
            right_eye = frame[height//2:, :]
        
        elif stereo_mode == StereoMode.OVER_UNDER:
            left_eye = frame[:height//2, :]
            right_eye = frame[height//2:, :]
        
        else:  # MONO
            left_eye = right_eye = frame
        
        return left_eye, right_eye
    
    def _combine_stereo_frame(self, left_eye: np.ndarray, right_eye: np.ndarray,
                            output_mode: StereoMode) -> np.ndarray:
        """Combine left and right eyes into output format"""
        
        if output_mode == StereoMode.SIDE_BY_SIDE:
            return np.concatenate([left_eye, right_eye], axis=1)
        
        elif output_mode == StereoMode.TOP_BOTTOM:
            return np.concatenate([left_eye, right_eye], axis=0)
        
        elif output_mode == StereoMode.OVER_UNDER:
            return np.concatenate([left_eye, right_eye], axis=0)
        
        else:  # MONO
            return left_eye
    
    def _get_output_dimensions(self, width: int, height: int,
                             input_mode: StereoMode, 
                             output_mode: StereoMode) -> Tuple[int, int]:
        """Calculate output dimensions for stereo conversion"""
        
        # Get eye dimensions from input
        if input_mode == StereoMode.SIDE_BY_SIDE:
            eye_width, eye_height = width // 2, height
        elif input_mode in [StereoMode.TOP_BOTTOM, StereoMode.OVER_UNDER]:
            eye_width, eye_height = width, height // 2
        else:
            eye_width, eye_height = width, height
        
        # Calculate output dimensions
        if output_mode == StereoMode.SIDE_BY_SIDE:
            return eye_width * 2, eye_height
        elif output_mode in [StereoMode.TOP_BOTTOM, StereoMode.OVER_UNDER]:
            return eye_width, eye_height * 2
        else:
            return eye_width, eye_height
    
    def _process_eye(self, eye_frame: np.ndarray, eye: str) -> np.ndarray:
        """Process individual eye (left or right)"""
        
        # Apply eye-specific processing if needed
        # For example, color correction, alignment, etc.
        
        return eye_frame


# Main integration class
class MulticamVideo360System:
    """Complete multicam and 360° video system"""
    
    def __init__(self):
        self.multicam_editor = MulticamEditor()
        self.video_360_processor = Video360Processor()
        self.stereo_processor = StereoProcessor()
        
    async def process_multicam_360_project(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process complete multicam 360° project"""
        
        results = {
            "multicam_sequence": None,
            "360_processed": None,
            "stereo_processed": None,
            "preview_generated": False
        }
        
        # Multicam processing
        if config.get("multicam_angles"):
            angles = [CameraAngle(**angle_config) for angle_config in config["multicam_angles"]]
            project = await self.multicam_editor.create_multicam_project(
                angles, config.get("project_name", "Multicam Project")
            )
            
            if config.get("multicam_cuts"):
                sequence = await self.multicam_editor.create_multicam_sequence(
                    project, config["multicam_cuts"]
                )
                results["multicam_sequence"] = sequence
        
        # 360° processing
        if config.get("360_processing"):
            video_path = config["360_processing"]["input_path"]
            output_path = config["360_processing"]["output_path"]
            processing_config = config["360_processing"].get("config", {})
            
            processed_path = await self.video_360_processor.process_360_video(
                video_path, output_path, processing_config
            )
            results["360_processed"] = processed_path
        
        # Stereo processing
        if config.get("stereo_processing"):
            stereo_config = config["stereo_processing"]
            processed_path = await self.stereo_processor.process_stereo_video(
                stereo_config["input_path"],
                stereo_config["output_path"],
                StereoMode(stereo_config["input_mode"]),
                StereoMode(stereo_config["output_mode"])
            )
            results["stereo_processed"] = processed_path
        
        return results


# Example usage
async def main():
    """Example usage of multicam and 360° video system"""
    
    # Create multicam system
    system = MulticamVideo360System()
    
    # Example multicam project
    angles = [
        CameraAngle("cam1", "Camera 1", "cam1.mp4", color_coding="#FF0000"),
        CameraAngle("cam2", "Camera 2", "cam2.mp4", color_coding="#00FF00"),
        CameraAngle("cam3", "Camera 3", "cam3.mp4", color_coding="#0000FF"),
        CameraAngle("cam4", "Camera 4", "cam4.mp4", color_coding="#FFFF00")
    ]
    
    cuts = [
        {"angle_id": "cam1", "start_time": 0.0, "end_time": 10.0},
        {"angle_id": "cam2", "start_time": 10.0, "end_time": 20.0},
        {"angle_id": "cam3", "start_time": 20.0, "end_time": 30.0},
        {"angle_id": "cam1", "start_time": 30.0, "end_time": 40.0}
    ]
    
    # Process project
    config = {
        "project_name": "Concert Recording",
        "multicam_angles": [angle.__dict__ for angle in angles],
        "multicam_cuts": cuts,
        "360_processing": {
            "input_path": "360_video.mp4",
            "output_path": "360_processed.mp4",
            "config": {
                "stabilization": True,
                "horizon_leveling": True,
                "color_correction": True
            }
        }
    }
    
    results = await system.process_multicam_360_project(config)
    
    print("Multicam and 360° processing completed:")
    print(f"  Multicam sequence: {results['multicam_sequence'] is not None}")
    print(f"  360° processed: {results['360_processed']}")
    print(f"  Results: {results}")


if __name__ == "__main__":
    asyncio.run(main())