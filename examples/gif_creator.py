#!/usr/bin/env python3
"""
GIF Creator - gui_image_studio
==============================

Utility to create custom animated GIFs for testing gui_image_studio functionality.
Creates various types of animations with different patterns and effects.
"""

import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_loading_spinner(filepath, size=(64, 64), frames=12, colors=None):
    """Create a loading spinner animation."""
    if colors is None:
        colors = [(100, 150, 255), (150, 200, 255), (200, 220, 255)]

    images = []
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 3

    for frame in range(frames):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw spinning dots
        for i in range(8):
            angle = (frame * 30 + i * 45) * math.pi / 180
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)

            # Fade effect based on position
            alpha = int(255 * (1 - i / 8))
            color = colors[i % len(colors)] + (alpha,)

            dot_size = 6
            draw.ellipse(
                [x - dot_size, y - dot_size, x + dot_size, y + dot_size], fill=color
            )

        images.append(img)

    # Save as animated GIF
    images[0].save(
        filepath,
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
        disposal=2,
    )
    print(f"Created loading spinner: {filepath}")


def create_pulse_animation(filepath, size=(64, 64), frames=20, color=(255, 100, 100)):
    """Create a pulsing circle animation."""
    images = []
    center = (size[0] // 2, size[1] // 2)
    max_radius = min(size) // 3

    for frame in range(frames):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Pulsing effect
        pulse = math.sin(frame * 2 * math.pi / frames)
        radius = max_radius * (0.5 + 0.5 * pulse)
        alpha = int(255 * (0.3 + 0.7 * abs(pulse)))

        fill_color = color + (alpha,)
        outline_color = color + (min(255, alpha + 50),)

        draw.ellipse(
            [
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ],
            fill=fill_color,
            outline=outline_color,
            width=2,
        )

        images.append(img)

    images[0].save(
        filepath,
        save_all=True,
        append_images=images[1:],
        duration=80,
        loop=0,
        disposal=2,
    )
    print(f"Created pulse animation: {filepath}")


def create_wave_animation(filepath, size=(128, 64), frames=30, colors=None):
    """Create a wave animation."""
    if colors is None:
        colors = [(0, 150, 255), (100, 200, 255), (200, 230, 255)]

    images = []

    for frame in range(frames):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw wave
        points = []
        for x in range(size[0]):
            # Multiple wave components
            y1 = math.sin((x + frame * 4) * 2 * math.pi / 40) * 10
            y2 = math.sin((x + frame * 2) * 2 * math.pi / 60) * 5
            y = size[1] // 2 + y1 + y2
            points.append((x, y))

        # Draw wave lines
        for i, color in enumerate(colors):
            offset = i * 3
            wave_points = [(x, y + offset) for x, y in points]

            if len(wave_points) > 1:
                for j in range(len(wave_points) - 1):
                    draw.line(
                        [wave_points[j], wave_points[j + 1]],
                        fill=color + (200,),
                        width=2,
                    )

        images.append(img)

    images[0].save(
        filepath,
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
        disposal=2,
    )
    print(f"Created wave animation: {filepath}")


def create_rotating_square(filepath, size=(64, 64), frames=24, color=(100, 255, 100)):
    """Create a rotating square animation."""
    images = []
    center = (size[0] // 2, size[1] // 2)
    square_size = min(size) // 3

    for frame in range(frames):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Rotation angle
        angle = frame * 360 / frames

        # Calculate rotated square corners
        corners = []
        for dx, dy in [
            (-square_size, -square_size),
            (square_size, -square_size),
            (square_size, square_size),
            (-square_size, square_size),
        ]:
            # Rotate point
            rad = math.radians(angle)
            x = center[0] + dx * math.cos(rad) - dy * math.sin(rad)
            y = center[1] + dx * math.sin(rad) + dy * math.cos(rad)
            corners.append((x, y))

        # Draw square
        draw.polygon(corners, fill=color + (200,), outline=color + (255,))

        # Add center dot
        dot_size = 3
        draw.ellipse(
            [
                center[0] - dot_size,
                center[1] - dot_size,
                center[0] + dot_size,
                center[1] + dot_size,
            ],
            fill=(255, 255, 255, 255),
        )

        images.append(img)

    images[0].save(
        filepath,
        save_all=True,
        append_images=images[1:],
        duration=80,
        loop=0,
        disposal=2,
    )
    print(f"Created rotating square: {filepath}")


def create_progress_bar(filepath, size=(128, 32), frames=20, color=(0, 200, 0)):
    """Create a progress bar animation."""
    images = []

    for frame in range(frames):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Progress bar background
        bg_color = (50, 50, 50, 200)
        draw.rounded_rectangle(
            [2, 2, size[0] - 2, size[1] - 2],
            radius=5,
            fill=bg_color,
            outline=(100, 100, 100, 255),
        )

        # Progress fill
        progress = frame / (frames - 1)
        fill_width = int((size[0] - 8) * progress)

        if fill_width > 0:
            draw.rounded_rectangle(
                [4, 4, 4 + fill_width, size[1] - 4], radius=3, fill=color + (255,)
            )

        # Add shine effect
        if fill_width > 10:
            shine_x = 4 + fill_width - 10
            draw.rounded_rectangle(
                [shine_x, 6, shine_x + 8, size[1] - 6],
                radius=2,
                fill=(255, 255, 255, 100),
            )

        images.append(img)

    images[0].save(
        filepath,
        save_all=True,
        append_images=images[1:],
        duration=150,
        loop=0,
        disposal=2,
    )
    print(f"Created progress bar: {filepath}")


def create_bouncing_ball(filepath, size=(64, 64), frames=30, color=(255, 150, 0)):
    """Create a bouncing ball animation."""
    images = []
    ball_radius = 8

    for frame in range(frames):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Ball position (bouncing vertically)
        t = frame / frames
        # Parabolic motion
        y = (
            size[1]
            - ball_radius
            - 5
            - abs(math.sin(t * 2 * math.pi)) * (size[1] - 2 * ball_radius - 10)
        )
        x = size[0] // 2

        # Ball shadow
        shadow_y = size[1] - 5
        shadow_alpha = int(100 * (1 - abs(y - shadow_y) / (size[1] - ball_radius)))
        if shadow_alpha > 0:
            draw.ellipse(
                [x - ball_radius, shadow_y - 2, x + ball_radius, shadow_y + 2],
                fill=(0, 0, 0, shadow_alpha),
            )

        # Ball
        draw.ellipse(
            [x - ball_radius, y - ball_radius, x + ball_radius, y + ball_radius],
            fill=color + (255,),
            outline=(200, 100, 0, 255),
            width=1,
        )

        # Ball highlight
        highlight_size = 3
        draw.ellipse(
            [
                x - highlight_size,
                y - ball_radius + 2,
                x + highlight_size,
                y - ball_radius + 2 + highlight_size * 2,
            ],
            fill=(255, 255, 255, 150),
        )

        images.append(img)

    images[0].save(
        filepath,
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
        disposal=2,
    )
    print(f"Created bouncing ball: {filepath}")


def create_color_cycle(filepath, size=(64, 64), frames=36):
    """Create a color cycling animation."""
    images = []
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 3

    for frame in range(frames):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # HSV color cycling
        hue = (frame * 360 / frames) % 360

        # Convert HSV to RGB
        import colorsys

        r, g, b = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))

        # Draw gradient circle
        for i in range(radius):
            alpha = int(255 * (1 - i / radius))
            circle_color = color + (alpha,)

            draw.ellipse(
                [
                    center[0] - radius + i,
                    center[1] - radius + i,
                    center[0] + radius - i,
                    center[1] + radius - i,
                ],
                outline=circle_color,
            )

        images.append(img)

    images[0].save(
        filepath,
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0,
        disposal=2,
    )
    print(f"Created color cycle: {filepath}")


