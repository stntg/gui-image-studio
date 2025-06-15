import os
import base64
from io import BytesIO
from PIL import Image

def embed_images_from_folder(folder_path, output_file="embedded_images.py", compression_quality=85):
    """
    Processes all valid images in a folder, applies optional JPEG/WebP compression,
    categorizes them by theme (if the filename starts with a theme followed by an underscore),
    and writes them into an output Python file.
    
    Args:
        folder_path (str): Path to the folder containing images.
        output_file (str): Name of the generated Python file.
        compression_quality (int): JPEG/WebP quality (1-100). Lower means more compression.
    """
    # Dictionary that will map theme names to image key: base64 value pairs.
    images_dict = {}
    
    # Function to store image under given theme and key
    def store_image(theme, key, encoded):
        if theme not in images_dict:
            images_dict[theme] = {}
        images_dict[theme][key] = encoded

    # Allowed image extensions
    valid_extensions = (".gif", ".png", ".ico", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(valid_extensions):
            continue

        file_path = os.path.join(folder_path, filename)
        # Determine theme from filename. For example, dark_icon.png → theme "dark", key "icon.png"
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

    print(f"Embedded images saved in {output_file} (compression quality {compression_quality})")

# Example usage:
if __name__ == "__main__":
    folder_path = "images_folder"  # Replace with your directory
    embed_images_from_folder(folder_path, compression_quality=75)
