Animation Creation
==================

This guide demonstrates how to create and work with animations using GUI Image Studio, including loading animated GIFs, creating custom animations, and implementing animation playback in your applications.

Loading Animated GIFs
----------------------

Basic Animation Loading
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gui_image_studio import get_image
    import tkinter as tk

    # Load animated GIF
    animation_data = get_image(
        "spinner.gif",
        framework="tkinter",
        size=(100, 100),
        animated=True,
        frame_delay=100
    )

    # Extract animation components
    frames = animation_data["animated_frames"]
    delay = animation_data["frame_delay"]
    frame_count = len(frames)

    print(f"Loaded {frame_count} frames with {delay}ms delay")

Animation with Transformations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Apply effects to animated GIF
    enhanced_animation = get_image(
        "animation.gif",
        framework="customtkinter",
        size=(200, 200),
        animated=True,
        frame_delay=80,
        tint_color=(100, 150, 255),
        tint_intensity=0.2,
        contrast=1.1,
        rotate=10
    )

    # All frames will have transformations applied
    processed_frames = enhanced_animation["animated_frames"]

Simple Animation Player
-----------------------

Basic Tkinter Player
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class SimpleAnimationPlayer:
        def __init__(self, root, animation_path):
            self.root = root
            self.root.title("Simple Animation Player")

            # Load animation
            self.animation_data = get_image(
                animation_path,
                framework="tkinter",
                size=(200, 200),
                animated=True
            )

            self.frames = self.animation_data["animated_frames"]
            self.delay = self.animation_data["frame_delay"]
            self.current_frame = 0
            self.playing = True

            self.setup_ui()
            self.animate()

        def setup_ui(self):
            # Animation display
            self.image_label = tk.Label(self.root)
            self.image_label.pack(pady=20)

            # Controls
            controls = tk.Frame(self.root)
            controls.pack(pady=10)

            self.play_btn = tk.Button(
                controls,
                text="Pause",
                command=self.toggle_play
            )
            self.play_btn.pack(side=tk.LEFT, padx=5)

            self.reset_btn = tk.Button(
                controls,
                text="Reset",
                command=self.reset
            )
            self.reset_btn.pack(side=tk.LEFT, padx=5)

        def animate(self):
            if self.playing and self.frames:
                # Display current frame
                self.image_label.configure(image=self.frames[self.current_frame])

                # Move to next frame
                self.current_frame = (self.current_frame + 1) % len(self.frames)

                # Schedule next frame
                self.root.after(self.delay, self.animate)

        def toggle_play(self):
            self.playing = not self.playing
            self.play_btn.configure(text="Play" if not self.playing else "Pause")
            if self.playing:
                self.animate()

        def reset(self):
            self.current_frame = 0
            if not self.playing:
                self.image_label.configure(image=self.frames[0])

    # Usage
    if __name__ == "__main__":
        root = tk.Tk()
        player = SimpleAnimationPlayer(root, "sample_animation.gif")
        root.mainloop()

