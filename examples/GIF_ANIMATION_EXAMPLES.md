# GIF Animation Examples - gui_image_studio

This directory contains comprehensive examples demonstrating animated GIF
capabilities in gui_image_studio. These examples showcase various animation
techniques, performance optimization, and integration patterns for both Tkinter
and CustomTkinter applications.

## 📁 Example Files

### Core Animation Examples

#### `gif_animation_showcase.py`

##### Comprehensive GIF Animation Demonstration

- **Purpose**: Complete showcase of animated GIF capabilities
- **Features**:
  - Basic animation playback controls (play, pause, stop, reset)
  - Speed control with real-time adjustment
  - Multiple simultaneous animations
  - Animation transformations (tint, contrast, grayscale, rotation)
  - Synchronized animation groups
  - Performance monitoring and metrics
  - Animation gallery with various effects
- **UI Components**: Tabbed interface with different animation categories
- **Best For**: Understanding all animation features and performance characteristics

#### `ctk_gif_animations.py`

##### CustomTkinter-Specific Animation Examples

- **Purpose**: Modern UI animations using CustomTkinter
- **Features**:
  - Loading spinners in multiple sizes
  - Interactive animated buttons
  - Hover effects and transitions
  - Theme-aware animations
  - Progress indicators
  - Advanced animation controls
  - Performance monitoring
- **UI Components**: Modern dark/light themed interface
- **Best For**: CustomTkinter applications requiring polished animations

#### `04_animated_gifs.py`

##### Basic Animation Integration

- **Purpose**: Simple animated GIF integration examples
- **Features**:
  - Basic animation loading and playback
  - Transform animations (tint, contrast, grayscale)
  - Speed control demonstrations
  - Both Tkinter and CustomTkinter examples
- **Best For**: Getting started with animated GIFs

### Utility Tools

#### `gif_creator.py`

##### Custom GIF Animation Generator

- **Purpose**: Create custom animated GIFs for testing
- **Animations Available**:
  - Loading spinners (various styles and colors)
  - Pulsing circles with fade effects
  - Wave animations with multiple frequencies
  - Rotating geometric shapes
  - Progress bars with shine effects
  - Bouncing balls with physics
  - Color cycling gradients
  - Animated text with wave effects
- **Usage**: `python gif_creator.py [animation_type]`
- **Best For**: Creating custom test animations

## 🚀 Quick Start

### 1. Basic Animation Example

```python
import gui_image_studio

# Load an animated GIF
animation = gui_image_studio.get_image(
    "animation.gif",
    framework="tkinter",
    size=(64, 64),
    animated=True,
    frame_delay=150
)

# Use in your application
frames = animation["animated_frames"]
delay = animation["frame_delay"]

# Animate in a loop
def animate(frame_index=0):
    label.configure(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    root.after(delay, animate, frame_index)

animate()
```

### 2. Animation with Transformations

```python
# Load with visual effects
animation = gui_image_studio.get_image(
    "spinner.gif",
    framework="customtkinter",
    size=(48, 48),
    animated=True,
    tint_color=(100, 150, 255),
    tint_intensity=0.4,
    contrast=1.2,
    frame_delay=100
)
```

### 3. Speed-Controlled Animation

```python
def start_animation_with_speed(speed_multiplier=1.0):
    def animate(frame_index=0):
        if animation_active:
            label.configure(image=frames[frame_index])
            frame_index = (frame_index + 1) % len(frames)
            adjusted_delay = int(base_delay / speed_multiplier)
            root.after(adjusted_delay, animate, frame_index)
    animate()
```

## 🎯 Animation Types Demonstrated

### Loading Animations

- **Spinners**: Rotating dots, circles, and geometric shapes
- **Progress Bars**: Filling bars with shine effects
- **Pulsing Elements**: Breathing effects for status indicators

### Interactive Animations

- **Button States**: Play, pause, stop, record animations
- **Hover Effects**: Mouse-over triggered animations
- **State Transitions**: Smooth transitions between UI states

### Visual Effects

- **Color Transformations**: Tint, saturation, contrast adjustments
- **Geometric Transformations**: Rotation, scaling, positioning
- **Theme Integration**: Dark/light theme compatible animations

### Performance Optimized

- **Frame Caching**: Efficient memory usage
- **Speed Control**: Real-time speed adjustment
- **Resource Management**: Proper cleanup and disposal

## 🛠️ Running the Examples

### Prerequisites

```bash
# Install required packages
pip install pillow numpy

# For CustomTkinter examples
pip install customtkinter
```

### Running Individual Examples

#### Comprehensive Showcase

```bash
python gif_animation_showcase.py
```

Features:

- Multiple animation tabs
- Performance monitoring
- Real-time controls
- Gallery of effects

#### CustomTkinter Demo

```bash
python ctk_gif_animations.py
```

Features:

- Modern UI design
- Theme switching
- Interactive elements
- Advanced controls

#### Create Custom GIFs

