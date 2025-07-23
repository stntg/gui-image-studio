Theme System
============

GUI Image Studio includes a comprehensive theme system that adapts images for different visual contexts and GUI frameworks. This guide covers theme usage, customization, and integration patterns.

Overview of Theme System
-------------------------

The theme system provides:

- **Built-in themes** for common use cases
- **Framework-specific optimization** for tkinter and customtkinter
- **Automatic color adaptation** based on theme context
- **Dynamic theme switching** in applications
- **Custom theme creation** for specific needs
- **Theme-aware image caching** for performance

Built-in Themes
----------------

Default Themes
~~~~~~~~~~~~~~

GUI Image Studio includes three primary themes:

.. code-block:: python

    from gui_image_studio import get_image

    # Default theme (neutral, works everywhere)
    default_image = get_image(
        "icon.png",
        framework="tkinter",
        theme="default",
        size=(64, 64)
    )

    # Light theme (optimized for light backgrounds)
    light_image = get_image(
        "icon.png",
        framework="tkinter",
        theme="light",
        size=(64, 64)
    )

    # Dark theme (optimized for dark backgrounds)
    dark_image = get_image(
        "icon.png",
        framework="customtkinter",
        theme="dark",
        size=(64, 64)
    )

Theme Characteristics
~~~~~~~~~~~~~~~~~~~~~

**Default Theme:**
- Neutral color balance
- Works on any background
- No automatic adjustments
- Best for general-purpose use

**Light Theme:**
- Optimized for light backgrounds
- Slightly darker borders/shadows
- Enhanced contrast for visibility
- Ideal for traditional desktop applications

**Dark Theme:**
- Optimized for dark backgrounds
- Lighter edges and highlights
- Reduced harsh contrasts
- Perfect for modern dark UIs

Framework Integration
---------------------

Tkinter Theme Integration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class ThemedTkinterApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Themed Tkinter App")

            # Set background color
            self.root.configure(bg='white')  # Light theme

            # Load theme-appropriate images
            self.setup_images()
            self.setup_ui()

        def setup_images(self):
            """Load images with light theme."""
            self.home_icon = get_image(
                "home_icon",
                framework="tkinter",
                theme="light",
                size=(32, 32)
            )

            self.save_icon = get_image(
                "save_icon",
                framework="tkinter",
                theme="light",
                size=(32, 32)
            )

            self.background = get_image(
                "app_background",
                framework="tkinter",
                theme="light",
                size=(800, 600)
            )

        def setup_ui(self):
            # Background
            bg_label = tk.Label(self.root, image=self.background)
            bg_label.place(x=0, y=0)

            # Toolbar with themed icons
            toolbar = tk.Frame(self.root, bg='white')
            toolbar.pack(side=tk.TOP, fill=tk.X)

            home_btn = tk.Button(
                toolbar,
                image=self.home_icon,
                text="Home",
                compound=tk.LEFT,
                bg='white'
            )
            home_btn.pack(side=tk.LEFT, padx=5, pady=5)

            save_btn = tk.Button(
                toolbar,
                image=self.save_icon,
                text="Save",
                compound=tk.LEFT,
                bg='white'
            )
            save_btn.pack(side=tk.LEFT, padx=5, pady=5)

    # Usage
    if __name__ == "__main__":
        root = tk.Tk()
        app = ThemedTkinterApp(root)
        root.mainloop()

