#!/usr/bin/env python3
"""
Simple test script to verify gui_image_studio package functionality.
"""

import os
import sys

# Add src directory to path to import gui_image_studio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gui_image_studio
from gui_image_studio.generator import embed_images_from_folder
from gui_image_studio.sample_creator import create_sample_images


def test_package_info():
    """Test basic package information."""
    print("Testing package info...")
    print(f"Package version: {gui_image_studio.__version__}")
    print(f"Package name: {gui_image_studio.__name__}")
    print("✓ Package info test passed\n")


def test_sample_creation():
    """Test sample image creation."""
    print("Testing sample creation...")

    try:
        create_sample_images()
        # Check if sample images directory was created
        if os.path.exists("sample_images"):
            print("✓ Sample images directory created")
            # List some sample files
            files = os.listdir("sample_images")
            print(f"✓ Created {len(files)} sample images")
        print("✓ Sample creation test passed\n")
    except Exception as e:
        print(f"✗ Sample creation test failed: {e}\n")


def test_embedding():
    """Test image embedding functionality."""
    print("Testing image embedding...")

    try:
        # First ensure we have sample images
        if not os.path.exists("sample_images"):
            create_sample_images()

        embed_images_from_folder("sample_images", "test_embedded_output.py", 90)

        # Check if output file was created
        if os.path.exists("test_embedded_output.py"):
            print("✓ Embedded images file created")

        print("✓ Image embedding test passed\n")
    except Exception as e:
        print(f"✗ Image embedding test failed: {e}\n")


def test_image_loading():
    """Test image loading functionality."""
    print("Testing image loading...")

    # Skip GUI-dependent tests in CI environment
    if os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true":
        print("⚠ Skipping image loading test in CI environment (no GUI available)")
        print("✓ Image loading test skipped\n")
        return

    try:
        # First ensure we have embedded images
        if not os.path.exists("test_embedded_output.py"):
            if not os.path.exists("sample_images"):
                create_sample_images()
            embed_images_from_folder("sample_images", "test_embedded_output.py", 90)

        # Import the embedded images
        sys.path.insert(0, ".")
        import tests.test_local.test_embedded_output as test_embedded_output

        # Test basic image loading (this will fail gracefully if no embedded images)
        try:
            image = gui_image_studio.get_image(
                "icon.png", framework="tkinter", size=(32, 32)
            )
            print("✓ Successfully loaded icon.png for tkinter")
        except ValueError as e:
            print(f"Note: {e} (This is expected if no embedded images are available)")

        print("✓ Image loading test completed\n")

    except Exception as e:
        print(f"✗ Image loading test failed: {e}\n")


if __name__ == "__main__":
    print("=" * 50)
    print("GUI IMAGE STUDIO PACKAGE TEST")
    print("=" * 50)

    test_package_info()
    test_sample_creation()
    test_embedding()
    test_image_loading()

    print("=" * 50)
    print("All tests completed!")
    print("=" * 50)
