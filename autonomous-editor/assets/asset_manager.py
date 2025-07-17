# assets/asset_manager.py
import os

class AssetManager:
    """Manages access to the creative arsenal: fonts, sfx, and overlays."""
    def __init__(self, base_path="assets"):
        self.base_path = base_path
        self.fonts_path = os.path.join(base_path, "fonts")
        self.sfx_path = os.path.join(base_path, "sfx")
        self.overlays_path = os.path.join(base_path, "overlays")
        self._validate_paths()

    def _validate_paths(self):
        """Ensure all asset directories exist, creating them if necessary."""
        os.makedirs(self.fonts_path, exist_ok=True)
        os.makedirs(self.sfx_path, exist_ok=True)
        os.makedirs(self.overlays_path, exist_ok=True)

    def get_font(self, font_name: str) -> str:
        """Returns the full path to a font file."""
        path = os.path.join(self.fonts_path, font_name)
        if not os.path.exists(path):
            print(f"Warning: Font '{font_name}' not found at '{path}'. Falling back to default.")
            return "Arial-Bold" # A safe, universal fallback.
        return path

    def get_sfx(self, sfx_name: str) -> str:
        """Returns the full path to a sound effect file."""
        path = os.path.join(self.sfx_path, sfx_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sound effect '{sfx_name}' not found at '{path}'.")
        return path