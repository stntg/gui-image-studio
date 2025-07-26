"""
Image effects for the GUI toolkit.

This module provides image transformation effects that can be applied
to images in the GUI application, following the same self-registry
pattern as tools.
"""

# Import all effects to trigger registration
from . import (
    blur_effect,
    brightness_effect,
    contrast_effect,
    edge_enhance_effect,
    emboss_effect,
    flip_horizontal_effect,
    flip_vertical_effect,
    grayscale_effect,
    invert_effect,
    posterize_effect,
    rotate_effect,
    saturation_effect,
    sepia_effect,
    sharpen_effect,
    solarize_effect,
)

__all__ = [
    "brightness_effect",
    "contrast_effect",
    "saturation_effect",
    "blur_effect",
    "sharpen_effect",
    "grayscale_effect",
    "sepia_effect",
    "invert_effect",
    "flip_horizontal_effect",
    "flip_vertical_effect",
    "rotate_effect",
    "posterize_effect",
    "solarize_effect",
    "emboss_effect",
    "edge_enhance_effect",
]
