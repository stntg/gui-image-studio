"""
Tests for the unified image effects core.

This module tests all image processing functions to ensure consistency
between CLI and GUI operations.
"""

import pytest
from PIL import Image

from gui_image_studio.core.image_effects import (
    add_border,
    apply_blur,
    apply_brightness,
    apply_contrast,
    apply_format_conversion,
    apply_grayscale,
    apply_rotation,
    apply_saturation,
    apply_sharpness,
    apply_tint,
    apply_transformations,
    apply_transparency,
    create_thumbnail,
    crop_to_square,
    resize,
)


@pytest.fixture
def sample_image():
    """Create a sample RGBA image for testing."""
    return Image.new("RGBA", (100, 100), color=(255, 0, 0, 255))


@pytest.fixture
def sample_rgb_image():
    """Create a sample RGB image for testing."""
    return Image.new("RGB", (100, 100), color=(255, 0, 0))


class TestResize:
    """Test image resizing functionality."""

    def test_resize_basic(self, sample_image):
        """Test basic image resizing."""
        resized = resize(sample_image, (50, 50))
        assert resized.size == (50, 50)
        assert resized.mode == sample_image.mode

    def test_resize_preserve_aspect(self, sample_image):
        """Test resizing with aspect ratio preservation."""
        # Create a non-square image
        rect_image = Image.new("RGBA", (200, 100), color=(255, 0, 0, 255))
        resized = resize(rect_image, (50, 50), preserve_aspect=True)

        # Should be 50x25 to preserve 2:1 aspect ratio
        assert resized.size[0] <= 50
        assert resized.size[1] <= 50
        assert resized.size == (50, 25)

    def test_resize_upscale(self, sample_image):
        """Test upscaling an image."""
        resized = resize(sample_image, (200, 200))
        assert resized.size == (200, 200)


class TestColorTransformations:
    """Test color-related transformations."""

    def test_grayscale_conversion(self, sample_image):
        """Test grayscale conversion."""
        gray = apply_grayscale(sample_image)
        assert gray.mode == "RGBA"
        assert gray.size == sample_image.size

        # Check that it's actually grayscale (R=G=B)
        pixel = gray.getpixel((50, 50))
        assert pixel[0] == pixel[1] == pixel[2]  # R=G=B

    def test_contrast_adjustment(self, sample_image):
        """Test contrast adjustment."""
        # Increase contrast
        high_contrast = apply_contrast(sample_image, 2.0)
        assert high_contrast.size == sample_image.size
        assert high_contrast.mode == sample_image.mode

        # Decrease contrast
        low_contrast = apply_contrast(sample_image, 0.5)
        assert low_contrast.size == sample_image.size

        # Test edge cases
        with pytest.raises(ValueError):
            apply_contrast(sample_image, -1.0)

    def test_saturation_adjustment(self, sample_image):
        """Test saturation adjustment."""
        # Increase saturation
        high_sat = apply_saturation(sample_image, 2.0)
        assert high_sat.size == sample_image.size

        # Desaturate (grayscale)
        desaturated = apply_saturation(sample_image, 0.0)
        assert desaturated.size == sample_image.size

        # Test edge cases
        with pytest.raises(ValueError):
            apply_saturation(sample_image, -1.0)

    def test_brightness_adjustment(self, sample_image):
        """Test brightness adjustment."""
        # Increase brightness
        bright = apply_brightness(sample_image, 1.5)
        assert bright.size == sample_image.size

        # Decrease brightness
        dark = apply_brightness(sample_image, 0.5)
        assert dark.size == sample_image.size

        # Test edge cases
        with pytest.raises(ValueError):
            apply_brightness(sample_image, -1.0)

    def test_tint_application(self, sample_image):
        """Test color tinting."""
        # Apply blue tint
        tinted = apply_tint(sample_image, (0, 0, 255), 0.5)
        assert tinted.size == sample_image.size
        assert tinted.mode == "RGBA"

        # No tint (intensity = 0)
        no_tint = apply_tint(sample_image, (0, 0, 255), 0.0)
        assert no_tint.tobytes() == sample_image.tobytes()

        # Test edge cases
        with pytest.raises(ValueError):
            apply_tint(sample_image, (0, 0, 255), -0.1)

        with pytest.raises(ValueError):
            apply_tint(sample_image, (0, 0, 255), 1.1)


class TestGeometricTransformations:
    """Test geometric transformations."""

    def test_rotation(self, sample_image):
        """Test image rotation."""
        # 90-degree rotation
        rotated = apply_rotation(sample_image, 90)
        assert rotated.size == (100, 100)  # Square, so size unchanged

        # 45-degree rotation (should expand)
        rotated_45 = apply_rotation(sample_image, 45, expand=True)
        assert rotated_45.size[0] > 100  # Should be larger due to expansion
        assert rotated_45.size[1] > 100

        # No expansion
        rotated_no_expand = apply_rotation(sample_image, 45, expand=False)
        assert rotated_no_expand.size == (100, 100)

    def test_transparency(self, sample_image):
        """Test transparency adjustment."""
        # Semi-transparent
        semi_transparent = apply_transparency(sample_image, 0.5)
        assert semi_transparent.size == sample_image.size

        # Fully transparent
        transparent = apply_transparency(sample_image, 0.0)
        assert transparent.size == sample_image.size

        # Test edge cases
        with pytest.raises(ValueError):
            apply_transparency(sample_image, -0.1)

        with pytest.raises(ValueError):
            apply_transparency(sample_image, 1.1)


