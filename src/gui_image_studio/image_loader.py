from __future__ import annotations

# Standard library
import base64
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Optional, Tuple

# Third-party
from PIL import Image, ImageSequence

# Local application imports
try:
    from . import embedded_images
except ImportError:

    class EmbeddedImages:
        embedded_images = {"default": {}}

    embedded_images: Any = EmbeddedImages()

# Import unified image processing core
from .core.image_effects import apply_transformations
from .core.io_utils import load_image_from_base64


@dataclass
class ImageConfig:
    """Configuration class for image processing parameters."""

    image_name: str
    framework: str = "tkinter"
    size: Tuple[int, int] = (32, 32)
    theme: str = "default"
    grayscale: bool = False
    rotate: int = 0
    transparency: float = 1.0
    format_override: Optional[str] = None
    animated: bool = False
    frame_delay: int = 100
    tint_color: Optional[Tuple[int, int, int]] = None
    tint_intensity: float = 0.0
    contrast: float = 1.0
    saturation: float = 1.0

    def to_transforms_dict(self) -> dict:
        """Convert configuration to transforms dictionary."""
        return {
            "grayscale": self.grayscale,
            "rotate": self.rotate,
            "transparency": self.transparency,
            "size": self.size,
            "contrast": self.contrast,
            "saturation": self.saturation,
            "tint_color": self.tint_color,
            "tint_intensity": self.tint_intensity,
            "format_override": self.format_override,
        }


def _get_image_data(image_name: str, theme: str) -> Image.Image:
    """
    Retrieve and decode image data from embedded images.

    Args:
        image_name (str): Name of the image file.
        theme (str): Theme name.

    Returns:
        PIL.Image: Opened PIL Image object.

    Raises:
        ValueError: If image is not found in the specified theme.
    """
    theme_dict = embedded_images.embedded_images.get(
        theme
    ) or embedded_images.embedded_images.get("default")

    if not theme_dict or image_name not in theme_dict:
        raise ValueError(f"Image '{image_name}' not found in theme '{theme}'.")

    # Use the unified core for loading base64 data
    return load_image_from_base64(theme_dict[image_name])


def _apply_image_transformations(img: Image.Image, **transforms: Any) -> Image.Image:
    """
    Apply various transformations to a PIL Image using the unified core.

    Args:
        img (PIL.Image): The image to transform.
        **transforms: Transformation parameters.

    Returns:
        PIL.Image: The transformed image.
    """
    # Use the unified image processing core
    return apply_transformations(img, **transforms)


def _create_framework_image(
    img: Image.Image, framework: str, size: Optional[Tuple[int, int]]
) -> Any:
    """
    Convert PIL Image to framework-specific image object.

    Args:
        img (PIL.Image): The PIL image to convert.
        framework (str): Target framework ("tkinter" or "customtkinter").
        size (tuple): Image size for CustomTkinter.

    Returns:
        Framework-specific image object.
    """
    if framework.lower() == "customtkinter":
        import customtkinter as ctk

        return ctk.CTkImage(light_image=img, size=size)
    else:
        from PIL import ImageTk

        return ImageTk.PhotoImage(img)


def _is_animated_gif(img: Image.Image, animated: bool) -> bool:
    """
    Check if image is an animated GIF that should be processed as animated.

    Args:
        img (PIL.Image): The image to check.
        animated (bool): Whether animated processing is requested.

    Returns:
        bool: True if image should be processed as animated GIF.
    """
    return (
        animated
        and img.format == "GIF"
        and getattr(img, "is_animated", False)
        and getattr(img, "n_frames", 1) > 1
    )


