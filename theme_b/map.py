# -*- coding: utf-8 -*-
"""v0.1.6 深空玻璃(B) —— 颜色语义重映射表"""

# 中性色：浅色主题 → 深空玻璃（必须反相，否则深底上看不清）
NEUTRAL = {
    '#1a2233': '#e9efff',   # 主文字 ink
    '#475569': '#aabdd9',   # 次级文字 slate
    '#5b6678': '#9db0d2',   # 弱化文字 muted
    '#9aa6b5': '#8093b6',   # 更弱文字
    '#64748b': '#94a6c7',   # 辅助文字
    '#0f172a': '#eef3ff',   # 深墨 → 亮
    '#1a3a66': '#a8c5f0',   # 深蓝字 → 亮蓝
    '#94a3b8': '#61759d',   # 箭头/连线灰
    '#cbd5e1': '#43537b',   # 浅边框
    '#d4dce6': '#354265',   # 浅边框2
    '#e2e8f0': '#2b3654',   # 边框
    '#d8dee8': '#33405f',   # 边框
    '#e6ebf1': '#2c3856',   # 边框
    '#dbe2ec': '#2e3a59',   # 边框
    '#d3e2ff': '#2b3f6d',   # 蓝边框
    '#d6e6ff': '#2d4272',   # 蓝边框
    '#eef2f7': '#1a2340',   # 极浅底
    '#f1f5f9': '#1c2542',   # 极浅底
    '#fafbfc': '#121b31',   # 纸底
    '#fbfcfe': '#111a30',   # 画布纸底
    '#f8fafc': '#141d34',   # hover 底
    '#fbfdff': '#131c33',   # 卡片底
    '#f6f9fd': '#151e37',   # 斑马纹
    '#f4f7fb': '#0a0f1e',   # 页面底
    '#e6ecf7': '#26314f',   # 进度条槽
    '#ffffff': '#141d33',   # SVG 卡片底（注意：#fff 三位写法是白字，保留）
}

# 浅色语义底 → 深色半透明色调
TINT = {
    '#fff7ed': '#2a1e0c',   # amber 提示底
    '#fef3c7': '#2c2410',   # amber 底
    '#fff3c4': '#2c2410',
    '#fff7e0': '#2b2310',
    '#eef4ff': '#152346',   # blue 释义底
    '#eef3fb': '#182548',   # blue 底
    '#f0f6ff': '#152banned', # placeholder(会被覆盖)
    '#f0f9ff': '#0d2133',   # sky 底
    '#dbeafe': '#17274c',   # blue 底
    '#bfdbfe': '#1d3260',   # blue 底
    '#e8f5ee': '#0f2419',   # green 底
    '#fed7aa': '#4a3313',   # amber 边框
}
TINT['#f0f6ff'] = '#152banned'
TINT['#f0f6ff'] = '#16244a'   # readout 蓝底

# 语义强调色：保持色相，提亮以适配深底（WCAG AA on #0a0f1e）
SEMANTIC = {
    '#f59e0b': '#fbbf24',   # amber
    '#b45309': '#fcd34d',   # 深 amber 文字
    '#a16207': '#fcd34d',
    '#16a34a': '#34d399',   # green
    '#22c55e': '#4ade80',
    '#0ea5e9': '#38bdf8',   # sky
    '#0c4a6e': '#7dd3fc',   # 深 sky 文字
    '#dc2626': '#f87171',   # red
    '#991b1b': '#fca5a5',
    '#7f1d1d': '#fca5a5',
    '#9a3412': '#fdba74',
    '#7c2d12': '#fdba74',
    '#1d4ed8': '#7aa2ff',   # blue
    '#2563eb': '#5b8cff',
    '#3370ff': '#5b8cff',
    '#2b5fe0': '#7c6cff',
    '#60a5fa': '#7fb2ff',
    '#93c5fd': '#a8c8ff',
    '#fb923c': '#fdba74',
    '#fbbf24': '#fcd34d',
}

# 合并（顺序：先长后短，避免 #fff 误伤 #ffffff）
HTML_MAP = {}
HTML_MAP.update(NEUTRAL)
HTML_MAP.update(TINT)
HTML_MAP.update(SEMANTIC)

# ===== Canvas(JS) 专用 =====
# 场景语义色（天空/草地/路面/车体）保持不变，只改「图表外壳」
CANVAS_KEEP = {
    '#bfe0ff',  # 天空
    '#9fd49a',  # 草地
    '#eaf1f8',  # 道路场景底（本身是浅色场景，保留）
    '#0e1726', '#0b1020', '#0e1a2b',  # 已是深色
}

CANVAS_MAP = {
    '#fbfcfe': '#0f1729',   # 图表纸底 → 深
    '#fff':    '#0f1729',   # 仅在 fillRect 全屏时替换（脚本内特判）
    '#eef2f7': 'rgba(255,255,255,0.07)',
    '#e2e8f0': 'rgba(255,255,255,0.10)',
    '#cbd5e1': 'rgba(255,255,255,0.16)',
    '#b9c6d4': 'rgba(255,255,255,0.20)',
    '#9aa6b5': '#8093b6',
    '#94a3b8': '#7286aa',
    '#475569': '#aabdd9',
    '#1a2233': '#e9efff',
    '#5b6678': '#9db0d2',
    '#fff3c4': '#2c2410',
    '#fff7e0': '#2b2310',
}
CANVAS_MAP.update(SEMANTIC)

# rgba 形式的重映射（canvas 内）
CANVAS_RGBA = {
    'rgba(37,99,235,':   'rgba(91,140,255,',    # 蓝
    'rgba(26,34,51,':    'rgba(233,239,255,',   # 深墨 → 亮
    'rgba(220,225,235,': 'rgba(255,255,255,',
    'rgba(34,197,94,':   'rgba(52,211,153,',    # 绿
    'rgba(22,163,74,':   'rgba(52,211,153,',
    'rgba(220,38,38,':   'rgba(248,113,113,',   # 红
    'rgba(245,158,11,':  'rgba(251,191,36,',    # 琥珀
    'rgba(14,165,233,':  'rgba(56,189,248,',    # 天蓝
}
