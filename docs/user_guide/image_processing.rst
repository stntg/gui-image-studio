Image Processing
================

This comprehensive guide covers all image processing capabilities in GUI Image Studio, from basic transformations to advanced effects and batch operations.

Overview of Image Processing
-----------------------------

GUI Image Studio provides powerful image processing capabilities through:

- **Real-time transformations** during image loading
- **Non-destructive editing** that preserves original images
- **Batch processing** for multiple images
- **Framework integration** for tkinter and customtkinter
- **High-quality algorithms** for professional results

Core Transformation Parameters
------------------------------

All transformations are applied through the ``get_image()`` function:

.. code-block:: python

    from gui_image_studio import get_image

    image = get_image(
        "source_image.jpg",
        framework="tkinter",          # Target GUI framework
        size=(width, height),         # Resize dimensions
        rotate=degrees,               # Rotation angle
        tint_color=(r, g, b),        # Color tint RGB values
        tint_intensity=0.0-1.0,      # Tint strength
        contrast=1.0,                # Contrast adjustment
        saturation=1.0,              # Saturation adjustment
        grayscale=False,             # Convert to grayscale
        transparency=1.0,            # Overall transparency
        theme="default",             # Theme adaptation
        animated=False,              # Handle animated GIFs
        frame_delay=100              # Animation timing
    )

Size and Scaling Operations
---------------------------

Resizing and Scaling
~~~~~~~~~~~~~~~~~~~~~

**Basic Resizing:**

.. code-block:: python

    # Resize to exact dimensions
    image = get_image(
        "photo.jpg",
        framework="tkinter",
        size=(800, 600)
    )

    # Common sizes for different purposes
    thumbnail = get_image("photo.jpg", framework="tkinter", size=(150, 150))
    icon = get_image("icon.png", framework="tkinter", size=(32, 32))
    banner = get_image("banner.jpg", framework="tkinter", size=(1200, 300))

**Aspect Ratio Considerations:**

.. code-block:: python

    # For maintaining aspect ratio, calculate dimensions
    def calculate_size(original_size, target_width=None, target_height=None):
        orig_w, orig_h = original_size

        if target_width and not target_height:
            # Scale by width
            ratio = target_width / orig_w
            return (target_width, int(orig_h * ratio))
        elif target_height and not target_width:
            # Scale by height
            ratio = target_height / orig_h
            return (int(orig_w * ratio), target_height)
        else:
            # Use provided dimensions
            return (target_width, target_height)

    # Usage example
    new_size = calculate_size((1920, 1080), target_width=800)
    image = get_image("photo.jpg", framework="tkinter", size=new_size)

**Quality Considerations:**

.. code-block:: python

    # High-quality resizing for important images
    high_quality = get_image(
        "important_photo.jpg",
        framework="customtkinter",
        size=(1024, 768)
    )

    # Smaller sizes for thumbnails (faster processing)
    thumbnail = get_image(
        "photo.jpg",
        framework="tkinter",
        size=(100, 100)
    )

Geometric Transformations
-------------------------

Rotation Operations
~~~~~~~~~~~~~~~~~~~

**Basic Rotation:**

.. code-block:: python

    # Rotate by specific angles
    rotated_90 = get_image("image.png", framework="tkinter", rotate=90)
    rotated_45 = get_image("image.png", framework="tkinter", rotate=45)
    rotated_custom = get_image("image.png", framework="tkinter", rotate=23.5)

**Common Rotation Patterns:**

.. code-block:: python

    # Portrait to landscape
    landscape = get_image("portrait.jpg", framework="tkinter", rotate=90)

    # Artistic angles
    artistic = get_image("photo.jpg", framework="tkinter", rotate=15)

    # Correction rotations
    corrected = get_image("crooked_photo.jpg", framework="tkinter", rotate=-2.3)

**Rotation with Other Transformations:**

