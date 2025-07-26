"""
Invert colors effect.
"""

from PIL import Image, ImageOps

from .base_effect import BaseEffect, register_effect


@register_effect
class InvertEffect(BaseEffect):
    """Invert image colors."""

    def __init__(self):
        super().__init__(name="invert", display_name="Invert Colors", category="color")

        # No parameters for invert
        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for invert effect."""
        return "invert"

    def get_description(self) -> str:
        """Return description of invert effect."""
        return "Invert all colors in the image (negative effect)"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Invert image colors."""
        # Handle RGBA images by preserving alpha channel
        if image.mode == "RGBA":
            alpha = image.split()[-1]
            rgb_image = image.convert("RGB")
            inverted = ImageOps.invert(rgb_image)
            inverted = inverted.convert("RGBA")
            inverted.putalpha(alpha)
            return inverted
        else:
            return ImageOps.invert(image.convert("RGB")).convert(image.mode)
