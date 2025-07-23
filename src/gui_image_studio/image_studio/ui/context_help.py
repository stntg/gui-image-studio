"""
Context-sensitive help system for Image Studio.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Dict, Optional

from ..toolkit.tools import ToolRegistry

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class ContextHelpManager:
    """Manages context-sensitive help display."""

    def __init__(self, app: "EnhancedImageDesignerGUI"):
        self.app = app
        self.help_tooltip = None

    def show_tool_help(self, tool_name: str, widget: tk.Widget, x: int, y: int):
        """Show help tooltip for a specific tool."""
        tool = ToolRegistry.get_tool(tool_name)
        if not tool:
            return

        self.hide_help()

        # Create tooltip window
        self.help_tooltip = tk.Toplevel(self.app.root)
        self.help_tooltip.wm_overrideredirect(True)
        self.help_tooltip.configure(bg="#ffffe0", relief="solid", borderwidth=1)

        # Position tooltip
        self.help_tooltip.geometry(f"+{x+10}+{y+10}")

        # Create content
        content_frame = tk.Frame(self.help_tooltip, bg="#ffffe0")
        content_frame.pack(padx=5, pady=5)

        # Tool name
        name_label = tk.Label(
            content_frame,
            text=tool.display_name,
            font=("Arial", 10, "bold"),
            bg="#ffffe0",
            fg="#000000",
        )
        name_label.pack(anchor=tk.W)

        # Tool description
        desc_label = tk.Label(
            content_frame,
            text=tool.get_description(),
            font=("Arial", 9),
            bg="#ffffe0",
            fg="#333333",
            wraplength=250,
            justify=tk.LEFT,
        )
        desc_label.pack(anchor=tk.W, pady=(2, 0))

        # Tool capabilities
        capabilities = []
        if tool.supports_click():
            capabilities.append("Click to draw")
        if tool.supports_drag():
            capabilities.append("Drag for strokes")
        if tool.supports_preview():
            capabilities.append("Live preview")
        if tool.requires_text_input():
            capabilities.append("Text input required")

        if capabilities:
            cap_text = " • ".join(capabilities)
            cap_label = tk.Label(
                content_frame,
                text=cap_text,
                font=("Arial", 8),
                bg="#ffffe0",
                fg="#666666",
                wraplength=250,
                justify=tk.LEFT,
            )
            cap_label.pack(anchor=tk.W, pady=(5, 0))

        # Keyboard shortcut (if available)
        shortcuts = self.get_tool_shortcuts()
        if tool_name in shortcuts:
            shortcut_label = tk.Label(
                content_frame,
                text=f"Shortcut: {shortcuts[tool_name]}",
                font=("Arial", 8, "italic"),
                bg="#ffffe0",
                fg="#0066cc",
            )
            shortcut_label.pack(anchor=tk.W, pady=(3, 0))

        # Auto-hide after delay
        self.app.root.after(5000, self.hide_help)

    def hide_help(self):
        """Hide the help tooltip."""
        if self.help_tooltip:
            self.help_tooltip.destroy()
            self.help_tooltip = None

    def get_tool_shortcuts(self) -> Dict[str, str]:
        """Get keyboard shortcuts for tools."""
        return {
            "brush": "B",
            "pencil": "P",
            "eraser": "E",
            "line": "L",
            "rectangle": "R",
            "circle": "C",
            "text": "T",
            "fill": "F",
            "spray": "S",
            "marker": "M",
            "highlighter": "H",
        }


class QuickHelpPanel:
    """Quick help panel that can be embedded in the main interface."""

    def __init__(self, parent: tk.Widget, app: "EnhancedImageDesignerGUI"):
        self.parent = parent
        self.app = app
        self.current_tool = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the quick help panel UI."""
        # Main frame
        self.frame = ttk.LabelFrame(self.parent, text="Quick Help")

        # Tool info frame
        self.tool_frame = ttk.Frame(self.frame)
        self.tool_frame.pack(fill=tk.X, padx=5, pady=5)

        # Tool name label
        self.tool_name_label = ttk.Label(
            self.tool_frame, text="No tool selected", font=("Arial", 10, "bold")
        )
        self.tool_name_label.pack(anchor=tk.W)

        # Tool description label
        self.tool_desc_label = ttk.Label(
            self.tool_frame,
            text="Select a tool to see help information",
            font=("Arial", 9),
            wraplength=200,
            justify=tk.LEFT,
        )
        self.tool_desc_label.pack(anchor=tk.W, pady=(2, 0))

        # Usage tips label
        self.usage_label = ttk.Label(
            self.tool_frame,
            text="",
            font=("Arial", 8),
            foreground="#666666",
            wraplength=200,
            justify=tk.LEFT,
        )
        self.usage_label.pack(anchor=tk.W, pady=(5, 0))

        # Separator
        ttk.Separator(self.frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)

        # Tips frame
        tips_frame = ttk.Frame(self.frame)
        tips_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Tips label
        tips_title = ttk.Label(tips_frame, text="💡 Tip:", font=("Arial", 9, "bold"))
        tips_title.pack(anchor=tk.W)

        self.tip_label = ttk.Label(
            tips_frame,
            text="Press F1 for comprehensive help",
            font=("Arial", 8),
            wraplength=200,
            justify=tk.LEFT,
        )
        self.tip_label.pack(anchor=tk.W)

        # Update initially
        self.update_help()

        # Schedule regular updates
        self.schedule_update()

    def schedule_update(self):
        """Schedule regular help updates."""
        self.update_help()
        self.parent.after(1000, self.schedule_update)  # Update every second

    def update_help(self):
        """Update help information based on current tool."""
        current_tool = self.app.drawing_tools.get_current_tool()

        if current_tool != self.current_tool:
            self.current_tool = current_tool
            self.refresh_tool_help()

    def refresh_tool_help(self):
        """Refresh the tool help display."""
        if not self.current_tool:
            self.tool_name_label.config(text="No tool selected")
            self.tool_desc_label.config(text="Select a tool to see help information")
            self.usage_label.config(text="")
            self.tip_label.config(text="Press F1 for comprehensive help")
            return

        tool = ToolRegistry.get_tool(self.current_tool)
        if not tool:
            return

        # Update tool name
        self.tool_name_label.config(text=tool.display_name)

        # Update description
        self.tool_desc_label.config(text=tool.get_description())

        # Update usage information
        usage_info = self.get_tool_usage_info(tool)
        self.usage_label.config(text=usage_info)

        # Update tip
        tip = self.get_tool_tip(self.current_tool)
        self.tip_label.config(text=tip)

    def get_tool_usage_info(self, tool) -> str:
        """Get usage information for a tool."""
        usage_parts = []

        if tool.supports_click() and tool.supports_drag():
            if tool.supports_preview():
                usage_parts.append("Click & drag to create shape")
            else:
                usage_parts.append("Click to draw points, drag for strokes")
        elif tool.supports_click():
            if tool.requires_text_input():
                usage_parts.append("Click to place text cursor")
            else:
                usage_parts.append("Click to apply effect")

        if tool.supports_preview():
            usage_parts.append("Live preview while dragging")

        return " • ".join(usage_parts)

    def get_tool_tip(self, tool_name: str) -> str:
        """Get a helpful tip for the current tool."""
        tips = {
            "brush": "Hold Shift while dragging for straight lines",
            "pencil": "Perfect for pixel-perfect editing at high zoom",
            "eraser": "Use different sizes for precise or broad erasing",
            "line": "Hold Shift to constrain to 45-degree angles",
            "rectangle": "Hold Shift to create perfect squares",
            "circle": "Hold Shift to create perfect circles",
            "text": "Choose font and size before placing text",
            "fill": "Click on enclosed areas to fill with color",
            "spray": "Vary speed of movement for different effects",
            "marker": "Great for highlighting and semi-transparent effects",
            "highlighter": "Perfect for creating bright accent marks",
        }

        return tips.get(
            tool_name, "Experiment with different settings for best results"
        )

    def get_frame(self) -> ttk.Frame:
        """Get the main frame widget."""
        return self.frame


