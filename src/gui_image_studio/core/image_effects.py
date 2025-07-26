"""
Unified image effects and transformations.

This module provides the core image processing functions used by both CLI and GUI interfaces.
All functions are pure - they take an image and parameters, return a transformed image,
without side effects like I/O or progress bars.

New effects can be registered using the effects registry system for automatic discovery.
"""

from io import BytesIO
from typing import Any, Dict, Optional, Tuple

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Import the effects registry for new effect registration
from .effects_registry import (
    auto_register_effect,
    bool_parameter,
    choice_parameter,
    create_parameter,
    float_parameter,
    int_parameter,
)


def resize(
    image: Image.Image,
    size: Tuple[int, int],
    resample: Optional[int] = None,
    preserve_aspect: bool = False,
) -> Image.Image:
    """
    Resize an image to the specified dimensions.

    Args:
        image: PIL Image object to resize
        size: Target size as (width, height)
        resample: Resampling algorithm (defaults to LANCZOS)
        preserve_aspect: If True, preserve aspect ratio (size becomes max dimensions)

    Returns:
        Resized PIL Image object
    """
    if resample is None:
        # Handle different Pillow versions
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS  # type: ignore

    if preserve_aspect:
        # Calculate size preserving aspect ratio
        image.thumbnail(size, resample)
        return image
    else:
        return image.resize(size, resample)


def apply_grayscale(image: Image.Image) -> Image.Image:
    """
    Convert image to grayscale while preserving alpha channel.

    Args:
        image: PIL Image object to convert

    Returns:
        Grayscale PIL Image object in RGBA mode
    """
    return ImageOps.grayscale(image).convert("RGBA")


def apply_rotation(
    image: Image.Image, angle: float, expand: bool = True
) -> Image.Image:
    """
    Rotate an image by the specified angle.

    Args:
        image: PIL Image object to rotate
        angle: Rotation angle in degrees (positive = clockwise)
        expand: If True, expand output to fit entire rotated image

    Returns:
        Rotated PIL Image object
    """
    return image.rotate(angle, expand=expand)


def apply_transparency(image: Image.Image, alpha: float) -> Image.Image:
    """
    Apply transparency/opacity to an image.

    Args:
        image: PIL Image object
        alpha: Transparency level (0.0 = fully transparent, 1.0 = fully opaque)

    Returns:
        PIL Image object with adjusted transparency
    """
    if alpha < 0.0 or alpha > 1.0:
        raise ValueError("Alpha must be between 0.0 and 1.0")

    # Use brightness enhancement to simulate transparency
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(alpha)


def apply_contrast(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust image contrast.

    Args:
        image: PIL Image object
        factor: Contrast factor (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)

    Returns:
        PIL Image object with adjusted contrast
    """
    if factor < 0.0:
        raise ValueError("Contrast factor must be non-negative")

    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def apply_saturation(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust image color saturation.

    Args:
        image: PIL Image object
        factor: Saturation factor (1.0 = no change, >1.0 = more saturated, 0.0 = grayscale)

    Returns:
        PIL Image object with adjusted saturation
    """
    if factor < 0.0:
        raise ValueError("Saturation factor must be non-negative")

    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


def apply_brightness(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust image brightness.

    Args:
        image: PIL Image object
        factor: Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)

    Returns:
        PIL Image object with adjusted brightness
    """
    if factor < 0.0:
        raise ValueError("Brightness factor must be non-negative")

    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def apply_sharpness(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust image sharpness.

    Args:
        image: PIL Image object
        factor: Sharpness factor (1.0 = no change, >1.0 = sharper, <1.0 = blurred)

    Returns:
        PIL Image object with adjusted sharpness
    """
    if factor < 0.0:
        raise ValueError("Sharpness factor must be non-negative")

    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)


def apply_blur(image: Image.Image, radius: float = 2.0) -> Image.Image:
    """
    Apply Gaussian blur to an image.

    Args:
        image: PIL Image object to blur
        radius: Blur radius (higher = more blur)

    Returns:
        Blurred PIL Image object
    """
    if radius < 0.0:
        raise ValueError("Blur radius must be non-negative")

    return image.filter(ImageFilter.GaussianBlur(radius))


