#!/usr/bin/env python3
"""
Advanced Features Examples - gui_image_studio
=========================================

This example demonstrates advanced features and edge cases:
- Format conversion
- Error handling
- Performance considerations
- Complex transformations
- Integration patterns
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

import gui_image_studio


class AdvancedFeaturesDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Loader - Advanced Features")
        self.root.geometry("800x600")

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Create notebook for different sections
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Format conversion tab
        self.create_format_tab(notebook)

        # Error handling tab
        self.create_error_handling_tab(notebook)

        # Performance tab
        self.create_performance_tab(notebook)

        # Complex transformations tab
        self.create_complex_transformations_tab(notebook)

        # Integration patterns tab
        self.create_integration_tab(notebook)

    def create_format_tab(self, notebook):
        """Create format conversion demonstration tab."""
        format_frame = ttk.Frame(notebook)
        notebook.add(format_frame, text="Format Conversion")

        ttk.Label(
            format_frame, text="Format Conversion Examples", font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Format conversion controls
        control_frame = ttk.Frame(format_frame)
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(control_frame, text="Convert to format:").pack(side=tk.LEFT)

        self.format_var = tk.StringVar(value="PNG")
        format_combo = ttk.Combobox(
            control_frame,
            textvariable=self.format_var,
            values=["PNG", "JPEG", "BMP", "TIFF"],
            state="readonly",
        )
        format_combo.pack(side=tk.LEFT, padx=10)

        convert_btn = ttk.Button(
            control_frame,
            text="Convert & Display",
            command=self.demonstrate_format_conversion,
        )
        convert_btn.pack(side=tk.LEFT, padx=10)

        # Display area
        self.format_display_frame = ttk.Frame(format_frame)
        self.format_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.format_info_text = tk.Text(self.format_display_frame, height=8, width=50)
        self.format_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.format_image_label = tk.Label(
            self.format_display_frame, text="Converted image will appear here"
        )
        self.format_image_label.pack(side=tk.RIGHT, padx=20)

    def create_error_handling_tab(self, notebook):
        """Create error handling demonstration tab."""
        error_frame = ttk.Frame(notebook)
        notebook.add(error_frame, text="Error Handling")

        ttk.Label(
            error_frame, text="Error Handling Examples", font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Error scenarios
        scenarios = [
            ("Non-existent image", "nonexistent.png"),
            ("Invalid theme", "icon.png"),
            ("Invalid parameters", "icon.png"),
        ]

        for i, (description, image_name) in enumerate(scenarios):
            scenario_frame = ttk.LabelFrame(error_frame, text=description)
            scenario_frame.pack(fill=tk.X, padx=20, pady=5)

            btn_frame = ttk.Frame(scenario_frame)
            btn_frame.pack(pady=10)

            if i == 0:  # Non-existent image
                ttk.Button(
                    btn_frame,
                    text="Try to load non-existent image",
                    command=lambda: self.test_nonexistent_image(),
                ).pack()
            elif i == 1:  # Invalid theme
                ttk.Button(
                    btn_frame,
                    text="Try invalid theme",
                    command=lambda: self.test_invalid_theme(),
                ).pack()
            elif i == 2:  # Invalid parameters
                ttk.Button(
                    btn_frame,
                    text="Try invalid parameters",
                    command=lambda: self.test_invalid_parameters(),
                ).pack()

        # Error log
        ttk.Label(error_frame, text="Error Log:").pack(anchor=tk.W, padx=20)
        self.error_log = tk.Text(error_frame, height=10, width=70)
        self.error_log.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Clear log button
        ttk.Button(error_frame, text="Clear Log", command=self.clear_error_log).pack(
            pady=5
        )

    def create_performance_tab(self, notebook):
        """Create performance testing tab."""
        perf_frame = ttk.Frame(notebook)
        notebook.add(perf_frame, text="Performance")

        ttk.Label(
            perf_frame, text="Performance Testing", font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Performance tests
        test_frame = ttk.Frame(perf_frame)
        test_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(
            test_frame, text="Batch Load Test", command=self.run_batch_load_test
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            test_frame,
            text="Transformation Speed Test",
            command=self.run_transformation_test,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            test_frame, text="Memory Usage Test", command=self.run_memory_test
        ).pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            perf_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)

        # Results display
        self.perf_results = tk.Text(perf_frame, height=15, width=70)
        self.perf_results.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_complex_transformations_tab(self, notebook):
        """Create complex transformations tab."""
        complex_frame = ttk.Frame(notebook)
        notebook.add(complex_frame, text="Complex Transformations")

        ttk.Label(
            complex_frame,
            text="Complex Transformation Combinations",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        # Preset complex transformations
        presets = [
            {
                "name": "Vintage Photo",
                "params": {
                    "tint_color": (255, 220, 177),
                    "tint_intensity": 0.2,
                    "contrast": 0.8,
                    "saturation": 0.6,
                    "transparency": 0.9,
                },
            },
            {
                "name": "Neon Glow",
                "params": {
                    "tint_color": (0, 255, 255),
                    "tint_intensity": 0.4,
                    "contrast": 1.5,
                    "saturation": 2.0,
                },
            },
            {
                "name": "Dramatic B&W",
                "params": {"grayscale": True, "contrast": 2.0, "transparency": 0.8},
            },
            {
                "name": "Rotated Fade",
                "params": {
                    "rotate": 15,
                    "transparency": 0.6,
                    "tint_color": (200, 200, 255),
                    "tint_intensity": 0.3,
                },
            },
        ]

        # Create grid of complex transformations
        grid_frame = ttk.Frame(complex_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.complex_labels = {}

        for i, preset in enumerate(presets):
            row = i // 2
            col = i % 2

            preset_frame = ttk.LabelFrame(grid_frame, text=preset["name"])
            preset_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Image display
            img_label = tk.Label(preset_frame, text="Click 'Apply' to see result")
            img_label.pack(pady=10)

            # Apply button
            ttk.Button(
                preset_frame,
                text="Apply Transformation",
                command=lambda p=preset: self.apply_complex_transformation(p),
            ).pack(pady=5)

            self.complex_labels[preset["name"]] = img_label

        # Configure grid weights
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)

    def create_integration_tab(self, notebook):
        """Create integration patterns tab."""
        integration_frame = ttk.Frame(notebook)
        notebook.add(integration_frame, text="Integration Patterns")

        ttk.Label(
            integration_frame,
            text="Integration Patterns & Best Practices",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        # Pattern examples
        patterns_text = tk.Text(integration_frame, height=20, width=80, wrap=tk.WORD)
        patterns_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        patterns_content = """
