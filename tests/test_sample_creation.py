"""
Tests for the unified sample creation core.

This module tests the sample creation functionality to ensure consistency
and proper generation of various image types and themes.
"""

import tempfile
from pathlib import Path

import pytest
from PIL import Image

from gui_image_studio.core.sample_creation import (
    STANDARD_SIZES,
    THEME_COLORS,
    SampleImageGenerator,
    create_sample_image_set,
    create_sample_images_legacy_compatible,
)


class TestSampleImageGenerator:
    """Test the SampleImageGenerator class."""

    def test_generator_initialization(self):
        """Test generator initialization with different themes."""
        # Default theme
        gen_default = SampleImageGenerator()
        assert gen_default.theme == "default"
        assert gen_default.colors == THEME_COLORS["default"]

        # Dark theme
        gen_dark = SampleImageGenerator("dark")
        assert gen_dark.theme == "dark"
        assert gen_dark.colors == THEME_COLORS["dark"]

        # Invalid theme falls back to default
        gen_invalid = SampleImageGenerator("nonexistent")
        assert gen_invalid.theme == "nonexistent"
        assert gen_invalid.colors == THEME_COLORS["default"]

    def test_create_icon_basic(self):
        """Test basic icon creation."""
        generator = SampleImageGenerator("default")

        # Test different icon types
        icon_types = ["home", "settings", "help", "file", "folder", "gear"]

        for icon_type in icon_types:
            icon = generator.create_icon(icon_type)

            assert isinstance(icon, Image.Image)
            assert icon.size == (32, 32)  # Default icon size
            assert icon.mode == "RGBA"

            # Check that the image is not completely transparent
            pixels = list(icon.getdata())
            non_transparent = [p for p in pixels if p[3] > 0]
            assert (
                len(non_transparent) > 0
            ), f"Icon {icon_type} is completely transparent"

    def test_create_icon_custom_size(self):
        """Test icon creation with custom sizes."""
        generator = SampleImageGenerator("default")

        sizes = [(16, 16), (48, 48), (64, 64), (128, 128)]

        for size in sizes:
            icon = generator.create_icon("home", size)
            assert icon.size == size

    def test_create_button_basic(self):
        """Test basic button creation."""
        generator = SampleImageGenerator("default")

        # Test different button styles
        styles = ["flat", "raised", "rounded"]

        for style in styles:
            button = generator.create_button("Test", style=style)

            assert isinstance(button, Image.Image)
            assert button.size == (64, 32)  # Default button size
            assert button.mode == "RGBA"

            # Check that the button has content
            pixels = list(button.getdata())
            non_transparent = [p for p in pixels if p[3] > 0]
            assert (
                len(non_transparent) > 0
            ), f"Button style {style} is completely transparent"

    def test_create_button_custom_text_size(self):
        """Test button creation with custom text and size."""
        generator = SampleImageGenerator("default")

        button = generator.create_button("Custom Button", size=(100, 50))
        assert button.size == (100, 50)

    def test_create_shape_basic(self):
        """Test basic shape creation."""
        generator = SampleImageGenerator("default")

        shapes = ["circle", "square", "triangle", "star", "diamond"]

        for shape in shapes:
            # Test filled shapes
            filled_shape = generator.create_shape(shape, filled=True)
            assert isinstance(filled_shape, Image.Image)
            assert filled_shape.size == (64, 64)  # Default size
            assert filled_shape.mode == "RGBA"

            # Test outline shapes
            outline_shape = generator.create_shape(shape, filled=False)
            assert isinstance(outline_shape, Image.Image)
            assert outline_shape.size == (64, 64)

            # Both should have content
            for img in [filled_shape, outline_shape]:
                pixels = list(img.getdata())
                non_transparent = [p for p in pixels if p[3] > 0]
                assert (
                    len(non_transparent) > 0
                ), f"Shape {shape} is completely transparent"

    def test_create_gradient_basic(self):
        """Test basic gradient creation."""
        generator = SampleImageGenerator("default")

        directions = ["horizontal", "vertical", "diagonal", "radial"]

        for direction in directions:
            gradient = generator.create_gradient(direction=direction)

            assert isinstance(gradient, Image.Image)
            assert gradient.size == (200, 150)  # Default size
            assert gradient.mode == "RGBA"

            # Check that gradient has variation (not solid color)
            pixels = list(gradient.getdata())
            unique_colors = set(pixels)
            assert (
                len(unique_colors) > 1
            ), f"Gradient {direction} appears to be solid color"

    def test_create_gradient_custom_colors(self):
        """Test gradient creation with custom colors."""
        generator = SampleImageGenerator("default")

        custom_colors = [
            (255, 0, 0, 255),  # Red
            (0, 255, 0, 255),  # Green
            (0, 0, 255, 255),  # Blue
        ]

        gradient = generator.create_gradient(colors=custom_colors)
        assert isinstance(gradient, Image.Image)

        # Check that the gradient contains colors similar to our input
        pixels = list(gradient.getdata())

        # Should have some reddish pixels
        red_pixels = [p for p in pixels if p[0] > 200 and p[1] < 100 and p[2] < 100]
        assert len(red_pixels) > 0, "Gradient doesn't contain red pixels"

    def test_create_pattern_basic(self):
        """Test basic pattern creation."""
        generator = SampleImageGenerator("default")

        patterns = ["checkerboard", "stripes", "dots", "grid"]

        for pattern in patterns:
            pattern_img = generator.create_pattern(pattern)

            assert isinstance(pattern_img, Image.Image)
            assert pattern_img.size == (200, 150)  # Default size
            assert pattern_img.mode == "RGBA"

            # Patterns should have variation
            pixels = list(pattern_img.getdata())
            unique_colors = set(pixels)
            assert (
                len(unique_colors) > 1
            ), f"Pattern {pattern} appears to be solid color"

    def test_create_animated_frames(self):
        """Test animated frame creation."""
        generator = SampleImageGenerator("default")

        animations = ["spinner", "pulse", "bounce"]

        for animation in animations:
            frames = generator.create_animated_frames(animation_type=animation)

            assert isinstance(frames, list)
            assert len(frames) == 8  # Default frame count

            for i, frame in enumerate(frames):
                assert isinstance(frame, Image.Image)
                assert frame.size == (64, 64)  # Default size
                assert frame.mode == "RGBA"

                # Each frame should have content
                pixels = list(frame.getdata())
                non_transparent = [p for p in pixels if p[3] > 0]
                assert (
                    len(non_transparent) > 0
                ), f"Frame {i} of {animation} is transparent"

            # Frames should be different from each other
            frame_data = [list(frame.getdata()) for frame in frames]
            unique_frames = set(tuple(data) for data in frame_data)
            assert len(unique_frames) > 1, f"Animation {animation} frames are identical"


