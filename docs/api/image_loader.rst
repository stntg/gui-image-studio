Image Loader Module
===================

The ``image_loader`` module provides core functionality for loading, processing, and saving images.

.. automodule:: gui_image_studio.image_loader
   :members:
   :undoc-members:
   :show-inheritance:

Core Functions
--------------

get_image
~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.get_image

Load images from various sources including files, embedded resources, and URLs.

**Parameters:**
  * ``image_name`` (str): Path to image file or embedded resource name
  * ``fallback_color`` (str, optional): Color to use if image loading fails

**Returns:**
  * ``PIL.Image.Image``: Loaded image object

**Raises:**
  * ``FileNotFoundError``: If image file is not found
  * ``PIL.UnidentifiedImageError``: If image format is not supported

**Examples:**

.. code-block:: python

   # Load from file
   image = get_image("photo.jpg")

   # Load embedded resource
   icon = get_image("sample_icon")

   # Load with fallback
   image = get_image("might_not_exist.png", fallback_color="#FF0000")

save_image
~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.save_image

Save images to files in various formats.

**Parameters:**
  * ``image`` (PIL.Image.Image): Image to save
  * ``output_path`` (str): Path where to save the image
  * ``quality`` (int, optional): JPEG quality (1-100, default 95)
  * ``optimize`` (bool, optional): Optimize file size (default True)

**Examples:**

.. code-block:: python

   # Save as PNG
   save_image(image, "output.png")

   # Save as JPEG with specific quality
   save_image(image, "output.jpg", quality=85)

   # Save optimized GIF
   save_image(animated_image, "output.gif", optimize=True)

Image Processing Functions
--------------------------

resize_image
~~~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.resize_image

Resize images while maintaining quality.

**Parameters:**
  * ``image`` (PIL.Image.Image): Source image
  * ``size`` (Tuple[int, int]): Target size (width, height)
  * ``resample`` (int, optional): Resampling algorithm (default LANCZOS)
  * ``maintain_aspect`` (bool, optional): Maintain aspect ratio (default False)

**Examples:**

.. code-block:: python

   # Resize to exact dimensions
   resized = resize_image(image, (800, 600))

   # Resize maintaining aspect ratio
   resized = resize_image(image, (800, 600), maintain_aspect=True)

apply_tint
~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.apply_tint

Apply color tints to images.

**Parameters:**
  * ``image`` (PIL.Image.Image): Source image
  * ``color`` (str): Tint color (hex string, RGB tuple, or color name)
  * ``opacity`` (float, optional): Tint opacity (0.0-1.0, default 0.3)
  * ``blend_mode`` (str, optional): Blending mode (default "multiply")

**Examples:**

.. code-block:: python

   # Apply red tint
   tinted = apply_tint(image, "#FF0000")

   # Apply blue tint with custom opacity
   tinted = apply_tint(image, "blue", opacity=0.5)

   # Apply tint with overlay blend mode
   tinted = apply_tint(image, "#00FF00", blend_mode="overlay")

rotate_image
~~~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.rotate_image

Rotate images by specified angles.

**Parameters:**
  * ``image`` (PIL.Image.Image): Source image
  * ``angle`` (float): Rotation angle in degrees
  * ``expand`` (bool, optional): Expand canvas to fit rotated image (default True)
  * ``fillcolor`` (str, optional): Background color for empty areas

**Examples:**

.. code-block:: python

   # Rotate 90 degrees clockwise
   rotated = rotate_image(image, 90)

   # Rotate 45 degrees with white background
   rotated = rotate_image(image, 45, fillcolor="white")

flip_image
~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.flip_image

Flip images horizontally or vertically.

**Parameters:**
  * ``image`` (PIL.Image.Image): Source image
  * ``horizontal`` (bool, optional): Flip horizontally (default False)
  * ``vertical`` (bool, optional): Flip vertically (default False)

**Examples:**

