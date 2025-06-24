#!/usr/bin/env python3
"""
CustomTkinter Contrast & Saturation Example - gui_image_studio
==========================================================

This example demonstrates contrast and saturation adjustments using CustomTkinter.
Shows interactive sliders for real-time adjustment of image properties.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import tkinter as tk

import customtkinter as ctk

import gui_image_studio


class ContrastSaturationDemo:
    def __init__(self):
        # Set CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("CustomTkinter - Contrast & Saturation Demo")
        self.root.geometry("600x500")

        self.setup_ui()
        self.update_image()

    def setup_ui(self):
        """Set up the user interface."""
        # Title
        title_label = ctk.CTkLabel(
            self.root,
            text="Contrast & Saturation Adjustment",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(pady=20)

        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Controls frame
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Image selection
        ctk.CTkLabel(
            controls_frame, text="Image:", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))

        self.image_var = tk.StringVar(value="colorful.png")
        image_combo = ctk.CTkComboBox(
            controls_frame,
            variable=self.image_var,
            values=["colorful.png", "icon.png", "logo.png"],
            command=self.on_image_change,
        )
        image_combo.pack(pady=(0, 20))

        # Contrast control
        ctk.CTkLabel(
            controls_frame, text="Contrast:", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))

        self.contrast_var = tk.DoubleVar(value=1.0)
        contrast_slider = ctk.CTkSlider(
            controls_frame,
            from_=0.1,
            to=3.0,
            variable=self.contrast_var,
            command=self.update_image,
        )
        contrast_slider.pack(pady=(0, 5))

        self.contrast_label = ctk.CTkLabel(controls_frame, text="1.0")
        self.contrast_label.pack(pady=(0, 20))

        # Saturation control
        ctk.CTkLabel(
            controls_frame, text="Saturation:", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))

        self.saturation_var = tk.DoubleVar(value=1.0)
        saturation_slider = ctk.CTkSlider(
            controls_frame,
            from_=0.0,
            to=3.0,
            variable=self.saturation_var,
            command=self.update_image,
        )
        saturation_slider.pack(pady=(0, 5))

        self.saturation_label = ctk.CTkLabel(controls_frame, text="1.0")
        self.saturation_label.pack(pady=(0, 20))

        # Additional controls
        ctk.CTkLabel(
            controls_frame,
            text="Additional Effects:",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(10, 5))

        self.grayscale_var = tk.BooleanVar()
        grayscale_check = ctk.CTkCheckBox(
            controls_frame,
            text="Grayscale",
            variable=self.grayscale_var,
            command=self.update_image,
        )
        grayscale_check.pack(pady=5)

        # Tint controls
        ctk.CTkLabel(
            controls_frame, text="Tint Intensity:", font=ctk.CTkFont(size=12)
        ).pack(pady=(10, 5))

        self.tint_var = tk.DoubleVar(value=0.0)
        tint_slider = ctk.CTkSlider(
            controls_frame,
            from_=0.0,
            to=1.0,
            variable=self.tint_var,
            command=self.update_image,
        )
        tint_slider.pack(pady=(0, 5))

        self.tint_label = ctk.CTkLabel(controls_frame, text="0.0")
        self.tint_label.pack(pady=(0, 10))

        # Reset button
        reset_btn = ctk.CTkButton(
            controls_frame, text="Reset All", command=self.reset_values
        )
        reset_btn.pack(pady=20)

        # Presets
        ctk.CTkLabel(
            controls_frame, text="Presets:", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 5))

        presets = [
            ("Vivid", {"contrast": 1.3, "saturation": 1.5}),
            ("Muted", {"contrast": 0.8, "saturation": 0.5}),
            ("High Contrast", {"contrast": 2.0, "saturation": 1.0}),
            ("Vintage", {"contrast": 0.9, "saturation": 0.7, "tint": 0.2}),
        ]

        for name, values in presets:
            btn = ctk.CTkButton(
                controls_frame,
                text=name,
                width=100,
                command=lambda v=values: self.apply_preset(v),
            )
            btn.pack(pady=2)

        # Image display frame
        image_frame = ctk.CTkFrame(main_frame)
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = ctk.CTkLabel(image_frame, text="Image will appear here")
        self.image_label.pack(expand=True)

    def on_image_change(self, value):
        """Handle image selection change."""
        self.update_image()

    def update_image(self, value=None):
        """Update the displayed image with current settings."""
        try:
            # Get current values
            contrast = self.contrast_var.get()
            saturation = self.saturation_var.get()
            grayscale = self.grayscale_var.get()
            tint_intensity = self.tint_var.get()

            # Update labels
            self.contrast_label.configure(text=f"{contrast:.1f}")
            self.saturation_label.configure(text=f"{saturation:.1f}")
            self.tint_label.configure(text=f"{tint_intensity:.1f}")

            # Prepare parameters
            params = {
                "framework": "customtkinter",
                "size": (200, 200),
                "theme": "dark",
                "contrast": contrast,
                "saturation": saturation,
                "grayscale": grayscale,
            }

            # Add tint if intensity > 0
            if tint_intensity > 0:
                params["tint_color"] = (100, 150, 255)  # Blue tint
                params["tint_intensity"] = tint_intensity

            # Load and display image
            image = gui_image_studio.get_image(self.image_var.get(), **params)
            self.image_label.configure(image=image, text="")

        except Exception as e:
            self.image_label.configure(text=f"Error loading image:\n{str(e)}")

    def reset_values(self):
        """Reset all values to defaults."""
        self.contrast_var.set(1.0)
        self.saturation_var.set(1.0)
        self.tint_var.set(0.0)
        self.grayscale_var.set(False)
        self.update_image()

    def apply_preset(self, preset_values):
        """Apply a preset configuration."""
        self.contrast_var.set(preset_values.get("contrast", 1.0))
        self.saturation_var.set(preset_values.get("saturation", 1.0))
        self.tint_var.set(preset_values.get("tint", 0.0))
        self.grayscale_var.set(preset_values.get("grayscale", False))
        self.update_image()

    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main function."""
    try:
        demo = ContrastSaturationDemo()
        demo.run()
    except ImportError:
        print(
            "CustomTkinter not installed. Please install with: pip install customtkinter"
        )
    except Exception as e:
        print(f"Error running demo: {e}")


if __name__ == "__main__":
    main()
