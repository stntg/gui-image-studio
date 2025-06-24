Sample Creator Module
=====================

The ``sample_creator`` module provides functionality for generating sample images for testing, development, and demonstration purposes.

.. automodule:: gui_image_studio.sample_creator
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The sample creator module allows you to:

* Generate various types of test images
* Create sample images with different properties
* Produce animated GIF samples
* Generate images for performance testing
* Create consistent test data

This is particularly useful for:

* Testing image processing algorithms
* Demonstrating application features
* Performance benchmarking
* Unit and integration testing
* Documentation examples

Main Classes
------------

SampleCreator
~~~~~~~~~~~~~

.. autoclass:: gui_image_studio.sample_creator.SampleCreator
   :members:
   :undoc-members:
   :show-inheritance:

The main class for creating sample images.

**Initialization:**

.. code-block:: python

    from gui_image_studio.sample_creator import SampleCreator

    creator = SampleCreator(
        output_dir="sample_images",
        size=(256, 256),
        formats=['png', 'jpg', 'gif']
    )

**Basic Usage:**

.. code-block:: python

    # Create all default samples
    creator.create_all_samples()

**Advanced Configuration:**

.. code-block:: python

    creator = SampleCreator(
        output_dir="test_data",
        size=(512, 512),
        formats=['png'],
        count=5,
        include_animated=True
    )

**Methods:**

create_all_samples
^^^^^^^^^^^^^^^^^^

.. automethod:: gui_image_studio.sample_creator.SampleCreator.create_all_samples

Create all types of sample images.

**Returns:**
  * ``bool``: True if all samples were created successfully

**Example:**

.. code-block:: python

    success = creator.create_all_samples()
    if success:
        print("All samples created successfully")

create_icon_samples
^^^^^^^^^^^^^^^^^^^

.. automethod:: gui_image_studio.sample_creator.SampleCreator.create_icon_samples

Create icon-style sample images.

**Parameters:**
  * ``count`` (int, optional): Number of icons to create

**Example:**

.. code-block:: python

    creator.create_icon_samples(count=10)

create_photo_samples
^^^^^^^^^^^^^^^^^^^^

.. automethod:: gui_image_studio.sample_creator.SampleCreator.create_photo_samples

Create photo-style sample images.

**Parameters:**
  * ``count`` (int, optional): Number of photos to create

**Example:**

.. code-block:: python

    creator.create_photo_samples(count=5)

create_gradient_samples
^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: gui_image_studio.sample_creator.SampleCreator.create_gradient_samples

Create gradient sample images for testing filters.

**Parameters:**
  * ``count`` (int, optional): Number of gradients to create

**Example:**

.. code-block:: python

    creator.create_gradient_samples(count=3)

create_animated_samples
^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: gui_image_studio.sample_creator.SampleCreator.create_animated_samples

Create animated GIF sample images.

**Parameters:**
  * ``count`` (int, optional): Number of animations to create

**Example:**

.. code-block:: python

    creator.create_animated_samples(count=2)

create_transparency_samples
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: gui_image_studio.sample_creator.SampleCreator.create_transparency_samples

Create images with transparency for testing alpha channel handling.

**Parameters:**
  * ``count`` (int, optional): Number of transparent images to create

**Example:**

.. code-block:: python

    creator.create_transparency_samples(count=3)

Sample Types
------------

Icon Samples
~~~~~~~~~~~~

**Generated Icons:**

* **Simple Geometric**: Circles, squares, triangles
* **Symbolic**: Home, save, open, settings icons
* **Colorful**: Various color schemes and styles
* **Sizes**: Multiple sizes (16x16, 32x32, 64x64)

**Example Icon Creation:**

.. code-block:: python

    def create_home_icon(size=(32, 32)):
        """Create a simple home icon."""
        from PIL import Image, ImageDraw

        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw house shape
        width, height = size
        # ... drawing code ...

        return image

Photo Samples
~~~~~~~~~~~~~

**Generated Photos:**