Advanced Animation Player
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from gui_image_studio import get_image

    class AdvancedAnimationPlayer:
        def __init__(self, root, animation_path):
            self.root = root
            self.root.title("Advanced Animation Player")
            self.root.geometry("500x400")

            # Load animation
            self.animation_data = get_image(
                animation_path,
                framework="tkinter",
                size=(300, 300),
                animated=True
            )

            self.frames = self.animation_data["animated_frames"]
            self.original_delay = self.animation_data["frame_delay"]
            self.current_delay = self.original_delay
            self.current_frame = 0
            self.playing = False
            self.loop_count = 0

            self.setup_ui()

        def setup_ui(self):
            # Main container
            main_frame = tk.Frame(self.root)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Animation display
            self.image_label = tk.Label(main_frame)
            self.image_label.pack(pady=10)

            # Progress bar
            self.progress = ttk.Progressbar(
                main_frame,
                length=400,
                mode='determinate'
            )
            self.progress.pack(fill=tk.X, pady=5)

            # Controls frame
            controls = tk.Frame(main_frame)
            controls.pack(pady=10)

            # Playback controls
            self.play_btn = tk.Button(
                controls,
                text="Play",
                command=self.toggle_play,
                width=8
            )
            self.play_btn.grid(row=0, column=0, padx=5)

            self.stop_btn = tk.Button(
                controls,
                text="Stop",
                command=self.stop,
                width=8
            )
            self.stop_btn.grid(row=0, column=1, padx=5)

            self.prev_btn = tk.Button(
                controls,
                text="◀",
                command=self.prev_frame,
                width=4
            )
            self.prev_btn.grid(row=0, column=2, padx=5)

            self.next_btn = tk.Button(
                controls,
                text="▶",
                command=self.next_frame,
                width=4
            )
            self.next_btn.grid(row=0, column=3, padx=5)

            # Speed control
            speed_frame = tk.Frame(main_frame)
            speed_frame.pack(pady=10)

            tk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
            self.speed_var = tk.DoubleVar(value=1.0)
            speed_scale = tk.Scale(
                speed_frame,
                from_=0.1,
                to=3.0,
                resolution=0.1,
                orient=tk.HORIZONTAL,
                variable=self.speed_var,
                command=self.update_speed,
                length=200
            )
            speed_scale.pack(side=tk.LEFT, padx=10)

            # Info display
            self.info_label = tk.Label(
                main_frame,
                text="",
                font=("Arial", 10)
            )
            self.info_label.pack(pady=5)

            # Initialize display
            self.update_display()

        def animate(self):
            if self.playing and self.frames:
                self.update_display()

                # Move to next frame
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0
                    self.loop_count += 1

                # Schedule next frame
                self.root.after(self.current_delay, self.animate)

        def toggle_play(self):
            self.playing = not self.playing
            self.play_btn.configure(text="Pause" if self.playing else "Play")
            if self.playing:
                self.animate()

        def stop(self):
            self.playing = False
            self.current_frame = 0
            self.loop_count = 0
            self.play_btn.configure(text="Play")
            self.update_display()

        def prev_frame(self):
            self.current_frame = (self.current_frame - 1) % len(self.frames)
            self.update_display()

        def next_frame(self):
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.update_display()

        def update_speed(self, value=None):
            speed = self.speed_var.get()
            self.current_delay = max(10, int(self.original_delay / speed))

        def update_display(self):
            if self.frames:
                # Update image
                self.image_label.configure(image=self.frames[self.current_frame])

                # Update progress bar
                progress = (self.current_frame / len(self.frames)) * 100
                self.progress['value'] = progress

                # Update info
                info_text = (
                    f"Frame: {self.current_frame + 1}/{len(self.frames)} | "
                    f"Loop: {self.loop_count + 1} | "
                    f"Speed: {self.speed_var.get():.1f}x | "
                    f"Delay: {self.current_delay}ms"
                )
                self.info_label.configure(text=info_text)

    # Usage
    if __name__ == "__main__":
        root = tk.Tk()
        player = AdvancedAnimationPlayer(root, "complex_animation.gif")
        root.mainloop()

Creating Custom Animations
---------------------------

