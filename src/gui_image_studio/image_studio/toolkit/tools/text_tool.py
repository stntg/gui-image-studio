# text_tool.py

import os
import tkinter as tk
from functools import lru_cache
from tkinter import simpledialog
from typing import Any, Dict, List, Optional, Tuple

from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

from .base_tool import BaseTool, register_tool


@register_tool
class TextTool(BaseTool):
    """Text tool for adding text to images. Uses matplotlib.font_manager to locate system fonts across platforms."""

    def __init__(self) -> None:
        super().__init__(name="text", display_name="Text", cursor="xterm")

        # Default settings
        self.settings: Dict[str, Any] = {
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
        root = kwargs.get("root")
        if root:
            text = simpledialog.askstring("Text Input", "Enter text:", parent=root)
        else:
            temp_root = tk.Tk()
            temp_root.withdraw()
            text = simpledialog.askstring("Text Input", "Enter text:")
            temp_root.destroy()

        if text:
            self._draw_text(
                image,
                x,
                y,
                text,
                font_size=kwargs.get("font_size", self.settings["font_size"]),
                color=kwargs.get("color", self.settings["color"]),
                font_family=kwargs.get("font_family", self.settings["font_family"]),
                bold=kwargs.get("bold", self.settings["bold"]),
                italic=kwargs.get("italic", self.settings["italic"]),
            )

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
        self,
        image: Image.Image,
        x: int,
        y: int,
        text: str,
        *,
        font_size: int,
        color: str,
        font_family: str,
        bold: bool,
        italic: bool,
    ) -> None:
        """Draw the given text onto the image at (x, y)."""
        draw = ImageDraw.Draw(image)
        font = self._load_font(font_family, font_size, bold, italic)
        fill = self._parse_color(color)
        draw.text((x, y), text, font=font, fill=fill)

    @lru_cache(maxsize=64)
    def _find_font_path(self, family: str, bold: bool, italic: bool) -> Optional[str]:
        """Locate a font file matching the requested family and style. Caches up to 64 lookups."""
        # Build style suffix
        style = ""
        if bold:
            style += " Bold"
        if italic:
            style += " Italic"

        query = f"{family}{style}".strip()
        try:
            path = font_manager.findfont(query, fallback_to_default=False)
            if os.path.exists(path):
                return path
        except (OSError, IOError, AttributeError):
            # Font file not found or not accessible
            pass

        # Fallback to plain family
        try:
            path = font_manager.findfont(family, fallback_to_default=True)
            return path if os.path.exists(path) else None
        except Exception:
            return None

    def _load_font(
        self, family: str, size: int, bold: bool, italic: bool
    ) -> ImageFont.FreeTypeFont:
        """Return an ImageFont instance, or PIL’s default if lookup fails."""
        font_path = self._find_font_path(family, bold, italic)
        try:
            if font_path:
                return ImageFont.truetype(font_path, size)
        except (OSError, IOError):
            # Font file not found or not accessible
            pass

        # Graceful fallback
        try:
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()

    @staticmethod
    def _parse_color(color_str: str) -> Tuple[int, int, int, int]:
        """Convert '#RRGGBB' to RGBA tuple, or default black."""
        if isinstance(color_str, str) and color_str.startswith("#"):
            hex_ = color_str.lstrip("#")
            if len(hex_) == 6:
                r, g, b = tuple(int(hex_[i : i + 2], 16) for i in (0, 2, 4))
                return (r, g, b, 255)
        return (0, 0, 0, 255)

    @staticmethod
    @lru_cache(maxsize=1)
    def _get_available_font_families() -> List[str]:
        """Return a sorted list of installed font family names. Cached so the scan runs only once."""
        return sorted({f.name for f in font_manager.fontManager.ttflist})

    def get_settings_panel(self) -> Optional[Dict[str, Any]]:
        """Return settings panel configuration, with a dynamic font-family dropdown."""
        families = self._get_available_font_families()
        return {
            "font_size": {
                "type": "slider",
                "label": "Font Size",
                "min": 8,
                "max": 72,
                "default": self.settings["font_size"],
            },
            "font_family": {
                "type": "dropdown",
                "label": "Font Family",
                "options": families,
                "default": self.settings["font_family"],
            },
            "bold": {
                "type": "checkbox",
                "label": "Bold",
                "default": self.settings["bold"],
            },
            "italic": {
                "type": "checkbox",
                "label": "Italic",
                "default": self.settings["italic"],
            },
        }

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Enforce valid ranges and types on user-provided settings."""
        validated: Dict[str, Any] = {}
        validated["font_size"] = max(8, min(72, int(settings.get("font_size", 12))))
        validated["color"] = settings.get("color", "#000000")
        validated["font_family"] = settings.get("font_family", "Arial")
        validated["bold"] = bool(settings.get("bold", False))
        validated["italic"] = bool(settings.get("italic", False))
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


# Instantiate (auto-registers via decorator)
text_tool = TextTool()
