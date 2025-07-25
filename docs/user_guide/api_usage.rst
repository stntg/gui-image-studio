API Usage
=========

This guide provides comprehensive coverage of the GUI Image Studio Python API, including core functions, advanced usage patterns, and integration techniques.

Core API Overview
------------------

GUI Image Studio provides a simple yet powerful API centered around a few key functions:

.. code-block:: python

    from gui_image_studio import (
        get_image,                    # Load and transform images
        embed_images_from_folder,     # Create embedded image resources
        create_sample_images          # Generate sample images
    )

Primary Functions
-----------------

get_image()
~~~~~~~~~~~

The main function for loading and transforming images:

.. code-block:: python

    def get_image(
        image_name: str,
        framework: str = "tkinter",
        size: tuple = (32, 32),
        theme: str = "default",
        rotate: int = 0,
        grayscale: bool = False,
        tint_color: tuple = None,
        tint_intensity: float = 0.0,
        contrast: float = 1.0,
        saturation: float = 1.0,
        transparency: float = 1.0,
        animated: bool = False,
        frame_delay: int = 100,
        format_override: str = None
    ) -> Union[PhotoImage, CTkImage, dict]:

**Parameters:**

- ``image_name`` (str): Path to image file or embedded image name
- ``framework`` (str): Target GUI framework ("tkinter" or "customtkinter")
- ``size`` (tuple): Target dimensions as (width, height)
- ``theme`` (str): Theme adaptation ("default", "light", "dark")
- ``rotate`` (int): Rotation angle in degrees
- ``grayscale`` (bool): Convert to grayscale
- ``tint_color`` (tuple): RGB color tint as (R, G, B)
- ``tint_intensity`` (float): Tint strength (0.0-1.0)
- ``contrast`` (float): Contrast adjustment (1.0 = normal)
- ``saturation`` (float): Saturation adjustment (1.0 = normal)
- ``transparency`` (float): Overall transparency (0.0-1.0)
- ``animated`` (bool): Process animated GIFs
- ``frame_delay`` (int): Animation frame delay in milliseconds
- ``format_override`` (str): Force specific output format

**Return Values:**

- For static images: Framework-specific image object
- For animated images: Dictionary with frame data

**Examples:**

.. code-block:: python

    # Basic usage
    image = get_image("icon.png", framework="tkinter")

    # With transformations
    enhanced_image = get_image(
        "photo.jpg",
        framework="customtkinter",
        size=(400, 300),
        contrast=1.2,
        saturation=1.1,
        tint_color=(255, 240, 220),
        tint_intensity=0.1
    )

    # Animated GIF
    animation = get_image(
        "spinner.gif",
        framework="tkinter",
        size=(50, 50),
        animated=True,
        frame_delay=80
    )

embed_images_from_folder()
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create embedded Python modules from image folders:

.. code-block:: python

    def embed_images_from_folder(
        folder_path: str,
        output_file: str = "embedded_images.py",
        compression_quality: int = 85
    ) -> bool:

**Parameters:**

- ``folder_path`` (str): Path to folder containing images
- ``output_file`` (str): Output Python file path
- ``compression_quality`` (int): JPEG/WebP quality (1-100)

**Examples:**

.. code-block:: python

    # Basic embedding
    embed_images_from_folder("images/", "resources.py")

    # High-quality embedding
    embed_images_from_folder(
        "icons/",
        "src/icons.py",
        compression_quality=95
    )

create_sample_images()
~~~~~~~~~~~~~~~~~~~~~~

Generate sample images for testing:

.. code-block:: python

    def create_sample_images(output_dir: str = "sample_images") -> bool:

**Parameters:**

- ``output_dir`` (str): Directory to create samples in

**Examples:**

.. code-block:: python

    # Create in default location
    create_sample_images()

    # Create in specific directory
    create_sample_images("test_data/samples")

Launching the Visual Designer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The visual image designer is launched using the command-line interface:

**Command:**

.. code-block:: bash

    gui-image-studio-designer

**Examples:**

.. code-block:: bash

    # Launch the visual designer
    gui-image-studio-designer

    # Launch from Python script (using subprocess)
    import subprocess
    subprocess.run(["gui-image-studio-designer"])

Advanced API Usage
------------------

Error Handling
~~~~~~~~~~~~~~

Proper error handling is essential for robust applications:

