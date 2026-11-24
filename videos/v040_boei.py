"""#040 防衛特別所得税 — 令和9年（2027年）1月1日以後の所得から、所得税額の1%の防衛特別所得税が始まる・
同時に復興特別所得税が2.1%→1.1%に下がる・合計2.1%は変わらず源泉徴収税額の計算方法に変更なし・
復興特別所得税の課税期間は令和19年末→令和29年末まで10年間延長。
Sources (fetched 2026-11-24): 国税庁 防衛特別所得税及び復興特別所得税に関するQ&A（令和8年5月） /
防衛特別所得税及び復興特別所得税の源泉徴収のあらまし（令和9年1月以後の源泉徴収） / 財務省 令和8年度税制改正パンフレット（防衛力強化に係る財源確保のための税制措置）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

PUR, TEA = "#8E5BD9", "#19A7A7"   # 防衛特別所得税 / 復興特別所得税


def calendar(cx, cy, top, big, sy=1.0):
    """Original tear-off calendar, 300x320, centred on (cx, cy); sy squashes it vertically for a flip."""
    x, y = cx - 150, cy - 160
    c = (f'<rect x="{x}" y="{y}" width="300" height="320" rx="22" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<path d="M{x} {y+90} L{x} {y+22} Q{x} {y} {x+22} {y} L{x+278} {y} Q{x+300} {y} {x+300} {y+22} L{x+300} {y+90} Z" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
         + txt(cx, y + 64, top, 50, WHT) + txt(cx, y + 250, big, 130))
    for k in (70, 230):
        c += f'<rect x="{x+k-9}" y="{y-24}" width="18" height="50" rx="9" fill="{BLK}"/>'
    return f'<g transform="translate(0,{cy:.1f}) scale(1,{max(sy, 0.02):.3f}) translate(0,{-cy:.1f})">{c}</g>'


def d0(t, T):
    out = head(t, "2027年1月から", 96, "新しい税金がはじまる", 90)
    t0 = 0.3 * T
    x = clamp((t - t0) / 0.5)
    sy = abs(math.cos(math.pi * x))
    out += calendar(270, 740, "2026年", "12月", sy) if x < 0.5 else calendar(270, 740, "2027年", "1月", sy)
    t1 = 0.55 * T
    out += monster(760, 720 - 14 * abs(math.sin(t * 5)), PUR, t, 0.9 * pop(t, t1))
    out += grp(760, 950, pop(t, t1 + 0.3), pill(760, 950, "防衛特別所得税", 46, 430))
    return out


def d1(t, T):
    out = head(t, "所得税の額に", 90, "1% 上乗せ", 140)
    w = 680 * prog(t, 0.2, 0.7)
    out += hbar(120, 640, w, RED, 130)
    out += grp(460, 705, pop(t, 0.7), txt(460, 726, "所得税の額", 60, WHT))
    t0 = 0.5 * T
    out += grp(860, 705, pop(t, t0), f'<rect x="810" y="640" width="100" height="130" rx="8" fill="{PUR}" stroke="{BLK}" stroke-width="6"/>')
    out += grp(860, 590, pop(t, t0 + 0.2), txt(860, 610, "＋1%", 64, PUR))
    out += grp(400, 900, pop(t, t0 + 0.5), pill(400, 900, "所得税の額 × 1%", 48, 500, PNK))
    out += monster(850, 900, PUR, t, 0.5 * pop(t, t0 + 0.3))
    return out


def d2(t, T):
    out = head(t, "かわりに 復興の税が", 84, "2.1% → 1.1%", 130)
    t0 = 0.5 * T
    p = prog(t, t0, 1.0)
    out += grp(540, 600, pop(t, 0.2), txt(540, 618, "復興特別所得税", 56))
    out += f'<rect x="120" y="650" width="840" height="110" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="120" y="650" width="{840-400*p:.1f}" height="110" rx="14" fill="{TEA}" stroke="{BLK}" stroke-width="8"/>'
    v = 2.1 - 1.0 * p
    out += grp(540, 890, pop(t, 0.35), txt(540, 940, f"{v:.1f}%", 150, PNK if p >= 1 else BLK))
    return out


def d3(t, T):
    out = head(t, "合わせると", 90, "2.1%のまま", 140)
    base, u = 940, 140
    out += f'<line x1="130" y1="{base+4}" x2="950" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    h1 = 2.1 * u * prog(t, 0.2, 0.6)
    out += f'<rect x="170" y="{base-h1:.1f}" width="260" height="{h1:.1f}" fill="{TEA}" stroke="{BLK}" stroke-width="8"/>'
    out += grp(300, base - 147, pop(t, 0.7), txt(300, base - 130, "復興 2.1%", 44, WHT))
    out += grp(300, 590, pop(t, 0.3), txt(300, 606, "いま", 50))
    t0 = 0.3 * T
    h2 = 1.1 * u * prog(t, t0, 0.5)
    h3 = 1.0 * u * prog(t, t0 + 0.5, 0.5)
    if h2 > 0:
        out += f'<rect x="650" y="{base-h2:.1f}" width="260" height="{h2:.1f}" fill="{TEA}" stroke="{BLK}" stroke-width="8"/>'
        out += grp(780, base - 77, pop(t, t0 + 0.4), txt(780, base - 62, "復興 1.1%", 44, WHT))
    if h3 > 0:
        out += f'<rect x="650" y="{base-1.1*u-h3:.1f}" width="260" height="{h3:.1f}" fill="{PUR}" stroke="{BLK}" stroke-width="8"/>'
        out += grp(780, base - 224, pop(t, t0 + 0.9), txt(780, base - 208, "防衛 1%", 44, WHT))
    out += grp(780, 590, pop(t, t0), txt(780, 606, "2027年から", 50))
    out += grp(540, 790, pop(t, 0.65 * T), txt(540, 830, "＝", 130, PNK))
    return out


def d4(t, T):
    out = head(t, "ただし 復興の税は", 86, "10年 長くなる", 120)
    out += f'<line x1="120" y1="800" x2="960" y2="800" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    out += hbar(120, 700, 420 * prog(t, 0.2, 0.6), TEA, 80)
    t0 = 0.45 * T
    out += hbar(540, 700, 400 * prog(t, t0, 0.9), PNK, 80)
    out += grp(380, 650, pop(t, 0.5), txt(380, 668, "令和19年まで", 46))
    out += grp(740, 640, pop(t, t0 + 0.3), pill(740, 640, "＋10年", 50, 260, PNK))
    out += grp(690, 900, pop(t, t0 + 0.9), txt(690, 925, "令和29年まで", 70, PNK))
    out += monster(220, 900, TEA, t, 0.45 * pop(t, 0.3), chomp=False)
    return out


def d5(t, T):
    out = head(t, "合計は同じ", 90, "期間が10年のびる", 104)
    for k, (cx, col) in enumerate(((330, PUR), (750, TEA))):
        out += monster(cx, 690 - 24 * abs(math.sin(t * 6 + k * 0.8)), col, t + k * 0.2, 0.62 * pop(t, 0.3 + k * 0.15))
    out += grp(540, 690, pop(t, 0.6), txt(540, 720, "＋", 100))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["2027年の1月から、新しい税金がはじまります。", "名前は、防衛特別所得税。"], cap="防衛特別所得税", note="※令和9年1月1日以後の所得から", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.3", "swish"), ("f0.55", "pop"), ("f0.55+0.3", "ding")]),
    dict(narr=["所得税の額に、1パーセントを上乗せする税金です。"], cap="所得税の額の1%", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), ("f0.5", "pop"), ("f0.5+0.5", "tick")]),
    dict(narr=["かわりに、復興特別所得税が、1.1パーセントに下がります。"], cap="復興特別所得税は下がる", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.5", "drop"), ("f0.5+1.0", "ding")]),
    dict(narr=["合わせると、2.1パーセントのまま。", "毎月引かれる税金の計算は、変わりません。"], cap="合計2.1%で変わらず", note="※源泉徴収税額の計算方法に変更なし", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "tick"), ("f0.3", "tick"), ("f0.3+0.5", "tick"), ("f0.65", "ding")]),
    dict(narr=["ただし、復興特別所得税の期間は、10年のびて、令和29年までです。"], cap="令和29年まで延長", note="※改正前は令和19年12月31日まで", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), ("f0.45", "swish"), ("f0.45+0.9", "ding")]),
    dict(narr=["合計は同じで、期間がのびる。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v040_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v040_boei.mp4")
