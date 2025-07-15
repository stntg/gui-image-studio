#!/usr/bin/env python3

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Try both possible MoviePy import paths
try:
    from moviepy.editor import ImageSequenceClip
except ModuleNotFoundError:
    from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

import gui_image_studio as gis  # your library


def tint_image(img: Image.Image, color: tuple[int, int, int], alpha: float = 0.5) -> Image.Image:
    """Overlay a solid-color tint onto an RGBA image."""
    overlay = Image.new("RGBA", img.size, color + (0,))
    return Image.blend(img, overlay, alpha)


def make_frames(source: Path) -> list[Image.Image]:
    """
    Produce a sequence of demo frames:
      1. Placeholder generation if source missing
      2. Original image
      3. Rotated
      4. Tinted
      5. Contrast-adjusted via gui-image-studio API
      6. Resized
    """
    # If demo/source.png doesn't exist, generate a placeholder
    if not source.exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        placeholder = Image.new("RGBA", (400, 300), (30, 144, 255, 255))
        draw = ImageDraw.Draw(placeholder)
        font = ImageFont.load_default()
        text = "gui-image-studio\nDemo"

        # Compute size for multiline text via textbbox
        lines = text.split("\n")
        line_spacing = 4
        widths, heights = [], []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            widths.append(w)
            heights.append(h)

        total_h = sum(heights) + (len(lines) - 1) * line_spacing
        max_w = max(widths)
        x0 = (400 - max_w) / 2
        y0 = (300 - total_h) / 2

        # Draw each line centered
        y = y0
        for w, h, line in zip(widths, heights, lines):
            draw.text((x0, y), line, fill=(255, 255, 255, 255), font=font)
            y += h + line_spacing

        placeholder.save(source)

    # Load base image
    base = Image.open(source).convert("RGBA")

    frames = []
    # 1. Original
    frames.append(base)

    # 2. Rotated 30°
    frames.append(base.rotate(30, expand=True))

    # 3. Tinted
    frames.append(tint_image(base, (0, 120, 255), alpha=0.4))

    # 4. Contrast adjustment via gui-image-studio
    contr = gis.transforms.adjust_contrast(base, factor=1.5)
    frames.append(contr)

    # 5. Resized to 60%
    w, h = base.size
    frames.append(base.resize((int(w * 0.6), int(h * 0.6)), Image.LANCZOS))

    return frames


def generate_demo_video():
    """
    Assemble frames into a demo/demo.mp4 at 1 fps,
    encoded with H.264 for broad compatibility.
    """
    src = Path("demo/source.png")
    out_dir = Path("demo")
    out_dir.mkdir(exist_ok=True)
    out_mp4 = out_dir / "demo.mp4"

    frames = make_frames(src)
    clip = ImageSequenceClip(frames, fps=1)
    clip.write_videofile(
        str(out_mp4),
        codec="libx264",
        fps=1,
        ffmpeg_params=["-pix_fmt", "yuv420p"]
    )

    print(f"Demo video written to {out_mp4}")


if __name__ == "__main__":
    generate_demo_video()