.. code-block:: python

    import os
    from gui_image_studio import get_image

    def safe_load_image(image_path, **kwargs):
        """Safely load an image with comprehensive error handling."""

        try:
            # Check if file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # Check file size (optional)
            file_size = os.path.getsize(image_path)
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                raise ValueError(f"Image file too large: {file_size / 1024 / 1024:.1f}MB")

            # Load image
            image = get_image(image_path, **kwargs)

            return {
                'success': True,
                'image': image,
                'path': image_path
            }

        except FileNotFoundError as e:
            return {
                'success': False,
                'error': 'file_not_found',
                'message': str(e),
                'path': image_path
            }

        except ValueError as e:
            return {
                'success': False,
                'error': 'invalid_image',
                'message': str(e),
                'path': image_path
            }

        except Exception as e:
            return {
                'success': False,
                'error': 'unknown_error',
                'message': str(e),
                'path': image_path
            }

    # Usage
    result = safe_load_image(
        "photo.jpg",
        framework="tkinter",
        size=(800, 600)
    )

    if result['success']:
        image = result['image']
        print(f"Successfully loaded: {result['path']}")
    else:
        print(f"Error loading image: {result['error']} - {result['message']}")

Parameter Validation
~~~~~~~~~~~~~~~~~~~~

Validate parameters before processing:

.. code-block:: python

    def validate_image_parameters(**kwargs):
        """Validate image processing parameters."""

        errors = []

        # Validate framework
        framework = kwargs.get('framework', 'tkinter')
        if framework not in ['tkinter', 'customtkinter']:
            errors.append(f"Invalid framework: {framework}")

        # Validate size
        size = kwargs.get('size', (32, 32))
        if not isinstance(size, tuple) or len(size) != 2:
            errors.append("Size must be a tuple of (width, height)")
        elif any(not isinstance(x, int) or x <= 0 for x in size):
            errors.append("Size dimensions must be positive integers")
        elif any(x > 5000 for x in size):
            errors.append("Size dimensions too large (max 5000)")

        # Validate rotation
        rotate = kwargs.get('rotate', 0)
        if not isinstance(rotate, (int, float)):
            errors.append("Rotation must be a number")
        elif not -360 <= rotate <= 360:
            errors.append("Rotation must be between -360 and 360 degrees")

        # Validate tint intensity
        tint_intensity = kwargs.get('tint_intensity', 0.0)
        if not isinstance(tint_intensity, (int, float)):
            errors.append("Tint intensity must be a number")
        elif not 0.0 <= tint_intensity <= 1.0:
            errors.append("Tint intensity must be between 0.0 and 1.0")

        # Validate contrast
        contrast = kwargs.get('contrast', 1.0)
        if not isinstance(contrast, (int, float)):
            errors.append("Contrast must be a number")
        elif not 0.1 <= contrast <= 3.0:
            errors.append("Contrast must be between 0.1 and 3.0")

        # Validate saturation
        saturation = kwargs.get('saturation', 1.0)
        if not isinstance(saturation, (int, float)):
            errors.append("Saturation must be a number")
        elif not 0.0 <= saturation <= 3.0:
            errors.append("Saturation must be between 0.0 and 3.0")

        # Validate transparency
        transparency = kwargs.get('transparency', 1.0)
        if not isinstance(transparency, (int, float)):
            errors.append("Transparency must be a number")
        elif not 0.0 <= transparency <= 1.0:
            errors.append("Transparency must be between 0.0 and 1.0")

        # Validate tint color
        tint_color = kwargs.get('tint_color')
        if tint_color is not None:
            if not isinstance(tint_color, tuple) or len(tint_color) != 3:
                errors.append("Tint color must be a tuple of (R, G, B)")
            elif any(not isinstance(x, int) or not 0 <= x <= 255 for x in tint_color):
                errors.append("Tint color values must be integers between 0 and 255")

        return errors

    def validated_get_image(image_name, **kwargs):
        """Load image with parameter validation."""

        # Validate parameters
        errors = validate_image_parameters(**kwargs)
        if errors:
            raise ValueError(f"Parameter validation failed: {'; '.join(errors)}")

        # Load image
        return get_image(image_name, **kwargs)

    # Usage
    try:
        image = validated_get_image(
            "photo.jpg",
            framework="tkinter",
            size=(800, 600),
            contrast=1.2,
            tint_intensity=0.3
        )
    except ValueError as e:
        print(f"Validation error: {e}")

