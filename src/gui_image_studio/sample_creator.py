#!/usr/bin/env python3
"""
Script to create sample images for comprehensive gui_image_studio examples.
This creates various types of images including static icons, animated GIFs, and
themed variants.
"""

import math
import os

from PIL import Image, ImageDraw

# Try to import numpy, use fallback if not available
try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def create_sample_images():
    """Create a variety of sample images for testing gui_image_studio functionality."""

    # Create images directory
    images_dir = "sample_images"
    os.makedirs(images_dir, exist_ok=True)

    # 1. Basic icon (default theme)
    create_basic_icon(os.path.join(images_dir, "icon.png"))

    # 2. Themed icons (dark and light themes)
    create_themed_icon(os.path.join(images_dir, "dark_icon.png"), "dark")
    create_themed_icon(os.path.join(images_dir, "light_icon.png"), "light")

    # 3. Button icons
    create_button_icon(os.path.join(images_dir, "button.png"), "Play")
    create_button_icon(os.path.join(images_dir, "dark_button.png"), "Stop", "dark")
    create_button_icon(os.path.join(images_dir, "light_button.png"), "Pause", "light")

    # 4. Logo/banner
    create_logo(os.path.join(images_dir, "logo.png"))
    create_logo(os.path.join(images_dir, "dark_logo.png"), "dark")

    # 5. Animated GIF
    create_animated_gif(os.path.join(images_dir, "animation.gif"))
    create_animated_gif(os.path.join(images_dir, "dark_animation.gif"), "dark")

    # 6. Various shapes for transformation testing
    create_shape_icon(os.path.join(images_dir, "circle.png"), "circle")
    create_shape_icon(os.path.join(images_dir, "square.png"), "square")
    create_shape_icon(os.path.join(images_dir, "triangle.png"), "triangle")

    # 7. Colorful image for tint/saturation testing
    create_colorful_image(os.path.join(images_dir, "colorful.png"))

    print(f"Sample images created in '{images_dir}' directory")


def create_basic_icon(filepath):
    """Create a basic icon with a simple design."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a simple house icon
    # Base
    draw.rectangle(
        [10, 35, 54, 54],
        fill=(100, 150, 200, 255),
        outline=(50, 100, 150, 255),
        width=2,
    )
    # Roof
    draw.polygon(
        [(32, 10), (8, 35), (56, 35)],
        fill=(150, 100, 50, 255),
        outline=(100, 50, 25, 255),
    )
    # Door
    draw.rectangle([28, 42, 36, 54], fill=(80, 40, 20, 255))
    # Windows
    draw.rectangle(
        [15, 40, 22, 47], fill=(200, 200, 100, 255), outline=(150, 150, 50, 255)
    )
    draw.rectangle(
        [42, 40, 49, 47], fill=(200, 200, 100, 255), outline=(150, 150, 50, 255)
    )

    img.save(filepath)


def create_themed_icon(filepath, theme):
    """Create themed variants of icons."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if theme == "dark":
        # Dark theme colors
        primary = (200, 200, 200, 255)
        secondary = (150, 150, 150, 255)
        accent = (100, 150, 255, 255)
    else:  # light theme
        # Light theme colors
        primary = (50, 50, 50, 255)
        secondary = (100, 100, 100, 255)
        accent = (255, 100, 100, 255)

    # Draw a gear icon
    center = (32, 32)
    outer_radius = 25
    inner_radius = 15
    teeth = 8

    # Draw gear teeth
    for i in range(teeth):
        angle1 = math.radians(i * 360 / teeth)
        angle2 = math.radians((i + 0.3) * 360 / teeth)
        angle3 = math.radians((i + 0.7) * 360 / teeth)
        angle4 = math.radians((i + 1) * 360 / teeth)

        x1 = center[0] + outer_radius * math.cos(angle1)
        y1 = center[1] + outer_radius * math.sin(angle1)
        x2 = center[0] + (outer_radius + 5) * math.cos(angle2)
        y2 = center[1] + (outer_radius + 5) * math.sin(angle2)
        x3 = center[0] + (outer_radius + 5) * math.cos(angle3)
        y3 = center[1] + (outer_radius + 5) * math.sin(angle3)
        x4 = center[0] + outer_radius * math.cos(angle4)
        y4 = center[1] + outer_radius * math.sin(angle4)

        draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=primary)

    # Draw main circle
    draw.ellipse(
        [
            center[0] - outer_radius,
            center[1] - outer_radius,
            center[0] + outer_radius,
            center[1] + outer_radius,
        ],
        fill=primary,
        outline=secondary,
    )

    # Draw inner circle
    draw.ellipse(
        [
            center[0] - inner_radius,
            center[1] - inner_radius,
            center[0] + inner_radius,
            center[1] + inner_radius,
        ],
        fill=accent,
    )

    # Draw center hole
    draw.ellipse(
        [center[0] - 8, center[1] - 8, center[0] + 8, center[1] + 8], fill=(0, 0, 0, 0)
    )

    img.save(filepath)