INTEGRATION PATTERNS & BEST PRACTICES

1. LAZY LOADING PATTERN
   Load images only when needed to improve startup time:

   class ImageManager:
       def __init__(self):
           self._cache = {}

       def get_image(self, name, **kwargs):
           key = (name, frozenset(kwargs.items()))
           if key not in self._cache:
               self._cache[key] = gui_image_studio.get_image(name, **kwargs)
           return self._cache[key]

2. THEME-AWARE COMPONENT PATTERN
   Create components that automatically adapt to theme changes:

   class ThemedButton(tk.Button):
       def __init__(self, parent, image_name, **kwargs):
           self.image_name = image_name
           self.current_theme = "default"
           super().__init__(parent, **kwargs)
           self.update_theme()

       def update_theme(self, theme="default"):
           if theme != self.current_theme:
               self.current_theme = theme
               image = gui_image_studio.get_image(
                   self.image_name,
                   framework="tkinter",
                   theme=theme
               )
               self.configure(image=image)
               self.image = image  # Keep reference

3. ASYNC LOADING PATTERN
   Load images in background threads for better responsiveness:

   def load_image_async(image_name, callback, **kwargs):
       def load():
           try:
               image = gui_image_studio.get_image(image_name, **kwargs)
               callback(image, None)
           except Exception as e:
               callback(None, e)

       threading.Thread(target=load, daemon=True).start()

4. ANIMATION MANAGER PATTERN
   Centralized management of multiple animations:

   class AnimationManager:
       def __init__(self, root):
           self.root = root
           self.animations = {}
           self.jobs = {}

       def add_animation(self, name, label, anim_data):
           self.animations[name] = (label, anim_data)

       def start_animation(self, name):
           if name in self.animations:
               label, anim_data = self.animations[name]
               self._animate(name, label, anim_data, 0)

       def _animate(self, name, label, anim_data, frame_idx):
           frames = anim_data["animated_frames"]
           if frames and name in self.animations:
               label.configure(image=frames[frame_idx])
               next_idx = (frame_idx + 1) % len(frames)
               job_id = self.root.after(
                   anim_data["frame_delay"],
                   self._animate, name, label, anim_data, next_idx
               )
               self.jobs[name] = job_id

5. ERROR HANDLING PATTERN
   Graceful degradation when images fail to load:

   def safe_get_image(image_name, fallback_text="Image not available", **kwargs):
       try:
           return gui_image_studio.get_image(image_name, **kwargs)
       except Exception as e:
           print(f"Failed to load {image_name}: {e}")
           # Return a placeholder or None
           return None

   # Usage:
   image = safe_get_image("icon.png", framework="tkinter")
   if image:
       label.configure(image=image)
   else:
       label.configure(text="Icon not available")