Caching and Performance
~~~~~~~~~~~~~~~~~~~~~~~

Implement caching for better performance:

.. code-block:: python

    import hashlib
    from functools import lru_cache

    class ImageCache:
        def __init__(self, max_size=100):
            self.cache = {}
            self.access_order = []
            self.max_size = max_size
            self.hit_count = 0
            self.miss_count = 0

        def _create_key(self, image_name, **kwargs):
            """Create a unique cache key."""
            key_data = f"{image_name}_{sorted(kwargs.items())}"
            return hashlib.md5(key_data.encode()).hexdigest()

        def get_image(self, image_name, **kwargs):
            """Get image with caching."""
            cache_key = self._create_key(image_name, **kwargs)

            if cache_key in self.cache:
                # Cache hit
                self.hit_count += 1

                # Move to end (LRU)
                self.access_order.remove(cache_key)
                self.access_order.append(cache_key)

                return self.cache[cache_key]

            # Cache miss - load image
            self.miss_count += 1
            image = get_image(image_name, **kwargs)

            # Add to cache
            self.cache[cache_key] = image
            self.access_order.append(cache_key)

            # Maintain cache size
            while len(self.cache) > self.max_size:
                oldest_key = self.access_order.pop(0)
                del self.cache[oldest_key]

            return image

        def clear_cache(self):
            """Clear the entire cache."""
            self.cache.clear()
            self.access_order.clear()

        def get_stats(self):
            """Get cache statistics."""
            total_requests = self.hit_count + self.miss_count
            hit_rate = (self.hit_count / total_requests) * 100 if total_requests > 0 else 0

            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'hits': self.hit_count,
                'misses': self.miss_count,
                'hit_rate': hit_rate
            }

    # Global cache instance
    image_cache = ImageCache(max_size=200)

    # Usage
    def cached_get_image(image_name, **kwargs):
        """Get image with caching."""
        return image_cache.get_image(image_name, **kwargs)

    # Example usage
    image1 = cached_get_image("icon.png", framework="tkinter", size=(32, 32))
    image2 = cached_get_image("icon.png", framework="tkinter", size=(32, 32))  # From cache

    # Check cache statistics
    stats = image_cache.get_stats()
    print(f"Cache hit rate: {stats['hit_rate']:.1f}%")

Framework-Specific Integration
------------------------------

Tkinter Integration Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from gui_image_studio import get_image

    class TkinterImageManager:
        def __init__(self, root):
            self.root = root
            self.images = {}  # Keep references to prevent garbage collection

        def load_image(self, name, image_path, **kwargs):
            """Load and store image with reference."""
            image = get_image(
                image_path,
                framework="tkinter",
                **kwargs
            )
            self.images[name] = image
            return image

        def get_image(self, name):
            """Get previously loaded image."""
            return self.images.get(name)

        def create_image_button(self, parent, image_name, text="", **kwargs):
            """Create button with image."""
            image = self.images.get(image_name)
            if not image:
                raise ValueError(f"Image '{image_name}' not loaded")

            button = tk.Button(
                parent,
                image=image,
                text=text,
                compound=tk.LEFT,
                **kwargs
            )

            # Keep reference
            button.image = image

            return button

        def create_image_label(self, parent, image_name, **kwargs):
            """Create label with image."""
            image = self.images.get(image_name)
            if not image:
                raise ValueError(f"Image '{image_name}' not loaded")

            label = tk.Label(
                parent,
                image=image,
                **kwargs
            )

            # Keep reference
            label.image = image

            return label

    # Usage example
    class TkinterImageApp:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Tkinter Image App")

            # Initialize image manager
            self.image_manager = TkinterImageManager(self.root)

            # Load images
            self.load_images()
            self.setup_ui()

        def load_images(self):
            """Load all application images."""
            images_to_load = [
                ("home_icon", "home.png", {"size": (24, 24)}),
                ("save_icon", "save.png", {"size": (24, 24)}),
                ("logo", "logo.png", {"size": (64, 64)}),
                ("background", "bg.jpg", {"size": (800, 600)})
            ]

            for name, path, kwargs in images_to_load:
                try:
                    self.image_manager.load_image(name, path, **kwargs)
                    print(f"Loaded: {name}")
                except Exception as e:
                    print(f"Failed to load {name}: {e}")

        def setup_ui(self):
            # Background
            try:
                bg_label = self.image_manager.create_image_label(self.root, "background")
                bg_label.place(x=0, y=0)
            except ValueError:
                pass  # Background not loaded

            # Toolbar
            toolbar = tk.Frame(self.root, bg='white')
            toolbar.pack(side=tk.TOP, fill=tk.X)

            # Buttons with icons
            try:
                home_btn = self.image_manager.create_image_button(
                    toolbar,
                    "home_icon",
                    text="Home",
                    command=self.home_action
                )
                home_btn.pack(side=tk.LEFT, padx=5, pady=5)

                save_btn = self.image_manager.create_image_button(
                    toolbar,
                    "save_icon",
                    text="Save",
                    command=self.save_action
                )
                save_btn.pack(side=tk.LEFT, padx=5, pady=5)

            except ValueError as e:
                print(f"Error creating buttons: {e}")

        def home_action(self):
            print("Home clicked")

        def save_action(self):
            print("Save clicked")

        def run(self):
            self.root.mainloop()