.. code-block:: python

    # Rotate and resize
    processed = get_image(
        "image.jpg",
        framework="customtkinter",
        size=(400, 400),
        rotate=45,
        tint_color=(255, 200, 100),
        tint_intensity=0.2
    )

Color Adjustments
-----------------

Tinting and Color Effects
~~~~~~~~~~~~~~~~~~~~~~~~~

**Basic Color Tinting:**

.. code-block:: python

    # Red tint
    red_tinted = get_image(
        "photo.jpg",
        framework="tkinter",
        tint_color=(255, 0, 0),
        tint_intensity=0.3
    )

    # Blue tint
    blue_tinted = get_image(
        "photo.jpg",
        framework="tkinter",
        tint_color=(0, 100, 255),
        tint_intensity=0.4
    )

    # Warm tone
    warm = get_image(
        "photo.jpg",
        framework="tkinter",
        tint_color=(255, 200, 150),
        tint_intensity=0.2
    )

**Color Intensity Levels:**

.. code-block:: python

    # Subtle tint (10%)
    subtle = get_image(
        "image.jpg",
        framework="tkinter",
        tint_color=(255, 100, 0),
        tint_intensity=0.1
    )

    # Moderate tint (30%)
    moderate = get_image(
        "image.jpg",
        framework="tkinter",
        tint_color=(255, 100, 0),
        tint_intensity=0.3
    )

    # Strong tint (60%)
    strong = get_image(
        "image.jpg",
        framework="tkinter",
        tint_color=(255, 100, 0),
        tint_intensity=0.6
    )

**Predefined Color Schemes:**

.. code-block:: python

    # Define common color schemes
    COLOR_SCHEMES = {
        'sepia': (210, 180, 140),
        'cool_blue': (100, 150, 255),
        'warm_orange': (255, 180, 100),
        'vintage': (200, 180, 120),
        'cyberpunk': (0, 255, 150),
        'sunset': (255, 150, 80),
        'ocean': (50, 150, 200),
        'forest': (100, 180, 100)
    }

    # Apply color schemes
    sepia_image = get_image(
        "photo.jpg",
        framework="tkinter",
        tint_color=COLOR_SCHEMES['sepia'],
        tint_intensity=0.4
    )

Contrast and Saturation
~~~~~~~~~~~~~~~~~~~~~~~

**Contrast Adjustments:**

.. code-block:: python

    # Increase contrast (values > 1.0)
    high_contrast = get_image(
        "photo.jpg",
        framework="tkinter",
        contrast=1.5
    )

    # Decrease contrast (values < 1.0)
    low_contrast = get_image(
        "photo.jpg",
        framework="tkinter",
        contrast=0.7
    )

    # Extreme contrast for artistic effect
    dramatic = get_image(
        "photo.jpg",
        framework="tkinter",
        contrast=2.0
    )

**Saturation Adjustments:**

.. code-block:: python

    # Boost saturation for vibrant colors
    vibrant = get_image(
        "photo.jpg",
        framework="tkinter",
        saturation=1.5
    )

    # Reduce saturation for muted tones
    muted = get_image(
        "photo.jpg",
        framework="tkinter",
        saturation=0.6
    )

    # Desaturated (almost grayscale)
    desaturated = get_image(
        "photo.jpg",
        framework="tkinter",
        saturation=0.2
    )

**Combined Adjustments:**

.. code-block:: python

    # Professional photo enhancement
    enhanced = get_image(
        "photo.jpg",
        framework="customtkinter",
        contrast=1.2,
        saturation=1.1,
        tint_color=(255, 240, 220),
        tint_intensity=0.1
    )

    # Vintage film look
    vintage = get_image(
        "photo.jpg",
        framework="tkinter",
        contrast=1.3,
        saturation=0.8,
        tint_color=(210, 180, 140),
        tint_intensity=0.3
    )

Grayscale and Transparency
--------------------------