* **Landscapes**: Mountains, beaches, forests
* **Portraits**: Simple face-like patterns
* **Objects**: Geometric objects with realistic lighting
* **Textures**: Wood, metal, fabric patterns

**Example Photo Creation:**

.. code-block:: python

    def create_landscape_photo(size=(800, 600)):
        """Create a simple landscape photo."""
        from PIL import Image, ImageDraw
        import random

        image = Image.new('RGB', size, '#87CEEB')  # Sky blue
        draw = ImageDraw.Draw(image)

        # Draw mountains, trees, etc.
        # ... drawing code ...

        return image

Gradient Samples
~~~~~~~~~~~~~~~~

**Generated Gradients:**

* **Linear**: Horizontal, vertical, diagonal gradients
* **Radial**: Circular gradients from center
* **Multi-color**: Complex color transitions
* **Patterns**: Repeating gradient patterns

**Example Gradient Creation:**

.. code-block:: python

    def create_linear_gradient(size=(256, 256), colors=['#FF0000', '#0000FF']):
        """Create a linear gradient."""
        from PIL import Image
        import numpy as np

        width, height = size
        # Create gradient using numpy
        # ... gradient calculation ...

        return Image.fromarray(gradient_array)

Animated Samples
~~~~~~~~~~~~~~~~

**Generated Animations:**

* **Rotating Objects**: Spinning shapes and icons
* **Color Transitions**: Smooth color changes
* **Moving Elements**: Bouncing balls, sliding objects
* **Morphing Shapes**: Shape transformations

**Example Animation Creation:**

.. code-block:: python

    def create_spinning_animation(size=(128, 128), frames=20):
        """Create a spinning square animation."""
        from PIL import Image, ImageDraw

        images = []
        for i in range(frames):
            angle = (360 / frames) * i
            image = Image.new('RGBA', size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)

            # Draw rotated square
            # ... rotation and drawing code ...

            images.append(image)

        return images

Transparency Samples
~~~~~~~~~~~~~~~~~~~~

**Generated Transparent Images:**

* **Alpha Gradients**: Gradual transparency effects
* **Cutout Shapes**: Shapes with transparent backgrounds
* **Overlay Elements**: Semi-transparent overlays
* **Complex Alpha**: Multiple transparency levels

**Example Transparency Creation:**

.. code-block:: python

    def create_alpha_gradient(size=(256, 256)):
        """Create an image with alpha gradient."""
        from PIL import Image
        import numpy as np

        # Create RGBA image with alpha gradient
        # ... alpha calculation ...

        return Image.fromarray(rgba_array, 'RGBA')

Utility Functions
-----------------

create_sample_image
~~~~~~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.sample_creator.create_sample_image

Create a single sample image of specified type.

**Parameters:**
  * ``sample_type`` (str): Type of sample ('icon', 'photo', 'gradient', etc.)
  * ``size`` (Tuple[int, int]): Image dimensions
  * ``output_path`` (str): Path to save the image
  * ``parameters`` (dict, optional): Type-specific parameters

**Returns:**
  * ``PIL.Image.Image``: Created sample image

**Example:**

.. code-block:: python

    # Create a gradient sample
    image = create_sample_image(
        'gradient',
        (512, 512),
        'test_gradient.png',
        {'colors': ['#FF0000', '#00FF00', '#0000FF']}
    )

generate_test_suite
~~~~~~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.sample_creator.generate_test_suite

Generate a complete test suite of sample images.

**Parameters:**
  * ``output_dir`` (str): Directory for test images
  * ``sizes`` (List[Tuple[int, int]]): List of image sizes to generate
  * ``formats`` (List[str]): List of formats to generate

**Example:**

.. code-block:: python

    generate_test_suite(
        'test_suite',
        sizes=[(64, 64), (256, 256), (1024, 1024)],
        formats=['png', 'jpg', 'gif']
    )

validate_samples
~~~~~~~~~~~~~~~~

.. autofunction:: gui_image_studio.sample_creator.validate_samples

