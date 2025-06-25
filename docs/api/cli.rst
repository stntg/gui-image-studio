Command Line Interface
======================

The ``cli`` module provides command-line interfaces for GUI Image Studio functionality.

.. automodule:: gui_image_studio.cli
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

GUI Image Studio provides three main command-line tools:

* ``gui-image-studio-designer`` - Launch the main GUI application
* ``gui-image-studio-create-samples`` - Generate sample images for testing
* ``gui-image-studio-generate`` - Create embedded image resources

All commands support ``--help`` and ``--version`` options.

Main Commands
-------------

Designer Application
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.cli.launch_designer

Launch the main GUI Image Studio application.

**Usage:**

.. code-block:: bash

    gui-image-studio-designer [OPTIONS] [FILE]

**Options:**

* ``--version`` - Show version information
* ``--theme THEME`` - Set initial theme (light/dark)
* ``--fullscreen`` - Start in fullscreen mode
* ``--debug`` - Enable debug mode
* ``--config FILE`` - Use custom configuration file

**Examples:**

.. code-block:: bash

    # Launch with default settings
    gui-image-studio-designer

    # Launch with specific image
    gui-image-studio-designer photo.jpg

    # Launch with dark theme
    gui-image-studio-designer --theme dark

    # Launch in fullscreen
    gui-image-studio-designer --fullscreen

    # Launch with debug output
    gui-image-studio-designer --debug

**Return Codes:**

* ``0`` - Success
* ``1`` - General error
* ``2`` - Invalid arguments
* ``3`` - File not found
* ``4`` - Permission error

Sample Creator
~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.cli.create_sample_images

Generate sample images for testing and development.

**Usage:**

.. code-block:: bash

    gui-image-studio-create-samples [OPTIONS]

**Options:**

* ``--output-dir DIR`` - Output directory (default: ./sample_images)
* ``--count N`` - Number of each sample type to create (default: 1)
* ``--size WxH`` - Image size (default: 256x256)
* ``--formats FORMAT`` - Comma-separated list of formats (default: png,jpg,gif)
* ``--animated`` - Include animated GIF samples
* ``--overwrite`` - Overwrite existing files
* ``--verbose`` - Verbose output

**Examples:**

.. code-block:: bash

    # Create default samples
    gui-image-studio-create-samples

    # Create samples in specific directory
    gui-image-studio-create-samples --output-dir test_images

    # Create multiple samples of each type
    gui-image-studio-create-samples --count 5

    # Create large samples
    gui-image-studio-create-samples --size 1024x1024

    # Create only PNG samples
    gui-image-studio-create-samples --formats png

    # Include animated samples
    gui-image-studio-create-samples --animated

    # Verbose output with overwrite
    gui-image-studio-create-samples --verbose --overwrite

**Generated Samples:**

* ``sample_icon.png`` - Small icon for UI testing
* ``sample_photo.jpg`` - Photograph for processing tests
* ``sample_gradient.png`` - Gradient for filter testing
* ``sample_transparent.png`` - Image with transparency
* ``sample_animation.gif`` - Animated GIF (if --animated)
* ``sample_large.jpg`` - Large image for performance testing

Resource Generator
~~~~~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.cli.generate_embedded_images

Generate embedded image resources for distribution.

**Usage:**

.. code-block:: bash

    gui-image-studio-generate [OPTIONS]

**Options:**

* ``--folder DIR`` - Input folder containing images (default: ./images)
* ``--output FILE`` - Output Python file (default: embedded_images.py)
* ``--module-name NAME`` - Module name for generated code
* ``--format FORMAT`` - Encoding format (base64/bytes, default: base64)
* ``--compress`` - Compress images before embedding
* ``--quality N`` - JPEG quality for compression (1-100, default: 85)
* ``--max-size WxH`` - Maximum image size (default: no limit)
* ``--exclude PATTERN`` - Exclude files matching pattern
* ``--include PATTERN`` - Include only files matching pattern

