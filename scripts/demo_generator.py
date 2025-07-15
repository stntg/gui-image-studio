#!/usr/bin/env python3

import base64
from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from moviepy import ImageSequenceClip

# Monkey-patch gui-image-studio to return raw PIL.Image
import gui_image_studio.image_loader as _loader
_loader._create_framework_image = lambda pil_img, framework, size: pil_img

from gui_image_studio.image_loader import embedded_images, ImageConfig, get_image_from_config


DEMO_SIZE = (400, 300)  # canonical width × height


def create_placeholder(path: Path, size: Tuple[int,int] = (400, 300)) -> None:
    """
    Generate a colorful, shape-filled demo image so your rotations, tints
    and contrasts really stand out.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    w, h = size

    # 1) Gradient background (red→blue horizontally, green ramp vertically)
    img = Image.new("RGB", size)
    for x in range(w):
        for y in range(h):
            r = int(255 * x / w)
            b = 255 - r
            g = int(128 + 127 * (y / h))
            img.putpixel((x, y), (r, g, b))

    draw = ImageDraw.Draw(img)

    # 2) White rectangle
    draw.rectangle((50,  50, 150, 100), outline="white", width=4)

    # 3) Yellow ellipse
    draw.ellipse((200, 50, 300, 150), outline="yellow", width=4)

    # 4) Green triangle
    tri = [(100, 220), (200, 220), (150, 140)]
    draw.polygon(tri, outline="green", width=4)

    # 5) Diagonal white line
    draw.line((0, h, w, 0), fill="white", width=2)

    # 6) “Demo” text in bottom-right
    font = ImageFont.load_default()
    text = "Demo"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((w - tw - 10, h - th - 10), text, fill="white", font=font)

    img.save(path)


def embed_image(path: Path, name: str = "source.png") -> None:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    embedded_images.embedded_images.setdefault("default", {})[name] = data


def make_frames() -> list[Image.Image]:
    """
    Generate a list of PIL Images, all forced to DEMO_SIZE via ImageOps.fit
    so that ImageSequenceClip will accept them.
    """
    common = dict(
        image_name="source.png",
        theme="default",
        framework="tkinter",  # ignored by our monkey-patch
        size=DEMO_SIZE,
    )

    configs = [
        ImageConfig(**common),
        ImageConfig(**common, rotate=30),
        ImageConfig(**common, tint_color=(0, 120, 255), tint_intensity=0.4),
        ImageConfig(**common, contrast=1.5),
        # smaller logical size, but we’ll fit it back to DEMO_SIZE below
        ImageConfig(image_name="source.png", theme="default", framework="tkinter", size=(240, 180)),
    ]

    frames: list[Image.Image] = []
    for cfg in configs:
        pil = get_image_from_config(cfg)  # returns PIL.Image thanks to monkey-patch
        # ensure exact DEMO_SIZE by center-cropping or padding
        fit = ImageOps.fit(pil.convert("RGBA"), DEMO_SIZE, centering=(0.5, 0.5))
        frames.append(fit)

    return frames


def generate_demo_video():
    demo_dir = Path("demo")
    demo_dir.mkdir(exist_ok=True)
    src = demo_dir / "source.png"

    if not src.exists():
        create_placeholder(src)
    embed_image(src)

    frames = make_frames()

    # Convert to NumPy arrays for MoviePy
    arrays = [np.array(img.convert("RGB")) for img in frames]

    out_mp4 = demo_dir / "demo.mp4"
    clip = ImageSequenceClip(arrays, fps=1)
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
