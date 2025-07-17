# config.py

# --- Caption Style Configuration ---
# Defines the visual appearance of the dynamic captions.
CAPTION_STYLE = {
    "font": "Arial-Bold",  # A default font, place your .ttf in assets/fonts/
    "fontsize": 72,
    "color": "white",
    "stroke_color": "black",
    "stroke_width": 3,
    "highlight_color": "#FFFF00",  # Yellow for the active word
}

# --- AI Director Style Profiles ---
# Defines the "personality" of the editor. The Director uses these
# parameters to make creative decisions.
STYLE_PROFILES = {
    "high_energy_meme": {
        "description": "Fast-paced, aggressive zooms, quick cuts, and lots of effects. Perfect for memes and short-form content.",
        "allow_sfx": True,
        "allowed_effects": ["zoom_punch", "screen_shake", "rgb_split"],
        "allowed_transitions": ["glitch", "whip_pan"],
        "effect_frequency": 0.5,  # 0.0 (never) to 1.0 (very often)
        "transition_frequency": 0.7,
        "zoom_intensity": 1.15,  # e.g., 1.15 = 15% zoom
        "use_hook_text": True,
        "use_progress_bar": True,
    },
    "calm_corporate": {
        "description": "Clean, professional, with subtle effects and smooth transitions. Ideal for corporate videos or tutorials.",
        "allow_sfx": False,
        "allowed_effects": [],
        "allowed_transitions": [],  # Could add a "crossfade" later
        "effect_frequency": 0.0,
        "transition_frequency": 0.1,
        "zoom_intensity": 1.05,
        "use_hook_text": False,
        "use_progress_bar": False,
    },
    "viral_tiktok": {
        "description": "Maximum viral potential with aggressive cuts, dramatic effects, and constant engagement.",
        "allow_sfx": True,
        "allowed_effects": ["zoom_punch", "screen_shake", "rgb_split", "glitch"],
        "allowed_transitions": ["glitch", "whip_pan", "zoom"],
        "effect_frequency": 0.8,
        "transition_frequency": 0.9,
        "zoom_intensity": 1.25,
        "use_hook_text": True,
        "use_progress_bar": True,
    },
    "cinematic": {
        "description": "Film-quality editing with smooth transitions and subtle effects.",
        "allow_sfx": False,
        "allowed_effects": ["zoom_punch"],
        "allowed_transitions": ["zoom"],
        "effect_frequency": 0.2,
        "transition_frequency": 0.3,
        "zoom_intensity": 1.08,
        "use_hook_text": False,
        "use_progress_bar": False,
    },
    # Add more profiles here as needed
}

def get_default_style():
    """Returns the name of the default style profile."""
    return "high_energy_meme"

def get_style_profile(style_name: str):
    """Returns the style profile dictionary for the given style name."""
    return STYLE_PROFILES.get(style_name, STYLE_PROFILES[get_default_style()])