"""
Fill tool implementation.
"""

from typing import Any, Dict, Optional

from PIL import Image, ImageDraw

from .base_tool import BaseTool, register_tool


@register_tool
class FillTool(BaseTool):
    """Fill tool for flood filling areas with color."""

    def __init__(self):
        super().__init__(name="fill", display_name="Fill", cursor="spraycan")
        self.settings = {
            "color": "#000000",
            "tolerance": 0,  # Color tolerance for fill
            "contiguous": True,  # Only fill connected pixels
        }

    def get_icon(self) -> str:
        """Return the icon name for the fill tool."""
        return "fill"

    def get_description(self) -> str:
        """Return description of the fill tool."""
        return "Fill an area with color using flood fill algorithm"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - perform flood fill."""
        color = kwargs.get("color", self.settings["color"])
        tolerance = kwargs.get("tolerance", self.settings["tolerance"])
        contiguous = kwargs.get("contiguous", self.settings["contiguous"])

        # Convert hex color to RGB tuple
        try:
            if color.startswith("#"):
                hex_color = color[1:]
                rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
                rgba_color = rgb_color + (255,)  # Add alpha
            else:
                rgba_color = color
        except (ValueError, IndexError):
            rgba_color = (0, 0, 0, 255)  # Default to black

        # Perform flood fill
        try:
            if contiguous:
                # Standard flood fill with tolerance
                # Convert tolerance from 0-100 scale to 0-255 scale for PIL
                thresh = int((tolerance / 100.0) * 255)
                ImageDraw.floodfill(image, (x, y), rgba_color, thresh=thresh)
            else:
                # Non-contiguous fill: replace all pixels of the same color
                self._non_contiguous_fill(image, x, y, rgba_color, tolerance)
        except Exception as e:
            # Handle flood fill errors (e.g., clicking outside image bounds)
            print(f"Flood fill error: {e}")

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - no action for fill tool."""
        pass

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - no action for fill tool."""
        pass

    def _non_contiguous_fill(
        self, image: Image.Image, x: int, y: int, fill_color: tuple, tolerance: int
    ) -> None:
        """Fill all pixels of similar color throughout the image (non-contiguous)."""
        # Get the target color at the clicked position
        try:
            target_color = image.getpixel((x, y))
            if isinstance(target_color, int):
                # Grayscale image
                target_color = (target_color, target_color, target_color, 255)
            elif len(target_color) == 3:
                # RGB image, add alpha
                target_color = target_color + (255,)
            elif len(target_color) == 4:
                # RGBA image
                pass
            else:
                return  # Unsupported format
        except IndexError:
            # Click outside image bounds
            return

        # Convert tolerance from 0-100 scale to actual color difference
        tolerance_value = int((tolerance / 100.0) * 255)

        # Get image data
        width, height = image.size
        pixels = image.load()

        # Replace all similar pixels
        for py in range(height):
            for px in range(width):
                current_pixel = pixels[px, py]

                # Ensure current pixel is in RGBA format
                if isinstance(current_pixel, int):
                    current_pixel = (current_pixel, current_pixel, current_pixel, 255)
                elif len(current_pixel) == 3:
                    current_pixel = current_pixel + (255,)

                # Calculate color difference (Euclidean distance in RGB space)
                if self._color_similar(current_pixel, target_color, tolerance_value):
                    pixels[px, py] = fill_color

    def _color_similar(self, color1: tuple, color2: tuple, tolerance: int) -> bool:
        """Check if two colors are similar within tolerance."""
        # Calculate Euclidean distance in RGB space (ignore alpha for comparison)
        r_diff = abs(color1[0] - color2[0])
        g_diff = abs(color1[1] - color2[1])
        b_diff = abs(color1[2] - color2[2])

        # Use maximum difference in any channel (simpler than Euclidean distance)
        max_diff = max(r_diff, g_diff, b_diff)
        return max_diff <= tolerance

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "tolerance": {
                "type": "slider",
                "label": "Color Tolerance",
                "min": 0,
                "max": 100,
                "default": 0,
            },
            "contiguous": {
                "type": "checkbox",
                "label": "Contiguous Fill",
                "default": True,
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate fill settings."""
        validated = {}
        validated["color"] = settings.get("color", "#000000")
        validated["tolerance"] = max(0, min(100, settings.get("tolerance", 0)))
        validated["contiguous"] = settings.get("contiguous", True)
        return validated

    def get_cursor_for_size(self, size: int) -> str:
        """Return fill cursor (always spraycan)."""
        return "spraycan"


# Tool instance is automatically registered via decorator
fill_tool = FillTool()
