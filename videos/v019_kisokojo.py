"""#019 令和8年分から 基礎控除58万→62万円・給与所得控除の最低保障額65万→74万円（12月の年末調整で反映）。
Sources (fetched 2026-11-17):
  国税庁 令和8年度税制改正による所得税の基礎控除の引上げ等について https://www.nta.go.jp/users/gensen/2026kiso/index.htm
  同 Q&A（令和8年5月） https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def d0(t, T):
    out = head(t, "今年の年末調整から", 80, "基礎控除が62万円に", 92)
    cx, cy = 540, 740
    p = prog(t, 0.45 * T, 0.8)
    val = int(round(58 + 4 * p))
    sh = (f'<path d="M{cx-190} {cy-170} L{cx+190} {cy-170} L{cx+190} {cy+30} Q{cx+190} {cy+160} {cx} {cy+215} Q{cx-190} {cy+160} {cx-190} {cy+30} Z" fill="{PNK if p >= 1 else WHT}" stroke="{BLK}" stroke-width="10" stroke-linejoin="round"/>'
          + txt(cx, cy - 80, "基礎控除", 56, WHT if p >= 1 else BLK) + txt(cx, cy + 60, f"{val}万円", 108, WHT if p >= 1 else BLK))
    out += grp(cx, cy, pop(t, 0.2) * (1 + 0.12 * p), sh)
    out += grp(190, 600, pop(t, 0.35), pill(190, 600, "58万円", 44, 200))
    return out + grp(880, 600, pop(t, 0.45 * T + 0.8), pill(880, 600, "＋4万円", 44, 200, PNK, WHT), rot=8)


def d1(t, T):
    out = head(t, "引ける金額がふえると", 80, "税金の対象がへる", 100)
    x, y, w, h = 120, 660, 840, 120
    f = 0.35 + 0.12 * prog(t, 0.5 * T, 0.8)
    out += grp(540, 720, pop(t, 0.2), f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{RED}" stroke="{BLK}" stroke-width="8"/>'
               f'<rect x="{x+4}" y="{y+4}" width="{w*f-4:.1f}" height="{h-8}" rx="12" fill="{GLD}"/>'
               f'<line x1="{x+w*f:.1f}" y1="{y-18}" x2="{x+w*f:.1f}" y2="{y+h+18}" stroke="{BLK}" stroke-width="8"/>')
    out += grp(270, 620, pop(t, 0.35), txt(125, 632, "引ける分（控除）", 42, BLK, "start"))
    out += grp(800, 620, pop(t, 0.5), txt(955, 632, "税金の対象", 42, BLK, "end"))
    out += grp(350, 890, pop(t, 0.5 * T), pill(350, 890, "引ける分がふえる", 46, 460, BLK, YEL))
    ms = 0.62 - 0.14 * prog(t, 0.5 * T, 0.8)
    return out + monster(810, 900 - 8 * abs(math.sin(t * 5)), RED, t, ms * pop(t, 0.5))


def d2(t, T):
    out = head(t, "会社員の控除も", 80, "最低65万→74万円", 96)
    base = 920
    out += f'<line x1="250" y1="{base+4}" x2="830" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for x, v, col, lab, t0 in ((320, 65, BLK, "これまで", 0.15 * T), (590, 74, PNK, "今年から", 0.5 * T)):
        hh = v * 3.6 * prog(t, t0, 0.6)
        if hh > 0:
            out += f'<rect x="{x}" y="{base-hh:.1f}" width="170" height="{hh:.1f}" rx="10" fill="{col}" stroke="{BLK}" stroke-width="6"/>'
        out += grp(x + 85, base - v * 3.6 - 30, pop(t, t0 + 0.5, 0.3), txt(x + 85, base - v * 3.6 - 16, f"{v}万円", 60, col))
        out += grp(x + 85, base + 50, pop(t, t0, 0.3), txt(x + 85, base + 62, lab, 42))
    return out + grp(885, 700, pop(t, 0.5 * T + 0.6), pill(885, 700, "＋9万円", 40, 190, PNK, WHT), rot=8)


def d3(t, T):
    out = head(t, "計算し直すのは", 80, "12月の年末調整", 110)
    x0, x1, y = 140, 940, 720
    step = (x1 - x0) / 11
    p = prog(t, 0.1 * T, 0.5 * T)
    out += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{BLK}" stroke-width="10" stroke-linecap="round"/>'
    for k in range(12):
        on = p * 11 >= k
        out += f'<circle cx="{x0+k*step:.1f}" cy="{y}" r="{16 if k < 11 else 22}" fill="{(GLD if k < 11 else PNK) if on else WHT}" stroke="{BLK}" stroke-width="6"/>'
    out += txt(x0, y + 70, "1月", 40) + txt(x0 + 9.6 * step, y + 70, "11月", 40)
    out += grp(480, 610, pop(t, 0.15 * T), pill(480, 610, "11月までは今までどおり", 42, 600))
    if t < 0.6 * T:
        out += coin(x0 + (x1 - x0) * p, y - 60 - 14 * abs(math.sin(t * 8)), 34)
    big = f'<circle cx="{x1}" cy="{y}" r="62" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>' + txt(x1, y + 16, "12月", 46, WHT)
    out += grp(x1, y, pop(t, 0.6 * T) * (1 + 0.05 * math.sin(t * 9)), big)
    return out + grp(560, 910, pop(t, 0.6 * T + 0.2), card(180, 850, 760, 120, txt(560, 930, "1年分をまとめて計算し直す", 50)))


def d5(t, T):
    out = head(t, "もどる金額は", 80, "人によってちがう", 100)
    for k, (cx, r) in enumerate(((290, 44), (540, 70), (790, 56))):
        out += grp(cx, 700, pop(t, 0.25 + k * 0.15), coin(cx, 700 - 26 * abs(math.sin(t * 6 + k * 0.9)), r))
    return out + follow(t, 0.5 * T)


SCENES = [
    dict(narr=["今年から、基礎控除が58万円から62万円に上がりました。", "税金を計算する前に、引ける金額です。"], cap="基礎控除 58万→62万円",
         note="※所得税。合計所得2,350万円以下の場合", draw=d0, sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "swish"), ("f0.45+0.8", "ding")]),
    dict(narr=["引ける金額がふえると、税金がかかる部分がへります。"], cap="税金がかかる部分がへる", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.5", "swish"), ("f0.5+0.8", "pop")]),
    dict(narr=["会社員の経費がわり、給与所得控除。", "その最低額も、65万円から74万円に。"], cap="給与所得控除の最低額",
         note="※給与の収入が220万円未満の人に関係", draw=d2, sfx=[(0.0, "whoosh"), ("f0.15", "tick"), ("f0.5", "tick"), ("f0.5+0.6", "ding")]),
    dict(narr=["11月までの給料は、今までどおりの計算。", "12月の年末調整で、1年分を計算し直します。"], cap="12月にまとめて反映", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.1", "swish"), ("f0.6", "ding"), ("f0.6+0.2", "pop")]),
    dict(narr=["もどる金額があるかは、人によってちがいます。", "フォローして、お金の仕組みを学ぼう。"], cap="明細で控除を見てみよう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.25, "pop"), (0.4, "pop"), (0.55, "pop"), ("f0.5", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v019_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v019_kisokojo.mp4")
