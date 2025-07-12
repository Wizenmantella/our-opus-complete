#!/usr/bin/env python3
"""
Advanced Typography Engine - Complete text and typography system
Supports all professional text features, animations, and effects
"""

import asyncio
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
import math

logger = logging.getLogger(__name__)


class TextAlignment(Enum):
    """Text alignment options"""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    START = "start"
    END = "end"


class TextTransform(Enum):
    """Text transformation options"""
    NONE = "none"
    UPPERCASE = "uppercase"
    LOWERCASE = "lowercase"
    CAPITALIZE = "capitalize"
    SMALL_CAPS = "small_caps"


class FontWeight(Enum):
    """Font weight options"""
    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    REGULAR = 400
    MEDIUM = 500
    SEMI_BOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    BLACK = 900


class FontStretch(Enum):
    """Font stretch options"""
    ULTRA_CONDENSED = "ultra_condensed"
    EXTRA_CONDENSED = "extra_condensed"
    CONDENSED = "condensed"
    SEMI_CONDENSED = "semi_condensed"
    NORMAL = "normal"
    SEMI_EXPANDED = "semi_expanded"
    EXPANDED = "expanded"
    EXTRA_EXPANDED = "extra_expanded"
    ULTRA_EXPANDED = "ultra_expanded"


class TextEffect(Enum):
    """Text effects and styles"""
    NONE = "none"
    SHADOW = "shadow"
    OUTLINE = "outline"
    GLOW = "glow"
    EMBOSS = "emboss"
    ENGRAVE = "engrave"
    GRADIENT = "gradient"
    PATTERN = "pattern"
    TEXTURE = "texture"
    STROKE = "stroke"
    BEVEL = "bevel"
    REFLECTION = "reflection"
    PERSPECTIVE = "perspective"
    DISTORTION = "distortion"
    CHROMATIC_ABERRATION = "chromatic_aberration"
    KINETIC_TYPOGRAPHY = "kinetic_typography"


class AnimationType(Enum):
    """Text animation types"""
    NONE = "none"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    SLIDE_IN_LEFT = "slide_in_left"
    SLIDE_IN_RIGHT = "slide_in_right"
    SLIDE_IN_TOP = "slide_in_top"
    SLIDE_IN_BOTTOM = "slide_in_bottom"
    SCALE_IN = "scale_in"
    SCALE_OUT = "scale_out"
    ROTATE_IN = "rotate_in"
    ROTATE_OUT = "rotate_out"
    BOUNCE_IN = "bounce_in"
    BOUNCE_OUT = "bounce_out"
    ELASTIC_IN = "elastic_in"
    ELASTIC_OUT = "elastic_out"
    TYPEWRITER = "typewriter"
    REVEAL = "reveal"
    WORD_BY_WORD = "word_by_word"
    LETTER_BY_LETTER = "letter_by_letter"
    FLICKER = "flicker"
    GLOW_PULSE = "glow_pulse"
    COLOR_CYCLE = "color_cycle"
    WAVE = "wave"
    SHAKE = "shake"
    VIBRATE = "vibrate"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    FLIP_X = "flip_x"
    FLIP_Y = "flip_y"
    SPIRAL_IN = "spiral_in"
    SPIRAL_OUT = "spiral_out"


@dataclass
class Color:
    """Color representation with alpha"""
    r: float = 1.0  # 0.0 to 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
    
    @classmethod
    def from_hex(cls, hex_color: str) -> 'Color':
        """Create color from hex string"""
        hex_color = hex_color.lstrip('#')
        return cls(
            r=int(hex_color[0:2], 16) / 255.0,
            g=int(hex_color[2:4], 16) / 255.0,
            b=int(hex_color[4:6], 16) / 255.0,
            a=1.0 if len(hex_color) == 6 else int(hex_color[6:8], 16) / 255.0
        )
    
    def to_hex(self) -> str:
        """Convert to hex string"""
        return f"#{int(self.r*255):02x}{int(self.g*255):02x}{int(self.b*255):02x}{int(self.a*255):02x}"


@dataclass
class Gradient:
    """Gradient definition"""
    type: str = "linear"  # linear, radial, conic
    colors: List[Tuple[float, Color]] = field(default_factory=list)  # position, color
    angle: float = 0.0  # degrees
    center_x: float = 0.5  # 0.0 to 1.0
    center_y: float = 0.5  # 0.0 to 1.0


