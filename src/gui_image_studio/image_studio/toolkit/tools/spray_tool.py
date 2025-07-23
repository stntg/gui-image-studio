"""
Spray paint tool implementation - example of adding a new tool.
"""

import random
from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class SprayTool(BaseTool):
    """Spray paint tool for creating spray paint effects."""

    def __init__(self):
        super().__init__(name="spray", display_name="Spray Paint", cursor="spraycan")
        self.settings = {
            "size": 20,
            "color": "#000000",
            "density": 50,  # Spray density (1-100)
            "pressure": 75,  # Spray pressure affects spread
        }

    def get_icon(self) -> str:
        """Return the icon name for the spray tool."""
        return "spray"

    def get_description(self) -> str:
        """Return description of the spray tool."""
        return "Create spray paint effects with adjustable density and pressure"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - create spray effect."""
        self._spray_paint(image, x, y, **kwargs)

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - create spray effect along drag path."""
        # Create spray effect at multiple points along the drag path
        steps = max(1, int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) // 5)
        for i in range(steps + 1):
            t = i / max(1, steps)
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            self._spray_paint(image, x, y, **kwargs)

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - no special action for spray."""
        pass

    def _spray_paint(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Create spray paint effect at given position."""
        draw = ImageDraw.Draw(image)
        size = kwargs.get("size", self.settings["size"])
        color = kwargs.get("color", "#000000")  # Use passed color or default black
        density = kwargs.get("density", self.settings["density"])
        pressure = kwargs.get("pressure", self.settings["pressure"])

        # Convert hex color to RGB
        try:
            if color.startswith("#"):
                hex_color = color[1:]
                rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
            else:
                rgb_color = color
        except (ValueError, IndexError):
            rgb_color = (0, 0, 0)  # Default to black

        # Calculate number of spray dots based on density
        num_dots = int((density / 100) * (size**2) / 10)

        # Calculate spray radius based on size and pressure
        spray_radius = (size * pressure) / 100

        # Create spray effect
        for _ in range(num_dots):
            # Random position within spray radius
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(0, spray_radius)

            dot_x = int(x + distance * random.uniform(-1, 1)) # nosec B311
            dot_y = int(y + distance * random.uniform(-1, 1)) # nosec B311

            # Vary dot size slightly
            dot_size = random.randint(1, max(1, size // 10))

            # Draw spray dot
            try:
                if dot_size == 1:
                    draw.point((dot_x, dot_y), fill=rgb_color)
                else:
                    draw.ellipse(
                        [
                            dot_x - dot_size // 2,
                            dot_y - dot_size // 2,
                            dot_x + dot_size // 2,
                            dot_y + dot_size // 2,
                        ],
                        fill=rgb_color,
                    )
            except (ValueError, IndexError):
                # Skip dots that are outside image bounds
                pass

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "size": {
                "type": "slider",
                "label": "Spray Size",
                "min": 5,
                "max": 100,
                "default": 20,
            },
            "density": {
                "type": "slider",
                "label": "Spray Density",
                "min": 1,
                "max": 100,
                "default": 50,
            },
            "pressure": {
                "type": "slider",
                "label": "Spray Pressure",
                "min": 10,
                "max": 100,
                "default": 75,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate spray settings."""
        validated = {}
        validated["size"] = max(5, min(100, settings.get("size", 20)))
        validated["color"] = settings.get("color", "#000000")
        validated["density"] = max(1, min(100, settings.get("density", 50)))
        validated["pressure"] = max(10, min(100, settings.get("pressure", 75)))
        return validated

    def get_cursor_for_size(self, size: int) -> str:
        """Return spray cursor."""
        return "spraycan"


# Tool instance is automatically registered via decorator
spray_tool = SprayTool()
