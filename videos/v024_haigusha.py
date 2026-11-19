"""#024 配偶者控除 — 最高38万円・配偶者の給与収入136万円以下（令和8年分）・こえても配偶者特別控除で段階的・本人の合計所得1,000万円超は対象外。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def person(cx, cy, col):
    """Simple round person ~110px wide, feet at cy+70."""
    return (f'<path d="M{cx-52} {cy+70} L{cx-52} {cy+5} Q{cx-52} {cy-35} {cx} {cy-35} Q{cx+52} {cy-35} {cx+52} {cy+5} L{cx+52} {cy+70} Z" fill="{col}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy-75}" r="40" fill="#FFD9B0" stroke="{BLK}" stroke-width="7"/>'
            f'<circle cx="{cx-14}" cy="{cy-78}" r="5" fill="{BLK}"/><circle cx="{cx+14}" cy="{cy-78}" r="5" fill="{BLK}"/>')


def d0(t, T):
    out = head(t, "結婚している人は", 90, "最高38万円 引ける", 96)
    out += person(390, 700 - 12 * abs(math.sin(t * 4)), BLU)
    out += person(690, 700 - 12 * abs(math.sin(t * 4 + 1.2)), PNK)
    hs = 1 + 0.15 * math.sin(t * 7)
    heart = f'<path d="M540 720 C470 660 490 600 540 640 C590 600 610 660 540 720 Z" fill="{RED}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
    out += grp(540, 665, hs, heart)
    n = int(round(38 * prog(t, 0.3, 1.2)))
    return out + pill(540, 900, f"所得から −{n}万円", 62, 640, BLK, YEL)


def d1(t, T):
    out = head(t, "条件は 配偶者の給料が", 76, "年136万円以下", 120)
    p = prog(t, 0.2 * T, 1.6)
    out += grp(300, 610, pop(t, 0.15, 0.3), txt(120, 625, "配偶者の給料（1年）", 46, BLK, "start"))
    out += f'<rect x="120" y="670" width="840" height="110" rx="12" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += hbar(120, 670, 571 * p, GRN, 110)
    out += f'<line x1="691" y1="640" x2="691" y2="810" stroke="{BLK}" stroke-width="8" stroke-dasharray="16 10"/>'
    out += grp(400, 725, pop(t, 0.2 * T + 1.6), txt(405, 745, "配偶者控除 OK", 52))
    out += grp(825, 725, pop(t, 0.2 * T + 1.9), txt(825, 745, "こえる", 46, "#888"))
    return out + txt(540, 950, f"{int(round(136 * p))}万円", 130, PNK if p >= 1 else BLK)


def d2(t, T):
    out = head(t, "こえても すぐ0円じゃない", 70, "少しずつ へる", 120)
    r = [38, 36, 31, 26, 21, 16, 11, 6, 3]
    out += vbars(t, r, [str(v) for v in r], x0=150, step=(0.75 * T - 0.5) / 9, hi=PNK)
    return out + grp(840, 640, pop(t, 0.3), pill(840, 640, "単位:万円", 38, 250))


def d3(t, T):
    out = head(t, "ただし 自分の所得が", 80, "1,000万円超は ×", 100)
    p = prog(t, 0.15 * T, 2.0)
    out += grp(250, 600, pop(t, 0.15, 0.3), txt(120, 615, "自分の所得", 48, BLK, "start"))
    out += f'<rect x="120" y="660" width="840" height="110" rx="12" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += hbar(120, 660, min(840 * p, 700), BLU, 110)
    out += hbar(820, 660, clamp(840 * p - 700, 0, 140), PNK, 110)
    out += f'<line x1="820" y1="630" x2="820" y2="800" stroke="{BLK}" stroke-width="8" stroke-dasharray="16 10"/>'
    out += txt(820, 850, "1,000万円", 46)
    shake = 8 * math.sin(t * 40) * (1 - clamp((t - 0.15 * T - 2.0) / 0.5)) if t > 0.15 * T + 2.0 else 0
    return out + grp(540, 940, pop(t, 0.15 * T + 2.0), pill(540 + shake, 940, "配偶者控除は使えない", 52, 640, PNK))


def d4(t, T):
    out = head(t, "引くのは 税金じゃなく", 76, "所得から", 130)
    p = prog(t, 0.3 * T, 1.0)
    out += hbar(120, 600, 640, GLD, 120) + txt(440, 682, "所得", 64)
    out += grp(0, 0, 1, hbar(760 + 20 * p, 600 - 50 * p, 200, PNK, 120) + txt(860 + 20 * p, 678 - 50 * p, "38万円", 48, WHT), op=1 - 0.75 * p)
    out += grp(440, 790, pop(t, 0.3 * T + 0.9), f'<polygon points="400,750 480,750 480,790 510,790 440,840 370,790 400,790" fill="{BLK}"/>')
    return out + grp(440, 920, pop(t, 0.3 * T + 1.2), card(140, 860, 600, 120, txt(440, 942, "のこりに税率をかける", 50)))


def d5(t, T):
    out = head(t, "会社員は", 90, "年末調整で手続き", 104)
    b = 10 * abs(math.sin(t * 5))
    doc = card(410, 545 - b, 260, 300)
    for k in range(4):
        doc += f'<line x1="445" y1="{610+k*52-b:.0f}" x2="{635 - (60 if k == 3 else 0)}" y2="{610+k*52-b:.0f}" stroke="{BLK}" stroke-width="10" stroke-linecap="round"/>'
    out += grp(540, 695, pop(t, 0.2), doc)
    chk = f'<circle cx="690" cy="800" r="48" fill="{GRN}" stroke="{BLK}" stroke-width="7"/><path d="M666 800 L684 820 L716 780" fill="none" stroke="{WHT}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    return out + grp(690, 800, pop(t, 0.3 * T), chk) + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["結婚している人は、所得から最高38万円引けます。", "配偶者控除です。"], cap="配偶者控除 最高38万円", note="※本人の合計所得900万円以下の場合", draw=d0,
         sfx=[(0.0, "whoosh"), (0.3, "swish"), (1.5, "ding")]),
    dict(narr=["条件は、配偶者の給料が、ねん136万円以下であること。"], cap="給料が年136万円以下", note="※令和8年分・収入が給与だけの場合", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.2", "swish"), ("f0.2+1.6", "ding")]),
    dict(narr=["こえても、すぐゼロにはなりません。", "配偶者特別控除で、少しずつへります。"], cap="配偶者特別控除", note="※配偶者の合計所得62万円超133万円以下", draw=d2,
         sfx=[(0.0, "whoosh"), (0.5, "tick"), ("f0.25", "tick"), ("f0.5", "tick"), ("f0.75", "ding")]),
    dict(narr=["ただし、自分の所得が1000万円をこえると、使えません。"], cap="所得1,000万円超は対象外", note="※納税者本人の合計所得金額", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.15", "swish"), ("f0.15+2.0", "drop")]),
    dict(narr=["38万円は、税金から引くのではありません。", "税金を計算する前の、所得から引きます。"], cap="所得から引く控除", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.3", "swish"), ("f0.3+0.9", "pop"), ("f0.3+1.2", "pop")]),
    dict(narr=["会社員は、年末調整で手続きします。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.3", "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v024_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v024_haigusha.mp4")
