#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重绘更简约自然的猫头鹰图标：去翅膀/脚，缩小镜头眼，浅色肚皮做层次。"""
from PIL import Image, ImageDraw

S = 512
WHITE = "white"
DARK = "#1D1D1F"
BG = "#3370FF"
RING = "#BBD3FF"          # 镜头虹膜环（浅蓝）
BELLY = "#EAF1FF"         # 浅色肚皮
BEAK = "#FF8A5B"          # 小喙（克制的暖色点缀）


def lens(draw, cx, cy, R):
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], fill=WHITE)
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=RING, width=max(3, int(R * 0.14)))
    draw.ellipse([cx - R * 0.66, cy - R * 0.66, cx + R * 0.66, cy + R * 0.66], fill=RING)
    draw.ellipse([cx - R * 0.36, cy - R * 0.36, cx + R * 0.36, cy + R * 0.36], fill=DARK)
    g = max(4, int(R * 0.2))
    draw.ellipse([cx - R * 0.48, cy - R * 0.48, cx - R * 0.48 + g, cy - R * 0.48 + g], fill=WHITE)


def owl(draw):
    # 圆角方形底
    draw.rounded_rectangle([0, 0, S, S], radius=110, fill=BG)

    # 身体 + 头 合并成自然轮廓（先大椭圆身体，再头圆叠加）
    draw.ellipse([138, 210, 374, 462], fill=WHITE)   # 身体（下宽）
    draw.ellipse([146, 92, 366, 312], fill=WHITE)    # 头

    # 耳簇（小、柔，贴头顶两侧）
    draw.polygon([(196, 120), (172, 58), (236, 104)], fill=WHITE)
    draw.polygon([(316, 120), (340, 58), (276, 104)], fill=WHITE)

    # 浅色肚皮（层次，扁平双色）
    draw.ellipse([182, 300, 330, 452], fill=BELLY)

    # 眼睛（镜头眼，缩小、间距自然）
    lens(draw, 214, 232, 44)
    lens(draw, 298, 232, 44)

    # 小喙（克制的暖色）
    draw.polygon([(256, 262), (247, 250), (265, 250)], fill=BEAK)


if __name__ == "__main__":
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)
    owl(d)
    img.save("icons/cand_A.png")
    img.resize((192, 192), Image.LANCZOS).save("icons/cand_A_192.png")
    print("owl v2 saved")