Grayscale Conversion
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Convert to grayscale
    bw_image = get_image(
        "color_photo.jpg",
        framework="tkinter",
        grayscale=True
    )

    # Grayscale with contrast boost
    dramatic_bw = get_image(
        "photo.jpg",
        framework="tkinter",
        grayscale=True,
        contrast=1.4
    )

    # Grayscale with tint (sepia effect)
    sepia = get_image(
        "photo.jpg",
        framework="tkinter",
        grayscale=True,
        tint_color=(210, 180, 140),
        tint_intensity=0.5
    )

Transparency Effects
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Semi-transparent overlay
    overlay = get_image(
        "background.jpg",
        framework="customtkinter",
        transparency=0.7
    )

    # Subtle transparency
    subtle_transparent = get_image(
        "image.png",
        framework="tkinter",
        transparency=0.9
    )

    # Watermark effect
    watermark = get_image(
        "logo.png",
        framework="tkinter",
        size=(200, 100),
        transparency=0.3
    )

Theme-Aware Processing
----------------------

Theme Integration
~~~~~~~~~~~~~~~~~

GUI Image Studio supports theme-aware image processing:

.. code-block:: python

    # Dark theme optimization
    dark_image = get_image(
        "icon.png",
        framework="customtkinter",
        theme="dark",
        size=(64, 64)
    )

    # Light theme optimization
    light_image = get_image(
        "icon.png",
        framework="tkinter",
        theme="light",
        size=(64, 64)
    )

    # Default theme
    default_image = get_image(
        "icon.png",
        framework="tkinter",
        theme="default",
        size=(64, 64)
    )

**Dynamic Theme Switching:**

.. code-block:: python

    class ThemeAwareImageLoader:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.current_theme = "default"
            self.image_cache = {}

        def set_theme(self, theme):
            self.current_theme = theme
            self.image_cache.clear()  # Clear cache for theme change

        def load_image(self, name, **kwargs):
            cache_key = f"{name}_{self.current_theme}_{kwargs}"

            if cache_key not in self.image_cache:
                self.image_cache[cache_key] = get_image(
                    name,
                    framework=self.framework,
                    theme=self.current_theme,
                    **kwargs
                )

            return self.image_cache[cache_key]

    # Usage
    loader = ThemeAwareImageLoader("customtkinter")

    # Load with current theme
    icon = loader.load_image("icon.png", size=(32, 32))

    # Switch theme and reload
    loader.set_theme("dark")
    dark_icon = loader.load_image("icon.png", size=(32, 32))

Animated GIF Processing
-----------------------

Working with Animations
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Load animated GIF
    animation = get_image(
        "animated.gif",
        framework="tkinter",
        size=(200, 200),
        animated=True,
        frame_delay=100
    )

    # Extract animation data
    frames = animation["animated_frames"]
    delay = animation["frame_delay"]
    frame_count = len(frames)

**Animation Playback:**

.. code-block:: python

    import tkinter as tk

    class AnimationPlayer:
        def __init__(self, root, animation_data):
            self.root = root
            self.frames = animation_data["animated_frames"]
            self.delay = animation_data["frame_delay"]
            self.current_frame = 0
            self.playing = True

            self.label = tk.Label(root)
            self.label.pack()

            self.play_animation()

        def play_animation(self):
            if self.playing and self.frames:
                # Display current frame
                self.label.configure(image=self.frames[self.current_frame])

                # Move to next frame
                self.current_frame = (self.current_frame + 1) % len(self.frames)

                # Schedule next frame
                self.root.after(self.delay, self.play_animation)

        def pause(self):
            self.playing = False

        def resume(self):
            self.playing = True
            self.play_animation()

**Animation with Transformations:**

.. code-block:: python

    # Apply effects to animated GIF
    processed_animation = get_image(
        "animated.gif",
        framework="customtkinter",
        size=(150, 150),
        animated=True,
        frame_delay=80,
        tint_color=(255, 100, 100),
        tint_intensity=0.2,
        contrast=1.1
    )

Batch Processing Patterns
-------------------------

