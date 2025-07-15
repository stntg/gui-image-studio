#!/usr/bin/env python3

import base64
from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip

# Monkey-patch gui-image-studio’s framework loader to return PIL.Image directly
import gui_image_studio.image_loader as _loader
_loader._create_framework_image = lambda pil_img, framework, size: pil_img

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


def embed_image(path: Path, name: str = "source.png") -> None:
    """
    Base64-encode the local PNG and inject into the default theme registry
    so get_image_from_config() can load it.
    """
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    embedded_images.embedded_images.setdefault("default", {})[name] = data


def make_frames() -> list[Image.Image]:
    """
    Build demo frames by configuring ImageConfig for each transform,
    then calling get_image_from_config(cfg) which now returns a PIL.Image.
    """
    common = dict(
        image_name="source.png",
        theme="default",
        framework="tkinter",  # ignored after our patch
        size=(400, 300),
    )

    configs = [
        ImageConfig(**common),
        ImageConfig(**common, rotate=30),
        ImageConfig(**common, tint_color=(0, 120, 255), tint_intensity=0.4),
        ImageConfig(**common, contrast=1.5),
        # smaller size override
        ImageConfig(
            image_name="source.png",
            theme="default",
            framework="tkinter",
            size=(240, 180),
        ),
    ]

    frames = []
    for cfg in configs:
        pil_img = get_image_from_config(cfg)
        frames.append(pil_img)

    return frames


def generate_demo_video():
    demo_dir = Path("demo")
    demo_dir.mkdir(exist_ok=True)
    src = demo_dir / "source.png"

    # Step-1: placeholder + embed
    if not src.exists():
        create_placeholder(src)
    embed_image(src)

    # Step-2: render PIL frames
    pil_frames = make_frames()

    # Step-3: convert to numpy arrays so MoviePy can see .shape
    np_frames = [np.array(img.convert("RGB")) for img in pil_frames]

    # Step-4: assemble video
    out_mp4 = demo_dir / "demo.mp4"
    clip = ImageSequenceClip(np_frames, fps=1)
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