def apply_tint(
    image: Image.Image, tint_color: Tuple[int, int, int], intensity: float
) -> Image.Image:
    """
    Apply a color tint to an image.

    Args:
        image: PIL Image object to tint
        tint_color: RGB color tuple (r, g, b) where each value is 0-255
        intensity: Tint intensity (0.0 = no tint, 1.0 = full tint)

    Returns:
        Tinted PIL Image object
    """
    if intensity < 0.0 or intensity > 1.0:
        raise ValueError("Tint intensity must be between 0.0 and 1.0")

    if intensity == 0.0:
        return image

    # Ensure image is in RGBA mode
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Create tint overlay
    overlay = Image.new("RGBA", image.size, tint_color + (255,))

    # Blend with original image
    return Image.blend(image, overlay, intensity)


def apply_format_conversion(image: Image.Image, target_format: str) -> Image.Image:
    """
    Convert image to a different format.

    Args:
        image: PIL Image object to convert
        target_format: Target format (PNG, JPEG, etc.)

    Returns:
        PIL Image object in the target format
    """
    buffer = BytesIO()

    # Handle JPEG format (no alpha channel)
    if target_format.upper() == "JPEG":
        if image.mode in ("RGBA", "LA"):
            # Create white background for transparency
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(
                image, mask=image.split()[-1] if image.mode == "RGBA" else None
            )
            image = background

    image.save(buffer, format=target_format)
    buffer.seek(0)
    return Image.open(buffer)


def apply_transformations(image: Image.Image, **transforms: Any) -> Image.Image:
    """
    Apply multiple transformations to an image in sequence.

    This is the main function that orchestrates all transformations,
    maintaining compatibility with the existing API.

    Args:
        image: PIL Image object to transform
        **transforms: Transformation parameters

    Returns:
        Transformed PIL Image object
    """
    # Extract transformation parameters with defaults
    grayscale = transforms.get("grayscale", False)
    rotate = transforms.get("rotate", 0)
    transparency = transforms.get("transparency", 1.0)
    size = transforms.get("size")
    contrast = transforms.get("contrast", 1.0)
    saturation = transforms.get("saturation", 1.0)
    brightness = transforms.get("brightness", 1.0)
    sharpness = transforms.get("sharpness", 1.0)
    blur_radius = transforms.get("blur_radius", 0.0)
    tint_color = transforms.get("tint_color")
    tint_intensity = transforms.get("tint_intensity", 0.0)
    format_override = transforms.get("format_override")

    # Apply transformations in sequence
    result = image

    if grayscale:
        result = apply_grayscale(result)

    if rotate != 0:
        result = apply_rotation(result, rotate)

    if transparency != 1.0:
        result = apply_transparency(result, transparency)

    if size:
        result = resize(result, size)

    if contrast != 1.0:
        result = apply_contrast(result, contrast)

    if saturation != 1.0:
        result = apply_saturation(result, saturation)

    if brightness != 1.0:
        result = apply_brightness(result, brightness)

    if sharpness != 1.0:
        result = apply_sharpness(result, sharpness)

    if blur_radius > 0.0:
        result = apply_blur(result, blur_radius)

    if tint_color is not None and tint_intensity > 0.0:
        result = apply_tint(result, tint_color, tint_intensity)

    if format_override:
        result = apply_format_conversion(result, format_override)

    return result


