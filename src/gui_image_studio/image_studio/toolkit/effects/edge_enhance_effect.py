"""
Edge enhance effect.
"""

from PIL import Image, ImageFilter

from .base_effect import BaseEffect, choice_parameter, register_effect


@register_effect
class EdgeEnhanceEffect(BaseEffect):
    """Enhance edges in the image."""

    def __init__(self):
        super().__init__(
            name="edge_enhance", display_name="Edge Enhance", category="enhancement"
        )

        # Add parameters
        self.add_parameter(
            choice_parameter(
                name="mode",
                display_name="Enhancement Mode",
                choices=["normal", "more"],
                default="normal",
                description="Edge enhancement strength",
            )
        )

        self.preview_safe = True

    def get_icon(self) -> str:
        """Return the icon name for edge enhance effect."""
        return "edge_enhance"

    def get_description(self) -> str:
        """Return description of edge enhance effect."""
        return "Enhance edges in the image to make details more prominent"

    def apply_effect(self, image: Image.Image, **params) -> Image.Image:
        """Apply edge enhancement to the image."""
        mode = params.get("mode", "normal")

        if mode == "more":
            return image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        else:
            return image.filter(ImageFilter.EDGE_ENHANCE)
