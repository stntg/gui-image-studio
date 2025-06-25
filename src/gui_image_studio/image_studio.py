#!/usr/bin/env python3
"""
Enhanced Image Studio GUI for gui_image_studio package using threepanewindows.
A visual tool for developers to design images/icons and generate embedded code.
Features detachable left and right panels with fixed width.
FUNCTIONALITY IS IDENTICAL TO THE ORIGINAL - ONLY THE UI LAYOUT USES THREEPANEWINDOWS.
"""

import base64
import json
import os
import tempfile
import tkinter as tk
from io import BytesIO
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk
from typing import Dict, List, Optional, Tuple

import threepanewindows
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageTk

from .generator import embed_images_from_folder


class EnhancedImageDesignerGUI:
    """Main GUI application for image design and code generation."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI Image Studio - Enhanced")
        self.root.geometry("1200x700")
        self.root.minsize(800, 500)

        # Application state
        self.current_images: Dict[str, Image.Image] = {}
        self.image_previews: Dict[str, ImageTk.PhotoImage] = {}
        self.selected_image: Optional[str] = None
        self.temp_dir = tempfile.mkdtemp()

        # Design tools state
        self.current_tool = "brush"
        self.brush_size = 5
        self.brush_color = "#000000"
        self.canvas_size = (300, 300)
        self.zoom_level = 1.0
        self.show_grid = False
        self.drawing = False
        self.start_x = 0
        self.start_y = 0

        # Shape preview state
        self.preview_shape = None  # Canvas item ID for preview shape
        self.preview_active = False

        # Pixel highlight for precise drawing
        self.pixel_highlight = None  # Canvas item ID for pixel highlight
        self.last_highlight_pos = None  # Track last highlighted position

        # Cursor settings
        self.cursor_settings = {
            "handedness": "right",  # 'left' or 'right'
            "brush": "crosshair",
            "pencil": "crosshair",
            "eraser": "dotbox",
            "line": "crosshair",
            "rectangle": "crosshair",
            "circle": "crosshair",
            "text": "xterm",
            "fill": "spraycan",
            "custom_cursors": {},  # Store custom cursor data
        }

        # Load cursor settings from file if exists
        self.load_cursor_settings()

        self.setup_ui()
        self.setup_bindings()

        # Initialize default tool
        self.select_tool("brush")

        # Initialize UI state
        self.update_ui_state()
        self.update_canvas()  # Show initial instructions
        self.update_preview()  # Show initial preview

        # After creating self.root (or root), center the window on the desktop and ensure it's fully visible above the taskbar
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        # Reserve space for the Windows taskbar (typically ~40px, adjust if needed)
        TASKBAR_HEIGHT = 80
        if h > hs - TASKBAR_HEIGHT:
            h = hs - TASKBAR_HEIGHT

        x = max((ws // 2) - (w // 2), 0)
        y = max((hs - TASKBAR_HEIGHT) // 2 - (h // 2), 0)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        print(f"Window centered at {x}, {y} with size {w}x{h}")
        print(f"w width: {w}, height: {h}, screen width: {ws}, screen height: {hs}")

    def setup_button_styles(self):
        """Setup custom button styles for prominent display."""
        style = ttk.Style()

        # Create a prominent style for New button (green)
        style.configure(
            "ProminentNew.TButton",
            background="#4CAF50",  # Green background
            foreground="white",  # White text
            font=("Arial", 8, "bold"),
        )

        # Create a prominent style for Load button (blue)
        style.configure(
            "ProminentLoad.TButton",
            background="#2196F3",  # Blue background
            foreground="white",  # White text
            font=("Arial", 8, "bold"),
        )

        # Map hover states for better interaction
        style.map(
            "ProminentNew.TButton", background=[("active", "#45a049")]
        )  # Darker green on hover

        style.map(
            "ProminentLoad.TButton", background=[("active", "#1976D2")]
        )  # Darker blue on hover

    def setup_ui(self):
        """Setup the enhanced user interface with threepanewindows."""
        # Create menu bar first
        self.setup_menu()

        # Configure custom button styles for prominence
        self.setup_button_styles()

        # Configure pane configurations
        left_config = threepanewindows.PaneConfig(
            title="Tools & Images",
            icon="🛠️",
            min_width=200,
            max_width=200,
            default_width=200,
            fixed_width=200,
            resizable=False,
            detachable=True,
            closable=False,
        )

        center_config = threepanewindows.PaneConfig(
            title="Canvas", icon="🎨", resizable=True, detachable=False, closable=False
        )

        right_config = threepanewindows.PaneConfig(
            title="Properties & Code",
            icon="⚙️",
            min_width=200,
            max_width=200,
            default_width=200,
            fixed_width=200,
            resizable=False,
            detachable=True,
            closable=False,
        )

        # Create the enhanced three-pane window
        self.three_pane = threepanewindows.EnhancedDockableThreePaneWindow(
            master=self.root,
            left_config=left_config,
            center_config=center_config,
            right_config=right_config,
            left_builder=self.build_left_panel,
            center_builder=self.build_center_panel,
            right_builder=self.build_right_panel,
            theme_name="light",
            enable_animations=True,
            menu_bar=None,  # We'll handle menu separately
        )

        self.three_pane.pack(fill=tk.BOTH, expand=True)

        # Store references to the pane frames
        self.left_frame = self.three_pane.get_pane_frame("left")
        self.center_frame = self.three_pane.get_pane_frame("center")
        self.right_frame = self.three_pane.get_pane_frame("right")

    def build_left_panel(self, parent):
        """Build the left panel with tools and image management."""
        self.setup_left_panel(parent)

    def build_center_panel(self, parent):
        """Build the center panel with the drawing canvas."""
        self.setup_center_panel(parent)

    def build_right_panel(self, parent):
        """Build the right panel with properties and code generation."""
        self.setup_right_panel(parent)

    def setup_menu(self):
        """Setup the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="New Image", command=self.new_image, accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Load Image", command=self.load_image, accelerator="Ctrl+O"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Export Images", command=self.export_images)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", command=self.root.quit, accelerator="Ctrl+Q"
        )

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Canvas", command=self.clear_canvas)
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Toggle Grid", command=self.toggle_grid, accelerator="G"
        )

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="+")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="-")
        view_menu.add_command(
            label="Reset Zoom", command=self.reset_zoom, accelerator="0"
        )
        view_menu.add_separator()
        view_menu.add_command(label="Fit to Window", command=self.fit_to_window)

        # Panels menu (new for enhanced version)
        panels_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Panels", menu=panels_menu)
        panels_menu.add_command(
            label="Toggle Left Panel", command=self.toggle_left_panel
        )
        panels_menu.add_command(
            label="Toggle Right Panel", command=self.toggle_right_panel
        )
        panels_menu.add_separator()
        panels_menu.add_command(
            label="Reset Panel Layout", command=self.reset_panel_layout
        )

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(
            label="Cursor Settings...", command=self.open_cursor_settings
        )
        settings_menu.add_separator()
        settings_menu.add_command(
            label="Reset to Defaults", command=self.reset_cursor_settings
        )

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(
            label="Quick Start Guide", command=self.show_quick_start, accelerator="F1"
        )
        help_menu.add_command(label="Drawing Tools Help", command=self.show_tools_help)
        help_menu.add_command(label="Code Generation Help", command=self.show_code_help)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="Tips & Tricks", command=self.show_tips)
        help_menu.add_command(
            label="Troubleshooting", command=self.show_troubleshooting
        )
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)

        # Bind keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_image())
        self.root.bind("<Control-o>", lambda e: self.load_image())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<F1>", lambda e: self.show_quick_start())
        self.root.bind("<Key-g>", lambda e: self.toggle_grid())
        self.root.bind("<Key-plus>", lambda e: self.zoom_in())
        self.root.bind("<Key-minus>", lambda e: self.zoom_out())
        self.root.bind("<Key-0>", lambda e: self.reset_zoom())

    def setup_left_panel(self, parent):
        """Setup the left panel with tools and image management."""
        # Tools section - more compact
        tools_frame = ttk.LabelFrame(parent, text="Design Tools")
        tools_frame.pack(fill=tk.X, padx=3, pady=3)

        # Tool buttons - more compact with shorter labels
        tools_grid = ttk.Frame(tools_frame)
        tools_grid.pack(fill=tk.X, padx=3, pady=3)

        self.tool_buttons = {}
        tools = [
            ("brush", "🖌️ Brush"),
            ("pencil", "✏️ Pencil"),
            ("eraser", "🧽 Eraser"),
            ("line", "📏 Line"),
            ("rectangle", "⬜ Rect"),
            ("circle", "⭕ Circle"),
            ("text", "📝 Text"),
            ("fill", "🪣 Fill"),
        ]

        for i, (tool, label) in enumerate(tools):
            btn = tk.Button(
                tools_grid,
                text=label,
                command=lambda t=tool: self.select_tool(t),
                font=("Arial", 8),
                relief="raised",
                bd=1,
            )
            btn.grid(row=i // 2, column=i % 2, sticky="ew", padx=1, pady=1)
            self.tool_buttons[tool] = btn

        tools_grid.columnconfigure(0, weight=1)
        tools_grid.columnconfigure(1, weight=1)

        # Tool properties - more compact
        props_frame = ttk.LabelFrame(parent, text="Tool Properties")
        props_frame.pack(fill=tk.X, padx=3, pady=3)

        # Brush size - smaller font and padding
        ttk.Label(props_frame, text="Size:", font=("Arial", 8)).pack(
            anchor=tk.W, padx=3
        )
        self.size_var = tk.IntVar(value=5)
        size_scale = ttk.Scale(
            props_frame,
            from_=1,
            to=50,
            variable=self.size_var,
            orient=tk.HORIZONTAL,
            length=150,
        )
        size_scale.pack(fill=tk.X, padx=3, pady=1)

        # Color picker - more compact
        color_frame = ttk.Frame(props_frame)
        color_frame.pack(fill=tk.X, padx=3, pady=3)

        ttk.Label(color_frame, text="Color:", font=("Arial", 8)).pack(side=tk.LEFT)
        self.color_button = tk.Button(
            color_frame,
            bg=self.brush_color,
            width=4,
            height=1,
            command=self.choose_color,
        )
        self.color_button.pack(side=tk.RIGHT)

        # Image management section - more compact
        images_frame = ttk.LabelFrame(parent, text="Images")
        images_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # Image list - smaller font
        list_frame = ttk.Frame(images_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        self.image_listbox = tk.Listbox(list_frame, font=("Arial", 8))
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.image_listbox.yview
        )
        self.image_listbox.configure(yscrollcommand=scrollbar.set)

        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Image management buttons - more compact
        btn_frame = ttk.Frame(images_frame)
        btn_frame.pack(fill=tk.X, padx=3, pady=3)

        # Use grid for more compact button layout
        # Use tk.Button for better color control
        self.new_image_btn = tk.Button(
            btn_frame,
            text="🆕 New",
            command=self.new_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        )
        self.new_image_btn.grid(row=0, column=0, sticky="ew", padx=1, pady=1)

        self.load_image_btn = tk.Button(
            btn_frame,
            text="📁 Load",
            command=self.load_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        )
        self.load_image_btn.grid(row=0, column=1, sticky="ew", padx=1, pady=1)

        tk.Button(
            btn_frame,
            text="Copy",
            command=self.duplicate_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).grid(row=1, column=0, sticky="ew", padx=1, pady=1)
        tk.Button(
            btn_frame,
            text="Delete",
            command=self.delete_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).grid(row=1, column=1, sticky="ew", padx=1, pady=1)

        # Configure grid weights for buttons
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

    def setup_center_panel(self, parent):
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
            command=self.zoom_in,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            zoom_frame,
            text="Zoom Out",
            command=self.zoom_out,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            zoom_frame,
            text="Fit",
            command=self.zoom_fit,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT, padx=2)

        # Grid toggle
        self.grid_var = tk.BooleanVar()
        grid_check = ttk.Checkbutton(
            zoom_frame, text="Grid", variable=self.grid_var, command=self.toggle_grid
        )
        grid_check.pack(side=tk.LEFT, padx=5)

        # Cursor settings button
        cursor_btn = tk.Button(
            zoom_frame,
            text="⚙️",
            command=self.open_cursor_settings,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=3,
        )
        cursor_btn.pack(side=tk.LEFT, padx=2)

        # Canvas frame
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create canvas with scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg="white", scrollregion=(0, 0, 600, 450))

        h_scrollbar = ttk.Scrollbar(
            canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        v_scrollbar = ttk.Scrollbar(
            canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )

        self.canvas.configure(
            xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set
        )

        self.canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

    def setup_right_panel(self, parent):
        """Setup the right panel with properties and code generation."""
        # Image properties
        props_frame = ttk.LabelFrame(parent, text="Image Properties")
        props_frame.pack(fill=tk.X, padx=2, pady=2)

        # Image name
        ttk.Label(props_frame, text="Name:", font=("Arial", 8)).pack(
            anchor=tk.W, padx=3
        )
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(
            props_frame, textvariable=self.name_var, font=("Arial", 8)
        )
        name_entry.pack(fill=tk.X, padx=3, pady=1)
        name_entry.bind("<KeyRelease>", self.on_name_change)

        # Image size - more compact layout
        size_frame = ttk.Frame(props_frame)
        size_frame.pack(fill=tk.X, padx=3, pady=2)

        ttk.Label(size_frame, text="Size:", font=("Arial", 8)).grid(
            row=0, column=0, sticky="w"
        )
        self.width_var = tk.IntVar(value=300)
        self.height_var = tk.IntVar(value=300)

        # Smaller entry widgets
        ttk.Entry(
            size_frame, textvariable=self.width_var, width=4, font=("Arial", 8)
        ).grid(row=0, column=1, padx=1)
        ttk.Label(size_frame, text="x", font=("Arial", 8)).grid(row=0, column=2)
        ttk.Entry(
            size_frame, textvariable=self.height_var, width=4, font=("Arial", 8)
        ).grid(row=0, column=3, padx=1)
        tk.Button(
            size_frame,
            text="Apply",
            command=self.resize_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        ).grid(row=0, column=4, padx=2)

        # Configure grid weights for size frame
        size_frame.columnconfigure(4, weight=1)

        # Transformations - more compact
        transform_frame = ttk.LabelFrame(parent, text="Transformations")
        transform_frame.pack(fill=tk.X, padx=2, pady=2)

        # Rotation
        ttk.Label(transform_frame, text="Rotation:", font=("Arial", 8)).pack(
            anchor=tk.W, padx=3
        )
        self.rotation_var = tk.IntVar()
        rotation_scale = ttk.Scale(
            transform_frame,
            from_=0,
            to=360,
            variable=self.rotation_var,
            orient=tk.HORIZONTAL,
            command=self.apply_rotation,
        )
        rotation_scale.pack(fill=tk.X, padx=3, pady=2)

        # Also bind variable changes to rotation
        self.rotation_var.trace("w", self.apply_rotation)

        # Filters in a more compact grid layout
        filters_frame = ttk.Frame(transform_frame)
        filters_frame.pack(fill=tk.X, padx=3, pady=3)

        tk.Button(
            filters_frame,
            text="Blur",
            command=self.apply_blur,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        ).grid(row=0, column=0, padx=1, pady=1)
        tk.Button(
            filters_frame,
            text="Sharp",
            command=self.apply_sharpen,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        ).grid(row=0, column=1, padx=1, pady=1)
        tk.Button(
            filters_frame,
            text="Emboss",
            command=self.apply_emboss,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        ).grid(row=0, column=2, padx=1, pady=1)

        # Configure grid weights for filters
        filters_frame.columnconfigure(0, weight=1)
        filters_frame.columnconfigure(1, weight=1)
        filters_frame.columnconfigure(2, weight=1)

        # Code generation - more compact
        code_frame = ttk.LabelFrame(parent, text="Code Generation")
        code_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Generation options - more compact
        options_frame = ttk.Frame(code_frame)
        options_frame.pack(fill=tk.X, padx=2, pady=2)

        ttk.Label(options_frame, text="Framework:", font=("Arial", 8)).pack(anchor=tk.W)
        self.framework_var = tk.StringVar(value="tkinter")
        framework_combo = ttk.Combobox(
            options_frame,
            textvariable=self.framework_var,
            values=["tkinter", "customtkinter"],
            state="readonly",
            font=("Arial", 8),
            height=3,
        )
        framework_combo.pack(fill=tk.X, pady=1)

        ttk.Label(options_frame, text="Usage:", font=("Arial", 8)).pack(anchor=tk.W)
        self.usage_var = tk.StringVar(value="general")
        usage_combo = ttk.Combobox(
            options_frame,
            textvariable=self.usage_var,
            values=[
                "general",
                "buttons",
                "icons",
                "backgrounds",
                "sprites",
                "ui_elements",
            ],
            state="readonly",
            font=("Arial", 8),
            height=6,
        )
        usage_combo.pack(fill=tk.X, pady=1)

        ttk.Label(options_frame, text="Quality:", font=("Arial", 8)).pack(anchor=tk.W)
        self.quality_var = tk.IntVar(value=85)
        quality_scale = ttk.Scale(
            options_frame,
            from_=1,
            to=100,
            variable=self.quality_var,
            orient=tk.HORIZONTAL,
            length=150,
        )
        quality_scale.pack(fill=tk.X, pady=1)

        # Generation buttons - vertical layout for narrow panel
        btn_frame = ttk.Frame(code_frame)
        btn_frame.pack(fill=tk.X, padx=2, pady=2)

        tk.Button(
            btn_frame,
            text="Preview Code",
            command=self.preview_code,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(fill=tk.X, pady=1)
        tk.Button(
            btn_frame,
            text="Generate File",
            command=self.generate_code_file,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(fill=tk.X, pady=1)
        tk.Button(
            btn_frame,
            text="Export Images",
            command=self.export_images,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(fill=tk.X, pady=1)

        # Preview section - smaller height for narrow panel
        preview_frame = ttk.LabelFrame(code_frame, text="Live Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Preview canvas - smaller height
        self.preview_canvas = tk.Canvas(preview_frame, bg="white", height=100)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Bind framework/usage changes to update preview
        framework_combo.bind("<<ComboboxSelected>>", self.update_preview)
        usage_combo.bind("<<ComboboxSelected>>", self.update_preview)

    def setup_bindings(self):
        """Setup event bindings."""
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Motion>", self.on_canvas_motion)

        self.image_listbox.bind("<<ListboxSelect>>", self.on_image_select)

        # Keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_image())
        self.root.bind("<Control-o>", lambda e: self.load_image())
        self.root.bind("<Control-s>", lambda e: self.export_images())
        self.root.bind("<Delete>", lambda e: self.delete_image())

    def select_tool(self, tool):
        """Select a drawing tool."""
        # Clear any active preview when switching tools
        self.clear_preview()
        self.clear_pixel_highlight()
        self.drawing = False

        self.current_tool = tool

        # Update button states
        for t, btn in self.tool_buttons.items():
            if t == tool:
                btn.configure(
                    bg="#0078d4", fg="white", relief="sunken"
                )  # Selected state
            else:
                btn.configure(
                    bg="SystemButtonFace", fg="SystemButtonText", relief="raised"
                )  # Normal state

        # Update cursor with proper orientation
        self.update_tool_cursor(tool)

    def update_tool_cursor(self, tool):
        """Update the canvas cursor based on the selected tool and user settings."""
        # Get the user's preferred cursor for this tool
        preferred_cursor = self.cursor_settings.get(tool, "crosshair")

        # Check if it's a custom cursor
        if preferred_cursor.startswith("custom:"):
            cursor_name = preferred_cursor[7:]  # Remove 'custom:' prefix
            if cursor_name in self.cursor_settings["custom_cursors"]:
                cursor_data = self.cursor_settings["custom_cursors"][cursor_name]
                try:
                    self.canvas.configure(cursor=cursor_data)
                    return
                except tk.TclError:
                    pass  # Fall back to default options

        # Define fallback options for each tool based on platform and handedness
        fallback_options = self.get_cursor_fallback_options(tool)

        # Try the preferred cursor first, then fallbacks
        cursors_to_try = [preferred_cursor] + fallback_options

        # Remove duplicates while preserving order
        seen = set()
        cursors_to_try = [x for x in cursors_to_try if not (x in seen or seen.add(x))]

        # Try each cursor option until one works
        for cursor in cursors_to_try:
            try:
                self.canvas.configure(cursor=cursor)
                return  # Success, exit the method
            except tk.TclError:
                continue  # Try the next cursor

        # If all cursors fail, use arrow as final fallback
        try:
            self.canvas.configure(cursor="arrow")
        except tk.TclError:
            pass  # Give up if even arrow fails

    def get_cursor_fallback_options(self, tool):
        """Get fallback cursor options based on tool, platform, and handedness."""
        # Base options for each tool
        base_options = {
            "brush": ["crosshair", "pencil", "dotbox"],
            "pencil": ["crosshair", "pencil", "dotbox"],
            "eraser": ["dotbox", "crosshair"],
            "line": ["crosshair", "plus"],
            "rectangle": ["crosshair", "plus"],
            "circle": ["crosshair", "plus"],
            "text": ["xterm", "ibeam"],
            "fill": ["spraycan", "crosshair"],
        }

        options = base_options.get(tool, ["arrow"])

        # Adjust for handedness (left-handed users might prefer different orientations)
        if self.cursor_settings["handedness"] == "left":
            # Add left-handed friendly cursors
            left_handed_alternatives = {
                "pencil": ["ul_angle", "top_left_corner"],
                "brush": ["ul_angle", "top_left_corner"],
            }
            if tool in left_handed_alternatives:
                options = left_handed_alternatives[tool] + options

        return options

    def load_cursor_settings(self):
        """Load cursor settings from file."""
        try:
            import json
            import os

            settings_file = os.path.join(
                os.path.expanduser("~"), ".gui_image_studio_cursors.json"
            )
            if os.path.exists(settings_file):
                with open(settings_file, "r") as f:
                    saved_settings = json.load(f)
                    self.cursor_settings.update(saved_settings)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Warning: Could not load cursor settings: {e}. Using defaults.")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Warning: Invalid cursor settings file format: {e}. Using defaults.")
        except Exception as e:
            print(
                f"Warning: Unexpected error loading cursor settings: {e}. Using defaults."
            )

    def save_cursor_settings(self):
        """Save cursor settings to file."""
        try:
            import json
            import os

            settings_file = os.path.join(
                os.path.expanduser("~"), ".gui_image_studio_cursors.json"
            )
            with open(settings_file, "w") as f:
                json.dump(self.cursor_settings, f, indent=2)
        except (PermissionError, OSError) as e:
            print(f"Warning: Could not save cursor settings: {e}")
        except (TypeError, ValueError) as e:
            print(f"Warning: Invalid cursor settings data: {e}")
        except Exception as e:
            print(f"Warning: Unexpected error saving cursor settings: {e}")

    def reset_cursor_settings(self):
        """Reset cursor settings to defaults."""
        if tk.messagebox.askyesno(
            "Reset Cursor Settings",
            "Are you sure you want to reset all cursor settings to defaults?",
        ):
            self.cursor_settings = {
                "handedness": "right",
                "brush": "crosshair",
                "pencil": "crosshair",
                "eraser": "dotbox",
                "line": "crosshair",
                "rectangle": "crosshair",
                "circle": "crosshair",
                "text": "xterm",
                "fill": "spraycan",
                "custom_cursors": {},
            }
            self.save_cursor_settings()
            # Update current tool cursor
            self.update_tool_cursor(self.current_tool)
            tk.messagebox.showinfo(
                "Settings Reset", "Cursor settings have been reset to defaults."
            )

    def open_cursor_settings(self):
        """Open the cursor settings dialog."""
        CursorSettingsDialog(self.root, self)

    def choose_color(self):
        """Open color chooser dialog."""
        color = colorchooser.askcolor(color=self.brush_color)
        if color[1]:
            self.brush_color = color[1]
            self.color_button.configure(bg=self.brush_color)

    def new_image(self):
        """Create a new blank image."""
        dialog = ImageSizeDialog(self.root)
        if dialog.result:
            width, height, name = dialog.result

            # Create new PIL image
            image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

            # Generate unique name if needed
            if not name:
                name = f"image_{len(self.current_images) + 1}"
            elif name in self.current_images:
                counter = 1
                base_name = name
                while f"{base_name}_{counter}" in self.current_images:
                    counter += 1
                name = f"{base_name}_{counter}"

            self.current_images[name] = image
            self.update_image_list()
            self.select_image(name)

    def load_image(self):
        """Load an image from file."""
        file_path = filedialog.askopenfilename(
            title="Load Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            try:
                image = Image.open(file_path)
                # Convert to RGBA for consistency
                if image.mode != "RGBA":
                    image = image.convert("RGBA")

                # Get name from filename
                name = os.path.splitext(os.path.basename(file_path))[0]

                # Ensure unique name
                if name in self.current_images:
                    counter = 1
                    base_name = name
                    while f"{base_name}_{counter}" in self.current_images:
                        counter += 1
                    name = f"{base_name}_{counter}"

                self.current_images[name] = image
                self.update_image_list()
                self.select_image(name)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def duplicate_image(self):
        """Duplicate the selected image."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        original = self.current_images[self.selected_image]
        copy = original.copy()

        # Generate new name
        base_name = self.selected_image
        counter = 1
        new_name = f"{base_name}_copy"
        while new_name in self.current_images:
            counter += 1
            new_name = f"{base_name}_copy_{counter}"

        self.current_images[new_name] = copy
        self.update_image_list()
        self.select_image(new_name)

    def delete_image(self):
        """Delete the selected image."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        if messagebox.askyesno("Confirm", f"Delete image '{self.selected_image}'?"):
            del self.current_images[self.selected_image]
            if self.selected_image in self.image_previews:
                del self.image_previews[self.selected_image]

            self.selected_image = None
            self.update_image_list()
            self.canvas.delete("all")

    def update_image_list(self):
        """Update the image list display."""
        self.image_listbox.delete(0, tk.END)
        for name in sorted(self.current_images.keys()):
            self.image_listbox.insert(tk.END, name)
        self.update_ui_state()
        self.update_preview()

    def update_ui_state(self):
        """Update UI elements based on current state."""
        has_images = len(self.current_images) > 0

        if not has_images:
            # Make the buttons more prominent when no images exist
            self.new_image_btn.configure(
                text="🆕 New",
                bg="#4CAF50",  # Green background
                fg="white",  # White text
                font=("Arial", 8, "bold"),
                activebackground="#45a049",  # Darker green when pressed
                activeforeground="white",
            )
            self.load_image_btn.configure(
                text="📁 Load",
                bg="#2196F3",  # Blue background
                fg="white",  # White text
                font=("Arial", 8, "bold"),
                activebackground="#1976D2",  # Darker blue when pressed
                activeforeground="white",
            )
        else:
            # Normal button appearance when images exist - using consistent colors across platforms
            self.new_image_btn.configure(
                text="🆕 New",
                bg="#f0f0f0",  # Light gray background (consistent across platforms)
                fg="#000000",  # Black text
                font=("Arial", 8),
                activebackground="#e0e0e0",  # Slightly darker gray when pressed
                activeforeground="#000000",
            )
            self.load_image_btn.configure(
                text="📁 Load",
                bg="#f0f0f0",  # Light gray background (consistent across platforms)
                fg="#000000",  # Black text
                font=("Arial", 8),
                activebackground="#e0e0e0",  # Slightly darker gray when pressed
                activeforeground="#000000",
            )

    def update_preview(self, event=None):
        """Update the live preview based on current settings."""
        if not hasattr(self, "preview_canvas"):
            return

        # Clear previous preview
        self.preview_canvas.delete("all")

        if not self.current_images:
            # Show placeholder when no images
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()

            if canvas_width <= 1:
                # Canvas not ready, try again later
                self.root.after(100, self.update_preview)
                return

            center_x = canvas_width // 2
            center_y = canvas_height // 2

            self.preview_canvas.create_text(
                center_x,
                center_y,
                text="Create images to see preview",
                fill="#888888",
                font=("Arial", 9),
            )  # 12
            return

        # Get current settings
        framework = self.framework_var.get()
        usage_type = self.usage_var.get()

        # Generate preview based on framework and usage type
        self.generate_preview(framework, usage_type)

    def generate_preview(self, framework, usage_type):
        """Generate visual preview for the selected framework and usage type."""
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        if canvas_width <= 1:
            self.root.after(100, lambda: self.generate_preview(framework, usage_type))
            return

        # Convert first few images to PhotoImage for display
        preview_images = []
        count = 0
        max_images = 6  # Limit preview to 6 images

        for name, pil_image in self.current_images.items():
            if count >= max_images:
                break

            try:
                # Resize image for preview if too large
                display_image = pil_image.copy()
                if display_image.width > 64 or display_image.height > 64:
                    display_image.thumbnail((64, 64), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(display_image)
                preview_images.append((name, photo, display_image))
                count += 1
            except Exception as e:
                print(f"Error creating preview for {name}: {e}")
                continue

        if not preview_images:
            return

        # Generate preview based on usage type
        if usage_type == "buttons":
            self.preview_buttons(preview_images, framework)
        elif usage_type == "icons":
            self.preview_icons(preview_images, framework)
        elif usage_type == "backgrounds":
            self.preview_backgrounds(preview_images, framework)
        elif usage_type == "sprites":
            self.preview_sprites(preview_images, framework)
        elif usage_type == "ui_elements":
            self.preview_ui_elements(preview_images, framework)
        else:  # general
            self.preview_general(preview_images, framework)

    def preview_buttons(self, preview_images, framework):
        """Preview images as buttons."""
        self.preview_canvas.create_text(
            10,
            10,
            text=f"{framework.title()} Buttons:",
            anchor=tk.NW,
            font=("Arial", 10, "bold"),
        )

        x, y = 20, 30
        for name, photo, pil_image in preview_images:
            # Draw button-like rectangle
            btn_width = photo.width() + 60
            btn_height = photo.height() + 20

            if x + btn_width > self.preview_canvas.winfo_width() - 10:
                x = 20
                y += btn_height + 10

            # Button background
            self.preview_canvas.create_rectangle(
                x,
                y,
                x + btn_width,
                y + btn_height,
                fill="#e1e1e1",
                outline="#999999",
                width=2,
            )

            # Image
            img_x = x + 10
            img_y = y + (btn_height - photo.height()) // 2
            self.preview_canvas.create_image(img_x, img_y, image=photo, anchor=tk.NW)

            # Text
            text_x = img_x + photo.width() + 10
            text_y = y + btn_height // 2
            display_name = name.replace(".png", "").replace("_", " ").title()
            self.preview_canvas.create_text(
                text_x, text_y, text=display_name, anchor=tk.W, font=("Arial", 9)
            )

            # Keep reference to prevent garbage collection
            setattr(self.preview_canvas, f"preview_img_{name}", photo)

            x += btn_width + 10

    def preview_icons(self, preview_images, framework):
        """Preview images as icons."""
        self.preview_canvas.create_text(
            10,
            10,
            text=f"{framework.title()} Icons:",
            anchor=tk.NW,
            font=("Arial", 10, "bold"),
        )

        x, y = 20, 30
        cols = 0
        max_cols = 6

        for name, photo, pil_image in preview_images:
            if cols >= max_cols:
                cols = 0
                x = 20
                y += 80

            # Icon with label
            self.preview_canvas.create_image(x + 32, y + 16, image=photo)

            # Label below icon
            display_name = name.replace(".png", "").replace("_", " ")
            self.preview_canvas.create_text(
                x + 32, y + 50, text=display_name, anchor=tk.N, font=("Arial", 8)
            )

            setattr(self.preview_canvas, f"preview_img_{name}", photo)

            x += 70
            cols += 1

    def preview_backgrounds(self, preview_images, framework):
        """Preview images as backgrounds."""
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        # Ensure canvas is ready
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(
                50, lambda: self.preview_backgrounds(preview_images, framework)
            )
            return

        self.preview_canvas.create_text(
            10,
            10,
            text=f"{framework.title()} Backgrounds:",
            anchor=tk.NW,
            font=("Arial", 10, "bold"),
        )

        # Use first image as background
        if preview_images:
            name, photo, pil_image = preview_images[0]

            # Calculate available space
            available_width = canvas_width - 40
            available_height = canvas_height - 60

            if available_width > 50 and available_height > 50:
                # Create scaled background that fits nicely
                aspect_ratio = pil_image.width / pil_image.height

                if available_width / available_height > aspect_ratio:
                    # Height is limiting factor
                    new_height = min(available_height, 150)
                    new_width = int(new_height * aspect_ratio)
                else:
                    # Width is limiting factor
                    new_width = min(available_width, 250)
                    new_height = int(new_width / aspect_ratio)

                bg_image = pil_image.copy()
                bg_image = bg_image.resize(
                    (new_width, new_height), Image.Resampling.LANCZOS
                )
                bg_photo = ImageTk.PhotoImage(bg_image)

                # Center the background
                bg_x = (canvas_width - new_width) // 2
                bg_y = 30

                # Draw background
                self.preview_canvas.create_image(
                    bg_x, bg_y, image=bg_photo, anchor=tk.NW
                )

                # Overlay text with better positioning
                text_x = bg_x + new_width // 2
                text_y = bg_y + 20

                # Shadow effect
                self.preview_canvas.create_text(
                    text_x + 1,
                    text_y + 1,
                    text="Background Image",
                    fill="black",
                    font=("Arial", 12, "bold"),
                    anchor=tk.CENTER,
                )
                self.preview_canvas.create_text(
                    text_x,
                    text_y,
                    text="Background Image",
                    fill="white",
                    font=("Arial", 12, "bold"),
                    anchor=tk.CENTER,
                )

                setattr(self.preview_canvas, f"preview_bg_{name}", bg_photo)

    def preview_sprites(self, preview_images, framework):
        """Preview images as game sprites."""
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        # Ensure canvas is ready
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(50, lambda: self.preview_sprites(preview_images, framework))
            return

        self.preview_canvas.create_text(
            10,
            10,
            text=f"{framework.title()} Sprites:",
            anchor=tk.NW,
            font=("Arial", 10, "bold"),
        )

        # Simulate a game scene with proper bounds
        margin = 15
        scene_x = margin
        scene_y = 30
        scene_width = canvas_width - (2 * margin)
        scene_height = canvas_height - scene_y - margin

        if scene_width > 50 and scene_height > 50:
            # Draw scene background (sky)
            self.preview_canvas.create_rectangle(
                scene_x,
                scene_y,
                scene_x + scene_width,
                scene_y + scene_height,
                fill="#87CEEB",
                outline="#4682B4",
                width=1,
            )

            # Add ground (bottom 25% of scene)
            ground_height = max(20, scene_height // 4)
            ground_y = scene_y + scene_height - ground_height
            self.preview_canvas.create_rectangle(
                scene_x,
                ground_y,
                scene_x + scene_width,
                scene_y + scene_height,
                fill="#90EE90",
                outline="#228B22",
                width=1,
            )

            # Place sprites on the ground with proper spacing
            if preview_images:
                available_width = scene_width - 40  # Leave margins
                sprite_spacing = min(80, available_width // len(preview_images))
                sprite_x = scene_x + 20

                for name, photo, pil_image in preview_images:
                    if sprite_x + photo.width() > scene_x + scene_width - 20:
                        break  # Don't overflow scene

                    # Place sprite on ground
                    sprite_y = ground_y - photo.height()
                    if sprite_y < scene_y + 10:  # If sprite is too tall, place it lower
                        sprite_y = scene_y + 10

                    self.preview_canvas.create_image(
                        sprite_x, sprite_y, image=photo, anchor=tk.NW
                    )

                    setattr(self.preview_canvas, f"preview_sprite_{name}", photo)
                    sprite_x += max(photo.width() + 10, sprite_spacing)

    def preview_ui_elements(self, preview_images, framework):
        """Preview images as UI elements."""
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        # Ensure canvas is ready
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(
                50, lambda: self.preview_ui_elements(preview_images, framework)
            )
            return

        self.preview_canvas.create_text(
            10,
            10,
            text=f"{framework.title()} UI Elements:",
            anchor=tk.NW,
            font=("Arial", 10, "bold"),
        )

        # Create a mock UI layout with proper spacing
        margin = 15
        ui_x = margin
        ui_y = 30
        ui_width = canvas_width - (2 * margin)

        # Toolbar
        toolbar_height = 35
        if ui_width > 50:  # Only draw if there's enough space
            self.preview_canvas.create_rectangle(
                ui_x,
                ui_y,
                ui_x + ui_width,
                ui_y + toolbar_height,
                fill="#f0f0f0",
                outline="#cccccc",
                width=1,
            )

            # Place images as toolbar icons with proper spacing
            icon_x = ui_x + 8
            icon_spacing = min(50, ui_width // max(len(preview_images[:4]), 1))

            for i, (name, photo, pil_image) in enumerate(preview_images[:4]):
                if icon_x + photo.width() > ui_x + ui_width - 8:
                    break  # Don't overflow toolbar

                # Center icon vertically in toolbar
                icon_y = ui_y + (toolbar_height - photo.height()) // 2
                self.preview_canvas.create_image(
                    icon_x, icon_y, image=photo, anchor=tk.NW
                )

                setattr(self.preview_canvas, f"preview_ui_{name}", photo)
                icon_x += max(photo.width() + 8, icon_spacing)

            # Main content area
            content_y = ui_y + toolbar_height + 10
            content_height = max(60, canvas_height - content_y - 40)

            if content_height > 20:
                self.preview_canvas.create_rectangle(
                    ui_x,
                    content_y,
                    ui_x + ui_width,
                    content_y + content_height,
                    fill="#ffffff",
                    outline="#dddddd",
                    width=1,
                )

                # Add some content text
                self.preview_canvas.create_text(
                    ui_x + ui_width // 2,
                    content_y + content_height // 2,
                    text="Main Content Area",
                    fill="#666666",
                    font=("Arial", 10),
                    anchor=tk.CENTER,
                )

            # Status bar
            status_y = content_y + content_height + 5
            status_height = 22

            if status_y + status_height < canvas_height - 5:
                self.preview_canvas.create_rectangle(
                    ui_x,
                    status_y,
                    ui_x + ui_width,
                    status_y + status_height,
                    fill="#e8e8e8",
                    outline="#cccccc",
                    width=1,
                )

                # Status icon and text
                if len(preview_images) > 4:
                    name, photo, pil_image = preview_images[4]
                    # Scale status icon to fit
                    status_icon_size = min(16, photo.height(), status_height - 4)
                    if (
                        photo.height() > status_icon_size
                        or photo.width() > status_icon_size
                    ):
                        small_img = pil_image.copy()
                        small_img.thumbnail(
                            (status_icon_size, status_icon_size),
                            Image.Resampling.LANCZOS,
                        )
                        small_photo = ImageTk.PhotoImage(small_img)
                        self.preview_canvas.create_image(
                            ui_x + 4, status_y + 3, image=small_photo, anchor=tk.NW
                        )
                        setattr(
                            self.preview_canvas, f"preview_status_{name}", small_photo
                        )
                    else:
                        self.preview_canvas.create_image(
                            ui_x + 4, status_y + 3, image=photo, anchor=tk.NW
                        )
                        setattr(self.preview_canvas, f"preview_status_{name}", photo)

                # Status text
                self.preview_canvas.create_text(
                    ui_x + 30,
                    status_y + status_height // 2,
                    text="Ready",
                    fill="#333333",
                    font=("Arial", 9),
                    anchor=tk.W,
                )

    def preview_general(self, preview_images, framework):
        """Preview images in general layout."""
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        # Ensure canvas is ready
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(50, lambda: self.preview_general(preview_images, framework))
            return

        self.preview_canvas.create_text(
            10,
            10,
            text=f"{framework.title()} - General Usage:",
            anchor=tk.NW,
            font=("Arial", 10, "bold"),
        )

        # Dynamic grid layout based on canvas size
        margin = 20
        start_x = margin
        start_y = 35
        available_width = canvas_width - (2 * margin)

        # Calculate grid dimensions
        if preview_images:
            avg_width = sum(photo.width() for _, photo, _ in preview_images) // len(
                preview_images
            )
            max_cols = max(1, available_width // (avg_width + 25))
        else:
            max_cols = 4

        x, y = start_x, start_y
        col = 0
        row_height = 0

        for name, photo, pil_image in preview_images:
            # Check if we need to wrap to next row
            if col >= max_cols or (
                col > 0 and x + photo.width() + 25 > canvas_width - margin
            ):
                col = 0
                x = start_x
                y += row_height + 35  # Space for image + label + padding
                row_height = 0

            # Check if we have enough vertical space
            if y + photo.height() + 25 > canvas_height - 10:
                break  # Don't overflow canvas

            # Draw image with border
            self.preview_canvas.create_rectangle(
                x - 1,
                y - 1,
                x + photo.width() + 1,
                y + photo.height() + 1,
                outline="#cccccc",
                width=1,
            )
            self.preview_canvas.create_image(x, y, image=photo, anchor=tk.NW)

            # Label below image
            display_name = name.replace(".png", "").replace("_", " ")
            if len(display_name) > 12:  # Truncate long names
                display_name = display_name[:12] + "..."
            self.preview_canvas.create_text(
                x + photo.width() // 2,
                y + photo.height() + 8,
                text=display_name,
                anchor=tk.N,
                font=("Arial", 8),
            )

            setattr(self.preview_canvas, f"preview_general_{name}", photo)

            # Update position for next image
            x += photo.width() + 25
            row_height = max(row_height, photo.height())
            col += 1

    # Menu action methods
    def clear_canvas(self):
        """Clear the current canvas."""
        if self.selected_image and self.selected_image in self.current_images:
            # Create a new blank image with same dimensions
            current_img = self.current_images[self.selected_image]
            new_img = Image.new("RGBA", current_img.size, (255, 255, 255, 0))
            self.current_images[self.selected_image] = new_img
            self.update_canvas()
            self.update_preview()

    def zoom_in(self):
        """Zoom in on the canvas."""
        self.zoom_level = min(self.zoom_level * 1.2, 10.0)
        self.update_canvas()

    def zoom_out(self):
        """Zoom out on the canvas."""
        self.zoom_level = max(self.zoom_level / 1.2, 0.1)
        self.update_canvas()

    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.zoom_level = 1.0
        self.update_canvas()

    def fit_to_window(self):
        """Fit image to window size."""
        if self.selected_image and self.selected_image in self.current_images:
            img = self.current_images[self.selected_image]
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                zoom_x = (canvas_width - 40) / img.width
                zoom_y = (canvas_height - 40) / img.height
                self.zoom_level = min(zoom_x, zoom_y, 5.0)  # Cap at 5x
                self.update_canvas()

    # Help system methods
    def show_quick_start(self):
        """Show quick start guide."""
        HelpWindow(self.root, "Quick Start Guide", self.get_quick_start_content())

    def show_tools_help(self):
        """Show drawing tools help."""
        HelpWindow(self.root, "Drawing Tools Help", self.get_tools_help_content())

    def show_code_help(self):
        """Show code generation help."""
        HelpWindow(self.root, "Code Generation Help", self.get_code_help_content())

    def show_shortcuts(self):
        """Show keyboard shortcuts."""
        HelpWindow(self.root, "Keyboard Shortcuts", self.get_shortcuts_content())

    def show_tips(self):
        """Show tips and tricks."""
        HelpWindow(self.root, "Tips & Tricks", self.get_tips_content())

    def show_troubleshooting(self):
        """Show troubleshooting guide."""
        HelpWindow(self.root, "Troubleshooting", self.get_troubleshooting_content())

    def show_about(self):
        """Show about dialog."""
        HelpWindow(self.root, "About GUI Image Studio", self.get_about_content())

    def get_quick_start_content(self):
        """Get quick start guide content."""
        return """
🚀 QUICK START GUIDE

Welcome to GUI Image Studio! Here's how to get started:

1. CREATE YOUR FIRST IMAGE
   • Click "🆕 Create Your First Image!" button
   • Choose size (32x32 for icons, 64x64 for buttons)
   • Click OK to create a blank canvas

2. CHOOSE YOUR DRAWING TOOL
   • 🖌️ Brush: Freehand drawing
   • ✏️ Pencil: Pixel-perfect editing (best with Grid)
   • 🧽 Eraser: Remove pixels
   • Shapes: Line, Rectangle, Circle
   • T Text: Add text labels

3. START DRAWING
   • Left-click and drag to draw
   • Use the color picker to change colors
   • Enable Grid (checkbox) for pixel art
   • Zoom in/out with mouse wheel or +/- keys

4. PREVIEW YOUR WORK
   • Watch the Live Preview panel update automatically
   • Change Framework (tkinter/customtkinter)
   • Try different Usage Types (buttons, icons, etc.)

5. GENERATE CODE
   • Click "Preview Code" to see generated Python code
   • Click "Generate File" to save code to a .py file
   • Copy and paste into your Python project

🎯 PRO TIP: For pixel art, use Pencil tool + Grid + 400% zoom!

Need more help? Check the other help sections in the Help menu.
"""

    def get_tools_help_content(self):
        """Get drawing tools help content."""
        return """
🛠️ DRAWING TOOLS GUIDE

🖌️ BRUSH TOOL
• Purpose: Freehand drawing with smooth strokes
• Best for: Artistic drawing, organic shapes, sketching
• Usage: Left-click and drag to draw
• Tips: Great for filling large areas and general drawing

✏️ PENCIL TOOL
• Purpose: Pixel-perfect editing
• Best for: Pixel art, precise editing, detailed work
• Usage: Left-click to place single pixels, drag for lines
• Tips: Enable Grid and zoom in 4x+ for pixel art

🧽 ERASER TOOL
• Purpose: Remove pixels or make areas transparent
• Best for: Corrections, creating transparency
• Usage: Left-click and drag to erase
• Tips: Creates true transparency in PNG format

─ LINE TOOL
• Purpose: Draw straight lines
• Best for: Geometric shapes, borders, technical drawings
• Usage: Click and drag from start to end point
• Tips: Hold Shift for horizontal/vertical lines

▭ RECTANGLE TOOL
• Purpose: Draw rectangular shapes
• Best for: Buttons, frames, UI elements
• Usage: Click and drag to define rectangle
• Tips: Hold Shift for perfect squares

○ CIRCLE TOOL
• Purpose: Draw circular shapes
• Best for: Icons, decorative elements, buttons
• Usage: Click and drag to define circle
• Tips: Hold Shift for perfect circles

T TEXT TOOL
• Purpose: Add text to images
• Best for: Labels, icons with text, UI elements
• Usage: Click where you want text, type in dialog
• Tips: Text scales with zoom level for better visibility

🪣 FILL TOOL
• Purpose: Flood fill connected areas
• Best for: Filling large areas, coloring regions
• Usage: Click on area to fill
• Tips: Works great for coloring outlined shapes

🎨 COLOR PICKER
• Click the color square to choose colors
• Supports RGB and transparency
• Recent colors are remembered
"""

    def get_code_help_content(self):
        """Get code generation help content."""
        return """
💻 CODE GENERATION GUIDE

📋 OVERVIEW
GUI Image Studio generates Python code that embeds your images as base64 strings, eliminating the need for external image files.

🛠️ FRAMEWORKS SUPPORTED

TKINTER (Standard Python GUI)
• Uses PIL/Pillow and ImageTk.PhotoImage
• Compatible with all Python installations
• Best for: Desktop applications, simple GUIs

CUSTOMTKINTER (Modern Python GUI)
• Uses CTkImage for high-quality rendering
• Supports dark/light themes automatically
• Best for: Modern applications, professional UIs

🎯 USAGE TYPES

GENERAL
• Basic image loading functions
• Flexible for any use case
• Standard helper functions included

BUTTONS
• Specialized button creation functions
• Text + image combinations
• Ready-to-use button examples

ICONS
• Small, scalable graphics functions
• System integration ready
• Consistent sizing helpers

BACKGROUNDS
• Full-screen background support
• Tiled pattern functions
• Responsive scaling examples

SPRITES
• Game object graphics
• Animation frame support
• Performance optimized code

UI ELEMENTS
• Custom control creation
• Themed interface support
• Professional appearance helpers

⚙️ QUALITY SETTINGS
• 1-30: High compression, smaller files
• 31-70: Balanced compression and quality
• 71-85: Good quality, reasonable size (recommended)
• 86-100: Highest quality, larger files

📝 HOW TO USE GENERATED CODE
1. Copy the generated embedded_images dictionary
2. Copy the helper functions
3. Import required libraries (PIL, tkinter/customtkinter)
4. Use the provided examples as templates
5. Customize for your specific needs

💡 INTEGRATION TIPS
• Test generated code in your target framework
• Keep image names consistent for easy organization
• Use themes (filename prefixes) for organization
• Consider file size vs quality trade-offs
"""

    def get_shortcuts_content(self):
        """Get keyboard shortcuts content."""
        return """
⌨️ KEYBOARD SHORTCUTS

📁 FILE OPERATIONS
• Ctrl+N: Create new image
• Ctrl+O: Load existing image
• Ctrl+Q: Exit application

✏️ EDITING
• G: Toggle grid display
• Space: Pan canvas (when zoomed)

🔍 VIEW CONTROLS
• + (Plus): Zoom in
• - (Minus): Zoom out
• 0 (Zero): Reset zoom to 100%
• Mouse Wheel: Zoom in/out at cursor

🛠️ TOOL SELECTION
• B: Select Brush tool
• P: Select Pencil tool
• E: Select Eraser tool
• L: Select Line tool
• R: Select Rectangle tool
• C: Select Circle tool
• T: Select Text tool
• F: Select Fill tool

🎨 DRAWING
• Left Click: Draw/place pixel
• Left Click + Drag: Draw continuous stroke
• Right Click: Secondary action (context menu)
• Shift + Drag: Constrain to straight lines/perfect shapes

📋 INTERFACE
• F1: Show this help
• Tab: Cycle through panels
• Esc: Cancel current operation

🖱️ MOUSE CONTROLS
• Left Click: Primary drawing action
• Right Click: Context menu
• Middle Click: Pan canvas
• Scroll Wheel: Zoom in/out
• Ctrl + Scroll: Fine zoom control

💡 PRO TIPS
• Hold Shift while drawing shapes for perfect squares/circles
• Use Space to pan around when zoomed in
• Right-click on images in the list for more options
• Use G to quickly toggle grid for pixel art work
"""

    def get_tips_content(self):
        """Get tips and tricks content."""
        return """
💡 TIPS & TRICKS

🎨 DESIGN GUIDELINES

FOR ICONS (16x16 to 48x48)
• Keep designs simple and recognizable
• Use high contrast colors for visibility
• Avoid fine details that won't show at small sizes
• Test at actual size, not zoomed in
• Use consistent style across icon sets

FOR BUTTONS (64x64 and larger)
• Leave space for text if combining with labels
• Use consistent styling across button sets
• Consider hover/pressed state variations
• Make clickable areas visually clear
• Test with your application's color scheme

FOR PIXEL ART
• Use Pencil tool + Grid + high zoom (400%+)
• Start with basic shapes, add details later
• Use limited color palettes for authentic look
• Consider animation frames if creating sprites
• Save frequently to avoid losing work

🚀 WORKFLOW OPTIMIZATION

EFFICIENT CREATION PROCESS
1. Plan your design before starting
2. Start with basic shapes using shape tools
3. Add details with pencil tool
4. Use fill tool for large areas
5. Preview frequently in target context

ORGANIZATION TIPS
• Use consistent naming conventions
• Group related images by theme (dark_, light_, etc.)
• Keep backup copies of important images
• Test generated code early in development
• Document your color schemes and sizes

PERFORMANCE TIPS
• Use appropriate image sizes for purpose
• Optimize quality settings (70-85 recommended)
• Test loading performance in your app
• Consider using themes for different UI modes

🎯 ADVANCED TECHNIQUES

MULTI-THEME WORKFLOW
• Name files with theme prefixes: dark_icon.png, light_icon.png
• Generated code automatically organizes by theme
• Easy to switch themes in your application
• Consistent naming makes maintenance easier

PIXEL-PERFECT EDITING
• Enable Grid for precise pixel placement
• Zoom to 400% or higher for detail work
• Use Pencil tool for single-pixel accuracy
• Plan your pixel grid before starting

COLOR MANAGEMENT
• Use your app's color scheme consistently
• Test with colorblind-friendly palettes
• Consider dark/light theme variations
• Save color swatches for consistency

INTEGRATION BEST PRACTICES
• Generate code early to test integration
• Use meaningful variable names
• Keep image dimensions consistent within categories
• Document your image usage patterns

🔧 TROUBLESHOOTING QUICK FIXES

PERFORMANCE ISSUES
• Reduce zoom level if drawing is slow
• Close other applications to free memory
• Use smaller image sizes for better performance
• Restart application if it becomes unresponsive

VISUAL ISSUES
• Check image format (PNG for transparency)
• Verify colors are correct in target framework
• Test at actual usage size, not zoomed
• Ensure sufficient contrast for visibility

CODE INTEGRATION PROBLEMS
• Verify all required libraries are installed
• Check that image names don't conflict
• Test generated code in clean environment
• Ensure proper import statements are included
"""

    def get_troubleshooting_content(self):
        """Get troubleshooting content."""
        return """
🔧 TROUBLESHOOTING GUIDE

🚨 COMMON ISSUES & SOLUTIONS

APPLICATION WON'T START
Problem: Error when launching GUI Image Studio
Solutions:
• Check Python version: python --version (need 3.7+)
• Install dependencies: pip install pillow customtkinter
• Try direct launch: python src/gui_image_studio/image_studio.py
• Check for conflicting Python installations

IMAGES NOT DISPLAYING
Problem: Loaded images don't appear or show as broken
Solutions:
• Verify image format is supported (PNG, JPG, BMP, GIF, TIFF, WebP)
• Check if image file is corrupted (try opening in other programs)
• Ensure image isn't too large (max recommended: 1024x1024)
• Try creating a new image instead of loading

DRAWING TOOLS NOT WORKING
Problem: Tools don't draw or behave unexpectedly
Solutions:
• Check if an image is selected in the image list
• Verify canvas is focused (click on it first)
• Try switching tools and switching back
• Restart application if tools are unresponsive

CODE GENERATION FAILS
Problem: "Preview Code" or "Generate File" doesn't work
Solutions:
• Ensure at least one image is created
• Check that framework is properly selected
• Verify output directory is writable
• Try generating with different quality settings

PREVIEW NOT UPDATING
Problem: Live preview doesn't show changes
Solutions:
• Try changing framework/usage type to refresh
• Check that images are properly loaded in the list
• Resize the window to refresh preview canvas
• Restart application if preview is stuck

⚡ PERFORMANCE ISSUES

SLOW DRAWING RESPONSE
Problem: Drawing feels laggy or unresponsive
Solutions:
• Reduce zoom level if very high (try 100-200%)
• Close other memory-intensive applications
• Use smaller image sizes (under 512x512)
• Restart the application to clear memory

LARGE FILE SIZES
Problem: Generated code files are too large
Solutions:
• Reduce quality setting (try 70-85)
• Use PNG only when transparency is needed
• Use JPEG for photographic content
• Consider smaller image dimensions

APPLICATION CRASHES
Problem: Application closes unexpectedly
Solutions:
• Check available system memory
• Avoid extremely large images (>2048x2048)
• Save work frequently
• Update Python and dependencies

🔍 ERROR MESSAGES

"Canvas not ready"
• Wait a moment and try the operation again
• Resize the window to refresh canvas
• Check if image is properly selected
• Restart application if persistent

"Failed to generate code"
• Verify at least one image exists
• Check output directory permissions
• Try a different output location
• Ensure disk space is available

"Image format not supported"
• Convert image to PNG, JPG, or BMP format
• Check if file is corrupted
• Try loading a different image
• Use image editing software to re-save

"Memory error"
• Close other applications
• Use smaller image sizes
• Restart the application
• Check available system RAM

🛠️ ADVANCED TROUBLESHOOTING

DEPENDENCY ISSUES
Check installed packages:
```
pip list | grep -i pillow
pip list | grep -i customtkinter
```

Reinstall if needed:
```
pip uninstall pillow customtkinter
pip install pillow customtkinter
```

PYTHON PATH ISSUES
If imports fail, try:
```
export PYTHONPATH="${PYTHONPATH}:/path/to/gui-image-studio/src"
```

PERMISSION ISSUES
On Windows, run as administrator if file operations fail
On Linux/Mac, check file permissions: chmod 755

🆘 GETTING HELP

If problems persist:
1. Note the exact error message
2. Record steps to reproduce the issue
3. Check Python and dependency versions
4. Try with a fresh Python environment
5. Report bugs with detailed information

💡 PREVENTION TIPS
• Save work frequently
• Keep backups of important images
• Test generated code in clean environment
• Update dependencies regularly
• Use stable Python versions (3.8-3.11 recommended)
"""

    def get_about_content(self):
        """Get about dialog content."""
        return """
🎨 GUI IMAGE STUDIO

Version: 1.0.0
A comprehensive toolkit for creating and embedding images in Python GUI applications.

📋 FEATURES
• Visual image editor with professional drawing tools
• Support for tkinter and customtkinter frameworks
• Live preview of images in different usage contexts
• Automatic Python code generation with examples
• Base64 embedding for distribution without external files
• Multi-theme organization and management

🛠️ BUILT WITH
• Python 3.7+
• Tkinter (GUI framework)
• PIL/Pillow (image processing)
• CustomTkinter (modern UI components)

👥 DEVELOPED BY
The GUI Image Studio development team

📄 LICENSE
Open source - check LICENSE file for details

🌐 RESOURCES
• User Guide: USER_GUIDE.md
• Usage Examples: IMAGE_USAGE_GUIDE.md
• Source Code: Available in project repository

🎯 PURPOSE
GUI Image Studio was created to simplify the process of creating and integrating custom graphics into Python GUI applications. Whether you're building desktop apps, games, or professional software, this tool helps you create pixel-perfect graphics and seamlessly integrate them into your projects.

💡 PHILOSOPHY
We believe that great software deserves great graphics. GUI Image Studio makes it easy for developers to create professional-looking applications without needing separate image editing software or dealing with external file dependencies.

🚀 GET STARTED
Press F1 or check the Help menu for guides and tutorials.

Happy creating! 🎉
"""

    def select_image(self, name):
        """Select an image for editing."""
        if name not in self.current_images:
            return

        self.selected_image = name
        self.name_var.set(name)

        # Update listbox selection
        items = list(self.image_listbox.get(0, tk.END))
        if name in items:
            index = items.index(name)
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(index)

        # Auto-zoom for small images
        image = self.current_images[name]
        if image.width < 300 and image.height < 300:
            # Calculate zoom to make image at least 300px on the larger dimension
            max_dim = max(image.width, image.height)
            self.zoom_level = max(1.5, 300 / max_dim)
        else:
            self.zoom_level = 1.0

        # Update canvas and preview
        self.update_canvas()
        self.update_preview()

        # Update properties
        self.width_var.set(image.width)
        self.height_var.set(image.height)

    def update_canvas(self):
        """Update the canvas display."""
        # Clear any active preview shapes and pixel highlights
        self.clear_preview()
        self.clear_pixel_highlight()

        if not self.selected_image:
            # Clear canvas and show instructions
            self.canvas.delete("all")
            self.show_canvas_instructions()
            return

        image = self.current_images[self.selected_image]

        # Create display image with zoom
        display_size = (
            int(image.width * self.zoom_level),
            int(image.height * self.zoom_level),
        )
        display_image = image.resize(display_size, Image.NEAREST)

        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(display_image)
        self.image_previews[self.selected_image] = photo

        # Clear and update canvas
        self.canvas.delete("all")
        self.canvas.create_image(10, 10, anchor=tk.NW, image=photo)

        # Draw grid if enabled
        if self.show_grid and self.zoom_level >= 4:
            self.draw_grid(display_size)

        # Update scroll region
        self.canvas.configure(
            scrollregion=(0, 0, display_size[0] + 20, display_size[1] + 20)
        )

        # Update preview when canvas changes
        if hasattr(self, "preview_canvas"):
            self.root.after_idle(self.update_preview)

    def show_canvas_instructions(self):
        """Show instructions on empty canvas."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not yet initialized, schedule for later
            self.root.after(100, self.show_canvas_instructions)
            return

        center_x = canvas_width // 2
        center_y = canvas_height // 2

        # Add background rectangle first (so it's behind the text)
        self.canvas.create_rectangle(
            center_x - 200,
            center_y - 100,
            center_x + 200,
            center_y + 100,
            outline="#cccccc",
            width=2,
            fill="#f9f9f9",
            tags="instructions",
        )

        # Main instruction text
        self.canvas.create_text(
            center_x,
            center_y - 70,
            text="🎨 Welcome to GUI Image Studio!",
            font=("Arial", 16, "bold"),
            fill="#333333",
            tags="instructions",
        )

        self.canvas.create_text(
            center_x,
            center_y - 30,
            text="To start drawing, you need to:",
            font=("Arial", 12),
            fill="#666666",
            tags="instructions",
        )

        self.canvas.create_text(
            center_x,
            center_y,
            text="• Click 'New' to make a new canvas",
            font=("Arial", 11),
            fill="#666666",
            tags="instructions",
        )

        self.canvas.create_text(
            center_x,
            center_y + 20,
            text="• Click 'Load' to open an existing file",
            font=("Arial", 11),
            fill="#666666",
            tags="instructions",
        )

        self.canvas.create_text(
            center_x,
            center_y + 50,
            text="Then select a tool and start creating!",
            font=("Arial", 11, "italic"),
            fill="#0066cc",
            tags="instructions",
        )

        self.canvas.create_text(
            center_x,
            center_y + 80,
            text="💡 Tip: Use the Pencil tool with Grid for pixel art!",
            font=("Arial", 10),
            fill="#888888",
            tags="instructions",
        )

    def on_image_select(self, event):
        """Handle image selection from listbox."""
        selection = self.image_listbox.curselection()
        if selection:
            name = self.image_listbox.get(selection[0])
            self.select_image(name)

    def on_name_change(self, event):
        """Handle image name change."""
        if not self.selected_image:
            return

        new_name = self.name_var.get().strip()
        if not new_name or new_name == self.selected_image:
            return

        if new_name in self.current_images:
            messagebox.showwarning("Warning", "Name already exists")
            self.name_var.set(self.selected_image)
            return

        # Rename image
        image = self.current_images[self.selected_image]
        del self.current_images[self.selected_image]
        self.current_images[new_name] = image

        old_name = self.selected_image
        self.selected_image = new_name

        # Update preview if exists
        if old_name in self.image_previews:
            self.image_previews[new_name] = self.image_previews[old_name]
            del self.image_previews[old_name]

        self.update_image_list()
        self.select_image(new_name)

    def on_canvas_click(self, event):
        """Handle canvas click events."""
        if not self.selected_image:
            return

        # Convert canvas coordinates to image coordinates
        x = int((self.canvas.canvasx(event.x) - 10) / self.zoom_level)
        y = int((self.canvas.canvasy(event.y) - 10) / self.zoom_level)

        if self.current_tool in ["brush", "pencil", "eraser", "fill"]:
            self.last_x, self.last_y = x, y
            self.draw_on_image(x, y)
        elif self.current_tool in ["line", "rectangle", "circle"]:
            self.drawing = True
            self.start_x, self.start_y = x, y

        elif self.current_tool == "text":
            self.add_text(x, y)

    def on_canvas_drag(self, event):
        """Handle canvas drag events."""
        if not self.selected_image:
            return

        # Convert canvas coordinates to image coordinates
        x = int((self.canvas.canvasx(event.x) - 10) / self.zoom_level)
        y = int((self.canvas.canvasy(event.y) - 10) / self.zoom_level)

        if self.current_tool in ["brush", "pencil", "eraser"]:
            if hasattr(self, "last_x") and hasattr(self, "last_y"):
                self.draw_line_on_image(self.last_x, self.last_y, x, y)
            self.last_x, self.last_y = x, y
        elif self.drawing and self.current_tool in ["rectangle", "circle", "line"]:
            # Show preview while dragging
            self.update_shape_preview(self.start_x, self.start_y, x, y)

    def on_canvas_release(self, event):
        """Handle canvas release events."""
        if not self.selected_image:
            return

        if self.drawing and self.current_tool in ["line", "rectangle", "circle"]:
            # Convert canvas coordinates to image coordinates
            x = int((self.canvas.canvasx(event.x) - 10) / self.zoom_level)
            y = int((self.canvas.canvasy(event.y) - 10) / self.zoom_level)

            self.draw_shape(self.start_x, self.start_y, x, y)
            self.drawing = False
            self.clear_preview()

    def on_canvas_motion(self, event):
        """Handle canvas motion events for shape preview and pixel highlighting."""
        if not self.selected_image:
            return

        # Convert canvas coordinates to image coordinates
        x = int((self.canvas.canvasx(event.x) - 10) / self.zoom_level)
        y = int((self.canvas.canvasy(event.y) - 10) / self.zoom_level)

        # Show pixel highlight for drawing tools when grid is enabled
        if (
            self.show_grid
            and self.current_tool in ["brush", "pencil", "eraser"]
            and self.zoom_level >= 4
        ):
            self.update_pixel_highlight(x, y)
        else:
            self.clear_pixel_highlight()

        # Show shape preview for shape tools when drawing
        if self.drawing and self.current_tool in ["rectangle", "circle", "line"]:
            self.update_shape_preview(self.start_x, self.start_y, x, y)

    def update_shape_preview(self, x1, y1, x2, y2):
        """Update the preview shape on canvas."""
        # Clear existing preview
        self.clear_preview()

        # Convert image coordinates back to canvas coordinates for display
        canvas_x1 = x1 * self.zoom_level + 10
        canvas_y1 = y1 * self.zoom_level + 10
        canvas_x2 = x2 * self.zoom_level + 10
        canvas_y2 = y2 * self.zoom_level + 10

        # Create preview shape based on current tool
        if self.current_tool == "rectangle":
            self.preview_shape = self.canvas.create_rectangle(
                canvas_x1,
                canvas_y1,
                canvas_x2,
                canvas_y2,
                outline=self.brush_color,
                width=2,
                fill="",
                dash=(5, 5),
                tags="preview",
            )
        elif self.current_tool == "circle":
            self.preview_shape = self.canvas.create_oval(
                canvas_x1,
                canvas_y1,
                canvas_x2,
                canvas_y2,
                outline=self.brush_color,
                width=2,
                fill="",
                dash=(5, 5),
                tags="preview",
            )
        elif self.current_tool == "line":
            self.preview_shape = self.canvas.create_line(
                canvas_x1,
                canvas_y1,
                canvas_x2,
                canvas_y2,
                fill=self.brush_color,
                width=2,
                dash=(5, 5),
                tags="preview",
            )

        self.preview_active = True

    def clear_preview(self):
        """Clear the preview shape from canvas."""
        if self.preview_shape:
            self.canvas.delete(self.preview_shape)
            self.preview_shape = None
        self.preview_active = False

    def update_pixel_highlight(self, x, y):
        """Highlight the pixel that will be affected by drawing tools."""
        # Only highlight if position changed
        if self.last_highlight_pos == (x, y):
            return

        self.last_highlight_pos = (x, y)

        # Clear existing highlight
        self.clear_pixel_highlight()

        # Check if coordinates are within image bounds
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        if x < 0 or y < 0 or x >= image.width or y >= image.height:
            return

        # Convert image coordinates to canvas coordinates
        canvas_x = x * self.zoom_level + 10
        canvas_y = y * self.zoom_level + 10

        # Create highlight rectangle around the pixel
        self.pixel_highlight = self.canvas.create_rectangle(
            canvas_x,
            canvas_y,
            canvas_x + self.zoom_level,
            canvas_y + self.zoom_level,
            outline="#FF0000",
            width=1,
            fill="",
            dash=(2, 2),
            tags="pixel_highlight",
        )

    def clear_pixel_highlight(self):
        """Clear the pixel highlight from canvas."""
        if self.pixel_highlight:
            self.canvas.delete(self.pixel_highlight)
            self.pixel_highlight = None
        self.last_highlight_pos = None

    def draw_on_image(self, x, y):
        """Draw on the current image."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        draw = ImageDraw.Draw(image)

        size = self.size_var.get()

        if self.current_tool == "brush":
            # Draw circle
            draw.ellipse(
                [x - size // 2, y - size // 2, x + size // 2, y + size // 2],
                fill=self.brush_color,
            )
        elif self.current_tool == "pencil":
            # Draw single pixel or small square for pixel-perfect editing
            if self.show_grid and self.zoom_level >= 4:
                # Pixel-perfect mode - draw single pixel
                draw.point((x, y), fill=self.brush_color)
            else:
                # Normal pencil mode - small circle
                pencil_size = max(1, size // 2)
                draw.ellipse(
                    [
                        x - pencil_size // 2,
                        y - pencil_size // 2,
                        x + pencil_size // 2,
                        y + pencil_size // 2,
                    ],
                    fill=self.brush_color,
                )
        elif self.current_tool == "eraser":
            # Erase (draw transparent)
            draw.ellipse(
                [x - size // 2, y - size // 2, x + size // 2, y + size // 2],
                fill=(0, 0, 0, 0),
            )
        elif self.current_tool == "fill":
            # Flood fill
            try:
                # Convert hex color to RGB
                color = tuple(int(self.brush_color[i : i + 2], 16) for i in (1, 3, 5))
                color = color + (255,)  # Add alpha
                ImageDraw.floodfill(image, (x, y), color)
            except (ValueError, IndexError) as e:
                # Invalid color format or coordinates out of bounds
                print(f"Warning: Flood fill failed: {e}")
            except Exception as e:
                # Other flood fill errors (e.g., same color fill)
                print(f"Warning: Flood fill operation failed: {e}")

        self.update_canvas()

    def draw_shape(self, x1, y1, x2, y2):
        """Draw a shape on the current image."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        draw = ImageDraw.Draw(image)

        size = self.size_var.get()
        color = self.brush_color

        if self.current_tool == "line":
            draw.line([x1, y1, x2, y2], fill=color, width=size)
        elif self.current_tool == "rectangle":
            # Ensure proper rectangle coordinates
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)
            draw.rectangle([left, top, right, bottom], outline=color, width=size)
        elif self.current_tool == "circle":
            # Calculate circle bounds
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)
            draw.ellipse([left, top, right, bottom], outline=color, width=size)

        self.update_canvas()

    def add_text(self, x, y):
        """Add text to the current image."""
        if not self.selected_image:
            return

        # Simple text input dialog
        text = simpledialog.askstring("Add Text", "Enter text:")
        if text:
            image = self.current_images[self.selected_image]
            draw = ImageDraw.Draw(image)

            try:
                # Try to use a default font with size based on brush size
                font_size = max(12, self.size_var.get() * 2)
                font = ImageFont.load_default()
            except (OSError, IOError, ImportError) as e:
                # Font loading failed, use None (PIL will use built-in font)
                print(f"Warning: Could not load default font: {e}")
                font = None

            draw.text((x, y), text, fill=self.brush_color, font=font)
            self.update_canvas()

    def draw_line_on_image(self, x1, y1, x2, y2):
        """Draw a line on the current image."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        draw = ImageDraw.Draw(image)

        size = self.size_var.get()

        if self.current_tool == "brush":
            draw.line([x1, y1, x2, y2], fill=self.brush_color, width=size)
        elif self.current_tool == "pencil":
            # Pencil draws thin lines, pixel-perfect when grid is on
            if self.show_grid and self.zoom_level >= 4:
                draw.line([x1, y1, x2, y2], fill=self.brush_color, width=1)
            else:
                pencil_size = max(1, size // 2)
                draw.line([x1, y1, x2, y2], fill=self.brush_color, width=pencil_size)
        elif self.current_tool == "eraser":
            draw.line([x1, y1, x2, y2], fill=(0, 0, 0, 0), width=size)

        self.update_canvas()

    def resize_image(self):
        """Resize the current image."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        width = self.width_var.get()
        height = self.height_var.get()

        if width <= 0 or height <= 0:
            messagebox.showerror("Error", "Invalid size")
            return

        image = self.current_images[self.selected_image]
        resized = image.resize((width, height), Image.LANCZOS)
        self.current_images[self.selected_image] = resized

        self.update_canvas()

    def zoom_in(self):
        """Zoom in on the canvas."""
        self.zoom_level = min(self.zoom_level * 1.5, 10.0)
        self.update_canvas()

    def zoom_out(self):
        """Zoom out on the canvas."""
        self.zoom_level = max(self.zoom_level / 1.5, 0.1)
        self.update_canvas()

    def zoom_fit(self):
        """Fit image to canvas."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        canvas_width = self.canvas.winfo_width() - 20
        canvas_height = self.canvas.winfo_height() - 20

        if canvas_width > 0 and canvas_height > 0:
            zoom_x = canvas_width / image.width
            zoom_y = canvas_height / image.height
            self.zoom_level = min(zoom_x, zoom_y, 1.0)
            self.update_canvas()

    def toggle_grid(self):
        """Toggle grid display."""
        self.show_grid = self.grid_var.get()
        self.update_canvas()

    def draw_grid(self, display_size):
        """Draw grid on canvas."""
        # Only show grid when zoomed in enough
        if self.zoom_level < 4:
            return

        width, height = display_size
        grid_spacing = int(
            self.zoom_level
        )  # Each pixel becomes this many screen pixels

        # Draw vertical lines (every pixel boundary)
        for x in range(0, width + 1, grid_spacing):
            self.canvas.create_line(
                x + 10, 10, x + 10, height + 10, fill="#888888", width=1, tags="grid"
            )

        # Draw horizontal lines (every pixel boundary)
        for y in range(0, height + 1, grid_spacing):
            self.canvas.create_line(
                10, y + 10, width + 10, y + 10, fill="#888888", width=1, tags="grid"
            )

    def apply_blur(self):
        """Apply blur filter to current image."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        blurred = image.filter(ImageFilter.BLUR)
        self.current_images[self.selected_image] = blurred
        self.update_canvas()

    def apply_sharpen(self):
        """Apply sharpen filter to current image."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        sharpened = image.filter(ImageFilter.SHARPEN)
        self.current_images[self.selected_image] = sharpened
        self.update_canvas()

    def apply_emboss(self):
        """Apply emboss filter to current image."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        embossed = image.filter(ImageFilter.EMBOSS)
        self.current_images[self.selected_image] = embossed
        self.update_canvas()

    def apply_rotation(self, *args):
        """Apply rotation to current image based on rotation scale."""
        if not self.selected_image:
            return

        angle = self.rotation_var.get()
        if angle == 0:
            return  # No rotation needed

        image = self.current_images[self.selected_image]
        # Rotate the image (PIL rotates counter-clockwise)
        rotated = image.rotate(angle, expand=True, fillcolor=(255, 255, 255, 0))
        self.current_images[self.selected_image] = rotated
        self.update_canvas()

    def preview_code(self):
        """Preview the generated embedded code."""
        if not self.current_images:
            messagebox.showwarning("Warning", "No images to generate code for")
            return

        # Save images to temp directory
        temp_images_dir = os.path.join(self.temp_dir, "preview_images")
        os.makedirs(temp_images_dir, exist_ok=True)

        for name, image in self.current_images.items():
            # Convert RGBA to RGB if needed for JPEG
            if image.mode == "RGBA":
                # Create white background

                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(
                    image, mask=image.split()[-1]
                )  # Use alpha channel as mask
                save_image = background
            else:
                save_image = image

            image_path = os.path.join(temp_images_dir, f"{name}.png")
            image.save(image_path, "PNG")

        # Generate embedded code
        temp_output = os.path.join(self.temp_dir, "preview_embedded.py")
        embed_images_from_folder(temp_images_dir, temp_output, self.quality_var.get())

        # Read and display the generated code
        try:
            with open(temp_output, "r") as f:
                code_content = f.read()

            # Show code preview window
            CodePreviewWindow(
                self.root, code_content, self.framework_var.get(), self.usage_var.get()
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code preview: {str(e)}")

    def generate_code_file(self):
        """Generate the embedded code file."""
        if not self.current_images:
            messagebox.showwarning("Warning", "No images to generate code for")
            return

        # Ask for output file
        output_file = filedialog.asksaveasfilename(
            title="Save Embedded Code",
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )

        if not output_file:
            return

        try:
            # Save images to temp directory
            temp_images_dir = os.path.join(self.temp_dir, "export_images")
            os.makedirs(temp_images_dir, exist_ok=True)

            for name, image in self.current_images.items():
                image_path = os.path.join(temp_images_dir, f"{name}.png")
                image.save(image_path, "PNG")

            # Generate embedded code
            embed_images_from_folder(
                temp_images_dir, output_file, self.quality_var.get()
            )

            messagebox.showinfo("Success", f"Embedded code generated: {output_file}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code file: {str(e)}")

    def export_images(self):
        """Export images to a folder."""
        if not self.current_images:
            messagebox.showwarning("Warning", "No images to export")
            return

        # Ask for output directory
        output_dir = filedialog.askdirectory(title="Select Export Directory")
        if not output_dir:
            return

        try:
            for name, image in self.current_images.items():
                image_path = os.path.join(output_dir, f"{name}.png")
                image.save(image_path, "PNG")

            messagebox.showinfo("Success", f"Images exported to: {output_dir}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export images: {str(e)}")

    def toggle_left_panel(self):
        """Toggle left panel visibility."""
        if hasattr(self, "three_pane"):
            self.three_pane.toggle_pane("left")

    def toggle_right_panel(self):
        """Toggle right panel visibility."""
        if hasattr(self, "three_pane"):
            self.three_pane.toggle_pane("right")

    def reset_panel_layout(self):
        """Reset panel layout to default."""
        if hasattr(self, "three_pane"):
            self.three_pane.reset_layout()

    def run(self):
        """Run the application."""
        self.root.mainloop()

        # Cleanup temp directory
        import shutil

        try:
            shutil.rmtree(self.temp_dir)
        except (OSError, FileNotFoundError) as e:
            # Temp directory cleanup failed, but this is not critical
            print(f"Warning: Could not clean up temp directory {self.temp_dir}: {e}")


class ImageSizeDialog:
    """Dialog for creating new images with custom size."""

    def __init__(self, parent):
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Image")
        self.dialog.geometry("300x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry(
            "+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50)
        )

        self.setup_ui()

        # Wait for dialog to complete
        self.dialog.wait_window()

    def setup_ui(self):
        """Setup the dialog UI."""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Name
        ttk.Label(main_frame, text="Name:").pack(anchor=tk.W)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var).pack(fill=tk.X, pady=(0, 10))

        # Size
        size_frame = ttk.Frame(main_frame)
        size_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(size_frame, text="Width:").pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=300)
        ttk.Entry(size_frame, textvariable=self.width_var, width=8).pack(
            side=tk.LEFT, padx=(5, 10)
        )

        ttk.Label(size_frame, text="Height:").pack(side=tk.LEFT)
        self.height_var = tk.IntVar(value=300)
        ttk.Entry(size_frame, textvariable=self.height_var, width=8).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(
            size_frame,
            text="Apply",
            command=self.create,
            font=("Arial", 9),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT, padx=5)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        tk.Button(
            btn_frame,
            text="Cancel",
            command=self.cancel,
            font=("Arial", 9),
            relief="raised",
            bd=1,
        ).pack(side=tk.RIGHT, padx=(5, 0))
        tk.Button(
            btn_frame,
            text="Create",
            command=self.create,
            font=("Arial", 9),
            relief="raised",
            bd=1,
        ).pack(side=tk.RIGHT)

        # Bind Enter key
        self.dialog.bind("<Return>", lambda e: self.create())
        self.dialog.bind("<Escape>", lambda e: self.cancel())

        # Focus on name entry
        self.name_var.set("new_image")

    def create(self):
        """Create the image."""
        try:
            width = self.width_var.get()
            height = self.height_var.get()
            name = self.name_var.get().strip()

            if width <= 0 or height <= 0:
                messagebox.showerror("Error", "Invalid size")
                return

            self.result = (width, height, name)
            self.dialog.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid size values")

    def cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()


class CodePreviewWindow:
    """Window for previewing generated code."""

    def __init__(self, parent, code_content, framework, usage_type="general"):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Code Preview - {framework} ({usage_type})")
        self.window.geometry("800x600")
        self.window.transient(parent)

        self.framework = framework
        self.usage_type = usage_type
        self.setup_ui(code_content)

    def setup_ui(self, code_content):
        """Setup the preview window UI."""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Info label
        info_label = ttk.Label(main_frame, text="Generated embedded code preview:")
        info_label.pack(anchor=tk.W, pady=(0, 10))

        # Text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_widget = tk.Text(text_frame, wrap=tk.NONE, font=("Consolas", 10))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=self.text_widget.yview
        )
        h_scrollbar = ttk.Scrollbar(
            text_frame, orient=tk.HORIZONTAL, command=self.text_widget.xview
        )

        self.text_widget.configure(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
        )

        # Grid layout
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Generate enhanced code with usage examples
        enhanced_code = self.generate_enhanced_code(code_content)

        # Insert enhanced code content
        self.text_widget.insert(tk.END, enhanced_code)
        self.text_widget.configure(state=tk.DISABLED)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(
            btn_frame,
            text="Copy to Clipboard",
            command=lambda: self.copy_to_clipboard(enhanced_code),
            font=("Arial", 9),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT)
        tk.Button(
            btn_frame,
            text="Close",
            command=self.window.destroy,
            font=("Arial", 9),
            relief="raised",
            bd=1,
        ).pack(side=tk.RIGHT)

    def generate_enhanced_code(self, base_code):
        """Generate enhanced code with usage examples."""
        examples = self.get_usage_examples()

        enhanced = base_code + "\n\n" + examples
        return enhanced

    def get_usage_examples(self):
        """Get usage examples based on framework and usage type."""
        examples = {
            "tkinter": {
                "general": '''
# Usage Examples for Tkinter

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import base64
from io import BytesIO

def load_image_from_base64(base64_string):
    """Load PIL Image from base64 string."""
    image_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_data))

def create_photo_image(base64_string):
    """Create PhotoImage for tkinter from base64 string."""
    pil_image = load_image_from_base64(base64_string)
    return ImageTk.PhotoImage(pil_image)

# Example usage:
root = tk.Tk()

# For buttons:
for theme, images in embedded_images.items():
    for name, data in images.items():
        photo = create_photo_image(data)
        btn = tk.Button(root, image=photo, text=f"{theme}_{name}")
        btn.pack(pady=5)
        # Keep reference to prevent garbage collection
        btn.image = photo

# For labels (icons):
for theme, images in embedded_images.items():
    for name, data in images.items():
        photo = create_photo_image(data)
        label = tk.Label(root, image=photo)
        label.pack(pady=5)
        label.image = photo

# For canvas backgrounds:
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()
for theme, images in embedded_images.items():
    for name, data in images.items():
        photo = create_photo_image(data)
        canvas.create_image(200, 150, image=photo)
        canvas.image = photo  # Keep reference
        break  # Use first image as background
''',
                "buttons": '''
# Button-specific usage for Tkinter

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import base64
from io import BytesIO

def create_button_with_image(parent, base64_string, text="", command=None):
    """Create a button with embedded image."""
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))
    photo = ImageTk.PhotoImage(pil_image)

    btn = tk.Button(parent, image=photo, text=text, compound=tk.LEFT, command=command)
    btn.image = photo  # Keep reference
    return btn

# Example usage:
root = tk.Tk()
root.title("Image Buttons")

for theme, images in embedded_images.items():
    frame = ttk.LabelFrame(root, text=f"{theme.title()} Theme")
    frame.pack(fill=tk.X, padx=10, pady=5)

    for name, data in images.items():
        btn = create_button_with_image(frame, data, text=name.replace('.png', ''))
        btn.pack(side=tk.LEFT, padx=5, pady=5)
''',
                "icons": '''
# Icon usage for Tkinter

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import base64
from io import BytesIO

def create_icon_label(parent, base64_string, size=(32, 32)):
    """Create a label with resized icon."""
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))
    pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(pil_image)

    label = tk.Label(parent, image=photo, text="")
    label.image = photo
    return label

# Example usage:
root = tk.Tk()
root.title("Icon Gallery")

# Create icon grid
row, col = 0, 0
for theme, images in embedded_images.items():
    for name, data in images.items():
        icon = create_icon_label(root, data, size=(48, 48))
        icon.grid(row=row, column=col, padx=10, pady=10)

        # Add label
        tk.Label(root, text=name.replace('.png', '')).grid(row=row+1, column=col)

        col += 1
        if col > 4:  # 5 icons per row
            col = 0
            row += 2
''',
                "backgrounds": '''
# Background usage for Tkinter

import tkinter as tk
from PIL import Image, ImageTk
import base64
from io import BytesIO

def set_background_image(widget, base64_string, size=None):
    """Set background image for a widget."""
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))

    if size:
        pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)

    photo = ImageTk.PhotoImage(pil_image)

    if isinstance(widget, tk.Canvas):
        widget.create_image(0, 0, anchor=tk.NW, image=photo)
        widget.image = photo
    else:
        widget.configure(image=photo)
        widget.image = photo

# Example usage:
root = tk.Tk()
root.title("Background Images")

# Canvas with background
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Use first available image as background
for theme, images in embedded_images.items():
    for name, data in images.items():
        set_background_image(canvas, data, size=(400, 300))
        break
    break
''',
            },
            "customtkinter": {
                "general": '''
# Usage Examples for CustomTkinter

import customtkinter as ctk
from PIL import Image, ImageTk
import base64
from io import BytesIO

def load_image_from_base64(base64_string):
    """Load PIL Image from base64 string."""
    image_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_data))

def create_ctk_image(base64_string, size=None):
    """Create CTkImage for customtkinter from base64 string."""
    pil_image = load_image_from_base64(base64_string)
    if size:
        return ctk.CTkImage(light_image=pil_image, size=size)
    return ctk.CTkImage(light_image=pil_image)

# Example usage:
ctk.set_appearance_mode("dark")  # or "light"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("CustomTkinter with Embedded Images")

# For buttons:
for theme, images in embedded_images.items():
    for name, data in images.items():
        ctk_image = create_ctk_image(data, size=(32, 32))
        btn = ctk.CTkButton(root, image=ctk_image, text=f"{theme}_{name}")
        btn.pack(pady=5)

# For labels (icons):
for theme, images in embedded_images.items():
    for name, data in images.items():
        ctk_image = create_ctk_image(data, size=(48, 48))
        label = ctk.CTkLabel(root, image=ctk_image, text="")
        label.pack(pady=5)

root.mainloop()
''',
                "buttons": '''
# Button-specific usage for CustomTkinter

import customtkinter as ctk
from PIL import Image
import base64
from io import BytesIO

def create_ctk_button_with_image(parent, base64_string, text="", command=None):
    """Create a CustomTkinter button with embedded image."""
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))
    ctk_image = ctk.CTkImage(light_image=pil_image, size=(24, 24))

    btn = ctk.CTkButton(parent, image=ctk_image, text=text, command=command)
    return btn

# Example usage:
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("CustomTkinter Image Buttons")

for theme, images in embedded_images.items():
    frame = ctk.CTkFrame(root)
    frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(frame, text=f"{theme.title()} Theme", font=("Arial", 16, "bold")).pack(pady=5)

    for name, data in images.items():
        btn = create_ctk_button_with_image(frame, data, text=name.replace('.png', ''))
        btn.pack(side="left", padx=5, pady=5)

root.mainloop()
''',
                "icons": '''
# Icon usage for CustomTkinter

import customtkinter as ctk
from PIL import Image
import base64
from io import BytesIO

def create_ctk_icon_label(parent, base64_string, size=(32, 32)):
    """Create a CustomTkinter label with resized icon."""
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))
    ctk_image = ctk.CTkImage(light_image=pil_image, size=size)

    label = ctk.CTkLabel(parent, image=ctk_image, text="")
    return label

# Example usage:
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("CustomTkinter Icon Gallery")

# Create scrollable frame for icons
scrollable_frame = ctk.CTkScrollableFrame(root, width=600, height=400)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Create icon grid
row, col = 0, 0
for theme, images in embedded_images.items():
    for name, data in images.items():
        icon = create_ctk_icon_label(scrollable_frame, data, size=(48, 48))
        icon.grid(row=row, column=col, padx=10, pady=10)

        # Add label
        ctk.CTkLabel(scrollable_frame, text=name.replace('.png', '')).grid(row=row+1, column=col)

        col += 1
        if col > 4:  # 5 icons per row
            col = 0
            row += 2

root.mainloop()
''',
                "backgrounds": '''
# Background usage for CustomTkinter

import customtkinter as ctk
from PIL import Image
import base64
from io import BytesIO

def set_ctk_background_image(widget, base64_string, size=None):
    """Set background image for a CustomTkinter widget."""
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))

    if size:
        pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)

    # For CustomTkinter, we can use it as a label background
    ctk_image = ctk.CTkImage(light_image=pil_image, size=pil_image.size)

    if hasattr(widget, 'configure'):
        # Create a label with the background image
        bg_label = ctk.CTkLabel(widget, image=ctk_image, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        return bg_label

# Example usage:
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("CustomTkinter Background Images")
root.geometry("600x400")

# Use first available image as background
for theme, images in embedded_images.items():
    for name, data in images.items():
        bg_label = set_ctk_background_image(root, data, size=(600, 400))

        # Add some content on top
        content_frame = ctk.CTkFrame(root, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(content_frame, text="Content over background",
                    font=("Arial", 20, "bold")).pack()
        break
    break

root.mainloop()
''',
            },
        }

        framework_examples = examples.get(self.framework, {})
        usage_example = framework_examples.get(
            self.usage_type,
            framework_examples.get(
                "general", "# No specific examples available for this combination."
            ),
        )

        return usage_example

    def copy_to_clipboard(self, content):
        """Copy content to clipboard."""
        self.window.clipboard_clear()
        self.window.clipboard_append(content)
        messagebox.showinfo("Success", "Code copied to clipboard!")


class HelpWindow:
    """Window for displaying help content."""

    def __init__(self, parent, title, content):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("700x500")
        self.window.transient(parent)

        # Make window modal
        self.window.grab_set()

        self.setup_ui(content)

        # Center the window
        self.center_window()

    def setup_ui(self, content):
        """Setup the help window UI."""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Text widget
        self.text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#f8f9fa",
            fg="#212529",
            padx=15,
            pady=15,
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=self.text_widget.yview
        )
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        # Pack text and scrollbar
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert content with formatting
        self.insert_formatted_content(content)

        # Make text read-only
        self.text_widget.configure(state=tk.DISABLED)

        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        # Buttons
        tk.Button(
            btn_frame,
            text="Print",
            command=self.print_content,
            font=("Arial", 9),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT)
        tk.Button(
            btn_frame,
            text="Copy All",
            command=self.copy_content,
            font=("Arial", 9),
            relief="raised",
            bd=1,
        ).pack(side=tk.LEFT, padx=(10, 0))
        tk.Button(
            btn_frame,
            text="Close",
            command=self.window.destroy,
            font=("Arial", 9),
            relief="raised",
            bd=1,
        ).pack(side=tk.RIGHT)

    def insert_formatted_content(self, content):
        """Insert content with basic formatting."""
        self.text_widget.configure(state=tk.NORMAL)

        # Configure text tags for formatting
        self.text_widget.tag_configure(
            "heading", font=("Arial", 14, "bold"), foreground="#0066cc"
        )
        self.text_widget.tag_configure(
            "subheading", font=("Arial", 12, "bold"), foreground="#333333"
        )
        self.text_widget.tag_configure(
            "bullet", font=("Consolas", 11), foreground="#666666"
        )
        self.text_widget.tag_configure(
            "code", font=("Consolas", 10), background="#e9ecef", foreground="#d63384"
        )
        self.text_widget.tag_configure(
            "emphasis", font=("Arial", 11, "bold"), foreground="#198754"
        )

        lines = content.strip().split("\n")
        for line in lines:
            line = line.rstrip()

            # Empty line
            if not line:
                self.text_widget.insert(tk.END, "\n")
                continue

            # Main headings (🎨, 🛠️, etc.)
            if any(emoji in line for emoji in ["🎨", "🛠️", "💻", "⌨️", "💡", "🔧", "📚"]):
                self.text_widget.insert(tk.END, line + "\n", "heading")
                self.text_widget.insert(tk.END, "=" * 50 + "\n\n", "heading")
                continue

            # Subheadings (ALL CAPS or starting with emoji)
            if (line.isupper() and len(line) > 3) or any(
                emoji in line[:3]
                for emoji in ["📋", "🚀", "🎯", "⚙️", "📝", "💡", "🔍", "🆘", "⚡", "🚨"]
            ):
                self.text_widget.insert(tk.END, line + "\n", "subheading")
                continue

            # Bullet points
            if line.startswith("•") or line.startswith("-"):
                self.text_widget.insert(tk.END, line + "\n", "bullet")
                continue

            # Code blocks (lines starting with spaces or containing code-like content)
            if line.startswith("  ") or any(
                keyword in line
                for keyword in ["python", "pip", "import", "def ", "class ", "```"]
            ):
                self.text_widget.insert(tk.END, line + "\n", "code")
                continue

            # Emphasis (lines with specific keywords)
            if any(
                word in line.lower()
                for word in ["problem:", "solution:", "tip:", "note:", "warning:"]
            ):
                self.text_widget.insert(tk.END, line + "\n", "emphasis")
                continue

            # Regular text
            self.text_widget.insert(tk.END, line + "\n")

        self.text_widget.configure(state=tk.DISABLED)

    def center_window(self):
        """Center the window on the screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def print_content(self):
        """Print the help content."""
        try:
            temp_file = self._create_temp_file()
            self._execute_print_command(temp_file)
        except Exception as e:
            messagebox.showerror("Print Error", f"Could not print: {str(e)}")

    def _create_temp_file(self):
        """Create a temporary file with the help content."""
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            content = self.text_widget.get(1.0, tk.END)
            f.write(content)
            return f.name

    def _execute_print_command(self, temp_file):
        """Execute the appropriate print command based on the operating system."""
        import os

        if os.name == "nt":
            self._print_on_windows(temp_file)
        else:
            self._print_on_unix(temp_file)

    def _print_on_windows(self, temp_file):
        """Handle printing on Windows systems."""
        import os
        import subprocess  # nosec B404 - subprocess needed for system printing
        import tempfile

        self._validate_temp_file(temp_file)

        # Use full path to cmd.exe for security
        cmd_path = os.path.join(
            os.environ.get("SYSTEMROOT", "C:\\Windows"), "System32", "cmd.exe"
        )

        if not os.path.exists(cmd_path):
            raise Exception("Windows command processor not found")

        try:
            subprocess.run(  # nosec B603 - controlled subprocess call with validated inputs
                [cmd_path, "/c", "start", "/min", "", temp_file],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tempfile.gettempdir(),  # Set working directory to temp for additional security
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            raise Exception(f"Failed to open file for printing: {str(e)}")

    def _validate_temp_file(self, temp_file):
        """Validate that the temporary file is in a safe location."""
        import os
        import tempfile

        if not (
            os.path.exists(temp_file)
            and os.path.dirname(temp_file) == tempfile.gettempdir()
        ):
            raise Exception("Invalid temporary file path for printing")

    def _print_on_unix(self, temp_file):
        """Handle printing on Unix/Linux/Mac systems."""
        import shutil

        # Try print commands in order of preference
        print_commands = [
            ("lpr", self._try_lpr_command),
            ("lp", self._try_lp_command),
            ("xdg-open", self._try_xdg_open_command),
        ]

        for cmd_name, cmd_func in print_commands:
            cmd_path = shutil.which(cmd_name)
            if cmd_path:
                cmd_func(cmd_path, temp_file)
                return

        raise Exception(
            "No suitable print command found. Please install lpr, lp, or ensure xdg-open is available."
        )

    def _try_lpr_command(self, lpr_path, temp_file):
        """Try to print using the lpr command."""
        self._run_print_command([lpr_path, temp_file])

    def _try_lp_command(self, lp_path, temp_file):
        """Try to print using the lp command."""
        self._run_print_command([lp_path, temp_file])

    def _try_xdg_open_command(self, xdg_open_path, temp_file):
        """Try to print using the xdg-open command."""
        self._run_print_command([xdg_open_path, temp_file])

    def _run_print_command(self, command):
        """Run a print command and handle errors."""
        import subprocess  # nosec B404 - subprocess needed for system printing

        try:
            subprocess.run(
                command, check=True, capture_output=True, text=True
            )  # nosec B603 - controlled subprocess call with validated inputs
        except subprocess.CalledProcessError as e:
            raise Exception(f"Print command failed: {e.stderr if e.stderr else str(e)}")

    def copy_content(self):
        """Copy all content to clipboard."""
        content = self.text_widget.get(1.0, tk.END)
        self.window.clipboard_clear()
        self.window.clipboard_append(content)
        messagebox.showinfo("Copied", "Help content copied to clipboard!")


class CursorSettingsDialog:
    """Dialog for configuring cursor settings."""

    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Cursor Settings")
        self.window.geometry("600x500")
        self.window.resizable(True, True)

        # Make dialog modal
        self.window.transient(parent)
        self.window.grab_set()

        # Center the dialog
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")

        self.setup_ui()

        # Focus the dialog
        self.window.focus_set()

    def setup_ui(self):
        """Set up the cursor settings dialog UI."""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # General settings tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        self.setup_general_tab(general_frame)

        # Tool cursors tab
        tools_frame = ttk.Frame(notebook)
        notebook.add(tools_frame, text="Tool Cursors")
        self.setup_tools_tab(tools_frame)

        # Custom cursors tab
        custom_frame = ttk.Frame(notebook)
        notebook.add(custom_frame, text="Custom Cursors")
        self.setup_custom_tab(custom_frame)

        # Available cursors tab
        available_frame = ttk.Frame(notebook)
        notebook.add(available_frame, text="Available Cursors")
        self.setup_available_tab(available_frame)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            buttons_frame, text="Test Current Tool", command=self.test_current_cursor
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(
            buttons_frame, text="Reset to Defaults", command=self.reset_to_defaults
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(buttons_frame, text="Cancel", command=self.cancel).pack(
            side=tk.RIGHT, padx=(5, 0)
        )
        ttk.Button(buttons_frame, text="Apply", command=self.apply_settings).pack(
            side=tk.RIGHT, padx=5
        )
        ttk.Button(buttons_frame, text="OK", command=self.ok).pack(
            side=tk.RIGHT, padx=5
        )

    def setup_general_tab(self, parent):
        """Set up the general settings tab."""
        # Handedness setting
        handedness_frame = ttk.LabelFrame(parent, text="Handedness", padding=10)
        handedness_frame.pack(fill=tk.X, pady=(0, 10))

        self.handedness_var = tk.StringVar(value=self.app.cursor_settings["handedness"])

        ttk.Radiobutton(
            handedness_frame,
            text="Right-handed",
            variable=self.handedness_var,
            value="right",
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            handedness_frame,
            text="Left-handed",
            variable=self.handedness_var,
            value="left",
        ).pack(anchor=tk.W)

        # Info label
        info_label = ttk.Label(
            handedness_frame,
            text="Left-handed mode provides alternative cursor orientations\n"
            "for better precision when drawing with your left hand.",
            foreground="gray",
        )
        info_label.pack(anchor=tk.W, pady=(5, 0))

        # Platform info
        platform_frame = ttk.LabelFrame(parent, text="Platform Information", padding=10)
        platform_frame.pack(fill=tk.X, pady=(0, 10))

        import platform

        platform_info = f"Operating System: {platform.system()} {platform.release()}\n"
        platform_info += f"Python Version: {platform.python_version()}\n"
        platform_info += f"Tkinter Version: {tk.TkVersion}"

        ttk.Label(platform_frame, text=platform_info, foreground="gray").pack(
            anchor=tk.W
        )

    def setup_tools_tab(self, parent):
        """Set up the tool cursors tab."""
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Tool cursor settings
        self.cursor_vars = {}
        tools = [
            "brush",
            "pencil",
            "eraser",
            "line",
            "rectangle",
            "circle",
            "text",
            "fill",
        ]

        for i, tool in enumerate(tools):
            tool_frame = ttk.LabelFrame(
                scrollable_frame, text=f"{tool.title()} Tool", padding=10
            )
            tool_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

            # Current setting
            current_cursor = self.app.cursor_settings.get(tool, "crosshair")
            self.cursor_vars[tool] = tk.StringVar(value=current_cursor)

            # Cursor selection
            cursor_frame = ttk.Frame(tool_frame)
            cursor_frame.pack(fill=tk.X)

            ttk.Label(cursor_frame, text="Cursor:").pack(side=tk.LEFT)

            # Get all available cursors including custom ones
            all_cursors = self.get_available_cursors()
            custom_cursors = [
                f"custom:{name}"
                for name in self.app.cursor_settings["custom_cursors"].keys()
            ]
            all_cursors.extend(custom_cursors)

            cursor_combo = ttk.Combobox(
                cursor_frame,
                textvariable=self.cursor_vars[tool],
                values=all_cursors,
                state="readonly",
                width=15,
            )
            cursor_combo.pack(side=tk.LEFT, padx=(5, 0))

            # Cursor preview
            preview_frame = ttk.Frame(cursor_frame)
            preview_frame.pack(side=tk.LEFT, padx=(5, 0))

            preview_canvas = tk.Canvas(
                preview_frame,
                width=50,
                height=30,
                bg="lightgray",
                relief="sunken",
                bd=1,
            )
            preview_canvas.pack()

            # Add hover instruction
            preview_canvas.create_text(
                25, 15, text="hover", fill="darkgray", font=("Arial", 8)
            )

            # Store preview canvas reference for updates
            setattr(self, f"preview_canvas_{tool}", preview_canvas)

            # Test button
            ttk.Button(
                cursor_frame, text="Test", command=lambda t=tool: self.test_cursor(t)
            ).pack(side=tk.LEFT, padx=(5, 0))

            # Update preview when cursor selection changes
            cursor_combo.bind(
                "<<ComboboxSelected>>", lambda e, t=tool: self.update_cursor_preview(t)
            )

            # Initialize preview
            self.update_cursor_preview(tool)

    def setup_custom_tab(self, parent):
        """Set up the custom cursors tab."""
        # Instructions
        instructions = ttk.Label(
            parent,
            text="Create custom cursors using cursor data strings or file paths.\n"
            "Custom cursors will appear in tool selection with 'custom:' prefix.",
            foreground="gray",
        )
        instructions.pack(anchor=tk.W, pady=(0, 10))

        # Custom cursor list
        list_frame = ttk.LabelFrame(parent, text="Custom Cursors", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Listbox with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)

        self.custom_listbox = tk.Listbox(list_container)
        custom_scrollbar = ttk.Scrollbar(
            list_container, orient="vertical", command=self.custom_listbox.yview
        )
        self.custom_listbox.configure(yscrollcommand=custom_scrollbar.set)

        self.custom_listbox.pack(side="left", fill="both", expand=True)
        custom_scrollbar.pack(side="right", fill="y")

        # Populate custom cursors
        self.refresh_custom_list()

        # Buttons for custom cursors
        custom_buttons = ttk.Frame(list_frame)
        custom_buttons.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            custom_buttons, text="Add Custom Cursor", command=self.add_custom_cursor
        ).pack(side=tk.LEFT)
        ttk.Button(
            custom_buttons, text="Edit Selected", command=self.edit_custom_cursor
        ).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(
            custom_buttons, text="Delete Selected", command=self.delete_custom_cursor
        ).pack(side=tk.LEFT, padx=(5, 0))

    def setup_available_tab(self, parent):
        """Set up the available cursors tab."""
        # Instructions
        instructions = ttk.Label(
            parent,
            text="These are the standard cursors available on your platform.\n"
            "Click 'Test' to preview how each cursor looks.",
            foreground="gray",
        )
        instructions.pack(anchor=tk.W, pady=(0, 10))

        # Available cursors list
        available_frame = ttk.Frame(parent)
        available_frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollable list
        canvas = tk.Canvas(available_frame)
        scrollbar = ttk.Scrollbar(
            available_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # List available cursors
        available_cursors = self.get_available_cursors()
        for i, cursor in enumerate(available_cursors):
            cursor_frame = ttk.Frame(scrollable_frame)
            cursor_frame.pack(fill=tk.X, pady=2, padx=10)

            # Cursor name
            ttk.Label(cursor_frame, text=cursor, width=20).pack(side=tk.LEFT)

            # Cursor preview
            preview_frame = ttk.Frame(cursor_frame)
            preview_frame.pack(side=tk.LEFT, padx=(5, 0))

            preview_canvas = tk.Canvas(
                preview_frame,
                width=50,
                height=30,
                bg="lightgray",
                relief="sunken",
                bd=1,
            )
            preview_canvas.pack()

            # Show cursor name and hover instruction
            preview_canvas.create_text(
                25, 10, text=cursor[:8], fill="black", font=("Arial", 7)
            )
            preview_canvas.create_text(
                25, 22, text="hover", fill="darkgray", font=("Arial", 6)
            )

            # Apply the actual cursor to the preview canvas
            try:
                preview_canvas.configure(cursor=cursor)
            except tk.TclError:
                preview_canvas.configure(cursor="arrow")
                preview_canvas.create_text(
                    25, 15, text="⚠", fill="red", font=("Arial", 8)
                )

            # Test button
            ttk.Button(
                cursor_frame,
                text="Test",
                command=lambda c=cursor: self.test_specific_cursor(c),
            ).pack(side=tk.LEFT, padx=(5, 0))

    def get_available_cursors(self):
        """Get list of available cursors for the platform."""
        # Standard Tkinter cursors that work on most platforms
        cursors = [
            "arrow",
            "based_arrow_down",
            "based_arrow_up",
            "boat",
            "bogosity",
            "bottom_left_corner",
            "bottom_right_corner",
            "bottom_side",
            "bottom_tee",
            "box_spiral",
            "center_ptr",
            "circle",
            "clock",
            "coffee_mug",
            "cross",
            "cross_reverse",
            "crosshair",
            "diamond_cross",
            "dot",
            "dotbox",
            "double_arrow",
            "draft_large",
            "draft_small",
            "draped_box",
            "exchange",
            "fleur",
            "gobbler",
            "gumby",
            "hand1",
            "hand2",
            "heart",
            "icon",
            "iron_cross",
            "left_ptr",
            "left_side",
            "left_tee",
            "leftbutton",
            "ll_angle",
            "lr_angle",
            "man",
            "middlebutton",
            "mouse",
            "pencil",
            "pirate",
            "plus",
            "question_arrow",
            "right_ptr",
            "right_side",
            "right_tee",
            "rightbutton",
            "rtl_logo",
            "sailboat",
            "sb_down_arrow",
            "sb_h_double_arrow",
            "sb_left_arrow",
            "sb_right_arrow",
            "sb_up_arrow",
            "sb_v_double_arrow",
            "shuttle",
            "sizing",
            "spider",
            "spraycan",
            "star",
            "target",
            "tcross",
            "top_left_arrow",
            "top_left_corner",
            "top_right_corner",
            "top_side",
            "top_tee",
            "trek",
            "ul_angle",
            "umbrella",
            "ur_angle",
            "watch",
            "xterm",
            "X_cursor",
        ]
        return sorted(cursors)

    def update_cursor_preview(self, tool):
        """Update the cursor preview for a specific tool."""
        try:
            preview_canvas = getattr(self, f"preview_canvas_{tool}", None)
            if not preview_canvas:
                return

            # Clear previous preview
            preview_canvas.delete("all")

            # Get current cursor
            cursor_name = self.cursor_vars[tool].get()

            # Handle custom cursors
            if cursor_name.startswith("custom:"):
                display_name = cursor_name[7:]  # Remove 'custom:' prefix
                if display_name in self.app.cursor_settings["custom_cursors"]:
                    actual_cursor = self.app.cursor_settings["custom_cursors"][
                        display_name
                    ]
                else:
                    actual_cursor = "arrow"  # Fallback
            else:
                actual_cursor = cursor_name
                display_name = cursor_name

            # Show cursor name and hover instruction
            preview_canvas.create_text(
                25, 10, text=display_name[:8], fill="black", font=("Arial", 7)
            )
            preview_canvas.create_text(
                25, 22, text="hover", fill="darkgray", font=("Arial", 6)
            )

            # Apply the actual cursor to the preview canvas
            try:
                preview_canvas.configure(cursor=actual_cursor)
            except tk.TclError:
                preview_canvas.configure(cursor="arrow")
                preview_canvas.create_text(
                    25, 15, text="⚠", fill="red", font=("Arial", 8)
                )

        except Exception as e:
            # If preview fails, just show a generic indicator
            if hasattr(self, f"preview_canvas_{tool}"):
                canvas = getattr(self, f"preview_canvas_{tool}")
                canvas.delete("all")
                canvas.create_text(25, 15, text="?", fill="gray", font=("Arial", 12))

    def draw_cursor_preview(self, canvas, cursor_name):
        """Draw a visual representation of the cursor."""
        # Create a simple visual representation based on cursor type
        cursor_representations = {
            "arrow": lambda: self.draw_arrow_cursor(canvas),
            "crosshair": lambda: self.draw_crosshair_cursor(canvas),
            "dotbox": lambda: self.draw_dotbox_cursor(canvas),
            "pencil": lambda: self.draw_pencil_cursor(canvas),
            "spraycan": lambda: self.draw_spraycan_cursor(canvas),
            "xterm": lambda: self.draw_xterm_cursor(canvas),
            "plus": lambda: self.draw_plus_cursor(canvas),
            "hand1": lambda: self.draw_hand_cursor(canvas),
            "hand2": lambda: self.draw_hand_cursor(canvas),
            "watch": lambda: self.draw_watch_cursor(canvas),
            "target": lambda: self.draw_target_cursor(canvas),
            "tcross": lambda: self.draw_tcross_cursor(canvas),
        }

        # Draw the appropriate representation or a generic one
        if cursor_name in cursor_representations:
            cursor_representations[cursor_name]()
        else:
            # Generic cursor representation
            canvas.create_text(20, 15, text="⚬", fill="black", font=("Arial", 10))

    def draw_arrow_cursor(self, canvas):
        """Draw arrow cursor representation."""
        canvas.create_polygon(
            [5, 5, 5, 20, 10, 15, 15, 25, 20, 20, 12, 12],
            fill="black",
            outline="white",
            width=1,
        )

    def draw_crosshair_cursor(self, canvas):
        """Draw crosshair cursor representation."""
        canvas.create_line(20, 5, 20, 25, fill="black", width=1)
        canvas.create_line(10, 15, 30, 15, fill="black", width=1)
        canvas.create_oval(18, 13, 22, 17, outline="black", width=1)

    def draw_dotbox_cursor(self, canvas):
        """Draw dotbox cursor representation."""
        canvas.create_rectangle(15, 10, 25, 20, outline="black", width=1, dash=(2, 2))
        canvas.create_oval(19, 14, 21, 16, fill="black")

    def draw_pencil_cursor(self, canvas):
        """Draw pencil cursor representation."""
        canvas.create_line(10, 20, 25, 5, fill="brown", width=3)
        canvas.create_polygon([23, 7, 27, 3, 30, 6, 26, 10], fill="gray")
        canvas.create_oval(9, 19, 11, 21, fill="black")

    def draw_spraycan_cursor(self, canvas):
        """Draw spraycan cursor representation."""
        canvas.create_rectangle(15, 8, 25, 22, fill="silver", outline="black")
        canvas.create_rectangle(18, 5, 22, 8, fill="black")
        # Spray dots
        for i, (x, y) in enumerate([(12, 12), (28, 10), (30, 16), (13, 18)]):
            canvas.create_oval(x, y, x + 1, y + 1, fill="blue")

    def draw_xterm_cursor(self, canvas):
        """Draw xterm cursor representation."""
        canvas.create_line(20, 8, 20, 22, fill="black", width=2)
        canvas.create_line(17, 8, 23, 8, fill="black", width=1)
        canvas.create_line(17, 22, 23, 22, fill="black", width=1)

    def draw_plus_cursor(self, canvas):
        """Draw plus cursor representation."""
        canvas.create_line(20, 8, 20, 22, fill="black", width=2)
        canvas.create_line(13, 15, 27, 15, fill="black", width=2)

    def draw_hand_cursor(self, canvas):
        """Draw hand cursor representation."""
        canvas.create_oval(15, 12, 25, 20, fill="peachpuff", outline="black")
        canvas.create_rectangle(12, 8, 16, 15, fill="peachpuff", outline="black")
        canvas.create_rectangle(16, 6, 20, 13, fill="peachpuff", outline="black")
        canvas.create_rectangle(20, 7, 24, 14, fill="peachpuff", outline="black")
        canvas.create_rectangle(24, 9, 28, 16, fill="peachpuff", outline="black")

    def draw_watch_cursor(self, canvas):
        """Draw watch cursor representation."""
        canvas.create_oval(12, 8, 28, 24, fill="silver", outline="black", width=2)
        canvas.create_line(20, 16, 20, 12, fill="black", width=2)
        canvas.create_line(20, 16, 24, 16, fill="black", width=1)

    def draw_target_cursor(self, canvas):
        """Draw target cursor representation."""
        canvas.create_oval(10, 6, 30, 26, outline="red", width=2)
        canvas.create_oval(15, 11, 25, 21, outline="red", width=1)
        canvas.create_line(20, 6, 20, 26, fill="red", width=1)
        canvas.create_line(10, 16, 30, 16, fill="red", width=1)

    def draw_tcross_cursor(self, canvas):
        """Draw tcross cursor representation."""
        canvas.create_line(20, 5, 20, 25, fill="black", width=2)
        canvas.create_line(5, 15, 35, 15, fill="black", width=2)

    def refresh_custom_list(self):
        """Refresh the custom cursors list."""
        self.custom_listbox.delete(0, tk.END)
        for name in self.app.cursor_settings["custom_cursors"].keys():
            self.custom_listbox.insert(tk.END, name)

    def test_cursor(self, tool):
        """Test the cursor for a specific tool."""
        cursor = self.cursor_vars[tool].get()
        self.test_specific_cursor(cursor)

    def test_specific_cursor(self, cursor):
        """Test a specific cursor."""
        try:
            # Create a non-modal test window
            CursorTestWindow(self.window, self.app, cursor)

        except tk.TclError as e:
            tk.messagebox.showerror(
                "Cursor Error", f"Cannot display cursor '{cursor}':\n{str(e)}"
            )

    def test_current_cursor(self):
        """Test the cursor for the currently selected tool."""
        self.test_cursor(self.app.current_tool)

    def add_custom_cursor(self):
        """Add a new custom cursor."""
        CustomCursorDialog(self.window, self, None)

    def edit_custom_cursor(self):
        """Edit the selected custom cursor."""
        selection = self.custom_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning(
                "No Selection", "Please select a custom cursor to edit."
            )
            return

        cursor_name = self.custom_listbox.get(selection[0])
        CustomCursorDialog(self.window, self, cursor_name)

    def delete_custom_cursor(self):
        """Delete the selected custom cursor."""
        selection = self.custom_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning(
                "No Selection", "Please select a custom cursor to delete."
            )
            return

        cursor_name = self.custom_listbox.get(selection[0])
        if tk.messagebox.askyesno(
            "Delete Custom Cursor",
            f"Are you sure you want to delete the custom cursor '{cursor_name}'?",
        ):
            del self.app.cursor_settings["custom_cursors"][cursor_name]
            self.refresh_custom_list()

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        if tk.messagebox.askyesno(
            "Reset to Defaults",
            "Are you sure you want to reset all cursor settings to defaults?",
        ):
            # Reset handedness
            self.handedness_var.set("right")

            # Reset tool cursors
            defaults = {
                "brush": "crosshair",
                "pencil": "crosshair",
                "eraser": "dotbox",
                "line": "crosshair",
                "rectangle": "crosshair",
                "circle": "crosshair",
                "text": "xterm",
                "fill": "spraycan",
            }

            for tool, default_cursor in defaults.items():
                if tool in self.cursor_vars:
                    self.cursor_vars[tool].set(default_cursor)

    def apply_settings(self):
        """Apply the current settings."""
        # Update handedness
        self.app.cursor_settings["handedness"] = self.handedness_var.get()

        # Update tool cursors
        for tool, var in self.cursor_vars.items():
            self.app.cursor_settings[tool] = var.get()

        # Save settings
        self.app.save_cursor_settings()

        # Update current tool cursor
        self.app.update_tool_cursor(self.app.current_tool)

        tk.messagebox.showinfo(
            "Settings Applied", "Cursor settings have been applied and saved."
        )

    def ok(self):
        """Apply settings and close dialog."""
        self.apply_settings()
        self.window.destroy()

    def cancel(self):
        """Close dialog without applying changes."""
        self.window.destroy()


class CustomCursorDialog:
    """Dialog for creating/editing custom cursors."""

    def __init__(self, parent, settings_dialog, cursor_name=None):
        self.settings_dialog = settings_dialog
        self.cursor_name = cursor_name
        self.is_edit = cursor_name is not None

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Custom Cursor" if self.is_edit else "Add Custom Cursor")
        self.window.geometry("500x400")
        self.window.resizable(True, True)

        # Make dialog modal
        self.window.transient(parent)
        self.window.grab_set()

        # Center the dialog
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")

        self.setup_ui()

        if self.is_edit:
            self.load_cursor_data()

        # Bind text changes to update preview
        self.data_text.bind("<KeyRelease>", self.update_preview)
        self.data_text.bind("<ButtonRelease>", self.update_preview)

        # Initial preview update
        self.update_preview()

        # Bind text changes to update preview
        self.data_text.bind("<KeyRelease>", self.update_preview)
        self.data_text.bind("<ButtonRelease>", self.update_preview)

        # Initial preview update
        self.update_preview()

        # Focus the dialog
        self.window.focus_set()

    def setup_ui(self):
        """Set up the custom cursor dialog UI."""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cursor name
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(name_frame, text="Cursor Name:").pack(side=tk.LEFT)
        self.name_var = tk.StringVar(value=self.cursor_name or "")
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Cursor data
        data_frame = ttk.LabelFrame(main_frame, text="Cursor Data", padding=10)
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Instructions
        instructions = ttk.Label(
            data_frame,
            text="Enter cursor data as a string (e.g., 'crosshair') or file path to cursor file.",
            foreground="gray",
        )
        instructions.pack(anchor=tk.W, pady=(0, 5))

        # Data text area with preview
        text_preview_frame = ttk.Frame(data_frame)
        text_preview_frame.pack(fill=tk.BOTH, expand=True)

        # Text area
        text_frame = ttk.Frame(text_preview_frame)
        text_frame.pack(side="left", fill="both", expand=True)

        self.data_text = tk.Text(text_frame, height=10, wrap=tk.WORD)
        data_scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.data_text.yview
        )
        self.data_text.configure(yscrollcommand=data_scrollbar.set)

        self.data_text.pack(side="left", fill="both", expand=True)
        data_scrollbar.pack(side="right", fill="y")

        # Preview area
        preview_frame = ttk.LabelFrame(text_preview_frame, text="Preview", padding=5)
        preview_frame.pack(side="right", fill="y", padx=(10, 0))

        self.preview_canvas = tk.Canvas(
            preview_frame, width=60, height=60, bg="white", relief="sunken", bd=2
        )
        self.preview_canvas.pack(pady=5)

        ttk.Label(
            preview_frame,
            text="Live Preview\n(hover to test)",
            font=("Arial", 8),
            foreground="gray",
        ).pack()

        # Preview area
        preview_frame = ttk.LabelFrame(text_preview_frame, text="Preview", padding=5)
        preview_frame.pack(side="right", fill="y", padx=(10, 0))

        self.preview_canvas = tk.Canvas(
            preview_frame, width=60, height=60, bg="white", relief="sunken", bd=2
        )
        self.preview_canvas.pack(pady=5)

        ttk.Label(
            preview_frame,
            text="Live Preview\n(hover to test)",
            font=("Arial", 8),
            foreground="gray",
        ).pack()

        # Buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)

        ttk.Button(buttons_frame, text="Test Cursor", command=self.test_cursor).pack(
            side=tk.LEFT
        )
        ttk.Button(buttons_frame, text="Browse File...", command=self.browse_file).pack(
            side=tk.LEFT, padx=(5, 0)
        )

        ttk.Button(buttons_frame, text="Cancel", command=self.cancel).pack(
            side=tk.RIGHT
        )
        ttk.Button(buttons_frame, text="Save", command=self.save_cursor).pack(
            side=tk.RIGHT, padx=(0, 5)
        )

    def load_cursor_data(self):
        """Load existing cursor data for editing."""
        if (
            self.cursor_name
            in self.settings_dialog.app.cursor_settings["custom_cursors"]
        ):
            cursor_data = self.settings_dialog.app.cursor_settings["custom_cursors"][
                self.cursor_name
            ]
            self.data_text.insert(1.0, cursor_data)

    def update_preview(self, event=None):
        """Update the cursor preview."""
        try:
            cursor_data = self.data_text.get(1.0, tk.END).strip()
            if not cursor_data:
                # Clear preview
                self.preview_canvas.delete("all")
                self.preview_canvas.create_text(
                    30, 30, text="?", fill="gray", font=("Arial", 16)
                )
                return

            # Clear previous preview
            self.preview_canvas.delete("all")

            # Draw visual representation
            if hasattr(self.settings_dialog, "draw_cursor_preview"):
                self.settings_dialog.draw_cursor_preview(
                    self.preview_canvas, cursor_data
                )
            else:
                # Fallback representation
                self.preview_canvas.create_text(
                    30, 30, text="⚬", fill="black", font=("Arial", 12)
                )

            # Apply cursor to preview canvas
            try:
                self.preview_canvas.configure(cursor=cursor_data)
            except tk.TclError:
                self.preview_canvas.configure(cursor="arrow")
                # Show error indicator
                self.preview_canvas.create_text(
                    30, 50, text="⚠", fill="red", font=("Arial", 10)
                )

        except Exception:
            # Show error in preview
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(
                30, 30, text="✗", fill="red", font=("Arial", 16)
            )

    def browse_file(self):
        """Browse for a cursor file."""
        from tkinter import filedialog

        filename = filedialog.askopenfilename(
            title="Select Cursor File",
            filetypes=[("Cursor files", "*.cur *.ani"), ("All files", "*.*")],
        )
        if filename:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(1.0, f"@{filename}")

    def test_cursor(self):
        """Test the custom cursor."""
        cursor_data = self.data_text.get(1.0, tk.END).strip()
        if not cursor_data:
            tk.messagebox.showwarning("No Data", "Please enter cursor data to test.")
            return

        try:
            # Create a test window for the custom cursor
            CursorTestWindow(self.window, self.settings_dialog.app, cursor_data)

        except tk.TclError as e:
            tk.messagebox.showerror(
                "Cursor Error", f"Cannot display custom cursor:\n{str(e)}"
            )

    def save_cursor(self):
        """Save the custom cursor."""
        name = self.name_var.get().strip()
        cursor_data = self.data_text.get(1.0, tk.END).strip()

        if not name:
            tk.messagebox.showwarning(
                "Missing Name", "Please enter a name for the custom cursor."
            )
            return

        if not cursor_data:
            tk.messagebox.showwarning("Missing Data", "Please enter cursor data.")
            return

        # Check if name already exists (and we're not editing the same one)
        if (
            not self.is_edit
            and name in self.settings_dialog.app.cursor_settings["custom_cursors"]
        ):
            if not tk.messagebox.askyesno(
                "Name Exists",
                f"A custom cursor named '{name}' already exists. Replace it?",
            ):
                return

        # Save the cursor
        self.settings_dialog.app.cursor_settings["custom_cursors"][name] = cursor_data
        self.settings_dialog.refresh_custom_list()

        tk.messagebox.showinfo(
            "Cursor Saved", f"Custom cursor '{name}' has been saved."
        )
        self.window.destroy()

    def cancel(self):
        """Cancel and close dialog."""
        self.window.destroy()


class CursorTestWindow:
    """Window for testing cursors interactively."""

    def __init__(self, parent, app, cursor):
        self.app = app
        self.cursor = cursor
        self.original_cursor = None

        self.window = tk.Toplevel(parent)
        self.window.title(f"Testing Cursor: {cursor}")
        self.window.geometry("400x300")
        self.window.resizable(True, True)

        # Don't make it modal - user needs to interact with main canvas
        self.window.transient(parent)

        # Center the dialog
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (300 // 2)
        self.window.geometry(f"400x300+{x}+{y}")

        self.setup_ui()
        self.apply_cursor()

        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # Focus the dialog
        self.window.focus_set()

    def setup_ui(self):
        """Set up the cursor test window UI."""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(
            main_frame,
            text=f"Testing Cursor: {self.cursor}",
            font=("Arial", 12, "bold"),
        )
        title_label.pack(pady=(0, 20))

        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="The cursor has been applied to the main canvas.\n\n"
            "Move your mouse over the canvas area to see the cursor in action.\n\n"
            "You can continue working with the application while this window is open.\n\n"
            "Click 'Restore Original' or close this window to return to the normal cursor.",
            justify=tk.CENTER,
            foreground="navy",
        )
        instructions.pack(pady=(0, 20))

        # Test area (canvas to show cursor here too)
        test_frame = ttk.LabelFrame(main_frame, text="Test Area", padding=10)
        test_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.test_canvas = tk.Canvas(test_frame, bg="white", height=100)
        self.test_canvas.pack(fill=tk.BOTH, expand=True)

        # Apply cursor to test canvas too
        try:
            self.test_canvas.configure(cursor=self.cursor)
        except tk.TclError:
            pass

        # Add some visual elements to the test canvas
        self.test_canvas.create_text(
            100,
            30,
            text="Move mouse here to test cursor",
            fill="gray",
            font=("Arial", 10),
        )
        self.test_canvas.create_rectangle(20, 50, 180, 80, outline="lightblue", width=2)

        # Buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)

        ttk.Button(
            buttons_frame, text="Restore Original", command=self.restore_cursor
        ).pack(side=tk.LEFT)
        ttk.Button(
            buttons_frame, text="Apply to Current Tool", command=self.apply_to_tool
        ).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(buttons_frame, text="Close", command=self.close_window).pack(
            side=tk.RIGHT
        )

    def apply_cursor(self):
        """Apply the test cursor to the main canvas."""
        try:
            # Store original cursor
            self.original_cursor = self.app.canvas.cget("cursor")

            # Apply test cursor
            self.app.canvas.configure(cursor=self.cursor)

        except tk.TclError as e:
            tk.messagebox.showerror(
                "Cursor Error", f"Cannot apply cursor '{self.cursor}':\n{str(e)}"
            )
            self.close_window()

    def restore_cursor(self):
        """Restore the original cursor."""
        if self.original_cursor:
            try:
                self.app.canvas.configure(cursor=self.original_cursor)
                tk.messagebox.showinfo(
                    "Cursor Restored",
                    f"Original cursor '{self.original_cursor}' has been restored.",
                )
            except tk.TclError:
                pass

    def apply_to_tool(self):
        """Apply this cursor to the current tool."""
        current_tool = self.app.current_tool
        if tk.messagebox.askyesno(
            "Apply Cursor", f"Apply cursor '{self.cursor}' to the {current_tool} tool?"
        ):
            self.app.cursor_settings[current_tool] = self.cursor
            self.app.save_cursor_settings()
            tk.messagebox.showinfo(
                "Cursor Applied",
                f"Cursor '{self.cursor}' has been applied to the {current_tool} tool.",
            )

    def close_window(self):
        """Close the test window and restore original cursor."""
        self.restore_cursor()
        self.window.destroy()


def main():
    """Main entry point for the Enhanced Image Studio GUI."""
    app = EnhancedImageDesignerGUI()
    app.run()


if __name__ == "__main__":
    main()
