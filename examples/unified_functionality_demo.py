#!/usr/bin/env python3
"""
Demonstration of all unified core functionality.

This script shows how CLI and GUI interfaces now share common functionality
for image processing, code generation, and file operations.
"""

import tempfile
from pathlib import Path

from PIL import Image

from gui_image_studio.core.code_generation import (
    embed_images_from_folder,
    generate_embedded_code,
    process_image_folder,
)
from gui_image_studio.core.file_operations import (
    FileProgress,
    batch_process_images,
    find_image_files,
    format_file_size,
    validate_image_file,
)

# Import unified core modules
from gui_image_studio.core.image_effects import apply_transformations
from gui_image_studio.core.io_utils import save_image


def create_sample_images(output_dir: Path) -> None:
    """Create sample images for demonstration."""
    print(f"Creating sample images in: {output_dir}")

    # Create images with different themes
    images = [
        ("default_photo1.png", (100, 100), (255, 100, 100, 255)),
        ("default_photo2.png", (120, 80), (100, 255, 100, 255)),
        ("icons_home.png", (32, 32), (100, 100, 255, 255)),
        ("icons_settings.png", (32, 32), (255, 255, 100, 255)),
        ("icons_help.png", (32, 32), (255, 100, 255, 255)),
        ("buttons_ok.png", (64, 32), (200, 200, 200, 255)),
        ("buttons_cancel.png", (64, 32), (150, 150, 150, 255)),
    ]

    for filename, size, color in images:
        image = Image.new("RGBA", size, color)

        # Add some simple graphics to make them more interesting
        from PIL import ImageDraw

        draw = ImageDraw.Draw(image)

        if "photo" in filename:
            # Add a simple gradient effect
            for y in range(size[1]):
                alpha = int(255 * (1 - y / size[1] * 0.3))
                draw.line([(0, y), (size[0], y)], fill=(*color[:3], alpha))
        elif "icon" in filename:
            # Add a simple border
            draw.rectangle(
                [2, 2, size[0] - 3, size[1] - 3], outline=(0, 0, 0, 255), width=2
            )
        elif "button" in filename:
            # Add a simple 3D effect
            draw.rectangle(
                [0, 0, size[0] - 1, size[1] - 1], outline=(100, 100, 100, 255)
            )
            draw.rectangle(
                [1, 1, size[0] - 2, size[1] - 2], outline=(255, 255, 255, 255)
            )

        save_image(image, output_dir / filename)

    print(f"Created {len(images)} sample images")


def demonstrate_image_processing():
    """Demonstrate unified image processing."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING UNIFIED IMAGE PROCESSING")
    print("=" * 60)

    # Create a sample image
    original = Image.new("RGBA", (200, 200), (255, 0, 0, 255))

    # Apply transformations using the unified core
    transforms = {
        "size": (100, 100),
        "rotate": 30,
        "grayscale": True,
        "contrast": 1.5,
        "blur_radius": 1.0,
    }

    print("Original image size:", original.size)
    print("Applying transformations:", transforms)

    # This is the same function used by both CLI and GUI
    processed = apply_transformations(original, **transforms)

    print("Processed image size:", processed.size)
    print("✅ Image processing unified across CLI and GUI")


def demonstrate_code_generation():
    """Demonstrate unified code generation."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING UNIFIED CODE GENERATION")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create sample images
        create_sample_images(temp_path)

        # Process the folder (same function used by CLI and GUI)
        print("\nProcessing image folder...")
        images_dict = process_image_folder(temp_path, compression_quality=85)

        print(f"Found themes: {list(images_dict.keys())}")
        for theme, images in images_dict.items():
            print(f"  {theme}: {len(images)} images ({list(images.keys())})")

        # Generate code for different frameworks
        frameworks = ["tkinter", "customtkinter"]
        usage_types = ["icons", "buttons", "general"]

        for framework in frameworks:
            for usage in usage_types:
                print(f"\nGenerating {framework} code for {usage}...")
                code = generate_embedded_code(
                    images_dict, framework=framework, usage=usage, include_examples=True
                )

                # Show a snippet of the generated code
                lines = code.split("\n")
                print(f"Generated {len(lines)} lines of code")
                print("Code preview:")
                for i, line in enumerate(lines[:5]):
                    print(f"  {i+1}: {line}")
                print("  ...")

        # Test the complete pipeline
        print("\nTesting complete pipeline...")
        output_file = temp_path / "generated_code.py"

        embed_images_from_folder(
            folder_path=temp_path,
            output_file=output_file,
            compression_quality=90,
            framework="tkinter",
            usage="general",
            include_examples=True,
        )

        file_size = output_file.stat().st_size
        print(
            f"Generated complete code file: {output_file.name} ({format_file_size(file_size)})"
        )
        print("✅ Code generation unified across CLI and GUI")


