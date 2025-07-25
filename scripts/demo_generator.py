#!/usr/bin/env python3

import base64
from pathlib import Path
from typing import Tuple

import numpy as np
from moviepy import ImageSequenceClip
from PIL import Image, ImageDraw, ImageFont, ImageOps

import gui_image_studio.image_loader as _loader
from gui_image_studio.image_loader import (
    ImageConfig,
    embedded_images,
    get_image_from_config,
)

# Monkey-patch gui-image-studio so it returns raw PIL Images
_loader._create_framework_image = lambda pil_img, framework, size: pil_img
DEMO_SIZE = (400, 300)
FONT = ImageFont.load_default()


def create_placeholder(path: Path, size: Tuple[int, int] = DEMO_SIZE) -> None:
    """
    Generate a visually distinctive demo image:
      - Horizontal red→blue gradient with a green ramp
      - White rectangle, yellow ellipse, green triangle, diagonal line
      - “Demo” label bottom-right
    """
    w, h = size
    img = Image.new("RGB", size)
    pixels = img.load()
    for x in range(w):
        for y in range(h):
            r = int(255 * x / w)
            b = 255 - r
            g = int(128 + 127 * (y / h))
            pixels[x, y] = (r, g, b)

    draw = ImageDraw.Draw(img)
    # 1) White rectangle
    draw.rectangle((50, 50, 150, 100), outline="white", width=4)
    # 2) Yellow ellipse
    draw.ellipse((200, 50, 300, 150), outline="yellow", width=4)
    # 3) Green triangle
    triangle = [(100, 220), (200, 220), (150, 140)]
    draw.polygon(triangle, outline="green", width=4)
    # 4) Diagonal white line
    draw.line((0, h, w, 0), fill="white", width=2)
    # 5) “Demo” bottom-right
    text = "Demo"
    bbox = draw.textbbox((0, 0), text, font=FONT)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        (w - tw - 10, h - th - 10),
        text,
        font=FONT,
        fill="white",
        stroke_width=1,
        stroke_fill="black",
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def embed_image(path: Path, name: str = "source.png") -> None:
    """
    Base64-encode and inject into embedded_images['default'] so our loader sees it.
    """
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    embedded_images.embedded_images.setdefault("default", {})[name] = encoded


def make_frames() -> list[Image.Image]:
    """
    Create 5 frames via ImageConfig transforms, fit to DEMO_SIZE,
    then overlay a dynamic label per frame.
    """
    common = dict(
        image_name="source.png",
        theme="default",
        framework="tkinter",
        size=DEMO_SIZE,
    )

    configs = [
        ImageConfig(**common),
        ImageConfig(**common, rotate=30),
        ImageConfig(**common, tint_color=(0, 120, 255), tint_intensity=0.4),
        ImageConfig(**common, contrast=1.5),
        ImageConfig(
            image_name="source.png",
            theme="default",
            framework="tkinter",
            size=(240, 180),
        ),
    ]

    def label_for(cfg: ImageConfig) -> str:
        if cfg.rotate:
            return f"Rotate {cfg.rotate}°"
        if cfg.tint_intensity > 0:
            return f"Tint {int(cfg.tint_intensity * 100)}%"
        if cfg.contrast != 1.0:
            return f"Contrast ×{cfg.contrast}"
        if cfg.size != DEMO_SIZE:
            return f"Resize {int(cfg.size[0]/DEMO_SIZE[0]*100)}%"
        return "Original"

    frames = []
    for cfg in configs:
        pil = get_image_from_config(cfg)  # raw PIL via monkey-patch
        fit = ImageOps.fit(pil.convert("RGBA"), DEMO_SIZE)  # uniform sizing
        draw = ImageDraw.Draw(fit)
        # dynamic label top-left
        txt = label_for(cfg)
        draw.text(
            (10, 10), txt, font=FONT, fill="white", stroke_width=2, stroke_fill="black"
        )
        frames.append(fit)

    return frames


def generate_demo_video():
    demo_dir = Path("demo")
    demo_dir.mkdir(exist_ok=True)
    src = demo_dir / "source.png"

    if not src.exists():
        create_placeholder(src)
    embed_image(src)

    pil_frames = make_frames()
    arrays = [np.array(img.convert("RGB")) for img in pil_frames]

    out = demo_dir / "demo.mp4"
    clip = ImageSequenceClip(arrays, fps=1)
    clip.write_videofile(
        str(out),
        codec="libx264",
        fps=1,
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        logger=None,
    )

    print(f"✅ Demo video written to {out.absolute()}")


if __name__ == "__main__":
    generate_demo_video()
