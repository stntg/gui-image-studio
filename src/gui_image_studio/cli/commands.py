#!/usr/bin/env python3
"""
Enhanced command-line interface for gui_image_studio package.

This module provides CLI commands that use the unified image processing core,
ensuring consistency between CLI and GUI operations.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple

from .. import __version__
from ..core.code_generation import embed_images_from_folder
from ..core.effects_registry import EffectsRegistry
from ..core.image_effects import apply_transformations
from ..core.io_utils import load_image, save_image
from ..core.sample_creation import (
    create_sample_image_set,
    create_sample_images_legacy_compatible,
)


def image_processor() -> None:
    """
    Console script entry point for processing images with transformations.

    This is a new CLI command that demonstrates the unified image processing core.
    """
    parser = argparse.ArgumentParser(
        description="Process images with various transformations using the unified core",
        prog="gui-image-studio-process",
    )

    # Input/Output arguments
    parser.add_argument("--input", "-i", required=True, help="Input image file path")
    parser.add_argument("--output", "-o", required=True, help="Output image file path")

    # Transformation arguments
    parser.add_argument(
        "--resize",
        nargs=2,
        type=int,
        metavar=("WIDTH", "HEIGHT"),
        help="Resize image to WIDTH HEIGHT",
    )
    parser.add_argument(
        "--rotate",
        type=float,
        default=0.0,
        help="Rotate image by degrees (positive = clockwise)",
    )
    parser.add_argument(
        "--grayscale", action="store_true", help="Convert image to grayscale"
    )
    parser.add_argument(
        "--blur", type=float, default=0.0, help="Apply Gaussian blur with given radius"
    )
    parser.add_argument(
        "--contrast",
        type=float,
        default=1.0,
        help="Adjust contrast (1.0 = no change, >1.0 = more contrast)",
    )
    parser.add_argument(
        "--saturation",
        type=float,
        default=1.0,
        help="Adjust saturation (1.0 = no change, 0.0 = grayscale)",
    )
    parser.add_argument(
        "--brightness",
        type=float,
        default=1.0,
        help="Adjust brightness (1.0 = no change, >1.0 = brighter)",
    )
    parser.add_argument(
        "--transparency",
        type=float,
        default=1.0,
        help="Adjust transparency (1.0 = opaque, 0.0 = transparent)",
    )
    parser.add_argument(
        "--tint-color",
        nargs=3,
        type=int,
        metavar=("R", "G", "B"),
        help="Apply color tint with RGB values (0-255)",
    )
    parser.add_argument(
        "--tint-intensity",
        type=float,
        default=0.0,
        help="Tint intensity (0.0 = no tint, 1.0 = full tint)",
    )
    parser.add_argument(
        "--format", help="Convert to specified format (PNG, JPEG, etc.)"
    )
    parser.add_argument(
        "--quality", type=int, default=95, help="JPEG quality (1-100, default: 95)"
    )

    # Utility arguments
    parser.add_argument(
        "--preserve-aspect",
        action="store_true",
        help="Preserve aspect ratio when resizing",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Validate parameters
    if args.quality < 1 or args.quality > 100:
        print("Error: Quality must be between 1 and 100", file=sys.stderr)
        sys.exit(1)

    if args.tint_color:
        for val in args.tint_color:
            if val < 0 or val > 255:
                print(
                    "Error: Tint color values must be between 0 and 255",
                    file=sys.stderr,
                )
                sys.exit(1)

    try:
        # Load the image using unified core
        print(f"Loading image: {input_path}")
        image = load_image(input_path)

        # Prepare transformation parameters
        transforms = {
            "grayscale": args.grayscale,
            "rotate": args.rotate,
            "transparency": args.transparency,
            "contrast": args.contrast,
            "saturation": args.saturation,
            "brightness": args.brightness,
            "blur_radius": args.blur,
            "format_override": args.format,
        }

        # Add resize if specified
        if args.resize:
            transforms["size"] = tuple(args.resize)

        # Add tint if specified
        if args.tint_color and args.tint_intensity > 0.0:
            transforms["tint_color"] = tuple(args.tint_color)
            transforms["tint_intensity"] = args.tint_intensity

        # Apply transformations using unified core
        print("Applying transformations...")
        processed_image = apply_transformations(image, **transforms)

        # Save the result using unified core
        output_path = Path(args.output)
        print(f"Saving processed image: {output_path}")
        save_image(processed_image, output_path, quality=args.quality)

        print(f"Successfully processed image: {input_path} -> {output_path}")

    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        sys.exit(1)


def generate_embedded_images() -> None:
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
        "--framework",
        choices=["tkinter", "customtkinter"],
        default="tkinter",
        help="Target framework (default: tkinter)",
    )
    parser.add_argument(
        "--usage",
        choices=["icons", "buttons", "backgrounds", "general"],
        default="general",
        help="Usage type for examples (default: general)",
    )
    parser.add_argument(
        "--no-examples",
        action="store_true",
        help="Don't include usage examples in generated code",
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
        print(f"Processing images from: {args.folder}")
        print(f"Target framework: {args.framework}")
        print(f"Usage type: {args.usage}")
        print(f"Quality: {args.quality}")

        embed_images_from_folder(
            folder_path=args.folder,
            output_file=args.output,
            compression_quality=args.quality,
            framework=args.framework,
            usage=args.usage,
            include_examples=not args.no_examples,
        )

        print(f"Successfully generated {args.output}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def create_sample_images() -> None:
    """Console script entry point for creating sample images."""
    parser = argparse.ArgumentParser(
        description="Create sample images for testing gui_image_studio functionality",
        prog="gui-image-studio-create-samples",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="sample_images",
        help="Output directory for sample images (default: sample_images)",
    )
    parser.add_argument(
        "--themes",
        nargs="+",
        choices=["default", "dark", "light", "colorful"],
        default=["default", "dark", "light"],
        help="Themes to generate (default: default dark light)",
    )
    parser.add_argument(
        "--types",
        nargs="+",
        choices=["icons", "buttons", "shapes", "patterns", "gradients"],
        default=["icons", "buttons", "shapes"],
        help="Types of images to generate (default: icons buttons shapes)",
    )
    parser.add_argument(
        "--include-animations",
        action="store_true",
        help="Include animated GIF samples",
    )
    parser.add_argument(
        "--legacy-mode",
        action="store_true",
        help="Create images compatible with original sample_creator",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    try:
        if args.legacy_mode:
            # Use legacy-compatible creation
            print("Creating legacy-compatible sample images...")
            create_sample_images_legacy_compatible(args.output_dir)
        else:
            # Use new unified creation
            print(f"Creating sample images in: {args.output_dir}")
            print(f"Themes: {', '.join(args.themes)}")
            print(f"Types: {', '.join(args.types)}")
            print(f"Include animations: {args.include_animations}")

            created_files = create_sample_image_set(
                output_dir=args.output_dir,
                themes=args.themes,
                image_types=args.types,
                include_animations=args.include_animations,
            )

            # Report results
            total_files = sum(len(files) for files in created_files.values())
            print(f"\nSuccessfully created {total_files} sample images:")
            for theme, files in created_files.items():
                print(f"  {theme}: {len(files)} images")

        print(f"\nSample images saved to: {args.output_dir}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


def launch_designer() -> None:
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
        from ..image_studio.main_app import main

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
            "Usage: python -m gui_image_studio.cli.commands [process|generate|samples|designer]"
        )
        sys.exit(1)


def list_effects() -> None:
    """Console script entry point for listing available image effects."""
    parser = argparse.ArgumentParser(
        description="List available image effects and their parameters",
        prog="gui-image-studio-list-effects",
    )
    parser.add_argument(
        "--category",
        "-c",
        help="Filter effects by category",
    )
    parser.add_argument(
        "--detailed",
        "-d",
        action="store_true",
        help="Show detailed parameter information",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    try:
        effects = EffectsRegistry.get_all_effects()
        categories = EffectsRegistry.get_categories()

        if args.category:
            if args.category not in categories:
                print(f"Error: Unknown category '{args.category}'", file=sys.stderr)
                print(f"Available categories: {', '.join(categories.keys())}")
                sys.exit(1)

            effects_to_show = {
                name: effects[name] for name in categories[args.category]
            }
            print(f"Effects in category '{args.category}':")
        else:
            effects_to_show = effects
            print("All available image effects:")

        print("=" * 60)

        if args.detailed:
            # Detailed view with parameters
            for category, effect_names in categories.items():
                if args.category and category != args.category:
                    continue

                print(f"\n{category.upper()} EFFECTS:")
                print("-" * 40)

                for effect_name in effect_names:
                    if effect_name in effects_to_show:
                        effect = effects[effect_name]
                        print(f"\n• {effect.display_name} ({effect.name})")
                        print(f"  Description: {effect.description}")

                        if effect.parameters:
                            print("  Parameters:")
                            for param in effect.parameters:
                                param_info = (
                                    f"    - {param.name} ({param.param_type.__name__})"
                                )
                                if param.default is not None:
                                    param_info += f", default: {param.default}"
                                if (
                                    param.min_value is not None
                                    or param.max_value is not None
                                ):
                                    param_info += (
                                        f", range: {param.min_value}-{param.max_value}"
                                    )
                                if param.choices:
                                    param_info += f", choices: {param.choices}"
                                print(param_info)
                                if param.description:
                                    print(f"      {param.description}")
                        else:
                            print("  Parameters: None")
        else:
            # Simple list view
            for category, effect_names in categories.items():
                if args.category and category != args.category:
                    continue

                print(f"\n{category.upper()}:")
                for effect_name in effect_names:
                    if effect_name in effects_to_show:
                        effect = effects[effect_name]
                        print(f"  {effect.name:15} - {effect.display_name}")

        print(f"\nTotal effects: {len(effects_to_show)}")
        print(f"Categories: {', '.join(categories.keys())}")
        print("\nUse --detailed for parameter information")
        print("Use gui-image-studio-apply-effect to apply effects to images")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


def apply_effect() -> None:
    """Console script entry point for applying image effects."""
    parser = argparse.ArgumentParser(
        description="Apply image effects to files",
        prog="gui-image-studio-apply-effect",
    )
    parser.add_argument(
        "input_file",
        help="Input image file",
    )
    parser.add_argument(
        "output_file",
        help="Output image file",
    )
    parser.add_argument(
        "--effect",
        "-e",
        required=True,
        help="Effect name to apply",
    )
    parser.add_argument(
        "--params",
        "-p",
        action="append",
        help="Effect parameters in format key=value (can be used multiple times)",
    )
    parser.add_argument(
        "--list-effects",
        action="store_true",
        help="List available effects and exit",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    if args.list_effects:
        effects = EffectsRegistry.get_all_effects()
        print("Available effects:")
        for name, effect in effects.items():
            print(f"  {name:15} - {effect.display_name}")
        return

    try:
        # Check if effect exists
        effect = EffectsRegistry.get_effect(args.effect)
        if effect is None:
            print(f"Error: Unknown effect '{args.effect}'", file=sys.stderr)
            print("Use --list-effects to see available effects")
            sys.exit(1)

        # Parse parameters
        params = {}
        if args.params:
            for param_str in args.params:
                if "=" not in param_str:
                    print(
                        f"Error: Invalid parameter format '{param_str}'. Use key=value",
                        file=sys.stderr,
                    )
                    sys.exit(1)

                key, value = param_str.split("=", 1)

                # Try to convert value to appropriate type
                try:
                    # Try int first
                    if value.isdigit() or (
                        value.startswith("-") and value[1:].isdigit()
                    ):
                        params[key] = int(value)
                    # Try float
                    elif "." in value:
                        params[key] = float(value)
                    # Try boolean
                    elif value.lower() in ("true", "false"):
                        params[key] = value.lower() == "true"
                    # Keep as string
                    else:
                        params[key] = value
                except ValueError:
                    params[key] = value

        print(f"Loading image: {args.input_file}")
        image = load_image(args.input_file)

        print(f"Applying effect: {effect.display_name}")
        if params:
            print(f"Parameters: {params}")

        result = effect.apply(image, **params)

        print(f"Saving result: {args.output_file}")
        save_image(result, args.output_file)

        print("✅ Effect applied successfully!")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)