def _process_animated_gif(
    img: Image.Image,
    framework: str,
    size: Optional[Tuple[int, int]],
    frame_delay: int,
    **transforms: Any,
) -> list[Any]:
    """
    Process an animated GIF by applying transformations to each frame.

    Args:
        img (PIL.Image): The animated GIF image.
        framework (str): Target framework.
        size (tuple): Frame size.
        frame_delay (int): Delay between frames.
        **transforms: Transformation parameters.

    Returns:
        dict: Dictionary with "animated_frames" and "frame_delay" keys.

    Raises:
        RuntimeError: If frame processing fails.
    """
    frames = []
    try:
        for frame in ImageSequence.Iterator(img):
            frame = frame.convert("RGBA")
            frame = _apply_image_transformations(frame, size=size, **transforms)
            frame_obj = _create_framework_image(frame, framework, size)
            frames.append(frame_obj)
    except Exception as e:
        raise RuntimeError(f"Error processing animated GIF frames: {e}")

    return {"animated_frames": frames, "frame_delay": frame_delay}


def _process_image_with_config(config: ImageConfig) -> Any:
    """
    Process an image based on the provided configuration.

    Args:
        config (ImageConfig): Image processing configuration.

    Returns:
        Framework-specific image object or animated frames dictionary.
    """
    # Get the base image
    img = _get_image_data(config.image_name, config.theme)

    # Get transformation parameters
    transforms = config.to_transforms_dict()

    # Handle animated GIFs
    if _is_animated_gif(img, config.animated):
        return _process_animated_gif(
            img, config.framework, config.size, config.frame_delay, **transforms
        )

    # Process static image
    img = _apply_image_transformations(img, **transforms)
    return _create_framework_image(img, config.framework, config.size)


def get_image(
    image_name: str,
    framework: str = "tkinter",
    size: Tuple[int, int] = (32, 32),
    theme: str = "default",
    grayscale: bool = False,
    rotate: int = 0,
    transparency: float = 1.0,
    format_override: Optional[str] = None,
    animated: bool = False,
    frame_delay: int = 100,
    tint_color: Optional[str] = None,
    tint_intensity: float = 0.0,
    contrast: float = 1.0,
    saturation: float = 1.0,
) -> Any:
    """
    Retrieve an embedded image with dynamic transformations and optional animated
    GIF support.

    Args:
        image_name (str): Name of the image file (e.g., 'icon.png').
        framework (str): "tkinter" or "customtkinter".
        size (tuple): Desired dimensions; used for resizing. For animated GIFs,
            each frame is resized.
        theme (str): Theme name (e.g., "dark", "light"); falls back to "default"
            if not matched.
        grayscale (bool): Convert image to grayscale.
        rotate (int): Rotate image (or each frame) by the given degrees.
        transparency (float): Adjust brightness/opacity (0.0 to 1.0).
        format_override (str): Convert image to this format on the fly ("PNG",
            "JPEG", etc.).
        animated (bool): If True and image is an animated GIF, process all its frames.
        frame_delay (int): Delay (milliseconds) between frames for animated GIFs.
        tint_color (tuple or None): A tuple (R, G, B) for a tint overlay.
        tint_intensity (float): Blending factor (0.0 to 1.0) for tint; 0 means no tint.
        contrast (float): Contrast adjustment factor (1.0 means no change).
        saturation (float): Saturation adjustment factor (1.0 means no change).

    Returns:
        For static images:
          - A Tkinter PhotoImage or a CustomTkinter CTkImage.
        For animated GIFs:
          - A dictionary with keys "animated_frames" (a list of image objects) and
            "frame_delay".
            Use these frames in an animation loop.
    """
    config = ImageConfig(
        image_name=image_name,
        framework=framework,
        size=size,
        theme=theme,
        grayscale=grayscale,
        rotate=rotate,
        transparency=transparency,
        format_override=format_override,
        animated=animated,
        frame_delay=frame_delay,
        tint_color=tint_color,
        tint_intensity=tint_intensity,
        contrast=contrast,
        saturation=saturation,
    )

    return _process_image_with_config(config)


def get_image_from_config(config: ImageConfig) -> Any:
    """
    Retrieve an embedded image using an ImageConfig object.

    This is a convenience function for when you have complex configurations
    or want to reuse the same configuration multiple times.

    Args:
        config (ImageConfig): Complete image processing configuration.

    Returns:
        Same as get_image() - framework-specific image object or animated frames dictionary.
    """
    return _process_image_with_config(config)
