"""#025 国民年金と厚生年金のちがい — 2階建て・1階は20歳以上60歳未満の全員・2階は会社員/公務員・国民年金 月17,920円（令和8年度）・厚生年金18.3%を労使折半。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def person(cx, cy, col, s=1.0):
    """Simple round person ~90px wide, feet at cy+60."""
    p = (f'<path d="M{cx-42} {cy+60} L{cx-42} {cy+5} Q{cx-42} {cy-28} {cx} {cy-28} Q{cx+42} {cy-28} {cx+42} {cy+5} L{cx+42} {cy+60} Z" fill="{col}" stroke="{BLK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-60}" r="32" fill="#FFD9B0" stroke="{BLK}" stroke-width="6"/>'
         f'<circle cx="{cx-11}" cy="{cy-62}" r="4" fill="{BLK}"/><circle cx="{cx+11}" cy="{cy-62}" r="4" fill="{BLK}"/>')
    return grp(cx, cy + 60, s, p)


def slab(x, y, w, h, col, label, size=54):
    return f'<rect x="{x}" y="{y:.0f}" width="{w}" height="{h}" rx="10" fill="{col}" stroke="{BLK}" stroke-width="8"/>' + txt(x + w / 2, y + h / 2 + size * 0.36, label, size, WHT)


def d0(t, T):
    out = head(t, "厚生年金の保険料", 90, "半分は会社が払ってる", 88)
    d = 70 * prog(t, 0.3, 0.8) + 8 * math.sin(t * 5)
    cy, r = 740, 170
    out += f'<path d="M{540-d:.0f} {cy-r} A{r} {r} 0 0 0 {540-d:.0f} {cy+r} Z" fill="{GLD}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
    out += f'<path d="M{540+d:.0f} {cy-r} A{r} {r} 0 0 1 {540+d:.0f} {cy+r} Z" fill="{BLU}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
    out += txt(540 - d - 78, cy + 22, "自分", 60) + txt(540 + d + 78, cy + 22, "会社", 60, WHT)
    return out + grp(540, 960, pop(t, 0.6), txt(540, 978, "半分ずつ", 60))


def d1(t, T):
    out = head(t, "日本の年金は", 90, "2階建て", 140)
    p1 = prog(t, 0.15, 0.5)
    out += f'<line x1="130" y1="984" x2="950" y2="984" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    out += grp(540, 980, p1, slab(190, 820, 700, 160, BLU, "1階 国民年金", 62))
    t2 = 0.45 * T
    dy = -300 * (1 - prog(t, t2, 0.45))
    if t > t2:
        out += slab(290, 660 + dy, 500, 160, GRN, "2階 厚生年金", 56)
    return out + grp(540, 600, pop(t, t2 + 0.45), f'<polygon points="250,660 540,545 830,660" fill="{PNK}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>')


def d2(t, T):
    out = head(t, "1階は みんな", 90, "20歳から60歳未満", 100)
    out += slab(130, 880, 820, 110, BLU, "1階 国民年金", 54)
    for k, (lab, col) in enumerate((("自営業", RED), ("学生", GLD), ("会社員", GRN), ("公務員", PNK), ("無職など", "#999"))):
        cx, t0 = 210 + k * 165, 0.2 + k * 0.3
        out += person(cx, 816 - 10 * abs(math.sin(t * 5 + k)), col, pop(t, t0))
        out += grp(cx, 640, pop(t, t0 + 0.15, 0.25), pill(cx, 640, lab, 32, 156))
    return out


def d3(t, T):
    out = head(t, "2階は", 90, "会社員・公務員", 120)
    out += slab(130, 890, 820, 100, BLU, "1階 国民年金", 50)
    t2 = 0.3 * T
    p = prog(t, t2, 0.6)
    out += grp(730, 890, pop(t, t2 - 0.3, 0.3), slab(540, 770, 400, 120, GRN, "2階 厚生年金", 46))
    for k, (lab, col, up) in enumerate((("自営業", RED, 0), ("学生", GLD, 0), ("会社員", GRN, 1), ("公務員", PNK, 1))):
        cx = (210, 400, 640, 840)[k]
        cy = 826 - (120 * p if up else 0) - (8 * abs(math.sin(t * 5 + k)) if up else 0)
        out += person(cx, cy, col)
        out += pill(cx, cy - 130, lab, 32, 150)
    return out


def d4(t, T):
    out = head(t, "保険料のちがい", 90, "定額 と 給料の18.3%", 84)
    t2 = 0.45 * T
    left = card(100, 560, 420, 420, txt(310, 650, "国民年金", 56) + txt(310, 780, "月17,920円", 66, PNK) + pill(310, 900, "定額", 44, 220))
    right = card(560, 560, 420, 420, txt(770, 650, "厚生年金", 56) + txt(770, 780, "給料×18.3%", 60, BLU) + pill(770, 900, "会社と半分ずつ", 40, 340))
    out += grp(310, 770, pop(t, 0.2), left) + grp(770, 770, pop(t, t2), right)
    if t > 0.5:
        out += coin(480, 575 - 10 * abs(math.sin(t * 6)), 34)
    if t > t2 + 0.3:
        out += coin(940, 575 - 10 * abs(math.sin(t * 6 + 1)), 34)
    return out


def d5(t, T):
    out = head(t, "会社員は老後に", 90, "両方 受け取れる", 110)
    for j, (cx, lab, col) in enumerate(((320, "基礎年金", BLU), (760, "厚生年金", GRN))):
        out += grp(cx, 590, pop(t, 0.2 + j * 0.3), pill(cx, 590, lab, 48, 330, col))
        for k in range(3):
            out += grp(cx, 800 - k * 46, pop(t, 0.5 + j * 0.3 + k * 0.15, 0.25), coin(cx, 800 - k * 46, 40))
    out += grp(540, 720, pop(t, 0.8) * (1 + 0.08 * math.sin(t * 8)), txt(540, 760, "＋", 110, PNK))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["会社員の年金の保険料、半分は会社が払っています。"], cap="保険料は会社と半分ずつ", note="※厚生年金保険料は事業主と折半", draw=d0,
         sfx=[(0.0, "whoosh"), (0.3, "swish"), (0.6, "pop")]),
    dict(narr=["日本の年金は、2階建て。", "1階が国民年金、2階が厚生年金です。"], cap="国民年金と厚生年金", draw=d1,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.45", "swish"), ("f0.45+0.45", "ding")]),
    dict(narr=["1階の国民年金は、20歳から60歳未満の、みんなが入ります。"], cap="国民年金はみんな加入", note="※日本に住む20歳以上60歳未満", draw=d2,
         sfx=[(0.0, "whoosh")] + [(0.2 + k * 0.3, "pop") for k in range(5)]),
    dict(narr=["2階の厚生年金は、会社員や公務員などが入ります。"], cap="厚生年金は会社員など", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.3", "swish"), ("f0.3+0.6", "ding")]),
    dict(narr=["国民年金は、月17920円。", "厚生年金は、給料の18.3パーセントを会社と半分ずつ。"], cap="国民年金は月17,920円", note="※令和8年度の保険料", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "pop")]),
    dict(narr=["だから会社員は、老後に両方もらえます。", "フォローして学ぼう。"], cap="フォローして学ぼう", note="※厚生年金は給料と加入期間で決まる", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "pop"), (0.8, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v025_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v025_nenkin2kai.mp4")
