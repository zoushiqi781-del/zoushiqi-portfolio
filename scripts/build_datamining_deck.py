# -*- coding: utf-8 -*-
"""
Rebuild the 蜜雪冰城 datamining gallery as a clean, brand-consistent case-study deck.
Source of truth: the 4 real notebooks on the Desktop + the report docx.
- 01 cover (16:9 brown title slide, matches huanjiang/sanfu style)
- 02 overview (real numbers from the report)
- 03-12 the 10 REAL chart outputs, each framed with a title bar + one-line takeaway
Subtle single watermark only (no ugly tiled mess, no fake code-editor pages).
"""
import os
from PIL import Image, ImageDraw, ImageFont

CHARTS = r"D:\clawd\tmp_dm"          # the 10 extracted real charts (01.png..10.png)
DST = r"D:\clawd\tmp_dm\slides"       # output (reviewed before swapping into public)
os.makedirs(DST, exist_ok=True)

W, H = 1600, 900
CREAM = (255, 248, 240)
BROWN = (90, 50, 35)
PINK = (224, 98, 137)
BLUE = (60, 140, 202)
RED = (223, 67, 49)
YELLOW = (240, 197, 35)
CHARCOAL = (26, 26, 26)
GREY = (150, 130, 120)
WATERMARK = "邹诗琪 · 蜜雪冰城3·15舆情分析"

FONT = r"C:\Windows\Fonts\msyh.ttc"
FONTB = r"C:\Windows\Fonts\msyhbd.ttc"

def f(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)

def tw(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]

