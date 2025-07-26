#!/usr/bin/env python3
"""
Demonstration of the unified image processing core.

This script shows how both CLI and GUI interfaces use the same underlying
image processing functions, ensuring consistency and maintainability.
"""

import tempfile
from pathlib import Path

from PIL import Image

# Import the unified core
from gui_image_studio.core.image_effects import (
    add_border,
    apply_blur,
    apply_contrast,
    apply_grayscale,
    apply_rotation,
    apply_transformations,
    create_thumbnail,
    resize,
)
from gui_image_studio.core.io_utils import image_to_base64, load_image, save_image

# Import CLI and GUI components that use the core
from gui_image_studio.image_loader import _apply_image_transformations
from gui_image_studio.image_studio.core.image_manager import ImageManager


def create_sample_image() -> Image.Image:
    """Create a colorful sample image for demonstration."""
    # Create a gradient image
    image = Image.new("RGBA", (200, 200), color=(255, 255, 255, 255))

    # Add some colored rectangles
    from PIL import ImageDraw

    draw = ImageDraw.Draw(image)

    # Red rectangle
    draw.rectangle([20, 20, 80, 80], fill=(255, 0, 0, 255))

    # Green circle (approximated with ellipse)
    draw.ellipse([120, 20, 180, 80], fill=(0, 255, 0, 255))

    # Blue triangle (approximated with polygon)
    draw.polygon([(100, 120), (70, 180), (130, 180)], fill=(0, 0, 255, 255))

    # Yellow text
    try:
        from PIL import ImageFont

        # Try to use a default font, fall back to basic if not available
        font = ImageFont.load_default()
        draw.text((20, 150), "DEMO", fill=(255, 255, 0, 255), font=font)
    except:
        draw.text((20, 150), "DEMO", fill=(255, 255, 0, 255))

    return image


def demonstrate_core_functions():
    """Demonstrate individual core functions."""
    print("=== Demonstrating Core Functions ===")

    # Create sample image
    original = create_sample_image()
    print(f"Original image size: {original.size}")

    # Demonstrate resize
    resized = resize(original, (100, 100))
    print(f"Resized image size: {resized.size}")

    # Demonstrate blur
    blurred = apply_blur(original, radius=3.0)
    print("Applied blur with radius 3.0")

    # Demonstrate grayscale
    gray = apply_grayscale(original)
    print("Converted to grayscale")

    # Demonstrate rotation
    rotated = apply_rotation(original, 45)
    print(f"Rotated 45 degrees, new size: {rotated.size}")

    # Demonstrate contrast
    high_contrast = apply_contrast(original, 2.0)
    print("Applied high contrast (factor 2.0)")

    # Demonstrate thumbnail
    thumbnail = create_thumbnail(original, (64, 64))
    print(f"Created thumbnail size: {thumbnail.size}")

    # Demonstrate border
    bordered = add_border(original, 10, (255, 0, 255))  # Magenta border
    print(f"Added border, new size: {bordered.size}")

    return original


def demonstrate_composite_transformations(original):
    """Demonstrate composite transformations using apply_transformations."""
    print("\n=== Demonstrating Composite Transformations ===")

    # Define a complex set of transformations
    transforms = {
        "size": (150, 150),
        "rotate": 30,
        "contrast": 1.5,
        "saturation": 1.2,
        "blur_radius": 1.0,
        "tint_color": (255, 200, 0),  # Orange tint
        "tint_intensity": 0.1,
    }

    # Apply all transformations at once
    result = apply_transformations(original, **transforms)
    print(f"Applied composite transformations:")
    print(f"  - Resized to {transforms['size']}")
    print(f"  - Rotated {transforms['rotate']} degrees")
    print(f"  - Contrast factor {transforms['contrast']}")
    print(f"  - Saturation factor {transforms['saturation']}")
    print(f"  - Blur radius {transforms['blur_radius']}")
    print(f"  - Orange tint with intensity {transforms['tint_intensity']}")
    print(f"Final image size: {result.size}")

    return result, transforms


