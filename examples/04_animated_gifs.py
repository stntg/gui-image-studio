#!/usr/bin/env python3
"""
Animated GIF Examples - gui_image_studio
====================================

This example demonstrates how to work with animated GIFs using gui_image_studio.
Shows different animation techniques and controls.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import tkinter as tk
from tkinter import ttk

import gui_image_studio


class AnimatedGifDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Loader - Animated GIF Examples")
        self.root.geometry("700x500")

        self.animations = {}  # Store animation data
        self.animation_jobs = {}  # Store after() job IDs
        self.setup_ui()
        self.load_animations()

    def setup_ui(self):
        """Set up the user interface."""
        # Title
        title_label = ttk.Label(
            self.root, text="Animated GIF Examples", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Control panel
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        # Animation controls
        ttk.Button(
            control_frame, text="Start All", command=self.start_all_animations
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            control_frame, text="Stop All", command=self.stop_all_animations
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Reload", command=self.reload_animations).pack(
            side=tk.LEFT, padx=5
        )

        # Main content area
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create animation display areas
        self.create_animation_sections()

    def create_animation_sections(self):
        """Create sections for different animation examples."""
        # Basic animation section
        basic_frame = ttk.LabelFrame(self.content_frame, text="Basic Animation")
        basic_frame.pack(fill=tk.X, pady=5)

        self.basic_label = tk.Label(basic_frame, text="Animation will appear here")
        self.basic_label.pack(pady=10)

        basic_controls = ttk.Frame(basic_frame)
        basic_controls.pack()

        ttk.Button(
            basic_controls, text="Start", command=lambda: self.start_animation("basic")
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            basic_controls, text="Stop", command=lambda: self.stop_animation("basic")
        ).pack(side=tk.LEFT, padx=5)

        # Transformed animation section
        transform_frame = ttk.LabelFrame(
            self.content_frame, text="Transformed Animation"
        )
        transform_frame.pack(fill=tk.X, pady=5)

        transform_content = ttk.Frame(transform_frame)
        transform_content.pack(fill=tk.X, pady=10)

        # Multiple transformed versions
        self.transform_labels = {}
        transform_configs = [
            ("Original", {}),
            ("Tinted Green", {"tint_color": (0, 255, 0), "tint_intensity": 0.3}),
            ("High Contrast", {"contrast": 1.8, "saturation": 1.2}),
            ("Grayscale", {"grayscale": True}),
        ]

        for i, (name, config) in enumerate(transform_configs):
            col_frame = ttk.Frame(transform_content)
            col_frame.grid(row=0, column=i, padx=10)

            label = tk.Label(col_frame, text="Loading...")
            label.pack()

            name_label = ttk.Label(col_frame, text=name)
            name_label.pack()

            self.transform_labels[name] = label

        transform_controls = ttk.Frame(transform_frame)
        transform_controls.pack()

        ttk.Button(
            transform_controls,
            text="Start All",
            command=self.start_transform_animations,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            transform_controls, text="Stop All", command=self.stop_transform_animations
        ).pack(side=tk.LEFT, padx=5)

        # Speed control section
        speed_frame = ttk.LabelFrame(self.content_frame, text="Speed Control")
        speed_frame.pack(fill=tk.X, pady=5)

        self.speed_label = tk.Label(speed_frame, text="Speed controlled animation")
        self.speed_label.pack(pady=10)

        speed_controls = ttk.Frame(speed_frame)
        speed_controls.pack()

        ttk.Label(speed_controls, text="Speed:").pack(side=tk.LEFT)

        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(
            speed_controls,
            from_=0.1,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=self.update_speed,
        )
        speed_scale.pack(side=tk.LEFT, padx=10)

        ttk.Button(
            speed_controls, text="Start", command=lambda: self.start_speed_animation()
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            speed_controls, text="Stop", command=lambda: self.stop_animation("speed")
        ).pack(side=tk.LEFT, padx=5)

    def load_animations(self):
        """Load all animation data."""
        try:
            # Basic animation
            self.animations["basic"] = gui_image_studio.get_image(
                "animation.gif",
                framework="tkinter",
                size=(64, 64),
                theme="default",
                animated=True,
                frame_delay=150,
            )

            # Transformed animations
            transform_configs = [
                ("Original", {}),
                ("Tinted Green", {"tint_color": (0, 255, 0), "tint_intensity": 0.3}),
                ("High Contrast", {"contrast": 1.8, "saturation": 1.2}),
                ("Grayscale", {"grayscale": True}),
            ]

            for name, config in transform_configs:
                self.animations[f"transform_{name}"] = gui_image_studio.get_image(
                    "animation.gif",
                    framework="tkinter",
                    size=(48, 48),
                    theme="default",
                    animated=True,
                    frame_delay=120,
                    **config,
                )

            # Speed control animation
            self.animations["speed"] = gui_image_studio.get_image(
                "animation.gif",
                framework="tkinter",
                size=(64, 64),
                theme="default",
                animated=True,
                frame_delay=100,
            )

            print("All animations loaded successfully!")

        except Exception as e:
            print(f"Error loading animations: {e}")
            # Create fallback message
            for key in ["basic", "speed"]:
                self.animations[key] = {"animated_frames": [], "frame_delay": 100}

    def start_animation(self, animation_key):
        """Start a specific animation."""
        if animation_key not in self.animations:
            return

        anim_data = self.animations[animation_key]
        frames = anim_data["animated_frames"]

        if not frames:
            return

        # Stop existing animation
        self.stop_animation(animation_key)

        # Get the appropriate label
        if animation_key == "basic":
            label = self.basic_label
        elif animation_key == "speed":
            label = self.speed_label
        else:
            return

        def animate(frame_index=0):
            if animation_key in self.animation_jobs:  # Check if still running
                label.configure(image=frames[frame_index])
                frame_index = (frame_index + 1) % len(frames)

                delay = anim_data["frame_delay"]
                if animation_key == "speed":
                    delay = int(delay / self.speed_var.get())

                job_id = self.root.after(delay, animate, frame_index)
                self.animation_jobs[animation_key] = job_id

        # Start animation
        self.animation_jobs[animation_key] = True  # Mark as running
        animate()

    def stop_animation(self, animation_key):
        """Stop a specific animation."""
        if animation_key in self.animation_jobs:
            job_id = self.animation_jobs[animation_key]
            if job_id and job_id != True:
                self.root.after_cancel(job_id)
            del self.animation_jobs[animation_key]

    def start_transform_animations(self):
        """Start all transformed animations."""
        transform_configs = [
            ("Original", {}),
            ("Tinted Green", {"tint_color": (0, 255, 0), "tint_intensity": 0.3}),
            ("High Contrast", {"contrast": 1.8, "saturation": 1.2}),
            ("Grayscale", {"grayscale": True}),
        ]

        for name, config in transform_configs:
            animation_key = f"transform_{name}"
            if animation_key not in self.animations:
                continue

            anim_data = self.animations[animation_key]
            frames = anim_data["animated_frames"]

            if not frames:
                continue

            # Stop existing animation
            self.stop_animation(animation_key)

            label = self.transform_labels[name]

            def make_animate(anim_key, lbl):
                def animate(frame_index=0):
                    if anim_key in self.animation_jobs:
                        lbl.configure(image=frames[frame_index])
                        frame_index = (frame_index + 1) % len(frames)
                        job_id = self.root.after(
                            anim_data["frame_delay"], animate, frame_index
                        )
                        self.animation_jobs[anim_key] = job_id

                return animate

            self.animation_jobs[animation_key] = True
            make_animate(animation_key, label)()

    def stop_transform_animations(self):
        """Stop all transformed animations."""
        transform_names = ["Original", "Tinted Green", "High Contrast", "Grayscale"]
        for name in transform_names:
            self.stop_animation(f"transform_{name}")

    def start_speed_animation(self):
        """Start the speed-controlled animation."""
        self.start_animation("speed")

    def update_speed(self, value):
        """Update animation speed."""
        # Restart speed animation if it's running
        if "speed" in self.animation_jobs:
            self.start_speed_animation()

    def start_all_animations(self):
        """Start all animations."""
        self.start_animation("basic")
        self.start_transform_animations()
        self.start_speed_animation()

    def stop_all_animations(self):
        """Stop all animations."""
        for key in list(self.animation_jobs.keys()):
            self.stop_animation(key)

    def reload_animations(self):
        """Reload all animations."""
        self.stop_all_animations()
        self.load_animations()

    def run(self):
        """Start the application."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """Handle window closing."""
        self.stop_all_animations()
        self.root.destroy()


def customtkinter_animation_example():
    """Example of animated GIFs with CustomTkinter."""
    try:
        import customtkinter as ctk

        print("Running CustomTkinter animation example...")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        root = ctk.CTk()
        root.title("CustomTkinter Animated GIF")
        root.geometry("400x300")

        # Load animated GIF
        try:
            anim_data = gui_image_studio.get_image(
                "animation.gif",
                framework="customtkinter",
                size=(80, 80),
                theme="dark",
                animated=True,
                tint_color=(100, 150, 255),
                tint_intensity=0.2,
                frame_delay=120,
            )

            frames = anim_data["animated_frames"]
            delay = anim_data["frame_delay"]

            if frames:
                label = ctk.CTkLabel(root, text="")
                label.pack(pady=20)

                animation_running = {"value": False}

                def animate(frame_index=0):
                    if animation_running["value"]:
                        label.configure(image=frames[frame_index])
                        frame_index = (frame_index + 1) % len(frames)
                        root.after(delay, animate, frame_index)

                def start_animation():
                    animation_running["value"] = True
                    animate()

                def stop_animation():
                    animation_running["value"] = False

                # Control buttons
                button_frame = ctk.CTkFrame(root)
                button_frame.pack(pady=20)

                start_btn = ctk.CTkButton(
                    button_frame, text="Start", command=start_animation
                )
                start_btn.pack(side=tk.LEFT, padx=10)

                stop_btn = ctk.CTkButton(
                    button_frame, text="Stop", command=stop_animation
                )
                stop_btn.pack(side=tk.LEFT, padx=10)

                # Start automatically
                start_animation()

            else:
                error_label = ctk.CTkLabel(root, text="No animation frames available")
                error_label.pack(pady=20)

        except Exception as e:
            error_label = ctk.CTkLabel(root, text=f"Error loading animation:\n{str(e)}")
            error_label.pack(pady=20)

        root.mainloop()

    except ImportError:
        print("CustomTkinter not installed. Skipping CustomTkinter animation example.")


def main():
    """Run animated GIF examples."""
    print("Image Loader - Animated GIF Examples")
    print("===================================")
    print("1. Tkinter Animation Demo")
    print("2. CustomTkinter Animation Demo")
    print("3. Both Examples")

    choice = input("Choose an example (1-3): ").strip()

    if choice == "1":
        demo = AnimatedGifDemo()
        demo.run()
    elif choice == "2":
        customtkinter_animation_example()
    elif choice == "3":
        demo = AnimatedGifDemo()
        demo.run()
        customtkinter_animation_example()
    else:
        print("Invalid choice. Running Tkinter animation demo by default.")
        demo = AnimatedGifDemo()
        demo.run()


if __name__ == "__main__":
    main()
