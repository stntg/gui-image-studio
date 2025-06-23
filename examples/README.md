# GUI Image Studio Examples

This directory contains comprehensive examples demonstrating all features of the
`gui_image_studio` package. These examples show how to use the package effectively in
various scenarios with both Tkinter and CustomTkinter frameworks.

## Prerequisites

Before running the examples, make sure you have:

1. **Python 3.8+** installed
2. **Required packages**:

   ```bash
   pip install gui-image-studio
   # Or install from source:
   pip install -e .
   ```

3. **Generate sample images** (optional, for testing):

   ```bash
   gui-image-studio-create-samples
   # Or programmatically:
   python -c "import gui_image_studio; gui_image_studio.create_sample_images()"
   ```

## Example Files Overview

### 1. Basic Usage (`01_basic_usage.py`)

**What it demonstrates:**

- Fundamental usage with Tkinter and CustomTkinter
- Loading images with default settings
- Basic image display in GUI applications
- Proper reference management to prevent garbage collection

**Key features shown:**

- `gui_image_studio.get_image()` with minimal parameters
- Framework selection (`"tkinter"` vs `"customtkinter"`)
- Basic size specification
- Theme usage (`"default"`, `"dark"`, `"light"`)

**Run with:**

```bash
python examples/01_basic_usage.py
```

### 2. Theming Examples (`02_theming_examples.py`)

**What it demonstrates:**

- Theme-based image loading
- Automatic theme fallback
- Dynamic theme switching
- Theme comparison visualization

**Key features shown:**

- Theme parameter usage (`"default"`, `"dark"`, `"light"`)
- Filename-based theme detection (e.g., `dark_icon.png`)
- Error handling for missing themed images
- Interactive theme switching

**Run with:**

```bash
python examples/02_theming_examples.py
```

### 3. Image Transformations (`03_image_transformations.py`)

**What it demonstrates:**

- All available image transformation options
- Interactive parameter adjustment
- Real-time transformation preview
- Preset transformation combinations

**Key features shown:**

- Size adjustment (`size` parameter)
- Rotation (`rotate` parameter)
- Transparency/brightness (`transparency` parameter)
- Contrast adjustment (`contrast` parameter)
- Saturation adjustment (`saturation` parameter)
- Color tinting (`tint_color`, `tint_intensity` parameters)
- Grayscale conversion (`grayscale` parameter)

**Run with:**

```bash
python examples/03_image_transformations.py
```

### 4. Animated GIFs (`04_animated_gifs.py`)

**What it demonstrates:**

- Animated GIF loading and playback
- Animation control (start/stop)
- Speed adjustment
- Transformed animations
- Multiple simultaneous animations

**Key features shown:**

- `animated=True` parameter
- `frame_delay` parameter
- Animation data structure handling
- Animation loop implementation
- Transformation effects on animations

**Run with:**

```bash
python examples/04_animated_gifs.py
```

### 5. Advanced Features (`05_advanced_features.py`)

**What it demonstrates:**

- Format conversion capabilities
- Error handling strategies
- Performance testing
- Complex transformation combinations
- Integration patterns and best practices

**Key features shown:**

- `format_override` parameter
- Error handling and graceful degradation
- Performance benchmarking
- Memory usage considerations
- Advanced integration patterns

**Run with:**

```bash
python examples/05_advanced_features.py
```

## Sample Images

The examples use a variety of sample images created by `create_sample_images.py`:

### Default Theme Images

- `icon.png` - House icon for basic demonstrations
- `button.png` - Play button for UI elements
- `logo.png` - Sample logo/banner
- `animation.gif` - Animated rotating squares
- `colorful.png` - Rainbow stripes for transformation testing
- `circle.png`, `square.png`, `triangle.png` - Simple shapes

### Themed Images

- `dark_*.png` - Dark theme variants
- `light_*.png` - Light theme variants

## Common Usage Patterns

### Basic Image Loading

