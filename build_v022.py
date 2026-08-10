# -*- coding: utf-8 -*-
"""v0.2.2: 重新设计首页为 Notion 风格左右分栏，并修复 v0.2.1 遗留的孤立节点。"""
import io, re

SRC = "index.html"
html = io.open(SRC, encoding="utf-8").read()

# ---------- 1. 修复重复的 hero-chips（应为 8 个唯一） ----------
OLD_CHIPS = '''      <div class="hero-chips">
        <span class="hero-chip">光学基础 · 12</span>
        <span class="hero-chip">信赖性·车规 · 10</span>
        <span class="hero-chip">工艺制造 · 2</span>
        <span class="hero-chip">工程图纸 · 2</span>
        <span class="hero-chip">设备与仪器 · 5</span>
        <span class="hero-chip">工艺制造 · 2</span>
        <span class="hero-chip">工程图纸 · 2</span>
        <span class="hero-chip">模组与系统 · 6</span>
        <span class="hero-chip">材料与镜片 · 3</span>
        <span class="hero-chip">应用场景 · 5</span>
      </div>'''
NEW_CHIPS = '''      <div class="hero-chips">
        <span class="hero-chip">光学基础 · 12</span>
        <span class="hero-chip">信赖性·车规 · 10</span>
        <span class="hero-chip">设备与仪器 · 5</span>
        <span class="hero-chip">工艺制造 · 2</span>
        <span class="hero-chip">工程图纸 · 2</span>
        <span class="hero-chip">模组与系统 · 6</span>
        <span class="hero-chip">材料与镜片 · 3</span>
        <span class="hero-chip">应用场景 · 5</span>
      </div>'''
assert OLD_CHIPS in html, "OLD_CHIPS not found!"
html = html.replace(OLD_CHIPS, NEW_CHIPS, 1)
print("[1/7] hero-chips 去重 -> 8 个唯一")

# ---------- 2. cat-cards（含 3 个孤立卡片）-> 左列 cat-nav + 开启 home-split ----------
OLD_BLOCK = re.compile(r'<div class="cat-cards">.*?<div id="browse">', re.S)
assert OLD_BLOCK.search(html), "cat-cards block not found!"

CATS = [
    ("optics", "🔬", "光学基础", "Optics Fundamentals", "12"),
    ("reliability", "🌡️", "信赖性·车规", "Reliability & Qual", "10"),
    ("equipment", "⚙️", "设备与仪器", "Equipment & Tools", "5"),
    ("process", "🏭", "工艺制造", "Manufacturing", "2"),
    ("drawing", "📐", "工程图纸", "Engineering Drawing", "2"),
    ("module", "🔧", "模组与系统", "Module & System", "6"),
    ("material", "💎", "材料与镜片", "Materials & Lens", "3"),
    ("application", "🚗", "应用场景", "Applications", "5"),
]
items = []
for i, (cid, ic, lb, en, cnt) in enumerate(CATS):
    act = ' active' if cid == 'optics' else ''
    items.append(
        f'      <div class="cat-nav-item{act}" id="cat-{cid}" onclick="showCat(\'{cid}\')">\n'
        f'        <span class="cn-ic">{ic}</span>\n'
        f'        <span class="cn-lb">{lb}<span class="cn-en">{en}</span></span>\n'
        f'        <span class="cn-count">{cnt}</span>\n'
        f'      </div>'
    )
nav_html = (
    '      <div class="home-split">\n'
    '        <aside class="cat-nav">\n'
    '          <div class="cat-nav-h">知识分类 · 8</div>\n'
    + "\n".join(items) + "\n"
    '        </aside>\n'
    '      <div id="browse">'
)
html = OLD_BLOCK.sub(nav_html, html, 1)
print("[2/7] 首页改为 home-split：左列 cat-nav（8 项）+ 右列 browse")

# ---------- 3. 删除 #browse 内遗留的 .catbar（含 3 个孤立 cat） ----------
OLD_CATBAR = re.compile(r'<div class="catbar">.*?<div class="tabs" id="subtabs-optics">', re.S)
assert OLD_CATBAR.search(html), "catbar block not found!"
html = OLD_CATBAR.sub('<div class="tabs" id="subtabs-optics">', html, 1)
print("[3/7] 删除横向 catbar（分类选择改由左列 cat-nav 承担）")

# ---------- 4. 在 </section> 前闭合 home-split ----------
assert '</section><!-- /#view-home -->' in html
html = html.replace('</section><!-- /#view-home -->',
                    '      </div><!-- /home-split -->\n    </section><!-- /#view-home -->', 1)
print("[4/7] 闭合 home-split 容器")

