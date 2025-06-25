Image Processing Examples
=========================

This section demonstrates advanced image processing techniques using GUI Image Studio.

Advanced Filtering
------------------

**Custom Filter Implementation**

.. code-block:: python

    # Example: Advanced Image Filtering
    # Demonstrates how to implement and apply custom image filters.

    import gui_image_studio
    from PIL import Image, ImageFilter, ImageEnhance
    import numpy as np

    def apply_vintage_filter(image_path: str, output_path: str) -> bool:
        """
        Apply a vintage/retro filter to an image.

        Args:
            image_path: Path to input image
            output_path: Path for output image

        Returns:
            True if successful
        """
        try:
            # Load the image
            image = gui_image_studio.get_image(image_path)

            # Step 1: Reduce saturation for vintage look
            enhancer = ImageEnhance.Color(image)
            desaturated = enhancer.enhance(0.7)  # Reduce saturation by 30%

            # Step 2: Apply sepia tint
            sepia_tinted = gui_image_studio.apply_tint(desaturated, "#D2B48C", opacity=0.4)

            # Step 3: Add slight blur for softness
            softened = sepia_tinted.filter(ImageFilter.GaussianBlur(radius=0.5))

            # Step 4: Adjust contrast
            contrast_enhancer = ImageEnhance.Contrast(softened)
            final_image = contrast_enhancer.enhance(1.2)  # Increase contrast by 20%

            # Save the result
            gui_image_studio.save_image(final_image, output_path)
            return True

        except Exception as e:
            print(f"Error applying vintage filter: {e}")
            return False

    # Example usage
    if __name__ == "__main__":
        apply_vintage_filter("sample_images/sample_photo.jpg", "vintage_photo.jpg")

**Multi-Step Processing Pipeline**

.. code-block:: python

    # Example: Image Processing Pipeline
    # Shows how to create a multi-step processing pipeline for batch operations.

    import gui_image_studio
    from typing import List, Callable, Any
    from PIL import Image

    class ImageProcessor:
        """A flexible image processing pipeline."""

        def __init__(self):
            self.steps: List[Callable] = []

        def add_step(self, func: Callable, **kwargs) -> 'ImageProcessor':
            """Add a processing step to the pipeline."""
            self.steps.append(lambda img: func(img, **kwargs))
            return self

        def process(self, image: Image.Image) -> Image.Image:
            """Process image through all pipeline steps."""
            result = image
            for step in self.steps:
                result = step(result)
            return result

        def process_file(self, input_path: str, output_path: str) -> bool:
            """Process a file through the pipeline."""
            try:
                image = gui_image_studio.get_image(input_path)
                processed = self.process(image)
                gui_image_studio.save_image(processed, output_path)
                return True
            except Exception as e:
                print(f"Error processing {input_path}: {e}")
                return False

    # Define processing functions
    def resize_step(image: Image.Image, size: tuple) -> Image.Image:
        """Resize image step."""
        return gui_image_studio.resize_image(image, size)

    def tint_step(image: Image.Image, color: str, opacity: float = 0.3) -> Image.Image:
        """Apply tint step."""
        return gui_image_studio.apply_tint(image, color, opacity)

    def enhance_step(image: Image.Image, brightness: float = 1.0,
                    contrast: float = 1.0) -> Image.Image:
        """Enhance brightness and contrast."""
        from PIL import ImageEnhance

        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness)

        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast)

        return image

    # Example pipeline usage
    def create_thumbnail_pipeline():
        """Create a pipeline for generating thumbnails."""
        return (ImageProcessor()
                .add_step(resize_step, size=(150, 150))
                .add_step(enhance_step, brightness=1.1, contrast=1.2)
                .add_step(tint_step, color="#4ECDC4", opacity=0.1))

    def create_web_optimization_pipeline():
        """Create a pipeline for web-optimized images."""
        return (ImageProcessor()
                .add_step(resize_step, size=(800, 600))
                .add_step(enhance_step, contrast=1.1))

    # Usage example
    if __name__ == "__main__":
        # Create thumbnail
        thumb_processor = create_thumbnail_pipeline()
        thumb_processor.process_file("sample_images/sample_photo.jpg", "thumbnail.jpg")

        # Create web-optimized version
        web_processor = create_web_optimization_pipeline()
        web_processor.process_file("sample_images/sample_photo.jpg", "web_optimized.jpg")