@dataclass
class Shadow:
    """Shadow effect configuration"""
    offset_x: float = 2.0
    offset_y: float = 2.0
    blur_radius: float = 4.0
    color: Color = field(default_factory=lambda: Color(0, 0, 0, 0.5))
    spread: float = 0.0


@dataclass
class Outline:
    """Outline/stroke configuration"""
    width: float = 1.0
    color: Color = field(default_factory=lambda: Color(0, 0, 0, 1))
    position: str = "outside"  # inside, outside, center
    dash_pattern: List[float] = field(default_factory=list)
    line_cap: str = "round"  # round, square, butt
    line_join: str = "round"  # round, bevel, miter


@dataclass
class TextStyle:
    """Complete text styling configuration"""
    # Font properties
    font_family: str = "Arial"
    font_size: float = 24.0
    font_weight: FontWeight = FontWeight.REGULAR
    font_style: str = "normal"  # normal, italic, oblique
    font_stretch: FontStretch = FontStretch.NORMAL
    
    # Text properties
    color: Color = field(default_factory=lambda: Color(1, 1, 1, 1))
    background_color: Optional[Color] = None
    line_height: float = 1.2
    letter_spacing: float = 0.0
    word_spacing: float = 0.0
    text_align: TextAlignment = TextAlignment.LEFT
    text_transform: TextTransform = TextTransform.NONE
    
    # Effects
    shadow: Optional[Shadow] = None
    outline: Optional[Outline] = None
    gradient: Optional[Gradient] = None
    
    # Advanced effects
    opacity: float = 1.0
    blur: float = 0.0
    brightness: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0
    hue_shift: float = 0.0


@dataclass
class TextAnimation:
    """Text animation configuration"""
    type: AnimationType = AnimationType.NONE
    duration: float = 1.0  # seconds
    delay: float = 0.0
    ease: str = "ease_in_out"  # linear, ease_in, ease_out, ease_in_out, custom
    loop: bool = False
    reverse: bool = False
    
    # Animation-specific properties
    from_value: Dict[str, Any] = field(default_factory=dict)
    to_value: Dict[str, Any] = field(default_factory=dict)
    
    # Keyframe animation
    keyframes: List[Tuple[float, Dict[str, Any]]] = field(default_factory=list)
    
    # Special effects
    stagger: float = 0.0  # Delay between letters/words
    direction: str = "normal"  # normal, reverse, alternate


@dataclass
class TextLayer:
    """Individual text layer"""
    id: str
    text: str
    style: TextStyle
    animation: Optional[TextAnimation] = None
    
    # Position and transform
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    rotation: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    anchor_x: float = 0.5  # 0.0 = left, 0.5 = center, 1.0 = right
    anchor_y: float = 0.5  # 0.0 = top, 0.5 = center, 1.0 = bottom
    
    # Visibility
    visible: bool = True
    start_time: float = 0.0
    end_time: float = 10.0
    
    # Layout
    width: Optional[float] = None
    height: Optional[float] = None
    max_width: Optional[float] = None
    max_height: Optional[float] = None
    word_wrap: bool = True
    
    # Interaction
    clickable: bool = False
    hover_style: Optional[TextStyle] = None


@dataclass
class TextTemplate:
    """Reusable text template"""
    id: str
    name: str
    description: str = ""
    layers: List[TextLayer] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)  # Template variables
    category: str = "general"
    tags: List[str] = field(default_factory=list)


