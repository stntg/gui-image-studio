import base64
from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance, ImageSequence

# Try to import embedded_images, create empty dict if not found
try:
    from . import embedded_images
except ImportError:
    # Create a fallback embedded_images module
    class EmbeddedImages:
        embedded_images = {"default": {}}
    embedded_images = EmbeddedImages()

def get_image(image_name, framework="tkinter", size=(32, 32), theme="default",
              grayscale=False, rotate=0, transparency=1.0, format_override=None,
              animated=False, frame_delay=100, tint_color=None, tint_intensity=0.0,
              contrast=1.0, saturation=1.0):
    """
    Retrieve an embedded image with dynamic transformations and optional animated GIF support.
    
    Args:
        image_name (str): Name of the image file (e.g., 'icon.png').
        framework (str): "tkinter" or "customtkinter".
        size (tuple): Desired dimensions; used for resizing. For animated GIFs, each frame is resized.
        theme (str): Theme name (e.g., "dark", "light"); falls back to "default" if not matched.
        grayscale (bool): Convert image to grayscale.
        rotate (int): Rotate image (or each frame) by the given degrees.
        transparency (float): Adjust brightness/opacity (0.0 to 1.0).
        format_override (str): Convert image to this format on the fly ("PNG", "JPEG", etc.).
        animated (bool): If True and image is an animated GIF, process all its frames.
        frame_delay (int): Delay (milliseconds) between frames for animated GIFs.
        tint_color (tuple or None): A tuple (R, G, B) for a tint overlay.
        tint_intensity (float): Blending factor (0.0 to 1.0) for tint; 0 means no tint.
        contrast (float): Contrast adjustment factor (1.0 means no change).
        saturation (float): Saturation adjustment factor (1.0 means no change).
    
    Returns:
        For static images:
          - A Tkinter PhotoImage or a CustomTkinter CTkImage.
        For animated GIFs:
          - A dictionary with keys "animated_frames" (a list of image objects) and "frame_delay".
            Use these frames in an animation loop.
    """
    # Lookup image data: try specified theme; if not found, fallback to "default".
    theme_dict = embedded_images.embedded_images.get(theme) or embedded_images.embedded_images.get("default")
    if not theme_dict or image_name not in theme_dict:
        raise ValueError(f"Image '{image_name}' not found in theme '{theme}'.")
    
    # Decode the stored image data.
    image_data = base64.b64decode(theme_dict[image_name])
    stream = BytesIO(image_data)
    
    img = Image.open(stream)

    # For animated GIFs: process each frame individually.
    if animated and img.format == "GIF" and getattr(img, "is_animated", False) and getattr(img, "n_frames", 1) > 1:
        frames = []
        try:
            for frame in ImageSequence.Iterator(img):
                frame = frame.convert("RGBA")
                # Apply transformations on the frame.
                if grayscale:
                    frame = ImageOps.grayscale(frame).convert("RGBA")
                if rotate:
                    frame = frame.rotate(rotate, expand=True)
                if transparency < 1.0:
                    frame = ImageEnhance.Brightness(frame).enhance(transparency)
                if size:
                    frame = frame.resize(size, Image.LANCZOS)
                if contrast != 1.0:
                    frame = ImageEnhance.Contrast(frame).enhance(contrast)
                if saturation != 1.0:
                    frame = ImageEnhance.Color(frame).enhance(saturation)
                if tint_color is not None and tint_intensity > 0.0:
                    overlay = Image.new("RGBA", frame.size, tint_color + (255,))
                    frame = Image.blend(frame, overlay, tint_intensity)
                if format_override:
                    buffer = BytesIO()
                    frame.save(buffer, format=format_override)
                    frame = Image.open(BytesIO(buffer.getvalue()))
    
                # Convert frame to the appropriate image object.
                if framework.lower() == "customtkinter":
                    import customtkinter as ctk
                    frame_obj = ctk.CTkImage(light_image=frame, size=size)
                else:
                    from PIL import ImageTk
                    frame_obj = ImageTk.PhotoImage(frame)
                frames.append(frame_obj)
        except Exception as e:
            raise RuntimeError(f"Error processing animated GIF frames: {e}")
        
        return {"animated_frames": frames, "frame_delay": frame_delay}

    # Process a static (non-animated) image.
    if grayscale:
        img = ImageOps.grayscale(img).convert("RGBA")
    if rotate:
        img = img.rotate(rotate, expand=True)
    if transparency < 1.0:
        img = ImageEnhance.Brightness(img).enhance(transparency)
    if size:
        img = img.resize(size, Image.LANCZOS)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if saturation != 1.0:
        img = ImageEnhance.Color(img).enhance(saturation)
    if tint_color is not None and tint_intensity > 0.0:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        overlay = Image.new("RGBA", img.size, tint_color + (255,))
        img = Image.blend(img, overlay, tint_intensity)
    if format_override:
        buffer = BytesIO()
        img.save(buffer, format=format_override)
        img = Image.open(BytesIO(buffer.getvalue()))
    
    if framework.lower() == "customtkinter":
        import customtkinter as ctk
        return ctk.CTkImage(light_image=img, size=size)
    else:
        from PIL import ImageTk
        return ImageTk.PhotoImage(img)
