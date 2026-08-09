# -*- coding: utf-8 -*-
import re

SRC = 'index.html'
OUT = 'index.html'
with open(SRC, encoding='utf-8') as f:
    s = f.read()

VER = 'v0.1.5 · 2026-08-10'

# ---------- 1) SHELL OPEN (replace <div class="wrap">) ----------
SHELL_OPEN = '''<div id="app">
  <aside id="sidebar">
    <div class="brand"><img src="icon-192.png" alt="logo" class="brand-logo"><span>车载光学</span></div>
    <nav class="nav-list">
      <button class="nav-item active" data-page="home"><span class="ni-ic">🏠</span><span class="ni-lb">首页</span></button>
      <button class="nav-item" data-page="random"><span class="ni-ic">🎲</span><span class="ni-lb">随机知识</span></button>
      <button class="nav-item" data-page="dash"><span class="ni-ic">📊</span><span class="ni-lb">数据看板</span></button>
    </nav>
    <div class="side-foot">''' + VER + '''<br>离线可用 · 单文件</div>
  </aside>
  <main id="main">
    <header id="topbar">
      <span class="tb-title" id="tbTitle">首页</span>
      <span class="tb-prog" id="tbProg">已学 0/19</span>
    </header>
    <section id="view-home" class="view active">
'''

assert '<div class="wrap">' in s, 'wrap not found'
s = s.replace('<div class="wrap">', SHELL_OPEN, 1)

# ---------- 2) CAT CARDS + #browse open (before <div class="catbar">) ----------
CATCARDS = '''      <div class="cat-cards">
        <div class="cat-card" data-cat="optics"><div class="cc-ic">🔬</div><div class="cc-lb">光学</div><div class="cc-en">12 交互模块</div></div>
        <div class="cat-card" data-cat="reliability"><div class="cc-ic">🌡️</div><div class="cc-lb">信赖性</div><div class="cc-en">实车退化</div></div>
        <div class="cat-card" data-cat="process"><div class="cc-ic">🏭</div><div class="cc-lb">工艺</div><div class="cc-en">产线对照</div></div>
        <div class="cat-card" data-cat="drawing"><div class="cc-ic">📐</div><div class="cc-lb">图纸</div><div class="cc-en">符号图解</div></div>
      </div>
      <div id="browse">
'''
assert '<div class="catbar">' in s, 'catbar not found'
s = s.replace('<div class="catbar">', CATCARDS + '<div class="catbar">', 1)

# ---------- 3) CLOSE browse + home view, open random + dash, close app, add bottomtab ----------
CLOSE_BLOCK = '''      </div><!-- /#browse -->
    </section><!-- /#view-home -->

    <section id="view-random" class="view">
      <div class="reader glass" id="randHost"></div>
      <div class="rand-bar">
        <button class="gbtn" id="randNext">换一条 →</button>
        <button class="gbtn ghost" id="randFav">☆ 收藏</button>
        <button class="gbtn ghost" id="randBack">← 返回首页</button>
      </div>
    </section>

    <section id="view-dash" class="view">
      <div class="dash glass" id="dashHost"></div>
    </section>
  </main>
</div><!-- /#app -->

<nav id="bottomtab">
  <button class="bt-item active" data-page="home"><span class="bt-ic">🏠</span><span class="bt-lb">首页</span></button>
  <button class="bt-item" data-page="random"><span class="bt-ic">🎲</span><span class="bt-lb">随机</span></button>
  <button class="bt-item" data-page="dash"><span class="bt-ic">📊</span><span class="bt-lb">看板</span></button>
</nav>
'''

VER_OLD = '<div class="ver">版本 v0.1.4 · 2026-08-05 · 历史版本与变更见 CHANGELOG.md</div>'
assert VER_OLD in s, 'ver line not found'
s = s.replace(VER_OLD + '\n</div>', CLOSE_BLOCK, 1)

# ---------- 4) launch ver bump + tile→home view ----------
s = s.replace('<p class="ver">v0.1.4 · 2026-08-05</p>', '<p class="ver">' + VER + '</p>', 1)
s = s.replace('if (window.showCat) showCat(cat);',
              'if (window.showCat) showCat(cat); if (window.showView) showView(\'home\');', 1)