class TestThemeConsistency:
    """Test that different themes produce consistent but different results."""

    def test_theme_color_differences(self):
        """Test that different themes use different colors."""
        themes = ["default", "dark", "light", "colorful"]
        generators = [SampleImageGenerator(theme) for theme in themes]

        # Create the same icon with different themes
        icons = [gen.create_icon("home") for gen in generators]

        # Convert to pixel data for comparison
        icon_data = [list(icon.getdata()) for icon in icons]

        # All icons should be different
        for i in range(len(icon_data)):
            for j in range(i + 1, len(icon_data)):
                assert (
                    icon_data[i] != icon_data[j]
                ), f"Themes {themes[i]} and {themes[j]} produce identical icons"

    def test_theme_structure_consistency(self):
        """Test that different themes maintain the same structure."""
        themes = ["default", "dark", "light"]

        for theme in themes:
            generator = SampleImageGenerator(theme)

            # All themes should be able to create the same types of content
            icon = generator.create_icon("home")
            button = generator.create_button("Test")
            shape = generator.create_shape("circle")
            gradient = generator.create_gradient()
            pattern = generator.create_pattern("checkerboard")

            # All should be valid images
            for img in [icon, button, shape, gradient, pattern]:
                assert isinstance(img, Image.Image)
                assert img.mode == "RGBA"


