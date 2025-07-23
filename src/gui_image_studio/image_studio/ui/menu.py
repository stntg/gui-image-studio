"""
Menu setup for Image Studio.
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class MenuManager:
    """Manages the application menu."""

    def __init__(self, app: "EnhancedImageDesignerGUI"):
        self.app = app

    def setup_menu(self) -> None:
        """Setup the menu bar."""
        menubar = tk.Menu(self.app.root)
        self.app.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="New Image", command=self.app.new_image, accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Load Image", command=self.app.load_image, accelerator="Ctrl+O"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Export Images", command=self.app.export_images)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", command=self.app.root.quit, accelerator="Ctrl+Q"
        )

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Canvas", command=self.app.clear_canvas)
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Toggle Grid", command=self.app.toggle_grid, accelerator="G"
        )

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(
            label="Zoom In", command=self.app.zoom_in, accelerator="+"
        )
        view_menu.add_command(
            label="Zoom Out", command=self.app.zoom_out, accelerator="-"
        )
        view_menu.add_command(
            label="Reset Zoom", command=self.app.reset_zoom, accelerator="0"
        )
        view_menu.add_separator()
        view_menu.add_command(label="Fit to Window", command=self.app.fit_to_window)

        # Panels menu (new for enhanced version)
        panels_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Panels", menu=panels_menu)
        panels_menu.add_command(
            label="Toggle Left Panel", command=self.app.toggle_left_panel
        )
        panels_menu.add_command(
            label="Toggle Right Panel", command=self.app.toggle_right_panel
        )
        panels_menu.add_separator()
        panels_menu.add_command(
            label="Reset Panel Layout", command=self.app.reset_panel_layout
        )

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(
            label="Cursor Settings...", command=self.app.open_cursor_settings
        )
        settings_menu.add_separator()
        settings_menu.add_command(
            label="Reset to Defaults", command=self.app.reset_cursor_settings
        )

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(
            label="Help Contents", command=self.app.show_help, accelerator="F1"
        )
        help_menu.add_command(
            label="Interactive Tutorial", command=self.app.start_tutorial
        )
        help_menu.add_separator()
        help_menu.add_command(
            label="Keyboard Shortcuts", command=self.app.show_shortcuts_help
        )
        help_menu.add_command(label="Tool Reference", command=self.app.show_tools_help)
        help_menu.add_separator()
        help_menu.add_command(
            label="Troubleshooting", command=self.app.show_troubleshooting_help
        )
        help_menu.add_command(
            label="Online Documentation", command=self.app.open_online_help
        )
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.app.show_about)
