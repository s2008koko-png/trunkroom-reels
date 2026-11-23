"""#036 社会保険料控除 — 自分や生計を一にする家族の社会保険料を払ったら、その年に払った全額を所得から引ける・
給料から差し引かれた分も全額・国民年金は証明書を年末調整（保険料控除申告書）で提出・
家族の年金から天引きされた保険料は、払ったのがその家族なので自分の控除にはならない。
Sources (fetched 2026-11-23): 国税庁 No.1130 社会保険料控除 / 同Q&A（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

SKIN = "#FFD9B0"


def person(cx, cy, col, s=1.0):
    p = (f'<path d="M{cx-60} {cy+100} L{cx-60} {cy+30} Q{cx-60} {cy-20} {cx} {cy-20} Q{cx+60} {cy-20} {cx+60} {cy+30} L{cx+60} {cy+100} Z" fill="{col}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-58}" r="42" fill="{SKIN}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx-14}" cy="{cy-60}" r="5" fill="{BLK}"/><circle cx="{cx+14}" cy="{cy-60}" r="5" fill="{BLK}"/>'
         f'<path d="M{cx-12} {cy-44} Q{cx} {cy-34} {cx+12} {cy-44}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy, s, p)


def book(cx, cy, label, col=BLU, w=200, h=250):
    """A small notebook with a spine and a label."""
    x, y = cx - w / 2, cy - h / 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="{x}" y="{y}" width="34" height="{h}" rx="10" fill="{BLK}" opacity="0.35"/>'
            f'<rect x="{x+50}" y="{y+70}" width="{w-70}" height="90" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="5"/>'
            + txt(x + 50 + (w - 70) / 2, y + 133, label, 46))


def paper(cx, cy, title, w=230, h=280):
    x, y = cx - w / 2, cy - h / 2
    p = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>' + txt(cx, y + 70, title, 46)
    for k in range(3):
        p += f'<rect x="{x+30}" y="{y+110+k*42}" width="{w-60-(40 if k == 2 else 0)}" height="16" rx="6" fill="#BBB"/>'
    p += f'<circle cx="{x+w-52}" cy="{y+h-48}" r="26" fill="none" stroke="{PNK}" stroke-width="7"/>'
    return p


def office(cx, cy, label):
    """Simple office block centred on (cx, cy)."""
    x, y = cx - 130, cy - 170
    b = f'<rect x="{x}" y="{y}" width="260" height="340" fill="#DDE6F5" stroke="{BLK}" stroke-width="8"/>'
    for r in range(3):
        for c in range(3):
            b += f'<rect x="{x+34+c*72}" y="{y+34+r*66}" width="48" height="42" fill="{BLU}" stroke="{BLK}" stroke-width="5"/>'
    b += f'<rect x="{cx-36}" y="{y+250}" width="72" height="90" fill="{BLK}"/>'
    return b + pill(cx, y - 44, label, 44, 220)


def cross(cx, cy, r=70):
    return (f'<line x1="{cx-r}" y1="{cy-r}" x2="{cx+r}" y2="{cy+r}" stroke="{PNK}" stroke-width="26" stroke-linecap="round"/>'
            f'<line x1="{cx+r}" y1="{cy-r}" x2="{cx-r}" y2="{cy+r}" stroke="{PNK}" stroke-width="26" stroke-linecap="round"/>')


def d0(t, T):
    out = head(t, "子どもの年金を払ったら", 80, "親の税金がへる", 116)
    out += person(200, 740, BLU, pop(t, 0.1)) + grp(200, 890, pop(t, 0.2), txt(200, 905, "親", 50))
    out += person(470, 770, GRN, 0.78 * pop(t, 0.2)) + grp(470, 890, pop(t, 0.3), txt(470, 905, "子", 50))
    out += grp(820, 730, pop(t, 0.3), book(820, 730, "年金"))
    t0 = 0.35 * T
    p = prog(t, t0, 0.9)
    if 0 < p < 1:
        out += coin(300 + 470 * p, 700 - 190 * math.sin(math.pi * p), 44)
    out += grp(540, 965, pop(t, t0 + 0.9), pill(540, 965, "払った親が 控除を使える", 44, 620, PNK))
    return out


def d1(t, T):
    out = head(t, "払った保険料は", 90, "全額 引ける", 130)
    x0, y0, w, h, cut = 120, 640, 800, 120, 250
    t0 = 0.45 * T
    p = prog(t, t0, 0.7)
    out += grp(540, 600, pop(t, 0.15), txt(x0, 615, "所得（1年のもうけ）", 46, BLK, "start"))
    out += grp(540, 700, pop(t, 0.2), f'<rect x="{x0}" y="{y0}" width="{w-cut}" height="{h}" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>')
    dy = 170 * p
    piece = (f'<rect x="{x0+w-cut}" y="{y0+dy:.1f}" width="{cut}" height="{h}" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
             + txt(x0 + w - cut / 2, y0 + dy + 78, "保険料", 50, WHT))
    out += grp(540, 700, pop(t, 0.2), piece, rot=0)
    if p > 0:
        out += f'<line x1="{x0+w-cut}" y1="{y0-20}" x2="{x0+w-cut}" y2="{y0+h+20}" stroke="{BLK}" stroke-width="8" stroke-dasharray="14 12" opacity="{1-p*0.6:.2f}"/>'
    out += grp(x0 + (w - cut) / 2, y0 + 60, pop(t, t0 + 0.6), txt(x0 + (w - cut) / 2, y0 + 78, "税金の計算はここだけ", 46))
    out += grp(380, 900, pop(t, t0 + 0.9), pill(380, 900, "その年に払った全額", 44, 480))
    return out


def d2(t, T):
    out = head(t, "給料から引かれた分も", 84, "ぜんぶ対象", 130)
    items = [("健康保険", BLU), ("年金", GRN), ("介護保険", RED), ("雇用保険", PNK)]
    for k, (lab, col) in enumerate(items):
        x, y = 100 + (k % 2) * 460, 545 + (k // 2) * 230
        t0 = 0.25 * T + k * 0.38
        inner = (f'<circle cx="{x+80}" cy="{y+102}" r="46" fill="{col}" stroke="{BLK}" stroke-width="7"/>'
                 f'<path d="M{x+58} {y+102} L{x+74} {y+120} L{x+104} {y+82}" fill="none" stroke="{WHT}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
                 + txt(x + 270, y + 124, lab, 60))
        out += grp(x + 210, y + 102, pop(t, t0), card(x, y, 420, 205, inner))
    return out


def d3(t, T):
    out = head(t, "自分で払った国民年金は", 76, "証明書がいる", 130)
    out += grp(800, 790, pop(t, 0.2), office(800, 790, "会社"))
    p = prog(t, 0.45 * T, 1.0)
    x = 250 + 330 * p
    out += grp(x, 760, pop(t, 0.15) * (1 - 0.35 * p), paper(x, 760 - 60 * math.sin(math.pi * p), "証明書"), rot=-6 + 6 * p)
    out += grp(300, 965, pop(t, 0.45 * T + 0.9), pill(300, 965, "年末調整で出す", 44, 400, PNK))
    return out


def d4(t, T):
    out = head(t, "家族の年金から天引き", 84, "その分は引けない", 110)
    out += person(220, 720, PNK, pop(t, 0.15)) + grp(220, 870, pop(t, 0.25), txt(220, 885, "妻の年金", 46))
    t0 = 0.3 * T
    p = prog(t, t0, 0.8)
    for k in range(3):
        out += grp(360 + k * 60, 760, pop(t, 0.3 + k * 0.1), coin(360 + k * 60, 760, 36))
    if p > 0:
        out += coin(480 + 60 * p, 760 - 150 * p, 36, PNK, WHT)
        out += grp(600, 580, pop(t, t0 + 0.5), pill(600, 580, "保険料", 40, 200, PNK))
    out += person(830, 720, BLU, pop(t, 0.25)) + grp(830, 870, pop(t, 0.35), txt(830, 885, "夫", 46))
    out += grp(830, 720, pop(t, 0.62 * T), cross(830, 700, 80))
    out += grp(540, 965, pop(t, 0.62 * T + 0.4), pill(540, 965, "払った人が 引くルール", 44, 580))
    return out


def d5(t, T):
    out = head(t, "年末調整の前に", 90, "保険料をチェック", 110)
    out += grp(270, 700, pop(t, 0.2), paper(270, 700 - 12 * abs(math.sin(t * 5)), "証明書", 200, 240), rot=-5)
    out += grp(540, 700, pop(t, 0.35), book(540, 700 - 12 * abs(math.sin(t * 5 + 1)), "年金", BLU, 180, 220))
    out += grp(810, 700, pop(t, 0.5), coin(810, 700 - 12 * abs(math.sin(t * 5 + 2)), 62))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["子どもの国民年金を、親が払ったら、親の税金がへります。"], cap="家族の保険料も対象", note="※生計が同じ家族の分・へる額は人による", draw=d0,
         sfx=[(0.0, "whoosh"), (0.1, "pop"), ("f0.35", "swish"), ("f0.35+0.9", "ding")]),
    dict(narr=["これが、社会保険料控除。", "払った全額を、所得から引けます。"], cap="社会保険料控除", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "drop"), ("f0.45+0.9", "pop")]),
    dict(narr=["給料から引かれた分も、対象です。", "健康保険、年金、介護保険などです。"], cap="天引きの保険料も全額", draw=d2,
         sfx=[(0.0, "whoosh")] + [(f"f0.25+{k*0.38:.2f}", "pop") for k in range(4)]),
    dict(narr=["自分で払った国民年金は、証明書がいります。", "年末調整で、会社に出します。"], cap="証明書を会社に出す", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "swish"), ("f0.45+0.9", "ding")]),
    dict(narr=["ただし、家族の年金から天引きされた分は、引けません。", "払った人が、引くルールです。"], cap="引けるのは払った人", draw=d4,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.3", "tick"), ("f0.62", "drop")]),
    dict(narr=["年末調整の前に、たしかめよう。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v036_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v036_shaho.mp4")