Static Image to Animation
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gui_image_studio import get_image
    import tkinter as tk

    def create_rotation_animation(image_path, steps=12):
        """Create rotation animation from static image."""

        frames = []
        angle_step = 360 / steps

        for i in range(steps):
            angle = i * angle_step

            frame = get_image(
                image_path,
                framework="tkinter",
                size=(150, 150),
                rotate=angle
            )

            frames.append(frame)

        return {
            "animated_frames": frames,
            "frame_delay": 100,
            "frame_count": steps
        }

    def create_fade_animation(image_path, steps=10):
        """Create fade animation from static image."""

        frames = []

        for i in range(steps):
            alpha = 1.0 - (i / (steps - 1))

            frame = get_image(
                image_path,
                framework="tkinter",
                size=(150, 150),
                transparency=alpha
            )

            frames.append(frame)

        return {
            "animated_frames": frames,
            "frame_delay": 150,
            "frame_count": steps
        }

    def create_color_pulse_animation(image_path, colors, steps_per_color=5):
        """Create color pulsing animation."""

        frames = []

        for color in colors:
            for step in range(steps_per_color + 1):
                intensity = step / steps_per_color

                frame = get_image(
                    image_path,
                    framework="tkinter",
                    size=(150, 150),
                    tint_color=color,
                    tint_intensity=intensity
                )

                frames.append(frame)

        return {
            "animated_frames": frames,
            "frame_delay": 200,
            "frame_count": len(frames)
        }

    # Usage example
    class CustomAnimationDemo:
        def __init__(self, root):
            self.root = root
            self.root.title("Custom Animation Demo")

            self.current_animation = None
            self.current_frame = 0
            self.playing = False

            self.setup_ui()

        def setup_ui(self):
            # Animation display
            self.image_label = tk.Label(self.root, text="Select an animation type")
            self.image_label.pack(pady=20)

            # Animation type buttons
            button_frame = tk.Frame(self.root)
            button_frame.pack(pady=10)

            tk.Button(
                button_frame,
                text="Rotation",
                command=self.create_rotation
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                button_frame,
                text="Fade",
                command=self.create_fade
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                button_frame,
                text="Color Pulse",
                command=self.create_color_pulse
            ).pack(side=tk.LEFT, padx=5)

            # Play controls
            control_frame = tk.Frame(self.root)
            control_frame.pack(pady=10)

            self.play_btn = tk.Button(
                control_frame,
                text="Play",
                command=self.toggle_play,
                state=tk.DISABLED
            )
            self.play_btn.pack()

        def create_rotation(self):
            self.current_animation = create_rotation_animation("sample_icon", steps=16)
            self.reset_animation()

        def create_fade(self):
            self.current_animation = create_fade_animation("sample_icon", steps=15)
            self.reset_animation()

        def create_color_pulse(self):
            colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
            self.current_animation = create_color_pulse_animation("sample_icon", colors)
            self.reset_animation()

        def reset_animation(self):
            if self.current_animation:
                self.current_frame = 0
                self.playing = False
                self.play_btn.configure(text="Play", state=tk.NORMAL)

                # Show first frame
                frames = self.current_animation["animated_frames"]
                if frames:
                    self.image_label.configure(image=frames[0], text="")

        def toggle_play(self):
            if not self.current_animation:
                return

            self.playing = not self.playing
            self.play_btn.configure(text="Pause" if self.playing else "Play")

            if self.playing:
                self.animate()

        def animate(self):
            if self.playing and self.current_animation:
                frames = self.current_animation["animated_frames"]
                delay = self.current_animation["frame_delay"]

                # Display current frame
                self.image_label.configure(image=frames[self.current_frame])

                # Move to next frame
                self.current_frame = (self.current_frame + 1) % len(frames)

                # Schedule next frame
                self.root.after(delay, self.animate)

    # Usage
    if __name__ == "__main__":
        root = tk.Tk()
        demo = CustomAnimationDemo(root)
        root.mainloop()

Animation in GUI Components
---------------------------