class AdvancedTypographyEngine:
    """
    Advanced Typography Engine - Complete text and typography system
    Supports professional text features, animations, and effects
    """
    
    def __init__(self):
        self.text_layers: Dict[str, TextLayer] = {}
        self.templates: Dict[str, TextTemplate] = {}
        self.fonts_cache: Dict[str, Any] = {}
        self.animation_cache: Dict[str, Any] = {}
        
        # Typography settings
        self.canvas_width: int = 1920
        self.canvas_height: int = 1080
        self.frame_rate: float = 29.97
        
        # Font management
        self.available_fonts: List[str] = []
        self.font_fallbacks: Dict[str, List[str]] = {}
        
        # Performance settings
        self.use_gpu_acceleration: bool = True
        self.cache_rendered_text: bool = True
        self.max_cache_size: int = 1000
        
        logger.info("Advanced Typography Engine initialized")
        
        # Load system fonts and templates
        self._initialize_fonts()
        self._load_default_templates()
    
    def _initialize_fonts(self):
        """Initialize font system and load available fonts"""
        # Common system fonts
        system_fonts = [
            "Arial", "Helvetica", "Times", "Times New Roman", "Courier",
            "Courier New", "Georgia", "Verdana", "Trebuchet MS", "Impact",
            "Comic Sans MS", "Arial Black", "Palatino", "Garamond",
            "Bookman", "Avant Garde", "Optima", "Futura", "Gill Sans",
            "Century Gothic", "Lucida Grande", "Tahoma", "Geneva"
        ]
        
        # Professional fonts
        professional_fonts = [
            "Proxima Nova", "Helvetica Neue", "Avenir", "Gotham", "Din",
            "Montserrat", "Open Sans", "Lato", "Source Sans Pro", "Roboto",
            "Poppins", "Inter", "SF Pro Display", "Segoe UI", "Nunito",
            "Raleway", "Ubuntu", "Oxygen", "Cantarell", "Fira Sans"
        ]
        
        # Creative fonts
        creative_fonts = [
            "Bebas Neue", "Oswald", "Anton", "Bangers", "Fredoka One",
            "Righteous", "Lobster", "Dancing Script", "Pacifico", "Comfortaa",
            "Indie Flower", "Shadows Into Light", "Kalam", "Caveat",
            "Satisfy", "Great Vibes", "Amatic SC", "Permanent Marker"
        ]
        
        self.available_fonts = system_fonts + professional_fonts + creative_fonts
        
        # Set up font fallbacks
        self.font_fallbacks = {
            "serif": ["Times New Roman", "Times", "Georgia", "serif"],
            "sans-serif": ["Arial", "Helvetica", "Verdana", "sans-serif"],
            "monospace": ["Courier New", "Courier", "Monaco", "monospace"],
            "cursive": ["Dancing Script", "Pacifico", "Lobster", "cursive"],
            "fantasy": ["Impact", "Bangers", "Anton", "fantasy"]
        }
        
        logger.info(f"Loaded {len(self.available_fonts)} fonts")
    
    def _load_default_templates(self):
        """Load default text templates"""
        # Title templates
        title_template = TextTemplate(
            id="title_template",
            name="Main Title",
            description="Clean main title template",
            category="titles"
        )
        
        title_layer = TextLayer(
            id="title_layer",
            text="{title}",
            style=TextStyle(
                font_family="Montserrat",
                font_size=48.0,
                font_weight=FontWeight.BOLD,
                color=Color.from_hex("#FFFFFF"),
                shadow=Shadow(offset_x=3, offset_y=3, blur_radius=6, color=Color(0, 0, 0, 0.7))
            ),
            animation=TextAnimation(
                type=AnimationType.FADE_IN,
                duration=1.0,
                ease="ease_out"
            )
        )
        
        title_template.layers.append(title_layer)
        title_template.variables = {"title": "Your Title Here"}
        self.templates[title_template.id] = title_template
        
        # Subtitle template
        subtitle_template = TextTemplate(
            id="subtitle_template",
            name="Subtitle",
            description="Elegant subtitle template",
            category="titles"
        )
        
        subtitle_layer = TextLayer(
            id="subtitle_layer",
            text="{subtitle}",
            style=TextStyle(
                font_family="Open Sans",
                font_size=24.0,
                font_weight=FontWeight.REGULAR,
                color=Color.from_hex("#E0E0E0"),
                letter_spacing=2.0
            ),
            animation=TextAnimation(
                type=AnimationType.SLIDE_IN_BOTTOM,
                duration=0.8,
                delay=0.5,
                ease="ease_out"
            )
        )
        
        subtitle_template.layers.append(subtitle_layer)
        subtitle_template.variables = {"subtitle": "Your Subtitle Here"}
        self.templates[subtitle_template.id] = subtitle_template
        
        # Lower third template
        lower_third_template = TextTemplate(
            id="lower_third_template",
            name="Lower Third",
            description="Professional lower third template",
            category="graphics"
        )
        
        # Background layer
        bg_layer = TextLayer(
            id="bg_layer",
            text="",
            style=TextStyle(
                background_color=Color(0, 0.4, 0.8, 0.9),
                font_size=1.0
            ),
            width=400,
            height=80,
            y=-200
        )
        
        # Name layer
        name_layer = TextLayer(
            id="name_layer",
            text="{name}",
            style=TextStyle(
                font_family="Roboto",
                font_size=22.0,
                font_weight=FontWeight.BOLD,
                color=Color.from_hex("#FFFFFF")
            ),
            y=-210,
            animation=TextAnimation(
                type=AnimationType.SLIDE_IN_LEFT,
                duration=0.6,
                ease="ease_out"
            )
        )
        
        # Title layer
        title_layer = TextLayer(
            id="title_layer",
            text="{title}",
            style=TextStyle(
                font_family="Roboto",
                font_size=16.0,
                font_weight=FontWeight.REGULAR,
                color=Color.from_hex("#E0E0E0")
            ),
            y=-185,
            animation=TextAnimation(
                type=AnimationType.SLIDE_IN_LEFT,
                duration=0.6,
                delay=0.2,
                ease="ease_out"
            )
        )
        
        lower_third_template.layers.extend([bg_layer, name_layer, title_layer])
        lower_third_template.variables = {"name": "John Doe", "title": "Professional Title"}
        self.templates[lower_third_template.id] = lower_third_template
        
        logger.info(f"Loaded {len(self.templates)} default templates")
    
    def create_text_layer(self, text: str, style: TextStyle = None, 
                         animation: TextAnimation = None, **kwargs) -> str:
        """Create a new text layer"""
        import uuid
        
        layer_id = str(uuid.uuid4())
        
        layer = TextLayer(
            id=layer_id,
            text=text,
            style=style or TextStyle(),
            animation=animation,
            **kwargs
        )
        
        self.text_layers[layer_id] = layer
        logger.info(f"Created text layer: {layer_id}")
        return layer_id
    
    def update_text_layer(self, layer_id: str, **updates) -> bool:
        """Update text layer properties"""
        if layer_id not in self.text_layers:
            return False
        
        layer = self.text_layers[layer_id]
        
        for key, value in updates.items():
            if hasattr(layer, key):
                setattr(layer, key, value)
            elif hasattr(layer.style, key):
                setattr(layer.style, key, value)
            elif layer.animation and hasattr(layer.animation, key):
                setattr(layer.animation, key, value)
        
        logger.info(f"Updated text layer: {layer_id}")
        return True
    
    def apply_template(self, template_id: str, variables: Dict[str, str] = None) -> List[str]:
        """Apply a text template with variable substitution"""
        if template_id not in self.templates:
            logger.error(f"Template not found: {template_id}")
            return []
        
        template = self.templates[template_id]
        variables = variables or template.variables
        
        created_layers = []
        
        for template_layer in template.layers:
            # Substitute variables in text
            text = template_layer.text
            for var_name, var_value in variables.items():
                text = text.replace(f"{{{var_name}}}", var_value)
            
            # Create new layer from template
            layer = TextLayer(
                id=f"template_{template_id}_{len(created_layers)}",
                text=text,
                style=template_layer.style,
                animation=template_layer.animation,
                x=template_layer.x,
                y=template_layer.y,
                z=template_layer.z,
                rotation=template_layer.rotation,
                scale_x=template_layer.scale_x,
                scale_y=template_layer.scale_y,
                anchor_x=template_layer.anchor_x,
                anchor_y=template_layer.anchor_y,
                visible=template_layer.visible,
                start_time=template_layer.start_time,
                end_time=template_layer.end_time,
                width=template_layer.width,
                height=template_layer.height,
                max_width=template_layer.max_width,
                max_height=template_layer.max_height,
                word_wrap=template_layer.word_wrap
            )
            
            self.text_layers[layer.id] = layer
            created_layers.append(layer.id)
        
        logger.info(f"Applied template {template_id}, created {len(created_layers)} layers")
        return created_layers
    
    def create_animated_text(self, text: str, animation_type: AnimationType,
                           duration: float = 1.0, **animation_params) -> str:
        """Create animated text with predefined animations"""
        animation = TextAnimation(
            type=animation_type,
            duration=duration,
            **animation_params
        )
        
        # Set animation-specific defaults
        if animation_type == AnimationType.TYPEWRITER:
            animation.stagger = 0.05  # 50ms between letters
            animation.from_value = {"opacity": 0}
            animation.to_value = {"opacity": 1}
        
        elif animation_type == AnimationType.WORD_BY_WORD:
            animation.stagger = 0.2  # 200ms between words
            animation.from_value = {"scale": 0, "opacity": 0}
            animation.to_value = {"scale": 1, "opacity": 1}
        
        elif animation_type == AnimationType.GLOW_PULSE:
            animation.loop = True
            animation.from_value = {"glow_intensity": 0}
            animation.to_value = {"glow_intensity": 1}
            animation.direction = "alternate"
        
        elif animation_type == AnimationType.COLOR_CYCLE:
            animation.loop = True
            animation.keyframes = [
                (0.0, {"hue_shift": 0}),
                (0.33, {"hue_shift": 120}),
                (0.66, {"hue_shift": 240}),
                (1.0, {"hue_shift": 360})
            ]
        
        return self.create_text_layer(text, animation=animation)
    
    def create_kinetic_typography(self, text: str, style: str = "modern") -> List[str]:
        """Create kinetic typography sequence"""
        words = text.split()
        layers = []
        
        for i, word in enumerate(words):
            # Calculate positions and animations based on style
            if style == "modern":
                x_offset = (i % 3 - 1) * 200
                y_offset = (i // 3) * 100
                
                animation = TextAnimation(
                    type=AnimationType.SCALE_IN,
                    duration=0.8,
                    delay=i * 0.3,
                    ease="ease_out"
                )
                
                text_style = TextStyle(
                    font_family="Bebas Neue",
                    font_size=36 + (i % 3) * 12,
                    font_weight=FontWeight.BOLD,
                    color=Color.from_hex(["#FF6B35", "#004E89", "#FCBA28"][i % 3])
                )
            
            elif style == "elegant":
                x_offset = 0
                y_offset = i * 50
                
                animation = TextAnimation(
                    type=AnimationType.FADE_IN,
                    duration=1.2,
                    delay=i * 0.5,
                    ease="ease_in_out"
                )
                
                text_style = TextStyle(
                    font_family="Playfair Display",
                    font_size=28,
                    font_weight=FontWeight.REGULAR,
                    color=Color.from_hex("#2C2C2C"),
                    letter_spacing=2.0
                )
            
            layer_id = self.create_text_layer(
                text=word,
                style=text_style,
                animation=animation,
                x=x_offset,
                y=y_offset
            )
            
            layers.append(layer_id)
        
        logger.info(f"Created kinetic typography with {len(layers)} layers")
        return layers
    
    def add_text_effect(self, layer_id: str, effect: TextEffect, **effect_params) -> bool:
        """Add visual effect to text layer"""
        if layer_id not in self.text_layers:
            return False
        
        layer = self.text_layers[layer_id]
        
        if effect == TextEffect.SHADOW:
            layer.style.shadow = Shadow(
                offset_x=effect_params.get("offset_x", 2.0),
                offset_y=effect_params.get("offset_y", 2.0),
                blur_radius=effect_params.get("blur_radius", 4.0),
                color=effect_params.get("color", Color(0, 0, 0, 0.5))
            )
        
        elif effect == TextEffect.OUTLINE:
            layer.style.outline = Outline(
                width=effect_params.get("width", 2.0),
                color=effect_params.get("color", Color(0, 0, 0, 1)),
                position=effect_params.get("position", "outside")
            )
        
        elif effect == TextEffect.GRADIENT:
            layer.style.gradient = Gradient(
                type=effect_params.get("type", "linear"),
                colors=effect_params.get("colors", [(0.0, Color(1, 0, 0, 1)), (1.0, Color(0, 0, 1, 1))]),
                angle=effect_params.get("angle", 0.0)
            )
        
        elif effect == TextEffect.GLOW:
            layer.style.shadow = Shadow(
                offset_x=0,
                offset_y=0,
                blur_radius=effect_params.get("radius", 10.0),
                color=effect_params.get("color", Color(1, 1, 1, 0.8)),
                spread=effect_params.get("spread", 5.0)
            )
        
        logger.info(f"Added {effect.value} effect to layer {layer_id}")
        return True
    
    def animate_text_property(self, layer_id: str, property_name: str,
                            from_value: Any, to_value: Any, duration: float,
                            delay: float = 0.0, ease: str = "ease_in_out") -> bool:
        """Animate specific text property"""
        if layer_id not in self.text_layers:
            return False
        
        layer = self.text_layers[layer_id]
        
        if not layer.animation:
            layer.animation = TextAnimation()
        
        # Add keyframe animation
        layer.animation.keyframes.append((delay / duration, {property_name: from_value}))
        layer.animation.keyframes.append(((delay + duration) / duration, {property_name: to_value}))
        layer.animation.duration = max(layer.animation.duration, delay + duration)
        layer.animation.ease = ease
        
        logger.info(f"Added property animation for {property_name} on layer {layer_id}")
        return True
    
    def create_text_path_animation(self, layer_id: str, path_points: List[Tuple[float, float]],
                                 duration: float = 3.0) -> bool:
        """Animate text along a path"""
        if layer_id not in self.text_layers:
            return False
        
        layer = self.text_layers[layer_id]
        
        if not layer.animation:
            layer.animation = TextAnimation()
        
        # Create keyframes for path animation
        layer.animation.keyframes = []
        for i, (x, y) in enumerate(path_points):
            progress = i / (len(path_points) - 1) if len(path_points) > 1 else 0
            layer.animation.keyframes.append((progress, {"x": x, "y": y}))
        
        layer.animation.duration = duration
        layer.animation.ease = "ease_in_out"
        
        logger.info(f"Created path animation with {len(path_points)} points for layer {layer_id}")
        return True
    
    def render_text_layer(self, layer_id: str, time: float) -> Dict[str, Any]:
        """Render text layer at specific time"""
        if layer_id not in self.text_layers:
            return {}
        
        layer = self.text_layers[layer_id]
        
        # Check if layer is visible at this time
        if time < layer.start_time or time > layer.end_time or not layer.visible:
            return {"visible": False}
        
        # Calculate animated properties
        animated_props = self._calculate_animation_state(layer, time)
        
        # Build render data
        render_data = {
            "visible": True,
            "text": layer.text,
            "x": layer.x + animated_props.get("x", 0),
            "y": layer.y + animated_props.get("y", 0),
            "z": layer.z + animated_props.get("z", 0),
            "rotation": layer.rotation + animated_props.get("rotation", 0),
            "scale_x": layer.scale_x * animated_props.get("scale_x", 1),
            "scale_y": layer.scale_y * animated_props.get("scale_y", 1),
            "opacity": layer.style.opacity * animated_props.get("opacity", 1),
            "style": self._render_text_style(layer.style, animated_props),
            "layout": {
                "width": layer.width,
                "height": layer.height,
                "max_width": layer.max_width,
                "max_height": layer.max_height,
                "word_wrap": layer.word_wrap,
                "anchor_x": layer.anchor_x,
                "anchor_y": layer.anchor_y
            }
        }
        
        return render_data
    
    def _calculate_animation_state(self, layer: TextLayer, time: float) -> Dict[str, Any]:
        """Calculate animated property values at specific time"""
        if not layer.animation:
            return {}
        
        animation = layer.animation
        layer_time = time - layer.start_time - animation.delay
        
        if layer_time < 0 or layer_time > animation.duration:
            return {}
        
        progress = layer_time / animation.duration
        
        # Apply easing
        eased_progress = self._apply_easing(progress, animation.ease)
        
        animated_props = {}
        
        # Handle predefined animations
        if animation.type != AnimationType.NONE:
            animated_props.update(self._get_predefined_animation_values(animation.type, eased_progress))
        
        # Handle keyframe animations
        if animation.keyframes:
            animated_props.update(self._interpolate_keyframes(animation.keyframes, eased_progress))
        
        # Handle from/to values
        if animation.from_value and animation.to_value:
            for prop, from_val in animation.from_value.items():
                to_val = animation.to_value.get(prop, from_val)
                animated_props[prop] = self._interpolate_value(from_val, to_val, eased_progress)
        
        return animated_props
    
    def _apply_easing(self, progress: float, ease: str) -> float:
        """Apply easing function to progress"""
        if ease == "linear":
            return progress
        elif ease == "ease_in":
            return progress * progress
        elif ease == "ease_out":
            return 1 - (1 - progress) * (1 - progress)
        elif ease == "ease_in_out":
            if progress < 0.5:
                return 2 * progress * progress
            else:
                return 1 - 2 * (1 - progress) * (1 - progress)
        else:
            return progress  # Fallback to linear
    
    def _get_predefined_animation_values(self, animation_type: AnimationType, progress: float) -> Dict[str, Any]:
        """Get property values for predefined animations"""
        animations = {
            AnimationType.FADE_IN: {"opacity": progress},
            AnimationType.FADE_OUT: {"opacity": 1 - progress},
            AnimationType.SCALE_IN: {"scale_x": progress, "scale_y": progress},
            AnimationType.SCALE_OUT: {"scale_x": 1 - progress, "scale_y": 1 - progress},
            AnimationType.SLIDE_IN_LEFT: {"x": -100 * (1 - progress)},
            AnimationType.SLIDE_IN_RIGHT: {"x": 100 * (1 - progress)},
            AnimationType.SLIDE_IN_TOP: {"y": -100 * (1 - progress)},
            AnimationType.SLIDE_IN_BOTTOM: {"y": 100 * (1 - progress)},
            AnimationType.ROTATE_IN: {"rotation": 360 * (1 - progress)},
            AnimationType.ROTATE_OUT: {"rotation": 360 * progress},
            AnimationType.BOUNCE_IN: {
                "scale_x": 1 + 0.3 * math.sin(progress * math.pi * 4),
                "scale_y": 1 + 0.3 * math.sin(progress * math.pi * 4)
            },
            AnimationType.WAVE: {
                "y": 10 * math.sin(progress * math.pi * 6),
                "rotation": 5 * math.sin(progress * math.pi * 8)
            },
            AnimationType.SHAKE: {
                "x": 5 * math.sin(progress * math.pi * 20),
                "y": 5 * math.cos(progress * math.pi * 20)
            }
        }
        
        return animations.get(animation_type, {})
    
    def _interpolate_keyframes(self, keyframes: List[Tuple[float, Dict[str, Any]]], progress: float) -> Dict[str, Any]:
        """Interpolate between keyframes"""
        if not keyframes:
            return {}
        
        # Find surrounding keyframes
        before_keyframe = keyframes[0]
        after_keyframe = keyframes[-1]
        
        for i, (time, values) in enumerate(keyframes):
            if time <= progress:
                before_keyframe = (time, values)
                if i + 1 < len(keyframes):
                    after_keyframe = keyframes[i + 1]
            else:
                after_keyframe = (time, values)
                break
        
        # Interpolate between keyframes
        before_time, before_values = before_keyframe
        after_time, after_values = after_keyframe
        
        if before_time == after_time:
            return before_values
        
        local_progress = (progress - before_time) / (after_time - before_time)
        
        interpolated = {}
        for prop in before_values:
            if prop in after_values:
                before_val = before_values[prop]
                after_val = after_values[prop]
                interpolated[prop] = self._interpolate_value(before_val, after_val, local_progress)
            else:
                interpolated[prop] = before_values[prop]
        
        return interpolated
    
    def _interpolate_value(self, from_val: Any, to_val: Any, progress: float) -> Any:
        """Interpolate between two values"""
        if isinstance(from_val, (int, float)) and isinstance(to_val, (int, float)):
            return from_val + (to_val - from_val) * progress
        elif isinstance(from_val, Color) and isinstance(to_val, Color):
            return Color(
                r=from_val.r + (to_val.r - from_val.r) * progress,
                g=from_val.g + (to_val.g - from_val.g) * progress,
                b=from_val.b + (to_val.b - from_val.b) * progress,
                a=from_val.a + (to_val.a - from_val.a) * progress
            )
        else:
            return to_val if progress >= 0.5 else from_val
    
    def _render_text_style(self, style: TextStyle, animated_props: Dict[str, Any]) -> Dict[str, Any]:
        """Render text style with animations applied"""
        rendered_style = {
            "font_family": style.font_family,
            "font_size": style.font_size,
            "font_weight": style.font_weight.value,
            "font_style": style.font_style,
            "color": style.color,
            "line_height": style.line_height,
            "letter_spacing": style.letter_spacing,
            "word_spacing": style.word_spacing,
            "text_align": style.text_align.value,
            "text_transform": style.text_transform.value,
            "opacity": style.opacity * animated_props.get("opacity", 1),
            "blur": style.blur + animated_props.get("blur", 0),
            "brightness": style.brightness * animated_props.get("brightness", 1),
            "contrast": style.contrast * animated_props.get("contrast", 1),
            "saturation": style.saturation * animated_props.get("saturation", 1),
            "hue_shift": style.hue_shift + animated_props.get("hue_shift", 0)
        }
        
        # Add effects
        if style.shadow:
            rendered_style["shadow"] = style.shadow
        
        if style.outline:
            rendered_style["outline"] = style.outline
        
        if style.gradient:
            rendered_style["gradient"] = style.gradient
        
        if style.background_color:
            rendered_style["background_color"] = style.background_color
        
        return rendered_style
    
    def render_all_layers(self, time: float) -> List[Dict[str, Any]]:
        """Render all visible text layers at specific time"""
        rendered_layers = []
        
        # Sort layers by z-index
        sorted_layers = sorted(
            self.text_layers.values(),
            key=lambda layer: layer.z
        )
        
        for layer in sorted_layers:
            rendered = self.render_text_layer(layer.id, time)
            if rendered.get("visible", False):
                rendered_layers.append(rendered)
        
        return rendered_layers
    
    def export_typography_sequence(self, duration: float, frame_rate: float = None) -> List[List[Dict[str, Any]]]:
        """Export complete typography sequence as frame data"""
        frame_rate = frame_rate or self.frame_rate
        frame_count = int(duration * frame_rate)
        
        sequence = []
        
        for frame in range(frame_count):
            time = frame / frame_rate
            frame_data = self.render_all_layers(time)
            sequence.append(frame_data)
        
        logger.info(f"Exported typography sequence: {frame_count} frames")
        return sequence
    
    def create_subtitle_track(self, subtitle_data: List[Dict[str, Any]]) -> List[str]:
        """Create subtitle track from subtitle data"""
        layers = []
        
        for i, subtitle in enumerate(subtitle_data):
            text = subtitle.get("text", "")
            start_time = subtitle.get("start", 0.0)
            end_time = subtitle.get("end", start_time + 3.0)
            
            style = TextStyle(
                font_family="Arial",
                font_size=24.0,
                font_weight=FontWeight.REGULAR,
                color=Color.from_hex("#FFFFFF"),
                text_align=TextAlignment.CENTER,
                outline=Outline(width=2.0, color=Color(0, 0, 0, 1))
            )
            
            layer_id = self.create_text_layer(
                text=text,
                style=style,
                y=-300,  # Bottom of screen
                start_time=start_time,
                end_time=end_time,
                max_width=800,
                word_wrap=True
            )
            
            layers.append(layer_id)
        
        logger.info(f"Created subtitle track with {len(layers)} subtitles")
        return layers
    
    def get_typography_analysis(self) -> Dict[str, Any]:
        """Get comprehensive typography analysis"""
        analysis = {
            "total_layers": len(self.text_layers),
            "animated_layers": len([l for l in self.text_layers.values() if l.animation]),
            "templates_available": len(self.templates),
            "fonts_used": list(set(layer.style.font_family for layer in self.text_layers.values())),
            "effects_used": [],
            "animation_types": [],
            "performance_metrics": {
                "cache_size": len(self.animation_cache),
                "gpu_acceleration": self.use_gpu_acceleration
            }
        }
        
        # Analyze effects and animations
        for layer in self.text_layers.values():
            if layer.style.shadow:
                analysis["effects_used"].append("shadow")
            if layer.style.outline:
                analysis["effects_used"].append("outline")
            if layer.style.gradient:
                analysis["effects_used"].append("gradient")
            
            if layer.animation:
                analysis["animation_types"].append(layer.animation.type.value)
        
        analysis["effects_used"] = list(set(analysis["effects_used"]))
        analysis["animation_types"] = list(set(analysis["animation_types"]))
        
        return analysis


# Example usage and testing
async def demo_typography_engine():
    """Demonstrate typography engine capabilities"""
    typography = AdvancedTypographyEngine()
    
    # Create animated title
    title_id = typography.create_animated_text(
        "ULTIMATE VIDEO EDITOR",
        AnimationType.FADE_IN,
        duration=2.0
    )
    
    # Apply template
    lower_third_layers = typography.apply_template(
        "lower_third_template",
        {"name": "John Smith", "title": "Video Editor"}
    )
    
    # Create kinetic typography
    kinetic_layers = typography.create_kinetic_typography(
        "Amazing Professional Results",
        style="modern"
    )
    
    # Add effects
    typography.add_text_effect(title_id, TextEffect.GLOW, radius=15.0)
    
    # Render at specific time
    frame_data = typography.render_all_layers(1.0)
    
    # Get analysis
    analysis = typography.get_typography_analysis()
    
    print(f"Typography engine demo:")
    print(f"- Created {analysis['total_layers']} text layers")
    print(f"- {analysis['animated_layers']} animated layers")
    print(f"- Using fonts: {', '.join(analysis['fonts_used'][:3])}")
    print(f"- Effects: {', '.join(analysis['effects_used'])}")
    
    return typography


if __name__ == "__main__":
    asyncio.run(demo_typography_engine())