# ---------- 5) NEW CSS before </head> ----------
NEW_CSS = r'''
<style>
  /* ===== v0.1.5 新壳：玻璃 / 粒子 / 响应式导航 / 入场动画 ===== */
  :root{ --brand:#3370FF; --brand-700:#2b5fe0; --brand-ink:#0b1f4d; --ink:#eaf1ff; --sub:#a9c0ee; }
  html,body{height:100%;}
  body{ margin:0; color:var(--ink);
    background:
      radial-gradient(1200px 700px at 78% -10%, rgba(51,112,255,.45), transparent 60%),
      radial-gradient(900px 600px at 10% 110%, rgba(43,95,224,.40), transparent 55%),
      linear-gradient(160deg,#081430 0%,#0c2150 45%,#102a6e 100%);
    font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;
    -webkit-font-smoothing:antialiased; overflow-x:hidden;
  }
  #bg{position:fixed; inset:0; width:100%; height:100%; z-index:0; pointer-events:none;}
  #app{position:relative; z-index:1; display:flex; min-height:100vh;}
  #sidebar{ position:fixed; left:0; top:0; bottom:0; width:248px; z-index:50;
    display:flex; flex-direction:column; padding:22px 16px;
    background:rgba(10,26,64,.55); backdrop-filter:blur(22px); -webkit-backdrop-filter:blur(22px);
    border-right:1px solid rgba(255,255,255,.10); }
  .brand{display:flex; align-items:center; gap:11px; font-size:18px; font-weight:800; letter-spacing:.5px; color:#fff; padding:6px 8px 18px;}
  .brand-logo{width:38px; height:38px; border-radius:10px; box-shadow:0 4px 14px rgba(51,112,255,.45);}
  .nav-list{display:flex; flex-direction:column; gap:8px; margin-top:6px;}
  .nav-item{ display:flex; align-items:center; gap:12px; padding:12px 14px; border-radius:14px;
    background:transparent; border:1px solid transparent; color:var(--sub);
    font-size:15px; font-weight:600; cursor:pointer; text-align:left; transition:.18s; }
  .nav-item .ni-ic{font-size:19px;}
  .nav-item:hover{background:rgba(255,255,255,.06); color:#fff;}
  .nav-item.active{background:linear-gradient(135deg,var(--brand),var(--brand-700)); color:#fff; border-color:rgba(255,255,255,.25); box-shadow:0 8px 22px rgba(51,112,255,.40);}
  .side-foot{margin-top:auto; font-size:11px; color:rgba(169,192,238,.7); line-height:1.6; padding:10px 8px 0;}
  #main{margin-left:248px; flex:1; min-height:100vh; overflow-x:hidden;}
  #topbar{ position:sticky; top:0; z-index:40; display:flex; align-items:center; justify-content:space-between;
    padding:14px 22px; backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
    background:rgba(10,26,64,.40); border-bottom:1px solid rgba(255,255,255,.08); }
  .tb-title{font-size:17px; font-weight:700; color:#fff;}
  .tb-prog{font-size:12.5px; font-weight:600; color:#fff; background:rgba(51,112,255,.30); border:1px solid rgba(255,255,255,.18); padding:5px 12px; border-radius:999px;}
  .view{display:none; padding:22px; max-width:1100px; margin:0 auto;}
  .view.active{display:block; animation:viewIn .5s cubic-bezier(.22,.61,.36,1) both;}
  @keyframes viewIn{from{opacity:0; transform:translateY(16px);} to{opacity:1; transform:none;}}
  .hero{ position:relative; overflow:hidden; border-radius:24px; padding:30px 28px; margin-bottom:20px;
    background:rgba(255,255,255,.07); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,.14); box-shadow:0 18px 50px rgba(5,15,45,.35); }
  .hero-deco{opacity:.55;}
  .hero-badge{display:inline-block; font-size:12px; font-weight:700; color:#fff; background:rgba(51,112,255,.35); border:1px solid rgba(255,255,255,.22); padding:4px 12px; border-radius:999px; margin-bottom:10px;}
  .hero-title{font-size:30px; font-weight:800; color:#fff; margin:0; letter-spacing:1px;}
  .hero-sub{font-size:13px; color:var(--sub); letter-spacing:2px; margin:2px 0 14px;}
  .hero-chips{display:flex; flex-wrap:wrap; gap:8px;}
  .hero-chip{font-size:12px; color:#dbe6ff; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.14); padding:5px 11px; border-radius:999px;}
  .cat-cards{display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:22px;}
  @media(max-width:760px){ .cat-cards{grid-template-columns:repeat(2,1fr);} }
  .cat-card{ background:rgba(255,255,255,.92); border:1px solid rgba(255,255,255,.7); border-radius:18px; padding:18px 14px;
    text-align:center; cursor:pointer; transition:.18s; box-shadow:0 10px 28px rgba(5,15,45,.22); color:#16264f; animation:viewIn .55s both; }
  .cat-card:hover{transform:translateY(-4px); box-shadow:0 18px 40px rgba(51,112,255,.35);}
  .cc-ic{font-size:30px; line-height:1;} .cc-lb{font-size:16px; font-weight:800; margin-top:8px; color:#16264f;} .cc-en{font-size:11.5px; color:#5b6678; margin-top:2px;}
  .catbar{display:flex; flex-wrap:wrap; gap:10px; margin:6px 0 14px;}
  .cat{padding:9px 20px; border:1px solid rgba(255,255,255,.5); background:rgba(255,255,255,.85); border-radius:12px; cursor:pointer; font-size:14px; font-weight:700; color:#2a3f6e; transition:.15s;}
  .cat.active{background:var(--brand); color:#fff; border-color:var(--brand); box-shadow:0 6px 16px rgba(51,112,255,.4);}
  .tabs{display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px;}
  .tab{padding:8px 12px; border:1px solid rgba(255,255,255,.5); background:rgba(255,255,255,.82); border-radius:10px; cursor:pointer; font-size:13px; font-weight:600; color:#2a3f6e; text-align:center; transition:.15s; line-height:1.2;}
  .tab.active{background:var(--brand); color:#fff; border-color:var(--brand);}
  .tab .en{display:block; font-size:10px; font-weight:500; opacity:.8; margin-top:1px;}
  .panel{ background:rgba(255,255,255,.94); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,.7); border-radius:20px; padding:22px 24px; margin:16px 0;
    box-shadow:0 14px 38px rgba(5,15,45,.30); color:#1a2233; animation:viewIn .5s both; }
  .reader{background:rgba(255,255,255,.96); border:1px solid rgba(255,255,255,.75); border-radius:22px; padding:24px; box-shadow:0 18px 50px rgba(5,15,45,.35); color:#1a2233; min-height:200px;}
  .rand-bar{display:flex; gap:10px; flex-wrap:wrap; margin-top:16px;}
  .gbtn{font-size:14px; font-weight:700; color:#fff; background:linear-gradient(135deg,var(--brand),var(--brand-700)); border:none; border-radius:12px; padding:11px 18px; cursor:pointer; box-shadow:0 8px 20px rgba(51,112,255,.35); transition:.15s;}
  .gbtn:hover{transform:translateY(-2px);}
  .gbtn.ghost{background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.22); color:#fff; box-shadow:none;}
  .gbtn.on{background:linear-gradient(135deg,#f59e0b,#f97316);}
  .dash{background:rgba(255,255,255,.96); border:1px solid rgba(255,255,255,.75); border-radius:22px; padding:26px; box-shadow:0 18px 50px rgba(5,15,45,.35); color:#1a2233;}
  .dash h2{margin:0 0 4px; font-size:22px;} .dash .dsub{color:#5b6678; font-size:13px; margin-bottom:18px;}
  .stat-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:22px;}
  @media(max-width:680px){ .stat-grid{grid-template-columns:repeat(2,1fr);} }
  .stat{background:linear-gradient(160deg,#eef3ff,#e3ebff); border:1px solid #d8e2ff; border-radius:16px; padding:16px; text-align:center;}
  .stat .num{font-size:30px; font-weight:800; color:var(--brand);} .stat .lbl{font-size:12.5px; color:#5b6678; margin-top:2px;}
  .cat-prog{margin-bottom:14px;}
  .cp-head{display:flex; justify-content:space-between; font-size:13.5px; font-weight:700; color:#1a2233; margin-bottom:6px;}
  .cp-bar{height:10px; border-radius:999px; background:#e6ecf7; overflow:hidden;}
  .cp-fill{height:100%; border-radius:999px; background:linear-gradient(90deg,var(--brand),#5b8dff); transition:width .8s cubic-bezier(.22,.61,.36,1);}
  .recent{margin-top:18px;}
  .recent .ri{display:flex; align-items:center; justify-content:space-between; padding:10px 14px; background:#f4f7fc; border:1px solid #e6ecf7; border-radius:12px; margin-bottom:8px; cursor:pointer; transition:.15s;}
  .recent .ri:hover{background:#eaf0fb;}
  .recent .ri .rt{font-weight:700; color:#1a2233;} .recent .ri .re{font-size:11.5px; color:#5b6678;}
  .empty{color:#5b6678; font-size:13.5px; padding:18px; text-align:center; background:#f4f7fc; border-radius:14px;}
  #bottomtab{display:none; position:fixed; left:0; right:0; bottom:0; z-index:60; height:64px;
    align-items:center; justify-content:space-around; padding-bottom:env(safe-area-inset-bottom);
    background:rgba(10,26,64,.62); backdrop-filter:blur(22px); -webkit-backdrop-filter:blur(22px); border-top:1px solid rgba(255,255,255,.12);}
  .bt-item{display:flex; flex-direction:column; align-items:center; gap:2px; background:none; border:none; color:var(--sub); cursor:pointer; font-size:11px; font-weight:600;}
  .bt-item .bt-ic{font-size:20px;} .bt-item.active{color:#fff;} .bt-item.active .bt-ic{filter:drop-shadow(0 0 8px rgba(51,112,255,.9));}
  #homeFab{display:none !important;}
  @media(max-width:860px){ #sidebar{display:none;} #main{margin-left:0; padding-bottom:80px;} #bottomtab{display:flex;} }
  @media (prefers-reduced-motion: reduce){ .view.active,.panel,.cat-card{animation:none !important;} }
</style>
'''
assert '</head>' in s, 'head close not found'
s = s.replace('</head>', NEW_CSS + '\n</head>', 1)

