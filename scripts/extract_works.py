"""Extract key pages from work PDFs, add watermark, save to public/works/"""
import fitz  # PyMuPDF
import os
from PIL import Image, ImageDraw, ImageFont
import math

OUT_DIR = r"D:\clawd\shiqi-portfolio\public\works"
WATERMARK_TEXT = "邹诗琪 24120416"
DPI = 150  # good balance of quality vs file size

def add_watermark(img: Image.Image) -> Image.Image:
    """Add tiled diagonal semi-transparent watermark."""
    txt_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    # try to use a font, fallback to default
    font_size = max(28, img.width // 30)
    try:
        font = ImageFont.truetype("msyh.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", font_size)
        except:
            font = ImageFont.load_default()

    # measure text
    bbox = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # tile watermark diagonally
    step_x = int(tw * 2.5)
    step_y = int(th * 5)

    temp = Image.new("RGBA", (img.width * 2, img.height * 2), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp)

    for y in range(-img.height, img.height * 2, step_y):
        for x in range(-img.width, img.width * 2, step_x):
            temp_draw.text((x, y), WATERMARK_TEXT, font=font, fill=(120, 120, 120, 35))

    # rotate
    rotated = temp.rotate(30, expand=False, center=(img.width, img.height))
    # crop back to original size
    cx, cy = rotated.width // 2, rotated.height // 2
    half_w, half_h = img.width // 2, img.height // 2
    cropped = rotated.crop((cx - half_w, cy - half_h, cx + half_w, cy + half_h))

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    # ensure same size
    if cropped.size != img.size:
        cropped = cropped.resize(img.size)
    result = Image.alpha_composite(img, cropped)
    return result.convert("RGB")


def extract_pdf_pages(pdf_path: str, slug: str, pages: list[int], dpi: int = DPI):
    """Extract specific pages from PDF, watermark, save as JPG."""
    out_folder = os.path.join(OUT_DIR, slug)
    os.makedirs(out_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    total = doc.page_count
    print(f"  {slug}: {total} pages total, extracting {len(pages)} pages")

    saved = []
    for i, page_num in enumerate(pages):
        if page_num >= total:
            print(f"    skip page {page_num} (only {total} pages)")
            continue

        page = doc[page_num]
        # render at DPI
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # add watermark
        img = add_watermark(img)

        # save
        out_path = os.path.join(out_folder, f"{i+1:02d}.jpg")
        img.save(out_path, "JPEG", quality=82)
        saved.append(out_path)
        print(f"    saved page {page_num} -> {out_path}")

    doc.close()
    return saved


def copy_datamining_images(src_dir: str, slug: str):
    """Copy and watermark data mining visualization PNGs."""
    out_folder = os.path.join(OUT_DIR, slug)
    os.makedirs(out_folder, exist_ok=True)

    target_files = [
        "wordcloud.png",
        "word_frequency_top20.png",
        "lda_topics_top3.png",
        "lda_topic_distribution.png",
        "snownlp_sentiment.png",
        "sentiment_keywords.png",
        "roc_curve_comparison.png",
    ]

    saved = []
    for i, fname in enumerate(target_files):
        src = os.path.join(src_dir, fname)
        if not os.path.exists(src):
            print(f"    skip {fname} (not found)")
            continue

        img = Image.open(src).convert("RGB")
        img = add_watermark(img)
        out_path = os.path.join(out_folder, f"{i+1:02d}.jpg")
        img.save(out_path, "JPEG", quality=85)
        saved.append(out_path)
        print(f"    saved {fname} -> {out_path}")

    return saved


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. 秘境环江·毛南狂欢季 (全国一等奖)
    print("Extracting: huanjiang")
    extract_pdf_pages(
        r"C:\Users\35512\xwechat_files\wxid_4fdwxm53nyod22_588c\msg\file\2026-06\秘境环江 毛南嘉年华PPT.pdf",
        "huanjiang",
        [0, 1, 2, 3, 4, 5, 8, 12, 16, 20],  # key pages
    )

    # 2. 三福策划案
    print("Extracting: sanfu")
    extract_pdf_pages(
        r"C:\Users\35512\xwechat_files\wxid_4fdwxm53nyod22_588c\msg\file\2026-06\4组-邹诗琪-生活不单打，三福帮你搭.pdf",
        "sanfu",
        [0, 1, 2, 3, 4, 5, 8, 12, 16, 20],  # key pages
    )

    # 3. 蜜雪冰城数据挖掘
    print("Extracting: datamining")
    copy_datamining_images(
        r"C:\Users\35512\DataMining_Final",
        "datamining",
    )

    print("\nDone!")
