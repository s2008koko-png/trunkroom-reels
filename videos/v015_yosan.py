"""#015 国の予算の使い道 — 令和8年度一般会計 約122兆円。1位 社会保障 約39兆円(31.9%)、2位 国債費 約31兆円(25.6%)、
地方交付税交付金等17.1%・防衛7.3%・公共事業5.0%・文教及び科学振興4.9%。入るお金は税収 約84兆円(68.5%)、国債 約30兆円(24.2%)。
Sources (fetched 2026-11-15): 財務省 日本の財政関係資料（令和8年4月）202604_00.pdf / 令和8年度予算のポイント 01.pdf / 広報誌ファイナンス 特集 令和8年度予算について"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

PUR, TEA, GRY = "#8E5BFF", "#00B8C4", "#9A9A9A"
PARTS = [(0.319, PNK), (0.256, BLU), (0.171, GRN), (0.073, RED), (0.050, PUR), (0.049, TEA), (0.082, GRY)]
NOTE = "※令和8年度 一般会計予算（財務省）"


def pie(cx, cy, r, sweep=1.0, hi=None, spin=0.0):
    """Original pie chart drawn clockwise from 12 o'clock; sweep 0..1 reveals it; hi = index pulled out."""
    out = f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="{BLK}"/>'
    a0 = 0.0
    for k, (f, col) in enumerate(PARTS):
        a1 = min(a0 + f, sweep)
        if a1 <= a0:
            break
        s, e = 2 * math.pi * a0 - math.pi / 2 + spin, 2 * math.pi * a1 - math.pi / 2 + spin
        mid = (s + e) / 2
        off = 26 if hi == k else 0
        ox, oy = cx + off * math.cos(mid), cy + off * math.sin(mid)
        c = col if hi is None or hi == k else "#D9D9D9"
        out += (f'<path d="M{ox:.1f} {oy:.1f} L{ox+r*math.cos(s):.1f} {oy+r*math.sin(s):.1f} A{r} {r} 0 {1 if e-s > math.pi else 0} 1 {ox+r*math.cos(e):.1f} {oy+r*math.sin(e):.1f} Z" '
                f'fill="{c}" stroke="{BLK}" stroke-width="6" stroke-linejoin="round"/>')
        a0 += f
    return out


def d0(t, T):
    out = head(t, "国の1年の予算", 88, "約122兆円", 140)
    p = prog(t, 0.15, 0.45 * T)
    out += pie(300, 770, 190, sweep=p)
    val = int(round(122 * p))
    out += txt(765, 750, f"{val}兆円", 100, PNK if p >= 1 else BLK)
    out += grp(745, 890, pop(t, 0.6 * T) * (1 + 0.05 * math.sin(t * 9)), pill(745, 890, "何に使う？", 54, 360))
    return out


