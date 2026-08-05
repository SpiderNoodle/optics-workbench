#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""猫头鹰 v3：在 v2 基础上精修——更顺的轮廓、面部圆盘、锐利眼神、柔和耳簇、高光。"""
from PIL import Image, ImageDraw

S = 512
WHITE = "white"
DARK = "#1D1D1F"
BG = "#3370FF"
RING = "#C9DdFF"        # 镜头虹膜环（更浅，更柔和）
BELLY = "#EAF1FF"       # 浅色肚皮 / 面部圆盘
BEAK = "#FF8A5B"        # 小喙
SHEEN = "#F2F7FF"       # 头顶高光


def lens(draw, cx, cy, R):
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], fill=WHITE)
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=RING, width=max(2, int(R * 0.10)))
    draw.ellipse([cx - R * 0.70, cy - R * 0.70, cx + R * 0.70, cy + R * 0.70], fill=RING)
    draw.ellipse([cx - R * 0.46, cy - R * 0.46, cx + R * 0.46, cy + R * 0.46], fill=DARK)
    # 高光：让瞳孔像玻璃镜头
    g = max(4, int(R * 0.22))
    draw.ellipse([cx - R * 0.52, cy - R * 0.52, cx - R * 0.52 + g, cy - R * 0.52 + g], fill=WHITE)


def owl(draw):
    draw.rounded_rectangle([0, 0, S, S], radius=110, fill=BG)

    # 身体 + 头 合并成自然轮廓
    draw.ellipse([140, 238, 372, 462], fill=WHITE)   # 身体（下宽）
    draw.ellipse([146, 86, 366, 306], fill=WHITE)    # 头

    # 耳簇（小、柔、贴头顶两侧）
    draw.polygon([(200, 112), (178, 56), (238, 100)], fill=WHITE)
    draw.polygon([(312, 112), (334, 56), (274, 100)], fill=WHITE)

    # 面部圆盘（两个浅色圆，构成经典猫头鹰脸）
    draw.ellipse([168, 178, 268, 300], fill=BELLY)
    draw.ellipse([244, 178, 344, 300], fill=BELLY)

    # 头顶高光（柔和）
    draw.ellipse([176, 110, 240, 162], fill=SHEEN)

    # 眼睛（镜头眼，锐利：大瞳孔 + 细环）
    lens(draw, 214, 234, 42)
    lens(draw, 298, 234, 42)

    # 小喙
    draw.polygon([(256, 262), (247, 250), (265, 250)], fill=BEAK)


if __name__ == "__main__":
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)
    owl(d)
    img.save("icons/cand_A.png")
    img.resize((192, 192), Image.LANCZOS).save("icons/cand_A_192.png")
    print("owl v3 saved")
