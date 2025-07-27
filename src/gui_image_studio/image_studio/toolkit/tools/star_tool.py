"""
Star tool implementation.
"""

import math
from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class StarTool(BaseTool):
    """Star tool for drawing star shapes."""

    def __init__(self):
        super().__init__(name="star", display_name="Star", cursor="crosshair")
        self.settings = {"size": 20, "color": "#000000", "points": 5, "fill": False}

    def get_icon(self) -> str:
        """Return the icon name for the star tool."""
        return "star"

    def get_description(self) -> str:
        """Return description of the star tool."""
        return "Draw star shapes with customizable number of points"

    def supports_preview(self) -> bool:
        """Star tool supports preview."""
        return True

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - draw a star at the clicked position."""
        size = kwargs.get("size", self.settings["size"])
        color = kwargs.get("color", "#000000")
        points = kwargs.get("points", self.settings["points"])
        fill = kwargs.get("fill", self.settings["fill"])

        self._draw_star(image, x, y, size, color, points, fill)

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - no action during drag for star tool."""
        pass

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - draw star based on drag distance."""
        # Calculate size based on drag distance
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        size = max(10, int(distance))

        color = kwargs.get("color", "#000000")
        points = kwargs.get("points", self.settings["points"])
        fill = kwargs.get("fill", self.settings["fill"])

        # Draw star at the center of the drag
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        self._draw_star(image, center_x, center_y, size, color, points, fill)

    def create_preview(
        self, canvas, x1: int, y1: int, x2: int, y2: int, zoom: float, **kwargs
    ) -> Optional[int]:
        """Create a preview star on the canvas."""
        # Calculate size based on drag distance
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        size = max(10, int(distance / zoom))

        color = kwargs.get("color", "#000000")
        points = kwargs.get("points", self.settings["points"])

        # Calculate star points for preview
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        star_points = self._calculate_star_points(
            center_x, center_y, size * zoom, points
        )

        # Create preview polygon
        return canvas.create_polygon(star_points, outline=color, fill="", width=1)

    def _draw_star(
        self,
        image: Image.Image,
        x: int,
        y: int,
        size: int,
        color: str,
        points: int,
        fill: bool,
    ):
        """Draw a star shape on the image."""
        draw = ImageDraw.Draw(image)
        star_points = self._calculate_star_points(x, y, size, points)

        if fill:
            draw.polygon(star_points, fill=color, outline=color)
        else:
            draw.polygon(star_points, outline=color, fill=None)

    def _calculate_star_points(
        self, center_x: int, center_y: int, size: int, points: int
    ):
        """Calculate the points of a star."""
        star_points = []
        outer_radius = size
        inner_radius = size * 0.4  # Inner radius is 40% of outer radius

        for i in range(points * 2):
            angle = (i * math.pi) / points - math.pi / 2  # Start from top
            if i % 2 == 0:  # Outer point
                radius = outer_radius
            else:  # Inner point
                radius = inner_radius

            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            star_points.extend([x, y])

        return star_points

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "size": {
                "type": "slider",
                "label": "Star Size",
                "min": 10,
                "max": 100,
                "default": 20,
            },
            "points": {
                "type": "slider",
                "label": "Number of Points",
                "min": 3,
                "max": 12,
                "default": 5,
            },
            "fill": {
                "type": "checkbox",
                "label": "Fill Star",
                "default": False,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate star settings."""
        validated = {}
        validated["size"] = max(10, min(100, settings.get("size", 20)))
        validated["color"] = settings.get("color", "#000000")
        validated["points"] = max(3, min(12, settings.get("points", 5)))
        validated["fill"] = settings.get("fill", False)
        return validated


# Tool instance is automatically registered via decorator
star_tool = StarTool()
