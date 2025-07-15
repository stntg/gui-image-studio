#!/usr/bin/env python3

import os
import base64
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip

from gui_image_studio.image_loader import embedded_images, ImageConfig, get_image_from_config


def create_placeholder(path: Path, size: Tuple[int, int] = (400, 300)) -> None:
    """Generate a fallback PNG if demo/source.png is missing."""
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", size, (30, 144, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text = "gui-image-studio\nDemo"
    lines = text.split("\n")
    spacing = 4

    # Measure text
    widths, heights = [], []
    for line in lines:
        x0, y0, x1, y1 = draw.textbbox((0, 0), line, font=font)
        widths.append(x1 - x0)
        heights.append(y1 - y0)

    total_h = sum(heights) + spacing * (len(lines) - 1)
    max_w = max(widths)
    x0 = (size[0] - max_w) / 2
    y0 = (size[1] - total_h) / 2

    # Draw each line centered
    y = y0
    for line, h in zip(lines, heights):
        draw.text((x0, y), line, font=font, fill="white")
        y += h + spacing

    img.save(path)


def embed_image(path: Path, name: str = "source.png") -> None:
    """
    Base64-encode the local PNG and inject into embedded_images
    under the "default" theme so get_image_from_config() can load it.
    """
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    embedded_images.embedded_images.setdefault("default", {})[name] = data


def make_frames() -> list[Image.Image]:
    """
    Build demo frames by configuring ImageConfig for each transform
    and extracting the PIL Image from the Tkinter PhotoImage wrapper.
    """
    # Shared parameters for most frames
    common_args = dict(
        image_name="source.png",
        theme="default",
        framework="tkinter",
        size=(400, 300),
    )

    configs = [
        ImageConfig(**common_args),
        ImageConfig(**common_args, rotate=30),
        ImageConfig(**common_args, tint_color=(0, 120, 255), tint_intensity=0.4),
        ImageConfig(**common_args, contrast=1.5),
        # Explicitly override size here without **common_args
        ImageConfig(
            image_name="source.png",
            theme="default",
            framework="tkinter",
            size=(240, 180)
        ),
    ]

    frames: list[Image.Image] = []
    for cfg in configs:
        photo = get_image_from_config(cfg)
        # For tkinter, PhotoImage keeps the PIL image in _PhotoImage__photo
        pil_img = photo._PhotoImage__photo
        frames.append(pil_img)

    return frames


def generate_demo_video():
    demo_dir = Path("demo")
    demo_dir.mkdir(exist_ok=True)
    src = demo_dir / "source.png"

    # Create & embed placeholder if missing
    if not src.exists():
        create_placeholder(src)
    embed_image(src)

    # Render frames and write video
    out_mp4 = demo_dir / "demo.mp4"
    frames = make_frames()
    clip = ImageSequenceClip(frames, fps=1)
    clip.write_videofile(
        str(out_mp4),
        codec="libx264",
        fps=1,
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        logger=None,
    )

    print(f"✅ Demo video written to {out_mp4.absolute()}")


if __name__ == "__main__":
    generate_demo_video()
