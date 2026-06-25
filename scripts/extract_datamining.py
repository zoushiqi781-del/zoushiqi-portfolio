"""
Extract ALL DataMining_Final content into watermarked gallery images.
- All PNG charts (9 total)
- Notebook report pages (rendered as styled images)
- CSV data preview
"""
import os, json, textwrap, math
from PIL import Image, ImageDraw, ImageFont

SRC = r"C:\Users\35512\DataMining_Final"
DST = r"D:\clawd\shiqi-portfolio\public\works\datamining"
WATERMARK = "邹诗琪 15270025359"

os.makedirs(DST, exist_ok=True)

# --- fonts ---
def get_font(size, bold=False):
    paths = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

def add_watermark(img):
    """Add tiled diagonal watermark."""
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
            if x + rotated.width <= layer.width and y + rotated.height <= layer.height and x >= 0 and y >= 0:
                layer.paste(rotated, (x, y), rotated)

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    result = Image.alpha_composite(img, layer)
    return result.convert("RGB")


def process_chart(png_path, out_name):
    """Watermark a chart PNG."""
    img = Image.open(png_path).convert("RGBA")
    # Ensure reasonable size
    if img.width < 800:
        ratio = 800 / img.width
        img = img.resize((800, int(img.height * ratio)), Image.LANCZOS)
    result = add_watermark(img)
    result.save(os.path.join(DST, out_name), quality=92)
    print(f"  Chart: {out_name}")


def render_notebook_cover(nb_title, nb_subtitle, sections, out_name):
    """Create a styled cover/summary page for a notebook."""
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), (255, 252, 245))
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (W, 120)], fill=(90, 50, 35))
    title_font = get_font(36, bold=True)
    sub_font = get_font(20)
    body_font = get_font(18)
    small_font = get_font(14)

    draw.text((40, 25), nb_title, fill=(255, 248, 240), font=title_font)
    draw.text((40, 80), nb_subtitle, fill=(255, 248, 240, 180), font=sub_font)

    # Sections
    y = 150
    for i, sec in enumerate(sections):
        # Section number circle
        cx, cy = 60, y + 12
        draw.ellipse([(cx-15, cy-15), (cx+15, cy+15)], fill=(224, 98, 137))
        draw.text((cx-5, cy-10), str(i+1), fill="white", font=body_font)

        # Section title
        draw.text((90, y), sec["title"], fill=(90, 50, 35), font=get_font(22, bold=True))
        y += 35

        # Section description
        if "desc" in sec:
            lines = textwrap.wrap(sec["desc"], width=55)
            for line in lines[:3]:
                draw.text((90, y), line, fill=(100, 80, 70), font=body_font)
                y += 26
        y += 20

    # Footer
    draw.text((40, H - 50), "邹诗琪 · 上海大学 · 数据挖掘期末作业", fill=(150, 130, 120), font=small_font)
    draw.text((W - 300, H - 50), "Python · Jupyter Notebook", fill=(150, 130, 120), font=small_font)

    result = add_watermark(img.convert("RGBA"))
    result.save(os.path.join(DST, out_name), quality=92)
    print(f"  Report cover: {out_name}")


def render_code_page(title, code_text, out_name):
    """Render a styled code preview page."""
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), (40, 42, 54))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([(0, 0), (W, 50)], fill=(30, 32, 44))
    title_font = get_font(16)
    code_font = get_font(14)

    # Window dots
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([(15 + i*25, 15), (15 + i*25 + 16, 31)], fill=color)

    draw.text((100, 15), title, fill=(200, 200, 200), font=title_font)

    # Code content
    y = 65
    lines = code_text.split("\n")
    colors = {
        "import": (255, 121, 198),
        "def ": (80, 250, 123),
        "class ": (80, 250, 123),
        "from": (255, 121, 198),
        "#": (98, 114, 164),
        "print": (139, 233, 253),
        "return": (255, 121, 198),
        "if ": (255, 121, 198),
        "for ": (255, 121, 198),
    }

    for i, line in enumerate(lines[:40]):
        # Line number
        draw.text((15, y), f"{i+1:3d}", fill=(100, 100, 120), font=code_font)

        # Determine color
        color = (248, 248, 242)
        stripped = line.lstrip()
        for keyword, kcolor in colors.items():
            if stripped.startswith(keyword):
                color = kcolor
                break

        draw.text((55, y), line[:90], fill=color, font=code_font)
        y += 18
        if y > H - 30:
            break

    result = add_watermark(img.convert("RGBA"))
    result.save(os.path.join(DST, out_name), quality=92)
    print(f"  Code page: {out_name}")


