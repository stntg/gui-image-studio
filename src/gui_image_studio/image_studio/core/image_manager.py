"""
Image management functionality.
"""

import tempfile
from typing import Dict, Optional

from PIL import Image, ImageTk


class ImageManager:
    """Manages image operations and storage."""

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

    def update_preview(self, name: str) -> None:
        """Update the preview for an image."""
        if name not in self.current_images:
            return

        image = self.current_images[name]
        # Create thumbnail for preview
        preview_size = (64, 64)
        preview_image = image.copy()
        preview_image.thumbnail(preview_size, Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        self.image_previews[name] = ImageTk.PhotoImage(preview_image)

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
