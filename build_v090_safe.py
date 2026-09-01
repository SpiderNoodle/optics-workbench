# -*- coding: utf-8 -*-
"""
v0.9.0 构建脚本（安全版）：四项修改
1. Kindle 主题释义文字降亮（仅 CSS）
2. 新增 Office/WPS 主题（仅 CSS + 主题选择器 HTML）
3. 单位速查模块改为可滑动表格形式（CSS + 安全 JS，try-catch 包裹）
4. 随机模块换条添加简洁淡入淡出动画（CSS + 安全 JS，不包装原有函数）
版本：0.8.7 -> 0.9.0
"""
import io, re

SRC = "index.html"
html = io.open(SRC, encoding="utf-8").read()
original_len = len(html)
report = []

def log(msg):
    print(msg)
    report.append(msg)

# ============================================================
# 修改 1：Kindle 主题释义文字降亮（仅 CSS，安全）
# ============================================================
log("\n=== 修改 1：Kindle 主题释义文字降亮 ===")

kindle_css = '''
  /* v0.9.0: Kindle 主题释义文字降亮 */
  [data-theme="kindle"] .define,
  [data-theme="kindle"] .define p,
  [data-theme="kindle"] .panel-desc,
  [data-theme="kindle"] .spec-text,
  [data-theme="kindle"] .knowledge-desc {
    color: #3a3a3a !important;
  }
  [data-theme="kindle"] .define b,
  [data-theme="kindle"] .define strong {
    color: #1a1a1a !important;
  }
'''

style_end = html.rfind('</style>')
if style_end > 0:
    html = html[:style_end] + kindle_css + html[style_end:]
    log("[OK] Kindle 主题释义降亮 CSS 已插入")
else:
    log("[SKIP] 未找到 </style>")

# ============================================================
# 修改 2：新增 Office/WPS 主题（CSS + 主题选择器 HTML）
# ============================================================
log("\n=== 修改 2：新增 Office/WPS 主题 ===")

office_css = '''
  /* v0.9.0: Office/WPS 主题（仿 Excel 办公风格）*/
  [data-theme="office"] {
    --bg-1: #f3f3f3;
    --bg-2: #e8e8e8;
    --surface: #ffffff;
    --surface-2: #fafafa;
    --text: #1f1f1f;
    --text-2: #404040;
    --muted: #606060;
    --muted-2: #808080;
    --brand: #217346;
    --brand-2: #2e9b5e;
    --brand-light: #e6f2ec;
    --line: #d4d4d4;
    --line-light: #e8e8e8;
    --acc-line: #217346;
    --r-l: 4px;
    --r-m: 3px;
    --r-s: 2px;
    --sh: 0 1px 3px rgba(0,0,0,.08);
    --sh-lg: 0 4px 12px rgba(0,0,0,.1);
    --canvas-bg: #ffffff;
    --glass-blur: blur(0px);
    --hero-grad: linear-gradient(135deg,#217346,#2e9b5e);
    --tab-active-bg: #e6f2ec;
    --tab-active-border: #217346;
    --table-header-bg: #217346;
    --table-header-text: #ffffff;
    --table-row-alt: #f8f8f8;
    --table-border: #d4d4d4;
  }
  [data-theme="office"] body {
    font-family: "Calibri", "Segoe UI", system-ui, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #f3f3f3;
  }
  [data-theme="office"] .panel,
  [data-theme="office"] .card,
  [data-theme="office"] .glass {
    background: #ffffff;
    border: 1px solid #d4d4d4;
    border-radius: 4px;
    box-shadow: none;
    backdrop-filter: none;
  }
  [data-theme="office"] .tab {
    border-radius: 3px 3px 0 0;
    border: 1px solid transparent;
    border-bottom: none;
  }
  [data-theme="office"] .tab.active {
    background: #ffffff;
    border-color: #d4d4d4;
    border-bottom: 2px solid #217346;
    color: #217346;
    font-weight: 600;
  }
  [data-theme="office"] .hero {
    background: linear-gradient(135deg,#217346,#2e9b5e);
    border-radius: 0;
  }
  [data-theme="office"] .btn-primary {
    background: #217346;
    border-radius: 3px;
  }
  [data-theme="office"] .btn-primary:hover {
    background: #1a5c38;
  }
  [data-theme="office"] ::-webkit-scrollbar {
    width: 16px;
    height: 16px;
  }
  [data-theme="office"] ::-webkit-scrollbar-track {
    background: #f0f0f0;
  }
  [data-theme="office"] ::-webkit-scrollbar-thumb {
    background: #c0c0c0;
    border: 3px solid #f0f0f0;
    border-radius: 0;
  }
  [data-theme="office"] ::-webkit-scrollbar-thumb:hover {
    background: #a0a0a0;
  }
'''

