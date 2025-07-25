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
    from gui_image_studio import get_image

    # Load an image with transformations
    image = get_image(
        "sample.png",
        framework="tkinter",
        size=(800, 600),
        tint_color=(255, 107, 107),
        tint_intensity=0.3
    )

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

    from gui_image_studio import get_image

    # Load from file with basic settings
    image = get_image("path/to/image.png", framework="tkinter")

    # Load with transformations
    image = get_image(
        "path/to/image.png",
        framework="customtkinter",
        size=(200, 200),
        theme="dark"
    )

**Applying Transformations**

.. code-block:: python

    from gui_image_studio import get_image

    # Apply transformations during loading
    image = get_image(
        "photo.jpg",
        framework="customtkinter",
        size=(200, 200),
        rotate=45,
        tint_color=(255, 0, 0),
        tint_intensity=0.3,
        contrast=1.2,
        saturation=1.5,
        grayscale=False,
        transparency=1.0
    )

**Using Images in GUI Applications**

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    root = tk.Tk()

    # Load image for tkinter
    photo = get_image(
        "my_image.png",
        framework="tkinter",
        size=(100, 100),
        theme="default"
    )
    label = tk.Label(root, image=photo)
    label.pack()

    root.mainloop()

Working with Animated GIFs
---------------------------

GUI Image Studio supports animated GIF processing:

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

    # Use the frames in your application
    frames = animation_data["animated_frames"]
    delay = animation_data["frame_delay"]

**Embedding Images from Folders**

.. code-block:: python

    from gui_image_studio import embed_images_from_folder

    # Process all images in a folder
    embed_images_from_folder(
        folder_path="images/",
        output_file="embedded_images.py",
        compression_quality=85
    )

Working with Themes
--------------------

GUI Image Studio supports theme-aware image loading:

**Using Themes with Images**

.. code-block:: python

    from gui_image_studio import get_image

    # Load image with dark theme
    dark_image = get_image(
        "icon.png",
        framework="customtkinter",
        theme="dark",
        size=(64, 64)
    )

    # Load image with light theme
    light_image = get_image(
        "icon.png",
        framework="tkinter",
        theme="light",
        size=(64, 64)
    )

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

**Animation Creation Workflow** To be implemented in image_studio app

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