CustomTkinter Theme Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import customtkinter as ctk
    from gui_image_studio import get_image

    class ThemedCustomTkinterApp:
        def __init__(self):
            # Set CustomTkinter appearance
            ctk.set_appearance_mode("dark")  # "light", "dark", "system"
            ctk.set_default_color_theme("blue")

            self.root = ctk.CTk()
            self.root.title("Themed CustomTkinter App")
            self.root.geometry("800x600")

            self.current_theme = "dark"

            self.setup_images()
            self.setup_ui()

        def setup_images(self):
            """Load images with current theme."""
            self.logo = get_image(
                "app_logo",
                framework="customtkinter",
                theme=self.current_theme,
                size=(100, 100)
            )

            self.toolbar_icons = {
                'new': get_image(
                    "new_icon",
                    framework="customtkinter",
                    theme=self.current_theme,
                    size=(24, 24)
                ),
                'open': get_image(
                    "open_icon",
                    framework="customtkinter",
                    theme=self.current_theme,
                    size=(24, 24)
                ),
                'save': get_image(
                    "save_icon",
                    framework="customtkinter",
                    theme=self.current_theme,
                    size=(24, 24)
                )
            }

        def setup_ui(self):
            # Main container
            main_frame = ctk.CTkFrame(self.root)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Header with logo
            header = ctk.CTkFrame(main_frame)
            header.pack(fill="x", pady=(0, 20))

            logo_label = ctk.CTkLabel(
                header,
                image=self.logo,
                text=""
            )
            logo_label.pack(side="left", padx=20, pady=20)

            # Theme toggle button
            theme_btn = ctk.CTkButton(
                header,
                text="Toggle Theme",
                command=self.toggle_theme
            )
            theme_btn.pack(side="right", padx=20, pady=20)

            # Toolbar
            toolbar = ctk.CTkFrame(main_frame)
            toolbar.pack(fill="x", pady=(0, 20))

            # Toolbar buttons with icons
            self.toolbar_buttons = {}
            for name, icon in self.toolbar_icons.items():
                btn = ctk.CTkButton(
                    toolbar,
                    image=icon,
                    text=name.capitalize(),
                    width=100,
                    command=lambda n=name: self.toolbar_action(n)
                )
                btn.pack(side="left", padx=10, pady=10)
                self.toolbar_buttons[name] = btn

        def toggle_theme(self):
            """Toggle between light and dark themes."""
            if self.current_theme == "dark":
                self.current_theme = "light"
                ctk.set_appearance_mode("light")
            else:
                self.current_theme = "dark"
                ctk.set_appearance_mode("dark")

            # Reload images with new theme
            self.setup_images()
            self.update_ui_images()

        def update_ui_images(self):
            """Update UI elements with new themed images."""
            # Update logo
            logo_label = self.root.winfo_children()[0].winfo_children()[0].winfo_children()[0]
            logo_label.configure(image=self.logo)

            # Update toolbar icons
            for name, button in self.toolbar_buttons.items():
                button.configure(image=self.toolbar_icons[name])

        def toolbar_action(self, action):
            print(f"Toolbar action: {action}")

        def run(self):
            self.root.mainloop()

    # Usage
    if __name__ == "__main__":
        app = ThemedCustomTkinterApp()
        app.run()

Dynamic Theme Switching
------------------------

Theme Manager Class
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class ThemeManager:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.current_theme = "default"
            self.image_cache = {}
            self.theme_callbacks = []

        def set_theme(self, theme_name):
            """Change the current theme."""
            if theme_name != self.current_theme:
                old_theme = self.current_theme
                self.current_theme = theme_name

                # Clear cache to force reload with new theme
                self.image_cache.clear()

                # Notify callbacks
                for callback in self.theme_callbacks:
                    callback(old_theme, theme_name)

        def get_current_theme(self):
            """Get the current theme name."""
            return self.current_theme

        def load_image(self, image_name, **kwargs):
            """Load image with current theme."""
            # Create cache key
            cache_key = f"{image_name}_{self.current_theme}_{hash(str(sorted(kwargs.items())))}"

            if cache_key not in self.image_cache:
                self.image_cache[cache_key] = get_image(
                    image_name,
                    framework=self.framework,
                    theme=self.current_theme,
                    **kwargs
                )

            return self.image_cache[cache_key]

        def register_theme_callback(self, callback):
            """Register a callback for theme changes."""
            self.theme_callbacks.append(callback)

        def unregister_theme_callback(self, callback):
            """Unregister a theme change callback."""
            if callback in self.theme_callbacks:
                self.theme_callbacks.remove(callback)

        def preload_images(self, image_list, **kwargs):
            """Preload images for all themes."""
            themes = ["default", "light", "dark"]

            for theme in themes:
                old_theme = self.current_theme
                self.current_theme = theme

                for image_name in image_list:
                    self.load_image(image_name, **kwargs)

                self.current_theme = old_theme

    # Usage example
    class ThemeAwareApplication:
        def __init__(self, root):
            self.root = root
            self.theme_manager = ThemeManager("customtkinter")

            # Register for theme changes
            self.theme_manager.register_theme_callback(self.on_theme_changed)

            self.setup_ui()

        def setup_ui(self):
            # Load images using theme manager
            self.icon = self.theme_manager.load_image("app_icon", size=(64, 64))
            self.background = self.theme_manager.load_image("background", size=(800, 600))

            # Create UI elements
            self.icon_label = tk.Label(self.root, image=self.icon)
            self.icon_label.pack(pady=20)

            # Theme selection buttons
            theme_frame = tk.Frame(self.root)
            theme_frame.pack(pady=10)

            for theme in ["default", "light", "dark"]:
                btn = tk.Button(
                    theme_frame,
                    text=theme.capitalize(),
                    command=lambda t=theme: self.change_theme(t)
                )
                btn.pack(side=tk.LEFT, padx=5)

        def change_theme(self, theme_name):
            """Change application theme."""
            self.theme_manager.set_theme(theme_name)

        def on_theme_changed(self, old_theme, new_theme):
            """Handle theme change."""
            print(f"Theme changed from {old_theme} to {new_theme}")

            # Reload images
            self.icon = self.theme_manager.load_image("app_icon", size=(64, 64))
            self.background = self.theme_manager.load_image("background", size=(800, 600))

            # Update UI
            self.icon_label.configure(image=self.icon)

