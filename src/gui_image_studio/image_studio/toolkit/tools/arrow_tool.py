"""
Arrow tool implementation.
"""

import math
from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class ArrowTool(BaseTool):
    """Arrow tool for drawing arrow shapes."""

    def __init__(self):
        super().__init__(name="arrow", display_name="Arrow", cursor="crosshair")
        self.settings = {"size": 20, "color": "#000000", "head_size": 10, "fill": False}

    def get_icon(self) -> str:
        """Return the icon name for the arrow tool."""
        return "arrow"

    def get_description(self) -> str:
        """Return description of the arrow tool."""
        return "Draw arrow shapes pointing in any direction"

    def supports_preview(self) -> bool:
        """Arrow tool supports preview."""
        return True

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - draw a default arrow pointing right."""
        size = kwargs.get("size", self.settings["size"])
        color = kwargs.get("color", "#000000")
        head_size = kwargs.get("head_size", self.settings["head_size"])
        fill = kwargs.get("fill", self.settings["fill"])

        # Draw a horizontal arrow pointing right
        self._draw_arrow(image, x - size, y, x + size, y, color, head_size, fill)

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - no action during drag for arrow tool."""
        pass

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - draw arrow from start to end point."""
        color = kwargs.get("color", "#000000")
        head_size = kwargs.get("head_size", self.settings["head_size"])
        fill = kwargs.get("fill", self.settings["fill"])

        self._draw_arrow(image, x1, y1, x2, y2, color, head_size, fill)

    def create_preview(
        self, canvas, x1: int, y1: int, x2: int, y2: int, zoom: float, **kwargs
    ) -> Optional[int]:
        """Create a preview arrow on the canvas."""
        color = kwargs.get("color", "#000000")
        head_size = kwargs.get("head_size", self.settings["head_size"])

        # Calculate arrow points for preview
        arrow_points = self._calculate_arrow_points(x1, y1, x2, y2, head_size * zoom)

        # Create preview polygon
        return canvas.create_polygon(arrow_points, outline=color, fill="", width=1)

    def _draw_arrow(
        self,
        image: Image.Image,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: str,
        head_size: int,
        fill: bool,
    ):
        """Draw an arrow shape on the image."""
        draw = ImageDraw.Draw(image)
        arrow_points = self._calculate_arrow_points(x1, y1, x2, y2, head_size)

        if fill:
            draw.polygon(arrow_points, fill=color, outline=color)
        else:
            draw.polygon(arrow_points, outline=color, fill=None)

    def _calculate_arrow_points(
        self, x1: int, y1: int, x2: int, y2: int, head_size: int
    ):
        """Calculate the points of an arrow."""
        # Calculate arrow direction
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            return [x1, y1, x1, y1, x1, y1]  # Degenerate case

        # Normalize direction
        ux = dx / length
        uy = dy / length

        # Perpendicular vector
        px = -uy
        py = ux

        # Arrow shaft width
        shaft_width = head_size * 0.3

        # Calculate arrow points
        # Start with the shaft
        shaft_x1 = x1 + px * shaft_width
        shaft_y1 = y1 + py * shaft_width
        shaft_x2 = x1 - px * shaft_width
        shaft_y2 = y1 - py * shaft_width

        # Arrow head base
        head_base_x = x2 - ux * head_size
        head_base_y = y2 - uy * head_size

        # Arrow head sides
        head_side1_x = head_base_x + px * head_size
        head_side1_y = head_base_y + py * head_size
        head_side2_x = head_base_x - px * head_size
        head_side2_y = head_base_y - py * head_size

        # Shaft to head connection
        shaft_end1_x = head_base_x + px * shaft_width
        shaft_end1_y = head_base_y + py * shaft_width
        shaft_end2_x = head_base_x - px * shaft_width
        shaft_end2_y = head_base_y - py * shaft_width

        # Return arrow points in order
        return [
            shaft_x1,
            shaft_y1,  # Shaft start top
            shaft_end1_x,
            shaft_end1_y,  # Shaft end top
            head_side1_x,
            head_side1_y,  # Head side 1
            x2,
            y2,  # Arrow tip
            head_side2_x,
            head_side2_y,  # Head side 2
            shaft_end2_x,
            shaft_end2_y,  # Shaft end bottom
            shaft_x2,
            shaft_y2,  # Shaft start bottom
        ]

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "size": {
                "type": "slider",
                "label": "Arrow Length",
                "min": 10,
                "max": 100,
                "default": 20,
            },
            "head_size": {
                "type": "slider",
                "label": "Arrow Head Size",
                "min": 5,
                "max": 30,
                "default": 10,
            },
            "fill": {
                "type": "checkbox",
                "label": "Fill Arrow",
                "default": False,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate arrow settings."""
        validated = {}
        validated["size"] = max(10, min(100, settings.get("size", 20)))
        validated["color"] = settings.get("color", "#000000")
        validated["head_size"] = max(5, min(30, settings.get("head_size", 10)))
        validated["fill"] = settings.get("fill", False)
        return validated


# Tool instance is automatically registered via decorator
arrow_tool = ArrowTool()
