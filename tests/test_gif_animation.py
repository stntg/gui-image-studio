#!/usr/bin/env python3
"""
Simple test script for GIF animation functionality
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import tkinter as tk
import gui_image_studio


def test_gif_animation():
    """Test basic GIF animation loading."""
    print("Testing GIF animation functionality...")

    # Create a root window (required for Tkinter PhotoImage)
    root = tk.Tk()
    root.title("GIF Animation Test")
    root.geometry("300x200")

    try:
        # Test loading animated GIF
        print("Loading animation.gif...")
        anim = gui_image_studio.get_image(
            "animation.gif", framework="tkinter", animated=True, size=(64, 64)
        )

        frames = anim.get("animated_frames", [])
        delay = anim.get("frame_delay", 100)

        print(f"✓ Successfully loaded {len(frames)} frames with {delay}ms delay")

        if frames:
            # Create a label to display the animation
            label = tk.Label(root, text="Animation will appear here")
            label.pack(pady=20)

            # Animation control
            current_frame = [0]
            animation_job = [None]

            def animate():
                if animation_job[0] is not None:
                    label.configure(image=frames[current_frame[0]])
                    current_frame[0] = (current_frame[0] + 1) % len(frames)
                    animation_job[0] = root.after(delay, animate)

            def start_animation():
                if animation_job[0] is None:
                    animation_job[0] = True
                    animate()
                    start_btn.configure(text="Stop", command=stop_animation)

            def stop_animation():
                if animation_job[0] is not None:
                    if animation_job[0] != True:
                        root.after_cancel(animation_job[0])
                    animation_job[0] = None
                    start_btn.configure(text="Start", command=start_animation)

            # Control button
            start_btn = tk.Button(root, text="Start Animation", command=start_animation)
            start_btn.pack(pady=10)

            # Status label
            status_label = tk.Label(root, text=f"Ready - {len(frames)} frames loaded")
            status_label.pack()

            print("✓ Animation test window created successfully!")
            print("Click 'Start Animation' to test the animation.")

            # Start the GUI
            root.mainloop()
        else:
            print("✗ No animation frames found")
            root.destroy()

    except Exception as e:
        print(f"✗ Error testing animation: {e}")
        root.destroy()
        return False

    return True


if __name__ == "__main__":
    success = test_gif_animation()
    if success:
        print("GIF animation test completed successfully!")
    else:
        print("GIF animation test failed!")
        sys.exit(1)
