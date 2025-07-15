#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image

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
