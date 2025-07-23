"""
Line tool implementation.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class LineTool(BaseTool):
    """Line tool for drawing straight lines."""

    def __init__(self):
        super().__init__(name="line", display_name="Line", cursor="crosshair")
        self.settings = {
            "width": 2,
            "color": "#000000",
            "style": "solid",  # solid, dashed, dotted
        }

    def get_icon(self) -> str:
        """Return the icon name for the line tool."""
        return "line"

    def get_description(self) -> str:
        """Return description of the line tool."""
        return "Draw straight lines between two points"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - start line (no action until release)."""
        pass

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - no action during drag (preview handles this)."""
        pass

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - draw the final line."""
        draw = ImageDraw.Draw(image)
        width = kwargs.get("width", self.settings["width"])
        color = kwargs.get("color", "#000000")  # Use passed color or default black

        # Convert hex color to RGBA tuple for PIL
        try:
            if color.startswith("#"):
                hex_color = color[1:]
                rgba_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
                rgba_color = rgba_color + (255,)  # Add alpha channel
            else:
                rgba_color = color
        except (ValueError, IndexError):
            rgba_color = (0, 0, 0, 255)  # Default to black

        # Draw the line
        draw.line([x1, y1, x2, y2], fill=rgba_color, width=width)

    def supports_preview(self) -> bool:
        """Line tool supports preview."""
        return True

    def create_preview(
        self, canvas, x1: int, y1: int, x2: int, y2: int, zoom: float, **kwargs
    ) -> Optional[int]:
        """Create a preview line on the canvas."""
        color = kwargs.get("color", "#000000")  # Use passed color or default black

        # Convert image coordinates to canvas coordinates
        canvas_x1 = x1 * zoom + 10
        canvas_y1 = y1 * zoom + 10
        canvas_x2 = x2 * zoom + 10
        canvas_y2 = y2 * zoom + 10

        # Create preview line
        return canvas.create_line(
            canvas_x1,
            canvas_y1,
            canvas_x2,
            canvas_y2,
            fill=color,
            width=2,
            dash=(5, 5),
            tags="preview",
        )

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "width": {
                "type": "slider",
                "label": "Line Width",
                "min": 1,
                "max": 20,
                "default": 2,
            },
            "style": {
                "type": "dropdown",
                "label": "Line Style",
                "options": ["solid", "dashed", "dotted"],
                "default": "solid",
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate line settings."""
        validated = {}
        validated["width"] = max(1, min(20, settings.get("width", 2)))
        validated["color"] = settings.get("color", "#000000")
        validated["style"] = settings.get("style", "solid")
        if validated["style"] not in ["solid", "dashed", "dotted"]:
            validated["style"] = "solid"
        return validated


# Tool instance is automatically registered via decorator
line_tool = LineTool()