**Examples:**

.. code-block:: bash

    # Generate from default folder
    gui-image-studio-generate

    # Generate from specific folder
    gui-image-studio-generate --folder assets/icons

    # Generate with custom output file
    gui-image-studio-generate --output my_images.py

    # Generate with compression
    gui-image-studio-generate --compress --quality 75

    # Generate with size limit
    gui-image-studio-generate --max-size 512x512

    # Generate excluding thumbnails
    gui-image-studio-generate --exclude "*thumb*"

    # Generate only PNG files
    gui-image-studio-generate --include "*.png"

**Generated Code Example:**

.. code-block:: python

    # embedded_images.py (generated)
    """
    Embedded images for GUI Image Studio
    Generated on: 2024-06-22 10:30:00
    """

    import base64
    from io import BytesIO
    from PIL import Image

    # Image data
    IMAGES = {
        'sample_icon': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQ...',
        'sample_photo': '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAA...',
    }

    def get_image(name: str) -> Image.Image:
        """Get embedded image by name."""
        if name not in IMAGES:
            raise KeyError(f"Image '{name}' not found")

        data = base64.b64decode(IMAGES[name])
        return Image.open(BytesIO(data))

    def list_images() -> list:
        """List all available embedded images."""
        return list(IMAGES.keys())

Available Functions
-------------------

The CLI module provides the following functions that can be used programmatically:

.. autofunction:: gui_image_studio.cli.generate_embedded_images
.. autofunction:: gui_image_studio.cli.create_sample_images
.. autofunction:: gui_image_studio.cli.launch_designer

Configuration
-------------

CLI Configuration File
~~~~~~~~~~~~~~~~~~~~~~

CLI tools can use a configuration file to set default options:

**Location:**
  * Windows: ``%APPDATA%\gui-image-studio\config.ini``
  * macOS: ``~/Library/Application Support/gui-image-studio/config.ini``
  * Linux: ``~/.config/gui-image-studio/config.ini``

**Format:**

.. code-block:: ini

    [designer]
    theme = dark
    fullscreen = false
    debug = false

    [samples]
    output_dir = ./sample_images
    count = 1
    size = 256x256
    formats = png,jpg,gif
    animated = false

    [generator]
    folder = ./images
    output = embedded_images.py
    format = base64
    compress = false
    quality = 85

**Environment Variables:**

CLI tools also respect environment variables:

.. code-block:: bash

    export GUI_IMAGE_STUDIO_THEME=dark
    export GUI_IMAGE_STUDIO_DEBUG=1
    export GUI_IMAGE_STUDIO_CONFIG=/path/to/config.ini

Advanced Usage
--------------

Scripting with CLI Tools
~~~~~~~~~~~~~~~~~~~~~~~~~

**Batch Sample Creation:**

.. code-block:: bash

    #!/bin/bash
    # Create samples for different test scenarios

    # Small samples for unit tests
    gui-image-studio-create-samples --output-dir tests/fixtures --size 32x32 --count 3

    # Medium samples for integration tests
    gui-image-studio-create-samples --output-dir tests/integration --size 256x256 --animated

    # Large samples for performance tests
    gui-image-studio-create-samples --output-dir tests/performance --size 2048x2048

**Automated Resource Generation:**

.. code-block:: bash

    #!/bin/bash
    # Build script for embedding resources

    # Compress and embed icons
    gui-image-studio-generate --folder assets/icons --output src/icons.py --compress --max-size 64x64

    # Embed sample images
    gui-image-studio-generate --folder sample_images --output src/samples.py --quality 75

**CI/CD Integration:**

.. code-block:: yaml

    # GitHub Actions example
    - name: Generate embedded resources
      run: |
        gui-image-studio-create-samples --output-dir test_data
        gui-image-studio-generate --folder assets --output src/embedded.py

**PowerShell Scripting (Windows):**

