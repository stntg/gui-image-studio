#!/usr/bin/env python3
"""
CustomTkinter GIF Animations - gui_image_studio
===============================================

Specialized examples for animated GIFs in CustomTkinter applications.
Demonstrates modern UI patterns with animated elements.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    import customtkinter as ctk

    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    print(
        "CustomTkinter not available. Please install it with: pip install customtkinter"
    )

import gui_image_studio


class CTkGifAnimationDemo:
    def __init__(self):
        if not CTK_AVAILABLE:
            return

        # Configure CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("GUI Image Studio - CustomTkinter GIF Animations")
        self.root.geometry("900x600")

        # Animation control
        self.animations = {}
        self.animation_jobs = {}
        self.animation_states = {}

        self.setup_ui()
        self.load_animations()

    def setup_ui(self):
        """Set up the CustomTkinter interface."""
        # Main title
        title_label = ctk.CTkLabel(
            self.root,
            text="CustomTkinter GIF Animations",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.pack(pady=20)

        # Create tabview
        self.tabview = ctk.CTkTabview(self.root, width=850, height=500)
        self.tabview.pack(padx=20, pady=10)

        # Add tabs
        self.tabview.add("Loading Animations")
        self.tabview.add("Interactive Elements")
        self.tabview.add("Themed Animations")
        self.tabview.add("Advanced Controls")

        self.setup_loading_tab()
        self.setup_interactive_tab()
        self.setup_themed_tab()
        self.setup_advanced_tab()

        # Global controls
        self.setup_global_controls()

    def setup_loading_tab(self):
        """Set up loading animations tab."""
        tab = self.tabview.tab("Loading Animations")

        # Loading spinners section
        spinner_frame = ctk.CTkFrame(tab)
        spinner_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            spinner_frame,
            text="Loading Spinners",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        spinner_container = ctk.CTkFrame(spinner_frame)
        spinner_container.pack(pady=10)

        # Different sized spinners
        self.spinner_labels = {}
        spinner_configs = [
            ("Small", {"size": (32, 32)}),
            ("Medium", {"size": (48, 48)}),
            ("Large", {"size": (64, 64)}),
            ("Extra Large", {"size": (80, 80)}),
        ]

        for i, (name, config) in enumerate(spinner_configs):
            frame = ctk.CTkFrame(spinner_container)
            frame.grid(row=0, column=i, padx=10, pady=10)

            label = ctk.CTkLabel(frame, text="")
            label.pack(pady=10)

            name_label = ctk.CTkLabel(frame, text=name)
            name_label.pack()

            self.spinner_labels[name] = label

        # Spinner controls
        spinner_controls = ctk.CTkFrame(spinner_frame)
        spinner_controls.pack(pady=10)

        ctk.CTkButton(
            spinner_controls, text="Start Spinners", command=self.start_spinners
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            spinner_controls, text="Stop Spinners", command=self.stop_spinners
        ).pack(side="left", padx=5)

        # Progress indicators
        progress_frame = ctk.CTkFrame(tab)
        progress_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            progress_frame,
            text="Animated Progress Indicators",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        self.progress_label = ctk.CTkLabel(progress_frame, text="")
        self.progress_label.pack(pady=10)

        progress_controls = ctk.CTkFrame(progress_frame)
        progress_controls.pack(pady=10)

        ctk.CTkButton(
            progress_controls,
            text="Start Progress",
            command=self.start_progress_animation,
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            progress_controls,
            text="Stop Progress",
            command=self.stop_progress_animation,
        ).pack(side="left", padx=5)

    def setup_interactive_tab(self):
        """Set up interactive elements tab."""
        tab = self.tabview.tab("Interactive Elements")

        # Animated buttons
        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            button_frame,
            text="Animated Buttons",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        button_container = ctk.CTkFrame(button_frame)
        button_container.pack(pady=10)

        # Create animated buttons
        self.animated_buttons = {}
        button_types = ["Play", "Pause", "Stop", "Record"]

        for i, btn_type in enumerate(button_types):
            btn_frame = ctk.CTkFrame(button_container)
            btn_frame.grid(row=0, column=i, padx=10, pady=10)

            # Animated icon
            icon_label = ctk.CTkLabel(btn_frame, text="")
            icon_label.pack(pady=5)

            # Button
            button = ctk.CTkButton(
                btn_frame,
                text=btn_type,
                width=80,
                command=lambda t=btn_type: self.toggle_button_animation(t),
            )
            button.pack(pady=5)

            self.animated_buttons[btn_type] = {"icon": icon_label, "button": button}

        # Hover effects
        hover_frame = ctk.CTkFrame(tab)
        hover_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            hover_frame,
            text="Hover Animations",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        self.hover_label = ctk.CTkLabel(hover_frame, text="Hover over me!")
        self.hover_label.pack(pady=20)

        # Bind hover events
        self.hover_label.bind("<Enter>", self.on_hover_enter)
        self.hover_label.bind("<Leave>", self.on_hover_leave)

    def setup_themed_tab(self):
        """Set up themed animations tab."""
        tab = self.tabview.tab("Themed Animations")

        # Theme selector
        theme_selector_frame = ctk.CTkFrame(tab)
        theme_selector_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            theme_selector_frame,
            text="Theme Selection",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        theme_controls = ctk.CTkFrame(theme_selector_frame)
        theme_controls.pack(pady=10)

        self.theme_var = ctk.StringVar(value="dark")

        ctk.CTkRadioButton(
            theme_controls,
            text="Dark Theme",
            variable=self.theme_var,
            value="dark",
            command=self.change_theme,
        ).pack(side="left", padx=10)
        ctk.CTkRadioButton(
            theme_controls,
            text="Light Theme",
            variable=self.theme_var,
            value="light",
            command=self.change_theme,
        ).pack(side="left", padx=10)

        # Themed animations display
        themed_frame = ctk.CTkFrame(tab)
        themed_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            themed_frame,
            text="Themed Animations",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        themed_container = ctk.CTkFrame(themed_frame)
        themed_container.pack(pady=10)

        self.themed_labels = {}
        themed_types = ["Default", "Accent", "Success", "Warning", "Error"]

        for i, theme_type in enumerate(themed_types):
            frame = ctk.CTkFrame(themed_container)
            frame.grid(row=0, column=i, padx=10, pady=10)

            label = ctk.CTkLabel(frame, text="")
            label.pack(pady=10)

            type_label = ctk.CTkLabel(frame, text=theme_type)
            type_label.pack()

            self.themed_labels[theme_type] = label

        # Themed controls
        themed_controls = ctk.CTkFrame(themed_frame)
        themed_controls.pack(pady=10)

        ctk.CTkButton(
            themed_controls, text="Start Themed", command=self.start_themed_animations
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            themed_controls, text="Stop Themed", command=self.stop_themed_animations
        ).pack(side="left", padx=5)

    def setup_advanced_tab(self):
        """Set up advanced controls tab."""
        tab = self.tabview.tab("Advanced Controls")

        # Performance monitor
        perf_frame = ctk.CTkFrame(tab)
        perf_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            perf_frame,
            text="Performance Monitor",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        self.perf_textbox = ctk.CTkTextbox(perf_frame, height=150)
        self.perf_textbox.pack(fill="x", padx=10, pady=10)

        perf_controls = ctk.CTkFrame(perf_frame)
        perf_controls.pack(pady=10)

        ctk.CTkButton(
            perf_controls,
            text="Start Monitoring",
            command=self.start_performance_monitoring,
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            perf_controls, text="Clear Log", command=self.clear_performance_log
        ).pack(side="left", padx=5)

        # Advanced animation controls
        advanced_frame = ctk.CTkFrame(tab)
        advanced_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            advanced_frame,
            text="Advanced Animation Controls",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        # Speed control
        speed_frame = ctk.CTkFrame(advanced_frame)
        speed_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(speed_frame, text="Global Speed:").pack(side="left", padx=10)

        self.speed_var = ctk.DoubleVar(value=1.0)
        self.speed_slider = ctk.CTkSlider(
            speed_frame,
            from_=0.1,
            to=3.0,
            variable=self.speed_var,
            command=self.update_global_speed,
        )
        self.speed_slider.pack(side="left", padx=10, fill="x", expand=True)

        self.speed_label = ctk.CTkLabel(speed_frame, text="1.0x")
        self.speed_label.pack(side="left", padx=10)

        # Quality control
        quality_frame = ctk.CTkFrame(advanced_frame)
        quality_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(quality_frame, text="Animation Quality:").pack(
            side="left", padx=10
        )

        self.quality_var = ctk.StringVar(value="high")
        quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            values=["low", "medium", "high"],
            variable=self.quality_var,
            command=self.update_quality,
        )
        quality_menu.pack(side="left", padx=10)

    def setup_global_controls(self):
        """Set up global control panel."""
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            control_frame, text="🎬 Start All", command=self.start_all_animations
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            control_frame, text="⏹ Stop All", command=self.stop_all_animations
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            control_frame, text="🔄 Reload", command=self.reload_animations
        ).pack(side="left", padx=5)

        # Status
        self.status_label = ctk.CTkLabel(control_frame, text="Ready")
        self.status_label.pack(side="right", padx=10)

    def load_animations(self):
        """Load all animation data for CustomTkinter."""
        self.status_label.configure(text="Loading animations...")

        try:
            # Spinner animations
            spinner_configs = [
                ("Small", {"size": (32, 32)}),
                ("Medium", {"size": (48, 48)}),
                ("Large", {"size": (64, 64)}),
                ("Extra Large", {"size": (80, 80)}),
            ]

            for name, config in spinner_configs:
                self.animations[f"spinner_{name}"] = gui_image_studio.get_image(
                    "animation.gif",
                    framework="customtkinter",
                    animated=True,
                    frame_delay=100,
                    **config,
                )

            # Progress animation
            self.animations["progress"] = gui_image_studio.get_image(
                "animation.gif",
                framework="customtkinter",
                size=(64, 64),
                animated=True,
                frame_delay=80,
                tint_color=(0, 150, 255),
                tint_intensity=0.3,
            )

            # Button animations
            button_types = ["Play", "Pause", "Stop", "Record"]
            for btn_type in button_types:
                self.animations[f"button_{btn_type}"] = gui_image_studio.get_image(
                    "animation.gif",
                    framework="customtkinter",
                    size=(32, 32),
                    animated=True,
                    frame_delay=150,
                )

            # Hover animation
            self.animations["hover"] = gui_image_studio.get_image(
                "animation.gif",
                framework="customtkinter",
                size=(48, 48),
                animated=True,
                frame_delay=120,
                tint_color=(255, 200, 100),
                tint_intensity=0.4,
            )

            # Themed animations
            theme_colors = {
                "Default": (100, 150, 255),
                "Accent": (255, 100, 150),
                "Success": (100, 255, 150),
                "Warning": (255, 200, 100),
                "Error": (255, 100, 100),
            }

            for theme_type, color in theme_colors.items():
                self.animations[f"themed_{theme_type}"] = gui_image_studio.get_image(
                    "animation.gif",
                    framework="customtkinter",
                    size=(48, 48),
                    animated=True,
                    frame_delay=130,
                    tint_color=color,
                    tint_intensity=0.5,
                )

            self.status_label.configure(
                text=f"Loaded {len(self.animations)} animations"
            )
            self.log_performance(
                f"Successfully loaded {len(self.animations)} animations"
            )

        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")
            self.log_performance(f"Error loading animations: {e}")

    def start_animation(self, animation_key, label_widget):
        """Start a specific animation."""
        if animation_key not in self.animations:
            return

        anim_data = self.animations[animation_key]
        frames = anim_data.get("animated_frames", [])

        if not frames:
            return

        # Stop existing animation
        self.stop_animation(animation_key)

        # Mark as active
        self.animation_states[animation_key] = True

        def animate(frame_index=0):
            if self.animation_states.get(animation_key, False):
                label_widget.configure(image=frames[frame_index])
                frame_index = (frame_index + 1) % len(frames)

                delay = int(anim_data.get("frame_delay", 100) / self.speed_var.get())
                job_id = self.root.after(delay, animate, frame_index)
                self.animation_jobs[animation_key] = job_id

        animate()

    def stop_animation(self, animation_key):
        """Stop a specific animation."""
        self.animation_states[animation_key] = False

        if animation_key in self.animation_jobs:
            job_id = self.animation_jobs[animation_key]
            if job_id:
                self.root.after_cancel(job_id)
            del self.animation_jobs[animation_key]

    def start_spinners(self):
        """Start all spinner animations."""
        for name in ["Small", "Medium", "Large", "Extra Large"]:
            label = self.spinner_labels[name]
            self.start_animation(f"spinner_{name}", label)

    def stop_spinners(self):
        """Stop all spinner animations."""
        for name in ["Small", "Medium", "Large", "Extra Large"]:
            self.stop_animation(f"spinner_{name}")

    def start_progress_animation(self):
        """Start progress animation."""
        self.start_animation("progress", self.progress_label)

    def stop_progress_animation(self):
        """Stop progress animation."""
        self.stop_animation("progress")

    def toggle_button_animation(self, button_type):
        """Toggle button animation."""
        animation_key = f"button_{button_type}"

        if self.animation_states.get(animation_key, False):
            self.stop_animation(animation_key)
            self.animated_buttons[button_type]["button"].configure(
                text=f"Start {button_type}"
            )
        else:
            label = self.animated_buttons[button_type]["icon"]
            self.start_animation(animation_key, label)
            self.animated_buttons[button_type]["button"].configure(
                text=f"Stop {button_type}"
            )

    def on_hover_enter(self, event):
        """Handle hover enter."""
        self.start_animation("hover", self.hover_label)

    def on_hover_leave(self, event):
        """Handle hover leave."""
        self.stop_animation("hover")
        self.hover_label.configure(image="", text="Hover over me!")

    def change_theme(self):
        """Change application theme."""
        theme = self.theme_var.get()
        ctk.set_appearance_mode(theme)
        self.log_performance(f"Theme changed to: {theme}")

    def start_themed_animations(self):
        """Start themed animations."""
        for theme_type in ["Default", "Accent", "Success", "Warning", "Error"]:
            label = self.themed_labels[theme_type]
            self.start_animation(f"themed_{theme_type}", label)

    def stop_themed_animations(self):
        """Stop themed animations."""
        for theme_type in ["Default", "Accent", "Success", "Warning", "Error"]:
            self.stop_animation(f"themed_{theme_type}")

    def update_global_speed(self, value):
        """Update global animation speed."""
        speed = float(value)
        self.speed_label.configure(text=f"{speed:.1f}x")
        self.log_performance(f"Global speed changed to: {speed:.1f}x")

    def update_quality(self, quality):
        """Update animation quality."""
        self.log_performance(f"Animation quality changed to: {quality}")

    def start_performance_monitoring(self):
        """Start performance monitoring."""
        self.log_performance("Performance monitoring started")
        self.monitor_performance()

    def monitor_performance(self):
        """Monitor animation performance."""
        active_animations = sum(1 for state in self.animation_states.values() if state)
        self.log_performance(f"Active animations: {active_animations}")

        if active_animations > 0:
            self.root.after(1000, self.monitor_performance)

    def log_performance(self, message):
        """Log performance message."""
        import time

        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        current_text = self.perf_textbox.get("1.0", "end")
        self.perf_textbox.delete("1.0", "end")
        self.perf_textbox.insert("1.0", log_entry + current_text)

    def clear_performance_log(self):
        """Clear performance log."""
        self.perf_textbox.delete("1.0", "end")

    def start_all_animations(self):
        """Start all animations."""
        self.start_spinners()
        self.start_progress_animation()
        self.start_themed_animations()
        self.status_label.configure(text="All animations started")

    def stop_all_animations(self):
        """Stop all animations."""
        for animation_key in list(self.animation_states.keys()):
            self.stop_animation(animation_key)

        # Reset button states
        for button_type in ["Play", "Pause", "Stop", "Record"]:
            self.animated_buttons[button_type]["button"].configure(text=button_type)

        self.status_label.configure(text="All animations stopped")

    def reload_animations(self):
        """Reload all animations."""
        self.stop_all_animations()
        self.load_animations()

    def run(self):
        """Start the application."""
        if not CTK_AVAILABLE:
            print("CustomTkinter is required for this example.")
            return

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """Handle window closing."""
        self.stop_all_animations()
        self.root.destroy()


def main():
    """Run the CustomTkinter GIF Animation Demo."""
    if not CTK_AVAILABLE:
        print("This example requires CustomTkinter.")
        print("Install it with: pip install customtkinter")
        return

    print("Starting CustomTkinter GIF Animation Demo...")

    app = CTkGifAnimationDemo()
    app.run()


if __name__ == "__main__":
    main()
