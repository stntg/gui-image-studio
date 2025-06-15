#!/usr/bin/env python3
"""
Script to generate embedded_images.py from sample images.
"""

import sys
import os

# Add src directory to path to import img2res
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from img2res import embed_images_from_folder

if __name__ == "__main__":
    # Generate embedded images from sample_images folder
    embed_images_from_folder(
        folder_path="sample_images",
        output_file="src/embedded_images.py",
        compression_quality=85
    )
    print("Embedded images generated successfully!")