Validate that generated samples meet requirements.

**Parameters:**
  * ``sample_dir`` (str): Directory containing samples
  * ``requirements`` (dict): Validation requirements

**Returns:**
  * ``bool``: True if all samples are valid

**Example:**

.. code-block:: python

    requirements = {
        'min_size': (32, 32),
        'max_size': (2048, 2048),
        'required_formats': ['png', 'jpg'],
        'min_count': 5
    }

    is_valid = validate_samples('sample_images', requirements)

Configuration
-------------

**Sample Configuration:**

.. code-block:: python

    config = {
        'icon_samples': {
            'count': 10,
            'sizes': [(16, 16), (32, 32), (64, 64)],
            'styles': ['geometric', 'symbolic', 'colorful']
        },
        'photo_samples': {
            'count': 5,
            'sizes': [(800, 600), (1920, 1080)],
            'types': ['landscape', 'portrait', 'object']
        },
        'gradient_samples': {
            'count': 8,
            'types': ['linear', 'radial', 'multi-color'],
            'color_schemes': ['warm', 'cool', 'monochrome']
        },
        'animated_samples': {
            'count': 3,
            'frame_count': 20,
            'duration': 100,  # milliseconds
            'types': ['rotation', 'color_transition', 'movement']
        }
    }

    creator = SampleCreator(config=config)

**Quality Settings:**

.. code-block:: python

    creator = SampleCreator(
        quality_settings={
            'jpg_quality': 95,
            'png_compression': 6,
            'gif_optimization': True
        }
    )

Advanced Usage
--------------

**Custom Sample Types:**

.. code-block:: python

    class CustomSampleCreator(SampleCreator):
        def create_custom_samples(self, count=1):
            """Create custom sample type."""
            for i in range(count):
                # Create custom image
                image = self.create_custom_image()

                # Save with naming convention
                filename = f"custom_sample_{i+1:03d}.png"
                output_path = os.path.join(self.output_dir, filename)
                image.save(output_path)

        def create_custom_image(self):
            """Create a custom image."""
            # Custom image creation logic
            pass

**Batch Generation:**

.. code-block:: python

    def generate_test_data():
        """Generate comprehensive test data."""

        # Small images for unit tests
        small_creator = SampleCreator("tests/small", size=(64, 64))
        small_creator.create_all_samples()

        # Medium images for integration tests
        medium_creator = SampleCreator("tests/medium", size=(256, 256))
        medium_creator.create_all_samples()

        # Large images for performance tests
        large_creator = SampleCreator("tests/large", size=(2048, 2048))
        large_creator.create_photo_samples(count=3)

**Parameterized Generation:**

.. code-block:: python

    def create_parameterized_samples():
        """Create samples with various parameters."""

        creator = SampleCreator("parameterized_samples")

        # Different sizes
        for size in [(64, 64), (128, 128), (256, 256)]:
            creator.size = size
            creator.create_icon_samples(count=2)

        # Different color schemes
        color_schemes = ['warm', 'cool', 'monochrome', 'vibrant']
        for scheme in color_schemes:
            creator.create_gradient_samples(
                count=1,
                parameters={'color_scheme': scheme}
            )

**Performance Testing Samples:**

.. code-block:: python

    def create_performance_samples():
        """Create samples for performance testing."""

        # Memory usage tests
        memory_creator = SampleCreator("performance/memory")
        memory_creator.create_photo_samples(
            count=1,
            size=(8192, 8192)  # Very large image
        )

        # Processing speed tests
        speed_creator = SampleCreator("performance/speed")
        speed_creator.create_all_samples(count=100)  # Many small images

        # Animation performance tests
        anim_creator = SampleCreator("performance/animation")
        anim_creator.create_animated_samples(
            count=1,
            parameters={'frame_count': 100, 'size': (512, 512)}
        )

Integration with Testing
------------------------

**Unit Test Integration:**

