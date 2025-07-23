"""
Pencil tool implementation.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class PencilTool(BaseTool):
    """Pencil tool for precise pixel-perfect drawing."""

    def __init__(self):
        super().__init__(name="pencil", display_name="Pencil", cursor="crosshair")
        self.settings = {"size": 1, "color": "#000000", "pixel_perfect": True}

    def get_icon(self) -> str:
        """Return the icon name for the pencil tool."""
        return "pencil"

    def get_description(self) -> str:
        """Return description of the pencil tool."""
        return "Draw precise lines and pixels, perfect for pixel art"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - draw a pixel or small circle."""
        draw = ImageDraw.Draw(image)
        size = kwargs.get("size", self.settings["size"])
        color = kwargs.get("color", "#000000")  # Use passed color or default black
        show_grid = kwargs.get("show_grid", False)
        zoom_level = kwargs.get("zoom_level", 1.0)

        if show_grid and zoom_level >= 4:
            # Pixel-perfect mode - draw single pixel
            draw.point((x, y), fill=color)
        else:
            # Normal pencil mode - small circle
            pencil_size = max(1, size // 2) if size > 1 else 1
            draw.ellipse(
                [
                    x - pencil_size // 2,
                    y - pencil_size // 2,
                    x + pencil_size // 2,
                    y + pencil_size // 2,
                ],
                fill=color,
            )

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - draw thin line between points."""
        draw = ImageDraw.Draw(image)
        size = kwargs.get("size", self.settings["size"])
        color = kwargs.get("color", "#000000")  # Use passed color or default black
        show_grid = kwargs.get("show_grid", False)
        zoom_level = kwargs.get("zoom_level", 1.0)

        if show_grid and zoom_level >= 4:
            # Pixel-perfect mode - draw 1px line
            draw.line([x1, y1, x2, y2], fill=color, width=1)
        else:
            # Normal pencil mode - thin line
            pencil_size = max(1, size // 2) if size > 1 else 1
            draw.line([x1, y1, x2, y2], fill=color, width=pencil_size)

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - no special action for pencil."""
        pass

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "size": {
                "type": "slider",
                "label": "Pencil Size",
                "min": 1,
                "max": 10,
                "default": 1,
            },
            "pixel_perfect": {
                "type": "checkbox",
                "label": "Pixel Perfect Mode",
                "default": True,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate pencil settings."""
        validated = {}
        validated["size"] = max(1, min(10, settings.get("size", 1)))
        validated["color"] = settings.get("color", "#000000")
        validated["pixel_perfect"] = settings.get("pixel_perfect", True)
        return validated

    def get_cursor_for_size(self, size: int) -> str:
        """Return crosshair cursor for pencil (always precise)."""
        return "crosshair"


# Tool instance is automatically registered via decorator
pencil_tool = PencilTool()
