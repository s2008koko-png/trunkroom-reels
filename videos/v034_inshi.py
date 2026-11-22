"""#034 印紙税（領収書） — 売上代金の受取書は記載金額5万円以上で200円・5万円未満は非課税・100万円超400円…と段階的・
レシートや預り書も同じ・営業に関しない受取書は非課税。
Sources (fetched 2026-11-22): 国税庁 No.7105 金銭又は有価証券の受取書、領収書 / No.7141 印紙税額の一覧表（その2）（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

SKIN = "#FFD9B0"


def receipt(cx, cy, title, amount, w=300, h=330, acol=BLK):
    """Paper slip with a zigzag bottom edge, centred on (cx, cy)."""
    x0, y0 = cx - w / 2, cy - h / 2
    n = 8
    zig = " ".join(f"L{x0 + w - (k + 0.5) * w / n:.1f} {y0 + h + 22:.1f} L{x0 + w - (k + 1) * w / n:.1f} {y0 + h:.1f}" for k in range(n))
    p = f'<path d="M{x0} {y0} L{x0+w} {y0} L{x0+w} {y0+h} {zig} Z" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
    p += txt(cx, y0 + 70, title, 50)
    p += f'<line x1="{x0+30}" y1="{y0+100}" x2="{x0+w-30}" y2="{y0+100}" stroke="{BLK}" stroke-width="5" stroke-dasharray="12 10"/>'
    p += txt(cx, y0 + 190, amount, 58, acol)
    p += f'<rect x="{x0+40}" y="{y0+230}" width="{w-80}" height="16" rx="6" fill="#BBB"/><rect x="{x0+40}" y="{y0+262}" width="{w-150}" height="16" rx="6" fill="#BBB"/>'
    return p


def stamp(cx, cy, label="200円", s=1.0, rot=-8.0):
    """Original small tax stamp: scalloped rectangle with a value."""
    w, h = 150, 180
    dots = "".join(f'<circle cx="{cx - w/2 + k * w/6:.1f}" cy="{yy}" r="9" fill="{PNK}"/>' for k in range(7) for yy in (cy - h / 2, cy + h / 2))
    dots += "".join(f'<circle cx="{xx}" cy="{cy - h/2 + k * h/7:.1f}" r="9" fill="{PNK}"/>' for k in range(8) for xx in (cx - w / 2, cx + w / 2))
    st = (dots + f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="{PNK}"/>'
          f'<rect x="{cx-w/2+14}" y="{cy-h/2+14}" width="{w-28}" height="{h-28}" fill="none" stroke="{WHT}" stroke-width="5"/>'
          + txt(cx, cy - 12, "税", 56, WHT) + txt(cx, cy + 50, label, 40, WHT))
    return grp(cx, cy, s, st, rot=rot)


def person(cx, cy, col, s=1.0):
    p = (f'<path d="M{cx-60} {cy+100} L{cx-60} {cy+30} Q{cx-60} {cy-20} {cx} {cy-20} Q{cx+60} {cy-20} {cx+60} {cy+30} L{cx+60} {cy+100} Z" fill="{col}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-58}" r="42" fill="{SKIN}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx-14}" cy="{cy-60}" r="5" fill="{BLK}"/><circle cx="{cx+14}" cy="{cy-60}" r="5" fill="{BLK}"/>'
         f'<path d="M{cx-12} {cy-44} Q{cx} {cy-34} {cx+12} {cy-44}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy, s, p)


def d0(t, T):
    out = head(t, "5万円以上の領収書に", 84, "200円の税金", 130)
    out += grp(400, 760, pop(t, 0.15), receipt(400, 760, "領収書", "50,000円", 400, 380), rot=-4)
    # the stamp slams down
    t0 = 0.4 * T
    x = clamp((t - t0) / 0.25)
    if x > 0:
        s = 2.2 - 1.2 * (1 - (1 - x) ** 3)
        out += stamp(790, 760, s=s, rot=-8 + 3 * math.sin(t * 5) * (x >= 1))
    return out


def d1(t, T):
    out = head(t, "この税金の名前は", 84, "印紙税", 150)
    out += grp(290, 740, pop(t, 0.2), receipt(290, 740, "領収書", "49,999円", 330, 330))
    out += grp(790, 740, pop(t, 0.35), receipt(790, 740, "領収書", "50,000円", 330, 330, PNK))
    out += grp(290, 965, pop(t, 0.45 * T), pill(290, 965, "0円", 50, 220, GRN))
    out += grp(790, 965, pop(t, 0.45 * T + 0.5), pill(790, 965, "200円", 50, 240, PNK))
    out += grp(540, 740, pop(t, 0.5), txt(540, 765, "→", 80))
    return out


def d2(t, T):
    out = head(t, "金額が大きいほど", 84, "税金も上がる", 124)
    base = 990
    out += f'<line x1="100" y1="{base}" x2="980" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    rows = [("5万〜", "200円", 60), ("100万超", "400円", 115), ("200万超", "600円", 170), ("300万超", "1,000円", 250), ("500万超", "2,000円", 350)]
    step = (0.7 * T - 0.4) / 5
    for k, (lab, val, hh) in enumerate(rows):
        t0 = 0.4 + k * step
        p = prog(t, t0, 0.4)
        if p <= 0:
            continue
        x = 120 + k * 172
        h = hh * p
        out += f'<rect x="{x}" y="{base-h:.1f}" width="150" height="{h:.1f}" fill="{PNK if k == 4 else GLD}" stroke="{BLK}" stroke-width="7"/>'
        out += grp(x + 75, base - h - 28, pop(t, t0 + 0.2, 0.25), txt(x + 75, base - h - 16, val, 40, PNK if k == 4 else BLK))
        out += grp(x + 75, base - 26, pop(t, t0 + 0.1, 0.25), txt(x + 75, base - 16, lab, 32, WHT if k == 4 else BLK))
    return out


def d3(t, T):
    out = head(t, "名前がちがっても", 84, "あつかいは同じ", 116)
    for k, (lab, t0) in enumerate((("領収証", 0.2), ("レシート", 0.45 * T), ("預り書", 0.65 * T))):
        cx = 220 + k * 320
        dy = -10 * abs(math.sin(t * 4 + k))
        out += grp(cx, 760, pop(t, t0), receipt(cx, 740 + dy, "", "", 260, 300) + txt(cx, 668 + dy, lab, 50))
    out += grp(540, 965, pop(t, 0.65 * T + 0.4), pill(540, 965, "受け取りの証明", 44, 420, PNK))
    return out


def d4(t, T):
    out = head(t, "商売ではない個人には", 84, "かからない", 130)
    out += person(220, 760, BLU, pop(t, 0.2)) + person(860, 760, GRN, pop(t, 0.3))
    # a slip passes between two people
    p = prog(t, 0.3 * T, 0.9)
    x = 330 + 370 * p
    out += grp(x, 770, pop(t, 0.3 * T, 0.3), f'<rect x="{x-45}" y="{715 - 50*math.sin(math.pi*p):.1f}" width="90" height="110" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
               f'<line x1="{x-25}" y1="{748 - 50*math.sin(math.pi*p):.1f}" x2="{x+25}" y2="{748 - 50*math.sin(math.pi*p):.1f}" stroke="{BLK}" stroke-width="5"/>'
               f'<line x1="{x-25}" y1="{775 - 50*math.sin(math.pi*p):.1f}" x2="{x+25}" y2="{775 - 50*math.sin(math.pi*p):.1f}" stroke="{BLK}" stroke-width="5"/>')
    k = pop(t, 0.6 * T)
    out += stamp(540, 660, "", s=0.62 * k, rot=0)
    out += grp(540, 660, k, f'<line x1="470" y1="590" x2="610" y2="730" stroke="{BLK}" stroke-width="20" stroke-linecap="round"/>'
                             f'<line x1="610" y1="590" x2="470" y2="730" stroke="{BLK}" stroke-width="20" stroke-linecap="round"/>')
    out += grp(540, 950, pop(t, 0.6 * T + 0.3), pill(540, 950, "非課税", 50, 250, GRN))
    return out


def d5(t, T):
    out = head(t, "高い買い物の領収書を", 84, "見てみよう", 130)
    out += grp(300, 700, pop(t, 0.2), receipt(300, 690 - 10 * abs(math.sin(t * 5)), "領収書", "", 240, 250), rot=-5)
    out += stamp(620, 700 - 12 * abs(math.sin(t * 5 + 1)), s=0.8 * pop(t, 0.35))
    out += grp(850, 700, pop(t, 0.5), coin(850, 700 - 12 * abs(math.sin(t * 5 + 2)), 60))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["5万円以上の領収書には、200円の税金がかかります。"], cap="領収書にも税金がある", draw=d0,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.4+0.2", "chomp"), ("f0.4+0.5", "ding")]),
    dict(narr=["これを、印紙税といいます。", "5万円未満なら、かかりません。"], cap="5万円未満は0円", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), ("f0.45", "tick"), ("f0.45+0.5", "tick")]),
    dict(narr=["100万円をこえると、400円。", "金額が大きいほど、上がっていきます。"], cap="100万円超は400円", note="※売上代金の受取書の場合", draw=d2,
         sfx=[(0.0, "whoosh")] + [(f"f{0.14 * k:.2f}+0.4", "tick") for k in range(5)]),
    dict(narr=["名前は、かんけいありません。", "レシートや預り書も、おなじあつかいです。"], cap="レシートも対象", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "pop"), ("f0.65", "pop")]),
    dict(narr=["ただし、商売ではない個人の受取書には、かかりません。"], cap="個人どうしは非課税", note="※営業に関しない受取書は非課税", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.3", "swish"), ("f0.6", "ding")]),
    dict(narr=["大きな買い物をしたら、領収書を見てみよう。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v034_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v034_inshi.mp4")
