Generator Module
================

The ``generator`` module provides functionality for creating embedded image resources and generating Python code for image distribution.

.. automodule:: gui_image_studio.generator
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The generator module allows you to:

* Convert images to base64-encoded strings
* Generate Python modules with embedded images
* Create optimized image resources for distribution
* Batch process image folders

This is particularly useful for:

* Distributing applications with embedded icons
* Creating self-contained packages
* Reducing external dependencies
* Improving application startup time

Main Functions
--------------

embed_images_from_folder
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.generator.embed_images_from_folder

The main function for generating embedded image resources from a folder.

**Basic Usage:**

.. code-block:: python

    from gui_image_studio import embed_images_from_folder

    # Generate embedded images from a folder
    embed_images_from_folder(
        folder_path="assets/icons",
        output_file="embedded_icons.py",
        compression_quality=85
    )

**Parameters:**

* ``folder_path`` (str): Path to the folder containing images
* ``output_file`` (str): Name of the generated Python file (default: "embedded_images.py")
* ``compression_quality`` (int): JPEG/WebP quality 1-100 (default: 85)

**Methods:**

generate
^^^^^^^^

.. automethod:: gui_image_studio.generator.ImageGenerator.generate

Generate the embedded images Python module.

**Returns:**
  * ``bool``: True if generation was successful

**Example:**

.. code-block:: python

    success = generator.generate()
    if success:
        print("Resources generated successfully")
    else:
        print("Generation failed")

add_image
^^^^^^^^^

.. automethod:: gui_image_studio.generator.ImageGenerator.add_image

Add a single image to the generator.

**Parameters:**
  * ``image_path`` (str): Path to the image file
  * ``name`` (str, optional): Name for the embedded image (defaults to filename)

**Example:**

.. code-block:: python

    generator.add_image("icon.png", "main_icon")
    generator.add_image("logo.jpg")  # Uses "logo" as name

remove_image
^^^^^^^^^^^^

.. automethod:: gui_image_studio.generator.ImageGenerator.remove_image

Remove an image from the generator.

**Parameters:**
  * ``name`` (str): Name of the image to remove

**Example:**

.. code-block:: python

    generator.remove_image("unwanted_icon")

list_images
^^^^^^^^^^^

.. automethod:: gui_image_studio.generator.ImageGenerator.list_images

List all images currently in the generator.

**Returns:**
  * ``List[str]``: List of image names

**Example:**

.. code-block:: python

    images = generator.list_images()
    print(f"Images to embed: {', '.join(images)}")

set_compression
^^^^^^^^^^^^^^^

.. automethod:: gui_image_studio.generator.ImageGenerator.set_compression

Configure image compression settings.

**Parameters:**
  * ``compress`` (bool): Enable compression
  * ``quality`` (int): JPEG quality (1-100)
  * ``max_size`` (Tuple[int, int], optional): Maximum image size

**Example:**

.. code-block:: python

    generator.set_compression(True, quality=75, max_size=(256, 256))

Utility Functions
-----------------

encode_image
~~~~~~~~~~~~

.. autofunction:: gui_image_studio.generator.encode_image

Encode a single image to base64 string.

**Parameters:**
  * ``image_path`` (str): Path to the image file
  * ``format`` (str, optional): Output format ('base64' or 'bytes')
  * ``compress`` (bool, optional): Apply compression
  * ``quality`` (int, optional): JPEG quality for compression

**Returns:**
  * ``str``: Encoded image data

**Example:**

.. code-block:: python

    encoded = encode_image("icon.png", format="base64")
    print(f"Encoded size: {len(encoded)} characters")

decode_image
~~~~~~~~~~~~

.. autofunction:: gui_image_studio.generator.decode_image

Decode a base64 string back to PIL Image.

**Parameters:**
  * ``encoded_data`` (str): Base64 encoded image data

**Returns:**
  * ``PIL.Image.Image``: Decoded image

**Example:**

.. code-block:: python

    from PIL import Image

    encoded = encode_image("icon.png")
    image = decode_image(encoded)
    print(f"Decoded image size: {image.size}")

compress_image
~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.generator.compress_image

Compress an image with specified settings.

