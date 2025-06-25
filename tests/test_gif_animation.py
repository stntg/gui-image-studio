#!/usr/bin/env python3
"""
Simple test script for GIF animation functionality
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import tkinter as tk

import gui_image_studio


def test_gif_animation():
    """Test basic GIF animation loading."""
    print("Testing GIF animation functionality...")

    # Skip GUI-dependent tests in CI environment
    if os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true":
        print("⚠ Skipping GIF animation test in CI environment (no GUI available)")
        print("✓ GIF animation test skipped")
        return True

    # Create a root window (required for Tkinter PhotoImage)
    root = tk.Tk()
    root.title("GIF Animation Test")
    root.geometry("300x200")

    # Don't show the window in headless mode
    root.withdraw()

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
            # Create a label to display the animation (but don't show it)
            label = tk.Label(root, text="Animation will appear here")
            label.pack(pady=20)

            # Test that we can create the animation components
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

            def stop_animation():
                if animation_job[0] is not None:
                    if animation_job[0] != True:
                        root.after_cancel(animation_job[0])
                    animation_job[0] = None

            # Test animation controls
            start_animation()
            root.update()  # Process one update cycle
            stop_animation()

            print("✓ Animation test components created successfully!")

            # Clean up
            root.destroy()
            return True
        else:
            print("✗ No animation frames found")
            root.destroy()
            return False

    except Exception as e:
        print(f"✗ Error testing animation: {e}")
        root.destroy()
        return False


if __name__ == "__main__":
    success = test_gif_animation()
    if success:
        print("GIF animation test completed successfully!")
    else:
        print("GIF animation test failed!")
        sys.exit(1)
