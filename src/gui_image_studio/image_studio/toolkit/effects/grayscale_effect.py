"""
Grayscale effect.
"""

from PIL import Image, ImageOps

from .base_effect import BaseEffect, register_effect


@register_effect
class GrayscaleEffect(BaseEffect):
    """Convert image to grayscale."""

    def __init__(self):
        super().__init__(name="grayscale", display_name="Grayscale", category="color")

        # No parameters for grayscale
        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for grayscale effect."""
        return "grayscale"

    def get_description(self) -> str:
        """Return description of grayscale effect."""
        return "Convert the image to grayscale (black and white)"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Convert image to grayscale."""
        return ImageOps.grayscale(image).convert("RGBA")
