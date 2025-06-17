# 📦 GUI Image Studio Package Documentation

## Overview

The **gui-image-studio** package is a comprehensive toolkit for creating, editing, and embedding images in Python GUI applications. It provides both interactive tools and programmatic APIs for seamless image integration.

## Package Structure

```
gui-image-studio/
├── src/
│   ├── gui_image_studio/          # Main GUI application
│   │   ├── __init__.py           # Package initialization
│   │   ├── image_studio.py       # Main GUI application
│   │   ├── generator.py          # Image embedding utilities
│   │   └── image_loader.py       # Image loading helpers
│   └── image_loader.py           # Standalone image loader
├── launch_designer.py            # Application launcher
├── test_image_studio_fixes.py    # Main test suite
├── test_help_system.py           # Help system tests
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
- **`generate_embedded_images()`**: Command-line interface

#### Features:
- 📁 **Batch Processing**: Convert multiple images at once
- 🗂️ **Theme Organization**: Automatic categorization by filename
- ⚙️ **Quality Control**: Adjustable compression settings
- 📝 **Code Generation**: Clean, readable Python output

### 3. Image Loader (`gui_image_studio.image_loader`)

Helper functions for loading embedded images in applications.

#### Key Functions:
- **`load_image_from_base64()`**: Convert base64 to PIL Image
- **`create_photo_image()`**: Create tkinter PhotoImage
- **`create_ctk_image()`**: Create CustomTkinter CTkImage
- **`get_available_frameworks()`**: Check framework availability

#### Features:
- 🛠️ **Framework Support**: tkinter and customtkinter
- 🔄 **Format Conversion**: Seamless format handling
- 📏 **Size Management**: Automatic scaling and sizing
- 🎨 **Theme Support**: Light/dark theme compatibility

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

# Or use the command
gui-image-studio
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

### 3. Loading Embedded Images

```python
# For tkinter applications
from gui_image_studio import load_image_from_base64, create_photo_image
import tkinter as tk

# Load image
pil_image = load_image_from_base64(embedded_images['theme']['image.png'])
photo = create_photo_image(embedded_images['theme']['image.png'])

# Use in tkinter
root = tk.Tk()
label = tk.Label(root, image=photo)
label.pack()
```

```python
# For customtkinter applications
from gui_image_studio import create_ctk_image
import customtkinter as ctk

# Create CTkImage
ctk_image = create_ctk_image(embedded_images['theme']['image.png'], size=(32, 32))

# Use in customtkinter
root = ctk.CTk()
button = ctk.CTkButton(root, image=ctk_image, text="Button")
button.pack()
```

## API Reference

### ImageDesignerGUI Class

#### Constructor
```python
ImageDesignerGUI()
```
Creates the main application instance.

#### Key Methods
- **`run()`**: Start the application
- **`new_image()`**: Create new image dialog
- **`load_image()`**: Load existing image
- **`select_tool(tool_name)`**: Change drawing tool
- **`update_preview()`**: Refresh live preview
- **`preview_code()`**: Show code generation preview
- **`export_images()`**: Export images to files

#### Drawing Tools
- **`select_tool("brush")`**: Freehand drawing
- **`select_tool("pencil")`**: Pixel-perfect editing
- **`select_tool("eraser")`**: Remove pixels
- **`select_tool("line")`**: Straight lines
- **`select_tool("rectangle")`**: Rectangular shapes
- **`select_tool("circle")`**: Circular shapes
- **`select_tool("text")`**: Text labels
- **`select_tool("fill")`**: Flood fill

### Generator Functions

#### embed_images_from_folder()
```python
embed_images_from_folder(
    folder_path: str,
    output_file: str = "embedded_images.py",
    compression_quality: int = 85
) -> None
```

**Parameters:**
- `folder_path`: Directory containing images
- `output_file`: Output Python file name
- `compression_quality`: JPEG/WebP quality (1-100)

**Supported Formats:**
- PNG, JPG, JPEG, BMP, TIFF, GIF, WebP

#### generate_embedded_images()
```python
generate_embedded_images() -> None
```
Command-line interface for image embedding.

**Usage:**
```bash
gui-image-studio-generate --folder images --output embedded.py --quality 85
```

### Image Loader Functions

#### load_image_from_base64()
```python
load_image_from_base64(base64_string: str) -> Image.Image
```
Convert base64 string to PIL Image.

#### create_photo_image()
```python
create_photo_image(base64_string: str) -> ImageTk.PhotoImage
```
Create tkinter PhotoImage from base64.

#### create_ctk_image()
```python
create_ctk_image(
    base64_string: str,
    size: tuple = None
) -> ctk.CTkImage
```
Create CustomTkinter CTkImage from base64.

## Configuration

### Default Settings
```python
# Image creation defaults
DEFAULT_IMAGE_SIZE = (64, 64)
DEFAULT_BACKGROUND_COLOR = (255, 255, 255, 0)  # Transparent
DEFAULT_BRUSH_SIZE = 3
DEFAULT_ZOOM_LEVEL = 1.0

# Code generation defaults
DEFAULT_FRAMEWORK = "tkinter"
DEFAULT_USAGE_TYPE = "general"
DEFAULT_QUALITY = 85

# UI defaults
GRID_ENABLED = False
AUTO_ZOOM_THRESHOLD = 400
```

### Customization
Settings can be modified by editing the source files or through the GUI interface.

## Framework Integration

### Tkinter Integration
```python
import tkinter as tk
from tkinter import ttk
from gui_image_studio import create_photo_image

class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
    
    def setup_ui(self):
        # Load embedded images
        icon = create_photo_image(embedded_images['icons']['settings.png'])
        
        # Create UI elements
        button = tk.Button(self.root, image=icon, text="Settings")
        button.image = icon  # Keep reference
        button.pack()
```

### CustomTkinter Integration
```python
import customtkinter as ctk
from gui_image_studio import create_ctk_image

class MyModernApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.setup_ui()
    
    def setup_ui(self):
        # Load embedded images
        icon = create_ctk_image(embedded_images['icons']['settings.png'], size=(24, 24))
        
        # Create modern UI elements
        button = ctk.CTkButton(self.root, image=icon, text="Settings")
        button.pack()
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

## Testing

### Running Tests
```bash
# Test main functionality
python test_image_studio_fixes.py

# Test help system
python test_help_system.py

# Test specific features
python -c "from gui_image_studio import ImageDesignerGUI; app = ImageDesignerGUI()"
```

### Test Coverage
- ✅ Image creation and editing
- ✅ Drawing tools functionality
- ✅ Code generation
- ✅ Framework integration
- ✅ Help system
- ✅ Live preview
- ✅ Import/export operations

## Contributing

### Development Setup
```bash
git clone <repository>
cd gui-image-studio
pip install -e .
pip install -r requirements-dev.txt  # If available
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document all public functions
- Include docstrings for classes and methods

### Testing
- Add tests for new features
- Ensure existing tests pass
- Test on multiple Python versions
- Test with different image formats

## License

This project is open source. See LICENSE file for details.

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
**Last Updated**: 2024  
**Maintainers**: GUI Image Studio development team