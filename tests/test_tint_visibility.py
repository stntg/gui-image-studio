#!/usr/bin/env python3
"""
Test tint visibility - create a simple demo showing clear tint effects

This test file provides visual verification that the tinting functionality
is working correctly. It displays a grid of images with different tint
colors and intensities for easy comparison.

Usage: python test_tint_visibility.py
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import tkinter as tk
import gui_image_studio


def test_tint_visibility():
    """Test tint with strong, clearly visible effects."""
    print("Testing tint visibility with strong effects...")

    root = tk.Tk()
    root.title("Tint Visibility Test")
    root.geometry("800x400")

    # Create a grid of tinted images
    images = []

    # Test different tint colors and intensities
    tint_tests = [
        ("Original", None, 0.0),
        ("Red 50%", (255, 0, 0), 0.5),
        ("Green 50%", (0, 255, 0), 0.5),
        ("Blue 50%", (0, 0, 255), 0.5),
        ("Yellow 30%", (255, 255, 0), 0.3),
        ("Purple 40%", (255, 0, 255), 0.4),
        ("Orange 60%", (255, 128, 0), 0.6),
        ("Dark Red 70%", (128, 0, 0), 0.7),
    ]

    for i, (name, color, intensity) in enumerate(tint_tests):
        row = i // 4
        col = i % 4

        frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
        frame.grid(row=row, column=col, padx=5, pady=5)

        try:
            # Load image with tint
            image = gui_image_studio.get_image(
                "colorful.png",
                framework="tkinter",
                size=(96, 96),
                tint_color=color,
                tint_intensity=intensity,
            )

            # Display image
            img_label = tk.Label(frame, image=image)
            img_label.pack()

            # Label
            text_label = tk.Label(frame, text=name, font=("Arial", 10, "bold"))
            text_label.pack()

            # Keep reference
            images.append(image)

        except Exception as e:
            error_label = tk.Label(frame, text=f"Error:\n{name}", fg="red")
            error_label.pack()
            print(f"Error with {name}: {e}")

    # Keep all image references
    root.images = images

    # Instructions
    instructions = tk.Label(
        root,
        text="Compare the original image with the tinted versions.\nTinting should be clearly visible with these strong intensities.\nThis test verifies that gui_image_studio.get_image() tint parameters work correctly.",
        font=("Arial", 11),
        pady=10,
        justify=tk.CENTER,
    )
    instructions.grid(row=2, column=0, columnspan=4)

    # Add technical info
    tech_info = tk.Label(
        root,
        text="Technical: Uses tint_color=(R,G,B) and tint_intensity=0.0-1.0 parameters",
        font=("Arial", 9),
        fg="gray",
    )
    tech_info.grid(row=3, column=0, columnspan=4, pady=(0, 10))

    print("✓ Tint visibility test window created")
    print("✓ Check if tinting effects are clearly visible")
    print("✓ This test helps developers verify tinting functionality")

    root.mainloop()


if __name__ == "__main__":
    test_tint_visibility()
