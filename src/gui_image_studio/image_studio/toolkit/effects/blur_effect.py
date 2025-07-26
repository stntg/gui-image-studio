"""
Blur effect.
"""

from PIL import Image, ImageFilter

from .base_effect import BaseEffect, float_parameter, register_effect


@register_effect
class BlurEffect(BaseEffect):
    """Apply blur to image."""

    def __init__(self):
        super().__init__(name="blur", display_name="Blur", category="filter")

        # Add parameters
        self.add_parameter(
            float_parameter(
                name="radius",
                display_name="Blur Radius",
                default=2.0,
                min_val=0.0,
                max_val=20.0,
                description="Blur radius (higher values = more blur)",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for blur effect."""
        return "blur"

    def get_description(self) -> str:
        """Return description of blur effect."""
        return "Apply Gaussian blur to the image"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply blur to the image."""
        radius = params.get("radius", 2.0)

        if radius <= 0.0:
            return image

        return image.filter(ImageFilter.GaussianBlur(radius=radius))
