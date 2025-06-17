# 🚀 GUI Image Studio - Quick Reference

## Essential Shortcuts
| Action | Shortcut | Description |
|--------|----------|-------------|
| **New Image** | `Ctrl+N` | Create a new blank image |
| **Load Image** | `Ctrl+O` | Load existing image file |
| **Toggle Grid** | `G` | Show/hide pixel grid |
| **Zoom In** | `+` | Increase zoom level |
| **Zoom Out** | `-` | Decrease zoom level |
| **Reset Zoom** | `0` | Reset to 100% zoom |
| **Help** | `F1` | Show quick start guide |

## Drawing Tools
| Tool | Icon | Best For | Tip |
|------|------|----------|-----|
| **Brush** | 🖌️ | Freehand drawing | Good for organic shapes |
| **Pencil** | ✏️ | Pixel art | Use with Grid + high zoom |
| **Eraser** | 🧽 | Corrections | Creates transparency |
| **Line** | ─ | Straight lines | Hold Shift for H/V lines |
| **Rectangle** | ▭ | UI elements | Hold Shift for squares |
| **Circle** | ○ | Icons, buttons | Hold Shift for perfect circles |
| **Text** | T | Labels | Scales with zoom level |
| **Fill** | 🪣 | Large areas | Fills connected pixels |

## Image Sizes
| Purpose | Recommended Size | Notes |
|---------|------------------|-------|
| **Small Icons** | 16x16, 24x24 | System tray, toolbar |
| **Standard Icons** | 32x32, 48x48 | Application icons |
| **Buttons** | 64x64, 80x40 | UI buttons with text |
| **Sprites** | 32x32, 64x64 | Game objects |
| **Backgrounds** | Variable | Match your UI size |

## Code Generation
| Framework | Best For | Features |
|-----------|----------|----------|
| **tkinter** | Standard Python GUIs | PhotoImage, universal compatibility |
| **customtkinter** | Modern Python GUIs | CTkImage, dark/light themes |

| Usage Type | Purpose | Generated Code Includes |
|------------|---------|------------------------|
| **general** | Any use case | Basic loading functions |
| **buttons** | Interactive elements | Button creation helpers |
| **icons** | Small graphics | Icon sizing functions |
| **backgrounds** | Full-screen images | Background scaling code |
| **sprites** | Game graphics | Performance optimized code |
| **ui_elements** | Custom controls | Professional UI helpers |

## Quality Settings
| Range | Use Case | File Size | Quality |
|-------|----------|-----------|---------|
| **1-30** | Web thumbnails | Smallest | Low |
| **31-70** | General use | Medium | Good |
| **71-85** | **Recommended** | Balanced | High |
| **86-100** | Print quality | Largest | Highest |

## Pixel Art Workflow
1. **Setup**: Pencil tool + Grid enabled + 400% zoom
2. **Plan**: Sketch basic shape first
3. **Build**: Add details pixel by pixel
4. **Test**: Check at actual size (100% zoom)
5. **Refine**: Adjust colors and details

## Multi-Theme Organization
- **Naming**: `theme_imagename.png`
- **Examples**: 
  - `dark_icon.png` → Theme: "dark"
  - `light_button.png` → Theme: "light"
  - `game_sprite.png` → Theme: "game"

## Common Issues & Quick Fixes
| Problem | Quick Fix |
|---------|-----------|
| **Slow drawing** | Reduce zoom level |
| **Preview not updating** | Change framework/usage type |
| **Large file sizes** | Reduce quality to 70-85 |
| **Blurry images** | Use PNG format, check zoom |
| **Code won't work** | Check framework imports |

## Integration Template
```python
# Basic integration template
import tkinter as tk
from PIL import Image, ImageTk
import base64
from io import BytesIO

def load_image(base64_string):
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))
    return ImageTk.PhotoImage(pil_image)

# Use your embedded images
root = tk.Tk()
photo = load_image(embedded_images['theme']['image.png'])
button = tk.Button(root, image=photo, text="My Button")
button.pack()
root.mainloop()
```

## Pro Tips
- 💡 **Save frequently** - No auto-save yet
- 🎯 **Test at actual size** - Don't rely on zoomed view
- 🎨 **Use consistent colors** - Match your app theme
- 📏 **Plan dimensions** - Consistent sizes look professional
- 🔄 **Preview early** - Generate code to test integration
- 📋 **Organize by theme** - Use filename prefixes
- ⚡ **Optimize quality** - 85 is usually perfect
- 🖱️ **Right-click images** - Access more options

---
**Need more help?** Press `F1` in the application or check the Help menu!