# ---------- 5. CSS：替换 .cat-cards 区块为 home-split / cat-nav 样式 ----------
OLD_CSS = re.compile(r'  \.cat-cards\{.*?/\* ---- 随机页 ---- \*/', re.S)
assert OLD_CSS.search(html), "cat-cards CSS not found!"
NEW_CSS = '''  /* ---- 首页：Notion 风格左右分栏 ---- */
  .home-split{ display:flex; gap:20px; align-items:stretch; margin-top:10px; }
  .cat-nav{
    width:248px; flex-shrink:0; align-self:stretch;
    display:flex; flex-direction:column; gap:3px;
    padding:10px; border-radius:var(--r-l);
    background:var(--surface); border:1px solid var(--line);
    backdrop-filter:var(--glass-blur); -webkit-backdrop-filter:var(--glass-blur);
    box-shadow:var(--sh);
    max-height:calc(100vh - 168px); overflow:auto; position:sticky; top:74px;
    animation:viewIn .5s both;
  }
  .cat-nav-h{
    font-size:11px; font-weight:700; letter-spacing:.09em; text-transform:uppercase;
    color:var(--muted-2); padding:6px 12px 9px;
  }
  .cat-nav-item{
    display:flex; align-items:center; gap:11px; cursor:pointer;
    padding:9px 11px; border-radius:12px; border:1px solid transparent;
    color:var(--muted); font-size:14px; font-weight:600; line-height:1.3;
    transition:background .2s,color .2s,border-color .2s,transform .2s;
  }
  .cat-nav-item .cn-ic{
    width:34px; height:34px; flex-shrink:0; border-radius:9px; font-size:18px;
    display:flex; align-items:center; justify-content:center;
    background:linear-gradient(135deg,rgba(91,140,255,.16),rgba(124,108,255,.10));
    transition:background .25s;
  }
  .cat-nav-item .cn-lb{ flex:1; min-width:0; }
  .cat-nav-item .cn-en{ display:block; font-size:10.5px; font-weight:500; color:var(--muted-2); margin-top:1px; }
  .cat-nav-item .cn-count{
    font-size:11px; font-weight:700; color:var(--brand);
    background:rgba(91,140,255,.12); padding:2px 8px; border-radius:99px; flex-shrink:0;
  }
  .cat-nav-item:hover{ background:rgba(255,255,255,.05); color:var(--text); border-color:var(--line); }
  .cat-nav-item.active{
    background:linear-gradient(135deg,rgba(91,140,255,.20),rgba(124,108,255,.12));
    color:var(--text); border-color:var(--acc-line);
    box-shadow:0 0 0 1px rgba(91,140,255,.22),var(--sh);
  }
  .cat-nav-item.active .cn-ic{ background:linear-gradient(135deg,var(--brand),var(--brand-2)); }
  #browse{ flex:1; min-width:0; }
  @media(max-width:980px){
    .cat-nav{ width:210px; }
  }
  @media(max-width:860px){
    .home-split{ flex-direction:column; gap:14px; }
    .cat-nav{
      width:100%; flex-direction:row; max-height:none; position:static;
      overflow-x:auto; overflow-y:hidden; padding:8px; gap:8px;
    }
    .cat-nav-h{ display:none; }
    .cat-nav-item{ flex:0 0 auto; align-items:center; }
    .cat-nav-item .cn-en{ display:none; }
  }
  /* ---- 随机页 ---- */'''
html = OLD_CSS.sub(NEW_CSS, html, 1)
print("[5/7] CSS：cat-cards -> home-split / cat-nav（含响应式）")

# ---------- 6. 版本号 v0.2.1 -> v0.2.2 ----------
assert "车载光学百科 v0.2.1" in html
html = html.replace("车载光学百科 v0.2.1", "车载光学百科 v0.2.2", 1)
assert "v0.2.0 · 2026-08-10" in html
html = html.replace("v0.2.0 · 2026-08-10", "v0.2.2 · 2026-08-10", 1)
print("[6/7] 版本号 -> v0.2.2")

# ---------- 7. 断言：无孤立节点残留 ----------
assert 'class="cat-cards"' not in html, "cat-cards 残留!"
assert '<div class="catbar">' not in html, "catbar 残留!"
# 8 个分类 id 在 cat-nav 中（每个恰好 1 次）
for c in ['optics','reliability','equipment','process','drawing','module','material','application']:
    assert html.count('id="cat-%s"' % c) == 1, "cat-%s 数量异常" % c
# nav 项：7 个普通 + 1 个 active = 8
nav_count = html.count('class="cat-nav-item"') + html.count('class="cat-nav-item active"')
assert nav_count == 8, "cat-nav-item 数量应为 8，实得 %d" % nav_count
assert html.count('home-split') >= 2, "home-split 开闭不完整"
print("[7/7] 断言通过：无孤立节点，8 分类导航就位")

io.open(SRC, "w", encoding="utf-8").write(html)
print("OK -> 写入", SRC)
