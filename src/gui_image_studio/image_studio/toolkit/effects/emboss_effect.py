"""
Emboss effect.
"""

from PIL import Image, ImageFilter

from .base_effect import BaseEffect, register_effect


@register_effect
class EmbossEffect(BaseEffect):
    """Apply emboss filter for 3D effect."""

    def __init__(self):
        super().__init__(name="emboss", display_name="Emboss", category="filter")

        # No parameters for emboss
        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for emboss effect."""
        return "emboss"

    def get_description(self) -> str:
        """Return description of emboss effect."""
        return "Apply an emboss filter to create a 3D raised effect"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply emboss effect to the image."""
        return image.filter(ImageFilter.EMBOSS)
