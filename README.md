# GUI Image Studio

[![PyPI version](https://img.shields.io/pypi/v/gui-image-studio.svg)](https://pypi.org/project/gui-image-studio/)
[![Python versions](https://img.shields.io/pypi/pyversions/gui-image-studio.svg)](https://pypi.org/project/gui-image-studio/)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://stntg.github.io/gui-image-studio/)
[![CI Status](https://github.com/stntg/gui-image-studio/workflows/CI/badge.svg)](https://github.com/stntg/gui-image-studio/actions)
[![Documentation Build](https://github.com/stntg/gui-image-studio/workflows/Documentation/badge.svg)](https://github.com/stntg/gui-image-studio/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CodeFactor](https://www.codefactor.io/repository/github/stntg/gui-image-studio/badge)](https://www.codefactor.io/repository/github/stntg/gui-image-studio)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python toolkit for creating, embedding, and managing images in
Python GUI applications with support for tkinter and customtkinter.

## 📚 Documentation

**[📖 Full Documentation](https://stntg.github.io/gui-image-studio/)** -
Complete guides, API reference, and examples

Quick links:

- [🚀 Quick Start Guide](https://stntg.github.io/gui-image-studio/quickstart.html)
- [📖 API Reference](https://stntg.github.io/gui-image-studio/api/)
- [💡 Examples](https://stntg.github.io/gui-image-studio/examples/)
- [🛠️ Installation Guide](https://stntg.github.io/gui-image-studio/installation.html)
- [🗺️ Development Roadmap](DEVELOPMENT_ROADMAP.md) - Future features and
  development plans

## Features

- 🎨 **Visual Image Studio GUI** - Create and edit images with drawing tools
- 🖼️ Convert images to base64 encoded strings
- 📁 Batch process entire folders of images
- 🎨 Support for multiple GUI frameworks (tkinter, customtkinter)
- 🔧 Image transformations (resize, rotate, flip, tint, contrast, saturation)
- 📦 Generate embedded Python modules for easy distribution
- 🎬 Animated GIF support
- 🎯 High-quality compression options
- 📝 Sample image generation for testing
- 👁️ Real-time code preview and generation
- 🔍 **Comprehensive Image Information** - Detailed image analysis with smart
  recommendations
- 🌟 **Advanced Transparency Features** - Preserve existing transparency when
  making areas transparent

## Installation

### From PyPI (when published)

```bash
pip install gui-image-studio
```

### From Source

```bash
git clone https://github.com/stntg/gui-image-studio.git
cd gui-image-studio
pip install -e .
```

## Quick Start

### Image Studio GUI

Launch the visual image studio to create images with drawing tools:

```bash
# For PyPI installations (recommended)
gui-image-studio-designer

# For development/contributors (GitHub repo only)
python launch_designer.py
```

The Image Studio GUI provides:

- Drawing tools (brush, eraser, shapes, text)
- Image transformations and filters
- Multiple image management
- Real-time preview
- Code generation with preview
- Export capabilities

### Basic Usage

```python
from gui_image_studio import get_image, embed_images_from_folder

# Get a single image with transformations
image = get_image(
    "my_image.png",
    framework="tkinter",
    size=(64, 64),
    theme="default"
)

# Embed all images from a folder
embed_images_from_folder(
    folder_path="images/",
    output_file="embedded_images.py",
    compression_quality=85
)
```

### Using Embedded Images

```python
# After embedding images, use them in your GUI
import gui_image_studio
import tkinter as tk

root = tk.Tk()

# Load embedded image with transformations
photo = gui_image_studio.get_image(
    "my_image.png",
    framework="tkinter",
    size=(100, 100),
    theme="default"
)
label = tk.Label(root, image=photo)
label.pack()

root.mainloop()
```

### Command Line Interface

```bash
# Or use the dedicated command
gui-image-studio-designer

# Create sample images for testing
gui-image-studio-create-samples

# Embed images from a folder
gui-image-studio-generate \
  --folder images/ \
  --output embedded_images.py \
  --quality 85
```

## Advanced Features

### Image Transformations

```python
from gui_image_studio import get_image

# Apply transformations
image = get_image(
    "photo.jpg",
    framework="customtkinter",
    size=(200, 200),
    rotate=45,
    tint_color=(255, 0, 0),
    tint_intensity=0.3,
    contrast=1.2,
    saturation=1.5,
    grayscale=False,
    transparency=1.0
)
```

### Animated GIFs

```python
from gui_image_studio import get_image

# Load animated GIF
animation_data = get_image(
    "animation.gif",
    framework="customtkinter",
    size=(100, 100),
    animated=True,
    frame_delay=100
)

# Use the frames in your application
frames = animation_data["animated_frames"]
delay = animation_data["frame_delay"]
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
- `06_image_designer_gui.py` - Launch the Image Studio GUI
- `07_using_designed_images.py` - Use images created with the designer

Run all examples:

```bash
python examples/run_examples.py
```

## API Reference

### Core Functions

#### `get_image(image_name, framework="tkinter", **kwargs)`

Load and return an image object for the specified GUI framework.

**Parameters:**

- `image_name` (str): Name of the embedded image (e.g., 'icon.png')
- `framework` (str): GUI framework ("tkinter" or "customtkinter")
- `size` (tuple): Resize image to (width, height), default (32, 32)
- `theme` (str): Theme name ("default", "dark", "light"), default "default"
- `rotate` (int): Rotate image by degrees, default 0
- `grayscale` (bool): Convert to grayscale, default False
- `tint_color` (tuple): Apply color tint as (R, G, B), default None
- `tint_intensity` (float): Tint blending factor (0.0-1.0), default 0.0
- `contrast` (float): Adjust contrast (1.0 = normal), default 1.0
- `saturation` (float): Adjust saturation (1.0 = normal), default 1.0
- `transparency` (float): Adjust transparency (0.0-1.0), default 1.0
- `animated` (bool): Process animated GIFs, default False
- `frame_delay` (int): Animation frame delay in ms, default 100
- `format_override` (str): Convert to format ("PNG", "JPEG", etc.), default None

#### embed_images_from_folder

```python
embed_images_from_folder(
    folder_path,
    output_file="embedded_images.py",
    compression_quality=85
)
```

Process all images in a folder and generate an embedded Python module.

**Parameters:**

- `folder_path` (str): Path to folder containing images
- `output_file` (str): Output Python file path, default "embedded_images.py"
- `compression_quality` (int): JPEG/WebP compression quality (1-100),
  default 85

**Supported Formats:**

- PNG, JPG, JPEG, BMP, TIFF, GIF, WebP, ICO

### Sample Creation

#### `create_sample_images(output_dir="sample_images")`

Generate sample images for testing purposes.

## Development

### Setting up Development Environment

```bash
git clone https://github.com/stntg/gui-image-studio.git
cd gui-image-studio
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
python test_package.py
```

### Project Structure

```text
gui-image-studio/
├── src/gui_image_studio/     # Main package
│   ├── __init__.py           # Package initialization
│   ├── __main__.py           # Module entry point
│   ├── cli.py                # Command line interface
│   ├── generator.py          # Image embedding generator
│   ├── image_loader.py       # Image loading utilities
│   ├── image_studio.py       # GUI Image Studio application
│   ├── sample_creator.py     # Sample image creation
│   ├── embedded_images.py    # Default embedded images
│   ├── embedded_icons.py     # Embedded UI icons
│   ├── py.typed              # Type hints marker
│   └── image_studio/         # Modular Image Studio components
│       ├── main_app.py       # Main application entry
│       ├── core/             # Core functionality modules
│       ├── ui/               # User interface components
│       ├── toolkit/          # Drawing tools and icons
│       └── utils/            # Utility functions
├── examples/                 # Usage examples and demos
├── tests/                    # Test files and test data
├── docs/                     # Sphinx documentation
├── scripts/                  # Development and build scripts
├── README.md                 # This file
├── LICENSE                   # License file
├── DEVELOPMENT_ROADMAP.md    # Development roadmap
├── pyproject.toml            # Modern Python packaging
├── setup.py                  # Legacy packaging support
├── tox.ini                   # Testing configuration
└── launch_designer.py        # Development launcher script (GitHub repo only)
```

## Requirements

- Python 3.8+
- Pillow (PIL) >= 8.0.0
- tkinter (usually included with Python)
- customtkinter >= 5.0.0 (optional, for customtkinter support)
- threepanewindows (for advanced window management)

## Contributing

We welcome contributions! Please see our [Development Roadmap](DEVELOPMENT_ROADMAP.md)
for planned features and development priorities.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major features, please check the roadmap and consider opening an issue
for discussion first.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE)
file for details.

## Changelog

### Version 1.1.0

- **Info Button Feature**: Added comprehensive image information display with
  detailed analysis
  - Shows file properties, metadata, and technical specifications
  - Displays color analysis with unique colors count and distribution
  - Provides memory usage estimates and smart recommendations
  - Features professional icon-based UI with fallback support
  - Located in Image Properties section next to Apply button
- **Transparency Preservation**: Enhanced transparency preservation in image
  processing
  - Existing transparent areas are now preserved when making additional areas
    transparent
  - Semi-transparent pixels maintain their exact alpha values
  - Only processes non-transparent pixels that match the selected color
  - Enhanced user feedback shows existing vs. newly transparent pixel counts
- **Technical Improvements**: Better path resolution for icon loading and
  enhanced error handling

### Version 1.0.1

- **Security Fixes**: Fixed partial executable path vulnerability in Windows
  print function
- **Documentation Updates**: Complete documentation overhaul with updated API
  references
- **Bug Fixes**: Fixed Python code block syntax errors and GitHub Actions
  workflow issues
- **Transparency Features**: Enhanced transparency preservation in image
  processing
- **Info Button**: Added comprehensive image information display with detailed
  analysis

### Version 1.0.0

- Initial release of gui-image-studio package
- **GUI Image Studio**: Visual image editor with drawing tools
- Core image embedding functionality with `embed_images_from_folder()`
- Advanced image loading with `get_image()` function
- Support for tkinter and customtkinter frameworks
- Image transformation features (resize, rotate, tint, contrast,
  saturation)
- Theme support (default, dark, light)
- Animated GIF support with frame processing
- Command line interface with console scripts
- Sample image generation for testing
- High-quality compression options
- Comprehensive example collection

## Support

If you encounter any issues or have questions, please
[open an issue](https://github.com/stntg/gui-image-studio/issues) on GitHub.

## Acknowledgments

- Built with [Pillow](https://pillow.readthedocs.io/) for image processing
- Supports [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
  for modern GUI development
- Inspired by the need for easy image embedding in Python GUI
  applications
