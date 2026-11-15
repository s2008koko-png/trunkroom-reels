"""#014 退職金と税金 — 退職所得控除（20年まで1年40万円・20年超は1年70万円、勤続30年で1,500万円）、引いた残りを半分にして計算、
国税庁の計算例（退職金2,300万円・勤続30年→所得税等 約38万円）、申告書を出さないと20.42%が引かれ確定申告で精算。
Sources (fetched 2026-11-15): 国税庁 No.1420 退職金を受け取ったとき(退職所得) / No.2732 退職手当等に対する源泉徴収（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

BRN = "#B07A3C"


def bag(cx, cy, s=1.0, label="", rot=0.0):
    """Original money bag ~220x240 centred at (cx, cy)."""
    g = (f'<path d="M{cx-50} {cy-70} Q{cx-150} {cy+20} {cx-100} {cy+100} Q{cx} {cy+140} {cx+100} {cy+100} Q{cx+150} {cy+20} {cx+50} {cy-70} Z" fill="{BRN}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<polygon points="{cx-58},{cy-70} {cx-78},{cy-128} {cx},{cy-104} {cx+78},{cy-128} {cx+58},{cy-70}" fill="{BRN}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<rect x="{cx-64}" y="{cy-84}" width="128" height="24" rx="10" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>'
         + txt(cx, cy + 62, label or "¥", 60 if label else 96, WHT))
    return grp(cx, cy, s, g, rot=rot)


def shield(cx, cy, s=1.0):
    g = (f'<path d="M{cx-90} {cy-90} L{cx+90} {cy-90} L{cx+90} {cy+10} Q{cx+90} {cy+80} {cx} {cy+120} Q{cx-90} {cy+80} {cx-90} {cy+10} Z" fill="{BLU}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         + txt(cx, cy + 20, "控除", 64, WHT))
    return grp(cx, cy, s, g)


def d0(t, T):
    out = head(t, "勤続30年の退職金", 84, "1,500万円まで所得税0円", 74)
    out += bag(280, 770 + 8 * math.sin(t * 5), 1.15)
    out += shield(560, 760, pop(t, 0.25 * T))
    out += monster(840, 770, RED, t, 0.7, chomp=t < 0.25 * T, rot=8 * math.sin(t * 8) if t > 0.25 * T else 0)
    if t > 0.25 * T + 0.3:
        out += grp(840, 590, pop(t, 0.25 * T + 0.3), pill(840, 585, "所得税 0円", 44, 300, PNK))
    return out


def d1(t, T):
    out = head(t, "長く勤めるほど", 84, "割引が大きくなる", 104)
    x0, base, n = 150, 960, 30
    bw = 26
    k_now = n * clamp((t - 0.12 * T) / (0.62 * T))
    out += f'<line x1="{x0-10}" y1="{base+4}" x2="{x0+n*bw+10}" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k in range(n):
        if k >= k_now:
            break
        v = 40 * (k + 1) if k < 20 else 800 + 70 * (k - 19)
        h = v * 0.215
        out += f'<rect x="{x0+k*bw}" y="{base-h:.1f}" width="{bw-4}" height="{h:.1f}" rx="3" fill="{BLU if k < 20 else PNK}"/>'
    out += txt(x0 + 20 * bw, base + 44, "20年", 36) + txt(x0 + n * bw - 10, base + 44, "30年", 36)
    out += grp(330, 610, pop(t, 0.15 * T), pill(330, 610, "1年ごとに40万円", 42, 400, BLU))
    out += grp(380, 710, pop(t, 0.55 * T), pill(380, 710, "21年目から70万円", 42, 430, PNK))
    out += grp(870, 590, pop(t, 0.74 * T + 0.1), txt(990, 610, "1,500万円", 52, PNK, "end"))
    return out


def d2(t, T):
    out = head(t, "さらに残りを", 84, "半分にして計算", 120)
    rows = [("退職金", 2300, GLD, "2,300万円", 0.05 * T), ("割引", 1500, BLU, "−1,500万円", 0.25 * T), ("残り", 800, "#999", "800万円", 0.45 * T), ("半分", 400, PNK, "400万円", 0.65 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 545 + k * 112
        out += grp(180, y + 50, pop(t, t0, 0.3), txt(120, y + 68, lab, 50, BLK, "start"))
        out += hbar(300, y + 18, v * 0.2 * prog(t, t0 + 0.1, 0.5), col, 70)
        out += grp(300 + v * 0.2 + 120, y + 50, pop(t, t0 + 0.5, 0.3), txt(300 + v * 0.2 + 18, y + 70, val, 48, PNK if k == 3 else BLK, "start"))
    return out


def d3(t, T):
    out = head(t, "この例の所得税は", 84, "約38万円", 140)
    out += bag(250, 770, 0.95, "2,300万")
    out += monster(800, 780, RED, t, 0.72 * pop(t, 0.2))
    if t > 0.5:
        q = ((t - 0.5) / 1.1) % 1.0
        out += coin(380 + 320 * q, 760 - 120 * math.sin(math.pi * q), 34)
    out += grp(800, 590, pop(t, 0.45 * T), pill(800, 585, "約38万円", 50, 300, PNK))
    return out


def d4(t, T):
    out = head(t, "申告書を出さないと", 80, "20.42%引かれる", 110)
    sheet = card(130, 570, 320, 380) + f'<rect x="134" y="574" width="312" height="72" rx="14" fill="{BLK}"/>' + txt(290, 626, "申告書", 48, YEL)
    for k in range(3):
        sheet += f'<rect x="170" y="{690+k*66}" width="240" height="22" rx="8" fill="#BBB"/>'
    out += grp(290, 760, pop(t, 0.15), sheet, rot=-5 + 4 * math.sin(t * 4))
    out += grp(290, 760, pop(t, 0.2 * T), f'<line x1="170" y1="640" x2="410" y2="900" stroke="{PNK}" stroke-width="18" stroke-linecap="round"/><line x1="410" y1="640" x2="170" y2="900" stroke="{PNK}" stroke-width="18" stroke-linecap="round"/>')
    x, y, w = 540, 620, 420
    p = prog(t, 0.3 * T, 0.8)
    out += f'<rect x="{x}" y="{y}" width="{w}" height="96" rx="14" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="{x+w-w*0.2042*p:.1f}" y="{y+4}" width="{w*0.2042*p:.1f}" height="88" rx="8" fill="{RED}"/>' if p > 0.02 else ""
    out += grp(750, 780, pop(t, 0.3 * T + 0.5), txt(750, 800, "20.42%", 84, RED))
    out += grp(750, 920, pop(t, 0.62 * T), pill(750, 920, "確定申告で精算", 46, 420))
    return out


def d5(t, T):
    out = head(t, "退職金の税金は", 84, "軽くなるしくみ", 116)
    for k, cx in enumerate((250, 540, 830)):
        out += bag(cx, 700 - 24 * abs(math.sin(t * 6 + k * 0.8)), 0.6 * pop(t, 0.3 + k * 0.15))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["30年勤めた人の退職金。", "1500万円までは、所得税がかかりません。"], cap="1,500万円まで所得税0円", csize=56, note="※勤続30年の退職所得控除（国税庁）", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.25", "pop"), ("f0.25+0.3", "ding")]),
    dict(narr=["割引は、20年までは1年ごとに40万円。", "21年目からは、70万円です。"], cap="30年で1,500万円", note="※800万円＋70万円×(30年−20年)", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.15", "pop"), ("f0.55", "pop"), ("f0.74", "ding")]),
    dict(narr=["さらに、割引のあとの残りを、半分にして計算します。"], cap="残りを半分にして計算", note="※例：退職金2,300万円・勤続30年", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.05", "tick"), ("f0.25", "tick"), ("f0.45", "tick"), ("f0.65", "ding")]),
    dict(narr=["この例だと、2300万円に対して、所得税は約38万円です。"], cap="2,300万円で約38万円", note="※国税庁の計算例・復興特別所得税を含む", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "ding")]),
    dict(narr=["ただし、申告書を出さないと、20.42パーセントが引かれます。"], cap="出さないと20.42%", note="※あとで確定申告をして精算", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.2", "pop"), ("f0.3", "drop"), ("f0.62", "pop")]),
    dict(narr=["退職金は、税金が軽くなるしくみ。", "フォローして、お金を学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), (0.6, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v014_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v014_taishoku.mp4")
