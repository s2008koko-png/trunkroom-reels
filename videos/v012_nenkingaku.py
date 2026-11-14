"""#012 年金はいくら？（令和8年度） — 国民年金の満額 月70,608円（前年度69,308円・+1.9%）、保険料 月17,920円、
会社員夫婦モデル 月237,279円（平均的な収入で40年就業・老齢厚生年金＋2人分の老齢基礎年金）。
Sources (fetched 2026-11-14): 日本年金機構 令和8年4月分からの年金額等について / 国民年金保険料（更新日2026年4月1日）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def disc(cx, cy, w=170):
    """One flat coin seen from the side (for stacks)."""
    return (f'<ellipse cx="{cx}" cy="{cy+22:.1f}" rx="{w/2}" ry="24" fill="#C99400" stroke="{BLK}" stroke-width="6"/>'
            f'<rect x="{cx-w/2}" y="{cy:.1f}" width="{w}" height="22" fill="#C99400"/>'
            f'<ellipse cx="{cx}" cy="{cy:.1f}" rx="{w/2}" ry="24" fill="{GLD}" stroke="{BLK}" stroke-width="6"/>')


def jar(cx, cy, fill=0.0, s=1.0):
    """Original savings jar ~220x280; `fill` 0..1 raises the gold level."""
    lv = 190 * fill
    j = (f'<rect x="{cx-100}" y="{cy-100}" width="200" height="230" rx="36" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         + (f'<rect x="{cx-92}" y="{cy+122-lv:.1f}" width="184" height="{lv:.1f}" rx="26" fill="{GLD}"/>' if lv > 4 else "")
         + f'<rect x="{cx-76}" y="{cy-138}" width="152" height="44" rx="12" fill="{BLU}" stroke="{BLK}" stroke-width="8"/>'
         + f'<rect x="{cx-70}" y="{cy-30}" width="140" height="64" rx="10" fill="{BLK}"/>' + txt(cx, cy + 18, "年金", 46, YEL))
    return grp(cx, cy, s, j)


def d0(t, T):
    out = head(t, "国民年金の満額は", 84, "月70,608円", 130)
    for k in range(7):
        t0 = 0.25 + k * 0.1 * T
        if t > t0:
            y = 940 - k * 44 - 260 * (1 - prog(t, t0, 0.3))
            out += disc(230, y)
    p = prog(t, 0.25, 0.7 * T)
    out += grp(660, 640, pop(t, 0.2), pill(660, 640, "令和8年度・月額", 44, 420))
    return out + grp(660, 800, 1 + 0.06 * math.sin(t * 8) * (p >= 1), txt(660, 840, "70,608円", 118, PNK if p >= 1 else BLK))


def d1(t, T):
    out = head(t, "前の年度より", 84, "1.9%アップ", 130)
    up = 45 * prog(t, 0.45 * T, 0.7)
    out += grp(290, 800, pop(t, 0.15), card(110, 700, 360, 230, txt(290, 770, "令和7年度", 46) + txt(290, 880, "69,308円", 72)))
    out += grp(770, 800, pop(t, 0.3 * T), f'<g transform="translate(0,{-up:.1f})">' + card(590, 700, 380, 230, txt(780, 770, "令和8年度", 46, PNK) + txt(780, 880, "70,608円", 76, PNK)) + '</g>')
    out += grp(530, 800, pop(t, 0.3 * T + 0.2), txt(530, 835, "→", 80))
    return out + grp(540, 585, pop(t, 0.45 * T + 0.6) * (1 + 0.05 * math.sin(t * 9)), pill(540, 585, "月 +1,300円", 48, 380, PNK))


def d2(t, T):
    out = head(t, "払う保険料は", 84, "月17,920円", 130)
    out += grp(215, 720, 1.5 * pop(t, 0.15), icon("wallet", 150, 640))
    n = clamp((t - 0.5) / max(0.1, T - 1.2))
    out += jar(760, 760, 0.15 + 0.8 * n, pop(t, 0.3))
    if t > 0.5:
        p = ((t - 0.5) / 0.8) % 1.0
        out += coin(300 + 460 * p, 640 - 110 * math.sin(math.pi * p), 40)
    return out + grp(380, 945, pop(t, 0.5), pill(380, 945, "国民年金・令和8年度", 42, 470))


def d3(t, T):
    out = head(t, "会社員の夫婦モデル", 84, "月23万7,279円", 104)
    for k, x in enumerate((180, 545)):
        t0 = 0.2 + k * 0.3
        out += grp(x + 177, 890, pop(t, t0), f'<rect x="{x}" y="830" width="355" height="130" rx="14" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>' + txt(x + 177, 915, "基礎年金", 56))
    td = 0.45 * T
    if t > td:
        y = 690 - 200 * (1 - prog(t, td, 0.4))
        out += f'<rect x="180" y="{y:.1f}" width="720" height="134" rx="14" fill="{BLU}" stroke="{BLK}" stroke-width="8"/>' + txt(540, y + 88, "厚生年金", 64, WHT)
    return out + grp(540, 590, pop(t, td + 0.5), pill(540, 590, "2人分 ＋ 厚生年金", 48, 520, BLK, YEL))


def d4(t, T):
    out = head(t, "ただしこれは目安", 84, "人によってちがう", 104)
    out += f'<line x1="150" y1="964" x2="930" y2="964" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k, col in enumerate((RED, BLU, GRN, PNK)):
        x = 190 + k * 190
        h = (150 + 110 * math.sin(t * 2.6 + k * 1.7)) * prog(t, 0.2 + k * 0.15, 0.4) + 60 * prog(t, 0.2 + k * 0.15, 0.4)
        out += f'<rect x="{x}" y="{960-h:.1f}" width="130" height="{h:.1f}" rx="10" fill="{col}" stroke="{BLK}" stroke-width="7"/>' if h > 2 else ""
        out += grp(x + 65, 930 - h, pop(t, 0.4 + k * 0.15), txt(x + 65, 940 - h, "？", 70))
    return out


def d5(t, T):
    out = head(t, "年金は", 100, "数字で知っておこう", 96)
    for k, cx in enumerate((270, 540, 810)):
        out += grp(cx, 700, pop(t, 0.3 + k * 0.15), coin(cx, 700 - 30 * abs(math.sin(t * 6 + k * 0.8)), 78))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["国民年金は、満額で月に7万608円。", "これは、令和8年度の金額。"], cap="令和8年度の満額(月額)", csize=58, note="※老齢基礎年金・昭和31年4月2日以後生まれ", draw=d0,
         sfx=[(0.0, "whoosh")] + [(f"f{0.1*k:.1f}+0.25", "tick") for k in range(7)] + [("f0.7+0.25", "ding")]),
    dict(narr=["前の年度は、6万9308円。", "1.9パーセント上がりました。"], cap="前の年度から1.9%アップ", csize=58, draw=d1,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.3", "pop"), ("f0.45", "swish"), ("f0.45+0.6", "ding")]),
    dict(narr=["払う保険料は、月に1万7920円。"], cap="保険料は月17,920円", note="※国民年金保険料（令和8年度）", draw=d2,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.9, "tick"), (1.7, "tick"), (2.5, "tick")]),
    dict(narr=["会社員だった人は、厚生年金が上に乗ります。", "夫婦2人のモデルで、月に約23万7千円。"], cap="夫婦2人分の標準的な額", note="※平均的な収入で40年働いた場合・夫婦2人分", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "pop"), ("f0.45", "drop"), ("f0.45+0.5", "ding")]),
    dict(narr=["ただし、これは目安。", "働き方や期間で、金額は変わります。"], cap="金額は人によってちがう", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), (0.65, "pop")]),
    dict(narr=["年金は、数字で知っておこう。", "フォローして、お金を学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), (0.6, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v012_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v012_nenkingaku.mp4")
