"""#002 ふるさと納税のしくみ — 自己負担は実質2,000円 (source: 総務省 ふるさと納税ポータル)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def gift(cx, cy):
    return (f'<rect x="{cx-110}" y="{cy-50}" width="220" height="150" rx="10" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="{cx-125}" y="{cy-95}" width="250" height="55" rx="10" fill="{PNK2}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="{cx-18}" y="{cy-95}" width="36" height="195" fill="{GLD}" stroke="{BLK}" stroke-width="6"/>'
            f'<ellipse cx="{cx-38}" cy="{cy-118}" rx="38" ry="24" fill="{GLD}" stroke="{BLK}" stroke-width="7"/>'
            f'<ellipse cx="{cx+38}" cy="{cy-118}" rx="38" ry="24" fill="{GLD}" stroke="{BLK}" stroke-width="7"/>')


def who(x, y, kind, label):
    return card(x, y, 300, 300, icon(kind, x + 85, y + 40) + txt(x + 150, y + 258, label, 54))


def d0(t, T):
    out = head(t, "ふるさと納税の自己負担", 70, "実質2,000円", 120)
    t0 = 0.4 * T
    p = prog(t, t0, 0.8)
    w1 = 840 * 28 / 30
    bar = (f'<rect x="120" y="610" width="840" height="120" rx="16" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>')
    if p > 0:
        bar += (f'<rect x="124" y="614" width="{w1-4:.1f}" height="112" rx="12" fill="{GRN}" opacity="{p:.2f}"/>'
                f'<rect x="{120+w1:.1f}" y="614" width="{840-w1-4:.1f}" height="112" rx="8" fill="{PNK}" opacity="{p:.2f}"/>')
    out += grp(540, 670, pop(t, 0.2), bar + txt(540, 585, "寄付 30,000円", 54))
    out += grp(540, 800, pop(t, t0 + 0.3), txt(120, 815, "28,000円 → 税金から引かれる", 46, BLK, "start"))
    out += grp(540, 920, pop(t, t0 + 0.9), txt(540, 950, "自己負担 2,000円", 84, PNK))
    return out


def d1(t, T):
    out = head(t, "好きな町に寄付すると", 76, "税金が安くなる", 110)
    out += grp(260, 740, pop(t, 0.2), who(110, 590, "wallet", "あなた")) + grp(820, 740, pop(t, 0.4), who(670, 590, "house", "好きな町"))
    p = prog(t, 0.25 * T, 0.8)
    if 0 < p < 1:
        x = 420 + 240 * p
        out += coin(x, 720 - 90 * math.sin(math.pi * p))
    out += grp(540, 730, pop(t, 0.25 * T + 0.8), txt(540, 750, "→", 110, BLK))
    out += grp(540, 950, pop(t, 0.6 * T), pill(540, 950, "翌年の税金 −28,000円", 50, 680, PNK))
    return out


def d2(t, T):
    out = head(t, "寄付した町から", 80, "お礼の品が届く", 110)
    out += grp(260, 720, pop(t, 0.2), who(110, 570, "house", "寄付した町"))
    p = prog(t, 0.3, 0.9)
    gx = 300 + 420 * p
    out += grp(gx, 730, pop(t, 0.3) * (1 + 0.04 * math.sin(t * 8)), gift(gx, 730 - 60 * math.sin(math.pi * p)), rot=6 * math.sin(t * 6))
    out += grp(540, 950, pop(t, 0.55 * T), pill(540, 950, "お礼は寄付額の3割まで", 48, 660))
    return out


def d3(t, T):
    out = head(t, "ただし上限がある", 84, "年収と家族で変わる", 96)
    out += f'<line x1="150" y1="924" x2="930" y2="924" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k, (cx, h, lab) in enumerate(((300, 130, "年収 少なめ"), (540, 220, "ふつう"), (780, 310, "多め"))):
        t0 = 0.4 + k * 0.5
        hh = h * prog(t, t0, 0.5)
        if hh > 0:
            out += f'<rect x="{cx-80}" y="{920-hh:.1f}" width="160" height="{hh:.1f}" rx="8" fill="{GRN}" stroke="{BLK}" stroke-width="6"/>'
        out += grp(cx, 920 - h - 40, pop(t, t0 + 0.45), pill(cx, 920 - h - 40, "上限", 40, 150, PNK))
        out += grp(cx, 975, pop(t, t0), txt(cx, 990, lab, 40))
    return out


def d4(t, T):
    out = head(t, "会社員で5つまでなら", 76, "確定申告いらない", 104)
    for k in range(5):
        x = 105 + k * 185
        out += grp(x + 65, 660, pop(t, 0.3 + k * 0.25), icon("house", x, 590) + f'<circle cx="{x+110}" cy="{600}" r="30" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>' + txt(x + 110, 615, str(k + 1), 40, WHT))
    out += grp(540, 890, pop(t, 0.55 * T), card(190, 800, 700, 180, txt(540, 915, "申請書を出すだけ", 76)))
    return out


def d5(t, T):
    out = head(t, "今年の分は", 80, "12月31日まで", 120)
    out += grp(300, 700, pop(t, 0.3) * (1 + 0.04 * math.sin(t * 7)), gift(300, 720), rot=5 * math.sin(t * 5))
    out += monster(760, 690 - 20 * abs(math.sin(t * 6)), BLU, t, 0.7 * pop(t, 0.5))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["ふるさと納税、自己負担は、実質2000円だけ。", "仕組みは、30秒でわかります。"], cap="寄付しても実質2,000円", note="※3万円を寄付した例・上限あり", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.4", "swish"), ("f0.4+0.9", "ding")]),
    dict(narr=["好きな町に寄付すると、2000円を超えた分だけ、税金が安くなる。"], cap="2,000円を超えた分が対象", note="※3万円を寄付した例・上限あり", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.4, "pop"), ("f0.25", "swish"), ("f0.6", "ding")]),
    dict(narr=["しかも、寄付した町から、お礼の品が届く。", "お礼は、寄付額の3割まで。"], cap="お礼は寄付額の3割まで", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.3, "swish"), ("f0.55", "pop")]),
    dict(narr=["ただし、安くなる金額には上限がある。", "上限は、年収や家族構成で変わります。"], cap="上限は人によってちがう", draw=d3,
         sfx=[(0.0, "whoosh"), (0.85, "tick"), (1.35, "tick"), (1.85, "tick")]),
    dict(narr=["会社員で、寄付先が5つまでなら、申請書を出すだけ。", "確定申告は、不要です。"], cap="寄付先は5つまで", note="※ワンストップ特例制度（総務省）", draw=d4,
         sfx=[(0.0, "whoosh")] + [(0.3 + k * 0.25, "pop") for k in range(5)] + [("f0.55", "ding")]),
    dict(narr=["今年の分は、12月31日まで。", "フォローして、お金の仕組みを学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v002_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v002_furusato.mp4")
