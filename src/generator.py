#!/usr/bin/env python3
"""
Image embedding generator for gui_image_studio package.
"""

import base64
import os
from io import BytesIO

from PIL import Image


def embed_images_from_folder(
    folder_path, output_file="embedded_images.py", compression_quality=85
):
    """
    Processes all valid images in a folder, applies optional JPEG/WebP compression,
    categorizes them by theme (if the filename starts with a theme followed by
    an underscore),
    and writes them into an output Python file.

    Args:
        folder_path (str): Path to the folder containing images.
        output_file (str): Name of the generated Python file.
        compression_quality (int): JPEG/WebP quality (1-100). Lower means more
            compression.
    """
    # Dictionary that will map theme names to image key: base64 value pairs.
    images_dict = {}

    # Function to store image under given theme and key
    def store_image(theme, key, encoded):
        if theme not in images_dict:
            images_dict[theme] = {}
        images_dict[theme][key] = encoded

    # Allowed image extensions
    valid_extensions = (
        ".gif",
        ".png",
        ".ico",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
        ".webp",
    )

    if not os.path.exists(folder_path):
        print(
            f"Warning: Folder '{folder_path}' does not exist. "
            "Creating empty embedded_images.py"
        )
        images_dict = {"default": {}}
    else:
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(valid_extensions):
                continue

            file_path = os.path.join(folder_path, filename)
            # Determine theme from filename. For example, dark_icon.png → theme
            # "dark", key "icon.png"
            if "_" in filename:
                theme_candidate, remainder = filename.split("_", 1)
                # Ensure theme_candidate is alphabetic (or you can adjust this check)
                if theme_candidate.isalpha():
                    theme = theme_candidate.lower()
                    key = remainder
                else:
                    theme = "default"
                    key = filename
            else:
                theme = "default"
                key = filename

            # Open the image and, where applicable, compress it.
            try:
                with Image.open(file_path) as img:
                    # If the format supports compression, apply it.
                    if img.format in ["JPEG", "WEBP"]:
                        buffer = BytesIO()
                        img.save(buffer, format=img.format, quality=compression_quality)
                        byte_data = buffer.getvalue()
                    else:
                        with open(file_path, "rb") as f:
                            byte_data = f.read()

                    encoded_string = base64.b64encode(byte_data).decode("utf-8")
                    store_image(theme, key, encoded_string)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Write the resulting dictionary to the output Python file.
    with open(output_file, "w") as py_file:
        py_file.write("# Auto-generated embedded images file\n")
        py_file.write("embedded_images = {\n")
        for theme, images in images_dict.items():
            py_file.write(f"    '{theme}': {{\n")
            for key, data in images.items():
                py_file.write(f"        '{key}': '''{data}''',\n")
            py_file.write("    },\n")
        py_file.write("}\n")

    print(
        f"Embedded images saved in {output_file} "
        f"(compression quality {compression_quality})"
    )


def generate_embedded_images():
    """Console script entry point for generating embedded images."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate embedded images from a folder"
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

    args = parser.parse_args()

    embed_images_from_folder(args.folder, args.output, args.quality)


if __name__ == "__main__":
    generate_embedded_images()
