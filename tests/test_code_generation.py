"""
Tests for the unified code generation core.

This module tests the code generation functionality to ensure consistency
between CLI and GUI code generation operations.
"""

import tempfile
from pathlib import Path

import pytest
from PIL import Image

from gui_image_studio.core.code_generation import (
    embed_images_from_folder,
    generate_embedded_code,
    get_available_themes,
    get_images_in_theme,
    process_image_folder,
    validate_compression_quality,
)


@pytest.fixture
def sample_images_folder():
    """Create a temporary folder with sample images."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create sample images with different themes
        images = [
            ("default_image1.png", (50, 50), (255, 0, 0, 255)),
            ("default_image2.png", (60, 60), (0, 255, 0, 255)),
            ("icons_home.png", (32, 32), (0, 0, 255, 255)),
            ("icons_settings.png", (32, 32), (255, 255, 0, 255)),
            ("buttons_ok.png", (64, 32), (255, 0, 255, 255)),
        ]

        for filename, size, color in images:
            image = Image.new("RGBA", size, color)
            image.save(temp_path / filename, "PNG")

        yield temp_path


class TestImageFolderProcessing:
    """Test image folder processing functionality."""

    def test_process_image_folder_basic(self, sample_images_folder):
        """Test basic folder processing."""
        result = process_image_folder(sample_images_folder)

        # Should have three themes: default, icons, buttons
        assert len(result) == 3
        assert "default" in result
        assert "icons" in result
        assert "buttons" in result

        # Check image counts per theme
        assert len(result["default"]) == 2  # image1, image2
        assert len(result["icons"]) == 2  # home, settings
        assert len(result["buttons"]) == 1  # ok

        # Check that all values are base64 strings
        for theme, images in result.items():
            for key, data in images.items():
                assert isinstance(data, str)
                assert len(data) > 0

    def test_process_image_folder_quality_parameter(self, sample_images_folder):
        """Test compression quality parameter."""
        # Test different quality settings
        result_high = process_image_folder(sample_images_folder, compression_quality=95)
        result_low = process_image_folder(sample_images_folder, compression_quality=10)

        # Both should have same structure
        assert set(result_high.keys()) == set(result_low.keys())

        # For JPEG images, low quality should generally produce shorter base64 strings
        # (though this might not always be true for very small test images)
        assert len(result_high) > 0
        assert len(result_low) > 0

    def test_process_image_folder_invalid_quality(self, sample_images_folder):
        """Test invalid compression quality values."""
        with pytest.raises(ValueError):
            process_image_folder(sample_images_folder, compression_quality=0)

        with pytest.raises(ValueError):
            process_image_folder(sample_images_folder, compression_quality=101)

    def test_process_image_folder_nonexistent(self):
        """Test processing non-existent folder."""
        with pytest.raises(FileNotFoundError):
            process_image_folder("nonexistent_folder")

    def test_process_image_folder_empty(self):
        """Test processing empty folder."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = process_image_folder(temp_dir)
            assert result == {}


class TestCodeGeneration:
    """Test code generation functionality."""

    def test_generate_embedded_code_basic(self, sample_images_folder):
        """Test basic code generation."""
        images_dict = process_image_folder(sample_images_folder)
        code = generate_embedded_code(images_dict)

        # Check that code contains expected elements
        assert "EMBEDDED_IMAGES = {" in code
        assert "def load_image(" in code
        assert "import base64" in code
        assert "import tkinter as tk" in code

        # Check that all themes are included
        assert '"default"' in code
        assert '"icons"' in code
        assert '"buttons"' in code

    def test_generate_embedded_code_frameworks(self, sample_images_folder):
        """Test code generation for different frameworks."""
        images_dict = process_image_folder(sample_images_folder)

        # Test tkinter
        tkinter_code = generate_embedded_code(images_dict, framework="tkinter")
        assert "import tkinter as tk" in tkinter_code
        assert "customtkinter" not in tkinter_code

        # Test customtkinter
        ctk_code = generate_embedded_code(images_dict, framework="customtkinter")
        assert "import customtkinter as ctk" in ctk_code
        assert "import tkinter as tk" in ctk_code

    def test_generate_embedded_code_usage_types(self, sample_images_folder):
        """Test code generation for different usage types."""
        images_dict = process_image_folder(sample_images_folder)

        usage_types = ["icons", "buttons", "backgrounds", "general"]

        for usage in usage_types:
            code = generate_embedded_code(images_dict, usage=usage)
            assert f"# Generated tkinter code for {usage}" in code
            assert "def load_image(" in code

    def test_generate_embedded_code_no_examples(self, sample_images_folder):
        """Test code generation without examples."""
        images_dict = process_image_folder(sample_images_folder)

        with_examples = generate_embedded_code(images_dict, include_examples=True)
        without_examples = generate_embedded_code(images_dict, include_examples=False)

        # Code without examples should be shorter
        assert len(without_examples) < len(with_examples)
        assert "# Usage Examples" not in without_examples
        assert "if __name__ == '__main__':" not in without_examples