Color Manipulation
------------------

**Advanced Color Operations**

.. code-block:: python

    # Example: Advanced Color Manipulation
    # Demonstrates sophisticated color manipulation techniques.

    import gui_image_studio
    from PIL import Image, ImageEnhance
    import colorsys

    def adjust_hue_saturation_lightness(image_path: str, hue_shift: float = 0,
                                       saturation_factor: float = 1.0,
                                       lightness_factor: float = 1.0) -> Image.Image:
        """
        Adjust HSL values of an image.

        Args:
            image_path: Path to input image
            hue_shift: Hue shift in degrees (-180 to 180)
            saturation_factor: Saturation multiplier (0.0 to 2.0)
            lightness_factor: Lightness multiplier (0.0 to 2.0)

        Returns:
            Processed PIL Image
        """
        image = gui_image_studio.get_image(image_path)

        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Get pixel data
        pixels = image.load()
        width, height = image.size

        # Process each pixel
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]

                # Convert RGB to HSL
                h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

                # Apply adjustments
                h = (h + hue_shift/360.0) % 1.0  # Normalize hue
                s = max(0, min(1, s * saturation_factor))  # Clamp saturation
                l = max(0, min(1, l * lightness_factor))   # Clamp lightness

                # Convert back to RGB
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                pixels[x, y] = (int(r*255), int(g*255), int(b*255))

        return image

    def create_color_variations(image_path: str, output_dir: str = "color_variations"):
        """Create multiple color variations of an image."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        # Original image
        original = gui_image_studio.get_image(image_path)
        gui_image_studio.save_image(original, f"{output_dir}/original.jpg")

        # Hue variations
        hue_shifts = [-60, -30, 30, 60, 120, 180]
        for shift in hue_shifts:
            varied = adjust_hue_saturation_lightness(image_path, hue_shift=shift)
            gui_image_studio.save_image(varied, f"{output_dir}/hue_shift_{shift:+d}.jpg")

        # Saturation variations
        sat_factors = [0.3, 0.6, 1.5, 2.0]
        for factor in sat_factors:
            varied = adjust_hue_saturation_lightness(image_path, saturation_factor=factor)
            gui_image_studio.save_image(varied, f"{output_dir}/saturation_{factor:.1f}.jpg")

        # Lightness variations
        light_factors = [0.5, 0.7, 1.3, 1.6]
        for factor in light_factors:
            varied = adjust_hue_saturation_lightness(image_path, lightness_factor=factor)
            gui_image_studio.save_image(varied, f"{output_dir}/lightness_{factor:.1f}.jpg")

    # Example usage
    if __name__ == "__main__":
        create_color_variations("sample_images/sample_photo.jpg")

**Color Palette Extraction**

.. code-block:: python

    # Example: Color Palette Extraction
    # Extract dominant colors from images and create color palettes.

    import gui_image_studio
    from PIL import Image
    from collections import Counter
    import numpy as np

    def extract_dominant_colors(image_path: str, num_colors: int = 5) -> list:
        """
        Extract dominant colors from an image.

        Args:
            image_path: Path to input image
            num_colors: Number of dominant colors to extract

        Returns:
            List of RGB tuples representing dominant colors
        """
        image = gui_image_studio.get_image(image_path)

        # Resize for faster processing
        image = image.resize((150, 150))

        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Get all pixels
        pixels = list(image.getdata())

        # Count color frequency
        color_counts = Counter(pixels)

        # Get most common colors
        dominant_colors = [color for color, count in color_counts.most_common(num_colors)]

        return dominant_colors

    def create_color_palette_image(colors: list, size: tuple = (400, 100)) -> Image.Image:
        """Create a visual color palette from a list of colors."""
        width, height = size
        palette = Image.new('RGB', size)

        color_width = width // len(colors)

        for i, color in enumerate(colors):
            # Create rectangle for each color
            x1 = i * color_width
            x2 = (i + 1) * color_width if i < len(colors) - 1 else width

            # Fill the rectangle with the color
            for x in range(x1, x2):
                for y in range(height):
                    palette.putpixel((x, y), color)

        return palette

    def analyze_image_colors(image_path: str, output_dir: str = "color_analysis"):
        """Perform comprehensive color analysis of an image."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        # Extract dominant colors
        colors = extract_dominant_colors(image_path, num_colors=8)

        # Create palette image
        palette = create_color_palette_image(colors)
        palette_path = f"{output_dir}/color_palette.png"
        gui_image_studio.save_image(palette, palette_path)

        # Create tinted versions using dominant colors
        original = gui_image_studio.get_image(image_path)

        for i, color in enumerate(colors[:5]):  # Use top 5 colors
            # Convert RGB tuple to hex
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

            # Apply tint
            tinted = gui_image_studio.apply_tint(original, hex_color, opacity=0.3)
            tinted_path = f"{output_dir}/tinted_with_color_{i+1}.jpg"
            gui_image_studio.save_image(tinted, tinted_path)

        # Print color information
        print(f"Dominant colors extracted from {image_path}:")
        for i, color in enumerate(colors, 1):
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            print(f"  {i}. RGB{color} -> {hex_color}")

    # Example usage
    if __name__ == "__main__":
        analyze_image_colors("sample_images/sample_photo.jpg")

