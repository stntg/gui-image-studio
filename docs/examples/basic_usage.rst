Basic Usage Examples
====================

This section demonstrates the fundamental operations you can perform with GUI Image Studio.

Loading and Saving Images
--------------------------

The most basic operations involve loading images from files and saving them in different formats.

**Simple Load and Save**

.. code-block:: python

    # Example: Basic Image Loading and Saving
    # Demonstrates how to load an image from a file and save it in a different format.

    import gui_image_studio

    def convert_image_format(input_path: str, output_path: str) -> bool:
        """
        Convert an image from one format to another.

        Args:
            input_path: Path to the input image
            output_path: Path for the output image

        Returns:
            True if successful, False otherwise
        """
        try:
            # Load the image
            image = gui_image_studio.get_image(input_path)

            # Save in new format
            gui_image_studio.save_image(image, output_path)

            print(f"Successfully converted {input_path} to {output_path}")
            return True

        except FileNotFoundError:
            print(f"Error: Could not find input file {input_path}")
            return False
        except Exception as e:
            print(f"Error converting image: {e}")
            return False

    # Example usage
    if __name__ == "__main__":
        # Convert JPEG to PNG
        convert_image_format("sample_images/sample_photo.jpg", "output.png")

        # Convert PNG to JPEG
        convert_image_format("sample_images/sample_icon.png", "output.jpg")

**Loading with Error Handling**

.. code-block:: python

    # Example: Robust Image Loading with Error Handling
    # Shows how to handle various error conditions when loading images.

    import gui_image_studio
    import os
    from typing import Optional
    from PIL import Image

    def safe_load_image(image_path: str, fallback_color: str = "#CCCCCC") -> Optional[Image.Image]:
        """
        Safely load an image with comprehensive error handling.

        Args:
            image_path: Path to the image file
            fallback_color: Color to use if loading fails

        Returns:
            PIL Image object or None if all attempts fail
        """
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"Warning: File {image_path} does not exist")
            return None

        # Check file size
        file_size = os.path.getsize(image_path)
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            print(f"Warning: File {image_path} is very large ({file_size / 1024 / 1024:.1f}MB)")

        try:
            # Attempt to load the image
            image = gui_image_studio.get_image(image_path)
            print(f"Successfully loaded {image_path} ({image.size[0]}x{image.size[1]})")
            return image

        except gui_image_studio.PIL.UnidentifiedImageError:
            print(f"Error: {image_path} is not a valid image file")
            return None
        except MemoryError:
            print(f"Error: Not enough memory to load {image_path}")
            return None
        except PermissionError:
            print(f"Error: Permission denied accessing {image_path}")
            return None
        except Exception as e:
            print(f"Unexpected error loading {image_path}: {e}")
            return None

    # Example usage
    if __name__ == "__main__":
        test_files = [
            "sample_images/sample_photo.jpg",
            "sample_images/sample_icon.png",
            "nonexistent_file.jpg",
            "sample_images/sample_animation.gif"
        ]

        for file_path in test_files:
            image = safe_load_image(file_path)
            if image:
                print(f"  Format: {image.format}, Mode: {image.mode}")
            print()

Basic Image Transformations
----------------------------

These examples show how to perform common image transformations.

**Resizing Images**

.. code-block:: python

    # Example: Image Resizing Operations
    # Demonstrates different ways to resize images while maintaining quality.

    import gui_image_studio
    from typing import Tuple

    def resize_image_examples():
        """Demonstrate various image resizing techniques."""

        # Load a sample image
        image = gui_image_studio.get_image("sample_images/sample_photo.jpg")
        original_size = image.size
        print(f"Original size: {original_size[0]}x{original_size[1]}")

        # 1. Resize to exact dimensions
        resized_exact = gui_image_studio.resize_image(image, (800, 600))
        gui_image_studio.save_image(resized_exact, "resized_exact.jpg")
        print("Saved: resized_exact.jpg (800x600)")

        # 2. Resize maintaining aspect ratio (fit within bounds)
        def resize_maintain_aspect(img, max_size: Tuple[int, int]) -> Tuple[int, int]:
            """Calculate new size maintaining aspect ratio."""
            width, height = img.size
            max_width, max_height = max_size

            # Calculate scaling factor
            scale = min(max_width / width, max_height / height)

            new_width = int(width * scale)
            new_height = int(height * scale)

            return (new_width, new_height)

        new_size = resize_maintain_aspect(image, (800, 600))
        resized_aspect = gui_image_studio.resize_image(image, new_size)
        gui_image_studio.save_image(resized_aspect, "resized_aspect.jpg")
        print(f"Saved: resized_aspect.jpg ({new_size[0]}x{new_size[1]})")

        # 3. Create thumbnail
        thumbnail_size = (150, 150)
        thumb_size = resize_maintain_aspect(image, thumbnail_size)
        thumbnail = gui_image_studio.resize_image(image, thumb_size)
        gui_image_studio.save_image(thumbnail, "thumbnail.jpg")
        print(f"Saved: thumbnail.jpg ({thumb_size[0]}x{thumb_size[1]})")

        # 4. Scale by percentage
        scale_factor = 0.5  # 50% of original size
        scaled_size = (int(original_size[0] * scale_factor),
                      int(original_size[1] * scale_factor))
        scaled = gui_image_studio.resize_image(image, scaled_size)
        gui_image_studio.save_image(scaled, "scaled_50percent.jpg")
        print(f"Saved: scaled_50percent.jpg ({scaled_size[0]}x{scaled_size[1]})")

    if __name__ == "__main__":
        resize_image_examples()

