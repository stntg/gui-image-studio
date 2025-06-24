#!/usr/bin/env python3
"""
Command-line interface for gui_image_studio package.
"""

import argparse
import sys

from . import __version__
from .generator import embed_images_from_folder
from .sample_creator import create_sample_images as _create_sample_images


def generate_embedded_images():
    """Console script entry point for generating embedded images."""
    parser = argparse.ArgumentParser(
        description="Generate embedded images from a folder",
        prog="gui-image-studio-generate",
    )
    parser.add_argument(
        "--folder",
        "-f",
        default="sample_images",
        help="Folder containing images (default: sample_images)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="embedded_images.py",
        help="Output file name (default: embedded_images.py)",
    )
    parser.add_argument(
        "--quality",
        "-q",
        type=int,
        default=85,
        help="Compression quality 1-100 (default: 85)",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

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
        description="Create sample images for testing gui_image_studio functionality",
        prog="gui_image_studio-create-samples",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="sample_images",
        help="Output directory for sample images (default: sample_images)",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    try:
        # Create the sample images
        _create_sample_images()

        # If a different output directory was specified, we'd need to modify the
        # sample_creator
        # For now, just inform the user
        if args.output_dir != "sample_images":
            print("Note: Sample images were created in 'sample_images' directory.")
            print(
                f"To use a different directory, please move the files to "
                f"'{args.output_dir}'"
            )

        print("Successfully created sample images")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def launch_designer():
    """Console script entry point for launching the image studio GUI."""
    parser = argparse.ArgumentParser(
        description="Launch the GUI Image Studio",
        prog="gui-image-studio-designer",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    try:
        from .image_studio import main

        main()
    except ImportError as e:
        print(f"Error importing GUI components: {e}", file=sys.stderr)
        print(
            "Make sure tkinter is available (usually built-in with Python)",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error launching studio: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # This allows the module to be run directly for testing
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        generate_embedded_images()
    elif len(sys.argv) > 1 and sys.argv[1] == "samples":
        create_sample_images()
    elif len(sys.argv) > 1 and sys.argv[1] == "designer":
        launch_designer()
    else:
        print("Usage: python -m gui_image_studio.cli [generate|samples|designer]")
        sys.exit(1)
