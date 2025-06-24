Quick Start Guide
=================

This guide will help you get started with GUI Image Studio in just a few minutes.

Your First Image Editing Session
---------------------------------

Let's launch the application and perform basic image editing:

**Step 1: Launch the Application**

.. code-block:: bash

    gui-image-studio-designer

**Step 2: Load an Image**

1. Click **File → Open** or press ``Ctrl+O``
2. Select an image file (PNG, JPEG, GIF, etc.)
3. The image will appear in the main canvas

**Step 3: Apply Basic Edits**

.. code-block:: python

    # You can also use the Python API directly
    import gui_image_studio

    # Load an image
    image = gui_image_studio.get_image("sample.png")

    # Apply a tint
    tinted = gui_image_studio.apply_tint(image, "#FF6B6B")

    # Resize the image
    resized = gui_image_studio.resize_image(tinted, (800, 600))

    # Save the result
    gui_image_studio.save_image(resized, "output.png")

Understanding the Interface
---------------------------

The GUI Image Studio interface consists of several key areas:

**Main Canvas**
  The central area where your image is displayed and edited.

**Tool Palette**
  Left sidebar containing editing tools like brush, selection, filters.

**Properties Panel**
  Right sidebar showing current tool settings and image properties.

**Timeline** (for animations)
  Bottom panel for managing animated GIF frames and timing.

**Menu Bar**
  Standard menu with File, Edit, View, Tools, and Help options.

Basic Image Operations
----------------------

**Loading Images**

.. code-block:: python

    import gui_image_studio

    # Load from file
    image = gui_image_studio.get_image("path/to/image.png")

    # Load from URL (if supported)
    image = gui_image_studio.get_image("https://example.com/image.jpg")

**Applying Transformations**

.. code-block:: python

    # Resize image
    resized = gui_image_studio.resize_image(image, (width, height))

    # Apply color tint
    tinted = gui_image_studio.apply_tint(image, "#FF6B6B")

    # Rotate image
    rotated = gui_image_studio.rotate_image(image, 90)

    # Flip image
    flipped = gui_image_studio.flip_image(image, horizontal=True)

**Saving Images**

.. code-block:: python

    # Save in different formats
    gui_image_studio.save_image(image, "output.png")
    gui_image_studio.save_image(image, "output.jpg", quality=95)
    gui_image_studio.save_image(image, "output.gif")

Creating Your First Animation
------------------------------

GUI Image Studio excels at creating animated GIFs:

.. code-block:: python

    import gui_image_studio

    # Create frames for animation
    frames = []
    base_image = gui_image_studio.get_image("base.png")

    # Create 10 frames with different tints
    for i in range(10):
        hue = i * 36  # 0 to 324 degrees
        tinted = gui_image_studio.apply_hue_shift(base_image, hue)
        frames.append(tinted)

    # Create animated GIF
    gui_image_studio.create_animation(frames, "rainbow.gif", duration=100)

**Using the GUI for Animations**

1. Load your base image
2. Click **Animation → New Animation**
3. Add frames using **Animation → Add Frame**
4. Adjust timing in the timeline
5. Export with **File → Export Animation**

Working with Themes
--------------------

GUI Image Studio supports both light and dark themes:

**Switching Themes in GUI**

1. Go to **View → Theme**
2. Select **Light** or **Dark**
3. The interface will update immediately

**Setting Theme Programmatically**

.. code-block:: python

    import gui_image_studio

    # Set dark theme
    gui_image_studio.set_theme("dark")

    # Set light theme
    gui_image_studio.set_theme("light")

Command Line Tools
------------------

GUI Image Studio includes several command-line utilities:

**Create Sample Images**

.. code-block:: bash

    gui-image-studio-create-samples
    # Creates sample images in ./sample_images/

**Generate Embedded Resources**

.. code-block:: bash

    gui-image-studio-generate --folder images/
    # Generates embedded_images.py with base64-encoded images

**Batch Processing** (if available)

.. code-block:: bash

    gui-image-studio-batch --input folder/ --output processed/ --filter tint --color "#FF6B6B"

Common Workflows
----------------

**Photo Enhancement Workflow**

1. Load photo
2. Adjust brightness/contrast
3. Apply color correction
4. Sharpen if needed
5. Export in desired format

**Icon Creation Workflow**

1. Create or load base image
2. Resize to icon dimensions (16x16, 32x32, 64x64)
3. Apply appropriate styling
4. Export as PNG with transparency

**Animation Creation Workflow**

1. Plan your animation frames
2. Create base images
3. Use timeline to arrange frames
4. Adjust timing and transitions
5. Export as optimized GIF

Keyboard Shortcuts
------------------

**File Operations**
  * ``Ctrl+O`` - Open file
  * ``Ctrl+S`` - Save file
  * ``Ctrl+Shift+S`` - Save as
  * ``Ctrl+N`` - New file

**Edit Operations**
  * ``Ctrl+Z`` - Undo
  * ``Ctrl+Y`` - Redo
  * ``Ctrl+C`` - Copy
  * ``Ctrl+V`` - Paste

**View Operations**
  * ``Ctrl++`` - Zoom in
  * ``Ctrl+-`` - Zoom out
  * ``Ctrl+0`` - Fit to window
  * ``F11`` - Fullscreen

**Tools**
  * ``B`` - Brush tool
  * ``E`` - Eraser tool
  * ``S`` - Selection tool
  * ``T`` - Text tool

Getting Help
------------

**In-Application Help**

* Press ``F1`` for context-sensitive help
* Use **Help → User Guide** for comprehensive documentation
* Check **Help → About** for version information

**Online Resources**

* `GitHub Repository <https://github.com/stntg/gui-image-studio>`_
* `Issue Tracker <https://github.com/stntg/gui-image-studio/issues>`_
* `Documentation <https://gui-image-studio.readthedocs.io/>`_

**Sample Projects**

Run the examples to see GUI Image Studio in action:

.. code-block:: bash

    python examples/01_basic_usage.py
    python examples/02_theming_examples.py
    python examples/04_animated_gifs.py

Next Steps
----------

Now that you have GUI Image Studio running:

1. **Explore the Examples**: Check out the :doc:`examples/index` for more complex use cases
2. **Read the User Guide**: Learn about advanced features in :doc:`user_guide/index`
3. **API Reference**: Dive deep into the :doc:`api/index` for complete documentation
4. **Customize**: Create your own filters and tools
5. **Contribute**: Help improve GUI Image Studio by contributing to the project

Tips for Success
-----------------

**Performance Tips**

* Work with reasonably sized images (under 4K for smooth performance)
* Use PNG for images with transparency
* Use JPEG for photographs without transparency
* Optimize GIF animations by reducing colors and frame rate

**Quality Tips**

* Always work with the highest quality source images
* Save your work frequently
* Use non-destructive editing when possible
* Keep backups of original images

**Workflow Tips**

* Plan your edits before starting
* Use layers when available
* Test animations at different speeds
* Export in multiple formats for different use cases

That's it! You now have a solid foundation for using GUI Image Studio effectively.
