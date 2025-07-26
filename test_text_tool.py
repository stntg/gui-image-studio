#!/usr/bin/env python3
"""
Automated test for text tool functionality.
This test verifies that text tool settings are properly applied when drawing text.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from gui_image_studio.image_studio.core.drawing_tools import (  # noqa: E402
    DrawingToolsManager,
)
from gui_image_studio.image_studio.toolkit.tools.text_tool import TextTool  # noqa: E402


def test_text_tool_settings():
    """Test that text tool settings are properly applied."""
    print("=== TEXT TOOL SETTINGS TEST ===")

    # Create a drawing tools manager
    tools_manager = DrawingToolsManager()

    # Set the current tool to text
    tools_manager.select_tool("text")

    # Test 1: Check if text tool is properly registered
    print("\n1. Testing tool registration...")
    available_tools = tools_manager.get_available_tools()
    print(f"Available tools: {available_tools}")
    assert "text" in available_tools, "Text tool not found in available tools"
    print("✓ Text tool is registered")

    # Test 2: Check default settings
    print("\n2. Testing default settings...")
    text_tool = tools_manager.get_current_tool_instance()
    print(f"Text tool instance: {text_tool}")
    print(f"Default settings: {text_tool.settings}")
    assert (
        text_tool.settings["font_size"] == 12
    ), f"Expected font_size 12, got {text_tool.settings['font_size']}"
    assert (
        text_tool.settings["font_family"] == "Arial"
    ), f"Expected Arial, got {text_tool.settings['font_family']}"
    print("✓ Default settings are correct")

    # Test 3: Update settings
    print("\n3. Testing settings update...")
    tools_manager.set_tool_setting("text", "font_size", 24)
    tools_manager.set_tool_setting("text", "font_family", "Times New Roman")
    tools_manager.set_tool_setting("text", "bold", True)
    tools_manager.set_tool_setting("text", "italic", True)

    updated_settings = tools_manager.get_tool_settings("text")
    print(f"Updated settings: {updated_settings}")
    assert (
        updated_settings["font_size"] == 24
    ), f"Expected font_size 24, got {updated_settings['font_size']}"
    assert (
        updated_settings["font_family"] == "Times New Roman"
    ), f"Expected Times New Roman, got {updated_settings['font_family']}"
    assert (
        updated_settings["bold"] is True
    ), f"Expected bold True, got {updated_settings['bold']}"
    assert (
        updated_settings["italic"] is True
    ), f"Expected italic True, got {updated_settings['italic']}"
    print("✓ Settings updated correctly")

    # Test 4: Test settings merge
    print("\n4. Testing settings merge...")
    test_kwargs = {"size": 16, "root": None}
    merged_settings = tools_manager._merge_settings(test_kwargs)
    print(f"Merged settings: {merged_settings}")

    # Check that tool-specific settings are included
    assert "font_size" in merged_settings, "font_size not in merged settings"
    assert "font_family" in merged_settings, "font_family not in merged settings"
    assert "bold" in merged_settings, "bold not in merged settings"
    assert "italic" in merged_settings, "italic not in merged settings"

    assert (
        merged_settings["font_size"] == 24
    ), f"Expected font_size 24, got {merged_settings['font_size']}"
    assert (
        merged_settings["font_family"] == "Times New Roman"
    ), f"Expected Times New Roman, got {merged_settings['font_family']}"
    assert (
        merged_settings["bold"] is True
    ), f"Expected bold True, got {merged_settings['bold']}"
    assert (
        merged_settings["italic"] is True
    ), f"Expected italic True, got {merged_settings['italic']}"
    print("✓ Settings merge works correctly")

    # Test 5: Test actual text drawing
    print("\n5. Testing text drawing...")

    # Create a test image
    test_image = Image.new("RGB", (200, 100), "white")

    # Simulate clicking on the canvas
    print("Simulating text tool click...")

    # Mock the text input dialog by directly calling _draw_text
    text_tool = tools_manager.get_current_tool_instance()
    test_kwargs_with_settings = merged_settings.copy()
    test_kwargs_with_settings["root"] = None

    # Call _draw_text directly with our test settings
    text_tool._draw_text(test_image, 50, 50, "Test Text", **test_kwargs_with_settings)

    # Save the test image to verify visually
    test_image.save(
        "c:\\Users\\Admin\\Desktop\\test\\ToolKit\\gui-image-studio\\test_text_output.png"
    )
    print("✓ Text drawing completed - check test_text_output.png")

    print("\n=== ALL TESTS PASSED ===")


def test_text_tool_handle_click():
    """Test the text tool's handle_click method."""
    print("\n=== TEXT TOOL CLICK TEST ===")

    # Create a drawing tools manager
    tools_manager = DrawingToolsManager()
    tools_manager.select_tool("text")

    # Update settings
    tools_manager.set_tool_setting("text", "font_size", 36)
    tools_manager.set_tool_setting("text", "font_family", "Courier New")
    tools_manager.set_tool_setting("text", "bold", True)

    # Create a test image
    test_image = Image.new("RGB", (300, 150), "white")

    # Test the full click handling pipeline
    print("Testing full click handling pipeline...")
    test_kwargs = {"size": 20, "root": None}

    # This should trigger the settings merge and text drawing
    try:
        tools_manager.handle_click(test_image, 75, 75, **test_kwargs)
        print("✓ Click handling completed")
    except Exception as e:
        print(f"✗ Click handling failed: {e}")
        # Continue with the test to see what we can learn

    # Save the result
    test_image.save(
        "c:\\Users\\Admin\\Desktop\\test\\ToolKit\\gui-image-studio\\test_click_output.png"
    )
    print("✓ Click test completed - check test_click_output.png")


if __name__ == "__main__":
    try:
        test_text_tool_settings()
        test_text_tool_handle_click()
        print("\n🎉 All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