6. RESOURCE CLEANUP PATTERN
   Proper cleanup of image resources:

   class ImageWidget:
       def __init__(self):
           self.images = []  # Keep references

       def set_image(self, image_name, **kwargs):
           image = gui_image_studio.get_image(image_name, **kwargs)
           self.images.append(image)  # Prevent GC
           return image

       def cleanup(self):
           self.images.clear()  # Allow GC

7. CONFIGURATION-DRIVEN LOADING
   Use configuration files to define image loading parameters:

   IMAGE_CONFIG = {
       "icons": {
           "size": (32, 32),
           "theme": "default"
       },
       "buttons": {
           "size": (80, 32),
           "contrast": 1.1
       }
   }

   def load_configured_image(image_name, config_key, **overrides):
       config = IMAGE_CONFIG.get(config_key, {})
       config.update(overrides)
       return gui_image_studio.get_image(image_name, **config)
        """

        patterns_text.insert(tk.END, patterns_content)
        patterns_text.configure(state=tk.DISABLED)

        # Demo button
        ttk.Button(
            integration_frame,
            text="Run Integration Demo",
            command=self.run_integration_demo,
        ).pack(pady=10)

    def demonstrate_format_conversion(self):
        """Demonstrate format conversion."""
        format_type = self.format_var.get()

        try:
            start_time = time.time()

            # Load image with format conversion
            image = gui_image_studio.get_image(
                "colorful.png",
                framework="tkinter",
                size=(128, 128),
                format_override=format_type,
            )

            load_time = time.time() - start_time

            # Display image
            self.format_image_label.configure(image=image)
            self.format_image_label.image = image

            # Show info
            info = f"Format Conversion Results:\n"
            info += f"Original: PNG\n"
            info += f"Converted to: {format_type}\n"
            info += f"Load time: {load_time:.3f} seconds\n"
            info += f"Size: 128x128 pixels\n"
            info += f"Success: Image converted and displayed\n"

            self.format_info_text.delete(1.0, tk.END)
            self.format_info_text.insert(tk.END, info)

        except Exception as e:
            error_info = f"Format Conversion Error:\n"
            error_info += f"Target format: {format_type}\n"
            error_info += f"Error: {str(e)}\n"

            self.format_info_text.delete(1.0, tk.END)
            self.format_info_text.insert(tk.END, error_info)

    def test_nonexistent_image(self):
        """Test loading a non-existent image."""
        try:
            image = gui_image_studio.get_image("nonexistent.png", framework="tkinter")
        except Exception as e:
            self.log_error(f"Non-existent image test: {str(e)}")

    def test_invalid_theme(self):
        """Test using an invalid theme."""
        try:
            image = gui_image_studio.get_image(
                "icon.png", framework="tkinter", theme="invalid_theme"
            )
        except Exception as e:
            self.log_error(f"Invalid theme test: {str(e)}")

    def test_invalid_parameters(self):
        """Test using invalid parameters."""
        try:
            image = gui_image_studio.get_image(
                "icon.png", framework="tkinter", size=(-10, -10), contrast=-5.0
            )
        except Exception as e:
            self.log_error(f"Invalid parameters test: {str(e)}")

    def log_error(self, message):
        """Log an error message."""
        timestamp = time.strftime("%H:%M:%S")
        self.error_log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.error_log.see(tk.END)

    def clear_error_log(self):
        """Clear the error log."""
        self.error_log.delete(1.0, tk.END)

    def run_batch_load_test(self):
        """Run batch loading performance test."""

        def test():
            self.perf_results.insert(tk.END, "Starting batch load test...\n")

            images = [
                "icon.png",
                "colorful.png",
                "circle.png",
                "square.png",
                "triangle.png",
            ]
            sizes = [(32, 32), (64, 64), (128, 128)]

            total_tests = len(images) * len(sizes)
            completed = 0

            start_time = time.time()

            for image_name in images:
                for size in sizes:
                    try:
                        load_start = time.time()
                        image = gui_image_studio.get_image(
                            image_name, framework="tkinter", size=size
                        )
                        load_time = time.time() - load_start

                        self.perf_results.insert(
                            tk.END, f"Loaded {image_name} at {size}: {load_time:.3f}s\n"
                        )

                    except Exception as e:
                        self.perf_results.insert(
                            tk.END, f"Failed to load {image_name} at {size}: {e}\n"
                        )

                    completed += 1
                    self.progress_var.set((completed / total_tests) * 100)
                    self.root.update()

            total_time = time.time() - start_time
            self.perf_results.insert(
                tk.END, f"\nBatch test completed in {total_time:.3f}s\n"
            )
            self.perf_results.insert(
                tk.END, f"Average time per image: {total_time/total_tests:.3f}s\n\n"
            )

            self.progress_var.set(0)

        threading.Thread(target=test, daemon=True).start()

    def run_transformation_test(self):
        """Run transformation speed test."""

        def test():
            self.perf_results.insert(tk.END, "Starting transformation speed test...\n")

            transformations = [
                ("Original", {}),
                ("Grayscale", {"grayscale": True}),
                ("Rotated", {"rotate": 45}),
                ("Tinted", {"tint_color": (255, 0, 0), "tint_intensity": 0.5}),
                ("High Contrast", {"contrast": 2.0}),
                (
                    "Complex",
                    {
                        "grayscale": True,
                        "rotate": 30,
                        "contrast": 1.5,
                        "saturation": 0.5,
                    },
                ),
            ]

            for i, (name, params) in enumerate(transformations):
                try:
                    start_time = time.time()
                    image = gui_image_studio.get_image(
                        "colorful.png", framework="tkinter", size=(128, 128), **params
                    )
                    load_time = time.time() - start_time

                    self.perf_results.insert(
                        tk.END, f"{name} transformation: {load_time:.3f}s\n"
                    )

                except Exception as e:
                    self.perf_results.insert(
                        tk.END, f"{name} transformation failed: {e}\n"
                    )

                self.progress_var.set(((i + 1) / len(transformations)) * 100)
                self.root.update()

            self.perf_results.insert(tk.END, "\nTransformation test completed\n\n")
            self.progress_var.set(0)

        threading.Thread(target=test, daemon=True).start()

    def run_memory_test(self):
        """Run memory usage test."""
        self.perf_results.insert(
            tk.END, "Memory test: Loading multiple large images...\n"
        )

        try:
            images = []
            for i in range(10):
                image = gui_image_studio.get_image(
                    "colorful.png", framework="tkinter", size=(256, 256)
                )
                images.append(image)
                self.perf_results.insert(tk.END, f"Loaded image {i+1}/10\n")
                self.progress_var.set(((i + 1) / 10) * 100)
                self.root.update()

            self.perf_results.insert(
                tk.END, f"Successfully loaded {len(images)} large images\n"
            )
            self.perf_results.insert(
                tk.END,
                "Images kept in memory - check task manager for memory usage\n\n",
            )

        except Exception as e:
            self.perf_results.insert(tk.END, f"Memory test failed: {e}\n\n")

        self.progress_var.set(0)

    def apply_complex_transformation(self, preset):
        """Apply a complex transformation preset."""
        try:
            image = gui_image_studio.get_image(
                "colorful.png", framework="tkinter", size=(100, 100), **preset["params"]
            )

            label = self.complex_labels[preset["name"]]
            label.configure(image=image)
            label.image = image

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply {preset['name']}: {e}")

    def run_integration_demo(self):
        """Run a demonstration of integration patterns."""
        demo_window = tk.Toplevel(self.root)
        demo_window.title("Integration Demo")
        demo_window.geometry("400x300")

        # Lazy loading example
        class LazyImageManager:
            def __init__(self):
                self._cache = {}

            def get_image(self, name, **kwargs):
                key = (name, frozenset(kwargs.items()))
                if key not in self._cache:
                    self._cache[key] = gui_image_studio.get_image(name, **kwargs)
                return self._cache[key]

        manager = LazyImageManager()

        ttk.Label(demo_window, text="Integration Demo - Lazy Loading").pack(pady=10)

        def load_cached_image():
            try:
                # This will be cached after first load
                image = manager.get_image(
                    "icon.png", framework="tkinter", size=(64, 64)
                )

                if hasattr(load_cached_image, "label"):
                    load_cached_image.label.configure(image=image)
                    load_cached_image.label.image = image
                else:
                    load_cached_image.label = tk.Label(demo_window, image=image)
                    load_cached_image.label.pack(pady=10)
                    load_cached_image.label.image = image

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

        ttk.Button(
            demo_window, text="Load Image (Cached)", command=load_cached_image
        ).pack(pady=5)

        ttk.Label(
            demo_window,
            text="Click multiple times - first load is slower,\nsubsequent loads use cache",
        ).pack(pady=10)

    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Run advanced features examples."""
    print("Image Loader - Advanced Features Examples")
    print("========================================")

    demo = AdvancedFeaturesDemo()
    demo.run()


if __name__ == "__main__":
    main()