Custom Theme Creation
---------------------

Creating Custom Themes
~~~~~~~~~~~~~~~~~~~~~~~

While GUI Image Studio doesn't support custom theme definitions directly, you can create theme-like behavior by applying consistent transformations:

.. code-block:: python

    class CustomThemeProcessor:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.custom_themes = {
                'corporate': {
                    'tint_color': (0, 100, 200),
                    'tint_intensity': 0.1,
                    'contrast': 1.1,
                    'saturation': 0.9
                },
                'warm': {
                    'tint_color': (255, 200, 150),
                    'tint_intensity': 0.15,
                    'contrast': 1.05,
                    'saturation': 1.1
                },
                'cool': {
                    'tint_color': (150, 200, 255),
                    'tint_intensity': 0.12,
                    'contrast': 1.08,
                    'saturation': 0.95
                },
                'high_contrast': {
                    'contrast': 1.5,
                    'saturation': 1.2,
                    'tint_intensity': 0.0
                },
                'vintage': {
                    'tint_color': (210, 180, 140),
                    'tint_intensity': 0.3,
                    'contrast': 1.2,
                    'saturation': 0.8,
                    'grayscale': False
                }
            }

        def load_themed_image(self, image_name, custom_theme, **kwargs):
            """Load image with custom theme applied."""

            if custom_theme not in self.custom_themes:
                raise ValueError(f"Unknown custom theme: {custom_theme}")

            theme_params = self.custom_themes[custom_theme].copy()

            # Merge with any additional parameters
            theme_params.update(kwargs)

            return get_image(
                image_name,
                framework=self.framework,
                **theme_params
            )

        def create_theme_set(self, image_name, themes=None, **base_kwargs):
            """Create a set of images with different custom themes."""

            if themes is None:
                themes = list(self.custom_themes.keys())

            theme_set = {}

            for theme_name in themes:
                theme_set[theme_name] = self.load_themed_image(
                    image_name,
                    theme_name,
                    **base_kwargs
                )

            return theme_set

    # Usage
    def create_custom_themed_icons():
        processor = CustomThemeProcessor("customtkinter")

        # Create icon set with custom themes
        icon_set = processor.create_theme_set(
            "main_icon",
            themes=['corporate', 'warm', 'cool'],
            size=(64, 64)
        )

        # Use different themed versions
        corporate_icon = icon_set['corporate']
        warm_icon = icon_set['warm']
        cool_icon = icon_set['cool']

        return icon_set

Theme-Aware Components
----------------------

Themed Button Component
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class ThemedButton:
        def __init__(self, parent, image_name, text="", theme_manager=None, **kwargs):
            self.parent = parent
            self.image_name = image_name
            self.text = text
            self.theme_manager = theme_manager or ThemeManager()
            self.kwargs = kwargs

            # Create button
            self.button = tk.Button(
                parent,
                text=text,
                compound=tk.LEFT,
                **kwargs
            )

            # Load initial image
            self.update_image()

            # Register for theme changes
            if self.theme_manager:
                self.theme_manager.register_theme_callback(self.on_theme_changed)

        def update_image(self):
            """Update button image with current theme."""
            image = self.theme_manager.load_image(
                self.image_name,
                size=(24, 24)
            )
            self.button.configure(image=image)

            # Keep reference to prevent garbage collection
            self.button.image = image

        def on_theme_changed(self, old_theme, new_theme):
            """Handle theme change."""
            self.update_image()

        def pack(self, **kwargs):
            self.button.pack(**kwargs)

        def grid(self, **kwargs):
            self.button.grid(**kwargs)

        def configure(self, **kwargs):
            self.button.configure(**kwargs)

    # Usage
    class ThemedButtonDemo:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Themed Button Demo")

            # Create theme manager
            self.theme_manager = ThemeManager("tkinter")

            # Create themed buttons
            self.save_btn = ThemedButton(
                self.root,
                "save_icon",
                "Save",
                self.theme_manager,
                command=self.save_action
            )
            self.save_btn.pack(pady=10)

            self.open_btn = ThemedButton(
                self.root,
                "open_icon",
                "Open",
                self.theme_manager,
                command=self.open_action
            )
            self.open_btn.pack(pady=10)

            # Theme selection
            theme_frame = tk.Frame(self.root)
            theme_frame.pack(pady=20)

            tk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)

            for theme in ["default", "light", "dark"]:
                btn = tk.Button(
                    theme_frame,
                    text=theme,
                    command=lambda t=theme: self.theme_manager.set_theme(t)
                )
                btn.pack(side=tk.LEFT, padx=5)

        def save_action(self):
            print("Save clicked")

        def open_action(self):
            print("Open clicked")

        def run(self):
            self.root.mainloop()

