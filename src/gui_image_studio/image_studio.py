#!/usr/bin/env python3
"""
Image Studio GUI for gui_image_studio package.
A visual tool for developers to design images/icons and generate embedded code.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import os
import json
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter, ImageEnhance
import base64
from io import BytesIO
import tempfile

from .generator import embed_images_from_folder


class ImageDesignerGUI:
    """Main GUI application for image design and code generation."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI Image Studio")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Application state
        self.current_images: Dict[str, Image.Image] = {}
        self.image_previews: Dict[str, ImageTk.PhotoImage] = {}
        self.selected_image: Optional[str] = None
        self.temp_dir = tempfile.mkdtemp()
        
        # Design tools state
        self.current_tool = "brush"
        self.brush_size = 5
        self.brush_color = "#000000"
        self.canvas_size = (400, 400)
        self.zoom_level = 1.0
        
        self.setup_ui()
        self.setup_bindings()
        
    def setup_ui(self):
        """Setup the main user interface."""
        # Create main paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Tools and image list
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Center panel - Canvas
        center_frame = ttk.Frame(main_paned)
        main_paned.add(center_frame, weight=3)
        
        # Right panel - Properties and code
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        self.setup_left_panel(left_frame)
        self.setup_center_panel(center_frame)
        self.setup_right_panel(right_frame)
        
    def setup_left_panel(self, parent):
        """Setup the left panel with tools and image management."""
        # Tools section
        tools_frame = ttk.LabelFrame(parent, text="Design Tools")
        tools_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Tool buttons
        tools_grid = ttk.Frame(tools_frame)
        tools_grid.pack(fill=tk.X, padx=5, pady=5)
        
        self.tool_buttons = {}
        tools = [
            ("brush", "🖌️ Brush"),
            ("eraser", "🧽 Eraser"),
            ("line", "📏 Line"),
            ("rectangle", "⬜ Rectangle"),
            ("circle", "⭕ Circle"),
            ("text", "📝 Text"),
            ("fill", "🪣 Fill")
        ]
        
        for i, (tool, label) in enumerate(tools):
            btn = ttk.Button(tools_grid, text=label, 
                           command=lambda t=tool: self.select_tool(t))
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=2, pady=2)
            self.tool_buttons[tool] = btn
            
        tools_grid.columnconfigure(0, weight=1)
        tools_grid.columnconfigure(1, weight=1)
        
        # Tool properties
        props_frame = ttk.LabelFrame(parent, text="Tool Properties")
        props_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Brush size
        ttk.Label(props_frame, text="Size:").pack(anchor=tk.W, padx=5)
        self.size_var = tk.IntVar(value=5)
        size_scale = ttk.Scale(props_frame, from_=1, to=50, 
                              variable=self.size_var, orient=tk.HORIZONTAL)
        size_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Color picker
        color_frame = ttk.Frame(props_frame)
        color_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(color_frame, text="Color:").pack(side=tk.LEFT)
        self.color_button = tk.Button(color_frame, bg=self.brush_color, 
                                     width=3, command=self.choose_color)
        self.color_button.pack(side=tk.RIGHT)
        
        # Image management section
        images_frame = ttk.LabelFrame(parent, text="Images")
        images_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Image list
        list_frame = ttk.Frame(images_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.image_listbox = tk.Listbox(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Image management buttons
        btn_frame = ttk.Frame(images_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="New Image", 
                  command=self.new_image).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Load Image", 
                  command=self.load_image).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Duplicate", 
                  command=self.duplicate_image).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Delete", 
                  command=self.delete_image).pack(fill=tk.X, pady=2)
        
    def setup_center_panel(self, parent):
        """Setup the center panel with the drawing canvas."""
        # Canvas controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Canvas:").pack(side=tk.LEFT)
        
        # Zoom controls
        zoom_frame = ttk.Frame(controls_frame)
        zoom_frame.pack(side=tk.RIGHT)
        
        ttk.Button(zoom_frame, text="Zoom In", 
                  command=self.zoom_in).pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_frame, text="Zoom Out", 
                  command=self.zoom_out).pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_frame, text="Fit", 
                  command=self.zoom_fit).pack(side=tk.LEFT, padx=2)
        
        # Canvas frame
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg="white", 
                               scrollregion=(0, 0, 800, 600))
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, 
                                   command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, 
                                   command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, 
                             yscrollcommand=v_scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
    def setup_right_panel(self, parent):
        """Setup the right panel with properties and code generation."""
        # Image properties
        props_frame = ttk.LabelFrame(parent, text="Image Properties")
        props_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Image name
        ttk.Label(props_frame, text="Name:").pack(anchor=tk.W, padx=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(props_frame, textvariable=self.name_var)
        name_entry.pack(fill=tk.X, padx=5, pady=2)
        name_entry.bind('<KeyRelease>', self.on_name_change)
        
        # Image size
        size_frame = ttk.Frame(props_frame)
        size_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(size_frame, text="Size:").pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=400)
        self.height_var = tk.IntVar(value=400)
        
        ttk.Entry(size_frame, textvariable=self.width_var, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Label(size_frame, text="x").pack(side=tk.LEFT)
        ttk.Entry(size_frame, textvariable=self.height_var, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(size_frame, text="Apply", command=self.resize_image).pack(side=tk.LEFT, padx=5)
        
        # Transformations
        transform_frame = ttk.LabelFrame(parent, text="Transformations")
        transform_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Rotation
        ttk.Label(transform_frame, text="Rotation:").pack(anchor=tk.W, padx=5)
        self.rotation_var = tk.IntVar()
        rotation_scale = ttk.Scale(transform_frame, from_=0, to=360, 
                                  variable=self.rotation_var, orient=tk.HORIZONTAL)
        rotation_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Filters
        filters_frame = ttk.Frame(transform_frame)
        filters_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(filters_frame, text="Blur", 
                  command=self.apply_blur).pack(side=tk.LEFT, padx=2)
        ttk.Button(filters_frame, text="Sharpen", 
                  command=self.apply_sharpen).pack(side=tk.LEFT, padx=2)
        ttk.Button(filters_frame, text="Emboss", 
                  command=self.apply_emboss).pack(side=tk.LEFT, padx=2)
        
        # Code generation
        code_frame = ttk.LabelFrame(parent, text="Code Generation")
        code_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Generation options
        options_frame = ttk.Frame(code_frame)
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(options_frame, text="Framework:").pack(anchor=tk.W)
        self.framework_var = tk.StringVar(value="tkinter")
        framework_combo = ttk.Combobox(options_frame, textvariable=self.framework_var,
                                      values=["tkinter", "customtkinter"], state="readonly")
        framework_combo.pack(fill=tk.X, pady=2)
        
        ttk.Label(options_frame, text="Quality:").pack(anchor=tk.W)
        self.quality_var = tk.IntVar(value=85)
        quality_scale = ttk.Scale(options_frame, from_=1, to=100, 
                                 variable=self.quality_var, orient=tk.HORIZONTAL)
        quality_scale.pack(fill=tk.X, pady=2)
        
        # Generation buttons
        btn_frame = ttk.Frame(code_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Preview Code", 
                  command=self.preview_code).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Generate File", 
                  command=self.generate_code_file).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Export Images", 
                  command=self.export_images).pack(fill=tk.X, pady=2)
        
    def setup_bindings(self):
        """Setup event bindings."""
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        self.image_listbox.bind("<<ListboxSelect>>", self.on_image_select)
        
        # Keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_image())
        self.root.bind("<Control-o>", lambda e: self.load_image())
        self.root.bind("<Control-s>", lambda e: self.export_images())
        self.root.bind("<Delete>", lambda e: self.delete_image())
        
    def select_tool(self, tool):
        """Select a drawing tool."""
        self.current_tool = tool
        
        # Update button states
        for t, btn in self.tool_buttons.items():
            if t == tool:
                btn.configure(style="Accent.TButton")
            else:
                btn.configure(style="TButton")
                
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
                ("All files", "*.*")
            ]
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
            
        # Update canvas
        self.update_canvas()
        
        # Update properties
        image = self.current_images[name]
        self.width_var.set(image.width)
        self.height_var.set(image.height)
        
    def update_canvas(self):
        """Update the canvas display."""
        if not self.selected_image:
            return
            
        image = self.current_images[self.selected_image]
        
        # Create display image with zoom
        display_size = (int(image.width * self.zoom_level), 
                       int(image.height * self.zoom_level))
        display_image = image.resize(display_size, Image.NEAREST)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(display_image)
        self.image_previews[self.selected_image] = photo
        
        # Clear and update canvas
        self.canvas.delete("all")
        self.canvas.create_image(10, 10, anchor=tk.NW, image=photo)
        
        # Update scroll region
        self.canvas.configure(scrollregion=(0, 0, display_size[0] + 20, display_size[1] + 20))
        
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
        
        self.last_x, self.last_y = x, y
        self.draw_on_image(x, y)
        
    def on_canvas_drag(self, event):
        """Handle canvas drag events."""
        if not self.selected_image:
            return
            
        # Convert canvas coordinates to image coordinates
        x = int((self.canvas.canvasx(event.x) - 10) / self.zoom_level)
        y = int((self.canvas.canvasy(event.y) - 10) / self.zoom_level)
        
        if hasattr(self, 'last_x') and hasattr(self, 'last_y'):
            self.draw_line_on_image(self.last_x, self.last_y, x, y)
            
        self.last_x, self.last_y = x, y
        
    def on_canvas_release(self, event):
        """Handle canvas release events."""
        if hasattr(self, 'last_x'):
            delattr(self, 'last_x')
        if hasattr(self, 'last_y'):
            delattr(self, 'last_y')
            
    def draw_on_image(self, x, y):
        """Draw on the current image."""
        if not self.selected_image:
            return
            
        image = self.current_images[self.selected_image]
        draw = ImageDraw.Draw(image)
        
        size = self.size_var.get()
        
        if self.current_tool == "brush":
            # Draw circle
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                        fill=self.brush_color)
        elif self.current_tool == "eraser":
            # Erase (draw transparent)
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                        fill=(0, 0, 0, 0))
                        
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
                background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
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
            with open(temp_output, 'r') as f:
                code_content = f.read()
                
            # Show code preview window
            CodePreviewWindow(self.root, code_content, self.framework_var.get())
            
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
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
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
            embed_images_from_folder(temp_images_dir, output_file, self.quality_var.get())
            
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
            
    def run(self):
        """Run the application."""
        # Create initial image
        self.new_image()
        self.root.mainloop()
        
        # Cleanup temp directory
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass


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
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_ui()
        
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
        self.width_var = tk.IntVar(value=400)
        ttk.Entry(size_frame, textvariable=self.width_var, width=8).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(size_frame, text="Height:").pack(side=tk.LEFT)
        self.height_var = tk.IntVar(value=400)
        ttk.Entry(size_frame, textvariable=self.height_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="Create", command=self.create).pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.create())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
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
    
    def __init__(self, parent, code_content, framework):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Code Preview - {framework}")
        self.window.geometry("800x600")
        self.window.transient(parent)
        
        self.setup_ui(code_content)
        
    def setup_ui(self, code_content):
        """Setup the preview window UI."""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info label
        info_label = ttk.Label(main_frame, 
                              text="Generated embedded code preview:")
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = tk.Text(text_frame, wrap=tk.NONE, font=("Consolas", 10))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        
        self.text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        # Insert code content
        self.text_widget.insert(tk.END, code_content)
        self.text_widget.configure(state=tk.DISABLED)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Copy to Clipboard", 
                  command=lambda: self.copy_to_clipboard(code_content)).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Close", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
                  
    def copy_to_clipboard(self, content):
        """Copy content to clipboard."""
        self.window.clipboard_clear()
        self.window.clipboard_append(content)
        messagebox.showinfo("Success", "Code copied to clipboard!")


def main():
    """Main entry point for the Image Studio GUI."""
    app = ImageDesignerGUI()
    app.run()


if __name__ == "__main__":
    main()