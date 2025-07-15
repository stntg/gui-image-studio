#!/usr/bin/env python3

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

import gui_image_studio as gis
from gui_image_studio.image_loader import ImageConfig, get_image_from_config


def make_placeholder(path: Path, size=(400, 300)) -> None:
    """Create a simple fallback PNG if demo/source.png is missing."""
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

    total_h = sum(heights) + (len(lines) - 1) * spacing
    max_w = max(widths)
    x_start = (size[0] - max_w) / 2
    y_start = (size[1] - total_h) / 2

    y = y_start
    for line, h in zip(lines, heights):
        draw.text((x_start, y), line, font=font, fill="white")
        y += h + spacing

    img.save(path)


def make_frames(source: Path) -> list[Image.Image]:
    """
    Build frames using get_image_from_config() with different transformations.
    Since get_image_from_config returns a framework-specific object,
    we grab the raw PIL Image via its internal config logic.
    """
    if not source.exists():
        make_placeholder(source)

    frames = []
    base_params = {
        "image_name": str(source.name),
        "theme": "default",
        "framework": "tkinter",
        "size": (400, 300),
    }

    # 1. Original
    cfg1 = ImageConfig(**base_params)
    img1 = get_image_from_config(cfg1)._PhotoImage__photo.zoom(1)  # workaround to extract
    frames.append(cfg1.to_transforms_dict()["size"])  # insert placeholder size

    # 2. Rotated
    cfg2 = ImageConfig(**base_params, rotate=30)
    img2 = get_image_from_config(cfg2)._PhotoImage__photo.zoom(1)
    frames.append(img2)

    # 3. Tinted
    cfg3 = ImageConfig(**base_params, tint_color=(0, 120, 255), tint_intensity=0.4)
    img3 = get_image_from_config(cfg3)._PhotoImage__photo.zoom(1)
    frames.append(img3)

    # 4. Contrast
    cfg4 = ImageConfig(**base_params, contrast=1.5)
    img4 = get_image_from_config(cfg4)._PhotoImage__photo.zoom(1)
    frames.append(img4)

    # 5. Resized to 60%
    cfg5 = ImageConfig(**base_params, size=(240, 180))
    img5 = get_image_from_config(cfg5)._PhotoImage__photo.zoom(1)
    frames.append(img5)

    # Convert each frame to actual Image object if needed
    pil_frames = [Image.open(frame) if isinstance(frame, str) else frame for frame in frames]
    return pil_frames


def generate_demo_video():
    src = Path("demo/source.png")
    out_dir = Path("demo")
    out_dir.mkdir(exist_ok=True)
    out_mp4 = out_dir / "demo.mp4"

    frames = make_frames(src)
    clip = ImageSequenceClip(frames, fps=1)
    clip.write_videofile(str(out_mp4),
                         codec="libx264",
                         fps=1,
                         ffmpeg_params=["-pix_fmt", "yuv420p"])

    print(f"✅ Demo video written to {out_mp4}")


if __name__ == "__main__":
    generate_demo_video()
