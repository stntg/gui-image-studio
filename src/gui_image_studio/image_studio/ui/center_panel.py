"""
Center panel UI setup for Image Studio.
Contains the drawing canvas and canvas controls.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class CenterPanel:
    """Manages the center panel UI with the drawing canvas."""

    def __init__(self, app: "EnhancedImageDesignerGUI"):
        self.app = app

    def setup(self, parent):
        """Setup the center panel with the drawing canvas."""
        # Canvas controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(controls_frame, text="Canvas:").pack(side=tk.LEFT)

        # Zoom controls
        zoom_frame = ttk.Frame(controls_frame)
        zoom_frame.pack(side=tk.RIGHT)

        tk.Button(
            zoom_frame,
            text="Zoom In",
            command=self.app.zoom_in,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            zoom_frame,
            text="Zoom Out",
            command=self.app.zoom_out,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            zoom_frame,
            text="Fit",
            command=self.app.zoom_fit,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT, padx=2)

        # Grid toggle
        self.app.grid_var = tk.BooleanVar()
        grid_check = ttk.Checkbutton(
            zoom_frame,
            text="Grid",
            variable=self.app.grid_var,
            command=self.app.toggle_grid,
        )
        grid_check.pack(side=tk.LEFT, padx=5)

        # Cursor settings button
        cursor_btn = tk.Button(
            zoom_frame,
            text="⚙️",
            command=self.app.open_cursor_settings,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=3,
        )
        cursor_btn.pack(side=tk.LEFT, padx=2)

        # Create canvas using canvas manager
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.app.canvas = self.app.canvas_manager.create_canvas(canvas_frame)
