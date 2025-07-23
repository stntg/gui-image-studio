"""
Brush tool implementation.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class BrushTool(BaseTool):
    """Brush tool for freehand drawing with variable size."""

    def __init__(self):
        super().__init__(name="brush", display_name="Brush", cursor="crosshair")
        self.settings = {"size": 5, "color": "#000000", "opacity": 255}

    def get_icon(self) -> str:
        """Return the icon name for the brush tool."""
        return "brush"

    def get_description(self) -> str:
        """Return description of the brush tool."""
        return "Draw freehand with a circular brush of variable size"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - draw a circle."""
        draw = ImageDraw.Draw(image)
        size = kwargs.get("size", self.settings["size"])
        color = kwargs.get("color", "#000000")  # Use passed color or default black

        # Draw circle at click position
        draw.ellipse(
            [x - size // 2, y - size // 2, x + size // 2, y + size // 2], fill=color
        )

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - draw line between points."""
        draw = ImageDraw.Draw(image)
        size = kwargs.get("size", self.settings["size"])
        color = kwargs.get("color", "#000000")  # Use passed color or default black

        # Draw line between drag points
        draw.line([x1, y1, x2, y2], fill=color, width=size)

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - no special action for brush."""
        pass

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "size": {
                "type": "slider",
                "label": "Brush Size",
                "min": 1,
                "max": 50,
                "default": 5,
            },
            "opacity": {
                "type": "slider",
                "label": "Opacity",
                "min": 1,
                "max": 255,
                "default": 255,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate brush settings."""
        validated = {}
        validated["size"] = max(1, min(50, settings.get("size", 5)))
        validated["color"] = settings.get("color", "#000000")
        validated["opacity"] = max(1, min(255, settings.get("opacity", 255)))
        return validated

    def get_cursor_for_size(self, size: int) -> str:
        """Return appropriate cursor for brush size."""
        if size <= 3:
            return "crosshair"
        elif size <= 10:
            return "dotbox"
        else:
            return "circle"


# Tool instance is automatically registered via decorator
brush_tool = BrushTool()
