"""
Saturation adjustment effect.
"""

from PIL import Image, ImageEnhance

from .base_effect import BaseEffect, float_parameter, register_effect


@register_effect
class SaturationEffect(BaseEffect):
    """Adjust image color saturation."""

    def __init__(self):
        super().__init__(name="saturation", display_name="Saturation", category="color")

        # Add parameters
        self.add_parameter(
            float_parameter(
                name="factor",
                display_name="Saturation",
                default=1.0,
                min_val=0.0,
                max_val=3.0,
                description="Saturation factor (0.0 = grayscale, 1.0 = normal, >1.0 = more saturated)",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for saturation effect."""
        return "saturation"

    def get_description(self) -> str:
        """Return description of saturation effect."""
        return "Adjust the color saturation of the image"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply saturation adjustment to the image."""
        factor = params.get("factor", 1.0)

        if factor == 1.0:
            return image

        if factor < 0.0:
            factor = 0.0

        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