class TestSampleImageSet:
    """Test the complete sample image set creation."""

    def test_create_sample_image_set_basic(self):
        """Test basic sample image set creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            created_files = create_sample_image_set(temp_dir)

            # Should return a dictionary
            assert isinstance(created_files, dict)

            # Should have default themes
            expected_themes = ["default", "dark", "light"]
            assert set(created_files.keys()) == set(expected_themes)

            # Each theme should have files
            for theme, files in created_files.items():
                assert isinstance(files, list)
                assert len(files) > 0

                # Check that files actually exist
                for filename in files:
                    file_path = Path(temp_dir) / filename
                    assert file_path.exists(), f"File {filename} was not created"

                    # Verify it's a valid image
                    with Image.open(file_path) as img:
                        assert img.mode in ["RGBA", "RGB", "P"]  # Valid image modes

    def test_create_sample_image_set_custom_options(self):
        """Test sample image set creation with custom options."""
        with tempfile.TemporaryDirectory() as temp_dir:
            created_files = create_sample_image_set(
                output_dir=temp_dir,
                themes=["dark", "colorful"],
                image_types=["icons", "shapes"],
                include_animations=False,
            )

            # Should only have requested themes
            assert set(created_files.keys()) == {"dark", "colorful"}

            # Should not have animation files
            all_files = []
            for files in created_files.values():
                all_files.extend(files)

            gif_files = [f for f in all_files if f.endswith(".gif")]
            assert len(gif_files) == 0, "Found GIF files when animations disabled"

    def test_create_sample_image_set_with_animations(self):
        """Test sample image set creation with animations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            created_files = create_sample_image_set(
                output_dir=temp_dir,
                themes=["default"],
                image_types=["icons"],
                include_animations=True,
            )

            # Should have animation files
            all_files = []
            for files in created_files.values():
                all_files.extend(files)

            gif_files = [f for f in all_files if f.endswith(".gif")]
            assert len(gif_files) > 0, "No GIF files found when animations enabled"

            # Verify GIF files are valid
            for gif_file in gif_files:
                file_path = Path(temp_dir) / gif_file
                with Image.open(file_path) as img:
                    assert img.format == "GIF"
                    assert img.is_animated


class TestLegacyCompatibility:
    """Test legacy compatibility functions."""

    def test_create_sample_images_legacy_compatible(self):
        """Test legacy-compatible sample creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            create_sample_images_legacy_compatible(temp_dir)

            temp_path = Path(temp_dir)

            # Check for expected legacy files
            expected_files = [
                "icon.png",
                "dark_icon.png",
                "light_icon.png",
                "button.png",
                "dark_button.png",
                "light_button.png",
                "logo.png",
                "dark_logo.png",
                "circle.png",
                "square.png",
                "triangle.png",
                "colorful.png",
                "animation.gif",
                "dark_animation.gif",
            ]

            for filename in expected_files:
                file_path = temp_path / filename
                assert file_path.exists(), f"Legacy file {filename} was not created"

                # Verify it's a valid image
                with Image.open(file_path) as img:
                    assert img.mode in ["RGBA", "RGB", "P"]


class TestConstants:
    """Test module constants and configurations."""

    def test_theme_colors_structure(self):
        """Test that theme colors have consistent structure."""
        required_keys = ["primary", "secondary", "accent", "background", "text"]

        for theme_name, colors in THEME_COLORS.items():
            assert isinstance(colors, dict), f"Theme {theme_name} colors is not a dict"

            for key in required_keys:
                assert key in colors, f"Theme {theme_name} missing color key: {key}"

                color = colors[key]
                assert isinstance(
                    color, tuple
                ), f"Color {key} in theme {theme_name} is not a tuple"
                assert len(color) == 4, f"Color {key} in theme {theme_name} is not RGBA"

                # All color values should be 0-255
                for component in color:
                    assert (
                        0 <= component <= 255
                    ), f"Invalid color component in {theme_name}.{key}: {component}"

    def test_standard_sizes_structure(self):
        """Test that standard sizes are properly defined."""
        for size_name, size in STANDARD_SIZES.items():
            assert isinstance(size, tuple), f"Size {size_name} is not a tuple"
            assert len(size) == 2, f"Size {size_name} is not a 2-tuple"
            assert all(
                isinstance(dim, int) and dim > 0 for dim in size
            ), f"Invalid dimensions in {size_name}"


if __name__ == "__main__":
    pytest.main([__file__])
