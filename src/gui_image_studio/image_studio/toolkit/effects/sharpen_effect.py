"""
Sharpen effect.
"""

from PIL import Image, ImageEnhance

from .base_effect import BaseEffect, float_parameter, register_effect


@register_effect
class SharpenEffect(BaseEffect):
    """Sharpen image details."""

    def __init__(self):
        super().__init__(name="sharpen", display_name="Sharpen", category="enhancement")

        # Add parameters
        self.add_parameter(
            float_parameter(
                name="factor",
                display_name="Sharpness",
                default=1.0,
                min_val=0.0,
                max_val=3.0,
                description="Sharpness factor (1.0 = no change, >1.0 = sharper, <1.0 = softer)",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for sharpen effect."""
        return "sharpen"

    def get_description(self) -> str:
        """Return description of sharpen effect."""
        return "Sharpen the image to enhance details"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply sharpening to the image."""
        factor = params.get("factor", 1.0)

        if factor == 1.0:
            return image

        if factor < 0.0:
            factor = 0.0

        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
