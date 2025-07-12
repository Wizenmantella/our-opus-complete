#!/usr/bin/env python3
"""
Advanced AI Analysis Engine
Complete AI-powered video analysis system with scene detection, content understanding, and intelligent recommendations.

Features:
- Scene cut detection with multiple algorithms
- Auto reframe/smart conform
- Content-aware analysis
- Face recognition and tracking
- Object detection and classification
- Depth map generation
- Motion analysis and camera movement detection
- Audio content analysis
- Emotion and sentiment analysis
- Style detection and recommendation
- Beat detection and rhythm analysis
- Auto highlight detection
- Smart trimming suggestions
- Content categorization
- Quality assessment
- Auto-transcription and caption generation
"""

import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration
from ultralytics import YOLO
import librosa
import soundfile as sf
from scipy import signal
from scipy.spatial.distance import cosine
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Any, Union
import asyncio
import logging
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import json
import pickle
from datetime import datetime, timedelta
import mediapipe as mp
import openai
from anthropic import Anthropic

# Audio analysis
import aubio
import essentia
import essentia.standard as es

logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Content type classifications"""
    INTERVIEW = "interview"
    DOCUMENTARY = "documentary"
    MUSIC_VIDEO = "music_video"
    VLOG = "vlog"
    EDUCATIONAL = "educational"
    COMMERCIAL = "commercial"
    SOCIAL_MEDIA = "social_media"
    FILM = "film"
    SPORTS = "sports"
    NEWS = "news"
    GAMING = "gaming"
    LIVESTREAM = "livestream"


class SceneType(Enum):
    """Scene type classifications"""
    CLOSE_UP = "close_up"
    MEDIUM_SHOT = "medium_shot"
    WIDE_SHOT = "wide_shot"
    EXTREME_CLOSE_UP = "extreme_close_up"
    EXTREME_WIDE_SHOT = "extreme_wide_shot"
    OVER_SHOULDER = "over_shoulder"
    TWO_SHOT = "two_shot"
    GROUP_SHOT = "group_shot"
    CUTAWAY = "cutaway"
    INSERT = "insert"


class CameraMovement(Enum):
    """Camera movement types"""
    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOLLY_IN = "dolly_in"
    DOLLY_OUT = "dolly_out"
    HANDHELD = "handheld"
    STABILIZED = "stabilized"


class EmotionalTone(Enum):
    """Emotional tone classifications"""
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CALM = "calm"
    ANGRY = "angry"
    SURPRISED = "surprised"
    FEARFUL = "fearful"
    DISGUSTED = "disgusted"
    NEUTRAL = "neutral"
    ENERGETIC = "energetic"
    MYSTERIOUS = "mysterious"
    ROMANTIC = "romantic"


@dataclass
class SceneInfo:
    """Scene information structure"""
    start_frame: int
    end_frame: int
    start_time: float
    end_time: float
    duration: float
    scene_type: SceneType
    camera_movement: CameraMovement
    emotional_tone: EmotionalTone
    objects: List[Dict[str, Any]] = field(default_factory=list)
    faces: List[Dict[str, Any]] = field(default_factory=list)
    audio_features: Dict[str, Any] = field(default_factory=dict)
    visual_features: Dict[str, Any] = field(default_factory=dict)
    quality_score: float = 0.0
    importance_score: float = 0.0
    highlight_potential: float = 0.0


@dataclass
class ContentAnalysis:
    """Complete content analysis structure"""
    content_type: ContentType
    overall_tone: EmotionalTone
    pacing: str
    energy_level: float
    scenes: List[SceneInfo]
    transitions: List[Dict[str, Any]]
    highlights: List[Dict[str, Any]]
    audio_analysis: Dict[str, Any]
    visual_style: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    recommendations: Dict[str, Any]


class AdvancedAIAnalysisEngine:
    """Advanced AI analysis engine for comprehensive video understanding"""
    
    def __init__(self, device: str = "auto"):
        self.device = self._setup_device(device)
        
        # AI Models
        self.yolo_model = None
        self.depth_model = None
        self.emotion_model = None
        self.whisper_model = None
        self.whisper_processor = None
        self.scene_classifier = None
        self.style_classifier = None
        
        # MediaPipe components
        self.mp_face_detection = None
        self.mp_pose = None
        self.mp_hands = None
        self.mp_face_mesh = None
        
        # Audio analysis tools
        self.tempo_tracker = None
        self.onset_detector = None
        self.pitch_tracker = None
        
        # Analysis cache
        self.analysis_cache = {}
        
        # Feature extractors
        self.visual_features = VisualFeatureExtractor()
        self.audio_features = AudioFeatureExtractor()
        self.scene_detector = SceneDetector()
        self.object_tracker = ObjectTracker()
        
        logger.info("Advanced AI Analysis Engine initialized")
    
    def _setup_device(self, device: str) -> str:
        """Setup compute device"""
        if device == "auto":
            if torch.backends.mps.is_available():
                return "mps"
            elif torch.cuda.is_available():
                return "cuda"
            else:
                return "cpu"
        return device
    
    def _load_ai_models(self):
        """Load all AI models"""
        try:
            # Object detection
            if self.yolo_model is None:
                self.yolo_model = YOLO('yolov8x.pt')  # Use largest model for best accuracy
            
            # Depth estimation
            if self.depth_model is None:
                self.depth_model = pipeline("depth-estimation", model="Intel/dpt-large")
            
            # Emotion recognition
            if self.emotion_model is None:
                self.emotion_model = pipeline("image-classification", 
                                            model="j-hartmann/emotion-english-distilroberta-base")
            
            # Speech recognition
            if self.whisper_model is None:
                self.whisper_processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
                self.whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
            
            # MediaPipe
            if self.mp_face_detection is None:
                self.mp_face_detection = mp.solutions.face_detection.FaceDetection(
                    model_selection=1, min_detection_confidence=0.5)
                self.mp_pose = mp.solutions.pose.Pose(
                    static_image_mode=False, model_complexity=2, 
                    enable_segmentation=True, min_detection_confidence=0.5)
                self.mp_hands = mp.solutions.hands.Hands(
                    static_image_mode=False, max_num_hands=2, 
                    min_detection_confidence=0.5)
                self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
                    static_image_mode=False, max_num_faces=5, 
                    refine_landmarks=True, min_detection_confidence=0.5)
            
            # Audio analysis
            if self.tempo_tracker is None:
                self.tempo_tracker = aubio.tempo("default", 512, 256, 44100)
                self.onset_detector = aubio.onset("default", 512, 256, 44100)
                self.pitch_tracker = aubio.pitch("default", 512, 256, 44100)
            
            logger.info("All AI models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading AI models: {e}")
    
    async def analyze_video_comprehensive(self, video_path: str, 
                                        audio_path: Optional[str] = None,
                                        config: Optional[Dict[str, Any]] = None) -> ContentAnalysis:
        """Perform comprehensive video analysis"""
        
        logger.info(f"Starting comprehensive analysis of {video_path}")
        
        # Load models
        self._load_ai_models()
        
        # Default config
        if config is None:
            config = {
                "scene_detection": True,
                "object_detection": True,
                "face_analysis": True,
                "emotion_analysis": True,
                "audio_analysis": True,
                "quality_assessment": True,
                "highlight_detection": True,
                "style_analysis": True,
                "transcription": True
            }
        
        # Load video
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps
        
        logger.info(f"Video info: {total_frames} frames, {fps} fps, {duration:.2f}s")
        
        # Scene detection
        scenes = []
        if config["scene_detection"]:
            scenes = await self.scene_detector.detect_scenes(video_path)
            logger.info(f"Detected {len(scenes)} scenes")
        
        # Visual analysis
        visual_analysis = await self._analyze_visual_content(cap, scenes, config)
        
        # Audio analysis
        audio_analysis = {}
        if config["audio_analysis"]:
            audio_analysis = await self.audio_features.analyze_audio(
                audio_path or video_path)
            logger.info("Audio analysis completed")
        
        # Content type classification
        content_type = await self._classify_content_type(visual_analysis, audio_analysis)
        
        # Overall tone and style analysis
        overall_tone, visual_style = await self._analyze_style_and_tone(
            visual_analysis, audio_analysis)
        
        # Quality assessment
        quality_metrics = {}
        if config["quality_assessment"]:
            quality_metrics = await self._assess_video_quality(visual_analysis)
        
        # Highlight detection
        highlights = []
        if config["highlight_detection"]:
            highlights = await self._detect_highlights(scenes, audio_analysis)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(
            content_type, scenes, audio_analysis, quality_metrics)
        
        # Calculate transitions
        transitions = await self._analyze_transitions(scenes)
        
        # Calculate energy level and pacing
        energy_level = self._calculate_energy_level(scenes, audio_analysis)
        pacing = self._determine_pacing(scenes, audio_analysis)
        
        cap.release()
        
        # Create comprehensive analysis
        analysis = ContentAnalysis(
            content_type=content_type,
            overall_tone=overall_tone,
            pacing=pacing,
            energy_level=energy_level,
            scenes=scenes,
            transitions=transitions,
            highlights=highlights,
            audio_analysis=audio_analysis,
            visual_style=visual_style,
            quality_metrics=quality_metrics,
            recommendations=recommendations
        )
        
        logger.info("Comprehensive analysis completed")
        return analysis
    
    async def _analyze_visual_content(self, cap: cv2.VideoCapture, 
                                    scenes: List[SceneInfo], 
                                    config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visual content comprehensively"""
        
        visual_analysis = {
            "frame_analysis": [],
            "object_detections": [],
            "face_detections": [],
            "emotions": [],
            "camera_movements": [],
            "shot_types": [],
            "color_analysis": [],
            "composition_analysis": [],
            "motion_analysis": []
        }
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Sample frames for analysis (every 30 frames for performance)
        sample_interval = max(1, total_frames // 200)  # Max 200 samples
        
        prev_frame = None
        frame_idx = 0
        
        while frame_idx < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                break
            
            timestamp = frame_idx / fps
            
            # Frame-level analysis
            frame_analysis = {
                "frame": frame_idx,
                "timestamp": timestamp,
                "analysis": {}
            }
            
            # Object detection
            if config.get("object_detection", True):
                objects = await self._detect_objects_frame(frame)
                frame_analysis["analysis"]["objects"] = objects
                visual_analysis["object_detections"].extend(objects)
            
            # Face detection and analysis
            if config.get("face_analysis", True):
                faces = await self._analyze_faces_frame(frame)
                frame_analysis["analysis"]["faces"] = faces
                visual_analysis["face_detections"].extend(faces)
            
            # Emotion analysis
            if config.get("emotion_analysis", True):
                emotions = await self._analyze_emotions_frame(frame)
                frame_analysis["analysis"]["emotions"] = emotions
                visual_analysis["emotions"].extend(emotions)
            
            # Camera movement analysis
            if prev_frame is not None:
                movement = await self._analyze_camera_movement(prev_frame, frame)
                frame_analysis["analysis"]["camera_movement"] = movement
                visual_analysis["camera_movements"].append(movement)
            
            # Shot type classification
            shot_type = await self._classify_shot_type(frame)
            frame_analysis["analysis"]["shot_type"] = shot_type
            visual_analysis["shot_types"].append(shot_type)
            
            # Color analysis
            color_analysis = await self._analyze_colors(frame)
            frame_analysis["analysis"]["color"] = color_analysis
            visual_analysis["color_analysis"].append(color_analysis)
            
            # Composition analysis
            composition = await self._analyze_composition(frame)
            frame_analysis["analysis"]["composition"] = composition
            visual_analysis["composition_analysis"].append(composition)
            
            # Motion analysis
            if prev_frame is not None:
                motion = await self._analyze_motion(prev_frame, frame)
                frame_analysis["analysis"]["motion"] = motion
                visual_analysis["motion_analysis"].append(motion)
            
            visual_analysis["frame_analysis"].append(frame_analysis)
            
            prev_frame = frame.copy()
            frame_idx += sample_interval
        
        return visual_analysis
    
    async def _detect_objects_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Detect objects in single frame"""
        
        results = self.yolo_model(frame)
        objects = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    obj = {
                        "class": result.names[int(box.cls)],
                        "confidence": float(box.conf),
                        "bbox": box.xyxy[0].tolist(),
                        "normalized_bbox": box.xywhn[0].tolist(),
                        "area": float(box.xywh[0][2] * box.xywh[0][3])
                    }
                    objects.append(obj)
        
        return objects
    
    async def _analyze_faces_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze faces in single frame"""
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Face detection
        face_results = self.mp_face_detection.process(rgb_frame)
        faces = []
        
        if face_results.detections:
            for detection in face_results.detections:
                bbox = detection.location_data.relative_bounding_box
                
                face = {
                    "confidence": detection.score[0],
                    "bbox": [bbox.xmin, bbox.ymin, bbox.width, bbox.height],
                    "landmarks": [],
                    "attributes": {}
                }
                
                # Get face landmarks
                mesh_results = self.mp_face_mesh.process(rgb_frame)
                if mesh_results.multi_face_landmarks:
                    for face_landmarks in mesh_results.multi_face_landmarks:
                        landmarks = []
                        for landmark in face_landmarks.landmark:
                            landmarks.append([landmark.x, landmark.y, landmark.z])
                        face["landmarks"] = landmarks
                        break
                
                # Analyze face attributes
                face["attributes"] = await self._analyze_face_attributes(frame, bbox)
                
                faces.append(face)
        
        return faces
    
    async def _analyze_face_attributes(self, frame: np.ndarray, 
                                     bbox: List[float]) -> Dict[str, Any]:
        """Analyze face attributes"""
        
        height, width = frame.shape[:2]
        
        # Extract face region
        x = int(bbox[0] * width)
        y = int(bbox[1] * height)
        w = int(bbox[2] * width)
        h = int(bbox[3] * height)
        
        face_region = frame[y:y+h, x:x+w]
        
        if face_region.size == 0:
            return {}
        
        # Analyze attributes
        attributes = {
            "age_estimate": self._estimate_age(face_region),
            "gender_estimate": self._estimate_gender(face_region),
            "emotion": self._detect_emotion(face_region),
            "gaze_direction": self._estimate_gaze(face_region),
            "head_pose": self._estimate_head_pose(face_region)
        }
        
        return attributes
    
    def _estimate_age(self, face_region: np.ndarray) -> str:
        """Estimate age from face region"""
        # Simplified age estimation based on face features
        # In practice, would use a trained age estimation model
        gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        
        # Analyze texture and wrinkles
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        if edge_density > 0.1:
            return "senior"
        elif edge_density > 0.05:
            return "adult"
        else:
            return "young"
    
    def _estimate_gender(self, face_region: np.ndarray) -> str:
        """Estimate gender from face region"""
        # Simplified gender estimation
        # In practice, would use a trained gender classification model
        return "unknown"  # Placeholder
    
    def _detect_emotion(self, face_region: np.ndarray) -> Dict[str, float]:
        """Detect emotion from face region"""
        # Simplified emotion detection
        # In practice, would use emotion recognition model
        return {
            "happy": 0.5,
            "sad": 0.1,
            "angry": 0.1,
            "surprised": 0.1,
            "fear": 0.1,
            "disgust": 0.05,
            "neutral": 0.05
        }
    
    def _estimate_gaze(self, face_region: np.ndarray) -> Dict[str, float]:
        """Estimate gaze direction"""
        return {"x": 0.0, "y": 0.0, "confidence": 0.5}
    
    def _estimate_head_pose(self, face_region: np.ndarray) -> Dict[str, float]:
        """Estimate head pose"""
        return {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}
    
    async def _analyze_emotions_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze emotions in frame"""
        
        # Convert frame to PIL Image for emotion model
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Overall frame emotion
        try:
            emotion_result = self.emotion_model(rgb_frame)
            emotions = [{
                "type": "overall",
                "emotions": emotion_result,
                "dominant_emotion": max(emotion_result, key=lambda x: x['score'])
            }]
        except:
            emotions = []
        
        return emotions
    
    async def _analyze_camera_movement(self, prev_frame: np.ndarray, 
                                     curr_frame: np.ndarray) -> Dict[str, Any]:
        """Analyze camera movement between frames"""
        
        # Convert to grayscale
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        # Detect features
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(prev_gray, None)
        kp2, des2 = orb.detectAndCompute(curr_gray, None)
        
        if des1 is None or des2 is None:
            return {"movement_type": CameraMovement.STATIC, "magnitude": 0.0}
        
        # Match features
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        
        if len(matches) < 10:
            return {"movement_type": CameraMovement.STATIC, "magnitude": 0.0}
        
        # Extract matched points
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        
        # Calculate homography
        try:
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if M is None:
                return {"movement_type": CameraMovement.STATIC, "magnitude": 0.0}
        except:
            return {"movement_type": CameraMovement.STATIC, "magnitude": 0.0}
        
        # Analyze transformation
        movement_analysis = self._analyze_homography(M)
        
        return movement_analysis
    
    def _analyze_homography(self, homography: np.ndarray) -> Dict[str, Any]:
        """Analyze homography matrix to determine camera movement"""
        
        # Extract transformation components
        translation_x = homography[0, 2]
        translation_y = homography[1, 2]
        
        # Calculate scale
        scale_x = np.sqrt(homography[0, 0]**2 + homography[0, 1]**2)
        scale_y = np.sqrt(homography[1, 0]**2 + homography[1, 1]**2)
        
        # Calculate rotation
        rotation = np.arctan2(homography[1, 0], homography[0, 0])
        
        # Determine movement type
        movement_type = CameraMovement.STATIC
        magnitude = 0.0
        
        if abs(translation_x) > 5:
            movement_type = CameraMovement.PAN_RIGHT if translation_x > 0 else CameraMovement.PAN_LEFT
            magnitude = abs(translation_x)
        elif abs(translation_y) > 5:
            movement_type = CameraMovement.TILT_DOWN if translation_y > 0 else CameraMovement.TILT_UP
            magnitude = abs(translation_y)
        elif scale_x > 1.02 or scale_y > 1.02:
            movement_type = CameraMovement.ZOOM_IN
            magnitude = max(scale_x, scale_y) - 1.0
        elif scale_x < 0.98 or scale_y < 0.98:
            movement_type = CameraMovement.ZOOM_OUT
            magnitude = 1.0 - min(scale_x, scale_y)
        
        return {
            "movement_type": movement_type,
            "magnitude": magnitude,
            "translation": [translation_x, translation_y],
            "scale": [scale_x, scale_y],
            "rotation": rotation
        }
    
    async def _classify_shot_type(self, frame: np.ndarray) -> Dict[str, Any]:
        """Classify shot type based on frame content"""
        
        # Detect faces and people
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = self.mp_face_detection.process(rgb_frame)
        
        # Count faces and estimate sizes
        face_count = 0
        face_sizes = []
        
        if face_results.detections:
            face_count = len(face_results.detections)
            for detection in face_results.detections:
                bbox = detection.location_data.relative_bounding_box
                face_area = bbox.width * bbox.height
                face_sizes.append(face_area)
        
        # Classify shot type
        if face_count == 0:
            shot_type = SceneType.WIDE_SHOT
        elif face_count == 1:
            face_area = face_sizes[0]
            if face_area > 0.3:
                shot_type = SceneType.EXTREME_CLOSE_UP
            elif face_area > 0.15:
                shot_type = SceneType.CLOSE_UP
            elif face_area > 0.05:
                shot_type = SceneType.MEDIUM_SHOT
            else:
                shot_type = SceneType.WIDE_SHOT
        elif face_count == 2:
            shot_type = SceneType.TWO_SHOT
        else:
            shot_type = SceneType.GROUP_SHOT
        
        return {
            "shot_type": shot_type,
            "face_count": face_count,
            "average_face_size": np.mean(face_sizes) if face_sizes else 0.0,
            "confidence": 0.8
        }
    
    async def _analyze_colors(self, frame: np.ndarray) -> Dict[str, Any]:
        """Analyze color properties of frame"""
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Calculate color statistics
        color_analysis = {
            "dominant_colors": self._get_dominant_colors(frame),
            "brightness": np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)),
            "contrast": np.std(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)),
            "saturation": np.mean(hsv[:, :, 1]),
            "hue_distribution": self._analyze_hue_distribution(hsv),
            "temperature": self._estimate_color_temperature(frame),
            "mood": self._estimate_color_mood(frame)
        }
        
        return color_analysis
    
    def _get_dominant_colors(self, frame: np.ndarray, k: int = 5) -> List[List[int]]:
        """Extract dominant colors using k-means"""
        
        # Reshape frame for clustering
        pixels = frame.reshape(-1, 3)
        
        # Perform k-means clustering
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get dominant colors
        colors = kmeans.cluster_centers_.astype(int)
        
        # Sort by cluster size
        labels = kmeans.labels_
        color_counts = []
        for i in range(k):
            count = np.sum(labels == i)
            color_counts.append((count, colors[i]))
        
        color_counts.sort(reverse=True)
        dominant_colors = [color.tolist() for _, color in color_counts]
        
        return dominant_colors
    
    def _analyze_hue_distribution(self, hsv: np.ndarray) -> Dict[str, float]:
        """Analyze hue distribution"""
        
        hue_channel = hsv[:, :, 0]
        hist = cv2.calcHist([hue_channel], [0], None, [180], [0, 180])
        hist = hist.flatten() / hist.sum()
        
        # Define color ranges
        color_ranges = {
            "red": (0, 10),
            "orange": (10, 25),
            "yellow": (25, 35),
            "green": (35, 85),
            "cyan": (85, 95),
            "blue": (95, 125),
            "purple": (125, 155),
            "pink": (155, 170),
            "red2": (170, 180)
        }
        
        hue_distribution = {}
        for color, (start, end) in color_ranges.items():
            if color == "red2":
                hue_distribution["red"] += np.sum(hist[start:end])
            else:
                hue_distribution[color] = np.sum(hist[start:end])
        
        return hue_distribution
    
    def _estimate_color_temperature(self, frame: np.ndarray) -> str:
        """Estimate color temperature"""
        
        # Calculate average color
        avg_color = np.mean(frame, axis=(0, 1))
        b, g, r = avg_color
        
        # Simple color temperature estimation
        if b > r:
            return "cool"
        elif r > b * 1.2:
            return "warm"
        else:
            return "neutral"
    
    def _estimate_color_mood(self, frame: np.ndarray) -> str:
        """Estimate mood from colors"""
        
        dominant_colors = self._get_dominant_colors(frame, 3)
        
        # Analyze dominant colors for mood
        if any(color[0] < 50 and color[1] < 50 and color[2] < 50 for color in dominant_colors):
            return "dark"
        elif any(color[0] > 200 and color[1] > 200 and color[2] > 200 for color in dominant_colors):
            return "bright"
        elif any(color[0] > color[1] and color[0] > color[2] for color in dominant_colors):
            return "warm"
        elif any(color[2] > color[0] and color[2] > color[1] for color in dominant_colors):
            return "cool"
        else:
            return "neutral"
    
    async def _analyze_composition(self, frame: np.ndarray) -> Dict[str, Any]:
        """Analyze frame composition"""
        
        height, width = frame.shape[:2]
        
        # Rule of thirds analysis
        third_lines_v = [width // 3, 2 * width // 3]
        third_lines_h = [height // 3, 2 * height // 3]
        
        # Interest points at intersections
        interest_points = [
            (third_lines_v[0], third_lines_h[0]),
            (third_lines_v[1], third_lines_h[0]),
            (third_lines_v[0], third_lines_h[1]),
            (third_lines_v[1], third_lines_h[1])
        ]
        
        # Edge detection for leading lines
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Detect lines
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                               minLineLength=100, maxLineGap=10)
        
        # Analyze symmetry
        symmetry = self._analyze_symmetry(frame)
        
        # Calculate composition score
        composition_score = self._calculate_composition_score(frame, lines, symmetry)
        
        composition_analysis = {
            "rule_of_thirds_score": self._score_rule_of_thirds(frame, interest_points),
            "leading_lines_count": len(lines) if lines is not None else 0,
            "symmetry": symmetry,
            "composition_score": composition_score,
            "balance": self._analyze_visual_balance(frame),
            "depth_cues": self._analyze_depth_cues(frame)
        }
        
        return composition_analysis
    
    def _score_rule_of_thirds(self, frame: np.ndarray, 
                            interest_points: List[Tuple[int, int]]) -> float:
        """Score adherence to rule of thirds"""
        
        # Find areas of interest (high contrast regions)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate gradient magnitude
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Check activity near interest points
        score = 0.0
        for x, y in interest_points:
            # Define region around interest point
            x1, y1 = max(0, x-50), max(0, y-50)
            x2, y2 = min(frame.shape[1], x+50), min(frame.shape[0], y+50)
            
            region_activity = np.mean(magnitude[y1:y2, x1:x2])
            score += region_activity
        
        # Normalize score
        max_possible = np.max(magnitude) * len(interest_points)
        return score / max_possible if max_possible > 0 else 0.0
    
    def _analyze_symmetry(self, frame: np.ndarray) -> Dict[str, float]:
        """Analyze frame symmetry"""
        
        height, width = frame.shape[:2]
        
        # Vertical symmetry
        left_half = frame[:, :width//2]
        right_half = cv2.flip(frame[:, width//2:], 1)
        
        # Ensure same dimensions
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]
        
        vertical_symmetry = cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
        
        # Horizontal symmetry
        top_half = frame[:height//2, :]
        bottom_half = cv2.flip(frame[height//2:, :], 0)
        
        min_height = min(top_half.shape[0], bottom_half.shape[0])
        top_half = top_half[:min_height, :]
        bottom_half = bottom_half[:min_height, :]
        
        horizontal_symmetry = cv2.matchTemplate(top_half, bottom_half, cv2.TM_CCOEFF_NORMED)[0][0]
        
        return {
            "vertical": float(vertical_symmetry),
            "horizontal": float(horizontal_symmetry),
            "overall": (vertical_symmetry + horizontal_symmetry) / 2
        }
    
    def _calculate_composition_score(self, frame: np.ndarray, 
                                   lines: Optional[np.ndarray], 
                                   symmetry: Dict[str, float]) -> float:
        """Calculate overall composition score"""
        
        # Combine multiple composition factors
        symmetry_score = symmetry["overall"]
        line_score = min(1.0, len(lines) / 10) if lines is not None else 0.0
        
        # Add other composition factors
        composition_score = (symmetry_score + line_score) / 2
        
        return float(composition_score)
    
    def _analyze_visual_balance(self, frame: np.ndarray) -> Dict[str, float]:
        """Analyze visual balance of frame"""
        
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        
        # Calculate center of mass
        y_coords, x_coords = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
        total_mass = np.sum(gray)
        
        if total_mass > 0:
            center_x = np.sum(gray * x_coords) / total_mass
            center_y = np.sum(gray * y_coords) / total_mass
        else:
            center_x, center_y = width / 2, height / 2
        
        # Calculate balance scores
        x_balance = 1.0 - abs(center_x - width/2) / (width/2)
        y_balance = 1.0 - abs(center_y - height/2) / (height/2)
        
        return {
            "horizontal": float(x_balance),
            "vertical": float(y_balance),
            "overall": float((x_balance + y_balance) / 2)
        }
    
    def _analyze_depth_cues(self, frame: np.ndarray) -> Dict[str, Any]:
        """Analyze depth cues in frame"""
        
        # Blur detection for depth of field
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_metric = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Size variation analysis
        contours, _ = cv2.findContours(cv2.Canny(gray, 50, 150), 
                                     cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            areas = [cv2.contourArea(c) for c in contours]
            size_variation = np.std(areas) / np.mean(areas) if np.mean(areas) > 0 else 0
        else:
            size_variation = 0
        
        return {
            "depth_of_field": blur_metric,
            "size_variation": size_variation,
            "perspective_lines": 0  # Placeholder for perspective analysis
        }
    
    async def _analyze_motion(self, prev_frame: np.ndarray, 
                            curr_frame: np.ndarray) -> Dict[str, Any]:
        """Analyze motion between frames"""
        
        # Convert to grayscale
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, None, None)
        
        # Calculate motion statistics
        if flow[0] is not None and len(flow[0]) > 0:
            motion_vectors = flow[0] - flow[1] if flow[1] is not None else flow[0]
            motion_magnitude = np.linalg.norm(motion_vectors, axis=1)
            
            motion_analysis = {
                "average_motion": float(np.mean(motion_magnitude)),
                "max_motion": float(np.max(motion_magnitude)),
                "motion_variance": float(np.var(motion_magnitude)),
                "motion_direction": self._calculate_dominant_motion_direction(motion_vectors),
                "motion_smoothness": self._calculate_motion_smoothness(motion_vectors)
            }
        else:
            motion_analysis = {
                "average_motion": 0.0,
                "max_motion": 0.0,
                "motion_variance": 0.0,
                "motion_direction": "static",
                "motion_smoothness": 1.0
            }
        
        return motion_analysis
    
    def _calculate_dominant_motion_direction(self, motion_vectors: np.ndarray) -> str:
        """Calculate dominant motion direction"""
        
        if len(motion_vectors) == 0:
            return "static"
        
        # Calculate average motion vector
        avg_motion = np.mean(motion_vectors, axis=0)
        
        # Determine direction
        if np.linalg.norm(avg_motion) < 1.0:
            return "static"
        
        angle = np.arctan2(avg_motion[1], avg_motion[0]) * 180 / np.pi
        
        if -22.5 <= angle < 22.5:
            return "right"
        elif 22.5 <= angle < 67.5:
            return "down_right"
        elif 67.5 <= angle < 112.5:
            return "down"
        elif 112.5 <= angle < 157.5:
            return "down_left"
        elif 157.5 <= angle <= 180 or -180 <= angle < -157.5:
            return "left"
        elif -157.5 <= angle < -112.5:
            return "up_left"
        elif -112.5 <= angle < -67.5:
            return "up"
        elif -67.5 <= angle < -22.5:
            return "up_right"
        else:
            return "static"
    
    def _calculate_motion_smoothness(self, motion_vectors: np.ndarray) -> float:
        """Calculate motion smoothness"""
        
        if len(motion_vectors) < 2:
            return 1.0
        
        # Calculate variance in motion directions
        angles = np.arctan2(motion_vectors[:, 1], motion_vectors[:, 0])
        angle_variance = np.var(angles)
        
        # Convert to smoothness score (0 = chaotic, 1 = smooth)
        smoothness = 1.0 / (1.0 + angle_variance)
        
        return float(smoothness)
    
    async def _classify_content_type(self, visual_analysis: Dict[str, Any], 
                                   audio_analysis: Dict[str, Any]) -> ContentType:
        """Classify content type based on analysis"""
        
        # Analyze visual features
        face_count = len(visual_analysis.get("face_detections", []))
        object_variety = len(set(obj["class"] for obj in visual_analysis.get("object_detections", [])))
        
        # Analyze audio features
        speech_presence = audio_analysis.get("speech_ratio", 0.0)
        music_presence = audio_analysis.get("music_ratio", 0.0)
        
        # Classification logic
        if face_count > 50 and speech_presence > 0.7:
            if object_variety < 5:
                return ContentType.INTERVIEW
            else:
                return ContentType.VLOG
        elif music_presence > 0.6:
            return ContentType.MUSIC_VIDEO
        elif speech_presence > 0.8 and object_variety > 10:
            return ContentType.DOCUMENTARY
        elif face_count < 10 and object_variety > 15:
            if "sport" in str(visual_analysis.get("object_detections", [])).lower():
                return ContentType.SPORTS
            else:
                return ContentType.FILM
        else:
            return ContentType.SOCIAL_MEDIA
    
    async def _analyze_style_and_tone(self, visual_analysis: Dict[str, Any], 
                                    audio_analysis: Dict[str, Any]) -> Tuple[EmotionalTone, Dict[str, Any]]:
        """Analyze overall style and emotional tone"""
        
        # Analyze emotional content
        emotions = visual_analysis.get("emotions", [])
        if emotions:
            dominant_emotions = [e.get("dominant_emotion", {}).get("label", "neutral") for e in emotions]
            emotion_counts = {}
            for emotion in dominant_emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Map to EmotionalTone
            emotion_mapping = {
                "happy": EmotionalTone.HAPPY,
                "joy": EmotionalTone.HAPPY,
                "sad": EmotionalTone.SAD,
                "anger": EmotionalTone.ANGRY,
                "surprise": EmotionalTone.SURPRISED,
                "fear": EmotionalTone.FEARFUL,
                "disgust": EmotionalTone.DISGUSTED,
                "neutral": EmotionalTone.NEUTRAL
            }
            
            most_common_emotion = max(emotion_counts, key=emotion_counts.get)
            overall_tone = emotion_mapping.get(most_common_emotion, EmotionalTone.NEUTRAL)
        else:
            overall_tone = EmotionalTone.NEUTRAL
        
        # Analyze visual style
        color_analysis = visual_analysis.get("color_analysis", [])
        if color_analysis:
            avg_brightness = np.mean([c.get("brightness", 128) for c in color_analysis])
            avg_saturation = np.mean([c.get("saturation", 128) for c in color_analysis])
            color_temperatures = [c.get("temperature", "neutral") for c in color_analysis]
            
            visual_style = {
                "brightness_level": "bright" if avg_brightness > 150 else "dark" if avg_brightness < 100 else "medium",
                "saturation_level": "high" if avg_saturation > 150 else "low" if avg_saturation < 100 else "medium",
                "color_temperature": max(set(color_temperatures), key=color_temperatures.count),
                "style_classification": self._classify_visual_style(avg_brightness, avg_saturation, color_temperatures)
            }
        else:
            visual_style = {
                "brightness_level": "medium",
                "saturation_level": "medium",
                "color_temperature": "neutral",
                "style_classification": "standard"
            }
        
        return overall_tone, visual_style
    
    def _classify_visual_style(self, brightness: float, saturation: float, 
                             temperatures: List[str]) -> str:
        """Classify visual style based on color characteristics"""
        
        if brightness > 180 and saturation > 150:
            return "vibrant_modern"
        elif brightness < 80 and "cool" in temperatures:
            return "cinematic_dark"
        elif brightness > 150 and "warm" in temperatures:
            return "bright_commercial"
        elif saturation < 100:
            return "desaturated_artistic"
        else:
            return "standard"
    
    async def _assess_video_quality(self, visual_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall video quality"""
        
        frame_analysis = visual_analysis.get("frame_analysis", [])
        
        if not frame_analysis:
            return {"overall_score": 0.0}
        
        # Collect quality metrics
        brightness_scores = []
        contrast_scores = []
        composition_scores = []
        motion_smoothness = []
        
        for frame in frame_analysis:
            analysis = frame.get("analysis", {})
            
            # Color quality
            color_data = analysis.get("color", {})
            brightness = color_data.get("brightness", 128)
            contrast = color_data.get("contrast", 50)
            
            # Normalize scores
            brightness_score = 1.0 - abs(brightness - 128) / 128
            contrast_score = min(1.0, contrast / 100)
            
            brightness_scores.append(brightness_score)
            contrast_scores.append(contrast_score)
            
            # Composition quality
            composition = analysis.get("composition", {})
            composition_scores.append(composition.get("composition_score", 0.0))
            
            # Motion quality
            motion = analysis.get("motion", {})
            motion_smoothness.append(motion.get("motion_smoothness", 1.0))
        
        # Calculate overall quality metrics
        quality_metrics = {
            "brightness_quality": float(np.mean(brightness_scores)),
            "contrast_quality": float(np.mean(contrast_scores)),
            "composition_quality": float(np.mean(composition_scores)),
            "motion_quality": float(np.mean(motion_smoothness)),
            "consistency": self._calculate_consistency(frame_analysis),
            "technical_quality": self._assess_technical_quality(visual_analysis)
        }
        
        # Overall score
        quality_metrics["overall_score"] = np.mean([
            quality_metrics["brightness_quality"],
            quality_metrics["contrast_quality"],
            quality_metrics["composition_quality"],
            quality_metrics["motion_quality"],
            quality_metrics["consistency"],
            quality_metrics["technical_quality"]
        ])
        
        return quality_metrics
    
    def _calculate_consistency(self, frame_analysis: List[Dict[str, Any]]) -> float:
        """Calculate visual consistency across frames"""
        
        if len(frame_analysis) < 2:
            return 1.0
        
        # Analyze brightness consistency
        brightness_values = []
        for frame in frame_analysis:
            color_data = frame.get("analysis", {}).get("color", {})
            brightness_values.append(color_data.get("brightness", 128))
        
        brightness_variance = np.var(brightness_values)
        consistency_score = 1.0 / (1.0 + brightness_variance / 1000)
        
        return float(consistency_score)
    
    def _assess_technical_quality(self, visual_analysis: Dict[str, Any]) -> float:
        """Assess technical quality aspects"""
        
        # Placeholder for technical quality assessment
        # In practice, would analyze sharpness, noise, compression artifacts, etc.
        return 0.8
    
    async def _detect_highlights(self, scenes: List[SceneInfo], 
                               audio_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect potential highlights in content"""
        
        highlights = []
        
        for scene in scenes:
            highlight_score = 0.0
            
            # Visual interest factors
            if scene.importance_score > 0.7:
                highlight_score += 0.3
            
            if scene.emotional_tone in [EmotionalTone.EXCITED, EmotionalTone.HAPPY, EmotionalTone.SURPRISED]:
                highlight_score += 0.2
            
            if scene.camera_movement != CameraMovement.STATIC:
                highlight_score += 0.1
            
            # Audio factors
            audio_features = scene.audio_features
            if audio_features.get("volume_peak", False):
                highlight_score += 0.2
            
            if audio_features.get("tempo_change", False):
                highlight_score += 0.1
            
            if audio_features.get("speech_clarity", 0) > 0.8:
                highlight_score += 0.1
            
            # Mark as highlight if score is high enough
            if highlight_score > 0.5:
                highlights.append({
                    "start_time": scene.start_time,
                    "end_time": scene.end_time,
                    "score": highlight_score,
                    "reasons": self._get_highlight_reasons(scene, highlight_score),
                    "scene_info": scene
                })
        
        # Sort by score
        highlights.sort(key=lambda x: x["score"], reverse=True)
        
        return highlights
    
    def _get_highlight_reasons(self, scene: SceneInfo, score: float) -> List[str]:
        """Get reasons why scene is considered a highlight"""
        
        reasons = []
        
        if scene.importance_score > 0.7:
            reasons.append("High visual interest")
        
        if scene.emotional_tone in [EmotionalTone.EXCITED, EmotionalTone.HAPPY]:
            reasons.append("Positive emotional content")
        
        if scene.camera_movement != CameraMovement.STATIC:
            reasons.append("Dynamic camera movement")
        
        if scene.audio_features.get("volume_peak", False):
            reasons.append("Audio peak")
        
        return reasons
    
    async def _generate_recommendations(self, content_type: ContentType, 
                                      scenes: List[SceneInfo], 
                                      audio_analysis: Dict[str, Any],
                                      quality_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate editing recommendations based on analysis"""
        
        recommendations = {
            "editing_style": self._recommend_editing_style(content_type, scenes),
            "pacing": self._recommend_pacing(scenes, audio_analysis),
            "color_grading": self._recommend_color_grading(scenes, quality_metrics),
            "audio_enhancements": self._recommend_audio_enhancements(audio_analysis),
            "transitions": self._recommend_transitions(scenes),
            "text_elements": self._recommend_text_elements(content_type, scenes),
            "music": self._recommend_music(content_type, audio_analysis),
            "effects": self._recommend_effects(scenes),
            "trimming": self._recommend_trimming(scenes)
        }
        
        return recommendations
    
    def _recommend_editing_style(self, content_type: ContentType, 
                               scenes: List[SceneInfo]) -> Dict[str, Any]:
        """Recommend editing style based on content"""
        
        style_map = {
            ContentType.INTERVIEW: "professional_clean",
            ContentType.DOCUMENTARY: "informative_dynamic",
            ContentType.MUSIC_VIDEO: "rhythmic_creative",
            ContentType.VLOG: "casual_engaging",
            ContentType.COMMERCIAL: "polished_impactful",
            ContentType.SOCIAL_MEDIA: "trendy_fast",
            ContentType.FILM: "cinematic_artistic"
        }
        
        base_style = style_map.get(content_type, "standard")
        
        # Adjust based on scene characteristics
        avg_energy = np.mean([scene.importance_score for scene in scenes])
        
        if avg_energy > 0.8:
            modifier = "high_energy"
        elif avg_energy < 0.3:
            modifier = "calm"
        else:
            modifier = "balanced"
        
        return {
            "base_style": base_style,
            "energy_modifier": modifier,
            "recommended_style": f"{base_style}_{modifier}",
            "confidence": 0.8
        }
    
    def _recommend_pacing(self, scenes: List[SceneInfo], 
                        audio_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend pacing based on content analysis"""
        
        avg_scene_duration = np.mean([scene.duration for scene in scenes])
        audio_tempo = audio_analysis.get("average_tempo", 120)
        
        if avg_scene_duration > 5 and audio_tempo < 100:
            pacing = "slow"
        elif avg_scene_duration < 2 or audio_tempo > 140:
            pacing = "fast"
        else:
            pacing = "medium"
        
        return {
            "recommended_pacing": pacing,
            "target_scene_duration": 3.0 if pacing == "fast" else 5.0 if pacing == "slow" else 4.0,
            "cut_frequency": "high" if pacing == "fast" else "low" if pacing == "slow" else "medium"
        }
    
    def _recommend_color_grading(self, scenes: List[SceneInfo], 
                               quality_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend color grading approach"""
        
        brightness_quality = quality_metrics.get("brightness_quality", 0.5)
        contrast_quality = quality_metrics.get("contrast_quality", 0.5)
        
        recommendations = []
        
        if brightness_quality < 0.6:
            recommendations.append({
                "adjustment": "brightness",
                "value": 0.2 if brightness_quality < 0.3 else 0.1,
                "reason": "Low brightness detected"
            })
        
        if contrast_quality < 0.6:
            recommendations.append({
                "adjustment": "contrast",
                "value": 0.3 if contrast_quality < 0.3 else 0.2,
                "reason": "Low contrast detected"
            })
        
        # Style-based recommendations
        dominant_tones = [scene.emotional_tone for scene in scenes]
        if EmotionalTone.CINEMATIC in dominant_tones or EmotionalTone.MYSTERIOUS in dominant_tones:
            recommendations.append({
                "adjustment": "color_grade",
                "style": "cinematic_teal_orange",
                "reason": "Cinematic content detected"
            })
        
        return {"adjustments": recommendations}
    
    def _recommend_audio_enhancements(self, audio_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend audio enhancements"""
        
        recommendations = []
        
        noise_level = audio_analysis.get("noise_level", 0.0)
        if noise_level > 0.3:
            recommendations.append({
                "enhancement": "noise_reduction",
                "intensity": "high" if noise_level > 0.6 else "medium",
                "reason": "Background noise detected"
            })
        
        dynamic_range = audio_analysis.get("dynamic_range", 1.0)
        if dynamic_range < 0.3:
            recommendations.append({
                "enhancement": "dynamic_range_expansion",
                "intensity": "medium",
                "reason": "Limited dynamic range"
            })
        
        speech_clarity = audio_analysis.get("speech_clarity", 1.0)
        if speech_clarity < 0.7:
            recommendations.append({
                "enhancement": "dialogue_enhancement",
                "intensity": "high",
                "reason": "Poor speech clarity"
            })
        
        return recommendations
    
    def _recommend_transitions(self, scenes: List[SceneInfo]) -> Dict[str, Any]:
        """Recommend transitions between scenes"""
        
        # Analyze scene relationships
        transition_recommendations = []
        
        for i in range(len(scenes) - 1):
            current_scene = scenes[i]
            next_scene = scenes[i + 1]
            
            # Determine transition type
            if current_scene.emotional_tone != next_scene.emotional_tone:
                transition_type = "crossfade"
            elif current_scene.scene_type == next_scene.scene_type:
                transition_type = "cut"
            else:
                transition_type = "dissolve"
            
            transition_recommendations.append({
                "from_scene": i,
                "to_scene": i + 1,
                "type": transition_type,
                "duration": 0.5 if transition_type != "cut" else 0.0
            })
        
        return {"transitions": transition_recommendations}
    
    def _recommend_text_elements(self, content_type: ContentType, 
                               scenes: List[SceneInfo]) -> List[Dict[str, Any]]:
        """Recommend text elements"""
        
        recommendations = []
        
        # Face-based lower thirds
        face_scenes = [scene for scene in scenes if len(scene.faces) > 0]
        if face_scenes and content_type in [ContentType.INTERVIEW, ContentType.DOCUMENTARY]:
            recommendations.append({
                "type": "lower_thirds",
                "timing": "auto_detect_faces",
                "style": "professional",
                "reason": "Faces detected in interview/documentary content"
            })
        
        # Title recommendations
        if content_type in [ContentType.VLOG, ContentType.SOCIAL_MEDIA]:
            recommendations.append({
                "type": "title_sequence",
                "timing": "beginning",
                "style": "modern_dynamic",
                "reason": "Social media content benefits from engaging titles"
            })
        
        return recommendations
    
    def _recommend_music(self, content_type: ContentType, 
                       audio_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend music enhancements"""
        
        music_presence = audio_analysis.get("music_ratio", 0.0)
        
        if music_presence < 0.1:
            # Recommend adding background music
            genre_map = {
                ContentType.DOCUMENTARY: "ambient_documentary",
                ContentType.VLOG: "upbeat_indie",
                ContentType.COMMERCIAL: "corporate_uplifting",
                ContentType.SOCIAL_MEDIA: "trendy_electronic"
            }
            
            recommended_genre = genre_map.get(content_type, "general_background")
            
            return {
                "add_music": True,
                "genre": recommended_genre,
                "volume_level": 0.3,
                "sync_to_cuts": True
            }
        else:
            return {
                "add_music": False,
                "enhance_existing": True,
                "equalization": "dialogue_focus"
            }
    
    def _recommend_effects(self, scenes: List[SceneInfo]) -> List[Dict[str, Any]]:
        """Recommend visual effects"""
        
        recommendations = []
        
        # Stabilization for shaky footage
        shaky_scenes = [scene for scene in scenes 
                       if scene.camera_movement == CameraMovement.HANDHELD]
        
        if shaky_scenes:
            recommendations.append({
                "effect": "stabilization",
                "scenes": [scene.start_time for scene in shaky_scenes],
                "intensity": "medium",
                "reason": "Handheld camera movement detected"
            })
        
        # Color correction for poorly lit scenes
        dark_scenes = [scene for scene in scenes 
                      if scene.quality_score < 0.5]
        
        if dark_scenes:
            recommendations.append({
                "effect": "brightness_correction",
                "scenes": [scene.start_time for scene in dark_scenes],
                "intensity": "medium",
                "reason": "Low quality lighting detected"
            })
        
        return recommendations
    
    def _recommend_trimming(self, scenes: List[SceneInfo]) -> Dict[str, Any]:
        """Recommend trimming operations"""
        
        # Find scenes with low importance
        low_importance_scenes = [scene for scene in scenes 
                               if scene.importance_score < 0.3]
        
        # Find very long scenes
        long_scenes = [scene for scene in scenes if scene.duration > 10]
        
        recommendations = {
            "remove_scenes": [
                {
                    "start_time": scene.start_time,
                    "end_time": scene.end_time,
                    "reason": "Low importance score"
                }
                for scene in low_importance_scenes
            ],
            "trim_scenes": [
                {
                    "start_time": scene.start_time,
                    "suggested_duration": 8.0,
                    "reason": "Scene too long"
                }
                for scene in long_scenes
            ]
        }
        
        return recommendations
    
    async def _analyze_transitions(self, scenes: List[SceneInfo]) -> List[Dict[str, Any]]:
        """Analyze transitions between scenes"""
        
        transitions = []
        
        for i in range(len(scenes) - 1):
            current_scene = scenes[i]
            next_scene = scenes[i + 1]
            
            transition = {
                "from_scene": i,
                "to_scene": i + 1,
                "timestamp": current_scene.end_time,
                "type": "cut",  # Default
                "quality": "smooth",
                "visual_similarity": self._calculate_visual_similarity(current_scene, next_scene),
                "audio_continuity": self._calculate_audio_continuity(current_scene, next_scene)
            }
            
            transitions.append(transition)
        
        return transitions
    
    def _calculate_visual_similarity(self, scene1: SceneInfo, scene2: SceneInfo) -> float:
        """Calculate visual similarity between scenes"""
        # Placeholder - would compare visual features
        return 0.5
    
    def _calculate_audio_continuity(self, scene1: SceneInfo, scene2: SceneInfo) -> float:
        """Calculate audio continuity between scenes"""
        # Placeholder - would compare audio features
        return 0.5
    
    def _calculate_energy_level(self, scenes: List[SceneInfo], 
                              audio_analysis: Dict[str, Any]) -> float:
        """Calculate overall energy level"""
        
        visual_energy = np.mean([scene.importance_score for scene in scenes])
        audio_energy = audio_analysis.get("energy_level", 0.5)
        
        return (visual_energy + audio_energy) / 2
    
    def _determine_pacing(self, scenes: List[SceneInfo], 
                        audio_analysis: Dict[str, Any]) -> str:
        """Determine overall pacing"""
        
        avg_scene_duration = np.mean([scene.duration for scene in scenes])
        audio_tempo = audio_analysis.get("average_tempo", 120)
        
        if avg_scene_duration < 3 or audio_tempo > 140:
            return "fast"
        elif avg_scene_duration > 6 and audio_tempo < 100:
            return "slow"
        else:
            return "medium"


# Supporting classes

class VisualFeatureExtractor:
    """Extract visual features from video frames"""
    
    def __init__(self):
        self.feature_cache = {}
    
    async def extract_features(self, frame: np.ndarray) -> Dict[str, Any]:
        """Extract comprehensive visual features"""
        
        features = {
            "color_histogram": self._extract_color_histogram(frame),
            "texture_features": self._extract_texture_features(frame),
            "edge_density": self._calculate_edge_density(frame),
            "spatial_complexity": self._calculate_spatial_complexity(frame)
        }
        
        return features
    
    def _extract_color_histogram(self, frame: np.ndarray) -> np.ndarray:
        """Extract color histogram"""
        hist = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        return cv2.normalize(hist, hist).flatten()
    
    def _extract_texture_features(self, frame: np.ndarray) -> Dict[str, float]:
        """Extract texture features using LBP"""
        from skimage.feature import local_binary_pattern
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        lbp = local_binary_pattern(gray, 8, 1, method='uniform')
        
        hist, _ = np.histogram(lbp.ravel(), bins=10, range=(0, 10))
        hist = hist.astype(float)
        hist /= (hist.sum() + 1e-7)
        
        return {
            "lbp_uniformity": np.sum(hist[:9]) / np.sum(hist),
            "texture_energy": np.sum(hist**2),
            "texture_entropy": -np.sum(hist * np.log2(hist + 1e-7))
        }
    
    def _calculate_edge_density(self, frame: np.ndarray) -> float:
        """Calculate edge density"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return np.sum(edges > 0) / edges.size
    
    def _calculate_spatial_complexity(self, frame: np.ndarray) -> float:
        """Calculate spatial complexity"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate gradient magnitude
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        return np.std(magnitude) / np.mean(magnitude + 1e-7)


class AudioFeatureExtractor:
    """Extract audio features and analyze audio content"""
    
    def __init__(self):
        self.sample_rate = 22050
        self.hop_length = 512
    
    async def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        """Comprehensive audio analysis"""
        
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Basic features
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Spectral features
            spectral_features = self._extract_spectral_features(y, sr)
            
            # Rhythm features
            rhythm_features = self._extract_rhythm_features(y, sr)
            
            # Harmonic features
            harmonic_features = self._extract_harmonic_features(y, sr)
            
            # Speech/music classification
            content_classification = self._classify_audio_content(y, sr)
            
            # Quality assessment
            quality_metrics = self._assess_audio_quality(y, sr)
            
            # Emotional features
            emotional_features = self._extract_emotional_features(y, sr)
            
            analysis = {
                "duration": duration,
                "sample_rate": sr,
                "spectral_features": spectral_features,
                "rhythm_features": rhythm_features,
                "harmonic_features": harmonic_features,
                "content_classification": content_classification,
                "quality_metrics": quality_metrics,
                "emotional_features": emotional_features,
                "speech_ratio": content_classification.get("speech_probability", 0.0),
                "music_ratio": content_classification.get("music_probability", 0.0),
                "noise_level": quality_metrics.get("noise_level", 0.0),
                "energy_level": spectral_features.get("rms_energy", 0.0),
                "average_tempo": rhythm_features.get("tempo", 120)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Audio analysis failed: {e}")
            return {}
    
    def _extract_spectral_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Extract spectral features"""
        
        # Spectral centroid
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        
        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)
        
        # RMS energy
        rms = librosa.feature.rms(y=y)
        
        # MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Spectral contrast
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        
        return {
            "spectral_centroid_mean": float(np.mean(spectral_centroid)),
            "spectral_centroid_std": float(np.std(spectral_centroid)),
            "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
            "zcr_mean": float(np.mean(zcr)),
            "rms_energy": float(np.mean(rms)),
            "mfcc_means": np.mean(mfccs, axis=1).tolist(),
            "spectral_contrast_mean": np.mean(spectral_contrast, axis=1).tolist()
        }
    
    def _extract_rhythm_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Extract rhythm and tempo features"""
        
        # Tempo and beats
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        
        # Onset detection
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr)
        
        # Rhythm patterns
        tempogram = librosa.feature.tempogram(y=y, sr=sr)
        
        return {
            "tempo": float(tempo),
            "beat_count": len(beats),
            "onset_count": len(onset_times),
            "rhythm_strength": float(np.mean(tempogram)),
            "tempo_consistency": self._calculate_tempo_consistency(beats, sr)
        }
    
    def _calculate_tempo_consistency(self, beats: np.ndarray, sr: int) -> float:
        """Calculate tempo consistency"""
        if len(beats) < 2:
            return 0.0
        
        beat_intervals = np.diff(beats) / sr
        return 1.0 / (1.0 + np.std(beat_intervals))
    
    def _extract_harmonic_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Extract harmonic features"""
        
        # Harmonic-percussive separation
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=y_harmonic, sr=sr)
        
        # Tonnetz (tonal centroid features)
        tonnetz = librosa.feature.tonnetz(y=y_harmonic, sr=sr)
        
        return {
            "harmonic_ratio": float(np.sum(y_harmonic**2) / (np.sum(y**2) + 1e-7)),
            "percussive_ratio": float(np.sum(y_percussive**2) / (np.sum(y**2) + 1e-7)),
            "chroma_mean": np.mean(chroma, axis=1).tolist(),
            "tonnetz_mean": np.mean(tonnetz, axis=1).tolist()
        }
    
    def _classify_audio_content(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Classify audio content (speech vs music vs noise)"""
        
        # Extract features for classification
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Simple heuristic-based classification
        # In practice, would use trained machine learning model
        
        # Speech indicators
        speech_score = 0.0
        if 80 < spectral_centroid < 300:  # Typical speech range
            speech_score += 0.3
        if 0.01 < zcr < 0.1:  # Speech ZCR range
            speech_score += 0.3
        if np.std(mfccs[1:3]) > 10:  # Formant variation
            speech_score += 0.4
        
        # Music indicators
        music_score = 0.0
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        harmonic_ratio = np.sum(y_harmonic**2) / (np.sum(y**2) + 1e-7)
        if harmonic_ratio > 0.3:  # Strong harmonic content
            music_score += 0.5
        
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        if 60 < tempo < 200:  # Musical tempo range
            music_score += 0.3
        
        chroma = librosa.feature.chroma_stft(y=y_harmonic, sr=sr)
        if np.std(chroma) > 0.1:  # Tonal variation
            music_score += 0.2
        
        # Noise score (remainder)
        noise_score = max(0.0, 1.0 - speech_score - music_score)
        
        # Normalize scores
        total = speech_score + music_score + noise_score
        if total > 0:
            speech_score /= total
            music_score /= total
            noise_score /= total
        
        return {
            "speech_probability": speech_score,
            "music_probability": music_score,
            "noise_probability": noise_score
        }
    
    def _assess_audio_quality(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Assess audio quality metrics"""
        
        # Signal-to-noise ratio estimation
        # Split signal into frames and estimate noise floor
        frame_length = sr  # 1 second frames
        frames = librosa.util.frame(y, frame_length=frame_length, hop_length=frame_length//2)
        
        frame_energies = np.array([np.sum(frame**2) for frame in frames.T])
        
        # Estimate noise floor as lowest 10% of frames
        noise_floor = np.percentile(frame_energies, 10)
        signal_energy = np.percentile(frame_energies, 90)
        
        snr = 10 * np.log10((signal_energy + 1e-7) / (noise_floor + 1e-7))
        
        # Dynamic range
        rms = librosa.feature.rms(y=y)
        dynamic_range = np.max(rms) / (np.min(rms) + 1e-7)
        
        # Clipping detection
        clipping_ratio = np.sum(np.abs(y) > 0.99) / len(y)
        
        # Frequency response assessment
        stft = librosa.stft(y)
        magnitude = np.abs(stft)
        freq_response = np.mean(magnitude, axis=1)
        freq_balance = np.std(freq_response) / np.mean(freq_response)
        
        return {
            "snr": float(snr),
            "dynamic_range": float(dynamic_range),
            "clipping_ratio": float(clipping_ratio),
            "frequency_balance": float(freq_balance),
            "noise_level": float(noise_floor),
            "overall_quality": self._calculate_overall_audio_quality(snr, dynamic_range, clipping_ratio)
        }
    
    def _calculate_overall_audio_quality(self, snr: float, dynamic_range: float, 
                                       clipping_ratio: float) -> float:
        """Calculate overall audio quality score"""
        
        # Normalize individual metrics
        snr_score = min(1.0, max(0.0, (snr - 10) / 40))  # 10-50 dB range
        dr_score = min(1.0, max(0.0, (dynamic_range - 1) / 19))  # 1-20 range
        clip_score = max(0.0, 1.0 - clipping_ratio * 10)  # Penalize clipping
        
        # Weighted average
        quality_score = (snr_score * 0.4 + dr_score * 0.3 + clip_score * 0.3)
        
        return float(quality_score)
    
    def _extract_emotional_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract emotional features from audio"""
        
        # Tempo-based emotion
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Spectral features for emotion
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        
        # Energy-based features
        rms = librosa.feature.rms(y=y)
        energy_variance = np.var(rms)
        
        # Simple emotion mapping
        # In practice, would use trained emotion recognition model
        
        valence = 0.5  # Positive/negative
        arousal = 0.5  # Calm/excited
        
        # Tempo influence on arousal
        if tempo > 120:
            arousal += (tempo - 120) / 200
        else:
            arousal -= (120 - tempo) / 200
        
        # Spectral brightness influence on valence
        if spectral_centroid > 2000:
            valence += 0.2
        elif spectral_centroid < 1000:
            valence -= 0.2
        
        # Energy variance influence on arousal
        if energy_variance > 0.01:
            arousal += 0.3
        
        # Clamp values
        valence = max(0.0, min(1.0, valence))
        arousal = max(0.0, min(1.0, arousal))
        
        return {
            "valence": valence,  # Positive/negative emotion
            "arousal": arousal,  # Energy/excitement level
            "tempo_emotion": "energetic" if tempo > 120 else "calm",
            "brightness": "bright" if spectral_centroid > 2000 else "dark"
        }


class SceneDetector:
    """Detect scenes and shots in video"""
    
    def __init__(self):
        self.threshold = 0.3
        self.min_scene_length = 1.0  # seconds
    
    async def detect_scenes(self, video_path: str) -> List[SceneInfo]:
        """Detect scenes using multiple algorithms"""
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Detect cuts using multiple methods
        histogram_cuts = await self._detect_histogram_cuts(cap)
        edge_cuts = await self._detect_edge_cuts(cap)
        optical_flow_cuts = await self._detect_optical_flow_cuts(cap)
        
        # Combine cut detection results
        all_cuts = sorted(set(histogram_cuts + edge_cuts + optical_flow_cuts))
        
        # Filter cuts that are too close together
        filtered_cuts = self._filter_close_cuts(all_cuts, fps)
        
        # Create scene information
        scenes = []
        for i in range(len(filtered_cuts) + 1):
            start_frame = filtered_cuts[i-1] if i > 0 else 0
            end_frame = filtered_cuts[i] if i < len(filtered_cuts) else total_frames - 1
            
            scene = SceneInfo(
                start_frame=start_frame,
                end_frame=end_frame,
                start_time=start_frame / fps,
                end_time=end_frame / fps,
                duration=(end_frame - start_frame) / fps,
                scene_type=SceneType.MEDIUM_SHOT,  # Will be updated later
                camera_movement=CameraMovement.STATIC,  # Will be updated later
                emotional_tone=EmotionalTone.NEUTRAL  # Will be updated later
            )
            
            scenes.append(scene)
        
        cap.release()
        
        return scenes
    
    async def _detect_histogram_cuts(self, cap: cv2.VideoCapture) -> List[int]:
        """Detect cuts using histogram differences"""
        
        cuts = []
        prev_hist = None
        frame_idx = 0
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Calculate histogram
            hist = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            
            if prev_hist is not None:
                # Calculate histogram difference
                diff = cv2.compareHist(hist, prev_hist, cv2.HISTCMP_CORREL)
                
                if diff < (1.0 - self.threshold):
                    cuts.append(frame_idx)
            
            prev_hist = hist
            frame_idx += 1
        
        return cuts
    
    async def _detect_edge_cuts(self, cap: cv2.VideoCapture) -> List[int]:
        """Detect cuts using edge differences"""
        
        cuts = []
        prev_edges = None
        frame_idx = 0
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Calculate edges
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            if prev_edges is not None:
                # Calculate edge difference
                diff = np.sum(np.abs(edges.astype(np.float32) - prev_edges.astype(np.float32)))
                diff /= (edges.shape[0] * edges.shape[1] * 255)  # Normalize
                
                if diff > self.threshold:
                    cuts.append(frame_idx)
            
            prev_edges = edges
            frame_idx += 1
        
        return cuts
    
    async def _detect_optical_flow_cuts(self, cap: cv2.VideoCapture) -> List[int]:
        """Detect cuts using optical flow discontinuities"""
        
        cuts = []
        prev_gray = None
        frame_idx = 0
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_gray is not None:
                # Calculate optical flow
                flow = cv2.calcOpticalFlowPyrLK(prev_gray, gray, None, None)
                
                if flow[0] is not None and len(flow[0]) > 0:
                    # Calculate flow magnitude
                    flow_magnitude = np.linalg.norm(flow[0] - flow[1] if flow[1] is not None else flow[0], axis=1)
                    avg_flow = np.mean(flow_magnitude)
                    
                    # Detect sudden flow changes (potential cuts)
                    if avg_flow > 50:  # Threshold for flow discontinuity
                        cuts.append(frame_idx)
            
            prev_gray = gray
            frame_idx += 1
        
        return cuts
    
    def _filter_close_cuts(self, cuts: List[int], fps: float) -> List[int]:
        """Filter out cuts that are too close together"""
        
        if not cuts:
            return cuts
        
        min_frames = int(self.min_scene_length * fps)
        filtered_cuts = [cuts[0]]
        
        for cut in cuts[1:]:
            if cut - filtered_cuts[-1] >= min_frames:
                filtered_cuts.append(cut)
        
        return filtered_cuts


class ObjectTracker:
    """Track objects across video frames"""
    
    def __init__(self):
        self.trackers = {}
        self.next_id = 0
    
    async def track_objects(self, video_path: str, object_detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Track objects across frames"""
        
        # Group detections by frame
        frame_detections = {}
        for detection in object_detections:
            frame = detection.get("frame", 0)
            if frame not in frame_detections:
                frame_detections[frame] = []
            frame_detections[frame].append(detection)
        
        # Track objects across frames
        object_tracks = {}
        
        for frame_idx in sorted(frame_detections.keys()):
            detections = frame_detections[frame_idx]
            
            # Update existing tracks
            for track_id, track_data in self.trackers.items():
                # Try to match detection to existing track
                best_match = self._find_best_match(track_data["last_detection"], detections)
                
                if best_match:
                    # Update track
                    track_data["detections"].append(best_match)
                    track_data["last_detection"] = best_match
                    detections.remove(best_match)
                else:
                    # Track lost
                    track_data["active"] = False
            
            # Create new tracks for unmatched detections
            for detection in detections:
                track_id = self.next_id
                self.next_id += 1
                
                self.trackers[track_id] = {
                    "id": track_id,
                    "class": detection["class"],
                    "detections": [detection],
                    "last_detection": detection,
                    "active": True
                }
        
        # Convert to output format
        for track_id, track_data in self.trackers.items():
            object_tracks[track_id] = {
                "track_id": track_id,
                "object_class": track_data["class"],
                "detections": track_data["detections"],
                "duration": len(track_data["detections"]),
                "confidence": np.mean([d["confidence"] for d in track_data["detections"]])
            }
        
        return object_tracks
    
    def _find_best_match(self, last_detection: Dict[str, Any], 
                        current_detections: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find best matching detection for tracking"""
        
        if not current_detections:
            return None
        
        last_bbox = last_detection["bbox"]
        last_class = last_detection["class"]
        
        best_match = None
        best_score = 0.0
        
        for detection in current_detections:
            if detection["class"] != last_class:
                continue
            
            # Calculate IoU
            iou = self._calculate_iou(last_bbox, detection["bbox"])
            
            # Combined score (IoU + confidence)
            score = iou * 0.7 + detection["confidence"] * 0.3
            
            if score > best_score and score > 0.3:  # Minimum threshold
                best_score = score
                best_match = detection
        
        return best_match
    
    def _calculate_iou(self, bbox1: List[float], bbox2: List[float]) -> float:
        """Calculate Intersection over Union of two bounding boxes"""
        
        x1 = max(bbox1[0], bbox2[0])
        y1 = max(bbox1[1], bbox2[1])
        x2 = min(bbox1[2], bbox2[2])
        y2 = min(bbox1[3], bbox2[3])
        
        if x2 <= x1 or y2 <= y1:
            return 0.0
        
        intersection = (x2 - x1) * (y2 - y1)
        area1 = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
        area2 = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0


# Example usage
async def main():
    """Example usage of the Advanced AI Analysis Engine"""
    
    # Initialize analysis engine
    analysis_engine = AdvancedAIAnalysisEngine()
    
    # Perform comprehensive analysis
    analysis = await analysis_engine.analyze_video_comprehensive(
        "sample_video.mp4",
        config={
            "scene_detection": True,
            "object_detection": True,
            "face_analysis": True,
            "emotion_analysis": True,
            "audio_analysis": True,
            "quality_assessment": True,
            "highlight_detection": True,
            "style_analysis": True
        }
    )
    
    # Print results
    print(f"Content Type: {analysis.content_type}")
    print(f"Overall Tone: {analysis.overall_tone}")
    print(f"Detected {len(analysis.scenes)} scenes")
    print(f"Found {len(analysis.highlights)} highlights")
    print(f"Overall Quality: {analysis.quality_metrics.get('overall_score', 0):.2f}")
    
    # Print recommendations
    print("\nRecommendations:")
    for category, recommendations in analysis.recommendations.items():
        print(f"  {category}: {recommendations}")


if __name__ == "__main__":
    asyncio.run(main())