style_end = html.rfind('</style>')
if style_end > 0:
    html = html[:style_end] + office_css + html[style_end:]
    log("[OK] Office 主题 CSS 已插入")

# 主题选择器添加 Office 选项
theme_chip_pattern = re.compile(
    r'(class="theme-chip[^"]*"[^>]*data-theme=")([^"]+)(")',
    re.IGNORECASE
)
matches = list(theme_chip_pattern.finditer(html))
if matches:
    log(f"  找到 {len(matches)} 个主题选项")
    last_match = matches[-1]
    office_chip = '''
        <div class="theme-chip" data-theme="office" onclick="setTheme('office')">
          <div class="theme-swatch" style="background:linear-gradient(135deg,#217346,#e6f2ec);border:1px solid #d4d4d4;"></div>
          <div class="theme-info">
            <div class="theme-name">Office / WPS</div>
            <div class="theme-desc">Excel 办公风格</div>
          </div>
        </div>'''
    html = html[:last_match.end()] + office_chip + html[last_match.end():]
    log("[OK] Office 主题选项已添加到主题选择器")
else:
    log("[SKIP] 未找到主题选择器结构")

# ============================================================
# 修改 3：单位速查模块表格化（CSS + 安全 JS）
# ============================================================
log("\n=== 修改 3：单位速查模块表格化 ===")

spec_css = '''
  /* v0.9.0: 单位速查表格样式 */
  .spec-table-wrap {
    margin: 12px 0;
    border: 1px solid var(--line);
    border-radius: var(--r-m);
    overflow: hidden;
    background: var(--surface);
  }
  .spec-table-scroll {
    max-height: 280px;
    overflow-y: auto;
    overflow-x: auto;
  }
  .spec-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  .spec-table thead th {
    position: sticky;
    top: 0;
    background: var(--table-header-bg, var(--brand));
    color: var(--table-header-text, #fff);
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 12px;
    border-bottom: 2px solid var(--line);
    white-space: nowrap;
  }
  .spec-table tbody td {
    padding: 7px 12px;
    border-bottom: 1px solid var(--table-border, var(--line-light));
    vertical-align: top;
    line-height: 1.5;
  }
  .spec-table tbody tr:nth-child(even) {
    background: var(--table-row-alt, var(--surface-2));
  }
  .spec-table .spec-symbol {
    font-weight: 700;
    color: var(--brand);
    font-family: "Consolas", "Monaco", monospace;
    white-space: nowrap;
  }
  .spec-table .spec-unit {
    color: var(--text-2);
    font-family: "Consolas", "Monaco", monospace;
    white-space: nowrap;
  }
  .spec-table .spec-en {
    color: var(--muted);
    font-size: 12px;
    font-style: italic;
  }
  .spec-table-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--muted);
    padding: 6px 12px;
    background: var(--surface-2);
    border-bottom: 1px solid var(--line);
  }
'''

style_end = html.rfind('</style>')
if style_end > 0:
    html = html[:style_end] + spec_css + html[style_end:]
    log("[OK] 单位速查表格 CSS 已插入")

# 安全 JS：try-catch 包裹，不包装原有函数
spec_js = '''
  /* v0.9.0: 单位速查表格化（安全版，try-catch 包裹）*/
  try {
    function convertSpecToTableSafe() {
      var blocks = document.querySelectorAll('.spec, .spec-block, .unit-spec, .quick-ref');
      for (var i = 0; i < blocks.length; i++) {
        var block = blocks[i];
        if (block.getAttribute('data-spec-converted')) continue;
        block.setAttribute('data-spec-converted', '1');
        var text = block.innerText || block.textContent || '';
        var lines = text.split('\\n').filter(function(l) { return l.trim().length > 0; });
        if (lines.length < 2) continue;
        var items = [];
        for (var j = 0; j < lines.length; j++) {
          var line = lines[j].trim();
          var parts = line.split(/[：:]/);
          if (parts.length >= 2) {
            var symbol = parts[0].trim();
            var rest = parts.slice(1).join(':').trim();
            items.push({symbol: symbol, meaning: rest, unit: '', en: ''});
          }
        }
        if (items.length === 0) continue;
        var tableHtml = '<div class="spec-table-wrap"><div class="spec-table-title">数值 · 单位速查</div><div class="spec-table-scroll"><table class="spec-table"><thead><tr><th>符号</th><th>含义</th><th>单位</th><th>英文全称</th></tr></thead><tbody>';
        for (var k = 0; k < items.length; k++) {
          var it = items[k];
          tableHtml += '<tr><td class="spec-symbol">' + it.symbol + '</td><td>' + it.meaning + '</td><td class="spec-unit">' + it.unit + '</td><td class="spec-en">' + it.en + '</td></tr>';
        }
        tableHtml += '</tbody></table></div></div>';
        block.innerHTML = tableHtml;
      }
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() { setTimeout(convertSpecToTableSafe, 100); });
    } else {
      setTimeout(convertSpecToTableSafe, 100);
    }
  } catch(e) { console.warn('spec table convert error:', e); }
'''

