"""#044 出産育児一時金 — 健康保険から1児につき50万円（産科医療補償制度に加入の医療機関等で妊娠週数22週以降に出産した場合・
2023年4月1日以降の出産）・被保険者と被扶養者の出産が対象・多胎児は胎児数分・直接支払制度：協会けんぽから医療機関等へ直接支払い、
窓口で高額な出産費用を支払う必要がない・費用が一時金を超えたら超えた額を窓口で支払う（55万円の例）・
下回ったら差額を申請して受け取れる（40万円の例）・直接支払制度は医療機関等で合意文書を交わす（協会けんぽへの事前申請は不要）。
Sources (fetched 2026-11-25): 協会けんぽ 出産育児一時金 / よくあるご質問 子どもが生まれたとき（出産育児一時金）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def baby(cx, cy, s=1.0, col=BLU):
    """Original swaddled baby, ~200x250, centred on (cx, cy)."""
    b = (f'<ellipse cx="{cx}" cy="{cy+50}" rx="92" ry="110" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
         f'<path d="M{cx-70} {cy-10} Q{cx} {cy+70} {cx+70} {cy-10}" fill="none" stroke="{WHT}" stroke-width="10" stroke-linecap="round"/>'
         f'<circle cx="{cx}" cy="{cy-50}" r="72" fill="#FFD9B0" stroke="{BLK}" stroke-width="8"/>'
         f'<path d="M{cx-8} {cy-122} q14 -26 26 -4" fill="none" stroke="{BLK}" stroke-width="7" stroke-linecap="round"/>'
         f'<path d="M{cx-40} {cy-52} q12 -14 24 0" fill="none" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>'
         f'<path d="M{cx+16} {cy-52} q12 -14 24 0" fill="none" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>'
         f'<circle cx="{cx-46}" cy="{cy-28}" r="11" fill="{PNK}" opacity="0.55"/><circle cx="{cx+46}" cy="{cy-28}" r="11" fill="{PNK}" opacity="0.55"/>'
         f'<path d="M{cx-12} {cy-22} q12 12 24 0" fill="none" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>')
    return grp(cx, cy, s, b)


def d0(t, T):
    out = head(t, "赤ちゃんが生まれると", 84, "1人につき 50万円", 100)
    out += baby(245, 770 - 10 * abs(math.sin(t * 4)))
    out += pill(710, 600, "健康保険から", 50, 400)
    for k in range(5):  # coins hopping under the number
        out += coin(490 + k * 105, 950 - 26 * abs(math.sin(t * 5 + k * 0.7)), 34)
    out += grp(710, 780, 1 + 0.04 * math.sin(t * 6), txt(710, 838, "50万円", 160, PNK))
    return out


def d1(t, T):
    out = head(t, "扶養の家族の出産でも", 84, "ふたごなら2人分", 104)
    t0 = 0.5 * T
    out += baby(300, 660 - 10 * abs(math.sin(t * 4)), 0.8 * pop(t, 0.2))
    out += grp(300, 835, pop(t, 0.45), pill(300, 835, "50万円", 54, 280))
    out += baby(780, 660 - 10 * abs(math.sin(t * 4 + 1)), 0.8 * pop(t, t0), PNK)
    out += grp(780, 835, pop(t, t0 + 0.25), pill(780, 835, "50万円", 54, 280))
    out += grp(540, 670, pop(t, t0 + 0.1), txt(540, 700, "＋", 90))
    out += grp(540, 965, pop(t, t0 + 0.6), txt(540, 990, "合計 100万円", 80, PNK))
    return out


def d2(t, T):
    out = head(t, "お金は 病院へ", 96, "直接 払われる", 124)
    out += grp(250, 700, pop(t, 0.2), card(100, 600, 300, 200, txt(250, 722, "健康保険", 62)))
    out += grp(830, 700, pop(t, 0.45), card(680, 600, 300, 200, icon("hospital", 765, 630)))
    if t > 0.8:
        for k in range(3):
            ph = ((t - 0.8) * 0.8 + k / 3) % 1
            out += grp(0, 0, 1, coin(430 + 220 * ph, 700 - 40 * math.sin(ph * math.pi), 34), op=math.sin(ph * math.pi) ** 0.5)
    out += grp(540, 920, pop(t, 0.55 * T), pill(540, 920, "窓口で大金はいらない", 50, 640, PNK))
    return out


def d3(t, T):
    out = head(t, "出産費用が55万円なら", 84, "窓口で5万円", 130)
    x0, y, h = 155, 650, 110
    out += grp(540, 600, pop(t, 0.15), txt(540, 616, "出産費用 55万円", 54))
    w = 700 * prog(t, 0.25, 0.7)
    out += f'<rect x="{x0}" y="{y}" width="{max(w, 1):.1f}" height="{h}" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>'
    out += grp(x0 + 350, 705, pop(t, 0.8), txt(x0 + 350, 724, "健康保険 50万円", 56))
    t0 = 0.5 * T
    w2 = 70 * prog(t, t0, 0.4)
    if w2 > 0:
        out += f'<rect x="{x0+700}" y="{y}" width="{w2:.1f}" height="{h}" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
    out += grp(890, 800, pop(t, t0 + 0.3), txt(925, 818, "↑ 自分で払う", 42, PNK, "end"))
    out += grp(540, 930, pop(t, t0 + 0.6), txt(540, 970, "差の 5万円", 110, PNK))
    return out


def d4(t, T):
    out = head(t, "40万円なら", 90, "差額10万円がもどる", 96)
    x0, y, h = 120, 650, 110
    out += grp(470, 600, pop(t, 0.15), txt(470, 616, "一時金 50万円", 54))
    out += f'<rect x="{x0}" y="{y}" width="560" height="{h}" fill="#BDBDBD" stroke="{BLK}" stroke-width="8"/>'
    out += grp(x0 + 280, 705, pop(t, 0.3), txt(x0 + 280, 724, "出産費用 40万円", 54))
    t0 = 0.45 * T
    p = prog(t, t0, 0.7)
    px, py = x0 + 560 + 110 * p, y + 150 * p
    out += f'<rect x="{px:.1f}" y="{py:.1f}" width="140" height="{h}" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>' + txt(px + 70, py + 74, "10万", 54, WHT)
    out += grp(px + 70, 945, pop(t, t0 + 0.7), txt(px + 70, 960, "あなたへ", 44, PNK))
    out += grp(400, 890, pop(t, t0 + 0.6), pill(400, 890, "申請して受け取る", 52, 520))
    return out


def d5(t, T):
    out = head(t, "手続きは病院で", 90, "書類に合意する", 116)
    out += baby(300, 700 - 14 * abs(math.sin(t * 5)), 0.62 * pop(t, 0.2))
    out += grp(550, 700, pop(t, 0.35), coin(550, 700 - 14 * abs(math.sin(t * 5 + 1)), 62))
    out += baby(800, 700 - 14 * abs(math.sin(t * 5 + 2)), 0.62 * pop(t, 0.5), PNK)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["赤ちゃんが生まれると、健康保険から、子ども1人につき50万円が出ます。"], cap="出産育児一時金", note="※産科医療補償制度の病院で22週以降の出産", draw=d0,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.6", "ding")]),
    dict(narr=["扶養に入っている家族の出産でも出ます。", "ふたごなら、2人分です。"], cap="ふたごなら100万円", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.5", "pop"), ("f0.5+0.6", "ding")]),
    dict(narr=["お金は、健康保険から病院へ、直接払われます。", "窓口で大金を用意しなくて大丈夫。"], cap="直接支払制度", note="※協会けんぽの場合", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.45, "pop"), (0.8, "swish"), ("f0.55", "ding")]),
    dict(narr=["出産費用が55万円なら、窓口で払うのは、差の5万円。"], cap="こえた分だけ払う", draw=d3,
         sfx=[(0.0, "whoosh"), (0.25, "swish"), ("f0.5", "tick"), ("f0.5+0.6", "ding")]),
    dict(narr=["ぎゃくに40万円なら、差額の10万円を、申請して受け取れます。"], cap="安くすんだら差額", draw=d4,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.45", "drop"), ("f0.45+0.6", "ding")]),
    dict(narr=["手続きは、病院で書類に合意すればOK。", "フォローして学ぼう。"], cap="フォローして学ぼう", note="※直接支払制度を使う場合", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v044_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v044_shussan.mp4")
