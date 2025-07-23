First Steps
===========

Welcome to GUI Image Studio! This guide will help you get started with the basics of using GUI Image Studio for image processing and GUI development.

Quick Start Checklist
----------------------

Before we begin, make sure you have:

✅ **Installed GUI Image Studio** (see :doc:`installation_guide`)
✅ **Python 3.8+** installed
✅ **Basic Python knowledge**
✅ **A few test images** (or use our sample creator)

Your First Image
-----------------

Let's start with the most basic operation - loading and displaying an image.

**Step 1: Create Sample Images**

First, let's create some sample images to work with:

.. code-block:: bash

    gui-image-studio-create-samples

This creates a `sample_images/` folder with various test images.

**Step 2: Load Your First Image**

.. code-block:: python

    from gui_image_studio import get_image
    import tkinter as tk

    # Create a simple window
    root = tk.Tk()
    root.title("My First GUI Image Studio App")

    # Load an image
    image = get_image(
        "sample_icon",  # Use built-in sample
        framework="tkinter",
        size=(64, 64)
    )

    # Display it
    label = tk.Label(root, image=image)
    label.pack(pady=20)

    # Keep reference to prevent garbage collection
    label.image = image

    root.mainloop()

**Step 3: Run Your First App**

Save the code above as `first_app.py` and run:

.. code-block:: bash

    python first_app.py

Congratulations! You've created your first GUI Image Studio application.

Understanding the Basics
-------------------------

Core Concepts
~~~~~~~~~~~~~

**1. Framework Support**

GUI Image Studio supports two main GUI frameworks:

.. code-block:: python

    # For standard tkinter
    image = get_image("my_image.png", framework="tkinter")

    # For modern customtkinter
    image = get_image("my_image.png", framework="customtkinter")

**2. Image Sources**

You can load images from various sources:

.. code-block:: python

    # Built-in samples
    image = get_image("sample_icon", framework="tkinter")

    # Local files
    image = get_image("path/to/image.png", framework="tkinter")

    # From embedded resources (after using embed_images_from_folder)
    image = get_image("my_embedded_image", framework="tkinter")

**3. Image Transformations**

Apply transformations during loading:

.. code-block:: python

    image = get_image(
        "sample_photo",
        framework="tkinter",
        size=(200, 150),           # Resize
        rotate=45,                 # Rotate 45 degrees
        tint_color=(255, 0, 0),   # Red tint
        tint_intensity=0.3,        # 30% tint strength
        contrast=1.2,              # Increase contrast
        saturation=1.1,            # Boost saturation
        grayscale=False            # Keep in color
    )

Working with Different Frameworks
----------------------------------

Tkinter Example
~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class ImageApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Tkinter Image App")

            # Load and display image
            self.image = get_image(
                "sample_icon",
                framework="tkinter",
                size=(100, 100)
            )

            self.label = tk.Label(root, image=self.image)
            self.label.pack(pady=20)

            # Add a button to change image
            self.button = tk.Button(
                root,
                text="Change Color",
                command=self.change_color
            )
            self.button.pack()

        def change_color(self):
            # Load same image with different tint
            self.image = get_image(
                "sample_icon",
                framework="tkinter",
                size=(100, 100),
                tint_color=(0, 255, 0),  # Green tint
                tint_intensity=0.5
            )
            self.label.configure(image=self.image)

    if __name__ == "__main__":
        root = tk.Tk()
        app = ImageApp(root)
        root.mainloop()

CustomTkinter Example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import customtkinter as ctk
    from gui_image_studio import get_image

    class ModernImageApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Modern Image App")

            # Set appearance mode
            ctk.set_appearance_mode("dark")

            # Load image for customtkinter
            self.image = get_image(
                "sample_icon",
                framework="customtkinter",
                size=(100, 100),
                theme="dark"  # Use dark theme
            )

            # Create CTkLabel with image
            self.label = ctk.CTkLabel(
                root,
                image=self.image,
                text=""  # No text, just image
            )
            self.label.pack(pady=20)

            # Add modern button
            self.button = ctk.CTkButton(
                root,
                text="Apply Effect",
                command=self.apply_effect
            )
            self.button.pack(pady=10)

        def apply_effect(self):
            # Apply a cool effect
            self.image = get_image(
                "sample_icon",
                framework="customtkinter",
                size=(100, 100),
                theme="dark",
                rotate=15,
                tint_color=(100, 200, 255),  # Cool blue
                tint_intensity=0.4,
                contrast=1.3
            )
            self.label.configure(image=self.image)

    if __name__ == "__main__":
        root = ctk.CTk()
        app = ModernImageApp(root)
        root.mainloop()

