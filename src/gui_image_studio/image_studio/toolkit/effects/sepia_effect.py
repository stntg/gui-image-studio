"""
Sepia tone effect.
"""

from PIL import Image, ImageOps

from .base_effect import BaseEffect, float_parameter, register_effect


@register_effect
class SepiaEffect(BaseEffect):
    """Apply sepia tone effect."""

    def __init__(self):
        super().__init__(name="sepia", display_name="Sepia Tone", category="color")

        # Add parameters
        self.add_parameter(
            float_parameter(
                name="intensity",
                display_name="Sepia Intensity",
                default=1.0,
                min_val=0.0,
                max_val=1.0,
                description="Intensity of the sepia effect (0.0 = no effect, 1.0 = full sepia)",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for sepia effect."""
        return "sepia"

    def get_description(self) -> str:
        """Return description of sepia effect."""
        return "Apply a warm sepia tone effect to the image"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply sepia tone to the image."""
        intensity = params.get("intensity", 1.0)

        if intensity <= 0.0:
            return image

        # Convert to grayscale first
        grayscale = ImageOps.grayscale(image).convert("RGBA")

        # Apply sepia tint
        sepia_color = (244, 222, 179, 255)  # Warm sepia color

        # Create sepia overlay
        overlay = Image.new("RGBA", grayscale.size, sepia_color)

        # Blend with grayscale image
        sepia_strength = intensity * 0.6
        result = Image.blend(grayscale, overlay, sepia_strength)

        return result
