Animation Tools
===============

GUI Image Studio provides comprehensive support for working with animated images, particularly animated GIFs. This guide covers loading, processing, displaying, and creating animations.

Overview of Animation Support
-----------------------------

GUI Image Studio's animation capabilities include:

- **Loading animated GIFs** with frame extraction
- **Frame-by-frame processing** with transformations
- **Playback control** with customizable timing
- **Animation display** in GUI applications
- **Performance optimization** for smooth playback
- **Integration** with both tkinter and customtkinter

Loading Animated Images
-----------------------

Basic Animation Loading
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gui_image_studio import get_image

    # Load animated GIF
    animation_data = get_image(
        "animated.gif",
        framework="tkinter",
        size=(200, 200),
        animated=True,
        frame_delay=100
    )

    # Extract animation components
    frames = animation_data["animated_frames"]
    delay = animation_data["frame_delay"]
    frame_count = len(frames)

    print(f"Loaded {frame_count} frames with {delay}ms delay")

Animation Data Structure
~~~~~~~~~~~~~~~~~~~~~~~~

When ``animated=True``, ``get_image()`` returns a dictionary:

.. code-block:: python

    animation_data = {
        "animated_frames": [frame1, frame2, frame3, ...],  # List of frame images
        "frame_delay": 100,  # Delay between frames in milliseconds
        "loop_count": 0,     # Number of loops (0 = infinite)
        "frame_count": 10    # Total number of frames
    }

**Accessing Animation Properties:**

.. code-block:: python

    # Get individual frames
    first_frame = animation_data["animated_frames"][0]
    last_frame = animation_data["animated_frames"][-1]

    # Get timing information
    delay_ms = animation_data["frame_delay"]
    delay_seconds = delay_ms / 1000.0

    # Calculate total duration
    total_duration = len(animation_data["animated_frames"]) * delay_ms
    print(f"Animation duration: {total_duration/1000:.1f} seconds")

Animation with Transformations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apply transformations to all frames simultaneously:

.. code-block:: python

    # Apply effects to entire animation
    processed_animation = get_image(
        "animated.gif",
        framework="customtkinter",
        size=(150, 150),
        animated=True,
        frame_delay=80,
        tint_color=(255, 100, 100),
        tint_intensity=0.3,
        contrast=1.2,
        saturation=1.1,
        rotate=15
    )

    # All frames will have the same transformations applied
    enhanced_frames = processed_animation["animated_frames"]

Animation Playback
------------------

