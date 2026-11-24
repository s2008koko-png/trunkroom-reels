"""#041 セルフメディケーション税制 — 対象の市販薬（スイッチOTC医薬品等）の購入費が年12,000円をこえたら、
こえた分（最高88,000円）を所得から引ける・対象商品は領収書等に表示がある・申告する人がその年に健康診断や予防接種などの
「一定の取組」をしていることが条件・通常の医療費控除とは選択適用（併用不可）・確定申告で明細書を添付。
Sources (fetched 2026-11-24): 国税庁 No.1129 特定一般用医薬品等購入費を支払ったとき（医療費控除の特例）
【セルフメディケーション税制】（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def medbox(cx, cy, col=BLU, s=1.0):
    """Original medicine box with a white cross, 130x150, centred on (cx, cy)."""
    b = (f'<rect x="{cx-65}" y="{cy-75}" width="130" height="150" rx="14" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{cx-65}" y="{cy-75}" width="130" height="34" rx="10" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{cx-12}" y="{cy-22}" width="24" height="76" fill="{WHT}"/><rect x="{cx-38}" y="{cy+4}" width="76" height="24" fill="{WHT}"/>')
    return grp(cx, cy, s, b)


def receipt(cx, cy, hl=0.0, w=300, h=400):
    """Original receipt with a zigzag bottom; hl (0..1) highlights the marked line."""
    x, y = cx - w / 2, cy - h / 2
    pts = f"{x},{y} {x+w},{y} {x+w},{y+h-20} " + " ".join(f"{x+w-(k+1)*w/10:.1f},{y+h-(0 if k % 2 == 0 else 20)}" for k in range(10))
    r = f'<polygon points="{pts}" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
    r += txt(cx, y + 66, "レシート", 44)
    for k in range(4):
        yy = y + 110 + k * 62
        if k == 1:
            r += f'<rect x="{x+18}" y="{yy-10}" width="{w-36}" height="50" rx="8" fill="{PNK}" opacity="{0.25+0.75*hl:.2f}"/>'
            r += txt(x + 48, yy + 30, "★", 40, BLK) + f'<rect x="{x+80}" y="{yy+4}" width="{w-190}" height="22" rx="6" fill="{BLK}"/>'
        else:
            r += f'<rect x="{x+30}" y="{yy+4}" width="{w-140}" height="22" rx="6" fill="{BLK}"/>'
        r += f'<rect x="{x+w-90}" y="{yy+4}" width="60" height="22" rx="6" fill="{BLK}"/>'
    return r


def check(cx, cy, r=42):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GRN}" stroke="{BLK}" stroke-width="7"/>'
            f'<path d="M{cx-r*0.45} {cy} L{cx-r*0.1} {cy+r*0.35} L{cx+r*0.5} {cy-r*0.35}" fill="none" stroke="{WHT}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>')


def d0(t, T):
    out = head(t, "ドラッグストアの薬代が", 80, "年12,000円をこえたら？", 76)
    cols = (BLU, GRN, RED, BLU, GRN)
    for k in range(5):
        cx = 200 + k * 170
        s = 1.0 if k == 0 else pop(t, 0.3 + k * 0.12 * T)
        out += medbox(cx, 680 - 8 * abs(math.sin(t * 5 + k)), cols[k], s)
    p = prog(t, 0.3, 0.6 * T)
    v = int(round(12000 * (0.2 + 0.8 * p) / 100)) * 100
    done = p >= 0.999
    out += txt(540, 950, f"{v:,}円" + ("超" if done else ""), 130, PNK if done else BLK)
    return out


def d1(t, T):
    out = head(t, "こえた分を", 90, "所得から引ける", 116)
    x0, y0, h = 120, 650, 110
    w = 750 * prog(t, 0.2, 0.7)
    t0 = 0.4 * T
    split = t >= t0
    out += grp(495, 600, pop(t, 0.2), txt(495, 616, "薬代 30,000円の例", 46))
    if w > 0:
        out += f'<rect x="{x0}" y="{y0}" width="{min(w, 300):.1f}" height="{h}" fill="{"#BDBDBD" if split else GLD}" stroke="{BLK}" stroke-width="8"/>'
    if w > 300:
        out += f'<rect x="{x0+300}" y="{y0}" width="{w-300:.1f}" height="{h}" fill="{PNK if split else GLD}" stroke="{BLK}" stroke-width="8"/>'
    out += grp(x0 + 150, 705, pop(t, t0), txt(x0 + 150, 722, "12,000円", 46))
    out += grp(x0 + 525, 705, pop(t, t0 + 0.3), txt(x0 + 525, 724, "引ける 18,000円", 50, WHT))
    out += grp(540, 900, pop(t, 0.7 * T), pill(540, 900, "上限 88,000円", 56, 520))
    return out


def d2(t, T):
    out = head(t, "対象の薬は", 90, "レシートに表示がある", 90)
    hl = 0.5 + 0.5 * math.sin(t * 7) if t > 0.45 * T else 0.0
    out += grp(320, 770, pop(t, 0.15), receipt(320, 770, hl), rot=-3)
    out += grp(770, 660, pop(t, 0.45 * T), pill(770, 660, "★ 対象の表示", 44, 400, PNK))
    out += medbox(770, 870 - 8 * abs(math.sin(t * 5)), BLU, pop(t, 0.3))
    return out


def d3(t, T):
    out = head(t, "条件は", 90, "健診などを受けること", 90)
    for k, lab in enumerate(("健康診断", "予防接種", "がん検診")):
        y = 550 + k * 150
        t0 = 0.25 * T + k * 0.2 * T
        out += grp(540, y + 62, pop(t, t0), card(150, y, 780, 124, txt(590, y + 88, lab, 74)))
        out += grp(250, y + 62, pop(t, t0 + 0.25), check(250, y + 62))
    return out


def d4(t, T):
    out = head(t, "ふつうの医療費控除とは", 80, "どちらか1つ", 130)
    sel = int(t / 0.7) % 2 if t > 0.3 * T else -1
    for k, (x, l1, s1, l2, s2) in enumerate(((100, "ふつうの", 46, "医療費控除", 66), (580, "セルフメディ", 46, "ケーション税制", 50))):
        ring = f'<rect x="{x-14}" y="566" width="428" height="288" rx="30" fill="none" stroke="{PNK}" stroke-width="16"/>' if sel == k else ""
        out += grp(x + 200, 710, pop(t, 0.2 + k * 0.25), ring + card(x, 580, 400, 260, txt(x + 200, 680, l1, s1) + txt(x + 200, 770, l2, s2)))
    out += grp(540, 710, pop(t, 0.6), txt(540, 728, "か", 50))
    out += grp(540, 940, pop(t, 0.3 * T), pill(540, 940, "両方は使えない", 52, 480, PNK))
    return out


def d5(t, T):
    out = head(t, "薬のレシートは", 90, "とっておこう", 130)
    out += grp(300, 700, 0.6 * pop(t, 0.2), receipt(300, 700 - 16 * abs(math.sin(t * 5)), 1.0), rot=-6)
    out += medbox(540, 700 - 14 * abs(math.sin(t * 5 + 1)), GRN, pop(t, 0.35))
    out += grp(780, 700, pop(t, 0.5), coin(780, 700 - 14 * abs(math.sin(t * 5 + 2)), 62))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["ドラッグストアの薬代が、1年で1万2000円をこえたら、使える制度があります。"], cap="セルフメディケーション税制", csize=58, draw=d0,
         sfx=[(0.0, "whoosh")] + [(f"f{0.12*k:.2f}+0.3", "pop") for k in range(1, 5)] + [("f0.6+0.3", "ding")]),
    dict(narr=["こえた分を、所得から引けます。", "上限は、8万8000円です。"], cap="最高88,000円", note="※対象の薬代が年3万円の計算例", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), ("f0.4", "pop"), ("f0.7", "ding")]),
    dict(narr=["対象は、決められた市販の薬だけ。", "レシートに、対象の表示があります。"], cap="レシートを確認", note="※スイッチOTC医薬品など", draw=d2,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.45", "ding")]),
    dict(narr=["条件は、その年に、健康診断や予防接種などを、受けていること。"], cap="健診や予防接種が条件", note="※申告する本人が受けていること", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.25", "pop"), ("f0.45", "pop"), ("f0.65", "pop")]),
    dict(narr=["ただし、ふつうの医療費控除とは、どちらか1つしか選べません。"], cap="どちらか1つを選ぶ", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.45, "pop"), ("f0.3", "tick"), ("f0.3+0.7", "tick"), ("f0.3+1.4", "tick")]),
    dict(narr=["確定申告で使うので、レシートはとっておこう。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v041_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v041_selfmed.mp4")
