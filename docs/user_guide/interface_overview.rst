Interface Overview
==================

This guide provides a comprehensive overview of the GUI Image Studio interface, including the visual designer, command-line tools, and Python API.

Visual Designer Interface
--------------------------

The GUI Image Studio Designer is the main visual interface for creating and editing images.

Launching the Designer
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # For PyPI installations (recommended)
    gui-image-studio-designer

    # For development/contributors (GitHub repo only)
    python launch_designer.py

Main Window Layout
~~~~~~~~~~~~~~~~~~

The designer uses a three-pane window layout:

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────┐
    │ Menu Bar: File | Edit | View | Tools | Help                │
    ├─────────────────────────────────────────────────────────────┤
    │ Toolbar: [New] [Open] [Save] [Undo] [Redo] [Zoom] ...      │
    ├─────────────┬─────────────────────────────┬─────────────────┤
    │             │                             │                 │
    │   Tools     │        Canvas Area          │   Properties    │
    │   Panel     │                             │     Panel       │
    │             │   ┌─────────────────────┐   │                 │
    │ • Brush     │   │                     │   │ • Size          │
    │ • Pencil    │   │     Image Canvas    │   │ • Color         │
    │ • Eraser    │   │                     │   │ • Opacity       │
    │ • Shapes    │   │                     │   │ • Filters       │
    │ • Text      │   └─────────────────────┘   │ • Transform     │
    │ • Fill      │                             │ • Export        │
    │             │                             │                 │
    └─────────────┴─────────────────────────────┴─────────────────┘

Menu Bar
~~~~~~~~

**File Menu:**
- **New**: Create new image
- **Open**: Load existing image
- **Save**: Save current image
- **Save As**: Save with new name/format
- **Import**: Import from various sources
- **Export**: Export in different formats
- **Recent**: Recently opened files
- **Exit**: Close application

**Edit Menu:**
- **Undo**: Reverse last action (Ctrl+Z)
- **Redo**: Restore undone action (Ctrl+Y)
- **Cut**: Cut selection (Ctrl+X)
- **Copy**: Copy selection (Ctrl+C)
- **Paste**: Paste from clipboard (Ctrl+V)
- **Select All**: Select entire image (Ctrl+A)
- **Clear**: Clear selection

**View Menu:**
- **Zoom In**: Increase magnification (Ctrl++)
- **Zoom Out**: Decrease magnification (Ctrl+-)
- **Fit to Window**: Fit image to window
- **Actual Size**: Show at 100% size
- **Grid**: Toggle grid overlay
- **Rulers**: Toggle ruler display

**Tools Menu:**
- **Brush Tool**: Freehand drawing
- **Pencil Tool**: Precise drawing
- **Eraser Tool**: Remove pixels
- **Shape Tools**: Rectangles, circles, lines
- **Text Tool**: Add text
- **Fill Tool**: Flood fill areas

**Help Menu:**
- **Documentation**: Open help documentation
- **About**: Application information
- **Keyboard Shortcuts**: Shortcut reference

Toolbar
~~~~~~~

The toolbar provides quick access to common functions:

.. code-block:: text

    [📄] New     [📁] Open    [💾] Save    [↶] Undo    [↷] Redo
    [🔍+] Zoom In [🔍-] Zoom Out [⚙️] Settings [❓] Help

Tools Panel
~~~~~~~~~~~

**Drawing Tools:**

.. code-block:: text

    🖌️ Brush Tool
    ├─ Size: 1-100 pixels
    ├─ Opacity: 0-100%
    ├─ Hardness: 0-100%
    └─ Blend Mode: Normal, Multiply, Screen, etc.

    ✏️ Pencil Tool
    ├─ Size: 1-20 pixels
    ├─ Opacity: 0-100%
    └─ Anti-aliasing: On/Off

    🧽 Eraser Tool
    ├─ Size: 1-100 pixels
    ├─ Hardness: 0-100%
    └─ Mode: Normal, Background

**Shape Tools:**

