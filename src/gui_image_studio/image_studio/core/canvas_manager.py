"""
Canvas management functionality.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Optional, Tuple

from PIL import Image, ImageDraw, ImageTk

if TYPE_CHECKING:
    from ..main_app import EnhancedImageDesignerGUI


class CanvasManager:
    """Manages the drawing canvas operations."""

    def __init__(self, app: "EnhancedImageDesignerGUI"):
        self.app = app
        self.canvas: Optional[tk.Canvas] = None
        self.canvas_image: Optional[Image.Image] = None
        self.canvas_photo: Optional[ImageTk.PhotoImage] = None
        self.canvas_item_id: Optional[int] = None

    def create_canvas(self, parent) -> tk.Canvas:
        """Create and setup the drawing canvas."""
        # Create canvas with scrollbars - exact copy from original
        self.canvas = tk.Canvas(parent, bg="white", scrollregion=(0, 0, 600, 450))

        h_scrollbar = ttk.Scrollbar(
            parent, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        v_scrollbar = ttk.Scrollbar(
            parent, orient=tk.VERTICAL, command=self.canvas.yview
        )

        self.canvas.configure(
            xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set
        )

        self.canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Setup canvas bindings - copied from original
        self.setup_canvas_bindings()

        # Initialize canvas image
        self.create_new_image()

        return self.canvas

    def setup_canvas_bindings(self):
        """Setup canvas event bindings."""
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Motion>", self.on_canvas_motion)

    def create_new_image(self, size: Tuple[int, int] = (300, 300)) -> None:
        """Create a new blank image on the canvas."""
        self.canvas_image = Image.new("RGBA", size, (255, 255, 255, 255))
        self.update_canvas_display()

    def update_canvas_display(self) -> None:
        """Update the canvas display with the current image."""
        if not self.canvas or not self.canvas_image:
            return

        # Apply zoom
        zoom = self.app.drawing_tools.get_zoom_level()
        display_size = (
            int(self.canvas_image.width * zoom),
            int(self.canvas_image.height * zoom),
        )

        # Resize image for display
        display_image = self.canvas_image.resize(display_size, Image.Resampling.NEAREST)
        self.canvas_photo = ImageTk.PhotoImage(display_image)

        # Clear canvas and add image
        self.canvas.delete("all")

        # Add grid if enabled
        if self.app.drawing_tools.show_grid:
            self.draw_grid(display_size, zoom)

        # Add image to canvas
        self.canvas_item_id = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.canvas_photo
        )

        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_grid(self, size: Tuple[int, int], zoom: float) -> None:
        """Draw grid on the canvas."""
        grid_size = max(1, int(10 * zoom))  # Grid every 10 pixels at 1x zoom

        # Vertical lines
        for x in range(0, size[0], grid_size):
            self.canvas.create_line(x, 0, x, size[1], fill="#e0e0e0", width=1)

        # Horizontal lines
        for y in range(0, size[1], grid_size):
            self.canvas.create_line(0, y, size[0], y, fill="#e0e0e0", width=1)

    def clear_canvas(self) -> None:
        """Clear the canvas."""
        if self.canvas_image:
            self.canvas_image = Image.new(
                "RGBA", self.canvas_image.size, (255, 255, 255, 255)
            )
            self.update_canvas_display()

    def get_canvas_coordinates(self, event) -> Tuple[int, int]:
        """Convert screen coordinates to canvas coordinates."""
        if not self.canvas:
            return 0, 0

        # Get canvas coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        # Convert to image coordinates considering zoom
        zoom = self.app.drawing_tools.get_zoom_level()
        image_x = int(canvas_x / zoom)
        image_y = int(canvas_y / zoom)

        return image_x, image_y

    def draw_pixel(self, x: int, y: int, color: str, size: int = 1) -> None:
        """Draw a pixel or brush stroke on the canvas."""
        if not self.canvas_image:
            return

        draw = ImageDraw.Draw(self.canvas_image)

        if size == 1:
            # Single pixel
            if 0 <= x < self.canvas_image.width and 0 <= y < self.canvas_image.height:
                draw.point((x, y), fill=color)
        else:
            # Brush stroke
            radius = size // 2
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

        self.update_canvas_display()

    def draw_line(
        self, x1: int, y1: int, x2: int, y2: int, color: str, width: int = 1
    ) -> None:
        """Draw a line on the canvas."""
        if not self.canvas_image:
            return

        draw = ImageDraw.Draw(self.canvas_image)
        draw.line((x1, y1, x2, y2), fill=color, width=width)
        self.update_canvas_display()

    def draw_rectangle(
        self, x1: int, y1: int, x2: int, y2: int, color: str, filled: bool = False
    ) -> None:
        """Draw a rectangle on the canvas."""
        if not self.canvas_image:
            return

        draw = ImageDraw.Draw(self.canvas_image)
        if filled:
            draw.rectangle((x1, y1, x2, y2), fill=color)
        else:
            draw.rectangle((x1, y1, x2, y2), outline=color)
        self.update_canvas_display()

    def draw_circle(
        self, x1: int, y1: int, x2: int, y2: int, color: str, filled: bool = False
    ) -> None:
        """Draw a circle on the canvas."""
        if not self.canvas_image:
            return

        draw = ImageDraw.Draw(self.canvas_image)
        if filled:
            draw.ellipse((x1, y1, x2, y2), fill=color)
        else:
            draw.ellipse((x1, y1, x2, y2), outline=color)
        self.update_canvas_display()

    # Canvas event handlers - copied from original
    def on_canvas_click(self, event):
        """Handle canvas click events."""
        if not self.app.selected_image:
            return

        # Convert canvas coordinates to image coordinates
        x = int(
            (self.canvas.canvasx(event.x) - 10)
            / self.app.drawing_tools.get_zoom_level()
        )
        y = int(
            (self.canvas.canvasy(event.y) - 10)
            / self.app.drawing_tools.get_zoom_level()
        )

        current_tool = self.app.drawing_tools.get_current_tool()

        # Get tools that support click operations (excluding preview tools and text)
        click_tools = self.app.drawing_tools.get_tools_by_capability("click")
        preview_tools = self.app.drawing_tools.get_tools_by_capability("preview")
        text_tools = self.app.drawing_tools.get_tools_by_capability("text_input")

        # Remove preview and text tools from click tools for immediate drawing
        immediate_click_tools = [
            t for t in click_tools if t not in preview_tools and t not in text_tools
        ]

        if current_tool in immediate_click_tools:
            self.app.last_x, self.app.last_y = x, y
            self.app.draw_on_image(x, y)
        elif current_tool in preview_tools:
            self.app.drawing = True
            self.app.start_x, self.app.start_y = x, y
            print(f"Shape tool {current_tool} started at ({x}, {y})")  # Debug

        elif current_tool in text_tools:
            self.app.add_text(x, y)

    def on_canvas_drag(self, event):
        """Handle canvas drag events."""
        if not self.app.selected_image:
            return

        # Convert canvas coordinates to image coordinates
        x = int(
            (self.canvas.canvasx(event.x) - 10)
            / self.app.drawing_tools.get_zoom_level()
        )
        y = int(
            (self.canvas.canvasy(event.y) - 10)
            / self.app.drawing_tools.get_zoom_level()
        )

        current_tool = self.app.drawing_tools.get_current_tool()

        # Get tools that support drag operations
        drag_tools = self.app.drawing_tools.get_tools_by_capability("drag")
        preview_tools = self.app.drawing_tools.get_tools_by_capability("preview")

        # Tools that support drag but not preview (immediate drawing)
        immediate_drag_tools = [t for t in drag_tools if t not in preview_tools]

        if current_tool in immediate_drag_tools:
            if hasattr(self.app, "last_x") and hasattr(self.app, "last_y"):
                self.app.draw_line_on_image(self.app.last_x, self.app.last_y, x, y)
            self.app.last_x, self.app.last_y = x, y
        elif self.app.drawing and current_tool in preview_tools:
            # Show preview while dragging
            self.update_shape_preview(self.app.start_x, self.app.start_y, x, y)

    def on_canvas_release(self, event):
        """Handle canvas release events."""
        if not self.app.selected_image:
            return

        current_tool = self.app.drawing_tools.get_current_tool()

        # Get tools that support release operations (preview tools)
        release_tools = self.app.drawing_tools.get_tools_by_capability("release")

        if self.app.drawing and current_tool in release_tools:
            # Convert canvas coordinates to image coordinates
            x = int(
                (self.canvas.canvasx(event.x) - 10)
                / self.app.drawing_tools.get_zoom_level()
            )
            y = int(
                (self.canvas.canvasy(event.y) - 10)
                / self.app.drawing_tools.get_zoom_level()
            )

            print(
                f"Shape tool {current_tool} finished at ({x}, {y}) from ({self.app.start_x}, {self.app.start_y})"
            )  # Debug
            self.app.draw_shape(self.app.start_x, self.app.start_y, x, y)
            self.app.drawing = False
            self.clear_preview()

    def on_canvas_motion(self, event):
        """Handle canvas motion events for shape preview and pixel highlighting."""
        if not self.app.selected_image:
            return

        # Convert canvas coordinates to image coordinates
        x = int(
            (self.canvas.canvasx(event.x) - 10)
            / self.app.drawing_tools.get_zoom_level()
        )
        y = int(
            (self.canvas.canvasy(event.y) - 10)
            / self.app.drawing_tools.get_zoom_level()
        )

        # Show pixel highlight for drawing tools when grid is enabled
        current_tool = self.app.drawing_tools.get_current_tool()

        # Get tools that support immediate drawing (for pixel highlighting)
        immediate_draw_tools = self.app.drawing_tools.get_tools_by_capability("click")
        preview_tools = self.app.drawing_tools.get_tools_by_capability("preview")
        text_tools = self.app.drawing_tools.get_tools_by_capability("text_input")

        # Tools that draw immediately (not preview or text tools)
        pixel_highlight_tools = [
            t
            for t in immediate_draw_tools
            if t not in preview_tools and t not in text_tools
        ]

        if (
            self.app.drawing_tools.show_grid
            and current_tool in pixel_highlight_tools
            and self.app.drawing_tools.get_zoom_level() >= 4
        ):
            self.update_pixel_highlight(x, y)
        else:
            self.clear_pixel_highlight()

        # Show shape preview for shape tools when drawing
        if self.app.drawing and current_tool in ["rectangle", "circle", "line"]:
            self.update_shape_preview(self.app.start_x, self.app.start_y, x, y)

    def update_shape_preview(self, x1, y1, x2, y2):
        """Update the preview shape on canvas."""
        # Clear existing preview
        self.clear_preview()

        # Convert image coordinates back to canvas coordinates for display
        canvas_x1 = x1 * self.app.drawing_tools.get_zoom_level() + 10
        canvas_y1 = y1 * self.app.drawing_tools.get_zoom_level() + 10
        canvas_x2 = x2 * self.app.drawing_tools.get_zoom_level() + 10
        canvas_y2 = y2 * self.app.drawing_tools.get_zoom_level() + 10

        # Create preview shape using new tool system
        preview_id = self.app.drawing_tools.create_preview(self.canvas, x1, y1, x2, y2)
        if preview_id:
            self.app.preview_shape = preview_id
        else:
            # Fallback for tools that don't support preview
            self.app.preview_shape = None

        self.app.preview_active = True

    def clear_preview(self):
        """Clear the preview shape from canvas."""
        if self.app.preview_shape:
            self.canvas.delete(self.app.preview_shape)
            self.app.preview_shape = None
        self.app.preview_active = False

    def update_pixel_highlight(self, x, y):
        """Highlight the pixel that will be affected by drawing tools."""
        # Only highlight if position changed
        if self.app.last_highlight_pos == (x, y):
            return

        self.app.last_highlight_pos = (x, y)

        # Clear existing highlight
        self.clear_pixel_highlight()

        # Check if coordinates are within image bounds
        if not self.app.selected_image:
            return

        image = self.app.current_images[self.app.selected_image]
        if x < 0 or y < 0 or x >= image.width or y >= image.height:
            return

        # Convert image coordinates to canvas coordinates
        canvas_x = x * self.app.drawing_tools.get_zoom_level() + 10
        canvas_y = y * self.app.drawing_tools.get_zoom_level() + 10

        # Create highlight rectangle around the pixel
        self.app.pixel_highlight = self.canvas.create_rectangle(
            canvas_x,
            canvas_y,
            canvas_x + self.app.drawing_tools.get_zoom_level(),
            canvas_y + self.app.drawing_tools.get_zoom_level(),
            outline="#FF0000",
            width=1,
            fill="",
            dash=(2, 2),
            tags="pixel_highlight",
        )

    def clear_pixel_highlight(self):
        """Clear the pixel highlight from canvas."""
        if self.app.pixel_highlight:
            self.canvas.delete(self.app.pixel_highlight)
            self.app.pixel_highlight = None
        self.app.last_highlight_pos = None
