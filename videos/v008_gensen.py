"""#008 源泉徴収票の見方 — 見るのは4か所だけ（支払金額／給与所得控除後の金額／所得控除の額の合計額／源泉徴収税額）。
Sources (fetched 2026-11-13): 国税庁 令和8年分 法定調書の作成と提出の手引 第2 給与所得の源泉徴収票 / No.7411 / No.1410 給与所得控除 / No.1400 給与所得"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

NAMES = ["支払金額", "控除後の金額", "所得控除合計", "源泉徴収税額"]
NUM = "①②③④"
EX = "※例：年収500万円の会社員"


def strip(t, hi):
    """Mini 源泉徴収票 across the top of the stage (y 540..700) with box `hi` lit."""
    out = card(110, 540, 860, 160)
    for k in range(4):
        x = 128 + k * 208
        on = k == hi
        pulse = 1 + (0.05 * math.sin(t * 8) if on else 0)
        box = (f'<rect x="{x}" y="558" width="196" height="124" rx="12" fill="{PNK if on else "#EEE"}" stroke="{BLK}" stroke-width="5"/>'
               + txt(x + 98, 610, NUM[k], 44, WHT if on else "#999") + txt(x + 98, 660, NAMES[k], 28, WHT if on else "#999"))
        out += grp(x + 98, 620, pulse, box)
    return grp(540, 620, pop(t, 0.15), out)


def d0(t, T):
    out = head(t, "源泉徴収票", 90, "見るのは4か所だけ", 96)
    paper = card(150, 540, 780, 450, f'<rect x="150" y="540" width="780" height="70" rx="20" fill="{BLK}"/>' + txt(540, 592, "給与所得の源泉徴収票", 40, WHT))
    for r in range(4):
        paper += f'<line x1="190" y1="{800+r*45}" x2="{890 - (r % 2) * 180}" y2="{800+r*45}" stroke="#CCC" stroke-width="12" stroke-linecap="round"/>'
    out += paper
    for k in range(4):
        x = 172 + k * 187
        box = f'<rect x="{x}" y="640" width="175" height="120" rx="12" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>' + txt(x + 87, 722, NUM[k], 70, WHT)
        out += grp(x + 87, 700, pop(t, 0.3 * T + k * 0.3) * (1 + 0.04 * math.sin(t * 8 + k)), box)
    return out


def d1(t, T):
    out = head(t, "① 支払金額", 84, "引かれる前の年収", 104) + strip(t, 0)
    p = prog(t, 0.3 * T, 0.8)
    out += hbar(130, 760, 820 * p, GLD, 90)
    out += grp(540, 805, pop(t, 0.3 * T + 0.7), txt(540, 826, "500万円", 64))
    return out + grp(540, 930, pop(t, 0.6 * T), pill(540, 930, "手取りではない", 52, 480, BLK, YEL))


def d2(t, T):
    out = head(t, "② 給与所得控除後", 84, "会社員の控除を引いた後", 78) + strip(t, 1)
    w, cut = 820, 820 * 144 / 500
    p = prog(t, 0.45 * T, 0.7)
    out += hbar(130, 760, w - cut, GLD, 90)
    out += f'<g opacity="{1-0.6*p:.2f}">' + hbar(130 + w - cut, 760 - 25 * p, cut, BLK, 90) + txt(130 + w - cut / 2, 822 - 25 * p, "控除144万", 38, WHT) + '</g>'
    out += grp(130 + (w - cut) / 2, 805, pop(t, 0.45 * T + 0.5), txt(130 + (w - cut) / 2, 826, "356万円", 64))
    return out + grp(540, 930, pop(t, 0.45 * T + 0.8), pill(540, 930, "500万 − 144万 ＝ 356万", 46, 660, PNK))


def d3(t, T):
    out = head(t, "③ 所得控除の合計", 84, "保険や家族の分を引く", 88) + strip(t, 2)
    items = [("社会保険料", GRN, 250, 790), ("生命保険料", BLU, 560, 790), ("配偶者・扶養", RED, 850, 790), ("基礎控除", BLK, 400, 920), ("など", PNK, 700, 920)]
    for k, (lab, col, cx, cy) in enumerate(items):
        t0 = 0.2 * T + k * 0.12 * T
        dy = -160 * (1 - prog(t, t0, 0.35))
        out += grp(cx, cy + dy, pop(t, t0), pill(cx, cy + dy, lab, 42, 290 if len(lab) > 2 else 170, col))
    return out


def d4(t, T):
    out = head(t, "④ 源泉徴収税額", 84, "1年分の所得税はコレ", 90) + strip(t, 3)
    out += monster(280, 860, RED, t, 0.6 * pop(t, 0.25))
    for k in range(4):
        t0 = 0.3 * T + k * 0.35
        p = prog(t, t0, 0.5)
        if 0 < p < 1:
            out += coin(900 - 560 * p, 800 + 60 * math.sin(p * math.pi) * -1 + 60, 36)
    return out + grp(700, 860, pop(t, 0.35 * T), txt(700, 840, "年末調整の", 52) + txt(700, 920, "後の金額", 72, PNK))


def d5(t, T):
    out = head(t, "もらえるのは", 80, "翌年1月末まで", 110)
    paper = card(390, 560, 300, 250, f'<rect x="390" y="560" width="300" height="56" rx="20" fill="{BLK}"/>' + txt(540, 600, "源泉徴収票", 34, WHT)
                 + "".join(f'<rect x="{410+k*68}" y="640" width="58" height="56" rx="8" fill="{PNK}"/>' for k in range(4))
                 + f'<line x1="420" y1="735" x2="660" y2="735" stroke="#CCC" stroke-width="10" stroke-linecap="round"/><line x1="420" y1="770" x2="580" y2="770" stroke="#CCC" stroke-width="10" stroke-linecap="round"/>')
    out += grp(540, 685, pop(t, 0.2), paper, rot=4 * math.sin(t * 3))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["会社からもらう、源泉徴収票。", "見るのは、この4か所だけ。"], cap="この4か所だけ見ればOK", csize=60, draw=d0,
         sfx=[(0.0, "whoosh")] + [(f"f0.3+{k*0.3:.1f}", "pop") for k in range(4)]),
    dict(narr=["ひとつめ、支払金額。", "税金を引かれる前の、1年の給料です。"], cap="手取りではなく年収", note=EX, draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.3", "swish"), ("f0.6", "pop")]),
    dict(narr=["ふたつめ。年収から給与所得控除を引いた金額。", "500万円なら、356万円。"], cap="500万→356万円",
         note="※令和8年分：500万×20%+44万＝144万円", draw=d2, sfx=[(0.0, "whoosh"), ("f0.45", "swish"), ("f0.45+0.8", "ding")]),
    dict(narr=["みっつめ。保険料や扶養、基礎控除などの合計。", "大きいほど、税金は小さくなります。"], cap="引ける金額の合計", draw=d3,
         sfx=[(0.0, "whoosh")] + [(f"f{0.2+k*0.12:.2f}", "pop") for k in range(5)]),
    dict(narr=["よっつめ、源泉徴収税額。", "年末調整後の、1年分の所得税です。"], cap="1年分の所得税", note="※復興特別所得税をふくむ合計", draw=d4,
         sfx=[(0.0, "whoosh"), (0.25, "pop"), ("f0.3+0.5", "chomp"), ("f0.3+1.2", "chomp")]),
    dict(narr=["翌年1月末までにもらえます。", "なくさず、取っておこう。"], cap="なくさず取っておこう",
         note="※令和8年分は令和9年2月1日まで", draw=d5, sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v008_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v008_gensen.mp4")
