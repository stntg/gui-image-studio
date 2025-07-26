#!/usr/bin/env python3
"""
Integration test for text tool with the actual application setup.
"""

import os
import sys
import tkinter as tk

from PIL import Image

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from gui_image_studio.image_studio.main_app import (  # noqa: E402
    EnhancedImageDesignerGUI,
)


def test_text_tool_integration():
    """Test text tool integration with the main application."""
    print("=== TEXT TOOL INTEGRATION TEST ===")

    try:
        # Create the application (it creates its own root)
        app = EnhancedImageDesignerGUI()
        app.root.withdraw()  # Hide the main window

        # Create a test image
        test_image = Image.new("RGB", (400, 200), "white")
        app.images = [test_image]
        app.selected_image = test_image

        # Select the text tool
        app.drawing_tools.select_tool("text")
        print(f"Selected tool: {app.drawing_tools.get_current_tool()}")

        # Update text tool settings
        app.drawing_tools.set_tool_setting("text", "font_size", 48)
        app.drawing_tools.set_tool_setting("text", "font_family", "Times New Roman")
        app.drawing_tools.set_tool_setting("text", "bold", True)
        app.drawing_tools.set_tool_setting("text", "italic", True)

        print("Updated text tool settings:")
        settings = app.drawing_tools.get_tool_settings("text")
        for key, value in settings.items():
            print(f"  {key}: {value}")

        # Simulate a canvas click (this should trigger the text input dialog)
        print("\nSimulating canvas click...")

        # Get the text tool instance and call _draw_text directly
        text_tool = app.drawing_tools.get_current_tool_instance()

        # Prepare kwargs as they would be passed from the main app
        kwargs = {
            "size": app.size_var.get() if hasattr(app, "size_var") else 20,
            "root": app.root,
        }

        # Merge settings as the drawing tools manager would do
        merged_kwargs = app.drawing_tools._merge_settings(kwargs)

        print("Merged kwargs for text tool:")
        for key, value in merged_kwargs.items():
            print(f"  {key}: {value}")

        # Draw text directly (bypassing the dialog)
        print("\nDrawing text directly...")
        text_tool._draw_text(test_image, 100, 100, "Integration Test", **merged_kwargs)

        # Save the result
        test_image.save(
            "c:\\Users\\Admin\\Desktop\\test\\ToolKit\\gui-image-studio\\integration_test_output.png"
        )
        print("✓ Integration test completed - check integration_test_output.png")

        # Test the full click handling (this would show the dialog in a real scenario)
        print("\nTesting full click handling (dialog would appear)...")
        try:
            # This would normally show a dialog, but we'll catch any issues
            app.drawing_tools.handle_click(test_image, 200, 100, **kwargs)
            print("✓ Click handling completed")
        except Exception as e:
            print(f"Click handling issue: {e}")

        # Save the final result
        test_image.save(
            "c:\\Users\\Admin\\Desktop\\test\\ToolKit\\gui-image-studio\\integration_test_final.png"
        )
        print("✓ Final integration test completed")

    finally:
        app.root.destroy()

    print("\n🎉 Integration test completed!")


if __name__ == "__main__":
    test_text_tool_integration()
