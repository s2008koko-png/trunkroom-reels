"""#005 ボーナスから引かれる4つ — 50万円の手取りは約41万円
(sources: 日本年金機構 厚生年金保険の保険料 / 協会けんぽ 令和8年度保険料率（東京）・子ども・子育て支援金率 /
厚生労働省 令和8年度雇用保険料率 / 国税庁 No.2523・賞与に対する源泉徴収税額の算出率の表（令和8年分）).

Estimate behind the numbers (bonus 500,000円, 協会けんぽ東京, under 40, no dependants, monthly pay 300,000円):
  厚生年金 18.3%/2 = 9.15%            -> 45,750
  健康保険 9.85%/2 + 支援金 0.23%/2   -> 24,625 + 575 = 25,200
  雇用保険 5/1000                     -> 2,500
  所得税 前月の社保控除後 約25.6万円 → 率4.084% × (500,000 − 73,450) -> 約17,400
  合計 約90,900 → 手取り 約409,000
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

NOTE = "※東京・40歳未満・月給30万円の目安"
PUR = "#8E5BFF"


def bag(cx, cy):
    """Bonus envelope (賞与袋)."""
    x, y = cx - 170, cy - 130
    return (f'<rect x="{x}" y="{y}" width="340" height="260" rx="16" fill="#F7E7C6" stroke="{BLK}" stroke-width="8"/>'
            f'<polygon points="{x},{y} {cx},{y+90} {x+340},{y}" fill="#EBD3A0" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
            + pill(cx, cy + 60, "賞与", 60, 220, PNK))


def jar(cx, cy, fill):
    """Pension jar that fills up (fill 0..1)."""
    x, y, w, h = cx - 120, cy - 130, 240, 270
    fh = (h - 16) * fill
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="{x+8}" y="{y+h-8-fh:.1f}" width="{w-16}" height="{fh:.1f}" rx="24" fill="{GLD}"/>'
            f'<rect x="{x+30}" y="{y-34}" width="{w-60}" height="38" rx="10" fill="{BLK}"/>'
            + txt(cx, cy + 30, "年金", 64))


def d0(t, T):
    out = head(t, "ボーナス50万円", 96, "約9万円が消える", 110)
    t0 = 0.42 * T
    p = prog(t, t0, 1.0)
    out += grp(300, 720, pop(t, 0.2), bag(300, 720), rot=3 * math.sin(t * 4))
    for k in range(4):
        q = prog(t, t0 + k * 0.15, 0.8)
        if 0 < q < 1:
            x, y = 300 + 80 * q + k * 20, 640 - 150 * math.sin(math.pi * q) - 60 * q
            out += grp(x, y, 1, coin(x, y, 36), op=1 - q * q)
    val = 50 - 9 * p
    out += grp(720, 700, pop(t, 0.35), txt(720, 720, f"{val:.0f}万円", 130, PNK if p >= 1 else BLK))
    out += grp(720, 850, pop(t, t0 + 1.0), pill(720, 850, "手取り 約41万円", 46, 440))
    return out


def d1(t, T):
    out = head(t, "引かれるのは", 84, "この4つ", 130)
    items = [("厚生年金", GRN), ("健康保険", BLU), ("雇用保険", PUR), ("所得税", RED)]
    for k, (lab, col) in enumerate(items):
        x, y = 110 + (k % 2) * 450, 560 + (k // 2) * 220
        t0 = 0.15 * T + k * 0.16 * T
        inner = (f'<circle cx="{x+85}" cy="{y+95}" r="52" fill="{col}" stroke="{BLK}" stroke-width="7"/>' + txt(x + 85, y + 118, str(k + 1), 64, WHT)
                 + txt(x + 270, y + 118, lab, 58))
        out += grp(x + 205, y + 95, pop(t, t0), card(x, y, 410, 190, inner), rot=2 * math.sin(t * 4 + k))
    return out


def d2(t, T):
    out = head(t, "いちばん大きいのは", 80, "厚生年金", 130, tb=0.15 * T)
    rows = [("厚生年金", 45750, GRN, "約4.6万円", 0.08 * T), ("健康保険", 25200, BLU, "約2.5万円", 0.52 * T), ("雇用保険", 2500, PUR, "2,500円", 0.76 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 555 + k * 145
        w = v / 45750 * 520
        out += grp(250, y + 20, pop(t, t0, 0.3), txt(130, y + 36, lab, 46, BLK, "start"))
        out += hbar(130, y + 52, w * prog(t, t0 + 0.15, 0.6), col)
        out += grp(130 + w + 110, y + 84, pop(t, t0 + 0.6, 0.3), txt(130 + w + 22, y + 102, val, 52, BLK, "start"))
    return out


def d3(t, T):
    out = head(t, "所得税の率は", 84, "前の月の給料で決まる", 88)
    rates = ["0%", "2%", "4%", "6%", "8%", "10%"]
    tm = 0.3 * T
    pos = 2 * prog(t, tm, 1.0)  # marker walks to the 3rd step (約4%)
    for k, r in enumerate(rates):
        x, h = 120 + k * 142, 60 + k * 44
        on = t > tm + 0.9 and k == 2
        out += grp(x + 64, 930 - h / 2, pop(t, 0.2 + k * 0.07, 0.25),
                   f'<rect x="{x}" y="{930-h}" width="128" height="{h}" rx="10" fill="{RED if on else WHT}" stroke="{BLK}" stroke-width="7"/>'
                   + txt(x + 64, 915, r, 40, WHT if on else BLK))
    k0, fr = int(pos), pos - int(pos)
    mx = 184 + pos * 142
    my = 930 - (60 + pos * 44) - 50 - 60 * abs(math.sin(math.pi * fr))
    out += grp(mx, my, pop(t, 0.5), coin(mx, my, 44))
    out += grp(770, 610, pop(t, 0.25), pill(770, 610, "率（約）", 44, 260))
    out += grp(300, 610, pop(t, tm + 1.0), pill(300, 610, "約1.7万円", 54, 360, RED))
    return out


def d4(t, T):
    out = head(t, "ただし厚生年金は", 80, "将来の年金に入る", 104)
    fill = 0.15 + 0.6 * prog(t, 0.3 * T, 1.2)
    out += grp(540, 760, pop(t, 0.2), jar(540, 760, fill))
    for k, (sx, lab, t0) in enumerate(((-1, "あなた", 0.25 * T), (1, "会社", 0.6 * T))):
        cx = 540 + sx * 330
        out += grp(cx, 900, pop(t, t0 - 0.2 if t0 > 0.3 else 0.3), pill(cx, 900, lab, 46, 230, BLK if sx < 0 else GRN))
        for j in range(2):
            q = prog(t, t0 + j * 0.25, 0.7)
            if 0 < q < 1:
                x, y = cx - sx * 330 * q, 760 - 240 * math.sin(math.pi * q) * 0.9 - 130 * q
                out += coin(x, y, 36)
        if t <= t0:
            out += grp(cx, 760, pop(t, 0.35 + k * 0.1), coin(cx, 760, 44))
    out += grp(870, 600, pop(t, 0.6 * T + 0.5), pill(870, 600, "同じ額", 44, 200, PNK))
    return out


def d5(t, T):
    out = head(t, "ボーナスの予定は", 84, "手取りで立てよう", 104)
    out += grp(300, 700, pop(t, 0.3), bag(300, 700).replace("賞与", "手取り"), rot=3 * math.sin(t * 4))
    out += monster(780, 690 - 20 * abs(math.sin(t * 6)), GRN, t, 0.66 * pop(t, 0.45))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["ボーナス50万円。", "約9万円は、最初から引かれます。"], cap="50万円→手取り約41万円", csize=58, note=NOTE, draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.42", "drop"), ("f0.42+1.0", "ding")]),
    dict(narr=["引かれるのは、厚生年金、健康保険、雇用保険、所得税の4つ。"], cap="ボーナスから引かれる4つ", csize=58, draw=d1,
         sfx=[(0.0, "whoosh")] + [(f"f{0.15+k*0.16:.2f}", "pop") for k in range(4)]),
    dict(narr=["最大は厚生年金、約4万6000円。", "健康保険は、約2万5000円。"], cap="ボーナス50万円の目安", note=NOTE, draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.08", "tick"), ("f0.52", "tick"), ("f0.76", "tick")]),
    dict(narr=["所得税の率は、前の月の給料で決まります。", "この例だと、約1万7000円。"], cap="所得税は約1.7万円", note=NOTE, draw=d3,
         sfx=[(0.0, "whoosh"), (0.5, "pop"), ("f0.3", "swish"), ("f0.3+1.0", "ding")]),
    dict(narr=["ただし厚生年金は、将来の年金の計算に入ります。", "会社も、同じ額を負担。"], cap="会社も同じ額を負担", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.25", "swish"), ("f0.6", "swish"), ("f0.6+0.5", "ding")]),
    dict(narr=["ボーナスの予定は、手取りで立てよう。", "フォローして、お金の仕組みを学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v005_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v005_bonus.mp4")
