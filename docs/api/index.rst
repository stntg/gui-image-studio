API Reference
=============

Complete API documentation for all GUI Image Studio classes and functions.

.. toctree::
   :maxdepth: 2
   :caption: API Modules:

   image_loader
   image_studio
   generator
   sample_creator
   cli

Overview
--------

The GUI Image Studio API is organized into several modules:

Core Image Processing
~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.get_image

GUI Application
~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.launch_designer

Resource Generation
~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.embed_images_from_folder

Sample Creation
~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.create_sample_images

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.cli.generate_embedded_images
   gui_image_studio.cli.create_sample_images
   gui_image_studio.cli.launch_designer

Quick Reference
---------------

Most Common Functions
~~~~~~~~~~~~~~~~~~~~~

For most applications, you'll primarily use these functions:

.. code-block:: python

   from gui_image_studio import (
       get_image,                    # Load images from files or resources
       embed_images_from_folder,     # Generate embedded images
       create_sample_images,         # Create sample images
       launch_designer,              # Launch GUI designer
   )

Basic Usage Pattern
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import gui_image_studio

   # Load an image with transformations
   image = gui_image_studio.get_image(
       "path/to/image.png",
       framework="tkinter",
       size=(800, 600),
       tint_color=(255, 107, 107),
       tint_intensity=0.3
   )

   # Create sample images
   gui_image_studio.create_sample_images()

   # Generate embedded images from folder
   gui_image_studio.embed_images_from_folder("images/", "embedded.py")

Common Parameters
~~~~~~~~~~~~~~~~~

Most functions accept these common parameters:

* ``image`` - PIL Image object or path to image file
* ``size`` - Tuple of (width, height) for dimensions
* ``color`` - Color specification (hex string, RGB tuple, or color name)
* ``output_path`` - Path where to save the processed image
* ``quality`` - JPEG quality (1-100, default 95)

Image Format Support
~~~~~~~~~~~~~~~~~~~~

**Supported Input Formats:**
  PNG, JPEG, GIF, BMP, TIFF, WebP, ICO

**Supported Output Formats:**
  PNG, JPEG, GIF, BMP, TIFF, WebP

**Animation Support:**
  GIF (with frame timing and optimization)

Error Handling
~~~~~~~~~~~~~~

All functions raise appropriate exceptions for invalid parameters:

* ``FileNotFoundError`` - Image file not found
* ``ValueError`` - Invalid parameter values
* ``TypeError`` - Wrong parameter types
* ``PIL.UnidentifiedImageError`` - Unsupported image format
* ``MemoryError`` - Image too large to process

Type Hints
~~~~~~~~~~

All public APIs include comprehensive type hints for better IDE support and static analysis:

.. code-block:: python

   from typing import Tuple, Union, Optional
   from PIL import Image

   def resize_image(
       image: Union[Image.Image, str],
       size: Tuple[int, int],
       resample: int = Image.LANCZOS
   ) -> Image.Image:
       """Resize an image to the specified dimensions."""

Configuration
~~~~~~~~~~~~~

Global configuration options:

.. code-block:: python

   import gui_image_studio

   # Set default image quality
   gui_image_studio.set_default_quality(90)

   # Set default theme
   gui_image_studio.set_theme("dark")

   # Enable/disable verbose logging
   gui_image_studio.set_verbose(True)

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Memory Usage:**
  Large images consume significant memory. Consider resizing before processing.

**Processing Speed:**
  Complex operations may take time with large images. Use progress callbacks when available.

**File I/O:**
  Loading and saving images involves disk I/O. Cache frequently used images in memory.

**Threading:**
  GUI operations must run on the main thread. Use worker threads for heavy processing.

Examples by Category
--------------------

**Basic Image Loading**

.. code-block:: python

   # Load from file
   image = gui_image_studio.get_image("photo.jpg")

   # Load from embedded resources
   image = gui_image_studio.get_image("sample_icon")

   # Load with error handling
   try:
       image = gui_image_studio.get_image("might_not_exist.png")
   except FileNotFoundError:
       print("Image not found")

**Image Transformations**

.. code-block:: python

   # Load image with transformations applied
   resized = gui_image_studio.get_image(
       "image.png",
       size=(800, 600)
   )

   # Apply color effects
   tinted = gui_image_studio.get_image(
       "image.png",
       tint_color=(255, 107, 107),
       tint_intensity=0.3
   )

   # Geometric transformations
   rotated = gui_image_studio.get_image(
       "image.png",
       rotate=45
   )

**Batch Processing**

.. code-block:: python

   # Generate embedded images from a folder
   gui_image_studio.embed_images_from_folder(
       "input_images/",
       "embedded_images.py",
       compression_quality=85
   )

   # Create sample images for testing
   gui_image_studio.create_sample_images()

**GUI Integration**

.. code-block:: python

   import tkinter as tk
   import gui_image_studio

   # Launch the GUI designer
   gui_image_studio.launch_designer()

   # Or use images in your own GUI
   root = tk.Tk()
   image = gui_image_studio.get_image(
       "icon.png",
       framework="tkinter",
       size=(64, 64)
   )
   label = tk.Label(root, image=image)
   label.pack()
   root.mainloop()

Migration Guide
---------------

**From Version 0.x to 1.0**

* Function names have been standardized
* Error handling has been improved
* Type hints have been added throughout
* Some deprecated functions have been removed

**Key Changes**

* Simplified API with focus on ``get_image()`` function
* All image transformations now handled through ``get_image()`` parameters
* Embedded image generation through ``embed_images_from_folder()``
* GUI designer accessible via ``launch_designer()``