Themed Image Gallery
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class ThemedImageGallery:
        def __init__(self, root, image_list, theme_manager=None):
            self.root = root
            self.image_list = image_list
            self.theme_manager = theme_manager or ThemeManager()
            self.image_labels = []

            self.setup_ui()

            # Register for theme changes
            self.theme_manager.register_theme_callback(self.on_theme_changed)

        def setup_ui(self):
            # Gallery frame
            self.gallery_frame = tk.Frame(self.root)
            self.gallery_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Load and display images
            self.load_gallery_images()

            # Theme controls
            controls = tk.Frame(self.root)
            controls.pack(pady=10)

            tk.Label(controls, text="Gallery Theme:").pack(side=tk.LEFT)

            for theme in ["default", "light", "dark"]:
                btn = tk.Button(
                    controls,
                    text=theme.capitalize(),
                    command=lambda t=theme: self.change_theme(t)
                )
                btn.pack(side=tk.LEFT, padx=5)

        def load_gallery_images(self):
            """Load all gallery images with current theme."""
            # Clear existing images
            for label in self.image_labels:
                label.destroy()
            self.image_labels.clear()

            # Load images in grid
            row, col = 0, 0
            max_cols = 4

            for image_name in self.image_list:
                image = self.theme_manager.load_image(
                    image_name,
                    size=(150, 150)
                )

                label = tk.Label(
                    self.gallery_frame,
                    image=image,
                    relief=tk.RAISED,
                    borderwidth=2
                )
                label.grid(row=row, column=col, padx=5, pady=5)
                label.image = image  # Keep reference

                self.image_labels.append(label)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

        def change_theme(self, theme_name):
            """Change gallery theme."""
            self.theme_manager.set_theme(theme_name)

        def on_theme_changed(self, old_theme, new_theme):
            """Handle theme change."""
            print(f"Gallery theme changed to {new_theme}")
            self.load_gallery_images()

Performance Considerations
--------------------------

Theme Caching Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class OptimizedThemeManager:
        def __init__(self, framework="tkinter", cache_size=200):
            self.framework = framework
            self.current_theme = "default"
            self.cache = {}
            self.cache_order = []
            self.max_cache_size = cache_size
            self.theme_callbacks = []

        def load_image(self, image_name, **kwargs):
            """Load image with optimized caching."""
            cache_key = self._create_cache_key(image_name, **kwargs)

            # Check cache
            if cache_key in self.cache:
                # Move to end (LRU)
                self.cache_order.remove(cache_key)
                self.cache_order.append(cache_key)
                return self.cache[cache_key]

            # Load image
            image = get_image(
                image_name,
                framework=self.framework,
                theme=self.current_theme,
                **kwargs
            )

            # Add to cache
            self._add_to_cache(cache_key, image)

            return image

        def _create_cache_key(self, image_name, **kwargs):
            """Create a unique cache key."""
            key_parts = [image_name, self.current_theme]
            key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
            return "|".join(key_parts)

        def _add_to_cache(self, key, image):
            """Add image to cache with size management."""
            self.cache[key] = image
            self.cache_order.append(key)

            # Maintain cache size
            while len(self.cache) > self.max_cache_size:
                oldest_key = self.cache_order.pop(0)
                del self.cache[oldest_key]

        def clear_theme_cache(self, theme_name=None):
            """Clear cache for specific theme or all themes."""
            if theme_name is None:
                self.cache.clear()
                self.cache_order.clear()
            else:
                # Remove entries for specific theme
                keys_to_remove = [
                    key for key in self.cache.keys()
                    if f"|{theme_name}|" in key
                ]

                for key in keys_to_remove:
                    del self.cache[key]
                    if key in self.cache_order:
                        self.cache_order.remove(key)

        def get_cache_stats(self):
            """Get cache statistics."""
            return {
                'size': len(self.cache),
                'max_size': self.max_cache_size,
                'hit_rate': getattr(self, '_hit_count', 0) / getattr(self, '_request_count', 1)
            }