.. code-block:: python

    import unittest
    from gui_image_studio.sample_creator import SampleCreator

    class TestImageProcessing(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            """Create test samples once for all tests."""
            cls.creator = SampleCreator("test_samples")
            cls.creator.create_all_samples()

        def test_image_loading(self):
            """Test loading sample images."""
            # Test with generated samples
            pass

        def test_image_processing(self):
            """Test processing sample images."""
            # Test with generated samples
            pass

**Pytest Integration:**

.. code-block:: python

    import pytest
    from gui_image_studio.sample_creator import SampleCreator

    @pytest.fixture(scope="session")
    def sample_images():
        """Create sample images for testing."""
        creator = SampleCreator("pytest_samples")
        creator.create_all_samples()
        return creator.output_dir

    def test_with_samples(sample_images):
        """Test using sample images."""
        # Use sample_images directory
        pass

**Continuous Integration:**

.. code-block:: yaml

    # GitHub Actions example
    - name: Generate test samples
      run: |
        python -c "
        from gui_image_studio.sample_creator import SampleCreator
        creator = SampleCreator('ci_samples')
        creator.create_all_samples()
        "

Error Handling
--------------

**Common Issues:**

* **Disk Space**: Large samples may fill disk
* **Memory**: High-resolution samples consume memory
* **Permissions**: Output directory write permissions
* **Dependencies**: Missing PIL/Pillow dependencies

**Error Handling Example:**

.. code-block:: python

    try:
        creator = SampleCreator("samples")
        creator.create_all_samples()
    except PermissionError:
        print("Cannot write to output directory")
    except MemoryError:
        print("Not enough memory for large samples")
    except Exception as e:
        print(f"Sample creation failed: {e}")

**Validation:**

.. code-block:: python

    def safe_create_samples(output_dir, max_size=(1024, 1024)):
        """Safely create samples with validation."""

        # Check disk space
        free_space = shutil.disk_usage(output_dir).free
        if free_space < 100 * 1024 * 1024:  # 100MB
            raise RuntimeError("Insufficient disk space")

        # Create with size limit
        creator = SampleCreator(output_dir, size=max_size)
        return creator.create_all_samples()

Performance Considerations
--------------------------

**Memory Usage:**

* Large images consume significant memory
* Animated samples require memory for all frames
* Consider creating samples in batches

**Disk Usage:**

* High-resolution samples create large files
* Multiple formats multiply disk usage
* Clean up old samples regularly

**Generation Time:**

* Complex samples take longer to generate
* Animated samples require more processing
* Consider parallel generation for large batches

**Optimization Tips:**

.. code-block:: python

    # Optimize for speed
    creator = SampleCreator(
        size=(256, 256),  # Reasonable size
        formats=['png'],  # Single format
        count=1  # Minimal count
    )

    # Optimize for comprehensive testing
    creator = SampleCreator(
        size=(512, 512),
        formats=['png', 'jpg', 'gif'],
        count=5,
        include_animated=True
    )

    # Generate optimized samples
    creator.create_all_samples()

**Memory Management:**

.. code-block:: python

    # For large sample generation
    import gc

    def create_large_samples():
        """Create large samples with memory management."""
        creator = SampleCreator("large_samples", size=(2048, 2048))

        # Create samples one by one to manage memory
        for i in range(10):
            creator.create_photo_samples(count=1)
            gc.collect()  # Force garbage collection

        print("Large samples created successfully")

Summary
-------

The Sample Creator module provides comprehensive functionality for generating test images and sample data. It supports various image types, formats, and configurations to meet different testing and development needs.

**Key Features:**

* Multiple sample types (icons, photos, gradients, animations, transparency)
* Configurable sizes, formats, and quality settings
* Batch generation capabilities
* Custom sample type support
* Performance optimization options
* Comprehensive validation tools

**Best Practices:**

* Use appropriate sample sizes for your testing needs
* Choose formats that match your application requirements
* Implement proper error handling for sample generation
* Consider memory usage when generating large samples
* Validate generated samples before use in tests
