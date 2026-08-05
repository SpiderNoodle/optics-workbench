#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 4 款扁平动物角色图标（飞书/高德风格单色蓝底 + 白色角色 + 镜头眼）。"""
from PIL import Image, ImageDraw

S = 512
WHITE = "white"
DARK = "#1D1D1F"
CORAL = "#FF8A5B"


def rounded_bg(draw, color):
    draw.rounded_rectangle([0, 0, S, S], radius=112, fill=color)


def lens(draw, cx, cy, R, ring):
    """镜头眼：白眼球 + 彩色虹膜环 + 深色瞳孔 + 高光。"""
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], fill=WHITE)
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=ring, width=max(3, int(R * 0.16)))
    draw.ellipse([cx - R * 0.62, cy - R * 0.62, cx + R * 0.62, cy + R * 0.62], fill=ring)
    draw.ellipse([cx - R * 0.34, cy - R * 0.34, cx + R * 0.34, cy + R * 0.34], fill=DARK)
    g = max(4, int(R * 0.18))
    draw.ellipse([cx - R * 0.46, cy - R * 0.46, cx - R * 0.46 + g, cy - R * 0.46 + g], fill=WHITE)


def owl(draw, bg):
    rounded_bg(draw, bg)
    ring = "#9DC1FF"
    # 耳簇
    draw.polygon([(150, 175), (205, 95), (220, 185)], fill=WHITE)
    draw.polygon([(362, 175), (307, 95), (292, 185)], fill=WHITE)
    # 身体
    draw.ellipse([126, 165, 386, 452], fill=WHITE)
    # 翅膀点缀
    draw.ellipse([126, 250, 170, 420], fill=ring)
    draw.ellipse([342, 250, 386, 420], fill=ring)
    # 眼睛（镜头）
    lens(draw, 206, 258, 60, ring)
    lens(draw, 306, 258, 60, ring)
    # 喙
    draw.polygon([(256, 300), (236, 338), (276, 338)], fill=CORAL)
    # 脚
    draw.polygon([(210, 446), (198, 470), (224, 470)], fill=CORAL)
    draw.polygon([(302, 446), (290, 470), (316, 470)], fill=CORAL)


def cat(draw, bg):
    rounded_bg(draw, bg)
    ring = "#9AD0FF"
    # 耳朵
    draw.polygon([(150, 165), (120, 78), (232, 150)], fill=WHITE)
    draw.polygon([(362, 165), (392, 78), (280, 150)], fill=WHITE)
    draw.polygon([(168, 158), (150, 105), (208, 150)], fill=ring)
    draw.polygon([(344, 158), (362, 105), (304, 150)], fill=ring)
    # 头
    draw.ellipse([118, 150, 394, 420], fill=WHITE)
    # 眼睛
    lens(draw, 206, 250, 48, ring)
    lens(draw, 306, 250, 48, ring)
    # 鼻
    draw.polygon([(256, 296), (242, 282), (270, 282)], fill=CORAL)
    # 胡须
    for dx in (-1, 1):
        x0 = 256 + dx * 18
        for k, dy in enumerate((300, 312, 324)):
            draw.line([x0, dy, x0 + dx * 95, dy - 6 + k * 4], fill=ring, width=4)


def fox(draw, bg):
    rounded_bg(draw, bg)
    ring = "#9DC1FF"
    # 耳朵
    draw.polygon([(150, 220), (120, 105), (240, 185)], fill=WHITE)
    draw.polygon([(362, 220), (392, 105), (272, 185)], fill=WHITE)
    draw.polygon([(170, 205), (152, 130), (228, 185)], fill=ring)
    draw.polygon([(342, 205), (360, 130), (284, 185)], fill=ring)
    # 脸（上宽下尖）
    draw.polygon([(150, 215), (362, 215), (312, 320), (256, 470), (200, 320)], fill=WHITE)
    # 眼睛
    lens(draw, 214, 265, 40, ring)
    lens(draw, 298, 265, 40, ring)
    # 鼻
    draw.polygon([(256, 430), (242, 408), (270, 408)], fill=DARK)


def deer(draw, bg):
    rounded_bg(draw, bg)
    ring = "#9AD0FF"
    # 鹿角
    antler = WHITE
    lw = 11
    for s in (-1, 1):
        bx = 256 + s * 34
        draw.line([bx, 150, bx, 70], fill=antler, width=lw)              # 主枝
        draw.line([bx, 110, bx + s * 42, 78], fill=antler, width=lw)     # 上分叉
        draw.line([bx, 130, bx + s * 38, 110], fill=antler, width=lw)    # 下分叉
    # 耳朵
    draw.ellipse([110, 200, 168, 262], fill=WHITE)
    draw.ellipse([344, 200, 402, 262], fill=WHITE)
    # 头
    draw.ellipse([140, 170, 372, 402], fill=WHITE)
    # 眼睛
    lens(draw, 212, 270, 42, ring)
    lens(draw, 300, 270, 42, ring)
    # 鼻吻
    draw.ellipse([238, 350, 274, 384], fill=DARK)


def make(draw_fn, bg, name):
    img = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(img)
    draw_fn(d, bg)
    img.save(f"icons/cand_{name}.png")
    img.resize((192, 192), Image.LANCZOS).save(f"icons/cand_{name}_192.png")
    print("saved", name)


if __name__ == "__main__":
    make(owl, "#3370FF", "A")   # 飞书蓝 · 猫头鹰
    make(cat, "#1488F0", "B")   # 高德蓝 · 猫
    make(fox, "#245BDB", "C")   # 飞书深蓝 · 狐狸
    make(deer, "#1C86E8", "D")  # 高德蓝 · 鹿
