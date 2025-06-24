#!/usr/bin/env python3
"""
Image Transformations Examples - gui_image_studio
=============================================

This example demonstrates various image transformation capabilities:
- Resizing
- Rotation
- Grayscale conversion
- Transparency adjustment
- Contrast and saturation adjustment
- Tinting
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import tkinter as tk
from tkinter import Scale, ttk

import gui_image_studio


class TransformationDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Loader - Transformation Examples")
        self.root.geometry("900x700")  # Increased height to accommodate all controls

        self.current_image_name = "colorful.png"
        self.setup_ui()
        self.update_image()

    def setup_ui(self):
        """Set up the user interface."""
        # Control panel with scrollbar
        control_container = ttk.Frame(self.root)
        control_container.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Create a canvas and scrollbar for the control panel
        canvas = tk.Canvas(control_container, width=250)
        scrollbar = ttk.Scrollbar(
            control_container, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Use scrollable_frame instead of control_frame for all controls
        control_frame = scrollable_frame

        # Title for control panel
        title_label = ttk.Label(
            control_frame, text="Image Transformations", font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Image selection
        ttk.Label(control_frame, text="Image:").pack(anchor=tk.W)
        self.image_var = tk.StringVar(value=self.current_image_name)
        image_combo = ttk.Combobox(
            control_frame,
            textvariable=self.image_var,
            values=[
                "colorful.png",
                "icon.png",
                "circle.png",
                "square.png",
                "triangle.png",
            ],
            state="readonly",
            width=15,
        )
        image_combo.pack(pady=(0, 10), fill=tk.X)
        image_combo.bind("<<ComboboxSelected>>", self.on_image_change)

        # Size controls
        ttk.Label(control_frame, text="Size:").pack(anchor=tk.W)
        size_frame = ttk.Frame(control_frame)
        size_frame.pack(fill=tk.X, pady=(0, 10))

        self.width_var = tk.IntVar(value=128)
        self.height_var = tk.IntVar(value=128)

        ttk.Label(size_frame, text="W:").grid(row=0, column=0)
        width_scale = Scale(
            size_frame,
            from_=32,
            to=256,
            orient=tk.HORIZONTAL,
            variable=self.width_var,
            command=self.update_image,
        )
        width_scale.grid(row=0, column=1)

        ttk.Label(size_frame, text="H:").grid(row=1, column=0)
        height_scale = Scale(
            size_frame,
            from_=32,
            to=256,
            orient=tk.HORIZONTAL,
            variable=self.height_var,
            command=self.update_image,
        )
        height_scale.grid(row=1, column=1)

        # Rotation
        ttk.Label(control_frame, text="Rotation (degrees):").pack(anchor=tk.W)
        self.rotation_var = tk.IntVar(value=0)
        rotation_scale = Scale(
            control_frame,
            from_=0,
            to=360,
            orient=tk.HORIZONTAL,
            variable=self.rotation_var,
            command=self.update_image,
        )
        rotation_scale.pack(fill=tk.X, pady=(0, 10))

        # Transparency
        ttk.Label(control_frame, text="Transparency:").pack(anchor=tk.W)
        self.transparency_var = tk.DoubleVar(value=1.0)
        transparency_scale = Scale(
            control_frame,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.transparency_var,
            command=self.update_image,
        )
        transparency_scale.pack(fill=tk.X, pady=(0, 10))

        # Contrast
        ttk.Label(control_frame, text="Contrast:").pack(anchor=tk.W)
        self.contrast_var = tk.DoubleVar(value=1.0)
        contrast_scale = Scale(
            control_frame,
            from_=0.1,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.contrast_var,
            command=self.update_image,
        )
        contrast_scale.pack(fill=tk.X, pady=(0, 10))

        # Saturation
        ttk.Label(control_frame, text="Saturation:").pack(anchor=tk.W)
        self.saturation_var = tk.DoubleVar(value=1.0)
        saturation_scale = Scale(
            control_frame,
            from_=0.0,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.saturation_var,
            command=self.update_image,
        )
        saturation_scale.pack(fill=tk.X, pady=(0, 10))

        # Tint controls
        ttk.Label(control_frame, text="Tint Color:").pack(anchor=tk.W)
        tint_frame = ttk.Frame(control_frame)
        tint_frame.pack(fill=tk.X, pady=(0, 5))

        self.tint_r = tk.IntVar(value=0)
        self.tint_g = tk.IntVar(value=0)
        self.tint_b = tk.IntVar(value=0)

        ttk.Label(tint_frame, text="R:").grid(row=0, column=0)
        Scale(
            tint_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.tint_r,
            command=self.update_image,
            length=80,
        ).grid(row=0, column=1)

        ttk.Label(tint_frame, text="G:").grid(row=1, column=0)
        Scale(
            tint_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.tint_g,
            command=self.update_image,
            length=80,
        ).grid(row=1, column=1)

        ttk.Label(tint_frame, text="B:").grid(row=2, column=0)
        Scale(
            tint_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.tint_b,
            command=self.update_image,
            length=80,
        ).grid(row=2, column=1)

        # Tint intensity
        ttk.Label(control_frame, text="Tint Intensity:").pack(anchor=tk.W)
        self.tint_intensity_var = tk.DoubleVar(value=0.0)
        tint_intensity_scale = Scale(
            control_frame,
            from_=0.0,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.tint_intensity_var,
            command=self.update_image,
        )
        tint_intensity_scale.pack(fill=tk.X, pady=(0, 10))

        # Grayscale checkbox
        self.grayscale_var = tk.BooleanVar()
        grayscale_check = ttk.Checkbutton(
            control_frame,
            text="Grayscale",
            variable=self.grayscale_var,
            command=self.update_image,
        )
        grayscale_check.pack(anchor=tk.W, pady=(0, 10))

        # Reset button
        reset_button = ttk.Button(
            control_frame, text="Reset All", command=self.reset_values
        )
        reset_button.pack(fill=tk.X)

        # Image display area
        self.image_frame = ttk.Frame(self.root)
        self.image_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        self.image_label = tk.Label(self.image_frame, text="Image will appear here")
        self.image_label.pack(expand=True)

    def on_image_change(self, event=None):
        """Handle image selection change."""
        self.current_image_name = self.image_var.get()
        self.update_image()

    def update_image(self, event=None):
        """Update the displayed image with current transformation settings."""
        try:
            # Get current values
            size = (self.width_var.get(), self.height_var.get())
            rotation = self.rotation_var.get()
            transparency = self.transparency_var.get()
            contrast = self.contrast_var.get()
            saturation = self.saturation_var.get()
            grayscale = self.grayscale_var.get()

            # Tint color and intensity
            tint_color = None
            tint_intensity = self.tint_intensity_var.get()
            if tint_intensity > 0:
                tint_color = (self.tint_r.get(), self.tint_g.get(), self.tint_b.get())

            # Load transformed image
            image = gui_image_studio.get_image(
                self.current_image_name,
                framework="tkinter",
                size=size,
                theme="default",
                grayscale=grayscale,
                rotate=rotation,
                transparency=transparency,
                contrast=contrast,
                saturation=saturation,
                tint_color=tint_color,
                tint_intensity=tint_intensity,
            )

            # Update display
            self.image_label.configure(image=image)
            self.image_label.image = image  # Keep reference

        except Exception as e:
            self.image_label.configure(text=f"Error loading image:\n{str(e)}")

    def reset_values(self):
        """Reset all transformation values to defaults."""
        self.width_var.set(128)
        self.height_var.set(128)
        self.rotation_var.set(0)
        self.transparency_var.set(1.0)
        self.contrast_var.set(1.0)
        self.saturation_var.set(1.0)
        self.tint_r.set(0)
        self.tint_g.set(0)
        self.tint_b.set(0)
        self.tint_intensity_var.set(0.0)
        self.grayscale_var.set(False)
        self.update_image()

    def run(self):
        """Start the application."""
        self.root.mainloop()


def preset_transformations_example():
    """Show some preset transformation examples."""
    root = tk.Tk()
    root.title("Preset Transformations")
    root.geometry("600x400")

    # Define some interesting presets
    presets = [
        {"name": "Original", "params": {"size": (64, 64)}},
        {
            "name": "Sepia Tone",
            "params": {
                "size": (64, 64),
                "tint_color": (255, 200, 150),
                "tint_intensity": 0.3,
                "saturation": 0.7,
            },
        },
        {
            "name": "High Contrast",
            "params": {"size": (64, 64), "contrast": 2.0, "saturation": 1.5},
        },
        {
            "name": "Faded",
            "params": {"size": (64, 64), "transparency": 0.5, "saturation": 0.3},
        },
        {
            "name": "Blue Tint",
            "params": {
                "size": (64, 64),
                "tint_color": (100, 150, 255),
                "tint_intensity": 0.4,
            },
        },
        {
            "name": "Rotated Grayscale",
            "params": {"size": (64, 64), "rotate": 45, "grayscale": True},
        },
    ]

    # Create grid of preset examples
    for i, preset in enumerate(presets):
        row = i // 3
        col = i % 3

        try:
            image = gui_image_studio.get_image(
                "colorful.png", framework="tkinter", **preset["params"]
            )

            frame = ttk.Frame(root)
            frame.grid(row=row, column=col, padx=20, pady=20)

            img_label = tk.Label(frame, image=image)
            img_label.pack()

            name_label = ttk.Label(frame, text=preset["name"])
            name_label.pack()

            # Keep reference
            img_label.image = image

        except Exception as e:
            print(f"Error creating preset '{preset['name']}': {e}")

    root.mainloop()


def main():
    """Run transformation examples."""
    print("Image Loader - Transformation Examples")
    print("=====================================")
    print("1. Interactive Transformation Demo")
    print("2. Preset Transformations")
    print("3. Both Examples")

    choice = input("Choose an example (1-3): ").strip()

    if choice == "1":
        demo = TransformationDemo()
        demo.run()
    elif choice == "2":
        preset_transformations_example()
    elif choice == "3":
        demo = TransformationDemo()
        demo.run()
        preset_transformations_example()
    else:
        print("Invalid choice. Running interactive demo by default.")
        demo = TransformationDemo()
        demo.run()


if __name__ == "__main__":
    main()