Animated Button
~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class AnimatedButton:
        def __init__(self, parent, animation_path, text="", command=None):
            self.parent = parent
            self.command = command

            # Load animation
            self.animation_data = get_image(
                animation_path,
                framework="tkinter",
                size=(32, 32),
                animated=True
            )

            self.frames = self.animation_data["animated_frames"]
            self.delay = self.animation_data["frame_delay"]
            self.current_frame = 0
            self.animating = False

            # Create button
            self.button = tk.Button(
                parent,
                text=text,
                image=self.frames[0] if self.frames else None,
                compound=tk.LEFT,
                command=self.on_click
            )

            # Bind hover events
            self.button.bind("<Enter>", self.start_animation)
            self.button.bind("<Leave>", self.stop_animation)

        def start_animation(self, event=None):
            if not self.animating:
                self.animating = True
                self.animate()

        def stop_animation(self, event=None):
            self.animating = False
            # Reset to first frame
            if self.frames:
                self.button.configure(image=self.frames[0])
                self.current_frame = 0

        def animate(self):
            if self.animating and self.frames:
                # Update button image
                self.button.configure(image=self.frames[self.current_frame])

                # Next frame
                self.current_frame = (self.current_frame + 1) % len(self.frames)

                # Schedule next update
                self.parent.after(self.delay, self.animate)

        def on_click(self):
            if self.command:
                self.command()

        def pack(self, **kwargs):
            self.button.pack(**kwargs)

        def grid(self, **kwargs):
            self.button.grid(**kwargs)

    # Usage
    class AnimatedButtonDemo:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Animated Button Demo")

            # Create animated buttons
            self.save_btn = AnimatedButton(
                self.root,
                "save_animation.gif",
                "Save File",
                command=self.save_file
            )
            self.save_btn.pack(pady=10)

            self.load_btn = AnimatedButton(
                self.root,
                "load_animation.gif",
                "Load File",
                command=self.load_file
            )
            self.load_btn.pack(pady=10)

        def save_file(self):
            print("Save file clicked!")

        def load_file(self):
            print("Load file clicked!")

        def run(self):
            self.root.mainloop()

Loading Indicator
~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    import threading
    import time
    from gui_image_studio import get_image

    class AnimatedLoadingIndicator:
        def __init__(self, parent):
            self.parent = parent

            # Create spinner animation
            self.animation_data = get_image(
                "spinner.gif",
                framework="tkinter",
                size=(50, 50),
                animated=True
            )

            self.frames = self.animation_data["animated_frames"]
            self.delay = self.animation_data["frame_delay"]
            self.current_frame = 0
            self.active = False

            # Create UI elements
            self.frame = tk.Frame(parent)

            self.spinner_label = tk.Label(self.frame)
            self.spinner_label.pack()

            self.status_label = tk.Label(self.frame, text="")
            self.status_label.pack()

        def show(self, message="Loading..."):
            """Show the loading indicator."""
            self.status_label.configure(text=message)
            self.frame.pack(pady=20)

            self.active = True
            self.animate()

        def hide(self):
            """Hide the loading indicator."""
            self.active = False
            self.frame.pack_forget()

        def update_message(self, message):
            """Update the loading message."""
            self.status_label.configure(text=message)

        def animate(self):
            if self.active and self.frames:
                # Update spinner
                self.spinner_label.configure(image=self.frames[self.current_frame])

                # Next frame
                self.current_frame = (self.current_frame + 1) % len(self.frames)

                # Schedule next update
                self.parent.after(self.delay, self.animate)

    # Usage example
    class LoadingDemo:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Loading Indicator Demo")
            self.root.geometry("300x200")

            # Create loading indicator
            self.loading = AnimatedLoadingIndicator(self.root)

            # Create demo button
            self.demo_btn = tk.Button(
                self.root,
                text="Start Long Operation",
                command=self.start_operation
            )
            self.demo_btn.pack(pady=20)

        def start_operation(self):
            """Simulate a long-running operation."""
            self.demo_btn.configure(state=tk.DISABLED)
            self.loading.show("Processing...")

            # Start background thread
            thread = threading.Thread(target=self.long_operation)
            thread.daemon = True
            thread.start()

        def long_operation(self):
            """Simulate long operation with progress updates."""
            steps = ["Initializing...", "Processing data...", "Finalizing..."]

            for i, step in enumerate(steps):
                self.root.after(0, self.loading.update_message, step)
                time.sleep(2)  # Simulate work

            # Complete
            self.root.after(0, self.operation_complete)

        def operation_complete(self):
            """Called when operation is complete."""
            self.loading.hide()
            self.demo_btn.configure(state=tk.NORMAL)

            # Show completion message
            result_label = tk.Label(self.root, text="Operation completed!", fg="green")
            result_label.pack()

            # Remove message after 3 seconds
            self.root.after(3000, result_label.destroy)

        def run(self):
            self.root.mainloop()

    # Usage
    if __name__ == "__main__":
        demo = LoadingDemo()
        demo.run()

