# Unified Image Processing Core

This document describes the unified image processing core that powers both the
CLI and GUI interfaces of GUI Image Studio.

## Overview

The unified core eliminates code duplication and ensures consistent behavior
between different interfaces by centralizing all image processing logic in a
single, well-tested module.

## Architecture

```text
gui_image_studio/
├── core/                          # Unified image processing core
│   ├── __init__.py               # Core API exports
│   ├── image_effects.py          # Pure image transformation functions
│   └── io_utils.py               # Image I/O utilities
├── cli/                          # CLI interface (thin adapter)
│   ├── __init__.py
│   └── commands.py               # CLI commands using core
├── image_loader.py               # Legacy CLI (now uses core)
└── image_studio/                 # GUI interface (thin adapter)
    └── core/
        └── image_manager.py      # GUI image management using core
```

## Core Modules

### `core/image_effects.py`

Contains pure image transformation functions that:

- Take PIL Image objects and parameters
- Return transformed PIL Image objects
- Have no side effects (no I/O, no progress bars)
- Are fully testable in isolation

**Key Functions:**

- `resize()` - Resize images with optional aspect ratio preservation
- `apply_grayscale()` - Convert to grayscale while preserving alpha
- `apply_rotation()` - Rotate images with expansion options
- `apply_blur()` - Apply Gaussian blur
- `apply_contrast()` - Adjust image contrast
- `apply_saturation()` - Adjust color saturation
- `apply_brightness()` - Adjust image brightness
- `apply_tint()` - Apply color tints
- `apply_transformations()` - Apply multiple transformations in sequence

**Convenience Functions:**

- `create_thumbnail()` - Create thumbnails preserving aspect ratio
- `crop_to_square()` - Crop images to square format
- `add_border()` - Add solid color borders

### `core/io_utils.py`

Handles image loading and saving without side effects in the core processing functions:

**Key Functions:**

- `load_image()` - Load images from file paths
- `save_image()` - Save images to files with format detection
- `load_image_from_data()` - Load from raw bytes
- `load_image_from_base64()` - Load from base64 strings
- `image_to_bytes()` - Convert images to bytes
- `image_to_base64()` - Convert images to base64

## Interface Adapters

### CLI Interface (`cli/commands.py`)

The CLI interface is now a thin adapter that:

1. Parses command-line arguments
2. Loads images using `core/io_utils`
3. Applies transformations using `core/image_effects`
4. Saves results using `core/io_utils`

**New CLI Command:**

```bash
gui-image-studio-process --input image.png --output processed.png \
    --resize 100 100 --blur 2.0 --grayscale
```

### GUI Interface (`image_studio/core/image_manager.py`)

The GUI's ImageManager now uses the unified core for:

- Loading images from files
- Applying transformations
- Creating thumbnails for previews
- Saving processed images

## Benefits

### 1. Single Source of Truth

- All image transformations live in one place
- Fixes and enhancements automatically apply to both CLI and GUI
- No more divergent behavior between interfaces

### 2. Testability

- Pure functions are easy to unit test
- No GUI or CLI dependencies in core tests
- Comprehensive test coverage for all transformations

### 3. Maintainability

- New effects only need to be implemented once
- Clear separation of concerns
- Easier to debug and profile

### 4. Consistency

- Identical behavior across all interfaces
- Same parameter handling and edge cases
- Consistent error messages

### 5. Extensibility

- Easy to add new transformation functions
- Plugin architecture possible through function registry
- Clean API for third-party extensions

## Usage Examples

### Using the Core Directly

```python
from gui_image_studio.core.image_effects import apply_transformations
from gui_image_studio.core.io_utils import load_image, save_image

# Load image
image = load_image("input.png")

# Apply multiple transformations
result = apply_transformations(
    image,
    size=(200, 200),
    rotate=45,
    grayscale=True,
    contrast=1.5,
    blur_radius=2.0
)

# Save result
save_image(result, "output.png")
```

### Using Individual Functions