Basic Animation Player
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class AnimationPlayer:
        def __init__(self, root, animation_path):
            self.root = root
            self.root.title("Animation Player")

            # Load animation
            self.animation_data = get_image(
                animation_path,
                framework="tkinter",
                size=(300, 300),
                animated=True
            )

            self.frames = self.animation_data["animated_frames"]
            self.delay = self.animation_data["frame_delay"]
            self.current_frame = 0
            self.playing = True
            self.loop_count = 0

            self.setup_ui()
            self.play_animation()

        def setup_ui(self):
            # Animation display
            self.image_label = tk.Label(self.root)
            self.image_label.pack(pady=20)

            # Controls
            controls = tk.Frame(self.root)
            controls.pack(pady=10)

            self.play_btn = tk.Button(controls, text="Pause", command=self.toggle_play)
            self.play_btn.pack(side=tk.LEFT, padx=5)

            self.reset_btn = tk.Button(controls, text="Reset", command=self.reset)
            self.reset_btn.pack(side=tk.LEFT, padx=5)

            # Frame info
            self.info_label = tk.Label(self.root, text="")
            self.info_label.pack()

        def play_animation(self):
            if self.playing and self.frames:
                # Display current frame
                self.image_label.configure(image=self.frames[self.current_frame])

                # Update info
                self.info_label.configure(
                    text=f"Frame {self.current_frame + 1}/{len(self.frames)} | Loop {self.loop_count + 1}"
                )

                # Move to next frame
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0
                    self.loop_count += 1

                # Schedule next frame
                self.root.after(self.delay, self.play_animation)

        def toggle_play(self):
            self.playing = not self.playing
            self.play_btn.configure(text="Play" if not self.playing else "Pause")
            if self.playing:
                self.play_animation()

        def reset(self):
            self.current_frame = 0
            self.loop_count = 0
            if not self.playing:
                self.image_label.configure(image=self.frames[0])
                self.info_label.configure(text="Frame 1/10 | Loop 1")

    # Usage
    if __name__ == "__main__":
        root = tk.Tk()
        player = AnimationPlayer(root, "sample_animation.gif")
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

            # Load animation
            self.animation_data = get_image(
                animation_path,
                framework="tkinter",
                size=(400, 400),
                animated=True
            )

            self.frames = self.animation_data["animated_frames"]
            self.original_delay = self.animation_data["frame_delay"]
            self.current_delay = self.original_delay
            self.current_frame = 0
            self.playing = False
            self.loop_count = 0
            self.max_loops = 0  # 0 = infinite

            self.setup_ui()

        def setup_ui(self):
            # Main frame
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
            self.play_btn = tk.Button(controls, text="Play", command=self.toggle_play)
            self.play_btn.grid(row=0, column=0, padx=5)

            self.stop_btn = tk.Button(controls, text="Stop", command=self.stop)
            self.stop_btn.grid(row=0, column=1, padx=5)

            self.prev_btn = tk.Button(controls, text="◀", command=self.prev_frame)
            self.prev_btn.grid(row=0, column=2, padx=5)

            self.next_btn = tk.Button(controls, text="▶", command=self.next_frame)
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
                command=self.update_speed
            )
            speed_scale.pack(side=tk.LEFT, padx=10)

            # Loop control
            loop_frame = tk.Frame(main_frame)
            loop_frame.pack(pady=5)

            tk.Label(loop_frame, text="Max Loops (0=infinite):").pack(side=tk.LEFT)
            self.loop_var = tk.IntVar(value=0)
            loop_spin = tk.Spinbox(
                loop_frame,
                from_=0,
                to=100,
                textvariable=self.loop_var,
                width=5
            )
            loop_spin.pack(side=tk.LEFT, padx=10)

            # Info display
            self.info_label = tk.Label(main_frame, text="", font=("Arial", 10))
            self.info_label.pack(pady=5)

            # Initialize display
            self.update_display()

        def play_animation(self):
            if self.playing and self.frames:
                # Check loop limit
                if self.loop_var.get() > 0 and self.loop_count >= self.loop_var.get():
                    self.stop()
                    return

                # Display current frame
                self.update_display()

                # Move to next frame
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0
                    self.loop_count += 1

                # Schedule next frame
                self.root.after(self.current_delay, self.play_animation)

        def toggle_play(self):
            self.playing = not self.playing
            self.play_btn.configure(text="Pause" if self.playing else "Play")
            if self.playing:
                self.play_animation()

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
            self.current_delay = int(self.original_delay / speed)

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
        player = AdvancedAnimationPlayer(root, "animated.gif")
        root.mainloop()

CustomTkinter Animation Integration
-----------------------------------