**Parameters:**
  * ``image`` (PIL.Image.Image): Image to compress
  * ``quality`` (int): JPEG quality (1-100)
  * ``max_size`` (Tuple[int, int], optional): Maximum dimensions

**Returns:**
  * ``PIL.Image.Image``: Compressed image

**Example:**

.. code-block:: python

    from gui_image_studio import get_image

    image = get_image("large_photo.jpg")
    compressed = compress_image(image, quality=70, max_size=(800, 600))

validate_image
~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.generator.validate_image

Validate that a file is a supported image format.

**Parameters:**
  * ``image_path`` (str): Path to the image file

**Returns:**
  * ``bool``: True if image is valid and supported

**Example:**

.. code-block:: python

    if validate_image("unknown_file.xyz"):
        print("Valid image file")
    else:
        print("Invalid or unsupported image")

Generated Code Structure
------------------------

The generator creates Python modules with the following structure:

**Basic Generated Module:**

.. code-block:: python

    """
    Embedded images for GUI Image Studio
    Generated on: 2024-06-22 10:30:00
    Source folder: assets/icons
    Total images: 5
    """

    import base64
    from io import BytesIO
    from PIL import Image
    from typing import Dict, List, Optional

    # Image metadata
    METADATA = {
        'generated_on': '2024-06-22 10:30:00',
        'source_folder': 'assets/icons',
        'total_images': 5,
        'compression': True,
        'quality': 85
    }

    # Image data dictionary
    IMAGES: Dict[str, str] = {
        'icon_home': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQ...',
        'icon_save': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQ...',
        'icon_open': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQ...',
        'logo_main': '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAA...',
        'background': 'iVBORw0KGgoAAAANSUhEUgAAAQAAAAEA...',
    }

    def get_image(name: str) -> Image.Image:
        """
        Get embedded image by name.

        Args:
            name: Name of the image to retrieve

        Returns:
            PIL Image object

        Raises:
            KeyError: If image name is not found
            ValueError: If image data is corrupted
        """
        if name not in IMAGES:
            available = ', '.join(list_images())
            raise KeyError(f"Image '{name}' not found. Available: {available}")

        try:
            data = base64.b64decode(IMAGES[name])
            return Image.open(BytesIO(data))
        except Exception as e:
            raise ValueError(f"Failed to decode image '{name}': {e}")

    def list_images() -> List[str]:
        """
        List all available embedded images.

        Returns:
            List of image names
        """
        return list(IMAGES.keys())

    def get_image_info(name: str) -> Dict[str, any]:
        """
        Get information about an embedded image.

        Args:
            name: Name of the image

        Returns:
            Dictionary with image information
        """
        if name not in IMAGES:
            raise KeyError(f"Image '{name}' not found")

        image = get_image(name)
        return {
            'name': name,
            'size': image.size,
            'mode': image.mode,
            'format': image.format,
            'encoded_size': len(IMAGES[name])
        }

    def save_image(name: str, output_path: str) -> bool:
        """
        Save an embedded image to file.

        Args:
            name: Name of the embedded image
            output_path: Path where to save the image

        Returns:
            True if successful
        """
        try:
            image = get_image(name)
            image.save(output_path)
            return True
        except Exception:
            return False

Configuration Options
---------------------

**Compression Settings:**

.. code-block:: python

    generator = ImageGenerator("assets")

    # Enable compression with quality setting
    generator.set_compression(True, quality=85)

    # Set maximum image size
    generator.set_compression(True, max_size=(512, 512))

    # Disable compression for lossless embedding
    generator.set_compression(False)

**Format Filtering:**

.. code-block:: python

    # Only include specific formats
    generator = ImageGenerator(
        "assets",
        formats=['png', 'jpg']  # Exclude GIF, BMP, etc.
    )

**Custom Naming:**

.. code-block:: python

    # Custom name mapping
    generator.add_image("icons/home-24px.png", "icon_home")
    generator.add_image("icons/save-24px.png", "icon_save")

**Output Customization:**

.. code-block:: python

    generator = ImageGenerator(
        input_folder="assets",
        output_file="my_resources.py",
        module_name="my_resources",
        template_file="custom_template.py"  # Use custom template
    )

Advanced Usage
--------------

**Batch Processing Multiple Folders:**

