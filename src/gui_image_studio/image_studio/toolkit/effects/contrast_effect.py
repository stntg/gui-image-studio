"""
Contrast adjustment effect.
"""

from PIL import Image, ImageEnhance

from .base_effect import BaseEffect, float_parameter, register_effect


@register_effect
class ContrastEffect(BaseEffect):
    """Adjust image contrast."""

    def __init__(self):
        super().__init__(
            name="contrast", display_name="Contrast", category="enhancement"
        )

        # Add parameters
        self.add_parameter(
            float_parameter(
                name="factor",
                display_name="Contrast",
                default=1.0,
                min_val=0.0,
                max_val=3.0,
                description="Contrast factor (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for contrast effect."""
        return "contrast"

    def get_description(self) -> str:
        """Return description of contrast effect."""
        return "Adjust the contrast of the image"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply contrast adjustment to the image."""
        factor = params.get("factor", 1.0)

        if factor == 1.0:
            return image

        if factor < 0.0:
            factor = 0.0

        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
