#!/usr/bin/env python3
"""
Example 06: Image Studio GUI Usage
==================================

This example demonstrates how to use the GUI Image Studio
to create and design images visually, then generate embedded code.

The Image Studio GUI provides:
- Visual image creation and editing tools
- Support for multiple images in one project
- Real-time preview of your designs
- Code generation with preview
- Export capabilities

Usage:
1. Run this script to launch the designer
2. Create new images or load existing ones
3. Use the drawing tools to design your images
4. Preview and generate embedded code
5. Use the generated code in your GUI applications
"""

import os
import sys

# Add the src directory to the Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    import gui_image_studio

    def main():
        """Launch the Image Studio GUI."""
        print("Launching GUI Image Studio...")
        print("\nFeatures:")
        print("- Create and edit images visually")
        print("- Multiple drawing tools (brush, shapes, text)")
        print("- Image transformations and filters")
        print("- Real-time preview")
        print("- Generate embedded Python code")
        print("- Export images to files")
        print("\nInstructions:")
        print("1. Use 'New Image' to create a blank canvas")
        print("2. Select drawing tools from the left panel")
        print("3. Draw on the canvas in the center")
        print("4. Adjust properties in the right panel")
        print("5. Use 'Preview Code' to see generated code")
        print("6. Use 'Generate File' to save embedded code")
        print("\nKeyboard shortcuts:")
        print("- Ctrl+N: New image")
        print("- Ctrl+O: Load image")
        print("- Ctrl+S: Export images")
        print("- Delete: Delete selected image")
        print()

        # Launch the studio
        gui_image_studio.launch_designer()

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Error importing gui_image_studio: {e}")
    print("\nMake sure to install the required dependencies:")
    print("pip install Pillow")
    print("\nFor customtkinter support (optional):")
    print("pip install customtkinter")
    sys.exit(1)
except Exception as e:
    print(f"Error running example: {e}")
    sys.exit(1)
