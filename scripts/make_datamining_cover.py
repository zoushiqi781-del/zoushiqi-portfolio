"""Create a proper cover/intro page for the datamining project."""
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
    step_x, step_y = 300, 200
    for y in range(-img.height, img.height * 2, step_y):
        for x in range(-img.width, img.width * 2, step_x):
            txt_img = Image.new("RGBA", (350, 50), (0,0,0,0))
            d = ImageDraw.Draw(txt_img)
            d.text((0, 0), WATERMARK, fill=(128, 128, 128, 45), font=font)
            rotated = txt_img.rotate(30, expand=True, resample=Image.BICUBIC)
            if 0 <= x < layer.width - rotated.width and 0 <= y < layer.height - rotated.height:
                layer.paste(rotated, (x, y), rotated)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    return Image.alpha_composite(img, layer).convert("RGB")

# --- Rename existing files: shift all by 1 ---
existing = sorted([f for f in os.listdir(DST) if f.endswith('.jpg')])
# Rename in reverse to avoid collision
for f in reversed(existing):
    num = int(f.replace('.jpg', ''))
    new_name = f"{num+1:02d}.jpg"
    os.rename(os.path.join(DST, f), os.path.join(DST, new_name))
    print(f"  Renamed {f} -> {new_name}")

# --- Create cover page as 01.jpg ---
W, H = 1200, 800
img = Image.new("RGB", (W, H), (90, 50, 35))  # felt-brown background
draw = ImageDraw.Draw(img)

# Decorative top stripe
for i, color in enumerate([(240, 197, 35), (224, 98, 137), (223, 67, 49), (60, 140, 202)]):
    draw.rectangle([(i * W // 4, 0), ((i+1) * W // 4, 8)], fill=color)

# Main title
title_font = get_font(48, bold=True)
sub_font = get_font(28)
body_font = get_font(20)
small_font = get_font(16)
tag_font = get_font(14, bold=True)

y = 60
draw.text((60, y), "蜜雪冰城 3·15", fill=(240, 197, 35), font=title_font)
y += 70
draw.text((60, y), '"隔夜柠檬片"事件', fill=(255, 248, 240), font=title_font)
y += 80

# Subtitle
draw.text((60, y), "微博舆情数据挖掘与分析", fill=(255, 248, 240, 200), font=sub_font)
y += 50

# Divider line
draw.line([(60, y), (W - 60, y)], fill=(255, 248, 240, 80), width=1)
y += 30

# Project description
desc_lines = [
    "基于 Python 对蜜雪冰城 3·15 食品安全事件进行微博舆情分析，",
    "涵盖数据采集、文本预处理、词频统计、LDA 主题模型、",
    "SnowNLP 情感分析及 BERT 深度学习情感分类。",
]
for line in desc_lines:
    draw.text((60, y), line, fill=(220, 210, 200), font=body_font)
    y += 32

y += 20

# Stats boxes
stats = [
    ("1,201", "条微博数据"),
    ("1,186", "条有效文本"),
    ("5,000", "维TF-IDF特征"),
    ("4", "个分析维度"),
]
box_w = (W - 120 - 45) // 4
for i, (num, label) in enumerate(stats):
    bx = 60 + i * (box_w + 15)
    draw.rounded_rectangle([(bx, y), (bx + box_w, y + 90)], radius=12, fill=(70, 40, 28))
    draw.text((bx + 20, y + 12), num, fill=(240, 197, 35), font=get_font(32, bold=True))
    draw.text((bx + 20, y + 55), label, fill=(180, 170, 160), font=small_font)

y += 115

# Tech tags
tags = ["Python", "jieba", "TF-IDF", "LDA", "SnowNLP", "BERT", "matplotlib", "微博爬虫"]
tag_colors = [(60,140,202), (224,98,137), (240,197,35), (223,67,49), (60,140,202), (224,98,137), (240,197,35), (223,67,49)]
tx = 60
for i, tag in enumerate(tags):
    tw = tag_font.getlength(tag) + 24
    color = tag_colors[i % len(tag_colors)]
    draw.rounded_rectangle([(tx, y), (tx + tw, y + 30)], radius=15, fill=color)
    draw.text((tx + 12, y + 6), tag, fill="white", font=tag_font)
    tx += tw + 10

# Bottom info
draw.text((60, H - 50), "邹诗琪 · 上海大学 · 新闻传播学院 · 广告学", fill=(150, 130, 120), font=small_font)
draw.text((W - 300, H - 50), "数据挖掘期末项目 · 2025", fill=(150, 130, 120), font=small_font)

result = add_watermark(img.convert("RGBA"))
result.save(os.path.join(DST, "01.jpg"), quality=92)
print(f"\nCreated cover: 01.jpg")

# Final count
files = sorted([f for f in os.listdir(DST) if f.endswith('.jpg')])
print(f"Total files: {len(files)}")
for f in files:
    print(f"  {f} ({os.path.getsize(os.path.join(DST, f)) // 1024}KB)")
