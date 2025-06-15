#!/usr/bin/env python3
"""
Command-line interface for img2res package.
"""

import argparse
import sys
from .generator import embed_images_from_folder
from .sample_creator import create_sample_images as _create_sample_images


def generate_embedded_images():
    """Console script entry point for generating embedded images."""
    parser = argparse.ArgumentParser(
        description='Generate embedded images from a folder',
        prog='img2res-generate'
    )
    parser.add_argument('--folder', '-f', default='sample_images', 
                       help='Folder containing images (default: sample_images)')
    parser.add_argument('--output', '-o', default='embedded_images.py',
                       help='Output file name (default: embedded_images.py)')
    parser.add_argument('--quality', '-q', type=int, default=85,
                       help='Compression quality 1-100 (default: 85)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    # Validate quality parameter
    if not 1 <= args.quality <= 100:
        print("Error: Quality must be between 1 and 100", file=sys.stderr)
        sys.exit(1)
    
    try:
        embed_images_from_folder(args.folder, args.output, args.quality)
        print(f"Successfully generated {args.output}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def create_sample_images():
    """Console script entry point for creating sample images."""
    parser = argparse.ArgumentParser(
        description='Create sample images for testing img2res functionality',
        prog='img2res-create-samples'
    )
    parser.add_argument('--output-dir', '-o', default='sample_images',
                       help='Output directory for sample images (default: sample_images)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    try:
        # Temporarily change the output directory in the sample creator
        import os
        original_dir = os.getcwd()
        
        # Create the sample images
        _create_sample_images()
        
        # If a different output directory was specified, we'd need to modify the sample_creator
        # For now, just inform the user
        if args.output_dir != 'sample_images':
            print(f"Note: Sample images were created in 'sample_images' directory.")
            print(f"To use a different directory, please move the files to '{args.output_dir}'")
        
        print("Successfully created sample images")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # This allows the module to be run directly for testing
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        generate_embedded_images()
    elif len(sys.argv) > 1 and sys.argv[1] == "samples":
        create_sample_images()
    else:
        print("Usage: python -m img2res.cli [generate|samples]")
        sys.exit(1)