# img2res

A Python package for embedding images as base64 strings with GUI framework support for tkinter and customtkinter.

## Features

- 🖼️ Convert images to base64 encoded strings
- 📁 Batch process entire folders of images
- 🎨 Support for multiple GUI frameworks (tkinter, customtkinter)
- 🔧 Image transformations (resize, rotate, flip, tint, contrast, saturation)
- 📦 Generate embedded Python modules for easy distribution
- 🎬 Animated GIF support
- 🎯 High-quality compression options
- 📝 Sample image generation for testing

## Installation

### From PyPI (when published)
```bash
pip install img2res
```

### From Source
```bash
git clone https://github.com/stntg/img2res.git
cd img2res
pip install -e .
```

## Quick Start

### Basic Usage

```python
from img2res import get_image, embed_images_from_folder

# Get a single image as PhotoImage object
image = get_image("my_image.png", framework="tkinter")

# Embed all images from a folder
embed_images_from_folder(
    input_folder="images/",
    output_file="embedded_images.py",
    framework="tkinter",
    quality=90
)
```

### Using Embedded Images

```python
# After embedding images, use them in your GUI
from embedded_images import get_image

import tkinter as tk
root = tk.Tk()

# Load embedded image
photo = get_image("my_image.png")
label = tk.Label(root, image=photo)
label.pack()

root.mainloop()
```

### Command Line Interface

```bash
# Create sample images for testing
python -m img2res.sample_creator

# Embed images from a folder
python -m img2res.cli embed-folder images/ --output embedded_images.py --framework tkinter
```

## Advanced Features

### Image Transformations

```python
from img2res import get_image

# Apply transformations
image = get_image(
    "photo.jpg",
    framework="customtkinter",
    size=(200, 200),
    rotation=45,
    flip="horizontal",
    tint_color="#FF0000",
    contrast=1.2,
    saturation=1.5
)
```

### Animated GIFs

```python
from img2res.image_loader import load_animated_gif

# Load animated GIF for customtkinter
frames = load_animated_gif("animation.gif", size=(100, 100))
```

## Supported Frameworks

- **tkinter**: Python's standard GUI library
- **customtkinter**: Modern tkinter-based framework

## Examples

Check out the `examples/` directory for comprehensive usage examples:

- `01_basic_usage.py` - Basic image loading and display
- `02_theming_examples.py` - Theme integration examples
- `03_image_transformations.py` - Image manipulation features
- `04_animated_gifs.py` - Animated GIF handling
- `05_advanced_features.py` - Advanced usage patterns

Run all examples:
```bash
python examples/run_examples.py
```

## API Reference

### Core Functions

#### `get_image(image_path, framework="tkinter", **kwargs)`
Load and return an image object for the specified GUI framework.

**Parameters:**
- `image_path` (str): Path to the image file
- `framework` (str): GUI framework ("tkinter" or "customtkinter")
- `size` (tuple): Resize image to (width, height)
- `rotation` (int): Rotate image by degrees
- `flip` (str): Flip image ("horizontal", "vertical", or "both")
- `tint_color` (str): Apply color tint (hex color)
- `contrast` (float): Adjust contrast (1.0 = normal)
- `saturation` (float): Adjust saturation (1.0 = normal)
- `quality` (int): JPEG compression quality (1-100)

#### `embed_images_from_folder(input_folder, output_file, framework="tkinter", **kwargs)`
Process all images in a folder and generate an embedded Python module.

**Parameters:**
- `input_folder` (str): Path to folder containing images
- `output_file` (str): Output Python file path
- `framework` (str): Target GUI framework
- `quality` (int): Compression quality (1-100)
- Additional transformation parameters as above

### Sample Creation

#### `create_sample_images(output_dir="sample_images")`
Generate sample images for testing purposes.

## Development

### Setting up Development Environment

```bash
git clone https://github.com/stntg/img2res.git
cd img2res
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
python test_package.py
```

### Project Structure

```
img2res/
├── src/img2res/           # Main package
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Command line interface
│   ├── generator.py       # Image embedding generator
│   ├── image_loader.py    # Image loading utilities
│   └── sample_creator.py  # Sample image creation
├── examples/              # Usage examples
├── tests/                 # Test files
├── README.md             # This file
├── LICENSE               # License file
├── pyproject.toml        # Modern Python packaging
└── setup.py              # Legacy packaging support
```

## Requirements

- Python 3.7+
- Pillow (PIL)
- tkinter (usually included with Python)
- customtkinter (optional, for customtkinter support)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0.0
- Initial release
- Basic image embedding functionality
- Support for tkinter and customtkinter
- Image transformation features
- Command line interface
- Comprehensive examples

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/stntg/img2res/issues) on GitHub.

## Acknowledgments

- Built with [Pillow](https://pillow.readthedocs.io/) for image processing
- Supports [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for modern GUI development
- Inspired by the need for easy image embedding in Python GUI applications