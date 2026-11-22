from pathlib import Path
import numpy as np
from PIL import Image
import imageio.v2 as imageio

W, H, FPS = 1280, 720, 24
DURATION = 15
ASSETS = Path("assets")
OUT = Path("anime-hotel-romance.mp4")

def load(name):
    p = ASSETS / name
    if not p.exists():
        raise SystemExit(f"Missing {p}. Check the assets folder.")
    return Image.open(p).convert("RGB")

def cover(img, zoom=1.0, pan_x=0.5, pan_y=0.5):
    scale = max(W / img.width, H / img.height) * zoom
    nw, nh = int(img.width * scale), int(img.height * scale)
    im = img.resize((nw, nh), Image.Resampling.LANCZOS)
    x = int(max(0, nw-W) * pan_x)
    y = int(max(0, nh-H) * pan_y)
    return im.crop((x, y, x+W, y+H))

def fit(img):
    bg = Image.new("RGB", (W, H), (241, 229, 211))
    scale = min(W/img.width, H/img.height)
    nw, nh = int(img.width*scale), int(img.height*scale)
    im = img.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(im, ((W-nw)//2, (H-nh)//2))
    return bg

def main():
    man = load("Gemini_Generated_Image_sdidi5sdidi5sdid.jpg")
    hotel = load("Code_Generated_Image (7).png")
    woman = load("Ficha de personaje anime en tonos lavanda.png")
    shots = [
        (3.2, hotel, "wide"),
        (2.0, man, "sheet"),
        (2.0, woman, "sheet"),
        (3.0, hotel, "push"),
        (2.3, man, "close"),
        (2.5, woman, "close"),
    ]
    writer = imageio.get_writer(str(OUT), fps=FPS, codec="libx264",
        quality=8, macro_block_size=1, ffmpeg_params=["-pix_fmt", "yuv420p"])
    try:
        for duration, img, mode in shots:
            frames = int(duration * FPS)
            for i in range(frames):
                t = i / max(1, frames-1)
                if mode == "sheet":
                    frame = fit(img)
                elif mode == "wide":
                    frame = cover(img, 1.0 + 0.035*t)
                elif mode == "push":
                    frame = cover(img, 1.0 + 0.12*t)
                else:
                    frame = cover(img, 1.15 + 0.10*t, 0.5, 0.28)
                fade = min(1.0, (i+1)/8, (frames-i)/8)
                if fade < 1:
                    frame = Image.blend(Image.new("RGB", (W,H), (18,12,16)), frame, fade)
                writer.append_data(np.asarray(frame))
    finally:
        writer.close()
    print(f"Created {OUT}")

if __name__ == "__main__":
    main()
