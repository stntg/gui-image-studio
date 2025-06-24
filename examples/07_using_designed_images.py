#!/usr/bin/env python3
"""
Example 07: Using Images Created with the Designer GUI
======================================================

This example demonstrates how to use images that were created with
the GUI Image Studio Designer in your actual GUI applications.

Workflow:
1. Create images using the Designer GUI (example 06)
2. Generate embedded code file (e.g., my_embedded_images.py)
3. Import and use the images in your GUI application (this example)

This example shows both tkinter and customtkinter usage.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

# Add the src directory to the Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    import gui_image_studio

    # Try to import customtkinter for enhanced GUI
    try:
        import customtkinter as ctk

        CUSTOMTKINTER_AVAILABLE = True
    except ImportError:
        CUSTOMTKINTER_AVAILABLE = False

except ImportError as e:
    print(f"Error importing gui_image_studio: {e}")
    sys.exit(1)


class ImageDisplayDemo:
    """Demo application showing how to use designer-created images."""

    def __init__(self):
        self.embedded_images_file = None
        self.embedded_module = None

    def create_tkinter_demo(self):
        """Create a tkinter demo window."""
        root = tk.Tk()
        root.title("Designer Images Demo - Tkinter")
        root.geometry("600x500")

        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="1. Use the Image Designer GUI to create images\n"
            "2. Generate embedded code file\n"
            "3. Load the file here to see your images",
            justify=tk.CENTER,
        )
        instructions.pack(pady=10)

        # Load button
        load_btn = ttk.Button(
            main_frame,
            text="Load Embedded Images File",
            command=self.load_embedded_file,
        )
        load_btn.pack(pady=10)

        # Images frame
        self.images_frame = ttk.LabelFrame(main_frame, text="Your Designer Images")
        self.images_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Status
        self.status_var = tk.StringVar(value="No embedded images loaded")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=5)

        root.mainloop()

    def create_customtkinter_demo(self):
        """Create a customtkinter demo window."""
        if not CUSTOMTKINTER_AVAILABLE:
            messagebox.showerror("Error", "CustomTkinter not available")
            return

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        root = ctk.CTk()
        root.title("Designer Images Demo - CustomTkinter")
        root.geometry("600x500")

        # Main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Instructions
        instructions = ctk.CTkLabel(
            main_frame,
            text="1. Use the Image Designer GUI to create images\n"
            "2. Generate embedded code file\n"
            "3. Load the file here to see your images",
            justify="center",
        )
        instructions.pack(pady=10)

        # Load button
        load_btn = ctk.CTkButton(
            main_frame,
            text="Load Embedded Images File",
            command=self.load_embedded_file,
        )
        load_btn.pack(pady=10)

        # Images frame
        self.images_frame = ctk.CTkFrame(main_frame)
        self.images_frame.pack(fill="both", expand=True, pady=10)

        # Status
        self.status_var = tk.StringVar(value="No embedded images loaded")
        status_label = ctk.CTkLabel(main_frame, textvariable=self.status_var)
        status_label.pack(pady=5)

        root.mainloop()

    def load_embedded_file(self):
        """Load an embedded images file."""
        from tkinter import filedialog

        file_path = filedialog.askopenfilename(
            title="Select Embedded Images File",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )

        if not file_path:
            return

        try:
            # Import the embedded images module dynamically
            import importlib.util

            spec = importlib.util.spec_from_file_location("embedded_images", file_path)
            self.embedded_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.embedded_module)

            self.display_images()
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load embedded images: {str(e)}")

    def display_images(self):
        """Display the loaded images."""
        if not self.embedded_module:
            return

        # Clear existing widgets
        for widget in self.images_frame.winfo_children():
            widget.destroy()

        try:
            # Get the embedded images dictionary
            if hasattr(self.embedded_module, "embedded_images"):
                images_dict = self.embedded_module.embedded_images
            else:
                messagebox.showerror("Error", "No embedded_images found in file")
                return

            # Create a scrollable frame for images
            canvas = tk.Canvas(self.images_frame)
            scrollbar = ttk.Scrollbar(
                self.images_frame, orient="vertical", command=canvas.yview
            )
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Display images by theme
            row = 0
            for theme, theme_images in images_dict.items():
                # Theme header
                theme_label = ttk.Label(
                    scrollable_frame, text=f"Theme: {theme}", font=("Arial", 12, "bold")
                )
                theme_label.grid(
                    row=row, column=0, columnspan=3, sticky="w", pady=(10, 5)
                )
                row += 1

                # Images in this theme
                col = 0
                for image_name, image_data in theme_images.items():
                    try:
                        # Use gui_image_studio to load the image
                        # Note: This would work if the embedded module has get_image function
                        if hasattr(self.embedded_module, "get_image"):
                            photo = self.embedded_module.get_image(image_name)
                        else:
                            # Fallback: decode base64 manually
                            import base64
                            from io import BytesIO

                            from PIL import Image, ImageTk

                            image_bytes = base64.b64decode(image_data)
                            pil_image = Image.open(BytesIO(image_bytes))
                            # Resize for display if too large
                            if pil_image.width > 100 or pil_image.height > 100:
                                pil_image.thumbnail((100, 100), Image.LANCZOS)
                            photo = ImageTk.PhotoImage(pil_image)

                        # Create image display
                        img_frame = ttk.Frame(scrollable_frame)
                        img_frame.grid(row=row, column=col, padx=5, pady=5)

                        img_label = ttk.Label(img_frame, image=photo)
                        img_label.image = photo  # Keep a reference
                        img_label.pack()

                        name_label = ttk.Label(img_frame, text=image_name)
                        name_label.pack()

                        col += 1
                        if col >= 3:  # 3 images per row
                            col = 0
                            row += 1

                    except Exception as e:
                        print(f"Error displaying image {image_name}: {e}")

                if col > 0:  # Move to next row if we have partial row
                    row += 1

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display images: {str(e)}")


def main():
    """Main function to run the demo."""
    print("GUI Image Studio - Using Designer Images Demo")
    print("=" * 50)
    print()
    print("This demo shows how to use images created with the Designer GUI")
    print("in your actual GUI applications.")
    print()
    print("Choose your GUI framework:")
    print("1. Tkinter (built-in)")
    print("2. CustomTkinter (modern)")
    print()

    while True:
        try:
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == "1":
                demo = ImageDisplayDemo()
                demo.create_tkinter_demo()
                break
            elif choice == "2":
                if CUSTOMTKINTER_AVAILABLE:
                    demo = ImageDisplayDemo()
                    demo.create_customtkinter_demo()
                    break
                else:
                    print(
                        "CustomTkinter not available. Install with: pip install customtkinter"
                    )
                    print("Falling back to Tkinter...")
                    demo = ImageDisplayDemo()
                    demo.create_tkinter_demo()
                    break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
