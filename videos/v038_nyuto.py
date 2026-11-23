"""#038 入湯税 — 温泉（鉱泉浴場）に入ると1人1日150円が標準の税金・鉱泉浴場のある市町村が課す目的税・
旅館などが特別徴収義務者として入湯客から徴収し市町村に納入・使い道は環境衛生施設／鉱泉源の保護管理施設／
消防施設など／観光の振興・150円は標準で、税率は各市町村が設定。
Sources (fetched 2026-11-23): 総務省 地方税制度 入湯税 / 様々な税"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

SKIN = "#FFD9B0"
WATER = "#7FD3F7"


def tub(cx, cy, t, s=1.0, bather=True):
    """Original hot-spring tub with wavy steam and a relaxed bather. ~360 wide."""
    b = ""
    for k in (-1, 0, 1):
        ph = t * 3 + k
        x = cx + k * 90
        b += (f'<path d="M{x} {cy-70} q{20*math.sin(ph):.1f} -35 0 -70 q{-20*math.sin(ph):.1f} -35 0 -70" fill="none" stroke="{WHT}" stroke-width="16" stroke-linecap="round" opacity="0.9"/>')
    if bather:
        b += (f'<circle cx="{cx}" cy="{cy-30}" r="44" fill="{SKIN}" stroke="{BLK}" stroke-width="7"/>'
              f'<rect x="{cx-34}" y="{cy-86}" width="68" height="24" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
              f'<path d="M{cx-22} {cy-34} q8 -10 16 0" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>'
              f'<path d="M{cx+6} {cy-34} q8 -10 16 0" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>'
              f'<path d="M{cx-10} {cy-14} q10 10 20 0" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    b += (f'<path d="M{cx-180} {cy} L{cx+180} {cy} L{cx+150} {cy+130} Q{cx} {cy+160} {cx-150} {cy+130} Z" fill="#B9773C" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
          f'<ellipse cx="{cx}" cy="{cy}" rx="180" ry="30" fill="{WATER}" stroke="{BLK}" stroke-width="8"/>')
    return grp(cx, cy, s, b)


def inn(cx, cy, s=1.0):
    """Original inn: wide curved roof + noren curtain."""
    b = (f'<rect x="{cx-110}" y="{cy-40}" width="220" height="150" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<path d="M{cx-160} {cy-36} Q{cx-80} {cy-60} {cx} {cy-130} Q{cx+80} {cy-60} {cx+160} {cy-36} Z" fill="#7A4A2A" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<rect x="{cx-50}" y="{cy+10}" width="100" height="100" fill="{BLK}"/>'
         f'<rect x="{cx-50}" y="{cy+10}" width="46" height="50" fill="{PNK}" stroke="{BLK}" stroke-width="4"/>'
         f'<rect x="{cx+4}" y="{cy+10}" width="46" height="50" fill="{PNK}" stroke="{BLK}" stroke-width="4"/>')
    return grp(cx, cy, s, b)


def hall(cx, cy, s=1.0):
    """Original town hall: block with a flag."""
    b = (f'<rect x="{cx-100}" y="{cy-50}" width="200" height="160" fill="#DDE6F5" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{cx-120}" y="{cy-76}" width="240" height="30" fill="{BLU}" stroke="{BLK}" stroke-width="8"/>'
         f'<line x1="{cx}" y1="{cy-76}" x2="{cx}" y2="{cy-150}" stroke="{BLK}" stroke-width="7"/>'
         f'<polygon points="{cx},{cy-150} {cx+50},{cy-134} {cx},{cy-118}" fill="{PNK}" stroke="{BLK}" stroke-width="5" stroke-linejoin="round"/>')
    for k in range(3):
        b += f'<rect x="{cx-76+k*58}" y="{cy-24}" width="36" height="40" fill="{BLU}" stroke="{BLK}" stroke-width="5"/>'
    b += f'<rect x="{cx-26}" y="{cy+44}" width="52" height="66" fill="{BLK}"/>'
    return grp(cx, cy, s, b)


def guest(cx, cy, s=1.0):
    p = (f'<path d="M{cx-52} {cy+100} L{cx-52} {cy+26} Q{cx-52} {cy-18} {cx} {cy-18} Q{cx+52} {cy-18} {cx+52} {cy+26} L{cx+52} {cy+100} Z" fill="{GRN}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-54}" r="40" fill="{SKIN}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx-13}" cy="{cy-56}" r="5" fill="{BLK}"/><circle cx="{cx+13}" cy="{cy-56}" r="5" fill="{BLK}"/>'
         f'<path d="M{cx-11} {cy-40} Q{cx} {cy-31} {cx+11} {cy-40}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy, s, p)


def d0(t, T):
    out = head(t, "温泉に入ると", 100, "1日150円の税金", 116)
    out += tub(380, 800, t, pop(t, 0.1))
    t0 = 0.45 * T
    s = pop(t, t0)
    out += grp(800, 720, s, coin(800, 720 - 10 * abs(math.sin(t * 5)), 80))
    out += grp(800, 880, pop(t, t0 + 0.3), pill(800, 880, "150円", 60, 280, PNK))
    return out


def d1(t, T):
    out = head(t, "この税金の名前は", 84, "入湯税", 150)
    out += tub(290, 790, t, 0.8 * pop(t, 0.15))
    out += hall(790, 730, pop(t, 0.4 * T))
    p = prog(t, 0.4 * T + 0.3, 0.6)
    if p > 0:
        out += f'<line x1="470" y1="760" x2="{470+170*p:.1f}" y2="760" stroke="{BLK}" stroke-width="12" stroke-linecap="round" stroke-dasharray="6 26"/>'
    out += grp(540, 955, pop(t, 0.4 * T + 0.6), pill(540, 955, "温泉がある市町村の税金", 44, 600))
    return out


def d2(t, T):
    out = head(t, "宿があずかって", 96, "市町村に納める", 120)
    out += guest(180, 740, pop(t, 0.1)) + inn(540, 740, pop(t, 0.2)) + hall(880, 740, 0.85 * pop(t, 0.3))
    for lab, x, t0 in (("お客さん", 180, 0.2), ("宿", 540, 0.3), ("市町村", 880, 0.4)):
        out += grp(x, 905, pop(t, t0), txt(x, 920, lab, 46))
    p1, p2 = prog(t, 0.25 * T, 0.8), prog(t, 0.6 * T, 0.8)
    if 0 < p1 < 1:
        out += coin(250 + 200 * p1, 720 - 110 * math.sin(math.pi * p1), 40)
    if 0 < p2 < 1:
        out += coin(640 + 160 * p2, 720 - 110 * math.sin(math.pi * p2), 40)
    return out


def d3(t, T):
    out = head(t, "使い道は決まってる", 90, "目的税", 150)
    items = [("環境・衛生", GRN), ("源泉を守る", BLU), ("消防", RED), ("観光", PNK)]
    for k, (lab, col) in enumerate(items):
        x, y = 100 + (k % 2) * 460, 545 + (k // 2) * 230
        t0 = 0.3 * T + k * 0.4
        inner = f'<rect x="{x}" y="{y}" width="40" height="205" rx="10" fill="{col}" stroke="{BLK}" stroke-width="8"/>' + txt(x + 228, y + 126, lab, 62)
        out += grp(x + 210, y + 102, pop(t, t0), card(x, y, 420, 205, inner))
    return out


def d4(t, T):
    out = head(t, "150円は「標準」", 96, "金額は市町村で決まる", 88)
    for k, (x, lab, col) in enumerate(((220, "？円", BLK), (540, "150円", PNK), (860, "？円", BLK))):
        t0 = 0.2 + k * 0.3
        out += hall(x, 720 - 10 * abs(math.sin(t * 4 + k)), 0.8 * pop(t, t0))
        out += grp(x, 900, pop(t, 0.4 * T + k * 0.3), pill(x, 900, lab, 54, 240, col))
    return out


def d5(t, T):
    out = head(t, "温泉に行ったら", 96, "明細を見てみよう", 110)
    out += tub(330, 730, t, 0.75 * pop(t, 0.2))
    out += grp(760, 700, pop(t, 0.4), coin(760, 700 - 14 * abs(math.sin(t * 5)), 70))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["温泉に入ると、ひとり1日150円の税金がかかります。"], cap="温泉にも税金がある", note="※標準の税率（1人1日）", draw=d0,
         sfx=[(0.0, "whoosh"), (0.1, "pop"), ("f0.45", "ding")]),
    dict(narr=["名前は、入湯税。", "温泉がある市町村の税金です。"], cap="入湯税は市町村の税金", draw=d1,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.4", "pop"), ("f0.4+0.6", "tick")]),
    dict(narr=["旅館などが、お客さんからあずかります。", "そして、市町村に納めます。"], cap="宿がまとめて納める", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.25", "swish"), ("f0.6", "swish")]),
    dict(narr=["使い道は、決まっています。", "衛生、源泉を守る、消防、観光などです。"], cap="使い道が決まった税金", note="※施設の整備や観光の振興の費用", draw=d3,
         sfx=[(0.0, "whoosh")] + [(f"f0.3+{k*0.4:.2f}", "pop") for k in range(4)]),
    dict(narr=["ただし、150円は標準です。", "金額は、市町村がそれぞれ決めます。"], cap="金額は市町村が決める", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "pop"), (0.8, "pop"), ("f0.4+0.3", "ding")]),
    dict(narr=["温泉に行ったら、明細を見てみよう。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.4, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v038_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v038_nyuto.mp4")
