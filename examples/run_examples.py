#!/usr/bin/env python3
"""
GUI Image Studio Examples Runner
===============================

This script provides an easy way to run all the gui_image_studio examples.
It checks prerequisites and guides users through the available examples.
"""

import importlib.util
import os
import subprocess
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("Checking prerequisites...")

    issues = []

    # Check Python version
    if sys.version_info < (3, 7):
        issues.append("Python 3.7+ is required")

    # Check PIL/Pillow
    try:
        import PIL

        print("✓ PIL/Pillow is available")
    except ImportError:
        issues.append("PIL/Pillow is not installed. Run: pip install Pillow")

    # Check CustomTkinter (optional)
    try:
        import customtkinter

        print("✓ CustomTkinter is available")
    except ImportError:
        print(
            "⚠ CustomTkinter is not installed (optional). Run: pip install customtkinter"
        )

    # Check if embedded_images.py exists
    embedded_images_path = os.path.join(
        os.path.dirname(__file__), "..", "src", "embedded_images.py"
    )
    if os.path.exists(embedded_images_path):
        print("✓ embedded_images.py found")
    else:
        issues.append("embedded_images.py not found. Run setup first.")

    # Check if sample images exist
    sample_images_path = os.path.join(os.path.dirname(__file__), "..", "sample_images")
    if os.path.exists(sample_images_path):
        print("✓ Sample images directory found")
    else:
        issues.append("Sample images not found. Run setup first.")

    return issues


def run_setup():
    """Run the setup process to create sample images and embedded_images.py."""
    print("\nRunning setup process...")

    try:
        # Change to project root directory
        project_root = os.path.dirname(os.path.dirname(__file__))
        os.chdir(project_root)

        print("Creating sample images...")
        # Use Python module execution instead of relying on PATH
        result = subprocess.run(
            [sys.executable, "-m", "gui_image_studio.create_samples"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error creating sample images: {result.stderr}")
            return False

        print("Generating embedded_images.py...")
        # Use Python module execution instead of relying on PATH
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "gui_image_studio.generator",
                "--folder",
                "sample_images",
                "--output",
                "embedded_images.py",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error generating embedded images: {result.stderr}")
            return False

        print("✓ Setup completed successfully!")
        return True

    except Exception as e:
        print(f"Setup failed: {e}")
        return False


def run_example(example_file):
    """Run a specific example file."""
    try:
        example_path = os.path.join(os.path.dirname(__file__), example_file)
        if not os.path.exists(example_path):
            print(f"Example file not found: {example_file}")
            return False

        print(f"\nRunning {example_file}...")
        print("=" * 50)

        # Run the example
        result = subprocess.run(
            [sys.executable, example_path], cwd=os.path.dirname(__file__)
        )

        if result.returncode == 0:
            print(f"✓ {example_file} completed successfully")
        else:
            print(f"⚠ {example_file} exited with code {result.returncode}")

        return True

    except KeyboardInterrupt:
        print(f"\n{example_file} interrupted by user")
        return True
    except Exception as e:
        print(f"Error running {example_file}: {e}")
        return False


def show_menu():
    """Show the main menu."""
    print("\n" + "=" * 60)
    print("IMAGE LOADER EXAMPLES")
    print("=" * 60)
    print("Choose an example to run:")
    print()
    print("1. Basic Usage Examples")
    print("   - Fundamental usage with Tkinter and CustomTkinter")
    print("   - Loading images with default settings")
    print()
    print("2. Theming Examples")
    print("   - Theme-based image loading")
    print("   - Dynamic theme switching")
    print()
    print("3. Image Transformations")
    print("   - All transformation options with interactive controls")
    print("   - Real-time parameter adjustment")
    print()
    print("4. Animated GIFs")
    print("   - Animated GIF loading and playback")
    print("   - Animation controls and effects")
    print()
    print("5. Advanced Features")
    print("   - Format conversion, error handling, performance")
    print("   - Integration patterns and best practices")
    print()
    print("6. Run All Examples (sequentially)")
    print("7. Setup (create sample images and embedded_images.py)")
    print("8. Check Prerequisites")
    print("9. Exit")
    print()


def handle_initial_setup():
    """Handle initial prerequisite checking and setup if needed."""
    issues = check_prerequisites()

    if not issues:
        return True

    print("\n⚠ Issues found:")
    for issue in issues:
        print(f"  - {issue}")

    # Check if setup is needed and offer to run it
    setup_needed = "embedded_images.py not found" in str(
        issues
    ) or "Sample images not found" in str(issues)

    if setup_needed:
        print("\nWould you like to run setup now? (y/n): ", end="")
        if input().lower().startswith("y"):
            if run_setup():
                issues = check_prerequisites()  # Re-check
            else:
                print("Setup failed. Please resolve issues manually.")
                return False

    if issues:
        print("\nPlease resolve the above issues before running examples.")
        return False

    return True


def get_examples_list():
    """Return the list of available examples."""
    return [
        ("01_basic_usage.py", "Basic Usage Examples"),
        ("02_theming_examples.py", "Theming Examples"),
        ("03_image_transformations.py", "Image Transformations"),
        ("04_animated_gifs.py", "Animated GIFs"),
        ("05_advanced_features.py", "Advanced Features"),
    ]


def handle_prerequisites_check():
    """Handle the prerequisites check menu option."""
    issues = check_prerequisites()
    if not issues:
        print("✓ All prerequisites are met!")
    else:
        print("⚠ Issues found:")
        for issue in issues:
            print(f"  - {issue}")


def handle_run_all_examples(examples):
    """Handle running all examples sequentially."""
    print("\nRunning all examples sequentially...")
    for example_file, description in examples:
        print(f"\n--- {description} ---")
        if not run_example(example_file):
            break
        input("\nPress Enter to continue to next example...")


def handle_single_example(choice, examples):
    """Handle running a single example."""
    example_index = int(choice) - 1
    example_file, description = examples[example_index]
    run_example(example_file)


def process_user_choice(choice, examples):
    """Process the user's menu choice."""
    if choice == "9":
        print("Goodbye!")
        return False
    elif choice == "8":
        handle_prerequisites_check()
    elif choice == "7":
        run_setup()
    elif choice == "6":
        handle_run_all_examples(examples)
    elif choice in ["1", "2", "3", "4", "5"]:
        handle_single_example(choice, examples)
    else:
        print("Invalid choice. Please enter a number between 1-9.")

    return True


def main():
    """Main function."""
    print("GUI Image Studio Examples Runner")
    print("============================")

    # Initial prerequisite check and setup
    if not handle_initial_setup():
        return

    examples = get_examples_list()

    # Main menu loop
    while True:
        show_menu()

        try:
            choice = input("Enter your choice (1-9): ").strip()

            if not process_user_choice(choice, examples):
                break

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
