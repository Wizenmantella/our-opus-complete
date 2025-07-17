# config.py

# --- Caption Style Configuration ---
# Defines the visual soul of our dynamic captions.
CAPTION_STYLE = {
    "font": "Montserrat-ExtraBold.ttf",  # A default font. Place your .ttf in assets/fonts/
    "fontsize": 72,
    "color": "white",
    "stroke_color": "black",
    "stroke_width": 3,
    "highlight_color": "#FFFF00",  # A piercing yellow for the active word.
}

# --- AI Director Style Profiles ---
# This is the editor's "brain chemistry." Each profile is a distinct creative personality.
STYLE_PROFILES = {
    "high_energy_meme": {
        "description": "Apocalyptically fast-paced. Aggressive zooms, psychotic cuts, and an onslaught of effects. Forged for memes and soul-crushing short-form content.",
        "allow_sfx": True,
        "sfx_map": {
            "glitch": "glitch.mp3",
            "whip_pan": "whoosh.mp3"
        },
        "allowed_effects": ["zoom_punch", "screen_shake"],
        "allowed_transitions": ["glitch", "whip_pan"],
        "effect_frequency": 0.6,  # 0.0 (never) to 1.0 (always on beat)
        "transition_frequency": 0.8,
        "zoom_intensity": 1.15,  # 15% zoom punch
        "shake_intensity": 10, # Pixels
        "use_hook_text": True,
        "use_progress_bar": True,
    },
    "calm_corporate": {
        "description": "Deceptively clean and ruthlessly professional. Subtle effects and smooth transitions that convey power without shouting. Forged for corporate dominance.",
        "allow_sfx": False,
        "sfx_map": {},
        "allowed_effects": [],
        "allowed_transitions": [], # A "crossfade" could be added here.
        "effect_frequency": 0.0,
        "transition_frequency": 0.1,
        "zoom_intensity": 1.05,
        "shake_intensity": 0,
        "use_hook_text": False,
        "use_progress_bar": False,
    },
}

def get_default_style():
    """Returns the name of the default style profile."""
    return "high_energy_meme"