**Applying Color Tints**

.. code-block:: python

    # Example: Color Tinting Operations
    # Shows how to apply various color tints and effects to images.

    import gui_image_studio

    def color_tinting_examples():
        """Demonstrate different color tinting techniques."""

        # Load a sample image
        image = gui_image_studio.get_image("sample_images/sample_photo.jpg")

        # Define color palette
        colors = {
            "warm_red": "#FF6B6B",
            "cool_blue": "#4ECDC4",
            "vintage_sepia": "#D2B48C",
            "forest_green": "#2ECC71",
            "sunset_orange": "#FF8C42",
            "royal_purple": "#9B59B6"
        }

        print("Applying color tints...")

        for name, color in colors.items():
            # Apply tint
            tinted = gui_image_studio.apply_tint(image, color)

            # Save with descriptive filename
            filename = f"tinted_{name}.jpg"
            gui_image_studio.save_image(tinted, filename)
            print(f"Saved: {filename} (tint: {color})")

        # Create a comparison grid (if you have PIL available)
        try:
            from PIL import Image

            # Load all tinted images
            tinted_images = []
            for name in colors.keys():
                tinted_img = gui_image_studio.get_image(f"tinted_{name}.jpg")
                # Resize for grid
                tinted_img = gui_image_studio.resize_image(tinted_img, (200, 150))
                tinted_images.append(tinted_img)

            # Create 2x3 grid
            grid_width = 200 * 3
            grid_height = 150 * 2
            grid = Image.new('RGB', (grid_width, grid_height), 'white')

            for i, img in enumerate(tinted_images):
                x = (i % 3) * 200
                y = (i // 3) * 150
                grid.paste(img, (x, y))

            gui_image_studio.save_image(grid, "tint_comparison_grid.jpg")
            print("Saved: tint_comparison_grid.jpg (comparison grid)")

        except ImportError:
            print("PIL not available for grid creation")

    if __name__ == "__main__":
        color_tinting_examples()

**Rotating and Flipping Images**

.. code-block:: python

    # Example: Image Rotation and Flipping
    # Demonstrates geometric transformations like rotation and flipping.

    import gui_image_studio

    def geometric_transformations():
        """Demonstrate rotation and flipping operations."""

        # Load a sample image
        image = gui_image_studio.get_image("sample_images/sample_icon.png")

        print("Applying geometric transformations...")

        # Rotation examples
        rotation_angles = [90, 180, 270, 45, -45]

        for angle in rotation_angles:
            rotated = gui_image_studio.rotate_image(image, angle)
            filename = f"rotated_{angle}deg.png"
            gui_image_studio.save_image(rotated, filename)
            print(f"Saved: {filename}")

        # Flipping examples
        flip_operations = [
            ("horizontal", True, False),
            ("vertical", False, True),
            ("both", True, True)
        ]

        for name, horizontal, vertical in flip_operations:
            flipped = gui_image_studio.flip_image(image,
                                                horizontal=horizontal,
                                                vertical=vertical)
            filename = f"flipped_{name}.png"
            gui_image_studio.save_image(flipped, filename)
            print(f"Saved: {filename}")

        # Combined transformations
        # Rotate and then flip
        rotated_flipped = gui_image_studio.rotate_image(image, 45)
        rotated_flipped = gui_image_studio.flip_image(rotated_flipped, horizontal=True)
        gui_image_studio.save_image(rotated_flipped, "rotated_45_flipped_h.png")
        print("Saved: rotated_45_flipped_h.png (combined transformation)")

    if __name__ == "__main__":
        geometric_transformations()

Working with Different Image Formats
-------------------------------------

**Format Conversion and Optimization**

.. code-block:: python

    # Example: Image Format Conversion and Optimization
    # Shows how to convert between different image formats and optimize file sizes.

    import gui_image_studio
    import os

    def format_conversion_examples():
        """Demonstrate format conversion and optimization."""

        # Load a sample image
        image = gui_image_studio.get_image("sample_images/sample_photo.jpg")

        print("Converting to different formats...")

        # Save as PNG (lossless)
        gui_image_studio.save_image(image, "converted.png")
        png_size = os.path.getsize("converted.png")
        print(f"PNG: {png_size / 1024:.1f} KB")

        # Save as JPEG with different quality levels
        quality_levels = [95, 85, 75, 60, 40]

        for quality in quality_levels:
            filename = f"converted_q{quality}.jpg"
            gui_image_studio.save_image(image, filename, quality=quality)
            file_size = os.path.getsize(filename)
            print(f"JPEG Q{quality}: {file_size / 1024:.1f} KB")

        # Save as WebP (if supported)
        try:
            gui_image_studio.save_image(image, "converted.webp")
            webp_size = os.path.getsize("converted.webp")
            print(f"WebP: {webp_size / 1024:.1f} KB")
        except Exception as e:
            print(f"WebP not supported: {e}")

        # Create optimized versions
        # Small thumbnail
        thumbnail = gui_image_studio.resize_image(image, (150, 150))
        gui_image_studio.save_image(thumbnail, "thumbnail_optimized.jpg", quality=80)
        thumb_size = os.path.getsize("thumbnail_optimized.jpg")
        print(f"Optimized thumbnail: {thumb_size / 1024:.1f} KB")

    if __name__ == "__main__":
        format_conversion_examples()

Batch Processing Basics
------------------------

**Processing Multiple Images**

.. code-block:: python

    # Example: Basic Batch Processing
    # Shows how to process multiple images with the same operations.

    import gui_image_studio
    import os
    from typing import List

    def batch_process_images(input_folder: str, output_folder: str,
                           operations: List[str] = None):
        """
        Process all images in a folder with specified operations.

        Args:
            input_folder: Folder containing input images
            output_folder: Folder for processed images
            operations: List of operations to perform
        """
        if operations is None:
            operations = ["resize", "tint"]

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Supported image extensions
        supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')

        # Find all image files
        image_files = []
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(supported_extensions):
                image_files.append(filename)

        print(f"Found {len(image_files)} images to process")

        # Process each image
        for i, filename in enumerate(image_files, 1):
            print(f"Processing {i}/{len(image_files)}: {filename}")

            try:
                # Load image
                input_path = os.path.join(input_folder, filename)
                image = gui_image_studio.get_image(input_path)

                # Apply operations
                processed_image = image

                if "resize" in operations:
                    # Resize to max 800x600 maintaining aspect ratio
                    width, height = processed_image.size
                    if width > 800 or height > 600:
                        scale = min(800 / width, 600 / height)
                        new_size = (int(width * scale), int(height * scale))
                        processed_image = gui_image_studio.resize_image(processed_image, new_size)

                if "tint" in operations:
                    # Apply a subtle blue tint
                    processed_image = gui_image_studio.apply_tint(processed_image, "#4ECDC4")

                # Save processed image
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_processed{ext}"
                output_path = os.path.join(output_folder, output_filename)
                gui_image_studio.save_image(processed_image, output_path)

                print(f"  Saved: {output_filename}")

            except Exception as e:
                print(f"  Error processing {filename}: {e}")

        print("Batch processing complete!")

    if __name__ == "__main__":
        # Process sample images
        batch_process_images("sample_images", "processed_images",
                           operations=["resize", "tint"])

Running the Examples
--------------------

To run these examples:

1. **Create sample images first:**

   .. code-block:: bash

       gui-image-studio-create-samples

2. **Run individual examples:**

   .. code-block:: bash

       python basic_load_save.py
       python resize_examples.py
       python tinting_examples.py

3. **Check the output files** in your current directory

Each example is self-contained and includes error handling to make it robust for real-world use.

Next Steps
----------

After mastering these basic operations, you can:

* Explore :doc:`image_processing` for advanced filtering and effects
* Learn about :doc:`animation_creation` for working with animated GIFs
* Check out :doc:`gui_application` for building complete image editing applications
* Try :doc:`batch_processing` for automating image workflows