# Convenience functions for common operations
def create_thumbnail(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """
    Create a thumbnail of an image preserving aspect ratio.

    Args:
        image: PIL Image object
        size: Maximum dimensions as (width, height)

    Returns:
        Thumbnail PIL Image object
    """
    thumbnail = image.copy()
    thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
    return thumbnail


def crop_to_square(image: Image.Image) -> Image.Image:
    """
    Crop image to a square using the center portion.

    Args:
        image: PIL Image object to crop

    Returns:
        Square PIL Image object
    """
    width, height = image.size
    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    return image.crop((left, top, right, bottom))


def add_border(
    image: Image.Image,
    border_width: int,
    border_color: Tuple[int, int, int] = (0, 0, 0),
) -> Image.Image:
    """
    Add a solid color border around an image.

    Args:
        image: PIL Image object
        border_width: Width of the border in pixels
        border_color: RGB color of the border

    Returns:
        PIL Image object with border
    """
    if border_width <= 0:
        return image

    width, height = image.size
    new_width = width + 2 * border_width
    new_height = height + 2 * border_width

    # Create new image with border color
    bordered = Image.new("RGBA", (new_width, new_height), border_color + (255,))

    # Paste original image in the center
    bordered.paste(image, (border_width, border_width))

    return bordered


# ============================================================================
# NEW EFFECTS USING THE REGISTRY SYSTEM
# ============================================================================
# These effects demonstrate the new self-registry system and can be discovered
# automatically by CLI and GUI interfaces.


@auto_register_effect(
    display_name="Sepia Tone",
    description="Apply a warm sepia tone effect",
    category="color",
    parameters=[float_parameter("intensity", 1.0, 0.0, 1.0, "Sepia effect intensity")],
)
def apply_sepia(image: Image.Image, intensity: float = 1.0) -> Image.Image:
    """Apply sepia tone effect to an image."""
    if intensity <= 0.0:
        return image

    # Convert to grayscale first
    grayscale = apply_grayscale(image)

    # Apply sepia tint
    sepia_color = (244, 222, 179)  # Warm sepia color
    return apply_tint(grayscale, sepia_color, intensity * 0.6)


@auto_register_effect(
    display_name="Emboss",
    description="Apply emboss filter for 3D effect",
    category="filter",
    parameters=[],
)
def apply_emboss(image: Image.Image) -> Image.Image:
    """Apply emboss filter to create a 3D effect."""
    return image.filter(ImageFilter.EMBOSS)


@auto_register_effect(
    display_name="Edge Enhance",
    description="Enhance edges in the image",
    category="enhancement",
    parameters=[
        choice_parameter("mode", ["normal", "more"], "normal", "Enhancement strength")
    ],
)
def apply_edge_enhance(image: Image.Image, mode: str = "normal") -> Image.Image:
    """Enhance edges in the image."""
    if mode == "more":
        return image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    else:
        return image.filter(ImageFilter.EDGE_ENHANCE)


@auto_register_effect(
    display_name="Find Edges",
    description="Detect and highlight edges",
    category="filter",
    parameters=[],
)
def apply_find_edges(image: Image.Image) -> Image.Image:
    """Find and highlight edges in the image."""
    return image.filter(ImageFilter.FIND_EDGES)


@auto_register_effect(
    display_name="Smooth",
    description="Apply smoothing filter",
    category="filter",
    parameters=[
        choice_parameter("mode", ["normal", "more"], "normal", "Smoothing strength")
    ],
)
def apply_smooth(image: Image.Image, mode: str = "normal") -> Image.Image:
    """Apply smoothing filter to reduce noise."""
    if mode == "more":
        return image.filter(ImageFilter.SMOOTH_MORE)
    else:
        return image.filter(ImageFilter.SMOOTH)


@auto_register_effect(
    display_name="Posterize",
    description="Reduce number of colors for poster effect",
    category="color",
    parameters=[int_parameter("bits", 4, 1, 8, "Number of bits per color channel")],
)
def apply_posterize(image: Image.Image, bits: int = 4) -> Image.Image:
    """Reduce the number of colors in the image."""
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


@auto_register_effect(
    display_name="Solarize",
    description="Invert colors above threshold",
    category="color",
    parameters=[int_parameter("threshold", 128, 0, 255, "Solarization threshold")],
)
def apply_solarize(image: Image.Image, threshold: int = 128) -> Image.Image:
    """Invert all pixel values above a threshold."""
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


@auto_register_effect(
    display_name="Invert Colors",
    description="Invert all colors in the image",
    category="color",
    parameters=[],
)
def apply_invert(image: Image.Image) -> Image.Image:
    """Invert all colors in the image."""
    return ImageOps.invert(image.convert("RGB")).convert(image.mode)


@auto_register_effect(
    display_name="Auto Contrast",
    description="Automatically adjust contrast",
    category="enhancement",
    parameters=[
        float_parameter(
            "cutoff", 0.0, 0.0, 50.0, "Percentage of pixels to ignore at extremes"
        )
    ],
)
def apply_autocontrast(image: Image.Image, cutoff: float = 0.0) -> Image.Image:
    """Automatically adjust image contrast."""
    # Handle RGBA images
    if image.mode == "RGBA":
        alpha = image.split()[-1]
        rgb_image = image.convert("RGB")
        contrasted = ImageOps.autocontrast(rgb_image, cutoff=cutoff)
        contrasted = contrasted.convert("RGBA")
        contrasted.putalpha(alpha)
        return contrasted
    else:
        return ImageOps.autocontrast(image, cutoff=cutoff)


@auto_register_effect(
    display_name="Equalize Histogram",
    description="Equalize the image histogram",
    category="enhancement",
    parameters=[],
)
def apply_equalize(image: Image.Image) -> Image.Image:
    """Equalize the image histogram for better contrast distribution."""
    # Handle RGBA images
    if image.mode == "RGBA":
        alpha = image.split()[-1]
        rgb_image = image.convert("RGB")
        equalized = ImageOps.equalize(rgb_image)
        equalized = equalized.convert("RGBA")
        equalized.putalpha(alpha)
        return equalized
    else:
        return ImageOps.equalize(image)


@auto_register_effect(
    display_name="Flip Horizontal",
    description="Flip image horizontally (mirror)",
    category="geometry",
    parameters=[],
)
def apply_flip_horizontal(image: Image.Image) -> Image.Image:
    """Flip image horizontally."""
    return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


@auto_register_effect(
    display_name="Flip Vertical",
    description="Flip image vertically",
    category="geometry",
    parameters=[],
)
def apply_flip_vertical(image: Image.Image) -> Image.Image:
    """Flip image vertically."""
    return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)


