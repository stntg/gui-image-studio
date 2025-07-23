#!/usr/bin/env python3
"""
Test script to verify that the image listbox works correctly when panels are detached/reattached.
"""

import tkinter as tk

from PIL import Image

from src.gui_image_studio.image_studio.main_app import EnhancedImageDesignerGUI


def test_panel_detach_functionality():
    """Test the panel detach/reattach functionality with image listbox."""

    # Create the application
    app = EnhancedImageDesignerGUI()

    # Create some test images programmatically
    test_images = {}
    for i in range(3):
        # Create a simple colored image
        img = Image.new("RGB", (100, 100), color=(255 * i // 2, 100, 150))
        test_images[f"test_image_{i+1}"] = img

    # Add the test images to the application
    for name, img in test_images.items():
        app.current_images[name] = img
        app.original_images[name] = img.copy()
        app.base_images[name] = img.copy()
        app.current_rotations[name] = 0

    # Update the image list to show the test images
    app.update_image_list()

    # Select the first image
    if test_images:
        first_image_name = list(test_images.keys())[0]
        app.select_image(first_image_name)

    print("Test setup complete!")
    print(f"Added {len(test_images)} test images to the application.")
    print("You can now test the detach/reattach functionality:")
    print("1. Verify that the image listbox shows the test images")
    print("2. Detach the left panel and verify the listbox is still populated")
    print(
        "3. Load a new image while detached and verify both old and new images appear"
    )
    print("4. Reattach the left panel and verify all images are still visible")

    # Start the application
    app.root.mainloop()


if __name__ == "__main__":
    test_panel_detach_functionality()
