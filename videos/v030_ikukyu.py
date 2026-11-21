"""#030 育児休業給付金 — 賃金の67%（181日目から50%）・出生後休業支援給付金13%（最大28日）・非課税・上限あり。
Sources (fetched 2026-11-21): 厚労省 育児休業等給付の内容と支給申請手続（2026年8月1日改訂版） 001461102.pdf /
出生後休業支援給付リーフレット 001599643.pdf"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

SKIN = "#FFD9B0"


def person(cx, cy, col, s=1.0):
    """Simple original person: round head + body. ~120 wide, 200 tall at s=1, centred on (cx, cy)."""
    p = (f'<path d="M{cx-60} {cy+100} L{cx-60} {cy+30} Q{cx-60} {cy-20} {cx} {cy-20} Q{cx+60} {cy-20} {cx+60} {cy+30} L{cx+60} {cy+100} Z" fill="{col}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-58}" r="42" fill="{SKIN}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx-14}" cy="{cy-60}" r="5" fill="{BLK}"/><circle cx="{cx+14}" cy="{cy-60}" r="5" fill="{BLK}"/>'
         f'<path d="M{cx-12} {cy-44} Q{cx} {cy-34} {cx+12} {cy-44}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy, s, p)


def baby(cx, cy, t, s=1.0):
    """Swaddled baby, rocking a little."""
    b = (f'<ellipse cx="{cx}" cy="{cy+30}" rx="52" ry="64" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx}" cy="{cy-36}" r="34" fill="{SKIN}" stroke="{BLK}" stroke-width="7"/>'
         f'<path d="M{cx-14} {cy-38} q6 -8 12 0 M{cx+2} {cy-38} q6 -8 12 0" fill="none" stroke="{BLK}" stroke-width="4" stroke-linecap="round"/>'
         f'<circle cx="{cx}" cy="{cy-22}" r="6" fill="{PNK}"/>')
    return grp(cx, cy + 60, s, b, rot=6 * math.sin(t * 3))


def d0(t, T):
    out = head(t, "育休中の給付金は", 80, "賃金の67%", 130)
    g, p = gauge(t, 0.45 * T, 0.67)
    out += grp(540, 655, pop(t, 0.2), g)
    val = int(round(100 - 33 * p))
    out += grp(400, 860, pop(t, 0.35), txt(400, 930, f"{val}%", 190, PNK if p >= 1 else BLK))
    return out + baby(820, 830, t, pop(t, 0.5))


def d1(t, T):
    out = head(t, "67%は180日まで", 84, "181日目から50%", 104, tb=0.5 * T)
    base = 985
    out += f'<line x1="110" y1="{base}" x2="970" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    h1 = 67 * 5.2 * prog(t, 0.3, 0.7)
    h2 = 50 * 5.2 * prog(t, 0.5 * T, 0.7)
    if h1 > 0:
        out += f'<rect x="130" y="{base-h1:.1f}" width="400" height="{h1:.1f}" fill="{PNK}" stroke="{BLK}" stroke-width="7"/>'
    if h2 > 0:
        out += f'<rect x="530" y="{base-h2:.1f}" width="420" height="{h2:.1f}" fill="{BLU}" stroke="{BLK}" stroke-width="7"/>'
    out += grp(330, 800, pop(t, 0.9), txt(330, 810, "67%", 110, WHT) + txt(330, 900, "はじめの180日", 46, WHT))
    out += grp(740, 850, pop(t, 0.5 * T + 0.6), txt(740, 850, "50%", 110, WHT) + txt(740, 930, "181日目から", 46, WHT))
    return out


def d2(t, T):
    out = head(t, "夫婦で14日以上 取ると", 76, "プラス13%", 130, tb=0.4 * T)
    out += person(190, 700, BLU, pop(t, 0.2)) + person(350, 700, PNK, pop(t, 0.4))
    out += grp(270, 890, pop(t, 0.7) * (1 + 0.04 * math.sin(t * 6)), pill(270, 890, "それぞれ14日以上", 36, 340))
    base, x = 985, 520
    h1 = 67 * 4.6 * prog(t, 0.3, 0.6)
    h2 = 13 * 4.6 * prog(t, 0.4 * T, 0.6)
    out += f'<line x1="{x-30}" y1="{base}" x2="{x+330}" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    if h1 > 0:
        out += f'<rect x="{x}" y="{base-h1:.1f}" width="200" height="{h1:.1f}" fill="{PNK}" stroke="{BLK}" stroke-width="7"/>'
        out += grp(x + 100, base - 150, pop(t, 0.8), txt(x + 100, base - 130, "67%", 70, WHT))
    if h2 > 0:
        out += f'<rect x="{x}" y="{base-h1-h2:.1f}" width="200" height="{h2:.1f}" fill="{GLD}" stroke="{BLK}" stroke-width="7"/>'
        out += grp(x + 100, base - h1 - 30, pop(t, 0.4 * T + 0.5), txt(x + 100, base - h1 - 12, "+13%", 46, BLK))
    out += grp(880, 640, pop(t, 0.7 * T), txt(870, 640, "合計", 50, BLK) + txt(870, 740, "80%", 90, PNK))
    out += grp(870, 830, pop(t, 0.7 * T + 0.3), pill(870, 830, "最大28日", 40, 220))
    return out


def d3(t, T):
    out = head(t, "給付金は非課税だから", 80, "手取り10割相当", 110, tb=0.55 * T)
    # tax + insurance monsters are pushed away from the money
    fly = prog(t, 0.2 * T, 0.8)
    out += monster(230 - 60 * fly, 720, RED, t, 0.6 * pop(t, 0.2), chomp=False, rot=-25 * fly)
    out += monster(850 + 60 * fly, 720, GRN, t, 0.6 * pop(t, 0.35), chomp=False, rot=25 * fly)
    for cx in (230 - 60 * fly, 850 + 60 * fly):
        k = pop(t, 0.2 * T + 0.3)
        out += grp(cx, 720, k, f'<line x1="{cx-90}" y1="630" x2="{cx+90}" y2="810" stroke="{PNK}" stroke-width="22" stroke-linecap="round"/>'
                                 f'<line x1="{cx+90}" y1="630" x2="{cx-90}" y2="810" stroke="{PNK}" stroke-width="22" stroke-linecap="round"/>')
    out += grp(170, 905, pop(t, 0.5), pill(170, 905, "税金 なし", 40, 250))
    out += grp(860, 905, pop(t, 0.65), pill(860, 905, "保険料 免除", 38, 260))
    for k in range(3):
        out += grp(540, 800 - k * 70, pop(t, 0.5 + k * 0.2), coin(540, 800 - k * 70 - 8 * abs(math.sin(t * 5 + k)), 56))
    return out


def d4(t, T):
    out = head(t, "ただし", 80, "上限がある", 130)
    top = 640
    out += f'<line x1="120" y1="{top}" x2="960" y2="{top}" stroke="{PNK}" stroke-width="12" stroke-dasharray="34 20"/>'
    out += grp(780, 590, pop(t, 0.3), pill(780, 590, "上限 約33万円", 40, 330, PNK))
    base = 985
    out += f'<line x1="120" y1="{base}" x2="960" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k, (lab, hh) in enumerate((("給料 少なめ", 170), ("ふつう", 260), ("給料 高め", 520))):
        x = 170 + k * 270
        h = min(hh * prog(t, 0.4 + k * 0.5, 0.7), base - top)
        hit = k == 2 and h >= base - top - 1
        if h > 0:
            out += f'<rect x="{x}" y="{base-h:.1f}" width="190" height="{h:.1f}" fill="{PNK if hit else GLD}" stroke="{BLK}" stroke-width="7"/>'
        out += grp(x + 95, base - 60, pop(t, 0.6 + k * 0.5), txt(x + 95, base - 40, lab, 34, WHT if hit else BLK))
    out += grp(805, 720, pop(t, 0.4 + 1.0 + 0.6), txt(805, 740, "ここまで", 44, WHT))
    return out


def d5(t, T):
    out = head(t, "申請は勤務先を通して", 80, "ハローワークへ", 120)
    out += person(230, 700, BLU, 0.8 * pop(t, 0.2)) + baby(350, 660, t, 0.6 * pop(t, 0.35))
    # paper travelling from the person to the office
    p = prog(t, 0.5, 1.0)
    x = 430 + 250 * p
    out += grp(x, 700 - 60 * math.sin(math.pi * p), pop(t, 0.5), f'<rect x="{x-40}" y="{650 - 60*math.sin(math.pi*p):.1f}" width="80" height="100" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
               f'<line x1="{x-22}" y1="{680 - 60*math.sin(math.pi*p):.1f}" x2="{x+22}" y2="{680 - 60*math.sin(math.pi*p):.1f}" stroke="{BLK}" stroke-width="5"/>'
               f'<line x1="{x-22}" y1="{705 - 60*math.sin(math.pi*p):.1f}" x2="{x+22}" y2="{705 - 60*math.sin(math.pi*p):.1f}" stroke="{BLK}" stroke-width="5"/>')
    bx = 760
    out += grp(bx + 90, 700, pop(t, 0.3), f'<rect x="{bx}" y="600" width="180" height="210" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
               f'<rect x="{bx-14}" y="580" width="208" height="30" fill="{GRN}" stroke="{BLK}" stroke-width="7"/>'
               + "".join(f'<rect x="{bx+24+c*56}" y="{634+r*58}" width="34" height="34" fill="{BLU}"/>' for c in range(3) for r in range(2))
               + f'<rect x="{bx+68}" y="756" width="44" height="54" fill="{BLK}"/>')
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["育休中は、賃金の67パーセントが給付金で出ます。"], cap="育休中は賃金の67%", note="※雇用保険に入っている人が対象", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "drop"), ("f0.45+1.0", "ding")]),
    dict(narr=["67パーセントは、最初の180日まで。", "181日目からは、50パーセント。"], cap="181日目からは50%", draw=d1,
         sfx=[(0.0, "whoosh"), (0.3, "tick"), ("f0.5", "tick"), ("f0.5+0.6", "pop")]),
    dict(narr=["夫婦ともに14日以上取ると、最大28日間、13パーセント上乗せ。"], cap="最大28日間 合計80%",
         note="※ひとり親などは本人だけで対象", draw=d2, sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.4, "pop"), ("f0.4", "tick"), ("f0.7", "ding")]),
    dict(narr=["税金がかからず、社会保険料も免除。", "だから80パーセントでも、手取りは10割相当。"], cap="手取りは10割相当",
         note="※保険料の免除は申し出が必要", draw=d3, sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.2", "swish"), ("f0.55", "ding")]),
    dict(narr=["ただし上限は、30日で約33万円。"], cap="30日で約33万円まで", note="※令和9年7月31日までの額", draw=d4,
         sfx=[(0.0, "whoosh"), (0.4, "tick"), (0.9, "tick"), (1.4, "tick"), (2.0, "pop")]),
    dict(narr=["申請は、勤務先を通してハローワークへ。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "swish"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v030_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v030_ikukyu.mp4")
