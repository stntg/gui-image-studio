"""
Unified sample creation core.

This module provides comprehensive sample image creation functionality used by both
CLI and GUI interfaces, with support for different themes, sizes, and image types.
"""

import math
import os
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont

from .io_utils import save_image

# Color schemes for different themes
THEME_COLORS = {
    "default": {
        "primary": (100, 150, 200, 255),
        "secondary": (50, 100, 150, 255),
        "accent": (200, 100, 50, 255),
        "background": (240, 240, 240, 255),
        "text": (50, 50, 50, 255),
    },
    "dark": {
        "primary": (200, 200, 200, 255),
        "secondary": (150, 150, 150, 255),
        "accent": (100, 150, 255, 255),
        "background": (40, 40, 40, 255),
        "text": (220, 220, 220, 255),
    },
    "light": {
        "primary": (50, 50, 50, 255),
        "secondary": (100, 100, 100, 255),
        "accent": (255, 100, 100, 255),
        "background": (255, 255, 255, 255),
        "text": (30, 30, 30, 255),
    },
    "colorful": {
        "primary": (255, 100, 100, 255),
        "secondary": (100, 255, 100, 255),
        "accent": (100, 100, 255, 255),
        "background": (255, 255, 100, 255),
        "text": (50, 50, 50, 255),
    },
}

# Standard sizes for different image types
STANDARD_SIZES = {
    "icon": (32, 32),
    "button": (64, 32),
    "logo": (128, 64),
    "banner": (256, 64),
    "square": (64, 64),
    "photo": (200, 150),
    "thumbnail": (96, 96),
}


