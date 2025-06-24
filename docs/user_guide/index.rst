User Guide
==========

Complete guide to using GUI Image Studio for image processing and application development.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   installation_guide
   first_steps
   interface_overview

.. toctree::
   :maxdepth: 2
   :caption: Core Features:

   image_processing
   animation_tools
   batch_operations
   theme_system

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics:

   custom_filters
   plugin_development
   performance_optimization
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Integration:

   api_usage
   gui_development
   command_line_tools
   scripting

Overview
--------

GUI Image Studio is a comprehensive image processing library and application that provides:

**Core Capabilities**
  * Professional image editing and processing
  * Animated GIF creation and editing
  * Batch processing workflows
  * Extensible plugin architecture

**User Interfaces**
  * Full-featured GUI application
  * Command-line tools for automation
  * Python API for integration
  * Web-based interface (planned)

**Target Users**
  * Graphic designers and artists
  * Software developers
  * Content creators
  * Automation specialists

Key Concepts
------------

**Images and Formats**

GUI Image Studio works with standard image formats:

* **Raster Images**: PNG, JPEG, GIF, BMP, TIFF, WebP
* **Animated Images**: GIF with frame timing and optimization
* **Transparency**: Full alpha channel support
* **Color Modes**: RGB, RGBA, Grayscale, Palette

**Processing Pipeline**

The typical image processing workflow:

1. **Load** - Import images from files or resources
2. **Process** - Apply filters, transformations, and effects
3. **Preview** - Review changes in real-time
4. **Export** - Save in desired format and quality

**Non-Destructive Editing**

GUI Image Studio supports non-destructive editing:

* Original images remain unchanged
* Operations create new image objects
* History tracking for undo/redo
* Layer-based editing (where supported)

Application Architecture
------------------------

**Modular Design**

GUI Image Studio is built with a modular architecture:

.. code-block:: text

    gui_image_studio/
    ├── image_loader.py      # Core image operations
    ├── image_studio.py      # GUI application
    ├── generator.py         # Resource generation
    ├── sample_creator.py    # Sample image creation
    └── cli.py              # Command-line interface

**Plugin System**

Extend functionality with custom plugins:

* **Filters**: Custom image processing algorithms
* **Tools**: New editing tools and brushes
* **Exporters**: Additional file format support
* **Themes**: Custom UI themes and styles

**API Layers**

Multiple API layers for different use cases:

* **High-Level API**: Simple functions for common operations
* **Mid-Level API**: Class-based interface with more control
* **Low-Level API**: Direct access to PIL/Pillow functionality

Getting Started Workflow
-------------------------

**1. Installation and Setup**

.. code-block:: bash

    # Install GUI Image Studio
    pip install gui-image-studio

    # Verify installation
    gui-image-studio-designer --version

    # Create sample images for testing
    gui-image-studio-create-samples

**2. Basic Usage**

.. code-block:: python

    import gui_image_studio

    # Load and process an image
    image = gui_image_studio.get_image("photo.jpg")
    processed = gui_image_studio.apply_tint(image, "#FF6B6B")
    gui_image_studio.save_image(processed, "output.png")

**3. GUI Application**

.. code-block:: bash

    # Launch the main application
    gui-image-studio-designer

**4. Advanced Features**

.. code-block:: python

    # Create animations
    frames = [gui_image_studio.rotate_image(image, angle)
              for angle in range(0, 360, 30)]
    gui_image_studio.create_animation(frames, "spinning.gif")

Common Use Cases
----------------

**Photo Enhancement**

Typical photo editing workflow:

1. Load high-resolution photo
2. Adjust brightness and contrast
3. Apply color correction
4. Sharpen or blur as needed
5. Export in web-optimized format

**Icon and Graphics Creation**

Creating icons and graphics:

1. Start with vector or high-res source
2. Resize to target dimensions
3. Apply appropriate styling
4. Export with transparency
5. Generate multiple sizes

**Batch Processing**

Automating repetitive tasks:

1. Define processing pipeline
2. Set up input/output folders
3. Configure error handling
4. Run batch operation
5. Review and validate results

**Animation Creation**

Creating animated content:

1. Plan animation sequence
2. Create or import frames
3. Set timing and transitions
4. Preview animation
5. Optimize and export

Best Practices
--------------

**Image Quality**

* Always work with the highest quality source images
* Use appropriate formats (PNG for graphics, JPEG for photos)
* Maintain aspect ratios when resizing
* Apply sharpening after resizing

**Performance**

* Resize large images before complex operations
* Use appropriate color modes (RGB vs RGBA)
* Cache frequently used images
* Use batch operations for multiple files

**File Management**

* Organize source images in logical folders
* Use descriptive filenames
* Keep backups of original images
* Document processing workflows

**Development**

* Use type hints for better code quality
* Implement proper error handling
* Write unit tests for custom functions
* Follow PEP 8 style guidelines

Troubleshooting
---------------

**Common Issues**

* **Memory errors**: Reduce image size or close other applications
* **Format errors**: Check file format support and corruption
* **Permission errors**: Verify file and folder permissions
* **Display issues**: Update graphics drivers and check system requirements

**Getting Help**

* Check the :doc:`troubleshooting` section for detailed solutions
* Review the :doc:`../api/index` for API documentation
* Search the `GitHub Issues <https://github.com/stntg/gui-image-studio/issues>`_
* Join the community discussions

**Reporting Issues**

When reporting issues, include:

* GUI Image Studio version
* Python version and platform
* Complete error messages
* Steps to reproduce
* Sample images (if relevant)

Next Steps
----------

Choose your path based on your needs:

**For End Users**
  * Start with :doc:`first_steps` for basic usage
  * Learn the :doc:`interface_overview` for GUI features
  * Explore :doc:`image_processing` for editing techniques

**For Developers**
  * Review :doc:`api_usage` for integration
  * Check :doc:`plugin_development` for extensions
  * Study :doc:`../examples/index` for code samples

**For Automation**
  * Learn :doc:`command_line_tools` for scripting
  * Explore :doc:`batch_operations` for workflows
  * Review :doc:`scripting` for advanced automation
