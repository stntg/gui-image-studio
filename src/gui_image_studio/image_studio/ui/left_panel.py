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

        # Create a frame for each tool (button + settings button)
        for i, (tool_name, tool_info) in enumerate(tools_info.items()):
            # Create a frame to hold both tool button and settings button
            tool_frame = ttk.Frame(tools_grid)
            tool_frame.grid(row=i // 2, column=i % 2, sticky="ew", padx=1, pady=1)

            # Get icon for the tool
            icon = icon_manager.get_icon(tool_info["icon"], size=16)

            # Create main tool button
            btn = tk.Button(
                tool_frame,
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

            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.app.tool_buttons[tool_name] = btn

            # Check if tool has settings panel
            settings_panel = self.app.drawing_tools.get_tool_settings_panel(tool_name)
            if settings_panel:
                # Create settings button with gear icon
                settings_btn = tk.Button(
                    tool_frame,
                    text="⚙",
                    command=lambda t=tool_name: self.app.open_tool_settings(t),
                    font=("Arial", 8),
                    relief="raised",
                    bd=1,
                    width=2,
                    padx=1,
                    pady=1,
                )
                settings_btn.pack(side=tk.RIGHT)

                # Add tooltip for settings button
                self._create_tooltip(
                    settings_btn, f"Settings for {tool_info['display_name']}"
                )

        tools_grid.columnconfigure(0, weight=1)
        tools_grid.columnconfigure(1, weight=1)

        # Dynamic tool settings panel
        self.app.settings_frame = ttk.LabelFrame(parent, text="Tool Settings")
        self.app.settings_frame.pack(fill=tk.X, padx=3, pady=3)

        # Initialize with default tool settings
        self.setup_tool_settings(self.app.drawing_tools.get_current_tool())

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

    def setup_tool_settings(self, tool_name: str):
        """Setup the settings panel for the specified tool."""
        # Clear existing settings widgets
        for widget in self.app.settings_frame.winfo_children():
            widget.destroy()

        # Update frame title
        tool_info = self.app.drawing_tools.get_tool_info(tool_name)
        if tool_info:
            self.app.settings_frame.configure(
                text=f"{tool_info['display_name']} Settings"
            )

        # Get tool settings panel configuration
        settings_panel = self.app.drawing_tools.get_tool_settings_panel(tool_name)
        current_settings = self.app.drawing_tools.get_tool_settings(tool_name)

        # Store references to setting variables for updates
        if not hasattr(self.app, "setting_vars"):
            self.app.setting_vars = {}
        self.app.setting_vars[tool_name] = {}

        if settings_panel:
            # Create tool-specific settings
            for setting_name, setting_config in settings_panel.items():
                self._create_setting_widget(
                    tool_name, setting_name, setting_config, current_settings
                )

        # Always include basic size and color controls
        self._create_basic_controls(tool_name, current_settings)

        # Update global size variable to match tool's size setting
        self._sync_global_size_with_tool(tool_name, current_settings)

    def _create_setting_widget(
        self, tool_name: str, setting_name: str, config: dict, current_settings: dict
    ):
        """Create a widget for a specific setting."""
        frame = ttk.Frame(self.app.settings_frame)
        frame.pack(fill=tk.X, padx=3, pady=2)

        # Label
        label_text = config.get("label", setting_name.title())
        ttk.Label(frame, text=f"{label_text}:", font=("Arial", 8)).pack(anchor=tk.W)

        if config["type"] == "slider":
            # Create slider
            current_value = current_settings.get(setting_name, config.get("default", 0))
            var = tk.IntVar(value=current_value)
            self.app.setting_vars[tool_name][setting_name] = var

            slider = ttk.Scale(
                frame,
                from_=config.get("min", 0),
                to=config.get("max", 100),
                variable=var,
                orient=tk.HORIZONTAL,
                length=150,
                command=lambda val, tn=tool_name, sn=setting_name: self._on_setting_change(
                    tn, sn, val
                ),
            )
            slider.pack(fill=tk.X, padx=3, pady=1)

            # Value label
            value_label = ttk.Label(frame, text=str(current_value), font=("Arial", 7))
            value_label.pack(anchor=tk.E)

            # Update value label when slider changes
            def update_label(val, label=value_label):
                label.configure(text=str(int(float(val))))

            var.trace_add("write", lambda *args, ul=update_label, v=var: ul(v.get()))

        elif config["type"] == "checkbox":
            # Create checkbox
            current_value = current_settings.get(
                setting_name, config.get("default", False)
            )
            var = tk.BooleanVar(value=current_value)
            self.app.setting_vars[tool_name][setting_name] = var

            checkbox = ttk.Checkbutton(
                frame,
                text=label_text,
                variable=var,
                command=lambda tn=tool_name, sn=setting_name, v=var: self._on_setting_change(
                    tn, sn, v.get()
                ),
            )
            checkbox.pack(anchor=tk.W, padx=3, pady=1)

            # Remove the label since checkbox has its own text
            frame.winfo_children()[0].destroy()  # Remove the label we created earlier

        elif config["type"] == "dropdown":
            # Create dropdown/combobox
            current_value = current_settings.get(
                setting_name, config.get("default", "")
            )
            var = tk.StringVar(value=current_value)
            self.app.setting_vars[tool_name][setting_name] = var

            options = config.get("options", [])
            dropdown = ttk.Combobox(
                frame,
                textvariable=var,
                values=options,
                state="readonly",
                font=("Arial", 8),
                width=15,
            )
            dropdown.pack(fill=tk.X, padx=3, pady=1)

            # Bind selection event
            dropdown.bind(
                "<<ComboboxSelected>>",
                lambda e, tn=tool_name, sn=setting_name, v=var: self._on_setting_change(
                    tn, sn, v.get()
                ),
            )

        elif config["type"] == "color":
            # Create color picker button
            current_value = current_settings.get(
                setting_name, config.get("default", "#000000")
            )
            var = tk.StringVar(value=current_value)
            self.app.setting_vars[tool_name][setting_name] = var

            color_btn_frame = ttk.Frame(frame)
            color_btn_frame.pack(fill=tk.X, padx=3, pady=1)

            color_button = tk.Button(
                color_btn_frame,
                bg=current_value,
                width=4,
                height=1,
                command=lambda tn=tool_name, sn=setting_name, v=var, btn=None: self._choose_setting_color(
                    tn, sn, v, btn
                ),
                relief="raised",
                bd=1,
            )
            color_button.pack(side=tk.LEFT)

            # Store button reference for color updates
            color_button.configure(
                command=lambda tn=tool_name, sn=setting_name, v=var, btn=color_button: self._choose_setting_color(
                    tn, sn, v, btn
                )
            )

            # Color value label
            color_label = ttk.Label(
                color_btn_frame, text=current_value, font=("Arial", 7)
            )
            color_label.pack(side=tk.LEFT, padx=(5, 0))

    def _create_basic_controls(self, tool_name: str, current_settings: dict):
        """Create basic size and color controls."""
        # Get tool settings panel to check what settings are already handled
        settings_panel = self.app.drawing_tools.get_tool_settings_panel(tool_name)
        handled_settings = set(settings_panel.keys()) if settings_panel else set()

        # Size control - only create if tool doesn't have its own size-related setting
        size_related_settings = {
            "size",
            "font_size",
            "width",
        }  # Common size-related setting names
        has_size_setting = bool(handled_settings & size_related_settings)

        if not has_size_setting:
            size_frame = ttk.Frame(self.app.settings_frame)
            size_frame.pack(fill=tk.X, padx=3, pady=2)

            ttk.Label(size_frame, text="Size:", font=("Arial", 8)).pack(anchor=tk.W)

            current_size = self.app.drawing_tools.get_brush_size()
            if not hasattr(self.app, "size_var"):
                self.app.size_var = tk.IntVar(value=current_size)
            else:
                self.app.size_var.set(current_size)

            size_scale = ttk.Scale(
                size_frame,
                from_=1,
                to=50,
                variable=self.app.size_var,
                orient=tk.HORIZONTAL,
                length=150,
                command=lambda val: self.app.drawing_tools.set_brush_size(
                    int(float(val))
                ),
            )
            size_scale.pack(fill=tk.X, padx=3, pady=1)

        # Color control
        color_frame = ttk.Frame(self.app.settings_frame)
        color_frame.pack(fill=tk.X, padx=3, pady=3)

        ttk.Label(color_frame, text="Color:", font=("Arial", 8)).pack(side=tk.LEFT)

        if not hasattr(self.app, "color_button") or self.app.color_button is None:
            self.app.color_button = tk.Button(
                color_frame,
                bg=self.app.drawing_tools.get_brush_color(),
                width=4,
                height=1,
                command=self.app.choose_color,
            )
        else:
            # Reparent existing color button
            try:
                self.app.color_button.pack_forget()
                self.app.color_button.configure(master=color_frame)
            except tk.TclError:
                # If the button was destroyed, create a new one
                self.app.color_button = tk.Button(
                    color_frame,
                    bg=self.app.drawing_tools.get_brush_color(),
                    width=4,
                    height=1,
                    command=self.app.choose_color,
                )

        self.app.color_button.pack(side=tk.RIGHT)

    def _on_setting_change(self, tool_name: str, setting_name: str, value):
        """Handle setting value changes."""
        try:
            # Handle different value types
            if isinstance(value, bool):
                # Boolean value from checkbox
                final_value = value
            elif isinstance(value, str):
                # Check if it's a numeric string (from slider) or text string (from dropdown/color)
                try:
                    # Try to convert to number (for sliders)
                    final_value = int(float(value))
                except ValueError:
                    # It's a text string (dropdown selection, color value, etc.)
                    final_value = value
            else:
                # Direct numeric value
                final_value = value

            # Update the tool setting
            self.app.drawing_tools.set_tool_setting(
                tool_name, setting_name, final_value
            )

            # Special handling for size-related settings to keep global brush size in sync
            if setting_name in ["size", "font_size", "width"] and isinstance(
                final_value, (int, float)
            ):
                # Update global brush size when tool's size-related setting changes
                self.app.drawing_tools.set_brush_size(int(final_value))
                if hasattr(self.app, "size_var"):
                    self.app.size_var.set(int(final_value))

        except (ValueError, TypeError):
            pass  # Ignore invalid values

    def _choose_setting_color(
        self, tool_name: str, setting_name: str, var: tk.StringVar, button: tk.Button
    ):
        """Open color chooser for a specific setting."""
        from tkinter import colorchooser

        current_color = var.get()
        color = colorchooser.askcolor(color=current_color)
        if color[1]:  # color[1] is the hex value
            var.set(color[1])
            button.configure(bg=color[1])

            # Update the color label if it exists
            parent_frame = button.master
            for widget in parent_frame.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(text=color[1])
                    break

            # Update the tool setting
            self._on_setting_change(tool_name, setting_name, color[1])

    def _sync_global_size_with_tool(self, tool_name: str, current_settings: dict):
        """Sync the global size variable with the tool's size-related setting."""
        # Find the tool's size-related setting
        size_value = None
        for size_key in ["size", "font_size", "width"]:
            if size_key in current_settings:
                size_value = current_settings[size_key]
                break

        # If tool has a size setting, update global size
        if size_value is not None and isinstance(size_value, (int, float)):
            self.app.drawing_tools.set_brush_size(int(size_value))
            if hasattr(self.app, "size_var"):
                self.app.size_var.set(int(size_value))
