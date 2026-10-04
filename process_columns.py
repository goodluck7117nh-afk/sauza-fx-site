# -*- coding: utf-8 -*-
"""旧サイトのコラムを新サイト用に加工する
- Vantageの紹介リンク（vpltd.co）と、IBコードの案内を削除
- ファイル名を英数字に変更
- 先頭に新サイトへ戻るバーと注記を追加（記事本体のデザインはそのまま）"""
import os, re, glob
from bs4 import BeautifulSoup

SRC = glob.glob("/home/claude/columns/*/")[0]
OUT = "/home/claude/sauza/cols"
os.makedirs(OUT, exist_ok=True)

def dec(s):
    return re.sub(r'#U([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)

# 元ファイル名 → (新ファイル名, グループ)
MAP = {
    "colum_kaigaiFX.html": ("col-kaigai-fx.html", "kaigai"),
    **{f"天眼_FX基礎知識_CHAPTER{i}.html": (f"basics-{i}.html", "kaigai") for i in range(1, 8)},
}

NOTE = {
    "ea": "このコラムのデータは、noteで販売している「天眼TripleMA-ASTシステム」のバックテストと運用記録です。GogoJungleで販売している「天眼金龍」とは、設定と成績が異なります。",
    "kaigai": "海外FX業者の多くは、日本の金融庁に登録していません。トラブルの際に日本の法律で保護されない場合があります。利用するかどうかは、リスクを理解したうえでご判断ください。",
    "tool": "",
}

def topbar(group):
    note = NOTE[group]
    note_html = (f'<div style="max-width:960px;margin:0 auto;padding:0 16px 10px;font-size:12px;line-height:1.7;color:#B9B2A2">{note}</div>'
                 if note else "")
    return BeautifulSoup(f'''<div id="sauza-topbar" style="background:#0B0E12;border-bottom:1px solid #2A2F36;font-family:'Zen Kaku Gothic New','Hiragino Sans','Yu Gothic',system-ui,sans-serif;position:relative;z-index:50">
  <div style="max-width:960px;margin:0 auto;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;font-size:13px">
    <a href="./" style="color:#D9A84A;text-decoration:none;font-weight:700;letter-spacing:.04em;display:flex;align-items:center;gap:8px"><img src="logo-mark.png" alt="" width="28" height="28" style="border-radius:6px;display:block">さうざーFX</a>
    <span style="display:flex;gap:16px;flex-wrap:wrap"><a href="blog.html" style="color:#ECEDEA;text-decoration:none">← コラム一覧</a><a href="products.html" style="color:#9BA3AA;text-decoration:none">商品一覧</a></span>
  </div>{note_html}
</div>''', "html.parser")

def strip_vantage(s):
    removed = 0
    for a in s.find_all("a", href=re.compile(r"vpltd\.co")):
        target = a
        p = a.parent
        for _ in range(3):
            if p is None or p.name in ("body", "section"):
                break
            other = p.get_text("", strip=True).replace(a.get_text("", strip=True), "")
            if p.name == "div" and len(other) < 160:
                target = p
                p = p.parent
            else:
                break
        target.decompose()
        removed += 1
    # IBリンクの注記
    for el in s.select(".vb-sub"):
        if "IB" in el.get_text():
            el.decompose()
    return removed

def fix_chapter7(s):
    # 手順1の文言
    for p in s.find_all("p"):
        if "このリンク経由" in p.get_text():
            p.string = "Vantageの公式サイトにアクセスします。URLは公式サイトの表記を確認し、似たドメインの偽サイトに注意してください。"
    # IBコードの行・注意書き
    for el in s.select(".setting-row"):
        if "IBコード" in el.get_text():
            el.decompose()
    for el in s.select(".warn-box"):
        if "IB" in el.get_text():
            el.decompose()
    # 既存口座へのIB紐付けセクション
    for sec in s.find_all("section"):
        if "すでにVantage口座をお持ちの方" in sec.get_text():
            sec.decompose()
    # 古い告知とXアカウント
    for el in s.find_all("div"):
        t = el.get_text()
        if "noteをフォロー" in t and "sauza_fx" in str(el) and len(t) < 200:
            el.clear()
            el.append(BeautifulSoup('🐦 <a href="https://x.com/alex767_fx" style="color:var(--accent);" target="_blank" rel="noopener">X（@alex767_fx）</a>で相場分析を発信しています', "html.parser"))
    for el in s.select(".cta-big"):
        el.decompose()

def fix_chapter6(s):
    # note版・旧バージョンの実績とロジック紹介を外す
    el = s.find(string=lambda t: t and "天眼TripleMA-ASTシステムの実績" in t)
    if el:
        el.parent.parent.decompose()
    lab = s.find(string=lambda t: t and "TENGAN EA LOGIC" in t)
    if lab:
        lab.find_parent("section").decompose()
    for t in s.find_all(string=lambda t: t and "（天眼EAがまさにこれ）" in t):
        t.replace_with(t.replace("（天眼EAがまさにこれ）", ""))

def process():
    report = []
    for fn in sorted(os.listdir(SRC)):
        name = dec(fn)
        if name not in MAP:
            continue
        new, group = MAP[name]
        s = BeautifulSoup(open(os.path.join(SRC, fn), encoding="utf-8"), "html.parser")
        n = strip_vantage(s)
        if "CHAPTER6" in name:
            fix_chapter6(s)
        if "CHAPTER7" in name:
            fix_chapter7(s)
        if s.title:
            s.title.string = re.sub(r"\s+", " ", s.title.get_text()).strip()
        s.body.insert(0, topbar(group))
        if s.head:
            s.head.append(BeautifulSoup('<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">', "html.parser"))
        out = str(s)
        out = re.sub(r"\s*／\s*IBコードの入力方法", "", out)
        out = out.replace("｜天眼EAのロジック概要", "").replace("天眼EAを稼働させるための", "EAを稼働させるための")
        left = len(re.findall(r"vpltd|7141165", out))
        open(os.path.join(OUT, new), "w", encoding="utf-8").write(out)
        report.append((new, group, n, left))
    for r in report:
        print(r)

if __name__ == "__main__":
    process()
