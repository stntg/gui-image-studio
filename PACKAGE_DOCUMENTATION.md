# 📦 GUI Image Studio Package Documentation

## Overview

The **gui-image-studio** package is a comprehensive toolkit for creating, editing,
and embedding images in Python GUI applications. It provides both interactive tools
and programmatic APIs for seamless image integration.

## Package Structure

```
gui-image-studio/
├── src/
│   ├── gui_image_studio/          # Main package
│   │   ├── __init__.py           # Package initialization
│   │   ├── __main__.py           # Module entry point
│   │   ├── cli.py                # Command line interface
│   │   ├── image_studio.py       # GUI Image Studio application
│   │   ├── generator.py          # Image embedding utilities
│   │   ├── image_loader.py       # Image loading with transformations
│   │   ├── sample_creator.py     # Sample image creation
│   │   └── embedded_images.py    # Default embedded images
├── launch_designer.py            # Application launcher
├── tests/                        # Test directory
├── examples/                     # Usage examples
├── docs/                         # Documentation
├── USER_GUIDE.md                 # Complete user guide
├── IMAGE_USAGE_GUIDE.md          # Usage examples
├── QUICK_REFERENCE.md            # Quick reference card
└── PACKAGE_DOCUMENTATION.md     # This file
```

## Components

### 1. GUI Image Studio (`gui_image_studio.image_studio`)

The main interactive application for creating and editing images.

#### Key Classes:
- **`ImageDesignerGUI`**: Main application class
- **`NewImageDialog`**: Dialog for creating new images
- **`CodePreviewWindow`**: Code generation preview
- **`HelpWindow`**: Comprehensive help system

#### Features:
- 🎨 **Drawing Tools**: Brush, Pencil, Eraser, Shapes, Text, Fill
- 🖼️ **Image Management**: Create, load, edit, organize images
- 📱 **Live Preview**: Real-time preview in different contexts
- 💻 **Code Generation**: Automatic Python code generation
- 📚 **Help System**: Built-in guides and documentation
- ⌨️ **Keyboard Shortcuts**: Efficient workflow support

### 2. Image Generator (`gui_image_studio.generator`)

Utilities for converting images to embedded Python code.

#### Key Functions:
- **`embed_images_from_folder()`**: Convert folder of images to Python code

#### Features:
- 📁 **Batch Processing**: Convert multiple images at once
- 🗂️ **Theme Organization**: Automatic categorization by filename
- ⚙️ **Quality Control**: Adjustable compression settings
- 📝 **Code Generation**: Clean, readable Python output

### 3. Image Loader (`gui_image_studio.image_loader`)

Advanced image loading with transformations and framework support.

#### Key Functions:
- **`get_image()`**: Main function for loading images with transformations
- **`get_image_from_config()`**: Load image using configuration object

#### Key Classes:
- **`ImageConfig`**: Configuration dataclass for image processing parameters

#### Features:
- 🛠️ **Framework Support**: tkinter and customtkinter
- 🎨 **Image Transformations**: resize, rotate, tint, contrast, saturation
- 🎬 **Animated GIF Support**: Full animation processing
- 🎭 **Theme Support**: Light, dark, and custom themes
- 🔄 **Format Conversion**: Dynamic format handling
- 📏 **Size Management**: Automatic scaling and sizing

## Installation

### From Source
```bash
cd gui-image-studio
pip install -e .
```

### Dependencies
```bash
pip install pillow customtkinter
```

## Usage Examples

### 1. Interactive Image Creation

```bash
# Launch the GUI application
python launch_designer.py

# Or use the package
python -m gui_image_studio

# Or use the CLI command
gui-image-studio-designer
```

### 2. Programmatic Image Embedding

```python
from gui_image_studio.generator import embed_images_from_folder

# Convert folder of images to Python code
embed_images_from_folder(
    folder_path="my_images",
    output_file="embedded_images.py",
    compression_quality=85
)
```

### 3. Loading Images with Transformations

```python
# For tkinter applications
import gui_image_studio
import tkinter as tk

# Load image with transformations
root = tk.Tk()
photo = gui_image_studio.get_image(
    "my_image.png",
    framework="tkinter",
    size=(64, 64),
    theme="default",
    tint_color=(100, 150, 200),
    tint_intensity=0.3
)
label = tk.Label(root, image=photo)
label.pack()
```

