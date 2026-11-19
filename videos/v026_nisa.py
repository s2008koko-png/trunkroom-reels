"""#026 NISAの税金面のしくみ（ルールの説明のみ）— 配当・譲渡益が非課税・ふつうは20%（所得税15%＋住民税5%）・年120万円/240万円・保有限度1,800万円・損失はないものとみなす。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def line_chart(pts, p, col):
    """Draw a polyline through pts up to fraction p (0..1); returns (svg, tip_x, tip_y)."""
    n = len(pts) - 1
    f = clamp(p) * n
    k = min(int(f), n - 1)
    a, b = pts[k], pts[k + 1]
    tx, ty = a[0] + (b[0] - a[0]) * (f - k), a[1] + (b[1] - a[1]) * (f - k)
    s = " ".join(f"{x},{y}" for x, y in pts[:k + 1]) + f" {tx:.0f},{ty:.0f}"
    return f'<polyline points="{s}" fill="none" stroke="{col}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>', tx, ty


def axes():
    return f'<path d="M150 560 L150 970 L940 970" fill="none" stroke="{BLK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'


def d0(t, T):
    out = head(t, "投資のもうけの税金", 84, "NISAなら 0円", 130)
    pts = [(170, 930), (300, 870), (420, 895), (560, 790), (700, 765), (860, 640)]
    ln, tx, ty = line_chart(pts, prog(t, 0.2, 2.2), GRN)
    out += axes() + ln + coin(tx, ty - 8 * abs(math.sin(t * 6)), 38)
    return out + grp(380, 640, pop(t, 0.5) * (1 + 0.04 * math.sin(t * 8)), pill(380, 640, "税金 0円", 64, 400, PNK))


def d1(t, T):
    out = head(t, "ふつうは もうけの", 84, "20%が税金", 130)
    t2 = 0.3 * T
    for k in range(10):
        x, y, s = 135 + k * 90, 620, pop(t, 0.1 + k * 0.05, 0.2)
        if k >= 8:
            q = prog(t, t2 + (k - 8) * 0.3, 0.6)
            x, y, s = x + (800 - x) * q, y + (850 - y) * q, s * (1 - 0.8 * q)
        out += grp(x, y, s, coin(x, y, 38))
    out += monster(800, 850, RED, t, 0.6 * pop(t, 0.3))
    out += grp(340, 790, pop(t, t2 + 0.3), pill(340, 790, "所得税 15%", 48, 400))
    return out + grp(340, 910, pop(t, t2 + 0.9), pill(340, 910, "住民税 5%", 48, 400, BLU))


def d2(t, T):
    out = head(t, "1年に買える上限は", 84, "2つの枠で決まる", 104)
    rows = [("つみたて投資枠", 120, PNK, "120万円", 0.1 * T), ("成長投資枠", 240, BLU, "240万円", 0.5 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 570 + k * 210
        out += grp(300, y + 30, pop(t, t0, 0.3), txt(130, y + 44, lab, 52, BLK, "start"))
        out += hbar(130, y + 70, v * 2.5 * prog(t, t0 + 0.15, 0.7), col, 90)
        out += grp(130 + v * 2.5 + 110, y + 115, pop(t, t0 + 0.7, 0.3), txt(130 + v * 2.5 + 22, y + 136, val, 56, BLK, "start"))
    return out


def d3(t, T):
    out = head(t, "ずっと持てる上限は", 80, "1,800万円", 140)
    p = prog(t, 0.15 * T, 1.8)
    h = 380 * p
    out += f'<rect x="150" y="570" width="300" height="400" rx="24" fill="{WHT}" stroke="{BLK}" stroke-width="10"/>'
    out += f'<rect x="160" y="{960-h:.0f}" width="280" height="{h:.0f}" rx="16" fill="{GLD}"/>'
    out += f'<rect x="230" y="540" width="140" height="40" rx="10" fill="{BLK}"/>'
    for k in range(3):
        ph = (t * 0.9 + k * 0.33) % 1.0
        if p < 1:
            out += grp(0, 0, 1, coin(220 + k * 80, 600 + 200 * ph, 24), op=1 - ph)
    out += txt(720, 760, f"{int(round(1800 * p)):,}万円", 96, PNK if p >= 1 else BLK)
    return out + grp(720, 880, pop(t, 0.15 * T + 1.8), pill(720, 880, "買った金額で数える", 40, 440))


def d4(t, T):
    out = head(t, "ただし 損をしても", 84, "ほかの利益と相殺できない", 74)
    x = 250 + 150 * abs(math.sin(t * 2.6))
    out += f'<line x1="560" y1="570" x2="560" y2="800" stroke="{BLK}" stroke-width="14" stroke-linecap="round"/>'
    out += pill(x, 690, "NISAの損", 46, 300, PNK)
    out += grp(790, 690, pop(t, 0.3), pill(790, 690, "ほかの利益", 46, 320, GLD, BLK))
    return out + grp(540, 900, pop(t, 0.4 * T) * (1 + 0.06 * math.sin(t * 9)), pill(540, 900, "相殺 ×", 70, 420))


def d5(t, T):
    out = head(t, "NISAは", 90, "税金のルール", 130)
    b = 10 * abs(math.sin(t * 5))
    out += grp(540, 640, pop(t, 0.2), card(170, 570 - b, 740, 140, txt(540, 664 - b, "もうけに税金がかからない", 54)))
    out += grp(540, 790, pop(t, 0.5), pill(540, 790, "18歳以上が利用できる", 40, 520))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["投資のもうけにかかる税金が、ニーサなら0円です。"], cap="NISAは非課税の制度", note="※NISA口座の上場株式等の配当・譲渡益", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), (0.5, "pop"), (2.4, "ding")]),
    dict(narr=["ふつうは、もうけの20パーセントが税金。", "所得税が15パーセント、住民税が5パーセントです。"], cap="所得税15%+住民税5%", note="※ほかに復興特別所得税がかかる", draw=d1,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.3", "swish"), ("f0.3+0.6", "chomp")]),
    dict(narr=["1年に買える上限は、つみたて投資枠が120万円、成長投資枠が240万円。"], cap="年間の投資上限額", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.1", "tick"), ("f0.5", "tick"), ("f0.5+0.7", "ding")]),
    dict(narr=["ずっと持てる上限は、買った金額で1800万円まで。"], cap="非課税保有限度額", note="※うち成長投資枠は1,200万円まで", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.15", "swish"), ("f0.15+1.8", "ding")]),
    dict(narr=["ただし、損をすることもあります。", "ニーサの損は、ほかの利益と相殺できません。"], cap="損は「ないもの」とされる", note="※損益通算・繰越控除はできない", draw=d4,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.4", "drop")]),
    dict(narr=["ニーサは、税金のルールです。", "フォローして学ぼう。"], cap="フォローして学ぼう", note="※買うかどうかは自分で決めること", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v026_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v026_nisa.mp4")