def render_data_preview(csv_path, out_name):
    """Render a styled data table preview."""
    import csv as csv_mod

    W, H = 1200, 800
    img = Image.new("RGB", (W, H), (255, 252, 245))
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([(0, 0), (W, 80)], fill=(60, 140, 202))
    title_font = get_font(28, bold=True)
    header_font = get_font(16, bold=True)
    cell_font = get_font(13)

    draw.text((30, 20), "微博舆情数据集预览", fill="white", font=title_font)

    # Read CSV
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv_mod.reader(f)
        headers = next(reader)
        rows = []
        for row in reader:
            rows.append(row)
            if len(rows) >= 15:
                break

    # Stats
    total_lines = sum(1 for _ in open(csv_path, "r", encoding="utf-8-sig")) - 1
    draw.text((30, 55), f"共 {total_lines} 条数据 · {len(headers)} 个字段", fill=(200, 230, 255), font=cell_font)

    # Table
    y_start = 100
    col_widths = [60, 350, 100, 80, 80, 80, 140]
    if len(headers) < len(col_widths):
        col_widths = col_widths[:len(headers)]

    # Header row
    x = 20
    draw.rectangle([(15, y_start), (W - 15, y_start + 35)], fill=(240, 235, 225))
    for i, h in enumerate(headers[:len(col_widths)]):
        draw.text((x, y_start + 8), h[:12], fill=(90, 50, 35), font=header_font)
        x += col_widths[i]

    # Data rows
    y = y_start + 40
    for row_idx, row in enumerate(rows):
        bg = (255, 252, 245) if row_idx % 2 == 0 else (245, 240, 232)
        draw.rectangle([(15, y), (W - 15, y + 38)], fill=bg)

        x = 20
        for i, cell in enumerate(row[:len(col_widths)]):
            text = str(cell)[:30]
            if i == 1:  # text column - show more
                text = str(cell)[:40]
            draw.text((x, y + 10), text, fill=(60, 50, 45), font=cell_font)
            x += col_widths[i]
        y += 38
        if y > H - 60:
            break

    # Footer
    draw.text((30, H - 40), f"数据来源：微博 · 蜜雪冰城3·15舆情", fill=(150, 130, 120), font=cell_font)

    result = add_watermark(img.convert("RGBA"))
    result.save(os.path.join(DST, out_name), quality=92)
    print(f"  Data preview: {out_name}")


# ====== MAIN ======
print("=== Extracting DataMining content ===\n")

# 1. All chart PNGs
chart_files = [
    ("wordcloud.png", "01.jpg"),
    ("word_frequency_top20.png", "02.jpg"),
    ("lda_perplexity_curve.png", "03.jpg"),
    ("lda_topics_top3.png", "04.jpg"),
    ("lda_topic_distribution.png", "05.jpg"),
    ("snownlp_sentiment.png", "06.jpg"),
    ("sentiment_keywords.png", "07.jpg"),
    ("roc_curve.png", "08.jpg"),
    ("roc_curve_comparison.png", "09.jpg"),
]

print("[1/5] Processing chart images...")
for src_name, dst_name in chart_files:
    src_path = os.path.join(SRC, src_name)
    if os.path.exists(src_path):
        process_chart(src_path, dst_name)
    else:
        print(f"  SKIP (not found): {src_name}")

