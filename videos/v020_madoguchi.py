"""#020 病院の窓口負担（自己負担割合）— 70歳未満3割・就学前2割・70〜74歳2割・75歳以上1割・現役並み所得は3割・高額療養費。
Sources (fetched 2026-11-17):
  協会けんぽ 療養の給付 https://www.kyoukaikenpo.or.jp/benefit/mynumber_insurance_card/index.html
  厚労省 後期高齢者の窓口負担割合の変更等 https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryouhoken/newpage_21060.html
  厚労省 70歳から74歳の方の医療費の窓口負担 https://www.mhlw.go.jp/seisakunitsuite/bunya/kenkou_iryou/iryouhoken/iryouhifutan.html
  厚労省 高額療養費制度の概要 https://www.mhlw.go.jp/content/001729632.pdf"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def d0(t, T):
    out = head(t, "病院代が1万円でも", 80, "払うのは3,000円", 100)
    x, y, w, h = 120, 650, 840, 120
    out += grp(540, 590, pop(t, 0.2), txt(540, 612, "医療費 10,000円", 64))
    a = prog(t, 0.5, 0.6)
    b = prog(t, 0.45 * T, 0.8)
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    if a > 0:
        out += f'<rect x="{x+4}" y="{y+4}" width="{w*0.3*a-4:.1f}" height="{h-8}" rx="12" fill="{PNK}"/>'
    if b > 0:
        out += f'<rect x="{x+w*0.3:.1f}" y="{y+4}" width="{w*0.7*b-4:.1f}" height="{h-8}" rx="12" fill="{BLU}"/>'
    out += grp(246, 830, pop(t, 0.8), txt(246, 842, "あなた3割", 44, PNK2))
    out += grp(246, 930, pop(t, 0.9), txt(246, 950, "3,000円", 76, PNK2))
    out += grp(666, 830, pop(t, 0.45 * T + 0.4), txt(666, 842, "健康保険が7割", 44, BLU))
    return out + grp(666, 930, pop(t, 0.45 * T + 0.5), txt(666, 950, "7,000円", 76, BLU))


def d1(t, T):
    out = head(t, "割合は", 80, "年れいで変わる", 120)
    base, x = 890, 120
    out += f'<line x1="105" y1="{base+4}" x2="975" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    segs = [(150, 2, GRN, "小学校前", 0.3 * T), (360, 3, PNK, "〜69歳", 0.12 * T), (150, 2, BLU, "70〜74歳", 0.5 * T), (180, 1, GLD, "75歳〜", 0.7 * T)]
    for wd, v, col, lab, t0 in segs:
        hh = v * 88 * prog(t, t0, 0.5)
        if hh > 0:
            out += f'<rect x="{x+4}" y="{base-hh:.1f}" width="{wd-8}" height="{hh:.1f}" rx="10" fill="{col}" stroke="{BLK}" stroke-width="6"/>'
        out += grp(x + wd / 2, base - v * 88 - 30, pop(t, t0 + 0.35, 0.3), txt(x + wd / 2, base - v * 88 - 14, f"{v}割", 62))
        out += grp(x + wd / 2, base + 45, pop(t, t0, 0.3), txt(x + wd / 2, base + 56, lab, 34))
        x += wd
    return out


def d2(t, T):
    out = head(t, "ただし70歳以上でも", 80, "所得が多いと3割", 100)
    base = 890
    out += f'<line x1="170" y1="{base+4}" x2="910" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    h1 = 2 * 88 * prog(t, 0.2, 0.5)
    if h1 > 0:
        out += f'<rect x="230" y="{base-h1:.1f}" width="220" height="{h1:.1f}" rx="10" fill="{BLU}" stroke="{BLK}" stroke-width="6"/>'
    out += grp(340, base - 206, pop(t, 0.6, 0.3), txt(340, base - 192, "1〜2割", 60))
    out += grp(340, base + 46, pop(t, 0.2, 0.3), txt(340, base + 58, "一般の所得", 38))
    h2 = 88 * (2 + prog(t, 0.5 * T, 0.7)) * prog(t, 0.3, 0.5)
    if h2 > 0:
        out += f'<rect x="600" y="{base-h2:.1f}" width="220" height="{h2:.1f}" rx="10" fill="{RED}" stroke="{BLK}" stroke-width="6"/>'
    out += grp(710, base - 294, pop(t, 0.5 * T + 0.6, 0.3), txt(710, base - 280, "3割", 68, RED))
    out += grp(710, base + 46, pop(t, 0.3, 0.3), txt(710, base + 58, "現役なみの所得", 38))
    for k in range(3):
        out += grp(900, 800 - k * 80, pop(t, 0.5 * T + k * 0.15), coin(900, 800 - k * 80 - 6 * abs(math.sin(t * 6 + k)), 34))
    return out


def d3(t, T):
    out = head(t, "1か月の自己負担には", 76, "上限がある", 130)
    ys = [930, 852, 774, 696]
    for k, yy in enumerate(ys):
        out += grp(300, yy, pop(t, 0.15 + k * 0.12, 0.25), coin(300, yy, 40))
    out += f'<line x1="150" y1="640" x2="520" y2="640" stroke="{PNK2}" stroke-width="10" stroke-dasharray="20 14"/>'
    out += grp(480, 610, pop(t, 0.3), txt(520, 624, "上限", 46, PNK2, "end"))
    f = prog(t, 0.55 * T, 0.8)
    for k, yy in enumerate((606, 572)):
        s = pop(t, 0.15 + (4 + k) * 0.12, 0.25)
        cx = 300 + (780 - 300) * f
        cy = yy + (830 - yy) * f - 150 * math.sin(math.pi * f)
        out += grp(cx, cy, s * (1 - 0.3 * f), coin(cx, cy, 40, PNK, WHT))
    out += grp(785, 850, pop(t, 0.3), icon("wallet", 700, 770) + "")
    return out + grp(770, 690, pop(t, 0.55 * T + 0.8), pill(770, 690, "こえた分は戻る", 46, 400, BLK, YEL))


def d4(t, T):
    out = head(t, "健康保険があるから", 80, "3割ですむ", 130)
    out += grp(315, 690, pop(t, 0.2), icon("hospital", 250, 620 - 14 * abs(math.sin(t * 5))))
    heart = (f'<path d="M760 760 C640 680 660 590 720 590 C748 590 760 612 760 628 C760 612 772 590 800 590 C860 590 880 680 760 760 Z" fill="{PNK}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>')
    out += grp(760, 680, pop(t, 0.35) * (1 + 0.07 * math.sin(t * 9)), heart)
    out += grp(540, 690, pop(t, 0.5), txt(540, 720, "＋", 90))
    return out + follow(t, 0.5 * T)


SCENES = [
    dict(narr=["病院で1万円かかっても、窓口で払うのは3000円。", "残りの7割は、健康保険が払っています。"], cap="自己負担は3割",
         note="※70歳未満（小学校入学後）の場合", draw=d0, sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "tick"), ("f0.45", "swish"), ("f0.45+0.5", "ding")]),
    dict(narr=["この割合は、年れいで変わります。", "小学校に入る前は2割、70歳からは2割、75歳からは1割。"], cap="年れいで3割・2割・1割",
         note="※一般的な所得の場合", draw=d1, sfx=[(0.0, "whoosh"), ("f0.12", "tick"), ("f0.3", "tick"), ("f0.5", "tick"), ("f0.7", "tick"), ("f0.7+0.4", "ding")]),
    dict(narr=["ただし70歳以上でも、現役なみの所得がある人は、3割です。"], cap="所得が多い人は3割",
         note="※75歳以上は所得により2割の人もいる", draw=d2, sfx=[(0.0, "whoosh"), (0.2, "tick"), (0.3, "tick"), ("f0.5", "swish"), ("f0.5+0.6", "ding")]),
    dict(narr=["さらに、1か月の自己負担には上限があります。", "こえた分は、あとで戻ってきます。"], cap="高額療養費制度",
         note="※上限額は年れいや所得で変わる", draw=d3, sfx=[(0.0, "whoosh")] + [(0.15 + k * 0.12, "tick") for k in range(6)] + [("f0.55", "swish"), ("f0.55+0.8", "ding")]),
    dict(narr=["3割ですむのは、健康保険があるから。", "フォローして、お金の仕組みを学ぼう。"], cap="保険のしくみを知ろう", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), ("f0.5", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v020_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v020_madoguchi.mp4")