script_end = html.rfind('</script>')
if script_end > 0:
    html = html[:script_end] + spec_js + html[script_end:]
    log("[OK] 单位速查表格 JS 已插入（安全版）")

# ============================================================
# 修改 4：随机模块换条动画（CSS + 安全 JS，不包装原有函数）
# ============================================================
log("\n=== 修改 4：随机模块换条动画（简洁版）===")

shuffle_css = '''
  /* v0.9.0: 随机模块换条动画（简洁淡入淡出）*/
  .rand-fade-target {
    transition: opacity 0.2s ease;
  }
  .rand-fade-target.fading {
    opacity: 0;
  }
'''

style_end = html.rfind('</style>')
if style_end > 0:
    html = html[:style_end] + shuffle_css + html[style_end:]
    log("[OK] 随机动画 CSS 已插入")

# 安全 JS：使用事件委托，不包装原有函数
shuffle_js = '''
  /* v0.9.0: 随机模块换条动画（安全版，事件委托，不包装原有函数）*/
  try {
    function initShuffleAnimation() {
      var target = document.getElementById('randHost') || 
                   document.querySelector('#view-random .panel') ||
                   document.querySelector('#view-random .rand-content') ||
                   document.querySelector('.rand-host');
      if (!target) return;
      target.classList.add('rand-fade-target');
      document.addEventListener('click', function(e) {
        var btn = e.target.closest('.shuffle-btn, [onclick*="shuffle"], [onclick*="random"], .rand-shuffle-btn, button');
        if (!btn) return;
        var isShuffle = btn.className && btn.className.indexOf('shuffle') >= 0;
        var onclick = btn.getAttribute('onclick') || '';
        if (!isShuffle && onclick.indexOf('shuffle') < 0 && onclick.indexOf('random') < 0 && onclick.indexOf('Random') < 0) return;
        var t = document.getElementById('randHost') || 
                document.querySelector('#view-random .panel') ||
                document.querySelector('#view-random .rand-content') ||
                document.querySelector('.rand-host');
        if (!t) return;
        t.classList.add('fading');
        setTimeout(function() {
          setTimeout(function() { t.classList.remove('fading'); }, 250);
        }, 50);
      }, true);
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() { setTimeout(initShuffleAnimation, 200); });
    } else {
      setTimeout(initShuffleAnimation, 200);
    }
  } catch(e) { console.warn('shuffle animation init error:', e); }
'''

script_end = html.rfind('</script>')
if script_end > 0:
    html = html[:script_end] + shuffle_js + html[script_end:]
    log("[OK] 随机动画 JS 已插入（安全版，事件委托）")

# ============================================================
# 版本号更新：0.8.7 -> 0.9.0
# ============================================================
log("\n=== 版本号更新 ===")

version_patterns = [
    (r'车载光学(?:百科|知识工作台)?\s*v0\.8\.\d+', '车载光学知识工作台 v0.9.0'),
    (r'v0\.8\.\d+\s*·\s*2026-\d{2}-\d{2}', 'v0.9.0 · 2026-09-01'),
]

for pattern, repl in version_patterns:
    match = re.search(pattern, html)
    if match:
        log(f"  找到版本号: {match.group()}")
        html = re.sub(pattern, repl, html, count=1)
        log(f"[OK] 版本号已更新为: {repl}")
    else:
        log(f"[SKIP] 未匹配版本号模式: {pattern}")

# ============================================================
# 写回文件
# ============================================================
log("\n=== 写回文件 ===")
io.open(SRC, "w", encoding="utf-8").write(html)
log(f"原始大小: {original_len} 字符")
log(f"修改后大小: {len(html)} 字符")
log(f"增加: {len(html) - original_len} 字符")

log("\n" + "="*60)
log("构建完成（安全版）！所有 JS 代码均用 try-catch 包裹，不包装原有函数。")
log("="*60)