# 2. Notebook report covers
print("\n[2/5] Creating notebook report pages...")

render_notebook_cover(
    "第一部分：数据预处理与词云",
    '蜜雪冰城3·15“隔夜柠檬片”事件舆情分析',
    [
        {"title": "数据读取", "desc": "导入1201条微博原始数据，包含文本、用户、转发评论等字段"},
        {"title": "数据清洗", "desc": "去除@用户、#话题#、URL、表情等干扰，过滤短文本和重复，保留1186条"},
        {"title": "jieba中文分词", "desc": "自定义词典+停用词过滤，提取有效关键词"},
        {"title": "TF-IDF向量化", "desc": "构建5000维特征矩阵，为后续主题模型和机器学习做准备"},
        {"title": "词频统计与词云", "desc": "Top30高频词：蜜雪冰城(1668)、门店(574)、隔夜(570)、消费者(527)"},
    ],
    "10.jpg"
)

render_notebook_cover(
    "第二部分：LDA主题模型分析",
    '蜜雪冰城3·15"隔夜柠檬片"事件舆情分析',
    [
        {"title": "困惑度选择最优主题数", "desc": "通过困惑度曲线确定LDA最优主题数K"},
        {"title": "LDA主题建模", "desc": "使用Latent Dirichlet Allocation提取文本潜在主题"},
        {"title": "主题词分布可视化", "desc": "展示每个主题的Top关键词及其权重"},
        {"title": "文档主题分布", "desc": "分析每条微博的主题归属和分布特征"},
    ],
    "11.jpg"
)

render_notebook_cover(
    "第三部分：情感分析",
    '蜜雪冰城3·15"隔夜柠檬片"事件舆情分析',
    [
        {"title": "SnowNLP情感分析", "desc": "基于SnowNLP对每条微博进行情感极性打分（0~1）"},
        {"title": "情感分布统计", "desc": "分析正面、中性、负面情感的比例分布"},
        {"title": "情感关键词提取", "desc": "提取不同情感类别中的特征关键词"},
    ],
    "12.jpg"
)

render_notebook_cover(
    "第四部分：深度学习情感分析",
    '蜜雪冰城3·15"隔夜柠檬片"事件舆情分析',
    [
        {"title": "BERT预训练模型", "desc": "使用BERT中文预训练模型进行文本编码和情感分类"},
        {"title": "模型训练与评估", "desc": "训练集/测试集划分，交叉验证评估模型性能"},
        {"title": "ROC曲线对比", "desc": "对比不同模型的AUC分数和分类效果"},
        {"title": "结果分析", "desc": "深度学习方法vs传统方法的情感分析效果对比"},
    ],
    "13.jpg"
)

# 3. Source code pages
print("\n[3/5] Creating source code pages...")

scrape_code = open(os.path.join(SRC, "scrape_weibo.py"), "r", encoding="utf-8").read()
render_code_page("scrape_weibo.py — 微博数据爬取脚本", scrape_code, "14.jpg")

preprocess_code = open(os.path.join(SRC, "data_preprocess.py"), "r", encoding="utf-8").read()
render_code_page("data_preprocess.py — 数据预处理脚本", preprocess_code, "15.jpg")

# 4. Data preview
print("\n[4/5] Creating data preview...")
csv_path = os.path.join(SRC, "weibo_cleaned_data.csv")
if os.path.exists(csv_path):
    render_data_preview(csv_path, "16.jpg")

# 5. Summary
print("\n[5/5] Done!")
out_files = sorted([f for f in os.listdir(DST) if f.endswith(".jpg")])
print(f"\nTotal files in {DST}: {len(out_files)}")
for f in out_files:
    size = os.path.getsize(os.path.join(DST, f))
    print(f"  {f} ({size // 1024}KB)")
