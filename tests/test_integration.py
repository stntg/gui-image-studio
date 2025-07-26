"""
Integration tests to verify CLI and GUI use the same unified core.

This module tests that both interfaces produce identical results when given
the same input and transformation parameters.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from gui_image_studio.core.image_effects import apply_transformations
from gui_image_studio.core.io_utils import load_image, save_image
from gui_image_studio.image_loader import _apply_image_transformations
from gui_image_studio.image_studio.core.image_manager import ImageManager


@pytest.fixture
def sample_image():
    """Create a sample RGBA image for testing."""
    return Image.new("RGBA", (100, 100), color=(255, 0, 0, 255))


@pytest.fixture
def temp_image_file(sample_image):
    """Create a temporary image file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        sample_image.save(tmp.name, "PNG")
        yield Path(tmp.name)
        # Cleanup
        Path(tmp.name).unlink(missing_ok=True)


class TestCLIGUIConsistency:
    """Test that CLI and GUI produce identical results."""

    def test_cli_gui_transformation_consistency(self, sample_image):
        """Test that CLI and GUI transformations produce identical results."""
        # Define transformation parameters
        transforms = {
            "grayscale": True,
            "rotate": 45,
            "size": (50, 50),
            "contrast": 1.5,
            "saturation": 0.8,
            "blur_radius": 2.0,
        }

        # Apply transformations using CLI path (image_loader)
        cli_result = _apply_image_transformations(sample_image.copy(), **transforms)

        # Apply transformations using unified core directly
        core_result = apply_transformations(sample_image.copy(), **transforms)

        # Results should be identical
        assert cli_result.size == core_result.size
        assert cli_result.mode == core_result.mode

        # Compare pixel data (allowing for minor floating-point differences)
        cli_pixels = list(cli_result.getdata())
        core_pixels = list(core_result.getdata())

        assert len(cli_pixels) == len(core_pixels)

        # Check that most pixels are identical (allowing for minor rounding differences)
        identical_pixels = sum(1 for a, b in zip(cli_pixels, core_pixels) if a == b)
        similarity_ratio = identical_pixels / len(cli_pixels)
        assert similarity_ratio > 0.95  # At least 95% identical

    def test_gui_image_manager_uses_core(self, sample_image):
        """Test that GUI ImageManager uses the unified core."""
        manager = ImageManager()

        # Add image to manager
        manager.add_image("test_image", sample_image.copy())

        # Apply transformations through manager
        transforms = {
            "grayscale": True,
            "size": (75, 75),
            "contrast": 2.0,
        }

        manager.apply_transformations_to_image("test_image", **transforms)
        gui_result = manager.get_image("test_image")

        # Apply same transformations using core directly
        core_result = apply_transformations(sample_image.copy(), **transforms)

        # Results should be identical
        assert gui_result.size == core_result.size
        assert gui_result.mode == core_result.mode

        # Compare pixel data
        gui_pixels = list(gui_result.getdata())
        core_pixels = list(core_result.getdata())

        identical_pixels = sum(1 for a, b in zip(gui_pixels, core_pixels) if a == b)
        similarity_ratio = identical_pixels / len(gui_pixels)
        assert similarity_ratio > 0.95

    def test_file_io_consistency(self, sample_image, temp_image_file):
        """Test that file I/O operations are consistent."""
        # Load image using unified core
        loaded_image = load_image(temp_image_file)

        # Should be in RGBA mode and same size as original
        assert loaded_image.mode == "RGBA"
        assert loaded_image.size == sample_image.size

        # Test saving and reloading
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = Path(tmp.name)

        try:
            # Save using unified core
            save_image(loaded_image, output_path)

            # Reload and verify
            reloaded = load_image(output_path)
            assert reloaded.size == loaded_image.size
            assert reloaded.mode == loaded_image.mode

        finally:
            output_path.unlink(missing_ok=True)


