#!/usr/bin/env python3
"""
Create icons for image effects.

This script generates appropriate icons for each image effect
following the same pattern as tool icons.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from src.gui_image_studio.core.io_utils import save_image
from src.gui_image_studio.core.sample_creation import SampleImageGenerator


def create_effect_icons():
    """Create icons for all image effects."""

    # Icon size and base settings
    icon_size = (32, 32)
    base_color = (100, 150, 200, 255)  # Default theme primary color

    # Output directory
    icons_dir = Path("src/gui_image_studio/image_studio/toolkit/icons/effects")
    icons_dir.mkdir(exist_ok=True)

    # Generator for creating base images
    generator = SampleImageGenerator("default")

    print("Creating effect icons...")

    # Enhancement effects
    create_brightness_icon(icons_dir, icon_size)
    create_contrast_icon(icons_dir, icon_size)
    create_sharpen_icon(icons_dir, icon_size)
    create_edge_enhance_icon(icons_dir, icon_size)

    # Color effects
    create_saturation_icon(icons_dir, icon_size)
    create_grayscale_icon(icons_dir, icon_size)
    create_sepia_icon(icons_dir, icon_size)
    create_invert_icon(icons_dir, icon_size)
    create_posterize_icon(icons_dir, icon_size)
    create_solarize_icon(icons_dir, icon_size)

    # Filter effects
    create_blur_icon(icons_dir, icon_size)
    create_emboss_icon(icons_dir, icon_size)

    # Geometry effects
    create_flip_horizontal_icon(icons_dir, icon_size)
    create_flip_vertical_icon(icons_dir, icon_size)
    create_rotate_icon(icons_dir, icon_size)

    print(f"✅ Created effect icons in: {icons_dir}")


def create_brightness_icon(icons_dir: Path, size: tuple):
    """Create brightness effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw sun-like symbol
    center = (size[0] // 2, size[1] // 2)
    radius = 8

    # Sun circle
    draw.ellipse(
        [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ],
        fill=(255, 255, 100, 255),
    )

    # Sun rays
    ray_length = 6
    for angle in range(0, 360, 45):
        import math

        x1 = center[0] + (radius + 2) * math.cos(math.radians(angle))
        y1 = center[1] + (radius + 2) * math.sin(math.radians(angle))
        x2 = center[0] + (radius + ray_length) * math.cos(math.radians(angle))
        y2 = center[1] + (radius + ray_length) * math.sin(math.radians(angle))
        draw.line([x1, y1, x2, y2], fill=(255, 255, 100, 255), width=2)

    save_image(img, icons_dir / "brightness.png")


def create_contrast_icon(icons_dir: Path, size: tuple):
    """Create contrast effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw half black, half white circle
    center = (size[0] // 2, size[1] // 2)
    radius = 12

    # Black half
    draw.pieslice(
        [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ],
        90,
        270,
        fill=(0, 0, 0, 255),
    )

    # White half
    draw.pieslice(
        [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ],
        270,
        90,
        fill=(255, 255, 255, 255),
    )

    # Border
    draw.ellipse(
        [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ],
        outline=(100, 100, 100, 255),
        width=1,
    )

    save_image(img, icons_dir / "contrast.png")


def create_saturation_icon(icons_dir: Path, size: tuple):
    """Create saturation effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw colorful gradient circles
    center = (size[0] // 2, size[1] // 2)
    colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255)]

    for i, color in enumerate(colors):
        offset_x = (i - 1) * 6
        offset_y = (i - 1) * 3
        radius = 8
        draw.ellipse(
            [
                center[0] + offset_x - radius,
                center[1] + offset_y - radius,
                center[0] + offset_x + radius,
                center[1] + offset_y + radius,
            ],
            fill=color,
        )

    save_image(img, icons_dir / "saturation.png")