CustomTkinter Integration Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import customtkinter as ctk
    from gui_image_studio import get_image

    class CustomTkinterImageManager:
        def __init__(self):
            self.images = {}
            self.current_theme = "dark"

        def set_theme(self, theme):
            """Change theme and reload images."""
            if theme != self.current_theme:
                self.current_theme = theme
                self.reload_all_images()

        def load_image(self, name, image_path, **kwargs):
            """Load image with current theme."""
            kwargs['theme'] = self.current_theme
            image = get_image(
                image_path,
                framework="customtkinter",
                **kwargs
            )
            self.images[name] = {
                'image': image,
                'path': image_path,
                'kwargs': kwargs
            }
            return image

        def get_image(self, name):
            """Get loaded image."""
            return self.images.get(name, {}).get('image')

        def reload_all_images(self):
            """Reload all images with current theme."""
            for name, data in self.images.items():
                kwargs = data['kwargs'].copy()
                kwargs['theme'] = self.current_theme

                new_image = get_image(
                    data['path'],
                    framework="customtkinter",
                    **kwargs
                )

                self.images[name]['image'] = new_image

    # Usage example
    class ModernImageApp:
        def __init__(self):
            # Set CustomTkinter theme
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")

            self.root = ctk.CTk()
            self.root.title("Modern Image App")
            self.root.geometry("900x600")

            # Initialize image manager
            self.image_manager = CustomTkinterImageManager()

            self.load_images()
            self.setup_ui()

        def load_images(self):
            """Load application images."""
            images = [
                ("logo", "logo.png", {"size": (80, 80)}),
                ("home", "home.png", {"size": (32, 32)}),
                ("settings", "settings.png", {"size": (32, 32)}),
                ("profile", "profile.png", {"size": (40, 40)})
            ]

            for name, path, kwargs in images:
                try:
                    self.image_manager.load_image(name, path, **kwargs)
                except Exception as e:
                    print(f"Failed to load {name}: {e}")

        def setup_ui(self):
            # Header
            header = ctk.CTkFrame(self.root, height=100)
            header.pack(fill="x", padx=20, pady=(20, 0))
            header.pack_propagate(False)

            # Logo
            logo_image = self.image_manager.get_image("logo")
            if logo_image:
                logo_label = ctk.CTkLabel(header, image=logo_image, text="")
                logo_label.pack(side="left", padx=20, pady=20)

            # Title
            title = ctk.CTkLabel(
                header,
                text="Modern Application",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title.pack(side="left", padx=20)

            # Theme toggle
            theme_btn = ctk.CTkButton(
                header,
                text="Toggle Theme",
                command=self.toggle_theme
            )
            theme_btn.pack(side="right", padx=20, pady=30)

            # Navigation
            nav_frame = ctk.CTkFrame(self.root)
            nav_frame.pack(fill="x", padx=20, pady=20)

            # Navigation buttons
            nav_items = [
                ("home", "Home"),
                ("settings", "Settings")
            ]

            self.nav_buttons = {}
            for icon_name, text in nav_items:
                icon = self.image_manager.get_image(icon_name)

                btn = ctk.CTkButton(
                    nav_frame,
                    image=icon,
                    text=text,
                    width=120,
                    command=lambda t=text: self.navigate(t)
                )
                btn.pack(side="left", padx=10, pady=10)

                self.nav_buttons[icon_name] = btn

        def toggle_theme(self):
            """Toggle between light and dark themes."""
            current_mode = ctk.get_appearance_mode()
            new_mode = "light" if current_mode == "Dark" else "dark"

            # Update CustomTkinter
            ctk.set_appearance_mode(new_mode)

            # Update image manager
            self.image_manager.set_theme(new_mode)

            # Update UI images
            self.update_ui_images()

        def update_ui_images(self):
            """Update all UI images after theme change."""
            # Update logo
            logo_image = self.image_manager.get_image("logo")
            if logo_image:
                # Find and update logo label
                header = self.root.winfo_children()[0]
                logo_label = header.winfo_children()[0]
                logo_label.configure(image=logo_image)

            # Update navigation buttons
            for icon_name, button in self.nav_buttons.items():
                icon = self.image_manager.get_image(icon_name)
                if icon:
                    button.configure(image=icon)

        def navigate(self, page):
            print(f"Navigate to: {page}")

        def run(self):
            self.root.mainloop()

Batch Processing with API
-------------------------

Automated Image Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from pathlib import Path
    from gui_image_studio import get_image, embed_images_from_folder

    class ImageProcessor:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}

        def process_folder(self, input_folder, output_folder, transformations):
            """Process all images in a folder."""

            os.makedirs(output_folder, exist_ok=True)

            results = {
                'processed': 0,
                'errors': 0,
                'error_list': []
            }

            for filename in os.listdir(input_folder):
                if Path(filename).suffix.lower() not in self.supported_formats:
                    continue

                input_path = os.path.join(input_folder, filename)

                try:
                    # Process image
                    processed_image = get_image(
                        input_path,
                        framework=self.framework,
                        **transformations
                    )

                    results['processed'] += 1
                    print(f"Processed: {filename}")

                except Exception as e:
                    results['errors'] += 1
                    results['error_list'].append(f"{filename}: {str(e)}")
                    print(f"Error processing {filename}: {e}")

            return results

        def create_icon_set(self, source_image, output_folder, sizes=None):
            """Create multiple icon sizes from source image."""

            if sizes is None:
                sizes = [16, 24, 32, 48, 64, 128, 256]

            os.makedirs(output_folder, exist_ok=True)

            base_name = Path(source_image).stem

            for size in sizes:
                try:
                    icon = get_image(
                        source_image,
                        framework=self.framework,
                        size=(size, size)
                    )

                    print(f"Created {size}x{size} icon")

                except Exception as e:
                    print(f"Error creating {size}x{size} icon: {e}")

        def optimize_for_web(self, input_folder, output_folder):
            """Optimize images for web use."""

            web_transformations = {
                'size': (1200, 800),
                'contrast': 1.05,
                'saturation': 1.02
            }

            return self.process_folder(
                input_folder,
                output_folder,
                web_transformations
            )

    # Usage
    def batch_process_images():
        processor = ImageProcessor("customtkinter")

        # Process photos
        photo_results = processor.optimize_for_web(
            "raw_photos/",
            "web_photos/"
        )

        print(f"Photo processing: {photo_results['processed']} processed, {photo_results['errors']} errors")

        # Create icon sets
        processor.create_icon_set(
            "logo.png",
            "icon_sets/logo/",
            sizes=[16, 32, 64, 128]
        )

