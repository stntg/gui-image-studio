#!/usr/bin/env python3

import os
import base64
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip

from gui_image_studio import embedded_images, get_image
from gui_image_studio.image_loader import ImageConfig


def create_placeholder(path: Path, size: Tuple[int, int] = (400, 300)) -> None:
    """Generate a fallback source PNG if one doesn't exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", size, (30, 144, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text = "gui-image-studio\nDemo"
    lines = text.split("\n")
    spacing = 4
    widths, heights = [], []

    for line in lines:
        x0, y0, x1, y1 = draw.textbbox((0, 0), line, font=font)
        widths.append(x1 - x0)
        heights.append(y1 - y0)

    total_h = sum(heights) + spacing * (len(lines) - 1)
    max_w = max(widths)
    x0 = (size[0] - max_w) / 2
    y0 = (size[1] - total_h) / 2
    y = y0

    for line, h in zip(lines, heights):
        draw.text((x0, y), line, font=font, fill="white")
        y += h + spacing

    img.save(path)


def embed_image(path: Path) -> None:
    """Embed the PNG file into the default theme registry for get_image."""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        embedded_images.embedded_images.setdefault("default", {})["source.png"] = encoded


def extract_pil_image(config: ImageConfig) -> Image.Image:
    """Extract raw PIL image from framework-specific get_image result."""
    # Since we’re using framework="tkinter", the result is an ImageTk.PhotoImage
    result = get_image_from_config(config)
    if hasattr(result, "_PhotoImage__photo"):
        # extract from Tkinter internal object
        return Image.open(result._PhotoImage__photo)  # crude workaround if needed
    else:
        raise ValueError("Unsupported image wrapper returned")


def make_frames(image_name: str) -> list[Image.Image]:
    """Create demo frames using get_image transformations."""
    base_kwargs = {
        "image_name": image_name,
        "framework": "tkinter",
        "size": (400, 300),
        "theme": "default"
    }

    frames = []

    # 1. Original
    cfg1 = ImageConfig(**base_kwargs)
    frames.append(get_image(cfg1.image_name, **cfg1.__dict__)._PhotoImage__photo.zoom(1))

    # 2. Rotated
    cfg2 = ImageConfig(**base_kwargs, rotate=30)
    frames.append(get_image(cfg2.image_name, **cfg2.__dict__)._PhotoImage__photo.zoom(1))

    # 3. Tinted
    cfg3 = ImageConfig(**base_kwargs, tint_color=(0, 120, 255), tint_intensity=0.4)
    frames.append(get_image(cfg3.image_name, **cfg3.__dict__)._PhotoImage__photo.zoom(1))

    # 4. Contrast
    cfg4 = ImageConfig(**base_kwargs, contrast=1.5)
    frames.append(get_image(cfg4.image_name, **cfg4.__dict__)._PhotoImage__photo.zoom(1))

    # 5. Resize smaller
    cfg5 = ImageConfig(**base_kwargs, size=(240, 180))
    frames.append(get_image(cfg5.image_name, **cfg5.__dict__)._PhotoImage__photo.zoom(1))

    return frames


def generate_demo_video():
    src_path = Path("demo/source.png")
    out_dir = Path("demo")
    out_dir.mkdir(exist_ok=True)
    out_mp4 = out_dir / "demo.mp4"

    if not src_path.exists():
        create_placeholder(src_path)
    embed_image(src_path)

    frames = make_frames("source.png")

    # Ensure all are PIL Images
    clip = ImageSequenceClip(frames, fps=1)
    clip.write_videofile(str(out_mp4),
                         codec="libx264",
                         fps=1,
                         ffmpeg_params=["-pix_fmt", "yuv420p"],
                         logger=None)

    print(f"✅ Demo video created at {out_mp4.absolute()}")


if __name__ == "__main__":
    generate_demo_video()
