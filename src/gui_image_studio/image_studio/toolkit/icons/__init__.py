"""
Icon management for tools.
"""

import os
import tkinter as tk
from typing import Dict, Optional

from PIL import Image, ImageDraw, ImageTk


class IconManager:
    """Manages tool icons and creates them if they don't exist."""

    def __init__(self):
        self.icon_cache: Dict[str, tk.PhotoImage] = {}
        self.icon_dir = os.path.join(os.path.dirname(__file__), "files")

        # Ensure icon directory exists
        os.makedirs(self.icon_dir, exist_ok=True)

        # Create default icons if they don't exist
        self._create_default_icons()

    def get_icon(self, tool_name: str, size: int = 16) -> Optional[tk.PhotoImage]:
        """Get icon for a tool, creating it if necessary."""
        cache_key = f"{tool_name}_{size}"

        if cache_key not in self.icon_cache:
            icon_path = os.path.join(self.icon_dir, f"{tool_name}.png")

            if not os.path.exists(icon_path):
                self._create_tool_icon(tool_name, icon_path)

            try:
                # Load and resize icon
                img = Image.open(icon_path)
                img = img.resize((size, size), Image.Resampling.LANCZOS)
                self.icon_cache[cache_key] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading icon for {tool_name}: {e}")
                return None

        return self.icon_cache.get(cache_key)

    def _create_default_icons(self):
        """Create default icons for all tools."""
        icon_definitions = {
            "brush": self._create_brush_icon,
            "pencil": self._create_pencil_icon,
            "eraser": self._create_eraser_icon,
            "line": self._create_line_icon,
            "rectangle": self._create_rectangle_icon,
            "circle": self._create_circle_icon,
            "text": self._create_text_icon,
            "fill": self._create_fill_icon,
            "spray": self._create_spray_icon,
        }

        for tool_name, create_func in icon_definitions.items():
            icon_path = os.path.join(self.icon_dir, f"{tool_name}.png")
            if not os.path.exists(icon_path):
                create_func(icon_path)

    def _create_tool_icon(self, tool_name: str, icon_path: str):
        """Create a generic icon for unknown tools."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Draw a simple tool icon
        draw.rectangle([2, 2, 22, 22], outline="#333333", width=2)
        draw.text((12, 12), tool_name[0].upper(), fill="#333333", anchor="mm")

        img.save(icon_path)

    def _create_brush_icon(self, icon_path: str):
        """Create brush icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Brush handle
        draw.rectangle([10, 2, 14, 18], fill="#8B4513")
        # Brush ferrule (metal part)
        draw.rectangle([8, 16, 16, 20], fill="#C0C0C0")
        # Brush bristles
        draw.ellipse([6, 18, 18, 22], fill="#654321")

        img.save(icon_path)

    def _create_pencil_icon(self, icon_path: str):
        """Create pencil icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Pencil body
        draw.polygon([(12, 2), (8, 6), (8, 20), (16, 20), (16, 6)], fill="#FFD700")
        # Pencil tip
        draw.polygon([(12, 2), (8, 6), (16, 6)], fill="#FFA500")
        # Lead
        draw.polygon([(12, 20), (10, 22), (14, 22)], fill="#333333")

        img.save(icon_path)

    def _create_eraser_icon(self, icon_path: str):
        """Create eraser icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Eraser body
        draw.rectangle([6, 8, 18, 16], fill="#FFB6C1")
        # Eraser band
        draw.rectangle([6, 10, 18, 12], fill="#FF69B4")

        img.save(icon_path)

    def _create_line_icon(self, icon_path: str):
        """Create line icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Diagonal line
        draw.line([(4, 20), (20, 4)], fill="#333333", width=2)
        # End points
        draw.ellipse([2, 18, 6, 22], fill="#333333")
        draw.ellipse([18, 2, 22, 6], fill="#333333")

        img.save(icon_path)

    def _create_rectangle_icon(self, icon_path: str):
        """Create rectangle icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Rectangle outline
        draw.rectangle([4, 6, 20, 18], outline="#333333", width=2)

        img.save(icon_path)

    def _create_circle_icon(self, icon_path: str):
        """Create circle icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Circle outline
        draw.ellipse([4, 4, 20, 20], outline="#333333", width=2)

        img.save(icon_path)

    def _create_text_icon(self, icon_path: str):
        """Create text icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Letter A
        draw.polygon(
            [(12, 4), (8, 20), (10, 20), (11, 16), (13, 16), (14, 20), (16, 20)],
            fill="#333333",
        )
        draw.rectangle([10.5, 13, 13.5, 14], fill="#FFFFFF")

        img.save(icon_path)

    def _create_fill_icon(self, icon_path: str):
        """Create fill/bucket icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Bucket body
        draw.polygon([(6, 10), (18, 10), (16, 20), (8, 20)], fill="#C0C0C0")
        # Bucket handle
        draw.arc([14, 6, 22, 14], 0, 180, fill="#333333", width=2)
        # Paint drip
        draw.ellipse([10, 16, 14, 20], fill="#4169E1")

        img.save(icon_path)

    def _create_spray_icon(self, icon_path: str):
        """Create spray paint icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Spray can body
        draw.rectangle([8, 8, 16, 20], fill="#C0C0C0")
        # Spray nozzle
        draw.rectangle([10, 6, 14, 8], fill="#333333")
        # Spray particles
        for x, y in [(6, 4), (18, 3), (5, 6), (19, 5), (7, 2)]:
            draw.ellipse([x, y, x + 1, y + 1], fill="#4169E1")

        img.save(icon_path)

    def _create_marker_icon(self, icon_path: str):
        """Create marker icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Marker body (thick)
        draw.rectangle([8, 2, 16, 18], fill="#FF6347")

        # Marker tip (black)
        draw.rectangle([10, 18, 14, 22], fill="#000000")

        # Marker cap area
        draw.rectangle([8, 2, 16, 6], fill="#DC143C")

        # Small highlight on body
        draw.line([9, 4, 9, 16], fill="#FF7F7F")

        img.save(icon_path)

    def _create_highlighter_icon(self, icon_path: str):
        """Create highlighter icon."""
        img = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Highlighter body (wide and flat)
        draw.rectangle([6, 8, 18, 16], fill="#FFD700")

        # Highlighter tip (wider)
        draw.rectangle([4, 14, 20, 18], fill="#FFFF00")

        # Highlighter cap
        draw.rectangle([6, 4, 18, 8], fill="#FFA500")

        # Highlight stroke example
        draw.rectangle([2, 19, 22, 21], fill="#FFFF00", outline=None)

        img.save(icon_path)


# Global icon manager instance
icon_manager = IconManager()