class TestTransformationChaining:
    """Test that transformation chaining works consistently."""

    def test_transformation_order_consistency(self, sample_image):
        """Test that transformation order produces consistent results."""
        # Test different orders of the same transformations
        transforms1 = {
            "size": (80, 80),
            "rotate": 90,
            "grayscale": True,
        }

        # Apply all at once
        result1 = apply_transformations(sample_image.copy(), **transforms1)

        # Apply step by step in same order
        temp_image = sample_image.copy()
        temp_image = apply_transformations(temp_image, size=(80, 80))
        temp_image = apply_transformations(temp_image, rotate=90)
        result2 = apply_transformations(temp_image, grayscale=True)

        # Results should be identical
        assert result1.size == result2.size
        assert result1.mode == result2.mode

    def test_complex_transformation_chain(self, sample_image):
        """Test complex transformation chains."""
        transforms = {
            "size": (60, 60),
            "rotate": 30,
            "grayscale": True,
            "contrast": 1.8,
            "blur_radius": 1.5,
            "tint_color": (0, 255, 0),
            "tint_intensity": 0.2,
        }

        # Apply using CLI path
        cli_result = _apply_image_transformations(sample_image.copy(), **transforms)

        # Apply using core directly
        core_result = apply_transformations(sample_image.copy(), **transforms)

        # Should produce similar results
        assert cli_result.size == core_result.size
        assert cli_result.mode == core_result.mode


class TestErrorHandling:
    """Test error handling consistency between CLI and GUI."""

    def test_invalid_transformation_parameters(self, sample_image):
        """Test that invalid parameters raise consistent errors."""
        # Test invalid contrast value
        with pytest.raises(ValueError):
            apply_transformations(sample_image, contrast=-1.0)

        with pytest.raises(ValueError):
            _apply_image_transformations(sample_image, contrast=-1.0)

        # Test invalid tint intensity
        with pytest.raises(ValueError):
            apply_transformations(
                sample_image, tint_color=(255, 0, 0), tint_intensity=1.5
            )

    def test_file_not_found_error(self):
        """Test file not found error handling."""
        with pytest.raises(FileNotFoundError):
            load_image("nonexistent_file.png")

    def test_image_manager_error_handling(self):
        """Test ImageManager error handling."""
        manager = ImageManager()

        # Test applying transformations to non-existent image
        with pytest.raises(ValueError):
            manager.apply_transformations_to_image("nonexistent", grayscale=True)

        # Test getting non-existent image
        assert manager.get_image("nonexistent") is None


class TestPerformanceConsistency:
    """Test that performance characteristics are consistent."""

    def test_large_image_processing(self):
        """Test processing of larger images."""
        # Create a larger test image
        large_image = Image.new("RGBA", (500, 500), color=(128, 128, 128, 255))

        transforms = {
            "size": (250, 250),
            "blur_radius": 3.0,
            "contrast": 1.2,
        }

        # Both should handle large images without issues
        cli_result = _apply_image_transformations(large_image.copy(), **transforms)
        core_result = apply_transformations(large_image.copy(), **transforms)

        assert cli_result.size == (250, 250)
        assert core_result.size == (250, 250)
        assert cli_result.mode == core_result.mode

    def test_multiple_transformations_performance(self, sample_image):
        """Test that multiple sequential transformations work efficiently."""
        manager = ImageManager()
        manager.add_image("test", sample_image.copy())

        # Apply multiple transformations
        transformations = [
            {"size": (80, 80)},
            {"rotate": 15},
            {"contrast": 1.1},
            {"blur_radius": 0.5},
            {"saturation": 1.2},
        ]

        for transform in transformations:
            manager.apply_transformations_to_image("test", **transform)

        final_result = manager.get_image("test")
        assert final_result is not None
        assert final_result.size == (80, 80)


class TestBackwardCompatibility:
    """Test that existing APIs still work."""

    def test_image_loader_backward_compatibility(self, sample_image):
        """Test that existing image_loader functions still work."""
        # Test the old API still produces results
        result = _apply_image_transformations(
            sample_image, grayscale=True, size=(64, 64), rotate=45
        )

        assert result.size == (64, 64)
        assert result.mode == "RGBA"

    def test_image_manager_backward_compatibility(self, sample_image):
        """Test that ImageManager maintains backward compatibility."""
        manager = ImageManager()

        # Test old-style methods still work
        manager.add_image("test", sample_image)
        assert manager.get_image("test") is not None
        assert "test" in manager.list_images()

        # Test preview generation
        preview = manager.get_preview("test")
        assert preview is not None


if __name__ == "__main__":
    pytest.main([__file__])
