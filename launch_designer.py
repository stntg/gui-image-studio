#!/usr/bin/env python3
"""
GUI Image Studio Launcher Script

This script provides a convenient way to launch the GUI Image Studio
without needing to use the command line interface.

Usage:
    python launch_designer.py
"""

import sys
import os

# Add the src directory to the Python path so we can import gui_image_studio
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

def main():
    """Launch the GUI Image Studio."""
    try:
        import gui_image_studio
        print(f"Launching GUI Image Studio v{gui_image_studio.__version__}")
        gui_image_studio.launch_designer()
    except ImportError as e:
        print(f"Error importing gui_image_studio: {e}")
        print("Make sure you have installed the package:")
        print("  pip install -e .")
        print("Or install the required dependencies:")
        print("  pip install pillow customtkinter")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI Image Studio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()