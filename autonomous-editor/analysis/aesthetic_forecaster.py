# analysis/aesthetic_forecaster.py
"""
Aesthetic Forecaster - Advanced trend prediction and style analysis for viral content creation.
This system predicts aesthetic trends and applies them to achieve maximum engagement.
"""

import numpy as np
import cv2
import torch
from typing import Dict, List, Any, Optional, Tuple
from project import VideoProject
import json
import colorsys
from datetime import datetime
import math

class AestheticForecaster:
    """
    The Aesthetic Forecaster analyzes visual trends and predicts optimal aesthetic choices
    for maximum viral potential and engagement.
    
    Core Capabilities:
    - Color trend analysis and prediction
    - Typography style forecasting
    - Visual effect trend tracking
    - Engagement pattern analysis
    - Viral aesthetic scoring
    - Platform-specific optimization
    """
    
    def __init__(self):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        # Viral aesthetic database (simulated trend data)
        self.viral_trends = {
            'color_palettes': {
                'high_contrast': {'score': 0.95, 'platforms': ['tiktok', 'instagram'], 'longevity': 0.8},
                'pastel_gradient': {'score': 0.88, 'platforms': ['instagram', 'youtube'], 'longevity': 0.6},
                'neon_cyberpunk': {'score': 0.92, 'platforms': ['tiktok', 'youtube'], 'longevity': 0.4},
                'earth_tones': {'score': 0.75, 'platforms': ['youtube', 'linkedin'], 'longevity': 0.9},
                'monochrome_pop': {'score': 0.85, 'platforms': ['instagram', 'tiktok'], 'longevity': 0.7}
            },
            'visual_effects': {
                'glitch_distortion': {'score': 0.93, 'trend_velocity': 0.8, 'fatigue_rate': 0.6},
                'parallax_motion': {'score': 0.87, 'trend_velocity': 0.6, 'fatigue_rate': 0.3},
                'chromatic_aberration': {'score': 0.89, 'trend_velocity': 0.7, 'fatigue_rate': 0.4},
                'film_grain': {'score': 0.82, 'trend_velocity': 0.5, 'fatigue_rate': 0.2},
                'lens_flare': {'score': 0.78, 'trend_velocity': 0.4, 'fatigue_rate': 0.5},
                'vhs_aesthetic': {'score': 0.86, 'trend_velocity': 0.6, 'fatigue_rate': 0.7}
            },
            'typography_styles': {
                'bold_sans_serif': {'score': 0.91, 'readability': 0.9, 'viral_factor': 0.85},
                'handwritten_script': {'score': 0.83, 'readability': 0.7, 'viral_factor': 0.75},
                'futuristic_display': {'score': 0.88, 'readability': 0.8, 'viral_factor': 0.9},
                'minimalist_clean': {'score': 0.79, 'readability': 0.95, 'viral_factor': 0.7},
                'glitch_distorted': {'score': 0.85, 'readability': 0.6, 'viral_factor': 0.95}
            }
        }
        
        # Platform-specific aesthetic preferences
        self.platform_preferences = {
            'tiktok': {
                'color_saturation': 0.9,
                'contrast_preference': 0.95,
                'motion_intensity': 0.9,
                'text_boldness': 0.9,
                'effect_intensity': 0.85
            },
            'instagram': {
                'color_saturation': 0.8,
                'contrast_preference': 0.8,
                'motion_intensity': 0.7,
                'text_boldness': 0.8,
                'effect_intensity': 0.7
            },
            'youtube': {
                'color_saturation': 0.7,
                'contrast_preference': 0.75,
                'motion_intensity': 0.6,
                'text_boldness': 0.75,
                'effect_intensity': 0.6
            }
        }
        
        print("→ [Aesthetic Forecaster] Initialized with viral trend database")
        print("→ [Aesthetic Forecaster] Ready for aesthetic trend analysis")
    
    def analyze_color_trends(self, project: VideoProject) -> Dict[str, Any]:
        """
        Analyzes current color palette and recommends viral color schemes.
        """
        print("→ [Aesthetic Forecaster] Analyzing color trends and viral potential...")
        
        cap = cv2.VideoCapture(project.video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Sample frames for color analysis
        color_analysis = {
            'dominant_colors': [],
            'color_distribution': {},
            'saturation_levels': [],
            'brightness_levels': [],
            'contrast_ratios': []
        }
        
        sample_frames = min(30, frame_count)
        frame_interval = max(1, frame_count // sample_frames)
        
        for i in range(0, frame_count, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to different color spaces
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            
            # Extract dominant colors using k-means
            pixels = frame.reshape(-1, 3)
            pixels = np.float32(pixels)
            
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, centers = cv2.kmeans(pixels, 5, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Convert centers to HSV for analysis
            centers_hsv = []
            for center in centers:
                bgr_pixel = np.uint8([[center]])
                hsv_pixel = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)
                centers_hsv.append(hsv_pixel[0][0])
            
            color_analysis['dominant_colors'].append(centers_hsv)
            
            # Calculate color metrics
            saturation = np.mean(hsv[:, :, 1])
            brightness = np.mean(hsv[:, :, 2])
            contrast = np.std(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            
            color_analysis['saturation_levels'].append(saturation)
            color_analysis['brightness_levels'].append(brightness)
            color_analysis['contrast_ratios'].append(contrast)
        
        cap.release()
        
        # Analyze color trends
        avg_saturation = np.mean(color_analysis['saturation_levels'])
        avg_brightness = np.mean(color_analysis['brightness_levels'])
        avg_contrast = np.mean(color_analysis['contrast_ratios'])
        
        # Predict optimal color palette
        optimal_palette = self._predict_optimal_color_palette(avg_saturation, avg_brightness, avg_contrast)
        
        # Score current palette against viral trends
        palette_score = self._score_color_palette(color_analysis)
        
        return {
            'color_analysis': color_analysis,
            'current_palette_score': palette_score,
            'optimal_palette': optimal_palette,
            'color_recommendations': self._generate_color_recommendations(palette_score),
            'trend_alignment': self._assess_color_trend_alignment(color_analysis)
        }
    
    def predict_viral_effects(self, project: VideoProject) -> Dict[str, Any]:
        """
        Predicts which visual effects will maximize viral potential.
        """
        print("→ [Aesthetic Forecaster] Predicting viral effect combinations...")
        
        # Analyze current video characteristics
        video_analysis = self._analyze_video_characteristics(project)
        
        # Predict optimal effects based on content type and current trends
        effect_predictions = []
        
        for effect_name, effect_data in self.viral_trends['visual_effects'].items():
            # Calculate viral potential score
            base_score = effect_data['score']
            trend_bonus = effect_data['trend_velocity'] * 0.1
            fatigue_penalty = effect_data['fatigue_rate'] * 0.05
            
            # Adjust based on video characteristics
            content_match = self._calculate_content_effect_match(video_analysis, effect_name)
            
            final_score = base_score + trend_bonus - fatigue_penalty + content_match
            
            effect_predictions.append({
                'effect': effect_name,
                'viral_score': min(final_score, 1.0),
                'trend_strength': effect_data['trend_velocity'],
                'fatigue_risk': effect_data['fatigue_rate'],
                'content_match': content_match,
                'recommended_intensity': self._calculate_optimal_intensity(effect_name, video_analysis)
            })
        
        # Sort by viral score
        effect_predictions.sort(key=lambda x: x['viral_score'], reverse=True)
        
        # Select top effects that work well together
        compatible_effects = self._select_compatible_effects(effect_predictions[:5])
        
        return {
            'all_predictions': effect_predictions,
            'recommended_effects': compatible_effects,
            'effect_timing': self._predict_effect_timing(project, compatible_effects),
            'viral_potential': self._calculate_overall_viral_potential(compatible_effects)
        }
    
    def forecast_typography_trends(self, project: VideoProject) -> Dict[str, Any]:
        """
        Forecasts optimal typography choices for maximum engagement.
        """
        print("→ [Aesthetic Forecaster] Forecasting typography trends...")
        
        # Analyze transcript for text content
        text_analysis = {
            'word_count': 0,
            'average_word_length': 0,
            'sentiment_intensity': 0,
            'urgency_level': 0,
            'emotional_words': []
        }
        
        if project.transcript:
            all_words = []
            for segment in project.transcript:
                words = segment.get('text', '').split()
                all_words.extend(words)
            
            text_analysis['word_count'] = len(all_words)
            text_analysis['average_word_length'] = np.mean([len(word) for word in all_words]) if all_words else 0
            
            # Simple sentiment analysis
            emotional_words = ['amazing', 'incredible', 'shocking', 'unbelievable', 'wow', 'omg']
            text_analysis['emotional_words'] = [word for word in all_words if word.lower() in emotional_words]
            text_analysis['sentiment_intensity'] = len(text_analysis['emotional_words']) / max(len(all_words), 1)
        
        # Predict optimal typography
        typography_predictions = []
        
        for font_name, font_data in self.viral_trends['typography_styles'].items():
            # Calculate suitability score
            readability_weight = 0.3 if text_analysis['word_count'] > 100 else 0.2
            viral_weight = 0.7 if text_analysis['sentiment_intensity'] > 0.1 else 0.5
            
            suitability_score = (
                font_data['readability'] * readability_weight +
                font_data['viral_factor'] * viral_weight +
                font_data['score'] * 0.3
            )
            
            typography_predictions.append({
                'font_style': font_name,
                'suitability_score': suitability_score,
                'readability': font_data['readability'],
                'viral_factor': font_data['viral_factor'],
                'recommended_size': self._calculate_optimal_font_size(text_analysis),
                'recommended_color': self._predict_optimal_text_color(project)
            })
        
        typography_predictions.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return {
            'text_analysis': text_analysis,
            'typography_predictions': typography_predictions,
            'recommended_typography': typography_predictions[0] if typography_predictions else None,
            'text_placement_zones': self._predict_optimal_text_placement(project)
        }
    
    def generate_platform_optimization(self, project: VideoProject, target_platform: str = 'tiktok') -> Dict[str, Any]:
        """
        Generates platform-specific aesthetic optimizations.
        """
        print(f"→ [Aesthetic Forecaster] Optimizing for {target_platform.upper()} platform...")
        
        if target_platform not in self.platform_preferences:
            target_platform = 'tiktok'  # Default to TikTok
        
        prefs = self.platform_preferences[target_platform]
        
        # Generate platform-specific recommendations
        optimization = {
            'color_adjustments': {
                'saturation_boost': prefs['color_saturation'] - 0.7,  # Baseline 0.7
                'contrast_enhancement': prefs['contrast_preference'] - 0.75,  # Baseline 0.75
                'brightness_adjustment': 0.1 if prefs['color_saturation'] > 0.8 else 0.0
            },
            'motion_settings': {
                'animation_speed': prefs['motion_intensity'],
                'transition_intensity': prefs['motion_intensity'] * 0.8,
                'parallax_strength': prefs['motion_intensity'] * 0.6
            },
            'typography_settings': {
                'font_weight': prefs['text_boldness'],
                'outline_thickness': prefs['text_boldness'] * 2,
                'drop_shadow_intensity': prefs['text_boldness'] * 0.8
            },
            'effect_intensity': {
                'overall_intensity': prefs['effect_intensity'],
                'distortion_strength': prefs['effect_intensity'] * 0.7,
                'filter_opacity': prefs['effect_intensity'] * 0.6
            }
        }
        
        # Platform-specific viral features
        if target_platform == 'tiktok':
            optimization['viral_features'] = {
                'quick_cuts': True,
                'beat_sync': True,
                'trending_sounds': True,
                'hook_optimization': True,
                'vertical_optimization': True
            }
        elif target_platform == 'instagram':
            optimization['viral_features'] = {
                'aesthetic_consistency': True,
                'story_optimization': True,
                'hashtag_optimization': True,
                'engagement_hooks': True,
                'square_format': True
            }
        elif target_platform == 'youtube':
            optimization['viral_features'] = {
                'retention_optimization': True,
                'thumbnail_optimization': True,
                'watch_time_optimization': True,
                'subscribe_prompts': True,
                'end_screen_optimization': True
            }
        
        return {
            'platform': target_platform,
            'optimization_settings': optimization,
            'viral_score_boost': self._calculate_viral_score_boost(optimization),
            'implementation_priority': self._rank_implementation_priority(optimization)
        }
    
    def _predict_optimal_color_palette(self, saturation: float, brightness: float, contrast: float) -> Dict[str, Any]:
        """Predicts optimal color palette based on current video characteristics."""
        # Analyze current color characteristics
        if saturation > 200 and contrast > 60:
            return {
                'name': 'high_contrast',
                'primary_colors': [(255, 0, 100), (0, 255, 200), (255, 255, 0)],
                'viral_score': 0.95,
                'adjustment_needed': 'minimal'
            }
        elif saturation < 150 and brightness > 180:
            return {
                'name': 'pastel_gradient',
                'primary_colors': [(255, 200, 220), (200, 220, 255), (220, 255, 200)],
                'viral_score': 0.88,
                'adjustment_needed': 'moderate'
            }
        else:
            return {
                'name': 'balanced_vibrant',
                'primary_colors': [(255, 100, 150), (100, 200, 255), (200, 255, 100)],
                'viral_score': 0.85,
                'adjustment_needed': 'significant'
            }
    
    def _score_color_palette(self, color_analysis: Dict) -> float:
        """Scores current color palette against viral trends."""
        if not color_analysis['saturation_levels']:
            return 0.5
        
        avg_saturation = np.mean(color_analysis['saturation_levels'])
        avg_contrast = np.mean(color_analysis['contrast_ratios'])
        
        # Viral color characteristics
        saturation_score = min(avg_saturation / 200.0, 1.0)
        contrast_score = min(avg_contrast / 80.0, 1.0)
        
        return (saturation_score * 0.6 + contrast_score * 0.4)
    
    def _generate_color_recommendations(self, palette_score: float) -> List[str]:
        """Generates specific color recommendations."""
        recommendations = []
        
        if palette_score < 0.6:
            recommendations.append("Increase color saturation by 20-30%")
            recommendations.append("Apply contrast enhancement")
            recommendations.append("Add vibrant accent colors")
        elif palette_score < 0.8:
            recommendations.append("Fine-tune color balance")
            recommendations.append("Enhance key color moments")
        else:
            recommendations.append("Maintain current color aesthetic")
            recommendations.append("Consider subtle enhancements")
        
        return recommendations
    
    def _assess_color_trend_alignment(self, color_analysis: Dict) -> Dict[str, float]:
        """Assesses how well current colors align with viral trends."""
        alignment_scores = {}
        
        for trend_name, trend_data in self.viral_trends['color_palettes'].items():
            # Simplified trend alignment calculation
            base_score = trend_data['score']
            alignment_scores[trend_name] = base_score * 0.7  # Placeholder calculation
        
        return alignment_scores
    
    def _analyze_video_characteristics(self, project: VideoProject) -> Dict[str, Any]:
        """Analyzes video characteristics for effect matching."""
        return {
            'motion_intensity': 0.5,  # Placeholder
            'color_complexity': 0.6,  # Placeholder
            'content_type': 'general',  # Placeholder
            'duration': project.clip.duration if project.clip else 0
        }
    
    def _calculate_content_effect_match(self, video_analysis: Dict, effect_name: str) -> float:
        """Calculates how well an effect matches the video content."""
        # Simplified matching logic
        if effect_name == 'glitch_distortion' and video_analysis['motion_intensity'] > 0.7:
            return 0.2
        elif effect_name == 'parallax_motion' and video_analysis['color_complexity'] > 0.6:
            return 0.15
        else:
            return 0.1
    
    def _calculate_optimal_intensity(self, effect_name: str, video_analysis: Dict) -> float:
        """Calculates optimal intensity for an effect."""
        base_intensity = 0.7
        
        if video_analysis['motion_intensity'] > 0.8:
            return base_intensity * 0.8  # Reduce intensity for high-motion content
        elif video_analysis['motion_intensity'] < 0.3:
            return base_intensity * 1.2  # Increase intensity for low-motion content
        
        return base_intensity
    
    def _select_compatible_effects(self, top_effects: List[Dict]) -> List[Dict]:
        """Selects effects that work well together."""
        # Simple compatibility logic
        compatible = []
        
        for effect in top_effects:
            if len(compatible) < 3:  # Limit to 3 effects max
                compatible.append(effect)
        
        return compatible
    
    def _predict_effect_timing(self, project: VideoProject, effects: List[Dict]) -> Dict[str, List[Tuple[float, float]]]:
        """Predicts optimal timing for effects."""
        timing = {}
        
        for effect in effects:
            # Simplified timing logic
            effect_name = effect['effect']
            duration = project.clip.duration if project.clip else 10
            
            if effect_name == 'glitch_distortion':
                timing[effect_name] = [(0.0, 0.5), (duration * 0.7, duration * 0.8)]
            else:
                timing[effect_name] = [(0.0, duration)]
        
        return timing
    
    def _calculate_overall_viral_potential(self, effects: List[Dict]) -> float:
        """Calculates overall viral potential of effect combination."""
        if not effects:
            return 0.5
        
        scores = [effect['viral_score'] for effect in effects]
        return np.mean(scores)
    
    def _calculate_optimal_font_size(self, text_analysis: Dict) -> int:
        """Calculates optimal font size based on text analysis."""
        base_size = 48
        
        if text_analysis['word_count'] > 100:
            return base_size - 8  # Smaller for lots of text
        elif text_analysis['sentiment_intensity'] > 0.2:
            return base_size + 12  # Larger for emotional content
        
        return base_size
    
    def _predict_optimal_text_color(self, project: VideoProject) -> Tuple[int, int, int]:
        """Predicts optimal text color."""
        # Default to high-contrast white with outline
        return (255, 255, 255)
    
    def _predict_optimal_text_placement(self, project: VideoProject) -> List[str]:
        """Predicts optimal text placement zones."""
        return ['top_third', 'bottom_third', 'center_left', 'center_right']
    
    def _calculate_viral_score_boost(self, optimization: Dict) -> float:
        """Calculates expected viral score boost from optimization."""
        base_boost = 0.15
        
        # Add bonuses for high-impact optimizations
        if optimization['color_adjustments']['saturation_boost'] > 0.1:
            base_boost += 0.05
        if optimization['motion_settings']['animation_speed'] > 0.8:
            base_boost += 0.05
        if optimization['effect_intensity']['overall_intensity'] > 0.8:
            base_boost += 0.05
        
        return min(base_boost, 0.3)
    
    def _rank_implementation_priority(self, optimization: Dict) -> List[str]:
        """Ranks implementation priority of optimizations."""
        priorities = []
        
        if optimization['color_adjustments']['saturation_boost'] > 0.1:
            priorities.append('color_saturation')
        if optimization['motion_settings']['animation_speed'] > 0.8:
            priorities.append('motion_effects')
        if optimization['typography_settings']['font_weight'] > 0.8:
            priorities.append('typography')
        if optimization['effect_intensity']['overall_intensity'] > 0.7:
            priorities.append('visual_effects')
        
        return priorities
    
    def comprehensive_aesthetic_forecast(self, project: VideoProject, target_platform: str = 'tiktok') -> Dict[str, Any]:
        """
        Performs comprehensive aesthetic forecasting and optimization.
        """
        print("→ [Aesthetic Forecaster] Generating comprehensive aesthetic forecast...")
        
        # Analyze all aesthetic dimensions
        color_forecast = self.analyze_color_trends(project)
        effect_forecast = self.predict_viral_effects(project)
        typography_forecast = self.forecast_typography_trends(project)
        platform_optimization = self.generate_platform_optimization(project, target_platform)
        
        # Calculate overall aesthetic score
        aesthetic_scores = {
            'color_score': color_forecast['current_palette_score'],
            'effect_score': effect_forecast['viral_potential'],
            'typography_score': typography_forecast['recommended_typography']['suitability_score'] if typography_forecast['recommended_typography'] else 0.5,
            'platform_alignment': platform_optimization['viral_score_boost']
        }
        
        overall_aesthetic_score = np.mean(list(aesthetic_scores.values()))
        
        # Generate master recommendations
        master_recommendations = {
            'immediate_actions': [],
            'medium_term_actions': [],
            'long_term_strategy': []
        }
        
        # Prioritize recommendations
        if aesthetic_scores['color_score'] < 0.7:
            master_recommendations['immediate_actions'].extend(color_forecast['color_recommendations'])
        
        if aesthetic_scores['effect_score'] < 0.8:
            master_recommendations['immediate_actions'].append(f"Apply {effect_forecast['recommended_effects'][0]['effect']} at {effect_forecast['recommended_effects'][0]['recommended_intensity']:.1f} intensity")
        
        if aesthetic_scores['typography_score'] < 0.8:
            master_recommendations['medium_term_actions'].append(f"Implement {typography_forecast['recommended_typography']['font_style']} typography")
        
        forecast_result = {
            'overall_aesthetic_score': overall_aesthetic_score,
            'aesthetic_breakdown': aesthetic_scores,
            'color_forecast': color_forecast,
            'effect_forecast': effect_forecast,
            'typography_forecast': typography_forecast,
            'platform_optimization': platform_optimization,
            'master_recommendations': master_recommendations,
            'viral_potential_rating': self._calculate_viral_potential_rating(overall_aesthetic_score),
            'trend_longevity': self._predict_trend_longevity(aesthetic_scores)
        }
        
        print(f"→ [Aesthetic Forecaster] Forecast complete - Overall score: {overall_aesthetic_score:.3f}")
        print(f"→ [Aesthetic Forecaster] Viral potential: {forecast_result['viral_potential_rating']}")
        
        return forecast_result
    
    def _calculate_viral_potential_rating(self, score: float) -> str:
        """Calculates viral potential rating."""
        if score >= 0.9:
            return "EXPLOSIVE"
        elif score >= 0.8:
            return "HIGH"
        elif score >= 0.7:
            return "MODERATE"
        elif score >= 0.6:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _predict_trend_longevity(self, scores: Dict[str, float]) -> Dict[str, str]:
        """Predicts how long current trends will last."""
        return {
            'color_trends': "6-12 months",
            'effect_trends': "3-6 months",
            'typography_trends': "12-18 months",
            'platform_trends': "2-4 months"
        }