.. code-block:: powershell

    # PowerShell script for Windows
    $ErrorActionPreference = "Stop"

    # Create test samples
    gui-image-studio-create-samples --output-dir "test_images" --verbose

    # Generate resources
    gui-image-studio-generate --folder "assets" --output "embedded.py" --compress

    Write-Host "Resource generation complete"

Error Handling
--------------

**Exit Codes:**

All CLI tools use standard exit codes:

* ``0`` - Success
* ``1`` - General error
* ``2`` - Invalid command line arguments
* ``3`` - File or directory not found
* ``4`` - Permission denied
* ``5`` - Insufficient disk space
* ``6`` - Unsupported image format
* ``7`` - Memory error

**Error Messages:**

CLI tools provide clear error messages:

.. code-block:: bash

    $ gui-image-studio-designer nonexistent.jpg
    Error: File 'nonexistent.jpg' not found
    Exit code: 3

    $ gui-image-studio-create-samples --size invalid
    Error: Invalid size format 'invalid'. Use format: WIDTHxHEIGHT
    Exit code: 2

**Logging:**

Enable detailed logging for troubleshooting:

.. code-block:: bash

    # Enable verbose output
    gui-image-studio-designer --debug --verbose

    # Redirect output to file
    gui-image-studio-create-samples --verbose > creation.log 2>&1

Integration Examples
--------------------

**Makefile Integration:**

.. code-block:: makefile

    # Makefile for project build
    .PHONY: samples resources clean

    samples:
        gui-image-studio-create-samples --output-dir test_data

    resources:
        gui-image-studio-generate --folder assets --output src/embedded.py --compress

    clean:
        rm -rf test_data src/embedded.py

**Python Script Integration:**

.. code-block:: python

    import subprocess
    import sys

    def generate_resources():
        """Generate embedded resources using CLI."""
        try:
            result = subprocess.run([
                'gui-image-studio-generate',
                '--folder', 'assets',
                '--output', 'src/embedded.py',
                '--compress'
            ], check=True, capture_output=True, text=True)

            print("Resources generated successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error generating resources: {e.stderr}")
            return False

    if __name__ == "__main__":
        if not generate_resources():
            sys.exit(1)

**Docker Integration:**

.. code-block:: dockerfile

    FROM python:3.9-slim

    # Install GUI Image Studio
    RUN pip install gui-image-studio

    # Copy assets
    COPY assets/ /app/assets/

    # Generate embedded resources
    WORKDIR /app
    RUN gui-image-studio-generate --folder assets --output embedded.py

    # Your application code
    COPY . /app/
    CMD ["python", "app.py"]

Performance Considerations
--------------------------

**Large Image Handling:**

.. code-block:: bash

    # For large images, use compression and size limits
    gui-image-studio-generate --folder large_images --compress --max-size 1024x1024 --quality 70

**Memory Usage:**

.. code-block:: bash

    # Monitor memory usage during generation
    /usr/bin/time -v gui-image-studio-generate --folder assets

**Parallel Processing:**

.. code-block:: bash

    # Process multiple folders in parallel
    gui-image-studio-generate --folder icons &
    gui-image-studio-generate --folder photos &
    wait

Troubleshooting
---------------

**Common Issues:**

1. **Command not found:**

   .. code-block:: bash

       # Ensure GUI Image Studio is installed
       pip install gui-image-studio

       # Check installation
       pip show gui-image-studio

2. **Permission errors:**

   .. code-block:: bash

       # Use --output-dir with write permissions
       gui-image-studio-create-samples --output-dir ~/test_images

3. **Memory errors with large images:**

   .. code-block:: bash

       # Use size limits and compression
       gui-image-studio-generate --max-size 512x512 --compress

4. **Display issues (Linux):**

   .. code-block:: bash

       # Set display for headless systems
       export DISPLAY=:0
       gui-image-studio-designer

**Debug Mode:**

Enable debug mode for detailed troubleshooting:

.. code-block:: bash

    gui-image-studio-designer --debug
    # Shows detailed error messages and stack traces