def create_blur_icon(icons_dir: Path, size: tuple):
    """Create blur effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw sharp and blurred elements
    # Sharp rectangle
    draw.rectangle([4, 4, 14, 14], fill=(100, 150, 200, 255))

    # Blurred rectangle (simulated with multiple overlapping rectangles)
    blur_color = (100, 150, 200, 100)
    for offset in range(3):
        draw.rectangle(
            [18 + offset, 18 + offset, 28 + offset, 28 + offset], fill=blur_color
        )

    save_image(img, icons_dir / "blur.png")


def create_sharpen_icon(icons_dir: Path, size: tuple):
    """Create sharpen effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw sharp triangular shapes
    center = (size[0] // 2, size[1] // 2)

    # Sharp triangles
    points1 = [
        (center[0] - 8, center[1] + 6),
        (center[0], center[1] - 8),
        (center[0] + 8, center[1] + 6),
    ]
    draw.polygon(points1, fill=(100, 150, 200, 255))

    # Add sharp edges
    draw.line(
        [(center[0] - 8, center[1] + 6), (center[0], center[1] - 8)],
        fill=(255, 255, 255, 255),
        width=2,
    )
    draw.line(
        [(center[0], center[1] - 8), (center[0] + 8, center[1] + 6)],
        fill=(255, 255, 255, 255),
        width=2,
    )

    save_image(img, icons_dir / "sharpen.png")


def create_grayscale_icon(icons_dir: Path, size: tuple):
    """Create grayscale effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw gradient from black to white
    for x in range(size[0]):
        gray_value = int(255 * x / size[0])
        color = (gray_value, gray_value, gray_value, 255)
        draw.line([(x, 8), (x, size[1] - 8)], fill=color)

    save_image(img, icons_dir / "grayscale.png")


def create_sepia_icon(icons_dir: Path, size: tuple):
    """Create sepia effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw sepia-toned gradient
    sepia_colors = [(101, 67, 33, 255), (160, 120, 90, 255), (205, 175, 149, 255)]

    for i, color in enumerate(sepia_colors):
        x_start = i * (size[0] // 3)
        x_end = (i + 1) * (size[0] // 3)
        for x in range(x_start, x_end):
            draw.line([(x, 8), (x, size[1] - 8)], fill=color)

    save_image(img, icons_dir / "sepia.png")


def create_invert_icon(icons_dir: Path, size: tuple):
    """Create invert effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw inverted yin-yang style
    center = (size[0] // 2, size[1] // 2)
    radius = 12

    # White background circle
    draw.ellipse(
        [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ],
        fill=(255, 255, 255, 255),
    )

    # Black half
    draw.pieslice(
        [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ],
        0,
        180,
        fill=(0, 0, 0, 255),
    )

    save_image(img, icons_dir / "invert.png")


def create_flip_horizontal_icon(icons_dir: Path, size: tuple):
    """Create flip horizontal effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw arrow pointing left and right
    center_y = size[1] // 2

    # Left arrow
    draw.polygon(
        [(8, center_y), (16, center_y - 4), (16, center_y + 4)],
        fill=(100, 150, 200, 255),
    )

    # Right arrow
    draw.polygon(
        [(24, center_y), (16, center_y - 4), (16, center_y + 4)],
        fill=(100, 150, 200, 255),
    )

    # Vertical line in middle
    draw.line(
        [(size[0] // 2, 6), (size[0] // 2, size[1] - 6)],
        fill=(150, 150, 150, 255),
        width=2,
    )

    save_image(img, icons_dir / "flip_horizontal.png")


def create_flip_vertical_icon(icons_dir: Path, size: tuple):
    """Create flip vertical effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw arrow pointing up and down
    center_x = size[0] // 2

    # Up arrow
    draw.polygon(
        [(center_x, 8), (center_x - 4, 16), (center_x + 4, 16)],
        fill=(100, 150, 200, 255),
    )

    # Down arrow
    draw.polygon(
        [(center_x, 24), (center_x - 4, 16), (center_x + 4, 16)],
        fill=(100, 150, 200, 255),
    )

    # Horizontal line in middle
    draw.line(
        [(6, size[1] // 2), (size[0] - 6, size[1] // 2)],
        fill=(150, 150, 150, 255),
        width=2,
    )

    save_image(img, icons_dir / "flip_vertical.png")


def create_rotate_icon(icons_dir: Path, size: tuple):
    """Create rotate effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw circular arrow
    center = (size[0] // 2, size[1] // 2)
    radius = 10

    # Draw arc
    import math

    points = []
    for angle in range(45, 315, 10):
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] + radius * math.sin(math.radians(angle))
        points.append((x, y))

    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(100, 150, 200, 255), width=2)

    # Arrow head
    end_angle = 315
    x = center[0] + radius * math.cos(math.radians(end_angle))
    y = center[1] + radius * math.sin(math.radians(end_angle))

    # Arrow tip
    draw.polygon([(x, y), (x - 3, y - 3), (x - 3, y + 3)], fill=(100, 150, 200, 255))

    save_image(img, icons_dir / "rotate.png")


def create_posterize_icon(icons_dir: Path, size: tuple):
    """Create posterize effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw blocks of solid colors (poster effect)
    colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (255, 255, 0, 255)]
    block_size = size[0] // 2

    for i, color in enumerate(colors):
        x = (i % 2) * block_size
        y = (i // 2) * block_size
        draw.rectangle(
            [x + 2, y + 2, x + block_size - 2, y + block_size - 2], fill=color
        )

    save_image(img, icons_dir / "posterize.png")


def create_solarize_icon(icons_dir: Path, size: tuple):
    """Create solarize effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw wave pattern to represent solarization
    center_y = size[1] // 2

    import math

    points = []
    for x in range(size[0]):
        y = center_y + int(8 * math.sin(x * math.pi / 8))
        points.append((x, y))

    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(100, 150, 200, 255), width=2)

    # Add threshold line
    draw.line([(0, center_y), (size[0], center_y)], fill=(255, 100, 100, 255), width=1)

    save_image(img, icons_dir / "solarize.png")


def create_emboss_icon(icons_dir: Path, size: tuple):
    """Create emboss effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw 3D-looking rectangle
    # Base rectangle
    draw.rectangle([8, 8, 24, 24], fill=(128, 128, 128, 255))

    # Highlight (top-left)
    draw.line([(8, 8), (24, 8)], fill=(255, 255, 255, 255), width=2)
    draw.line([(8, 8), (8, 24)], fill=(255, 255, 255, 255), width=2)

    # Shadow (bottom-right)
    draw.line([(24, 8), (24, 24)], fill=(64, 64, 64, 255), width=2)
    draw.line([(8, 24), (24, 24)], fill=(64, 64, 64, 255), width=2)

    save_image(img, icons_dir / "emboss.png")


def create_edge_enhance_icon(icons_dir: Path, size: tuple):
    """Create edge enhance effect icon."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw shape with enhanced edges
    center = (size[0] // 2, size[1] // 2)

    # Base shape
    draw.rectangle(
        [center[0] - 8, center[1] - 8, center[0] + 8, center[1] + 8],
        fill=(100, 150, 200, 255),
    )

    # Enhanced edges (white outline)
    draw.rectangle(
        [center[0] - 8, center[1] - 8, center[0] + 8, center[1] + 8],
        outline=(255, 255, 255, 255),
        width=2,
    )

    # Additional edge lines
    draw.line(
        [(center[0] - 6, center[1] - 6), (center[0] + 6, center[1] - 6)],
        fill=(255, 255, 255, 255),
        width=1,
    )
    draw.line(
        [(center[0] - 6, center[1] + 6), (center[0] + 6, center[1] + 6)],
        fill=(255, 255, 255, 255),
        width=1,
    )

    save_image(img, icons_dir / "edge_enhance.png")


if __name__ == "__main__":
    create_effect_icons()
