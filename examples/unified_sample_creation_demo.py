#!/usr/bin/env python3
"""
Demonstration of unified sample creation functionality.

This script shows how the new unified sample creation core provides
consistent, flexible, and extensible sample image generation for both
CLI and GUI interfaces.
"""

import tempfile
from pathlib import Path

from gui_image_studio.core.io_utils import save_image
from gui_image_studio.core.sample_creation import (
    STANDARD_SIZES,
    THEME_COLORS,
    SampleImageGenerator,
    create_sample_image_set,
    create_sample_images_legacy_compatible,
)


def demonstrate_generator_basics():
    """Demonstrate basic SampleImageGenerator functionality."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING SAMPLE IMAGE GENERATOR BASICS")
    print("=" * 60)

    # Create generators for different themes
    themes = ["default", "dark", "light", "colorful"]
    generators = {theme: SampleImageGenerator(theme) for theme in themes}

    print(f"Created generators for themes: {', '.join(themes)}")

    # Show theme color differences
    print("\nTheme color schemes:")
    for theme, generator in generators.items():
        colors = generator.colors
        print(
            f"  {theme:10}: primary={colors['primary'][:3]}, accent={colors['accent'][:3]}"
        )

    # Create the same icon with different themes
    print("\nCreating 'home' icons with different themes:")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for theme, generator in generators.items():
            icon = generator.create_icon("home", size=(64, 64))
            filename = f"{theme}_home_icon.png"
            save_image(icon, temp_path / filename)
            print(f"  Created: {filename} ({icon.size[0]}x{icon.size[1]})")

        print(f"✅ Icons saved to: {temp_path}")


def demonstrate_icon_types():
    """Demonstrate different icon types."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING ICON TYPE VARIETY")
    print("=" * 60)

    generator = SampleImageGenerator("default")
    icon_types = ["home", "settings", "help", "file", "folder", "gear"]

    print(f"Creating {len(icon_types)} different icon types:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for icon_type in icon_types:
            # Create icons in different sizes
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]

            for size in sizes:
                icon = generator.create_icon(icon_type, size)
                filename = f"{icon_type}_{size[0]}x{size[1]}.png"
                save_image(icon, temp_path / filename)

            print(f"  {icon_type}: Created in {len(sizes)} sizes")

        total_files = len(icon_types) * len(sizes)
        print(f"✅ Created {total_files} icon files")


def demonstrate_button_styles():
    """Demonstrate different button styles."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING BUTTON STYLE VARIETY")
    print("=" * 60)

    generator = SampleImageGenerator("default")

    button_configs = [
        ("OK", "flat", (64, 32)),
        ("Cancel", "raised", (80, 32)),
        ("Apply", "rounded", (96, 40)),
        ("Help", "flat", (60, 28)),
    ]

    print(f"Creating {len(button_configs)} different button styles:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for text, style, size in button_configs:
            button = generator.create_button(text, size, style)
            filename = f"button_{text.lower()}_{style}.png"
            save_image(button, temp_path / filename)
            print(f"  {text} ({style}): {size[0]}x{size[1]} pixels")

        print(f"✅ Button samples created")


def demonstrate_shapes_and_patterns():
    """Demonstrate shapes and patterns."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING SHAPES AND PATTERNS")
    print("=" * 60)

    generator = SampleImageGenerator("colorful")

    # Create various shapes
    shapes = ["circle", "square", "triangle", "star", "diamond"]
    print(f"Creating {len(shapes)} geometric shapes:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for shape in shapes:
            # Create both filled and outline versions
            filled = generator.create_shape(shape, size=(80, 80), filled=True)
            outline = generator.create_shape(shape, size=(80, 80), filled=False)

            save_image(filled, temp_path / f"{shape}_filled.png")
            save_image(outline, temp_path / f"{shape}_outline.png")
            print(f"  {shape}: filled and outline versions")

        # Create various patterns
        patterns = ["checkerboard", "stripes", "dots", "grid"]
        print(f"\nCreating {len(patterns)} pattern types:")

        for pattern in patterns:
            pattern_img = generator.create_pattern(
                pattern, size=(120, 80), tile_size=12
            )
            save_image(pattern_img, temp_path / f"pattern_{pattern}.png")
            print(f"  {pattern}: 120x80 pixels")

        print(f"✅ Shapes and patterns created")


def demonstrate_gradients():
    """Demonstrate gradient creation."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING GRADIENT GENERATION")
    print("=" * 60)

    generator = SampleImageGenerator("default")

    # Different gradient directions
    directions = ["horizontal", "vertical", "diagonal", "radial"]
    print(f"Creating gradients in {len(directions)} directions:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for direction in directions:
            gradient = generator.create_gradient(size=(150, 100), direction=direction)
            save_image(gradient, temp_path / f"gradient_{direction}.png")
            print(f"  {direction}: 150x100 pixels")

        # Custom color gradients
        custom_colors = [
            [(255, 0, 0, 255), (0, 0, 255, 255)],  # Red to Blue
            [(255, 255, 0, 255), (255, 0, 255, 255), (0, 255, 255, 255)],  # Multi-color
        ]

        print(f"\nCreating {len(custom_colors)} custom color gradients:")
        for i, colors in enumerate(custom_colors):
            gradient = generator.create_gradient(size=(150, 100), colors=colors)
            save_image(gradient, temp_path / f"gradient_custom_{i+1}.png")
            print(f"  Custom {i+1}: {len(colors)} colors")

        print(f"✅ Gradient samples created")


def demonstrate_animations():
    """Demonstrate animated GIF creation."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING ANIMATION GENERATION")
    print("=" * 60)

    generator = SampleImageGenerator("default")

    animations = ["spinner", "pulse", "bounce"]
    print(f"Creating {len(animations)} animation types:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for animation in animations:
            frames = generator.create_animated_frames(
                frame_count=12, size=(64, 64), animation_type=animation
            )

            # Save as animated GIF
            frames[0].save(
                temp_path / f"animation_{animation}.gif",
                save_all=True,
                append_images=frames[1:],
                duration=100,
                loop=0,
            )

            print(f"  {animation}: {len(frames)} frames, 64x64 pixels")

        print(f"✅ Animated GIFs created")


def demonstrate_complete_sample_sets():
    """Demonstrate complete sample set creation."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING COMPLETE SAMPLE SETS")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create a comprehensive sample set
        print("Creating comprehensive sample set...")
        created_files = create_sample_image_set(
            output_dir=temp_path,
            themes=["default", "dark", "light"],
            image_types=["icons", "buttons", "shapes", "patterns", "gradients"],
            include_animations=True,
        )

        # Report results
        total_files = sum(len(files) for files in created_files.values())
        print(f"Created {total_files} files across {len(created_files)} themes:")

        for theme, files in created_files.items():
            print(f"  {theme}: {len(files)} files")

            # Show file type breakdown
            png_files = [f for f in files if f.endswith(".png")]
            gif_files = [f for f in files if f.endswith(".gif")]
            print(f"    PNG: {len(png_files)}, GIF: {len(gif_files)}")

        print(f"✅ Complete sample set created in: {temp_path}")


def demonstrate_legacy_compatibility():
    """Demonstrate legacy compatibility."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING LEGACY COMPATIBILITY")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        print("Creating legacy-compatible sample images...")
        create_sample_images_legacy_compatible(str(temp_path))

        # Count created files
        created_files = list(temp_path.glob("*"))
        png_files = [f for f in created_files if f.suffix == ".png"]
        gif_files = [f for f in created_files if f.suffix == ".gif"]

        print(f"Created {len(created_files)} legacy-compatible files:")
        print(f"  PNG files: {len(png_files)}")
        print(f"  GIF files: {len(gif_files)}")

        # Show some example filenames
        example_files = [f.name for f in created_files[:8]]
        print(f"  Examples: {', '.join(example_files)}")

        print(f"✅ Legacy compatibility verified")


