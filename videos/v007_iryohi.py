"""#007 医療費控除 — 家族の病院代が年10万円をこえたら、こえた分を所得から引ける。
Sources (fetched 2026-11-13): 国税庁 No.1120 医療費を支払ったとき / No.1122 医療費控除の対象となる医療費 [令和8年4月1日現在法令等]"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def receipt(cx, cy, s=1.0, rot=0.0):
    """Small paper receipt ~80x110 with a pink cross."""
    r = (f'<rect x="{cx-40}" y="{cy-55}" width="80" height="110" rx="6" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
         f'<rect x="{cx-8}" y="{cy-40}" width="16" height="44" fill="{PNK}"/><rect x="{cx-22}" y="{cy-26}" width="44" height="16" fill="{PNK}"/>'
         f'<line x1="{cx-24}" y1="{cy+22}" x2="{cx+24}" y2="{cy+22}" stroke="{BLK}" stroke-width="5"/>'
         f'<line x1="{cx-24}" y1="{cy+38}" x2="{cx+10}" y2="{cy+38}" stroke="{BLK}" stroke-width="5"/>')
    return grp(cx, cy, s, r, rot=rot)


def person(cx, cy, col, s=1.0):
    p = (f'<path d="M{cx-58} {cy+110} Q{cx-58} {cy+20} {cx} {cy+20} Q{cx+58} {cy+20} {cx+58} {cy+110} Z" fill="{col}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx}" cy="{cy-25}" r="46" fill="#FFD9B0" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx-16}" cy="{cy-30}" r="6" fill="{BLK}"/><circle cx="{cx+16}" cy="{cy-30}" r="6" fill="{BLK}"/>'
         f'<path d="M{cx-16} {cy-8} Q{cx} {cy+6} {cx+16} {cy-8}" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>')
    return grp(cx, cy, s, p)


def d0(t, T):
    out = head(t, "家族の病院代が", 80, "年10万円をこえたら？", 84)
    x, y, w, h = 120, 760, 840, 90
    p = prog(t, 0.25 * T, 0.5 * T)
    line = x + w * 0.6
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    fw = w * 0.9 * p
    if fw > 12:
        out += f'<rect x="{x+4}" y="{y+4}" width="{min(fw, w*0.6)-4:.1f}" height="{h-8}" rx="14" fill="{GLD}"/>'
    if fw > w * 0.6:
        out += f'<rect x="{line:.1f}" y="{y+4}" width="{fw-w*0.6:.1f}" height="{h-8}" fill="{PNK}"/>'
    out += f'<line x1="{line}" y1="{y-16}" x2="{line}" y2="{y+h+16}" stroke="{BLK}" stroke-width="8" stroke-dasharray="16 10"/>'
    out += pill(line, y - 60, "10万円", 42, 220)
    for k in range(5):
        tk = 0.25 * T + k * 0.1 * T
        out += receipt(170 + k * 185, 590, pop(t, tk), rot=(-8 + 4 * k))
    val = int(round(15 * p))
    return out + grp(540, 920, 1, txt(540, 985, f"{val}万円", 120, PNK if val > 10 else BLK))


def d1(t, T):
    out = head(t, "計算はひき算", 90, "医療費−保険金−10万円", 76)
    rows = [("払った医療費", 30, GLD, "30万円", 0.05 * T), ("保険金など", 5, BLU, "−5万円", 0.3 * T), ("決まった金額", 10, BLK, "−10万円", 0.45 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 545 + k * 135
        out += grp(250, y + 20, pop(t, t0, 0.3), txt(130, y + 36, lab, 44, BLK, "start"))
        out += hbar(130, y + 52, v * 18 * prog(t, t0 + 0.15, 0.5), col, 56)
        out += grp(130 + v * 18 + 100, y + 84, pop(t, t0 + 0.5, 0.3), txt(130 + v * 18 + 20, y + 98, val, 50, BLK, "start"))
    res = card(560, 800, 420, 185, txt(770, 862, "引ける金額", 42) + txt(770, 958, "15万円", 92, PNK))
    return out + grp(770, 892, pop(t, 0.72 * T), res)


def d2(t, T):
    out = head(t, "家族の分も", 90, "まとめて足せる", 110)
    ppl = [(210, GRN), (540, BLU), (870, RED)]
    for k, (cx, col) in enumerate(ppl):
        out += person(cx, 640 - 8 * abs(math.sin(t * 5 + k)), col, pop(t, 0.2 + k * 0.25))
        t0 = 0.35 * T + k * 0.3
        p = prog(t, t0, 0.6)
        if 0 < p < 1:
            out += receipt(cx + (540 - cx) * p, 760 + 120 * p, 0.8, rot=30 * p)
    out += grp(540, 900, pop(t, 0.3 * T), icon("wallet", 475, 830))
    n = sum(1 for k in range(3) if t > 0.35 * T + k * 0.3 + 0.6)
    return out + grp(760, 900, pop(t, 0.35 * T + 0.6), pill(760, 900, f"領収書 {n}人分", 44, 300, PNK))


def d3(t, T):
    out = head(t, "入るもの・入らないもの", 76, "治療は○ 予防は×", 100)
    L = [("治療・入院", 0.1), ("かぜ薬", 0.22), ("電車・バス代", 0.34)]
    R = [("健康診断", 0.55), ("ビタミン剤", 0.67), ("ガソリン代", 0.79)]
    for col, items, x, mark in ((GRN, L, 100, "○"), (PNK, R, 560, "×")):
        for k, (lab, f) in enumerate(items):
            y = 555 + k * 145
            inner = f'<circle cx="{x+62}" cy="{y+60}" r="42" fill="{col}" stroke="{BLK}" stroke-width="6"/>' + txt(x + 62, y + 80, mark, 56, WHT) + txt(x + 120, y + 78, lab, 46, BLK, "start")
            out += grp(x + 210, y + 60, pop(t, f * T), card(x, y, 420, 120, inner))
    return out


def d4(t, T):
    out = head(t, "ただし", 80, "全額は戻らない", 110)
    g, p = gauge(t, 0.3 * T, 0.8, y=610, h=110)
    out += grp(540, 665, pop(t, 0.2), g)
    out += grp(250, 570, pop(t, 0.25), pill(250, 572, "所得", 44, 200))
    out += grp(830, 572, pop(t, 0.3 * T + 1.0), pill(830, 572, "ここを引く", 40, 260, PNK))
    q = prog(t, 0.6 * T, 0.8)
    out += monster(300, 870, RED, t, (0.62 - 0.14 * q) * pop(t, 0.5 * T), chomp=False)
    return out + grp(690, 870, pop(t, 0.6 * T + 0.5), txt(690, 850, "税金は", 56) + txt(690, 940, "その一部だけ減る", 60, PNK))


def d5(t, T):
    out = head(t, "12月31日までの分を", 76, "確定申告で出す", 110)
    for k in range(6):
        out += receipt(165 + k * 150, 680 - 14 * abs(math.sin(t * 5 + k)), pop(t, 0.2 + k * 0.12), rot=(-10 + 4 * k))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["家族の病院代、年10万円をこえた？", "こえた分は、所得から引けるかも。"], cap="こえた分を所得から引ける", csize=58, draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.25", "tick"), ("f0.35", "tick"), ("f0.45", "tick"), ("f0.55", "tick"), ("f0.65", "tick"), ("f0.75", "ding")]),
    dict(narr=["医療費から、保険金などと10万円を引きます。", "30万円払って保険金5万円なら、15万円。"], cap="例：30万−5万−10万",
         note="※総所得200万円未満は所得の5%・最高200万円", draw=d1, sfx=[(0.0, "whoosh"), ("f0.05", "tick"), ("f0.3", "tick"), ("f0.45", "tick"), ("f0.72", "ding")]),
    dict(narr=["生計がいっしょの家族の分も、まとめて足せます。"], cap="生計が同じ家族はOK", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.45, "pop"), (0.7, "pop"), ("f0.35+0.6", "tick"), ("f0.35+0.9", "tick"), ("f0.35+1.2", "tick")]),
    dict(narr=["治療やかぜ薬、通院の電車代は対象。", "健康診断やビタミン剤は、原則対象外。"], cap="治療は○ 予防は×",
         note="※健康診断は原則×・マイカーのガソリン代も×", draw=d3, sfx=[(0.0, "whoosh")] + [(f"f{f}", "pop") for f in (0.1, 0.22, 0.34, 0.55, 0.67, 0.79)]),
    dict(narr=["ただし全額は戻らず、所得から引くしくみです。"], cap="所得から引くしくみ", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.3", "drop"), ("f0.5", "pop"), ("f0.6+0.5", "ding")]),
    dict(narr=["今年の分は、12月31日までに払った分。", "領収書を集めて、確定申告へ。"], cap="領収書を集めておこう", draw=d5,
         sfx=[(0.0, "whoosh")] + [(0.2 + k * 0.12, "pop") for k in range(6)] + [("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v007_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v007_iryohi.mp4")
