#!/usr/bin/env python3
"""
Simple test script to verify img2res package functionality.
"""

import img2res

def test_package_info():
    """Test basic package information."""
    print("Testing package info...")
    print(f"Package version: {img2res.__version__}")
    print(f"Available functions: {img2res.__all__}")
    print(f"Available frameworks: {img2res.get_available_frameworks()}")
    print(f"Missing dependencies: {img2res.check_dependencies()}")
    print("✓ Package info test passed\n")

def test_image_loading():
    """Test image loading functionality."""
    print("Testing image loading...")
    
    try:
        # Test loading a basic image
        image = img2res.get_image("icon.png", framework="tkinter", size=(32, 32))
        print("✓ Successfully loaded icon.png for tkinter")
        
        # Test loading with theme
        dark_image = img2res.get_image("icon.png", framework="tkinter", size=(32, 32), theme="dark")
        print("✓ Successfully loaded dark themed icon.png")
        
        # Test loading with transformations
        transformed_image = img2res.get_image(
            "circle.png", 
            framework="tkinter", 
            size=(64, 64),
            rotate=45,
            grayscale=True,
            transparency=0.8
        )
        print("✓ Successfully loaded circle.png with transformations")
        
        print("✓ Image loading test passed\n")
        
    except Exception as e:
        print(f"✗ Image loading test failed: {e}\n")

def test_sample_creation():
    """Test sample image creation."""
    print("Testing sample creation...")
    
    try:
        img2res.create_sample_images()
        print("✓ Sample creation test passed\n")
    except Exception as e:
        print(f"✗ Sample creation test failed: {e}\n")

def test_embedding():
    """Test image embedding functionality."""
    print("Testing image embedding...")
    
    try:
        img2res.embed_images_from_folder("sample_images", "test_embedded_output.py", 90)
        print("✓ Image embedding test passed\n")
    except Exception as e:
        print(f"✗ Image embedding test failed: {e}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("IMG2RES PACKAGE TEST")
    print("=" * 50)
    
    test_package_info()
    test_sample_creation()
    test_embedding()
    test_image_loading()
    
    print("=" * 50)
    print("All tests completed!")
    print("=" * 50)