Creating Your Image Library
----------------------------

Embedding Images from Folders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For distribution, you'll want to embed images directly in your Python code:

**Step 1: Organize Your Images**

.. code-block:: text

    my_project/
    ├── images/
    │   ├── icons/
    │   │   ├── home.png
    │   │   ├── save.png
    │   │   └── open.png
    │   └── backgrounds/
    │       ├── main_bg.jpg
    │       └── splash.png
    └── src/
        └── my_app.py

**Step 2: Generate Embedded Images**

.. code-block:: bash

    # Generate from icons folder
    gui-image-studio-generate \
      --folder images/icons \
      --output src/icons.py \
      --quality 95

    # Generate from backgrounds folder
    gui-image-studio-generate \
      --folder images/backgrounds \
      --output src/backgrounds.py \
      --quality 80

**Step 3: Use Embedded Images**

.. code-block:: python

    # Import your embedded images
    import sys
    sys.path.append('src')

    from gui_image_studio import get_image
    import tkinter as tk

    # Now you can use embedded images by name
    root = tk.Tk()

    # Use embedded icons (filename without extension)
    home_icon = get_image("home", framework="tkinter", size=(32, 32))
    save_icon = get_image("save", framework="tkinter", size=(32, 32))

    # Create buttons with icons
    home_btn = tk.Button(root, image=home_icon, text="Home", compound=tk.LEFT)
    save_btn = tk.Button(root, image=save_icon, text="Save", compound=tk.LEFT)

    home_btn.pack(pady=5)
    save_btn.pack(pady=5)

    root.mainloop()

Working with Animated GIFs
---------------------------

GUI Image Studio supports animated GIF processing:

.. code-block:: python

    from gui_image_studio import get_image
    import tkinter as tk

    class AnimatedApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Animated GIF Example")

            # Load animated GIF
            self.animation_data = get_image(
                "sample_animation.gif",  # You'll need an animated GIF
                framework="tkinter",
                size=(200, 200),
                animated=True,
                frame_delay=100
            )

            # Extract frames and delay
            self.frames = self.animation_data["animated_frames"]
            self.delay = self.animation_data["frame_delay"]
            self.current_frame = 0

            # Create label for animation
            self.label = tk.Label(root)
            self.label.pack(pady=20)

            # Start animation
            self.animate()

        def animate(self):
            # Display current frame
            self.label.configure(image=self.frames[self.current_frame])

            # Move to next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)

            # Schedule next frame
            self.root.after(self.delay, self.animate)

    if __name__ == "__main__":
        root = tk.Tk()
        app = AnimatedApp(root)
        root.mainloop()

Using the Visual Designer
--------------------------

GUI Image Studio includes a visual designer for creating and editing images:

**Launch the Designer**

.. code-block:: bash

    gui-image-studio-designer

**Designer Features:**

- **Drawing Tools**: Brush, pencil, eraser, shapes
- **Image Transformations**: Resize, rotate, flip, filters
- **Multiple Images**: Work with several images at once
- **Real-time Preview**: See changes instantly
- **Code Generation**: Generate Python code for your images
- **Export Options**: Save in various formats

**Basic Designer Workflow:**

1. **Create New Image** or **Open Existing**
2. **Use Drawing Tools** to create/edit
3. **Apply Transformations** as needed
4. **Preview Results** in real-time
5. **Generate Code** for use in your applications
6. **Export** final images

Common Patterns
---------------

Icon Management
~~~~~~~~~~~~~~~

.. code-block:: python

    from gui_image_studio import get_image
    import tkinter as tk

    class IconManager:
        def __init__(self, framework="tkinter", size=(24, 24)):
            self.framework = framework
            self.size = size
            self.cache = {}

        def get_icon(self, name, **kwargs):
            # Create cache key
            key = f"{name}_{kwargs}"

            if key not in self.cache:
                self.cache[key] = get_image(
                    name,
                    framework=self.framework,
                    size=self.size,
                    **kwargs
                )

            return self.cache[key]

    # Usage
    icons = IconManager(size=(32, 32))

    root = tk.Tk()

    # Get icons with caching
    home_icon = icons.get_icon("home")
    save_icon = icons.get_icon("save", tint_color=(0, 255, 0))

    tk.Button(root, image=home_icon).pack()
    tk.Button(root, image=save_icon).pack()

    root.mainloop()

