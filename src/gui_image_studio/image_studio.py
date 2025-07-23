#!/usr/bin/env python3
"""
Entry point for the refactored Image Studio application.
This maintains compatibility while using the new modular structure.
"""

import os
import sys

# Add the src directory to the path to enable absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from gui_image_studio.image_studio.main_app import main

if __name__ == "__main__":
    main()