class SampleImageGenerator:
    """Generator for creating various types of sample images."""

    def __init__(self, theme: str = "default"):
        """
        Initialize the sample image generator.

        Args:
            theme: Color theme to use ("default", "dark", "light", "colorful")
        """
        self.theme = theme
        self.colors = THEME_COLORS.get(theme, THEME_COLORS["default"])

    def create_icon(
        self, icon_type: str = "home", size: Tuple[int, int] = (32, 32)
    ) -> Image.Image:
        """
        Create an icon image.

        Args:
            icon_type: Type of icon ("home", "settings", "help", "file", "folder", "gear")
            size: Icon size as (width, height)

        Returns:
            PIL Image object
        """
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Scale drawing coordinates based on size
        scale_x = size[0] / 32
        scale_y = size[1] / 32

        if icon_type == "home":
            self._draw_home_icon(draw, scale_x, scale_y)
        elif icon_type == "settings" or icon_type == "gear":
            self._draw_gear_icon(draw, size)
        elif icon_type == "help":
            self._draw_help_icon(draw, size)
        elif icon_type == "file":
            self._draw_file_icon(draw, scale_x, scale_y)
        elif icon_type == "folder":
            self._draw_folder_icon(draw, scale_x, scale_y)
        else:
            # Default to a simple circle
            self._draw_circle_icon(draw, size)

        return img

    def create_button(
        self,
        text: str = "Button",
        size: Tuple[int, int] = (64, 32),
        style: str = "flat",
    ) -> Image.Image:
        """
        Create a button image.

        Args:
            text: Button text
            size: Button size as (width, height)
            style: Button style ("flat", "raised", "rounded")

        Returns:
            PIL Image object
        """
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if style == "raised":
            self._draw_raised_button(draw, size, text)
        elif style == "rounded":
            self._draw_rounded_button(draw, size, text)
        else:  # flat
            self._draw_flat_button(draw, size, text)

        return img

    def create_shape(
        self,
        shape_type: str = "circle",
        size: Tuple[int, int] = (64, 64),
        filled: bool = True,
    ) -> Image.Image:
        """
        Create a geometric shape image.

        Args:
            shape_type: Type of shape ("circle", "square", "triangle", "star", "diamond")
            size: Image size as (width, height)
            filled: Whether the shape should be filled

        Returns:
            PIL Image object
        """
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if shape_type == "circle":
            self._draw_circle(draw, size, filled)
        elif shape_type == "square":
            self._draw_square(draw, size, filled)
        elif shape_type == "triangle":
            self._draw_triangle(draw, size, filled)
        elif shape_type == "star":
            self._draw_star(draw, size, filled)
        elif shape_type == "diamond":
            self._draw_diamond(draw, size, filled)
        else:
            # Default to circle
            self._draw_circle(draw, size, filled)

        return img

    def create_gradient(
        self,
        size: Tuple[int, int] = (200, 150),
        direction: str = "horizontal",
        colors: Optional[List[Tuple[int, int, int, int]]] = None,
    ) -> Image.Image:
        """
        Create a gradient image.

        Args:
            size: Image size as (width, height)
            direction: Gradient direction ("horizontal", "vertical", "diagonal", "radial")
            colors: List of RGBA colors for gradient (uses theme colors if None)

        Returns:
            PIL Image object
        """
        if colors is None:
            colors = [self.colors["primary"], self.colors["accent"]]

        img = Image.new("RGBA", size, (0, 0, 0, 0))

        if direction == "radial":
            self._create_radial_gradient(img, colors)
        else:
            self._create_linear_gradient(img, direction, colors)

        return img

    def create_pattern(
        self,
        pattern_type: str = "checkerboard",
        size: Tuple[int, int] = (200, 150),
        tile_size: int = 16,
    ) -> Image.Image:
        """
        Create a pattern image.

        Args:
            pattern_type: Type of pattern ("checkerboard", "stripes", "dots", "grid")
            size: Image size as (width, height)
            tile_size: Size of pattern tiles

        Returns:
            PIL Image object
        """
        img = Image.new("RGBA", size, self.colors["background"])
        draw = ImageDraw.Draw(img)

        if pattern_type == "checkerboard":
            self._draw_checkerboard(draw, size, tile_size)
        elif pattern_type == "stripes":
            self._draw_stripes(draw, size, tile_size)
        elif pattern_type == "dots":
            self._draw_dots(draw, size, tile_size)
        elif pattern_type == "grid":
            self._draw_grid(draw, size, tile_size)

        return img

    def create_animated_frames(
        self,
        frame_count: int = 8,
        size: Tuple[int, int] = (64, 64),
        animation_type: str = "spinner",
    ) -> List[Image.Image]:
        """
        Create frames for an animated GIF.

        Args:
            frame_count: Number of animation frames
            size: Frame size as (width, height)
            animation_type: Type of animation ("spinner", "pulse", "bounce")

        Returns:
            List of PIL Image objects
        """
        frames = []

        for i in range(frame_count):
            progress = i / frame_count

            if animation_type == "spinner":
                frame = self._create_spinner_frame(size, progress)
            elif animation_type == "pulse":
                frame = self._create_pulse_frame(size, progress)
            elif animation_type == "bounce":
                frame = self._create_bounce_frame(size, progress)
            else:
                frame = self._create_spinner_frame(size, progress)

            frames.append(frame)

        return frames

    # Private helper methods for drawing specific elements

    def _draw_home_icon(self, draw: ImageDraw.Draw, scale_x: float, scale_y: float):
        """Draw a home icon."""
        # Base
        draw.rectangle(
            [10 * scale_x, 18 * scale_y, 22 * scale_x, 28 * scale_y],
            fill=self.colors["primary"],
            outline=self.colors["secondary"],
            width=max(1, int(scale_x)),
        )
        # Roof
        draw.polygon(
            [
                (16 * scale_x, 8 * scale_y),
                (8 * scale_x, 18 * scale_y),
                (24 * scale_x, 18 * scale_y),
            ],
            fill=self.colors["accent"],
            outline=self.colors["secondary"],
        )
        # Door
        draw.rectangle(
            [14 * scale_x, 22 * scale_y, 18 * scale_x, 28 * scale_y],
            fill=self.colors["secondary"],
        )

    def _draw_gear_icon(self, draw: ImageDraw.Draw, size: Tuple[int, int]):
        """Draw a gear icon."""
        center = (size[0] // 2, size[1] // 2)
        outer_radius = min(size) // 3
        inner_radius = outer_radius // 2
        teeth = 8

        # Draw gear teeth
        for i in range(teeth):
            angle1 = math.radians(i * 360 / teeth)
            angle2 = math.radians((i + 0.3) * 360 / teeth)
            angle3 = math.radians((i + 0.7) * 360 / teeth)
            angle4 = math.radians((i + 1) * 360 / teeth)

            tooth_height = outer_radius // 4

            x1 = center[0] + outer_radius * math.cos(angle1)
            y1 = center[1] + outer_radius * math.sin(angle1)
            x2 = center[0] + (outer_radius + tooth_height) * math.cos(angle2)
            y2 = center[1] + (outer_radius + tooth_height) * math.sin(angle2)
            x3 = center[0] + (outer_radius + tooth_height) * math.cos(angle3)
            y3 = center[1] + (outer_radius + tooth_height) * math.sin(angle3)
            x4 = center[0] + outer_radius * math.cos(angle4)
            y4 = center[1] + outer_radius * math.sin(angle4)

            draw.polygon(
                [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=self.colors["primary"]
            )

        # Draw main circle
        draw.ellipse(
            [
                center[0] - outer_radius,
                center[1] - outer_radius,
                center[0] + outer_radius,
                center[1] + outer_radius,
            ],
            fill=self.colors["primary"],
            outline=self.colors["secondary"],
        )

        # Draw inner circle
        draw.ellipse(
            [
                center[0] - inner_radius,
                center[1] - inner_radius,
                center[0] + inner_radius,
                center[1] + inner_radius,
            ],
            fill=self.colors["background"],
            outline=self.colors["secondary"],
        )

    def _draw_help_icon(self, draw: ImageDraw.Draw, size: Tuple[int, int]):
        """Draw a help (question mark) icon."""
        center = (size[0] // 2, size[1] // 2)
        radius = min(size) // 2 - 2

        # Draw circle background
        draw.ellipse(
            [
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ],
            fill=self.colors["primary"],
            outline=self.colors["secondary"],
        )

        # Draw question mark (simplified)
        # Top curve
        draw.arc(
            [
                center[0] - radius // 2,
                center[1] - radius // 2,
                center[0] + radius // 2,
                center[1],
            ],
            start=180,
            end=0,
            fill=self.colors["text"],
            width=2,
        )

        # Vertical line
        draw.line(
            [center[0], center[1], center[0], center[1] + radius // 3],
            fill=self.colors["text"],
            width=2,
        )

        # Dot
        dot_size = 2
        draw.ellipse(
            [
                center[0] - dot_size,
                center[1] + radius // 2 - dot_size,
                center[0] + dot_size,
                center[1] + radius // 2 + dot_size,
            ],
            fill=self.colors["text"],
        )

    def _draw_file_icon(self, draw: ImageDraw.Draw, scale_x: float, scale_y: float):
        """Draw a file icon."""
        # Main rectangle
        draw.rectangle(
            [8 * scale_x, 6 * scale_y, 20 * scale_x, 26 * scale_y],
            fill=self.colors["background"],
            outline=self.colors["primary"],
            width=max(1, int(scale_x)),
        )

        # Folded corner
        draw.polygon(
            [
                (16 * scale_x, 6 * scale_y),
                (20 * scale_x, 6 * scale_y),
                (20 * scale_x, 10 * scale_y),
            ],
            fill=self.colors["secondary"],
        )

        # Lines representing text
        for i, y in enumerate([12, 16, 20]):
            width = 8 if i < 2 else 6
            draw.line(
                [10 * scale_x, y * scale_y, (10 + width) * scale_x, y * scale_y],
                fill=self.colors["text"],
                width=max(1, int(scale_y)),
            )

    def _draw_folder_icon(self, draw: ImageDraw.Draw, scale_x: float, scale_y: float):
        """Draw a folder icon."""
        # Folder tab
        draw.rectangle(
            [6 * scale_x, 10 * scale_y, 14 * scale_x, 14 * scale_y],
            fill=self.colors["accent"],
            outline=self.colors["secondary"],
        )

        # Main folder body
        draw.rectangle(
            [6 * scale_x, 14 * scale_y, 26 * scale_x, 24 * scale_y],
            fill=self.colors["primary"],
            outline=self.colors["secondary"],
            width=max(1, int(scale_x)),
        )

    def _draw_circle_icon(self, draw: ImageDraw.Draw, size: Tuple[int, int]):
        """Draw a simple circle icon."""
        center = (size[0] // 2, size[1] // 2)
        radius = min(size) // 2 - 2

        draw.ellipse(
            [
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ],
            fill=self.colors["primary"],
            outline=self.colors["secondary"],
            width=2,
        )

    def _draw_flat_button(self, draw: ImageDraw.Draw, size: Tuple[int, int], text: str):
        """Draw a flat button."""
        draw.rectangle(
            [0, 0, size[0] - 1, size[1] - 1],
            fill=self.colors["primary"],
            outline=self.colors["secondary"],
        )

        # Add text (simplified - just a rectangle representing text)
        text_width = len(text) * 4
        text_height = 8
        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2

        draw.rectangle(
            [text_x, text_y, text_x + text_width, text_y + text_height],
            fill=self.colors["text"],
        )

    def _draw_raised_button(
        self, draw: ImageDraw.Draw, size: Tuple[int, int], text: str
    ):
        """Draw a raised button with 3D effect."""
        # Main button
        draw.rectangle([1, 1, size[0] - 2, size[1] - 2], fill=self.colors["primary"])

        # Highlight (top and left)
        draw.line([0, 0, size[0] - 1, 0], fill=self.colors["background"], width=1)
        draw.line([0, 0, 0, size[1] - 1], fill=self.colors["background"], width=1)

        # Shadow (bottom and right)
        draw.line(
            [1, size[1] - 1, size[0] - 1, size[1] - 1],
            fill=self.colors["secondary"],
            width=1,
        )
        draw.line(
            [size[0] - 1, 1, size[0] - 1, size[1] - 1],
            fill=self.colors["secondary"],
            width=1,
        )

        # Text
        text_width = len(text) * 4
        text_height = 8
        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2

        draw.rectangle(
            [text_x, text_y, text_x + text_width, text_y + text_height],
            fill=self.colors["text"],
        )

    def _draw_rounded_button(
        self, draw: ImageDraw.Draw, size: Tuple[int, int], text: str
    ):
        """Draw a rounded button."""
        radius = min(size[1] // 4, 8)

        # Draw rounded rectangle using arcs and lines
        # This is a simplified version - for production, you'd want proper rounded rectangles
        draw.rectangle(
            [radius, 0, size[0] - radius, size[1]], fill=self.colors["primary"]
        )
        draw.rectangle(
            [0, radius, size[0], size[1] - radius], fill=self.colors["primary"]
        )

        # Corner circles
        draw.ellipse([0, 0, radius * 2, radius * 2], fill=self.colors["primary"])
        draw.ellipse(
            [size[0] - radius * 2, 0, size[0], radius * 2], fill=self.colors["primary"]
        )
        draw.ellipse(
            [0, size[1] - radius * 2, radius * 2, size[1]], fill=self.colors["primary"]
        )
        draw.ellipse(
            [size[0] - radius * 2, size[1] - radius * 2, size[0], size[1]],
            fill=self.colors["primary"],
        )

        # Text
        text_width = len(text) * 4
        text_height = 8
        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2

        draw.rectangle(
            [text_x, text_y, text_x + text_width, text_y + text_height],
            fill=self.colors["text"],
        )

    def _draw_circle(self, draw: ImageDraw.Draw, size: Tuple[int, int], filled: bool):
        """Draw a circle."""
        center = (size[0] // 2, size[1] // 2)
        radius = min(size) // 2 - 2

        if filled:
            draw.ellipse(
                [
                    center[0] - radius,
                    center[1] - radius,
                    center[0] + radius,
                    center[1] + radius,
                ],
                fill=self.colors["primary"],
                outline=self.colors["secondary"],
            )
        else:
            draw.ellipse(
                [
                    center[0] - radius,
                    center[1] - radius,
                    center[0] + radius,
                    center[1] + radius,
                ],
                outline=self.colors["primary"],
                width=3,
            )

    def _draw_square(self, draw: ImageDraw.Draw, size: Tuple[int, int], filled: bool):
        """Draw a square."""
        side = min(size) - 4
        x = (size[0] - side) // 2
        y = (size[1] - side) // 2

        if filled:
            draw.rectangle(
                [x, y, x + side, y + side],
                fill=self.colors["primary"],
                outline=self.colors["secondary"],
            )
        else:
            draw.rectangle(
                [x, y, x + side, y + side], outline=self.colors["primary"], width=3
            )

    def _draw_triangle(self, draw: ImageDraw.Draw, size: Tuple[int, int], filled: bool):
        """Draw a triangle."""
        center_x = size[0] // 2
        height = min(size) - 4
        width = int(height * 0.866)  # Equilateral triangle

        points = [
            (center_x, 2),  # Top
            (center_x - width // 2, height),  # Bottom left
            (center_x + width // 2, height),  # Bottom right
        ]

        if filled:
            draw.polygon(
                points, fill=self.colors["primary"], outline=self.colors["secondary"]
            )
        else:
            draw.polygon(points, outline=self.colors["primary"], width=3)

    def _draw_star(self, draw: ImageDraw.Draw, size: Tuple[int, int], filled: bool):
        """Draw a 5-pointed star."""
        center = (size[0] // 2, size[1] // 2)
        outer_radius = min(size) // 2 - 2
        inner_radius = outer_radius // 2

        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)  # Start from top
            if i % 2 == 0:  # Outer points
                x = center[0] + outer_radius * math.cos(angle)
                y = center[1] + outer_radius * math.sin(angle)
            else:  # Inner points
                x = center[0] + inner_radius * math.cos(angle)
                y = center[1] + inner_radius * math.sin(angle)
            points.append((x, y))

        if filled:
            draw.polygon(
                points, fill=self.colors["primary"], outline=self.colors["secondary"]
            )
        else:
            draw.polygon(points, outline=self.colors["primary"], width=2)

    def _draw_diamond(self, draw: ImageDraw.Draw, size: Tuple[int, int], filled: bool):
        """Draw a diamond."""
        center = (size[0] // 2, size[1] // 2)
        half_width = size[0] // 2 - 2
        half_height = size[1] // 2 - 2

        points = [
            (center[0], center[1] - half_height),  # Top
            (center[0] + half_width, center[1]),  # Right
            (center[0], center[1] + half_height),  # Bottom
            (center[0] - half_width, center[1]),  # Left
        ]

        if filled:
            draw.polygon(
                points, fill=self.colors["primary"], outline=self.colors["secondary"]
            )
        else:
            draw.polygon(points, outline=self.colors["primary"], width=3)

    def _create_linear_gradient(
        self, img: Image.Image, direction: str, colors: List[Tuple[int, int, int, int]]
    ):
        """Create a linear gradient."""
        width, height = img.size

        for y in range(height):
            for x in range(width):
                if direction == "horizontal":
                    progress = x / width
                elif direction == "vertical":
                    progress = y / height
                elif direction == "diagonal":
                    progress = (x + y) / (width + height)
                else:
                    progress = x / width

                # Interpolate between colors
                if len(colors) == 2:
                    color = self._interpolate_color(colors[0], colors[1], progress)
                else:
                    # Multi-color gradient
                    segment = progress * (len(colors) - 1)
                    idx = int(segment)
                    local_progress = segment - idx

                    if idx >= len(colors) - 1:
                        color = colors[-1]
                    else:
                        color = self._interpolate_color(
                            colors[idx], colors[idx + 1], local_progress
                        )

                img.putpixel((x, y), color)

    def _create_radial_gradient(
        self, img: Image.Image, colors: List[Tuple[int, int, int, int]]
    ):
        """Create a radial gradient."""
        width, height = img.size
        center_x, center_y = width // 2, height // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)

        for y in range(height):
            for x in range(width):
                distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                progress = min(distance / max_distance, 1.0)

                if len(colors) == 2:
                    color = self._interpolate_color(colors[0], colors[1], progress)
                else:
                    segment = progress * (len(colors) - 1)
                    idx = int(segment)
                    local_progress = segment - idx

                    if idx >= len(colors) - 1:
                        color = colors[-1]
                    else:
                        color = self._interpolate_color(
                            colors[idx], colors[idx + 1], local_progress
                        )

                img.putpixel((x, y), color)

    def _interpolate_color(
        self,
        color1: Tuple[int, int, int, int],
        color2: Tuple[int, int, int, int],
        t: float,
    ) -> Tuple[int, int, int, int]:
        """Interpolate between two RGBA colors."""
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
            int(color1[3] + (color2[3] - color1[3]) * t),
        )

    def _draw_checkerboard(
        self, draw: ImageDraw.Draw, size: Tuple[int, int], tile_size: int
    ):
        """Draw a checkerboard pattern."""
        for y in range(0, size[1], tile_size):
            for x in range(0, size[0], tile_size):
                if (x // tile_size + y // tile_size) % 2:
                    draw.rectangle(
                        [
                            x,
                            y,
                            min(x + tile_size, size[0]),
                            min(y + tile_size, size[1]),
                        ],
                        fill=self.colors["primary"],
                    )

    def _draw_stripes(
        self, draw: ImageDraw.Draw, size: Tuple[int, int], tile_size: int
    ):
        """Draw a striped pattern."""
        for x in range(0, size[0], tile_size * 2):
            draw.rectangle(
                [x, 0, min(x + tile_size, size[0]), size[1]],
                fill=self.colors["primary"],
            )

    def _draw_dots(self, draw: ImageDraw.Draw, size: Tuple[int, int], tile_size: int):
        """Draw a dotted pattern."""
        dot_radius = tile_size // 4
        for y in range(tile_size, size[1], tile_size):
            for x in range(tile_size, size[0], tile_size):
                draw.ellipse(
                    [x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius],
                    fill=self.colors["primary"],
                )

    def _draw_grid(self, draw: ImageDraw.Draw, size: Tuple[int, int], tile_size: int):
        """Draw a grid pattern."""
        # Vertical lines
        for x in range(0, size[0], tile_size):
            draw.line([x, 0, x, size[1]], fill=self.colors["primary"], width=1)

        # Horizontal lines
        for y in range(0, size[1], tile_size):
            draw.line([0, y, size[0], y], fill=self.colors["primary"], width=1)

    def _create_spinner_frame(
        self, size: Tuple[int, int], progress: float
    ) -> Image.Image:
        """Create a frame for a spinning animation."""
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center = (size[0] // 2, size[1] // 2)
        radius = min(size) // 3

        # Draw spinning arc
        start_angle = int(progress * 360)
        end_angle = start_angle + 90

        draw.arc(
            [
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ],
            start=start_angle,
            end=end_angle,
            fill=self.colors["primary"],
            width=4,
        )

        return img

    def _create_pulse_frame(
        self, size: Tuple[int, int], progress: float
    ) -> Image.Image:
        """Create a frame for a pulsing animation."""
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        center = (size[0] // 2, size[1] // 2)
        base_radius = min(size) // 4
        pulse_radius = int(base_radius * (1 + 0.5 * math.sin(progress * 2 * math.pi)))

        draw.ellipse(
            [
                center[0] - pulse_radius,
                center[1] - pulse_radius,
                center[0] + pulse_radius,
                center[1] + pulse_radius,
            ],
            fill=self.colors["primary"],
        )

        return img

    def _create_bounce_frame(
        self, size: Tuple[int, int], progress: float
    ) -> Image.Image:
        """Create a frame for a bouncing animation."""
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        ball_radius = min(size) // 8
        center_x = size[0] // 2

        # Bounce motion
        bounce_height = size[1] // 3
        y_offset = int(bounce_height * abs(math.sin(progress * math.pi)))
        center_y = size[1] - ball_radius - y_offset

        draw.ellipse(
            [
                center_x - ball_radius,
                center_y - ball_radius,
                center_x + ball_radius,
                center_y + ball_radius,
            ],
            fill=self.colors["primary"],
        )

        return img


def create_sample_image_set(
    output_dir: Union[str, Path],
    themes: Optional[List[str]] = None,
    image_types: Optional[List[str]] = None,
    include_animations: bool = True,
) -> Dict[str, List[str]]:
    """
    Create a comprehensive set of sample images.

    Args:
        output_dir: Directory to save images
        themes: List of themes to generate ("default", "dark", "light", "colorful")
        image_types: List of image types to generate
        include_animations: Whether to create animated GIFs

    Returns:
        Dictionary mapping themes to lists of created filenames
    """
    if themes is None:
        themes = ["default", "dark", "light"]

    if image_types is None:
        image_types = ["icons", "buttons", "shapes", "patterns"]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    created_files = {}

    for theme in themes:
        generator = SampleImageGenerator(theme)
        theme_files = []

        if "icons" in image_types:
            # Create various icons
            icon_types = ["home", "settings", "help", "file", "folder"]
            for icon_type in icon_types:
                filename = f"{theme}_{icon_type}.png"
                image = generator.create_icon(icon_type, STANDARD_SIZES["icon"])
                save_image(image, output_path / filename)
                theme_files.append(filename)

        if "buttons" in image_types:
            # Create various buttons
            button_configs = [
                ("ok", "flat"),
                ("cancel", "raised"),
                ("apply", "rounded"),
            ]
            for text, style in button_configs:
                filename = f"{theme}_{text}.png"
                image = generator.create_button(
                    text.title(), STANDARD_SIZES["button"], style
                )
                save_image(image, output_path / filename)
                theme_files.append(filename)

        if "shapes" in image_types:
            # Create geometric shapes
            shapes = ["circle", "square", "triangle", "star", "diamond"]
            for shape in shapes:
                filename = f"{theme}_{shape}.png"
                image = generator.create_shape(shape, STANDARD_SIZES["square"])
                save_image(image, output_path / filename)
                theme_files.append(filename)

        if "patterns" in image_types:
            # Create patterns
            patterns = ["checkerboard", "stripes", "dots", "grid"]
            for pattern in patterns:
                filename = f"{theme}_{pattern}.png"
                image = generator.create_pattern(pattern, STANDARD_SIZES["photo"])
                save_image(image, output_path / filename)
                theme_files.append(filename)

        if "gradients" in image_types:
            # Create gradients
            gradients = ["horizontal", "vertical", "radial"]
            for gradient in gradients:
                filename = f"{theme}_gradient_{gradient}.png"
                image = generator.create_gradient(STANDARD_SIZES["photo"], gradient)
                save_image(image, output_path / filename)
                theme_files.append(filename)

        if (
            include_animations and theme == "default"
        ):  # Only create animations for default theme
            # Create animated GIFs
            animations = ["spinner", "pulse", "bounce"]
            for animation in animations:
                filename = f"{theme}_{animation}.gif"
                frames = generator.create_animated_frames(
                    8, STANDARD_SIZES["square"], animation
                )

                # Save as animated GIF
                frames[0].save(
                    output_path / filename,
                    save_all=True,
                    append_images=frames[1:],
                    duration=100,
                    loop=0,
                )
                theme_files.append(filename)

        created_files[theme] = theme_files

    return created_files


def create_sample_images_legacy_compatible(output_dir: str = "sample_images") -> None:
    """
    Create sample images compatible with the legacy sample_creator interface.

    Args:
        output_dir: Output directory for sample images
    """
    # Create the same images as the original sample_creator for backward compatibility
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Use default theme generator
    generator = SampleImageGenerator("default")

    # Create basic icon
    icon = generator.create_icon("home", (64, 64))
    save_image(icon, output_path / "icon.png")

    # Create themed icons
    for theme in ["dark", "light"]:
        themed_generator = SampleImageGenerator(theme)
        icon = themed_generator.create_icon("settings", (64, 64))
        save_image(icon, output_path / f"{theme}_icon.png")

    # Create buttons
    for theme, text in [("default", "Play"), ("dark", "Stop"), ("light", "Pause")]:
        button_generator = SampleImageGenerator(
            theme if theme != "default" else "default"
        )
        button = button_generator.create_button(text, (64, 32))
        prefix = f"{theme}_" if theme != "default" else ""
        save_image(button, output_path / f"{prefix}button.png")

    # Create logos (using gradient)
    for theme in ["default", "dark"]:
        logo_generator = SampleImageGenerator(theme)
        logo = logo_generator.create_gradient((128, 64), "horizontal")
        prefix = f"{theme}_" if theme != "default" else ""
        save_image(logo, output_path / f"{prefix}logo.png")

    # Create shapes
    shapes = ["circle", "square", "triangle"]
    for shape in shapes:
        shape_image = generator.create_shape(shape, (64, 64))
        save_image(shape_image, output_path / f"{shape}.png")

    # Create colorful image
    colorful_generator = SampleImageGenerator("colorful")
    colorful = colorful_generator.create_gradient((200, 150), "radial")
    save_image(colorful, output_path / "colorful.png")

    # Create animated GIFs
    for theme, animation in [("default", "spinner"), ("dark", "pulse")]:
        anim_generator = SampleImageGenerator(theme)
        frames = anim_generator.create_animated_frames(8, (64, 64), animation)

        prefix = f"{theme}_" if theme != "default" else ""
        frames[0].save(
            output_path / f"{prefix}animation.gif",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )

    print(f"Sample images created in '{output_dir}' directory")
