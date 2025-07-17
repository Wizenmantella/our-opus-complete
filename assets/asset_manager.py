# assets/asset_manager.py
import os

class AssetManager:
    """Manages access to creative assets like fonts, sfx, and overlays."""
    
    def __init__(self, base_path="assets"):
        self.base_path = base_path
        self.fonts_path = os.path.join(base_path, "fonts")
        self.sfx_path = os.path.join(base_path, "sfx")
        self.overlays_path = os.path.join(base_path, "overlays")
        self._validate_paths()

    def _validate_paths(self):
        """Ensure all asset directories exist."""
        os.makedirs(self.fonts_path, exist_ok=True)
        os.makedirs(self.sfx_path, exist_ok=True)
        os.makedirs(self.overlays_path, exist_ok=True)

    def get_font(self, font_name: str) -> str:
        """Returns the full path to a font file."""
        path = os.path.join(self.fonts_path, font_name)
        if not os.path.exists(path):
            print(f"Warning: Font '{font_name}' not found at '{path}'. Using default.")
            # In a real app, you might have a guaranteed default font.
            return "Arial"  # Default fallback
        return path

    def get_sfx(self, sfx_name: str) -> str:
        """Returns the full path to a sound effect file."""
        path = os.path.join(self.sfx_path, sfx_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sound effect '{sfx_name}' not found at '{path}'.")
        return path

    def get_overlay(self, overlay_name: str) -> str:
        """Returns the full path to an overlay file."""
        path = os.path.join(self.overlays_path, overlay_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Overlay '{overlay_name}' not found at '{path}'.")
        return path

    def list_fonts(self) -> list:
        """Returns a list of available font files."""
        if not os.path.exists(self.fonts_path):
            return []
        return [f for f in os.listdir(self.fonts_path) if f.endswith(('.ttf', '.otf'))]

    def list_sfx(self) -> list:
        """Returns a list of available sound effect files."""
        if not os.path.exists(self.sfx_path):
            return []
        return [f for f in os.listdir(self.sfx_path) if f.endswith(('.mp3', '.wav', '.ogg'))]

    def list_overlays(self) -> list:
        """Returns a list of available overlay files."""
        if not os.path.exists(self.overlays_path):
            return []
        return [f for f in os.listdir(self.overlays_path) if f.endswith(('.mp4', '.mov', '.png', '.gif'))]