Preloading Strategies
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def preload_themed_images(theme_manager, image_list, themes=None):
        """Preload images for multiple themes."""

        if themes is None:
            themes = ["default", "light", "dark"]

        current_theme = theme_manager.get_current_theme()

        print(f"Preloading {len(image_list)} images for {len(themes)} themes...")

        for theme in themes:
            theme_manager.set_theme(theme)

            for image_name in image_list:
                # Load common sizes
                for size in [(16, 16), (24, 24), (32, 32), (64, 64)]:
                    theme_manager.load_image(image_name, size=size)

        # Restore original theme
        theme_manager.set_theme(current_theme)

        print("Preloading complete")

Best Practices
--------------

Theme Design Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

1. **Consistency**: Use consistent theme application across your application
2. **Accessibility**: Ensure themes provide adequate contrast
3. **Performance**: Cache themed images appropriately
4. **User Choice**: Allow users to select their preferred theme

.. code-block:: python

    # Good: Consistent theme usage
    class ConsistentThemedApp:
        def __init__(self):
            self.theme_manager = ThemeManager("customtkinter")

            # Load all images through theme manager
            self.icons = {
                'home': self.theme_manager.load_image("home", size=(32, 32)),
                'save': self.theme_manager.load_image("save", size=(32, 32)),
                'open': self.theme_manager.load_image("open", size=(32, 32))
            }

Theme Testing
~~~~~~~~~~~~~

.. code-block:: python

    def test_theme_compatibility(image_list, themes=None):
        """Test image compatibility across themes."""

        if themes is None:
            themes = ["default", "light", "dark"]

        theme_manager = ThemeManager("tkinter")
        results = {}

        for theme in themes:
            theme_manager.set_theme(theme)
            theme_results = []

            for image_name in image_list:
                try:
                    image = theme_manager.load_image(image_name, size=(64, 64))
                    theme_results.append({'image': image_name, 'status': 'success'})
                except Exception as e:
                    theme_results.append({'image': image_name, 'status': 'error', 'error': str(e)})

            results[theme] = theme_results

        return results

Integration Examples
--------------------