Performance Optimization
------------------------

Efficient Animation Playback
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class OptimizedAnimationPlayer:
        def __init__(self, root, animation_path):
            self.root = root
            self.animation_data = get_image(
                animation_path,
                framework="tkinter",
                animated=True
            )

            self.frames = self.animation_data["animated_frames"]
            self.delay = self.animation_data["frame_delay"]

            # Performance optimizations
            self.current_frame = 0
            self.playing = False
            self.after_id = None  # Track scheduled callbacks

            # Preload optimization
            self.preload_frames()

            self.setup_ui()

        def preload_frames(self):
            """Preload all frames for smooth playback."""
            print(f"Preloading {len(self.frames)} frames...")

            # Force all frames to be rendered/cached
            for frame in self.frames:
                # Access frame properties to ensure it's loaded
                _ = frame.width()
                _ = frame.height()

            print("Preloading complete")

        def setup_ui(self):
            self.image_label = tk.Label(self.root)
            self.image_label.pack()

            # Controls
            controls = tk.Frame(self.root)
            controls.pack()

            tk.Button(controls, text="Play", command=self.play).pack(side=tk.LEFT)
            tk.Button(controls, text="Pause", command=self.pause).pack(side=tk.LEFT)
            tk.Button(controls, text="Stop", command=self.stop).pack(side=tk.LEFT)

        def play(self):
            if not self.playing:
                self.playing = True
                self.animate()

        def pause(self):
            self.playing = False
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None

        def stop(self):
            self.pause()
            self.current_frame = 0
            self.update_display()

        def animate(self):
            if self.playing:
                self.update_display()

                # Move to next frame
                self.current_frame = (self.current_frame + 1) % len(self.frames)

                # Schedule next frame with error handling
                try:
                    self.after_id = self.root.after(self.delay, self.animate)
                except tk.TclError:
                    # Widget was destroyed
                    self.playing = False

        def update_display(self):
            try:
                self.image_label.configure(image=self.frames[self.current_frame])
            except (tk.TclError, IndexError):
                # Handle errors gracefully
                self.playing = False

        def cleanup(self):
            """Clean up resources when done."""
            self.pause()
            self.frames.clear()

