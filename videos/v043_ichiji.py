"""#043 一時所得 — 懸賞や福引きの賞金品・競馬や競輪の払戻金・生命保険の一時金や損害保険の満期返戻金など
（営利を目的とする継続的行為から生じたもの等を除く）・計算：総収入金額−収入を得るために支出した金額（直接要した金額に限る）
−特別控除額（最高50万円）・その2分の1を給与所得など他の所得と合計して税額を計算・一時所得の合計が年50万円以下なら
確定申告は不要・マイナポイント（カード取得等で付与されたもの）も一時所得。
Sources (fetched 2026-11-25): 国税庁 No.1490 一時所得 / No.1490 一時所得 Q&A（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

EX = "※賞金100万円・直接の支出10万円の例"


def ticket(cx, cy, s=1.0, rot=0.0):
    """Original winning ticket, 280x160, centred on (cx, cy)."""
    b = (f'<rect x="{cx-140}" y="{cy-80}" width="280" height="160" rx="18" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<circle cx="{cx-140}" cy="{cy}" r="22" fill="{YEL}" stroke="{BLK}" stroke-width="8"/><circle cx="{cx+140}" cy="{cy}" r="22" fill="{YEL}" stroke="{BLK}" stroke-width="8"/>'
         f'<line x1="{cx-70}" y1="{cy-70}" x2="{cx-70}" y2="{cy+70}" stroke="{BLK}" stroke-width="5" stroke-dasharray="12 10"/>'
         + txt(cx + 30, cy + 30, "当たり", 62, PNK))
    return grp(cx, cy, s, b, rot=rot)


def d0(t, T):
    out = head(t, "懸賞や競馬のもうけ", 84, "年50万円まで 0円", 100)
    out += ticket(300, 700, 1.0, 6 * math.sin(t * 6))
    for k in range(4):  # coins jumping out of the ticket
        ph = (t * 0.7 + k / 4) % 1
        out += grp(0, 0, 1, coin(330 + 90 * k * ph, 600 - 120 * math.sin(ph * math.pi) + 40 * ph, 30), op=1 - ph * 0.8)
    out += monster(800, 730, RED, t, 0.7, chomp=False)
    out += grp(860, 560, 1, txt(900 + 6 * math.sin(t * 2), 590 - 8 * math.sin(t * 2), "Zzz", 54))
    out += grp(540, 945, 1 if t < 0.5 else 1 + 0.04 * math.sin(t * 7), pill(540, 945, "所得税 0円", 60, 440, PNK))
    return out


def d1(t, T):
    out = head(t, "これは", 90, "一時所得", 140)
    for k, lab in enumerate(("懸賞の賞金", "競馬・競輪の払戻金", "保険の満期金など")):
        y = 550 + k * 150
        t0 = 0.2 * T + k * 0.2 * T
        out += grp(540, y + 62, pop(t, t0), card(150, y, 780, 124, txt(600, y + 86, lab, 64)))
        out += grp(240, y + 62, pop(t, t0 + 0.2), coin(240, y + 62 - 6 * abs(math.sin(t * 5 + k)), 40))
    return out


def d2(t, T):
    out = head(t, "かかったお金と", 90, "最高50万円を引く", 104)
    x0, y, h = 120, 650, 110
    out += grp(540, 600, pop(t, 0.15), txt(540, 616, "入ったお金 100万円", 54))
    w = 840 * prog(t, 0.2, 0.6)
    t1, t2, t3 = 0.3 * T, 0.55 * T, 0.78 * T
    segs = [(0, 84, "#BDBDBD" if t > t1 else GLD), (84, 420, PNK if t > t2 else GLD), (504, 336, GLD)]
    for a, ww, col in segs:
        vis = min(ww, w - a)
        if vis > 0:
            out += f'<rect x="{x0+a}" y="{y}" width="{vis:.1f}" height="{h}" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
    out += grp(x0 + 60, 810, pop(t, t1), txt(x0, 808, "かかった", 34, BLK, "start") + txt(x0, 852, "10万円", 40, BLK, "start"))
    out += grp(x0 + 294, 705, pop(t, t2), txt(x0 + 294, 722, "−50万円", 54, WHT))
    out += grp(x0 + 294, 810, pop(t, t2 + 0.2), txt(x0 + 294, 812, "特別控除", 38))
    out += grp(x0 + 672, 705, pop(t, t3), txt(x0 + 672, 724, "40万円", 60))
    out += grp(540, 940, pop(t, t3 + 0.2), pill(540, 940, "のこり 40万円", 56, 500))
    return out


def d3(t, T):
    out = head(t, "税金の計算に入るのは", 80, "のこりの半分だけ", 104)
    t0 = 0.35 * T
    p = prog(t, t0, 0.5)
    gap = 60 * p
    out += f'<rect x="{240-gap/2:.1f}" y="610" width="300" height="110" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="{540+gap/2:.1f}" y="610" width="300" height="110" fill="{GLD if p <= 0 else WHT}" stroke="{BLK}" stroke-width="8" stroke-dasharray="{"0" if p <= 0 else "18 12"}" opacity="{1-0.6*p:.2f}"/>'
    if p <= 0:
        out += grp(540, 665, pop(t, 0.2), txt(540, 686, "のこり 40万円", 58))
    else:
        out += grp(390 - gap / 2, 665, pop(t, t0), txt(390 - gap / 2, 686, "20万円", 60))
        out += grp(690 + gap / 2, 665, pop(t, t0 + 0.2), txt(690 + gap / 2, 684, "計算に入れない", 36), op=0.7)
    out += grp(540, 800, pop(t, 0.6 * T), txt(540, 818, "給料などと合計するのは", 50))
    out += grp(540, 920, pop(t, 0.6 * T + 0.25), txt(540, 970, "20万円", 140, PNK))
    return out


def d4(t, T):
    out = head(t, "ただし50万円は", 90, "1年間の合計", 124)
    labs = ("懸賞", "競馬", "ポイント")
    for k, lab in enumerate(labs):
        cx = 230 + k * 310
        t0 = 0.15 + k * 0.18 * T
        out += grp(cx, 590, pop(t, t0), pill(cx, 590, lab, 50, 270))
        if t > t0 + 0.3:
            ph = ((t - t0) * 0.9) % 1
            out += grp(0, 0, 1, coin(cx + (540 - cx) * ph * 0.5, 670 + 110 * ph, 30), op=1 - ph * 0.6)
    out += grp(540, 870, pop(t, 0.55 * T), card(170, 790, 740, 170, txt(540, 900, "ぜんぶ足して 50万円", 68)))
    return out


def d5(t, T):
    out = head(t, "たまたまのお金にも", 84, "ルールがある", 124)
    out += ticket(300, 700 - 14 * abs(math.sin(t * 5)), 0.8 * pop(t, 0.2), -6)
    out += grp(560, 700, pop(t, 0.35), coin(560, 700 - 14 * abs(math.sin(t * 5 + 1)), 62))
    out += ticket(810, 700 - 14 * abs(math.sin(t * 5 + 2)), 0.8 * pop(t, 0.5), 6)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["懸賞の賞金や、競馬の払戻金。", "もうけが、ねん50万円までなら、所得税はかかりません。"], cap="もうけ50万円まで0円", note="※一時所得の特別控除は最高50万円", draw=d0,
         sfx=[(0.0, "whoosh"), (0.4, "pop"), ("f0.5", "ding")]),
    dict(narr=["これは一時所得。", "たまたま入った、一回きりのお金です。"], cap="一回きりのお金", note="※仕事や営利目的で続けるものは除く", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.2", "pop"), ("f0.4", "pop"), ("f0.6", "pop")]),
    dict(narr=["入ったお金から、かかったお金を引き、さらに最高50万円を引きます。"], cap="最高50万円を引く", note=EX, draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), ("f0.3", "tick"), ("f0.55", "tick"), ("f0.78", "ding")]),
    dict(narr=["のこりの半分だけが、給料などと合計されて、税金の計算に入ります。"], cap="のこりの半分だけ", note=EX, draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.35", "swish"), ("f0.6+0.25", "ding")]),
    dict(narr=["ただし50万円は、1年間の合計。", "マイナポイントなども、一時所得です。"], cap="1年分を合計する", draw=d4,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.18+0.15", "pop"), ("f0.36+0.15", "pop"), ("f0.55", "ding")]),
    dict(narr=["たまたまのお金にも、ルールあり。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v043_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v043_ichiji.mp4")
