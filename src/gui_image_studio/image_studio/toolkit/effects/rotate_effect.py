"""
Rotate effect.
"""

from PIL import Image

from .base_effect import BaseEffect, bool_parameter, float_parameter, register_effect


@register_effect
class RotateEffect(BaseEffect):
    """Rotate image by specified angle."""

    def __init__(self):
        super().__init__(name="rotate", display_name="Rotate", category="geometry")

        # Add parameters
        self.add_parameter(
            float_parameter(
                name="angle",
                display_name="Rotation Angle",
                default=0.0,
                min_val=-360.0,
                max_val=360.0,
                description="Rotation angle in degrees (positive = clockwise)",
            )
        )

        self.add_parameter(
            bool_parameter(
                name="expand",
                display_name="Expand Canvas",
                default=True,
                description="Expand canvas to fit rotated image",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for rotate effect."""
        return "rotate"

    def get_description(self) -> str:
        """Return description of rotate effect."""
        return "Rotate the image by a specified angle"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Rotate the image."""
        angle = params.get("angle", 0.0)
        expand = params.get("expand", True)

        if angle == 0.0:
            return image

        return image.rotate(angle, expand=expand)