Memory-Efficient Animation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class MemoryEfficientPlayer:
        def __init__(self, root, animation_path, max_cached_frames=10):
            self.root = root
            self.animation_path = animation_path
            self.max_cached_frames = max_cached_frames

            # Load animation metadata only
            self.animation_data = get_image(
                animation_path,
                framework="tkinter",
                animated=True,
                size=(1, 1)  # Minimal size for metadata
            )

            self.total_frames = len(self.animation_data["animated_frames"])
            self.delay = self.animation_data["frame_delay"]

            # Frame cache
            self.frame_cache = {}
            self.cache_order = []

            self.current_frame = 0
            self.playing = False

            self.setup_ui()

        def get_frame(self, frame_index):
            """Get frame with caching."""
            if frame_index in self.frame_cache:
                # Move to end of cache order (LRU)
                self.cache_order.remove(frame_index)
                self.cache_order.append(frame_index)
                return self.frame_cache[frame_index]

            # Load frame on demand
            frame = get_image(
                self.animation_path,
                framework="tkinter",
                size=(200, 200),
                animated=True
            )["animated_frames"][frame_index]

            # Add to cache
            self.frame_cache[frame_index] = frame
            self.cache_order.append(frame_index)

            # Maintain cache size
            while len(self.frame_cache) > self.max_cached_frames:
                oldest = self.cache_order.pop(0)
                del self.frame_cache[oldest]

            return frame

        def setup_ui(self):
            self.image_label = tk.Label(self.root)
            self.image_label.pack()

            # Show cache info
            self.cache_info = tk.Label(self.root, text="")
            self.cache_info.pack()

            # Controls
            controls = tk.Frame(self.root)
            controls.pack()

            tk.Button(controls, text="Play", command=self.play).pack(side=tk.LEFT)
            tk.Button(controls, text="Pause", command=self.pause).pack(side=tk.LEFT)

        def play(self):
            self.playing = True
            self.animate()

        def pause(self):
            self.playing = False

        def animate(self):
            if self.playing:
                # Get and display current frame
                frame = self.get_frame(self.current_frame)
                self.image_label.configure(image=frame)

                # Update cache info
                cache_info = f"Cache: {len(self.frame_cache)}/{self.max_cached_frames} frames"
                self.cache_info.configure(text=cache_info)

                # Next frame
                self.current_frame = (self.current_frame + 1) % self.total_frames

                # Schedule next
                self.root.after(self.delay, self.animate)

Complete Animation Application
------------------------------

