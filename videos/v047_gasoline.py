"""#047 ガソリンの税金 — 揮発油税 24,300円/kL＋地方揮発油税 4,400円/kL＝合計 28,700円/kL（1リットル 28.7円・本則税率・
令和7年12月31日〜）。令和7年12月30日までは特例税率（暫定税率）で 48,600円＋5,200円＝53,800円/kL（53.8円/L）。
令和7年12月31日に暫定税率が廃止。差は 25.1円/L。計算例：40L×28.7円＝1,148円。沖縄県は別の税率（軽減）。
Sources (fetched 2026-11-26): 国税庁 揮発油税等の特例税率の廃止について"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

OIL = "#FF9F1C"
NOTE = "※揮発油税＋地方揮発油税（沖縄県をのぞく）"


def drop(cx, cy, r, col=OIL):
    """Original teardrop, point up, centred on (cx, cy)."""
    return (f'<path d="M{cx:.1f} {cy-1.7*r:.1f} C{cx+0.3*r:.1f} {cy-0.9*r:.1f} {cx+r:.1f} {cy-0.3*r:.1f} {cx+r:.1f} {cy+0.2*r:.1f} '
            f'A{r} {r} 0 0 1 {cx-r:.1f} {cy+0.2*r:.1f} C{cx-r:.1f} {cy-0.3*r:.1f} {cx-0.3*r:.1f} {cy-0.9*r:.1f} {cx:.1f} {cy-1.7*r:.1f} Z" '
            f'fill="{col}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>')


def pump(cx, cy):
    """Original fuel pump ~260x380 centred on (cx, cy)."""
    return (f'<rect x="{cx-120}" y="{cy+150}" width="240" height="36" rx="8" fill="{BLK}"/>'
            f'<rect x="{cx-95}" y="{cy-180}" width="190" height="335" rx="22" fill="{RED}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="{cx-65}" y="{cy-150}" width="130" height="90" rx="10" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
            + txt(cx, cy - 86, "1L", 60)
            + f'<path d="M{cx+95} {cy-40} q70 0 70 70 v70 q0 40 36 40" fill="none" stroke="{BLK}" stroke-width="14" stroke-linecap="round"/>'
            f'<rect x="{cx+186}" y="{cy+118}" width="60" height="34" rx="8" fill="{BLK}"/>')


def car(cx, cy):
    """Original small car ~380x200 centred on (cx, cy)."""
    return (f'<path d="M{cx-110} {cy-30} L{cx-70} {cy-110} L{cx+70} {cy-110} L{cx+115} {cy-30} Z" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<rect x="{cx-190}" y="{cy-34}" width="380" height="104" rx="30" fill="{BLU}" stroke="{BLK}" stroke-width="8"/>'
            f'<circle cx="{cx-105}" cy="{cy+70}" r="42" fill="{BLK}"/><circle cx="{cx-105}" cy="{cy+70}" r="16" fill="{WHT}"/>'
            f'<circle cx="{cx+105}" cy="{cy+70}" r="42" fill="{BLK}"/><circle cx="{cx+105}" cy="{cy+70}" r="16" fill="{WHT}"/>'
            f'<circle cx="{cx+160}" cy="{cy+4}" r="12" fill="{YEL}" stroke="{BLK}" stroke-width="5"/>')


def d0(t, T):
    out = head(t, "ガソリン1リットル", 96, "28.7円が税金", 120)
    out += pump(250, 770)
    for k in range(3):  # drops falling from the nozzle
        ph = (t * 0.9 + k / 3) % 1
        out += grp(0, 0, 1, drop(466, 930 + 60 * ph, 14), op=1 - ph)
    out += drop(720, 760, 110)
    out += txt(720, 800, "税", 110, WHT)
    pulse = 1 if t < 0.4 else 1 + 0.05 * math.sin(t * 7)
    out += grp(720, 950, pulse, pill(720, 950, "28.7円", 62, 330, PNK))
    return out


def d1(t, T):
    out = head(t, "中身は", 100, "2つの税金", 130)
    rows = [("揮発油税", 24.3, RED, "24.3円", 0.12 * T), ("地方揮発油税", 4.4, BLU, "4.4円", 0.5 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 560 + k * 160
        w = v * 22
        out += grp(250, y + 20, pop(t, t0, 0.3), txt(130, y + 40, lab, 50, BLK, "start"))
        out += hbar(130, y + 58, w * prog(t, t0 + 0.15, 0.6), col, 70)
        out += grp(130 + w + 110, y + 93, pop(t, t0 + 0.6, 0.3), txt(130 + w + 24, y + 114, val, 60, BLK, "start"))
    out += grp(540, 930, pop(t, 0.8 * T), pill(540, 930, "合計 28.7円", 60, 480))
    return out


def d2(t, T):
    out = head(t, "2025年12月30日まで", 84, "53.8円だった", 120)
    U, base = 6.4, 960
    out += f'<line x1="140" y1="{base+4}" x2="940" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    h1 = 53.8 * U * prog(t, 0.15, 0.5)
    out += f'<rect x="190" y="{base-h1:.1f}" width="250" height="{h1:.1f}" rx="8" fill="{BLK}"/>'
    out += grp(315, 590, pop(t, 0.6), txt(315, 598, "53.8円", 60))
    out += grp(315, 900, pop(t, 0.6), txt(315, 918, "まえ", 50, WHT))
    t0 = 0.5 * T
    if t > t0 - 0.5:
        s = prog(t, t0 - 0.5, 0.4)
        v = 53.8 - 25.1 * prog(t, t0, 0.9)
        out += f'<rect x="640" y="{base-53.8*U*s:.1f}" width="250" height="{53.8*U*s:.1f}" rx="8" fill="none" stroke="{BLK}" stroke-width="6" stroke-dasharray="16 12"/>'
        out += f'<rect x="640" y="{base-v*U*s:.1f}" width="250" height="{v*U*s:.1f}" rx="8" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
        out += grp(765, 900, pop(t, t0), txt(765, 918, "いま", 50, WHT))
        out += grp(765, 700, pop(t, t0 + 0.9), txt(765, 716, "−25.1円", 54))
        out += grp(765, 590, pop(t, t0 + 1.1), txt(765, 598, "28.7円", 60, PNK))
    out += grp(540, 830, pop(t, t0 - 0.3), txt(540, 850, "→", 80))
    return out


def d3(t, T):
    out = head(t, "40リットル入れると", 90, "税金は1,148円", 110)
    out += car(310, 790 - 5 * abs(math.sin(t * 7)))
    p = prog(t, 0.2 * T, 0.55 * T)
    lit = int(round(40 * p))
    tax = int(round(lit * 28.7))
    out += drop(310, 600 - 10 * abs(math.sin(t * 5)), 26)
    out += card(560, 570, 400, 400)
    out += f'<rect x="590" y="{940-110*p:.1f}" width="340" height="{110*p:.1f}" rx="6" fill="{OIL}"/>'
    out += f'<rect x="590" y="830" width="340" height="110" rx="6" fill="none" stroke="{BLK}" stroke-width="6"/>'
    out += txt(760, 650, f"{lit}リットル", 62)
    out += txt(760, 770, f"{tax:,}円", 96, PNK)
    return out


def d4(t, T):
    out = head(t, "ただし値段は", 100, "税金だけで決まらない", 88)
    s = math.sin(t * 2.6)
    by = 760 - 50 * s
    barrel = (f'<rect x="170" y="{by-110:.1f}" width="200" height="230" rx="26" fill="#444" stroke="{BLK}" stroke-width="8"/>'
              f'<line x1="170" y1="{by-40:.1f}" x2="370" y2="{by-40:.1f}" stroke="{BLK}" stroke-width="8"/>'
              f'<line x1="170" y1="{by+50:.1f}" x2="370" y2="{by+50:.1f}" stroke="{BLK}" stroke-width="8"/>'
              + txt(270, by + 26, "原油", 56, WHT))
    out += grp(270, 760, pop(t, 0.2), barrel)
    up = s > 0
    board = card(520, 610, 400, 300, txt(720, 710, "お店の値段", 60)
                 + (f'<polygon points="720,{760} 790,{870} 650,{870}" fill="{RED}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>' if up else
                    f'<polygon points="720,{880} 790,{770} 650,{770}" fill="{BLU}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'))
    out += grp(720, 760, pop(t, 0.35), board)
    return out


def d5(t, T):
    out = head(t, "毎日の値段にも", 100, "税金のしくみ", 130)
    for k, cx in enumerate((270, 540, 810)):
        out += grp(cx, 720, pop(t, 0.2 + k * 0.15), drop(cx, 740 - 30 * abs(math.sin(t * 6 + k * 0.9)), 62))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["ガソリン1リットルには、28.7円の税金がかかっています。"], cap="1リットルに28.7円", note=NOTE, draw=d0,
         sfx=[(0.0, "whoosh"), (0.4, "pop"), ("f0.5", "ding")]),
    dict(narr=["中身は、キハツユ税が24.3円。", "地方キハツユ税が4.4円です。"], cap="2つ合わせて28.7円", note="※1リットルあたり", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.12", "tick"), ("f0.5", "tick"), ("f0.8", "ding")]),
    dict(narr=["じつは2025年の年末まで、53.8円でした。", "上乗せ分の25.1円が、なくなりました。"], cap="25.1円へった",
         note="※令和7年12月31日に暫定税率が廃止", draw=d2, sfx=[(0.0, "whoosh"), (0.15, "tick"), ("f0.5", "drop"), ("f0.5+1.1", "ding")]),
    dict(narr=["40リットル入れると、税金は1148円です。"], cap="40リットルで1,148円", note="※40リットル×28.7円", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.2", "swish"), ("f0.75", "ding")]),
    dict(narr=["ただし、お店の値段は、税金だけでは決まりません。", "原油の値段でも動きます。"], cap="原油の値段でも動く", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop")]),
    dict(narr=["毎日の値段にも、税金のしくみ。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v047_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v047_gasoline.mp4")
