"""
I/O utilities for image processing.

This module handles loading and saving images without side-effects in the core processing functions.
"""

import base64
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from PIL import Image


def load_image(path: Union[str, Path]) -> Image.Image:
    """
    Load an image from a file path.

    Args:
        path: Path to the image file

    Returns:
        PIL Image object in RGBA mode

    Raises:
        FileNotFoundError: If the image file doesn't exist
        IOError: If the image cannot be opened
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    try:
        image = Image.open(path)
        # Convert to RGBA for consistent processing
        return image.convert("RGBA")
    except Exception as e:
        raise IOError(f"Cannot open image {path}: {e}")


def load_image_from_data(image_data: bytes) -> Image.Image:
    """
    Load an image from raw bytes data.

    Args:
        image_data: Raw image bytes

    Returns:
        PIL Image object (preserves original mode for JPEG, converts to RGBA for others)

    Raises:
        IOError: If the image data cannot be processed
    """
    try:
        stream = BytesIO(image_data)
        image = Image.open(stream)

        # Preserve RGB mode for JPEG images, convert others to RGBA
        if image.format == "JPEG" and image.mode == "RGB":
            return image
        else:
            return image.convert("RGBA")
    except Exception as e:
        raise IOError(f"Cannot process image data: {e}")


def load_image_from_base64(base64_data: str) -> Image.Image:
    """
    Load an image from base64 encoded data.

    Args:
        base64_data: Base64 encoded image data

    Returns:
        PIL Image object in RGBA mode

    Raises:
        IOError: If the base64 data cannot be decoded or processed
    """
    try:
        image_data = base64.b64decode(base64_data)
        return load_image_from_data(image_data)
    except Exception as e:
        raise IOError(f"Cannot decode base64 image data: {e}")


def save_image(
    image: Image.Image,
    path: Union[str, Path],
    format: Optional[str] = None,
    quality: int = 95,
    **kwargs,
) -> None:
    """
    Save an image to a file.

    Args:
        image: PIL Image object to save
        path: Output file path
        format: Image format (PNG, JPEG, etc.). If None, inferred from path extension
        quality: JPEG quality (1-100, ignored for other formats)
        **kwargs: Additional arguments passed to PIL's save method

    Raises:
        IOError: If the image cannot be saved
    """
    path = Path(path)

    # Create parent directories if they don't exist
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except (ValueError, OSError) as e:
        raise IOError(f"Cannot create directory for {path}: {e}")

    # Infer format from extension if not provided
    if format is None:
        format = path.suffix.upper().lstrip(".")
        if format == "JPG":
            format = "JPEG"

    try:
        # Handle JPEG format (no alpha channel)
        if format == "JPEG":
            if image.mode in ("RGBA", "LA"):
                # Create white background for transparency
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(
                    image, mask=image.split()[-1] if image.mode == "RGBA" else None
                )
                image = background
            image.save(path, format=format, quality=quality, **kwargs)
        else:
            image.save(path, format=format, **kwargs)

    except Exception as e:
        raise IOError(f"Cannot save image to {path}: {e}")


def image_to_bytes(
    image: Image.Image, format: str = "PNG", quality: int = 95, **kwargs
) -> bytes:
    """
    Convert PIL Image to bytes.

    Args:
        image: PIL Image object
        format: Output format (PNG, JPEG, etc.)
        quality: JPEG quality (1-100, ignored for other formats)
        **kwargs: Additional arguments passed to PIL's save method

    Returns:
        Image data as bytes

    Raises:
        IOError: If the image cannot be converted
    """
    try:
        buffer = BytesIO()

        # Handle JPEG format (no alpha channel)
        if format.upper() == "JPEG":
            if image.mode in ("RGBA", "LA"):
                # Create white background for transparency
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(
                    image, mask=image.split()[-1] if image.mode == "RGBA" else None
                )
                image = background
            image.save(buffer, format=format, quality=quality, **kwargs)
        else:
            image.save(buffer, format=format, **kwargs)

        return buffer.getvalue()
    except Exception as e:
        raise IOError(f"Cannot convert image to bytes: {e}")


def image_to_base64(
    image: Image.Image, format: str = "PNG", quality: int = 95, **kwargs
) -> str:
    """
    Convert PIL Image to base64 string.

    Args:
        image: PIL Image object
        format: Output format (PNG, JPEG, etc.)
        quality: JPEG quality (1-100, ignored for other formats)
        **kwargs: Additional arguments passed to PIL's save method

    Returns:
        Base64 encoded image data

    Raises:
        IOError: If the image cannot be converted
    """
    try:
        image_bytes = image_to_bytes(image, format, quality, **kwargs)
        return base64.b64encode(image_bytes).decode("utf-8")
    except Exception as e:
        raise IOError(f"Cannot convert image to base64: {e}")