.. code-block:: python

    import tkinter as tk
    from tkinter import filedialog, messagebox
    from gui_image_studio import get_image, create_sample_images
    import os

    class AnimationStudio:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Animation Studio")
            self.root.geometry("800x600")

            self.current_animation = None
            self.current_frame = 0
            self.playing = False
            self.after_id = None

            self.setup_ui()

            # Create sample animations if none exist
            self.ensure_sample_animations()

        def setup_ui(self):
            # Menu bar
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)

            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="Open Animation", command=self.open_animation)
            file_menu.add_command(label="Create Samples", command=self.create_samples)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit)

            # Main layout
            main_frame = tk.Frame(self.root)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Animation display
            display_frame = tk.Frame(main_frame, relief=tk.SUNKEN, bd=2)
            display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))

            self.image_label = tk.Label(
                display_frame,
                text="Open an animation to begin",
                width=50,
                height=20,
                bg="white"
            )
            self.image_label.pack(expand=True)

            # Controls panel
            controls_frame = tk.Frame(main_frame)
            controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

            # Playback controls
            playback_frame = tk.Frame(controls_frame)
            playback_frame.pack(pady=5)

            self.play_btn = tk.Button(
                playback_frame,
                text="Play",
                command=self.toggle_play,
                state=tk.DISABLED,
                width=8
            )
            self.play_btn.pack(side=tk.LEFT, padx=5)

            self.stop_btn = tk.Button(
                playback_frame,
                text="Stop",
                command=self.stop,
                state=tk.DISABLED,
                width=8
            )
            self.stop_btn.pack(side=tk.LEFT, padx=5)

            # Frame navigation
            nav_frame = tk.Frame(controls_frame)
            nav_frame.pack(pady=5)

            self.prev_btn = tk.Button(
                nav_frame,
                text="◀ Prev",
                command=self.prev_frame,
                state=tk.DISABLED
            )
            self.prev_btn.pack(side=tk.LEFT, padx=5)

            self.frame_label = tk.Label(nav_frame, text="Frame: 0/0")
            self.frame_label.pack(side=tk.LEFT, padx=10)

            self.next_btn = tk.Button(
                nav_frame,
                text="Next ▶",
                command=self.next_frame,
                state=tk.DISABLED
            )
            self.next_btn.pack(side=tk.LEFT, padx=5)

            # Info panel
            info_frame = tk.Frame(controls_frame)
            info_frame.pack(pady=5)

            self.info_label = tk.Label(info_frame, text="No animation loaded")
            self.info_label.pack()

        def ensure_sample_animations(self):
            """Create sample animations if they don't exist."""
            sample_dir = "sample_animations"
            if not os.path.exists(sample_dir):
                try:
                    create_sample_images(sample_dir)
                    print(f"Created sample animations in {sample_dir}/")
                except Exception as e:
                    print(f"Could not create samples: {e}")

        def open_animation(self):
            """Open an animation file."""
            file_path = filedialog.askopenfilename(
                title="Select Animation",
                filetypes=[
                    ("GIF files", "*.gif"),
                    ("All files", "*.*")
                ]
            )

            if file_path:
                self.load_animation(file_path)

        def load_animation(self, file_path):
            """Load animation from file."""
            try:
                self.current_animation = get_image(
                    file_path,
                    framework="tkinter",
                    size=(400, 300),
                    animated=True
                )

                self.current_frame = 0
                self.playing = False

                # Enable controls
                self.play_btn.configure(state=tk.NORMAL, text="Play")
                self.stop_btn.configure(state=tk.NORMAL)
                self.prev_btn.configure(state=tk.NORMAL)
                self.next_btn.configure(state=tk.NORMAL)

                # Update display
                self.update_display()
                self.update_info()

                print(f"Loaded animation: {os.path.basename(file_path)}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load animation:\n{str(e)}")

        def create_samples(self):
            """Create sample animations."""
            try:
                create_sample_images("sample_animations")
                messagebox.showinfo("Success", "Sample animations created in 'sample_animations' folder")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create samples:\n{str(e)}")

        def toggle_play(self):
            """Toggle animation playback."""
            if not self.current_animation:
                return

            self.playing = not self.playing
            self.play_btn.configure(text="Pause" if self.playing else "Play")

            if self.playing:
                self.animate()
            elif self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None

        def stop(self):
            """Stop animation and reset to first frame."""
            self.playing = False
            self.current_frame = 0
            self.play_btn.configure(text="Play")

            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None

            self.update_display()

        def prev_frame(self):
            """Go to previous frame."""
            if self.current_animation:
                frames = self.current_animation["animated_frames"]
                self.current_frame = (self.current_frame - 1) % len(frames)
                self.update_display()

        def next_frame(self):
            """Go to next frame."""
            if self.current_animation:
                frames = self.current_animation["animated_frames"]
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.update_display()

        def animate(self):
            """Animation loop."""
            if self.playing and self.current_animation:
                frames = self.current_animation["animated_frames"]
                delay = self.current_animation["frame_delay"]

                self.update_display()

                # Move to next frame
                self.current_frame = (self.current_frame + 1) % len(frames)

                # Schedule next frame
                self.after_id = self.root.after(delay, self.animate)

        def update_display(self):
            """Update the image display."""
            if self.current_animation:
                frames = self.current_animation["animated_frames"]
                if frames:
                    self.image_label.configure(
                        image=frames[self.current_frame],
                        text=""
                    )

                    # Update frame counter
                    self.frame_label.configure(
                        text=f"Frame: {self.current_frame + 1}/{len(frames)}"
                    )

        def update_info(self):
            """Update animation info display."""
            if self.current_animation:
                frames = self.current_animation["animated_frames"]
                delay = self.current_animation["frame_delay"]
                total_time = len(frames) * delay / 1000.0

                info_text = (
                    f"Frames: {len(frames)} | "
                    f"Delay: {delay}ms | "
                    f"Duration: {total_time:.1f}s"
                )

                self.info_label.configure(text=info_text)

        def run(self):
            """Start the application."""
            self.root.mainloop()

    # Usage
    if __name__ == "__main__":
        app = AnimationStudio()
        app.run()

This comprehensive animation creation guide demonstrates various techniques for working with animations in GUI Image Studio, from basic playback to advanced custom animation creation and optimization techniques.
