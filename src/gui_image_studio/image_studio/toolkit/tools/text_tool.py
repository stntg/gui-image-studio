"""
Text tool implementation.
"""

import tkinter as tk
from tkinter import simpledialog
from typing import Any, Dict, Optional

from PIL import Image, ImageDraw, ImageFont

from .base_tool import BaseTool, register_tool


@register_tool
class TextTool(BaseTool):
    """Text tool for adding text to images."""

    def __init__(self):
        super().__init__(name="text", display_name="Text", cursor="xterm")
        self.settings = {
            "font_size": 12,
            "color": "#000000",
            "font_family": "Arial",
            "bold": False,
            "italic": False,
        }

    def get_icon(self) -> str:
        """Return the icon name for the text tool."""
        return "text"

    def get_description(self) -> str:
        """Return description of the text tool."""
        return "Add text to your image at the clicked position"

    def on_click(self, image: Image.Image, x: int, y: int, **kwargs) -> None:
        """Handle single click - show text input dialog and add text."""
        # Get text from user
        root = kwargs.get("root")  # Tkinter root window
        if root:
            text = simpledialog.askstring("Text Input", "Enter text:", parent=root)
        else:
            # Fallback if no root provided
            temp_root = tk.Tk()
            temp_root.withdraw()
            text = simpledialog.askstring("Text Input", "Enter text:")
            temp_root.destroy()

        if text:
            self._draw_text(image, x, y, text, **kwargs)

    def on_drag(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle drag - no action for text tool."""
        pass

    def on_release(
        self, image: Image.Image, x1: int, y1: int, x2: int, y2: int, **kwargs
    ) -> None:
        """Handle mouse release - no action for text tool."""
        pass

    def _draw_text(
        self, image: Image.Image, x: int, y: int, text: str, **kwargs
    ) -> None:
        """Draw text on the image."""
        draw = ImageDraw.Draw(image)
        font_size = kwargs.get("font_size", self.settings["font_size"])
        color = kwargs.get("color", "#000000")  # Use passed color or default black
        font_family = kwargs.get("font_family", self.settings["font_family"])
        bold = kwargs.get("bold", self.settings["bold"])
        italic = kwargs.get("italic", self.settings["italic"])

        # Try to load font
        try:
            # Construct font style
            font_style = ""
            if bold and italic:
                font_style = "bold italic"
            elif bold:
                font_style = "bold"
            elif italic:
                font_style = "italic"

            if font_style:
                font_name = f"{font_family} {font_style}"
            else:
                font_name = font_family

            font = ImageFont.truetype(font_name, font_size)
        except (OSError, IOError):
            # Fallback to default font
            try:
                font = ImageFont.load_default()
            except:
                font = None

        # Convert hex color to RGBA tuple for PIL
        try:
            if color.startswith("#"):
                hex_color = color[1:]
                rgba_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
                rgba_color = rgba_color + (255,)  # Add alpha channel
            else:
                rgba_color = color
        except (ValueError, IndexError):
            rgba_color = (0, 0, 0, 255)  # Default to black

        # Draw the text
        draw.text((x, y), text, fill=rgba_color, font=font)

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration."""
        return {
            "font_size": {
                "type": "slider",
                "label": "Font Size",
                "min": 8,
                "max": 72,
                "default": 12,
            },
            "font_family": {
                "type": "dropdown",
                "label": "Font Family",
                "options": [
                    "Arial",
                    "Times New Roman",
                    "Courier New",
                    "Helvetica",
                    "Verdana",
                ],
                "default": "Arial",
            },
            "bold": {"type": "checkbox", "label": "Bold", "default": False},
            "italic": {"type": "checkbox", "label": "Italic", "default": False},
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate text settings."""
        validated = {}
        validated["font_size"] = max(8, min(72, settings.get("font_size", 12)))
        validated["color"] = settings.get("color", "#000000")
        validated["font_family"] = settings.get("font_family", "Arial")
        validated["bold"] = settings.get("bold", False)
        validated["italic"] = settings.get("italic", False)
        return validated

    def requires_text_input(self) -> bool:
        """Text tool requires text input."""
        return True

    def supports_drag(self) -> bool:
        """Text tool doesn't support dragging."""
        return False

    def get_cursor_for_size(self, size: int) -> str:
        """Return text cursor (always xterm)."""
        return "xterm"


# Tool instance is automatically registered via decorator
text_tool = TextTool()
