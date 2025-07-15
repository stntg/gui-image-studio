#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image
from moviepy.editor import ImageSequenceClip
import gui_image_studio as gis  # your library

def tint_image(img: Image.Image, color: tuple[int,int,int], alpha=0.5):
    """Overlay a solid color to tint."""
    overlay = Image.new("RGBA", img.size, color + (0,))
    return Image.blend(img, overlay, alpha)

def make_frames(source: Path):
    """Use gui-image-studio’s API + PIL to produce a few demo frames."""
    # load via PIL for max control
    base = Image.open(source).convert("RGBA")

    frames: list[Image.Image] = []
    # 1. Original
    frames.append(base)

    # 2. Rotate 30°
    frames.append(base.rotate(30, expand=True))

    # 3. Tint blue via our helper
    frames.append(tint_image(base, (0, 120, 255), alpha=0.4))

    # 4. Use gui-image-studio’s API to adjust contrast
    contr_img = gis.transforms.adjust_contrast(base, factor=1.5)
    frames.append(contr_img)

    # 5. Resize down/up
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
    clip.write_videofile(str(out_mp4), codec="libx264", fps=1, 
                         ffmpeg_params=["-pix_fmt", "yuv420p"])
    print(f"Demo video written to {out_mp4}")

if __name__ == "__main__":
    generate_demo_video()