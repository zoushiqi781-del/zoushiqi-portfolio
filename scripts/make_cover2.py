"""Create a clean, pretty cover for datamining project matching the site's cream/felt aesthetic."""
import os
from PIL import Image, ImageDraw, ImageFont

DST = r"D:\clawd\shiqi-portfolio\public\works\datamining"
WATERMARK = "邹诗琪 15270025359"

def get_font(size, bold=False):
    paths = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

def add_watermark(img):
    layer = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(layer)
    font = get_font(28)
    for y in range(0, img.height, 200):
        for x in range(0, img.width, 300):
            txt_img = Image.new("RGBA", (350, 50), (0,0,0,0))
            d = ImageDraw.Draw(txt_img)
            d.text((0, 0), WATERMARK, fill=(128, 128, 128, 45), font=font)
            rotated = txt_img.rotate(30, expand=True, resample=Image.BICUBIC)
            if x + rotated.width <= layer.width and y + rotated.height <= layer.height:
                layer.paste(rotated, (x, y), rotated)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    return Image.alpha_composite(img, layer).convert("RGB")

W, H = 1200, 800
CREAM = (255, 248, 240)
BROWN = (90, 50, 35)
PINK = (224, 98, 137)
LIGHT = (245, 237, 227)

img = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(img)

# soft decorative circles (like the felt bg)
import random
random.seed(42)
for _ in range(6):
    cx = random.randint(0, W)
    cy = random.randint(0, H)
    r = random.randint(80, 200)
    colors = [(240,197,35,20), (224,98,137,15), (60,140,202,15), (223,67,49,12)]
    c = random.choice(colors)
    overlay = Image.new("RGBA", (r*2, r*2), (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([(0,0),(r*2,r*2)], fill=c)
    img_rgba = img.convert("RGBA")
    img_rgba.paste(overlay, (cx-r, cy-r), overlay)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

# Title
draw.text((80, 100), "蜜雪冰城 3·15 舆情分析", fill=BROWN, font=get_font(44, bold=True))

# Subtitle
draw.text((80, 170), '"隔夜柠檬片"事件 · 微博数据挖掘', fill=(150, 120, 100), font=get_font(24))

# Divider
draw.line([(80, 220), (500, 220)], fill=PINK, width=3)

# Description
desc = [
    "采集 1,201 条微博数据，运用 Python 进行",
    "文本预处理、词频统计、LDA 主题建模、",
    "SnowNLP 情感分析及 BERT 深度学习分类，",
    "多维度解读公众对食品安全事件的态度与情绪。",
]
y = 250
for line in desc:
    draw.text((80, y), line, fill=(120, 100, 85), font=get_font(20))
    y += 34

# Key numbers - simple, clean
y += 30
nums = [
    ("1,201", "条微博"),
    ("4", "个分析维度"),
    ("16", "张可视化"),
]
x = 80
for num, label in nums:
    draw.text((x, y), num, fill=PINK, font=get_font(36, bold=True))
    nw = get_font(36, bold=True).getlength(num)
    draw.text((x + nw + 10, y + 10), label, fill=(150, 130, 115), font=get_font(18))
    x += nw + get_font(18).getlength(label) + 50

# Bottom
draw.text((80, H - 70), "邹诗琪 · 上海大学新闻传播学院 · 广告学", fill=(180, 165, 150), font=get_font(16))
draw.text((80, H - 45), "数据挖掘期末项目 · 2025", fill=(200, 185, 170), font=get_font(14))

# Rename existing: shift all up by 1
existing = sorted([f for f in os.listdir(DST) if f.endswith('.jpg')])
for f in reversed(existing):
    num = int(f.replace('.jpg', ''))
    new_name = f"{num+1:02d}.jpg"
    os.rename(os.path.join(DST, f), os.path.join(DST, new_name))

# Save as 01.jpg
result = add_watermark(img.convert("RGBA"))
result.save(os.path.join(DST, "01.jpg"), quality=92)

files = sorted([f for f in os.listdir(DST) if f.endswith('.jpg')])
print(f"Total: {len(files)} files")
for f in files[:3]:
    print(f"  {f} ({os.path.getsize(os.path.join(DST, f))//1024}KB)")
