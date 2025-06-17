#!/usr/bin/env python3
"""
Launch script for the GUI Image Studio.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui_image_studio.image_studio import main
    main()
except ImportError as e:
    print(f"Error importing GUI Image Studio: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install Pillow")
    print("pip install customtkinter  # Optional, for customtkinter support")
    sys.exit(1)
except Exception as e:
    print(f"Error running GUI Image Studio: {e}")
    sys.exit(1)