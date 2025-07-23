#!/usr/bin/env python3
"""
Enhanced Image Studio GUI - Refactored Main Application.
A visual tool for developers to design images/icons and generate embedded code.
Features detachable left and right panels with fixed width.
"""

import base64
import gc
import json
import os
import tempfile
import tkinter as tk
from collections import Counter
from io import BytesIO
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk
from typing import Dict, List, Optional, Tuple

# Optional memory monitoring
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageTk
from threepanewindows import (  # type: ignore[import]
    EnhancedDockableThreePaneWindow,
    PaneConfig,
)

from gui_image_studio.embedded_icons import cleanup_icon, get_icon_path
from gui_image_studio.generator import embed_images_from_folder

from .core.canvas_manager import CanvasManager
from .core.drawing_tools import DrawingToolsManager

# Import refactored components
from .core.image_manager import ImageManager
from .ui.dialogs import CodePreviewWindow, HelpWindow, ImageSizeDialog, ToolTip
from .ui.menu import MenuManager
from .ui.panels import PanelManager


class EnhancedImageDesignerGUI:
    """Main GUI application for image design and code generation."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("GUI Image Studio - Enhanced")
        self.root.geometry("1200x700")
        self.root.minsize(800, 500)

        # Application state - copied from original
        self.current_images: Dict[str, Image.Image] = {}
        self.original_images: Dict[str, Image.Image] = (
            {}
        )  # Store originals for rotation
        self.base_images: Dict[str, Image.Image] = (
            {}
        )  # Store base images (before rotation)
        self.current_rotations: Dict[str, int] = {}  # Track current rotation angles
        self.image_previews: Dict[str, ImageTk.PhotoImage] = {}
        self.selected_image: Optional[str] = None
        self.temp_dir = tempfile.mkdtemp()

        # Canvas size (moved from drawing tools)
        self.canvas_size = (300, 300)

        # UI variables that will be created by panels
        self.size_var = tk.IntVar(value=5)
        self.width_var = tk.IntVar(value=300)
        self.height_var = tk.IntVar(value=300)
        self.name_var = tk.StringVar()

        # UI widgets (will be set during UI setup)
        self.canvas: Optional[tk.Canvas] = None
        self.image_listbox: Optional[tk.Listbox] = None
        self.color_button: Optional[tk.Button] = None
        self.preview_canvas: Optional[tk.Canvas] = None
        self.grid_var: Optional[tk.BooleanVar] = None
        self.rotation_var: Optional[tk.IntVar] = None

        # Drawing state variables
        self.drawing = False
        self.last_x = 0
        self.last_y = 0
        self.start_x = 0
        self.start_y = 0
        self.preview_shape = None
        self.preview_active = False
        self.pixel_highlight = None
        self.last_highlight_pos = None

        # Code generation variables
        self.quality_var = tk.IntVar(value=95)
        self.framework_var = tk.StringVar(value="tkinter")
        self.usage_var = tk.StringVar(value="general")

        # Add trace callbacks to update preview when settings change
        self.framework_var.trace("w", lambda *args: self.update_preview())
        self.usage_var.trace("w", lambda *args: self.update_preview())
        self.quality_var.trace("w", lambda *args: self.update_preview())

        # Icon paths for cleanup
        self.icon_paths: List[str] = []

        # Initialize managers first
        self.image_manager = ImageManager()
        self.drawing_tools = DrawingToolsManager()
        self.canvas_manager = CanvasManager(self)
        self.menu_manager = MenuManager(self)
        self.panel_manager = PanelManager(self)

        # Drawing state
        self.drawing_tools.show_grid = False
        self.drawing = False
        self.start_x = 0
        self.start_y = 0

        # Shape preview state
        self.preview_shape = None  # Canvas item ID for preview shape
        self.preview_active = False

        # Pixel highlight for precise drawing
        self.pixel_highlight = None  # Canvas item ID for pixel highlight
        self.last_highlight_pos = None  # Track last highlighted position

        # Cursor settings - copied from original
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

        self.tool_buttons = {}  # Dictionary to store tool button references

        # Load cursor settings from file if exists
        self.load_cursor_settings()

        self.setup_ui()
        self.setup_bindings()
        self.setup_preview_bindings()

        # Initialize default tool
        self.select_tool("brush")

        # Initialize UI state
        self.update_ui_state()
        self.update_canvas()  # Show initial instructions
        self.update_preview()  # Show initial preview

        # Center the window on the desktop
        self.center_window()

        # Set up proper cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self) -> None:
        """Center the window on the desktop."""
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

    def setup_button_styles(self) -> None:
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

    def setup_ui(self) -> None:
        """Setup the enhanced user interface with threepanewindows."""
        # Create menu bar first
        self.menu_manager.setup_menu()

        # Configure custom button styles for prominence
        self.setup_button_styles()

        # Configure pane configurations with embedded icons
        tools_icon = get_icon_path("tools")
        canvas_icon = get_icon_path("canvas")
        settings_icon = get_icon_path("settings")

        # Track icon paths for cleanup
        self.icon_paths.extend([tools_icon, canvas_icon, settings_icon])

        left_config = PaneConfig(
            title="Tools & Images",
            icon="🛠️",
            window_icon=tools_icon,
            custom_titlebar=True,
            custom_titlebar_shadow=True,
            detached_height=600,  # Fixed height for detached window
            detached_scrollable=True,  # Enable scrollbars if content is too tall
            min_width=200,
            max_width=200,
            default_width=200,
            fixed_width=200,
            resizable=False,
            detachable=True,
            closable=False,
        )

        center_config = PaneConfig(
            title="Canvas",
            icon="🎨",
            window_icon=canvas_icon,
            resizable=True,
            detachable=False,
            closable=False,
        )

        right_config = PaneConfig(
            title="Properties & Code",
            icon="⚙️",
            window_icon=settings_icon,
            custom_titlebar=True,
            custom_titlebar_shadow=False,  # No shadow for this panel
            detached_height=500,  # Different height for this panel
            detached_scrollable=True,
            min_width=200,
            max_width=200,
            default_width=200,
            fixed_width=200,
            resizable=False,
            detachable=True,
            closable=False,
        )

        # Create the enhanced three-pane window
        self.three_pane = EnhancedDockableThreePaneWindow(
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

    def build_left_panel(self, parent) -> None:
        """Build the left panel with tools and image management."""
        self.panel_manager.setup_left_panel(parent)
        # Update the image list and restore selection after the panel is rebuilt (e.g., after detach/reattach)
        self.root.after_idle(self._restore_left_panel_state)

    def _restore_left_panel_state(self) -> None:
        """Restore the left panel state after it's been rebuilt (detach/reattach)."""
        # Update the image list
        self.update_image_list()

        # Restore the selected image if there was one
        if self.selected_image and hasattr(self, "image_listbox"):
            try:
                items = list(self.current_images.keys())
                if self.selected_image in items:
                    index = items.index(self.selected_image)
                    self.image_listbox.selection_clear(0, tk.END)
                    self.image_listbox.selection_set(index)
                    self.image_listbox.see(index)
            except Exception as e:
                print(f"Error restoring image selection: {e}")

    def build_center_panel(self, parent) -> None:
        """Build the center panel with the drawing canvas."""
        self.panel_manager.setup_center_panel(parent)

    def build_right_panel(self, parent) -> None:
        """Build the right panel with properties and code generation."""
        self.panel_manager.setup_right_panel(parent)
        # Restore the right panel state after it's been rebuilt (detach/reattach)
        self.root.after_idle(self._restore_right_panel_state)

    def _restore_right_panel_state(self) -> None:
        """Restore the right panel state after it's been rebuilt (detach/reattach)."""
        # Update the properties if there's a selected image
        if self.selected_image and self.selected_image in self.current_images:
            image = self.current_images[self.selected_image]
            if hasattr(self, "width_var"):
                self.width_var.set(image.width)
            if hasattr(self, "height_var"):
                self.height_var.set(image.height)
            if hasattr(self, "name_var"):
                self.name_var.set(self.selected_image)

        # Update the preview
        self.update_preview()

    def setup_bindings(self):
        """Setup keyboard and mouse bindings."""
        # Keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_image())
        self.root.bind("<Control-o>", lambda e: self.load_image())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<KeyPress-g>", lambda e: self.toggle_grid())
        self.root.bind("<KeyPress-plus>", lambda e: self.zoom_in())
        self.root.bind("<KeyPress-minus>", lambda e: self.zoom_out())
        self.root.bind("<KeyPress-0>", lambda e: self.reset_zoom())

        # Help system key bindings
        self.root.bind("<F1>", lambda e: self.show_help())
        self.root.bind("<Control-F1>", lambda e: self.start_tutorial())

        # Tool selection key bindings
        self.root.bind(
            "<KeyPress-b>", lambda e: self.drawing_tools.select_tool("brush")
        )
        self.root.bind(
            "<KeyPress-p>", lambda e: self.drawing_tools.select_tool("pencil")
        )
        self.root.bind(
            "<KeyPress-e>", lambda e: self.drawing_tools.select_tool("eraser")
        )
        self.root.bind("<KeyPress-l>", lambda e: self.drawing_tools.select_tool("line"))
        self.root.bind(
            "<KeyPress-r>", lambda e: self.drawing_tools.select_tool("rectangle")
        )
        self.root.bind(
            "<KeyPress-c>", lambda e: self.drawing_tools.select_tool("circle")
        )
        self.root.bind("<KeyPress-t>", lambda e: self.drawing_tools.select_tool("text"))
        self.root.bind("<KeyPress-f>", lambda e: self.drawing_tools.select_tool("fill"))
        self.root.bind(
            "<KeyPress-s>", lambda e: self.drawing_tools.select_tool("spray")
        )
        self.root.bind(
            "<KeyPress-m>", lambda e: self.drawing_tools.select_tool("marker")
        )
        self.root.bind(
            "<KeyPress-h>", lambda e: self.drawing_tools.select_tool("highlighter")
        )

        # Image listbox binding is set up in panels.py

    def select_tool(self, tool):
        """Select a drawing tool."""
        # Clear any active preview when switching tools
        if hasattr(self, "canvas_manager"):
            self.canvas_manager.clear_preview()
            self.canvas_manager.clear_pixel_highlight()
        self.drawing = False

        # Use the tool manager to select the tool
        success = self.drawing_tools.select_tool(tool)
        if not success:
            print(f"Warning: Tool '{tool}' not found in registry")
            return

        # Update button states
        if hasattr(self, "tool_buttons"):
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
        if not hasattr(self, "canvas") or self.canvas is None:
            return

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

        return base_options.get(tool, ["crosshair", "arrow"])

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
                f"Warning: Unexpected error loading cursor settings: {e}. "
                "Using defaults."
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
        if messagebox.askyesno(
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
            self.update_tool_cursor(self.drawing_tools.get_current_tool())
            messagebox.showinfo(
                "Settings Reset", "Cursor settings have been reset to defaults."
            )

    def open_cursor_settings(self):
        """Open the cursor settings dialog."""
        # Placeholder - would need to implement CursorSettingsDialog
        messagebox.showinfo(
            "Cursor Settings",
            "Cursor settings dialog not yet implemented in refactored version.",
        )

    def choose_color(self):
        """Open color chooser dialog."""
        from tkinter import colorchooser

        color = colorchooser.askcolor(color=self.drawing_tools.get_brush_color())
        if color[1]:
            self.drawing_tools.set_brush_color(color[1])
            if hasattr(self, "color_button"):
                self.color_button.configure(bg=self.drawing_tools.get_brush_color())

    def update_ui_state(self):
        """Update UI state based on current selection."""
        # Placeholder for UI state updates
        pass

    def update_canvas(self):
        """Update the canvas display."""
        # Clear any active preview shapes and pixel highlights
        if hasattr(self, "canvas_manager"):
            self.canvas_manager.clear_preview()
            self.canvas_manager.clear_pixel_highlight()

        if not self.selected_image:
            # Clear canvas and show instructions
            if hasattr(self, "canvas"):
                self.canvas.delete("all")
                self.show_canvas_instructions()
            return

        image = self.current_images[self.selected_image]

        # Check if image is too large to process safely
        max_image_size = 4096  # Maximum original image dimension
        if image.width > max_image_size or image.height > max_image_size:
            # Show error and clear canvas
            if hasattr(self, "canvas"):
                self.canvas.delete("all")
                self.canvas.create_text(
                    200,
                    200,
                    text=f"Image too large to display safely\n({image.width}x{image.height})\nMaximum size: {max_image_size}x{max_image_size}",
                    fill="red",
                    font=("Arial", 12),
                    anchor=tk.CENTER,
                )
            return

        # Clean up old PhotoImage to prevent memory leaks
        if self.selected_image in self.image_previews:
            old_photo = self.image_previews[self.selected_image]
            # Force garbage collection of the old PhotoImage
            del old_photo

        # Create display image with zoom
        display_size = (
            int(image.width * self.drawing_tools.get_zoom_level()),
            int(image.height * self.drawing_tools.get_zoom_level()),
        )

        # Limit maximum display size to prevent memory issues
        max_display_size = 2048  # Maximum dimension in pixels
        if display_size[0] > max_display_size or display_size[1] > max_display_size:
            # Calculate scaling factor to fit within max size
            scale_factor = min(
                max_display_size / display_size[0], max_display_size / display_size[1]
            )
            display_size = (
                int(display_size[0] * scale_factor),
                int(display_size[1] * scale_factor),
            )

        try:
            display_image = image.resize(display_size, Image.NEAREST)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            self.image_previews[self.selected_image] = photo

            # Clean up the temporary display_image to free memory
            del display_image

        except MemoryError:
            # Handle memory error gracefully
            if hasattr(self, "canvas"):
                self.canvas.delete("all")
                self.canvas.create_text(
                    200,
                    200,
                    text="Not enough memory to display image\nTry reducing zoom level or image size",
                    fill="red",
                    font=("Arial", 12),
                    anchor=tk.CENTER,
                )
            # Reset zoom to a safer level
            self.drawing_tools.set_zoom_level(1.0)
            return
        except Exception as e:
            # Handle other errors
            if hasattr(self, "canvas"):
                self.canvas.delete("all")
                self.canvas.create_text(
                    200,
                    200,
                    text=f"Error displaying image:\n{str(e)}",
                    fill="red",
                    font=("Arial", 12),
                    anchor=tk.CENTER,
                )
            return

        # Clear and update canvas
        if hasattr(self, "canvas"):
            self.canvas.delete("all")
            self.canvas.create_image(10, 10, anchor=tk.NW, image=photo)

            # Draw grid if enabled
            if (
                self.drawing_tools.show_grid
                and self.drawing_tools.get_zoom_level() >= 4
            ):
                self.draw_grid(display_size)

            # Update scroll region
            self.canvas.configure(
                scrollregion=(0, 0, display_size[0] + 20, display_size[1] + 20)
            )

        # Update preview when canvas changes
        if hasattr(self, "preview_canvas"):
            self.root.after_idle(self.update_preview)

        # Periodic memory cleanup (every 10th canvas update)
        if not hasattr(self, "_cleanup_counter"):
            self._cleanup_counter = 0
        self._cleanup_counter += 1
        if self._cleanup_counter >= 10:
            self._cleanup_counter = 0
            self.root.after_idle(self.cleanup_memory)

    def show_canvas_instructions(self):
        """Show instructions on empty canvas."""
        if not hasattr(self, "canvas"):
            return

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

    def draw_grid(self, display_size):
        """Draw grid on the canvas."""
        if not hasattr(self, "canvas"):
            return

        grid_spacing = max(1, int(self.drawing_tools.get_zoom_level()))

        # Draw vertical lines
        for x in range(10, display_size[0] + 10, grid_spacing):
            self.canvas.create_line(
                x, 10, x, display_size[1] + 10, fill="#e0e0e0", width=1
            )

        # Draw horizontal lines
        for y in range(10, display_size[1] + 10, grid_spacing):
            self.canvas.create_line(
                10, y, display_size[0] + 10, y, fill="#e0e0e0", width=1
            )

    def cleanup_memory(self):
        """Cleanup memory periodically."""
        gc.collect()

    def on_image_select(self, event):
        """Handle image selection from listbox."""
        if hasattr(self, "image_listbox"):
            selection = self.image_listbox.curselection()
            if selection:
                name = self.image_listbox.get(selection[0])
                self.select_image(name)

    def select_image(self, name):
        """Select an image."""
        if name in self.current_images:
            self.selected_image = name
            self.update_canvas()
            self.update_preview()

            # Update properties
            image = self.current_images[name]
            if hasattr(self, "width_var"):
                self.width_var.set(image.width)
            if hasattr(self, "height_var"):
                self.height_var.set(image.height)
            if hasattr(self, "name_var"):
                self.name_var.set(name)

            # Update listbox selection
            if hasattr(self, "image_listbox"):
                try:
                    # Find the index of the selected image
                    items = list(self.current_images.keys())
                    if name in items:
                        index = items.index(name)
                        self.image_listbox.selection_clear(0, tk.END)
                        self.image_listbox.selection_set(index)
                        self.image_listbox.see(index)
                except Exception as e:
                    print(f"Error updating listbox selection: {e}")

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

    def on_image_select(self, event):
        """Handle image selection from listbox."""
        if hasattr(self, "image_listbox"):
            selection = self.image_listbox.curselection()
            if selection:
                name = self.image_listbox.get(selection[0])
                self.select_image(name)

    # Canvas event handlers are handled by CanvasManager

    # Drawing methods
    def draw_on_image(self, x, y):
        """Draw on the current image using the new tool system."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]

        # Use the new tool system
        kwargs = {
            "size": self.size_var.get(),
            "root": self.root,  # For text tool dialog
        }

        self.drawing_tools.handle_click(image, x, y, **kwargs)
        self.update_canvas()

    def draw_line_on_image(self, x1, y1, x2, y2):
        """Draw a line on the current image using the new tool system."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]

        # Use the new tool system
        kwargs = {"size": self.size_var.get(), "root": self.root}

        self.drawing_tools.handle_drag(image, x1, y1, x2, y2, **kwargs)
        self.update_canvas()

    def draw_shape(self, x1, y1, x2, y2):
        """Draw a shape on the current image using the new tool system."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]

        # Use the new tool system
        kwargs = {
            "size": self.size_var.get(),
            "width": self.size_var.get(),  # For line width
            "root": self.root,
        }

        self.drawing_tools.handle_release(image, x1, y1, x2, y2, **kwargs)
        self.update_canvas()

    def add_text(self, x, y):
        """Add text to the current image."""
        if not self.selected_image:
            return

        # Simple text input dialog
        from tkinter import simpledialog

        text = simpledialog.askstring("Add Text", "Enter text:")
        if text:
            image = self.current_images[self.selected_image]
            draw = ImageDraw.Draw(image)

            try:
                # Try to use a default font with size based on brush size
                font_size = max(12, self.size_var.get() * 2)
                from PIL import ImageFont

                font = ImageFont.load_default()
            except (OSError, IOError, ImportError) as e:
                # Font loading failed, use None (PIL will use built-in font)
                print(f"Warning: Could not load default font: {e}")
                font = None

            draw.text(
                (x, y), text, fill=self.drawing_tools.get_brush_color(), font=font
            )
            self.update_canvas()

    # Preview and highlight methods
    def update_shape_preview(self, x1, y1, x2, y2):
        """Update the preview shape on canvas."""
        # Clear existing preview
        self.clear_preview()

        # Convert image coordinates back to canvas coordinates for display
        canvas_x1 = x1 * self.drawing_tools.get_zoom_level() + 10
        canvas_y1 = y1 * self.drawing_tools.get_zoom_level() + 10
        canvas_x2 = x2 * self.drawing_tools.get_zoom_level() + 10
        canvas_y2 = y2 * self.drawing_tools.get_zoom_level() + 10

        # Create preview shape using new tool system
        preview_id = self.drawing_tools.create_preview(self.canvas, x1, y1, x2, y2)
        if preview_id:
            self.preview_shape = preview_id
        else:
            # Fallback for tools that don't support preview
            self.preview_shape = None

        self.preview_active = True

    def clear_preview(self):
        """Clear the preview shape from canvas."""
        if not hasattr(self, "canvas") or self.canvas is None:
            return
        if hasattr(self, "preview_shape") and self.preview_shape:
            self.canvas.delete(self.preview_shape)
            self.preview_shape = None
        self.preview_active = False

    def update_pixel_highlight(self, x, y):
        """Highlight the pixel that will be affected by drawing tools."""
        # Check if canvas is available
        if not hasattr(self, "canvas") or self.canvas is None:
            return

        # Only highlight if position changed
        if hasattr(self, "last_highlight_pos") and self.last_highlight_pos == (x, y):
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
        canvas_x = x * self.drawing_tools.get_zoom_level() + 10
        canvas_y = y * self.drawing_tools.get_zoom_level() + 10

        # Create highlight rectangle around the pixel
        self.pixel_highlight = self.canvas.create_rectangle(
            canvas_x,
            canvas_y,
            canvas_x + self.drawing_tools.get_zoom_level(),
            canvas_y + self.drawing_tools.get_zoom_level(),
            outline="#FF0000",
            width=1,
            fill="",
            dash=(2, 2),
            tags="pixel_highlight",
        )

    def clear_pixel_highlight(self):
        """Clear the pixel highlight from canvas."""
        if not hasattr(self, "canvas") or self.canvas is None:
            return
        if hasattr(self, "pixel_highlight") and self.pixel_highlight:
            self.canvas.delete(self.pixel_highlight)
            self.pixel_highlight = None
        if hasattr(self, "last_highlight_pos"):
            self.last_highlight_pos = None

    def update_preview(self, event=None):
        """Update the live preview based on current settings."""
        if not hasattr(self, "preview_canvas"):
            return

        # Clear previous preview
        self.preview_canvas.delete("all")

        # Clear old image references to prevent memory leaks
        if hasattr(self, "_preview_refs"):
            self._preview_refs.clear()
        else:
            self._preview_refs = []

        if not self.current_images:
            # Show placeholder when no images
            self._show_preview_placeholder("Create images to see preview")
            return

        # Get current settings
        framework = getattr(self, "framework_var", tk.StringVar(value="tkinter")).get()
        usage = getattr(self, "usage_var", tk.StringVar(value="general")).get()

        try:
            # Generate preview based on usage type
            if usage == "buttons":
                self.preview_buttons()
            elif usage == "icons":
                self.preview_icons()
            elif usage == "backgrounds":
                self.preview_backgrounds()
            elif usage == "sprites":
                self.preview_sprites()
            elif usage == "ui_elements":
                self.preview_ui_elements()
            else:
                self.preview_general()

            # Update scrollbar visibility
            self._update_preview_scrollbar()

        except Exception as e:
            print(f"Error generating preview: {e}")
            self._show_preview_placeholder("Preview generation error", color="#ff0000")

    def _show_preview_placeholder(self, text, color="#888888"):
        """Show placeholder text in preview canvas."""
        try:
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()

            if canvas_width <= 1:
                # Canvas not ready, try again later
                self.root.after(
                    100, lambda: self._show_preview_placeholder(text, color)
                )
                return

            center_x = canvas_width // 2
            center_y = canvas_height // 2

            self.preview_canvas.create_text(
                center_x,
                center_y,
                text=text,
                fill=color,
                font=("Arial", 9),
                justify=tk.CENTER,
            )
        except Exception as e:
            print(f"Error showing placeholder: {e}")

    def _update_preview_scrollbar(self):
        """Update scrollbar visibility based on content."""
        try:
            # Update scroll region
            bbox = self.preview_canvas.bbox("all")
            if bbox:
                # Add some padding to the scroll region
                padded_bbox = (bbox[0] - 5, bbox[1] - 5, bbox[2] + 5, bbox[3] + 5)
                self.preview_canvas.configure(scrollregion=padded_bbox)

                # Check if scrollbar is needed
                content_height = bbox[3] - bbox[1]
                canvas_height = self.preview_canvas.winfo_height()

                if content_height > canvas_height - 10:  # Account for padding
                    # Show scrollbar if it exists
                    if hasattr(self, "preview_scrollbar"):
                        self.preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                else:
                    # Hide scrollbar if it exists
                    if hasattr(self, "preview_scrollbar"):
                        self.preview_scrollbar.pack_forget()
            else:
                # No content, reset scroll region and hide scrollbar
                self.preview_canvas.configure(scrollregion=(0, 0, 0, 0))
                if hasattr(self, "preview_scrollbar"):
                    self.preview_scrollbar.pack_forget()

        except Exception as e:
            print(f"Error updating scrollbar: {e}")

    def _on_preview_mousewheel(self, event):
        """Handle mouse wheel scrolling in preview canvas."""
        try:
            if hasattr(self, "preview_canvas"):
                # Check if there's content to scroll
                bbox = self.preview_canvas.bbox("all")
                if bbox:
                    content_height = bbox[3] - bbox[1]
                    canvas_height = self.preview_canvas.winfo_height()

                    if content_height > canvas_height:
                        # Scroll the canvas
                        self.preview_canvas.yview_scroll(
                            int(-1 * (event.delta / 120)), "units"
                        )
        except Exception as e:
            print(f"Error handling mousewheel: {e}")

    def setup_preview_bindings(self):
        """Set up preview canvas event bindings."""
        try:
            # Wait a bit for UI to be fully initialized
            self.root.after(100, self._setup_preview_bindings_delayed)
        except Exception as e:
            print(f"Error setting up preview bindings: {e}")

    def _setup_preview_bindings_delayed(self):
        """Set up preview canvas bindings after UI is ready."""
        try:
            if hasattr(self, "preview_canvas"):
                # Bind mouse wheel scrolling
                self.preview_canvas.bind("<MouseWheel>", self._on_preview_mousewheel)
                self.preview_canvas.bind(
                    "<Button-4>",
                    lambda e: self._on_preview_mousewheel(
                        type("Event", (), {"delta": 120})()
                    ),
                )
                self.preview_canvas.bind(
                    "<Button-5>",
                    lambda e: self._on_preview_mousewheel(
                        type("Event", (), {"delta": -120})()
                    ),
                )

                # Make canvas focusable for keyboard events
                self.preview_canvas.configure(highlightthickness=0)

                print("Preview canvas bindings set up successfully")
            else:
                # Try again later if preview_canvas not ready
                self.root.after(200, self._setup_preview_bindings_delayed)
        except Exception as e:
            print(f"Error in delayed preview bindings setup: {e}")

    def on_drawing_complete(self):
        """Called when a drawing operation is completed."""
        try:
            # Update preview after drawing operations
            self.update_preview()
        except Exception as e:
            print(f"Error updating preview after drawing: {e}")

    def on_image_modified(self):
        """Called when an image is modified in any way."""
        try:
            # Update preview when image is modified
            self.update_preview()
        except Exception as e:
            print(f"Error updating preview after image modification: {e}")

    # Panel toggle methods
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

    # Code generation methods
    def generate_python_code(self):
        """Generate Python code for images."""
        messagebox.showinfo(
            "Code Generation",
            "Python code generation not yet implemented in refactored version.",
        )

    def generate_tkinter_code(self):
        """Generate Tkinter code for images."""
        messagebox.showinfo(
            "Code Generation",
            "Tkinter code generation not yet implemented in refactored version.",
        )

    def preview_code(self):
        """Preview the generated embedded code."""
        if not self.current_images:
            messagebox.showwarning("Warning", "No images to generate code for")
            return

        try:
            framework = self.framework_var.get()
            usage = self.usage_var.get()
            quality = self.quality_var.get()

            # Generate embedded images dictionary
            embedded_images = {}
            for name, image in self.current_images.items():
                # Convert to bytes
                buffer = BytesIO()
                image.save(buffer, format="PNG", quality=quality)
                image_bytes = buffer.getvalue()

                # Encode to base64
                encoded = base64.b64encode(image_bytes).decode("utf-8")
                embedded_images[name] = encoded

            # Generate code based on framework and usage
            code = self._generate_code_content(embedded_images, framework, usage)

            # Show in preview window
            CodePreviewWindow(self.root, f"Code Preview - {framework} ({usage})", code)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code preview: {str(e)}")

    def _generate_code_content(self, embedded_images, framework, usage):
        """Generate the actual code content."""
        code = f"# Generated {framework} code for {usage}\n"
        code += f"# Generated by GUI Image Studio\n\n"

        if framework == "tkinter":
            code += "import tkinter as tk\n"
            code += "from tkinter import ttk\n"
        else:
            code += "import customtkinter as ctk\n"

        code += "import base64\n"
        code += "from io import BytesIO\n"
        code += "from PIL import Image, ImageTk\n\n"

        # Add embedded images dictionary
        code += "# Embedded images dictionary\n"
        code += "embedded_images = {\n"
        for name, data in embedded_images.items():
            code += f'    "{name}": "{data}",\n'
        code += "}\n\n"

        # Add helper functions
        code += "def load_image(name, size=None):\n"
        code += '    """Load an embedded image by name."""\n'
        code += "    if name not in embedded_images:\n"
        code += "        return None\n"
        code += "    \n"
        code += "    # Decode base64 data\n"
        code += "    image_data = base64.b64decode(embedded_images[name])\n"
        code += "    image = Image.open(BytesIO(image_data))\n"
        code += "    \n"
        code += "    # Resize if requested\n"
        code += "    if size:\n"
        code += "        image = image.resize(size, Image.Resampling.LANCZOS)\n"
        code += "    \n"
        code += "    return ImageTk.PhotoImage(image)\n\n"

        # Add usage-specific examples
        if usage == "buttons":
            code += self._generate_button_examples(framework)
        elif usage == "icons":
            code += self._generate_icon_examples(framework)
        elif usage == "backgrounds":
            code += self._generate_background_examples(framework)
        else:
            code += self._generate_general_examples(framework)

        return code

    def _generate_button_examples(self, framework):
        """Generate button usage examples."""
        if framework == "tkinter":
            return """# Example: Using images in buttons
def create_button_with_image(parent, image_name, text="", command=None):
    image = load_image(image_name, size=(32, 32))
    button = tk.Button(
        parent,
        text=text,
        image=image,
        compound=tk.LEFT,
        command=command
    )
    button.image = image  # Keep reference
    return button

# Usage example:
# root = tk.Tk()
# button = create_button_with_image(root, "your_image_name", "Click me")
# button.pack()
"""
        else:
            return """# Example: Using images in CustomTkinter buttons
def create_button_with_image(parent, image_name, text="", command=None):
    image = load_image(image_name, size=(32, 32))
    button = ctk.CTkButton(
        parent,
        text=text,
        image=image,
        compound="left",
        command=command
    )
    return button

# Usage example:
# root = ctk.CTk()
# button = create_button_with_image(root, "your_image_name", "Click me")
# button.pack()
"""

    def _generate_icon_examples(self, framework):
        """Generate icon usage examples."""
        return """# Example: Using images as icons
def create_icon_label(parent, image_name, size=(24, 24)):
    image = load_image(image_name, size=size)
    label = tk.Label(parent, image=image)
    label.image = image  # Keep reference
    return label

# Usage example:
# icon = create_icon_label(parent, "your_icon_name")
# icon.pack()
"""

    def _generate_background_examples(self, framework):
        """Generate background usage examples."""
        return """# Example: Using images as backgrounds
def set_background_image(widget, image_name):
    image = load_image(image_name)
    widget.configure(image=image)
    widget.image = image  # Keep reference

# Usage example:
# canvas = tk.Canvas(root, width=400, height=300)
# bg_image = load_image("your_background_name")
# canvas.create_image(0, 0, anchor="nw", image=bg_image)
# canvas.image = bg_image  # Keep reference
"""

    def _generate_general_examples(self, framework):
        """Generate general usage examples."""
        return """# Example: General image usage
def display_image(parent, image_name, size=None):
    image = load_image(image_name, size=size)
    label = tk.Label(parent, image=image)
    label.image = image  # Keep reference
    return label

# Usage example:
# image_widget = display_image(parent, "your_image_name", size=(100, 100))
# image_widget.pack()
"""

    def generate_code_file(self):
        """Generate the embedded code file."""
        if not self.current_images:
            messagebox.showwarning("Warning", "No images to generate code for")
            return

        try:
            framework = self.framework_var.get()
            usage = self.usage_var.get()
            quality = self.quality_var.get()

            # Ask user for save location
            filename = filedialog.asksaveasfilename(
                title="Save Generated Code",
                defaultextension=".py",
                filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            )

            if not filename:
                return

            # Generate embedded images dictionary
            embedded_images = {}
            for name, image in self.current_images.items():
                buffer = BytesIO()
                image.save(buffer, format="PNG", quality=quality)
                image_bytes = buffer.getvalue()
                encoded = base64.b64encode(image_bytes).decode("utf-8")
                embedded_images[name] = encoded

            # Generate code
            code = self._generate_code_content(embedded_images, framework, usage)

            # Save to file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)

            messagebox.showinfo(
                "Code Generated", f"Code successfully saved to:\n{filename}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code file: {str(e)}")

    # Help and About methods
    def show_quick_start(self):
        """Show quick start guide."""
        messagebox.showinfo(
            "Help", "Quick start guide not yet implemented in refactored version."
        )

    def show_tools_help(self):
        """Show drawing tools help."""
        messagebox.showinfo(
            "Help", "Tools help not yet implemented in refactored version."
        )

    def show_info_help(self):
        """Show image information help."""
        messagebox.showinfo(
            "Help", "Info help not yet implemented in refactored version."
        )

    def show_transparency_help(self):
        """Show transparency features help."""
        messagebox.showinfo(
            "Help", "Transparency help not yet implemented in refactored version."
        )

    def show_code_help(self):
        """Show code generation help."""
        messagebox.showinfo(
            "Help", "Code help not yet implemented in refactored version."
        )

    def show_shortcuts(self):
        """Show keyboard shortcuts."""
        messagebox.showinfo(
            "Help", "Shortcuts help not yet implemented in refactored version."
        )

    def show_tips(self):
        """Show tips and tricks."""
        messagebox.showinfo("Help", "Tips not yet implemented in refactored version.")

    def show_troubleshooting(self):
        """Show troubleshooting guide."""
        messagebox.showinfo(
            "Help", "Troubleshooting not yet implemented in refactored version."
        )

    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About", "About dialog not yet implemented in refactored version."
        )

    # Image adjustment methods
    def apply_blur(self):
        """Apply blur filter to current image."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        try:
            image = self.current_images[self.selected_image]
            blurred = image.filter(ImageFilter.GaussianBlur(radius=1))
            self.current_images[self.selected_image] = blurred
            self.update_canvas()
            self.update_preview()
            messagebox.showinfo("Filter Applied", "Blur filter applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply blur filter: {str(e)}")

    def apply_sharpen(self):
        """Apply sharpen filter to current image."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        try:
            image = self.current_images[self.selected_image]
            sharpened = image.filter(ImageFilter.SHARPEN)
            self.current_images[self.selected_image] = sharpened
            self.update_canvas()
            self.update_preview()
            messagebox.showinfo(
                "Filter Applied", "Sharpen filter applied successfully!"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply sharpen filter: {str(e)}")

    def apply_emboss(self):
        """Apply emboss filter to current image."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        try:
            image = self.current_images[self.selected_image]
            embossed = image.filter(ImageFilter.EMBOSS)
            self.current_images[self.selected_image] = embossed
            self.update_canvas()
            self.update_preview()
            messagebox.showinfo("Filter Applied", "Emboss filter applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply emboss filter: {str(e)}")

    def apply_transparent_background(self):
        """Make background transparent."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        try:
            image = self.current_images[self.selected_image]

            # Convert to RGBA if not already
            if image.mode != "RGBA":
                image = image.convert("RGBA")

            # Ask user to choose background color method
            choice = messagebox.askyesnocancel(
                "Background Color Selection",
                "Choose background color method:\n\n"
                "Yes - Use color picker to select color\n"
                "No - Use top-left pixel color\n"
                "Cancel - Cancel operation",
            )

            if choice is None:  # Cancel
                return
            elif choice:  # Yes - color picker
                color = colorchooser.askcolor(title="Select Background Color")
                if not color[0]:  # User cancelled color picker
                    return
                bg_color = tuple(int(c) for c in color[0])
            else:  # No - use top-left pixel
                bg_color = image.getpixel((0, 0))[:3]  # Get RGB only

            # Ask for tolerance
            tolerance = simpledialog.askinteger(
                "Tolerance",
                "Enter color tolerance (0-100):\n"
                "Lower values = exact color match\n"
                "Higher values = broader color range",
                initialvalue=30,
                minvalue=0,
                maxvalue=100,
            )

            if tolerance is None:
                return

            # Apply transparency
            data = image.getdata()
            new_data = []

            for pixel in data:
                # Calculate color distance
                if len(pixel) >= 3:
                    r, g, b = pixel[:3]
                    distance = (
                        (r - bg_color[0]) ** 2
                        + (g - bg_color[1]) ** 2
                        + (b - bg_color[2]) ** 2
                    ) ** 0.5

                    # If within tolerance, make transparent
                    if distance <= tolerance * 2.55:  # Scale tolerance to 0-255 range
                        new_data.append((r, g, b, 0))  # Transparent
                    else:
                        new_data.append(pixel if len(pixel) == 4 else (r, g, b, 255))
                else:
                    new_data.append(pixel)

            # Create new image with transparency
            transparent_image = Image.new("RGBA", image.size)
            transparent_image.putdata(new_data)

            self.current_images[self.selected_image] = transparent_image
            self.update_canvas()
            self.update_preview()

            messagebox.showinfo(
                "Transparency Applied",
                f"Background color {bg_color} made transparent with tolerance {tolerance}",
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply transparency: {str(e)}")

    def remove_background(self):
        """Remove background from image."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        try:
            image = self.current_images[self.selected_image]

            # Convert to RGBA if not already
            if image.mode != "RGBA":
                image = image.convert("RGBA")

            # Ask user for background detection method
            choice = messagebox.askyesnocancel(
                "Background Detection",
                "Choose background detection method:\n\n"
                "Yes - Auto-detect from image corners\n"
                "No - Manual color selection\n"
                "Cancel - Cancel operation",
            )

            if choice is None:  # Cancel
                return
            elif choice:  # Yes - auto-detect
                # Sample corners to find most common background color
                width, height = image.size
                corner_pixels = [
                    image.getpixel((0, 0))[:3],  # Top-left
                    image.getpixel((width - 1, 0))[:3],  # Top-right
                    image.getpixel((0, height - 1))[:3],  # Bottom-left
                    image.getpixel((width - 1, height - 1))[:3],  # Bottom-right
                ]

                # Find most common corner color
                color_counts = Counter(corner_pixels)
                bg_color = color_counts.most_common(1)[0][0]

                messagebox.showinfo(
                    "Auto-detected Background",
                    f"Detected background color: RGB{bg_color}\n"
                    f"This color appeared in {color_counts[bg_color]} corners",
                )
            else:  # No - manual selection
                color = colorchooser.askcolor(title="Select Background Color to Remove")
                if not color[0]:  # User cancelled
                    return
                bg_color = tuple(int(c) for c in color[0])

            # Ask for tolerance
            tolerance = simpledialog.askinteger(
                "Removal Tolerance",
                "Enter removal tolerance (0-100):\n"
                "0 = Exact color match only\n"
                "50 = Moderate color range\n"
                "100 = Very broad color range",
                initialvalue=40,
                minvalue=0,
                maxvalue=100,
            )

            if tolerance is None:
                return

            # Apply smart background removal
            data = image.getdata()
            new_data = []
            pixels_removed = 0

            for pixel in data:
                if len(pixel) >= 3:
                    r, g, b = pixel[:3]

                    # Calculate Euclidean distance in RGB space
                    distance = (
                        (r - bg_color[0]) ** 2
                        + (g - bg_color[1]) ** 2
                        + (b - bg_color[2]) ** 2
                    ) ** 0.5

                    # Scale tolerance (0-100 to 0-441, max RGB distance)
                    max_distance = tolerance * 4.41

                    if distance <= max_distance:
                        new_data.append((r, g, b, 0))  # Make transparent
                        pixels_removed += 1
                    else:
                        new_data.append(pixel if len(pixel) == 4 else (r, g, b, 255))
                else:
                    new_data.append(pixel)

            # Create new image with removed background
            result_image = Image.new("RGBA", image.size)
            result_image.putdata(new_data)

            self.current_images[self.selected_image] = result_image
            self.update_canvas()
            self.update_preview()

            # Calculate percentage removed
            total_pixels = len(data)
            percentage = (pixels_removed / total_pixels) * 100

            messagebox.showinfo(
                "Background Removed",
                f"Background removal complete!\n\n"
                f"Color removed: RGB{bg_color}\n"
                f"Tolerance used: {tolerance}\n"
                f"Pixels made transparent: {pixels_removed:,}\n"
                f"Percentage of image: {percentage:.1f}%",
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove background: {str(e)}")

    def show_image_info(self):
        """Show comprehensive image information."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        try:
            image = self.current_images[self.selected_image]

            # Basic image information
            info = f"Image: {self.selected_image}\n"
            info += f"Size: {image.width} x {image.height} pixels\n"
            info += f"Mode: {image.mode}\n"
            info += f"Format: {getattr(image, 'format', 'Unknown')}\n"

            # Calculate approximate file size
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            size_bytes = buffer.tell()
            size_kb = size_bytes / 1024
            info += f"Estimated PNG size: {size_kb:.1f} KB\n"

            # Color information
            if image.mode == "RGBA":
                info += f"Has transparency: Yes\n"
            else:
                info += f"Has transparency: No\n"

            # Rotation info
            if self.selected_image in self.current_rotations:
                rotation = self.current_rotations[self.selected_image]
                info += f"Current rotation: {rotation}°\n"

            messagebox.showinfo("Image Information", info)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get image information: {str(e)}")

    def apply_rotation(self):
        """Apply rotation to current image."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        try:
            angle = self.rotation_var.get()
            if angle == 0:
                return

            image = self.current_images[self.selected_image]
            # Rotate with transparent background
            rotated = image.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
            self.current_images[self.selected_image] = rotated

            # Update current rotation tracking
            if self.selected_image not in self.current_rotations:
                self.current_rotations[self.selected_image] = 0
            self.current_rotations[self.selected_image] = (
                self.current_rotations[self.selected_image] + angle
            ) % 360

            self.update_canvas()
            self.update_preview()
            messagebox.showinfo(
                "Rotation Applied", f"Image rotated by {angle} degrees!"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply rotation: {str(e)}")

    def reset_rotation(self):
        """Reset image rotation to 0 degrees."""
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected")
            return

        try:
            # Reset to original image
            if self.selected_image in self.original_images:
                self.current_images[self.selected_image] = self.original_images[
                    self.selected_image
                ].copy()
                self.current_rotations[self.selected_image] = 0

                # Reset rotation controls
                if hasattr(self, "rotation_var"):
                    self.rotation_var.set(0)
                self.update_rotation_display()

                self.update_canvas()
                self.update_preview()
                messagebox.showinfo(
                    "Rotation Reset", "Image rotation reset to 0 degrees!"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset rotation: {str(e)}")

    def on_rotation_entry_change(self, event=None):
        """Handle rotation entry changes."""
        pass  # Placeholder

    def update_rotation_display(self):
        """Update rotation display."""
        pass  # Placeholder

    def update_base_image(self):
        """Update base image after transformations."""
        pass  # Placeholder

    # Memory and performance methods
    def cleanup_memory(self):
        """Clean up memory usage."""
        gc.collect()

    def check_memory_usage(self):
        """Check current memory usage."""
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            messagebox.showinfo(
                "Memory Usage", f"Current memory usage: {memory_mb:.1f} MB"
            )
        else:
            messagebox.showinfo(
                "Memory Usage", "Memory monitoring not available (psutil not installed)"
            )

    # Cursor settings methods
    def open_cursor_settings(self):
        """Open cursor settings dialog."""
        messagebox.showinfo(
            "Cursor Settings",
            "Cursor settings not yet implemented in refactored version.",
        )

    def load_cursor_settings(self):
        """Load cursor settings from file."""
        pass  # Already implemented

    def save_cursor_settings(self):
        """Save cursor settings to file."""
        pass  # Already implemented

    def reset_cursor_settings(self):
        """Reset cursor settings to defaults."""
        pass  # Already implemented

    # Export/Import methods
    def export_images(self):
        """Export images to folder."""
        if not self.current_images:
            messagebox.showwarning("Warning", "No images to export")
            return

        try:
            # Ask user to select export folder
            folder = filedialog.askdirectory(title="Select Export Folder")
            if not folder:
                return

            # Ask for export format
            format_choice = messagebox.askyesnocancel(
                "Export Format",
                "Choose export format:\n\n"
                "Yes - PNG (with transparency support)\n"
                "No - JPEG (smaller file size)\n"
                "Cancel - Cancel export",
            )

            if format_choice is None:  # Cancel
                return

            export_format = "PNG" if format_choice else "JPEG"
            file_extension = ".png" if format_choice else ".jpg"

            # For JPEG, ask about quality
            quality = 95  # Default quality
            if export_format == "JPEG":
                quality = simpledialog.askinteger(
                    "JPEG Quality",
                    "Enter JPEG quality (1-100):\n"
                    "Higher values = better quality, larger files",
                    initialvalue=95,
                    minvalue=1,
                    maxvalue=100,
                )
                if quality is None:
                    return

            # Export all images
            exported_count = 0
            errors = []

            for name, image in self.current_images.items():
                try:
                    # Clean filename
                    safe_name = "".join(
                        c for c in name if c.isalnum() or c in (" ", "-", "_")
                    ).rstrip()
                    if not safe_name:
                        safe_name = f"image_{exported_count + 1}"

                    filepath = os.path.join(folder, safe_name + file_extension)

                    # Handle file conflicts
                    counter = 1
                    original_filepath = filepath
                    while os.path.exists(filepath):
                        base_name = safe_name + f"_{counter}"
                        filepath = os.path.join(folder, base_name + file_extension)
                        counter += 1

                    # Convert image for export
                    export_image = image.copy()

                    if export_format == "JPEG":
                        # Convert RGBA to RGB for JPEG
                        if export_image.mode == "RGBA":
                            # Create white background
                            background = Image.new(
                                "RGB", export_image.size, (255, 255, 255)
                            )
                            background.paste(
                                export_image, mask=export_image.split()[-1]
                            )  # Use alpha as mask
                            export_image = background
                        elif export_image.mode != "RGB":
                            export_image = export_image.convert("RGB")

                        export_image.save(
                            filepath,
                            format=export_format,
                            quality=quality,
                            optimize=True,
                        )
                    else:  # PNG
                        export_image.save(filepath, format=export_format, optimize=True)

                    exported_count += 1

                except Exception as e:
                    errors.append(f"{name}: {str(e)}")

            # Show results
            result_message = f"Export completed!\n\n"
            result_message += f"Successfully exported: {exported_count} images\n"
            result_message += f"Format: {export_format}\n"
            result_message += f"Location: {folder}\n"

            if export_format == "JPEG":
                result_message += f"Quality: {quality}%\n"

            if errors:
                result_message += f"\nErrors ({len(errors)}):\n"
                result_message += "\n".join(errors[:5])  # Show first 5 errors
                if len(errors) > 5:
                    result_message += f"\n... and {len(errors) - 5} more errors"

            messagebox.showinfo("Export Complete", result_message)

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export images: {str(e)}")

    # Panel management methods (already implemented)
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

    # Right panel functionality
    def update_rotation_display(self, value=None):
        """Update rotation display when slider changes."""
        if hasattr(self, "rotation_var") and hasattr(self, "rotation_entry"):
            current_value = self.rotation_var.get()
            self.rotation_entry.delete(0, tk.END)
            self.rotation_entry.insert(0, str(current_value))

    def on_rotation_entry_change(self, event=None):
        """Handle rotation entry changes."""
        if hasattr(self, "rotation_entry") and hasattr(self, "rotation_var"):
            try:
                value = int(self.rotation_entry.get())
                value = max(0, min(360, value))  # Clamp to 0-360
                self.rotation_var.set(value)
            except ValueError:
                pass  # Ignore invalid input

    def preview_buttons(self):
        """Preview images as buttons."""
        if not hasattr(self, "preview_canvas"):
            return

        y_offset = 10
        canvas_width = self.preview_canvas.winfo_width() or 200

        for i, (name, image) in enumerate(
            list(self.current_images.items())[:3]
        ):  # Show first 3
            try:
                # Create a button preview
                button_img = image.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(button_img)

                # Create button-like background
                bg_x1, bg_y1 = 10, y_offset - 16
                bg_x2, bg_y2 = canvas_width - 10, y_offset + 16

                self.preview_canvas.create_rectangle(
                    bg_x1,
                    bg_y1,
                    bg_x2,
                    bg_y2,
                    fill="#f0f0f0",
                    outline="#cccccc",
                    width=1,
                )

                # Add image and text
                self.preview_canvas.create_image(30, y_offset, image=photo)
                self.preview_canvas.create_text(
                    50,
                    y_offset,
                    text=f"Button: {name[:15]}{'...' if len(name) > 15 else ''}",
                    anchor="w",
                    font=("Arial", 8),
                )

                # Keep reference to prevent garbage collection
                self._preview_refs.append(photo)
                y_offset += 40

            except Exception as e:
                print(f"Error creating button preview for {name}: {e}")
                continue

    def preview_icons(self):
        """Preview images as icons."""
        if not hasattr(self, "preview_canvas"):
            return

        x_offset = 15
        y_offset = 15
        icon_size = 24
        spacing_x = 60
        spacing_y = 45
        cols = 3

        for i, (name, image) in enumerate(
            list(self.current_images.items())[:6]
        ):  # Show first 6
            try:
                col = i % cols
                row = i // cols

                x = x_offset + col * spacing_x
                y = y_offset + row * spacing_y

                # Create icon
                icon_img = image.resize(
                    (icon_size, icon_size), Image.Resampling.LANCZOS
                )
                photo = ImageTk.PhotoImage(icon_img)

                # Create icon background
                self.preview_canvas.create_rectangle(
                    x - 2,
                    y - 2,
                    x + icon_size + 2,
                    y + icon_size + 2,
                    fill="white",
                    outline="#dddddd",
                    width=1,
                )

                self.preview_canvas.create_image(x, y, image=photo, anchor="nw")

                # Add icon name below
                self.preview_canvas.create_text(
                    x + icon_size // 2,
                    y + icon_size + 5,
                    text=name[:8] + ("..." if len(name) > 8 else ""),
                    anchor="n",
                    font=("Arial", 7),
                    fill="#666666",
                )

                # Keep reference
                self._preview_refs.append(photo)

            except Exception as e:
                print(f"Error creating icon preview for {name}: {e}")
                continue

    def preview_backgrounds(self):
        """Preview images as backgrounds."""
        if not hasattr(self, "preview_canvas"):
            return

        if not self.current_images:
            return

        try:
            # Use selected image or first available
            if self.selected_image and self.selected_image in self.current_images:
                name = self.selected_image
                image = self.current_images[name]
            else:
                name, image = next(iter(self.current_images.items()))

            canvas_width = self.preview_canvas.winfo_width() or 200
            bg_width = min(canvas_width - 20, 150)
            bg_height = int(bg_width * 0.6)  # 3:2 aspect ratio

            # Create background preview
            bg_img = image.resize((bg_width, bg_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(bg_img)

            # Create frame around background
            frame_x1, frame_y1 = 10, 10
            frame_x2, frame_y2 = 10 + bg_width, 10 + bg_height

            self.preview_canvas.create_rectangle(
                frame_x1 - 2,
                frame_y1 - 2,
                frame_x2 + 2,
                frame_y2 + 2,
                fill="white",
                outline="#333333",
                width=2,
            )

            self.preview_canvas.create_image(
                frame_x1, frame_y1, image=photo, anchor="nw"
            )

            # Add label
            self.preview_canvas.create_text(
                10,
                frame_y2 + 10,
                text=f"Background: {name[:20]}{'...' if len(name) > 20 else ''}",
                anchor="w",
                font=("Arial", 9),
                fill="#333333",
            )

            # Add sample content overlay
            self.preview_canvas.create_rectangle(
                frame_x1 + 10,
                frame_y1 + 10,
                frame_x1 + 80,
                frame_y1 + 30,
                fill="white",
                outline="#666666",
                stipple="gray50",
            )
            self.preview_canvas.create_text(
                frame_x1 + 45,
                frame_y1 + 20,
                text="Content",
                font=("Arial", 8),
                fill="#333333",
            )

            # Keep reference
            self._preview_refs.append(photo)

        except Exception as e:
            print(f"Error creating background preview: {e}")

    def preview_sprites(self):
        """Preview images as game sprites."""
        if not hasattr(self, "preview_canvas"):
            return

        canvas_width = self.preview_canvas.winfo_width() or 200
        canvas_height = self.preview_canvas.winfo_height() or 100

        # Get framework name
        framework = self.framework_var.get()

        self.preview_canvas.create_text(
            10,
            10,
            text=f"{framework.title()} Sprites:",
            anchor="nw",
            font=("Arial", 10, "bold"),
            fill="#333333",
        )

        if not self.current_images:
            # Show message when no image is selected
            self.preview_canvas.create_text(
                canvas_width // 2,
                canvas_height // 2,
                text="Select an image to see sprite preview",
                fill="#888888",
                font=("Arial", 12),
                anchor="center",
            )
            return

        # Use selected image or first available
        if self.selected_image and self.selected_image in self.current_images:
            name = self.selected_image
            image = self.current_images[name]
        else:
            name, image = next(iter(self.current_images.items()))

        # Show current image name
        self.preview_canvas.create_text(
            10,
            25,
            text=f"Current Sprite: {name}",
            anchor="nw",
            font=("Arial", 9),
            fill="#666666",
        )

        # Simulate a game scene with proper bounds
        margin = 15
        scene_x = margin
        scene_y = 45  # Adjusted for the additional text
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

            # Create sprite photo
            try:
                # Scale sprite appropriately for the scene
                max_sprite_size = min(scene_width // 3, scene_height // 2, 64)
                sprite_img = image.resize(
                    (max_sprite_size, max_sprite_size), Image.Resampling.LANCZOS
                )
                photo = ImageTk.PhotoImage(sprite_img)

                # Place the selected sprite in the center of the scene
                sprite_x = scene_x + (scene_width - photo.width()) // 2
                sprite_y = ground_y - photo.height()
                if sprite_y < scene_y + 10:  # If sprite is too tall, place it lower
                    sprite_y = scene_y + 10

                self.preview_canvas.create_image(
                    sprite_x, sprite_y, image=photo, anchor="nw"
                )

                # Keep reference
                self._preview_refs.append(photo)

            except Exception as e:
                print(f"Error creating sprite preview for {name}: {e}")

    def preview_ui_elements(self):
        """Preview images as UI elements."""
        if not hasattr(self, "preview_canvas"):
            return

        canvas_width = self.preview_canvas.winfo_width() or 200
        canvas_height = self.preview_canvas.winfo_height() or 100

        # Get framework name
        framework = self.framework_var.get()

        self.preview_canvas.create_text(
            10,
            10,
            text=f"{framework.title()} UI Elements:",
            anchor="nw",
            font=("Arial", 10, "bold"),
            fill="#333333",
        )

        # Create a mock UI layout with proper spacing
        margin = 15
        ui_x = margin
        ui_y = 30
        ui_width = canvas_width - (2 * margin)

        if ui_width <= 50:  # Not enough space
            return

        # Toolbar
        toolbar_height = 35
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
        toolbar_images = 0
        max_toolbar_images = max(4, min(8, len(self.current_images)))

        try:
            for i, (name, image) in enumerate(
                list(self.current_images.items())[:max_toolbar_images]
            ):
                if toolbar_images >= max_toolbar_images:
                    break

                # Create toolbar icon (24x24)
                icon_size = 24
                icon_img = image.resize(
                    (icon_size, icon_size), Image.Resampling.LANCZOS
                )
                photo = ImageTk.PhotoImage(icon_img)

                if icon_x + icon_size + 8 > ui_x + ui_width - 8:
                    break  # Don't overflow toolbar

                # Center icon vertically in toolbar
                icon_y = ui_y + (toolbar_height - icon_size) // 2
                self.preview_canvas.create_image(
                    icon_x, icon_y, image=photo, anchor="nw"
                )

                # Keep reference
                self._preview_refs.append(photo)
                icon_x += icon_size + 8
                toolbar_images += 1

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

                # Add remaining images in content area if any
                remaining_images = list(self.current_images.items())[toolbar_images:]
                if remaining_images and content_height > 40:
                    # Show some images in content area
                    content_icon_x = ui_x + 10
                    content_icon_y = content_y + 10
                    content_images_shown = 0
                    max_content_images = min(6, len(remaining_images))

                    for name, image in remaining_images[:max_content_images]:
                        # Create content icon (32x32)
                        content_icon_size = 32
                        content_img = image.resize(
                            (content_icon_size, content_icon_size),
                            Image.Resampling.LANCZOS,
                        )
                        photo = ImageTk.PhotoImage(content_img)

                        if (
                            content_icon_x + content_icon_size + 10
                            > ui_x + ui_width - 10
                        ):
                            content_icon_x = ui_x + 10
                            content_icon_y += content_icon_size + 10

                        if (
                            content_icon_y + content_icon_size
                            > content_y + content_height - 10
                        ):
                            break  # Don't overflow content area

                        self.preview_canvas.create_image(
                            content_icon_x, content_icon_y, image=photo, anchor="nw"
                        )

                        # Keep reference
                        self._preview_refs.append(photo)
                        content_icon_x += content_icon_size + 10
                        content_images_shown += 1

                    # Add text if there's space
                    if content_icon_y + 30 < content_y + content_height - 10:
                        self.preview_canvas.create_text(
                            ui_x + ui_width // 2,
                            content_y + content_height - 20,
                            text=f"Content Area ({content_images_shown} images)",
                            fill="#666666",
                            font=("Arial", 9),
                            anchor="center",
                        )

        except Exception as e:
            print(f"Error creating UI elements preview: {e}")

    def preview_general(self):
        """Preview images in general format."""
        if not hasattr(self, "preview_canvas"):
            return

        if not self.current_images:
            return

        try:
            # Use selected image or first available
            if self.selected_image and self.selected_image in self.current_images:
                name = self.selected_image
                image = self.current_images[name]
            else:
                name, image = next(iter(self.current_images.items()))

            # Create general preview
            preview_width, preview_height = 80, 60
            prev_img = image.resize(
                (preview_width, preview_height), Image.Resampling.LANCZOS
            )
            photo = ImageTk.PhotoImage(prev_img)

            canvas_width = self.preview_canvas.winfo_width() or 200
            center_x = canvas_width // 2

            # Create image frame
            frame_x = center_x - preview_width // 2
            frame_y = 15

            self.preview_canvas.create_rectangle(
                frame_x - 2,
                frame_y - 2,
                frame_x + preview_width + 2,
                frame_y + preview_height + 2,
                fill="white",
                outline="#333333",
                width=2,
            )

            self.preview_canvas.create_image(frame_x, frame_y, image=photo, anchor="nw")

            # Add image info
            self.preview_canvas.create_text(
                center_x,
                frame_y + preview_height + 10,
                text=f"{name[:15]}{'...' if len(name) > 15 else ''}",
                anchor="n",
                font=("Arial", 9, "bold"),
                fill="#333333",
            )

            # Add size info
            self.preview_canvas.create_text(
                center_x,
                frame_y + preview_height + 25,
                text=f"{image.width}×{image.height}px",
                anchor="n",
                font=("Arial", 7),
                fill="#666666",
            )

            # Add mode info
            mode_text = f"Mode: {image.mode}"
            if image.mode == "RGBA":
                mode_text += " (with transparency)"
            self.preview_canvas.create_text(
                center_x,
                frame_y + preview_height + 38,
                text=mode_text,
                anchor="n",
                font=("Arial", 7),
                fill="#666666",
            )

            # Keep reference
            self._preview_refs.append(photo)

        except Exception as e:
            print(f"Error creating general preview: {e}")

    # Image operations
    def new_image(self):
        """Create a new blank image."""
        dialog = ImageSizeDialog(self.root)

        if dialog.result:
            width, height, name = dialog.result

            # Generate unique name if needed
            if name in self.current_images:
                counter = 1
                base_name = name
                while f"{base_name}_{counter}" in self.current_images:
                    counter += 1
                name = f"{base_name}_{counter}"

            # Create new image
            image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
            self.current_images[name] = image
            self.original_images[name] = image.copy()
            self.base_images[name] = image.copy()
            self.current_rotations[name] = 0

            self.update_image_list()
            self.select_image(name)
            self.update_preview()

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

                # Check image size before processing
                max_load_size = 4096  # Maximum dimension for loading
                if image.width > max_load_size or image.height > max_load_size:
                    messagebox.showerror(
                        "Image Too Large",
                        f"Image is too large to load safely:\n"
                        f"Size: {image.width}x{image.height}\n"
                        f"Maximum: {max_load_size}x{max_load_size}\n\n"
                        f"Please resize the image before loading.",
                    )
                    return

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
                self.original_images[name] = image.copy()  # Store original for rotation
                self.base_images[name] = (
                    image.copy()
                )  # Store base image (before rotation)
                self.current_rotations[name] = 0  # Initialize rotation angle
                self.cleanup_memory()  # Clean up before updating UI
                self.update_image_list()
                self.select_image(name)
                self.update_preview()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

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

        # Update base image to the resized version and reset rotation
        self.update_base_image()

        self.update_canvas()
        self.update_preview()

    def update_base_image(self):
        """Update base image after resize."""
        if self.selected_image:
            self.base_images[self.selected_image] = self.current_images[
                self.selected_image
            ].copy()
            self.original_images[self.selected_image] = self.current_images[
                self.selected_image
            ].copy()
            self.current_rotations[self.selected_image] = 0

    def clear_canvas(self):
        """Clear the canvas."""
        self.canvas_manager.clear_canvas()

    # View operations
    def zoom_in(self):
        """Zoom in on the canvas."""
        current_zoom = self.drawing_tools.get_zoom_level()
        self.drawing_tools.set_zoom_level(current_zoom * 1.2)
        self.update_canvas()

    def zoom_out(self):
        """Zoom out on the canvas."""
        current_zoom = self.drawing_tools.get_zoom_level()
        self.drawing_tools.set_zoom_level(current_zoom / 1.2)
        self.update_canvas()

    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.drawing_tools.set_zoom_level(1.0)
        self.update_canvas()

    def fit_to_window(self):
        """Fit canvas to window."""
        # Placeholder for fit to window functionality
        pass

    def toggle_grid(self):
        """Toggle grid display."""
        self.drawing_tools.toggle_grid()
        self.update_canvas()

    # Settings
    def open_cursor_settings(self):
        """Open cursor settings dialog."""
        # Placeholder for cursor settings dialog
        pass

    # Help
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            "GUI Image Studio - Enhanced\n\n"
            "A visual tool for developers to design images/icons\n"
            "and generate embedded code.\n\n"
            "Refactored for better maintainability.",
        )

    def show_help(self):
        """Show help window."""
        HelpWindow(self.root, self)

    def start_tutorial(self):
        """Start the interactive tutorial."""
        from .ui.help_system import InteractiveTutorial

        tutorial = InteractiveTutorial(self.root, self)
        tutorial.start_basic_tutorial()

    def show_shortcuts_help(self):
        """Show keyboard shortcuts help."""
        help_window = HelpWindow(self.root, self)
        # Switch to shortcuts tab
        help_window.notebook.select(3)  # Shortcuts is the 4th tab (index 3)

    def show_tools_help(self):
        """Show tools reference help."""
        help_window = HelpWindow(self.root, self)
        # Switch to tools tab
        help_window.notebook.select(1)  # Tools is the 2nd tab (index 1)

    def show_troubleshooting_help(self):
        """Show troubleshooting help."""
        help_window = HelpWindow(self.root, self)
        # Switch to troubleshooting tab
        help_window.notebook.select(5)  # Troubleshooting is the 6th tab (index 5)

    def open_online_help(self):
        """Open online documentation."""
        from tkinter import messagebox

        messagebox.showinfo(
            "Online Help",
            "Online documentation would be available at:\n"
            "https://your-domain.com/image-studio/docs\n\n"
            "For now, use the comprehensive help system (F1) for detailed information.",
        )

    # Additional methods referenced by panels
    def choose_color(self):
        """Open color chooser dialog."""
        color = colorchooser.askcolor(color=self.drawing_tools.get_brush_color())
        if color[1]:  # color[1] is the hex string
            self.drawing_tools.set_brush_color(color[1])
            if hasattr(self, "color_button"):
                self.color_button.configure(bg=color[1])

    def duplicate_image(self):
        """Duplicate the selected image."""
        if self.selected_image and self.selected_image in self.current_images:
            original = self.current_images[self.selected_image]
            base_name = f"{self.selected_image}_copy"
            new_name = base_name

            # Ensure unique name
            counter = 1
            while new_name in self.current_images:
                new_name = f"{base_name}_{counter}"
                counter += 1

            # Duplicate the image and all related data
            self.current_images[new_name] = original.copy()
            self.original_images[new_name] = original.copy()
            self.base_images[new_name] = original.copy()
            self.current_rotations[new_name] = 0

            self.update_image_list()
            self.select_image(new_name)
            self.update_preview()

    def delete_image(self):
        """Delete the selected image."""
        if self.selected_image and self.selected_image in self.current_images:
            result = messagebox.askyesno(
                "Confirm Delete", f"Delete image '{self.selected_image}'?"
            )
            if result:
                # Remove from all image dictionaries
                name = self.selected_image
                if name in self.current_images:
                    del self.current_images[name]
                if name in self.original_images:
                    del self.original_images[name]
                if name in self.base_images:
                    del self.base_images[name]
                if name in self.current_rotations:
                    del self.current_rotations[name]
                if name in self.image_previews:
                    del self.image_previews[name]

                # Clear selection if this was the selected image
                self.selected_image = None

                # Select another image if available
                if self.current_images:
                    first_image = next(iter(self.current_images.keys()))
                    self.select_image(first_image)
                else:
                    # No images left, clear canvas
                    self.update_canvas()

                self.update_image_list()
                self.update_preview()

    def zoom_in(self):
        """Zoom in on the canvas."""
        self.drawing_tools.set_zoom_level(
            min(self.drawing_tools.get_zoom_level() * 1.5, 10.0)
        )
        self.update_canvas()

    def zoom_out(self):
        """Zoom out on the canvas."""
        self.drawing_tools.set_zoom_level(
            max(self.drawing_tools.get_zoom_level() / 1.5, 0.1)
        )
        self.update_canvas()

    def zoom_fit(self):
        """Fit image to canvas."""
        if not self.selected_image:
            return

        image = self.current_images[self.selected_image]
        if hasattr(self, "canvas"):
            canvas_width = self.canvas.winfo_width() - 20
            canvas_height = self.canvas.winfo_height() - 20

            if canvas_width > 0 and canvas_height > 0:
                zoom_x = canvas_width / image.width
                zoom_y = canvas_height / image.height
                self.drawing_tools.set_zoom_level(min(zoom_x, zoom_y, 10.0))
                self.update_canvas()

    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.drawing_tools.set_zoom_level(1.0)
        self.update_canvas()

    def toggle_grid(self):
        """Toggle grid display."""
        if hasattr(self, "grid_var"):
            self.drawing_tools.show_grid = self.grid_var.get()
        else:
            self.drawing_tools.show_grid = not self.drawing_tools.show_grid
        self.update_canvas()

    def on_name_change(self, event):
        """Handle name change in properties."""
        if self.selected_image and hasattr(self, "name_var"):
            new_name = self.name_var.get().strip()
            if new_name and new_name != self.selected_image:
                self.rename_image(self.selected_image, new_name)

    def resize_image(self):
        """Resize the current image."""
        if hasattr(self, "width_var") and hasattr(self, "height_var"):
            try:
                width = self.width_var.get()
                height = self.height_var.get()
                self.canvas_manager.create_new_image((width, height))
            except tk.TclError:
                messagebox.showerror("Error", "Invalid size values")

    def generate_python_code(self):
        """Generate Python code for images."""
        if not self.image_manager.list_images():
            messagebox.showwarning("Warning", "No images to generate code for.")
            return

        # Placeholder for code generation
        code = "# Generated Python code would go here\n"
        CodePreviewWindow(self.root, "Python Code", code)

    def generate_tkinter_code(self):
        """Generate Tkinter code for images."""
        if not self.image_manager.list_images():
            messagebox.showwarning("Warning", "No images to generate code for.")
            return

        # Placeholder for Tkinter code generation
        code = "# Generated Tkinter code would go here\n"
        CodePreviewWindow(self.root, "Tkinter Code", code)

    def update_image_list(self):
        """Update the image list display."""
        if hasattr(self, "image_listbox"):
            self.image_listbox.delete(0, tk.END)
            for name in self.current_images.keys():
                self.image_listbox.insert(tk.END, name)

            # Also update the image manager to keep it in sync
            if hasattr(self, "image_manager"):
                try:
                    # Clear and repopulate image manager
                    current_manager_images = self.image_manager.list_images()
                    for name in current_manager_images:
                        self.image_manager.remove_image(name)
                    for name, image in self.current_images.items():
                        self.image_manager.add_image(name, image)
                except Exception as e:
                    print(f"Error syncing image manager: {e}")

    # Drawing methods - copied from original
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

            draw.text(
                (x, y), text, fill=self.drawing_tools.get_brush_color(), font=font
            )
            self.update_canvas()

    def on_closing(self):
        """Handle application closing."""
        # Cleanup temporary files and icons
        try:
            import shutil

            if hasattr(self.image_manager, "temp_dir"):
                shutil.rmtree(self.image_manager.temp_dir, ignore_errors=True)

            # Cleanup embedded icons
            for icon_path in self.icon_paths:
                cleanup_icon(icon_path)
        except Exception:
            pass  # Ignore cleanup errors

        # Force garbage collection
        gc.collect()

        self.root.destroy()

    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = EnhancedImageDesignerGUI()
    app.run()


if __name__ == "__main__":
    main()
