"""
Fill tool implementation.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class FillTool(BaseTool):
    """Fill tool for flood filling areas with color."""

    def __init__(self):
        super().__init__(name="fill", display_name="Fill", cursor="spraycan")
        self.settings = {
            "color": "#000000",
            "tolerance": 0,  # Color tolerance for fill
            "contiguous": True,  # Only fill connected pixels
        }

    def get_icon(self) -> str:
        """Return the icon name for the fill tool."""
        return "fill"

    def get_description(self) -> str:
        """Return description of the fill tool."""
        return "Fill an area with color using flood fill algorithm"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - perform flood fill."""
        color = kwargs.get("color", "#000000")  # Use passed color or default black
        tolerance = kwargs.get("tolerance", self.settings["tolerance"])

        # Convert hex color to RGB tuple
        try:
            if color.startswith("#"):
                hex_color = color[1:]
                rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
                rgba_color = rgb_color + (255,)  # Add alpha
            else:
                rgba_color = color
        except (ValueError, IndexError):
            rgba_color = (0, 0, 0, 255)  # Default to black

        # Perform flood fill
        try:
            if tolerance > 0:
                # TODO: Implement tolerance-based flood fill
                # For now, use simple flood fill
                ImageDraw.floodfill(image, (x, y), rgba_color)
            else:
                ImageDraw.floodfill(image, (x, y), rgba_color)
        except Exception as e:
            # Handle flood fill errors (e.g., clicking outside image bounds)
            print(f"Flood fill error: {e}")

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - no action for fill tool."""
        pass

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - no action for fill tool."""
        pass

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "tolerance": {
                "type": "slider",
                "label": "Color Tolerance",
                "min": 0,
                "max": 100,
                "default": 0,
            },
            "contiguous": {
                "type": "checkbox",
                "label": "Contiguous Fill",
                "default": True,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate fill settings."""
        validated = {}
        validated["color"] = settings.get("color", "#000000")
        validated["tolerance"] = max(0, min(100, settings.get("tolerance", 0)))
        validated["contiguous"] = settings.get("contiguous", True)
        return validated

    def get_cursor_for_size(self, size: int) -> str:
        """Return fill cursor (always spraycan)."""
        return "spraycan"


# Tool instance is automatically registered via decorator
fill_tool = FillTool()