def create_text_animation(filepath, text="LOADING", size=(128, 64), frames=20):
    """Create animated text."""
    images = []

    for frame in range(frames):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Animate each letter
        for i, char in enumerate(text):
            # Wave effect for each character
            offset_y = math.sin((frame + i * 3) * 2 * math.pi / frames) * 5
            x = 10 + i * 15
            y = size[1] // 2 + offset_y

            # Color cycling
            hue = ((frame + i * 5) * 360 / frames) % 360
            import colorsys

            r, g, b = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
            color = (int(r * 255), int(g * 255), int(b * 255), 255)

            # Draw character
            try:
                draw.text((x, y), char, fill=color)
            except (OSError, IOError, AttributeError):
                # Fallback if font issues
                draw.rectangle([x, y, x + 10, y + 15], fill=color)

        images.append(img)

    images[0].save(
        filepath,
        save_all=True,
        append_images=images[1:],
        duration=120,
        loop=0,
        disposal=2,
    )
    print(f"Created text animation: {filepath}")


def create_all_sample_gifs():
    """Create all sample GIF animations."""
    # Create output directory
    output_dir = "sample_gifs"
    os.makedirs(output_dir, exist_ok=True)

    print("Creating sample GIF animations...")

    # Create various animations
    create_loading_spinner(os.path.join(output_dir, "spinner.gif"))
    create_pulse_animation(os.path.join(output_dir, "pulse.gif"))
    create_wave_animation(os.path.join(output_dir, "wave.gif"))
    create_rotating_square(os.path.join(output_dir, "rotating_square.gif"))
    create_progress_bar(os.path.join(output_dir, "progress.gif"))
    create_bouncing_ball(os.path.join(output_dir, "bouncing_ball.gif"))
    create_color_cycle(os.path.join(output_dir, "color_cycle.gif"))
    create_text_animation(os.path.join(output_dir, "text_loading.gif"))

    # Create themed variations
    create_loading_spinner(
        os.path.join(output_dir, "spinner_dark.gif"),
        colors=[(150, 150, 150), (200, 200, 200), (255, 255, 255)],
    )
    create_pulse_animation(
        os.path.join(output_dir, "pulse_green.gif"), color=(100, 255, 100)
    )
    create_pulse_animation(
        os.path.join(output_dir, "pulse_blue.gif"), color=(100, 150, 255)
    )

    # Create different sizes
    create_loading_spinner(os.path.join(output_dir, "spinner_small.gif"), size=(32, 32))
    create_loading_spinner(os.path.join(output_dir, "spinner_large.gif"), size=(96, 96))

    print(f"\nAll sample GIFs created in '{output_dir}' directory!")
    print("You can now use these GIFs to test gui_image_studio animation features.")