.. code-block:: text

    ⬜ Rectangle Tool
    ├─ Fill: Solid, Gradient, None
    ├─ Stroke: Width, Color
    └─ Corner Radius: 0-50 pixels

    ⭕ Circle Tool
    ├─ Fill: Solid, Gradient, None
    ├─ Stroke: Width, Color
    └─ Perfect Circle: On/Off

    📏 Line Tool
    ├─ Width: 1-50 pixels
    ├─ Style: Solid, Dashed, Dotted
    └─ Arrow Heads: None, Start, End, Both

**Text Tool:**

.. code-block:: text

    📝 Text Tool
    ├─ Font: Family, Size, Style
    ├─ Color: Text, Background
    ├─ Alignment: Left, Center, Right
    └─ Effects: Shadow, Outline

Properties Panel
~~~~~~~~~~~~~~~~

The properties panel changes based on the selected tool and current image:

**Image Properties:**

.. code-block:: text

    📊 Image Information
    ├─ Dimensions: 800 × 600 pixels
    ├─ File Size: 245 KB
    ├─ Color Mode: RGB
    ├─ Bit Depth: 8 bits/channel
    └─ [ℹ️] Info Button (detailed analysis)

**Transform Properties:**

.. code-block:: text

    🔄 Transform
    ├─ Size: Width × Height
    ├─ Rotation: 0-360 degrees
    ├─ Flip: Horizontal, Vertical
    └─ [Apply] [Reset]

**Color Properties:**

.. code-block:: text

    🎨 Color Adjustments
    ├─ Tint: Color picker + Intensity
    ├─ Contrast: -100 to +100
    ├─ Saturation: -100 to +100
    ├─ Brightness: -100 to +100
    └─ [Apply] [Reset]

**Filter Properties:**

.. code-block:: text

    🔧 Filters
    ├─ Blur: Gaussian, Motion
    ├─ Sharpen: Unsharp Mask
    ├─ Noise: Add, Remove
    └─ [Apply] [Preview]

Canvas Area
~~~~~~~~~~~

The main canvas area displays your image and provides:

**Navigation:**
- **Pan**: Click and drag to move around
- **Zoom**: Mouse wheel or zoom tools
- **Fit**: Double-click to fit to window

**Selection:**
- **Rectangle Select**: Drag to select area
- **Free Select**: Draw selection outline
- **Magic Wand**: Select similar colors

**Visual Aids:**
- **Grid**: Alignment grid overlay
- **Rulers**: Measurement rulers
- **Guides**: Snap-to guides

Working with Multiple Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The designer supports working with multiple images:

**Image Tabs:**

.. code-block:: text

    [Image1.png] [Image2.jpg] [New Image*] [+]

    • Active tab shows current image
    • * indicates unsaved changes
    • + creates new image
    • Right-click for context menu

**Image Management:**
- **New Tab**: Create new image
- **Close Tab**: Close current image
- **Switch Tabs**: Click or Ctrl+Tab
- **Duplicate**: Copy current image to new tab

Command-Line Interface
----------------------

GUI Image Studio provides several command-line tools for automation and batch processing.

Designer Launcher
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    gui-image-studio-designer [options]

**Options:**
- ``--help``: Show help message
- ``--version``: Show version information
- ``--file <path>``: Open specific file on startup
- ``--new``: Start with new image
- ``--fullscreen``: Launch in fullscreen mode

**Examples:**

.. code-block:: bash

    # Launch designer
    gui-image-studio-designer

    # Open specific file
    gui-image-studio-designer --file my_image.png

    # Start with new image
    gui-image-studio-designer --new

Sample Creator
~~~~~~~~~~~~~~

.. code-block:: bash

    gui-image-studio-create-samples [options]

**Options:**
- ``--output <dir>``: Output directory (default: sample_images)
- ``--count <n>``: Number of samples to create
- ``--size <WxH>``: Image dimensions
- ``--formats <list>``: File formats to create

**Examples:**

.. code-block:: bash

    # Create default samples
    gui-image-studio-create-samples

    # Create in specific directory
    gui-image-studio-create-samples --output test_images

    # Create specific size samples
    gui-image-studio-create-samples --size 256x256

