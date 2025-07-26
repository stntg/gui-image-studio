"""
Unified file operations core.

This module provides common file handling functionality used by both CLI and GUI,
including file validation, batch processing, and error handling.
"""

import os
from pathlib import Path
from typing import Generator, List, Optional, Tuple, Union

from PIL import Image

from .io_utils import load_image, save_image


class FileOperationError(Exception):
    """Base exception for file operation errors."""

    pass


class FileValidationError(FileOperationError):
    """Exception raised when file validation fails."""

    pass


def validate_image_file(file_path: Union[str, Path]) -> Path:
    """
    Validate that a file exists and is a valid image.

    Args:
        file_path: Path to the image file

    Returns:
        Validated Path object

    Raises:
        FileNotFoundError: If file doesn't exist
        FileValidationError: If file is not a valid image
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise FileValidationError(f"Path is not a file: {path}")

    # Check file extension
    valid_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
        ".ico",
    }
    if path.suffix.lower() not in valid_extensions:
        raise FileValidationError(f"Unsupported file type: {path.suffix}")

    # Try to open the image to verify it's valid
    try:
        with Image.open(path) as img:
            img.verify()  # Verify the image is not corrupted
    except Exception as e:
        raise FileValidationError(f"Invalid image file {path}: {e}")

    return path


def validate_output_path(
    output_path: Union[str, Path], create_dirs: bool = True
) -> Path:
    """
    Validate and prepare an output file path.

    Args:
        output_path: Desired output file path
        create_dirs: Whether to create parent directories if they don't exist

    Returns:
        Validated Path object

    Raises:
        FileOperationError: If path cannot be used for output
    """
    path = Path(output_path)

    # Create parent directories if requested
    if create_dirs and not path.parent.exists():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise FileOperationError(f"Cannot create directory {path.parent}: {e}")

    # Check if parent directory exists and is writable
    if not path.parent.exists():
        raise FileOperationError(f"Output directory does not exist: {path.parent}")

    if not os.access(path.parent, os.W_OK):
        raise FileOperationError(f"Output directory is not writable: {path.parent}")

    # Check if file already exists and is writable
    if path.exists() and not os.access(path, os.W_OK):
        raise FileOperationError(f"Output file is not writable: {path}")

    return path


def find_image_files(
    directory: Union[str, Path],
    recursive: bool = False,
    extensions: Optional[List[str]] = None,
) -> List[Path]:
    """
    Find all image files in a directory.

    Args:
        directory: Directory to search
        recursive: Whether to search subdirectories
        extensions: List of file extensions to include (default: common image types)

    Returns:
        List of Path objects for found image files

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")

    if not dir_path.is_dir():
        raise FileValidationError(f"Path is not a directory: {dir_path}")

    if extensions is None:
        extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".ico"]

    # Normalize extensions to lowercase
    extensions = [
        ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions
    ]

    image_files = []

    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"

    for file_path in dir_path.glob(pattern):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            try:
                # Quick validation that it's actually an image
                validate_image_file(file_path)
                image_files.append(file_path)
            except FileValidationError:
                # Skip invalid image files
                continue

    return sorted(image_files)


def batch_process_images(
    input_files: List[Union[str, Path]],
    output_directory: Union[str, Path],
    processor_func,
    name_template: str = "{stem}{suffix}",
    overwrite: bool = False,
    **processor_kwargs,
) -> Generator[Tuple[Path, Path, bool], None, None]:
    """
    Process multiple image files in batch.

    Args:
        input_files: List of input image file paths
        output_directory: Directory for output files
        processor_func: Function to process each image (takes image, returns image)
        name_template: Template for output filenames (supports {stem}, {suffix}, {name})
        overwrite: Whether to overwrite existing output files
        **processor_kwargs: Additional arguments for processor_func

    Yields:
        Tuple of (input_path, output_path, success) for each processed file

    Raises:
        FileNotFoundError: If output directory doesn't exist
    """
    output_dir = Path(output_directory)

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    for input_file in input_files:
        input_path = Path(input_file)
        success = False

        try:
            # Validate input file
            validate_image_file(input_path)

            # Generate output filename
            output_name = name_template.format(
                stem=input_path.stem, suffix=input_path.suffix, name=input_path.name
            )
            output_path = output_dir / output_name

            # Check if output already exists
            if output_path.exists() and not overwrite:
                print(f"Skipping {input_path} (output exists): {output_path}")
                yield (input_path, output_path, False)
                continue

            # Load and process the image
            image = load_image(input_path)
            processed_image = processor_func(image, **processor_kwargs)

            # Save the processed image
            save_image(processed_image, output_path)
            success = True

        except Exception as e:
            print(f"Error processing {input_path}: {e}")

        yield (input_path, output_path, success)


def safe_filename(filename: str, replacement: str = "_") -> str:
    """
    Convert a string to a safe filename by replacing invalid characters.

    Args:
        filename: Original filename
        replacement: Character to replace invalid characters with

    Returns:
        Safe filename string
    """
    # Characters that are invalid in filenames on most systems
    invalid_chars = '<>:"/\\|?*'

    safe_name = filename
    for char in invalid_chars:
        safe_name = safe_name.replace(char, replacement)

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(" .")

    # Ensure the filename isn't empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def get_unique_filename(base_path: Union[str, Path]) -> Path:
    """
    Generate a unique filename by appending a number if the file already exists.

    Args:
        base_path: Desired file path

    Returns:
        Unique Path object
    """
    path = Path(base_path)

    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def calculate_directory_size(directory: Union[str, Path]) -> int:
    """
    Calculate the total size of all files in a directory.

    Args:
        directory: Directory path

    Returns:
        Total size in bytes
    """
    total_size = 0
    dir_path = Path(directory)

    if not dir_path.exists():
        return 0

    for file_path in dir_path.rglob("*"):
        if file_path.is_file():
            try:
                total_size += file_path.stat().st_size
            except (OSError, IOError):
                # Skip files we can't access
                continue

    return total_size


def format_file_size(size_bytes: int) -> str:
    """
    Format a file size in bytes to a human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


class FileProgress:
    """Simple progress tracker for file operations."""

    def __init__(self, total: int):
        self.total = total
        self.current = 0
        self.errors = 0

    def update(self, success: bool = True):
        """Update progress counter."""
        self.current += 1
        if not success:
            self.errors += 1

    def get_progress(self) -> Tuple[int, int, int, float]:
        """Get current progress as (current, total, errors, percentage)."""
        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        return self.current, self.total, self.errors, percentage

    def is_complete(self) -> bool:
        """Check if all files have been processed."""
        return self.current >= self.total

    def __str__(self) -> str:
        """String representation of progress."""
        current, total, errors, percentage = self.get_progress()
        return f"{current}/{total} ({percentage:.1f}%) - {errors} errors"
