"""
Posterize effect.
"""

from PIL import Image, ImageOps

from .base_effect import BaseEffect, int_parameter, register_effect


@register_effect
class PosterizeEffect(BaseEffect):
    """Reduce number of colors for poster effect."""

    def __init__(self):
        super().__init__(name="posterize", display_name="Posterize", category="color")

        # Add parameters
        self.add_parameter(
            int_parameter(
                name="bits",
                display_name="Color Bits",
                default=4,
                min_val=1,
                max_val=8,
                description="Number of bits per color channel (lower = fewer colors)",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for posterize effect."""
        return "posterize"

    def get_description(self) -> str:
        """Return description of posterize effect."""
        return "Reduce the number of colors to create a poster-like effect"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply posterize effect to the image."""
        bits = params.get("bits", 4)

        # Handle RGBA images by converting to RGB, applying effect, then restoring alpha
        if image.mode == "RGBA":
            alpha = image.split()[-1]
            rgb_image = image.convert("RGB")
            posterized = ImageOps.posterize(rgb_image, bits)
            posterized = posterized.convert("RGBA")
            posterized.putalpha(alpha)
            return posterized
        else:
            return ImageOps.posterize(image, bits)