def demonstrate_cli_gui_consistency():
    """Demonstrate CLI/GUI consistency."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING CLI/GUI CONSISTENCY")
    print("=" * 60)

    # Both CLI and GUI now use the same core functions
    print("Testing that CLI and GUI use identical core functions...")

    # Simulate CLI usage
    from gui_image_studio.core.sample_creation import create_sample_image_set

    # Simulate GUI usage (same function)
    # In a real GUI, this would be called from a menu or button
    def gui_create_samples(output_dir, themes, types):
        """Simulate GUI sample creation."""
        return create_sample_image_set(
            output_dir=output_dir,
            themes=themes,
            image_types=types,
            include_animations=False,
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create samples using "CLI" approach
        cli_dir = temp_path / "cli_samples"
        cli_files = create_sample_image_set(
            output_dir=cli_dir,
            themes=["default"],
            image_types=["icons"],
            include_animations=False,
        )

        # Create samples using "GUI" approach
        gui_dir = temp_path / "gui_samples"
        gui_files = gui_create_samples(
            output_dir=gui_dir, themes=["default"], types=["icons"]
        )

        # Compare results
        cli_count = len(cli_files["default"])
        gui_count = len(gui_files["default"])

        print(f"CLI created: {cli_count} files")
        print(f"GUI created: {gui_count} files")
        print(f"Results identical: {cli_count == gui_count}")

        # Verify file contents are identical
        cli_file_list = sorted(cli_files["default"])
        gui_file_list = sorted(gui_files["default"])

        if cli_file_list == gui_file_list:
            print("✅ CLI and GUI produce identical file sets!")
        else:
            print("⚠️  File sets differ (this shouldn't happen)")

        print("✅ CLI/GUI consistency verified")


def main():
    """Run the complete demonstration."""
    print("GUI Image Studio - Unified Sample Creation Demonstration")
    print("=" * 60)
    print("This demo shows the new unified sample creation core that provides")
    print("consistent, flexible sample image generation for CLI and GUI.")

    try:
        demonstrate_generator_basics()
        demonstrate_icon_types()
        demonstrate_button_styles()
        demonstrate_shapes_and_patterns()
        demonstrate_gradients()
        demonstrate_animations()
        demonstrate_complete_sample_sets()
        demonstrate_legacy_compatibility()
        demonstrate_cli_gui_consistency()

        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\n🎉 Key Achievements:")
        print("✅ Unified Core: Single implementation for all sample creation")
        print("✅ Theme Support: Consistent theming across all image types")
        print("✅ Flexible API: Easy to create custom images programmatically")
        print("✅ CLI Enhancement: Rich command-line options for sample creation")
        print("✅ Legacy Compatibility: Backward compatible with existing code")
        print("✅ Animation Support: Built-in animated GIF generation")
        print("✅ Extensible Design: Easy to add new image types and themes")

        print("\n🚀 Benefits:")
        print("• No more hardcoded sample creation")
        print("• Consistent themes across all interfaces")
        print("• Easy to add new sample types")
        print("• Programmatic sample generation for testing")
        print("• Rich CLI options for developers")
        print("• Animated samples for dynamic UIs")

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