Modern Animation Display
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import customtkinter as ctk
    from gui_image_studio import get_image

    class ModernAnimationViewer:
        def __init__(self):
            # Set appearance
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")

            self.root = ctk.CTk()
            self.root.title("Modern Animation Viewer")
            self.root.geometry("600x500")

            self.animation_data = None
            self.frames = []
            self.current_frame = 0
            self.playing = False
            self.delay = 100

            self.setup_ui()

        def setup_ui(self):
            # Main container
            main_frame = ctk.CTkFrame(self.root)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Title
            title = ctk.CTkLabel(
                main_frame,
                text="Animation Viewer",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title.pack(pady=20)

            # Animation display area
            self.image_frame = ctk.CTkFrame(main_frame)
            self.image_frame.pack(pady=20)

            self.image_label = ctk.CTkLabel(
                self.image_frame,
                text="Load an animation to begin",
                width=400,
                height=300
            )
            self.image_label.pack(padx=20, pady=20)

            # Controls
            controls_frame = ctk.CTkFrame(main_frame)
            controls_frame.pack(fill="x", pady=10)

            # Load button
            self.load_btn = ctk.CTkButton(
                controls_frame,
                text="Load Animation",
                command=self.load_animation
            )
            self.load_btn.pack(side="left", padx=10, pady=10)

            # Play/Pause button
            self.play_btn = ctk.CTkButton(
                controls_frame,
                text="Play",
                command=self.toggle_play,
                state="disabled"
            )
            self.play_btn.pack(side="left", padx=10, pady=10)

            # Speed slider
            speed_frame = ctk.CTkFrame(controls_frame)
            speed_frame.pack(side="right", padx=10, pady=10)

            ctk.CTkLabel(speed_frame, text="Speed:").pack(side="left", padx=5)
            self.speed_slider = ctk.CTkSlider(
                speed_frame,
                from_=0.1,
                to=3.0,
                number_of_steps=29,
                command=self.update_speed
            )
            self.speed_slider.set(1.0)
            self.speed_slider.pack(side="left", padx=10)

            # Info display
            self.info_label = ctk.CTkLabel(main_frame, text="")
            self.info_label.pack(pady=10)

        def load_animation(self):
            # In a real app, you'd use a file dialog
            # For demo, we'll load a sample
            try:
                self.animation_data = get_image(
                    "sample_animation.gif",  # Replace with actual file
                    framework="customtkinter",
                    size=(350, 250),
                    animated=True,
                    theme="dark"
                )

                self.frames = self.animation_data["animated_frames"]
                self.delay = self.animation_data["frame_delay"]
                self.current_frame = 0

                # Enable controls
                self.play_btn.configure(state="normal")

                # Show first frame
                self.update_display()

            except Exception as e:
                # Show error (in real app, use proper error dialog)
                self.info_label.configure(text=f"Error loading animation: {e}")

        def toggle_play(self):
            if not self.frames:
                return

            self.playing = not self.playing
            self.play_btn.configure(text="Pause" if self.playing else "Play")

            if self.playing:
                self.animate()

        def animate(self):
            if self.playing and self.frames:
                self.update_display()

                # Next frame
                self.current_frame = (self.current_frame + 1) % len(self.frames)

                # Schedule next update
                self.root.after(self.delay, self.animate)

        def update_speed(self, value):
            original_delay = self.animation_data["frame_delay"] if self.animation_data else 100
            self.delay = int(original_delay / value)

        def update_display(self):
            if self.frames:
                self.image_label.configure(
                    image=self.frames[self.current_frame],
                    text=""
                )

                self.info_label.configure(
                    text=f"Frame {self.current_frame + 1}/{len(self.frames)}"
                )

        def run(self):
            self.root.mainloop()

    # Usage
    if __name__ == "__main__":
        app = ModernAnimationViewer()
        app.run()

Animation Processing Techniques
-------------------------------

Frame-by-Frame Processing
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gui_image_studio import get_image

    def process_animation_frames(animation_path, frame_processor):
        """
        Process each frame of an animation with a custom function.

        Args:
            animation_path: Path to animated GIF
            frame_processor: Function that takes and returns a frame
        """

        # Load original animation
        original = get_image(
            animation_path,
            framework="tkinter",
            animated=True
        )

        original_frames = original["animated_frames"]
        processed_frames = []

        # Process each frame
        for i, frame in enumerate(original_frames):
            print(f"Processing frame {i + 1}/{len(original_frames)}")

            # Apply custom processing
            processed_frame = frame_processor(frame, i)
            processed_frames.append(processed_frame)

        # Return new animation data
        return {
            "animated_frames": processed_frames,
            "frame_delay": original["frame_delay"],
            "frame_count": len(processed_frames)
        }

    # Example frame processors
    def fade_processor(frame, frame_index):
        """Gradually fade frames."""
        total_frames = 10  # Assume we know total
        alpha = 1.0 - (frame_index / total_frames) * 0.5

        # Note: This is conceptual - actual implementation would modify the frame
        return frame

    def color_cycle_processor(frame, frame_index):
        """Cycle through colors."""
        colors = [
            (255, 100, 100),  # Red
            (100, 255, 100),  # Green
            (100, 100, 255),  # Blue
        ]

        color = colors[frame_index % len(colors)]

        # Apply tint to frame (conceptual)
        return frame

Animation Effects
~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_fade_animation(image_path, frame_count=10):
        """Create a fade-out animation from a static image."""

        frames = []

        for i in range(frame_count):
            alpha = 1.0 - (i / (frame_count - 1))

            frame = get_image(
                image_path,
                framework="tkinter",
                size=(200, 200),
                transparency=alpha
            )

            frames.append(frame)

        return {
            "animated_frames": frames,
            "frame_delay": 100,
            "frame_count": frame_count
        }

    def create_rotation_animation(image_path, steps=12):
        """Create a rotation animation from a static image."""

        frames = []
        angle_step = 360 / steps

        for i in range(steps):
            angle = i * angle_step

            frame = get_image(
                image_path,
                framework="tkinter",
                size=(200, 200),
                rotate=angle
            )

            frames.append(frame)

        return {
            "animated_frames": frames,
            "frame_delay": 100,
            "frame_count": steps
        }

    def create_color_pulse_animation(image_path, colors, steps_per_color=5):
        """Create a color pulsing animation."""

        frames = []

        for color in colors:
            for intensity in [i / steps_per_color for i in range(steps_per_color + 1)]:
                frame = get_image(
                    image_path,
                    framework="tkinter",
                    size=(200, 200),
                    tint_color=color,
                    tint_intensity=intensity
                )

                frames.append(frame)

        return {
            "animated_frames": frames,
            "frame_delay": 150,
            "frame_count": len(frames)
        }

Performance Optimization
------------------------

Efficient Animation Playback
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class OptimizedAnimationPlayer:
        def __init__(self, root, animation_data):
            self.root = root
            self.animation_data = animation_data
            self.frames = animation_data["animated_frames"]
            self.delay = animation_data["frame_delay"]

            # Performance optimizations
            self.current_frame = 0
            self.playing = False
            self.after_id = None  # Track scheduled callbacks
            self.preload_frames = True

            # Preload optimization
            if self.preload_frames:
                self.preload_all_frames()

            self.setup_ui()

        def preload_all_frames(self):
            """Preload all frames to improve playback performance."""
            print(f"Preloading {len(self.frames)} frames...")

            # Force all frames to be rendered/cached
            for i, frame in enumerate(self.frames):
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

Memory Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

    class MemoryEfficientPlayer:
        def __init__(self, root, animation_path, max_cached_frames=20):
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

            # Load frame
            frame = get_image(
                self.animation_path,
                framework="tkinter",
                size=(300, 300),
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

Animation Utilities
-------------------

Animation Analysis
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def analyze_animation(animation_path):
        """Analyze an animated GIF and return detailed information."""

        animation_data = get_image(
            animation_path,
            framework="tkinter",
            animated=True
        )

        frames = animation_data["animated_frames"]
        delay = animation_data["frame_delay"]

        analysis = {
            'file_path': animation_path,
            'frame_count': len(frames),
            'frame_delay_ms': delay,
            'total_duration_ms': len(frames) * delay,
            'total_duration_seconds': (len(frames) * delay) / 1000.0,
            'fps': 1000.0 / delay if delay > 0 else 0,
            'frames_per_second': round(1000.0 / delay, 2) if delay > 0 else 0
        }

        # Analyze individual frames
        if frames:
            first_frame = frames[0]
            analysis.update({
                'frame_width': first_frame.width(),
                'frame_height': first_frame.height(),
                'dimensions': f"{first_frame.width()}x{first_frame.height()}"
            })

        return analysis

    def print_animation_info(animation_path):
        """Print detailed animation information."""

        info = analyze_animation(animation_path)

        print(f"Animation Analysis: {info['file_path']}")
        print(f"  Dimensions: {info['dimensions']}")
        print(f"  Frame Count: {info['frame_count']}")
        print(f"  Frame Delay: {info['frame_delay_ms']}ms")
        print(f"  Frame Rate: {info['frames_per_second']} FPS")
        print(f"  Total Duration: {info['total_duration_seconds']:.1f} seconds")

Animation Conversion
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def convert_animation_speed(animation_path, speed_multiplier):
        """Convert animation to different speed."""

        original = get_image(
            animation_path,
            framework="tkinter",
            animated=True
        )

        new_delay = int(original["frame_delay"] / speed_multiplier)
        new_delay = max(10, new_delay)  # Minimum 10ms delay

        return {
            "animated_frames": original["animated_frames"],
            "frame_delay": new_delay,
            "frame_count": len(original["animated_frames"])
        }

    def reverse_animation(animation_path):
        """Reverse the frame order of an animation."""

        original = get_image(
            animation_path,
            framework="tkinter",
            animated=True
        )

        reversed_frames = list(reversed(original["animated_frames"]))

        return {
            "animated_frames": reversed_frames,
            "frame_delay": original["frame_delay"],
            "frame_count": len(reversed_frames)
        }

    def loop_animation(animation_path, loop_count):
        """Create a looped version of an animation."""

        original = get_image(
            animation_path,
            framework="tkinter",
            animated=True
        )

        looped_frames = original["animated_frames"] * loop_count

        return {
            "animated_frames": looped_frames,
            "frame_delay": original["frame_delay"],
            "frame_count": len(looped_frames)
        }

Integration Examples
--------------------

Animation in GUI Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class AnimatedIconButton:
        """A button with an animated icon."""

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

    # Usage example
    class AnimatedButtonDemo:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Animated Button Demo")

            # Create animated buttons
            self.save_btn = AnimatedIconButton(
                self.root,
                "save_animation.gif",
                "Save File",
                command=self.save_file
            )
            self.save_btn.pack(pady=10)

            self.load_btn = AnimatedIconButton(
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

Loading Indicators
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class AnimatedLoadingIndicator:
        """An animated loading spinner."""

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

            # Create label for spinner
            self.label = tk.Label(parent)

            # Status text
            self.status_label = tk.Label(parent, text="")

        def show(self, message="Loading..."):
            """Show the loading indicator."""
            self.status_label.configure(text=message)
            self.label.pack()
            self.status_label.pack()

            self.active = True
            self.animate()

        def hide(self):
            """Hide the loading indicator."""
            self.active = False
            self.label.pack_forget()
            self.status_label.pack_forget()

        def animate(self):
            if self.active and self.frames:
                # Update spinner
                self.label.configure(image=self.frames[self.current_frame])

                # Next frame
                self.current_frame = (self.current_frame + 1) % len(self.frames)

                # Schedule next update
                self.parent.after(self.delay, self.animate)

        def update_message(self, message):
            """Update the loading message."""
            self.status_label.configure(text=message)

Best Practices
--------------

Performance Guidelines
~~~~~~~~~~~~~~~~~~~~~~

1. **Optimize Frame Sizes**: Don't load animations larger than needed
2. **Cache Wisely**: Use frame caching for frequently accessed animations
3. **Limit Concurrent Animations**: Too many animations can impact performance
4. **Use Appropriate Frame Rates**: Higher frame rates aren't always better

.. code-block:: python

    # Good: Appropriate size for use case
    icon_animation = get_image(
        "icon.gif",
        framework="tkinter",
        size=(32, 32),
        animated=True
    )

    # Avoid: Loading huge animations for small displays
    # huge_animation = get_image("animation.gif", size=(2000, 2000), animated=True)

Memory Management
~~~~~~~~~~~~~~~~~

1. **Clean Up Resources**: Stop animations when widgets are destroyed
2. **Use Frame Limits**: Don't cache unlimited frames
3. **Monitor Memory Usage**: Be aware of memory consumption with large animations

.. code-block:: python

    class ResponsibleAnimationPlayer:
        def __init__(self, root, animation_path):
            self.root = root
            self.animation_data = get_image(animation_path, animated=True)
            self.playing = False

            # Bind cleanup to window close
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        def on_closing(self):
            # Stop animation and clean up
            self.playing = False
            self.animation_data = None
            self.root.destroy()

User Experience
~~~~~~~~~~~~~~~

1. **Provide Controls**: Let users pause/play animations
2. **Respect Accessibility**: Consider users with motion sensitivity
3. **Smooth Playback**: Ensure consistent frame timing
4. **Graceful Degradation**: Handle missing or corrupted animations

Next Steps
----------

Now that you understand animation tools:

1. **Learn Batch Operations**: :doc:`batch_operations`
2. **Explore Theme System**: :doc:`theme_system`
3. **Try Advanced Examples**: :doc:`../examples/index`
4. **Build Custom Applications**: :doc:`gui_development`