Image Generator
~~~~~~~~~~~~~~~

.. code-block:: bash

    gui-image-studio-generate [options]

**Options:**
- ``--folder <path>``: Input folder path
- ``--output <file>``: Output Python file
- ``--quality <n>``: Compression quality (1-100)
- ``--recursive``: Process subfolders
- ``--formats <list>``: Include specific formats only

**Examples:**

.. code-block:: bash

    # Basic generation
    gui-image-studio-generate --folder images/ --output embedded.py

    # High quality with recursion
    gui-image-studio-generate \
      --folder assets/ \
      --output resources.py \
      --quality 95 \
      --recursive

    # Specific formats only
    gui-image-studio-generate \
      --folder icons/ \
      --output icons.py \
      --formats png,svg

Python API Interface
--------------------

The Python API provides programmatic access to all functionality.

Core Functions
~~~~~~~~~~~~~~

**get_image() Function:**

.. code-block:: python

    from gui_image_studio import get_image

    # Basic usage
    image = get_image("my_image.png", framework="tkinter")

    # With transformations
    image = get_image(
        "photo.jpg",
        framework="customtkinter",
        size=(200, 200),
        rotate=45,
        tint_color=(255, 0, 0),
        tint_intensity=0.3,
        contrast=1.2,
        saturation=1.1,
        grayscale=False,
        transparency=1.0,
        theme="dark"
    )

**embed_images_from_folder() Function:**

.. code-block:: python

    from gui_image_studio import embed_images_from_folder

    # Basic embedding
    embed_images_from_folder(
        folder_path="images/",
        output_file="embedded_images.py",
        compression_quality=85
    )

**create_sample_images() Function:**

.. code-block:: python

    from gui_image_studio import create_sample_images

    # Create samples in default location
    create_sample_images()

    # Create in specific directory
    create_sample_images(output_dir="my_samples")

**Launching the Visual Designer:**

.. code-block:: bash

    # Launch the visual designer
    gui-image-studio-designer

.. code-block:: python

    # Or from Python using subprocess
    import subprocess
    subprocess.run(["gui-image-studio-designer"])

Integration Patterns
~~~~~~~~~~~~~~~~~~~~~

**Tkinter Integration:**

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class MyApp:
        def __init__(self, root):
            self.root = root

            # Load images
            self.icon = get_image("icon.png", framework="tkinter", size=(32, 32))
            self.bg = get_image("background.jpg", framework="tkinter", size=(800, 600))

            # Use in widgets
            self.setup_ui()

        def setup_ui(self):
            # Background label
            bg_label = tk.Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0)

            # Icon button
            icon_btn = tk.Button(
                self.root,
                image=self.icon,
                text="Click Me",
                compound=tk.LEFT
            )
            icon_btn.pack(pady=20)

**CustomTkinter Integration:**

.. code-block:: python

    import customtkinter as ctk
    from gui_image_studio import get_image

    class ModernApp:
        def __init__(self):
            self.root = ctk.CTk()

            # Set theme
            ctk.set_appearance_mode("dark")

            # Load themed images
            self.load_images()
            self.setup_ui()

        def load_images(self):
            self.logo = get_image(
                "logo.png",
                framework="customtkinter",
                size=(100, 100),
                theme="dark"
            )

        def setup_ui(self):
            # Logo display
            logo_label = ctk.CTkLabel(
                self.root,
                image=self.logo,
                text=""
            )
            logo_label.pack(pady=20)

Keyboard Shortcuts
------------------

**Global Shortcuts:**

.. code-block:: text

    File Operations:
    Ctrl+N          New image
    Ctrl+O          Open image
    Ctrl+S          Save image
    Ctrl+Shift+S    Save As
    Ctrl+Q          Quit application

    Edit Operations:
    Ctrl+Z          Undo
    Ctrl+Y          Redo
    Ctrl+X          Cut
    Ctrl+C          Copy
    Ctrl+V          Paste
    Ctrl+A          Select All
    Delete          Clear selection

    View Operations:
    Ctrl++          Zoom In
    Ctrl+-          Zoom Out
    Ctrl+0          Actual Size
    Ctrl+F          Fit to Window
    F11             Toggle Fullscreen

