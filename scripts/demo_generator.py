#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image
from PIL import ImageDraw, ImageFont

# Try both imports
try:
    from moviepy.editor import ImageSequenceClip
except ModuleNotFoundError:
    from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

import gui_image_studio as gis  # your library

def tint_image(img: Image.Image, color: tuple[int,int,int], alpha=0.5):
    overlay = Image.new("RGBA", img.size, color + (0,))
    return Image.blend(img, overlay, alpha)

def make_frames(source: Path):
    # If demo/source.png is missing, generate a simple placeholder
    if not source.exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        placeholder = Image.new("RGBA", (400, 300), (30, 144, 255, 255))
        draw = ImageDraw.Draw(placeholder)
        font = ImageFont.load_default()
        text = "gui-image-studio\nDemo"
        # manually compute multiline size
        lines = text.split("\n")
        line_spacing = 4
        widths = []
        heights = []
        for line in lines:
            w, h_line = draw.textsize(line, font=font)
            widths.append(w)
            heights.append(h_line)
        total_height = sum(heights) + (len(lines) - 1) * line_spacing
        max_width = max(widths)
        x0 = (400 - max_width) / 2
        y0 = (300 - total_height) / 2
        # draw each line
        y = y0
        for i, line in enumerate(lines):
            draw.text((x0, y), line, fill=(255,255,255,255), font=font)
            y += heights[i] + line_spacing
        placeholder.save(source)
    base = Image.open(source).convert("RGBA")
    frames = [base]
    frames.append(base.rotate(30, expand=True))
    frames.append(tint_image(base, (0, 120, 255), alpha=0.4))
    # example gui-image-studio transform
    contr_img = gis.transforms.adjust_contrast(base, factor=1.5)
    frames.append(contr_img)
    w, h = base.size
    frames.append(base.resize((int(w * 0.6), int(h * 0.6)), Image.LANCZOS))
    return frames

def generate_demo_video():
    src = Path("demo/source.png")
    out_dir = Path("demo")
    out_dir.mkdir(exist_ok=True)
    out_mp4 = out_dir / "demo.mp4"

    frames = make_frames(src)
    clip = ImageSequenceClip([frame for frame in frames], fps=1)
    clip.write_videofile(str(out_mp4),
                         codec="libx264",
                         fps=1,
                         ffmpeg_params=["-pix_fmt", "yuv420p"])
    print(f"Demo video written to {out_mp4}")

if __name__ == "__main__":
    generate_demo_video()
