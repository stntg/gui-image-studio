"""
Rectangle tool implementation.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class RectangleTool(BaseTool):
    """Rectangle tool for drawing rectangles and squares."""

    def __init__(self):
        super().__init__(name="rectangle", display_name="Rectangle", cursor="crosshair")
        self.settings = {
            "width": 2,
            "color": "#000000",
            "fill": False,
            "fill_color": "#FFFFFF",
        }

    def get_icon(self) -> str:
        """Return the icon name for the rectangle tool."""
        return "rectangle"

    def get_description(self) -> str:
        """Return description of the rectangle tool."""
        return "Draw rectangles and squares by dragging from corner to corner"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - start rectangle (no action until release)."""
        pass

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - no action during drag (preview handles this)."""
        pass

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - draw the final rectangle."""
        draw = ImageDraw.Draw(image)
        width = kwargs.get("width", self.settings["width"])
        color = kwargs.get("color", "#000000")  # Use passed color or default black
        fill = kwargs.get("fill", self.settings["fill"])
        fill_color = kwargs.get("fill_color", self.settings["fill_color"])

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

        # Ensure proper rectangle coordinates
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)

        # Ensure rectangle has some size
        if right > left and bottom > top:
            if fill:
                # Convert fill color
                try:
                    if fill_color.startswith("#"):
                        hex_fill = fill_color[1:]
                        rgba_fill = tuple(
                            int(hex_fill[i : i + 2], 16) for i in (0, 2, 4)
                        )
                        rgba_fill = rgba_fill + (255,)
                    else:
                        rgba_fill = fill_color
                except (ValueError, IndexError):
                    rgba_fill = (255, 255, 255, 255)  # Default to white

                # Draw filled rectangle
                draw.rectangle(
                    [left, top, right, bottom],
                    fill=rgba_fill,
                    outline=rgba_color,
                    width=width,
                )
            else:
                # Draw outline only
                draw.rectangle(
                    [left, top, right, bottom], outline=rgba_color, width=width
                )

    def supports_preview(self) -> bool:
        """Rectangle tool supports preview."""
        return True

    def create_preview(
        self, canvas, x1: int, y1: int, x2: int, y2: int, zoom: float, **kwargs
    ) -> Optional[int]:
        """Create a preview rectangle on the canvas."""
        color = kwargs.get("color", "#000000")  # Use passed color or default black

        # Convert image coordinates to canvas coordinates
        canvas_x1 = x1 * zoom + 10
        canvas_y1 = y1 * zoom + 10
        canvas_x2 = x2 * zoom + 10
        canvas_y2 = y2 * zoom + 10

        # Create preview rectangle
        return canvas.create_rectangle(
            canvas_x1,
            canvas_y1,
            canvas_x2,
            canvas_y2,
            outline=color,
            width=2,
            fill="",
            dash=(5, 5),
            tags="preview",
        )

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "width": {
                "type": "slider",
                "label": "Border Width",
                "min": 1,
                "max": 20,
                "default": 2,
            },
            "fill": {"type": "checkbox", "label": "Fill Rectangle", "default": False},
            "fill_color": {
                "type": "color",
                "label": "Fill Color",
                "default": "#FFFFFF",
                "depends_on": "fill",
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate rectangle settings."""
        validated = {}
        validated["width"] = max(1, min(20, settings.get("width", 2)))
        validated["color"] = settings.get("color", "#000000")
        validated["fill"] = settings.get("fill", False)
        validated["fill_color"] = settings.get("fill_color", "#FFFFFF")
        return validated


# Tool instance is automatically registered via decorator
rectangle_tool = RectangleTool()
