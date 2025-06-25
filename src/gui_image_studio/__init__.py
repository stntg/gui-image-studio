"""
gui_image_studio - Image Resource Management for Python GUI Applications
========================================================================

A Python library for embedding and loading images efficiently in GUI applications.
Supports both Tkinter and CustomTkinter frameworks with advanced image transformations.

Key Features:
- Embed images as base64 data in Python files
- Load images with transformations (resize, rotate, tint, etc.)
- Theme support (light, dark, custom themes)
- Animated GIF support
- Framework agnostic (Tkinter, CustomTkinter)
- Memory efficient caching
- Easy integration

Basic Usage:
    import gui_image_studio

    # Load an image
    image = gui_image_studio.get_image(
        "icon.png",
        framework="tkinter",
        size=(64, 64),
        theme="dark"
    )

    # Use in your GUI
    label = tk.Label(root, image=image)
    label.pack()

Advanced Usage:
    # Load with transformations
    image = gui_image_studio.get_image(
        "button.png",
        framework="customtkinter",
        size=(100, 40),
        tint_color=(255, 100, 100),
        tint_intensity=0.3,
        rotate=15,
        contrast=1.2
    )

For more examples and documentation, see:
https://github.com/stntg/gui_image_studio
"""

__version__ = "1.0.1"
__author__ = "Stan Griffiths"
__email__ = "stantgriffiths@gmail.com"
__license__ = "MIT"

from .generator import embed_images_from_folder

# Import main functionality
from .image_loader import get_image
from .sample_creator import create_sample_images

# Make key functions available at package level
__all__ = [
    "get_image",
    "embed_images_from_folder",
    "create_sample_images",
    "launch_designer",
    "__version__",
]


def launch_designer():
    """Launch the GUI Image Studio."""
    try:
        from .image_studio import main

        main()
    except ImportError as e:
        print(f"Error importing GUI components: {e}")
        print("Make sure tkinter is available (usually built-in with Python)")
        raise
    except Exception as e:
        print(f"Error launching studio: {e}")
        raise


# Convenience imports for common use cases
try:
    import tkinter  # noqa: F401

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

try:
    import customtkinter  # noqa: F401

    CUSTOMTKINTER_AVAILABLE = True
except ImportError:
    CUSTOMTKINTER_AVAILABLE = False


def get_available_frameworks():
    """Return list of available GUI frameworks."""
    frameworks = []
    if TKINTER_AVAILABLE:
        frameworks.append("tkinter")
    if CUSTOMTKINTER_AVAILABLE:
        frameworks.append("customtkinter")
    return frameworks


def check_dependencies():
    """Check if all required dependencies are available."""
    missing = []

    try:
        import PIL  # noqa: F401
    except ImportError:
        missing.append("Pillow")

    if not TKINTER_AVAILABLE:
        missing.append("tkinter (usually built-in)")

    return missing


# Package metadata
__package_info__ = {
    "name": "gui_image_studio",
    "version": __version__,
    "description": (
        "A comprehensive Python toolkit for creating, embedding, and managing "
        "images in Python GUI applications with support for tkinter and customtkinter."
    ),
    "author": __author__,
    "license": __license__,
    "frameworks": get_available_frameworks(),
    "dependencies_missing": check_dependencies(),
}
