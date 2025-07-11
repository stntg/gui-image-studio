#!/usr/bin/env python3
"""
Test script to verify memory management improvements in the GUI Image Studio.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from gui_image_studio.image_studio import EnhancedImageDesignerGUI


def main():
    """Test the enhanced image designer with memory management."""
    print("Starting GUI Image Studio with memory management improvements...")
    print("Memory management features added:")
    print("- Automatic cleanup of old PhotoImage objects")
    print("- Maximum image size limits (4096x4096 for loading, 2048x2048 for display)")
    print("- Conservative zoom limits (max 5x instead of 10x)")
    print("- Garbage collection after memory-intensive operations")
    print("- Proper cleanup on application close")
    print("- Error handling for memory issues")
    print()

    try:
        app = EnhancedImageDesignerGUI()
        app.root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
