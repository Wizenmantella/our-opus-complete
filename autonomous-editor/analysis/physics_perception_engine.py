# analysis/physics_perception_engine.py
"""
Physics & Perception Engine - Advanced visual understanding system for autonomous video editing.
This engine understands object motion, spatial relationships, and visual physics in video content.
"""

import cv2
import numpy as np
import torch
from typing import Dict, List, Any, Optional, Tuple
from project import VideoProject
import json

class PhysicsPerceptionEngine:
    """
    The Physics & Perception Engine provides deep visual understanding through:
    - Object detection and tracking
    - Motion analysis and trajectory prediction
    - Spatial relationship understanding
    - Visual physics simulation
    - Scene composition analysis
    
    This enables the autonomous editor to make intelligent decisions about:
    - Where to place text overlays without obscuring important content
    - When to apply motion-based effects
    - How to predict optimal cut points based on object movement
    - Understanding scene depth and composition
    """
    
    def __init__(self):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.tracking_objects = {}
        self.scene_analysis = {
            'dominant_objects': [],
            'motion_vectors': [],
            'composition_zones': {},
            'depth_map': None,
            'attention_regions': []
        }
        
        # Initialize computer vision models
        self.feature_detector = cv2.SIFT_create()
        self.optical_flow_params = dict(
            winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )
        
        print(f"→ [Physics Engine] Initialized with {self.device.upper()} acceleration")
        print("→ [Physics Engine] Ready for advanced visual perception")
    
    def detect_objects_and_motion(self, project: VideoProject) -> Dict[str, Any]:
        """
        Detects objects and analyzes their motion patterns throughout the video.
        """
        print("→ [Physics Engine] Analyzing object motion and trajectories...")
        
        cap = cv2.VideoCapture(project.video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Initialize tracking variables
        tracked_objects = {}
        motion_analysis = {
            'object_trajectories': {},
            'motion_intensity': [],
            'direction_changes': [],
            'acceleration_patterns': []
        }
        
        # Object detection using background subtraction
        backSub = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
        
        prev_frame = None
        frame_index = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Apply background subtraction
            fg_mask = backSub.apply(frame)
            
            # Find contours for moving objects
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter and track significant objects
            significant_objects = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum object size
                    x, y, w, h = cv2.boundingRect(contour)
                    center = (x + w//2, y + h//2)
                    
                    significant_objects.append({
                        'center': center,
                        'bbox': (x, y, w, h),
                        'area': area,
                        'frame': frame_index
                    })
            
            # Track object motion if we have previous frame
            if prev_frame is not None and significant_objects:
                # Calculate optical flow for motion vectors
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                
                # Calculate motion intensity
                flow = cv2.calcOpticalFlowPyrLK(
                    prev_gray, gray,
                    np.array([obj['center'] for obj in significant_objects], dtype=np.float32),
                    None,
                    **self.optical_flow_params
                )
                
                if flow[0] is not None:
                    motion_vectors = []
                    for i, (old_pt, new_pt) in enumerate(zip(
                        [obj['center'] for obj in significant_objects], 
                        flow[0]
                    )):
                        if new_pt is not None:
                            motion_vector = (new_pt[0] - old_pt[0], new_pt[1] - old_pt[1])
                            motion_magnitude = np.linalg.norm(motion_vector)
                            motion_vectors.append({
                                'object_id': i,
                                'vector': motion_vector,
                                'magnitude': motion_magnitude,
                                'frame': frame_index
                            })
                    
                    motion_analysis['motion_intensity'].append(np.mean([mv['magnitude'] for mv in motion_vectors]))
                    motion_analysis['direction_changes'].extend(motion_vectors)
            
            prev_frame = frame.copy()
            frame_index += 1
            
            # Sample every 10 frames for performance
            if frame_index % 10 != 0:
                continue
                
            if frame_index > 300:  # Limit analysis to first 300 frames
                break
        
        cap.release()
        
        # Analyze motion patterns
        avg_motion_intensity = np.mean(motion_analysis['motion_intensity']) if motion_analysis['motion_intensity'] else 0
        motion_stability = 1.0 - (np.std(motion_analysis['motion_intensity']) / (avg_motion_intensity + 1e-8))
        
        return {
            'motion_analysis': motion_analysis,
            'avg_motion_intensity': avg_motion_intensity,
            'motion_stability': motion_stability,
            'dominant_motion_direction': self._calculate_dominant_direction(motion_analysis['direction_changes']),
            'frame_count_analyzed': frame_index
        }
    
    def analyze_visual_composition(self, project: VideoProject) -> Dict[str, Any]:
        """
        Analyzes visual composition using rule of thirds, leading lines, and visual weight.
        """
        print("→ [Physics Engine] Analyzing visual composition and safe zones...")
        
        cap = cv2.VideoCapture(project.video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        composition_analysis = {
            'safe_zones': [],
            'attention_regions': [],
            'visual_weight_distribution': [],
            'composition_balance': []
        }
        
        # Sample frames for composition analysis
        sample_frames = min(50, frame_count)
        frame_interval = max(1, frame_count // sample_frames)
        
        for i in range(0, frame_count, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break
            
            h, w = frame.shape[:2]
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply rule of thirds grid
            third_h, third_w = h // 3, w // 3
            
            # Calculate visual weight in each region
            regions = {
                'top_left': gray[0:third_h, 0:third_w],
                'top_center': gray[0:third_h, third_w:2*third_w],
                'top_right': gray[0:third_h, 2*third_w:w],
                'middle_left': gray[third_h:2*third_h, 0:third_w],
                'middle_center': gray[third_h:2*third_h, third_w:2*third_w],
                'middle_right': gray[third_h:2*third_h, 2*third_w:w],
                'bottom_left': gray[2*third_h:h, 0:third_w],
                'bottom_center': gray[2*third_h:h, third_w:2*third_w],
                'bottom_right': gray[2*third_h:h, 2*third_w:w]
            }
            
            # Calculate visual weight (variance indicates detail/interest)
            visual_weights = {}
            for region_name, region in regions.items():
                weight = np.var(region) + np.mean(region)
                visual_weights[region_name] = weight
            
            # Find safe zones (low visual weight areas good for text overlays)
            safe_zones = []
            for region_name, weight in visual_weights.items():
                if weight < np.mean(list(visual_weights.values())) * 0.7:
                    safe_zones.append(region_name)
            
            # Edge detection for leading lines
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
            
            # Calculate leading line strength
            leading_line_strength = len(lines) if lines is not None else 0
            
            composition_analysis['safe_zones'].append(safe_zones)
            composition_analysis['visual_weight_distribution'].append(visual_weights)
            composition_analysis['attention_regions'].append(self._find_attention_regions(gray))
            composition_analysis['composition_balance'].append(self._calculate_composition_balance(visual_weights))
        
        cap.release()
        
        # Aggregate results
        most_common_safe_zones = self._find_most_common_safe_zones(composition_analysis['safe_zones'])
        avg_composition_balance = np.mean(composition_analysis['composition_balance'])
        
        return {
            'composition_analysis': composition_analysis,
            'recommended_safe_zones': most_common_safe_zones,
            'avg_composition_balance': avg_composition_balance,
            'visual_stability': self._calculate_visual_stability(composition_analysis['visual_weight_distribution'])
        }
    
    def predict_optimal_cut_points(self, project: VideoProject) -> List[float]:
        """
        Predicts optimal cut points based on visual physics and motion analysis.
        """
        print("→ [Physics Engine] Predicting optimal cut points...")
        
        # Get motion analysis
        motion_data = self.detect_objects_and_motion(project)
        
        # Get scene transitions from existing analysis
        scene_changes = project.scene_timestamps if project.scene_timestamps else []
        
        # Analyze motion patterns for natural cut points
        motion_intensity = motion_data['motion_analysis']['motion_intensity']
        optimal_cuts = []
        
        if motion_intensity:
            # Find local minima in motion (good for cuts)
            for i in range(1, len(motion_intensity) - 1):
                if (motion_intensity[i] < motion_intensity[i-1] and 
                    motion_intensity[i] < motion_intensity[i+1] and 
                    motion_intensity[i] < np.mean(motion_intensity) * 0.5):
                    
                    # Convert frame index to timestamp
                    timestamp = (i * 10) / 30.0  # Assuming 30fps and 10-frame intervals
                    optimal_cuts.append(timestamp)
        
        # Combine with scene changes
        all_cuts = sorted(set(scene_changes + optimal_cuts))
        
        # Filter cuts that are too close together (minimum 2 seconds apart)
        filtered_cuts = []
        for cut in all_cuts:
            if not filtered_cuts or cut - filtered_cuts[-1] >= 2.0:
                filtered_cuts.append(cut)
        
        return filtered_cuts
    
    def analyze_depth_and_layers(self, project: VideoProject) -> Dict[str, Any]:
        """
        Analyzes visual depth and layering for sophisticated effect placement.
        """
        print("→ [Physics Engine] Analyzing depth and visual layers...")
        
        cap = cv2.VideoCapture(project.video_path)
        
        # Sample middle frame for depth analysis
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return {'depth_layers': [], 'foreground_mask': None}
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter for edge-preserving smoothing
        smooth = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Calculate depth cues using gradient magnitude
        grad_x = cv2.Sobel(smooth, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(smooth, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize gradient magnitude to create depth approximation
        depth_approximation = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Segment into depth layers using k-means
        Z = depth_approximation.reshape((-1, 1))
        Z = np.float32(Z)
        
        # K-means clustering for depth layers
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(Z, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Convert back to image shape
        depth_labels = labels.reshape(depth_approximation.shape)
        
        # Create depth layers
        depth_layers = []
        for i in range(3):
            layer_mask = (depth_labels == i).astype(np.uint8) * 255
            layer_area = np.sum(layer_mask > 0)
            depth_layers.append({
                'layer_id': i,
                'mask': layer_mask,
                'area': layer_area,
                'depth_level': float(centers[i][0])
            })
        
        # Sort layers by depth
        depth_layers.sort(key=lambda x: x['depth_level'], reverse=True)
        
        return {
            'depth_layers': depth_layers,
            'depth_approximation': depth_approximation,
            'foreground_mask': depth_layers[0]['mask'] if depth_layers else None
        }
    
    def _calculate_dominant_direction(self, motion_vectors: List[Dict]) -> Tuple[float, float]:
        """Calculate the dominant motion direction."""
        if not motion_vectors:
            return (0.0, 0.0)
        
        total_x = sum(mv['vector'][0] for mv in motion_vectors)
        total_y = sum(mv['vector'][1] for mv in motion_vectors)
        count = len(motion_vectors)
        
        return (total_x / count, total_y / count)
    
    def _find_attention_regions(self, gray_frame: np.ndarray) -> List[Dict]:
        """Find regions that naturally draw attention."""
        # Apply corner detection
        corners = cv2.goodFeaturesToTrack(gray_frame, maxCorners=100, qualityLevel=0.01, minDistance=10)
        
        attention_regions = []
        if corners is not None:
            for corner in corners:
                x, y = corner.ravel()
                attention_regions.append({
                    'center': (int(x), int(y)),
                    'type': 'corner',
                    'strength': float(gray_frame[int(y), int(x)])
                })
        
        return attention_regions
    
    def _calculate_composition_balance(self, visual_weights: Dict[str, float]) -> float:
        """Calculate overall composition balance."""
        # Compare left vs right visual weight
        left_weight = (visual_weights.get('top_left', 0) + 
                      visual_weights.get('middle_left', 0) + 
                      visual_weights.get('bottom_left', 0))
        
        right_weight = (visual_weights.get('top_right', 0) + 
                       visual_weights.get('middle_right', 0) + 
                       visual_weights.get('bottom_right', 0))
        
        # Calculate balance (closer to 1.0 = more balanced)
        total_weight = left_weight + right_weight
        if total_weight > 0:
            balance = 1.0 - abs(left_weight - right_weight) / total_weight
        else:
            balance = 1.0
        
        return balance
    
    def _find_most_common_safe_zones(self, safe_zones_list: List[List[str]]) -> List[str]:
        """Find the most commonly occurring safe zones."""
        zone_counts = {}
        for frame_zones in safe_zones_list:
            for zone in frame_zones:
                zone_counts[zone] = zone_counts.get(zone, 0) + 1
        
        # Return zones that appear in at least 30% of frames
        threshold = len(safe_zones_list) * 0.3
        return [zone for zone, count in zone_counts.items() if count >= threshold]
    
    def _calculate_visual_stability(self, weight_distributions: List[Dict]) -> float:
        """Calculate visual stability across frames."""
        if len(weight_distributions) < 2:
            return 1.0
        
        # Calculate variance in visual weight distribution
        region_variances = {}
        for region in weight_distributions[0].keys():
            weights = [frame[region] for frame in weight_distributions]
            region_variances[region] = np.var(weights)
        
        # Lower variance = higher stability
        avg_variance = np.mean(list(region_variances.values()))
        stability = 1.0 / (1.0 + avg_variance / 1000.0)  # Normalize
        
        return min(stability, 1.0)
    
    def comprehensive_visual_analysis(self, project: VideoProject) -> Dict[str, Any]:
        """
        Performs comprehensive visual analysis combining all physics perception capabilities.
        """
        print("→ [Physics Engine] Beginning comprehensive visual analysis...")
        
        # Analyze motion and objects
        motion_analysis = self.detect_objects_and_motion(project)
        
        # Analyze composition
        composition_analysis = self.analyze_visual_composition(project)
        
        # Predict optimal cuts
        optimal_cuts = self.predict_optimal_cut_points(project)
        
        # Analyze depth
        depth_analysis = self.analyze_depth_and_layers(project)
        
        # Compile comprehensive analysis
        analysis_result = {
            'motion_analysis': motion_analysis,
            'composition_analysis': composition_analysis,
            'optimal_cut_points': optimal_cuts,
            'depth_analysis': depth_analysis,
            'visual_intelligence': {
                'motion_stability': motion_analysis['motion_stability'],
                'composition_balance': composition_analysis['avg_composition_balance'],
                'visual_stability': composition_analysis['visual_stability'],
                'recommended_overlay_zones': composition_analysis['recommended_safe_zones']
            }
        }
        
        print(f"→ [Physics Engine] Analysis complete - {len(optimal_cuts)} optimal cuts identified")
        print(f"→ [Physics Engine] Motion stability: {motion_analysis['motion_stability']:.3f}")
        print(f"→ [Physics Engine] Composition balance: {composition_analysis['avg_composition_balance']:.3f}")
        
        return analysis_result