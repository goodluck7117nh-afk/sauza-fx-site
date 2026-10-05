# -*- coding: utf-8 -*-
"""さうざーFX サイト生成スクリプト
python3 build.py で
  dist/      … Netlify / Cloudflare Pages にそのまま置ける完全なHTML一式
  artifact/  … プレビュー公開用（トップページだけ骨組みなし）
を出力する。"""
import os, random, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://sauza-fx.netlify.app"  # 独自ドメインが決まったら "https://example.com" のように入れる（SNS用の画像に使う）
GGJ_URL = "https://www.gogojungle.co.jp/systemtrade/fx/78813"
X_URL = "https://x.com/alex767_fx"

# ------------------------------------------------------------------ CSS
CSS = r"""
:root{
  --bg:#0A0B0D; --surface:#121418; --surface-2:#181B20; --ink:#ECE7DA; --muted:#9C978B; --line:#262A30;
  --gold:#D4A445; --gold-ink:#E3B95E; --gold-soft:#2A2214; --on-gold:#15110A;
  --thumb:#07080A; --thumb-grid:#1C222A; --thumb-ink:#7F8B96;
  --up:#4CC08F; --down:#E3765F; --ok:#5ACB98; --ok-soft:#13261D; --wip:#A2A6AB; --wip-soft:#20242A;
  --warn:#E3B45A; --warn-soft:#2A2312;
  --serif:"Shippori Mincho B1","Hiragino Mincho ProN","Yu Mincho",serif;
  --sans:"Zen Kaku Gothic New","Hiragino Sans","Yu Gothic",system-ui,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
  --radius:6px;
  color-scheme:dark;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15.5px;line-height:1.85;-webkit-font-smoothing:antialiased}
img,svg{max-width:100%}
a{color:inherit}
h1,h2,h3,h4{font-family:var(--serif);line-height:1.4;margin:0;text-wrap:balance;font-weight:800}
p{margin:0}
.wrap{max-width:1120px;margin-inline:auto;padding-inline:20px}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:4px}

/* PR bar + header */
.prbar{background:var(--surface-2);color:var(--muted);font-size:12px;text-align:center;padding:6px 16px;line-height:1.6}
.site-header{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.hd{display:flex;align-items:center;gap:24px;min-height:64px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;flex-shrink:0}
.logo-mark{width:36px;height:36px;border-radius:8px;display:block;object-fit:cover;background:#0B0B0D}
.logo b{font-family:var(--serif);font-size:21px;letter-spacing:.04em;font-weight:800;color:var(--gold-ink)}
.logo small{display:block;font-family:var(--mono);font-size:10px;color:var(--gold);letter-spacing:.12em;line-height:1;margin-top:2px}
.gnav{display:flex;gap:4px;margin-left:auto;align-items:center}
.gnav a{text-decoration:none;font-size:14px;padding:8px 12px;border-radius:4px;color:var(--muted)}
.gnav a:hover{color:var(--ink);background:var(--surface-2)}
.gnav a[aria-current="page"]{color:var(--ink);font-weight:700}
.gnav a.nav-x{margin-left:8px;border:1px solid var(--line);color:var(--ink)}
.menu-btn{display:none;margin-left:auto;background:none;border:1px solid var(--line);border-radius:4px;padding:8px 12px;font:inherit;font-size:13px;color:var(--ink);cursor:pointer}
@media (max-width:860px){
  .menu-btn{display:block}
  .gnav{display:none;position:absolute;left:0;right:0;top:100%;flex-direction:column;align-items:stretch;gap:0;background:var(--surface);border-bottom:1px solid var(--line);padding:8px 20px 16px}
  .gnav a{padding:12px 4px;border-bottom:1px solid var(--line);border-radius:0}
  .gnav a.nav-x{margin:12px 0 0;border:1px solid var(--line);border-radius:4px;text-align:center}
  .site-header.open .gnav{display:flex}
}

/* common */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;text-decoration:none;font-weight:700;font-size:14px;padding:12px 22px;border-radius:4px;border:1px solid var(--line);line-height:1.3;cursor:pointer}
.btn-primary{background:linear-gradient(180deg,#E6BC68,#C8952F);border-color:#C8952F;color:var(--on-gold)}
.btn-gold{background:linear-gradient(180deg,#E6BC68,#C8952F);border-color:#C8952F;color:var(--on-gold)}
.btn-ghost{background:transparent;color:var(--gold-ink);border-color:color-mix(in srgb,var(--gold) 55%,transparent)}
.btn-sm{padding:8px 14px;font-size:13px}
.btn[aria-disabled="true"]{background:var(--surface-2);border-color:var(--line);color:var(--muted);cursor:default}
.eyebrow{font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;color:var(--gold-ink);text-transform:uppercase}
.section{padding-block:64px}
.section + .section{border-top:1px solid var(--line)}
.sec-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.sec-head h2{font-size:clamp(23px,2.8vw,30px);margin-top:6px}
.sec-head p{color:var(--muted);font-size:14px;max-width:32em}
.more-link{font-size:14px;font-weight:700;color:var(--gold-ink);text-decoration:none;white-space:nowrap}
.more-link:hover{text-decoration:underline}
.muted{color:var(--muted)}
.chip{display:inline-block;font-size:11.5px;font-weight:700;padding:2px 10px;border-radius:999px;line-height:1.7;white-space:nowrap}
.st-sale{background:var(--gold-soft);color:var(--gold-ink)}
.st-fwd{background:var(--ok-soft);color:var(--ok)}
.st-prep,.st-dev{background:var(--wip-soft);color:var(--wip)}
.tag{display:inline-block;font-family:var(--mono);font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:3px;padding:0 6px;line-height:1.8}
.num{font-family:var(--mono);font-variant-numeric:tabular-nums}

/* page title band */
.page-head{padding-block:40px 32px;border-bottom:1px solid var(--line)}
.crumb{font-size:12.5px;color:var(--muted);display:flex;gap:6px;flex-wrap:wrap}
.crumb a{color:var(--muted);text-decoration:none}
.crumb a:hover{color:var(--ink);text-decoration:underline}
.page-head h1{font-size:clamp(26px,3.6vw,38px);margin-top:10px}
.page-head p{color:var(--muted);margin-top:10px;max-width:38em}

/* hero */
.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;padding-block:56px 64px}
.hero h1{font-size:clamp(30px,4.4vw,50px);margin-block:16px 18px;letter-spacing:.01em}
.hero h1 em{font-style:normal;color:var(--gold-ink)}
.hero .lead{color:var(--muted);max-width:33em}
.hero .cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.spec-line{display:flex;gap:6px;flex-wrap:wrap}
.feature-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.feature-card .thumb{border-radius:0}
.feature-card .fc-body{padding:18px 20px 20px;display:grid;gap:10px}
.feature-card .fc-top{display:flex;justify-content:space-between;align-items:center;gap:8px}
.feature-card h2{font-size:22px}
.feature-card p{font-size:13.5px;color:var(--muted)}
.feature-card .fc-actions{display:flex;gap:8px;flex-wrap:wrap}

/* entry tiles */
.entries{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.entry{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;align-items:start;text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px}
.entry:hover{border-color:var(--gold)}
.entry .ico{grid-row:span 2;width:40px;height:40px;border-radius:6px;background:var(--gold-soft);display:grid;place-items:center}
.entry .ico svg{width:22px;height:22px;stroke:var(--gold-ink);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.entry b{font-size:16px}
.entry span{font-size:13px;color:var(--muted);line-height:1.6}

/* product grid */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}
.pcard{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;display:flex;flex-direction:column}
.pcard:hover{border-color:color-mix(in srgb,var(--gold) 60%,var(--line))}
.thumb{display:block;background:var(--thumb);aspect-ratio:16/9;width:100%;max-width:100%;position:relative}
.thumb svg{display:block;width:100%;height:100%}
.thumb .t-label{position:absolute;left:10px;top:8px;font-family:var(--mono);font-size:10px;letter-spacing:.08em;color:var(--thumb-ink)}
.pcard .pb{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.pcard .row{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.pcard h3{font-size:17.5px}
.pcard h3 a{text-decoration:none}
.pcard h3 a:hover{text-decoration:underline}
.pcard .sub{font-size:12.5px;color:var(--muted);line-height:1.6}
.pcard .pact{margin-top:auto;padding-top:8px}
.pcard .pact .btn{width:100%}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px}
.filters button{font:inherit;font-size:13px;padding:6px 14px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--muted);cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--gold);border-color:var(--gold);color:var(--on-gold)}
.count{font-size:13px;color:var(--muted);margin-bottom:12px}

/* thumbnail svg classes */
.g-line{stroke:var(--thumb-grid);stroke-width:1}
.c-up{fill:var(--up);stroke:var(--up)}
.c-dn{fill:var(--down);stroke:var(--down)}
.o-gold{stroke:#D9A84A;fill:none;stroke-width:2.2}
.o-box{fill:rgba(217,168,74,.10);stroke:#D9A84A;stroke-width:1;stroke-dasharray:4 3}
.o-lvl{stroke:#D9A84A;stroke-width:1.2;stroke-dasharray:6 4}
.o-dot{fill:#D9A84A}
.o-txt{fill:#D9A84A;font-family:"JetBrains Mono",monospace;font-size:10px}

/* policy */
.policy{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.policy div{border-top:2px solid var(--gold);padding-top:16px}
.policy h3{font-size:18px;margin-bottom:8px}
.policy p{font-size:14px;color:var(--muted)}

/* blog */
.posts{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.post{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px;display:flex;flex-direction:column;gap:8px}
.post .meta{display:flex;justify-content:space-between;gap:8px;font-size:12px;color:var(--muted)}
.post h3{font-size:17px}
.post p{font-size:13.5px;color:var(--muted)}
.post .soon{margin-top:auto;font-size:12px;color:var(--muted);padding-top:6px}

/* detail */
.detail{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;padding-block:36px 56px;align-items:start}
.detail .thumb{border-radius:var(--radius)}
.buybox{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:24px;display:grid;gap:14px}
.buybox h1{font-size:clamp(24px,3vw,32px)}
.buybox .fullname{font-size:13px;color:var(--muted);margin-top:-6px}
.buybox .actions{display:grid;gap:8px}
.buybox .note{font-size:12px;color:var(--muted);line-height:1.7}
.spec{width:100%;border-collapse:collapse;font-size:14px}
.spec th,.spec td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.spec th{width:34%;color:var(--muted);font-weight:500;background:var(--surface-2)}
.spec-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface)}
.spec-wrap .spec tr:last-child th,.spec-wrap .spec tr:last-child td{border-bottom:0}
.prose{max-width:44em}
.prose p + p{margin-top:12px}
.feats{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.feat{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px}
.feat h3{font-size:17px;margin-bottom:8px}
.feat p{font-size:14px;color:var(--muted)}
.flow{display:grid;grid-template-columns:repeat(4,1fr);gap:0;counter-reset:f}
.flow li{list-style:none;position:relative;padding:18px 20px 18px 20px;background:var(--surface);border:1px solid var(--line);margin-left:-1px}
.flow li:first-child{border-radius:var(--radius) 0 0 var(--radius);margin-left:0}
.flow li:last-child{border-radius:0 var(--radius) var(--radius) 0;border-color:var(--gold);background:var(--gold-soft)}
.flow b{display:block;font-size:15px}
.flow span{font-size:13px;color:var(--muted);line-height:1.6;display:block;margin-top:4px}
.flow .k{font-family:var(--mono);font-size:11px;color:var(--gold-ink);letter-spacing:.08em}
.faq{display:grid;gap:10px;max-width:52em}
.faq details{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:0 18px}
.faq summary{cursor:pointer;padding:14px 0;font-weight:700;list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";font-family:var(--mono);color:var(--gold-ink)}
.faq details[open] summary::after{content:"−"}
.faq summary::-webkit-details-marker{display:none}
.faq details p{padding-bottom:16px;font-size:14px;color:var(--muted)}
.alert{background:var(--warn-soft);color:var(--ink);border-radius:var(--radius);padding:16px 18px;font-size:13.5px;line-height:1.8}
.alert b{color:var(--warn)}

/* beginners */
.steps{display:grid;gap:0;counter-reset:s;max-width:52em}
.steps li{list-style:none;display:grid;grid-template-columns:44px 1fr;gap:16px;padding-bottom:26px;position:relative}
.steps li::before{counter-increment:s;content:counter(s);width:36px;height:36px;border-radius:50%;background:var(--gold);color:var(--on-gold);display:grid;place-items:center;font-family:var(--mono);font-weight:600;font-size:14px}
.steps li:not(:last-child)::after{content:"";position:absolute;left:17px;top:40px;bottom:4px;width:2px;background:var(--line)}
.steps b{display:block;font-size:16px;margin-top:4px}
.steps p{font-size:14px;color:var(--muted);margin-top:4px}
.steps code{font-family:var(--mono);font-size:12.5px;background:var(--surface-2);padding:1px 6px;border-radius:3px;color:var(--ink)}
.needs{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.cmp .box{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px}
.cmp h3{font-size:18px;margin-bottom:6px}
.cmp p{font-size:13.5px;color:var(--muted)}
.tbl{overflow-x:auto;margin-top:14px}
.tbl table{border-collapse:collapse;width:100%;min-width:440px;font-size:13px}
.tbl th,.tbl td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}
.tbl th{font-size:12px;color:var(--muted);font-weight:700}
.slot{display:inline-block;font-size:11px;color:var(--gold-ink);border:1px dashed var(--gold);padding:1px 8px;border-radius:3px;white-space:nowrap}

/* about / legal */
.dl{display:grid;grid-template-columns:9em 1fr;gap:0;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);max-width:52em}
.dl dt,.dl dd{margin:0;padding:14px 16px;border-bottom:1px solid var(--line);font-size:14px}
.dl dt{color:var(--muted);background:var(--surface-2)}
.dl dt:last-of-type,.dl dd:last-of-type{border-bottom:0}
.legal{max-width:46em;display:grid;gap:40px}
.legal h2{font-size:22px;margin-bottom:12px}
.legal p,.legal li{font-size:14.5px}
.legal ul,.legal ol{padding-left:1.3em;margin:8px 0 0;display:grid;gap:6px}
.legal p + p{margin-top:10px}

.about-brand{display:grid;grid-template-columns:200px 1fr;gap:28px;align-items:center;max-width:52em}
.about-brand img{width:100%;height:auto;border-radius:12px;display:block}
@media (max-width:520px){.about-brand{grid-template-columns:1fr}.about-brand img{max-width:220px}}
.thumb img{display:block;width:100%;height:100%;object-fit:cover}
.banner{margin:0}
.banner img{display:block;width:100%;height:auto;border-radius:var(--radius)}
.banner figcaption{font-size:12px;color:var(--muted);margin-top:8px;line-height:1.7}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;display:grid;gap:2px}
.s-label{font-size:12.5px;color:var(--muted)}
.s-val{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:clamp(24px,3vw,30px);font-weight:600;line-height:1.3}
.s-val small{font-size:.5em;margin-left:3px;color:var(--muted);font-weight:400}
.s-sub{font-size:12px;color:var(--muted);line-height:1.6}
@media (max-width:860px){.stats{grid-template-columns:repeat(2,1fr)}}
@media (max-width:420px){.stats{grid-template-columns:1fr}}
.hero-band{background:radial-gradient(ellipse 60% 70% at 78% 45%,rgba(212,164,69,.16),transparent 70%),linear-gradient(180deg,#0B0D12 0%,#0A0B0D 100%);border-bottom:1px solid var(--line);overflow:hidden}
.hero-band .hero{grid-template-columns:1.1fr .9fr;padding-block:64px 72px}
.hero-eyebrow{display:flex;align-items:center;gap:12px;font-family:var(--mono);font-size:12px;letter-spacing:.24em;color:var(--gold-ink)}
.hero-eyebrow span{display:inline-block;width:32px;height:2px;background:var(--gold)}
.hero-band h1{font-size:clamp(34px,5.2vw,64px);line-height:1.22;color:#F4F0E6}
.hero-band h1 em{background:linear-gradient(180deg,#F6D98C 0%,#D9A84A 55%,#A87A22 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero-band .lead{color:#BDB6A6;font-size:16px}
.hero-stats{display:flex;gap:36px;flex-wrap:wrap;margin-top:36px;padding-top:24px;border-top:1px solid var(--line)}
.hero-stats b{display:block;font-family:var(--serif);font-size:28px;color:var(--gold-ink);line-height:1.2}
.hero-stats span{font-size:12.5px;color:var(--muted)}
.hero-logo{position:relative;display:grid;place-items:center}
.hero-logo::before{content:"";position:absolute;inset:6%;border-radius:50%;background:radial-gradient(circle,rgba(230,188,104,.35),transparent 65%);filter:blur(30px)}
.hero-logo img{position:relative;width:min(100%,460px);height:auto;display:block;mix-blend-mode:lighten}
.feature-wide{display:grid;grid-template-columns:1.15fr .85fr;gap:0;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.feature-wide:hover{border-color:var(--gold)}
.feature-wide img{width:100%;height:100%;object-fit:cover;display:block}
.fw-body{padding:24px 26px;display:grid;gap:10px;align-content:start}
.fw-body h3{font-size:26px}
.fw-sub{font-size:13px;color:var(--muted);margin-top:-6px}
.fw-body p{font-size:14px}
.fw-stats{display:flex;gap:24px;margin:4px 0 0;flex-wrap:wrap}
.fw-stats dt{font-size:11.5px;color:var(--muted)}
.fw-stats dd{margin:0;font-family:var(--mono);font-size:22px;font-weight:600;color:var(--gold-ink)}
.fw-note{font-size:11.5px !important;color:var(--muted);line-height:1.6}
@media (max-width:860px){.hero-band .hero{grid-template-columns:1fr}.hero-logo{order:-1}.hero-logo img{width:min(70%,320px)}.feature-wide{grid-template-columns:1fr}}
.grp + .grp{margin-top:44px}
.grp-h{font-size:22px;margin-bottom:16px;display:flex;align-items:center;gap:12px}
.grp-h::after{content:"";flex:1;height:1px;background:var(--line)}
.st-free{background:#123A2A;color:#6FE0A8}
.free-band{display:grid;grid-template-columns:1.1fr .9fr;gap:0;background:linear-gradient(135deg,#12261D,#0E1114);border:1px solid #2A5A44;border-radius:var(--radius);overflow:hidden;text-decoration:none;color:inherit}

.free-band img{width:100%;height:100%;object-fit:cover;display:block}
.free-band .fb{padding:26px 28px;display:grid;gap:10px;align-content:center}
.free-band h3{font-size:24px}
.free-band p{font-size:14px;color:#BDB6A6}
.fb-list{list-style:none;margin:4px 0 0;padding:0;display:grid;gap:8px}
.fb-list a{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:10px 14px;border:1px solid #2A5A44;border-radius:10px;text-decoration:none;color:inherit;background:rgba(0,0,0,.25)}
.fb-list a:hover{border-color:#6FE0A8}
.fb-list b{font-family:'JetBrains Mono',monospace;font-size:13px;color:#ECEDEA}
.fb-list span{font-size:12.5px;color:#9FD9BC}
.fb-list a::after{content:"→";color:#6FE0A8}
.dl-box{background:var(--surface);border:1px solid #2A5A44;border-radius:var(--radius);padding:24px;display:grid;gap:14px}
.dl-box .btn-dl{background:linear-gradient(180deg,#5FD39A,#2E9E6E);border-color:#2E9E6E;color:#07140D;font-size:16px;padding:14px 22px}
.dl-box .terms{font-size:12px;color:var(--muted);line-height:1.7}
.dl-box .terms li{margin-bottom:2px}
.label-demo{font-family:var(--mono);background:#07080A;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;color:#FF6A3D;font-size:14px;overflow-x:auto;white-space:nowrap}
.shot{margin:0}
.shot img{display:block;width:100%;height:auto;border-radius:var(--radius);border:1px solid var(--line)}
.shot figcaption{font-size:12px;color:var(--muted);margin-top:8px}
@media (max-width:860px){.free-band{grid-template-columns:1fr}}
/* footer */
.site-footer{border-top:1px solid var(--line);background:var(--surface);margin-top:24px}
.ft{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:32px;padding-block:44px 28px}
.ft h4{font-family:var(--sans);font-size:13px;margin-bottom:10px}
.ft ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.ft a{font-size:13px;color:var(--muted);text-decoration:none}
.ft a:hover{color:var(--ink);text-decoration:underline}
.ft .about-ft p{font-size:13px;color:var(--muted);margin-top:10px;max-width:24em}
.ft-bottom{border-top:1px solid var(--line);padding-block:18px;font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.risk{font-size:12px;color:var(--muted);line-height:1.7;padding-bottom:20px}

@media (max-width:1000px){
  .grid{grid-template-columns:repeat(3,1fr)}
}
@media (max-width:860px){
  .hero,.detail{grid-template-columns:1fr;gap:32px}
  .entries,.policy,.posts,.feats,.needs{grid-template-columns:1fr}
  .grid{grid-template-columns:repeat(2,1fr)}
  .cmp{grid-template-columns:1fr}
  .flow{grid-template-columns:1fr}
  .flow li{margin-left:0;margin-top:-1px}
  .flow li:first-child{border-radius:var(--radius) var(--radius) 0 0;margin-top:0}
  .flow li:last-child{border-radius:0 0 var(--radius) var(--radius)}
  .ft{grid-template-columns:1fr 1fr}
  .ft .about-ft{grid-column:1/-1}
  .section{padding-block:48px}
}
@media (max-width:520px){
  .grid{grid-template-columns:1fr}
  .dl{grid-template-columns:1fr}
  .dl dt{border-bottom:0;padding-bottom:4px}
  .dl dd{padding-top:4px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}

/* ---------- EA講座 ---------- */
:root{--s-is:#5E8FCC;--s-oos:#B88A30}
.course-intro{display:grid;grid-template-columns:1.3fr .7fr;gap:40px;align-items:start}
.course-intro .prose p{font-size:15.5px}
.promise{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px 22px}
.promise h3{font-family:var(--sans);font-size:14px;margin-bottom:10px}
.promise ul{margin:0;padding-left:1.1em;display:grid;gap:6px;font-size:13.5px;color:var(--muted)}
.toc-meta{display:flex;gap:18px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin-top:18px}
.toc-meta b{color:var(--ink);font-family:var(--mono);font-variant-numeric:tabular-nums}
.part{display:grid;grid-template-columns:220px 1fr;gap:28px;padding-block:28px;border-top:1px solid var(--line)}
.part:first-child{border-top:0;padding-top:0}
.part-h .k{font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;color:var(--gold-ink)}
.part-h h3{font-size:20px;margin-block:4px 6px}
.part-h p{font-size:13px;color:var(--muted);line-height:1.7}
.ch{list-style:none;margin:0;padding:0;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);overflow:hidden}
.ch li{display:grid;grid-template-columns:3em 1fr auto;gap:14px;align-items:center;padding:13px 16px;border-top:1px solid var(--line)}
.ch li:first-child{border-top:0}
.ch .no{font-family:var(--mono);font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
.ch .t b{display:block;font-size:15px;font-weight:700;line-height:1.5}
.ch .t span{display:block;font-size:12.5px;color:var(--muted);line-height:1.6}
.ch li.ready{background:var(--gold-soft)}
.ch li.ready .t b a{text-decoration:none}
.ch li.ready .t b a:hover{text-decoration:underline}
.ch li.ready .no{color:var(--gold-ink)}
.st-read{background:var(--gold);color:var(--on-gold)}
@media (max-width:860px){
  .course-intro,.part{grid-template-columns:1fr;gap:16px}
  .ch li{grid-template-columns:2.4em 1fr;}
  .ch li .chip{grid-column:2;justify-self:start}
}

.post-link{text-decoration:none;color:inherit}
.post-link:hover{border-color:var(--gold)}
.post-link .soon{color:var(--gold-ink);font-weight:700}
.jump{font-size:13px;padding:6px 14px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);text-decoration:none}
.jump:hover{border-color:var(--gold)}
.data-note{font-size:13px;color:var(--muted);background:var(--surface-2);border-radius:var(--radius);padding:10px 14px;margin-bottom:18px}
/* ---------- FX入門 図 ---------- */
.chart-svg .d-path{fill:none;stroke:var(--ink);stroke-width:2;stroke-linejoin:round}
.chart-svg .d-up-f{fill:var(--up)}
.chart-svg .d-dn-f{fill:var(--down)}
.chart-svg .d-up-s{stroke:var(--up)}
.chart-svg .d-dn-s{stroke:var(--down)}
.chart-svg .d-lbl{fill:var(--ink);font-size:12px;font-weight:700}
.chart-svg .d-gain{fill:var(--gold-ink);font-size:13px;font-weight:700}
.chart-svg .d-note line{stroke:var(--muted);stroke-width:1;stroke-dasharray:3 3}
.chart-svg .d-note text{fill:var(--ink);font-size:12px}
.chart-svg .d-band{fill:var(--s-is);opacity:.75}
.chart-svg .d-hot{fill:none;stroke:var(--gold);stroke-width:2;stroke-dasharray:5 4}
.next-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-block:16px}
.next-card{display:grid;gap:4px;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px}
.next-card:hover{border-color:var(--gold)}
.next-card .k{font-family:var(--mono);font-size:11px;color:var(--gold-ink);letter-spacing:.1em}
.next-card b{font-size:16px}
.next-card span:last-child{font-size:13.5px;color:var(--muted);line-height:1.7}
.summary{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;margin-top:36px}
.summary h2{font-size:17px !important;margin:0 0 8px !important}
.summary ul{margin:0}
.step-tag{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--gold-ink)}
@media (max-width:640px){.next-grid{grid-template-columns:1fr}}
/* ---------- 記事 ---------- */
.article{max-width:46em;margin-inline:auto;padding-block:40px 24px}
.article .a-head .k{font-family:var(--mono);font-size:12px;color:var(--gold-ink);letter-spacing:.1em}
.article h1{font-size:clamp(25px,3.4vw,34px);margin-block:8px 14px}
.article .a-lead{font-size:16px;color:var(--muted)}
.article .a-meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.article h2{font-size:22px;margin-block:44px 14px;padding-top:4px}
.article h3{font-size:17px;margin-block:26px 8px}
.article p{font-size:15.5px}
.article p + p{margin-top:14px}
.article ul,.article ol{padding-left:1.3em;display:grid;gap:6px;margin:12px 0}
.article li{font-size:15px}
.point{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:0 var(--radius) var(--radius) 0;padding:16px 18px;margin-block:20px;font-size:14.5px}
.point b{display:block;margin-bottom:4px}
.figure{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:18px 18px 12px;margin-block:22px}
.figure .f-title{font-weight:700;font-size:14.5px}
.figure .f-sub{font-size:12.5px;color:var(--muted)}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--muted);margin-block:10px 4px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.chart-svg{display:block;width:100%;height:auto;overflow:visible}
.chart-svg .grid-l{stroke:var(--line);stroke-width:1}
.chart-svg .base-l{stroke:var(--muted);stroke-width:1}
.chart-svg .ref-l{stroke:var(--ink);stroke-width:1.2;stroke-dasharray:5 4}
.chart-svg .ax{fill:var(--muted);font-family:"JetBrains Mono",monospace;font-size:11px}
.chart-svg .cat{fill:var(--ink);font-size:12.5px;font-weight:700}
.chart-svg .cat2{fill:var(--muted);font-size:11.5px}
.chart-svg .val{fill:var(--ink);font-family:"JetBrains Mono",monospace;font-size:11.5px;font-weight:600}
.chart-svg .ref-t{fill:var(--ink);font-size:11px}
.chart-svg .b-is{fill:var(--s-is)}
.chart-svg .b-oos{fill:var(--s-oos)}
.chart-svg .bar{transition:opacity .15s}
.chart-svg g.cg:hover .bar{opacity:.85}
.chart-svg .hit{fill:transparent}
.f-note{font-size:12px;color:var(--muted);margin-top:8px;line-height:1.7}
.data-tbl{overflow-x:auto;margin-block:16px}
.data-tbl table{border-collapse:collapse;width:100%;min-width:460px;font-size:13.5px;background:var(--surface)}
.data-tbl th,.data-tbl td{padding:10px 12px;border:1px solid var(--line);text-align:left}
.data-tbl th{background:var(--surface-2);font-size:12.5px;color:var(--muted);font-weight:700}
.data-tbl td.n{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right}
.data-tbl .ng{color:var(--down)}
.verdict{font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;white-space:nowrap}
.v-ok{background:var(--ok-soft);color:var(--ok)}
.v-ng{background:var(--wip-soft);color:var(--muted)}
.checklist{list-style:none;padding:0 !important}
.checklist li{padding-left:1.8em;position:relative}
.checklist li::before{content:"";position:absolute;left:0;top:.45em;width:13px;height:13px;border:1.5px solid var(--gold);border-radius:3px}
.a-nav{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:48px}
.a-nav a,.a-nav span{display:block;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;text-decoration:none;background:var(--surface);font-size:14px}
.a-nav small{display:block;font-size:11.5px;color:var(--muted)}
.a-nav a:hover{border-color:var(--gold)}
.a-nav .next{text-align:right}
.a-nav span{color:var(--muted)}
"""