def d1(t, T):
    out = head(t, "1位は社会保障", 88, "約39兆円", 140)
    out += grp(290, 770, pop(t, 0.1), pie(290, 770, 180, hi=0))
    for k, lab in enumerate(("年金", "医療", "介護", "子育て")):
        cx, cy = 660 + (k % 2) * 220, 660 + (k // 2) * 150
        out += grp(cx, cy, pop(t, 0.35 * T + k * 0.3), pill(cx, cy, lab, 54, 200, PNK))
    return out + grp(770, 950, pop(t, 0.35 * T + 1.3), txt(770, 965, "全体の約3割", 50))


def d2(t, T):
    out = head(t, "2位は国債費 約31兆円", 80, "借金の返済と利子", 104)
    out += grp(290, 770, pop(t, 0.1), pie(290, 770, 180, hi=1))
    note = card(600, 590, 340, 250) + txt(770, 670, "国の借金", 56) + txt(770, 760, "返済＋利子", 56, BLU)
    out += grp(770, 715, pop(t, 0.3 * T), note, rot=3 * math.sin(t * 4))
    if t > 0.3 * T + 0.3:
        q = ((t - 0.3 * T - 0.3) / 1.0) % 1.0
        out += coin(420 + 200 * q, 900 - 60 * math.sin(math.pi * q), 34)
    return out + grp(770, 930, pop(t, 0.55 * T), pill(770, 930, "25.6%", 56, 240, BLU))


def d3(t, T):
    out = head(t, "そのほかの使い道", 88, "地方・防衛・公共事業", 88)
    rows = [("地方に配るお金", 17.1, GRN), ("防衛", 7.3, RED), ("公共事業", 5.0, PUR), ("教育・科学", 4.9, TEA)]
    for k, (lab, v, col) in enumerate(rows):
        t0 = 0.08 * T + k * 0.2 * T
        y = 545 + k * 112
        out += grp(260, y + 50, pop(t, t0, 0.3), txt(120, y + 68, lab, 46, BLK, "start"))
        out += hbar(470, y + 18, v * 20 * prog(t, t0 + 0.1, 0.5), col, 70)
        out += grp(470 + v * 20 + 90, y + 50, pop(t, t0 + 0.5, 0.3), txt(470 + v * 20 + 18, y + 70, f"{v}%", 48, BLK, "start"))
    return out


def d4(t, T):
    out = head(t, "お金はどこから？", 88, "税金 約84兆円", 120)
    x, y, w = 110, 600, 860
    segs = [(0.685, GLD, "税金", "約84兆円", 0.1 * T), (0.242, PNK, "国債", "約30兆円", 0.5 * T), (0.073, GRY, "", "", 0.5 * T + 0.6)]
    out += f'<rect x="{x}" y="{y}" width="{w}" height="130" rx="16" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    a = 0.0
    for f, col, lab, val, t0 in segs:
        p = prog(t, t0, 0.7)
        if p > 0.01:
            out += f'<rect x="{x+4+(w-8)*a:.1f}" y="{y+4}" width="{(w-8)*f*p:.1f}" height="122" fill="{col}" stroke="{BLK}" stroke-width="4"/>'
        cx = x + w * (a + f / 2)
        if lab:
            out += grp(cx, 800, pop(t, t0 + 0.5), txt(cx, 810, lab, 64, BLK) + txt(cx, 880, val, 52, PNK if lab == "国債" else BLK))
        a += f
    out += grp(770, 960, pop(t, 0.5 * T + 0.9), pill(760, 960, "国債＝国の借金", 44, 400, PNK))
    return out


def d5(t, T):
    out = head(t, "税金の使い道を", 88, "知っておこう", 124)
    out += grp(540, 700, pop(t, 0.2), pie(540, 700, 130, spin=t * 0.8))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["国の予算は、1年で約122兆円。", "何に使っているでしょう。"], cap="国の予算 約122兆円", note=NOTE, draw=d0,
         sfx=[(0.0, "whoosh"), (0.15, "swish"), ("f0.45+0.15", "ding"), ("f0.6", "pop")]),
    dict(narr=["1位は社会保障、約39兆円。", "年金、医療、介護、子育てです。"], cap="社会保障が約3割", note="※社会保障関係費 31.9%", draw=d1,
         sfx=[(0.0, "whoosh")] + [(f"f0.35+{k*0.3:.2f}", "pop") for k in range(4)]),
    dict(narr=["2位は国債費、約31兆円。", "借金の返済と利子です。"], cap="国債費は約31兆円", note="※国債費 25.6%", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.3", "pop"), ("f0.55", "ding")]),
    dict(narr=["3位は、地方に配るお金。", "防衛、公共事業、教育と科学が続きます。"], cap="地方に約17%", note="※地方交付税交付金等・文教及び科学振興", draw=d3,
         sfx=[(0.0, "whoosh")] + [(f"f{0.08+k*0.2:.2f}", "tick") for k in range(4)]),
    dict(narr=["入るお金は、税金が約84兆円。", "約30兆円は国債、つまり借金です。"], cap="税金84兆円 国債30兆円", csize=56, note="※税収68.5%・公債金24.2%", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.1", "tick"), ("f0.5", "drop"), ("f0.5+0.9", "pop")]),
    dict(narr=["使い道を知っておこう。", "フォローして、お金を学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v015_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v015_yosan.mp4")
