Image Studio GUI Module
=======================

The ``image_studio`` module provides the main GUI application class and related components for the GUI Image Studio application.

.. automodule:: gui_image_studio.image_studio
   :members:
   :undoc-members:
   :show-inheritance:

Main Application Class
----------------------

ImageStudio
~~~~~~~~~~~

.. autoclass:: gui_image_studio.image_studio.ImageStudio
   :members:
   :undoc-members:
   :show-inheritance:

The main GUI application class that provides a complete image editing interface.

**Initialization:**

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import ImageStudio

    root = tk.Tk()
    app = ImageStudio(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

**Key Features:**

* Professional image editing interface
* Real-time preview capabilities
* Undo/redo functionality
* Theme support (light/dark)
* Plugin architecture
* Batch processing tools
* Animation timeline (for GIFs)

**Main Components:**

* **Canvas Area**: Central image display and editing area
* **Tool Palette**: Left sidebar with editing tools
* **Properties Panel**: Right sidebar with tool settings
* **Menu Bar**: Standard application menus
* **Status Bar**: Information and progress display
* **Timeline**: Animation frame management (when applicable)

**Methods:**

load_image
^^^^^^^^^^

.. automethod:: gui_image_studio.image_studio.ImageStudio.load_image

Load an image into the editor.

**Parameters:**
  * ``file_path`` (str, optional): Path to image file. If None, opens file dialog.

**Example:**

.. code-block:: python

    # Load specific file
    app.load_image("photo.jpg")

    # Open file dialog
    app.load_image()

save_image
^^^^^^^^^^

.. automethod:: gui_image_studio.image_studio.ImageStudio.save_image

Save the current image.

**Parameters:**
  * ``file_path`` (str, optional): Path for saving. If None, opens save dialog.
  * ``quality`` (int, optional): JPEG quality (1-100, default 95)

**Example:**

.. code-block:: python

    # Save to specific file
    app.save_image("output.png")

    # Open save dialog
    app.save_image()

apply_filter
^^^^^^^^^^^^

.. automethod:: gui_image_studio.image_studio.ImageStudio.apply_filter

Apply a filter to the current image.

**Parameters:**
  * ``filter_name`` (str): Name of the filter to apply
  * ``parameters`` (dict, optional): Filter-specific parameters

**Example:**

.. code-block:: python

    # Apply blur filter
    app.apply_filter("blur", {"radius": 2.0})

    # Apply tint
    app.apply_filter("tint", {"color": "#FF6B6B", "opacity": 0.3})

undo
^^^^

.. automethod:: gui_image_studio.image_studio.ImageStudio.undo

Undo the last operation.

**Example:**

.. code-block:: python

    app.undo()

redo
^^^^

.. automethod:: gui_image_studio.image_studio.ImageStudio.redo

Redo the last undone operation.

**Example:**

.. code-block:: python

    app.redo()

set_theme
^^^^^^^^^

.. automethod:: gui_image_studio.image_studio.ImageStudio.set_theme

Change the application theme.

**Parameters:**
  * ``theme_name`` (str): Theme name ("light", "dark", or custom theme)

**Example:**

.. code-block:: python

    app.set_theme("dark")

GUI Components
--------------

ToolPalette
~~~~~~~~~~~

.. autoclass:: gui_image_studio.image_studio.ToolPalette
   :members:
   :undoc-members:

Left sidebar containing editing tools.

**Available Tools:**

* **Selection Tools**: Rectangle, ellipse, lasso, magic wand
* **Drawing Tools**: Brush, pencil, eraser, fill bucket
* **Transform Tools**: Move, rotate, scale, crop
* **Filter Tools**: Quick access to common filters

**Usage:**

.. code-block:: python

    # Access current tool
    current_tool = app.tool_palette.current_tool

    # Set tool programmatically
    app.tool_palette.set_tool("brush")

PropertiesPanel
~~~~~~~~~~~~~~~

.. autoclass:: gui_image_studio.image_studio.PropertiesPanel
   :members:
   :undoc-members:

Right sidebar showing tool properties and image information.

**Sections:**

* **Tool Properties**: Settings for the current tool
* **Image Information**: Size, format, color mode
* **History**: Recent operations
* **Layers**: Layer management (if supported)

**Usage:**

.. code-block:: python

    # Get image info
    info = app.properties_panel.get_image_info()
    print(f"Size: {info['size']}, Format: {info['format']}")

ImageCanvas
~~~~~~~~~~~

.. autoclass:: gui_image_studio.image_studio.ImageCanvas
   :members:
   :undoc-members:

Central canvas area for image display and editing.

**Features:**

* Zoom and pan capabilities
* Real-time editing preview
* Grid and ruler overlays
* Selection visualization
* Multi-layer support

**Usage:**

.. code-block:: python

    # Zoom operations
    app.canvas.zoom_in()
    app.canvas.zoom_out()
    app.canvas.fit_to_window()

    # Get canvas state
    zoom_level = app.canvas.get_zoom_level()
    selection = app.canvas.get_selection()

Timeline
~~~~~~~~

.. autoclass:: gui_image_studio.image_studio.Timeline
   :members:
   :undoc-members:

Animation timeline for GIF editing (shown when working with animated images).

**Features:**

* Frame-by-frame editing
* Timing adjustment
* Onion skinning
* Playback controls

**Usage:**

.. code-block:: python

    # Timeline operations (when animation is loaded)
    app.timeline.add_frame()
    app.timeline.delete_frame(frame_index)
    app.timeline.set_frame_duration(frame_index, 100)  # 100ms

Event System
------------

The ImageStudio class uses an event-driven architecture for communication between components.

**Event Types:**

* ``image_loaded``: Fired when a new image is loaded
* ``image_modified``: Fired when the image is changed
* ``tool_changed``: Fired when the active tool changes
* ``selection_changed``: Fired when the selection changes

**Event Handling:**

.. code-block:: python

    def on_image_loaded(event_data):
        print(f"Image loaded: {event_data['file_path']}")

    # Subscribe to events
    app.subscribe("image_loaded", on_image_loaded)

    # Fire custom events
    app.fire_event("custom_event", {"data": "value"})

Customization
-------------

**Custom Tools**

Create custom tools by extending the base Tool class:

.. code-block:: python

    from gui_image_studio.image_studio import Tool

    class CustomTool(Tool):
        def __init__(self):
            super().__init__("Custom Tool", "custom_icon.png")

        def on_mouse_down(self, x, y):
            # Handle mouse down event
            pass

        def on_mouse_drag(self, x, y):
            # Handle mouse drag event
            pass

        def on_mouse_up(self, x, y):
            # Handle mouse up event
            pass

    # Register the tool
    app.tool_palette.register_tool(CustomTool())

**Custom Filters**

Create custom filters:

.. code-block:: python

    from gui_image_studio.image_studio import Filter

    class CustomFilter(Filter):
        def __init__(self):
            super().__init__("Custom Filter", "custom_filter")

        def apply(self, image, parameters=None):
            # Apply custom processing
            processed_image = self.process_image(image, parameters)
            return processed_image

    # Register the filter
    app.register_filter(CustomFilter())

**Custom Themes**

Create custom themes:

.. code-block:: python

    custom_theme = {
        "name": "custom_theme",
        "colors": {
            "bg_primary": "#2B2B2B",
            "bg_secondary": "#3C3C3C",
            "fg_primary": "#FFFFFF",
            "fg_secondary": "#CCCCCC",
            "accent": "#007ACC",
            "border": "#555555"
        },
        "fonts": {
            "default": ("Segoe UI", 9),
            "heading": ("Segoe UI", 12, "bold"),
            "monospace": ("Consolas", 9)
        }
    }

    app.register_theme(custom_theme)
    app.set_theme("custom_theme")

Configuration
-------------

**Application Settings**

Configure the application behavior:

.. code-block:: python

    # Set default settings
    app.settings.update({
        "auto_save": True,
        "auto_save_interval": 300,  # 5 minutes
        "max_undo_levels": 50,
        "default_quality": 95,
        "show_grid": False,
        "grid_size": 10
    })

**Keyboard Shortcuts**

Customize keyboard shortcuts:

.. code-block:: python

    # Default shortcuts
    shortcuts = {
        "Ctrl+O": "open_file",
        "Ctrl+S": "save_file",
        "Ctrl+Z": "undo",
        "Ctrl+Y": "redo",
        "Ctrl++": "zoom_in",
        "Ctrl+-": "zoom_out",
        "Ctrl+0": "fit_to_window"
    }

    app.set_shortcuts(shortcuts)

Performance Considerations
--------------------------

**Memory Management**

* Large images are automatically tiled for display
* Undo history is limited to prevent memory issues
* Temporary files are cleaned up automatically

**Threading**

* Long operations run in background threads
* Progress indicators show operation status
* UI remains responsive during processing

**Optimization Tips**

.. code-block:: python

    # Optimize for large images
    app.settings["tile_size"] = 512  # Smaller tiles for large images
    app.settings["preview_quality"] = "fast"  # Faster preview rendering

    # Optimize for performance
    app.settings["real_time_preview"] = False  # Disable for complex operations
    app.settings["max_image_size"] = (4096, 4096)  # Limit maximum image size

Error Handling
--------------

The ImageStudio class provides comprehensive error handling:

**Common Exceptions:**

* ``ImageStudioError``: Base exception for application errors
* ``UnsupportedFormatError``: Unsupported image format
* ``InsufficientMemoryError``: Not enough memory for operation
* ``OperationCancelledError``: User cancelled operation

**Error Handling Example:**

.. code-block:: python

    try:
        app.load_image("large_image.jpg")
    except gui_image_studio.UnsupportedFormatError:
        print("Image format not supported")
    except gui_image_studio.InsufficientMemoryError:
        print("Not enough memory to load image")
    except Exception as e:
        print(f"Unexpected error: {e}")

**Error Recovery:**

The application includes automatic error recovery:

* Corrupted files are handled gracefully
* Memory errors trigger cleanup and retry
* UI state is preserved during errors
* Auto-save prevents data loss

Integration Examples
--------------------

**Embedding in Existing Applications**

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import ImageStudio

    class MyApplication:
        def __init__(self):
            self.root = tk.Tk()
            self.setup_ui()

        def setup_ui(self):
            # Create main frame
            main_frame = tk.Frame(self.root)
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Add other components
            toolbar = tk.Frame(main_frame)
            toolbar.pack(side=tk.TOP, fill=tk.X)

            # Embed ImageStudio
            self.image_studio = ImageStudio(main_frame)
            self.image_studio.pack(fill=tk.BOTH, expand=True)

            # Connect to events
            self.image_studio.subscribe("image_loaded", self.on_image_loaded)

        def on_image_loaded(self, event_data):
            # Handle image loaded event
            print(f"Image loaded in embedded editor: {event_data['file_path']}")

**Plugin Development**

.. code-block:: python

    from gui_image_studio.image_studio import Plugin

    class MyPlugin(Plugin):
        def __init__(self):
            super().__init__("My Plugin", "1.0.0")

        def initialize(self, app):
            # Add menu items
            app.add_menu_item("Plugins", "My Plugin", self.run_plugin)

            # Add toolbar button
            app.add_toolbar_button("My Plugin", "plugin_icon.png", self.run_plugin)

        def run_plugin(self):
            # Plugin functionality
            current_image = self.app.get_current_image()
            if current_image:
                processed = self.process_image(current_image)
                self.app.set_current_image(processed)

    # Register plugin
    app.register_plugin(MyPlugin())