class TestFullPipeline:
    """Test the complete embed_images_from_folder pipeline."""

    def test_embed_images_from_folder_basic(self, sample_images_folder):
        """Test complete pipeline from folder to file."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            embed_images_from_folder(
                folder_path=sample_images_folder,
                output_file=output_file,
                compression_quality=85,
            )

            # Check that output file was created
            assert output_file.exists()

            # Check that file contains expected content
            content = output_file.read_text(encoding="utf-8")
            assert "EMBEDDED_IMAGES = {" in content
            assert "def load_image(" in content
            assert '"default"' in content
            assert '"icons"' in content

        finally:
            output_file.unlink(missing_ok=True)

    def test_embed_images_from_folder_with_options(self, sample_images_folder):
        """Test pipeline with various options."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            embed_images_from_folder(
                folder_path=sample_images_folder,
                output_file=output_file,
                compression_quality=75,
                framework="customtkinter",
                usage="buttons",
                include_examples=False,
            )

            content = output_file.read_text(encoding="utf-8")
            assert "# Generated customtkinter code for buttons" in content
            assert "import customtkinter as ctk" in content
            assert "# Usage Examples" not in content

        finally:
            output_file.unlink(missing_ok=True)

    def test_embed_images_from_folder_empty_folder(self):
        """Test pipeline with empty folder."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
                output_file = Path(tmp.name)

            try:
                with pytest.raises(ValueError, match="No valid images found"):
                    embed_images_from_folder(temp_dir, output_file)
            finally:
                output_file.unlink(missing_ok=True)


class TestUtilityFunctions:
    """Test utility functions."""

    def test_get_available_themes(self, sample_images_folder):
        """Test getting available themes."""
        images_dict = process_image_folder(sample_images_folder)
        themes = get_available_themes(images_dict)

        assert isinstance(themes, list)
        assert "default" in themes
        assert "icons" in themes
        assert "buttons" in themes
        assert len(themes) == 3

    def test_get_images_in_theme(self, sample_images_folder):
        """Test getting images in a specific theme."""
        images_dict = process_image_folder(sample_images_folder)

        default_images = get_images_in_theme(images_dict, "default")
        assert len(default_images) == 2
        assert "image1" in default_images
        assert "image2" in default_images

        icons_images = get_images_in_theme(images_dict, "icons")
        assert len(icons_images) == 2
        assert "home" in icons_images
        assert "settings" in icons_images

        # Test non-existent theme
        empty_images = get_images_in_theme(images_dict, "nonexistent")
        assert empty_images == []

    def test_validate_compression_quality(self):
        """Test compression quality validation."""
        # Valid values
        assert validate_compression_quality(1) == 1
        assert validate_compression_quality(50) == 50
        assert validate_compression_quality(100) == 100

        # Clamping
        assert validate_compression_quality(0) == 1
        assert validate_compression_quality(-10) == 1
        assert validate_compression_quality(150) == 100

        # Invalid type
        with pytest.raises(ValueError):
            validate_compression_quality("50")

        with pytest.raises(ValueError):
            validate_compression_quality(50.5)


class TestErrorHandling:
    """Test error handling in code generation."""

    def test_invalid_folder_path(self):
        """Test handling of invalid folder paths."""
        with pytest.raises(FileNotFoundError):
            process_image_folder("nonexistent/path")

    def test_invalid_output_path(self, sample_images_folder):
        """Test handling of invalid output paths."""
        # Try to write to a directory that can't be created
        invalid_path = Path("/invalid\0path/output.py")

        with pytest.raises(IOError):
            embed_images_from_folder(sample_images_folder, invalid_path)

    def test_corrupted_image_handling(self):
        """Test handling of corrupted image files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a fake image file with invalid content
            fake_image = temp_path / "fake.png"
            fake_image.write_bytes(b"This is not an image")

            # Should not crash, but should skip the invalid file
            result = process_image_folder(temp_path)
            assert result == {}


if __name__ == "__main__":
    pytest.main([__file__])