Geometric Transformations
-------------------------

**Advanced Transformation Techniques**

.. code-block:: python

    # Example: Advanced Geometric Transformations
    # Demonstrates complex geometric transformations and perspective effects.

    import gui_image_studio
    from PIL import Image, ImageDraw
    import math

    def create_perspective_transform(image_path: str, perspective_factor: float = 0.3) -> Image.Image:
        """
        Apply a perspective transformation to create depth effect.

        Args:
            image_path: Path to input image
            perspective_factor: Strength of perspective effect (0.0 to 1.0)

        Returns:
            Transformed PIL Image
        """
        image = gui_image_studio.get_image(image_path)
        width, height = image.size

        # Calculate perspective transformation points
        offset = int(width * perspective_factor)

        # Define transformation: trapezoid to rectangle
        # Top edge is narrower than bottom edge
        transform_points = [
            (offset, 0),           # Top-left
            (width - offset, 0),   # Top-right
            (width, height),       # Bottom-right
            (0, height)            # Bottom-left
        ]

        # Create new image with perspective
        # Note: This is a simplified perspective transform
        # For more complex transforms, consider using PIL's transform method

        return image  # Placeholder - implement actual perspective transform

    def create_rotation_sequence(image_path: str, output_dir: str = "rotation_sequence"):
        """Create a sequence of rotated images."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        image = gui_image_studio.get_image(image_path)

        # Create rotation sequence
        angles = range(0, 360, 15)  # Every 15 degrees

        for angle in angles:
            rotated = gui_image_studio.rotate_image(image, angle)
            filename = f"rotation_{angle:03d}deg.png"
            output_path = os.path.join(output_dir, filename)
            gui_image_studio.save_image(rotated, output_path)

        print(f"Created {len(angles)} rotated images in {output_dir}")

    def create_scaling_sequence(image_path: str, output_dir: str = "scaling_sequence"):
        """Create a sequence of scaled images."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        image = gui_image_studio.get_image(image_path)
        original_size = image.size

        # Create scaling sequence
        scale_factors = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

        for factor in scale_factors:
            new_size = (int(original_size[0] * factor), int(original_size[1] * factor))
            scaled = gui_image_studio.resize_image(image, new_size)
            filename = f"scale_{factor:.2f}x.png"
            output_path = os.path.join(output_dir, filename)
            gui_image_studio.save_image(scaled, output_path)

        print(f"Created {len(scale_factors)} scaled images in {output_dir}")

    # Example usage
    if __name__ == "__main__":
        create_rotation_sequence("sample_images/sample_icon.png")
        create_scaling_sequence("sample_images/sample_icon.png")

Performance Optimization
------------------------

**Optimized Batch Processing**