```python
# For customtkinter applications
import gui_image_studio
import customtkinter as ctk

# Load image with transformations
root = ctk.CTk()
ctk_image = gui_image_studio.get_image(
    "my_image.png",
    framework="customtkinter",
    size=(32, 32),
    theme="dark",
    contrast=1.2,
    saturation=1.1
)
button = ctk.CTkButton(root, image=ctk_image, text="Button")
button.pack()
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

#### `embed_images_from_folder(folder_path, output_file="embedded_images.py", compression_quality=85)`

Process all images in a folder and generate an embedded Python module.

**Parameters:**

- `folder_path` (str): Path to folder containing images
- `output_file` (str): Output Python file path, default "embedded_images.py"
- `compression_quality` (int): JPEG/WebP compression quality (1-100), default 85

**Supported Formats:**
- PNG, JPG, JPEG, BMP, TIFF, GIF, WebP, ICO

#### `create_sample_images(output_dir="sample_images")`

Generate sample images for testing purposes.

## Command Line Interface

The package provides several CLI commands:

```bash
# Launch the GUI Image Studio
gui-image-studio-designer

# Create sample images for testing
gui-image-studio-create-samples

# Generate embedded images from a folder
gui-image-studio-generate --folder images/ --output embedded_images.py --quality 85
```

## Framework Integration

### Tkinter Integration
```python
import tkinter as tk
import gui_image_studio

root = tk.Tk()
photo = gui_image_studio.get_image(
    "icon.png",
    framework="tkinter",
    size=(32, 32),
    theme="default"
)
button = tk.Button(root, image=photo, text="My Button")
button.image = photo  # Keep reference
button.pack()
root.mainloop()
```

### CustomTkinter Integration
```python
import customtkinter as ctk
import gui_image_studio

ctk.set_appearance_mode("dark")
root = ctk.CTk()
ctk_image = gui_image_studio.get_image(
    "icon.png",
    framework="customtkinter",
    size=(32, 32),
    theme="dark"
)
button = ctk.CTkButton(root, image=ctk_image, text="My Button")
button.pack()
root.mainloop()
```

## Best Practices

### Image Creation
1. **Plan your design** before starting
2. **Use appropriate sizes** for your use case
3. **Test at actual size**, not zoomed in
4. **Use consistent styling** across your image set
5. **Save frequently** during creation

### Code Integration
1. **Generate code early** to test integration
2. **Use meaningful names** for images and themes
3. **Keep image references** to prevent garbage collection
4. **Test in target framework** before finalizing
5. **Document your image usage** patterns

### Performance Optimization
1. **Use appropriate quality settings** (70-85 recommended)
2. **Optimize image sizes** for purpose
3. **Group related images** by theme
4. **Test loading performance** in your application
5. **Consider lazy loading** for large image sets

## Troubleshooting

### Common Issues

#### Import Errors
```python
# Ensure proper installation
pip install pillow customtkinter

# Check Python path
import sys
sys.path.append('/path/to/gui-image-studio/src')
```

#### Image Display Issues
```python
# Keep image references in tkinter
button.image = photo  # Prevents garbage collection

# Use proper format for transparency
image.save('output.png', 'PNG')  # Not JPEG for transparency
```

#### Performance Issues
```python
# Optimize image sizes
if image.width > 512 or image.height > 512:
    image.thumbnail((512, 512), Image.Resampling.LANCZOS)

# Use appropriate quality
embed_images_from_folder(folder, output, quality=75)  # Not 100
```

## Requirements

- Python 3.8+
- Pillow (PIL) >= 8.0.0
- tkinter (usually included with Python)
- customtkinter >= 5.0.0 (optional, for customtkinter support)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

### Documentation
- **USER_GUIDE.md**: Complete user guide
- **IMAGE_USAGE_GUIDE.md**: Usage examples and patterns
- **QUICK_REFERENCE.md**: Quick reference card
- **Built-in Help**: Press F1 in the application

### Getting Help
1. Check the built-in help system (F1)
2. Review the documentation files
3. Check the troubleshooting section
4. Report issues with detailed information

---

**Version**: 1.0.0
**Last Updated**: 2024-12-19
**Maintainers**: GUI Image Studio development team