**Tool Shortcuts:**

.. code-block:: text

    B               Brush Tool
    P               Pencil Tool
    E               Eraser Tool
    R               Rectangle Tool
    C               Circle Tool
    L               Line Tool
    T               Text Tool
    F               Fill Tool
    M               Move Tool
    S               Select Tool

**Modifier Keys:**

.. code-block:: text

    Shift           Constrain proportions/angles
    Ctrl            Precision mode
    Alt             Alternative behavior
    Space           Temporary pan tool

Customization Options
---------------------

Theme Customization
~~~~~~~~~~~~~~~~~~~

The designer supports theme customization:

.. code-block:: bash

    # Launch with theme options
    gui-image-studio-designer --theme dark

.. code-block:: python

    # Or programmatically with theme setup
    import customtkinter as ctk
    import subprocess

    # Set global theme
    ctk.set_appearance_mode("dark")  # "light", "dark", "system"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

    # Launch with theme
    subprocess.run(["gui-image-studio-designer", "--theme", "dark"])

Workspace Layout
~~~~~~~~~~~~~~~~

Customize the workspace layout:

**Panel Arrangement:**
- Drag panels to reposition
- Resize panels by dragging borders
- Hide/show panels via View menu
- Save layout preferences

**Toolbar Customization:**
- Right-click toolbar to customize
- Add/remove tool buttons
- Rearrange button order
- Create custom tool groups

Settings and Preferences
~~~~~~~~~~~~~~~~~~~~~~~~

Access settings through **Edit → Preferences**:

**General Settings:**
- Default image size
- Auto-save interval
- Recent files count
- Startup behavior

**Tool Settings:**
- Default brush size
- Color picker behavior
- Selection options
- Grid settings

**Performance Settings:**
- Memory usage limits
- Undo history size
- Preview quality
- Hardware acceleration

Accessibility Features
----------------------

GUI Image Studio includes accessibility features:

**Visual Accessibility:**
- High contrast themes
- Scalable UI elements
- Customizable font sizes
- Color blind friendly palettes

**Keyboard Accessibility:**
- Full keyboard navigation
- Tab order optimization
- Shortcut key customization
- Screen reader compatibility

**Motor Accessibility:**
- Adjustable click sensitivity
- Sticky keys support
- Mouse alternatives
- Touch screen support

Tips and Best Practices
------------------------

Workflow Optimization
~~~~~~~~~~~~~~~~~~~~~

1. **Use Keyboard Shortcuts**: Learn common shortcuts for faster work
2. **Customize Workspace**: Arrange panels for your workflow
3. **Save Templates**: Create templates for common image sizes
4. **Use Layers**: Work non-destructively when possible

Performance Tips
~~~~~~~~~~~~~~~~

1. **Appropriate Image Sizes**: Don't work with unnecessarily large images
2. **Regular Saves**: Save work frequently to prevent data loss
3. **Memory Management**: Close unused images to free memory
4. **Hardware Acceleration**: Enable if available

Quality Guidelines
~~~~~~~~~~~~~~~~~~

1. **Use High Quality Sources**: Start with the best possible images
2. **Appropriate Formats**: PNG for graphics, JPEG for photos
3. **Compression Settings**: Balance file size and quality
4. **Color Management**: Use consistent color profiles

Getting Help
------------

**Built-in Help:**
- Press F1 for context-sensitive help
- Use Help menu for documentation
- Hover over tools for tooltips

**Online Resources:**
- Documentation: https://stntg.github.io/gui-image-studio/
- Examples: :doc:`../examples/index`
- API Reference: :doc:`../api/index`

**Community Support:**
- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share tips
- Examples Gallery: See what others have created

Next Steps
----------

Now that you understand the interface:

1. **Try the Tools**: :doc:`image_processing`
2. **Learn Advanced Features**: :doc:`../examples/index`
3. **Explore API Integration**: :doc:`api_usage`
4. **Build Your First App**: :doc:`gui_development`
