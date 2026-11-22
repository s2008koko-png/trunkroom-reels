"""#035 国際観光旅客税（出国税） — 出国1回につき3,000円（令和8年7月1日に1,000円から引上げ）・チケット代に上乗せして徴収・
日本人も外国人も、観光以外の目的でも対象・2歳未満と入国後24時間以内の乗継旅客などは対象外・観光施策の財源。
Sources (fetched 2026-11-22): 国税庁 国際観光旅客税について / 国際観光旅客税に関するQ&A（令和8年4月改訂）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

SKIN = "#FFD9B0"


def plane(cx, cy, s=1.0, rot=0.0):
    """Simple original side-view airplane ~320 wide, nose to the right."""
    p = (f'<polygon points="{cx-150},{cy-10} {cx-175},{cy-85} {cx-125},{cy-85} {cx-80},{cy-18}" fill="{PNK}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<path d="M{cx-160} {cy-22} L{cx+90} {cy-30} Q{cx+165} {cy-22} {cx+165} {cy+5} Q{cx+150} {cy+34} {cx+80} {cy+34} L{cx-120} {cy+34} Q{cx-165} {cy+26} {cx-160} {cy-22} Z" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<polygon points="{cx-30},{cy+14} {cx+50},{cy+14} {cx-50},{cy+100} {cx-90},{cy+100}" fill="{BLU}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
         + "".join(f'<circle cx="{cx-70+k*42}" cy="{cy-4}" r="10" fill="{BLU}"/>' for k in range(5))
         + f'<path d="M{cx+118} {cy-20} Q{cx+150} {cy-16} {cx+156} {cy-2} L{cx+112} {cy-2} Z" fill="{BLK}"/>')
    return grp(cx, cy, s, p, rot=rot)


def person(cx, cy, col, s=1.0):
    p = (f'<path d="M{cx-60} {cy+100} L{cx-60} {cy+30} Q{cx-60} {cy-20} {cx} {cy-20} Q{cx+60} {cy-20} {cx+60} {cy+30} L{cx+60} {cy+100} Z" fill="{col}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-58}" r="42" fill="{SKIN}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx-14}" cy="{cy-60}" r="5" fill="{BLK}"/><circle cx="{cx+14}" cy="{cy-60}" r="5" fill="{BLK}"/>'
         f'<path d="M{cx-12} {cy-44} Q{cx} {cy-34} {cx+12} {cy-44}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy, s, p)


def case(cx, cy, col, s=1.0):
    """Suitcase ~90x110."""
    c = (f'<path d="M{cx-20} {cy-55} L{cx-20} {cy-85} L{cx+20} {cy-85} L{cx+20} {cy-55}" fill="none" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<rect x="{cx-45}" y="{cy-55}" width="90" height="110" rx="12" fill="{col}" stroke="{BLK}" stroke-width="7"/>'
         f'<line x1="{cx-45}" y1="{cy-15}" x2="{cx+45}" y2="{cy-15}" stroke="{BLK}" stroke-width="5"/>'
         f'<circle cx="{cx-28}" cy="{cy+62}" r="9" fill="{BLK}"/><circle cx="{cx+28}" cy="{cy+62}" r="9" fill="{BLK}"/>')
    return grp(cx, cy, s, c)


def d0(t, T):
    out = head(t, "日本を出るたびに", 88, "3,000円の税金", 118)
    # runway
    out += f'<rect x="100" y="950" width="880" height="40" rx="8" fill="#444" stroke="{BLK}" stroke-width="7"/>'
    out += "".join(f'<rect x="{140+k*120}" y="966" width="60" height="8" fill="{WHT}"/>' for k in range(7))
    p = prog(t, 0.2, 0.9 * T)
    x, y = 250 + 480 * p, 880 - 230 * p ** 2
    out += plane(x, y, 0.9, rot=-4 - 14 * p)
    # a coin is left behind
    q = prog(t, 0.4 * T, 0.6)
    if q > 0:
        out += coin(300, 700 + 190 * q, 54)
        out += grp(300, 780, pop(t, 0.4 * T + 0.6), pill(300, 780, "3,000円", 46, 250, PNK))
    return out


def d1(t, T):
    out = head(t, "国際観光旅客税", 84, "7月から3倍に", 124, tb=0.45 * T)
    base = 985
    out += f'<line x1="130" y1="{base}" x2="950" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    h1 = 115 * prog(t, 0.3, 0.6)
    h2 = 345 * prog(t, 0.45 * T, 0.8)
    if h1 > 0:
        out += f'<rect x="200" y="{base-h1:.1f}" width="240" height="{h1:.1f}" fill="{BLK}" stroke="{BLK}" stroke-width="7"/>'
        out += grp(320, base - 150, pop(t, 0.7), txt(320, base - 135, "1,000円", 56, BLK))
        out += grp(320, base - 50, pop(t, 0.8), txt(320, base - 40, "6月まで", 42, WHT))
    if h2 > 0:
        out += f'<rect x="620" y="{base-h2:.1f}" width="240" height="{h2:.1f}" fill="{PNK}" stroke="{BLK}" stroke-width="7"/>'
        out += grp(740, base - 380, pop(t, 0.45 * T + 0.7), txt(740, base - 365, "3,000円", 62, PNK))
        out += grp(740, base - 50, pop(t, 0.45 * T + 0.8), txt(740, base - 40, "7月から", 42, WHT))
    out += grp(530, 800, pop(t, 0.45 * T), txt(530, 825, "→", 90))
    return out


def d2(t, T):
    out = head(t, "払うタイミングは", 84, "チケットを買うとき", 96)
    # ticket with a tear-off stub
    tk = (f'<rect x="130" y="610" width="820" height="290" rx="26" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
          f'<line x1="640" y1="620" x2="640" y2="890" stroke="{BLK}" stroke-width="6" stroke-dasharray="16 14"/>'
          f'<circle cx="640" cy="610" r="22" fill="{YEL}" stroke="{BLK}" stroke-width="8"/><circle cx="640" cy="900" r="22" fill="{YEL}" stroke="{BLK}" stroke-width="8"/>'
          + txt(385, 690, "航空券", 54) + txt(385, 790, "運賃", 80, BLU))
    out += grp(540, 755, pop(t, 0.2), tk)
    out += plane(385, 850, 0.32 * pop(t, 0.4))
    k = pop(t, 0.45 * T)
    out += grp(795, 755, k * (1 + 0.05 * math.sin(t * 7)), f'<rect x="662" y="640" width="266" height="230" rx="16" fill="{PNK}"/>' + txt(795, 725, "＋税金", 56, WHT) + txt(795, 820, "3,000円", 60, WHT))
    out += grp(540, 960, pop(t, 0.45 * T + 0.5), pill(540, 960, "代金に上乗せ", 44, 380))
    return out


def d3(t, T):
    out = head(t, "日本人も外国人も", 88, "出張や留学でも", 112, tb=0.45 * T)
    cols = (BLU, PNK, GRN, RED)
    labs = ("観光", "出張", "留学", "帰国")
    for k in range(4):
        cx = 190 + k * 235
        t0 = 0.2 + k * (0.6 * T / 4)
        dy = -10 * abs(math.sin(t * 4 + k))
        out += person(cx - 20, 720 + dy, cols[k], 0.85 * pop(t, t0)) + case(cx + 62, 770 + dy, GLD, 0.8 * pop(t, t0 + 0.1))
        out += grp(cx, 930, pop(t, t0 + 0.2), pill(cx, 930, labs[k], 44, 180))
    return out


def d4(t, T):
    out = head(t, "ただし", 84, "かからない人もいる", 100)
    # baby
    b = (f'<ellipse cx="290" cy="760" rx="62" ry="76" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="290" cy="682" r="42" fill="{SKIN}" stroke="{BLK}" stroke-width="7"/>'
         f'<path d="M272 680 q7 -9 14 0 M294 680 q7 -9 14 0" fill="none" stroke="{BLK}" stroke-width="4" stroke-linecap="round"/>'
         f'<circle cx="290" cy="700" r="7" fill="{PNK}"/>')
    out += grp(290, 750, pop(t, 0.2), card(120, 570, 340, 300) + grp(290, 800, 1, b, rot=5 * math.sin(t * 3)))
    out += grp(290, 935, pop(t, 0.4), pill(290, 935, "2歳未満", 46, 260, GRN))
    # clock: transit within 24 hours
    a = t * 140
    ck = (f'<circle cx="790" cy="720" r="100" fill="{WHT}" stroke="{BLK}" stroke-width="9"/>'
          + "".join(f'<line x1="{790+84*math.sin(math.radians(d)):.1f}" y1="{720-84*math.cos(math.radians(d)):.1f}" x2="{790+96*math.sin(math.radians(d)):.1f}" y2="{720-96*math.cos(math.radians(d)):.1f}" stroke="{BLK}" stroke-width="6"/>' for d in range(0, 360, 30))
          + f'<line x1="790" y1="720" x2="{790+70*math.sin(math.radians(a)):.1f}" y2="{720-70*math.cos(math.radians(a)):.1f}" stroke="{PNK}" stroke-width="9" stroke-linecap="round"/>'
          f'<line x1="790" y1="720" x2="{790+44*math.sin(math.radians(a/12)):.1f}" y2="{720-44*math.cos(math.radians(a/12)):.1f}" stroke="{BLK}" stroke-width="10" stroke-linecap="round"/>'
          f'<circle cx="790" cy="720" r="10" fill="{BLK}"/>')
    out += grp(790, 720, pop(t, 0.45 * T), card(620, 570, 340, 300) + ck)
    out += grp(790, 935, pop(t, 0.45 * T + 0.2), pill(790, 935, "24時間以内の乗り継ぎ", 34, 400, GRN))
    return out


def d5(t, T):
    out = head(t, "使い道は", 84, "観光のための政策", 104)
    p = (t * 0.25) % 1.0
    out += plane(170 + 740 * p, 720 - 90 * math.sin(math.pi * p), 0.55 * pop(t, 0.2), rot=-12 + 24 * p)
    for k in range(3):
        out += grp(330 + k * 210, 800, pop(t, 0.3 + k * 0.15), coin(330 + k * 210, 800 - 10 * abs(math.sin(t * 5 + k)), 40))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["日本を出国するたびに、3,000円の税金がかかります。"], cap="出国1回につき3,000円", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), ("f0.4", "drop"), ("f0.4+0.6", "ding")]),
    dict(narr=["名前は、国際観光旅客税。", "今年の7月に、1,000円から3,000円になりました。"], cap="1,000円から3,000円に", csize=58,
         note="※令和8年7月1日以後の出国（例外あり）", draw=d1, sfx=[(0.0, "whoosh"), (0.3, "tick"), ("f0.45", "tick"), ("f0.45+0.7", "pop")]),
    dict(narr=["航空券や船のチケット代に、上乗せされています。"], cap="チケット代といっしょに払う", csize=56, note="※原則の集め方", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "pop"), ("f0.45+0.5", "tick")]),
    dict(narr=["日本人も外国人も対象。", "出張や留学でも、かかります。"], cap="観光じゃなくても対象", draw=d3,
         sfx=[(0.0, "whoosh")] + [(f"f{0.15 * k:.2f}+0.2", "pop") for k in range(4)]),
    dict(narr=["ただし、2歳未満の子どもや、24時間以内に乗り継ぐ人は、かかりません。"], cap="対象外の人もいる", note="※ほかに乗員なども対象外", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "pop"), ("f0.45+0.2", "tick")]),
    dict(narr=["集めた税金は、観光のための政策に使われます。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), (0.3, "pop"), (0.45, "pop"), (0.6, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v035_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v035_shukkoku.mp4")
