"""#018 相続税の基礎控除 — 3,000万円＋600万円×法定相続人の数。
Sources (fetched 2026-11-17, 令和8年4月1日現在法令等):
  国税庁 No.4152 相続税の計算 / No.4102 相続税がかかる場合 / No.4205 相続税の申告と納税"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

BRN = "#C98A3B"


def bag(cx, cy, s=1.0, rot=0.0):
    """Original money bag, ~250px wide at s=1."""
    b = (f'<path d="M{cx-44} {cy-92} L{cx-70} {cy-150} L{cx-24} {cy-128} L{cx} {cy-156} L{cx+24} {cy-128} L{cx+70} {cy-150} L{cx+44} {cy-92} Z" fill="{BRN}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<ellipse cx="{cx}" cy="{cy+14}" rx="126" ry="112" fill="{BRN}" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{cx-56}" y="{cy-104}" width="112" height="26" rx="10" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>'
         + txt(cx, cy + 62, "¥", 130, BLK))
    return grp(cx, cy, s, b, rot=rot)


def person(cx, cy, col, s=1.0):
    """Simple original person: round head + rounded body, ~120px wide, feet at cy+110."""
    p = (f'<path d="M{cx-60} {cy+110} L{cx-60} {cy+40} Q{cx-60} {cy-10} {cx} {cy-10} Q{cx+60} {cy-10} {cx+60} {cy+40} L{cx+60} {cy+110} Z" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-52}" r="46" fill="#FFD9B0" stroke="{BLK}" stroke-width="8"/>'
         f'<circle cx="{cx-16}" cy="{cy-56}" r="6" fill="{BLK}"/><circle cx="{cx+16}" cy="{cy-56}" r="6" fill="{BLK}"/>'
         f'<path d="M{cx-14} {cy-36} Q{cx} {cy-24} {cx+14} {cy-36}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy + 110, s, p)


def d0(t, T):
    out = head(t, "親の遺産3,600万円まで", 76, "相続税は0円", 130)
    out += bag(290, 790 - 10 * abs(math.sin(t * 4)), pop(t, 0.2), rot=4 * math.sin(t * 3))
    p = prog(t, 0.5, 1.2)
    val = int(round(3600 * p / 100) * 100)
    out += grp(700, 720, pop(t, 0.35), txt(700, 750, f"{val:,}万円", 104, BLK))
    st = pill(700, 890, "相続税 0円", 70, 470, PNK, WHT)
    return out + grp(700, 890, pop(t, 0.5 * T), st, rot=-6)


def d1(t, T):
    out = head(t, "税金がかからないわく", 80, "基礎控除の計算", 110)
    out += grp(300, 655, pop(t, 0.25), card(100, 570, 400, 170, txt(300, 685, "3,000万円", 78)))
    out += grp(560, 655, pop(t, 0.33 * T), txt(560, 690, "＋", 90, PNK))
    out += grp(800, 655, pop(t, 0.4 * T), f'<rect x="620" y="570" width="360" height="170" rx="20" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>' + txt(800, 685, "600万円", 78))
    out += grp(330, 880, pop(t, 0.62 * T), pill(330, 880, "× 相続人の数", 52, 440))
    for k, col in enumerate((BLU, GRN, RED)):
        out += person(670 + k * 125, 820 - 10 * abs(math.sin(t * 5 + k)), col, 0.8 * pop(t, 0.62 * T + 0.25 + k * 0.25))
    return out


def d2(t, T):
    out = head(t, "配偶者と子ども2人なら", 76, "4,800万円まで0円", 100)
    n = 0
    for k, (cx, col, lab) in enumerate(((230, PNK, "配偶者"), (540, BLU, "子ども"), (850, GRN, "子ども"))):
        t0 = 0.12 * T + k * 0.2 * T
        if t >= t0:
            n += 1
        out += person(cx, 610 - 8 * abs(math.sin(t * 5 + k)), col, 0.85 * pop(t, t0))
        out += grp(cx, 775, pop(t, t0 + 0.15), pill(cx, 775, lab, 42, 230))
    out += grp(540, 860, pop(t, 0.1), txt(540, 872, f"3,000万円＋600万円×{max(n, 1)}人", 50))
    val = 3000 + 600 * max(n, 1)
    return out + grp(540, 950, pop(t, 0.1), txt(540, 985, f"{val:,}万円", 112, PNK if n == 3 else BLK))


def d3(t, T):
    out = head(t, "わくをこえたら", 80, "こえた分に税金", 110)
    x, y, w, h = 120, 600, 840, 120
    p = prog(t, 0.2, 0.9)
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="{x+4}" y="{y+4}" width="{max(0, min(w*p, w*0.6)-4):.1f}" height="{h-8}" rx="12" fill="{GLD}"/>'
    if w * p > w * 0.6:
        out += f'<rect x="{x+w*0.6:.1f}" y="{y+4}" width="{w*p-w*0.6-4:.1f}" height="{h-8}" rx="12" fill="{RED}"/>'
    out += f'<line x1="{x+w*0.6}" y1="{y-30}" x2="{x+w*0.6}" y2="{y+h+30}" stroke="{BLK}" stroke-width="8" stroke-dasharray="16 12"/>'
    out += grp(370, 790, pop(t, 0.3 * T), pill(370, 790, "わくの中は0円", 46, 420, BLK, YEL))
    out += grp(790, 560, pop(t, 0.55 * T), txt(792, 575, "こえた分", 44, BLK))
    out += monster(800, 870 - 8 * abs(math.sin(t * 5)), RED, t, 0.6 * pop(t, 0.55 * T))
    return out


def d4(t, T):
    out = head(t, "申告と納税は", 80, "10か月以内", 130)
    for k in range(10):
        t0 = 0.1 * T + k * 0.065 * T
        x, y = 125 + (k % 5) * 170, 560 + (k // 5) * 170
        last = k == 9
        s = pop(t, t0, 0.25) * ((1 + 0.05 * math.sin(t * 9)) if last and t > t0 + 0.3 else 1)
        tile = (f'<rect x="{x}" y="{y}" width="150" height="150" rx="18" fill="{PNK if last else WHT}" stroke="{BLK}" stroke-width="8"/>'
                + txt(x + 75, y + 104, str(k + 1), 84, WHT if last else BLK))
        out += grp(x + 75, y + 75, s, tile)
    return out + grp(540, 950, pop(t, 0.78 * T), pill(540, 950, "亡くなったのを知った翌日から", 44, 760))


def d5(t, T):
    out = head(t, "遺産がわく以下なら", 80, "申告も納税も不要", 100)
    out += bag(330, 700 - 16 * abs(math.sin(t * 5)), 0.62 * pop(t, 0.2))
    ck = (f'<circle cx="720" cy="690" r="92" fill="{GRN}" stroke="{BLK}" stroke-width="8"/>'
          f'<path d="M676 692 L708 726 L768 656" fill="none" stroke="{WHT}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')
    out += grp(720, 690, pop(t, 0.4) * (1 + 0.04 * math.sin(t * 8)), ck)
    return out + follow(t, 0.5 * T)


SCENES = [
    dict(narr=["親の遺産、3600万円までなら、相続税はゼロ円です。", "これは、そうぞくにんが1人のときの数字。"], cap="遺産3,600万円まで0円",
         note="※法定相続人が1人の場合の基礎控除額", draw=d0, sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "tick"), ("f0.5", "ding")]),
    dict(narr=["税金がかからないわくは、3000万円たす、600万円かける、そうぞくにんの数。"], cap="3,000万円＋600万円×人数", csize=56, draw=d1,
         sfx=[(0.0, "whoosh"), (0.25, "pop"), ("f0.4", "pop"), ("f0.62", "pop"), ("f0.62+0.25", "tick"), ("f0.62+0.5", "tick"), ("f0.62+0.75", "tick")]),
    dict(narr=["たとえば、はいぐうしゃと子ども2人なら、3人で4800万円。"], cap="相続人3人で4,800万円",
         note="※法定相続人が3人の場合", draw=d2, sfx=[(0.0, "whoosh"), ("f0.12", "pop"), ("f0.32", "pop"), ("f0.52", "pop"), ("f0.52+0.3", "ding")]),
    dict(narr=["遺産がこのわくをこえたら、こえた分に税金がかかります。"], cap="こえた分にだけかかる", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), ("f0.3", "pop"), ("f0.55", "chomp")]),
    dict(narr=["そのときは、亡くなったのを知った次の日から、10か月以内に申告と納税。"], cap="期限は10か月以内", draw=d4,
         sfx=[(0.0, "whoosh")] + [(f"f{0.1+k*0.065:.3f}", "tick") for k in range(9)] + [("f0.685", "ding")]),
    dict(narr=["わく以下なら、申告も納税もいりません。", "フォローして、お金の仕組みを学ぼう。"], cap="まず遺産の合計を知ろう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.4, "pop"), ("f0.5", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v018_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v018_sozoku.mp4")
