#!/usr/bin/env python3
"""
Command-line interface for gui_image_studio package.

This module provides backward compatibility while delegating to the new
unified CLI commands that use the image processing core.
"""

import sys

# Import the new unified CLI commands
from .cli.commands import (
    create_sample_images,
    generate_embedded_images,
    image_processor,
    launch_designer,
)

# Re-export for backward compatibility
__all__ = [
    "image_processor",
    "generate_embedded_images",
    "create_sample_images",
    "launch_designer",
]


if __name__ == "__main__":
    # This allows the module to be run directly for testing
    if len(sys.argv) > 1 and sys.argv[1] == "process":
        image_processor()
    elif len(sys.argv) > 1 and sys.argv[1] == "generate":
        generate_embedded_images()
    elif len(sys.argv) > 1 and sys.argv[1] == "samples":
        create_sample_images()
    elif len(sys.argv) > 1 and sys.argv[1] == "designer":
        launch_designer()
    else:
        print(
            "Usage: python -m gui_image_studio.cli [process|generate|samples|designer]"
        )
        print("  process   - Process images with transformations")
        print("  generate  - Generate embedded images from folder")
        print("  samples   - Create sample images")
        print("  designer  - Launch the GUI designer")
        sys.exit(1)
