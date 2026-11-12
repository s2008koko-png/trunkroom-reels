"""#004 年末調整 — 毎月の所得税は「仮」、年末に計算しなおす (source: 国税庁 No.2662 / No.2665 / 年末調整のしかた / 給与所得者と税)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def payslip(cx, cy, label, on):
    """Small pay slip: white sheet, month label, a red 'tax' line with a 仮 stamp."""
    x, y = cx - 95, cy - 120
    s = (f'<rect x="{x}" y="{y}" width="190" height="240" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
         + txt(cx, y + 62, label, 46)
         + f'<rect x="{x+24}" y="{y+92}" width="142" height="16" rx="8" fill="#CCC"/>'
         + f'<rect x="{x+24}" y="{y+124}" width="100" height="16" rx="8" fill="{RED}"/>')
    if on:
        s += (f'<circle cx="{cx+38}" cy="{y+186}" r="40" fill="none" stroke="{PNK}" stroke-width="8"/>' + txt(cx + 38, y + 204, "仮", 50, PNK))
    return s


def scale(cx, cy, tilt):
    """Balance scale; tilt in degrees (+ = left side down)."""
    beam = (f'<rect x="{cx-330}" y="{cy-10}" width="660" height="20" rx="10" fill="{BLK}"/>')
    pans = ""
    for sx, col, lab in ((-1, RED, "引かれた合計"), (1, GRN, "正しい税額")):
        px = cx + sx * 300 * math.cos(math.radians(tilt))
        py = cy - sx * 300 * math.sin(math.radians(tilt))
        pans += (f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px-90:.1f}" y2="{py+150:.1f}" stroke="{BLK}" stroke-width="6"/>'
                 f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px+90:.1f}" y2="{py+150:.1f}" stroke="{BLK}" stroke-width="6"/>'
                 f'<rect x="{px-120:.1f}" y="{py+150:.1f}" width="240" height="24" rx="12" fill="{BLK}"/>'
                 f'<rect x="{px-80:.1f}" y="{py+(40 if sx < 0 else 70):.1f}" width="160" height="{110 if sx < 0 else 80}" rx="10" fill="{col}" stroke="{BLK}" stroke-width="6"/>'
                 + pill(px, py + 222, lab, 36, 270))
    post = (f'<rect x="{cx-12}" y="{cy}" width="24" height="260" fill="{BLK}"/><rect x="{cx-110}" y="{cy+250}" width="220" height="26" rx="10" fill="{BLK}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="22" fill="{GLD}" stroke="{BLK}" stroke-width="7"/>')
    return post + grp(cx, cy, 1, beam, rot=-tilt) + pans


def sheet(cx, cy, label, done):
    x, y = cx - 120, cy - 150
    s = (f'<rect x="{x}" y="{y}" width="240" height="300" rx="12" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
         + "".join(f'<rect x="{x+28}" y="{y+150+k*38}" width="{184 if k < 2 else 120}" height="14" rx="7" fill="#CCC"/>' for k in range(3)))
    for k, line in enumerate(label):
        s += txt(cx, y + 62 + k * 50, line, 40)
    if done:
        s += (f'<circle cx="{x+200}" cy="{y+262}" r="38" fill="{GRN}" stroke="{BLK}" stroke-width="6"/>'
              f'<polyline points="{x+182},{y+262} {x+196},{y+278} {x+220},{y+246}" fill="none" stroke="{WHT}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    return s


def d0(t, T):
    out = head(t, "毎月引かれる所得税", 80, "じつは「仮」の金額", 96)
    step = 0.5 * T / 4
    for k, lab in enumerate(("1月", "2月", "3月", "…")):
        cx = 190 + k * 233
        t0 = 0.25 + k * 0.12
        out += grp(cx, 700, pop(t, t0), payslip(cx, 700, lab, t > 0.3 * T + k * step * 0.6), rot=3 * math.sin(t * 3 + k))
    out += grp(540, 930, pop(t, 0.7 * T), pill(540, 930, "ざっくり計算で引いている", 50, 720, PNK))
    return out


def d1(t, T):
    out = head(t, "年末に会社が", 84, "正しい額を計算しなおす", 84)
    tilt = 9 * (1 - prog(t, 0.35 * T, 1.2)) * math.cos(t * 4) + 9 * prog(t, 0.35 * T, 1.2)
    out += grp(540, 640, pop(t, 0.2), scale(540, 640, tilt))
    return out


def d2(t, T):
    out = head(t, "払いすぎなら戻る", 84, "足りなければ引かれる", 88)
    L = card(110, 560, 400, 400, pill(310, 620, "払いすぎ", 46, 280, GRN) + icon("wallet", 245, 760))
    R = card(570, 560, 400, 400, pill(770, 620, "足りない", 46, 280, RED) + icon("wallet", 705, 760))
    out += grp(310, 760, pop(t, 0.2), L) + grp(770, 760, pop(t, 0.4), R)
    for k in range(3):
        p = prog(t, 0.25 * T + k * 0.25, 0.7)
        if 0 < p:
            out += coin(310 + (k - 1) * 70 * (1 - p), 660 + 150 * p, 34)
    p = prog(t, 0.6 * T, 0.8)
    if p > 0:
        out += grp(770 + 60 * p, 800 - 130 * p, 1, coin(770 + 60 * p, 800 - 130 * p, 34), op=1 - 0.75 * p)
    out += grp(310, 925, pop(t, 0.25 * T + 0.9), txt(310, 940, "もどる", 50, GRN))
    out += grp(770, 925, pop(t, 0.6 * T + 0.5), txt(770, 940, "追加で引く", 50, RED))
    return out


def d3(t, T):
    out = head(t, "ズレる理由", 84, "控除を年末にまとめて引く", 76)
    # tax bar shrinks each time a deduction card lands
    labs = ["生命保険", "地震保険", "家族の変化"]
    n = sum(1 for k in range(3) if t > 0.25 * T + k * 0.2 * T + 0.3)
    w = 780 - 110 * sum(prog(t, 0.25 * T + k * 0.2 * T + 0.3, 0.4) for k in range(3))
    out += grp(540, 610, pop(t, 0.2), txt(150, 600, "税金", 50, BLK, "start") + hbar(290, 560, w - 130, RED, 70))
    for k, lab in enumerate(labs):
        t0 = 0.25 * T + k * 0.2 * T
        y = 760 + (1 - prog(t, t0, 0.4)) * -120
        out += grp(240 + k * 300, y, pop(t, t0, 0.3), card(110 + k * 300, y - 70, 260, 140, txt(240 + k * 300, y + 18, lab, 44)))
    out += grp(540, 940, pop(t, 0.25 * T + 0.3) if n else 0, pill(540, 940, "控除が入ると 税金がへる", 50, 700, GRN))
    return out


def d4(t, T):
    out = head(t, "だから大事なのが", 84, "会社に出す申告書", 100)
    labs = [("扶養控除等", "申告書"), ("基礎控除", "申告書"), ("保険料控除", "申告書")]
    for k, lab in enumerate(labs):
        cx = 220 + k * 320
        t0 = 0.2 + k * 0.3
        out += grp(cx, 740, pop(t, t0), sheet(cx, 740, lab, t > 0.45 * T + k * 0.35), rot=2.5 * math.sin(t * 3 + k * 2))
    return out


def d5(t, T):
    out = head(t, "年末調整は", 84, "1年分の税金の答え合わせ", 76)
    out += monster(250, 700 - 20 * abs(math.sin(t * 6)), RED, t, 0.62 * pop(t, 0.3))
    out += grp(700, 690, pop(t, 0.45), card(560, 580, 300, 220, f'<polyline points="640,690 690,745 790,630" fill="none" stroke="{GRN}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>'))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["毎月の給料から引かれる所得税。", "じつは、仮の金額です。"], cap="毎月の所得税は仮の金額", draw=d0,
         sfx=[(0.0, "whoosh"), (0.25, "pop"), ("f0.3", "tick"), ("f0.375", "tick"), ("f0.45", "tick"), ("f0.525", "tick"), ("f0.7", "ding")]),
    dict(narr=["年末に、会社が1年分の正しい税金を計算しなおします。", "これが、年末調整。"], cap="これが年末調整", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.35+1.2", "ding")]),
    dict(narr=["払いすぎていたら、戻ってくる。", "足りなければ、追加で引かれます。"], cap="差額を給料で精算", note="※通常は12月の給料で精算", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.25", "tick"), ("f0.25+0.9", "ding"), ("f0.6", "drop")]),
    dict(narr=["ズレる理由は、生命保険などの控除を、年末にまとめて引くから。"], cap="控除は年末にまとめて", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.25", "pop"), ("f0.45", "pop"), ("f0.65", "pop")]),
    dict(narr=["だから、会社に出す申告書が大事。", "出さないと、控除が入りません。"], cap="申告書を忘れずに", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "pop"), (0.8, "pop"), ("f0.45", "tick"), ("f0.45+0.35", "tick"), ("f0.45+0.7", "ding")]),
    dict(narr=["年末調整は、1年分の税金の答え合わせ。", "フォローして、お金の仕組みを学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v004_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v004_nenmatsu.mp4")