.. code-block:: python

    # Example: Optimized Batch Processing
    # Demonstrates efficient techniques for processing large numbers of images.

    import gui_image_studio
    import os
    import time
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    from typing import List, Callable

    def process_single_image(args: tuple) -> bool:
        """Process a single image (for use with multiprocessing)."""
        input_path, output_path, operations = args

        try:
            # Load image
            image = gui_image_studio.get_image(input_path)

            # Apply operations
            for operation, params in operations:
                if operation == 'resize':
                    image = gui_image_studio.resize_image(image, params['size'])
                elif operation == 'tint':
                    image = gui_image_studio.apply_tint(image, params['color'])
                elif operation == 'rotate':
                    image = gui_image_studio.rotate_image(image, params['angle'])

            # Save result
            gui_image_studio.save_image(image, output_path)
            return True

        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            return False

    def batch_process_threaded(input_files: List[str], output_dir: str,
                              operations: List[tuple], max_workers: int = 4) -> int:
        """
        Process images using threading for I/O-bound operations.

        Args:
            input_files: List of input file paths
            output_dir: Output directory
            operations: List of (operation_name, parameters) tuples
            max_workers: Maximum number of worker threads

        Returns:
            Number of successfully processed images
        """
        os.makedirs(output_dir, exist_ok=True)

        # Prepare arguments for each image
        args_list = []
        for input_path in input_files:
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_processed{ext}")
            args_list.append((input_path, output_path, operations))

        # Process with thread pool
        successful = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(process_single_image, args_list)
            successful = sum(results)

        return successful

    def batch_process_multiprocess(input_files: List[str], output_dir: str,
                                  operations: List[tuple], max_workers: int = None) -> int:
        """
        Process images using multiprocessing for CPU-bound operations.

        Args:
            input_files: List of input file paths
            output_dir: Output directory
            operations: List of (operation_name, parameters) tuples
            max_workers: Maximum number of worker processes

        Returns:
            Number of successfully processed images
        """
        if max_workers is None:
            max_workers = os.cpu_count()

        os.makedirs(output_dir, exist_ok=True)

        # Prepare arguments for each image
        args_list = []
        for input_path in input_files:
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_processed{ext}")
            args_list.append((input_path, output_path, operations))

        # Process with process pool
        successful = 0
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(process_single_image, args_list)
            successful = sum(results)

        return successful

    def benchmark_processing_methods(input_files: List[str]):
        """Benchmark different processing methods."""
        operations = [
            ('resize', {'size': (400, 300)}),
            ('tint', {'color': '#FF6B6B'})
        ]

        print(f"Benchmarking with {len(input_files)} images...")

        # Sequential processing
        start_time = time.time()
        sequential_success = 0
        for input_path in input_files:
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            output_path = f"sequential_{name}_processed{ext}"

            if process_single_image((input_path, output_path, operations)):
                sequential_success += 1

        sequential_time = time.time() - start_time

        # Threaded processing
        start_time = time.time()
        threaded_success = batch_process_threaded(input_files, "threaded_output", operations)
        threaded_time = time.time() - start_time

        # Multiprocess processing
        start_time = time.time()
        multiprocess_success = batch_process_multiprocess(input_files, "multiprocess_output", operations)
        multiprocess_time = time.time() - start_time

        # Print results
        print("\nBenchmark Results:")
        print(f"Sequential:   {sequential_success}/{len(input_files)} images in {sequential_time:.2f}s")
        print(f"Threaded:     {threaded_success}/{len(input_files)} images in {threaded_time:.2f}s")
        print(f"Multiprocess: {multiprocess_success}/{len(input_files)} images in {multiprocess_time:.2f}s")

        if sequential_time > 0:
            print(f"\nSpeedup:")
            print(f"Threaded:     {sequential_time/threaded_time:.2f}x")
            print(f"Multiprocess: {sequential_time/multiprocess_time:.2f}x")

    # Example usage
    if __name__ == "__main__":
        # Create test images first
        from gui_image_studio.sample_creator import SampleCreator
        creator = SampleCreator("benchmark_input", count=10)
        creator.create_photo_samples()

        # Get list of test images
        input_files = [f"benchmark_input/sample_photo_{i:03d}.jpg" for i in range(1, 11)]
        input_files = [f for f in input_files if os.path.exists(f)]

        # Run benchmark
        benchmark_processing_methods(input_files)

Running the Examples
--------------------

To run these image processing examples:

1. **Create sample images:**

   .. code-block:: bash

       gui-image-studio-create-samples

2. **Run individual examples:**

   .. code-block:: bash

       python vintage_filter.py
       python color_analysis.py
       python batch_processing.py

3. **Check output directories** for processed images

Each example demonstrates different aspects of image processing and can be adapted for your specific needs.

Next Steps
----------

After mastering these image processing techniques:

* Explore :doc:`animation_creation` for working with animated content
* Learn about :doc:`custom_filters` for creating your own processing algorithms
* Check out :doc:`batch_processing` for automating large-scale operations
* Try :doc:`gui_application` for building interactive image editors
