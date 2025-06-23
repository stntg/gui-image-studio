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
   gui_image_studio.save_image
   gui_image_studio.resize_image
   gui_image_studio.apply_tint
   gui_image_studio.rotate_image
   gui_image_studio.flip_image

GUI Application
~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.ImageStudio
   gui_image_studio.launch_designer

Resource Generation
~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.ImageGenerator
   gui_image_studio.generate_embedded_images

Sample Creation
~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.SampleCreator
   gui_image_studio.create_samples

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   gui_image_studio.cli.main
   gui_image_studio.cli.designer_main
   gui_image_studio.cli.generator_main
   gui_image_studio.cli.samples_main

Quick Reference
---------------

Most Common Functions
~~~~~~~~~~~~~~~~~~~~~

For most applications, you'll primarily use these functions:

.. code-block:: python

   from gui_image_studio import (
       get_image,           # Load images from files or resources
       save_image,          # Save images to files
       resize_image,        # Resize images
       apply_tint,          # Apply color tints
       ImageStudio,         # Main GUI application class
   )

Basic Usage Pattern
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import gui_image_studio

   # Load an image
   image = gui_image_studio.get_image("path/to/image.png")
   
   # Process the image
   processed = gui_image_studio.apply_tint(image, "#FF6B6B")
   resized = gui_image_studio.resize_image(processed, (800, 600))
   
   # Save the result
   gui_image_studio.save_image(resized, "output.png")

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

   # Resize maintaining aspect ratio
   resized = gui_image_studio.resize_image(image, (800, 600))
   
   # Apply color effects
   tinted = gui_image_studio.apply_tint(image, "#FF6B6B")
   
   # Geometric transformations
   rotated = gui_image_studio.rotate_image(image, 45)
   flipped = gui_image_studio.flip_image(image, horizontal=True)

**Batch Processing**

.. code-block:: python

   import os
   
   input_folder = "input_images/"
   output_folder = "processed_images/"
   
   for filename in os.listdir(input_folder):
       if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
           image = gui_image_studio.get_image(os.path.join(input_folder, filename))
           processed = gui_image_studio.apply_tint(image, "#FF6B6B")
           output_path = os.path.join(output_folder, f"tinted_{filename}")
           gui_image_studio.save_image(processed, output_path)

**GUI Integration**

.. code-block:: python

   import tkinter as tk
   from gui_image_studio import ImageStudio
   
   root = tk.Tk()
   app = ImageStudio(root)
   app.pack(fill=tk.BOTH, expand=True)
   root.mainloop()

Migration Guide
---------------

**From Version 0.x to 1.0**

* Function names have been standardized
* Error handling has been improved
* Type hints have been added throughout
* Some deprecated functions have been removed

**Deprecated Functions**

These functions are deprecated and will be removed in future versions:

* ``load_image()`` → Use ``get_image()``
* ``tint_image()`` → Use ``apply_tint()``
* ``create_gif()`` → Use ``create_animation()``