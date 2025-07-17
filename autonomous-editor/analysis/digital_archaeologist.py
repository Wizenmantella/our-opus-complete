# analysis/digital_archaeologist.py
"""
Digital Archaeologist - Zero-cost asset foraging through procedural generation and optimization.
This system creates and manages digital assets without external dependencies or costs.
"""

import numpy as np
import cv2
from typing import Dict, List, Any, Optional, Tuple
from project import VideoProject
import json
import os
from datetime import datetime
import hashlib

class DigitalArchaeologist:
    """
    The Digital Archaeologist discovers, generates, and optimizes digital assets
    to achieve zero operational expense while maintaining professional quality.
    
    Core Capabilities:
    - Procedural texture generation
    - Algorithmic pattern creation
    - Font synthesis and optimization
    - Color palette extraction and enhancement
    - Asset caching and reuse
    - Memory-efficient asset management
    """
    
    def __init__(self, asset_cache_dir: str = "assets/cache"):
        self.asset_cache_dir = asset_cache_dir
        self.generated_assets = {}
        self.asset_registry = {}
        
        # Create cache directory if it doesn't exist
        os.makedirs(asset_cache_dir, exist_ok=True)
        
        # Procedural generation seeds for consistency
        self.texture_seeds = {
            'noise': 12345,
            'gradient': 23456,
            'pattern': 34567,
            'organic': 45678
        }
        
        print("→ [Digital Archaeologist] Asset foraging system initialized")
        print(f"→ [Digital Archaeologist] Cache directory: {asset_cache_dir}")
        print("→ [Digital Archaeologist] Ready for zero-cost asset generation")
    
    def generate_procedural_texture(self, width: int, height: int, texture_type: str = 'noise') -> np.ndarray:
        """Generates procedural textures algorithmically."""
        
        # Set seed for reproducible results
        np.random.seed(self.texture_seeds.get(texture_type, 12345))
        
        if texture_type == 'noise':
            return self._generate_noise_texture(width, height)
        elif texture_type == 'gradient':
            return self._generate_gradient_texture(width, height)
        elif texture_type == 'pattern':
            return self._generate_pattern_texture(width, height)
        elif texture_type == 'organic':
            return self._generate_organic_texture(width, height)
        elif texture_type == 'geometric':
            return self._generate_geometric_texture(width, height)
        else:
            return self._generate_noise_texture(width, height)
    
    def _generate_noise_texture(self, width: int, height: int) -> np.ndarray:
        """Generates various noise-based textures."""
        # Perlin-like noise simulation
        texture = np.random.random((height, width, 3))
        
        # Apply multiple octaves for more natural look
        for octave in range(3):
            scale = 2 ** octave
            octave_noise = np.random.random((height // scale + 1, width // scale + 1, 3))
            
            # Resize octave to full size
            octave_resized = cv2.resize(octave_noise, (width, height), interpolation=cv2.INTER_LINEAR)
            
            # Blend with main texture
            texture += octave_resized * (0.5 ** octave)
        
        # Normalize
        texture = texture / np.max(texture)
        
        return (texture * 255).astype(np.uint8)
    
    def _generate_gradient_texture(self, width: int, height: int) -> np.ndarray:
        """Generates gradient-based textures."""
        # Create coordinate grids
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        X, Y = np.meshgrid(x, y)
        
        # Radial gradient
        center_x, center_y = 0.5, 0.5
        radius = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        
        # Create 3-channel gradient
        texture = np.zeros((height, width, 3))
        texture[:, :, 0] = radius  # Red channel
        texture[:, :, 1] = X  # Green channel (horizontal gradient)
        texture[:, :, 2] = Y  # Blue channel (vertical gradient)
        
        # Normalize and convert to uint8
        texture = (texture * 255).astype(np.uint8)
        
        return texture
    
    def _generate_pattern_texture(self, width: int, height: int) -> np.ndarray:
        """Generates geometric pattern textures."""
        texture = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create checkerboard pattern
        tile_size = min(width, height) // 8
        
        for y in range(height):
            for x in range(width):
                tile_x = x // tile_size
                tile_y = y // tile_size
                
                if (tile_x + tile_y) % 2 == 0:
                    texture[y, x] = [255, 255, 255]
                else:
                    texture[y, x] = [100, 100, 100]
        
        # Add some variation
        noise = np.random.randint(0, 50, (height, width, 3))
        texture = np.clip(texture.astype(int) + noise, 0, 255).astype(np.uint8)
        
        return texture
    
    def _generate_organic_texture(self, width: int, height: int) -> np.ndarray:
        """Generates organic, natural-looking textures."""
        # Start with noise base
        texture = self._generate_noise_texture(width, height)
        
        # Apply organic transformations
        # Simulate wood grain or stone patterns
        for i in range(3):  # RGB channels
            channel = texture[:, :, i].astype(float)
            
            # Apply sinusoidal distortion
            x_indices = np.arange(width)
            y_indices = np.arange(height)
            X, Y = np.meshgrid(x_indices, y_indices)
            
            distortion = 20 * np.sin(X * 0.02) + 15 * np.cos(Y * 0.03)
            
            # Apply distortion
            for y in range(height):
                for x in range(width):
                    new_x = int(np.clip(x + distortion[y, x], 0, width - 1))
                    channel[y, x] = texture[y, new_x, i]
            
            texture[:, :, i] = np.clip(channel, 0, 255).astype(np.uint8)
        
        return texture
    
    def _generate_geometric_texture(self, width: int, height: int) -> np.ndarray:
        """Generates geometric pattern textures."""
        texture = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create hexagonal pattern
        hex_size = min(width, height) // 12
        
        for y in range(height):
            for x in range(width):
                # Hexagonal grid calculation
                hex_x = x / hex_size
                hex_y = y / hex_size
                
                # Simplified hexagonal distance
                distance = abs(hex_x % 2 - 1) + abs(hex_y % 2 - 1)
                
                if distance < 0.8:
                    texture[y, x] = [200, 220, 255]  # Light blue
                else:
                    texture[y, x] = [50, 70, 100]   # Dark blue
        
        return texture
    
    def extract_color_palette(self, project: VideoProject, num_colors: int = 8) -> List[Tuple[int, int, int]]:
        """Extracts dominant color palette from video."""
        if not project.video_path:
            return [(255, 100, 100), (100, 255, 100), (100, 100, 255)]  # Default palette
        
        cap = cv2.VideoCapture(project.video_path)
        
        # Sample frames for color analysis
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_frames = min(10, frame_count)
        
        all_pixels = []
        
        for i in range(sample_frames):
            frame_idx = (i * frame_count) // sample_frames
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if ret:
                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (100, 100))
                pixels = small_frame.reshape(-1, 3)
                all_pixels.extend(pixels)
        
        cap.release()
        
        if not all_pixels:
            return [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
        
        # K-means clustering to find dominant colors
        pixels = np.array(all_pixels, dtype=np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Convert centers to RGB tuples
        palette = [(int(c[2]), int(c[1]), int(c[0])) for c in centers]  # BGR to RGB
        
        return palette
    
    def generate_typography_assets(self, text: str, style: str = 'bold') -> Dict[str, Any]:
        """Generates typography assets procedurally."""
        
        typography_assets = {
            'font_style': style,
            'text': text,
            'outlines': [],
            'shadows': [],
            'effects': []
        }
        
        # Define typography parameters based on style
        if style == 'bold':
            typography_assets.update({
                'weight': 'heavy',
                'outline_thickness': 3,
                'shadow_offset': (2, 2),
                'shadow_blur': 4
            })
        elif style == 'elegant':
            typography_assets.update({
                'weight': 'light',
                'outline_thickness': 1,
                'shadow_offset': (1, 1),
                'shadow_blur': 2
            })
        elif style == 'impact':
            typography_assets.update({
                'weight': 'black',
                'outline_thickness': 5,
                'shadow_offset': (3, 3),
                'shadow_blur': 6
            })
        
        return typography_assets
    
    def create_overlay_assets(self, width: int, height: int, overlay_type: str = 'frame') -> np.ndarray:
        """Creates overlay assets procedurally."""
        
        if overlay_type == 'frame':
            return self._create_frame_overlay(width, height)
        elif overlay_type == 'vignette':
            return self._create_vignette_overlay(width, height)
        elif overlay_type == 'border':
            return self._create_border_overlay(width, height)
        elif overlay_type == 'gradient':
            return self._create_gradient_overlay(width, height)
        else:
            return self._create_frame_overlay(width, height)
    
    def _create_frame_overlay(self, width: int, height: int) -> np.ndarray:
        """Creates a decorative frame overlay."""
        overlay = np.zeros((height, width, 4), dtype=np.uint8)  # RGBA
        
        # Frame thickness
        thickness = min(width, height) // 20
        
        # Create frame
        overlay[:thickness, :] = [255, 255, 255, 128]  # Top
        overlay[-thickness:, :] = [255, 255, 255, 128]  # Bottom
        overlay[:, :thickness] = [255, 255, 255, 128]  # Left
        overlay[:, -thickness:] = [255, 255, 255, 128]  # Right
        
        # Add corner decorations
        corner_size = thickness * 2
        overlay[:corner_size, :corner_size] = [255, 255, 255, 180]  # Top-left
        overlay[:corner_size, -corner_size:] = [255, 255, 255, 180]  # Top-right
        overlay[-corner_size:, :corner_size] = [255, 255, 255, 180]  # Bottom-left
        overlay[-corner_size:, -corner_size:] = [255, 255, 255, 180]  # Bottom-right
        
        return overlay
    
    def _create_vignette_overlay(self, width: int, height: int) -> np.ndarray:
        """Creates a vignette overlay."""
        overlay = np.zeros((height, width, 4), dtype=np.uint8)  # RGBA
        
        # Create coordinate grids
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        X, Y = np.meshgrid(x, y)
        
        # Radial distance from center
        radius = np.sqrt(X**2 + Y**2)
        
        # Vignette function
        vignette = np.exp(-radius**2)
        
        # Invert for darkening effect
        vignette = 1 - vignette
        vignette = np.clip(vignette * 255, 0, 255)
        
        # Apply to all color channels, use as alpha
        overlay[:, :, 3] = vignette.astype(np.uint8)
        
        return overlay
    
    def _create_border_overlay(self, width: int, height: int) -> np.ndarray:
        """Creates a simple border overlay."""
        overlay = np.zeros((height, width, 4), dtype=np.uint8)  # RGBA
        
        border_width = 5
        
        # Create border
        overlay[:border_width, :] = [255, 255, 255, 255]  # Top
        overlay[-border_width:, :] = [255, 255, 255, 255]  # Bottom
        overlay[:, :border_width] = [255, 255, 255, 255]  # Left
        overlay[:, -border_width:] = [255, 255, 255, 255]  # Right
        
        return overlay
    
    def _create_gradient_overlay(self, width: int, height: int) -> np.ndarray:
        """Creates a gradient overlay."""
        overlay = np.zeros((height, width, 4), dtype=np.uint8)  # RGBA
        
        # Create vertical gradient
        gradient = np.linspace(0, 255, height)
        
        for i in range(height):
            overlay[i, :, :3] = [100, 150, 200]  # Blue tint
            overlay[i, :, 3] = int(gradient[i] * 0.3)  # 30% max opacity
        
        return overlay
    
    def cache_asset(self, asset_data: np.ndarray, asset_id: str, asset_type: str) -> str:
        """Caches generated assets for reuse."""
        
        # Create hash for asset identification
        asset_hash = hashlib.md5(asset_data.tobytes()).hexdigest()[:8]
        filename = f"{asset_type}_{asset_id}_{asset_hash}.npy"
        filepath = os.path.join(self.asset_cache_dir, filename)
        
        # Save asset
        np.save(filepath, asset_data)
        
        # Update registry
        self.asset_registry[asset_id] = {
            'filepath': filepath,
            'type': asset_type,
            'hash': asset_hash,
            'created': datetime.now().isoformat(),
            'size': asset_data.shape
        }
        
        return filepath
    
    def load_cached_asset(self, asset_id: str) -> Optional[np.ndarray]:
        """Loads asset from cache if available."""
        
        if asset_id in self.asset_registry:
            filepath = self.asset_registry[asset_id]['filepath']
            if os.path.exists(filepath):
                return np.load(filepath)
        
        return None
    
    def optimize_asset_memory(self, asset: np.ndarray, quality: float = 0.8) -> np.ndarray:
        """Optimizes asset memory usage while maintaining quality."""
        
        # Reduce precision for memory efficiency
        if asset.dtype == np.float64:
            asset = asset.astype(np.float32)
        
        # Apply quality-based compression for images
        if len(asset.shape) >= 2:
            h, w = asset.shape[:2]
            
            # Reduce resolution if quality allows
            if quality < 1.0:
                new_h = int(h * quality)
                new_w = int(w * quality)
                if new_h > 0 and new_w > 0:
                    asset = cv2.resize(asset, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        return asset
    
    def comprehensive_asset_generation(self, project: VideoProject) -> Dict[str, Any]:
        """
        Performs comprehensive asset generation for the project.
        """
        print("→ [Digital Archaeologist] Beginning comprehensive asset generation...")
        
        # Extract video dimensions
        if project.clip:
            width = int(project.clip.w)
            height = int(project.clip.h)
        else:
            width, height = 1920, 1080  # Default HD
        
        generated_assets = {
            'textures': {},
            'overlays': {},
            'typography': {},
            'color_palette': [],
            'cache_info': {}
        }
        
        # Generate texture library
        texture_types = ['noise', 'gradient', 'pattern', 'organic', 'geometric']
        for texture_type in texture_types:
            texture = self.generate_procedural_texture(width // 4, height // 4, texture_type)
            asset_id = f"texture_{texture_type}_{width}x{height}"
            
            # Cache the asset
            cache_path = self.cache_asset(texture, asset_id, 'texture')
            
            generated_assets['textures'][texture_type] = {
                'data': texture,
                'cache_path': cache_path,
                'dimensions': (width // 4, height // 4)
            }
        
        # Generate overlay library
        overlay_types = ['frame', 'vignette', 'border', 'gradient']
        for overlay_type in overlay_types:
            overlay = self.create_overlay_assets(width, height, overlay_type)
            asset_id = f"overlay_{overlay_type}_{width}x{height}"
            
            # Cache the asset
            cache_path = self.cache_asset(overlay, asset_id, 'overlay')
            
            generated_assets['overlays'][overlay_type] = {
                'data': overlay,
                'cache_path': cache_path,
                'dimensions': (width, height)
            }
        
        # Extract color palette
        color_palette = self.extract_color_palette(project)
        generated_assets['color_palette'] = color_palette
        
        # Generate typography assets
        if project.transcript:
            sample_text = " ".join([
                segment.get('text', '')
                for segment in project.transcript[:3]  # First 3 segments
            ])[:50]  # Limit length
            
            if sample_text:
                typography_styles = ['bold', 'elegant', 'impact']
                for style in typography_styles:
                    typography = self.generate_typography_assets(sample_text, style)
                    generated_assets['typography'][style] = typography
        
        # Cache information
        generated_assets['cache_info'] = {
            'total_assets': len(self.asset_registry),
            'cache_directory': self.asset_cache_dir,
            'memory_usage_mb': self._calculate_cache_size_mb()
        }
        
        print(f"→ [Digital Archaeologist] Generated {len(texture_types)} textures")
        print(f"→ [Digital Archaeologist] Generated {len(overlay_types)} overlays") 
        print(f"→ [Digital Archaeologist] Extracted {len(color_palette)} dominant colors")
        print(f"→ [Digital Archaeologist] Cache size: {generated_assets['cache_info']['memory_usage_mb']:.1f} MB")
        
        return generated_assets
    
    def _calculate_cache_size_mb(self) -> float:
        """Calculates total cache size in MB."""
        total_size = 0
        
        for asset_info in self.asset_registry.values():
            filepath = asset_info['filepath']
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
        
        return total_size / (1024 * 1024)  # Convert to MB