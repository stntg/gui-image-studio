#!/usr/bin/env python3
"""
GIF Animation Showcase - gui_image_studio
==========================================

Comprehensive demonstration of animated GIF capabilities including:
- Basic animation playback
- Speed control and frame manipulation
- Multiple simultaneous animations
- Animation with transformations
- Performance monitoring
- Custom animation controls
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import threading
import time
import tkinter as tk
from tkinter import ttk

import gui_image_studio


class GifAnimationShowcase:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI Image Studio - GIF Animation Showcase")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Animation control variables
        self.animations = {}
        self.animation_jobs = {}
        self.performance_data = {}
        self.frame_counters = {}

        self.setup_ui()
        self.load_animations()

    def setup_ui(self):
        """Set up the comprehensive user interface."""
        # Main title
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, pady=10)

        title_label = tk.Label(
            title_frame,
            text="GIF Animation Showcase",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Comprehensive animated GIF demonstrations",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#666",
        )
        subtitle_label.pack()

        # Create notebook for different sections
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create different tabs
        self.create_basic_tab()
        self.create_advanced_tab()
        self.create_performance_tab()
        self.create_gallery_tab()

        # Global controls
        self.create_global_controls()

    def create_basic_tab(self):
        """Create basic animation controls tab."""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="Basic Controls")

        # Single animation with controls
        single_frame = ttk.LabelFrame(basic_frame, text="Single Animation Control")
        single_frame.pack(fill=tk.X, padx=10, pady=10)

        # Animation display
        self.single_label = tk.Label(
            single_frame,
            text="Animation will appear here",
            width=20,
            height=10,
            relief=tk.SUNKEN,
        )
        self.single_label.pack(pady=10)

        # Controls
        controls_frame = ttk.Frame(single_frame)
        controls_frame.pack(pady=5)

        ttk.Button(
            controls_frame,
            text="▶ Play",
            command=lambda: self.start_animation("single"),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            controls_frame,
            text="⏸ Pause",
            command=lambda: self.pause_animation("single"),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            controls_frame, text="⏹ Stop", command=lambda: self.stop_animation("single")
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            controls_frame,
            text="⏮ Reset",
            command=lambda: self.reset_animation("single"),
        ).pack(side=tk.LEFT, padx=5)

        # Speed control
        speed_frame = ttk.LabelFrame(basic_frame, text="Speed Control")
        speed_frame.pack(fill=tk.X, padx=10, pady=10)

        self.speed_label = tk.Label(
            speed_frame,
            text="Speed controlled animation",
            width=20,
            height=8,
            relief=tk.SUNKEN,
        )
        self.speed_label.pack(pady=10)

        speed_controls = ttk.Frame(speed_frame)
        speed_controls.pack(pady=5)

        ttk.Label(speed_controls, text="Speed:").pack(side=tk.LEFT)

        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = tk.Scale(
            speed_controls,
            from_=0.1,
            to=5.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=self.update_speed,
            length=200,
        )
        self.speed_scale.pack(side=tk.LEFT, padx=10)

        self.speed_display = ttk.Label(speed_controls, text="1.0x")
        self.speed_display.pack(side=tk.LEFT, padx=5)

        speed_buttons = ttk.Frame(speed_frame)
        speed_buttons.pack(pady=5)

        ttk.Button(
            speed_buttons, text="Start", command=lambda: self.start_animation("speed")
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            speed_buttons, text="Stop", command=lambda: self.stop_animation("speed")
        ).pack(side=tk.LEFT, padx=5)

    def create_advanced_tab(self):
        """Create advanced animation features tab."""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="Advanced Features")

        # Transformation showcase
        transform_frame = ttk.LabelFrame(
            advanced_frame, text="Animation with Transformations"
        )
        transform_frame.pack(fill=tk.X, padx=10, pady=10)

        # Grid of transformed animations
        transform_grid = ttk.Frame(transform_frame)
        transform_grid.pack(pady=10)

        self.transform_labels = {}
        self.transform_configs = [
            ("Original", {"size": (64, 64)}),
            (
                "Tinted Blue",
                {
                    "size": (64, 64),
                    "tint_color": (100, 150, 255),
                    "tint_intensity": 0.4,
                },
            ),
            ("High Contrast", {"size": (64, 64), "contrast": 2.0, "saturation": 1.5}),
            ("Grayscale", {"size": (64, 64), "grayscale": True}),
            ("Rotated", {"size": (64, 64), "rotate": 15}),
            (
                "Scaled",
                {
                    "size": (96, 96),
                    "tint_color": (255, 200, 100),
                    "tint_intensity": 0.2,
                },
            ),
        ]

        for i, (name, config) in enumerate(self.transform_configs):
            row, col = divmod(i, 3)

            item_frame = ttk.Frame(transform_grid)
            item_frame.grid(row=row, column=col, padx=10, pady=10)

            label = tk.Label(
                item_frame, text="Loading...", width=12, height=8, relief=tk.SUNKEN
            )
            label.pack()

            name_label = ttk.Label(item_frame, text=name, font=("Arial", 9))
            name_label.pack()

            self.transform_labels[name] = label

        # Transform controls
        transform_controls = ttk.Frame(transform_frame)
        transform_controls.pack(pady=10)

        ttk.Button(
            transform_controls,
            text="Start All Transforms",
            command=self.start_transform_animations,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            transform_controls,
            text="Stop All Transforms",
            command=self.stop_transform_animations,
        ).pack(side=tk.LEFT, padx=5)

        # Synchronized animations
        sync_frame = ttk.LabelFrame(advanced_frame, text="Synchronized Animations")
        sync_frame.pack(fill=tk.X, padx=10, pady=10)

        sync_grid = ttk.Frame(sync_frame)
        sync_grid.pack(pady=10)

        self.sync_labels = []
        for i in range(4):
            label = tk.Label(
                sync_grid, text=f"Sync {i+1}", width=10, height=6, relief=tk.SUNKEN
            )
            label.grid(row=0, column=i, padx=5)
            self.sync_labels.append(label)

        sync_controls = ttk.Frame(sync_frame)
        sync_controls.pack(pady=5)

        ttk.Button(
            sync_controls,
            text="Start Synchronized",
            command=self.start_synchronized_animations,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            sync_controls,
            text="Stop Synchronized",
            command=self.stop_synchronized_animations,
        ).pack(side=tk.LEFT, padx=5)

    def create_performance_tab(self):
        """Create performance monitoring tab."""
        perf_frame = ttk.Frame(self.notebook)
        self.notebook.add(perf_frame, text="Performance")

        # Performance display
        perf_display_frame = ttk.LabelFrame(perf_frame, text="Performance Metrics")
        perf_display_frame.pack(fill=tk.X, padx=10, pady=10)

        self.perf_text = tk.Text(perf_display_frame, height=15, width=80)
        perf_scrollbar = ttk.Scrollbar(
            perf_display_frame, orient=tk.VERTICAL, command=self.perf_text.yview
        )
        self.perf_text.configure(yscrollcommand=perf_scrollbar.set)

        self.perf_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        perf_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Performance controls
        perf_controls = ttk.Frame(perf_frame)
        perf_controls.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            perf_controls,
            text="Start Performance Test",
            command=self.start_performance_test,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            perf_controls, text="Clear Log", command=self.clear_performance_log
        ).pack(side=tk.LEFT, padx=5)

        # Auto-update performance display
        self.update_performance_display()

    def create_gallery_tab(self):
        """Create animation gallery tab."""
        gallery_frame = ttk.Frame(self.notebook)
        self.notebook.add(gallery_frame, text="Gallery")

        # Multiple animations showcase
        gallery_display = ttk.LabelFrame(gallery_frame, text="Animation Gallery")
        gallery_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollable frame for gallery
        canvas = tk.Canvas(gallery_display)
        scrollbar = ttk.Scrollbar(
            gallery_display, orient=tk.VERTICAL, command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create gallery items
        self.gallery_labels = {}
        gallery_items = [
            ("Default Animation", "animation.gif", {}),
            ("Dark Theme Animation", "dark_animation.gif", {}),
            ("Small Size", "animation.gif", {"size": (32, 32)}),
            ("Large Size", "animation.gif", {"size": (96, 96)}),
            (
                "Red Tint",
                "animation.gif",
                {"tint_color": (255, 100, 100), "tint_intensity": 0.5},
            ),
            (
                "Green Tint",
                "animation.gif",
                {"tint_color": (100, 255, 100), "tint_intensity": 0.5},
            ),
            (
                "Blue Tint",
                "animation.gif",
                {"tint_color": (100, 100, 255), "tint_intensity": 0.5},
            ),
            ("High Contrast", "animation.gif", {"contrast": 2.5}),
            ("Low Saturation", "animation.gif", {"saturation": 0.3}),
            ("Grayscale", "animation.gif", {"grayscale": True}),
        ]

        for i, (name, filename, config) in enumerate(gallery_items):
            row, col = divmod(i, 5)

            item_frame = ttk.Frame(scrollable_frame)
            item_frame.grid(row=row, column=col, padx=5, pady=5)

            label = tk.Label(
                item_frame, text="Loading...", width=10, height=8, relief=tk.SUNKEN
            )
            label.pack()

            name_label = ttk.Label(item_frame, text=name, font=("Arial", 8))
            name_label.pack()

            self.gallery_labels[name] = {
                "label": label,
                "filename": filename,
                "config": config,
            }

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Gallery controls
        gallery_controls = ttk.Frame(gallery_frame)
        gallery_controls.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            gallery_controls,
            text="Start All Gallery",
            command=self.start_gallery_animations,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            gallery_controls,
            text="Stop All Gallery",
            command=self.stop_gallery_animations,
        ).pack(side=tk.LEFT, padx=5)

    def create_global_controls(self):
        """Create global control panel."""
        global_frame = tk.Frame(self.root, bg="#f0f0f0")
        global_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(
            global_frame,
            text="🎬 Start All Animations",
            command=self.start_all_animations,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            global_frame, text="⏹ Stop All Animations", command=self.stop_all_animations
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            global_frame, text="🔄 Reload All", command=self.reload_all_animations
        ).pack(side=tk.LEFT, padx=5)

        # Status display
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(global_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT, padx=10)

    def load_animations(self):
        """Load all animation data."""
        self.status_var.set("Loading animations...")

        try:
            # Basic single animation
            self.animations["single"] = gui_image_studio.get_image(
                "animation.gif",
                framework="tkinter",
                size=(80, 80),
                animated=True,
                frame_delay=150,
            )

            # Speed controlled animation
            self.animations["speed"] = gui_image_studio.get_image(
                "animation.gif",
                framework="tkinter",
                size=(64, 64),
                animated=True,
                frame_delay=100,
            )

            # Transform animations
            for name, config in self.transform_configs:
                self.animations[f"transform_{name}"] = gui_image_studio.get_image(
                    "animation.gif",
                    framework="tkinter",
                    animated=True,
                    frame_delay=120,
                    **config,
                )

            # Synchronized animations
            for i in range(4):
                self.animations[f"sync_{i}"] = gui_image_studio.get_image(
                    "animation.gif",
                    framework="tkinter",
                    size=(48, 48),
                    animated=True,
                    frame_delay=100 + (i * 20),  # Slightly different delays
                )

            # Gallery animations
            for name, data in self.gallery_labels.items():
                self.animations[f"gallery_{name}"] = gui_image_studio.get_image(
                    data["filename"],
                    framework="tkinter",
                    size=(48, 48),
                    animated=True,
                    frame_delay=150,
                    **data["config"],
                )

            self.status_var.set(f"Loaded {len(self.animations)} animations")
            self.log_performance(
                "Animation Loading",
                f"Successfully loaded {len(self.animations)} animations",
            )

        except Exception as e:
            self.status_var.set(f"Error loading animations: {e}")
            self.log_performance("Animation Loading", f"Error: {e}")

    def start_animation(self, animation_key):
        """Start a specific animation."""
        if animation_key not in self.animations:
            return

        anim_data = self.animations[animation_key]
        frames = anim_data.get("animated_frames", [])

        if not frames:
            return

        # Stop existing animation
        self.stop_animation(animation_key)

        # Get the appropriate label
        label = self.get_label_for_animation(animation_key)
        if not label:
            return

        # Initialize frame counter
        self.frame_counters[animation_key] = 0

        def animate(frame_index=0):
            if animation_key in self.animation_jobs:
                label.configure(image=frames[frame_index])
                frame_index = (frame_index + 1) % len(frames)
                self.frame_counters[animation_key] += 1

                delay = anim_data.get("frame_delay", 100)
                if animation_key == "speed":
                    delay = int(delay / self.speed_var.get())

                job_id = self.root.after(delay, animate, frame_index)
                self.animation_jobs[animation_key] = job_id

        # Start animation
        self.animation_jobs[animation_key] = True
        animate()

        self.log_performance(f"Animation {animation_key}", "Started")

    def stop_animation(self, animation_key):
        """Stop a specific animation."""
        if animation_key in self.animation_jobs:
            job_id = self.animation_jobs[animation_key]
            if job_id and job_id != True:
                self.root.after_cancel(job_id)
            del self.animation_jobs[animation_key]

            self.log_performance(f"Animation {animation_key}", "Stopped")

    def pause_animation(self, animation_key):
        """Pause a specific animation."""
        self.stop_animation(animation_key)
        self.log_performance(f"Animation {animation_key}", "Paused")

    def reset_animation(self, animation_key):
        """Reset animation to first frame."""
        self.stop_animation(animation_key)

        if animation_key in self.animations:
            anim_data = self.animations[animation_key]
            frames = anim_data.get("animated_frames", [])

            if frames:
                label = self.get_label_for_animation(animation_key)
                if label:
                    label.configure(image=frames[0])

        self.frame_counters[animation_key] = 0
        self.log_performance(f"Animation {animation_key}", "Reset")

    def get_label_for_animation(self, animation_key):
        """Get the appropriate label widget for an animation."""
        if animation_key == "single":
            return self.single_label
        elif animation_key == "speed":
            return self.speed_label
        elif animation_key.startswith("transform_"):
            name = animation_key.replace("transform_", "")
            return self.transform_labels.get(name)
        elif animation_key.startswith("sync_"):
            index = int(animation_key.split("_")[1])
            return self.sync_labels[index] if index < len(self.sync_labels) else None
        elif animation_key.startswith("gallery_"):
            name = animation_key.replace("gallery_", "")
            return self.gallery_labels.get(name, {}).get("label")

        return None

    def update_speed(self, value):
        """Update animation speed."""
        speed = float(value)
        self.speed_display.configure(text=f"{speed:.1f}x")

        # Restart speed animation if it's running
        if "speed" in self.animation_jobs:
            self.start_animation("speed")

    def start_transform_animations(self):
        """Start all transform animations."""
        for name, _ in self.transform_configs:
            self.start_animation(f"transform_{name}")

    def stop_transform_animations(self):
        """Stop all transform animations."""
        for name, _ in self.transform_configs:
            self.stop_animation(f"transform_{name}")

    def start_synchronized_animations(self):
        """Start synchronized animations."""
        for i in range(4):
            self.start_animation(f"sync_{i}")

    def stop_synchronized_animations(self):
        """Stop synchronized animations."""
        for i in range(4):
            self.stop_animation(f"sync_{i}")

    def start_gallery_animations(self):
        """Start all gallery animations."""
        for name in self.gallery_labels.keys():
            self.start_animation(f"gallery_{name}")

    def stop_gallery_animations(self):
        """Stop all gallery animations."""
        for name in self.gallery_labels.keys():
            self.stop_animation(f"gallery_{name}")

    def start_all_animations(self):
        """Start all animations."""
        for animation_key in self.animations.keys():
            self.start_animation(animation_key)

        self.status_var.set("All animations started")

    def stop_all_animations(self):
        """Stop all animations."""
        for animation_key in list(self.animation_jobs.keys()):
            self.stop_animation(animation_key)

        self.status_var.set("All animations stopped")

    def reload_all_animations(self):
        """Reload all animations."""
        self.stop_all_animations()
        self.load_animations()

    def start_performance_test(self):
        """Start performance monitoring test."""
        self.log_performance("Performance Test", "Starting comprehensive test...")

        # Start all animations for performance testing
        self.start_all_animations()

        # Schedule performance monitoring
        self.root.after(5000, self.performance_test_results)  # Test for 5 seconds

    def performance_test_results(self):
        """Display performance test results."""
        total_frames = sum(self.frame_counters.values())
        active_animations = len(self.animation_jobs)

        self.log_performance(
            "Performance Test Results", f"Total frames rendered: {total_frames}"
        )
        self.log_performance(
            "Performance Test Results", f"Active animations: {active_animations}"
        )
        self.log_performance(
            "Performance Test Results",
            f"Average FPS per animation: {total_frames / max(active_animations, 1) / 5:.2f}",
        )

        # Stop all animations after test
        self.stop_all_animations()

    def log_performance(self, category, message):
        """Log performance information."""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {category}: {message}\n"

        self.perf_text.insert(tk.END, log_entry)
        self.perf_text.see(tk.END)

    def clear_performance_log(self):
        """Clear the performance log."""
        self.perf_text.delete(1.0, tk.END)

    def update_performance_display(self):
        """Update performance display periodically."""
        active_count = len(self.animation_jobs)
        total_frames = sum(self.frame_counters.values())

        if active_count > 0:
            self.log_performance(
                "Status",
                f"Active: {active_count} animations, Total frames: {total_frames}",
            )

        # Schedule next update
        self.root.after(2000, self.update_performance_display)

    def run(self):
        """Start the application."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """Handle window closing."""
        self.stop_all_animations()
        self.root.destroy()


def main():
    """Run the GIF Animation Showcase."""
    print("Starting GIF Animation Showcase...")
    print("This demo showcases comprehensive animated GIF capabilities.")

    app = GifAnimationShowcase()
    app.run()


if __name__ == "__main__":
    main()