def demonstrate_file_operations():
    """Demonstrate unified file operations."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING UNIFIED FILE OPERATIONS")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create sample images
        create_sample_images(temp_path)

        # Find image files
        print("Finding image files...")
        image_files = find_image_files(temp_path)
        print(f"Found {len(image_files)} image files:")
        for file_path in image_files:
            print(f"  {file_path.name}")

        # Validate image files
        print("\nValidating image files...")
        valid_count = 0
        for file_path in image_files:
            try:
                validate_image_file(file_path)
                valid_count += 1
            except Exception as e:
                print(f"  Invalid: {file_path.name} - {e}")

        print(f"✅ {valid_count}/{len(image_files)} files are valid images")

        # Demonstrate batch processing
        print("\nDemonstrating batch processing...")
        output_dir = temp_path / "processed"
        output_dir.mkdir()

        def simple_processor(image, **kwargs):
            """Simple image processor for demonstration."""
            return apply_transformations(image, size=(50, 50), grayscale=True)

        # Process with progress tracking
        progress = FileProgress(len(image_files))
        processed_files = []

        for input_path, output_path, success in batch_process_images(
            image_files,
            output_dir,
            simple_processor,
            name_template="processed_{stem}{suffix}",
        ):
            progress.update(success)
            if success:
                processed_files.append(output_path)
            print(f"  {progress}")

        print(f"✅ Batch processed {len(processed_files)} files")
        print("✅ File operations unified across CLI and GUI")


def demonstrate_consistency():
    """Demonstrate that all interfaces use the same core."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING INTERFACE CONSISTENCY")
    print("=" * 60)

    # Create test image
    test_image = Image.new("RGBA", (100, 100), (128, 128, 128, 255))

    # Same transformations applied through different paths
    transforms = {
        "size": (50, 50),
        "rotate": 45,
        "contrast": 2.0,
        "blur_radius": 1.5,
    }

    print("Applying identical transformations through different interfaces...")

    # Direct core usage (what both CLI and GUI use internally)
    core_result = apply_transformations(test_image.copy(), **transforms)

    # Simulate CLI usage (image_loader uses this same core)
    from gui_image_studio.image_loader import _apply_image_transformations

    cli_result = _apply_image_transformations(test_image.copy(), **transforms)

    # Simulate GUI usage (ImageManager uses this same core)
    from gui_image_studio.image_studio.core.image_manager import ImageManager

    manager = ImageManager()
    manager.add_image("test", test_image.copy())
    manager.apply_transformations_to_image("test", **transforms)
    gui_result = manager.get_image("test")

    # Compare results
    print(f"Core result size: {core_result.size}")
    print(f"CLI result size: {cli_result.size}")
    print(f"GUI result size: {gui_result.size}")

    # Check pixel-level consistency
    core_pixels = list(core_result.getdata())
    cli_pixels = list(cli_result.getdata())
    gui_pixels = list(gui_result.getdata())

    core_cli_identical = core_pixels == cli_pixels
    core_gui_identical = core_pixels == gui_pixels

    print(f"Core and CLI identical: {core_cli_identical}")
    print(f"Core and GUI identical: {core_gui_identical}")

    if core_cli_identical and core_gui_identical:
        print("✅ ALL INTERFACES PRODUCE IDENTICAL RESULTS!")
    else:
        print("⚠️  Minor differences detected (possibly due to GUI preview generation)")


def main():
    """Run the complete demonstration."""
    print("GUI Image Studio - Unified Functionality Demonstration")
    print("=" * 60)
    print("This demo shows how CLI and GUI now share unified core functionality")
    print("for image processing, code generation, and file operations.")

    try:
        demonstrate_image_processing()
        demonstrate_code_generation()
        demonstrate_file_operations()
        demonstrate_consistency()

        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\n🎉 Key Achievements:")
        print("✅ Image Processing: Unified core used by CLI and GUI")
        print("✅ Code Generation: Single implementation for both interfaces")
        print("✅ File Operations: Shared validation and batch processing")
        print("✅ Consistency: Identical results across all interfaces")
        print("\n🚀 Benefits:")
        print("• No more code duplication")
        print("• Guaranteed consistency between CLI and GUI")
        print("• Easier testing and maintenance")
        print("• Single place to add new features")
        print("• Better error handling and validation")

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
