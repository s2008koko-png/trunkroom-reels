"""#022 所得税は階段式（超過累進）— 税率23%でも全部に23%ではない。課税所得700万円の例。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

NOTE = "※控除後の所得700万円の例"
COLS = ["#9AD1FF", BLU, "#7A5CFF", RED]
# zone widths for a 700万円 bar drawn 840px wide (1万円 = 1.2px); the 23% zone is only 5万円
ZONES = [(195, "5%"), (135, "10%"), (365, "20%"), (5, "23%")]


def zonebar(t, t0, y=700, h=120, step=0.5):
    out = f'<rect x="120" y="{y}" width="840" height="{h}" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
    x = 120.0
    for k, (v, lab) in enumerate(ZONES):
        w = v * 1.2
        p = prog(t, t0 + k * step, 0.4)
        if p > 0:
            out += f'<rect x="{x:.1f}" y="{y}" width="{max(w*p, 2):.1f}" height="{h}" fill="{COLS[k]}" stroke="{BLK}" stroke-width="6"/>'
            if k < 3:
                out += grp(x + w / 2, y + h / 2, pop(t, t0 + k * step + 0.2, 0.25), txt(x + w / 2, y + h / 2 + 20, lab, 56, WHT if k else BLK))
        x += w
    return out


def d0(t, T):
    out = head(t, "税率23%でも", 96, "全部に23%じゃない", 96)
    wob = 6 * math.sin(t * 5)
    out += grp(330, 760, 1 + 0.04 * math.sin(t * 7), txt(330, 830, "23%", 230, BLK), rot=wob)
    p = prog(t, 0.45 * T, 0.4)
    if p > 0:  # a big cross drawn over "全部に"
        out += grp(760, 760, pop(t, 0.45 * T), card(590, 610, 340, 300, txt(760, 720, "全部に", 70) + txt(760, 830, "かける", 70)))
        out += f'<line x1="600" y1="620" x2="{600+320*p:.0f}" y2="{620+280*p:.0f}" stroke="{PNK}" stroke-width="16" stroke-linecap="round"/>'
        q = prog(t, 0.45 * T + 0.3, 0.4)
        if q > 0:
            out += f'<line x1="920" y1="620" x2="{920-320*q:.0f}" y2="{620+280*q:.0f}" stroke="{PNK}" stroke-width="16" stroke-linecap="round"/>'
    return out


def d1(t, T):
    out = head(t, "所得税は", 90, "階段式", 140)
    r = [5, 10, 20, 23, 33, 40, 45]
    out += f'<line x1="135" y1="984" x2="960" y2="984" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k, v in enumerate(r):
        tk = 0.4 + k * (0.7 * T - 0.4) / 7
        p = prog(t, tk, 0.35)
        if p <= 0:
            continue
        x, h = 150 + k * 114, v * 7.6 * p
        out += f'<rect x="{x}" y="{980-h:.1f}" width="114" height="{h:.1f}" fill="{BLU if k < 6 else RED}" stroke="{BLK}" stroke-width="6"/>'
        out += grp(x + 57, 980 - h - 30, pop(t, tk + 0.2, 0.25), txt(x + 57, 980 - h - 16, f"{v}%", 40))
    return out + grp(330, 600, pop(t, 0.3), pill(330, 600, "ぜんぶで7段階", 42, 380))


def d2(t, T):
    out = head(t, "所得700万円なら", 84, "ゾーンごとに計算", 104)
    t0 = 0.3 * T
    out += zonebar(t, t0, step=0.22 * T)
    for k, (x, lab) in enumerate(((120, "0"), (354, "195万"), (516, "330万"), (954, "695万"))):
        out += grp(x, 870, pop(t, t0 + max(0, k - 1) * 0.22 * T + 0.3 * (k > 0), 0.25), txt(x, 880, lab, 38, BLK, "middle" if 0 < k < 3 else ("start" if k == 0 else "end")))
    return out + grp(540, 620, pop(t, 0.2), pill(540, 620, "控除を引いたあとの所得 700万円", 40, 700))


def d3(t, T):
    out = head(t, "23%がかかるのは", 84, "たった5万円ぶん", 108)
    z = prog(t, 0.15 * T, 1.0)   # the bar slides left / grows so the last sliver becomes visible
    out += zonebar(t, -9, y=600, h=90)
    # magnifier over the right end
    cx, cy, r = 954 - 250 * z, 600 + 45 + 190 * z, 60 + 80 * z
    out += f'<line x1="954" y1="690" x2="{cx+r*0.5:.0f}" y2="{cy-r*0.8:.0f}" stroke="{BLK}" stroke-width="5" stroke-dasharray="14 10"/>'
    out += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{WHT}" stroke="{BLK}" stroke-width="10"/>'
    out += f'<line x1="{cx+r*0.7:.0f}" y1="{cy+r*0.7:.0f}" x2="{cx+r*1.25:.0f}" y2="{cy+r*1.25:.0f}" stroke="{BLK}" stroke-width="22" stroke-linecap="round"/>'
    if z > 0.9:
        out += f'<rect x="{cx-r*0.7:.0f}" y="{cy-r*0.6:.0f}" width="{r*0.7:.0f}" height="{r*0.8:.0f}" fill="{COLS[2]}"/><rect x="{cx:.0f}" y="{cy-r*0.6:.0f}" width="{r*0.42:.0f}" height="{r*0.8:.0f}" fill="{RED}" stroke="{BLK}" stroke-width="5"/>'
        out += grp(cx, cy, pop(t, 0.15 * T + 1.0, 0.25), txt(cx, cy + r * 0.6, "5万円", 44, RED))
    return out + grp(330, 850, pop(t, 0.55 * T), card(110, 770, 440, 170, txt(330, 835, "695万円を", 46) + txt(330, 900, "こえた分だけ", 46)))


def d4(t, T):
    out = head(t, "だから税金は", 90, "約97万円", 140)
    rows = [("全部に23%なら", 161, "#999", "161万円", 0.1 * T), ("じっさいは", 97.4, PNK, "約97万円", 0.5 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 560 + k * 210
        out += grp(300, y + 30, pop(t, t0, 0.3), txt(130, y + 44, lab, 50, BLK, "start"))
        out += hbar(130, y + 66, v * 3.6 * prog(t, t0 + 0.15, 0.7), col, 90)
        out += grp(130 + v * 3.6 + 120, y + 111, pop(t, t0 + 0.7, 0.3), txt(130 + v * 3.6 + 20, y + 132, val, 58, BLK, "start"))
    p = prog(t, 0.5 * T, 0.4)
    if p > 0:
        out += f'<line x1="120" y1="671" x2="{120+600*p:.0f}" y2="671" stroke="{BLK}" stroke-width="10" stroke-linecap="round"/>'
    return out


def d5(t, T):
    out = head(t, "税率が上がっても", 84, "手取りは逆転しない", 96)
    for k in range(4):   # coins climbing small steps
        x, h = 250 + k * 150, 50 + k * 45
        out += f'<rect x="{x}" y="{850-h}" width="150" height="{h}" fill="{BLU}" stroke="{BLK}" stroke-width="6"/>' if pop(t, 0.2 + k * 0.12) > 0 else ""
    q = (t * 0.9) % 1.0
    idx = int((t * 0.9) % 4)
    out += coin(325 + idx * 150, 850 - (50 + idx * 45) - 44 - 50 * abs(math.sin(q * math.pi)), 36)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["税率23パーセントでも、全部に23パーセントじゃない。"], cap="所得税のよくある誤解", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.45", "pop"), ("f0.45+0.1", "swish")]),
    dict(narr=["所得税は階段式。", "ゾーンごとに税率がちがいます。"], cap="5%から45%の7段階", draw=d1,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.7", "ding")]),
    dict(narr=["たとえば、控除後の所得が700万円。", "195万円までは5パーセント、その上は10、20パーセント。"], cap="下から順に税率をかける", note=NOTE, draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.3", "tick"), ("f0.52", "tick"), ("f0.74", "tick")]),
    dict(narr=["23パーセントがかかるのは、695万円をこえた5万円だけ。"], cap="23%は5万円ぶんだけ", note=NOTE, draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.15", "swish"), ("f0.15+1.0", "ding"), ("f0.55", "pop")]),
    dict(narr=["だから税金は、約97万円。", "全部に23パーセントの161万円より少ない。"], cap="161万円ではなく97万円", note="※復興特別所得税はのぞく", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.1", "tick"), ("f0.5", "tick"), ("f0.5+0.7", "ding")]),
    dict(narr=["税率が上がっても、所得税で手取りは減りません。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v022_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v022_zeiritsu.mp4")
