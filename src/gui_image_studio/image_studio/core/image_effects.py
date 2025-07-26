"""
Unified image effects and transformations.

This module provides the core image processing functions used by both CLI and GUI interfaces.
All functions are pure - they take an image and parameters, return a transformed image,
without side effects like I/O or progress bars.
"""

from io import BytesIO
from typing import Any, Dict, Optional, Tuple

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


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
