# 📚 GUI Image Studio - Complete User Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Getting Started](#getting-started)
4. [Interface Overview](#interface-overview)
5. [Drawing Tools](#drawing-tools)
6. [Image Management](#image-management)
7. [Code Generation](#code-generation)
8. [Live Preview](#live-preview)
9. [Advanced Features](#advanced-features)
10. [Troubleshooting](#troubleshooting)
11. [Tips & Best Practices](#tips--best-practices)
12. [API Reference](#api-reference)

---

## Overview

The **GUI Image Studio** is a comprehensive toolkit for creating, editing, and embedding images in Python GUI applications. It consists of two main components:

- **🎨 Image Studio**: Interactive image editor with drawing tools
- **📦 gui-image-studio Package**: Command-line tools and utilities for image embedding

### Key Features
- ✨ **Visual Image Editor**: Create and edit images with professional tools
- 🖼️ **Multiple Frameworks**: Support for tkinter and customtkinter
- 📱 **Live Preview**: See how images will look in your applications
- 🔧 **Code Generation**: Automatic Python code generation with examples
- 🎯 **Usage-Specific**: Optimized for buttons, icons, sprites, backgrounds
- 📋 **Base64 Embedding**: No external files needed for distribution

---

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation
```bash
# Install from the package directory
cd gui-image-studio
pip install -e .

# Or install required dependencies manually
pip install pillow customtkinter
```

### Launching the Application
```bash
# Method 1: Direct launch
python launch_designer.py

# Method 2: Using the package
python -m gui_image_studio

# Method 3: Command line tool
gui-image-studio
```

---

## Getting Started

### First Launch
1. **Launch the application** using one of the methods above
2. **Create your first image** by clicking "🆕 Create Your First Image!"
3. **Choose image dimensions** (recommended: 32x32 for icons, 64x64 for buttons)
4. **Start drawing** with the brush tool
5. **Preview your work** in the live preview panel

### Quick Start Tutorial
1. **Create a Simple Icon**:
   - Click "🆕 Create Your First Image!"
   - Set size to 32x32 pixels
   - Select the **Pencil** tool
   - Enable **Grid** for pixel-perfect editing
   - Draw a simple icon
   - See it appear in the live preview

2. **Generate Code**:
   - Select framework: **tkinter** or **customtkinter**
   - Choose usage type: **icons**
   - Click "Preview Code" to see generated code
   - Copy the code to your project

---

## Interface Overview

### Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│ 🎨 GUI Image Studio                                    [_][□][×]│
├─────────────────┬───────────────────────┬───────────────────┤
│                 │                       │                   │
│   Image List    │     Canvas Area       │   Tools Panel     │
│                 │                       │                   │
│ • image1.png    │  ┌─────────────────┐  │ 🖌️ Brush          │
│ • icon.png      │  │                 │  │ ✏️ Pencil         │
│ • button.png    │  │   Your Image    │  │ 🧽 Eraser         │
│                 │  │                 │  │ ─ Line           │
│ [New Image]     │  │                 │  │ ▭ Rectangle      │
│ [Load Image]    │  └─────────────────┘  │ ○ Circle         │
│                 │                       │ T Text           │
│                 │  Zoom: [100%] [Grid]  │ 🪣 Fill          │
│                 │                       │                   │
├─────────────────┼───────────────────────┼───────────────────┤
│                 │                       │                   │
│  Properties     │    Live Preview       │  Code Generation  │
│                 │                       │                   │
│ Size: 32x32     │ ┌─────────────────┐   │ Framework: tkinter│
│ Format: PNG     │ │ Button Preview  │   │ Usage: buttons    │
│ Colors: RGBA    │ │ [Icon] Button1  │   │ Quality: 85       │
│                 │ │ [Icon] Button2  │   │                   │
│                 │ └─────────────────┘   │ [Preview Code]    │
│                 │                       │ [Generate File]   │
│                 │                       │ [Export Images]   │
└─────────────────┴───────────────────────┴───────────────────┘
```

### Panel Descriptions

#### **Left Panel - Image Management**
- **Image List**: Shows all created/loaded images
- **New Image**: Create a new blank image
- **Load Image**: Import existing image files
- **Properties**: Display current image information

#### **Center Panel - Canvas Area**
- **Main Canvas**: Where you draw and edit images
- **Zoom Controls**: Adjust magnification level
- **Grid Toggle**: Show/hide pixel grid for precision

#### **Right Panel - Tools & Generation**
- **Drawing Tools**: All available drawing instruments
- **Live Preview**: Real-time preview of your images in context
- **Code Generation**: Framework selection and code export

---

## Drawing Tools

### 🖌️ **Brush Tool**
- **Purpose**: Freehand drawing with smooth strokes
- **Best for**: Artistic drawing, organic shapes, sketching
- **Controls**:
  - Left-click and drag to draw
  - Brush size adjustable in tool options
  - Color picker for custom colors
- **Tips**: Use for general drawing and filling large areas

### ✏️ **Pencil Tool**
- **Purpose**: Pixel-perfect editing
- **Best for**: Pixel art, precise editing, detailed work
- **Controls**:
  - Left-click to place single pixels
  - Drag for precise lines
  - Works best with Grid enabled
- **Tips**: Zoom in 4x or more for pixel art work

### 🧽 **Eraser Tool**
- **Purpose**: Remove pixels or make areas transparent
- **Best for**: Corrections, creating transparency
- **Controls**:
  - Left-click and drag to erase
  - Size adjustable like brush
- **Tips**: Creates true transparency in PNG format

### ─ **Line Tool**
- **Purpose**: Draw straight lines
- **Best for**: Geometric shapes, borders, technical drawings
- **Controls**:
  - Click and drag from start to end point
  - Hold Shift for horizontal/vertical lines
- **Tips**: Perfect for creating clean geometric designs

### ▭ **Rectangle Tool**
- **Purpose**: Draw rectangular shapes
- **Best for**: Buttons, frames, UI elements
- **Controls**:
  - Click and drag to define rectangle
  - Hold Shift for perfect squares
- **Options**: Filled or outline only

### ○ **Circle Tool**
- **Purpose**: Draw circular shapes
- **Best for**: Icons, decorative elements, buttons
- **Controls**:
  - Click and drag to define circle
  - Hold Shift for perfect circles
- **Options**: Filled or outline only

### T **Text Tool**
- **Purpose**: Add text to images
- **Best for**: Labels, icons with text, UI elements
- **Controls**:
  - Click where you want text
  - Type your text in the dialog
  - Choose font size and style
- **Tips**: Text scales with zoom level for better visibility

### 🪣 **Fill Tool**
- **Purpose**: Flood fill connected areas
- **Best for**: Filling large areas, coloring regions
- **Controls**:
  - Click on area to fill
  - Fills all connected pixels of same color
- **Tips**: Works great for coloring outlined shapes

---

## Image Management

### Creating New Images

#### **Standard Sizes**
- **Icons**: 16x16, 24x24, 32x32, 48x48
- **Buttons**: 64x64, 80x40, 100x30
- **Sprites**: 32x32, 64x64, 128x128
- **Custom**: Any size up to 1024x1024

#### **Format Options**
- **PNG**: Best for icons, transparency support
- **JPEG**: Good for photos, smaller file size
- **BMP**: Uncompressed, largest file size

### Loading Existing Images
1. Click "📁 Load Image" or "📁 Or Load an Existing Image"
2. Select image file (PNG, JPG, BMP, GIF, TIFF, WebP)
3. Image appears in the list and canvas
4. Edit as needed with drawing tools

### Image Operations
- **Duplicate**: Right-click image in list → Duplicate
- **Rename**: Right-click image in list → Rename
- **Delete**: Right-click image in list → Delete
- **Export**: Right-click image in list → Export

---

## Code Generation

### Framework Selection

#### **Tkinter (Standard Python GUI)**
```python
# Generated code example
import tkinter as tk
from PIL import Image, ImageTk
import base64
from io import BytesIO

def create_photo_image(base64_string):
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))
    return ImageTk.PhotoImage(pil_image)

# Usage
root = tk.Tk()
photo = create_photo_image(embedded_images['default']['icon.png'])
button = tk.Button(root, image=photo, text="My Button")
button.pack()
```

#### **CustomTkinter (Modern Python GUI)**
```python
# Generated code example
import customtkinter as ctk
from PIL import Image
import base64
from io import BytesIO

def create_ctk_image(base64_string, size=None):
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))
    if size:
        return ctk.CTkImage(light_image=pil_image, size=size)
    return ctk.CTkImage(light_image=pil_image)

# Usage
ctk.set_appearance_mode("dark")
root = ctk.CTk()
ctk_image = create_ctk_image(embedded_images['default']['icon.png'], size=(32, 32))
button = ctk.CTkButton(root, image=ctk_image, text="My Button")
button.pack()
```

### Usage Types

#### **General Purpose**
- Basic image loading and display
- Flexible for any use case
- Standard helper functions included

#### **Buttons**
- Specialized button creation functions
- Text + image combinations
- Hover effects support

#### **Icons**
- Small, scalable graphics
- System integration ready
- Consistent sizing helpers

#### **Backgrounds**
- Full-screen background support
- Tiled pattern functions
- Responsive scaling

#### **Sprites**
- Game object graphics
- Animation frame support
- Performance optimized

#### **UI Elements**
- Custom control creation
- Themed interface support
- Professional appearance

### Quality Settings
- **1-30**: High compression, smaller files, lower quality
- **31-70**: Balanced compression and quality
- **71-85**: Good quality, reasonable file size (recommended)
- **86-100**: Highest quality, larger files

---

## Live Preview

### Preview Modes

The live preview automatically updates to show how your images will appear in the selected framework and usage type.

#### **Button Preview**
```
┌─────────────────────────────────────┐
│ Tkinter Buttons:                    │
│                                     │
│ ┌──────────────┐ ┌──────────────┐   │
│ │ [🔧] Settings│ │ [💾] Save    │   │
│ └──────────────┘ └──────────────┘   │
│                                     │
│ ┌──────────────┐ ┌──────────────┐   │
│ │ [📁] Open    │ │ [❌] Close   │   │
│ └──────────────┘ └──────────────┘   │
└─────────────────────────────────────┘
```

#### **Icon Preview**
```
┌─────────────────────────────────────┐
│ Tkinter Icons:                      │
│                                     │
│  🔧      💾      📁      ❌         │
│Settings  Save    Open   Close       │
│                                     │
│  🏠      ⚙️      📊      🔍         │
│ Home   Config  Chart  Search       │
└─────────────────────────────────────┘
```

#### **Sprite Preview**
```
┌─────────────────────────────────────┐
│ Tkinter Sprites:                    │
│ ┌─────────────────────────────────┐ │
│ │ 🌤️ Sky Background              │ │
│ │                                 │ │
│ │     🏃 🐕 🌳 🏠               │ │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ │
│ │ Ground                          │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Preview Features
- **Real-time Updates**: Changes as you draw
- **Framework-Specific**: Adapts to selected framework
- **Usage-Aware**: Different layouts for different purposes
- **Responsive**: Scales to preview panel size

---

## Advanced Features

### Pixel Art Mode
1. Select the **Pencil** tool
2. Enable **Grid** display
3. Zoom to **400%** or higher
4. Each grid square represents one pixel
5. Perfect for creating retro-style graphics

### Multi-Theme Support
Organize images by themes using filename prefixes:
- `dark_icon.png` → Theme: "dark", Name: "icon.png"
- `light_button.png` → Theme: "light", Name: "button.png"
- `game_sprite.png` → Theme: "game", Name: "sprite.png"

### Batch Operations
- **Export All**: Export all images at once
- **Theme Export**: Export specific themes
- **Format Conversion**: Convert between formats

### Keyboard Shortcuts
- **Ctrl+N**: New image
- **Ctrl+O**: Open image
- **Ctrl+S**: Save current image
- **Ctrl+Z**: Undo (when available)
- **Ctrl+Y**: Redo (when available)
- **Space**: Pan canvas (when zoomed)
- **+/-**: Zoom in/out

---

## Troubleshooting

### Common Issues

#### **Application Won't Start**
```bash
# Check Python version
python --version  # Should be 3.7+

# Install dependencies
pip install pillow customtkinter

# Try launching directly
python src/gui_image_studio/image_studio.py
```

#### **Images Not Displaying**
- Check image format is supported (PNG, JPG, BMP, GIF, TIFF, WebP)
- Verify image isn't corrupted
- Try creating a new image instead

#### **Code Generation Fails**
- Ensure you have created at least one image
- Check that framework is properly selected
- Verify output directory is writable

#### **Preview Not Updating**
- Try changing framework/usage type to refresh
- Restart the application if preview is stuck
- Check that images are properly loaded

### Performance Issues

#### **Slow Drawing**
- Reduce zoom level if very high
- Close other applications to free memory
- Use smaller image sizes for better performance

#### **Large File Sizes**
- Reduce quality setting (try 70-85)
- Use PNG for images with transparency
- Use JPEG for photographic content

### Error Messages

#### **"Canvas not ready"**
- Wait a moment and try again
- Resize the window to refresh canvas
- Restart application if persistent

#### **"Failed to generate code"**
- Check that output directory exists and is writable
- Ensure at least one image is created
- Try a different output location

---

## Tips & Best Practices

### Design Guidelines

#### **For Icons (16x16 to 48x48)**
- Keep designs simple and recognizable
- Use high contrast colors
- Avoid fine details that won't be visible
- Test at actual size, not zoomed in

#### **For Buttons (64x64 and larger)**
- Leave space for text if combining with labels
- Use consistent styling across button set
- Consider hover/pressed states
- Make clickable area clear

#### **For Sprites (Game Graphics)**
- Use consistent pixel sizes across sprites
- Consider animation frames
- Optimize color palette for performance
- Test in actual game context

### Workflow Tips

#### **Efficient Image Creation**
1. **Plan your design** before starting
2. **Start with basic shapes** using shape tools
3. **Add details** with pencil tool
4. **Use fill tool** for large areas
5. **Preview frequently** to check appearance

#### **Code Integration**
1. **Generate code early** to test integration
2. **Use consistent naming** for easy organization
3. **Test in target framework** before finalizing
4. **Keep backups** of your image files

#### **Performance Optimization**
- **Use appropriate image sizes** for purpose
- **Optimize quality settings** for file size
- **Group related images** by theme
- **Test loading performance** in your application

### Color Guidelines

#### **For UI Elements**
- Use your application's color scheme
- Ensure sufficient contrast for accessibility
- Consider dark/light theme variations
- Test with colorblind-friendly palettes

#### **For Icons**
- Use standard icon colors when possible
- Maintain consistency across icon sets
- Consider platform conventions
- Test visibility on different backgrounds

---

## API Reference

### Command Line Tools

#### **gui-image-studio**
Launch the GUI Image Studio
```bash
gui-image-studio [options]
```

#### **gui-image-studio-generate**
Generate embedded images from folder
```bash
gui-image-studio-generate --folder images --output embedded.py --quality 85
```

### Python API

#### **Loading Images**
```python
from gui_image_studio import load_image_from_base64, create_photo_image

# Load PIL Image
pil_image = load_image_from_base64(base64_string)

# Create tkinter PhotoImage
photo = create_photo_image(base64_string)
```

#### **CustomTkinter Integration**
```python
import customtkinter as ctk
from gui_image_studio import create_ctk_image

# Create CTkImage
ctk_image = create_ctk_image(base64_string, size=(32, 32))

# Use in button
button = ctk.CTkButton(parent, image=ctk_image, text="Button")
```

#### **Image Processing**
```python
from gui_image_studio.generator import embed_images_from_folder

# Generate embedded images
embed_images_from_folder(
    folder_path="my_images",
    output_file="embedded.py",
    compression_quality=85
)
```

### Configuration Options

#### **Image Studio Settings**
```python
# Default settings (can be customized)
DEFAULT_IMAGE_SIZE = (64, 64)
DEFAULT_BACKGROUND_COLOR = (255, 255, 255, 0)  # Transparent
DEFAULT_BRUSH_SIZE = 3
DEFAULT_ZOOM_LEVEL = 1.0
GRID_ENABLED = False
AUTO_ZOOM_THRESHOLD = 400  # Auto-zoom for images smaller than 400px
```

#### **Code Generation Settings**
```python
# Framework options
SUPPORTED_FRAMEWORKS = ["tkinter", "customtkinter"]

# Usage types
USAGE_TYPES = ["general", "buttons", "icons", "backgrounds", "sprites", "ui_elements"]

# Quality range
QUALITY_RANGE = (1, 100)
DEFAULT_QUALITY = 85
```

---

## Support & Resources

### Getting Help
- **Built-in Help**: Press F1 or use Help menu in the application
- **Documentation**: Check the USER_GUIDE.md file
- **Examples**: See IMAGE_USAGE_GUIDE.md for usage examples

### Contributing
- Report bugs and request features
- Submit pull requests for improvements
- Share your created images and examples

### License
This project is open source. Check the LICENSE file for details.

---

**Happy Creating! 🎨**

*The GUI Image Studio team hopes this tool helps you create amazing graphics for your Python applications!*