```python
from gui_image_studio.core.image_effects import (
    resize, apply_blur, apply_grayscale
)

# Chain transformations manually
image = load_image("input.png")
image = resize(image, (100, 100))
image = apply_blur(image, 3.0)
image = apply_grayscale(image)
save_image(image, "output.png")
```

### CLI Usage

```bash
# Basic transformations
gui-image-studio-process -i input.png -o output.png --resize 200 200 --blur 2.0

# Complex transformations
gui-image-studio-process \
    --input photo.jpg \
    --output processed.png \
    --resize 300 300 \
    --rotate 15 \
    --contrast 1.2 \
    --saturation 1.1 \
    --tint-color 255 200 0 \
    --tint-intensity 0.1
```

### GUI Usage

```python
from gui_image_studio.image_studio.core.image_manager import ImageManager

manager = ImageManager()
manager.load_image_from_file("photo", "input.jpg")

# Apply transformations through GUI
manager.apply_transformations_to_image(
    "photo",
    size=(400, 300),
    contrast=1.3,
    saturation=0.9
)

# Save result
manager.save_image_to_file("photo", "output.jpg", quality=90)
```

## Testing

The unified core includes comprehensive tests:

### Unit Tests (`tests/test_image_effects.py`)

- Test each transformation function individually
- Test parameter validation and error handling
- Test edge cases and extreme values

### I/O Tests (`tests/test_io_utils.py`)

- Test image loading from various sources
- Test saving in different formats
- Test format conversion and quality settings

### Integration Tests (`tests/test_integration.py`)

- Verify CLI and GUI produce identical results
- Test complex transformation chains
- Test error handling consistency

### Running Tests

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_image_effects.py
pytest tests/test_io_utils.py
pytest tests/test_integration.py

# Run with coverage
pytest --cov=gui_image_studio.core
```

## Migration Guide

### For CLI Users

The existing CLI commands continue to work unchanged. The new
`gui-image-studio-process` command provides additional functionality.

### For GUI Users

The GUI interface remains the same. All transformations now use the unified
core internally.

### For Developers

If you were using internal transformation functions:

**Before:**

```python
from gui_image_studio.image_loader import _apply_image_transformations
result = _apply_image_transformations(image, grayscale=True, size=(100, 100))
```

**After:**

```python
from gui_image_studio.core.image_effects import apply_transformations
result = apply_transformations(image, grayscale=True, size=(100, 100))
```

## Performance Considerations

### Optimization

- Transformations are applied in optimal order
- Memory usage is minimized through in-place operations where possible
- PIL/Pillow optimizations are leveraged

### Caching

- The GUI ImageManager caches thumbnails
- Original images are preserved for non-destructive editing
- Transformation history can be maintained

### Batch Processing

The unified core makes batch processing straightforward:

```python
from pathlib import Path
from gui_image_studio.core.image_effects import apply_transformations
from gui_image_studio.core.io_utils import load_image, save_image

def batch_process(input_dir, output_dir, **transforms):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for image_file in input_path.glob("*.{png,jpg,jpeg}"):
        image = load_image(image_file)
        processed = apply_transformations(image, **transforms)
        save_image(processed, output_path / image_file.name)
```

## Future Enhancements

### Plugin System

A registry system could allow dynamic loading of transformation functions:

```python
from gui_image_studio.core.registry import register_effect

@register_effect("vintage")
def apply_vintage_effect(image, intensity=0.5):
    # Custom vintage effect implementation
    return processed_image
```

### Async Processing

For GUI responsiveness, transformations could be made async:

```python
import asyncio
from gui_image_studio.core.image_effects import apply_transformations_async

async def process_image_async(image, **transforms):
    return await apply_transformations_async(image, **transforms)
```

### GPU Acceleration

Future versions could leverage GPU acceleration for intensive operations
while maintaining the same API.

## Conclusion

The unified image processing core provides a solid foundation for consistent,
maintainable, and extensible image processing across all interfaces. It
eliminates code duplication, improves testability, and ensures that users get
identical results regardless of how they interact with GUI Image Studio.