.. code-block:: python

   # Flip horizontally
   flipped = flip_image(image, horizontal=True)

   # Flip vertically
   flipped = flip_image(image, vertical=True)

   # Flip both ways
   flipped = flip_image(image, horizontal=True, vertical=True)

Advanced Functions
------------------

apply_filter
~~~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.apply_filter

Apply various image filters and effects.

**Parameters:**
  * ``image`` (PIL.Image.Image): Source image
  * ``filter_type`` (str): Filter type ("blur", "sharpen", "emboss", etc.)
  * ``intensity`` (float, optional): Filter intensity (0.0-1.0, default 1.0)

**Examples:**

.. code-block:: python

   # Apply blur filter
   blurred = apply_filter(image, "blur", intensity=0.5)

   # Apply sharpen filter
   sharpened = apply_filter(image, "sharpen")

adjust_brightness
~~~~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.adjust_brightness

Adjust image brightness and contrast.

**Parameters:**
  * ``image`` (PIL.Image.Image): Source image
  * ``brightness`` (float, optional): Brightness factor (1.0 = no change)
  * ``contrast`` (float, optional): Contrast factor (1.0 = no change)

**Examples:**

.. code-block:: python

   # Increase brightness
   brighter = adjust_brightness(image, brightness=1.2)

   # Increase contrast
   contrasted = adjust_brightness(image, contrast=1.3)

   # Adjust both
   adjusted = adjust_brightness(image, brightness=1.1, contrast=1.2)

Utility Functions
-----------------

get_image_info
~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.get_image_info

Get detailed information about an image.

**Parameters:**
  * ``image`` (PIL.Image.Image): Image to analyze

**Returns:**
  * ``dict``: Dictionary containing image information

**Examples:**

.. code-block:: python

   info = get_image_info(image)
   print(f"Size: {info['size']}")
   print(f"Format: {info['format']}")
   print(f"Mode: {info['mode']}")

is_animated
~~~~~~~~~~~

.. autofunction:: gui_image_studio.image_loader.is_animated

Check if an image is animated (e.g., animated GIF).

**Parameters:**
  * ``image`` (PIL.Image.Image): Image to check

**Returns:**
  * ``bool``: True if image is animated

**Examples:**

.. code-block:: python

   if is_animated(image):
       print("This is an animated image")
   else:
       print("This is a static image")

Constants
---------

**Supported Formats**

.. code-block:: python

   SUPPORTED_INPUT_FORMATS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.ico']
   SUPPORTED_OUTPUT_FORMATS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp']

**Default Settings**

.. code-block:: python

   DEFAULT_QUALITY = 95
   DEFAULT_RESAMPLE = Image.LANCZOS
   DEFAULT_TINT_OPACITY = 0.3

**Color Constants**

.. code-block:: python

   TRANSPARENT = (0, 0, 0, 0)
   WHITE = (255, 255, 255)
   BLACK = (0, 0, 0)

Error Handling
--------------

The image_loader module provides comprehensive error handling:

**Common Exceptions:**

* ``FileNotFoundError``: Image file not found
* ``PIL.UnidentifiedImageError``: Unsupported image format
* ``ValueError``: Invalid parameter values
* ``MemoryError``: Image too large to process
* ``PermissionError``: Insufficient permissions to read/write file

**Error Handling Example:**

.. code-block:: python

   try:
       image = get_image("photo.jpg")
       processed = apply_tint(image, "#FF0000")
       save_image(processed, "output.png")
   except FileNotFoundError:
       print("Image file not found")
   except PIL.UnidentifiedImageError:
       print("Unsupported image format")
   except Exception as e:
       print(f"Unexpected error: {e}")

Performance Notes
-----------------

**Memory Usage:**
  Large images consume significant memory. Consider resizing before processing multiple operations.

**Processing Speed:**
  Complex filters and transformations may take time with large images. Consider showing progress indicators for long operations.

**File I/O:**
  Loading and saving images involves disk I/O. Cache frequently used images in memory when possible.

**Threading:**
  Most functions are thread-safe for read operations, but be careful with concurrent write operations.