def main():
    """Main function to create sample GIFs."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            create_all_sample_gifs()
        elif sys.argv[1] == "spinner":
            create_loading_spinner("spinner_demo.gif")
        elif sys.argv[1] == "pulse":
            create_pulse_animation("pulse_demo.gif")
        elif sys.argv[1] == "wave":
            create_wave_animation("wave_demo.gif")
        elif sys.argv[1] == "square":
            create_rotating_square("square_demo.gif")
        elif sys.argv[1] == "progress":
            create_progress_bar("progress_demo.gif")
        elif sys.argv[1] == "ball":
            create_bouncing_ball("ball_demo.gif")
        elif sys.argv[1] == "color":
            create_color_cycle("color_demo.gif")
        elif sys.argv[1] == "text":
            create_text_animation("text_demo.gif")
        else:
            print("Unknown animation type. Available types:")
            print("all, spinner, pulse, wave, square, progress, ball, color, text")
    else:
        print("GIF Creator - gui_image_studio")
        print("Usage: python gif_creator.py [animation_type]")
        print("\nAvailable animation types:")
        print("  all      - Create all sample animations")
        print("  spinner  - Loading spinner")
        print("  pulse    - Pulsing circle")
        print("  wave     - Wave animation")
        print("  square   - Rotating square")
        print("  progress - Progress bar")
        print("  ball     - Bouncing ball")
        print("  color    - Color cycling")
        print("  text     - Animated text")
        print("\nExample: python gif_creator.py all")


if __name__ == "__main__":
    main()