# ---------- 6) NEW APP JS before </body> ----------
NEW_JS = r'''
<script>
(function(){
  "use strict";
  var VER_TOTAL = 19;
  var LS = {
    get:function(k,d){ try{ var v=localStorage.getItem(k); return v?JSON.parse(v):d; }catch(e){ return d; } },
    set:function(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} }
  };
  function recordView(id){
    var seen = LS.get('optics_seen',[]);
    if(seen.indexOf(id)<0){ seen.push(id); LS.set('optics_seen',seen); }
    updateProg();
  }
  function toggleFav(id){
    var f = LS.get('optics_fav',[]); var i = f.indexOf(id);
    if(i<0) f.push(id); else f.splice(i,1);
    LS.set('optics_fav',f); return i<0;
  }
  var ITEMS = [];
  document.querySelectorAll('.tabs .tab').forEach(function(t){
    var id = t.id.replace('tab-','');
    var cat = t.closest('.tabs').id.replace('subtabs-','');
    var en = t.querySelector('.en') ? t.querySelector('.en').textContent : '';
    var title = ''; t.childNodes.forEach(function(n){ if(n.nodeType===3) title += n.textContent; });
    ITEMS.push({id:id, cat:cat, title:title.trim(), en:en});
  });
  var CATNAME = { optics:'光学', reliability:'信赖性', process:'工艺', drawing:'图纸' };
  function seenCount(){ return LS.get('optics_seen',[]).length; }

  var _showTab = showTab; showTab = function(id){ _showTab(id); recordView(id); };
  var _showCat = showCat; showCat = function(cat){ _showCat(cat); };

  var currentView = 'home';
  var randPanelEl = null;
  var lastRandId = null;
  var randHost = document.getElementById('randHost');
  var dashHost = document.getElementById('dashHost');
  var TITLES = { home:'首页', random:'随机知识', dash:'数据看板' };

  function updateProg(){ var p=document.getElementById('tbProg'); if(p) p.textContent='已学 '+seenCount()+'/'+VER_TOTAL; }

  function showView(page){
    if(currentView==='random' && page!=='random' && randPanelEl) returnRandom();
    currentView = page;
    document.querySelectorAll('.view').forEach(function(v){ v.classList.remove('active'); });
    var el = document.getElementById('view-'+page); if(el) el.classList.add('active');
    document.querySelectorAll('.nav-item').forEach(function(b){ b.classList.toggle('active', b.dataset.page===page); });
    document.querySelectorAll('.bt-item').forEach(function(b){ b.classList.toggle('active', b.dataset.page===page); });
    var tt = document.getElementById('tbTitle'); if(tt) tt.textContent = TITLES[page]||'';
    if(page==='dash') renderDash();
    if(page==='random' && !randPanelEl) nextRandom();
  }

  function returnRandom(){
    if(randPanelEl){ document.getElementById('browse').appendChild(randPanelEl); randPanelEl.classList.remove('show'); randPanelEl=null; }
  }
  function nextRandom(){
    returnRandom();
    var pool = ITEMS.filter(function(it){ return it.id!==lastRandId; });
    var pick = pool[Math.floor(Math.random()*pool.length)];
    lastRandId = pick.id;
    var panel = document.getElementById('panel-'+pick.id);
    if(!panel) return;
    randHost.appendChild(panel);
    panel.classList.add('show');
    if(renderMap && renderMap[pick.id]) renderMap[pick.id]();
    randPanelEl = panel;
    recordView(pick.id);
    var f = LS.get('optics_fav',[]); var on = f.indexOf(pick.id)>=0;
    var btn = document.getElementById('randFav'); if(btn){ btn.textContent = on?'★ 已收藏':'☆ 收藏'; btn.classList.toggle('on',on); }
    updateProg();
  }
  function stat(num,lbl){ return '<div class="stat"><div class="num">'+num+'</div><div class="lbl">'+lbl+'</div></div>'; }
  function renderDash(){
    var seen = LS.get('optics_seen',[]);
    var fav = LS.get('optics_fav',[]);
    var total = ITEMS.length; var seenN = seen.length; var pct = total?Math.round(seenN/total*100):0;
    var cats = {};
    ITEMS.forEach(function(it){ if(!cats[it.cat]) cats[it.cat]={name:CATNAME[it.cat],total:0,done:0}; cats[it.cat].total++; if(seen.indexOf(it.id)>=0) cats[it.cat].done++; });
    var html = '<h2>📊 学习数据看板</h2><div class="dsub">基于本地存储（localStorage），离线可用、隐私不出端</div>';
    html += '<div class="stat-grid">'+stat(seenN,'已学习知识点')+stat(pct+'%','总进度')+stat(fav.length,'已收藏')+'</div>';
    Object.keys(cats).forEach(function(k){
      var c = cats[k]; var p = c.total?Math.round(c.done/c.total*100):0;
      html += '<div class="cat-prog"><div class="cp-head"><span>'+c.name+'</span><span>'+c.done+'/'+c.total+'</span></div><div class="cp-bar"><div class="cp-fill" style="width:'+p+'%"></div></div></div>';
    });
    html += '<div class="recent"><div class="cp-head"><span>最近学习</span><span></span></div>';
    if(seen.length===0){ html += '<div class="empty">还没有学习记录，去首页或随机知识看看吧 🚀</div>'; }
    else {
      seen.slice().reverse().slice(0,8).forEach(function(id){
        var it = null; for(var i=0;i<ITEMS.length;i++){ if(ITEMS[i].id===id){ it=ITEMS[i]; break; } } if(!it) return;
        html += '<div class="ri" data-go="'+id+'"><div><div class="rt">'+it.title+'</div><div class="re">'+CATNAME[it.cat]+' · '+it.en+'</div></div><div style="color:#3370FF;font-size:18px;">→</div></div>';
      });
    }
    html += '</div>';
    dashHost.innerHTML = html;
    dashHost.querySelectorAll('.ri').forEach(function(r){
      r.addEventListener('click', function(){
        var id=r.dataset.go; var it=null; for(var i=0;i<ITEMS.length;i++){ if(ITEMS[i].id===id){ it=ITEMS[i]; break; } }
        if(it){ showCat(it.cat); showView('home'); var t=document.getElementById('tab-'+id); if(t) t.click(); window.scrollTo({top:0,behavior:'smooth'}); }
      });
    });
  }
  function initParticles(){
    var cv=document.getElementById('bg'); if(!cv) return;
    var ctx=cv.getContext('2d'); var DPR=Math.min(window.devicePixelRatio||1,2);
    var W,H,parts=[],raf;
    function resize(){
      W=cv.width=Math.floor(innerWidth*DPR); H=cv.height=Math.floor(innerHeight*DPR);
      cv.style.width=innerWidth+'px'; cv.style.height=innerHeight+'px';
      var n=Math.max(28, Math.min(90, Math.round(innerWidth*innerHeight/24000)));
      parts=[]; for(var i=0;i<n;i++){ parts.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*0.22*DPR,vy:(Math.random()-.5)*0.22*DPR,r:(Math.random()*1.5+0.5)*DPR}); }
    }
    function frame(){
      ctx.clearRect(0,0,W,H); var i,j,a,b,dx,dy,d;
      for(i=0;i<parts.length;i++){ a=parts[i]; a.x+=a.vx; a.y+=a.vy; if(a.x<0||a.x>W)a.vx*=-1; if(a.y<0||a.y>H)a.vy*=-1;
        ctx.beginPath(); ctx.arc(a.x,a.y,a.r,0,6.283); ctx.fillStyle='rgba(185,208,255,0.5)'; ctx.fill(); }
      for(i=0;i<parts.length;i++){ for(j=i+1;j<parts.length;j++){ a=parts[i]; b=parts[j]; dx=a.x-b.x; dy=a.y-b.y; d=Math.sqrt(dx*dx+dy*dy);
        if(d<130*DPR){ ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.strokeStyle='rgba(120,160,255,'+(0.10*(1-d/(130*DPR)))+')'; ctx.lineWidth=DPR; ctx.stroke(); } } }
      raf=requestAnimationFrame(frame);
    }
    resize(); window.addEventListener('resize', resize);
    if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches){ frame(); cancelAnimationFrame(raf); }
    else raf=requestAnimationFrame(frame);
  }
  document.querySelectorAll('.nav-item,.bt-item').forEach(function(b){ b.addEventListener('click', function(){ showView(b.dataset.page); }); });
  document.querySelectorAll('.cat-card').forEach(function(c){ c.addEventListener('click', function(){ showCat(c.dataset.cat); showView('home'); window.scrollTo({top:0,behavior:'smooth'}); }); });
  document.getElementById('randNext').addEventListener('click', nextRandom);
  document.getElementById('randBack').addEventListener('click', function(){ showView('home'); });
  document.getElementById('randFav').addEventListener('click', function(){ if(lastRandId){ var on=toggleFav(lastRandId); var btn=document.getElementById('randFav'); btn.textContent = on?'★ 已收藏':'☆ 收藏'; btn.classList.toggle('on',on); } });
  updateProg();
  initParticles();
  showView('home');
})();
</script>
'''
assert '</body>' in s, 'body close not found'
s = s.replace('</body>', NEW_JS + '\n</body>', 1)

# ---------- write + validate ----------
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(s)
print('written', len(s), 'bytes')

clean = re.sub(r'<(script|style)[\s\S]*?</\1>', '', s)
tags = re.findall(r'</?([a-zA-Z][a-zA-Z0-9]*)', clean)
void = {'br','hr','img','input','meta','link','area','base','col','embed','param','source','track','wbr','path','circle','line','rect','ellipse','polygon','polyline','stop','use','text'}
opens = closes = 0
for t in tags:
    if t in void: continue
    if t.startswith('/'): closes += 1
    else: opens += 1
print('TAG BALANCE open', opens, 'close', closes, 'diff', opens - closes)
