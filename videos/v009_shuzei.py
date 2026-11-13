"""#009 ビールの税金（酒税） — 350ml 1本に約54円。2026年10月にビール・発泡酒・新ジャンルが54.25円に一本化。
Sources (fetched 2026-11-13): 財務省 酒税に関する資料 / 酒税改革資料(d07_0.pdf) / 国税庁 酒税率一覧表（令和8年10月1日〜） / 手持品課税の案内（令和8年9月）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

PER = "※350mlあたりの酒税"


def can(cx, cy, col, s=1.0, tax=0.0, rot=0.0):
    """Original drink can ~150x270 centred at (cx, cy). `tax` 0..1 fills a pink band from the bottom."""
    x, y, w, h = cx - 75, cy - 135, 150, 270
    c = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
    if tax > 0.01:
        th = (h - 16) * tax
        c += f'<rect x="{x+8}" y="{y+h-8-th:.1f}" width="{w-16}" height="{th:.1f}" rx="14" fill="{PNK}"/>'
    c += (f'<rect x="{x+18}" y="{y-14}" width="{w-36}" height="26" rx="10" fill="#DDD" stroke="{BLK}" stroke-width="7"/>'
          f'<ellipse cx="{cx+18}" cy="{y-2}" rx="16" ry="6" fill="{BLK}"/>'
          f'<rect x="{x+22}" y="{y+40}" width="14" height="{h-90}" rx="7" fill="{WHT}" opacity="0.55"/>')
    return grp(cx, cy, s, c, rot=rot)


def d0(t, T):
    out = head(t, "350mlのビール1本", 80, "約54円が酒税", 120)
    p = prog(t, 0.35 * T, 1.0)
    out += can(330, 775, GLD, 1.45, tax=0.3 * p)
    val = int(round(54 * p))
    out += grp(720, 700, 1, txt(720, 700, "このうち", 56))
    return out + grp(720, 850, 1 + 0.08 * math.sin(t * 8) * (p >= 1), txt(720, 880, f"{val}円" if t > 0.35 * T else "？円", 170, PNK if p >= 1 else BLK))


def d1(t, T):
    out = head(t, "2026年10月から", 84, "税金がそろった", 110)
    base, unit = 960, 5.2
    for k, (cx, col, lab, a, b, t0) in enumerate(((300, GLD, "ビール", 63, 54, 0.15 * T), (760, GRN, "新ジャンル", 47, 54, 0.55 * T))):
        p = prog(t, t0 + 1.4, 0.8)
        v = a + (b - a) * p
        hh = v * unit
        out += grp(cx, 600, pop(t, t0), pill(cx, 585, lab, 42, 290, col, BLK if col == GLD else WHT))
        out += f'<rect x="{cx-90}" y="{base-hh:.1f}" width="180" height="{hh:.1f}" rx="10" fill="{col}" stroke="{BLK}" stroke-width="7"/>' if t > t0 else ""
        out += grp(cx, base - hh / 2, pop(t, t0 + 0.2), txt(cx, base - hh / 2 + 24, f"{int(round(v))}円", 68, BLK if col == GLD else WHT))
        arrow = "↓" if b < a else "↑"
        out += grp(cx + 160, 800, pop(t, t0 + 1.6), txt(cx + 160, 830, arrow, 110, PNK))
    y54 = base - 54 * unit
    return out + f'<line x1="110" y1="{y54:.1f}" x2="970" y2="{y54:.1f}" stroke="{BLK}" stroke-width="6" stroke-dasharray="14 10" opacity="{prog(t, 0.55*T+1.0, 0.3):.2f}"/>'


def d2(t, T):
    out = head(t, "いまは3つとも", 84, "同じ54.25円", 120)
    for k, (cx, col, lab) in enumerate(((230, GLD, "ビール"), (540, BLU, "発泡酒"), (850, GRN, "新ジャンル"))):
        t0 = 0.15 + k * 0.3
        out += can(cx, 720 - 10 * abs(math.sin(t * 5 + k)), col, 0.85 * pop(t, t0), tax=0.3 * prog(t, 0.5 * T, 0.6))
        out += grp(cx, 925, pop(t, t0 + 0.2), pill(cx, 925, lab, 42, 280))
    return out


def d3(t, T):
    out = head(t, "チューハイなども", 84, "28円→35円に", 120)
    p = prog(t, 0.4 * T, 0.9)
    out += can(300, 770, "#B58BFF", 1.35 * pop(t, 0.2), tax=0.16 + 0.04 * p)
    val = int(round(28 + 7 * p))
    out += grp(700, 720, pop(t, 0.3), txt(700, 760, f"{val}円", 170, PNK if p >= 1 else BLK))
    return out + grp(700, 900, pop(t, 0.4 * T + 0.9), pill(700, 900, "7円 上がった", 50, 400, PNK))


def d4(t, T):
    out = head(t, "なぜ そろえた？", 84, "似たお酒は同じ税に", 96)
    p = prog(t, 0.4 * T, 1.0)
    ang = -14 * (1 - p)
    beam = (f'<rect x="200" y="842" width="680" height="22" rx="11" fill="{BLK}"/>'
            + can(290, 740, GLD, 0.6) + can(790, 740, GRN, 0.6))
    out += grp(540, 853, pop(t, 0.2), grp(540, 853, 1, beam, rot=ang))
    out += grp(540, 920, pop(t, 0.2), f'<polygon points="540,862 480,985 600,985" fill="{PNK}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>')
    return out + grp(540, 590, pop(t, 0.4 * T + 0.9), pill(540, 590, "公平にするため", 52, 480, BLK, YEL))


def d5(t, T):
    out = head(t, "値段の中に", 84, "税金がかくれてる", 104)
    tag = (f'<polygon points="330,590 690,590 770,690 690,790 330,790" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<circle cx="700" cy="690" r="18" fill="{BLK}"/>' + txt(500, 725, "¥ ???", 96))
    out += grp(540, 690, pop(t, 0.2), tag, rot=3 * math.sin(t * 3))
    q = prog(t, 0.3 * T, 0.5)
    if q > 0:
        out += grp(860, 700 - 60 * q, q, coin(860, 700 - 60 * q, 50, PNK, WHT))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["350ミリのビール1本。", "約54円が、お酒の税金です。"], cap="ビール1本に約54円", note="※酒税54.25円。消費税は別にかかる", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.35", "drop"), ("f0.35+1.0", "ding")]),
    dict(narr=["この10月、ビールは約63円から54円に下がりました。", "新ジャンルは、約47円から54円に上がりました。"], cap="下がった・上がった",
         note="※350ml：63.35円・46.99円→54.25円", draw=d1, sfx=[(0.0, "whoosh"), ("f0.15", "pop"), ("f0.15+1.4", "drop"), ("f0.55", "pop"), ("f0.55+1.4", "swish"), ("f0.55+2.2", "ding")]),
    dict(narr=["ビール、発泡酒、新ジャンル。", "いまは、3つとも同じ税金です。"], cap="3つとも同じ税金", note=PER, draw=d2,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), (0.45, "pop"), (0.75, "pop"), ("f0.5", "ding")]),
    dict(narr=["チューハイなども、28円から35円に上がりました。"], cap="チューハイは7円アップ", note="※350mlあたり・2026年10月から", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.4", "swish"), ("f0.4+0.9", "ding")]),
    dict(narr=["理由は、公平さ。", "似たお酒で税がちがうと、売れゆきに影響するからです。"], cap="公平にするための改正",
         note="※全体の税収は変えない前提（税収中立）", draw=d4, sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.4", "swish"), ("f0.4+0.9", "ding")]),
    dict(narr=["値段の中には、税金がかくれています。", "フォローで、お金のしくみを学ぼう。"], cap="値段の中に税金あり", note="※お酒は20歳になってから", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.3", "tick"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v009_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v009_shuzei.mp4")