JS = r"""
(function(){
  var h=document.querySelector('.site-header'),b=document.querySelector('.menu-btn');
  if(h&&b){b.addEventListener('click',function(){var o=h.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');b.textContent=o?'閉じる':'メニュー';});}
  var f=document.querySelector('.filters');
  if(f){
    var cards=[].slice.call(document.querySelectorAll('[data-type]')),cnt=document.querySelector('.count');
    function apply(v){
      var n=0;
      cards.forEach(function(c){var show=v==='all'||c.dataset.type===v||(v==='sale'&&c.dataset.status==='sale');c.hidden=!show;if(show)n++;});
      if(cnt)cnt.textContent=n+'件の商品';
      [].forEach.call(document.querySelectorAll('.grp'),function(g){g.hidden=!g.querySelector('[data-type]:not([hidden])');});
    }
    f.addEventListener('click',function(e){
      var t=e.target.closest('button');if(!t)return;
      [].forEach.call(f.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===t?'true':'false');});
      apply(t.dataset.f);
    });
    apply('all');
  }
})();
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@600;800'
         '&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap">')

# ------------------------------------------------------------------ チャート風サムネイル（SVG）
def thumb(kind, label="", seed=1, height_ratio=9/16):
    W, H = 320, 180
    rnd = random.Random(seed)
    n = 22
    # 価格系列（上が高値）を種類ごとに作る
    p = []
    v = 100.0
    for i in range(n):
        t = i / (n - 1)
        if kind == "trend":
            drift = -2.2 if i > 8 else (0.8 if i > 5 else -0.4)
        elif kind == "lowfreq":
            drift = -1.0
        elif kind == "breakout":
            drift = 0 if i < 14 else -4.5
        elif kind == "hunt":
            drift = (0.0 if i < 10 else (3.5 if i < 13 else -3.2))
        elif kind == "vwap":
            drift = (-0.3 if i < 8 else -2.4 if i < 15 else 0.9 if i < 17 else -2.0)
        elif kind == "sr":
            drift = 2.6 * (1 if (i // 5) % 2 == 0 else -1)
        elif kind == "dow":
            drift = (-3.4 if (i // 4) % 2 == 0 else 2.0)
        else:
            drift = 0
        v += drift + rnd.uniform(-1.6, 1.6)
        if kind in ("breakout", "hunt") and i < 10:
            v = max(min(v, 108), 96)
        p.append(v)
    lo, hi = min(p) - 6, max(p) + 6
    def y(val):
        return 22 + (val - lo) / (hi - lo) * (H - 44)
    out = []
    for gy in (45, 90, 135):
        out.append(f'<line class="g-line" x1="0" y1="{gy}" x2="{W}" y2="{gy}"/>')
    step = (W - 40) / n
    xs = []
    prev = p[0] + rnd.uniform(-1, 1)
    for i, c in enumerate(p):
        o = prev
        x = 24 + i * step
        xs.append(x)
        top = min(o, c) - rnd.uniform(0.6, 2.6)
        bot = max(o, c) + rnd.uniform(0.6, 2.6)
        cls = "c-up" if c < o else "c-dn"  # 値が小さい＝上
        out.append(f'<line class="{cls}" x1="{x:.1f}" x2="{x:.1f}" y1="{y(top):.1f}" y2="{y(bot):.1f}" stroke-width="1.2"/>')
        bh = max(2, abs(y(c) - y(o)))
        out.append(f'<rect class="{cls}" x="{x-4.5:.1f}" y="{min(y(o),y(c)):.1f}" width="9" height="{bh:.1f}" rx="1" stroke-width="0"/>')
        prev = c
    # オーバーレイ
    if kind in ("trend", "lowfreq"):
        pts = []
        for i, c in enumerate(p):
            off = 7 if i > 8 else -7 if kind == "trend" and i < 6 else 7
            pts.append(f"{xs[i]:.1f},{y(c+off):.1f}")
        out.append(f'<polyline class="o-gold" points="{" ".join(pts)}"/>')
        k = 8 if kind == "trend" else 12
        out.append(f'<circle class="o-dot" cx="{xs[k]:.1f}" cy="{y(p[k]+7):.1f}" r="4"/>')
    elif kind == "breakout":
        bt, bb = y(min(p[:13]) - 1.5), y(max(p[:13]) + 1.5)
        out.append(f'<rect class="o-box" x="{xs[0]-8:.1f}" y="{bt:.1f}" width="{xs[13]-xs[0]+16:.1f}" height="{bb-bt:.1f}"/>')
        out.append(f'<circle class="o-dot" cx="{xs[15]:.1f}" cy="{bt:.1f}" r="4"/>')
    elif kind == "hunt":
        bt, bb = y(min(p[:10]) - 1), y(max(p[:10]) + 1)
        out.append(f'<rect class="o-box" x="{xs[0]-8:.1f}" y="{bt:.1f}" width="{xs[10]-xs[0]+16:.1f}" height="{bb-bt:.1f}"/>')
        k = max(range(10, 14), key=lambda i: p[i])
        out.append(f'<circle class="o-dot" cx="{xs[k]:.1f}" cy="{y(p[k]+3):.1f}" r="4"/>')
    elif kind == "vwap":
        acc, pts = 0, []
        for i, c in enumerate(p):
            acc += c
            pts.append(f"{xs[i]:.1f},{y(acc/(i+1)):.1f}")
        out.append(f'<polyline class="o-gold" points="{" ".join(pts)}"/>')
    elif kind == "sr":
        for val in (min(p) + 1, max(p) - 1):
            out.append(f'<line class="o-lvl" x1="0" x2="{W}" y1="{y(val):.1f}" y2="{y(val):.1f}"/>')
        out.append(f'<text class="o-txt" x="{W-58}" y="{y(min(p)+1)-5:.1f}">×4 *2</text>')
    elif kind == "dow":
        hi_idx = [i for i in range(1, n - 1) if p[i] < p[i-1] and p[i] <= p[i+1]]
        lo_idx = [i for i in range(1, n - 1) if p[i] > p[i-1] and p[i] >= p[i+1]]
        for i in hi_idx[-3:]:
            out.append(f'<text class="o-txt" x="{xs[i]-8:.1f}" y="{y(p[i])-12:.1f}">HH</text>')
        for i in lo_idx[-3:]:
            out.append(f'<text class="o-txt" x="{xs[i]-8:.1f}" y="{y(p[i])+20:.1f}">HL</text>')
    svg = f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{"".join(out)}</svg>'
    lab = f'<span class="t-label">{html.escape(label)}</span>' if label else ""
    return f'<span class="thumb">{svg}{lab}</span>'

# ------------------------------------------------------------------ 商品データ
STATUS = {"free": ("無料公開", "st-free"), "sale": ("販売中", "st-sale"), "fwd": ("デモでフォワード検証中", "st-fwd"),
          "prep": ("準備中", "st-prep"), "dev": ("開発中", "st-dev")}
PRODUCTS = [
    dict(id="tengan", name="天眼金龍", sub="TripleMA-ASTシステム【ゴールド専用】", type="ea", status="sale",
         sym="XAUUSD", tf="H1", kind="trend", seed=7, detail="tengan-kinryu.html", url=GGJ_URL,
         desc="TripleMAとSuperTrendの二重フィルターで、上昇はロング、下降はショートでトレンドに乗るEAです。", img="tengan-card.jpg"),
    dict(id="lh", name="LiquidityHunter GOLD", sub="ボックス × 流動性狩り × 反発", type="ea", status="fwd",
         sym="XAUUSD", tf="M5", kind="hunt", seed=3,
         desc="レンジの下抜けで損切りを巻き込んだあとの反発を狙うEAです。デモ口座でフォワード検証を続けています。"),
    dict(id="lh-btc", name="LiquidityHunter BTCUSD", sub="ビットコイン版", type="ea", status="fwd",
         sym="BTCUSD", tf="M5", kind="hunt", seed=8,
         desc="同じ流動性狩りのロジックを、値動きの大きいビットコインに合わせて調整した版です。"),
    dict(id="lh-nk", name="LiquidityHunter NIKKEI225", sub="日経225版", type="ea", status="fwd",
         sym="NIKKEI225", tf="M5", kind="hunt", seed=14,
         desc="日経225向けに調整した版です。3銘柄の中で、期間を分けた検証の結果が最も安定していました。"),
    dict(id="junbari", name="順バリ王", sub="アジア時間VWAP × 欧州・NY順張り", type="ea", status="fwd",
         sym="XAUUSD", tf="M15", kind="vwap", seed=11,
         desc="アジア時間のVWAPの形からその日の方向を判定し、欧州・NY時間の押し目と戻りを狙います。"),
    dict(id="lowadx", name="LowADX Breakout", sub="低ADXからのチャネルブレイク", type="ea", status="fwd",
         sym="XAUUSD", tf="H1", kind="breakout", seed=5,
         desc="ADXが低い静かな相場から、20本の高値・安値を抜けた方向へ順張りでついていくEAです。"),
    dict(id="tengan-vis", name="天眼金龍 Visualizer", sub="天眼金龍のシグナル表示インジケーター", type="ind", status="prep",
         sym="XAUUSD", tf="H1", kind="trend", seed=41,
         desc="天眼金龍と同じ判定で、SuperTrendの転換とエントリー条件をチャート上に表示します。EAの動きを目で確認したい方や、裁量トレードの補助に。"),
    dict(id="lh-vis", name="LiquidityHunter Visualizer", sub="流動性狩りの検出インジケーター", type="ind", status="prep",
         sym="XAUUSD・BTCUSD", tf="M5", kind="hunt", seed=43,
         desc="LiquidityHunterと同じロジックで、レンジのボックス、損切りを巻き込んだ下抜け、反発のサインを発注なしで表示します。"),
    dict(id="lowadx-vis", name="LowADX Breakout インジケーター", sub="低ADXブレイクアウトの確認用", type="ind", status="prep",
         sym="XAUUSD", tf="H1", kind="breakout", seed=47,
         desc="ADXが低い状態と20本の高値・安値のチャネルを表示し、ブレイクアウトの候補をチャート上で確認できます。"),
    dict(id="sr", name="SR_AutoLevels", sub="サポレジ自動描画インジケーター", type="ind", status="free",
         sym="MULTI", tf="H1・H4・D1", kind="sr", seed=17, detail="sr-autolevels.html", img="sr-card.jpg",
         desc="重要なサポート・レジスタンスを自動で引き、タッチ回数と出来高スパイクの実績をラベルで表示します。H1・H4・日足を重ねて表示。"),
    dict(id="dow", name="Million_DowTrend", sub="ダウ理論トレンド判定", type="ind", status="free",
         sym="MULTI", tf="ALL", kind="dow", seed=29, detail="dow-trend.html", img="dow-card.jpg",
         desc="高値・安値の切り上げと切り下げを自動判定し、トレンドの継続と転換をチャート上に表示します。H1・H4・日足のトレンドを一覧で確認できます。"),
    dict(id="ob", name="Million_OrderBlock", sub="オーダーブロック自動検出", type="ind", status="free",
         sym="MULTI", tf="ALL", kind="sr", seed=31, detail="order-block.html", img="ob-card.jpg",
         desc="強い値動きが始まった場所（オーダーブロック）を自動で見つけて箱で表示し、価格が抜けたら消します。上位足のOBも重ねて表示。"),
]

def pcard(p):
    st, cls = STATUS[p["status"]]
    tlabel = ("EA" if p["type"] == "ea" else "INDICATOR") + f" / {p['sym']} {p['tf']}"
    name_html = f'<a href="{p["detail"]}">{p["name"]}</a>' if p.get("detail") else p["name"]
    if p["status"] == "sale" and p.get("detail"):
        act = f'<a class="btn btn-primary btn-sm" href="{p["detail"]}">詳細を見る</a>'
    elif p["status"] == "free" and p.get("detail"):
        act = f'<a class="btn btn-primary btn-sm" href="{p["detail"]}">無料でダウンロード</a>'
    else:
        act = '<span class="btn btn-sm" aria-disabled="true">公開までお待ちください</span>'
    typ = "EA" if p["type"] == "ea" else "インジケーター"
    tags = f'<span class="tag">{p["sym"]}</span><span class="tag">{p["tf"]}</span><span class="tag">MT5</span>'
    t = (f'<span class="thumb"><img src="{p["img"]}" alt="{p["name"]}のバナー" loading="lazy" width="800" height="450"></span>'
         if p.get("img") else thumb(p["kind"], tlabel, p["seed"]))
    if p.get("detail"):
        t = f'<a href="{p["detail"]}" tabindex="-1" aria-hidden="true">{t}</a>'
    return f'''<article class="pcard" data-type="{p["type"]}" data-status="{p["status"]}">
  {t}
  <div class="pb">
    <div class="row"><span class="chip {cls}">{st}</span><span class="tag">{typ}</span></div>
    <h3>{name_html}</h3>
    <p class="sub">{p["sub"]}</p>
    <p class="sub">{p["desc"]}</p>
    <div class="row">{tags}</div>
    <div class="pact">{act}</div>
  </div>
</article>'''

# ------------------------------------------------------------------ 共通パーツ
LOGO_SVG = ('<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true">'
            '<line x1="5" y1="3" x2="5" y2="17" stroke="#D9A84A" stroke-width="1.4"/><rect x="2.5" y="6" width="5" height="7" fill="#D9A84A"/>'
            '<line x1="14" y1="2" x2="14" y2="14" stroke="#D9A84A" stroke-width="1.4"/><rect x="11.5" y="4" width="5" height="6" fill="#D9A84A"/></svg>')

NAV = [("./", "home", "ホーム"), ("fx-basics.html", "fx", "FX入門"), ("course.html", "course", "EA講座"),
       ("products.html", "products", "商品一覧"), ("blog.html", "blog", "コラム"), ("about.html", "about", "運営者")]

def header(active):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}"{cur if key == active else ""}>{label}</a>' for href, key, label in NAV)
    return f'''<div class="prbar">当サイトはアフィリエイト広告（PR）を含みます。掲載しているEA・インジケーターは利益を保証するものではありません。</div>
<header class="site-header">
  <div class="wrap hd">
    <a class="logo" href="./"><img class="logo-mark" src="logo-mark.png" alt="" width="36" height="36"><span><b>さうざーFX</b><small>GOLD EA LAB</small></span></a>
    <button class="menu-btn" type="button" aria-expanded="false">メニュー</button>
    <nav class="gnav" aria-label="メインメニュー">{links}<a class="nav-x" href="{X_URL}" target="_blank" rel="noopener">X @alex767_fx</a></nav>
  </div>
</header>'''

FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="ft">
      <div class="about-ft">
        <a class="logo" href="./"><img class="logo-mark" src="logo-mark.png" alt="" width="36" height="36"><span><b>さうざーFX</b><small>GOLD EA LAB</small></span></a>
        <p>XAUUSD（ゴールド）を中心に、EAとインジケーターを開発しています。</p>
      </div>
      <div><h4>商品</h4><ul>
        <li><a href="products.html">商品一覧</a></li>
        <li><a href="tengan-kinryu.html">天眼金龍</a></li>
        <li><a href="products.html#indicators">インジケーター</a></li></ul></div>
      <div><h4>サポート</h4><ul>
        <li><a href="fx-basics.html">FX入門</a></li>
        <li><a href="course.html">EA講座</a></li>
        <li><a href="beginners.html">EAの導入手順</a></li>
        <li><a href="blog.html">コラム</a></li>
        <li><a href="about.html">運営者情報</a></li></ul></div>
      <div><h4>規約・ポリシー</h4><ul>
        <li><a href="legal.html#disclaimer">免責事項</a></li>
        <li><a href="legal.html#ad">広告の表記について</a></li>
        <li><a href="legal.html#privacy">プライバシーポリシー</a></li></ul></div>
    </div>
    <p class="risk">FX・CFD取引は元本を超える損失が生じる可能性があります。掲載しているバックテストや運用実績は過去のもので、将来の成果を保証するものではありません。取引はご自身の判断と責任で行ってください。</p>
    <div class="ft-bottom"><span>© 2026 さうざーFX</span><span>当サイトの文章・画像の無断転載を禁じます</span></div>
  </div>
</footer>'''

def page(title, desc, active, body, full=True):
    og_img = f'<meta property="og:image" content="{SITE_URL}/og-image.jpg">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:site" content="@alex767_fx">\n' if SITE_URL else ""
    head = (f'<title>{title}</title>\n<meta name="description" content="{html.escape(desc)}">\n'
            f'<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
            f'<meta property="og:title" content="{html.escape(title)}">\n<meta property="og:description" content="{html.escape(desc)}">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="さうざーFX">\n{og_img}'
            f'{FONTS}\n<style>{CSS}</style>\n')
    content = f'{header(active)}\n<main>\n{body}\n</main>\n{FOOTER}\n<script>{JS}</script>\n'
    if not full:
        return head + content
    return ('<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + content + '</body>\n</html>\n')

def page_head(crumbs, h1, lead):
    cr = ' <span aria-hidden="true">/</span> '.join(
        [f'<a href="{h}">{t}</a>' for h, t in crumbs[:-1]] + [f'<span>{crumbs[-1][1]}</span>'])
    return f'''<div class="page-head"><div class="wrap">
  <nav class="crumb" aria-label="パンくずリスト">{cr}</nav>
  <h1>{h1}</h1>
  <p>{lead}</p>
</div></div>'''

ICON_BOOK = '<svg viewBox="0 0 24 24"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/><path d="M9 7h6"/></svg>'
ICON_GRID = '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>'
ICON_PEN = '<svg viewBox="0 0 24 24"><path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/></svg>'

EA_COLS = [
    ("col-quick-sl.html", "時間分析", "エントリー直後の3時間が一番危ない", "損切りの38%は、エントリーから3時間以内に発生していました。危ない時間帯と、そのときの向き合い方を解説します。"),
    ("col-losing-streak.html", "連敗分析", "12連敗しても破産しない設計", "バックテストで記録された最大12連敗。それでも口座が残った理由を、ロットと損切りの設計から説明します。"),
    ("col-signal.html", "シグナル分析", "ST転換とMAクロス、2つのシグナルを比較", "211トレードのデータで、2種類のエントリーシグナルの成績を比べました。"),
    ("col-yearly.html", "年別分析", "このEAは2024年から本番だった", "2022年はTP決済が1件もありませんでした。それでも4年間で利益が残った理由を、年別に分解します。"),
    ("col-weekday.html", "曜日分析", "木曜が最強、金曜が最弱？", "211トレードを曜日別に集計すると、思った以上にはっきりした差が出ました。"),
    ("col-hold-time.html", "保有時間", "勝ちトレードは長く持つ", "勝ちトレードと負けトレードでは、ポジションを持っている時間に大きな差がありました。"),
    ("col-volatility-lot.html", "ボラティリティ", "ゴールドの値幅が約6倍に。ロットを見直す理由", "4年分のSL幅を年別に並べると、ゴールドの値動きが大きく広がっていることが分かります。"),
    ("col-advanced.html", "運用設定", "1ポジvs2ポジ、固定ロットvsAutoLot", "ポジション数とロット管理の組み合わせ4パターンを、4年分のデータで比べました。"),
    ("col-tradelog.html", "ロジック", "トレードログを徹底分析", "211トレードから見えた、フィボナッチとの関係と損益の法則をまとめます。"),
    ("col-ict-fibo-atr.html", "ロジック", "EAのSL・TPはICTのフィボと一致していた", "EAが自動で決めるSLとTPの位置を、ICT手法のキーレベルと比べました。"),
    ("col-entry-story.html", "実例", "EAが自動で掴んだ絶好のエントリー", "2026年4月8日のエントリーでは、ICT・フィボナッチ・ATRの3つが一致していました。"),
    ("col-discretionary.html", "裁量活用", "天眼インジを裁量トレードに活用する", "M15の先行シグナルと、フィボナッチの押し目を組み合わせる方法を紹介します。"),
    ("col-prospect.html", "行動経済学", "FXで勝てない本当の理由", "プロスペクト理論から、裁量トレードで陥りやすい5つの罠と、EAで避けられる理由を解説します。"),
]
BASICS = [
    ("basics-1.html", "海外FXとは？国内FXとの違い", "FXの基本と、国内FX・海外FXの仕組みの違い"),
    ("basics-2.html", "ゴールド（XAUUSD）の特徴", "価格を動かす要因、取引時間帯、通貨ペアとの違い"),
    ("basics-3.html", "MT5の使い方", "インストールから、チャート・インジケーター・EAの設置まで"),
    ("basics-4.html", "レバレッジ・ロット・証拠金の計算", "何ロットで入ればよいかを自分で計算できるようにする"),
    ("basics-5.html", "ゼロカットとは", "追証なしの仕組みと、国内FXの追証リスクとの比較"),
    ("basics-6.html", "EA（自動売買）入門", "裁量トレードとの違いと、バックテストの読み方"),
    ("basics-7.html", "Vantage口座開設ガイド", "口座開設からMT5の設定、EAの稼働まで"),
]

def post_card(cat, title, desc, href=None):
    if href:
        return f'''<a class="post post-link" href="{href}">
  <div class="meta"><span class="tag">{cat}</span></div>
  <h3>{title}</h3>
  <p>{desc}</p>
  <p class="soon">読む →</p>
</a>'''
    return f'''<article class="post">
  <div class="meta"><span class="tag">{cat}</span></div>
  <h3>{title}</h3>
  <p>{desc}</p>
  <p class="soon">公開準備中</p>
</article>'''

# ------------------------------------------------------------------ 各ページ
def index_body():
    t = PRODUCTS[0]
    pick = "".join(pcard(p) for p in PRODUCTS[1:5])
    return f'''<div class="hero-band">
<div class="wrap hero">
  <div>
    <div class="hero-eyebrow"><span></span>SAUZER FX — GOLD EA LAB</div>
    <h1>ゴールドを、<br><em>検証し尽くして</em><br>自動売買にする。</h1>
    <p class="lead">XAUUSD（ゴールド）を中心に、MT5のEAとインジケーターを開発しています。期間を分けたテストでも優位性が残ったロジックだけを製品にしています。FXをいちばん最初から学べる入門講座も公開しています。</p>
    <div class="cta">
      <a class="btn btn-primary" href="products.html">商品を見る →</a>
      <a class="btn btn-ghost" href="fx-basics.html">FXを一から学ぶ</a>
    </div>
    <div class="hero-stats">
      <div><b>3銘柄</b><span>ゴールド・BTC・日経225</span></div>
      <div><b>MT5</b><span>すべての商品が対応</span></div>
      <div><b>全15章</b><span>初心者向けFX入門</span></div>
    </div>
  </div>
  <div class="hero-logo"><img src="logo.jpg" alt="さうざーFX（SAUZER FX）のロゴ" width="640" height="640"></div>
</div>
</div>

<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <div class="free-band">
      <img src="ob-card.jpg" alt="SR_AutoLevels・Million_DowTrend・Million_OrderBlockを同時に表示したゴールドのチャート" width="800" height="448">
      <div class="fb">
        <span class="chip st-free" style="justify-self:start">無料公開中</span>
        <h3>MT5インジケーター 3種</h3>
        <p>トレンド、節目、注文が集まった場所。チャートを読むための3つのインジケーターを、登録不要・無料で配布しています。</p>
        <ul class="fb-list">
          <li><a href="sr-autolevels.html"><b>SR_AutoLevels</b><span>サポレジを自動で引く</span></a></li>
          <li><a href="dow-trend.html"><b>Million_DowTrend</b><span>ダウ理論でトレンドを判定</span></a></li>
          <li><a href="order-block.html"><b>Million_OrderBlock</b><span>オーダーブロックを自動検出</span></a></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section feature-sec">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Featured</div><h2>販売中のEA</h2></div><a class="more-link" href="products.html">すべての商品を見る →</a></div>
    <a class="feature-wide" href="tengan-kinryu.html">
      <img src="tengan-card.jpg" alt="天眼金龍のバナー" width="800" height="450">
      <div class="fw-body">
        <div class="row" style="display:flex;gap:6px;flex-wrap:wrap"><span class="chip st-sale">販売中 ・ v1.4</span><span class="tag">XAUUSD</span><span class="tag">H1</span><span class="tag">MT5</span></div>
        <h3>天眼金龍</h3>
        <p class="fw-sub">TripleMA-ASTシステム【ゴールド専用】</p>
        <p>TripleMAとSuperTrendの二重フィルターで、上昇はロング、下降はショートでトレンドに乗るEAです。</p>
        <dl class="fw-stats"><div><dt>PF</dt><dd>1.72</dd></div><div><dt>最大DD</dt><dd>23.62%</dd></div><div><dt>取引数</dt><dd>271回</dd></div></dl>
        <p class="fw-note">2022年〜2026年9月のバックテスト（固定ロット0.1・初期証拠金100万円）。将来の成果を保証するものではありません。</p>
        <span class="btn btn-primary btn-sm" style="justify-self:start">詳細を見る →</span>
      </div>
    </a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:18px"><div><div class="eyebrow">Learn</div><h2>FXを一から学ぶ</h2></div><p>専門用語は、出てきたその場で説明します。この順番で読み進めてください。</p></div>
    <div class="entries path">
    <a class="entry" href="fx-basics.html"><span class="ico">{ICON_BOOK}</span><b>1. FX入門（全15章）</b><span>FXのしくみ、お金の計算、注文の出し方、損切り、税金まで。まったく初めての方はここから。</span></a>
    <a class="entry" href="course.html"><span class="ico">{ICON_PEN}</span><b>2. EA講座</b><span>自動売買（EA）の選び方、動かし方、成績の読み方を、章ごとに学べます。</span></a>
    <a class="entry" href="products.html"><span class="ico">{ICON_GRID}</span><b>3. 商品一覧</b><span>ゴールド、ビットコイン、日経225のEAとインジケーター。導入手順もあわせて確認できます。</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Products</div><h2>商品ピックアップ</h2></div>
      <a class="more-link" href="products.html">すべての商品を見る →</a>
    </div>
    <div class="grid">{pick}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Indicators</div><h2>インジケーター</h2></div>
      <p>EAと同じロジックをチャート上に表示するインジケーターも準備しています。EAの動きの確認や、裁量トレードの補助に使えます。</p>
    </div>
    <div class="grid">{"".join(pcard(p) for p in PRODUCTS if p["type"] == "ind")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Policy</div><h2>さうざーFXの開発方針</h2></div>
    </div>
    <div class="policy">
      <div><h3>ゴールドが中心</h3><p>主力はXAUUSDです。ほかの銘柄に広げるときは、同じロジックをそのまま使わず、銘柄ごとに検証をやり直します。LiquidityHunterは、ビットコインと日経225にも対応しています。</p></div>
      <div><h3>期間を分けて検証</h3><p>パラメータを決めた期間とは別の期間でもう一度テストし、両方で同じ傾向が出たロジックだけを採用します。片方でしか勝てない手法は製品にしません。</p></div>
      <div><h3>確定足で判断</h3><p>シグナルはローソク足が確定してから判定します。後からサインが消えたり変わったりしないので、バックテストと実運用の差が出にくくなります。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Columns</div><h2>おすすめの記事</h2></div>
      <a class="more-link" href="blog.html">コラム一覧へ →</a>
    </div>
    <div class="posts">{post_card("EA講座", "期間を分けて確かめる", "バックテストの成績が良くても、その期間に合わせただけかもしれません。調整に使っていない期間で確かめる方法です。", "course-oos.html")}{post_card("基礎知識", "ゴールド（XAUUSD）の特徴", "価格を動かす要因と、動きやすい時間帯。通貨ペアとの違いを整理します。", "basics-2.html")}{post_card("基礎知識", "レバレッジ・ロット・証拠金の計算", "何ロットで入ればよいかを、自分で計算できるようにします。", "basics-4.html")}</div>
  </div>
</section>'''

def products_body():
    cards = "".join(pcard(p) for p in PRODUCTS)
    return page_head([("./", "ホーム"), ("", "商品一覧")], "商品一覧",
                     "すべてMT5用です。ゴールド（XAUUSD）を中心に、ビットコインと日経225に対応したEAもあります。購入とダウンロードはGogoJungleで行います。") + f'''
<section class="section" style="padding-top:32px">
  <div class="wrap">
    <div class="filters" role="group" aria-label="商品の絞り込み">
      <button type="button" data-f="all" aria-pressed="true">すべて</button>
      <button type="button" data-f="sale" aria-pressed="false">販売中</button>
      <button type="button" data-f="ea" aria-pressed="false">EA</button>
      <button type="button" data-f="ind" aria-pressed="false">インジケーター</button>
    </div>
    <p class="count">{len(PRODUCTS)}件の商品</p>
    <div class="grp" data-grp="ea"><h2 class="grp-h">EA（自動売買）</h2><div class="grid">{"".join(pcard(p) for p in PRODUCTS if p["type"] == "ea")}</div></div>
    <div class="grp" data-grp="ind" id="indicators"><h2 class="grp-h">インジケーター</h2><div class="grid">{"".join(pcard(p) for p in PRODUCTS if p["type"] == "ind")}</div></div>
  </div>
</section>'''

def tengan_body():
    t = PRODUCTS[0]
    return '''<div class="wrap" style="padding-top:28px"><nav class="crumb" aria-label="パンくずリスト"><a href="./">ホーム</a> <span aria-hidden="true">/</span> <a href="products.html">商品一覧</a> <span aria-hidden="true">/</span> <span>天眼金龍</span></nav></div>''' + f'''
<div class="wrap detail">
  <div style="display:grid;gap:18px">
    <figure class="banner"><img src="tengan-banner.jpg" alt="天眼金龍 TripleMA-ASTシステム【ゴールド専用】のバナー。v1.4バックテスト実績（2022年〜2026年9月）：初期証拠金100万円、総損益+2,458,794円、プロフィットファクター1.72、最大ドローダウン23.62%（証拠金ベース）、取引回数271回" width="1672" height="941"><figcaption>バナーの実績は、固定ロット0.1で行ったv1.4のバックテスト結果です（<a href="#v14-results">詳細</a>）。過去のデータによる結果で、将来の成果を保証するものではありません。</figcaption></figure>
    <div class="spec-wrap"><table class="spec">
      <tr><th>商品名</th><td>天眼金龍 -TripleMA-ASTシステム【ゴールド専用】</td></tr>
      <tr><th>バージョン</th><td class="num">v1.4</td></tr>
      <tr><th>対応銘柄・時間足</th><td>XAUUSD・H1（1時間足）</td></tr>
      <tr><th>プラットフォーム</th><td>MetaTrader 5（MT5対応のブローカー全般）</td></tr>
      <tr><th>取引スタイル</th><td>トレンドフォロー（ロング・ショート両方）。設定でロングのみにも切り替え可能</td></tr>
      <tr><th>エントリー頻度</th><td>月5件程度</td></tr>
      <tr><th>同時保有</th><td>1ポジション（初期設定）</td></tr>
      <tr><th>損切り</th><td>ATR（14）× 1.5 の動的ストップロス</td></tr>
      <tr><th>利益確定</th><td>TP1（損切り幅の2.5倍）で30%を決済し、損切りを建値へ移動。残りはTP2（6倍）まで</td></tr>
      <tr><th>その他の決済</th><td>SuperTrendが反転したら全決済。TP1後24時間たっても決済されない場合は残りを決済</td></tr>
      <tr><th>ロット</th><td>固定ロット（初期0.1）／AutoLot（口座残高の一定%をリスクにする複利運用）</td></tr>
      <tr><th>販売</th><td>GogoJungle（商品ID <span class="num">78813</span>）</td></tr>
    </table></div>
  </div>
  <aside class="buybox">
    <span class="chip st-sale" style="justify-self:start">販売中 ・ v1.4</span>
    <h1 style="font-size:clamp(24px,3vw,32px)">天眼金龍</h1>
    <p class="fullname">TripleMA-ASTシステム【ゴールド専用】</p>
    <p>{t["desc"]}エントリーは月5件程度に絞り、トレンドが出た場面だけを狙います。</p>
    <div class="actions">
      <a class="btn btn-gold" href="{GGJ_URL}" target="_blank" rel="noopener">GogoJungleで購入する</a>
      <a class="btn btn-ghost" href="beginners.html">導入の流れを見る</a>
    </div>
    <p class="note">購入・ダウンロード・お支払いはGogoJungleで行います。価格と最新の成績は販売ページに掲載しています。</p>
  </aside>
</div>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Features</div><h2>3つの特徴</h2></div></div>
    <div class="feats">
      <div class="feat"><h3>トレンドの転換で入る</h3><p>相場の変動幅に合わせて感度が変わるAdaptive SuperTrendを使い、向きが変わったところでエントリーします。上向きならロング、下向きならショートです。</p></div>
      <div class="feat"><h3>3本のMAで方向をそろえる</h3><p>21EMAと50EMAの並び、200EMAに対する価格の位置、短期MAの傾きが、すべてトレンドの向きと一致したときだけ入ります。急すぎる傾きの「高値づかみ」も避けます。</p></div>
      <div class="feat"><h3>利益を残しながら伸ばす</h3><p>損切り幅の2.5倍で30%を利益確定し、残りは損切りを建値に移して6倍まで狙います。トレンドが反転したら、SuperTrendの転換で残りも決済します。</p></div>
    </div>
  </div>
</section>

<section class="section" id="v14-results">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Backtest</div><h2>v1.4のバックテスト結果</h2></div><p>2022年〜現在 ・ XAUUSD H1 ・ 固定ロット0.1 ・ 初期証拠金100万円 ・ MT5ストラテジーテスター（ヒストリー品質99%）</p></div>
    <div class="stats">
      <div class="stat"><span class="s-label">総損益</span><span class="s-val">+2,458,794<small>円</small></span><span class="s-sub">初期証拠金に対して +245.9%</span></div>
      <div class="stat"><span class="s-label">プロフィットファクター</span><span class="s-val">1.72</span><span class="s-sub">総利益 5,876,652円 ÷ 総損失 3,417,858円</span></div>
      <div class="stat"><span class="s-label">最大ドローダウン</span><span class="s-val">22.70<small>%</small></span><span class="s-sub">残高ベース（証拠金ベースは23.62%）</span></div>
      <div class="stat"><span class="s-label">取引数</span><span class="s-val">271</span><span class="s-sub">ロング162回・ショート109回</span></div>
      <div class="stat"><span class="s-label">勝率</span><span class="s-val">32.47<small>%</small></span><span class="s-sub">ロング36.42%・ショート26.61%</span></div>
      <div class="stat"><span class="s-label">平均損益比</span><span class="s-val">3.58</span><span class="s-sub">平均利益 66,780円 ÷ 平均損失 18,677円</span></div>
    </div>

    <div class="prose" style="margin-top:28px">
      <h3 style="font-size:18px;margin-bottom:8px">この結果の読み方</h3>
      <p>勝率は約3割で、10回のうち7回近くは負けます。それでも利益が残るのは、1回の勝ちが負けの約3.6倍あるからです。小さく負けて、トレンドに乗れたときに大きく取る、トレンドフォロー型の典型的な成績です。</p>
      <p>その代わり、負けが続く期間は避けられません。この期間の最大連敗は<b>20回</b>（合計−383,523円）、連続した損失の最大は−634,893円（11回）でした。運用を始めたあとに連敗が続いても慌てないように、この数字を前提に資金とロットを決めてください。</p>
    </div>

    <div class="data-tbl" style="max-width:52em">
      <table style="min-width:0">
        <thead><tr><th>項目</th><th>値</th></tr></thead>
        <tbody>
          <tr><td>リカバリーファクター</td><td class="n">3.72</td></tr>
          <tr><td>シャープレシオ</td><td class="n">2.66</td></tr>
          <tr><td>期待利得（1取引あたり）</td><td class="n">9,073円</td></tr>
          <tr><td>最大の勝ちトレード ／ 負けトレード</td><td class="n">372,640円 ／ −132,001円</td></tr>
          <tr><td>最大連勝 ／ 最大連敗</td><td class="n">4回 ／ 20回</td></tr>
          <tr><td>1か月あたりの取引数</td><td class="n">約4.8回</td></tr>
        </tbody>
      </table>
    </div>

    <figure class="banner" style="margin-top:24px">
      <img src="tengan-v14-report.jpg" alt="MT5ストラテジーテスターのバックテスト結果画面。天眼金龍v1.4、2022年から現在まで" width="1400" height="738" loading="lazy">
      <figcaption>MT5ストラテジーテスターの結果画面。時間帯別の取引で20時（サーバー時間）が0件なのは、初期設定の時間帯除外によるものです。バックテストは過去のデータによる結果で、将来の成果を保証するものではありません。</figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Logic</div><h2>エントリーまでの判定</h2></div><p>1時間足が確定するたびに、次の条件を確認します。</p></div>
    <ol class="flow" style="padding:0;margin:0">
      <li><span class="k">CHECK 1</span><b>SuperTrend転換</b><span>Adaptive SuperTrendの向きが切り替わる（上向きなら買い、下向きなら売り）</span></li>
      <li><span class="k">CHECK 2</span><b>MAの並びと位置</b><span>21EMAと50EMAの並び、200EMAに対する価格の位置が、どちらも同じ向き</span></li>
      <li><span class="k">CHECK 3</span><b>傾きと時間帯</b><span>21EMAの傾きが行き過ぎていない。除外している時間帯ではない</span></li>
      <li><span class="k">ENTRY</span><b>確定足で発注</b><span>損切りとTP2を同時に設定してエントリー</span></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Update</div><h2>v1.4の変更点</h2></div><p>v1.4の検証結果は<a href="#v14-results">このページの上</a>に掲載しています。新しい検証は順次追加します。</p></div>
    <ul class="prose" style="padding-left:1.2em;display:grid;gap:8px;margin:0">
      <li>エントリーを「SuperTrendの転換 × MAの並び」の1つの条件に整理</li>
      <li>MAの傾きフィルターを、ロングとショートで対称に判定するように変更</li>
      <li>値動きが荒れやすい時間帯を除外する設定を追加（初期設定はサーバー時間20時）</li>
      <li>TP1達成後、一定時間たっても決済されない残りポジションを決済する機能を追加</li>
      <li>EAを再起動しても、保有中のポジションの管理を引き継げるように改善</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">FAQ</div><h2>よくある質問</h2></div></div>
    <div class="faq">
      <details><summary>どの口座で使えますか？</summary><p>MT5でXAUUSD（ゴールド）を取引できる口座で動作します。業者によって銘柄名が「XAUUSD」以外になっている場合があるため、詳しい対応条件は販売ページをご確認ください。</p></details>
      <details><summary>最小ロットで使えますか？</summary><p>動作はしますが、最小ロット（多くの口座で0.01lot）では、TP1での一部決済ができず、TP1で全量が決済されます。TP2まで狙う設計を活かすには、最小ロットの2倍以上（0.02lot以上）で運用してください。</p></details>
      <details><summary>ロングだけで運用できますか？</summary><p>できます。パラメータの「LongOnly」をtrueにすると、ショートのエントリーを行いません。</p></details>
      <details><summary>パソコンを付けっぱなしにする必要がありますか？</summary><p>EAはMT5が起動している間だけ動きます。24時間動かすにはVPS（仮想サーバー）の利用をおすすめします。手順は<a href="beginners.html">EAの導入手順</a>で説明しています。</p></details>
      <details><summary>必ず利益が出ますか？</summary><p>いいえ。相場の状況によって連敗や資金の減少が起こります。バックテストは過去のデータでの結果で、将来の成績を保証するものではありません。</p></details>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap"><div class="alert"><b>ご注意</b>　FX・CFD取引は元本を超える損失が生じる可能性があります。EAの利用は、内容とリスクを理解したうえでご自身の判断で行ってください。</div></div>
</section>'''

def beginners_body():
    return page_head([("./", "ホーム"), ("", "EAの導入手順")], "EAの導入手順",
                     "EA（自動売買プログラム）を動かすまでに必要なものと、導入の流れを説明します。FXそのものが初めての方は、先に<a href=\"fx-basics.html\">FX入門</a>をお読みください。") + f'''
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">What is EA</div><h2>EAとは</h2></div></div>
    <div class="prose">
      <p>EA（Expert Advisor）は、MetaTrader（MT4・MT5）上で動く自動売買プログラムです。あらかじめ決めたルールに沿って、エントリー、損切り、利確を自動で行います。</p>
      <p>感情に左右されずにルールどおり取引できる一方で、相場の状況が変わるとルールが合わなくなることもあります。EAを動かしたあとも、定期的に成績を確認することが大切です。</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">You need</div><h2>必要なもの</h2></div></div>
    <div class="needs">
      <div class="feat"><h3>MT5が使えるFX口座</h3><p>ゴールド（XAUUSD）をMT5で取引できる口座が必要です。スプレッドが狭い口座ほど、EAの成績に有利です。</p></div>
      <div class="feat"><h3>VPS（推奨）</h3><p>MT5を24時間動かすための仮想サーバーです。自宅のパソコンを付けっぱなしにする必要がなくなります。</p></div>
      <div class="feat"><h3>EA本体</h3><p>GogoJungleで購入し、ダウンロードしたファイル（.ex5）をMT5に入れて使います。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Steps</div><h2>導入の流れ</h2></div><p>はじめての方でも、この順番で進めれば動かせます。</p></div>
    <ol class="steps" style="padding:0;margin:0">
      <li><div><b>MT5対応の口座を開設する</b><p>ゴールドを取引できるMT5口座を開設し、ログインIDとパスワードを受け取ります。</p></div></li>
      <li><div><b>MT5をインストールしてログインする</b><p>パソコンまたはVPSにMT5をインストールし、開設した口座でログインします。</p></div></li>
      <li><div><b>EAを購入してダウンロードする</b><p>GogoJungleで購入し、マイページからEAのファイルをダウンロードします。</p></div></li>
      <li><div><b>EAをMT5のフォルダに入れる</b><p>MT5の「ファイル」→「データフォルダを開く」から <code>MQL5\\Experts</code> にファイルを置き、MT5を再起動します。</p></div></li>
      <li><div><b>XAUUSDのH1チャートにセットする</b><p>XAUUSDの1時間足チャートを開き、EAをドラッグして設定を確認します。ツールバーの「アルゴ取引」をオンにすれば稼働します。</p></div></li>
    </ol>
  </div>
</section>

<section class="section" id="accounts">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Setup</div><h2>口座とVPSの選び方</h2></div><p>表の内容は掲載時点のものです。最新の条件は各社の公式サイトでご確認ください。</p></div>
    <div class="cmp">
      <div class="box">
        <h3>MT5が使える国内FX口座</h3>
        <p>比べるポイントは、ゴールドのスプレッド、最小取引単位、約定の安定性の3つです。</p>
        <div class="tbl"><table>
          <thead><tr><th>口座</th><th>ゴールド</th><th>最小単位</th><th>申込み</th></tr></thead>
          <tbody>
            <tr><td>口座A</td><td>要確認</td><td class="num">—</td><td><span class="slot">ASPリンク設置枠</span></td></tr>
            <tr><td>口座B</td><td>要確認</td><td class="num">—</td><td><span class="slot">ASPリンク設置枠</span></td></tr>
            <tr><td>口座C</td><td>要確認</td><td class="num">—</td><td><span class="slot">ASPリンク設置枠</span></td></tr>
          </tbody></table></div>
      </div>
      <div class="box">
        <h3>EA用VPS</h3>
        <p>MT5を1〜2つ動かすなら、メモリ2GB前後のWindowsプランが目安です。</p>
        <div class="tbl"><table>
          <thead><tr><th>VPS</th><th>OS</th><th>月額</th><th>申込み</th></tr></thead>
          <tbody>
            <tr><td>VPS A</td><td>Windows</td><td class="num">—</td><td><span class="slot">ASPリンク設置枠</span></td></tr>
            <tr><td>VPS B</td><td>Windows</td><td class="num">—</td><td><span class="slot">ASPリンク設置枠</span></td></tr>
          </tbody></table></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap"><div class="alert"><b>リスクについて</b>　EAを使っても損失が出ることはあります。最初は少ないロットで動かし、動作と成績を確認してから運用額を決めてください。</div></div>
</section>'''

def blog_body():
    rows = "".join(
        f'<li><span class="no">{i:02d}</span><span class="t"><b><a href="{h}" style="text-decoration:none">{t}</a></b><span>{d}</span></span><span class="chip st-read">読めます</span></li>'
        for i, (h, t, d) in enumerate(BASICS, 1))
    return page_head([("./", "ホーム"), ("", "コラム")], "コラム",
                     "FXとゴールドの基礎知識をまとめています。EAの選び方と成績の読み方は、EA講座で順番に解説しています。") + f'''
<section class="section" id="basics">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Basics</div><h2>海外FX基礎知識（全7章）</h2></div>
      <p>FXの基本から、MT5の使い方、EAを動かすまでを順番に解説しています。</p></div>
    <div class="alert" style="margin-bottom:20px"><b>ご注意</b>　海外FX業者の多くは、日本の金融庁に登録していません。トラブルの際に日本の法律で保護されない場合があります。国内口座との違いを理解したうえでご判断ください。</div>
    <ol class="ch">{rows}</ol>
    <div class="posts" style="margin-top:18px">{post_card("海外FX", "海外FXのメリット・デメリット", "税金、レバレッジ、ブローカー選びまで、良い点と注意点を両方まとめています。", "col-kaigai-fx.html")}{post_card("EA講座", "期間を分けて確かめる", "バックテストを調整期間と確認期間に分けて、過剰最適化を見抜く方法を解説します。", "course-oos.html")}</div>
  </div>
</section>'''

def about_body():
    return page_head([("./", "ホーム"), ("", "運営者情報")], "運営者情報",
                     "さうざーFXの運営者と、開発の方針について。") + f'''
<section class="section">
  <div class="wrap" style="display:grid;gap:32px">
    <div class="about-brand"><img src="logo.jpg" alt="さうざーFX（SAUZER FX）のロゴ" width="640" height="640"><div><div class="eyebrow">Brand</div><h2 style="font-size:24px;margin-top:6px">さうざーFX</h2><p class="muted" style="margin-top:8px;max-width:30em">ゴールドの値動きに挑むライオンと、右肩上がりのローソク足をモチーフにしたロゴです。</p></div></div>
    <dl class="dl">
      <dt>屋号</dt><dd>さうざーFX</dd>
      <dt>運営者</dt><dd>なりやん</dd>
      <dt>活動内容</dt><dd>ゴールド（XAUUSD）を中心としたEA・インジケーターの開発と販売、FX入門・EA講座の執筆</dd>
      <dt>販売先</dt><dd><a href="{GGJ_URL}" target="_blank" rel="noopener">GogoJungle</a>、note</dd>
      <dt>X</dt><dd><a href="{X_URL}" target="_blank" rel="noopener">@alex767_fx</a></dd>
      <dt>お問い合わせ</dt><dd>XのDMで受け付けています。商品の購入やダウンロードに関するお問い合わせは、GogoJungleのサポートもご利用ください。</dd>
    </dl>
    <div class="prose">
      <h2 style="font-size:22px;margin-bottom:12px">開発の考え方</h2>
      <p>EAは、バックテストの数字を良く見せようとすればいくらでも良く見せられます。さうざーFXでは、パラメータを決めた期間とは別の期間でもう一度テストし、両方で同じ傾向が出たロジックだけを製品にしています。</p>
      <p>これまでに試した手法の多くは、この基準を通りませんでした。うまくいかなかった検証も含めて、コラムで経過を公開していきます。</p>
    </div>
  </div>
</section>'''

def legal_body():
    return page_head([("./", "ホーム"), ("", "免責事項・プライバシーポリシー")], "免責事項・プライバシーポリシー",
                     "当サイトをご利用いただく前にお読みください。") + '''
<section class="section">
  <div class="wrap legal">
    <div id="disclaimer">
      <h2>免責事項</h2>
      <ul>
        <li>当サイトの情報は、投資判断の参考として提供するものです。特定の金融商品の売買を勧誘するものではありません。</li>
        <li>掲載しているバックテストや運用実績は過去のもので、将来の成果を保証するものではありません。</li>
        <li>FX・CFD取引はレバレッジを伴い、元本を超える損失が生じる可能性があります。取引はご自身の判断と責任で行ってください。</li>
        <li>当サイトの情報を利用したことで生じた損害について、運営者は責任を負いかねます。</li>
        <li>掲載内容は予告なく変更することがあります。</li>
      </ul>
    </div>
    <div id="ad">
      <h2>広告の表記について</h2>
      <p>当サイトはアフィリエイトプログラムを利用しています。記事内のリンクから商品やサービスに申し込まれた場合、運営者に報酬が支払われることがあります。</p>
      <p>広告を含むページには、その旨を表示しています。紹介する内容は、運営者が実際に検証・利用したうえで判断しています。</p>
      <p>EA講座の本文には業者の名前を出していません。検証に使っている口座は、紹介報酬の有無を明記したうえで、EA講座の第10章にまとめています。</p>
    </div>
    <div id="privacy">
      <h2>プライバシーポリシー</h2>
      <p>当サイトでは、アクセス状況の把握のためにGoogleアナリティクスを利用しています。Googleアナリティクスはデータ収集のためにCookieを使用しますが、個人を特定する情報は含まれません。Cookieはブラウザの設定で無効にできます。</p>
      <p>また、アフィリエイトプログラムでは、成果の計測のためにCookieが使用されることがあります。</p>
      <p>お問い合わせでいただいた情報は、回答のためにのみ使用し、法令に基づく場合を除いて第三者に提供しません。</p>
    </div>
    <div id="copyright">
      <h2>著作権</h2>
      <p>当サイトに掲載している文章、画像、図表の著作権は運営者に帰属します。無断での転載・複製はご遠慮ください。</p>
    </div>
  </div>
</section>'''

# ------------------------------------------------------------------ EA講座
ARTICLE_FILE = "course-oos.html"
COURSE = [
    ("PART 1", "EAの基本", "自動売買が何をしてくれて、何をしてくれないのか。", [
        (1, "EA（自動売買）とは", "任せられることと、任せられないこと", None),
        (2, "EAが1回の取引をするまで", "シグナルの判定から決済までを順に追う", None),
        (3, "ゴールドをEAで取引する理由と難しさ", "値幅、スプレッド、動きやすい時間帯", None),
    ]),
    ("PART 2", "動かす準備", "口座、MT5、VPS、EA本体。動かすまでに必要なものをそろえます。", [
        (4, "必要なものの全体図", "口座・MT5・VPS・EAと、準備の確認表", None),
        (5, "MT5へのEAの入れ方と設定", "データフォルダからアルゴ取引のオンまで", None),
        (6, "VPSで24時間動かす", "自宅のパソコンを付けっぱなしにしない方法", None),
        (7, "毎日確認すること", "操作ログ、マジックナンバー、保有ポジション", None),
    ]),
    ("PART 3", "口座の選び方", "同じEAでも、口座の条件で成績が変わります。", [
        (8, "ゴールドEAに向く口座の条件", "スプレッド、銘柄名、最小ロット、約定", None),
        (9, "国内口座と海外口座の違い", "金融庁の登録、レバレッジ、税金", None),
        (10, "さうざーFXが検証に使っている口座", "業者名を出すのはこのページだけ。紹介報酬の有無も明記します", None),
    ]),
    ("PART 4", "成績の読み方", "販売ページの数字を、自分で確かめられるようになるための章です。", [
        (11, "PF・最大DD・勝率・損益比", "4つの数字が表していること", None),
        (12, "バックテストはなぜ良く見えるのか", "過剰最適化とカーブフィッティング", None),
        (13, "期間を分けて確かめる", "調整に使っていない期間でも同じ結果が出るか", ARTICLE_FILE),
        (14, "販売ページで確かめること", "購入前に見る10の項目", None),
    ]),
    ("PART 5", "資金と運用", "動かし始めてから迷うことを先に決めておきます。", [
        (15, "証拠金とロットの決め方", "最小ロットのせいで複利が効かない問題", None),
        (16, "ドローダウン中にやること", "触ってよいこと、触ってはいけないこと", None),
        (17, "止めどきの決め方", "感情ではなく、事前に決めた数字で止める", None),
        (18, "複数のEAを組み合わせる", "相関が低い組み合わせで資金曲線をならす", None),
    ]),
    ("PART 6", "さうざーFXの開発記録", "うまくいかなかった検証も含めて、開発の経過を公開します。", [
        (19, "22の手法を検証して、残ったのは2つ", "有名な手法をゴールドで試した結果", None),
        (20, "買いと売りを分けて検証する", "ロングとショートの成績を別々に確かめる理由", None),
        (21, "実運用で確認していること", "バックテストと実際の注文がずれていないかを確かめる", None),
    ]),
]

def course_body():
    total = sum(len(c[3]) for c in COURSE)
    ready = sum(1 for c in COURSE for x in c[3] if x[3])
    parts = []
    for k, title, desc, chs in COURSE:
        rows = []
        for no, t, sub, link in chs:
            if link:
                rows.append(f'<li class="ready"><span class="no">{no:02d}</span><span class="t"><b><a href="{link}">{t}</a></b><span>{sub}</span></span><span class="chip st-read">読めます</span></li>')
            else:
                rows.append(f'<li><span class="no">{no:02d}</span><span class="t"><b>{t}</b><span>{sub}</span></span><span class="chip st-prep">準備中</span></li>')
        parts.append(f'''<div class="part">
  <div class="part-h"><span class="k">{k}</span><h3>{title}</h3><p>{desc}</p></div>
  <ol class="ch">{"".join(rows)}</ol>
</div>''')
    return page_head([("./", "ホーム"), ("", "EA講座")], "EA講座",
                     "EAを選び、動かし、止めるための判断材料を、ゴールドEAを開発している立場から順番にまとめていきます。") + f'''
<section class="section" style="padding-bottom:40px">
  <div class="wrap course-intro">
    <div class="prose">
      <p>EAを入れておけば勝手に増える、と考えて始めると、最初の大きなドローダウンで手が止まります。どのEAを選ぶか、いくらで動かすか、いつ止めるか。この3つを自分で決められるようになることが、この講座の目的です。</p>
      <p>さうざーFXはゴールド（XAUUSD）のEAを中心に作っているので、例は主にゴールドで説明します。検証の考え方は、実際の開発で使っているものです。</p>
      <div class="toc-meta"><span>全<b>{len(COURSE)}</b>部・<b>{total}</b>章</span><span>公開中 <b>{ready}</b>章</span><span>順次追加していきます</span></div>
    </div>
    <aside class="promise">
      <h3>この講座で守ること</h3>
      <ul>
        <li>「稼げる」とは書きません。過去の成績は将来の成績を約束しません。</li>
        <li>本文には業者の名前を出しません。口座の名前を出すのは第10章だけです。</li>
        <li>紹介報酬が発生するリンクには、その旨を明記します。</li>
      </ul>
    </aside>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="wrap">{"".join(parts)}</div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">FAQ</div><h2>よくある質問</h2></div></div>
    <div class="faq">
      <details><summary>誰に向けた講座ですか？</summary><p>これからEAを使ってみたい方と、すでに使っているけれど選び方や止めどきに迷っている方に向けています。FXの用語に慣れていない方は、先に<a href="beginners.html">初めての方へ</a>を読むと進めやすくなります。</p></details>
      <details><summary>この講座を読めば勝てますか？</summary><p>勝ちを約束するものではありません。EAを選んで動かすときに、何を見てどう判断するかの材料をまとめた講座です。</p></details>
      <details><summary>さうざーFXのEAを買わないと役に立ちませんか？</summary><p>いいえ。成績の読み方や資金管理の考え方は、どの開発者のEAにも当てはまります。他社のEAを選ぶときの確認にも使ってください。</p></details>
    </div>
  </div>
</section>'''

def pf_chart():
    data = [("ロジックA", "採用", 1.30, 1.45), ("ロジックB", "不採用", 0.75, 2.00), ("ロジックC", "不採用", 0.80, 1.30)]
    W, H = 640, 300
    L, R, T, B = 44, 12, 18, 52
    ymax = 2.2
    pw, ph = W - L - R, H - T - B
    def yv(v): return T + ph - v / ymax * ph
    out = []
    for v in (0.5, 1.0, 1.5, 2.0):
        out.append(f'<line class="grid-l" x1="{L}" x2="{W-R}" y1="{yv(v):.1f}" y2="{yv(v):.1f}"/>')
        out.append(f'<text class="ax" x="{L-8}" y="{yv(v)+4:.1f}" text-anchor="end">{v:.1f}</text>')
    out.append(f'<text class="ax" x="{L-8}" y="{yv(0)+4:.1f}" text-anchor="end">0</text>')
    gw = pw / len(data)
    bw = min(46, gw * 0.26)
    for i, (name, verdict, is_, oos) in enumerate(data):
        cx = L + gw * i + gw / 2
        g = [f'<g class="cg"><title>{name}：IS期間 PF {is_:.2f} ／ OOS期間 PF {oos:.2f}</title>',
             f'<rect class="hit" x="{L+gw*i:.1f}" y="{T}" width="{gw:.1f}" height="{ph}"/>']
        for j, (val, cls) in enumerate(((is_, "b-is"), (oos, "b-oos"))):
            x = cx - bw - 1 if j == 0 else cx + 1
            top = yv(val); base = yv(0); r = 4
            path = (f'M{x:.1f},{base:.1f} V{top+r:.1f} Q{x:.1f},{top:.1f} {x+r:.1f},{top:.1f} '
                    f'H{x+bw-r:.1f} Q{x+bw:.1f},{top:.1f} {x+bw:.1f},{top+r:.1f} V{base:.1f} Z')
            g.append(f'<path class="bar {cls}" d="{path}"/>')
            g.append(f'<text class="val" x="{x+bw/2:.1f}" y="{top-6:.1f}" text-anchor="middle">{val:.2f}</text>')
        g.append(f'<text class="cat" x="{cx:.1f}" y="{H-B+20}" text-anchor="middle">{name}</text>')
        g.append(f'<text class="cat2" x="{cx:.1f}" y="{H-B+37}" text-anchor="middle">{verdict}</text>')
        g.append('</g>')
        out.append("".join(g))
    out.append(f'<line class="base-l" x1="{L}" x2="{W-R}" y1="{yv(0):.1f}" y2="{yv(0):.1f}"/>')
    out.append(f'<line class="ref-l" x1="{L}" x2="{W-R}" y1="{yv(1):.1f}" y2="{yv(1):.1f}"/>')
    return (f'<svg class="chart-svg" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="説明用の架空の例。ロジックAはIS 1.30、OOS 1.45。ロジックBはIS 0.75、OOS 2.00。ロジックCはIS 0.80、OOS 1.30。">'
            + "".join(out) + '</svg>')

def article_body():
    return f'''<div class="wrap">
  <div style="padding-top:28px"><nav class="crumb" aria-label="パンくずリスト"><a href="./">ホーム</a> <span aria-hidden="true">/</span> <a href="course.html">EA講座</a> <span aria-hidden="true">/</span> <span>第13章</span></nav></div>
  <article class="article">
    <header class="a-head">
      <span class="k">PART 4 成績の読み方 ／ 第13章</span>
      <h1>期間を分けて確かめる</h1>
      <p class="a-lead">バックテストの成績が良くても、それはパラメータをその期間に合わせた結果かもしれません。調整に使っていない期間でも同じ結果が出るかを確かめる方法を、例を使って説明します。</p>
      <div class="a-meta"><span class="tag">XAUUSD</span><span class="tag">H1</span><span class="tag">バックテスト</span></div>
    </header>

    <h2>なぜ期間を分けるのか</h2>
    <p>EAのパラメータは、バックテストの成績を見ながら調整します。移動平均線の期間を変え、損切りの幅を変え、成績が良くなる組み合わせを探します。</p>
    <p>問題は、この作業を続けるほど、その期間に起きた値動きの「偶然」にまで合わせてしまうことです。過去のチャートにぴったり合ったEAは、バックテストの数字はきれいでも、これから先の相場では同じように勝てません。</p>
    <p>そこで、データを2つの期間に分けます。</p>
    <ul>
      <li><b>IS期間（インサンプル）</b>：パラメータの調整に使う期間</li>
      <li><b>OOS期間（アウトオブサンプル）</b>：調整には一切使わず、最後の確認だけに使う期間</li>
    </ul>
    <p>OOS期間は、EAにとって「まだ見ていない相場」の代わりです。ここでも成績が崩れなければ、そのロジックは特定の期間に合わせただけのものではない可能性が高くなります。</p>

    <div class="point"><b>さうざーFXの採用基準</b>IS期間とOOS期間の両方でPF（プロフィットファクター）が1.0を上回ること。片方だけが良いロジックは採用しません。</div>

    <h2>例：3つのロジックを比べる</h2>
    <p>考え方を、説明用の架空の例で見てみます。あるEAに、エントリーのロジックの候補がA・B・Cの3つあるとします。データを次の2つの期間に分けて、それぞれのPFを比べました。</p>
    <ul>
      <li>IS期間：パラメータを調整した前半の期間（下げ相場と横ばいを含む）</li>
      <li>OOS期間：調整に使っていない後半の期間（強い上昇相場）</li>
    </ul>

    <figure class="figure" style="margin-inline:0">
      <div class="f-title">ロジックごとのPF（IS期間とOOS期間）</div>
      <div class="f-sub">説明用の架空の数字です</div>
      <div class="legend"><span><i style="background:var(--s-is)"></i>IS期間（調整に使った期間）</span><span><i style="background:var(--s-oos)"></i>OOS期間（確認用の期間）</span><span><i style="background:none;border-top:1.5px dashed var(--ink);height:0;width:16px;border-radius:0;vertical-align:3px"></i>PF 1.0（損益ゼロの線）</span></div>
      {pf_chart()}
      <p class="f-note">PFは総利益÷総損失。1.0を上回れば利益、下回れば損失です。</p>
    </figure>

    <div class="data-tbl"><table>
      <thead><tr><th>ロジック</th><th>IS期間 PF</th><th>OOS期間 PF</th><th>判定</th></tr></thead>
      <tbody>
        <tr><td>ロジックA</td><td class="n">1.30</td><td class="n">1.45</td><td><span class="verdict v-ok">両期間で黒字・採用</span></td></tr>
        <tr><td>ロジックB</td><td class="n ng">0.75</td><td class="n">2.00</td><td><span class="verdict v-ng">方向が不一致・不採用</span></td></tr>
        <tr><td>ロジックC</td><td class="n ng">0.80</td><td class="n">1.30</td><td><span class="verdict v-ng">方向が不一致・不採用</span></td></tr>
      </tbody>
    </table></div>

    <h3>OOSで一番良いロジックを選ばない理由</h3>
    <p>OOS期間だけを見ると、PFが一番高いのはロジックBの2.00です。それでも採用しません。IS期間ではPF 0.75と、はっきり負けているからです。</p>
    <p>OOS期間は強い上昇相場でした。こういう相場では、どんな買いのきっかけでもある程度勝ててしまいます。下げ相場を含むIS期間で負けているロジックは、相場の性格が変われば、また負ける可能性が高いと考えます。</p>
    <p>採用するのは、両方の期間で利益が出ているロジックAです。OOSの数字はBより低くても、相場の性格が違う2つの期間で同じ傾向が出ていることの方が大切です。</p>

    <h2>期間を分けるときの注意点</h2>
    <h3>OOS期間を見てから調整しない</h3>
    <p>OOS期間の成績を見て「ここが悪いから直そう」とパラメータを変えた時点で、その期間はOOSではなくなります。OOS期間は最後に1回だけ確認するものと決めておきます。</p>
    <h3>相場の性格が違う期間を含める</h3>
    <p>上昇相場だけ、下降相場だけの期間で分けても、確認になりません。ISとOOSのどちらかに、上昇・下降・横ばいがそれぞれ含まれるように期間を選びます。</p>
    <h3>取引回数が少なすぎないか</h3>
    <p>取引が数件しかない期間のPFは、1件の勝ち負けで大きく変わります。特定の年だけを切り出して比べるときは、件数も必ず一緒に見ます。</p>

    <h2>販売ページを見るときのチェック</h2>
    <p>他の開発者のEAを選ぶときも、同じ視点で確認できます。</p>
    <ul class="checklist">
      <li>バックテストの期間は何年分か。短い期間だけを見せていないか</li>
      <li>調整に使った期間と、確認に使った期間を分けて説明しているか</li>
      <li>フォワード（実際の口座での運用）の成績も公開しているか</li>
      <li>期間ごと・年ごとの成績で、極端に良い年だけが全体を引き上げていないか</li>
    </ul>

    <nav class="a-nav" aria-label="前後の章">
      <span><small>前の章</small>第12章 バックテストはなぜ良く見えるのか（準備中）</span>
      <a class="next" href="course.html"><small>講座の目次へ</small>EA講座 全21章 →</a>
    </nav>
  </article>
</div>'''

from basics_content import STEPS as FX_STEPS, CHAPTERS as FX_CHAPTERS

def fx_slug(no):
    return f"fx-{no:02d}.html"

def fx_basics_body():
    parts = []
    for i, (k, title, desc) in enumerate(FX_STEPS):
        rows = "".join(
            f'<li><span class="no">{c["no"]:02d}</span><span class="t"><b><a href="{fx_slug(c["no"])}" style="text-decoration:none">{c["title"]}</a></b><span>{c["sub"]}</span></span><span class="chip st-read">読めます</span></li>'
            for c in FX_CHAPTERS if c["step"] == i)
        parts.append(f'''<div class="part">
  <div class="part-h"><span class="k">{k}</span><h3>{title}</h3><p>{desc}</p></div>
  <ol class="ch">{rows}</ol>
</div>''')
    return page_head([("./", "ホーム"), ("", "FX入門")], "FX入門（基本知識編）",
                     "FXをまったく知らない方が、一から順番に学べる入門講座です。全15章、1章5分ほどで読めます。") + f'''
<section class="section" style="padding-bottom:40px">
  <div class="wrap course-intro">
    <div class="prose">
      <p>FXは「通貨を売り買いして、値段の差で損益が出る取引」です。しくみ自体は単純ですが、レバレッジやロスカットを知らずに始めると、短い期間で資金を失うことがあります。</p>
      <p>この入門では、利益の出し方より先に、損失を小さく抑えるための知識を順番に説明します。第1章から順に読むと、FXの取引に必要な基本が一通り身につきます。</p>
      <div class="toc-meta"><span>全<b>{len(FX_STEPS)}</b>ステップ・<b>{len(FX_CHAPTERS)}</b>章</span><span>すべて公開中</span></div>
      <div class="cta" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px"><a class="btn btn-primary" href="{fx_slug(1)}">第1章から読む</a><a class="btn btn-ghost" href="{fx_slug(12)}">損切りの章へ</a></div>
    </div>
    <aside class="promise">
      <h3>この入門で守ること</h3>
      <ul>
        <li>専門用語は、出てきたその場で説明します。</li>
        <li>特定のFX会社をすすめません。</li>
        <li>計算の例は、しくみを説明するためのものです。実際の条件は各社でご確認ください。</li>
      </ul>
    </aside>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="wrap">{"".join(parts)}</div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Next</div><h2>入門を読み終えたら</h2></div></div>
    <div class="next-grid" style="max-width:52em">
      <a class="next-card" href="course.html"><span class="k">NEXT</span><b>EA講座</b><span>自動売買（EA）の選び方、動かし方、成績の読み方を学びます。</span></a>
      <a class="next-card" href="blog.html#basics"><span class="k">OPTION</span><b>海外FX基礎知識</b><span>海外FXのしくみと、国内FXとの違いを解説しています。</span></a>
    </div>
  </div>
</section>'''

def fx_article_body(c):
    k, step_title, _ = FX_STEPS[c["step"]]
    n = len(FX_CHAPTERS)
    prev_html = (f'<a href="{fx_slug(c["no"]-1)}"><small>前の章</small>第{c["no"]-1}章 {FX_CHAPTERS[c["no"]-2]["title"]}</a>'
                 if c["no"] > 1 else '<a href="fx-basics.html"><small>目次へ</small>FX入門 全15章</a>')
    next_html = (f'<a class="next" href="{fx_slug(c["no"]+1)}"><small>次の章</small>第{c["no"]+1}章 {FX_CHAPTERS[c["no"]]["title"]} →</a>'
                 if c["no"] < n else '<a class="next" href="course.html"><small>次に学ぶ</small>EA講座 →</a>')
    summ = "".join(f"<li>{x}</li>" for x in c["summary"])
    return f'''<div class="wrap">
  <div style="padding-top:28px"><nav class="crumb" aria-label="パンくずリスト"><a href="./">ホーム</a> <span aria-hidden="true">/</span> <a href="fx-basics.html">FX入門</a> <span aria-hidden="true">/</span> <span>第{c["no"]}章</span></nav></div>
  <article class="article">
    <header class="a-head">
      <span class="k">{k} {step_title} ／ 第{c["no"]}章（全{n}章）</span>
      <h1>{c["title"]}</h1>
      <p class="a-lead">{c["lead"]}</p>
    </header>
    {c["body"]}
    <div class="summary"><h2>この章のまとめ</h2><ul>{summ}</ul></div>
    <nav class="a-nav" aria-label="前後の章">{prev_html}{next_html}</nav>
  </article>
</div>'''

def sr_body():
    dl = "downloads/SR_AutoLevels_v120.ex5"
    return '''<div class="wrap" style="padding-top:28px"><nav class="crumb" aria-label="パンくずリスト"><a href="./">ホーム</a> <span aria-hidden="true">/</span> <a href="products.html#indicators">インジケーター</a> <span aria-hidden="true">/</span> <span>SR_AutoLevels</span></nav></div>''' + f'''
<div class="wrap detail">
  <div style="display:grid;gap:18px">
    <figure class="shot"><img src="sr-h1.jpg" alt="SR_AutoLevelsをXAUUSDの1時間足に表示した画面。H1の実線、H4の破線、日足の点線のサポート・レジスタンスと、タッチ回数のラベル" width="1600" height="778"><figcaption>XAUUSD 1時間足での表示例。実線がH1、破線がH4のライン。日足のラインは「[D1]」と表示。水色の点は出来高スパイク。</figcaption></figure>
  </div>
  <aside class="dl-box" id="download">
    <span class="chip st-free" style="justify-self:start">無料公開 ・ v1.20</span>
    <h1 style="font-size:clamp(24px,3vw,32px)">SR_AutoLevels</h1>
    <p class="fullname" style="font-size:13px;color:var(--muted);margin-top:-6px">重要サポレジ自動描画インジケーター（MT5）</p>
    <p>過去の高値・安値から、何度も意識された価格帯を自動で探して水平線を引きます。ラインごとにタッチ回数と出来高スパイクの実績を表示するので、どの線が強いかがひと目で分かります。</p>
    <a class="btn btn-dl" href="{dl}" download>無料でダウンロード（.ex5）</a>
    <ul class="terms" style="margin:0;padding-left:1.1em">
      <li>MetaTrader 5用です。登録やメールアドレスの入力は不要です。</li>
      <li>個人での利用は自由です。再配布・販売・改変品の配布はご遠慮ください。</li>
      <li>売買を推奨するものではなく、利益を保証するものでもありません。</li>
    </ul>
  </aside>
</div>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Features</div><h2>できること</h2></div></div>
    <div class="feats">
      <div class="feat"><h3>強い節目を自動で選ぶ</h3><p>直近500本の山と谷から、何度も止められた価格帯を探します。タッチ回数、出来高、出来高スパイクの回数で点数をつけ、強い順に線を引きます。</p></div>
      <div class="feat"><h3>3つの時間足を重ねて表示</h3><p>1時間足チャートではH1・H4・日足、4時間足ではH4・日足、日足チャートでは日足のみ。上位足と同じ価格帯にある線はまとめ、ラベルに「+H4」のように表示します。</p></div>
      <div class="feat"><h3>本物のブレイクを知らせる</h3><p>重要ラインに出来高スパイクを伴って価格が届いたときに通知します。同じラインで攻防が3回続くと「攻防激化」として知らせます。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">How to read</div><h2>ラベルの読み方</h2></div></div>
    <div class="label-demo">4383.19  [D1] ×4 *2 高VOL +H4 +H1</div>
    <div class="data-tbl" style="max-width:52em">
      <table style="min-width:0">
        <thead><tr><th>表示</th><th>意味</th></tr></thead>
        <tbody>
          <tr><td>4383.19</td><td>ラインの価格</td></tr>
          <tr><td>[D1]</td><td>日足で見つかったライン（基準の時間足のラインには付きません）</td></tr>
          <tr><td>×4</td><td>この価格帯で4回止められた（タッチ回数）</td></tr>
          <tr><td>*2</td><td>そのうち2回は、出来高が急に増えた足（スパイク）を伴った</td></tr>
          <tr><td>高VOL</td><td>この価格帯での平均出来高が、全体平均の1.3倍以上</td></tr>
          <tr><td>+H4 +H1</td><td>H4とH1でも同じ価格帯にラインがある（複数の時間足で意識されている強い節目）</td></tr>
        </tbody>
      </table>
    </div>
    <p class="muted" style="font-size:13px;max-width:46em">FXやCFDには取引所の出来高がないため、出来高にはティック出来高（値動きの回数）を使っています。取引の活発さの目安としてご覧ください。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Timeframes</div><h2>時間足ごとの表示</h2></div><p>開いているチャートの時間足に合わせて、表示するラインが自動で切り替わります。</p></div>
    <div style="display:grid;gap:28px">
      <figure class="shot"><img src="sr-h4.jpg" alt="SR_AutoLevelsを4時間足チャートに表示した画面。H4と日足のラインが表示されている" width="1600" height="778" loading="lazy"><figcaption><b>4時間足</b>：H4のライン（実線）と日足のライン（[D1]）を表示。H4でも意識されている日足のラインには「+H4」が付きます。</figcaption></figure>
      <figure class="shot"><img src="sr-d1.jpg" alt="SR_AutoLevelsを日足チャートに表示した画面。日足のサポート・レジスタンスのみが表示されている" width="1600" height="778" loading="lazy"><figcaption><b>日足</b>：日足のラインだけを表示し、長期の節目を確認できます。</figcaption></figure>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Install</div><h2>導入のしかた</h2></div></div>
    <ol class="steps" style="padding:0;margin:0">
      <li><div><b>ファイルをダウンロードする</b><p>上のボタンから <code>SR_AutoLevels_v120.ex5</code> をダウンロードします。</p></div></li>
      <li><div><b>MT5のフォルダに入れる</b><p>MT5の「ファイル」→「データフォルダを開く」から <code>MQL5\\Indicators</code> にファイルを置きます。</p></div></li>
      <li><div><b>MT5を再起動する</b><p>ナビゲーターの「インディケータ」に SR_AutoLevels が表示されます。</p></div></li>
      <li><div><b>チャートに付ける</b><p>チャートへドラッグして「OK」を押せば完了です。1時間足のチャートがおすすめです。</p></div></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">FAQ</div><h2>よくある質問</h2></div></div>
    <div class="faq">
      <details><summary>本当に無料ですか？</summary><p>はい、無料です。登録やメールアドレスの入力もいりません。</p></details>
      <details><summary>ゴールド以外でも使えますか？</summary><p>使えます。銘柄を問わず動きます。ただし、初期設定はXAUUSDの1時間足で調整しています。</p></details>
      <details><summary>ラインが表示されません</summary><p>H4・日足のデータを読み込むまで、数秒から数十秒かかることがあります。表示されないときは、時間足を一度切り替えてください。</p></details>
      <details><summary>このラインで売買すれば勝てますか？</summary><p>ラインは「過去に意識された価格帯」を示すもので、将来の値動きを保証するものではありません。損切りの位置や取引量は、<a href="fx-12.html">FX入門 第12章</a>の考え方を参考に、ご自身で決めてください。</p></details>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Next</div><h2>あわせて読む</h2></div></div>
    <div class="next-grid" style="max-width:52em">
      <a class="next-card" href="tengan-kinryu.html"><span class="k">EA</span><b>天眼金龍</b><span>ゴールド専用のトレンドフォローEA。v1.4のバックテスト結果を公開しています。</span></a>
      <a class="next-card" href="fx-basics.html"><span class="k">LEARN</span><b>FX入門（全15章）</b><span>サポート・レジスタンスの前に、FXの基本から順番に学べます。</span></a>
    </div>
  </div>
</section>'''

def dow_body():
    dl = "downloads/Million_DowTrend_v303.ex5"
    return '''<div class="wrap" style="padding-top:28px"><nav class="crumb" aria-label="パンくずリスト"><a href="./">ホーム</a> <span aria-hidden="true">/</span> <a href="products.html#indicators">インジケーター</a> <span aria-hidden="true">/</span> <span>Million_DowTrend</span></nav></div>''' + f'''
<div class="wrap detail">
  <div style="display:grid;gap:18px">
    <figure class="shot"><img src="dow-h4.jpg" alt="Million_DowTrendをXAUUSDの4時間足に表示した画面。高値と安値にHH・HL・LH・LLのラベル、戻り高値と直近安値のライン、左下にH1・H4・日足のトレンド一覧" width="1600" height="773"><figcaption>XAUUSD 4時間足での表示例。山と谷にHH・HL・LH・LLのラベル、点線で波の流れ、黄色の破線が戻り高値と直近安値。左下のパネルで各時間足のトレンドを確認できます。</figcaption></figure>
  </div>
  <aside class="dl-box" id="download">
    <span class="chip st-free" style="justify-self:start">無料公開 ・ v3.03</span>
    <h1 style="font-size:clamp(24px,3vw,32px)">Million_DowTrend</h1>
    <p class="fullname" style="font-size:13px;color:var(--muted);margin-top:-6px">ダウ理論トレンド判定インジケーター（MT5）</p>
    <p>高値と安値の切り上げ・切り下げを自動で判定し、いまが上昇トレンドか下降トレンドかをチャート上に表示します。トレンドが変わる価格（押し安値・戻り高値）も線で示します。</p>
    <a class="btn btn-dl" href="{dl}" download>無料でダウンロード（.ex5）</a>
    <ul class="terms" style="margin:0;padding-left:1.1em">
      <li>MetaTrader 5用です。登録やメールアドレスの入力は不要です。</li>
      <li>個人での利用は自由です。再配布・販売・改変品の配布はご遠慮ください。</li>
      <li>売買を推奨するものではなく、利益を保証するものでもありません。</li>
    </ul>
  </aside>
</div>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Features</div><h2>できること</h2></div></div>
    <div class="feats">
      <div class="feat"><h3>波の高値・安値を自動で判定</h3><p>確定した足だけで山と谷を見つけ、前の山・谷と比べてHH・HL・LH・LLのラベルを付けます。小さすぎる波はATRで除くので、細かいノイズに振り回されません。</p></div>
      <div class="feat"><h3>転換は終値のブレイクで判定</h3><p>下降トレンド中に終値が戻り高値を上抜けたら「上昇転換」、上昇トレンド中に終値が押し安値を下抜けたら「下降転換」。確定足で判定するため、あとから表示が変わりません。</p></div>
      <div class="feat"><h3>H1・H4・日足を一覧で確認</h3><p>左下のパネルに、開いているチャートとH1・H4・日足のトレンドを並べて表示します。上位足と同じ方向かどうかが、時間足を切り替えずに分かります。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">How to read</div><h2>表示の読み方</h2></div></div>
    <div class="data-tbl" style="max-width:52em">
      <table style="min-width:0">
        <thead><tr><th>表示</th><th>意味</th></tr></thead>
        <tbody>
          <tr><td>HH</td><td>高値の切り上げ（前の高値より高い）</td></tr>
          <tr><td>HL</td><td>安値の切り上げ（前の安値より高い）</td></tr>
          <tr><td>LH</td><td>高値の切り下げ（前の高値より低い）</td></tr>
          <tr><td>LL</td><td>安値の切り下げ（前の安値より低い）</td></tr>
          <tr><td>上昇転換 / 下降転換</td><td>終値が戻り高値・押し安値を抜け、トレンドが入れ替わった足</td></tr>
          <tr><td>押し安値</td><td>上昇トレンド中、終値でここを割ると下降転換になる価格</td></tr>
          <tr><td>戻り高値</td><td>下降トレンド中、終値でここを超えると上昇転換になる価格</td></tr>
          <tr><td>直近高値 / 直近安値</td><td>最新の山・谷。トレンドの判定には使わない参考の価格</td></tr>
        </tbody>
      </table>
    </div>
    <p class="muted" style="font-size:13px;max-width:46em">HHとHLが続けば上昇トレンド、LHとLLが続けば下降トレンドです。ダウ理論の基本は<a href="fx-11.html">FX入門 第11章「チャートの読み方」</a>で解説しています。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Example</div><h2>1時間足での表示</h2></div><p>短い時間足では転換が増えます。上位足のトレンドと合わせて見るのがおすすめです。</p></div>
    <figure class="shot"><img src="dow-h1.jpg" alt="Million_DowTrendをXAUUSDの1時間足に表示した画面。上昇転換と下降転換のマーカー、直近高値と押し安値のライン" width="1600" height="773" loading="lazy"><figcaption><b>1時間足</b>：H1は上昇転換、H4は下降トレンド。パネルを見ると、短期の上昇が上位足の流れに逆らっていることが分かります。</figcaption></figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Install</div><h2>導入のしかた</h2></div></div>
    <ol class="steps" style="padding:0;margin:0">
      <li><div><b>ファイルをダウンロードする</b><p>上のボタンから <code>Million_DowTrend_v303.ex5</code> をダウンロードします。</p></div></li>
      <li><div><b>MT5のフォルダに入れる</b><p>MT5の「ファイル」→「データフォルダを開く」から <code>MQL5\\Indicators</code> にファイルを置きます。</p></div></li>
      <li><div><b>MT5を再起動する</b><p>ナビゲーターの「インディケータ」に Million_DowTrend が表示されます。</p></div></li>
      <li><div><b>チャートに付ける</b><p>チャートへドラッグして「OK」を押せば完了です。どの時間足でも使えます。</p></div></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">FAQ</div><h2>よくある質問</h2></div></div>
    <div class="faq">
      <details><summary>本当に無料ですか？</summary><p>はい、無料です。登録やメールアドレスの入力もいりません。</p></details>
      <details><summary>あとから表示が変わる（リペイントする）ことはありますか？</summary><p>ありません。山と谷は左右5本の足が確定してから決まり、転換も確定した足の終値で判定します。そのぶん、表示は実際の山・谷から数本遅れます。</p></details>
      <details><summary>波が細かすぎる・大きすぎるときは？</summary><p>設定の「スイング判定の左右バー数」を大きくすると大きな波だけ、小さくすると細かい波も拾います。「最小の波の大きさ」でも調整できます。</p></details>
      <details><summary>ゴールド以外でも使えますか？</summary><p>使えます。銘柄や時間足を問わず動きます。</p></details>
      <details><summary>転換のサインで売買すれば勝てますか？</summary><p>転換は「過去の高値・安値を抜けた」という事実を示すもので、その後の値動きを保証するものではありません。損切りの位置や取引量は、<a href="fx-12.html">FX入門 第12章</a>の考え方を参考に、ご自身で決めてください。</p></details>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Next</div><h2>あわせて使う</h2></div></div>
    <div class="next-grid" style="max-width:52em">
      <a class="next-card" href="sr-autolevels.html"><span class="k">FREE</span><b>SR_AutoLevels</b><span>重要なサポート・レジスタンスを自動で引く無料インジケーター。押し安値・戻り高値と重なる節目の確認に。</span></a>
      <a class="next-card" href="order-block.html"><span class="k">FREE</span><b>Million_OrderBlock</b><span>トレンドの向きに合ったオーダーブロックで、戻りを待つ場所を探せます。</span></a>
      <a class="next-card" href="fx-11.html"><span class="k">LEARN</span><b>FX入門 第11章</b><span>ローソク足、時間足、ダウ理論の基本を解説しています。</span></a>
    </div>
  </div>
</section>'''

def ob_body():
    dl = "downloads/Million_OrderBlock_v100.ex5"
    return '''<div class="wrap" style="padding-top:28px"><nav class="crumb" aria-label="パンくずリスト"><a href="./">ホーム</a> <span aria-hidden="true">/</span> <a href="products.html#indicators">インジケーター</a> <span aria-hidden="true">/</span> <span>Million_OrderBlock</span></nav></div>''' + f'''
<div class="wrap detail">
  <div style="display:grid;gap:18px">
    <figure class="shot"><img src="ob-h1.jpg" alt="Million_OrderBlockをXAUUSDの1時間足に表示した画面。売りオーダーブロックの赤い箱と、H4・日足のオーダーブロックの点線の枠" width="1600" height="775"><figcaption>XAUUSD 1時間足での表示例（SR_AutoLevels・Million_DowTrendと同時に表示）。塗りつぶしの箱が1時間足のOB、点線の枠がH4・日足のOB。「×5」は価格が戻ってきた回数です。</figcaption></figure>
  </div>
  <aside class="dl-box" id="download">
    <span class="chip st-free" style="justify-self:start">無料公開 ・ v1.00</span>
    <h1 style="font-size:clamp(24px,3vw,32px)">Million_OrderBlock</h1>
    <p class="fullname" style="font-size:13px;color:var(--muted);margin-top:-6px">オーダーブロック自動検出インジケーター（MT5）</p>
    <p>強い値動きが始まる直前の足（オーダーブロック）を自動で見つけ、箱で表示します。価格が終値で反対側を抜けたら消えるので、いまも生きている場所だけが残ります。</p>
    <a class="btn btn-dl" href="{dl}" download>無料でダウンロード（.ex5）</a>
    <ul class="terms" style="margin:0;padding-left:1.1em">
      <li>MetaTrader 5用です。登録やメールアドレスの入力は不要です。</li>
      <li>個人での利用は自由です。再配布・販売・改変品の配布はご遠慮ください。</li>
      <li>売買を推奨するものではなく、利益を保証するものでもありません。</li>
    </ul>
  </aside>
</div>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Features</div><h2>できること</h2></div></div>
    <div class="feats">
      <div class="feat"><h3>強い動きの起点を見つける</h3><p>3本以内にATRの1.5倍以上動き、直近10本の高値（安値）を終値で更新した動きだけを対象に、その直前の逆向きの足をOBとします。小さな動きは拾いません。</p></div>
      <div class="feat"><h3>割れたOBは消える</h3><p>買いOBは終値で下端を割ったら、売りOBは終値で上端を超えたら消えます。戻ってきた回数を「×2」のように表示するので、何度試されたかも分かります。</p></div>
      <div class="feat"><h3>上位足のOBも重ねる</h3><p>1時間足チャートではH4と日足、4時間足チャートでは日足のOBを点線の枠で重ねます。表示は現在値に近いものだけ（片側3つまで）に絞ります。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">How to read</div><h2>表示の読み方</h2></div></div>
    <div class="data-tbl" style="max-width:52em">
      <table style="min-width:0">
        <thead><tr><th>表示</th><th>意味</th></tr></thead>
        <tbody>
          <tr><td>買いOB（緑の箱）</td><td>強い上昇が始まる直前の陰線。価格が戻ると、買いが入りやすい場所</td></tr>
          <tr><td>売りOB（赤の箱）</td><td>強い下落が始まる直前の陽線。価格が戻ると、売りが入りやすい場所</td></tr>
          <tr><td>[H4] [D1]</td><td>上位足で見つかったOB（点線の枠）</td></tr>
          <tr><td>×2</td><td>OBができたあと、価格が2回戻ってきた</td></tr>
        </tbody>
      </table>
    </div>
    <p class="muted" style="font-size:13px;max-width:46em">確定した足だけで判定するため、あとから表示が変わることはありません。確定足がOBに戻ってきたときに通知することもできます。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Example</div><h2>4時間足での表示</h2></div><p>下降トレンドでは、戻りの上に売りOBが並びます。日足のOB（点線）と重なる場所は、より意識されやすい価格帯です。</p></div>
    <figure class="shot"><img src="ob-h4.jpg" alt="Million_OrderBlockをXAUUSDの4時間足に表示した画面。下降トレンドの戻りに売りオーダーブロックが並んでいる" width="1600" height="775" loading="lazy"><figcaption><b>4時間足</b>：4時間足のOB（塗りつぶし）と日足のOB（点線の枠）。SR_AutoLevelsのラインと重なる場所に注目。</figcaption></figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Combine</div><h2>3つを組み合わせて読む</h2></div></div>
    <ol class="steps" style="padding:0;margin:0">
      <li><div><b>方向：Million_DowTrend</b><p>上位足と同じ向きのトレンドかを確かめます。下降トレンドなら売りOB、上昇トレンドなら買いOBを見ます。</p></div></li>
      <li><div><b>場所：Million_OrderBlock</b><p>トレンドと同じ向きのOBまで、価格が戻ってくるのを待ちます。OBの外側が、見方が間違っていたと判断する目安になります。</p></div></li>
      <li><div><b>目標：SR_AutoLevels</b><p>進む先にある強いサポレジが、利益確定の目安です。損切りまでの幅と比べて、十分な距離があるかを確かめます。</p></div></li>
    </ol>
    <p class="muted" style="font-size:13px;max-width:46em;margin-top:14px">この組み合わせは相場を読むための考え方で、機械的に売買して利益が出ることを確かめたものではありません。最終的な判断は、ご自身で行ってください。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Install</div><h2>導入のしかた</h2></div></div>
    <ol class="steps" style="padding:0;margin:0">
      <li><div><b>ファイルをダウンロードする</b><p>上のボタンから <code>Million_OrderBlock_v100.ex5</code> をダウンロードします。</p></div></li>
      <li><div><b>MT5のフォルダに入れる</b><p>MT5の「ファイル」→「データフォルダを開く」から <code>MQL5\\Indicators</code> にファイルを置きます。</p></div></li>
      <li><div><b>MT5を再起動する</b><p>ナビゲーターの「インディケータ」に Million_OrderBlock が表示されます。</p></div></li>
      <li><div><b>チャートに付ける</b><p>チャートへドラッグして「OK」を押せば完了です。どの時間足でも使えます。</p></div></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">FAQ</div><h2>よくある質問</h2></div></div>
    <div class="faq">
      <details><summary>本当に無料ですか？</summary><p>はい、無料です。登録やメールアドレスの入力もいりません。</p></details>
      <details><summary>OBが多すぎる・少なすぎるときは？</summary><p>設定の「OBと認める値幅（ATR倍率）」を大きくすると強い動きだけ、小さくすると多くのOBを拾います。表示数は「表示数（片側）」で変えられます。</p></details>
      <details><summary>上位足のOBが表示されません</summary><p>H4・日足のデータを読み込むまで、少し時間がかかることがあります。表示されないときは、時間足を一度切り替えてください。</p></details>
      <details><summary>OBに戻ったら必ず反発しますか？</summary><p>いいえ。OBは過去に注文が集まった場所で、反発を保証するものではありません。損切りの位置や取引量は、<a href="fx-12.html">FX入門 第12章</a>の考え方を参考に、ご自身で決めてください。</p></details>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Next</div><h2>あわせて使う</h2></div></div>
    <div class="next-grid" style="max-width:52em">
      <a class="next-card" href="dow-trend.html"><span class="k">FREE</span><b>Million_DowTrend</b><span>ダウ理論でトレンドを判定。どちら向きのOBを見るかが決まります。</span></a>
      <a class="next-card" href="sr-autolevels.html"><span class="k">FREE</span><b>SR_AutoLevels</b><span>重要なサポレジを自動で引く。利益確定の目安に。</span></a>
    </div>
  </div>
</section>'''

PAGES = [
    ("index.html", "さうざーFX", "ゴールド（XAUUSD）を中心にEA・インジケーターを開発・販売するさうざーFXの公式サイト。FX入門講座も公開中。", "home", index_body),
    ("products.html", "商品一覧｜さうざーFX", "さうざーFXのEA・インジケーターの一覧。ゴールド、ビットコイン、日経225。", "products", products_body),
    ("tengan-kinryu.html", "天眼金龍｜さうざーFX", "XAUUSD H1専用EA「天眼金龍 -TripleMA-ASTシステム【ゴールド専用】」の詳細。", "products", tengan_body),
    ("beginners.html", "EAの導入手順｜さうざーFX", "EAを動かすまでに必要なものと導入の流れ。", "beginners", beginners_body),
    ("fx-basics.html", "FX入門｜さうざーFX", "FXをまったく知らない方が一から学べる入門講座。しくみ、お金の計算、注文、損切り、税金まで全15章。", "fx", fx_basics_body),
    *[(fx_slug(c["no"]), f'{c["title"]}｜FX入門 第{c["no"]}章｜さうざーFX', c["lead"][:110], "fx", (lambda c=c: fx_article_body(c))) for c in FX_CHAPTERS],
    ("course.html", "EA講座｜さうざーFX", "EAの選び方、動かし方、成績の読み方、止めどきを章ごとに学べる講座。", "course", course_body),
    ("course-oos.html", "期間を分けて確かめる｜EA講座｜さうざーFX", "バックテストを調整期間と確認期間に分けて、過剰最適化を見抜く方法。", "course", article_body),
    ("blog.html", "コラム｜さうざーFX", "FXとゴールドの基礎知識。", "blog", blog_body),
    ("about.html", "運営者情報｜さうざーFX", "さうざーFXの運営者情報。", "about", about_body),
    ("sr-autolevels.html", "SR_AutoLevels（無料）｜さうざーFX", "重要なサポート・レジスタンスを自動で引くMT5インジケーターを無料配布。H1・H4・日足のラインを重ねて表示。", "products", sr_body),
    ("dow-trend.html", "Million_DowTrend（無料）｜さうざーFX", "ダウ理論で高値・安値の切り上げと切り下げを自動判定するMT5インジケーターを無料配布。H1・H4・日足のトレンドを一覧表示。", "products", dow_body),
    ("order-block.html", "Million_OrderBlock（無料）｜さうざーFX", "オーダーブロックを自動で検出し、割れるまで表示するMT5インジケーターを無料配布。H4・日足のOBも重ねて表示。", "products", ob_body),
    ("legal.html", "免責事項・プライバシーポリシー｜さうざーFX", "免責事項、広告表記、プライバシーポリシー。", "", legal_body),
]

def build():
    for d in ("dist", "artifact"):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    for fn, title, desc, active, fn_body in PAGES:
        body = fn_body()
        with open(os.path.join(ROOT, "dist", fn), "w", encoding="utf-8") as f:
            f.write(page(title, desc, active, body, full=True))
        art_full = fn != "index.html"
        with open(os.path.join(ROOT, "artifact", fn), "w", encoding="utf-8") as f:
            f.write(page(title, desc, active, body, full=art_full))
    import shutil, glob as _g
    cols = _g.glob(os.path.join(ROOT, "cols", "*.html")) + _g.glob(os.path.join(ROOT, "img", "*"))
    for c in cols:
        for d in ("dist", "artifact"):
            shutil.copy(c, os.path.join(ROOT, d, os.path.basename(c)))
    dl_src = os.path.join(ROOT, "downloads")
    if os.path.isdir(dl_src):
        os.makedirs(os.path.join(ROOT, "dist", "downloads"), exist_ok=True)
        for f in _g.glob(os.path.join(dl_src, "*.ex5")):
            shutil.copy(f, os.path.join(ROOT, "dist", "downloads", os.path.basename(f)))
    if SITE_URL:
        from datetime import date
        urls = [p[0] for p in PAGES] + [os.path.basename(c) for c in cols if c.endswith(".html")]
        today = date.today().isoformat()
        sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for u in urls:
            loc = SITE_URL + "/" + ("" if u == "index.html" else u)
            sm.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod></url>")
        sm.append("</urlset>")
        open(os.path.join(ROOT, "dist", "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
        open(os.path.join(ROOT, "dist", "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("built", len(PAGES), "pages +", len(cols), "columns")

if __name__ == "__main__":
    build()