Processing Multiple Images
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Basic Batch Processing:**

.. code-block:: python

    import os
    from gui_image_studio import get_image

    def process_image_folder(input_folder, output_folder, **transform_params):
        """Process all images in a folder with given transformations."""

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Supported image extensions
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}

        for filename in os.listdir(input_folder):
            name, ext = os.path.splitext(filename)

            if ext.lower() in image_extensions:
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, f"processed_{filename}")

                try:
                    # Process image
                    processed = get_image(
                        input_path,
                        framework="tkinter",
                        **transform_params
                    )

                    print(f"Processed: {filename}")

                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    # Usage
    process_image_folder(
        "input_images/",
        "output_images/",
        size=(800, 600),
        contrast=1.2,
        saturation=1.1
    )

**Advanced Batch Processing:**

.. code-block:: python

    class ImageBatchProcessor:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.processed_count = 0
            self.error_count = 0
            self.errors = []

        def process_batch(self, image_list, transformations, progress_callback=None):
            """Process a list of images with given transformations."""

            results = []
            total = len(image_list)

            for i, image_path in enumerate(image_list):
                try:
                    # Process image
                    processed = get_image(
                        image_path,
                        framework=self.framework,
                        **transformations
                    )

                    results.append({
                        'path': image_path,
                        'image': processed,
                        'status': 'success'
                    })

                    self.processed_count += 1

                except Exception as e:
                    results.append({
                        'path': image_path,
                        'error': str(e),
                        'status': 'error'
                    })

                    self.error_count += 1
                    self.errors.append(f"{image_path}: {e}")

                # Progress callback
                if progress_callback:
                    progress_callback(i + 1, total)

            return results

        def get_stats(self):
            return {
                'processed': self.processed_count,
                'errors': self.error_count,
                'error_list': self.errors
            }

    # Usage with progress tracking
    def progress_callback(current, total):
        percent = (current / total) * 100
        print(f"Progress: {current}/{total} ({percent:.1f}%)")

    processor = ImageBatchProcessor("customtkinter")

    image_files = ["img1.jpg", "img2.png", "img3.gif"]
    transformations = {
        'size': (400, 300),
        'contrast': 1.3,
        'saturation': 1.2,
        'tint_color': (255, 240, 220),
        'tint_intensity': 0.1
    }

    results = processor.process_batch(
        image_files,
        transformations,
        progress_callback
    )

    stats = processor.get_stats()
    print(f"Processed: {stats['processed']}, Errors: {stats['errors']}")

Quality and Performance Optimization
-------------------------------------

Image Quality Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~

**Choosing Appropriate Sizes:**

.. code-block:: python

    # Size guidelines for different use cases
    SIZES = {
        'thumbnail': (150, 150),
        'small_icon': (16, 16),
        'medium_icon': (32, 32),
        'large_icon': (64, 64),
        'button_image': (24, 24),
        'banner': (1200, 300),
        'background': (1920, 1080),
        'mobile_bg': (375, 667),
        'tablet_bg': (768, 1024)
    }

    # Load appropriate size
    thumbnail = get_image("photo.jpg", framework="tkinter", size=SIZES['thumbnail'])

**Quality vs Performance Trade-offs:**

.. code-block:: python

    # High quality for important images
    hero_image = get_image(
        "hero.jpg",
        framework="customtkinter",
        size=(1200, 600),
        contrast=1.1,
        saturation=1.05
    )

    # Lower quality for thumbnails (faster loading)
    thumbnail = get_image(
        "photo.jpg",
        framework="tkinter",
        size=(100, 100)
    )

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

**Caching Strategies:**