class HelpStatusBar:
    """Status bar component that shows contextual help."""

    def __init__(self, parent: tk.Widget, app: "EnhancedImageDesignerGUI"):
        self.parent = parent
        self.app = app

        self.setup_ui()

    def setup_ui(self):
        """Setup the help status bar."""
        self.frame = ttk.Frame(self.parent)

        # Help icon
        self.help_icon = ttk.Label(self.frame, text="❓")
        self.help_icon.pack(side=tk.LEFT, padx=(5, 2))

        # Help text
        self.help_text = ttk.Label(
            self.frame, text="Ready - Press F1 for help", font=("Arial", 9)
        )
        self.help_text.pack(side=tk.LEFT, padx=(0, 10))

        # Bind F1 key
        self.app.root.bind("<F1>", lambda e: self.app.show_help())

        # Schedule updates
        self.schedule_update()

    def schedule_update(self):
        """Schedule regular status updates."""
        self.update_status()
        self.parent.after(2000, self.schedule_update)  # Update every 2 seconds

    def update_status(self):
        """Update the help status."""
        current_tool = self.app.drawing_tools.get_current_tool()

        if current_tool:
            tool = ToolRegistry.get_tool(current_tool)
            if tool:
                shortcuts = {
                    "brush": "B",
                    "pencil": "P",
                    "eraser": "E",
                    "line": "L",
                    "rectangle": "R",
                    "circle": "C",
                    "text": "T",
                    "fill": "F",
                    "spray": "S",
                    "marker": "M",
                    "highlighter": "H",
                }

                shortcut = shortcuts.get(current_tool, "")
                shortcut_text = f" (Press {shortcut})" if shortcut else ""

                self.help_text.config(
                    text=f"{tool.display_name} selected{shortcut_text} - Press F1 for help"
                )
            else:
                self.help_text.config(text="Tool selected - Press F1 for help")
        else:
            self.help_text.config(text="Ready - Press F1 for help")

    def get_frame(self) -> ttk.Frame:
        """Get the status bar frame."""
        return self.frame
