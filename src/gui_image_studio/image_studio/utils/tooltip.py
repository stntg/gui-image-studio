"""
Tooltip utility for widgets.
"""

import tkinter as tk
from typing import Optional


class ToolTip:
    """Simple tooltip class for widgets."""

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event: Optional[tk.Event] = None) -> None:
        """Show tooltip on mouse enter."""
        if self.tooltip_window or not self.text:
            return

        # Get widget position for tooltip placement
        try:
            # For text widgets, try to get cursor position
            if isinstance(self.widget, tk.Text) and hasattr(self.widget, "bbox"):
                bbox = self.widget.bbox("insert")
                if bbox:
                    x, y, _, _ = bbox
                else:
                    x, y = 0, 0
            elif isinstance(self.widget, tk.Entry) and hasattr(self.widget, "bbox"):
                # For Entry widgets, bbox also supports "insert"
                bbox = self.widget.bbox("insert")
                if bbox:
                    x, y, _, _ = bbox
                else:
                    x, y = 0, 0
            else:
                # For other widgets, use default position
                x, y = 0, 0
        except (tk.TclError, TypeError, AttributeError):
            # Fallback if bbox fails
            x, y = 0, 0

        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 8),
        )
        label.pack(ipadx=1)

    def on_leave(self, event: Optional[tk.Event] = None) -> None:
        """Hide tooltip on mouse leave."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
        return
