#!/usr/bin/env python3
"""
Theming Examples - gui_image_studio
===============================

This example demonstrates how to use different themes with gui_image_studio.
Shows how images can be automatically themed based on filename prefixes.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import tkinter as tk
from tkinter import ttk

import gui_image_studio


class ThemingDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Loader - Theming Examples")
        self.root.geometry("600x400")

        self.current_theme = "default"
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Theme selection frame
        theme_frame = ttk.Frame(self.root)
        theme_frame.pack(pady=10, fill=tk.X, padx=20)

        ttk.Label(theme_frame, text="Select Theme:").pack(side=tk.LEFT)

        self.theme_var = tk.StringVar(value="default")
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["default", "dark", "light"],
            state="readonly",
        )
        theme_combo.pack(side=tk.LEFT, padx=10)
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)

        # Images display frame
        self.images_frame = ttk.Frame(self.root)
        self.images_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

        self.load_themed_images()

    def load_themed_images(self):
        """Load and display images for the current theme."""
        # Clear existing widgets
        for widget in self.images_frame.winfo_children():
            widget.destroy()

        theme = self.theme_var.get()

        # Create a grid of themed images
        images_to_load = [
            ("icon.png", "House Icon"),
            ("button.png", "Play Button"),
            ("logo.png", "Logo"),
        ]

        row = 0
        col = 0

        for image_name, description in images_to_load:
            try:
                # Load image with current theme
                image = gui_image_studio.get_image(
                    image_name, framework="tkinter", size=(64, 64), theme=theme
                )

                # Create frame for this image
                img_frame = ttk.Frame(self.images_frame)
                img_frame.grid(row=row, column=col, padx=20, pady=20)

                # Image label
                img_label = tk.Label(img_frame, image=image)
                img_label.pack()

                # Description label
                desc_label = ttk.Label(
                    img_frame, text=f"{description}\n({theme} theme)"
                )
                desc_label.pack()

                # Keep reference to prevent garbage collection
                img_label.image = image

                col += 1
                if col > 2:  # 3 columns max
                    col = 0
                    row += 1

            except ValueError as e:
                # Handle case where themed image doesn't exist
                print(f"Warning: {e}")

                # Try to load default version
                try:
                    image = gui_image_studio.get_image(
                        image_name, framework="tkinter", size=(64, 64), theme="default"
                    )

                    img_frame = ttk.Frame(self.images_frame)
                    img_frame.grid(row=row, column=col, padx=20, pady=20)

                    img_label = tk.Label(img_frame, image=image)
                    img_label.pack()

                    desc_label = ttk.Label(
                        img_frame, text=f"{description}\n(fallback to default)"
                    )
                    desc_label.pack()

                    img_label.image = image

                    col += 1
                    if col > 2:
                        col = 0
                        row += 1

                except ValueError:
                    print(f"Could not load {image_name} in any theme")

        # Add theme comparison section
        self.add_theme_comparison()

    def add_theme_comparison(self):
        """Add a section showing the same image in different themes."""
        comparison_frame = ttk.LabelFrame(self.images_frame, text="Theme Comparison")
        comparison_frame.grid(row=10, column=0, columnspan=3, pady=20, sticky="ew")

        themes = ["default", "dark", "light"]

        for i, theme in enumerate(themes):
            try:
                # Try to load icon in each theme
                image = gui_image_studio.get_image(
                    "icon.png", framework="tkinter", size=(48, 48), theme=theme
                )

                theme_frame = ttk.Frame(comparison_frame)
                theme_frame.grid(row=0, column=i, padx=10, pady=10)

                img_label = tk.Label(theme_frame, image=image)
                img_label.pack()

                theme_label = ttk.Label(theme_frame, text=theme.title())
                theme_label.pack()

                img_label.image = image

            except ValueError:
                # Theme doesn't exist, show placeholder
                theme_frame = ttk.Frame(comparison_frame)
                theme_frame.grid(row=0, column=i, padx=10, pady=10)

                placeholder = tk.Label(
                    theme_frame,
                    text="No image\navailable",
                    width=10,
                    height=3,
                    relief=tk.SUNKEN,
                )
                placeholder.pack()

                theme_label = ttk.Label(theme_frame, text=theme.title())
                theme_label.pack()

    def on_theme_change(self, event=None):
        """Handle theme selection change."""
        self.load_themed_images()

    def run(self):
        """Start the application."""
        self.root.mainloop()


def customtkinter_theming_example():
    """Example showing theming with CustomTkinter."""
    try:
        import customtkinter as ctk

        print("Running CustomTkinter theming example...")

        root = ctk.CTk()
        root.title("CustomTkinter Theming Example")
        root.geometry("500x400")

        # Current theme tracking
        current_image_theme = {"value": "default"}

        # UI Elements that will be created
        image_labels = {}

        def switch_theme():
            """Switch between light and dark appearance modes."""
            current = ctk.get_appearance_mode()
            new_mode = "light" if current.lower() == "dark" else "dark"
            ctk.set_appearance_mode(new_mode)

            # Update the theme button text
            theme_button.configure(
                text=f"Switch to {'Dark' if new_mode == 'light' else 'Light'} Mode"
            )

            # Update status
            status_label.configure(text=f"Current appearance: {new_mode.title()}")

        def switch_image_theme():
            """Switch between image themes (default, dark, light)."""
            themes = ["default", "dark", "light"]
            current_idx = themes.index(current_image_theme["value"])
            next_idx = (current_idx + 1) % len(themes)
            current_image_theme["value"] = themes[next_idx]

            load_themed_images(current_image_theme["value"])
            image_theme_button.configure(
                text=f"Image Theme: {current_image_theme['value'].title()}"
            )

        def load_themed_images(theme):
            """Load and display images with the specified theme."""
            # Clear existing images
            for widget in image_frame.winfo_children():
                widget.destroy()

            image_labels.clear()

            # Images to load
            images_to_load = [
                ("icon.png", "House Icon"),
                ("button.png", "Button"),
                ("logo.png", "Logo"),
            ]

            for i, (image_name, description) in enumerate(images_to_load):
                try:
                    # Try to load with specified theme
                    image = gui_image_studio.get_image(
                        image_name,
                        framework="customtkinter",
                        size=(64, 64),
                        theme=theme,
                    )

                    # Create container for this image
                    img_container = ctk.CTkFrame(image_frame)
                    img_container.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

                    # Image label
                    img_label = ctk.CTkLabel(img_container, image=image, text="")
                    img_label.pack(pady=5)

                    # Description label
                    desc_label = ctk.CTkLabel(
                        img_container, text=f"{description}\n({theme})"
                    )
                    desc_label.pack(pady=5)

                    image_labels[image_name] = img_label

                except ValueError as e:
                    print(
                        f"Warning: Could not load {image_name} with theme '{theme}': {e}"
                    )

                    # Try fallback to default
                    try:
                        image = gui_image_studio.get_image(
                            image_name,
                            framework="customtkinter",
                            size=(64, 64),
                            theme="default",
                        )

                        img_container = ctk.CTkFrame(image_frame)
                        img_container.grid(
                            row=0, column=i, padx=10, pady=10, sticky="nsew"
                        )

                        img_label = ctk.CTkLabel(img_container, image=image, text="")
                        img_label.pack(pady=5)

                        desc_label = ctk.CTkLabel(
                            img_container, text=f"{description}\n(fallback)"
                        )
                        desc_label.pack(pady=5)

                        image_labels[image_name] = img_label

                    except ValueError:
                        # Create placeholder
                        img_container = ctk.CTkFrame(image_frame)
                        img_container.grid(
                            row=0, column=i, padx=10, pady=10, sticky="nsew"
                        )

                        placeholder = ctk.CTkLabel(
                            img_container,
                            text="Image\nNot Available",
                            width=64,
                            height=64,
                        )
                        placeholder.pack(pady=5)

                        desc_label = ctk.CTkLabel(
                            img_container, text=f"{description}\n(missing)"
                        )
                        desc_label.pack(pady=5)

            # Configure grid weights
            for i in range(len(images_to_load)):
                image_frame.grid_columnconfigure(i, weight=1)

        # UI Setup
        title_label = ctk.CTkLabel(
            root,
            text="CustomTkinter Theming Demo",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(pady=20)

        # Control buttons frame
        controls_frame = ctk.CTkFrame(root)
        controls_frame.pack(pady=10)

        # Appearance theme button
        initial_mode = ctk.get_appearance_mode()
        theme_button = ctk.CTkButton(
            controls_frame,
            text=f"Switch to {'Light' if initial_mode.lower() == 'dark' else 'Dark'} Mode",
            command=switch_theme,
        )
        theme_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Image theme button
        image_theme_button = ctk.CTkButton(
            controls_frame,
            text=f"Image Theme: {current_image_theme['value'].title()}",
            command=switch_image_theme,
        )
        image_theme_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Status label
        status_label = ctk.CTkLabel(
            root, text=f"Current appearance: {initial_mode.title()}"
        )
        status_label.pack(pady=5)

        # Image display frame
        image_frame = ctk.CTkFrame(root)
        image_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

        # Instructions
        instructions = ctk.CTkLabel(
            root,
            text="• 'Switch Mode' changes CustomTkinter appearance (light/dark)\n• 'Image Theme' cycles through image themes (default/dark/light)",
            font=ctk.CTkFont(size=12),
        )
        instructions.pack(pady=10)

        # Load initial images
        load_themed_images(current_image_theme["value"])

        root.mainloop()

    except ImportError:
        print("CustomTkinter not installed. Skipping CustomTkinter theming example.")
        print("Install with: pip install customtkinter")


def main():
    """Run theming examples."""
    print("Image Loader - Theming Examples")
    print("===============================")
    print("1. Tkinter Theming Demo")
    print("2. CustomTkinter Theming Demo")
    print("3. Both Examples")

    choice = input("Choose an example (1-3): ").strip()

    if choice == "1":
        demo = ThemingDemo()
        demo.run()
    elif choice == "2":
        customtkinter_theming_example()
    elif choice == "3":
        demo = ThemingDemo()
        demo.run()
        customtkinter_theming_example()
    else:
        print("Invalid choice. Running Tkinter theming demo by default.")
        demo = ThemingDemo()
        demo.run()


if __name__ == "__main__":
    main()