.. code-block:: python

    class OptimizedImageLoader:
        def __init__(self, framework="tkinter", cache_size=100):
            self.framework = framework
            self.cache = {}
            self.cache_size = cache_size
            self.access_order = []

        def get_image(self, name, **kwargs):
            # Create cache key
            cache_key = f"{name}_{hash(str(sorted(kwargs.items())))}"

            if cache_key in self.cache:
                # Move to end (most recently used)
                self.access_order.remove(cache_key)
                self.access_order.append(cache_key)
                return self.cache[cache_key]

            # Load image
            image = get_image(name, framework=self.framework, **kwargs)

            # Add to cache
            self.cache[cache_key] = image
            self.access_order.append(cache_key)

            # Maintain cache size
            while len(self.cache) > self.cache_size:
                oldest = self.access_order.pop(0)
                del self.cache[oldest]

            return image

        def clear_cache(self):
            self.cache.clear()
            self.access_order.clear()

    # Usage
    loader = OptimizedImageLoader("customtkinter", cache_size=50)

    # These will be cached
    icon1 = loader.get_image("icon.png", size=(32, 32))
    icon2 = loader.get_image("icon.png", size=(32, 32))  # From cache

**Memory Management:**

.. code-block:: python

    import gc

    def process_large_batch(image_list, batch_size=10):
        """Process images in smaller batches to manage memory."""

        results = []

        for i in range(0, len(image_list), batch_size):
            batch = image_list[i:i + batch_size]

            # Process batch
            batch_results = []
            for image_path in batch:
                processed = get_image(
                    image_path,
                    framework="tkinter",
                    size=(400, 300)
                )
                batch_results.append(processed)

            results.extend(batch_results)

            # Force garbage collection after each batch
            gc.collect()

            print(f"Processed batch {i//batch_size + 1}")

        return results

Common Processing Recipes
--------------------------

Photo Enhancement
~~~~~~~~~~~~~~~~~

.. code-block:: python

    def enhance_photo(image_path, framework="tkinter"):
        """Standard photo enhancement recipe."""
        return get_image(
            image_path,
            framework=framework,
            contrast=1.15,
            saturation=1.1,
            tint_color=(255, 245, 235),
            tint_intensity=0.05
        )

    def vintage_effect(image_path, framework="tkinter"):
        """Vintage film effect."""
        return get_image(
            image_path,
            framework=framework,
            contrast=1.3,
            saturation=0.8,
            tint_color=(210, 180, 140),
            tint_intensity=0.4
        )

    def dramatic_bw(image_path, framework="tkinter"):
        """Dramatic black and white."""
        return get_image(
            image_path,
            framework=framework,
            grayscale=True,
            contrast=1.5
        )

Icon Processing
~~~~~~~~~~~~~~~

.. code-block:: python

    def create_icon_set(source_image, framework="tkinter"):
        """Create a set of icons in different sizes."""

        sizes = [16, 24, 32, 48, 64, 128, 256]
        icons = {}

        for size in sizes:
            icons[f"{size}x{size}"] = get_image(
                source_image,
                framework=framework,
                size=(size, size)
            )

        return icons

    def create_themed_icons(source_image, framework="customtkinter"):
        """Create icons for different themes."""

        themes = ["default", "light", "dark"]
        icons = {}

        for theme in themes:
            icons[theme] = get_image(
                source_image,
                framework=framework,
                size=(32, 32),
                theme=theme
            )

        return icons

Web Graphics
~~~~~~~~~~~~

.. code-block:: python

    def optimize_for_web(image_path, max_width=1200):
        """Optimize image for web use."""

        # Calculate appropriate size
        # (In real implementation, you'd get original dimensions first)
        web_size = (max_width, int(max_width * 0.75))  # Assume 4:3 ratio

        return get_image(
            image_path,
            framework="tkinter",
            size=web_size,
            contrast=1.05,
            saturation=1.02
        )

    def create_thumbnail_grid(image_list, thumb_size=(150, 150)):
        """Create thumbnails for a grid layout."""

        thumbnails = []

        for image_path in image_list:
            thumb = get_image(
                image_path,
                framework="tkinter",
                size=thumb_size
            )
            thumbnails.append(thumb)

        return thumbnails

Error Handling and Validation
------------------------------