@auto_register_effect(
    display_name="Gaussian Blur",
    description="Apply Gaussian blur with precise control",
    category="filter",
    parameters=[float_parameter("radius", 2.0, 0.0, 20.0, "Blur radius")],
)
def apply_gaussian_blur(image: Image.Image, radius: float = 2.0) -> Image.Image:
    """Apply Gaussian blur with precise radius control."""
    if radius <= 0.0:
        return image
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


@auto_register_effect(
    display_name="Unsharp Mask",
    description="Sharpen image using unsharp mask",
    category="enhancement",
    parameters=[
        float_parameter("radius", 2.0, 0.1, 10.0, "Blur radius for mask"),
        int_parameter("percent", 150, 0, 500, "Sharpening strength percentage"),
        int_parameter("threshold", 3, 0, 255, "Minimum difference threshold"),
    ],
)
def apply_unsharp_mask(
    image: Image.Image, radius: float = 2.0, percent: int = 150, threshold: int = 3
) -> Image.Image:
    """Apply unsharp mask for advanced sharpening."""
    return image.filter(
        ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold)
    )


@auto_register_effect(
    display_name="Color Balance",
    description="Adjust color balance in shadows, midtones, and highlights",
    category="color",
    parameters=[
        float_parameter("cyan_red", 0.0, -100.0, 100.0, "Cyan-Red balance"),
        float_parameter("magenta_green", 0.0, -100.0, 100.0, "Magenta-Green balance"),
        float_parameter("yellow_blue", 0.0, -100.0, 100.0, "Yellow-Blue balance"),
    ],
)
def apply_color_balance(
    image: Image.Image,
    cyan_red: float = 0.0,
    magenta_green: float = 0.0,
    yellow_blue: float = 0.0,
) -> Image.Image:
    """Adjust color balance (simplified implementation)."""
    if cyan_red == 0.0 and magenta_green == 0.0 and yellow_blue == 0.0:
        return image

    # Convert to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Apply color adjustments (simplified)
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Apply color balance adjustments
            r = max(0, min(255, r + cyan_red * 2.55))
            g = max(0, min(255, g + magenta_green * 2.55))
            b = max(0, min(255, b + yellow_blue * 2.55))

            pixels[x, y] = (int(r), int(g), int(b))

    return image


# Note: Auto-discovery of effects is handled by the effects_registry module

# Trigger discovery of legacy effects for backward compatibility
try:
    from .effects_registry import discover_and_register_effects

    discover_and_register_effects()
except ImportError:
    pass
