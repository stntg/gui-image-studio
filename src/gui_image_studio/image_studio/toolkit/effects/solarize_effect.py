"""
Solarize effect.
"""

from PIL import Image, ImageOps

from .base_effect import BaseEffect, int_parameter, register_effect


@register_effect
class SolarizeEffect(BaseEffect):
    """Invert colors above threshold."""

    def __init__(self):
        super().__init__(name="solarize", display_name="Solarize", category="color")

        # Add parameters
        self.add_parameter(
            int_parameter(
                name="threshold",
                display_name="Threshold",
                default=128,
                min_val=0,
                max_val=255,
                description="Solarization threshold (pixels above this value are inverted)",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for solarize effect."""
        return "solarize"

    def get_description(self) -> str:
        """Return description of solarize effect."""
        return "Invert pixel values above a threshold for a solarization effect"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply solarize effect to the image."""
        threshold = params.get("threshold", 128)

        # Handle RGBA images
        if image.mode == "RGBA":
            alpha = image.split()[-1]
            rgb_image = image.convert("RGB")
            solarized = ImageOps.solarize(rgb_image, threshold)
            solarized = solarized.convert("RGBA")
            solarized.putalpha(alpha)
            return solarized
        else:
            return ImageOps.solarize(image, threshold)
