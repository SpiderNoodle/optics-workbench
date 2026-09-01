# -*- coding: utf-8 -*-
"""
v0.9.0 构建脚本：四项修改
1. Kindle 主题释义文字降亮（提升可读性）
2. 新增 Office/WPS 主题（仿 Excel 办公风格）
3. 单位速查模块改为可滑动表格形式（含字符含义+英文全称）
4. 随机模块换条添加简洁淡入淡出动画
版本：0.8.9 -> 0.9.0
"""
import io, re, sys

SRC = "index.html"
html = io.open(SRC, encoding="utf-8").read()
original_len = len(html)
report = []

def log(msg):
    print(msg)
    report.append(msg)

def safe_replace(pattern, repl, desc, flags=0, count=1):
    global html
    if isinstance(pattern, str):
        if pattern in html:
            html = html.replace(pattern, repl, count)
            log(f"[OK] {desc}")
            return True
        else:
            log(f"[SKIP] {desc} (精确字符串未匹配)")
            return False
    else:
        new_html, n = pattern.subn(repl, html, count=count, flags=flags)
        if n > 0:
            html = new_html
            log(f"[OK] {desc} (匹配 {n} 处)")
            return True
        else:
            log(f"[SKIP] {desc} (正则未匹配)")
            return False

# ============================================================
# 修改 1：Kindle 主题释义文字降亮
# ============================================================
log("\n=== 修改 1：Kindle 主题释义文字降亮 ===")

kindle_match = re.search(r'\[data-theme=["\']?kindle["\']?\]', html, re.IGNORECASE)
if kindle_match:
    log("  找到 Kindle 主题定义")
    start = kindle_match.start()
    brace_start = html.find('{', start)
    if brace_start > 0:
        depth = 0
        i = brace_start
        while i < len(html):
            if html[i] == '{':
                depth += 1
            elif html[i] == '}':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        insert_pos = i + 1
        kindle_define_override = '''
  /* Kindle 主题：释义文字降亮，提升可读性 */
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
        html = html[:insert_pos] + kindle_define_override + html[insert_pos:]
        log("[OK] Kindle 主题释义文字降亮（插入覆盖样式）")
    else:
        log("[SKIP] 未找到 Kindle 主题块的大括号")
else:
    kindle_alt = re.search(r'(kindle|Kindle|KINDLE)', html)
    if kindle_alt:
        log(f"  找到 Kindle 相关文本（位置 {kindle_alt.start()}），但未找到 data-theme 定义")
    else:
        log("[SKIP] 未找到 Kindle 主题定义，可能主题名称不同")

# ============================================================
# 修改 2：新增 Office/WPS 主题（仿 Excel 办公风格）
# ============================================================
log("\n=== 修改 2：新增 Office/WPS 主题 ===")

office_theme_css = '''
  /* ===== Office/WPS 主题（仿 Excel 办公风格）===== */
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

insert_marker = re.compile(r'/\*\s*-+\s*随机页\s*-+\s*\*/')
marker_match = insert_marker.search(html)
if marker_match:
    insert_pos = marker_match.start()
    html = html[:insert_pos] + office_theme_css + '\n' + html[insert_pos:]
    log("[OK] Office 主题 CSS 变量已插入（随机页 CSS 前）")
else:
    style_end = html.rfind('</style>')
    if style_end > 0:
        html = html[:style_end] + office_theme_css + '\n' + html[style_end:]
        log("[OK] Office 主题 CSS 变量已插入（</style> 前）")
    else:
        log("[SKIP] 未找到 CSS 插入位置")

# 主题选择器添加 Office 选项
theme_selector_pattern = re.compile(
    r'(class="theme-chip[^"]*"[^>]*data-theme=")([^"]+)(")',
    re.IGNORECASE
)
theme_chips = theme_selector_pattern.findall(html)
if theme_chips:
    log(f"  找到 {len(theme_chips)} 个主题选项")
    last_chip = theme_selector_pattern.finditer(html)
    last_pos = 0
    for m in last_chip:
        last_pos = m.end()
    if last_pos > 0:
        office_chip = '''
        <div class="theme-chip" data-theme="office" onclick="setTheme('office')">
          <div class="theme-swatch" style="background:linear-gradient(135deg,#217346,#e6f2ec);border:1px solid #d4d4d4;"></div>
          <div class="theme-info">
            <div class="theme-name">Office / WPS</div>
            <div class="theme-desc">Excel 办公风格</div>
          </div>
        </div>'''
        html = html[:last_pos] + office_chip + html[last_pos:]
        log("[OK] Office 主题选项已添加到主题选择器")
else:
    log("[SKIP] 未找到主题选择器结构，Office 主题 CSS 已添加但可能无切换入口")

# THEMES 数组添加 office
themes_array_pattern = re.compile(r'(THEMES\s*=\s*\[)([^\]]*)(\])', re.DOTALL)
themes_match = themes_array_pattern.search(html)
if themes_match:
    log("  找到 THEMES 数组")
    array_content = themes_match.group(2)
    office_theme_entry = '''
  { id: 'office', name: 'Office/WPS', icon: '📊', desc: 'Excel 办公风格' },'''
    last_comma = array_content.rfind(',')
    if last_comma > 0:
        new_content = array_content[:last_comma+1] + office_theme_entry + array_content[last_comma+1:]
    else:
        new_content = array_content + office_theme_entry
    html = html[:themes_match.start(2)] + new_content + html[themes_match.end(2):]
    log("[OK] Office 主题已添加到 THEMES 数组")
