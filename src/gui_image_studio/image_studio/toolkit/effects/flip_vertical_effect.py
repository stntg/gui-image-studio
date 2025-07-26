"""
Flip vertical effect.
"""

from PIL import Image

from .base_effect import BaseEffect, register_effect


@register_effect
class FlipVerticalEffect(BaseEffect):
    """Flip image vertically."""

    def __init__(self):
        super().__init__(
            name="flip_vertical", display_name="Flip Vertical", category="geometry"
        )

        # No parameters for flip
        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for flip vertical effect."""
        return "flip_vertical"

    def get_description(self) -> str:
        """Return description of flip vertical effect."""
        return "Flip the image vertically (upside down)"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Flip image vertically."""
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