```python
import gui_image_studio

# Load a simple image
image = gui_image_studio.get_image(
    "icon.png",
    framework="tkinter",
    size=(64, 64),
    theme="default"
)
```

### Themed Image Loading

```python
# Load with theme (falls back to default if theme not available)
image = gui_image_studio.get_image(
    "icon.png",
    framework="customtkinter",
    size=(32, 32),
    theme="dark"
)
```

### Image Transformations

```python
# Apply multiple transformations
image = gui_image_studio.get_image(
    "colorful.png",
    framework="tkinter",
    size=(128, 128),
    rotate=45,
    tint_color=(255, 100, 100),
    tint_intensity=0.3,
    contrast=1.2,
    saturation=0.8,
    grayscale=False
)
```

### Animated GIF Loading

```python
# Load animated GIF
anim_data = gui_image_studio.get_image(
    "animation.gif",
    framework="tkinter",
    size=(64, 64),
    animated=True,
    frame_delay=120
)

frames = anim_data["animated_frames"]
delay = anim_data["frame_delay"]

# Implement animation loop
def animate(frame_index=0):
    label.configure(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    root.after(delay, animate, frame_index)
```

## Error Handling

The examples demonstrate proper error handling:

```python
try:
    image = gui_image_studio.get_image("image.png", framework="tkinter")
    label.configure(image=image)
    label.image = image  # Keep reference
except ValueError as e:
    print(f"Image loading failed: {e}")
    label.configure(text="Image not available")
```

## Performance Considerations

1. **Caching**: Consider implementing image caching for frequently used images
2. **Size optimization**: Use appropriate sizes to balance quality and performance
3. **Lazy loading**: Load images only when needed
4. **Memory management**: Keep references to prevent garbage collection,
   but clean up when no longer needed

## Integration Best Practices

1. **Reference Management**: Always keep references to loaded images
2. **Error Handling**: Implement graceful fallbacks for missing images
3. **Theme Consistency**: Use consistent theming throughout your application
4. **Performance**: Cache frequently used images and load asynchronously when possible
5. **Resource Cleanup**: Properly clean up resources when widgets are destroyed

## Troubleshooting

### Common Issues

1. **"Image not found" errors**: Ensure `embedded_images.py` is generated and in
   the correct location
2. **Garbage collection**: Keep references to images in your GUI code
3. **CustomTkinter not found**: Install with `pip install customtkinter`
4. **Animation not working**: Check that the GIF is actually animated and
   frames are available

### Debugging Tips

1. Check the `embedded_images.py` file to see what images are available
2. Use try-catch blocks to handle loading errors gracefully
3. Print image data structure to understand what's returned
4. Test with simple parameters first, then add complexity

## Creating Your Own Images

To add your own images to the examples:

1. Place images in the `sample_images` directory
2. Use naming convention: `theme_imagename.ext` (e.g., `dark_myicon.png`)
3. Run `gui-image-studio-generate --folder sample_images --output embedded_images.py`
   to update the embedded images
4. Use the image name (without theme prefix) in your code

## Framework Compatibility

The examples work with:

- **Tkinter**: Built into Python, always available
- **CustomTkinter**: Modern UI library, install separately

Both frameworks are supported by the same `gui_image_studio` API. Just change the
`framework` parameter.

## Developer Testing Tools

### Tint Visibility Test (`../test_tint_visibility.py`)

A visual testing tool that helps developers verify that the tinting functionality
is working correctly:

```bash
python test_tint_visibility.py
```

**What it shows:**

- Grid of images with different tint colors and intensities
- Side-by-side comparison with original image
- Strong tint effects for easy visual verification
- Technical parameter information

**Use cases:**

- Verify tinting is working after code changes
- Visual debugging of tint parameters
- Demonstration of tint capabilities
- Quick functional test for developers

This test is particularly useful when:

- Implementing new tint features
- Debugging tint-related issues
- Verifying cross-platform tint behavior
- Teaching others about tint functionality
