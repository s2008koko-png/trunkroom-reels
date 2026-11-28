"""#053 ひとり親控除 — 控除額35万円（所得から引く所得控除）。
要件：その年12月31日の現況で婚姻をしていない（または配偶者の生死が明らかでない）人で、
(1) 事実上婚姻関係と同様の事情にあると認められる人がいない (2) 生計を一にする子がいる
（子の総所得金額等が令和8年分は62万円以下・他の人の同一生計配偶者や扶養親族でない） (3) 合計所得金額500万円以下。
給与所得だけなら給与の収入金額6,777,778円以下で合計所得金額500万円以下。子の年齢に制限なし（Q&A）。
会社員は扶養控除等（異動）申告書で申告（年末調整）。計算例：税率10%なら所得税は35万円×10%＝3万5千円へる。
Sources (fetched 2026-11-28): 国税庁 No.1171 ひとり親控除・同Q&A（令和8年4月1日現在法令等）/
令和8年分 年末調整のしかた 2 各種控除額の確認 https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/105.pdf"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

GRY = "#BDBDBD"


def person(cx, cy, col, s=1.0):
    """Original simple person ~150x230 at s=1, feet at cy+115."""
    out = (f'<path d="M{cx-75} {cy+115} L{cx-75} {cy+30} Q{cx-75} {cy-25} {cx} {cy-25} Q{cx+75} {cy-25} {cx+75} {cy+30} L{cx+75} {cy+115} Z" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<circle cx="{cx}" cy="{cy-68}" r="48" fill="#FFD9B0" stroke="{BLK}" stroke-width="8"/>'
           f'<circle cx="{cx-16}" cy="{cy-72}" r="6" fill="{BLK}"/><circle cx="{cx+16}" cy="{cy-72}" r="6" fill="{BLK}"/>'
           f'<path d="M{cx-14} {cy-52} Q{cx} {cy-40} {cx+14} {cy-52}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy + 115, s, out)


def check(cx, cy, r=34):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GRN}" stroke="{BLK}" stroke-width="6"/>'
            f'<path d="M{cx-r*0.45:.1f} {cy} L{cx-r*0.1:.1f} {cy+r*0.38:.1f} L{cx+r*0.5:.1f} {cy-r*0.35:.1f}" fill="none" stroke="{WHT}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')


def d0(t, T):
    out = head(t, "ひとりで子育て中の人", 84, "35万円 引ける", 130)
    b = 8 * abs(math.sin(t * 4))
    out += person(190, 760 - b, PNK, 1.0) + person(340, 760 - b * 0.6, BLU, 0.6)
    t0 = 0.45 * T
    p = prog(t, t0, 1.0)
    out += grp(700, 590, pop(t, 0.2), txt(700, 608, "税金がかかる所得", 46))
    w = 480 - 150 * p
    out += f'<rect x="460" y="650" width="480" height="120" rx="12" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-dasharray="16 12"/>'
    out += f'<rect x="460" y="650" width="{w:.1f}" height="120" rx="12" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>'
    out += grp(700, 880, pop(t, t0 + 0.6), pill(700, 880, "−35万円", 70, 420, PNK))
    return out


def d1(t, T):
    out = head(t, "条件は", 100, "この3つ", 140)
    rows = ["結婚していない", "生計が同じ子がいる", "所得500万円以下"]
    for k, lab in enumerate(rows):
        y, t0 = 545 + k * 150, 0.12 * T + k * 0.24 * T
        inner = txt(250, y + 86, lab, 60, BLK, "start")
        out += grp(540, y + 65, pop(t, t0), card(120, y, 840, 130, inner))
        out += grp(185, y + 65, pop(t, t0 + 0.3), check(185, y + 65))
    return out


def d2(t, T):
    out = head(t, "給料だけの人なら", 100, "年収約677万円まで", 96)
    x0, x1, y = 140, 940, 760
    sx = lambda v: x0 + (x1 - x0) * v / 1000
    p = prog(t, 0.2 * T, 1.2)
    xm = sx(677.8 * p)
    out += f'<rect x="{x0}" y="{y-40}" width="{x1-x0}" height="80" rx="12" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    if xm - x0 > 8:
        out += f'<rect x="{x0+4}" y="{y-36}" width="{xm-x0-4:.1f}" height="72" rx="8" fill="{GRN}"/>'
    for v in (0, 250, 500, 750, 1000):
        out += f'<line x1="{sx(v)}" y1="{y+40}" x2="{sx(v)}" y2="{y+62}" stroke="{BLK}" stroke-width="6"/>' + txt(sx(v), y + 108, f"{v}万" if v else "0", 36)
    out += f'<polygon points="{xm-26:.1f},{y-96} {xm+26:.1f},{y-96} {xm:.1f},{y-48}" fill="{PNK}" stroke="{BLK}" stroke-width="6" stroke-linejoin="round"/>'
    out += grp(xm, y - 140, pop(t, 0.2 * T + 1.2), pill(min(xm, 760), y - 150, "約677万円", 52, 340, PNK))
    out += grp(540, 950, pop(t, 0.7 * T), pill(540, 950, "ここまでが対象", 50, 440))
    return out


def d3(t, T):
    out = head(t, "子どもの年齢は", 100, "決まりなし", 140)
    kids = [(230, 0.55, GRN, "5歳"), (500, 0.8, BLU, "15歳"), (790, 1.0, RED, "25歳")]
    for k, (cx, s, col, lab) in enumerate(kids):
        t0 = 0.1 * T + k * 0.14 * T
        out += person(cx, 705 - 6 * abs(math.sin(t * 5 + k)), col, s * pop(t, t0))
        out += grp(cx, 870, pop(t, t0 + 0.2), txt(cx, 888, lab, 56))
    out += grp(540, 955, pop(t, 0.6 * T), pill(540, 955, "子の所得が62万円以下", 48, 620, PNK))
    return out


def d4(t, T):
    out = head(t, "35万円がもどる", 100, "わけではない", 130)
    out += grp(350, 580, pop(t, 0.15), txt(140, 598, "所得から引く額", 46, BLK, "start"))
    out += hbar(140, 620, 760 * prog(t, 0.2, 0.7), GLD, 110)
    out += grp(520, 675, pop(t, 0.7), txt(520, 700, "35万円", 72))
    t0 = 0.5 * T
    out += grp(350, 800, pop(t, t0), txt(140, 818, "へる所得税（税率10%）", 46, PNK, "start"))
    out += hbar(140, 840, 76 * prog(t, t0 + 0.1, 0.5), PNK, 110)
    out += grp(420, 895, pop(t, t0 + 0.5), txt(246, 922, "3万5千円", 76, PNK, "start"))
    return out


def d5(t, T):
    out = head(t, "会社員は", 100, "年末調整で申告", 120)
    y = 545
    form = (f'<rect x="150" y="{y}" width="330" height="290" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="150" y="{y}" width="330" height="60" rx="14" fill="{BLK}"/>' + txt(315, y + 44, "申告書", 40, WHT))
    for k in range(3):
        form += f'<line x1="185" y1="{y+110+k*60}" x2="{340 + (k % 2) * 60}" y2="{y+110+k*60}" stroke="{GRY}" stroke-width="12" stroke-linecap="round"/>'
    out += grp(315, y + 145, pop(t, 0.2), form)
    out += grp(420, y + 225, pop(t, 0.2 * T + 0.5), check(420, y + 225, 44))
    b = 8 * abs(math.sin(t * 5))
    out += person(690, 690 - b, PNK, 0.9 * pop(t, 0.3)) + person(830, 690 - b * 0.6, BLU, 0.55 * pop(t, 0.4))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["ひとりで子どもを育てている人は、所得から35万円引けます。"], cap="ひとり親控除は35万円",
         note="※条件あり。税金の計算で所得から引く", draw=d0, sfx=[(0.0, "whoosh"), ("f0.45", "drop"), ("f0.45+0.6", "ding")]),
    dict(narr=["条件は3つ。", "結婚していない、生計が同じ子どもがいる、所得が500万円以下。"], cap="3つともあてはまる人",
         note="※事実婚の相手がいる人は対象外", draw=d1, sfx=[(0.0, "whoosh")] + [(f"f{0.12+k*0.24:.2f}", "pop") for k in range(3)]),
    dict(narr=["給料だけの人なら、年収およそ677万円までが対象です。"], cap="年収約677万円まで",
         note="※給与収入6,777,778円以下", draw=d2, sfx=[(0.0, "whoosh"), ("f0.2", "swish"), ("f0.2+1.2", "ding")]),
    dict(narr=["子どもの年齢に、決まりはありません。", "子どもの所得は、62万円以下が条件。"], cap="子の所得は62万円以下",
         note="※令和8年分。子の総所得金額等", draw=d3, sfx=[(0.0, "whoosh")] + [(f"f{0.1+k*0.14:.2f}", "pop") for k in range(3)] + [("f0.6", "ding")]),
    dict(narr=["ただし、35万円がもどるわけではありません。", "税率10パーセントなら、へる所得税は3万5千円。"], cap="へるのは税率のぶん",
         note="※所得税率10%の場合の計算例", draw=d4, sfx=[(0.0, "whoosh"), (0.2, "swish"), ("f0.5", "pop"), ("f0.5+0.5", "ding")]),
    dict(narr=["会社員は、年末調整で申告。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.2+0.5", "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v053_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v053_hitorioya.mp4")
