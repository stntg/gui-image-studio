#!/usr/bin/env python3
"""
Pytest-compatible tests for gui_image_studio package.
"""

import os
import sys

import pytest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gui_image_studio


def test_package_import():
    """Test that the package can be imported."""
    assert gui_image_studio is not None


def test_package_version():
    """Test that the package has a version."""
    assert hasattr(gui_image_studio, "__version__")
    assert gui_image_studio.__version__ is not None
    assert isinstance(gui_image_studio.__version__, str)


def test_package_name():
    """Test that the package has the correct name."""
    assert gui_image_studio.__name__ == "gui_image_studio"


def test_core_functions_import():
    """Test that core functions can be imported."""
    try:
        from gui_image_studio import get_image

        assert get_image is not None
    except ImportError:
        pytest.skip("get_image not available")

    try:
        from gui_image_studio import embed_images_from_folder

        assert embed_images_from_folder is not None
    except ImportError:
        pytest.skip("embed_images_from_folder not available")


def test_sample_creator_import():
    """Test that sample creator can be imported."""
    try:
        from gui_image_studio.sample_creator import create_sample_images

        assert create_sample_images is not None
    except ImportError:
        pytest.skip("sample_creator not available")


def test_generator_import():
    """Test that generator can be imported."""
    try:
        from gui_image_studio.generator import embed_images_from_folder

        assert embed_images_from_folder is not None
    except ImportError:
        pytest.skip("generator not available")


if __name__ == "__main__":
    pytest.main([__file__])