Robust Image Processing
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def safe_process_image(image_path, **kwargs):
        """Safely process an image with error handling."""

        try:
            # Validate image path
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")

            # Check file size (optional)
            file_size = os.path.getsize(image_path)
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                print(f"Warning: Large file size ({file_size / 1024 / 1024:.1f}MB)")

            # Process image
            result = get_image(image_path, **kwargs)

            return {
                'success': True,
                'image': result,
                'path': image_path
            }

        except FileNotFoundError as e:
            return {
                'success': False,
                'error': 'File not found',
                'message': str(e),
                'path': image_path
            }

        except Exception as e:
            return {
                'success': False,
                'error': 'Processing error',
                'message': str(e),
                'path': image_path
            }

    # Usage
    result = safe_process_image(
        "photo.jpg",
        framework="tkinter",
        size=(800, 600),
        contrast=1.2
    )

    if result['success']:
        image = result['image']
        print(f"Successfully processed: {result['path']}")
    else:
        print(f"Error: {result['error']} - {result['message']}")

Integration Examples
--------------------

Complete Application Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from tkinter import filedialog, messagebox
    from gui_image_studio import get_image

    class ImageProcessorApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Image Processor")
            self.root.geometry("800x600")

            self.current_image = None
            self.original_path = None

            self.setup_ui()

        def setup_ui(self):
            # Menu
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)

            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="Open", command=self.open_image)
            file_menu.add_command(label="Save", command=self.save_image)

            # Controls frame
            controls = tk.Frame(self.root)
            controls.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

            # Size controls
            tk.Label(controls, text="Size:").grid(row=0, column=0, sticky=tk.W)
            self.size_var = tk.StringVar(value="400x300")
            size_combo = tk.Entry(controls, textvariable=self.size_var, width=10)
            size_combo.grid(row=0, column=1, padx=5)

            # Contrast control
            tk.Label(controls, text="Contrast:").grid(row=0, column=2, sticky=tk.W)
            self.contrast_var = tk.DoubleVar(value=1.0)
            contrast_scale = tk.Scale(
                controls,
                from_=0.5,
                to=2.0,
                resolution=0.1,
                orient=tk.HORIZONTAL,
                variable=self.contrast_var
            )
            contrast_scale.grid(row=0, column=3, padx=5)

            # Process button
            process_btn = tk.Button(
                controls,
                text="Process",
                command=self.process_image
            )
            process_btn.grid(row=0, column=4, padx=10)

            # Image display
            self.image_label = tk.Label(self.root, text="No image loaded")
            self.image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        def open_image(self):
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("All files", "*.*")
                ]
            )

            if file_path:
                self.original_path = file_path
                self.process_image()

        def process_image(self):
            if not self.original_path:
                messagebox.showwarning("Warning", "Please open an image first")
                return

            try:
                # Parse size
                size_str = self.size_var.get()
                width, height = map(int, size_str.split('x'))

                # Process image
                self.current_image = get_image(
                    self.original_path,
                    framework="tkinter",
                    size=(width, height),
                    contrast=self.contrast_var.get()
                )

                # Display
                self.image_label.configure(image=self.current_image, text="")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {e}")

        def save_image(self):
            if not self.current_image:
                messagebox.showwarning("Warning", "No processed image to save")
                return

            file_path = filedialog.asksaveasfilename(
                title="Save Image",
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )

            if file_path:
                # Note: In a real implementation, you'd need to save the PIL image
                messagebox.showinfo("Info", f"Image would be saved to: {file_path}")

    if __name__ == "__main__":
        root = tk.Tk()
        app = ImageProcessorApp(root)
        root.mainloop()

Next Steps
----------

Now that you understand image processing:

1. **Explore Animation Tools**: :doc:`animation_tools`
2. **Learn Batch Operations**: :doc:`batch_operations`
3. **Try Advanced Examples**: :doc:`../examples/index`
4. **Build Custom Applications**: :doc:`gui_development`
