"""
Brightness adjustment effect.
"""

from PIL import Image, ImageEnhance

from .base_effect import BaseEffect, float_parameter, register_effect


@register_effect
class BrightnessEffect(BaseEffect):
    """Adjust image brightness."""

    def __init__(self):
        super().__init__(
            name="brightness", display_name="Brightness", category="enhancement"
        )

        # Add parameters
        self.add_parameter(
            float_parameter(
                name="factor",
                display_name="Brightness",
                default=1.0,
                min_val=0.0,
                max_val=3.0,
                description="Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for brightness effect."""
        return "brightness"

    def get_description(self) -> str:
        """Return description of brightness effect."""
        return "Adjust the brightness of the image"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply brightness adjustment to the image."""
        factor = params.get("factor", 1.0)

        if factor == 1.0:
            return image

        if factor < 0.0:
            factor = 0.0

        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
