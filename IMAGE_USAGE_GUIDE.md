# 🎨 GUI Image Studio - Usage Guide

## Overview

The GUI Image Studio creates embedded images that can be used in
**many different ways** beyond just buttons! The generated code includes
base64-encoded images that work across multiple frameworks and use cases.

## 🚀 **What Can You Create?**

### 1. **Icons & UI Elements**

- Application icons
- Toolbar icons
- Status indicators
- Menu icons
- Navigation elements

### 2. **Game Assets**

- Sprites for 2D games
- Background textures
- UI elements for games
- Character animations (frame by frame)
- Tile sets for tile-based games

### 3. **Web Graphics**

- Website icons
- Background images
- Decorative elements
- Button graphics
- Logo images

### 4. **Desktop Application Graphics**

- Window icons
- Splash screen images
- Background patterns
- Custom cursors
- Notification icons

## 🛠️ **Supported Frameworks**

### **Tkinter** (Standard Python GUI)

- **Buttons**: Image buttons with text combinations
- **Labels**: Icon displays and decorative elements
- **Canvas**: Background images, sprites, and custom graphics
- **Frames**: Background patterns and themed interfaces
- **PhotoImage**: Direct image display with transparency support

### **CustomTkinter** (Modern Python GUI)

- **CTkButton**: Modern styled buttons with embedded images
- **CTkLabel**: Clean icon displays with automatic scaling
- **CTkImage**: High-quality image rendering with light/dark mode support
- **CTkFrame**: Modern containers with background image support
- **Scrollable Frames**: Perfect for image galleries and icon collections
- **Dark/Light Themes**: Automatic image adaptation for different themes

## 🎯 **Usage Types Available**

### **General Purpose**

- Basic image loading and display
- Works with any image type
- Flexible sizing and positioning

### **Buttons**

- Specialized button creation
- Text + image combinations
- Hover effects support
- Click handling

### **Icons**

- Small, scalable graphics
- System integration
- Consistent sizing
- High-quality rendering

### **Backgrounds**

- Full-screen backgrounds
- Tiled patterns
- Gradient overlays
- Responsive scaling

### **Sprites**

- Game object graphics
- Animation frames
- Collision detection support
- Performance optimized

### **UI Elements**

- Custom controls
- Themed interfaces
- Consistent styling
- Professional appearance

## 📝 **How to Use**

### Step 1: Create Your Images

1. Launch GUI Image Studio
2. Click "Create Your First Image!" or "Load an Existing Image"
3. Use the drawing tools to create your graphics:
   - **Brush**: Freehand drawing
   - **Pencil**: Pixel-perfect editing (great with Grid)
   - **Shapes**: Lines, rectangles, circles
   - **Text**: Add text elements
   - **Fill**: Flood fill areas

### Step 2: Configure Generation

1. Select your target **Framework** (tkinter or customtkinter)
2. Choose your **Usage Type** (buttons, icons, sprites, etc.)
3. Adjust **Quality** settings (1-100)

### Step 3: Preview & Generate

1. **Live Preview**: Watch the preview panel update automatically as you:
   - Create or modify images
   - Change framework selection
   - Switch usage types
2. Click "Preview Code" to see the generated code with examples
3. Click "Generate File" to save the code to a .py file
4. Copy the code and integrate it into your project

## 💡 **Pro Tips**

### For Pixel Art:

- Use the **Pencil** tool
- Enable the **Grid** option
- Zoom in 4x or more
- Each grid square = 1 pixel

### For Icons:

- Keep images small (16x16, 32x32, 64x64)
- Use simple, clear designs
- Consider transparency (PNG format)

### For Game Sprites:

- Use consistent sizing
- Consider animation frames
- Optimize for performance
- Use appropriate color palettes

### For Web Graphics:

- Consider file size vs quality
- Use appropriate formats
- Test on different screen sizes
- Optimize for loading speed

## 🔧 **Advanced Features**

### Multi-Theme Support

- Organize images by themes (dark, light, etc.)
- Automatic categorization by filename
- Easy theme switching in code

### Quality Control

- Adjustable compression (1-100%)
- Format optimization
- Size optimization

### Export Options

- Python code generation
- Direct image export
- Multiple format support

### Live Preview

- **Real-time Updates**: See how your images will look instantly
- **Framework-Specific**: Preview adapts to selected framework
- **Usage-Aware**: Different layouts for buttons, icons, sprites, etc.
- **Interactive**: Updates as you draw and modify images

## 📚 **Example Projects**

### Simple Icon App (Tkinter)

```python
# Create a toolbar with custom icons
toolbar = tk.Frame(root)
for icon_name, icon_data in embedded_images['icons'].items():
    btn = create_icon_button(toolbar, icon_data, icon_name)
    btn.pack(side=tk.LEFT)
```

### Modern Button App (CustomTkinter)

```python
# Create modern buttons with custom icons
import customtkinter as ctk

ctk.set_appearance_mode("dark")
root = ctk.CTk()

for icon_name, icon_data in embedded_images['icons'].items():
    ctk_image = create_ctk_image(icon_data, size=(24, 24))
    btn = ctk.CTkButton(root, image=ctk_image, text=icon_name)
    btn.pack(pady=5)
```

### Icon Gallery (Tkinter)

```python
# Create a scrollable icon gallery
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

for name, data in embedded_images['icons'].items():
    photo = create_photo_image(data)
    label = tk.Label(scrollable_frame, image=photo)
    label.pack(side=tk.LEFT, padx=5)
```

## 🎉 **Get Creative!**

The possibilities are endless! You can create:

- Custom desktop applications with unique graphics
- Modern GUI applications with CustomTkinter styling
- Professional software with branded elements
- Icon libraries for your applications
- Themed interfaces with consistent graphics

**Remember**: All images are embedded directly in your code, so no external files
are needed for distribution!
