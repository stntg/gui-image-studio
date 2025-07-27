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
        style = kwargs.get("style", self.settings["style"])

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

        # Draw the line based on style
        if style == "solid":
            draw.line([x1, y1, x2, y2], fill=rgba_color, width=width)
        else:
            self._draw_styled_line(draw, x1, y1, x2, y2, rgba_color, width, style)

    def _draw_styled_line(self, draw, x1, y1, x2, y2, color, width, style):
        """Draw a dashed or dotted line."""
        import math

        # Calculate line length and direction
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            return

        # Normalize direction vector
        unit_x = dx / length
        unit_y = dy / length

        # Define dash patterns
        if style == "dashed":
            dash_length = max(8, width * 2)
            gap_length = max(4, width)
        elif style == "dotted":
            dash_length = max(2, width // 2 + 1)
            gap_length = max(3, width)
        else:
            return

        # Draw dashes/dots along the line
        current_pos = 0
        drawing = True

        while current_pos < length:
            if drawing:
                # Calculate start and end of current dash/dot
                start_pos = current_pos
                end_pos = min(current_pos + dash_length, length)

                # Calculate actual coordinates
                start_x = x1 + start_pos * unit_x
                start_y = y1 + start_pos * unit_y
                end_x = x1 + end_pos * unit_x
                end_y = y1 + end_pos * unit_y

                if style == "dotted" and dash_length <= 2:
                    # Draw dots as small circles for very small dash lengths
                    dot_radius = max(1, width // 2)
                    draw.ellipse(
                        [
                            start_x - dot_radius,
                            start_y - dot_radius,
                            start_x + dot_radius,
                            start_y + dot_radius,
                        ],
                        fill=color,
                    )
                else:
                    # Draw line segment
                    draw.line([start_x, start_y, end_x, end_y], fill=color, width=width)

                current_pos += dash_length
            else:
                # Skip gap
                current_pos += gap_length

            drawing = not drawing

    def supports_preview(self) -> bool:
        """Line tool supports preview."""
        return True

    def create_preview(
        self, canvas, x1: int, y1: int, x2: int, y2: int, zoom: float, **kwargs
    ) -> Optional[int]:
        """Create a preview line on the canvas."""
        color = kwargs.get("color", "#000000")  # Use passed color or default black
        width = kwargs.get("width", self.settings["width"])
        style = kwargs.get("style", self.settings["style"])

        # Convert image coordinates to canvas coordinates
        canvas_x1 = x1 * zoom + 10
        canvas_y1 = y1 * zoom + 10
        canvas_x2 = x2 * zoom + 10
        canvas_y2 = y2 * zoom + 10

        # Determine dash pattern based on style
        dash_pattern = None
        if style == "dashed":
            dash_pattern = (8, 4)
        elif style == "dotted":
            dash_pattern = (2, 3)

        # Create preview line
        return canvas.create_line(
            canvas_x1,
            canvas_y1,
            canvas_x2,
            canvas_y2,
            fill=color,
            width=max(1, int(width * zoom)),
            dash=dash_pattern,
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