def demonstrate_cli_gui_consistency(original, transforms):
    """Demonstrate that CLI and GUI produce identical results."""
    print("\n=== Demonstrating CLI/GUI Consistency ===")

    # Apply transformations using CLI path (image_loader)
    cli_result = _apply_image_transformations(original.copy(), **transforms)

    # Apply transformations using core directly
    core_result = apply_transformations(original.copy(), **transforms)

    # Apply transformations using GUI path (ImageManager)
    manager = ImageManager()
    manager.add_image("demo", original.copy())
    manager.apply_transformations_to_image("demo", **transforms)
    gui_result = manager.get_image("demo")

    # Compare results
    print(f"CLI result size: {cli_result.size}")
    print(f"Core result size: {core_result.size}")
    print(f"GUI result size: {gui_result.size}")

    # Check if they're identical
    cli_pixels = list(cli_result.getdata())
    core_pixels = list(core_result.getdata())
    gui_pixels = list(gui_result.getdata())

    cli_core_identical = cli_pixels == core_pixels
    core_gui_identical = core_pixels == gui_pixels

    print(f"CLI and Core results identical: {cli_core_identical}")
    print(f"Core and GUI results identical: {core_gui_identical}")

    if cli_core_identical and core_gui_identical:
        print("✅ All three methods produce identical results!")
    else:
        # Calculate similarity percentages
        cli_core_similarity = sum(
            1 for a, b in zip(cli_pixels, core_pixels) if a == b
        ) / len(cli_pixels)
        core_gui_similarity = sum(
            1 for a, b in zip(core_pixels, gui_pixels) if a == b
        ) / len(core_pixels)
        print(f"CLI/Core similarity: {cli_core_similarity:.2%}")
        print(f"Core/GUI similarity: {core_gui_similarity:.2%}")

    return cli_result, core_result, gui_result


def demonstrate_file_operations(image):
    """Demonstrate file I/O operations."""
    print("\n=== Demonstrating File Operations ===")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Save image
        output_file = temp_path / "demo_output.png"
        save_image(image, output_file)
        print(f"Saved image to: {output_file}")
        print(f"File size: {output_file.stat().st_size} bytes")

        # Load image back
        loaded = load_image(output_file)
        print(f"Loaded image size: {loaded.size}")
        print(f"Loaded image mode: {loaded.mode}")

        # Test JPEG conversion
        jpeg_file = temp_path / "demo_output.jpg"
        save_image(image, jpeg_file, quality=85)
        print(f"Saved JPEG version: {jpeg_file}")
        print(f"JPEG file size: {jpeg_file.stat().st_size} bytes")

        # Test base64 conversion
        base64_data = image_to_base64(image, "PNG")
        print(f"Base64 encoded length: {len(base64_data)} characters")
        print(f"Base64 preview: {base64_data[:50]}...")


def demonstrate_error_handling():
    """Demonstrate error handling in the unified core."""
    print("\n=== Demonstrating Error Handling ===")

    sample = Image.new("RGBA", (50, 50), color=(255, 0, 0, 255))

    # Test invalid parameters
    try:
        apply_contrast(sample, -1.0)  # Invalid contrast
    except ValueError as e:
        print(f"✅ Caught expected error for invalid contrast: {e}")

    try:
        apply_transformations(
            sample, tint_color=(255, 0, 0), tint_intensity=1.5
        )  # Invalid intensity
    except ValueError as e:
        print(f"✅ Caught expected error for invalid tint intensity: {e}")

    # Test file not found
    try:
        load_image("nonexistent_file.png")
    except FileNotFoundError as e:
        print(f"✅ Caught expected error for missing file: {e}")

    # Test ImageManager error handling
    manager = ImageManager()
    try:
        manager.apply_transformations_to_image("nonexistent", grayscale=True)
    except ValueError as e:
        print(f"✅ Caught expected error for nonexistent image: {e}")


def main():
    """Run the complete demonstration."""
    print("GUI Image Studio - Unified Core Demonstration")
    print("=" * 50)

    # Create and demonstrate core functions
    original = demonstrate_core_functions()

    # Demonstrate composite transformations
    transformed, transforms = demonstrate_composite_transformations(original)

    # Demonstrate CLI/GUI consistency
    cli_result, core_result, gui_result = demonstrate_cli_gui_consistency(
        original, transforms
    )

    # Demonstrate file operations
    demonstrate_file_operations(transformed)

    # Demonstrate error handling
    demonstrate_error_handling()

    print("\n" + "=" * 50)
    print("Demonstration completed successfully!")
    print("\nKey Benefits of the Unified Core:")
    print("• Single source of truth for all image transformations")
    print("• Consistent behavior between CLI and GUI")
    print("• Easy to test and maintain")
    print("• Extensible for new effects")
    print("• Clean separation of concerns")


if __name__ == "__main__":
    main()
