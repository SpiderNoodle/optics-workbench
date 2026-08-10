# -*- coding: utf-8 -*-
"""
v0.1.6 · 深空玻璃(B) 重构
  1) 删除启动页（#launch / .tile / .home-fab / launch CSS+JS）
  2) 三个 <style> 块 → 统一 B 主题（base.css + shell.css）
  3) HTML 区内联色（SVG fill/stroke + style 属性）语义化重映射
  4) JS 区 canvas 硬编码色重映射（保留场景语义色）
  5) 版本号 → v0.1.6
"""
import io, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
SRC = os.path.join(ROOT, 'index.html')
sys.path.insert(0, D)
from map import HTML_MAP, CANVAS_MAP, CANVAS_RGBA, CANVAS_KEEP  # noqa

src = io.open(SRC, encoding='utf-8').read()
orig_len = len(src)
log = []


def must(cond, msg):
    if not cond:
        raise SystemExit('!! FAIL: ' + msg)
    log.append('   ok  ' + msg)


# ══════════════ 1. 定位三个 style 块 ══════════════
sty = [(m.start(), m.end()) for m in re.finditer(r'<style>.*?</style>', src, re.S)]
must(len(sty) == 3, '找到 3 个 <style> 块')

base_css = io.open(os.path.join(D, 'base.css'), encoding='utf-8').read()
shell_css = io.open(os.path.join(D, 'shell.css'), encoding='utf-8').read()

# 从后往前替换，避免位移
s3, e3 = sty[2]
src = src[:s3] + '<style>\n' + shell_css + '</style>' + src[e3:]
s2, e2 = sty[1]
src = src[:s2] + '<!-- 启动页样式已移除 v0.1.6 -->' + src[e2:]   # 整块删除（含 launch/tile/home-fab）
s1, e1 = sty[0]
src = src[:s1] + '<style>\n' + base_css + '</style>' + src[e1:]
log.append('1) style 块：base 重写 / launch 块删除 / shell 重写')


# ══════════════ 2. 删除启动页 HTML ══════════════
m = re.search(r'<!-- ===== PWA 工作台：启动台.*?\n</div>\n', src, re.S)
must(m is not None, '定位启动页 HTML')
src = src[:m.start()] + src[m.end():]

# 删除 home-fab 按钮
m = re.search(r'<!-- 回启动台按钮 -->\s*<button class="home-fab".*?</button>\s*', src, re.S)
must(m is not None, '定位 home-fab 按钮')
src = src[:m.start()] + src[m.end():]
log.append('2) 启动页 HTML + 主页 FAB 已删除')


# ══════════════ 3. 删除启动页 JS ══════════════
old_js = re.search(
    r"\s*// 启动台交互\s*\n.*?document\.getElementById\('homeFab'\)\.classList\.add\('show'\);\s*\n",
    src, re.S)
must(old_js is not None, '定位启动页 JS')
src = src[:old_js.start()] + '\n' + src[old_js.end():]
log.append('3) 启动页 JS 已删除（tile/openLaunch/closeLaunch/homeFab）')


# ══════════════ 4. HTML 区颜色重映射 ══════════════
head_end = src.index('</head>')
body_start = src.index('<body>')
js_start = src.index('<script>', body_start)

html_zone = src[body_start:js_start]
before = html_zone

# 长键优先，避免 #ffffff 被 #fff 截断
for old in sorted(HTML_MAP, key=len, reverse=True):
    new = HTML_MAP[old]
    html_zone = re.sub(re.escape(old) + r'(?![0-9a-fA-F])', new, html_zone, flags=re.I)

changed_html = sum(1 for a, b in zip(before, html_zone) if a != b)
src = src[:body_start] + html_zone + src[js_start:]
log.append('4) HTML 区颜色重映射：%d 种规则已应用' % len(HTML_MAP))


# ══════════════ 5. JS 区 canvas 颜色重映射 ══════════════
js_start = src.index('<script>', src.index('<body>'))
js_zone = src[js_start:]

# 5a. 全屏纸底 fillRect：'#fbfcfe' / '#fff' → 深底
js_zone = js_zone.replace("x.fillStyle='#fbfcfe'; x.fillRect(0,0,w,h);",
                          "x.fillStyle='#0f1729'; x.fillRect(0,0,w,h);")
js_zone = js_zone.replace("x.fillStyle = '#eaf1f8'; x.fillRect(0,0,w,h);",
                          "x.fillStyle = '#16203a'; x.fillRect(0,0,w,h);")

# 5b. 逐色替换（跳过场景语义色）
for old in sorted(CANVAS_MAP, key=len, reverse=True):
    if old in CANVAS_KEEP:
        continue
    if old == '#fff':
        continue      # 白字保留，已在 5a 单独处理背景
    new = CANVAS_MAP[old]
    js_zone = re.sub(r"(['\"])" + re.escape(old) + r"(['\"])",
                     lambda mm, n=new: mm.group(1) + n + mm.group(2), js_zone, flags=re.I)

# 5c. rgba 前缀重映射
for old, new in CANVAS_RGBA.items():
    js_zone = js_zone.replace(old, new)

src = src[:js_start] + js_zone
log.append('5) JS/canvas 颜色重映射完成（场景语义色已保留）')


# ══════════════ 6. 版本号 ══════════════
src = src.replace('v0.1.5 · 2026-08-10', 'v0.1.6 · 2026-08-10')
src = src.replace('>v0.1.5<', '>v0.1.6<')
log.append('6) 版本号 → v0.1.6')


# ══════════════ 7. 校验 ══════════════
must('id="launch"' not in src, '启动页元素已彻底移除')
must('home-fab' not in src, 'home-fab 已彻底移除')
must("getElementById('homeFab')" not in src, 'homeFab JS 引用已清除')
must('id="bg"' in src, '粒子画布保留')
must('id="view-home"' in src and 'id="view-random"' in src and 'id="view-dash"' in src, '三页结构完整')
must('id="bottomtab"' in src and 'id="sidebar"' in src, '双导航完整')
must(src.count('<style>') == 2, 'style 块合并为 2 个')
must('#1a2233' not in src, '浅色主文字 #1a2233 已清零')
must('#475569' not in src, '浅色次级文字 #475569 已清零')

io.open(SRC, 'w', encoding='utf-8').write(src)

print('\n'.join(log))
print('\n体积：%d → %d bytes (%+d)' % (orig_len, len(src), len(src) - orig_len))
