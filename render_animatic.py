from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageEnhance
import imageio.v2 as imageio

W, H, FPS, DURATION = 1280, 720, 24, 15
ASSETS = Path("assets")
OUT = Path("anime-hotel-romance.mp4")

def load(name):
    p = ASSETS / name
    if not p.exists():
        raise SystemExit(f"Missing {p}. Upload the three reference images listed in README.md.")
    return Image.open(p).convert("RGB")

def cover(img, zoom=1.0, pan_x=0.5, pan_y=0.5):
    scale = max(W / img.width, H / img.height) * zoom
    nw, nh = int(img.width * scale), int(img.height * scale)
    im = img.resize((nw, nh), Image.Resampling.LANCZOS)
    max_x, max_y = max(0, nw-W), max(0, nh-H)
    x = int(max_x * pan_x)
    y = int(max_y * pan_y)
    return im.crop((x, y, x+W, y+H))

def fit(img):
    bg = Image.new("RGB", (W,H), (241,229,211))
    scale = min(W/img.width, H/img.height)
    nw, nh = int(img.width*scale), int(img.height*scale)
    im = img.resize((nw,nh), Image.Resampling.LANCZOS)
    bg.paste(im, ((W-nw)//2,(H-nh)//2))
    return bg

def main():
    man, hotel, woman = load("man.png"), load("hotel.png"), load("woman.png")
    # Storyboard-like animatic: establish corridor, introduce each character,
    # hold on the meeting location, then close on both character references.
    shots = [
        (0.0, 3.2, hotel, "wide"),
        (3.2, 5.2, man, "sheet"),
        (5.2, 7.2, woman, "sheet"),
        (7.2, 10.2, hotel, "push"),
        (10.2, 12.5, man, "close"),
        (12.5, 15.0, woman, "close"),
    ]
    writer = imageio.get_writer(str(OUT), fps=FPS, codec="libx264",
        quality=8, macro_block_size=1, ffmpeg_params=["-pix_fmt","yuv420p"])
    try:
        for start, end, img, mode in shots:
            frames = int((end-start)*FPS)
            for i in range(frames):
                t = i / max(1, frames-1)
                if mode == "sheet":
                    frame = fit(img)
                elif mode == "wide":
                    frame = cover(img, 1.0 + 0.035*t, 0.5, 0.5)
                elif mode == "push":
                    frame = cover(img, 1.0 + 0.12*t, 0.5, 0.5)
                else:
                    frame = cover(img, 1.15 + 0.10*t, 0.5, 0.28)
                # Gentle fade at shot boundaries.
                fade = min(1.0, (i+1)/8, (frames-i)/8)
                if fade < 1:
                    frame = Image.blend(Image.new("RGB",(W,H),(18,12,16)), frame, fade)
                writer.append_data(np.asarray(frame))
    finally:
        writer.close()
    print(f"Created {OUT}")

if __name__ == "__main__":
    main()
