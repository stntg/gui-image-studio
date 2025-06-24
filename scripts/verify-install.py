#!/usr/bin/env python3
"""
Installation Verification Script for GUI Image Studio

This script verifies that GUI Image Studio is properly installed and all
components are working correctly.
"""

import importlib
import sys
import traceback
from pathlib import Path


def test_basic_import():
    """Test basic package import."""
    print("Testing basic package import...")
    try:
        import gui_image_studio

        print(f"✓ Successfully imported gui_image_studio")
        print(f"✓ Version: {gui_image_studio.__version__}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import gui_image_studio: {e}")
        return False


def test_submodule_imports():
    """Test importing all submodules."""
    print("\nTesting submodule imports...")
    modules = [
        "gui_image_studio.image_studio",
        "gui_image_studio.generator",
        "gui_image_studio.image_loader",
        "gui_image_studio.embedded_images",
        "gui_image_studio.sample_creator",
        "gui_image_studio.cli",
    ]

    success_count = 0
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
            success_count += 1
        except ImportError as e:
            print(f"✗ {module}: {e}")
        except Exception as e:
            print(f"⚠ {module}: {e}")

    print(f"\nSubmodule import results: {success_count}/{len(modules)} successful")
    return success_count == len(modules)


def test_dependencies():
    """Test that all required dependencies are available."""
    print("\nTesting dependencies...")
    dependencies = [
        ("PIL", "Pillow"),
        ("tkinter", "tkinter (built-in)"),
    ]

    optional_dependencies = [
        ("customtkinter", "CustomTkinter"),
    ]

    success_count = 0
    total_count = len(dependencies)

    # Test required dependencies
    for module, name in dependencies:
        try:
            importlib.import_module(module)
            print(f"✓ {name}")
            success_count += 1
        except ImportError:
            print(f"✗ {name} (required)")

    # Test optional dependencies
    for module, name in optional_dependencies:
        try:
            importlib.import_module(module)
            print(f"✓ {name} (optional)")
        except ImportError:
            print(f"⚠ {name} (optional, not installed)")

    print(
        f"\nDependency results: {success_count}/{total_count} required dependencies available"
    )
    return success_count == total_count


def test_image_processing():
    """Test basic image processing functionality."""
    print("\nTesting image processing functionality...")
    try:
        import io

        from PIL import Image

        # Create a simple test image
        img = Image.new("RGB", (100, 100), color="red")

        # Test basic operations
        img_resized = img.resize((50, 50))
        print("✓ Image resize")

        # Test format conversion
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        print("✓ Image format conversion")

        # Test image loading from buffer
        buffer.seek(0)
        img_loaded = Image.open(buffer)
        print("✓ Image loading from buffer")

        return True
    except Exception as e:
        print(f"✗ Image processing test failed: {e}")
        return False


def test_gui_components():
    """Test GUI components (without actually showing windows)."""
    print("\nTesting GUI components...")
    try:
        import tkinter as tk

        # Test basic tkinter
        root = tk.Tk()
        root.withdraw()  # Hide the window
        print("✓ Tkinter root window creation")

        # Test basic widgets
        label = tk.Label(root, text="Test")
        print("✓ Tkinter Label widget")

        button = tk.Button(root, text="Test")
        print("✓ Tkinter Button widget")

        root.destroy()
        print("✓ Tkinter cleanup")

        return True
    except Exception as e:
        print(f"✗ GUI component test failed: {e}")
        return False


def test_cli_functionality():
    """Test CLI functionality."""
    print("\nTesting CLI functionality...")
    try:
        from gui_image_studio import cli

        print("✓ CLI module import")

        # Test that CLI functions exist
        if hasattr(cli, "main"):
            print("✓ CLI main function exists")
        else:
            print("⚠ CLI main function not found")

        return True
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False


def test_sample_creation():
    """Test sample image creation."""
    print("\nTesting sample creation...")
    try:
        import os

        # Test that the function can be imported and called
        # Note: create_sample_images() creates images in 'sample_images' directory
        # We'll just test that it can be called without errors
        import tempfile

        from gui_image_studio.sample_creator import create_sample_images

        # Change to temp directory to avoid creating files in project
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                create_sample_images()
                print("✓ Sample image creation")
            finally:
                os.chdir(original_cwd)

        return True
    except Exception as e:
        print(f"✗ Sample creation test failed: {e}")
        traceback.print_exc()
        return False


def run_comprehensive_test():
    """Run all tests and provide a summary."""
    print("🔍 GUI Image Studio Installation Verification")
    print("=" * 50)

    tests = [
        ("Basic Import", test_basic_import),
        ("Submodule Imports", test_submodule_imports),
        ("Dependencies", test_dependencies),
        ("Image Processing", test_image_processing),
        ("GUI Components", test_gui_components),
        ("CLI Functionality", test_cli_functionality),
        ("Sample Creation", test_sample_creation),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Print summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:<20} {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! GUI Image Studio is properly installed.")
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed. There may be installation issues.")
        return False


def main():
    """Main verification function."""
    success = run_comprehensive_test()

    if not success:
        print("\nTroubleshooting tips:")
        print("1. Make sure you installed with: pip install -e .[dev]")
        print("2. Check that all dependencies are installed")
        print(
            "3. Try reinstalling: pip uninstall gui-image-studio && pip install -e .[dev]"
        )
        print("4. Check the installation guide in CONTRIBUTING.md")
        sys.exit(1)

    print("\nNext steps:")
    print("- Run the examples: python examples/01_basic_usage.py")
    print("- Start the GUI: python -m gui_image_studio")
    print("- Run tests: pytest")
    print("- Read the documentation: README.md")


if __name__ == "__main__":
    main()
