#!/usr/bin/env python3
"""
Basic Usage Examples - gui_image_studio
====================================

This example demonstrates the fundamental usage of gui_image_studio with both
Tkinter and CustomTkinter frameworks.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import tkinter as tk

import gui_image_studio


def tkinter_example():
    """Basic Tkinter example with default settings."""
    print("Running Tkinter basic example...")

    root = tk.Tk()
    root.title("Basic Tkinter Example")
    root.geometry("400x300")

    # Status label for feedback
    status_label = tk.Label(
        root, text="Welcome to Tkinter Basic Example", font=("Arial", 12, "bold")
    )
    status_label.pack(pady=10)

    # Load a basic icon with default settings
    icon_image = gui_image_studio.get_image(
        "icon.png", framework="tkinter", size=(64, 64), theme="default"
    )

    # Create widgets
    icon_label = tk.Label(root, image=icon_image, text="Basic Icon", compound=tk.TOP)
    icon_label.pack(pady=10)

    # Load a button image
    button_image = gui_image_studio.get_image(
        "button.png", framework="tkinter", size=(80, 32)
    )

    # Button click counter
    click_count = {"value": 0}

    def on_button_click():
        click_count["value"] += 1
        status_label.configure(text=f"Button clicked {click_count['value']} times!")
        print(f"Tkinter button clicked {click_count['value']} times")

    def load_different_image():
        """Load a different image to show dynamic loading."""
        try:
            new_image = gui_image_studio.get_image(
                "colorful.png", framework="tkinter", size=(64, 64)
            )
            icon_label.configure(image=new_image, text="Colorful Image")
            icon_label.image = new_image  # Keep reference
            status_label.configure(text="Image changed to colorful.png")
        except Exception as e:
            status_label.configure(text=f"Error loading image: {e}")

    def reset_image():
        """Reset to original image."""
        icon_label.configure(image=icon_image, text="Basic Icon")
        status_label.configure(text="Image reset to icon.png")

    # Buttons frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=20)

    # Main button with image
    main_button = tk.Button(
        buttons_frame,
        image=button_image,
        text="Click Me",
        compound=tk.CENTER,
        command=on_button_click,
    )
    main_button.pack(side=tk.LEFT, padx=5)

    # Additional buttons to demonstrate functionality
    change_button = tk.Button(
        buttons_frame, text="Change Image", command=load_different_image
    )
    change_button.pack(side=tk.LEFT, padx=5)

    reset_button = tk.Button(buttons_frame, text="Reset Image", command=reset_image)
    reset_button.pack(side=tk.LEFT, padx=5)

    # Instructions
    instructions = tk.Label(
        root,
        text="• Click 'Click Me' to count clicks\n• Click 'Change Image' to load different image\n• Click 'Reset Image' to restore original",
        justify=tk.LEFT,
        font=("Arial", 9),
    )
    instructions.pack(pady=10)

    # Important: Keep references to prevent garbage collection
    root.icon_image = icon_image
    root.button_image = button_image

    root.mainloop()


def customtkinter_example():
    """Basic CustomTkinter example with default settings."""
    try:
        import customtkinter as ctk

        print("Running CustomTkinter basic example...")

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        root = ctk.CTk()
        root.title("Basic CustomTkinter Example")
        root.geometry("450x350")

        # Status label for feedback
        status_label = ctk.CTkLabel(
            root,
            text="Welcome to CustomTkinter Basic Example",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        status_label.pack(pady=15)

        # Load images for CustomTkinter
        icon_image = gui_image_studio.get_image(
            "icon.png", framework="customtkinter", size=(64, 64), theme="default"
        )

        button_image = gui_image_studio.get_image(
            "button.png", framework="customtkinter", size=(80, 32)
        )

        # Create widgets
        icon_label = ctk.CTkLabel(
            root, image=icon_image, text="Basic Icon", compound=tk.TOP
        )
        icon_label.pack(pady=15)

        # Button click counter
        click_count = {"value": 0}

        def on_button_click():
            click_count["value"] += 1
            status_label.configure(text=f"Button clicked {click_count['value']} times!")
            print(f"CustomTkinter button clicked {click_count['value']} times")

        def load_different_image():
            """Load a different image to show dynamic loading."""
            try:
                new_image = gui_image_studio.get_image(
                    "colorful.png", framework="customtkinter", size=(64, 64)
                )
                icon_label.configure(image=new_image, text="Colorful Image")
                status_label.configure(text="Image changed to colorful.png")
            except Exception as e:
                status_label.configure(text=f"Error loading image: {e}")

        def reset_image():
            """Reset to original image."""
            icon_label.configure(image=icon_image, text="Basic Icon")
            status_label.configure(text="Image reset to icon.png")

        def toggle_appearance():
            """Toggle between light and dark appearance modes."""
            current = ctk.get_appearance_mode()
            new_mode = "light" if current.lower() == "dark" else "dark"
            ctk.set_appearance_mode(new_mode)
            status_label.configure(text=f"Appearance changed to {new_mode} mode")

        # Buttons frame
        buttons_frame = ctk.CTkFrame(root)
        buttons_frame.pack(pady=20, padx=20, fill=tk.X)

        # Main button with image
        main_button = ctk.CTkButton(
            buttons_frame, image=button_image, text="Click Me", command=on_button_click
        )
        main_button.pack(pady=10)

        # Additional buttons in a grid
        button_grid = ctk.CTkFrame(buttons_frame)
        button_grid.pack(pady=10)

        change_button = ctk.CTkButton(
            button_grid, text="Change Image", command=load_different_image, width=120
        )
        change_button.grid(row=0, column=0, padx=5, pady=5)

        reset_button = ctk.CTkButton(
            button_grid, text="Reset Image", command=reset_image, width=120
        )
        reset_button.grid(row=0, column=1, padx=5, pady=5)

        appearance_button = ctk.CTkButton(
            button_grid, text="Toggle Theme", command=toggle_appearance, width=120
        )
        appearance_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Instructions
        instructions = ctk.CTkLabel(
            root,
            text="• Click 'Click Me' to count clicks\n• Click 'Change Image' to load different image\n• Click 'Reset Image' to restore original\n• Click 'Toggle Theme' to switch appearance",
            justify=tk.LEFT,
            font=ctk.CTkFont(size=11),
        )
        instructions.pack(pady=15)

        root.mainloop()

    except ImportError:
        print("CustomTkinter not installed. Skipping CustomTkinter example.")
        print("Install with: pip install customtkinter")


def main():
    """Run examples based on user choice."""
    print("Image Loader - Basic Usage Examples")
    print("===================================")
    print("1. Tkinter Example")
    print("2. CustomTkinter Example")
    print("3. Both Examples")

    choice = input("Choose an example (1-3): ").strip()

    if choice == "1":
        tkinter_example()
    elif choice == "2":
        customtkinter_example()
    elif choice == "3":
        tkinter_example()
        customtkinter_example()
    else:
        print("Invalid choice. Running Tkinter example by default.")
        tkinter_example()


if __name__ == "__main__":
    main()
