"""
Diamond tool implementation.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class DiamondTool(BaseTool):
    """Diamond tool for drawing diamond shapes."""

    def __init__(self):
        super().__init__(name="diamond", display_name="Diamond", cursor="crosshair")
        self.settings = {"size": 20, "color": "#000000", "fill": False, "rotation": 0}

    def get_icon(self) -> str:
        """Return the icon name for the diamond tool."""
        return "diamond"

    def get_description(self) -> str:
        """Return description of the diamond tool."""
        return "Draw diamond shapes with optional rotation"

    def supports_preview(self) -> bool:
        """Diamond tool supports preview."""
        return True

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - draw a diamond at the clicked position."""
        size = kwargs.get("size", self.settings["size"])
        color = kwargs.get("color", "#000000")
        fill = kwargs.get("fill", self.settings["fill"])
        rotation = kwargs.get("rotation", self.settings["rotation"])

        self._draw_diamond(image, x, y, size, size, color, fill, rotation)

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - no action during drag for diamond tool."""
        pass

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - draw diamond based on drag area."""
        color = kwargs.get("color", "#000000")
        fill = kwargs.get("fill", self.settings["fill"])
        rotation = kwargs.get("rotation", self.settings["rotation"])

        # Calculate diamond dimensions from drag area
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        self._draw_diamond(
            image, center_x, center_y, width, height, color, fill, rotation
        )

    def create_preview(
        self, canvas, x1: int, y1: int, x2: int, y2: int, zoom: float, **kwargs
    ) -> Optional[int]:
        """Create a preview diamond on the canvas."""
        color = kwargs.get("color", "#000000")
        rotation = kwargs.get("rotation", self.settings["rotation"])

        # Calculate diamond dimensions
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Calculate diamond points for preview
        diamond_points = self._calculate_diamond_points(
            center_x, center_y, width, height, rotation
        )

        # Create preview polygon
        return canvas.create_polygon(diamond_points, outline=color, fill="", width=1)

    def _draw_diamond(
        self,
        image: Image.Image,
        center_x: int,
        center_y: int,
        width: int,
        height: int,
        color: str,
        fill: bool,
        rotation: int,
    ):
        """Draw a diamond shape on the image."""
        draw = ImageDraw.Draw(image)
        diamond_points = self._calculate_diamond_points(
            center_x, center_y, width, height, rotation
        )

        if fill:
            draw.polygon(diamond_points, fill=color, outline=color)
        else:
            draw.polygon(diamond_points, outline=color, fill=None)

    def _calculate_diamond_points(
        self, center_x: int, center_y: int, width: int, height: int, rotation: int
    ):
        """Calculate the points of a diamond."""
        import math

        # Basic diamond points (before rotation)
        half_width = width // 2
        half_height = height // 2

        points = [
            (center_x, center_y - half_height),  # Top
            (center_x + half_width, center_y),  # Right
            (center_x, center_y + half_height),  # Bottom
            (center_x - half_width, center_y),  # Left
        ]

        # Apply rotation if specified
        if rotation != 0:
            angle = math.radians(rotation)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            rotated_points = []
            for px, py in points:
                # Translate to origin
                tx = px - center_x
                ty = py - center_y

                # Rotate
                rx = tx * cos_a - ty * sin_a
                ry = tx * sin_a + ty * cos_a

                # Translate back
                rotated_points.extend([center_x + rx, center_y + ry])

            return rotated_points
        else:
            # Flatten the points list
            flat_points = []
            for px, py in points:
                flat_points.extend([px, py])
            return flat_points

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "size": {
                "type": "slider",
                "label": "Diamond Size",
                "min": 10,
                "max": 100,
                "default": 20,
            },
            "rotation": {
                "type": "slider",
                "label": "Rotation (degrees)",
                "min": 0,
                "max": 360,
                "default": 0,
            },
            "fill": {
                "type": "checkbox",
                "label": "Fill Diamond",
                "default": False,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate diamond settings."""
        validated = {}
        validated["size"] = max(10, min(100, settings.get("size", 20)))
        validated["color"] = settings.get("color", "#000000")
        validated["rotation"] = max(0, min(360, settings.get("rotation", 0)))
        validated["fill"] = settings.get("fill", False)
        return validated


# Tool instance is automatically registered via decorator
diamond_tool = DiamondTool()
