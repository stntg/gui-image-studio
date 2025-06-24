# GUI Image Studio - Image Studio GUI

The Image Studio GUI is a comprehensive visual tool for developers to create,
edit, and design images/icons that can then be embedded into Python GUI
applications.

## Features

### Visual Design Tools

- **Drawing Tools**: Brush, eraser, line, rectangle, circle, text, and fill tools
- **Customizable Properties**: Adjustable brush size, color picker, and
  tool-specific settings
- **Real-time Canvas**: Interactive drawing canvas with zoom controls
- **Multiple Images**: Manage multiple images in a single project

### Image Management

- **Create New Images**: Start with blank canvases of custom sizes
- **Load Existing Images**: Import images from files (PNG, JPG, GIF, etc.)
- **Duplicate Images**: Copy existing images for variations
- **Rename Images**: Custom naming for organized projects
- **Delete Images**: Remove unwanted images from projects

### Image Transformations

- **Resize**: Change image dimensions
- **Rotate**: Rotate images by any angle
- **Filters**: Apply blur, sharpen, and emboss effects
- **Real-time Preview**: See changes immediately

### Code Generation

- **Framework Support**: Generate code for tkinter or customtkinter
- **Quality Control**: Adjustable compression quality (1-100)
- **Code Preview**: Preview generated code before saving
- **File Export**: Save embedded Python modules
- **Image Export**: Export images as individual files

## Getting Started

### Launch Methods

1. **Using the launcher script**:
   ```bash
   python launch_designer.py
   ```

2. **Using the package module**:
   ```bash
   python -m gui_image_studio
   ```

3. **Using the CLI command** (after installation):
   ```bash
   gui-image-studio-designer
   ```

4. **Using the package function**:
   ```python
   import gui_image_studio
   gui_image_studio.launch_designer()
   ```

### Interface Overview

The Image Studio GUI is divided into three main panels:

#### Left Panel - Tools & Image Management

- **Design Tools**: Select drawing tools (brush, eraser, shapes, etc.)
- **Tool Properties**: Adjust size, color, and other tool settings
- **Image List**: View and manage all images in your project
- **Management Buttons**: Create, load, duplicate, and delete images

#### Center Panel - Drawing Canvas

- **Interactive Canvas**: Main drawing area with zoom and scroll support
- **Zoom Controls**: Zoom in, zoom out, and fit-to-window options
- **Real-time Updates**: See your changes as you draw

#### Right Panel - Properties & Code Generation

- **Image Properties**: Name, size, and transformation settings
- **Transformations**: Rotation, filters, and effects
- **Code Generation**: Framework selection, quality settings, and export options

## Workflow

### 1. Creating Images

1. **Start a New Image**:
   - Click "New Image" in the left panel
   - Set desired width and height
   - Choose a name for your image
   - Click "Create"

2. **Load Existing Image**:
   - Click "Load Image" in the left panel
   - Select an image file from your computer
   - The image will be added to your project

### 2. Designing Images

1. **Select a Tool**:
   - Choose from brush, eraser, line, rectangle, circle, text, or fill
   - Adjust tool properties (size, color) as needed

2. **Draw on Canvas**:
   - Click and drag on the canvas to draw
   - Use zoom controls for detailed work
   - Switch between tools as needed

3. **Apply Transformations**:
   - Resize images using the width/height controls
   - Rotate images using the rotation slider
   - Apply filters (blur, sharpen, emboss) with the filter buttons

### 3. Managing Multiple Images

1. **Switch Between Images**:
   - Click on image names in the left panel list
   - Each image maintains its own state and properties

2. **Organize Images**:
   - Rename images by editing the name field in the right panel
   - Duplicate images for variations
   - Delete unwanted images

### 4. Generating Code

1. **Preview Code**:
   - Click "Preview Code" to see the generated embedded code
   - Review the code structure and content
   - Copy code to clipboard if needed

2. **Generate File**:
   - Click "Generate File" to save the embedded code as a Python file
   - Choose location and filename
   - The file will contain all your images as base64-encoded data

3. **Export Images**:
   - Click "Export Images" to save individual image files
   - Choose destination folder
   - Images will be saved as PNG files

## Using Generated Code

After generating embedded code, you can use it in your GUI applications:

```python
# Import your generated embedded images
from my_embedded_images import get_image

import tkinter as tk

# Create your GUI
root = tk.Tk()

# Load and use your designed images
my_icon = get_image("my_icon")
button = tk.Button(root, image=my_icon, text="My Button")
button.pack()

root.mainloop()
```

## Keyboard Shortcuts

- **Ctrl+N**: Create new image
- **Ctrl+O**: Load image from file
- **Ctrl+S**: Export images to files
- **Delete**: Delete selected image

## Tips and Best Practices

### Design Tips

1. **Start with the Right Size**: Consider your final use case when setting image dimensions
2. **Use Appropriate Colors**: Consider your GUI theme and color scheme
3. **Test Different Sizes**: Create variations for different UI contexts
4. **Keep It Simple**: Simple, clear designs work best for icons and UI elements

### Performance Tips

1. **Optimize Image Sizes**: Larger images result in larger embedded files
2. **Adjust Quality**: Balance file size vs. image quality using the quality slider
3. **Use Appropriate Formats**: The tool automatically optimizes format selection
4. **Group Related Images**: Keep related images in the same project for organization

### Code Generation Tips

1. **Choose the Right Framework**: Select tkinter or customtkinter based on your project
2. **Preview Before Generating**: Always preview code to ensure it meets your needs
3. **Use Descriptive Names**: Give your images meaningful names for easier code maintenance
4. **Test Generated Code**: Verify the generated code works in your target application

## Troubleshooting

### Common Issues

1. **GUI Won't Launch**:
   - Ensure tkinter is available (usually built-in with Python)
   - Check that Pillow is installed: `pip install Pillow`

2. **Images Not Displaying**:
   - Verify image files are valid and supported formats
   - Check file permissions and paths

3. **Code Generation Fails**:
   - Ensure you have write permissions to the output directory
   - Check that image names are valid Python identifiers

4. **Performance Issues**:
   - Reduce image sizes for better performance
   - Close unused images to free memory
   - Restart the application if it becomes sluggish

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Try with smaller, simpler images first
4. Restart the application
5. Report bugs on the project's GitHub repository

## Advanced Features

### Custom Themes

The generated code supports theme-based image organization. Images can be categorized by theme for different UI modes (light, dark, etc.).

### Integration with Existing Projects

The Image Studio GUI integrates seamlessly with existing gui_image_studio workflows. You can:
- Load images created with other tools
- Combine designer-created images with programmatically generated ones
- Use the same embedded code format across all tools

### Extensibility

The Image Studio GUI is built with extensibility in mind. Advanced users can:
- Add custom drawing tools
- Implement additional image filters
- Extend the code generation templates
- Integrate with external image processing libraries

## Examples

See the `examples/` directory for complete usage examples:
- `06_image_designer_gui.py` - Launch the studio
- `07_using_designed_images.py` - Use designer-created images in applications

## API Reference

The Image Studio GUI is primarily a visual tool, but it also exposes programmatic interfaces:

### ImageDesignerGUI Class

Main application class with methods for:
- Image management (create, load, save, delete)
- Drawing operations (tool selection, canvas interaction)
- Code generation (preview, export)

### Integration Functions

- `launch_designer()` - Launch the GUI from code
- `embed_images_from_folder()` - Generate embedded code from image files

For detailed API documentation, see the source code docstrings in `image_studio.py`.