def create_button_icon(filepath, text, theme="default"):
    """Create button-style icons with text."""
    img = Image.new("RGBA", (80, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if theme == "dark":
        bg_color = (60, 60, 60, 255)
        text_color = (220, 220, 220, 255)
        border_color = (100, 100, 100, 255)
    elif theme == "light":
        bg_color = (240, 240, 240, 255)
        text_color = (40, 40, 40, 255)
        border_color = (180, 180, 180, 255)
    else:
        bg_color = (100, 150, 200, 255)
        text_color = (255, 255, 255, 255)
        border_color = (70, 120, 170, 255)

    # Draw button background
    draw.rounded_rectangle(
        [2, 2, 78, 30], radius=5, fill=bg_color, outline=border_color, width=2
    )

    # Draw text (simplified - PIL's default font)
    try:
        # Try to get text bounds for centering
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (80 - text_width) // 2
        y = (32 - text_height) // 2
        draw.text((x, y), text, fill=text_color)
    except Exception:
        # Fallback if textbbox is not available
        draw.text((10, 10), text, fill=text_color)

    img.save(filepath)


def create_logo(filepath, theme="default"):
    """Create a logo/banner image."""
    img = Image.new("RGBA", (200, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if theme == "dark":
        bg_color = (40, 40, 40, 255)
        text_color = (220, 220, 220, 255)
        accent_color = (100, 150, 255, 255)
    else:
        bg_color = (250, 250, 250, 255)
        text_color = (50, 50, 50, 255)
        accent_color = (255, 100, 100, 255)

    # Background
    draw.rounded_rectangle([0, 0, 199, 59], radius=10, fill=bg_color)

    # Decorative elements
    draw.ellipse([10, 15, 30, 35], fill=accent_color)
    draw.ellipse([15, 20, 25, 30], fill=bg_color)

    # Text
    draw.text((45, 20), "IMG2RES", fill=text_color)

    img.save(filepath)


def create_animated_gif(filepath, theme="default"):
    """Create a simple animated GIF."""
    frames = []

    for i in range(8):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if theme == "dark":
            colors = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
        else:
            colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]

        # Rotating squares
        angle = i * 45
        center = (32, 32)
        size = 20

        # Calculate rotated square corners
        cos_a = math.cos(math.radians(angle))
        sin_a = math.sin(math.radians(angle))

        corners = []
        for dx, dy in [
            (-size // 2, -size // 2),
            (size // 2, -size // 2),
            (size // 2, size // 2),
            (-size // 2, size // 2),
        ]:
            x = center[0] + dx * cos_a - dy * sin_a
            y = center[1] + dx * sin_a + dy * cos_a
            corners.append((x, y))

        color_idx = i % len(colors)
        draw.polygon(corners, fill=colors[color_idx] + (255,))

        # Add a circle that pulses
        radius = 8 + 4 * math.sin(i * math.pi / 4)
        draw.ellipse(
            [
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ],
            fill=colors[(color_idx + 1) % len(colors)] + (200,),
        )

        frames.append(img)

    # Save as animated GIF
    frames[0].save(
        filepath,
        save_all=True,
        append_images=frames[1:],
        duration=150,
        loop=0,
        disposal=2,
    )


def create_shape_icon(filepath, shape):
    """Create simple shape icons for transformation testing."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if shape == "circle":
        draw.ellipse(
            [12, 12, 52, 52],
            fill=(255, 100, 100, 255),
            outline=(200, 50, 50, 255),
            width=3,
        )
    elif shape == "square":
        draw.rectangle(
            [12, 12, 52, 52],
            fill=(100, 255, 100, 255),
            outline=(50, 200, 50, 255),
            width=3,
        )
    elif shape == "triangle":
        draw.polygon(
            [(32, 12), (12, 52), (52, 52)],
            fill=(100, 100, 255, 255),
            outline=(50, 50, 200, 255),
        )

    img.save(filepath)


def create_colorful_image(filepath):
    """Create a colorful image for testing tint and saturation effects."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Create a rainbow-like pattern
    colors = [
        (255, 0, 0, 255),  # Red
        (255, 127, 0, 255),  # Orange
        (255, 255, 0, 255),  # Yellow
        (0, 255, 0, 255),  # Green
        (0, 0, 255, 255),  # Blue
        (75, 0, 130, 255),  # Indigo
        (148, 0, 211, 255),  # Violet
    ]

    # Draw colored stripes
    stripe_height = 64 // len(colors)
    for i, color in enumerate(colors):
        y1 = i * stripe_height
        y2 = (i + 1) * stripe_height
        draw.rectangle([0, y1, 64, y2], fill=color)

    # Add some geometric shapes
    draw.ellipse([10, 10, 30, 30], fill=(255, 255, 255, 200))
    draw.rectangle([34, 34, 54, 54], fill=(0, 0, 0, 200))

    img.save(filepath)


if __name__ == "__main__":
    create_sample_images()
