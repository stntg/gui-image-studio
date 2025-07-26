"""
Left panel UI setup for Image Studio.
Contains tools and image management functionality.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class LeftPanel:
    """Manages the left panel UI with tools and image management."""

    def __init__(self, app: "EnhancedImageDesignerGUI"):
        self.app = app

    def setup(self, parent):
        """Setup the left panel with tools and image management."""
        # Tools section - more compact
        tools_frame = ttk.LabelFrame(parent, text="Design Tools")
        tools_frame.pack(fill=tk.X, padx=3, pady=3)

        # Tool buttons - more compact with shorter labels
        tools_grid = ttk.Frame(tools_frame)
        tools_grid.pack(fill=tk.X, padx=3, pady=3)

        self.app.tool_buttons = {}

        # Get all registered tools from the drawing tools manager
        from ..toolkit.icons import icon_manager

        tools_info = self.app.drawing_tools.get_all_tool_info()

        for i, (tool_name, tool_info) in enumerate(tools_info.items()):
            # Get icon for the tool
            icon = icon_manager.get_icon(tool_info["icon"], size=16)

            # Create button with icon and text
            btn = tk.Button(
                tools_grid,
                text=tool_info["display_name"],
                image=icon if icon else None,
                compound=tk.LEFT if icon else tk.NONE,
                command=lambda t=tool_name: self.app.select_tool(t),
                font=("Arial", 8),
                relief="raised",
                bd=1,
                padx=2,
                pady=2,
            )

            # Keep a reference to the icon to prevent garbage collection
            if icon:
                btn.image = icon

            # Add tooltip with tool description
            self._create_tooltip(btn, tool_info["description"])

            btn.grid(row=i // 2, column=i % 2, sticky="ew", padx=1, pady=1)
            self.app.tool_buttons[tool_name] = btn

        tools_grid.columnconfigure(0, weight=1)
        tools_grid.columnconfigure(1, weight=1)

        # Tool properties - more compact
        props_frame = ttk.LabelFrame(parent, text="Tool Properties")
        props_frame.pack(fill=tk.X, padx=3, pady=3)

        # Brush size - smaller font and padding
        ttk.Label(props_frame, text="Size:", font=("Arial", 8)).pack(
            anchor=tk.W, padx=3
        )
        self.app.size_var = tk.IntVar(value=5)
        size_scale = ttk.Scale(
            props_frame,
            from_=1,
            to=50,
            variable=self.app.size_var,
            orient=tk.HORIZONTAL,
            length=150,
        )
        size_scale.pack(fill=tk.X, padx=3, pady=1)

        # Color picker - more compact
        color_frame = ttk.Frame(props_frame)
        color_frame.pack(fill=tk.X, padx=3, pady=3)

        ttk.Label(color_frame, text="Color:", font=("Arial", 8)).pack(side=tk.LEFT)
        self.app.color_button = tk.Button(
            color_frame,
            bg=self.app.drawing_tools.get_brush_color(),
            width=4,
            height=1,
            command=self.app.choose_color,
        )
        self.app.color_button.pack(side=tk.RIGHT)

        # Image management section - more compact
        images_frame = ttk.LabelFrame(parent, text="Images")
        images_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # Image list - smaller font
        list_frame = ttk.Frame(images_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        self.app.image_listbox = tk.Listbox(list_frame, font=("Arial", 8))
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.app.image_listbox.yview
        )
        self.app.image_listbox.configure(yscrollcommand=scrollbar.set)

        # Bind selection event
        self.app.image_listbox.bind("<<ListboxSelect>>", self.app.on_image_select)

        self.app.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Image management buttons - more compact
        btn_frame = ttk.Frame(images_frame)
        btn_frame.pack(fill=tk.X, padx=3, pady=3)

        # Use grid for more compact button layout
        self.app.new_image_btn = tk.Button(
            btn_frame,
            text="🆕 New",
            command=self.app.new_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        )
        self.app.new_image_btn.grid(row=0, column=0, sticky="ew", padx=1, pady=1)

        self.app.load_image_btn = tk.Button(
            btn_frame,
            text="📁 Load",
            command=self.app.load_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        )
        self.app.load_image_btn.grid(row=0, column=1, sticky="ew", padx=1, pady=1)

        tk.Button(
            btn_frame,
            text="Copy",
            command=self.app.duplicate_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).grid(row=1, column=0, sticky="ew", padx=1, pady=1)

        tk.Button(
            btn_frame,
            text="Delete",
            command=self.app.delete_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).grid(row=1, column=1, sticky="ew", padx=1, pady=1)

        # Configure grid weights for buttons
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

    def _create_tooltip(self, widget, text):
        """Create a simple tooltip for a widget."""

        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

            label = tk.Label(
                tooltip,
                text=text,
                background="lightyellow",
                relief="solid",
                borderwidth=1,
                font=("Arial", 8),
            )
            label.pack()

            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, "tooltip"):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
