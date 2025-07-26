"""
Tests for the I/O utilities module.

This module tests image loading and saving functionality.
"""

import base64
import tempfile
import time
from pathlib import Path

import pytest
from PIL import Image

from gui_image_studio.core.io_utils import (
    image_to_base64,
    image_to_bytes,
    load_image,
    load_image_from_base64,
    load_image_from_data,
    save_image,
)


def safe_unlink(path):
    """Safely unlink a file with retry for Windows."""
    for _ in range(3):
        try:
            Path(path).unlink(missing_ok=True)
            break
        except PermissionError:
            time.sleep(0.1)


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
        # Cleanup with retry for Windows
        safe_unlink(tmp.name)


class TestImageLoading:
    """Test image loading functionality."""

    def test_load_image_from_file(self, temp_image_file):
        """Test loading image from file path."""
        loaded = load_image(temp_image_file)
        assert loaded.mode == "RGBA"
        assert loaded.size == (100, 100)

    def test_load_image_from_string_path(self, temp_image_file):
        """Test loading image from string path."""
        loaded = load_image(str(temp_image_file))
        assert loaded.mode == "RGBA"
        assert loaded.size == (100, 100)

    def test_load_image_nonexistent_file(self):
        """Test loading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_image("nonexistent_file.png")

    def test_load_image_invalid_file(self):
        """Test loading invalid image file raises IOError."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"This is not an image")
            tmp.flush()

            with pytest.raises(IOError):
                load_image(tmp.name)

            safe_unlink(tmp.name)

    def test_load_image_from_data(self, sample_image):
        """Test loading image from raw bytes."""
        # Convert image to bytes
        from io import BytesIO

        with BytesIO() as buffer:
            sample_image.save(buffer, "PNG")
            image_data = buffer.getvalue()

        loaded = load_image_from_data(image_data)
        assert loaded.mode == "RGBA"
        assert loaded.size == (100, 100)

    def test_load_image_from_data_invalid(self):
        """Test loading invalid data raises IOError."""
        with pytest.raises(IOError):
            load_image_from_data(b"invalid image data")

    def test_load_image_from_base64(self, sample_image):
        """Test loading image from base64 string."""
        # Convert image to base64
        from io import BytesIO

        with BytesIO() as buffer:
            sample_image.save(buffer, "PNG")
            image_data = buffer.getvalue()
            base64_data = base64.b64encode(image_data).decode("utf-8")

        loaded = load_image_from_base64(base64_data)
        assert loaded.mode == "RGBA"
        assert loaded.size == (100, 100)

    def test_load_image_from_base64_invalid(self):
        """Test loading invalid base64 raises IOError."""
        with pytest.raises(IOError):
            load_image_from_base64("invalid base64 data")


