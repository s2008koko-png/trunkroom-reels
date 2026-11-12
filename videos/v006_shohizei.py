"""#006 消費税のしくみ — 同じ弁当でも店内10%・持ち帰り8% (sources: 国税庁 No.6303 / No.6102 / No.6101 /
軽減税率Q&A（制度概要編）/ 飲食料品に係る2年間の消費税率引下げに関するQ&A（令和8年9月）/ 財務省 消費税について教えてください)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def bento(cx, cy):
    x, y = cx - 110, cy - 70
    return (f'<rect x="{x}" y="{y}" width="220" height="140" rx="16" fill="{BLK}"/>'
            f'<rect x="{x+12}" y="{y+12}" width="110" height="116" rx="8" fill="{WHT}"/><circle cx="{x+67}" cy="{y+70}" r="16" fill="{PNK}"/>'
            f'<rect x="{x+132}" y="{y+12}" width="76" height="52" rx="8" fill="{GRN}"/><rect x="{x+132}" y="{y+74}" width="76" height="54" rx="8" fill="{GLD}"/>')


def onigiri(cx, cy):
    return (f'<path d="M{cx} {cy-60} Q{cx+85} {cy+50} {cx+55} {cy+55} L{cx-55} {cy+55} Q{cx-85} {cy+50} {cx} {cy-60} Z" fill="{WHT}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{cx-28}" y="{cy+8}" width="56" height="47" fill="{BLK}"/>')


def bottle(cx, cy):
    return (f'<rect x="{cx-14}" y="{cy-66}" width="28" height="22" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
            f'<rect x="{cx-30}" y="{cy-46}" width="60" height="106" rx="14" fill="{BLU}" stroke="{BLK}" stroke-width="7"/>'
            f'<rect x="{cx-30}" y="{cy-10}" width="60" height="30" fill="{WHT}" stroke="{BLK}" stroke-width="5"/>')


def mug(cx, cy):
    return (f'<rect x="{cx+28}" y="{cy-20}" width="34" height="50" rx="14" fill="none" stroke="{BLK}" stroke-width="9"/>'
            f'<rect x="{cx-40}" y="{cy-40}" width="74" height="100" rx="10" fill="{GLD}" stroke="{BLK}" stroke-width="7"/>'
            f'<ellipse cx="{cx-3}" cy="{cy-44}" rx="44" ry="20" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>')


def plate(cx, cy):
    return (f'<ellipse cx="{cx}" cy="{cy+10}" rx="56" ry="50" fill="{WHT}" stroke="{BLK}" stroke-width="7"/><ellipse cx="{cx}" cy="{cy+10}" rx="30" ry="26" fill="none" stroke="{BLK}" stroke-width="4"/>'
            f'<line x1="{cx-80}" y1="{cy-45}" x2="{cx-80}" y2="{cy+60}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="{cx+80}" y1="{cy-45}" x2="{cx+80}" y2="{cy+60}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>')


def shop(x, y):
    """130x140 shop with striped awning."""
    s = f'<rect x="{x+5}" y="{y+50}" width="120" height="90" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
    for k in range(4):
        s += f'<rect x="{x-5+k*35}" y="{y+10}" width="35" height="44" fill="{PNK if k % 2 == 0 else WHT}" stroke="{BLK}" stroke-width="6"/>'
    return s + f'<rect x="{x+48}" y="{y+86}" width="34" height="54" fill="{BLK}"/>'


def office(x, y):
    """130x140 tax office: columns + roof."""
    s = f'<polygon points="{x-8},{y+46} {x+65},{y} {x+138},{y+46}" fill="{BLK}"/><rect x="{x}" y="{y+124}" width="130" height="16" fill="{BLK}"/>'
    for k in range(4):
        s += f'<rect x="{x+8+k*33}" y="{y+52}" width="16" height="70" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
    return s


def person(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy-40}" r="34" fill="#FFD9B0" stroke="{BLK}" stroke-width="7"/>'
            f'<path d="M{cx-58} {cy+70} Q{cx-58} {cy} {cx} {cy} Q{cx+58} {cy} {cx+58} {cy+70} Z" fill="{BLU}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>')


def d0(t, T):
    out = head(t, "同じ500円の弁当でも", 80, "食べる場所で税がちがう", 80)
    for k, (cx, lab, price, col, t0) in enumerate(((300, "店で食べる", 550, RED, 0.3 * T), (780, "持ち帰り", 540, GRN, 0.62 * T))):
        p = prog(t, t0, 0.6)
        val = int(round(500 + (price - 500) * p))
        inner = pill(cx, 615, lab, 44, 320, col) + bento(cx, 755 + 6 * math.sin(t * 5 + k)) + txt(cx, 940, f"{val}円", 84, col if p >= 1 else BLK)
        out += grp(cx, 770, pop(t, 0.2 + k * 0.2), card(cx - 200, 555, 400, 425, inner))
    return out


def d1(t, T):
    out = head(t, "消費税は", 84, "10%と8%の2種類", 104)
    out += grp(300, 770, pop(t, 0.2), card(100, 555, 400, 425, pill(300, 620, "10%", 60, 240, RED)))
    out += grp(780, 770, pop(t, 0.35), card(580, 555, 400, 425, pill(780, 620, "8%", 60, 240, GRN)))
    L = [(mug, 210, 760, "お酒"), (plate, 390, 760, "外食")]
    R = [(onigiri, 690, 760, "食べ物"), (bottle, 870, 760, "飲み物")]
    for k, (fn, cx, cy, lab) in enumerate(R):
        t0 = 0.45 * T + k * 0.3
        out += grp(cx, cy, pop(t, t0), fn(cx, cy + 6 * math.sin(t * 5 + k)) + txt(cx, 920, lab, 42))
    for k, (fn, cx, cy, lab) in enumerate(L):
        t0 = 0.2 * T + k * 0.3
        out += grp(cx, cy, pop(t, t0), fn(cx, cy + 6 * math.sin(t * 5 + k)) + txt(cx, 920, lab, 42))
    return out


def d2(t, T):
    out = head(t, "10%の中身", 90, "国7.8% 地方2.2%", 100)
    p = prog(t, 0.3 * T, 0.8)
    gap = 60 * p
    wl, wr = 840 * 0.78, 840 * 0.22
    out += grp(540, 660, pop(t, 0.2),
               hbar(120 - gap / 2, 600, wl, RED, 130) + hbar(120 + wl + gap / 2, 600, wr, BLU, 130))
    out += grp(120 + wl / 2, 665, pop(t, 0.3 * T + 0.5), txt(120 + wl / 2 - gap / 2, 690, "国 7.8%", 72, WHT))
    out += grp(120 + wl + wr / 2, 800, pop(t, 0.3 * T + 0.9), pill(120 + wl + wr / 2 - 30, 800, "地方 2.2%", 46, 300, BLU))
    out += grp(540, 930, pop(t, 0.75 * T), pill(540, 930, "8%は 国6.24%＋地方1.76%", 44, 720))
    return out


def d3(t, T):
    out = head(t, "払うのは私たち", 90, "納めるのはお店", 110)
    xs = [200, 540, 880]
    out += grp(xs[0], 720, pop(t, 0.2), person(xs[0], 720) + pill(xs[0], 900, "客", 46, 160))
    out += grp(xs[1], 720, pop(t, 0.35), shop(xs[1] - 65, 650) + pill(xs[1], 900, "お店", 46, 200))
    out += grp(xs[2], 720, pop(t, 0.5), office(xs[2] - 65, 650) + pill(xs[2], 900, "税務署", 46, 220))
    for k, t0 in enumerate((0.25 * T, 0.62 * T)):
        q = prog(t, t0, 0.8)
        if 0 < q < 1:
            x = xs[k] + 340 * q
            out += coin(x, 640 - 110 * math.sin(math.pi * q), 38)
        out += grp(xs[k] + 170, 600, pop(t, t0 + 0.7), txt(xs[k] + 170, 620, "→", 80))
    return out


def d4(t, T):
    out = head(t, "集めたお金の使い道", 80, "年金・医療・介護・子育て", 76)
    labs = [("年金", GLD), ("医療", PNK), ("介護", GRN), ("子育て", BLU)]
    for k, (lab, col) in enumerate(labs):
        cx = 180 + k * 240
        t0 = 0.3 * T + k * 0.13 * T
        f = prog(t, t0, 0.6)
        out += grp(cx, 800, pop(t, 0.2 + k * 0.1),
                   f'<rect x="{cx-95}" y="660" width="190" height="250" rx="26" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
                   f'<rect x="{cx-87}" y="{902-170*f:.1f}" width="174" height="{170*f:.1f}" rx="18" fill="{col}"/>' + txt(cx, 960, lab, 46))
        q = prog(t, t0 - 0.3, 0.4)
        if 0 < q < 1:
            out += coin(cx, 560 + 160 * q, 34)
    return out


def d5(t, T):
    out = head(t, "来年4月から2年間", 90, "食べ物は1%になる予定", 84)
    p = prog(t, 0.3 * T, 1.0)
    out += grp(300, 740, pop(t, 0.2), onigiri(300, 700) + bottle(420, 700))
    out += grp(700, 700, pop(t, 0.3), txt(700, 740, f"{8 - 7 * p:.0f}%", 190, GRN if p >= 1 else BLK))
    return out + follow(t, 0.55 * T)


SCENES = [
    dict(narr=["同じ500円のお弁当。", "店で食べると550円、持ち帰ると540円。"], cap="店内10% 持ち帰り8%", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.4, "pop"), ("f0.3+0.6", "tick"), ("f0.62+0.6", "ding")]),
    dict(narr=["消費税は、ふつう10パーセント。", "お酒と外食をのぞく食べ物と飲み物は、8パーセント。"], cap="食べ物・飲み物は8%", note="※定期購読の新聞も8%", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.2", "pop"), ("f0.2+0.3", "pop"), ("f0.45", "pop"), ("f0.45+0.3", "pop")]),
    dict(narr=["10パーセントのうち、7.8は国、2.2は地方へ。"], cap="国と地方で分ける", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.3", "swish"), ("f0.75", "ding")]),
    dict(narr=["払うのは、わたしたち。", "税務署に納めるのは、お店。"], cap="お店がまとめて納める", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.25", "swish"), ("f0.62", "swish")]),
    dict(narr=["使い道は、年金、医療、介護、子育て支援。"], cap="社会保障に使われる", draw=d4,
         sfx=[(0.0, "whoosh")] + [(f"f{0.3+k*0.13:.2f}", "tick") for k in range(4)]),
    dict(narr=["来年4月から2年間、食べ物は、いっパーセントになる予定。", "フォローして、お金の仕組みを学ぼう。"], cap="フォローして学ぼう", note="※法案が成立した場合（国税庁Q&amp;A）", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.3", "drop"), ("f0.55", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v006_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v006_shohizei.mp4")
