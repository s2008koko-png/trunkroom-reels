"""#011 固定資産税 — 家や土地に毎年かかる。標準税率1.4%、1月1日の持ち主、評価は3年ごと、住宅用地1/6・新築3年1/2。
Sources (fetched 2026-11-14): 総務省 地方税制度 固定資産税の概要 / 同 概要図(000759190.pdf)"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

TEA = "#00B8C4"  # 固定資産税 monster


def house(cx, cy, s=1.0, col=RED, rot=0.0):
    """Original house ~260x230 centred at (cx, cy)."""
    h = (f'<rect x="{cx-100}" y="{cy-20}" width="200" height="130" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<polygon points="{cx-135},{cy-14} {cx},{cy-120} {cx+135},{cy-14}" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<rect x="{cx-70}" y="{cy+14}" width="52" height="46" fill="{BLU}" stroke="{BLK}" stroke-width="6"/>'
         f'<rect x="{cx+18}" y="{cy+30}" width="50" height="80" fill="{BLK}"/>')
    return grp(cx, cy, s, h, rot=rot)


def land(cx, cy, w=320, s=1.0):
    return grp(cx, cy, s, f'<rect x="{cx-w/2}" y="{cy-22}" width="{w}" height="44" rx="12" fill="#7BC96F" stroke="{BLK}" stroke-width="8"/>')


def gear(cx, cy, r, ang):
    g = "".join(f'<rect x="{cx-12}" y="{cy-r-16}" width="24" height="34" rx="5" fill="{BLK}" transform="rotate({k*45+ang:.1f} {cx} {cy})"/>' for k in range(8))
    return g + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#999" stroke="{BLK}" stroke-width="8"/><circle cx="{cx}" cy="{cy}" r="{r*0.35:.0f}" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'


def d0(t, T):
    out = head(t, "マイホームには", 84, "毎年1.4%の税金", 110)
    out += land(310, 950) + house(310, 820 + 5 * math.sin(t * 5), 1.15)
    out += monster(790, 810 - 14 * abs(math.sin(t * 5)), TEA, t, 0.72 * pop(t, 0.3 * T))
    if t > 0.3 * T + 0.3:
        p = ((t - 0.3 * T - 0.3) / 0.9) % 1.0
        out += coin(430 + 280 * p, 760 - 130 * math.sin(math.pi * p), 40)
    return out + grp(790, 590, pop(t, 0.3 * T + 0.2), pill(790, 580, "固定資産税", 42, 300, TEA))


def d1(t, T):
    out = head(t, "対象は3つ", 100, "土地・家・事業の設備", 86)
    for k, (cx, lab) in enumerate(((230, "土地"), (540, "家"), (850, "設備"))):
        t0 = 0.08 * T + k * 0.22 * T
        inner = {0: land(cx, 700, 190), 1: house(cx, 690, 0.62), 2: gear(cx, 690, 52, t * 90)}[k]
        out += grp(cx, 700, pop(t, t0), card(cx - 135, 570, 270, 300, inner + txt(cx, 838, lab, 60)))
    return out + grp(540, 945, pop(t, 0.72 * T), pill(540, 945, "かけるのは市町村", 48, 480, BLK, YEL))


def d2(t, T):
    out = head(t, "かかるのは", 84, "1月1日の持ち主", 110)
    days = ["12/30", "12/31", "1/1"]
    k = min(2, int(clamp(t / (0.45 * T)) * 3))
    flip = pop(t, k * 0.15 * T, 0.25) if k else 1
    cal = (card(120, 570, 340, 390) + f'<rect x="124" y="574" width="332" height="90" rx="14" fill="{PNK}"/>'
           f'<circle cx="200" cy="574" r="16" fill="{BLK}"/><circle cx="380" cy="574" r="16" fill="{BLK}"/>'
           + grp(290, 800, flip, txt(290, 850, days[k], 150 if k == 2 else 110, PNK if k == 2 else BLK)))
    out += grp(290, 765, pop(t, 0.1), cal)
    hit = 0.3 * T + 0.3
    out += land(740, 900, 300, pop(t, 0.25)) + house(740, 780 - 18 * abs(math.sin(t * 6)) * (t > hit), 0.95 * pop(t, 0.25), BLU)
    return out + grp(740, 600, pop(t, hit) * (1 + 0.05 * math.sin(t * 9)), pill(740, 600, "この日の持ち主", 44, 380, PNK))


def d3(t, T):
    out = head(t, "もとになるのは", 84, "評価額×1.4%", 120)
    for k, (cx, w, lab, col, fg) in enumerate(((230, 250, "評価額", WHT, BLK), (540, 250, "×1.4%", GLD, BLK), (850, 250, "税額", PNK, WHT))):
        t0 = 0.15 + k * 0.4
        out += grp(cx, 630, pop(t, t0), f'<rect x="{cx-w/2}" y="570" width="{w}" height="120" rx="20" fill="{col}" stroke="{BLK}" stroke-width="8"/>' + txt(cx, 652, lab, 60, fg))
        if k < 2:
            out += grp(cx + 155, 630, pop(t, t0 + 0.2), txt(cx + 155, 652, "→" if k == 0 else "＝", 56))
    cx, cy, r = 300, 860, 105
    dial = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    for j in range(3):
        a = math.radians(j * 120 - 90)
        dial += f'<line x1="{cx}" y1="{cy}" x2="{cx+r*math.cos(a):.1f}" y2="{cy+r*math.sin(a):.1f}" stroke="{BLK}" stroke-width="5" opacity="0.4"/>'
        b = math.radians(j * 120 - 30)
        dial += txt(cx + 62 * math.cos(b), cy + 62 * math.sin(b) + 14, f"{j+1}年", 34)
    ang = 360 * clamp((t - 0.45 * T) / (0.45 * T))
    dial += f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-r+14}" stroke="{PNK}" stroke-width="12" stroke-linecap="round" transform="rotate({ang:.1f} {cx} {cy})"/><circle cx="{cx}" cy="{cy}" r="12" fill="{BLK}"/>'
    out += grp(cx, cy, pop(t, 0.4 * T), dial)
    return out + grp(700, 860, pop(t, 0.45 * T + 0.2), pill(700, 860, "3年ごとに見直し", 48, 470))


def d4(t, T):
    out = head(t, "住宅の土地は", 84, "6分の1で計算", 120)
    for k, (lab, frac, col, t0, tag) in enumerate((("家が建つ土地（200㎡まで）", 1 / 6, "#7BC96F", 0.15 * T, "6分の1"), ("新築の家（3年間）", 0.5, RED, 0.6 * T, "半分"))):
        y = 560 + k * 220
        w = 780 * (1 - (1 - frac) * prog(t, t0, 0.9))
        out += grp(250, y + 20, pop(t, 0.1 + k * 0.15), txt(140, y + 40, lab, 44, BLK, "start"))
        out += f'<rect x="140" y="{y+62}" width="780" height="84" rx="10" fill="none" stroke="{BLK}" stroke-width="5" stroke-dasharray="14 10" opacity="0.5"/>'
        out += hbar(140, y + 62, w, col, 84)
        out += grp(140 + 780 * frac + 150, y + 104, pop(t, t0 + 0.9), pill(140 + 780 * frac + 150, y + 104, tag, 46, 230, PNK))
    return out


def d5(t, T):
    out = head(t, "家は買ったあとも", 84, "毎年お金がかかる", 100)
    for k, (cx, col) in enumerate(((250, RED), (540, BLU), (830, GRN))):
        out += house(cx, 730 - 26 * abs(math.sin(t * 6 + k * 0.8)), 0.66 * pop(t, 0.3 + k * 0.15), col)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["家や土地には、毎年、税金がかかります。", "税率は、ふつう1.4パーセント。"], cap="固定資産税 標準は1.4%", csize=58, note="※標準税率（総務省）", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.3", "pop"), ("f0.3+0.5", "chomp")]),
    dict(narr=["対象は、土地、家、事業で使う設備。", "かけるのは、市町村です。"], cap="かけるのは市町村", note="※東京23区は都が課税", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.08", "pop"), ("f0.30", "pop"), ("f0.52", "pop"), ("f0.72", "ding")]),
    dict(narr=["かかるのは、1月1日に持っている人。"], cap="1月1日の持ち主に課税", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.15", "tick"), ("f0.3", "tick"), ("f0.3+0.3", "ding")]),
    dict(narr=["税額は、土地や家の評価額をもとに計算。", "評価は、3年ごとに見直します。"], cap="評価は3年ごとに見直し", note="※正確には 課税標準額×税率", draw=d3,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), (0.55, "pop"), (0.95, "pop"), ("f0.45", "swish")]),
    dict(narr=["家が建つ土地は、200平方メートルまで、ろくぶんのいち。", "新築の家も、3年間は半分。"], cap="住宅には軽くする特例", note="※小規模住宅用地・新築住宅の特例(要件あり)", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.15", "drop"), ("f0.15+0.9", "pop"), ("f0.6", "drop"), ("f0.6+0.9", "pop")]),
    dict(narr=["家は、買ったあとも毎年お金がかかる。", "フォローして、お金を学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), (0.6, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v011_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v011_kotei.mp4")
