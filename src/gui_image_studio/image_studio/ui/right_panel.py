"""
Right panel UI setup for Image Studio.
Contains image properties, transformations, and code generation.
"""

import os
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from PIL import Image, ImageTk

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class RightPanel:
    """Manages the right panel UI with properties and code generation."""

    def __init__(self, app: "EnhancedImageDesignerGUI"):
        self.app = app

    def setup(self, parent):
        """Setup the right panel with properties and code generation."""
        # Import ToolTip for tooltips
        from ..ui.dialogs import ToolTip

        # Image properties
        props_frame = ttk.LabelFrame(parent, text="Image Properties")
        props_frame.pack(fill=tk.X, padx=2, pady=2)

        # Image name
        ttk.Label(props_frame, text="Name:", font=("Arial", 8)).pack(
            anchor=tk.W, padx=3
        )
        self.app.name_var = tk.StringVar()
        name_entry = ttk.Entry(
            props_frame, textvariable=self.app.name_var, font=("Arial", 8)
        )
        name_entry.pack(fill=tk.X, padx=3, pady=1)
        name_entry.bind("<KeyRelease>", self.app.on_name_change)

        # Image size - more compact layout
        size_frame = ttk.Frame(props_frame)
        size_frame.pack(fill=tk.X, padx=3, pady=2)

        ttk.Label(size_frame, text="Size:", font=("Arial", 8)).grid(
            row=0, column=0, sticky="w"
        )
        self.app.width_var = tk.IntVar(value=300)
        self.app.height_var = tk.IntVar(value=300)

        # Smaller entry widgets
        ttk.Entry(
            size_frame, textvariable=self.app.width_var, width=4, font=("Arial", 8)
        ).grid(row=0, column=1, padx=1)
        ttk.Label(size_frame, text="x", font=("Arial", 8)).grid(row=0, column=2)
        ttk.Entry(
            size_frame, textvariable=self.app.height_var, width=4, font=("Arial", 8)
        ).grid(row=0, column=3, padx=1)
        tk.Button(
            size_frame,
            text="Apply",
            command=self.app.resize_image,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        ).grid(row=0, column=4, padx=2)

        # Image info button with icon - positioned next to Apply button
        try:
            # Try to load info icon
            current_dir = os.path.dirname(__file__)
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(current_dir))
            )
            info_icon_path = os.path.join(
                project_root, "sample_images", "info-icon.png"
            )

            if os.path.exists(info_icon_path):
                from PIL import Image, ImageTk

                info_icon_img = Image.open(info_icon_path)
                info_icon_img = info_icon_img.resize((18, 18), Image.Resampling.LANCZOS)
                info_icon_photo = ImageTk.PhotoImage(info_icon_img)

                info_btn = tk.Button(
                    size_frame,
                    image=info_icon_photo,
                    command=self.app.show_image_info,
                    relief="raised",
                    bd=1,
                    width=24,
                    height=24,
                    bg="#f0f0f0",
                )
                info_btn.image = info_icon_photo  # Keep reference
            else:
                # Fallback to text
                info_btn = tk.Button(
                    size_frame,
                    text="ⓘ",
                    command=self.app.show_image_info,
                    font=("Arial", 10, "bold"),
                    relief="raised",
                    bd=1,
                    width=3,
                    fg="blue",
                )
        except Exception:
            # Fallback to text if any error
            info_btn = tk.Button(
                size_frame,
                text="ⓘ",
                command=self.app.show_image_info,
                font=("Arial", 10, "bold"),
                relief="raised",
                bd=1,
                width=3,
                fg="blue",
            )

        info_btn.grid(row=0, column=5, padx=1)
        ToolTip(
            info_btn,
            "Show detailed image information\n• File properties and metadata\n"
            "• Color analysis and statistics\n• Technical details and recommendations",
        )

        # Configure grid weights for size frame
        size_frame.columnconfigure(4, weight=1)

        # Transformations - more compact
        transform_frame = ttk.LabelFrame(parent, text="Transformations")
        transform_frame.pack(fill=tk.X, padx=2, pady=2)

        # Rotation
        ttk.Label(transform_frame, text="Rotation:", font=("Arial", 8)).pack(
            anchor=tk.W, padx=3
        )

        # Rotation controls frame
        rotation_controls_frame = ttk.Frame(transform_frame)
        rotation_controls_frame.pack(fill=tk.X, padx=3, pady=2)

        # Rotation slider
        self.app.rotation_var = tk.IntVar()
        rotation_scale = ttk.Scale(
            rotation_controls_frame,
            from_=0,
            to=360,
            variable=self.app.rotation_var,
            orient=tk.HORIZONTAL,
            command=self.app.update_rotation_display,
        )
        rotation_scale.pack(fill=tk.X, pady=(0, 2))

        # Rotation input and apply frame using grid layout
        rotation_input_frame = ttk.Frame(rotation_controls_frame)
        rotation_input_frame.pack(fill=tk.X)

        # Rotation input box
        ttk.Label(rotation_input_frame, text="Angle:", font=("Arial", 8)).grid(
            row=0, column=0, sticky=tk.W
        )
        self.app.rotation_entry = ttk.Entry(
            rotation_input_frame, width=4, font=("Arial", 8)
        )
        self.app.rotation_entry.grid(row=0, column=1, padx=1)
        self.app.rotation_entry.bind("<Return>", self.app.on_rotation_entry_change)
        self.app.rotation_entry.bind("<FocusOut>", self.app.on_rotation_entry_change)
        self.app.rotation_entry.bind("<KeyRelease>", self.app.on_rotation_entry_change)

        # Apply rotation button
        self.app.apply_rotation_btn = tk.Button(
            rotation_input_frame,
            text="Apply",
            command=self.app.apply_rotation,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        )
        self.app.apply_rotation_btn.grid(row=0, column=2, padx=2)

        # Reset rotation button
        reset_rotation_btn = tk.Button(
            rotation_input_frame,
            text="Reset",
            command=self.app.reset_rotation,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        )
        reset_rotation_btn.grid(row=0, column=3, padx=1)

        # Configure grid weights for rotation input frame
        rotation_input_frame.columnconfigure(2, weight=1)

        # Initialize rotation display
        self.app.update_rotation_display()

        # Filters in a more compact grid layout
        filters_frame = ttk.Frame(transform_frame)
        filters_frame.pack(fill=tk.X, padx=3, pady=3)

        tk.Button(
            filters_frame,
            text="Blur",
            command=self.app.apply_blur,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        ).grid(row=0, column=0, padx=1, pady=1)
        tk.Button(
            filters_frame,
            text="Sharp",
            command=self.app.apply_sharpen,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        ).grid(row=0, column=1, padx=1, pady=1)
        tk.Button(
            filters_frame,
            text="Emboss",
            command=self.app.apply_emboss,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        ).grid(row=0, column=2, padx=1, pady=1)

        # Transparent background button
        transp_btn = tk.Button(
            filters_frame,
            text="Transp.",
            command=self.app.apply_transparent_background,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        )
        transp_btn.grid(row=1, column=0, padx=1, pady=1)
        ToolTip(
            transp_btn,
            "Make background transparent\n• Choose color with picker or use "
            "top-left pixel\n• Adjustable tolerance for precision\n"
            "• Perfect for sprites and icons",
        )

        # Remove background button
        remove_bg_btn = tk.Button(
            filters_frame,
            text="Rm BG",
            command=self.app.remove_background,
            font=("Arial", 8),
            relief="raised",
            bd=1,
            width=6,
        )
        remove_bg_btn.grid(row=1, column=1, padx=1, pady=1)
        ToolTip(
            remove_bg_btn,
            "Smart background removal\n• Choose color manually or auto-detect\n"
            "• Analyzes image corners for background\n"
            "• Adjustable tolerance for precision",
        )

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
        self.app.framework_var = tk.StringVar(value="tkinter")
        framework_combo = ttk.Combobox(
            options_frame,
            textvariable=self.app.framework_var,
            values=["tkinter", "customtkinter"],
            state="readonly",
            font=("Arial", 8),
            height=3,
        )
        framework_combo.pack(fill=tk.X, pady=1)

        ttk.Label(options_frame, text="Usage:", font=("Arial", 8)).pack(anchor=tk.W)
        self.app.usage_var = tk.StringVar(value="general")
        usage_combo = ttk.Combobox(
            options_frame,
            textvariable=self.app.usage_var,
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
        self.app.quality_var = tk.IntVar(value=85)
        quality_scale = ttk.Scale(
            options_frame,
            from_=1,
            to=100,
            variable=self.app.quality_var,
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
            command=self.app.preview_code,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(fill=tk.X, pady=1)
        tk.Button(
            btn_frame,
            text="Generate File",
            command=self.app.generate_code_file,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(fill=tk.X, pady=1)
        tk.Button(
            btn_frame,
            text="Export Images",
            command=self.app.export_images,
            font=("Arial", 8),
            relief="raised",
            bd=1,
        ).pack(fill=tk.X, pady=1)

        # Preview section - smaller height for narrow panel
        preview_frame = ttk.LabelFrame(code_frame, text="Live Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Preview canvas with scrollbar support
        preview_container = ttk.Frame(preview_frame)
        preview_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Create canvas and scrollbar
        self.app.preview_canvas = tk.Canvas(preview_container, bg="white", height=100)
        self.app.preview_scrollbar = ttk.Scrollbar(
            preview_container, orient="vertical", command=self.app.preview_canvas.yview
        )
        self.app.preview_canvas.configure(yscrollcommand=self.app.preview_scrollbar.set)

        # Add tooltip to scrollbar
        self._create_tooltip(
            self.app.preview_scrollbar,
            "Scroll through icons\n• Mouse wheel\n• Trackpad gestures\n"
            "• Drag to scroll\n• Arrow keys (↑↓ = line, ←→ = fast)",
        )

        # Pack canvas and scrollbar
        self.app.preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.app.preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initially hide scrollbar
        self.app.preview_scrollbar.pack_forget()

        # Bind framework/usage changes to update preview
        framework_combo.bind("<<ComboboxSelected>>", self.app.update_preview)
        usage_combo.bind("<<ComboboxSelected>>", self.app.update_preview)

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