Theme-Aware Images
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gui_image_studio import get_image
    import customtkinter as ctk

    class ThemedApp:
        def __init__(self):
            self.root = ctk.CTk()
            self.current_theme = "dark"

            self.setup_ui()
            self.update_theme()

        def setup_ui(self):
            # Theme toggle button
            self.theme_btn = ctk.CTkButton(
                self.root,
                text="Toggle Theme",
                command=self.toggle_theme
            )
            self.theme_btn.pack(pady=10)

            # Image label
            self.image_label = ctk.CTkLabel(self.root, text="")
            self.image_label.pack(pady=20)

        def toggle_theme(self):
            # Switch theme
            self.current_theme = "light" if self.current_theme == "dark" else "dark"
            ctk.set_appearance_mode(self.current_theme)
            self.update_theme()

        def update_theme(self):
            # Load theme-appropriate image
            image = get_image(
                "sample_icon",
                framework="customtkinter",
                size=(100, 100),
                theme=self.current_theme
            )
            self.image_label.configure(image=image)

    if __name__ == "__main__":
        app = ThemedApp()
        app.root.mainloop()

Best Practices
--------------

Performance Tips
~~~~~~~~~~~~~~~~

1. **Cache Images**: Don't reload the same image repeatedly
2. **Appropriate Sizes**: Don't load huge images for small displays
3. **Use Compression**: Set appropriate quality levels for embedded images
4. **Lazy Loading**: Load images only when needed

.. code-block:: python

    # Good: Cache frequently used images
    class ImageCache:
        def __init__(self):
            self._cache = {}

        def get_image(self, name, **kwargs):
            key = f"{name}_{hash(str(kwargs))}"
            if key not in self._cache:
                self._cache[key] = get_image(name, **kwargs)
            return self._cache[key]

    # Usage
    cache = ImageCache()
    image = cache.get_image("icon", framework="tkinter", size=(32, 32))

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

    from gui_image_studio import get_image
    import tkinter as tk

    def safe_load_image(name, **kwargs):
        try:
            return get_image(name, **kwargs)
        except FileNotFoundError:
            print(f"Image '{name}' not found, using placeholder")
            # Return a placeholder or default image
            return get_image("sample_icon", **kwargs)
        except Exception as e:
            print(f"Error loading image '{name}': {e}")
            return None

    # Usage
    image = safe_load_image("might_not_exist.png", framework="tkinter")
    if image:
        label = tk.Label(root, image=image)
        label.pack()

Code Organization
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Good: Organize image resources
    class AppResources:
        def __init__(self, framework="tkinter"):
            self.framework = framework

            # Define all your images in one place
            self.icons = {
                'home': self._load_icon('home'),
                'save': self._load_icon('save'),
                'open': self._load_icon('open'),
            }

            self.backgrounds = {
                'main': self._load_bg('main_background'),
                'splash': self._load_bg('splash_screen'),
            }

        def _load_icon(self, name):
            return get_image(
                name,
                framework=self.framework,
                size=(24, 24)
            )

        def _load_bg(self, name):
            return get_image(
                name,
                framework=self.framework,
                size=(800, 600)
            )

    # Usage
    resources = AppResources("customtkinter")
    home_icon = resources.icons['home']

Next Steps
----------

Now that you understand the basics:

1. **Explore the Interface**: :doc:`interface_overview`
2. **Learn Image Processing**: :doc:`image_processing`
3. **Try Advanced Features**: :doc:`../examples/index`
4. **Read API Documentation**: :doc:`../api/index`

Common Next Actions
~~~~~~~~~~~~~~~~~~~

**For GUI Developers:**
- Learn about theme integration
- Explore customtkinter support
- Study the icon management patterns

**For Image Processing:**
- Experiment with transformations
- Learn about batch processing
- Try the visual designer

**For Distribution:**
- Master image embedding
- Optimize compression settings
- Set up build processes

Troubleshooting
---------------

**Image Not Displaying:**
- Check if image file exists
- Verify framework parameter matches your GUI
- Ensure you keep a reference to prevent garbage collection

**Performance Issues:**
- Reduce image sizes
- Use appropriate compression
- Implement caching

**Import Errors:**
- Verify installation: `pip show gui-image-studio`
- Check Python version compatibility
- Review dependency installation

Getting Help
------------

- **Documentation**: :doc:`../api/index`
- **Examples**: :doc:`../examples/index`
- **Issues**: https://github.com/stntg/gui-image-studio/issues
- **Discussions**: GitHub Discussions

Remember: Start simple, experiment often, and build up complexity gradually!