Complete Themed Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class CompleteThemedApplication:
        def __init__(self):
            # Initialize CustomTkinter
            ctk.set_appearance_mode("system")

            self.root = ctk.CTk()
            self.root.title("Complete Themed Application")
            self.root.geometry("1000x700")

            # Theme management
            self.theme_manager = ThemeManager("customtkinter")
            self.theme_manager.register_theme_callback(self.on_theme_changed)

            # Detect system theme
            self.detect_system_theme()

            self.setup_ui()
            self.preload_images()

        def detect_system_theme(self):
            """Detect and set system theme."""
            appearance = ctk.get_appearance_mode()
            if appearance == "Dark":
                self.theme_manager.set_theme("dark")
            else:
                self.theme_manager.set_theme("light")

        def setup_ui(self):
            # Main layout
            self.setup_header()
            self.setup_sidebar()
            self.setup_main_content()
            self.setup_status_bar()

        def setup_header(self):
            """Setup application header."""
            header = ctk.CTkFrame(self.root, height=80)
            header.pack(fill="x", padx=10, pady=(10, 0))
            header.pack_propagate(False)

            # Logo
            logo = self.theme_manager.load_image("app_logo", size=(60, 60))
            logo_label = ctk.CTkLabel(header, image=logo, text="")
            logo_label.pack(side="left", padx=20, pady=10)

            # Title
            title = ctk.CTkLabel(
                header,
                text="Themed Application",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title.pack(side="left", padx=20)

            # Theme toggle
            theme_btn = ctk.CTkButton(
                header,
                text="Toggle Theme",
                command=self.toggle_theme,
                width=120
            )
            theme_btn.pack(side="right", padx=20, pady=20)

        def setup_sidebar(self):
            """Setup navigation sidebar."""
            self.sidebar = ctk.CTkFrame(self.root, width=200)
            self.sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)
            self.sidebar.pack_propagate(False)

            # Navigation buttons
            nav_items = [
                ("home", "Home"),
                ("documents", "Documents"),
                ("settings", "Settings"),
                ("help", "Help")
            ]

            self.nav_buttons = {}
            for icon_name, text in nav_items:
                icon = self.theme_manager.load_image(icon_name, size=(24, 24))

                btn = ctk.CTkButton(
                    self.sidebar,
                    image=icon,
                    text=text,
                    anchor="w",
                    height=40,
                    command=lambda t=text: self.navigate_to(t)
                )
                btn.pack(fill="x", padx=10, pady=5)

                self.nav_buttons[icon_name] = btn

        def setup_main_content(self):
            """Setup main content area."""
            self.main_frame = ctk.CTkFrame(self.root)
            self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

            # Content will be loaded dynamically
            self.load_home_content()

        def setup_status_bar(self):
            """Setup status bar."""
            self.status_bar = ctk.CTkFrame(self.root, height=30)
            self.status_bar.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
            self.status_bar.pack_propagate(False)

            self.status_label = ctk.CTkLabel(
                self.status_bar,
                text=f"Theme: {self.theme_manager.get_current_theme().capitalize()}",
                font=ctk.CTkFont(size=12)
            )
            self.status_label.pack(side="left", padx=10, pady=5)

        def load_home_content(self):
            """Load home page content."""
            # Clear existing content
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # Welcome message
            welcome = ctk.CTkLabel(
                self.main_frame,
                text="Welcome to the Themed Application",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            welcome.pack(pady=30)

            # Feature showcase
            features_frame = ctk.CTkFrame(self.main_frame)
            features_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Load feature images
            feature_images = []
            for i in range(6):
                img = self.theme_manager.load_image(f"feature_{i+1}", size=(100, 100))
                feature_images.append(img)

            # Display in grid
            for i, img in enumerate(feature_images):
                row, col = divmod(i, 3)

                feature_label = ctk.CTkLabel(features_frame, image=img, text="")
                feature_label.grid(row=row, column=col, padx=20, pady=20)

        def toggle_theme(self):
            """Toggle between light and dark themes."""
            current = self.theme_manager.get_current_theme()
            new_theme = "light" if current == "dark" else "dark"

            # Update CustomTkinter appearance
            ctk.set_appearance_mode(new_theme)

            # Update theme manager
            self.theme_manager.set_theme(new_theme)

        def on_theme_changed(self, old_theme, new_theme):
            """Handle theme change."""
            print(f"Application theme changed from {old_theme} to {new_theme}")

            # Update status bar
            self.status_label.configure(text=f"Theme: {new_theme.capitalize()}")

            # Reload current content
            self.load_home_content()

            # Update navigation icons
            nav_items = [
                ("home", "Home"),
                ("documents", "Documents"),
                ("settings", "Settings"),
                ("help", "Help")
            ]

            for icon_name, text in nav_items:
                if icon_name in self.nav_buttons:
                    new_icon = self.theme_manager.load_image(icon_name, size=(24, 24))
                    self.nav_buttons[icon_name].configure(image=new_icon)

        def navigate_to(self, page):
            """Navigate to different pages."""
            print(f"Navigating to: {page}")
            # Implementation would load different content based on page

        def preload_images(self):
            """Preload commonly used images."""
            common_images = [
                "app_logo", "home", "documents", "settings", "help"
            ] + [f"feature_{i+1}" for i in range(6)]

            # Preload for both themes
            current_theme = self.theme_manager.get_current_theme()

            for theme in ["light", "dark"]:
                self.theme_manager.set_theme(theme)
                for image_name in common_images:
                    try:
                        self.theme_manager.load_image(image_name, size=(24, 24))
                        self.theme_manager.load_image(image_name, size=(60, 60))
                        self.theme_manager.load_image(image_name, size=(100, 100))
                    except:
                        pass  # Skip missing images

            # Restore original theme
            self.theme_manager.set_theme(current_theme)

        def run(self):
            self.root.mainloop()

    # Usage
    if __name__ == "__main__":
        app = CompleteThemedApplication()
        app.run()

Next Steps
----------

Now that you understand the theme system:

1. **Learn Custom Filters**: :doc:`custom_filters`
2. **Explore Performance Optimization**: :doc:`performance_optimization`
3. **Try Advanced Examples**: :doc:`../examples/index`
4. **Build Themed Applications**: :doc:`gui_development`
