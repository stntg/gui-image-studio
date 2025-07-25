Examples
========

This section contains practical examples showing how to use GUI Image Studio in real applications.

.. toctree::
   :maxdepth: 2
   :caption: Basic Examples:

   basic_usage
   image_processing
   gui_application

.. toctree::
   :maxdepth: 2
   :caption: Advanced Examples:

   animation_creation
   batch_processing
   custom_filters
   theme_integration

.. toctree::
   :maxdepth: 2
   :caption: Integration Examples:

   tkinter_integration
   customtkinter_integration
   web_integration
   plugin_development

.. toctree::
   :maxdepth: 2
   :caption: Real-World Applications:

   photo_editor
   icon_generator
   batch_converter
   animation_studio

Overview
--------

The examples are organized by complexity and use case:

**Basic Examples**
  Simple, straightforward examples perfect for getting started with GUI Image Studio.

**Advanced Examples**
  More complex examples showing professional features, custom filters, and advanced image processing.

**Integration Examples**
  Examples showing how to integrate GUI Image Studio with other frameworks and libraries.

**Real-World Applications**
  Complete application examples demonstrating practical use cases.

Running the Examples
--------------------

All examples can be run directly as Python scripts:

.. code-block:: bash

    python examples/01_basic_usage.py
    python examples/02_theming_examples.py
    python examples/04_animated_gifs.py

Or you can copy the code into your own projects and modify as needed.

Example Categories
------------------

**Image Processing Examples**
  Examples focusing on core image manipulation: resizing, filtering, color adjustment, and transformations.

**GUI Application Examples**
  Examples showing how to build complete GUI applications with image editing capabilities.

**Animation Examples**
  Examples demonstrating animated GIF creation, frame management, and timeline editing.

**Batch Processing Examples**
  Examples showing how to process multiple images automatically with various operations.

**Integration Examples**
  Examples showing how to integrate GUI Image Studio with other Python libraries and frameworks.

**Professional Applications**
  Real-world examples showing complete application architectures and advanced features.

Quick Start Examples
--------------------

**Load and Use an Image**

.. code-block:: python

    from gui_image_studio import get_image
    import tkinter as tk

    # Load an image for tkinter
    image = get_image("input.jpg", framework="tkinter", size=(200, 200))

    # Use in GUI
    root = tk.Tk()
    label = tk.Label(root, image=image)
    label.pack()
    root.mainloop()

**Apply Basic Effects**

.. code-block:: python

    from gui_image_studio import get_image

    # Load image with transformations
    image = get_image(
        "photo.jpg",
        framework="customtkinter",
        size=(800, 600),
        tint_color=(255, 107, 107),
        tint_intensity=0.3,
        contrast=1.2
    )

**Work with Animated GIFs**

.. code-block:: python

    from gui_image_studio import get_image

    # Load animated GIF
    animation_data = get_image(
        "animation.gif",
        framework="customtkinter",
        size=(100, 100),
        animated=True,
        frame_delay=100
    )

    # Access frames and timing
    frames = animation_data["animated_frames"]
    delay = animation_data["frame_delay"]

**Launch GUI Application**

.. code-block:: bash

    # Launch the Image Studio GUI
    gui-image-studio-designer

    # Or programmatically from Python
    import subprocess
    subprocess.run(["gui-image-studio-designer"])

Example Data
------------

Many examples use sample images that can be generated using:

.. code-block:: bash

    gui-image-studio-create-samples

This creates a ``sample_images/`` directory with various test images:

* ``sample_icon.png`` - Small icon for testing
* ``sample_photo.jpg`` - Photograph for processing
* ``sample_animation.gif`` - Animated GIF for testing
* ``sample_transparent.png`` - Image with transparency
* ``sample_large.jpg`` - Large image for performance testing

Code Style
----------

All examples follow these conventions:

* **Clear Comments**: Each section is well-commented
* **Error Handling**: Proper exception handling where appropriate
* **Type Hints**: Function signatures include type hints
* **Docstrings**: Functions include descriptive docstrings
* **PEP 8**: Code follows Python style guidelines

**Example Template:**

.. code-block:: python

    # Example: Basic Image Processing
    # This example demonstrates basic image loading, processing, and saving
    # operations using GUI Image Studio.

    import gui_image_studio
    from typing import Optional

    def process_image(input_path: str, output_path: str,
                     tint_color: str = "#FF6B6B") -> Optional[bool]:
        """
        Process an image with tint and resize operations.

        Args:
            input_path: Path to input image
            output_path: Path for output image
            tint_color: Hex color for tinting

        Returns:
            True if successful, None if failed
        """
        try:
            # Load image with transformations
            image = get_image(
                input_path,
                framework="tkinter",
                size=(800, 600),
                tint_color=tint_color,
                tint_intensity=0.3
            )

            return True

        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    if __name__ == "__main__":
        process_image("input.jpg", "output.png")

Contributing Examples
---------------------

We welcome contributions of new examples! When contributing:

1. **Follow the Template**: Use the standard example template
2. **Include Documentation**: Add clear comments and docstrings
3. **Test Thoroughly**: Ensure examples work with sample data
4. **Add to Index**: Update this index file to include your example
5. **Provide Sample Data**: Include any required sample files

**Example Submission Checklist:**

- [ ] Code follows PEP 8 style guidelines
- [ ] Includes comprehensive comments
- [ ] Has proper error handling
- [ ] Works with provided sample data
- [ ] Includes docstring with description
- [ ] Added to appropriate category in index
- [ ] Tested on multiple platforms (if possible)

Getting Help
------------

If you need help with the examples:

1. Check the :doc:`../api/index` for detailed API documentation
2. Review the :doc:`../quickstart` guide for basic concepts
3. Look at similar examples in the same category
4. Check the `GitHub Issues <https://github.com/stntg/gui-image-studio/issues>`_ for common problems
5. Create a new issue if you find bugs or have suggestions

Performance Tips
----------------

When working with the examples:

**For Large Images:**
  * Resize images before applying complex operations
  * Use appropriate image formats (PNG for graphics, JPEG for photos)
  * Consider memory usage with batch operations

**For Animations:**
  * Optimize frame count and duration
  * Use appropriate color palettes for GIFs
  * Test performance with different frame rates

**For GUI Applications:**
  * Use threading for long operations
  * Implement progress indicators
  * Cache frequently used images

**For Batch Processing:**
  * Process images in chunks
  * Use appropriate error handling
  * Consider parallel processing for independent operations
