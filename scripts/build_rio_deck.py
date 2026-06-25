# -*- coding: utf-8 -*-
"""Build the Rio微醺 gallery: a branded cover + 9 best frames from the 30s TVC."""
import os
from PIL import Image, ImageDraw, ImageFont

FR = r"D:\clawd\tmp_rio"
DST = r"D:\clawd\shiqi-portfolio\public\works\rio"
os.makedirs(DST, exist_ok=True)

CREAM = (255, 248, 240); BROWN = (90, 50, 35); PINK = (224, 98, 137)
BLUE = (60, 140, 202); RED = (223, 67, 49); YELLOW = (240, 197, 35); GREY = (150, 130, 120)
FONT = r"C:\Windows\Fonts\msyh.ttc"; FONTB = r"C:\Windows\Fonts\msyhbd.ttc"
WM = "邹诗琪 · Rio微醺 TVC"

def f(s, b=False): return ImageFont.truetype(FONTB if b else FONT, s)
def tw(d, t, fo): bb = d.textbbox((0, 0), t, font=fo); return bb[2]-bb[0], bb[3]-bb[1]

def watermark(img):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    tile = Image.new("RGBA", (440, 70), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((0, 0), WM, fill=(255, 255, 255, 42), font=f(24))
    tile = tile.rotate(28, expand=True, resample=Image.BICUBIC)
    for y in range(0, img.height, 320):
        for x in range(-80, img.width, 540):
            layer.paste(tile, (x, y), tile)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

# ---- cover ----
W, H = 1600, 900
img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img)
d.rectangle([(0, 0), (W, H)], fill=BROWN)
# hero frame card
hero = Image.open(os.path.join(FR, "f010.jpg")).convert("RGB")
cardw, cardh = 880, 495
hero = hero.resize((cardw, cardh), Image.LANCZOS)
hx, hy = (W - cardw)//2, 150
d.rounded_rectangle([(hx-6, hy-6), (hx+cardw+6, hy+cardh+6)], radius=20, fill=(60, 34, 24))
img.paste(hero, (hx, hy))
# play button
pcx, pcy = W//2, hy + cardh//2
d.ellipse([(pcx-46, pcy-46), (pcx+46, pcy+46)], fill=(255, 255, 255, 230))
d.polygon([(pcx-15, pcy-22), (pcx-15, pcy+22), (pcx+24, pcy)], fill=BROWN)
# eyebrow + title
eb = "RIO 微醺 · 30 秒 TVC 视频广告"
d.text(((W - tw(d, eb, f(26))[0])//2, 80), eb, fill=(255, 248, 240), font=f(26))
t1 = "今天，选「微醺」"
d.text(((W - tw(d, t1, f(56, True))[0])//2, hy + cardh + 40), t1, fill=YELLOW, font=f(56, True))
sub = "脚本 · 拍摄 · 剪辑 · 一支关于城市青年微醺生活的短片"
d.text(((W - tw(d, sub, f(24))[0])//2, hy + cardh + 120), sub, fill=CREAM, font=f(24))
# award chip + author
chip = "学院奖"
cw = tw(d, chip, f(24, True))[0] + 52
d.rounded_rectangle([((W-cw)//2, 800), ((W+cw)//2, 850)], radius=25, fill=RED)
d.text(((W - tw(d, chip, f(24, True))[0])//2, 810), chip, fill="white", font=f(24, True))
img.save(os.path.join(DST, "01.jpg"), quality=90)
print("cover -> 01.jpg")

# ---- frames ----
FRAMES = ["f003", "f014", "f010", "f016", "f020", "f024", "f025", "f026", "f028"]
for i, name in enumerate(FRAMES, start=2):
    im = Image.open(os.path.join(FR, name + ".jpg")).convert("RGB")
    watermark(im).save(os.path.join(DST, f"{i:02d}.jpg"), quality=86)
    print(f"{name} -> {i:02d}.jpg")
print("total", len(os.listdir(DST)))