def wrap_cjk(draw, text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        test = cur + ch
        if tw(draw, test, font)[0] > max_w and cur:
            lines.append(cur); cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines

def watermark(img):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    font = f(26)
    tile = Image.new("RGBA", (520, 80), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((0, 0), WATERMARK, fill=(120, 120, 120, 34), font=font)
    tile = tile.rotate(28, expand=True, resample=Image.BICUBIC)
    for y in range(0, H, 360):
        for x in range(-100, W, 620):
            layer.paste(tile, (x, y), tile)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

def base():
    img = Image.new("RGB", (W, H), CREAM)
    return img, ImageDraw.Draw(img)

def footer(draw):
    draw.text((60, H - 46), "邹诗琪 · 上海大学新闻传播学院 · 广告学", fill=GREY, font=f(18))
    t = "Python · jieba · scikit-learn · SnowNLP"
    draw.text((W - 60 - tw(draw, t, f(18))[0], H - 46), t, fill=GREY, font=f(18))


def make_cover(out):
    img, d = base()
    # brown panel
    d.rectangle([(0, 0), (W, H)], fill=CREAM)
    d.rectangle([(0, 250), (W, 620)], fill=BROWN)
    # accent dots (felt-palette nod)
    for cx, col, r in [(140, YELLOW, 46), (W - 150, PINK, 54), (250, RED, 26), (W - 320, BLUE, 30)]:
        d.ellipse([(cx - r, 120 - r), (cx + r, 120 + r)], fill=col)
    # eyebrow
    eb = "数据挖掘与分析 · 课程案例"
    d.text(((W - tw(d, eb, f(26))[0]) // 2, 300), eb, fill=(255, 248, 240, 200), font=f(26))
    # title
    t1 = "蜜雪冰城 2025·3·15"
    t2 = "「隔夜柠檬片」事件舆情分析"
    d.text(((W - tw(d, t1, f(58, True))[0]) // 2, 350), t1, fill=CREAM, font=f(58, True))
    d.text(((W - tw(d, t2, f(58, True))[0]) // 2, 430), t2, fill=YELLOW, font=f(58, True))
    sub = "从数据挖掘角度，看一场舆论的「反转」"
    d.text(((W - tw(d, sub, f(28))[0]) // 2, 540), sub, fill=(255, 248, 240), font=f(28))
    # tag chips
    tags = [("词频 & 词云", PINK), ("LDA 主题模型", BLUE), ("机器学习情感分类", RED)]
    chip_f = f(24, True)
    widths = [tw(d, t, chip_f)[0] + 56 for t, _ in tags]
    total = sum(widths) + 24 * (len(tags) - 1)
    x = (W - total) // 2
    for (t, col), wch in zip(tags, widths):
        d.rounded_rectangle([(x, 680), (x + wch, 730)], radius=25, fill=col)
        d.text((x + 28, 690), t, fill="white", font=chip_f)
        x += wch + 24
    foot = "邹诗琪 · 24120416 · 上海大学新闻传播学院广告学"
    d.text(((W - tw(d, foot, f(20))[0]) // 2, 800), foot, fill=GREY, font=f(20))
    watermark(img).save(out, quality=92)
    print("cover ->", out)


def make_overview(out):
    img, d = base()
    d.rectangle([(0, 0), (W, 110)], fill=BROWN)
    d.text((60, 32), "项目概览", fill=CREAM, font=f(40, True))
    d.text((W - 60 - tw(d, "OVERVIEW", f(22))[0], 48), "OVERVIEW", fill=(255, 248, 240), font=f(22))

    blocks = [
        ("背景", PINK, "2025年3·15，蜜雪冰城宜昌门店「隔夜柠檬片」被曝光。与以往食品安全事件不同，消费者非但没有一边倒批评，反而大面积「力挺」品牌，形成罕见的舆情反转。"),
        ("数据", BLUE, "Python 爬取微博 1201 条原始舆情文本 → 去 @用户 / 话题 / URL / 表情并去重 → 1186 条有效数据 → jieba 分词 + 自定义词典 → TF-IDF 构建 1186 × 5000 特征矩阵。"),
        ("方法", YELLOW, "① 词频统计与词云  ② LDA 主题建模（困惑度选最优主题数 = 10）  ③ 逻辑回归 / 随机森林情感分类  ④ SnowNLP 情感打分交叉验证。"),
        ("核心发现", RED, "低价定位建立的「心理预期」+ 雪王 IP 长期积累的情感认同，共同构成危机中的「情感缓冲」，这正是舆论反转的深层原因。"),
    ]
    y = 150
    for title, col, body in blocks:
        d.rounded_rectangle([(60, y), (W - 60, y + 150)], radius=18, fill=(255, 255, 255))
        d.rectangle([(60, y), (72, y + 150)], fill=col)
        d.text((100, y + 22), title, fill=col, font=f(28, True))
        lines = wrap_cjk(d, body, f(23), W - 320)
        ly = y + 24
        for ln in lines[:4]:
            d.text((300, ly), ln, fill=(70, 55, 48), font=f(23))
            ly += 34
        y += 168
    # model stat strip
    d.rounded_rectangle([(60, y), (W - 60, y + 70)], radius=18, fill=BROWN)
    stat = "模型表现：逻辑回归 准确率 84% / AUC 0.9125    ｜    随机森林 AUC 0.9228    ｜    SnowNLP 正面 67.7% vs 负面 32.3%"
    d.text((100, y + 22), stat, fill=CREAM, font=f(24, True))
    watermark(img).save(out, quality=92)
    print("overview ->", out)


def make_chart_slide(src_png, title, takeaway, accent, out):
    img, d = base()
    # header
    d.rectangle([(0, 0), (W, 110)], fill=BROWN)
    d.text((60, 30), title, fill=CREAM, font=f(36, True))
    # accent tab
    d.rectangle([(0, 0), (14, 110)], fill=accent)
    # white card
    cx0, cy0, cx1, cy1 = 60, 150, W - 60, H - 130
    # soft shadow
    d.rounded_rectangle([(cx0 + 6, cy0 + 8), (cx1 + 6, cy1 + 8)], radius=22, fill=(225, 215, 205))
    d.rounded_rectangle([(cx0, cy0), (cx1, cy1)], radius=22, fill="white")
    # place chart (contain)
    chart = Image.open(src_png).convert("RGB")
    pad = 36
    bw, bh = (cx1 - cx0) - 2 * pad, (cy1 - cy0) - 2 * pad
    scale = min(bw / chart.width, bh / chart.height)
    nw, nh = int(chart.width * scale), int(chart.height * scale)
    chart = chart.resize((nw, nh), Image.LANCZOS)
    px = cx0 + (cx1 - cx0 - nw) // 2
    py = cy0 + (cy1 - cy0 - nh) // 2
    img.paste(chart, (px, py))
    # takeaway bar
    d.ellipse([(60, H - 96), (78, H - 78)], fill=accent)
    d.text((92, H - 100), takeaway, fill=(70, 55, 48), font=f(24))
    footer(d)
    watermark(img).save(out, quality=92)
    print("chart ->", out)


# ---- build ----
make_cover(os.path.join(DST, "01.jpg"))
make_overview(os.path.join(DST, "02.jpg"))

# (source png, title, takeaway, accent)
SLIDES = [
    ("02.png", "舆情词云", "讨论核心：蜜雪冰城 · 隔夜 · 柠檬 · 门店 · 食品安全", BLUE),
    ("01.png", "高频词 Top20", "「蜜雪冰城」1668 次居首，门店、隔夜、问题紧随其后", PINK),
    ("03.png", "LDA 困惑度曲线", "主题数 = 10 时困惑度最低（1709），确定为最优主题数", YELLOW),
    ("04.png", "LDA 前三主题关键词", "主题 2 为核心议题：315 · 消费者 · 隔夜 · 曝光 · 食品安全", BLUE),
    ("05.png", "各主题文档数量分布", "讨论高度聚焦：主题 8、10 文档量最大，紧扣事件本身", RED),
    ("06.png", "情感标注分布", "词典法标注：正面 388 vs 负面 369，舆论态度高度分化", PINK),
    ("07.png", "ROC 曲线 · 逻辑回归", "逻辑回归 AUC = 0.9125，整体准确率 84%", BLUE),
    ("08.png", "ROC 曲线对比 · 多模型", "随机森林 AUC = 0.9228，略优于逻辑回归", RED),
    ("09.png", "情感分类特征词 Top10", "正面靠「柠檬水·好喝·便宜」，负面集中于「隔夜·曝光·315」", YELLOW),
    ("10.png", "SnowNLP 情感分布", "SnowNLP：正面 67.7% vs 负面 32.3%，情绪明显偏向力挺", PINK),
]
for i, (src, title, take, col) in enumerate(SLIDES, start=3):
    make_chart_slide(os.path.join(CHARTS, src), title, take, col, os.path.join(DST, f"{i:02d}.jpg"))

print("\nDONE. total slides:", len(os.listdir(DST)))