Integration Testing
-------------------

API Testing Framework
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import unittest
    import tempfile
    import os
    from gui_image_studio import get_image, create_sample_images

    class TestGUIImageStudioAPI(unittest.TestCase):

        def setUp(self):
            """Set up test environment."""
            self.temp_dir = tempfile.mkdtemp()

            # Create sample images for testing
            create_sample_images(self.temp_dir)

        def tearDown(self):
            """Clean up test environment."""
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)

        def test_basic_image_loading(self):
            """Test basic image loading functionality."""

            # Test with sample image
            image = get_image(
                "sample_icon",
                framework="tkinter",
                size=(64, 64)
            )

            self.assertIsNotNone(image)
            self.assertEqual(image.width(), 64)
            self.assertEqual(image.height(), 64)

        def test_image_transformations(self):
            """Test image transformation parameters."""

            # Test size transformation
            image = get_image(
                "sample_icon",
                framework="tkinter",
                size=(100, 50)
            )

            self.assertEqual(image.width(), 100)
            self.assertEqual(image.height(), 50)

        def test_framework_compatibility(self):
            """Test compatibility with different frameworks."""

            # Test tkinter
            tk_image = get_image(
                "sample_icon",
                framework="tkinter",
                size=(32, 32)
            )
            self.assertIsNotNone(tk_image)

            # Test customtkinter
            try:
                ctk_image = get_image(
                    "sample_icon",
                    framework="customtkinter",
                    size=(32, 32)
                )
                self.assertIsNotNone(ctk_image)
            except ImportError:
                self.skipTest("CustomTkinter not available")

        def test_error_handling(self):
            """Test error handling for invalid inputs."""

            # Test non-existent file
            with self.assertRaises(FileNotFoundError):
                get_image("non_existent_file.png", framework="tkinter")

            # Test invalid framework
            with self.assertRaises(ValueError):
                get_image("sample_icon", framework="invalid_framework")

        def test_parameter_validation(self):
            """Test parameter validation."""

            # Test invalid size
            with self.assertRaises(ValueError):
                get_image("sample_icon", framework="tkinter", size="invalid")

            # Test invalid tint intensity
            with self.assertRaises(ValueError):
                get_image("sample_icon", framework="tkinter", tint_intensity=2.0)

    # Run tests
    if __name__ == "__main__":
        unittest.main()

