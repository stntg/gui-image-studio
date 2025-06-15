#!/usr/bin/env python3
"""
Main entry point for gui_image_studio module.
Allows running: python -m gui_image_studio
"""

import sys

from .cli import generate_embedded_images
from .sample_creator import create_sample_images


def main():
    """Main entry point for the module."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command in ["sample", "samples", "create-samples"]:
            create_sample_images()
        elif command in ["generate", "embed"]:
            # Remove the command from sys.argv so argparse works correctly
            sys.argv = [sys.argv[0]] + sys.argv[2:]
            generate_embedded_images()
        elif command in ["help", "-h", "--help"]:
            print_help()
        else:
            print(f"Unknown command: {command}")
            print_help()
            sys.exit(1)
    else:
        print_help()


def print_help():
    """Print help information."""
    print("GUI Image Studio - Image Resource Management for Python GUI Applications")
    print()
    print("Usage:")
    print("  python -m gui_image_studio <command> [options]")
    print()
    print("Commands:")
    print("  samples, create-samples    Create sample images for testing")
    print("  generate, embed           Generate embedded images from folder")
    print("  help                      Show this help message")
    print()
    print("Examples:")
    print("  python -m gui_image_studio samples")
    print("  python -m gui_image_studio generate --folder images --output embedded.py")


if __name__ == "__main__":
    main()