class TestImageSaving:
    """Test image saving functionality."""

    def test_save_image_png(self, sample_image):
        """Test saving image as PNG."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = Path(tmp.name)

        try:
            save_image(sample_image, output_path)
            assert output_path.exists()

            # Verify the saved image
            loaded = Image.open(output_path)
            assert loaded.size == (100, 100)
        finally:
            safe_unlink(output_path)

    def test_save_image_jpeg(self, sample_image):
        """Test saving RGBA image as JPEG (should convert to RGB)."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            output_path = Path(tmp.name)

        try:
            save_image(sample_image, output_path, quality=90)
            assert output_path.exists()

            # Verify the saved image
            loaded = Image.open(output_path)
            assert loaded.mode == "RGB"  # Should be converted from RGBA
            assert loaded.size == (100, 100)
        finally:
            safe_unlink(output_path)

    def test_save_image_explicit_format(self, sample_image):
        """Test saving with explicit format parameter."""
        with tempfile.NamedTemporaryFile(suffix=".img", delete=False) as tmp:
            output_path = Path(tmp.name)

        try:
            save_image(sample_image, output_path, format="PNG")
            assert output_path.exists()

            # Verify the saved image
            loaded = Image.open(output_path)
            assert loaded.size == (100, 100)
        finally:
            safe_unlink(output_path)

    def test_save_image_create_directories(self, sample_image):
        """Test that save_image creates parent directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "subdir" / "image.png"

            save_image(sample_image, output_path)
            assert output_path.exists()
            assert output_path.parent.exists()

    def test_save_image_invalid_path(self, sample_image):
        """Test saving to invalid path raises IOError."""
        # Try to save to a directory that can't be created (invalid characters)
        # Use different invalid paths for different platforms
        import os

        if os.name == "nt":  # Windows
            invalid_path = Path("CON/image.png")  # CON is reserved on Windows
        else:  # Unix-like
            invalid_path = Path("/root/nonexistent/deeply/nested/path/image.png")

        with pytest.raises((IOError, OSError, ValueError)):
            save_image(sample_image, invalid_path)


class TestImageConversion:
    """Test image conversion utilities."""

    def test_image_to_bytes_png(self, sample_image):
        """Test converting image to PNG bytes."""
        image_bytes = image_to_bytes(sample_image, "PNG")
        assert isinstance(image_bytes, bytes)
        assert len(image_bytes) > 0

        # Verify the bytes can be loaded back
        loaded = load_image_from_data(image_bytes)
        assert loaded.size == (100, 100)
        assert loaded.mode == "RGBA"

    def test_image_to_bytes_jpeg(self, sample_image):
        """Test converting RGBA image to JPEG bytes."""
        image_bytes = image_to_bytes(sample_image, "JPEG", quality=80)
        assert isinstance(image_bytes, bytes)
        assert len(image_bytes) > 0

        # Verify the bytes can be loaded back
        loaded = load_image_from_data(image_bytes)
        assert loaded.size == (100, 100)
        # JPEG should not have alpha channel (RGB or similar)
        assert loaded.mode in ("RGB", "L")  # RGB or grayscale, no alpha

    def test_image_to_base64_png(self, sample_image):
        """Test converting image to base64 PNG."""
        base64_str = image_to_base64(sample_image, "PNG")
        assert isinstance(base64_str, str)
        assert len(base64_str) > 0

        # Verify the base64 can be loaded back
        loaded = load_image_from_base64(base64_str)
        assert loaded.size == (100, 100)
        assert loaded.mode == "RGBA"

    def test_image_to_base64_jpeg(self, sample_image):
        """Test converting RGBA image to base64 JPEG."""
        base64_str = image_to_base64(sample_image, "JPEG", quality=90)
        assert isinstance(base64_str, str)
        assert len(base64_str) > 0

        # Verify the base64 can be loaded back
        loaded = load_image_from_base64(base64_str)
        assert loaded.size == (100, 100)
        # JPEG should not have alpha channel (RGB or similar)
        assert loaded.mode in ("RGB", "L")  # RGB or grayscale, no alpha

    def test_conversion_roundtrip(self, sample_image):
        """Test full roundtrip: image -> bytes -> base64 -> image."""
        # Image to bytes
        image_bytes = image_to_bytes(sample_image, "PNG")

        # Bytes to base64
        base64_str = base64.b64encode(image_bytes).decode("utf-8")

        # Base64 back to image
        loaded = load_image_from_base64(base64_str)

        assert loaded.size == sample_image.size
        assert loaded.mode == sample_image.mode


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_load_rgb_image_converts_to_rgba(self):
        """Test that RGB images are converted to RGBA."""
        rgb_image = Image.new("RGB", (50, 50), color=(0, 255, 0))

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            rgb_image.save(tmp.name, "PNG")

            try:
                loaded = load_image(tmp.name)
                assert loaded.mode == "RGBA"
                assert loaded.size == (50, 50)
            finally:
                safe_unlink(tmp.name)

    def test_save_quality_parameter(self, sample_image):
        """Test JPEG quality parameter affects file size."""
        with tempfile.NamedTemporaryFile(
            suffix=".jpg", delete=False
        ) as tmp1, tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp2:

            path1 = Path(tmp1.name)
            path2 = Path(tmp2.name)

        try:
            # Save with high quality
            save_image(sample_image, path1, quality=95)

            # Save with low quality
            save_image(sample_image, path2, quality=10)

            # High quality should result in larger file
            assert path1.stat().st_size > path2.stat().st_size

        finally:
            safe_unlink(path1)
            safe_unlink(path2)

    def test_format_inference_from_extension(self, sample_image):
        """Test that format is correctly inferred from file extension."""
        test_cases = [
            (".png", "PNG"),
            (".jpg", "JPEG"),
            (".jpeg", "JPEG"),
            (".bmp", "BMP"),
        ]

        for ext, expected_format in test_cases:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                output_path = Path(tmp.name)

            try:
                save_image(sample_image, output_path)
                assert output_path.exists()

                # For JPEG, verify RGB conversion happened
                if expected_format == "JPEG":
                    loaded = Image.open(output_path)
                    assert loaded.mode == "RGB"

            finally:
                safe_unlink(output_path)


if __name__ == "__main__":
    pytest.main([__file__])
