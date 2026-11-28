"""#051 宝くじと税金 — 当せん金付証票の当せん金品には所得税を課さない（当せん金付証票法 第13条）。
当せん金品の総額は発売総額の5割以下（同 第5条）。当せん金の債権は行使できる時から1年間で時効（同 第12条）。
収益金（売上から当せん金・手数料・経費を引いた残額）は発売元の都道府県・指定都市に帰属し、公共事業等に充当（総務省）。
当せん金を人にあげた場合：贈与税は個人から贈与により財産を取得したときにかかる。1/1〜12/31にもらった合計から基礎控除110万円（国税庁 No.4402）。
くじの購入をすすめる内容ではなく、ルールの説明のみ。
Sources (fetched 2026-11-28): e-Gov 当せん金付証票法 / 総務省 宝くじ（地方財政制度）/ 国税庁 No.4402 贈与税がかかる場合（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

GRY, PUR = "#BDBDBD", "#8E5BD9"


def ticket(cx, cy, col=WHT, op=1.0):
    """Original lottery ticket ~380x190 centred on (cx, cy)."""
    out = (f'<rect x="{cx-190}" y="{cy-95}" width="380" height="190" rx="18" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
           f'<rect x="{cx-190}" y="{cy-95}" width="380" height="56" rx="18" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
           + txt(cx - 30, cy - 52, "くじ", 40, WHT)
           + f'<line x1="{cx+100}" y1="{cy-90}" x2="{cx+100}" y2="{cy+90}" stroke="{BLK}" stroke-width="5" stroke-dasharray="12 10"/>'
           + txt(cx - 45, cy + 62, "当たり", 70, BLK)
           + f'<circle cx="{cx+145}" cy="{cy+25}" r="26" fill="{GLD}" stroke="{BLK}" stroke-width="6"/>' + txt(cx + 145, cy + 37, "¥", 32))
    return grp(cx, cy, 1, out, op=op)


def person(cx, cy, col, s=1.0):
    """Original simple person ~150x230 centred on (cx, cy)."""
    out = (f'<path d="M{cx-75} {cy+115} L{cx-75} {cy+30} Q{cx-75} {cy-25} {cx} {cy-25} Q{cx+75} {cy-25} {cx+75} {cy+30} L{cx+75} {cy+115} Z" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<circle cx="{cx}" cy="{cy-68}" r="48" fill="#FFD9B0" stroke="{BLK}" stroke-width="8"/>'
           f'<circle cx="{cx-16}" cy="{cy-72}" r="6" fill="{BLK}"/><circle cx="{cx+16}" cy="{cy-72}" r="6" fill="{BLK}"/>'
           f'<path d="M{cx-14} {cy-52} Q{cx} {cy-40} {cx+14} {cy-52}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy, s, out)


def d0(t, T):
    out = head(t, "宝くじが当たっても", 90, "所得税は0円", 130)
    t0 = 0.45 * T
    out += grp(360, 700, 1, ticket(360, 700 - 10 * abs(math.sin(t * 4))), rot=-6 + 3 * math.sin(t * 3))
    back = prog(t, t0, 0.5)
    mx = 900 - 110 * prog(t, 0.2, 0.8) + 110 * back
    out += monster(mx, 720, RED, t, 0.68, chomp=t < t0, rot=18 * back)
    out += grp(680, 700, pop(t, t0), f'<circle cx="680" cy="700" r="58" fill="{WHT}" stroke="{PNK}" stroke-width="12"/><line x1="640" y1="740" x2="720" y2="660" stroke="{PNK}" stroke-width="12"/>')
    out += grp(420, 930, pop(t, t0 + 0.2), pill(420, 930, "所得税 0円", 62, 480, PNK))
    return out


def d1(t, T):
    out = head(t, "当せん金になるのは", 90, "売上の5割まで", 120)
    out += grp(540, 600, pop(t, 0.15), txt(540, 618, "くじの売上", 54))
    out += f'<rect x="140" y="660" width="800" height="150" rx="14" fill="{GRY}" stroke="{BLK}" stroke-width="8"/>'
    w = 400 * prog(t, 0.3 * T, 0.9)
    if w > 8:
        out += f'<rect x="144" y="664" width="{w-4:.1f}" height="142" rx="10" fill="{GLD}"/>'
    out += f'<line x1="540" y1="640" x2="540" y2="830" stroke="{BLK}" stroke-width="6" stroke-dasharray="14 10"/>'
    out += grp(340, 735, pop(t, 0.3 * T + 0.7), txt(340, 758, "当せん金", 64))
    out += grp(740, 735, pop(t, 0.3 * T + 0.2), txt(740, 756, "のこり", 56, WHT))
    out += grp(540, 920, pop(t, 0.6 * T), pill(540, 920, "5割がじょうげん", 54, 520, PNK))
    return out


def d2(t, T):
    out = head(t, "のこりの収益は", 100, "自治体の事業に", 120)
    out += grp(540, 585, pop(t, 0.15), pill(540, 585, "都道府県・指定都市", 50, 560))
    items = [("road", "公共事業", 100), ("house", "災害対策", 395), ("old", "高齢化対策", 690)]
    for k, (kind, lab, x) in enumerate(items):
        t0 = 0.3 * T + k * 0.18 * T
        inner = icon(kind, x + 75, 720) + txt(x + 140, 940, lab, 50 if len(lab) > 4 else 56)
        out += grp(x + 140, 835, pop(t, t0), card(x, 690, 280, 290, inner))
        if t > t0 - 0.5:
            ph = clamp((t - (t0 - 0.5)) / 0.5)
            cy = 620 + 70 * ph
            out += grp(x + 140, cy, 1, coin(x + 140, cy, 30), op=clamp((1 - ph) * 6))
    return out


def d3(t, T):
    out = head(t, "受け取れるのは", 100, "1年間だけ", 140)
    n = int(clamp((t - 0.2 * T) / (0.5 * T)) * 12 + 0.001)
    done = n >= 12
    out += grp(270, 700, pop(t, 0.15) * 0.92, ticket(270, 700, GRY if done else WHT), rot=-5)
    for k in range(12):
        x, y = 520 + (k % 4) * 112, 560 + (k // 4) * 112
        on = k < n
        out += f'<rect x="{x}" y="{y}" width="98" height="98" rx="12" fill="{PNK if on else WHT}" stroke="{BLK}" stroke-width="6"/>' + txt(x + 49, y + 66, f"{k+1}", 50, WHT if on else BLK)
    out += grp(540, 940, pop(t, 0.72 * T), pill(540, 940, "すぎると時効", 58, 480))
    return out


def d4(t, T):
    out = head(t, "人にあげると", 100, "贈与税の対象", 130)
    out += person(200, 730, GLD, pop(t, 0.15)) + person(660, 730, BLU, pop(t, 0.25))
    out += grp(200, 880, pop(t, 0.3), txt(200, 898, "当たった人", 40)) + grp(660, 880, pop(t, 0.4), txt(660, 898, "もらった人", 40))
    for k in range(3):
        if t > 0.6:
            ph = ((t - 0.6) * 0.7 + k / 3) % 1
            cx, cy = 290 + 290 * ph, 700 - 90 * math.sin(math.pi * ph)
            out += grp(cx, cy, 1, coin(cx, cy, 32), op=clamp((1 - ph) * 5) * clamp(ph * 8))
    t0 = 0.3 * T
    out += monster(880, 690 - 8 * abs(math.sin(t * 5)), PUR, t, 0.6 * pop(t, t0))
    out += grp(880, 820, pop(t, t0 + 0.2), pill(880, 820, "贈与税", 42, 190, PUR))
    out += grp(540, 960, pop(t, 0.58 * T), pill(540, 960, "年110万円までは0円", 50, 600, PNK))
    return out


def d5(t, T):
    out = head(t, "あげるときは", 100, "贈与税に注意", 130)
    for k, cx in enumerate((230, 540, 850)):
        cy = 690 - 30 * abs(math.sin(t * 6 + k * 0.9))
        out += grp(cx, cy, 0.66 * pop(t, 0.2 + k * 0.15), ticket(cx, cy), rot=(-8, 0, 8)[k])
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["宝くじが当たっても、所得税は0円。", "法律で決まっています。"], cap="当せん金に所得税なし",
         note="※当せん金付証票法 第13条", draw=d0, sfx=[(0.0, "whoosh"), ("f0.45", "pop"), ("f0.45+0.2", "ding")]),
    dict(narr=["当せん金にまわるのは、売上の5割まで。"], cap="当せん金は5割以下",
         note="※当せん金付証票法 第5条", draw=d1, sfx=[(0.0, "whoosh"), ("f0.3", "swish"), ("f0.6", "ding")]),
    dict(narr=["経費を引いたのこりは、都道府県や指定都市の収益。", "公共事業などに使われます。"], cap="のこりは自治体の事業へ",
         note="※使い道は発売した自治体が決める", draw=d2, csize=58, sfx=[(0.0, "whoosh"), (0.15, "pop")] + [(f"f{0.3+k*0.18:.2f}", "pop") for k in range(3)]),
    dict(narr=["当せん金を受け取れるのは、1年間。", "すぎると時効です。"], cap="1年で時効になる",
         note="※当せん金付証票法 第12条", draw=d3, sfx=[(0.0, "whoosh"), ("f0.2", "tick"), ("f0.45", "tick"), ("f0.7", "drop")]),
    dict(narr=["ただし、当たったお金を人にあげると、贈与税の対象。", "ねん110万円までは、かかりません。"], cap="あげると贈与税の対象",
         note="※もらった人の1年間の合計で判定", draw=d4, sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.3", "chomp"), ("f0.58", "ding")]),
    dict(narr=["当たっても所得税は0円。あげるときは贈与税に注意。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v051_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v051_takarakuji.mp4")
