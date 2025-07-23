"""
Dialog windows for Image Studio.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class ToolTip:
    """Simple tooltip class for widgets."""

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        # Bind events
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event: Optional[tk.Event] = None) -> None:
        """Show tooltip on mouse enter."""
        if self.tooltip_window:
            return

        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="lightyellow",
            relief="solid",
            borderwidth=1,
            font=("Arial", 8),
        )
        label.pack()

    def on_leave(self, event: Optional[tk.Event] = None) -> None:
        """Hide tooltip on mouse leave."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


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

    def __init__(self, parent, title: str, code: str):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("800x600")
        self.window.transient(parent)

        self.setup_ui(code)

    def setup_ui(self, code: str):
        """Setup the preview window UI."""
        # Create text widget with scrollbars
        text_frame = ttk.Frame(self.window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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

        # Insert code
        self.text_widget.insert(tk.END, code)
        self.text_widget.configure(state=tk.DISABLED)

        # Button frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(
            button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard
        ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(
            side=tk.RIGHT
        )

    def copy_to_clipboard(self):
        """Copy code to clipboard."""
        self.window.clipboard_clear()
        self.window.clipboard_append(self.text_widget.get(1.0, tk.END))
        messagebox.showinfo("Copied", "Code copied to clipboard!")


# Import the comprehensive help system
from .help_system import ComprehensiveHelpWindow


class HelpWindow(ComprehensiveHelpWindow):
    """Enhanced help window with comprehensive documentation."""

    def __init__(self, parent, app=None):
        # If app is not provided, try to get it from parent
        if app is None and hasattr(parent, "app"):
            app = parent.app
        elif app is None:
            # Fallback to basic help if app is not available
            self._create_basic_help(parent)
            return

        super().__init__(parent, app)

    def _create_basic_help(self, parent):
        """Create basic help window as fallback."""
        self.window = tk.Toplevel(parent)
        self.window.title("Image Studio Help")
        self.window.geometry("700x500")
        self.window.transient(parent)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tools tab
        tools_frame = ttk.Frame(notebook)
        notebook.add(tools_frame, text="Tools")

        tools_text = tk.Text(tools_frame, wrap=tk.WORD, font=("Arial", 10))
        tools_scrollbar = ttk.Scrollbar(
            tools_frame, orient=tk.VERTICAL, command=tools_text.yview
        )
        tools_text.configure(yscrollcommand=tools_scrollbar.set)

        tools_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tools_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tools_help = """
Drawing Tools:

• Brush: Freehand drawing with adjustable size
• Pencil: Precise pixel-by-pixel drawing
• Eraser: Remove pixels from the canvas
• Line: Draw straight lines
• Rectangle: Draw rectangles (filled or outline)
• Circle: Draw circles (filled or outline)
• Text: Add text to your image
• Fill: Fill areas with color

Keyboard Shortcuts:
• G: Toggle grid
• +: Zoom in
• -: Zoom out
• 0: Reset zoom
• Ctrl+N: New image
• Ctrl+O: Load image
• Ctrl+Q: Quit

For comprehensive help, please ensure the application is properly initialized.
        """

        tools_text.insert(tk.END, tools_help.strip())
        tools_text.configure(state=tk.DISABLED)

        # Close button
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(
            side=tk.RIGHT
        )


class CursorSettingsDialog:
    """Dialog for configuring cursor settings."""

    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Cursor Settings")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()

        messagebox.showinfo(
            "Not Implemented",
            "Cursor settings dialog not yet implemented in refactored version.",
        )
        self.window.destroy()


class CustomCursorDialog:
    """Dialog for creating/editing custom cursors."""

    def __init__(self, parent, app, cursor_name=None):
        self.app = app
        self.cursor_name = cursor_name
        self.window = tk.Toplevel(parent)
        self.window.title("Custom Cursor Editor")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()

        messagebox.showinfo(
            "Not Implemented",
            "Custom cursor dialog not yet implemented in refactored version.",
        )
        self.window.destroy()


class CursorTestWindow:
    """Window for testing cursors interactively."""

    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Cursor Test")
        self.window.geometry("400x300")
        self.window.transient(parent)

        messagebox.showinfo(
            "Not Implemented",
            "Cursor test window not yet implemented in refactored version.",
        )
        self.window.destroy()