```bash
# Create all sample animations
python gif_creator.py all

# Create specific animation types
python gif_creator.py spinner
python gif_creator.py pulse
python gif_creator.py wave
```

### Running All Examples

```bash
python run_examples.py
```

## 📊 Performance Considerations

### Memory Usage

- **Frame Caching**: Animations cache decoded frames for smooth playback
- **Size Optimization**: Use appropriate sizes to balance quality and memory
- **Cleanup**: Properly stop animations to free resources

### CPU Usage

- **Frame Rate**: Adjust `frame_delay` to balance smoothness and CPU usage
- **Concurrent Animations**: Monitor performance with multiple simultaneous animations
- **Transform Caching**: Transformations are cached for repeated use

### Best Practices

```python
# Good: Reasonable size and frame rate
animation = gui_image_studio.get_image(
    "spinner.gif",
    size=(48, 48),
    frame_delay=100,  # 10 FPS
    animated=True
)

# Avoid: Too large or too fast
animation = gui_image_studio.get_image(
    "spinner.gif",
    size=(200, 200),  # Large size
    frame_delay=16,   # 60+ FPS
    animated=True
)
```

## 🎨 Animation Customization

### Color Effects

```python
# Tint animation with custom color
animation = gui_image_studio.get_image(
    "animation.gif",
    tint_color=(255, 100, 150),  # Pink tint
    tint_intensity=0.3,          # 30% intensity
    animated=True
)
```

### Visual Enhancements

```python
# Enhanced contrast and saturation
animation = gui_image_studio.get_image(
    "animation.gif",
    contrast=1.5,      # 50% more contrast
    saturation=1.2,    # 20% more saturation
    animated=True
)
```

### Size and Rotation

```python
# Scaled and rotated animation
animation = gui_image_studio.get_image(
    "animation.gif",
    size=(80, 80),     # Custom size
    rotate=15,         # 15-degree rotation
    animated=True
)
```

## 🔧 Integration Patterns

### Tkinter Integration

```python
import tkinter as tk
import gui_image_studio

class AnimatedApp:
    def __init__(self):
        self.root = tk.Tk()
        self.animation_jobs = {}

    def start_animation(self, key, label, animation_data):
        frames = animation_data["animated_frames"]
        delay = animation_data["frame_delay"]

        def animate(frame_index=0):
            if key in self.animation_jobs:
                label.configure(image=frames[frame_index])
                frame_index = (frame_index + 1) % len(frames)
                job_id = self.root.after(delay, animate, frame_index)
                self.animation_jobs[key] = job_id

        animate()

    def stop_animation(self, key):
        if key in self.animation_jobs:
            self.root.after_cancel(self.animation_jobs[key])
            del self.animation_jobs[key]
```

### CustomTkinter Integration

```python
import customtkinter as ctk
import gui_image_studio

class ModernAnimatedApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.animation_states = {}

    def create_animated_button(self, parent, animation_file):
        frame = ctk.CTkFrame(parent)

        # Load animation
        animation = gui_image_studio.get_image(
            animation_file,
            framework="customtkinter",
            size=(32, 32),
            animated=True
        )

        # Create animated label
        label = ctk.CTkLabel(frame, text="")
        label.pack(pady=5)

        # Control button
        button = ctk.CTkButton(frame, text="Toggle",
                              command=lambda: self.toggle_animation(label, animation))
        button.pack(pady=5)

        return frame
```

## 🐛 Troubleshooting

### Common Issues

#### Animation Not Playing

```python
# Check if animated=True is set
animation = gui_image_studio.get_image(
    "animation.gif",
    animated=True  # Required for GIF animations
)

# Verify frames exist
frames = animation.get("animated_frames", [])
if not frames:
    print("No animation frames loaded")
```

#### Performance Issues

```python
# Reduce frame rate
animation = gui_image_studio.get_image(
    "animation.gif",
    frame_delay=200,  # Slower animation
    animated=True
)

# Reduce size
animation = gui_image_studio.get_image(
    "animation.gif",
    size=(32, 32),  # Smaller size
    animated=True
)
```

#### Memory Leaks

```python
# Always stop animations when done
def cleanup(self):
    for job_id in self.animation_jobs.values():
        if job_id:
            self.root.after_cancel(job_id)
    self.animation_jobs.clear()
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Load with debug info
animation = gui_image_studio.get_image(
    "animation.gif",
    animated=True,
    debug=True  # If available
)
```

## 📚 Additional Resources

### Related Examples

- `02_theming_examples.py` - Theme integration with animations
- `03_image_transformations.py` - Static image transformations
- `05_advanced_features.py` - Advanced gui_image_studio features

### Documentation

- Main README.md - Project overview
- API documentation - Detailed function references
- Performance guide - Optimization techniques

### Sample Assets

- `sample_images/` - Static test images
- `sample_gifs/` - Generated animated GIFs (created by gif_creator.py)

---

**Note**: These examples demonstrate the full capabilities of gui_image_studio's
animated GIF support. Start with the basic examples and gradually explore more
advanced features as needed for your application.
