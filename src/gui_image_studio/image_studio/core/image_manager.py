"""
Image management functionality using the unified core.
"""

import tempfile
from typing import Dict, Optional

from PIL import Image, ImageTk

# Import unified core functions
from ...core.image_effects import apply_transformations, create_thumbnail
from ...core.io_utils import load_image, save_image


class ImageManager:
    """Manages image operations and storage using the unified core."""

    def __init__(self):
        self.current_images: Dict[str, Image.Image] = {}
        self.original_images: Dict[str, Image.Image] = {}
        self.base_images: Dict[str, Image.Image] = {}
        self.current_rotations: Dict[str, int] = {}
        self.image_previews: Dict[str, ImageTk.PhotoImage] = {}
        self.selected_image: Optional[str] = None
        self.temp_dir = tempfile.mkdtemp()

    def add_image(self, name: str, image: Image.Image) -> None:
        """Add a new image to the manager."""
        self.current_images[name] = image
        self.original_images[name] = image.copy()
        self.base_images[name] = image.copy()
        self.current_rotations[name] = 0
        self.update_preview(name)

    def load_image_from_file(self, name: str, file_path: str) -> None:
        """Load an image from file using the unified core."""
        try:
            image = load_image(file_path)
            self.add_image(name, image)
        except Exception as e:
            raise IOError(f"Failed to load image {file_path}: {e}")

    def save_image_to_file(self, name: str, file_path: str, **kwargs) -> None:
        """Save an image to file using the unified core."""
        if name not in self.current_images:
            raise ValueError(f"Image '{name}' not found")

        try:
            save_image(self.current_images[name], file_path, **kwargs)
        except Exception as e:
            raise IOError(f"Failed to save image {file_path}: {e}")

    def apply_transformations_to_image(self, name: str, **transforms) -> None:
        """Apply transformations to an image using the unified core."""
        if name not in self.current_images:
            raise ValueError(f"Image '{name}' not found")

        try:
            # Apply transformations using the unified core
            transformed = apply_transformations(self.current_images[name], **transforms)
            self.current_images[name] = transformed
            self.update_preview(name)
        except Exception as e:
            raise RuntimeError(f"Failed to apply transformations: {e}")

    def update_preview(self, name: str) -> None:
        """Update the preview for an image using the unified core."""
        if name not in self.current_images:
            return

        try:
            # Use unified core for thumbnail creation
            image = self.current_images[name]
            preview_image = create_thumbnail(image, (64, 64))

            # Convert to PhotoImage
            self.image_previews[name] = ImageTk.PhotoImage(preview_image)
        except Exception as e:
            print(f"Warning: Failed to update preview for {name}: {e}")

    def get_image(self, name: str) -> Optional[Image.Image]:
        """Get an image by name."""
        return self.current_images.get(name)

    def get_preview(self, name: str) -> Optional[ImageTk.PhotoImage]:
        """Get a preview image by name."""
        return self.image_previews.get(name)

    def list_images(self) -> list[str]:
        """Get list of all image names."""
        return list(self.current_images.keys())

    def remove_image(self, name: str) -> None:
        """Remove an image from the manager."""
        if name in self.current_images:
            del self.current_images[name]
            del self.original_images[name]
            del self.base_images[name]
            del self.current_rotations[name]
            if name in self.image_previews:
                del self.image_previews[name]

    def reset_image(self, name: str) -> None:
        """Reset an image to its original state."""
        if name in self.original_images:
            self.current_images[name] = self.original_images[name].copy()
            self.current_rotations[name] = 0
            self.update_preview(name)

    def remove_image(self, name: str) -> None:
        """Remove an image from the manager."""
        for storage in [
            self.current_images,
            self.original_images,
            self.base_images,
            self.image_previews,
        ]:
            storage.pop(name, None)

        self.current_rotations.pop(name, None)

        if self.selected_image == name:
            self.selected_image = None

    def get_image(self, name: str) -> Optional[Image.Image]:
        """Get an image by name."""
        return self.current_images.get(name)

    def get_preview(self, name: str) -> Optional[ImageTk.PhotoImage]:
        """Get a preview image by name."""
        return self.image_previews.get(name)

    def list_images(self) -> list:
        """Get list of all image names."""
        return list(self.current_images.keys())

    def clear_all(self) -> None:
        """Clear all images."""
        self.current_images.clear()
        self.original_images.clear()
        self.base_images.clear()
        self.current_rotations.clear()
        self.image_previews.clear()
        self.selected_image = None
