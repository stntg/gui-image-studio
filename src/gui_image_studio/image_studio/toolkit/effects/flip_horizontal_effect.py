"""
Flip horizontal effect.
"""

from PIL import Image

from .base_effect import BaseEffect, register_effect


@register_effect
class FlipHorizontalEffect(BaseEffect):
    """Flip image horizontally (mirror)."""

    def __init__(self):
        super().__init__(
            name="flip_horizontal", display_name="Flip Horizontal", category="geometry"
        )

        # No parameters for flip
        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for flip horizontal effect."""
        return "flip_horizontal"

    def get_description(self) -> str:
        """Return description of flip horizontal effect."""
        return "Flip the image horizontally (mirror effect)"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Flip image horizontally."""
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
