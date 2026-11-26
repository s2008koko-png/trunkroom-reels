"""#046 介護保険料は40歳から — 40歳から64歳までの人（介護保険第2号被保険者）は、健康保険料率に介護保険料率が加わる。
協会けんぽの介護保険料率は全国一律 1.62%（令和8年3月分〈4月納付分〉から・前年度1.59%）。被保険者負担分は折半額。
計算例：標準報酬月額30万円 → 30万円×1.62%＝4,860円、折半額 2,430円（東京支部の保険料額表：健康保険料の折半額
14,775円〈該当しない〉→17,205円〈該当する〉、差 2,430円）。賞与（標準賞与額）にも保険料率をかける。
介護保険に必要な費用は40歳以上の人が納める介護保険料で賄う。
Sources (fetched 2026-11-26): 協会けんぽ 令和8年度保険料率 / 協会けんぽの介護保険料率について /
令和8年3月分からの保険料額表（東京支部）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

EX = "※協会けんぽ・標準報酬月額30万円の例"


def cake(cx, cy, t):
    """Original birthday cake ~320x300 centred on (cx, cy) with a '40' plate and flickering candles."""
    c = (f'<rect x="{cx-160}" y="{cy+10}" width="320" height="130" rx="18" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{cx-120}" y="{cy-80}" width="240" height="100" rx="18" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<path d="M{cx-156} {cy+50} q26 34 52 0 q26 34 52 0 q26 34 52 0 q26 34 52 0 q26 34 52 0 q26 34 52 0" fill="none" stroke="{PNK}" stroke-width="12" stroke-linecap="round"/>'
         + txt(cx, cy + 4, "40", 76, PNK))
    for k, dx in enumerate((-70, 0, 70)):
        f = 1 + 0.25 * math.sin(t * 14 + k * 2)
        c += (f'<rect x="{cx+dx-8}" y="{cy-130}" width="16" height="52" fill="{BLU}" stroke="{BLK}" stroke-width="5"/>'
              f'<ellipse cx="{cx+dx}" cy="{cy-150}" rx="{12*f:.1f}" ry="{20*f:.1f}" fill="{RED}" stroke="{BLK}" stroke-width="5"/>')
    return c


def heart(cx, cy, s=1.0):
    return grp(cx, cy, s, f'<path d="M{cx} {cy+34} C{cx-70} {cy-16} {cx-34} {cy-58} {cx} {cy-22} C{cx+34} {cy-58} {cx+70} {cy-16} {cx} {cy+34} Z" fill="{PNK}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>')


def d0(t, T):
    out = head(t, "40歳になると", 110, "手取りが少しへる", 104)
    out += cake(300, 790, t)
    out += grp(735, 800, 1.5, icon("wallet", 670, 730))
    for k in range(3):  # coins leaving the wallet
        ph = (t * 0.6 + k / 3) % 1
        out += grp(0, 0, 1, coin(760 + 130 * ph, 720 - 150 * ph, 34), op=1 - ph)
    return out


def d1(t, T):
    out = head(t, "はらうのは", 100, "40歳から64歳まで", 96)
    ax = lambda age: 120 + (age - 20) * 14
    out += f'<line x1="120" y1="800" x2="960" y2="800" stroke="{BLK}" stroke-width="10" stroke-linecap="round"/>'
    for a in (20, 40, 60, 80):
        out += f'<line x1="{ax(a)}" y1="780" x2="{ax(a)}" y2="820" stroke="{BLK}" stroke-width="8"/>' + txt(ax(a), 868, f"{a}", 40)
    w = (ax(65) - ax(40)) * prog(t, 0.25 * T, 0.9)
    out += hbar(ax(40), 690, w, GRN, 90)
    out += grp(ax(40), 650, pop(t, 0.25 * T), pill(ax(40), 610, "40歳", 52, 200))
    out += grp(ax(65), 650, pop(t, 0.25 * T + 0.9), pill(ax(65), 610, "64歳", 52, 200))
    out += grp(540, 950, pop(t, 0.65 * T), txt(540, 968, "健康保険料といっしょ", 58, PNK))
    return out


def d2(t, T):
    out = head(t, "料率は1.62%", 110, "本人はその半分", 110)
    v = 1.62 * prog(t, 0.2, 0.9)
    out += grp(540, 660, pop(t, 0.15), txt(540, 720, f"{v:.2f}%", 180))
    t0 = 0.55 * T
    gap = 50 * prog(t, t0, 0.5)
    if t > 0.35 * T:
        s = pop(t, 0.35 * T)
        out += grp(540, 875, s, f'<rect x="{120-gap/2:.1f}" y="810" width="420" height="130" rx="10" fill="{BLK}"/>' + txt(330 - gap / 2, 898, "会社", 66, WHT)
                   + f'<rect x="{540+gap/2:.1f}" y="810" width="420" height="130" rx="10" fill="{GRN}" stroke="{BLK}" stroke-width="8"/>' + txt(750 + gap / 2, 898, "本人", 66))
    return out


def d3(t, T):
    out = head(t, "月給30万円なら", 100, "月2,430円", 140)
    out += grp(540, 610, pop(t, 0.2), txt(540, 632, "30万円 × 1.62%", 78))
    out += grp(540, 720, pop(t, 0.3 * T), txt(540, 740, "÷ 2（本人の分）", 60))
    t0 = 0.5 * T
    v = int(round(2430 * prog(t, t0, 0.8)))
    out += grp(540, 900, pop(t, t0), txt(540, 960, f"{v:,}円", 170, PNK))
    return out


def d4(t, T):
    out = head(t, "ボーナスからも引かれる", 80, "使い道は介護の費用", 92)
    out += grp(260, 610, pop(t, 0.2), pill(260, 610, "毎月の給料", 46, 300))
    out += grp(260, 740, pop(t, 0.2 * T + 0.2), pill(260, 740, "ボーナス", 46, 300, PNK))
    for k in range(4):  # coins flowing to the person who needs care
        ph = (t * 0.55 + k / 4) % 1
        y0 = 610 if k % 2 == 0 else 740
        out += grp(0, 0, 1, coin(430 + 250 * ph, y0 + (690 - y0) * ph, 30), op=min(1, 2.2 - 2.2 * ph))
    out += grp(785, 700, 1.45 * pop(t, 0.3), icon("old", 720, 630))
    out += heart(900, 580, pop(t, 0.5 * T) * (1 + 0.12 * math.sin(t * 8)))
    out += grp(540, 940, pop(t, 0.55 * T), txt(540, 960, "介護サービスの費用に", 62))
    return out


def d5(t, T):
    out = head(t, "40歳になったら", 100, "給与明細を見よう", 104)
    slip = card(400, 545, 280, 290, txt(540, 606, "給与明細", 44))
    for k in range(4):
        hot = k == 2
        col = PNK if hot and int(t / 0.3) % 2 == 0 else ("#BDBDBD" if not hot else PNK2)
        slip += f'<rect x="430" y="{640+k*46}" width="{220 if not hot else 220}" height="24" rx="8" fill="{col}"/>'
    out += grp(540, 690, pop(t, 0.2), slip, rot=3 * math.sin(t * 4))
    out += monster(210, 720 - 16 * abs(math.sin(t * 6)), GRN, t, 0.55 * pop(t, 0.35))
    out += grp(860, 700, pop(t, 0.5), coin(860, 700 - 16 * abs(math.sin(t * 6 + 1)), 60))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["40歳になると、給料の手取りが少しへります。", "介護保険料が、引かれはじめるからです。"], cap="介護保険料がはじまる",
         note="※会社の健康保険に入っている人の場合", draw=d0, sfx=[(0.0, "whoosh"), (0.5, "pop"), ("f0.5", "drop")]),
    dict(narr=["はらうのは、40歳から64歳までの人。", "健康保険料といっしょに引かれます。"], cap="40歳から64歳まで", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.25", "swish"), ("f0.25+0.9", "pop"), ("f0.65", "ding")]),
    dict(narr=["協会けんぽの場合、料率は1.62パーセント。", "本人がはらうのは、その半分です。"], cap="会社と半分ずつ",
         note="※協会けんぽ 令和8年度・全国一律", draw=d2, sfx=[(0.0, "whoosh"), (0.2, "tick"), ("f0.35", "pop"), ("f0.55", "swish")]),
    dict(narr=["月給30万円なら、本人の分は、月2430円です。"], cap="月2,430円ふえる", note=EX, draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.3", "pop"), ("f0.5", "tick"), ("f0.5+0.8", "ding")]),
    dict(narr=["ボーナスからも引かれます。", "集めたお金は、介護サービスの費用になります。"], cap="介護をみんなで支える", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.2+0.2", "pop"), ("f0.5", "ding")]),
    dict(narr=["40歳になったら、給与明細を見てみよう。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v046_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v046_kaigo.mp4")
