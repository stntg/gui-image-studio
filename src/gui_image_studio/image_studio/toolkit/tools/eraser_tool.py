"""
Eraser tool implementation.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class EraserTool(BaseTool):
    """Eraser tool for removing parts of the image."""

    def __init__(self):
        super().__init__(name="eraser", display_name="Eraser", cursor="dotbox")
        self.settings = {
            "size": 10,
            "hardness": 100,  # 100 = hard edge, lower = soft edge
        }

    def get_icon(self) -> str:
        """Return the icon name for the eraser tool."""
        return "eraser"

    def get_description(self) -> str:
        """Return description of the eraser tool."""
        return "Erase parts of the image with a circular eraser"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - erase a circle."""
        draw = ImageDraw.Draw(image)
        size = kwargs.get("size", self.settings["size"])

        # Erase (draw transparent)
        draw.ellipse(
            [x - size // 2, y - size // 2, x + size // 2, y + size // 2],
            fill=(0, 0, 0, 0),  # Transparent
        )

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - erase line between points."""
        draw = ImageDraw.Draw(image)
        size = kwargs.get("size", self.settings["size"])

        # Erase line between drag points
        draw.line([x1, y1, x2, y2], fill=(0, 0, 0, 0), width=size)

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - no special action for eraser."""
        pass

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "size": {
                "type": "slider",
                "label": "Eraser Size",
                "min": 1,
                "max": 100,
                "default": 10,
            },
            "hardness": {
                "type": "slider",
                "label": "Hardness",
                "min": 1,
                "max": 100,
                "default": 100,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate eraser settings."""
        validated = {}
        validated["size"] = max(1, min(100, settings.get("size", 10)))
        validated["hardness"] = max(1, min(100, settings.get("hardness", 100)))
        return validated

    def get_cursor_for_size(self, size: int) -> str:
        """Return appropriate cursor for eraser size."""
        if size <= 5:
            return "dotbox"
        elif size <= 20:
            return "circle"
        else:
            return "sizing"


# Tool instance is automatically registered via decorator
eraser_tool = EraserTool()