Performance Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    from gui_image_studio import get_image, create_sample_images

    def performance_test():
        """Test API performance with various scenarios."""

        # Create test images
        create_sample_images("perf_test_images")

        # Test scenarios
        scenarios = [
            {
                'name': 'Basic Loading',
                'params': {'framework': 'tkinter', 'size': (64, 64)}
            },
            {
                'name': 'With Transformations',
                'params': {
                    'framework': 'tkinter',
                    'size': (200, 200),
                    'contrast': 1.2,
                    'saturation': 1.1,
                    'tint_color': (255, 200, 150),
                    'tint_intensity': 0.2
                }
            },
            {
                'name': 'Large Size',
                'params': {'framework': 'tkinter', 'size': (800, 600)}
            }
        ]

        results = {}

        for scenario in scenarios:
            name = scenario['name']
            params = scenario['params']

            # Time multiple iterations
            iterations = 10
            start_time = time.time()

            for _ in range(iterations):
                image = get_image("sample_icon", **params)

            end_time = time.time()
            avg_time = (end_time - start_time) / iterations

            results[name] = {
                'avg_time': avg_time,
                'iterations': iterations,
                'total_time': end_time - start_time
            }

            print(f"{name}: {avg_time:.3f}s average ({iterations} iterations)")

        return results

    # Run performance test
    if __name__ == "__main__":
        perf_results = performance_test()

Best Practices
--------------

API Usage Guidelines
~~~~~~~~~~~~~~~~~~~~

1. **Always specify framework**: Be explicit about target GUI framework
2. **Handle errors gracefully**: Implement proper error handling
3. **Cache frequently used images**: Use caching for better performance
4. **Validate parameters**: Check inputs before processing
5. **Keep image references**: Prevent garbage collection in GUI applications

.. code-block:: python

    # Good: Explicit and safe
    def load_app_images():
        images = {}

        image_configs = [
            ('home_icon', 'home.png', {'size': (24, 24)}),
            ('logo', 'logo.png', {'size': (64, 64)}),
        ]

        for name, path, config in image_configs:
            try:
                images[name] = get_image(
                    path,
                    framework="tkinter",  # Explicit framework
                    **config
                )
            except Exception as e:
                print(f"Failed to load {name}: {e}")
                # Provide fallback or default image
                images[name] = None

        return images

Memory Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Good: Proper memory management
    class ImageManager:
        def __init__(self):
            self.images = {}

        def load_image(self, name, path, **kwargs):
            """Load and cache image."""
            if name not in self.images:
                self.images[name] = get_image(path, **kwargs)
            return self.images[name]

        def clear_cache(self):
            """Clear image cache."""
            self.images.clear()

        def __del__(self):
            """Cleanup on destruction."""
            self.clear_cache()

Next Steps
----------

Now that you understand the API:

1. **Learn GUI Development**: :doc:`gui_development`
2. **Explore Command Line Tools**: :doc:`command_line_tools`
3. **Try Advanced Examples**: :doc:`../examples/index`
4. **Build Custom Applications**: Start your own projects!
