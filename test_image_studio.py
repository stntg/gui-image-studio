#!/usr/bin/env python3
"""
Test script for the Image Studio GUI functionality.
"""

import sys
import os
import tempfile
import shutil

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_studio_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from gui_image_studio.image_studio import ImageDesignerGUI, ImageSizeDialog, CodePreviewWindow
        print("✓ Image Studio GUI classes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Image Studio GUI: {e}")
        return False
        
    try:
        import gui_image_studio
        print("✓ Main package imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import main package: {e}")
        return False
        
    return True

def test_studio_creation():
    """Test that the studio GUI can be created (without showing)."""
    print("Testing GUI creation...")
    
    try:
        from gui_image_studio.image_studio import ImageDesignerGUI
        
        # Create the GUI object (but don't run it)
        app = ImageDesignerGUI()
        
        # Test basic properties
        assert hasattr(app, 'root'), "GUI should have root window"
        assert hasattr(app, 'current_images'), "GUI should have images dictionary"
        assert hasattr(app, 'canvas'), "GUI should have drawing canvas"
        
        print("✓ Image Studio GUI created successfully")
        
        # Clean up
        app.root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Failed to create Image Studio GUI: {e}")
        return False

def test_image_operations():
    """Test basic image operations."""
    print("Testing image operations...")
    
    try:
        from PIL import Image
        from gui_image_studio.image_studio import ImageDesignerGUI
        
        # Create a test image
        test_image = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
        
        # Create GUI (but don't show)
        app = ImageDesignerGUI()
        
        # Test adding image
        app.current_images["test_image"] = test_image
        assert "test_image" in app.current_images, "Image should be added to collection"
        
        # Test image selection
        app.select_image("test_image")
        assert app.selected_image == "test_image", "Image should be selected"
        
        print("✓ Basic image operations work correctly")
        
        # Clean up
        app.root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Failed image operations test: {e}")
        return False

def test_code_generation():
    """Test code generation functionality."""
    print("Testing code generation...")
    
    try:
        from PIL import Image
        from gui_image_studio.generator import embed_images_from_folder
        import tempfile
        import os
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test image
            test_image = Image.new("RGB", (50, 50), (0, 255, 0))
            image_path = os.path.join(temp_dir, "test.png")
            test_image.save(image_path)
            
            # Generate embedded code
            output_file = os.path.join(temp_dir, "embedded.py")
            embed_images_from_folder(temp_dir, output_file, 85)
            
            # Check if file was created
            assert os.path.exists(output_file), "Embedded code file should be created"
            
            # Check file content
            with open(output_file, 'r') as f:
                content = f.read()
                assert "embedded_images" in content, "File should contain embedded_images"
                assert "test" in content, "File should contain test image"
                
        print("✓ Code generation works correctly")
        return True
        
    except Exception as e:
        print(f"✗ Failed code generation test: {e}")
        return False

def main():
    """Run all tests."""
    print("GUI Image Studio - Test Suite")
    print("=" * 40)
    
    tests = [
        test_studio_imports,
        test_studio_creation,
        test_image_operations,
        test_code_generation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Image Studio GUI is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)