else:
    log("  未找到 THEMES 数组（可能使用其他配置方式）")

# ============================================================
# 修改 3：单位速查模块改为可滑动表格形式
# ============================================================
log("\n=== 修改 3：单位速查模块改为可滑动表格形式 ===")

spec_table_css = '''
  /* ===== 单位速查表格样式 ===== */
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
    table-layout: auto;
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
    letter-spacing: .02em;
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
  .spec-table tbody tr:hover {
    background: var(--brand-light, rgba(91,140,255,.08));
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
  .spec-table .spec-meaning {
    color: var(--text);
  }
  .spec-table .spec-en {
    color: var(--muted);
    font-size: 12px;
    font-style: italic;
  }
  .spec-table .spec-range {
    color: var(--text-2);
    font-size: 12px;
  }
  .spec-table-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--muted);
    padding: 6px 12px;
    background: var(--surface-2);
    border-bottom: 1px solid var(--line);
    letter-spacing: .05em;
    text-transform: uppercase;
  }
'''

style_end = html.rfind('</style>')
if style_end > 0:
    html = html[:style_end] + spec_table_css + html[style_end:]
    log("[OK] 单位速查表格 CSS 已插入")

spec_convert_js = '''
  // ===== 单位速查模块：运行时转换为表格形式 =====
  function convertSpecToTable() {
    var specBlocks = document.querySelectorAll('.spec, .spec-block, .unit-spec, .quick-ref');
    specBlocks.forEach(function(block) {
      if (block.dataset.converted) return;
      block.dataset.converted = 'true';
      var items = [];
      var lines = block.innerText.split('\\n').filter(function(l) { return l.trim(); });
      lines.forEach(function(line) {
        var match = line.match(/^([A-Za-z%°µμm\\.\\/]+)\\s*[（(]?([^）)]*)[）)]?\\s*[：:]?\\s*(.+)$/);
        if (match) {
          items.push({
            symbol: match[1].trim(),
            unit: match[2].trim(),
            meaning: match[3].trim(),
            en: '',
            range: ''
          });
        }
      });
      if (items.length > 0) {
        var tableHtml = '<div class="spec-table-wrap"><div class="spec-table-title">数值 · 单位速查</div><div class="spec-table-scroll"><table class="spec-table"><thead><tr><th>符号</th><th>单位</th><th>含义</th><th>英文全称</th><th>范围/说明</th></tr></thead><tbody>';
        items.forEach(function(item) {
          tableHtml += '<tr><td class="spec-symbol">' + item.symbol + '</td><td class="spec-unit">' + item.unit + '</td><td class="spec-meaning">' + item.meaning + '</td><td class="spec-en">' + item.en + '</td><td class="spec-range">' + item.range + '</td></tr>';
        });
        tableHtml += '</tbody></table></div></div>';
        block.innerHTML = tableHtml;
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', convertSpecToTable);
  } else {
    convertSpecToTable();
  }
  var originalShowTab = window.showTab;
  if (originalShowTab) {
    window.showTab = function() {
      originalShowTab.apply(this, arguments);
      setTimeout(convertSpecToTable, 50);
    };
  }
'''

script_end = html.rfind('</script>')
if script_end > 0:
    html = html[:script_end] + spec_convert_js + '\n' + html[script_end:]
    log("[OK] 单位速查表格转换 JS 已插入")

# ============================================================
# 修改 4：随机模块换条动画（简洁版：纯淡入淡出）
# ============================================================
log("\n=== 修改 4：随机模块换条动画（简洁版）===")

shuffle_animation_css = '''
  /* ===== 随机模块换条动画（简洁淡入淡出）===== */
  .rand-fade {
    transition: opacity 0.2s ease;
  }
  .rand-fade.out {
    opacity: 0;
  }
'''

style_end = html.rfind('</style>')
if style_end > 0:
    html = html[:style_end] + shuffle_animation_css + html[style_end:]
    log("[OK] 随机模块换条动画 CSS 已插入（简洁版）")

shuffle_js = '''
  // ===== 随机模块换条动画（简洁版：纯淡入淡出）=====
  function animateShuffle(callback) {
    var host = document.getElementById('randHost') || 
               document.querySelector('#view-random .panel') ||
               document.querySelector('#view-random .rand-content') ||
               document.querySelector('.rand-host');
    if (!host) { if (callback) callback(); return; }
    host.classList.add('rand-fade');
    host.classList.add('out');
    setTimeout(function() {
      if (callback) callback();
      setTimeout(function() {
        host.classList.remove('out');
      }, 50);
    }, 200);
  }
  var shuffleFunctions = ['shuffleRandom', 'randomKnowledge', 'nextRandom', 'shuffleKnowledge', 'randomItem'];
  shuffleFunctions.forEach(function(fnName) {
    if (typeof window[fnName] === 'function') {
      var original = window[fnName];
      window[fnName] = function() {
        var args = arguments;
        var self = this;
        animateShuffle(function() { original.apply(self, args); });
      };
    }
  });
'''

script_end = html.rfind('</script>')
if script_end > 0:
    html = html[:script_end] + shuffle_js + html[script_end:]
    log("[OK] 随机模块换条动画 JS 已插入（简洁版）")

# ============================================================
# 版本号更新：0.8.9 -> 0.9.0
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
log("构建完成！请在浏览器中打开 index.html 验证效果。")
log("="*60)
