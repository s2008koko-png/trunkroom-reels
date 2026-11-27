"""#050 報酬の源泉徴収 10.21% — 原稿料・講演料などの報酬・料金を支払うときは所得税および復興特別所得税を源泉徴収。
税額：支払金額A 100万円以下＝A×10.21%／100万円超＝(A−100万円)×20.42%＋102,100円（1円未満切捨て）。
例：10万円→10,210円（手取り89,790円）、150万円→204,200円。対象：原稿料・講演料・デザインの報酬・弁護士や税理士等の報酬など。
支払者が個人で給与の支払者でないときは源泉徴収不要。消費税は原則含めた額が対象（請求書等で区分されていれば報酬額のみで可）。
源泉徴収された税金が納めすぎの場合は還付申告で還付（納めすぎがなければ還付なし）。
Sources (fetched 2026-11-27): 国税庁 No.2795・No.2792（令和8年4月1日現在法令等）/ 令和8年版 源泉徴収のあらまし 第5 / 確定申告をすれば税金が還付される方"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

GRY = "#BDBDBD"


def office(cx, cy, label="会社"):
    """Original office building ~200x280 centred on (cx, cy)."""
    out = f'<rect x="{cx-100}" y="{cy-140}" width="200" height="280" rx="10" fill="#555" stroke="{BLK}" stroke-width="8"/>'
    for r in range(3):
        for c in range(3):
            out += f'<rect x="{cx-72+c*54}" y="{cy-112+r*52}" width="36" height="32" fill="{YEL}"/>'
    out += f'<rect x="{cx-70}" y="{cy+60}" width="140" height="62" rx="8" fill="{WHT}"/>' + txt(cx, cy + 108, label, 46)
    return out


def kuni(cx, cy):
    """Original treasury building with columns ~210x170 centred on (cx, cy), labelled 国."""
    out = (f'<polygon points="{cx-105},{cy-30} {cx},{cy-85} {cx+105},{cy-30}" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<rect x="{cx-105}" y="{cy+62}" width="210" height="24" fill="{BLK}"/>')
    for k in range(4):
        out += f'<rect x="{cx-88+k*52}" y="{cy-26}" width="22" height="88" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
    return out + f'<circle cx="{cx}" cy="{cy+18}" r="40" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>' + txt(cx, cy + 36, "国", 50, WHT)


def mini(kind, x, y):
    """Original 90x90 job icons: pen | mic | paint | badge."""
    if kind == "pen":
        return (f'<g transform="rotate(40 {x+45} {y+45})"><rect x="{x+32}" y="{y-2}" width="26" height="70" fill="{BLU}" stroke="{BLK}" stroke-width="6"/>'
                f'<polygon points="{x+32},{y+68} {x+58},{y+68} {x+45},{y+96}" fill="{WHT}" stroke="{BLK}" stroke-width="6" stroke-linejoin="round"/></g>')
    if kind == "mic":
        return (f'<rect x="{x+28}" y="{y}" width="34" height="56" rx="17" fill="{RED}" stroke="{BLK}" stroke-width="6"/>'
                f'<path d="M{x+16} {y+36} Q{x+16} {y+70} {x+45} {y+70} Q{x+74} {y+70} {x+74} {y+36}" fill="none" stroke="{BLK}" stroke-width="6"/>'
                f'<line x1="{x+45}" y1="{y+70}" x2="{x+45}" y2="{y+90}" stroke="{BLK}" stroke-width="6"/><line x1="{x+25}" y1="{y+90}" x2="{x+65}" y2="{y+90}" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>')
    if kind == "paint":
        return (f'<ellipse cx="{x+45}" cy="{y+48}" rx="46" ry="38" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
                f'<circle cx="{x+24}" cy="{y+40}" r="9" fill="{RED}"/><circle cx="{x+46}" cy="{y+28}" r="9" fill="{BLU}"/><circle cx="{x+68}" cy="{y+42}" r="9" fill="{GRN}"/><circle cx="{x+52}" cy="{y+64}" r="9" fill="{BLK}"/>')
    return (f'<circle cx="{x+45}" cy="{y+40}" r="38" fill="{GLD}" stroke="{BLK}" stroke-width="6"/>' + txt(x + 45, y + 56, "士", 44)
            + f'<polygon points="{x+22},{y+70} {x+12},{y+98} {x+38},{y+84}" fill="{PNK}" stroke="{BLK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<polygon points="{x+68},{y+70} {x+78},{y+98} {x+52},{y+84}" fill="{PNK}" stroke="{BLK}" stroke-width="5" stroke-linejoin="round"/>')


def d0(t, T):
    out = head(t, "報酬10万円のはずが", 90, "振込は89,790円", 104)
    t0 = 0.45 * T
    p = prog(t, t0, 1.0)
    val = int(round(100000 - 10210 * p))
    out += card(100, 580, 600, 300, f'<rect x="100" y="580" width="600" height="80" rx="20" fill="{BLK}"/>' + txt(400, 640, "通帳 ご入金", 46, WHT)
                + txt(400, 810, f"{val:,}円", 100, PNK if p >= 1 else BLK))
    out += monster(850, 730 - 8 * abs(math.sin(t * 5)), RED, t, 0.72, chomp=0 < p < 1)
    out += grp(400, 945, pop(t, t0 + 1.0), pill(400, 945, "−10,210円", 54, 420, PNK))
    return out


def d1(t, T):
    out = head(t, "先に引かれたのは", 96, "所得税など10.21%", 100)
    out += grp(210, 740, pop(t, 0.15), office(210, 740, "払う側"))
    out += grp(800, 620, pop(t, 0.25), icon("wallet", 735, 550) + txt(900, 650, "", 40))
    out += grp(800, 728, pop(t, 0.3), txt(800, 740, "あなた", 44))
    out += grp(820, 880, pop(t, 0.4 * T), kuni(820, 880))
    for k in range(3):
        ph = (t * 0.6 + k / 3) % 1
        if t > 0.5:
            cx, cy = 320 + 400 * ph, 690 - 60 * ph - 60 * math.sin(math.pi * ph)
            out += grp(cx, cy, 1, coin(cx, cy, 34), op=clamp((1 - ph) * 5))
    if t > 0.4 * T + 0.3:
        ph = ((t - 0.4 * T - 0.3) * 0.6) % 1
        cx, cy = 320 + 390 * ph, 800 + 90 * ph - 40 * math.sin(math.pi * ph)
        out += grp(cx, cy, 1, coin(cx, cy, 30, PNK, WHT), op=clamp((1 - ph) * 5))
    out += grp(500, 950, pop(t, 0.4 * T + 0.4), pill(500, 950, "10.21%", 52, 290, PNK))
    return out


def d2(t, T):
    out = head(t, "対象になる報酬は", 96, "決まっている", 120)
    items = [("pen", "原稿料", 100, 545), ("mic", "講演料", 560, 545), ("paint", "デザイン料", 100, 775), ("badge", "弁護士など", 560, 775)]
    for k, (kind, lab, x, y) in enumerate(items):
        t0 = 0.12 * T + k * 0.2 * T
        inner = mini(kind, x + 24, y + 52) + txt(x + 268, y + 124, lab, 56 if len(lab) > 3 else 68)
        out += grp(x + 210, y + 102, pop(t, t0), card(x, y, 420, 205, inner))
    return out


def d3(t, T):
    out = head(t, "100万円をこえた分は", 84, "20.42%", 150)
    w1 = 500 * prog(t, 0.12 * T, 0.6)
    w2 = 250 * prog(t, 0.45 * T, 0.5)
    out += hbar(150, 690, w1, GLD, 120)
    out += grp(400, 750, pop(t, 0.12 * T + 0.5), txt(400, 772, "10.21%", 62))
    out += grp(400, 640, pop(t, 0.12 * T + 0.3), txt(400, 656, "100万円まで", 48))
    if w2 > 0:
        out += hbar(650, 650, w2, PNK, 160)
    out += grp(775, 730, pop(t, 0.45 * T + 0.4), txt(775, 752, "20.42%", 58, WHT))
    out += grp(775, 600, pop(t, 0.45 * T + 0.2), txt(775, 616, "こえた分", 48, PNK))
    out += grp(540, 930, pop(t, 0.72 * T), pill(540, 930, "150万円なら 204,200円", 48, 680))
    return out


def d4(t, T):
    out = head(t, "納めすぎた分は", 100, "確定申告で戻る", 110)
    out += grp(220, 760, pop(t, 0.15), kuni(220, 760))
    out += grp(820, 760, pop(t, 0.25), icon("wallet", 755, 690) + txt(820, 880, "あなた", 44))
    out += grp(520, 600, pop(t, 0.3 * T), card(380, 548, 280, 100, txt(520, 620, "確定申告", 56)))
    t0 = 0.45 * T
    for k in range(3):
        if t > t0:
            ph = ((t - t0) * 0.7 + k / 3) % 1
            cx, cy = 320 + 440 * ph, 760 - 70 * math.sin(math.pi * ph)
            out += grp(cx, cy, 1, coin(cx, cy, 34), op=clamp((1 - ph) * 5) * clamp(ph * 8))
    out += grp(520, 955, pop(t, t0 + 0.4), pill(520, 955, "多く引かれた分", 46, 420, PNK))
    return out


def d5(t, T):
    out = head(t, "引かれた税金は", 100, "申告で精算", 130)
    for k, cx in enumerate((270, 540, 810)):
        out += grp(cx, 700, pop(t, 0.2 + k * 0.15), coin(cx, 710 - 34 * abs(math.sin(t * 6 + k * 0.9)), 78))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["報酬10万円なのに、振り込みは89,790円。"], cap="10,210円が先に引かれる",
         note="※源泉徴収の対象の報酬・消費税は考えない例", draw=d0, csize=58, sfx=[(0.0, "whoosh"), ("f0.45", "drop"), ("f0.45+1.0", "ding")]),
    dict(narr=["引かれたのは、所得税など10.21パーセント。", "支払うほうが国に納めます。"], cap="払う側が国に納める",
         note="※源泉徴収。支払者が会社などの場合", draw=d1, sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.4", "pop"), ("f0.4+0.4", "ding")]),
    dict(narr=["対象は、原稿料や講演料、デザイン料など。", "弁護士や税理士の報酬もです。"], cap="原稿料・講演料など", draw=d2,
         sfx=[(0.0, "whoosh")] + [(f"f{0.12+k*0.2:.2f}", "pop") for k in range(4)]),
    dict(narr=["1回で100万円をこえた分は、20.42パーセント。", "150万円なら、204,200円です。"], cap="こえた分は20.42%",
         note="※(150万−100万)×20.42%＋102,100円", draw=d3, sfx=[(0.0, "whoosh"), ("f0.12", "swish"), ("f0.45", "swish"), ("f0.72", "ding")]),
    dict(narr=["ただし、多く引かれた分は、確定申告で戻ります。"], cap="多い分は申告で戻る",
         note="※還付申告。納めすぎがなければ戻らない", draw=d4, sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.3", "pop"), ("f0.45+0.4", "ding")]),
    dict(narr=["引かれた税金は、確定申告で精算。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v050_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v050_hoshu.mp4")