class TestFilters:
    """Test image filters."""

    def test_blur_filter(self, sample_image):
        """Test Gaussian blur."""
        blurred = apply_blur(sample_image, 5.0)
        assert blurred.size == sample_image.size
        assert blurred.mode == sample_image.mode

        # Blurred image should be different from original
        assert blurred.tobytes() != sample_image.tobytes()

        # No blur
        no_blur = apply_blur(sample_image, 0.0)
        assert no_blur.tobytes() == sample_image.tobytes()

        # Test edge cases
        with pytest.raises(ValueError):
            apply_blur(sample_image, -1.0)

    def test_sharpness_adjustment(self, sample_image):
        """Test sharpness adjustment."""
        # Increase sharpness
        sharp = apply_sharpness(sample_image, 2.0)
        assert sharp.size == sample_image.size

        # Decrease sharpness (blur)
        soft = apply_sharpness(sample_image, 0.5)
        assert soft.size == sample_image.size

        # Test edge cases
        with pytest.raises(ValueError):
            apply_sharpness(sample_image, -1.0)


class TestFormatConversion:
    """Test format conversion."""

    def test_format_conversion_png_to_jpeg(self, sample_image):
        """Test PNG to JPEG conversion."""
        jpeg_image = apply_format_conversion(sample_image, "JPEG")
        assert jpeg_image.mode == "RGB"  # JPEG doesn't support alpha

    def test_format_conversion_rgb_to_png(self, sample_rgb_image):
        """Test RGB to PNG conversion."""
        png_image = apply_format_conversion(sample_rgb_image, "PNG")
        assert png_image.size == sample_rgb_image.size


class TestCompositeTransformations:
    """Test the main transformation function."""

    def test_apply_transformations_single(self, sample_image):
        """Test applying a single transformation."""
        result = apply_transformations(sample_image, grayscale=True)

        # Should be grayscale
        pixel = result.getpixel((50, 50))
        assert pixel[0] == pixel[1] == pixel[2]

    def test_apply_transformations_multiple(self, sample_image):
        """Test applying multiple transformations."""
        result = apply_transformations(
            sample_image,
            size=(50, 50),
            rotate=90,
            grayscale=True,
            contrast=1.5,
            blur_radius=2.0,
        )

        assert result.size == (50, 50)
        # Should be grayscale
        pixel = result.getpixel((25, 25))
        assert pixel[0] == pixel[1] == pixel[2]

    def test_apply_transformations_with_tint(self, sample_image):
        """Test transformations with tinting."""
        result = apply_transformations(
            sample_image, tint_color=(0, 255, 0), tint_intensity=0.3  # Green tint
        )

        assert result.size == sample_image.size
        assert result.mode == "RGBA"

    def test_apply_transformations_no_changes(self, sample_image):
        """Test transformations with default values (no changes)."""
        result = apply_transformations(sample_image)

        # Should be identical to original
        assert result.size == sample_image.size
        assert result.mode == sample_image.mode


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_create_thumbnail(self, sample_image):
        """Test thumbnail creation."""
        thumbnail = create_thumbnail(sample_image, (32, 32))

        # Should be smaller or equal to requested size
        assert thumbnail.size[0] <= 32
        assert thumbnail.size[1] <= 32

        # For a square image, should be exactly 32x32
        assert thumbnail.size == (32, 32)

    def test_crop_to_square(self, sample_image):
        """Test square cropping."""
        # Test with already square image
        square = crop_to_square(sample_image)
        assert square.size == (100, 100)

        # Test with rectangular image
        rect_image = Image.new("RGBA", (200, 100), color=(255, 0, 0, 255))
        square_from_rect = crop_to_square(rect_image)
        assert square_from_rect.size == (100, 100)

    def test_add_border(self, sample_image):
        """Test border addition."""
        bordered = add_border(sample_image, 10, (255, 255, 255))

        # Should be larger by 2 * border_width
        assert bordered.size == (120, 120)
        assert bordered.mode == "RGBA"

        # Test with zero border width
        no_border = add_border(sample_image, 0)
        assert no_border.size == sample_image.size

        # Test with negative border width
        negative_border = add_border(sample_image, -5)
        assert negative_border.size == sample_image.size


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_transformations(self, sample_image):
        """Test with empty transformation dictionary."""
        result = apply_transformations(sample_image, **{})
        assert result.size == sample_image.size
        assert result.mode == sample_image.mode

    def test_chained_transformations_order(self, sample_image):
        """Test that transformation order matters."""
        # Resize then rotate
        result1 = apply_transformations(sample_image, size=(50, 50), rotate=45)

        # Should have been resized to 50x50, then rotated (expanding size)
        assert result1.size[0] >= 50
        assert result1.size[1] >= 50

    def test_extreme_values(self, sample_image):
        """Test with extreme but valid values."""
        # Very high contrast
        high_contrast = apply_transformations(sample_image, contrast=10.0)
        assert high_contrast.size == sample_image.size

        # Very low saturation
        desaturated = apply_transformations(sample_image, saturation=0.01)
        assert desaturated.size == sample_image.size

        # Large rotation
        rotated = apply_transformations(sample_image, rotate=720)  # Two full rotations
        assert rotated.size == sample_image.size


if __name__ == "__main__":
    pytest.main([__file__])