.. code-block:: python

    from gui_image_studio.generator import ImageGenerator

    def generate_all_resources():
        """Generate resources from multiple folders."""

        # Icons
        icon_gen = ImageGenerator("assets/icons", "icons.py", "icons")
        icon_gen.set_compression(True, quality=95, max_size=(64, 64))
        icon_gen.generate()

        # Images
        image_gen = ImageGenerator("assets/images", "images.py", "images")
        image_gen.set_compression(True, quality=80, max_size=(512, 512))
        image_gen.generate()

        # Backgrounds
        bg_gen = ImageGenerator("assets/backgrounds", "backgrounds.py", "backgrounds")
        bg_gen.set_compression(True, quality=70, max_size=(1024, 768))
        bg_gen.generate()

**Custom Template:**

.. code-block:: python

    # Create custom template file
    template = '''"""Custom embedded images module
    Generated: 2024-01-01 12:00:00
    """

    IMAGES = {}

    def get_image(name):
        """Custom implementation"""
        return IMAGES.get(name)
    '''

    generator = ImageGenerator("assets", template=template)

**Progress Tracking:**

.. code-block:: python

    class ProgressGenerator(ImageGenerator):
        def generate(self):
            images = self.list_images()
            total = len(images)

            for i, name in enumerate(images, 1):
                print(f"Processing {i}/{total}: {name}")
                # Process image...

            return super().generate()

**Integration with Build Systems:**

.. code-block:: python

    # setup.py integration
    from gui_image_studio.generator import ImageGenerator

    def build_resources():
        """Build embedded resources during package build."""
        generator = ImageGenerator("src/assets", "src/resources.py")
        if not generator.generate():
            raise RuntimeError("Failed to generate resources")

    # Call during build
    build_resources()

Error Handling
--------------

**Common Exceptions:**

* ``FileNotFoundError``: Input folder or image files not found
* ``PermissionError``: Cannot write to output file
* ``ValueError``: Invalid image format or corrupted data
* ``MemoryError``: Image too large to process

**Error Handling Example:**

.. code-block:: python

    try:
        generator = ImageGenerator("assets", "resources.py")
        generator.generate()
    except FileNotFoundError as e:
        print(f"Input folder not found: {e}")
    except PermissionError as e:
        print(f"Cannot write output file: {e}")
    except ValueError as e:
        print(f"Invalid image data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

**Validation:**

.. code-block:: python

    # Validate before generation
    generator = ImageGenerator("assets")

    # Check input folder exists
    if not os.path.exists(generator.input_folder):
        raise FileNotFoundError(f"Input folder not found: {generator.input_folder}")

    # Check for valid images
    valid_images = [img for img in generator.list_images()
                    if validate_image(os.path.join(generator.input_folder, img))]

    if not valid_images:
        raise ValueError("No valid images found in input folder")

Performance Considerations
--------------------------

**Memory Usage:**

* Large images consume significant memory during encoding
* Consider using compression and size limits
* Process images in batches for large folders

**File Size:**

* Base64 encoding increases size by ~33%
* Compression can significantly reduce embedded size
* Balance quality vs. file size based on use case

**Generation Time:**

* Compression adds processing time
* Large images take longer to encode
* Consider parallel processing for large batches

**Optimization Tips:**

.. code-block:: python

    # Optimize for size
    generator.set_compression(True, quality=60, max_size=(256, 256))

    # Optimize for quality
    generator.set_compression(True, quality=95, max_size=(1024, 1024))

    # No compression for small images
    import os
    image_files = [os.path.join(generator.input_folder, f) for f in generator.list_images()]
    total_size = sum(os.path.getsize(f) for f in image_files if os.path.exists(f))
    if total_size < 1024 * 1024:  # 1MB
        generator.set_compression(False)

**Best Practices:**

* Use compression for distribution packages
* Test different quality settings for your use case
* Monitor memory usage with large image sets
* Consider using multiple smaller generators for very large projects
* Validate generated modules before deployment

**Troubleshooting:**

Common issues and solutions:

* **Out of memory**: Reduce image sizes or process in batches
* **Slow generation**: Enable compression and reduce quality
* **Large output files**: Use higher compression and smaller max_size
* **Import errors**: Check that all dependencies are installed

For more information, see the :doc:`../examples/index` and :doc:`../user_guide/index`.
