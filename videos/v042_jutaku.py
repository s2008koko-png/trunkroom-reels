"""#042 住宅ローン控除（住宅借入金等特別控除） — 年末のローン残高等×0.7%を所得税の額から引く（税額控除）・
計算例 残高2,000万円→14万円・省エネ基準適合住宅などは令和4〜9年入居で控除期間13年・要件：返済10年以上／床面積 原則50㎡以上／
合計所得2,000万円以下・令和6年以降入居の「その他の住宅」（省エネ基準に合わない新築）は原則対象外・
1年目は確定申告、2年目以降は年末調整（控除証明書兼申告書と年末残高等証明書を勤務先へ）。
Sources (fetched 2026-11-25): 国税庁 No.1211-1 住宅の新築等をし、令和4年以降に居住の用に供した場合（住宅借入金等特別控除）
（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def house(cx, cy, s=1.0, col=BLU):
    """Original big house, ~280x260, centred on (cx, cy)."""
    h = (f'<rect x="{cx-105}" y="{cy-20}" width="210" height="150" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<polygon points="{cx-140},{cy-14} {cx},{cy-130} {cx+140},{cy-14}" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<rect x="{cx+50}" y="{cy-120}" width="34" height="60" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{cx-75}" y="{cy+40}" width="56" height="90" fill="{BLK}"/>'
         f'<rect x="{cx+15}" y="{cy+20}" width="64" height="56" fill="{YEL}" stroke="{BLK}" stroke-width="7"/>'
         f'<line x1="{cx+47}" y1="{cy+20}" x2="{cx+47}" y2="{cy+76}" stroke="{BLK}" stroke-width="5"/>')
    return grp(cx, cy, s, h)


def check(cx, cy, r=38):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GRN}" stroke="{BLK}" stroke-width="7"/>'
            f'<path d="M{cx-r*0.45} {cy} L{cx-r*0.1} {cy+r*0.35} L{cx+r*0.5} {cy-r*0.35}" fill="none" stroke="{WHT}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')


def d0(t, T):
    out = head(t, "住宅ローンの年末残高", 80, "0.7%を税金から引ける", 84)
    out += house(235, 790 - 12 * abs(math.sin(t * 4)), 0.9)
    out += pill(700, 610, "年末残高 ×", 50, 380)
    out += grp(700, 780, 1 + 0.05 * math.sin(t * 6), txt(700, 845, "0.7%", 190, PNK))
    for k in range(3):  # coins drifting from the number toward the house
        ph = (t * 0.6 + k / 3) % 1
        out += grp(0, 0, 1, coin(560 - 170 * ph, 955 - 60 * math.sin(ph * math.pi), 30), op=1 - ph)
    return out


def d1(t, T):
    out = head(t, "残高2,000万円なら", 84, "14万円 引ける", 120)
    out += grp(540, 585, pop(t, 0.15), txt(540, 603, "年末のローン残高 2,000万円", 54))
    w = 840 * prog(t, 0.25, 0.8)
    out += hbar(120, 635, w, GLD, 100)
    t0 = 0.4 * T
    if t > t0:
        out += f'<rect x="930" y="635" width="30" height="100" rx="6" fill="{PNK}" stroke="{BLK}" stroke-width="6" opacity="{0.6+0.4*math.sin(t*9):.2f}"/>'
    out += grp(300, 840, pop(t, t0), txt(300, 868, "×0.7%＝", 80))
    out += grp(730, 840, pop(t, t0 + 0.35), txt(730, 885, "14万円", 136, PNK))
    out += grp(540, 955, pop(t, 0.7 * T), pill(540, 955, "税金そのものから引く", 46, 600))
    return out


def d2(t, T):
    out = head(t, "省エネ基準の新築など", 80, "最長13年つづく", 110)
    n = 0
    for k in range(13):
        tk = 0.3 + k * (0.6 * T - 0.3) / 13
        x = 111 + k * 66
        on = t >= tk
        n += on
        out += f'<rect x="{x}" y="620" width="58" height="80" rx="8" fill="{GLD if on else WHT}" stroke="{BLK}" stroke-width="6"/>'
        out += grp(x + 29, 660, pop(t, tk, 0.25), txt(x + 29, 674, str(k + 1), 34))
    out += txt(111, 750, "1年目", 36, BLK, "start") + txt(969, 750, "13年目", 36, BLK, "end")
    out += house(250, 890, 0.6 * pop(t, 0.2), GRN)
    out += txt(650, 950, f"{max(n, 1)}年", 180, PNK if n == 13 else BLK)
    return out


def d3(t, T):
    out = head(t, "ただし", 90, "条件がある", 130)
    for k, lab in enumerate(("返済は10年以上", "広さ 原則50㎡以上", "所得2,000万円以下")):
        y = 535 + k * 120
        t0 = 0.15 * T + k * 0.13 * T
        out += grp(540, y + 52, pop(t, t0), card(150, y, 780, 104, txt(590, y + 74, lab, 60)))
        out += grp(240, y + 52, pop(t, t0 + 0.25), check(240, y + 52))
    wob = 4 * math.sin(t * 8) if t > 0.6 * T else 0
    out += grp(540, 948, pop(t, 0.6 * T), pill(540, 948, "省エネ基準なしの新築は 原則×", 46, 800, PNK), rot=wob * 0.3)
    return out


def d4(t, T):
    out = head(t, "1年目は確定申告", 90, "2年目から年末調整", 96)
    sel = 0 if t < 0.5 * T else 1
    for k, (x, l1, l2) in enumerate(((100, "1年目", "確定申告"), (580, "2年目から", "年末調整"))):
        ring = f'<rect x="{x-14}" y="566" width="428" height="268" rx="30" fill="none" stroke="{PNK}" stroke-width="16" opacity="{0.6+0.4*math.sin(t*8):.2f}"/>' if sel == k else ""
        out += grp(x + 200, 700, pop(t, 0.2 + k * 0.4 * T), ring + card(x, 580, 400, 240, txt(x + 200, 670, l1, 54) + txt(x + 200, 770, l2, 84, PNK)))
    out += grp(540, 700, pop(t, 0.35 * T), txt(540, 722, "→", 64))
    out += grp(540, 930, pop(t, 0.65 * T), pill(540, 930, "会社に書類を出す", 52, 560))
    return out


def d5(t, T):
    out = head(t, "年末調整の書類", 90, "出し忘れに注意", 116)
    out += house(300, 700 - 16 * abs(math.sin(t * 5)), 0.75 * pop(t, 0.2))
    out += grp(560, 700, pop(t, 0.35), coin(560, 700 - 14 * abs(math.sin(t * 5 + 1)), 62))
    out += house(800, 700 - 16 * abs(math.sin(t * 5 + 2)), 0.75 * pop(t, 0.5), GRN)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["住宅ローンがある人は、年末の残高の0.7パーセントを、所得税から引けます。"], cap="住宅ローン控除", draw=d0,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.6", "ding")]),
    dict(narr=["残高が2000万円なら、14万円。", "所得ではなく、税金そのものから引きます。"], cap="2,000万円×0.7%", note="※上限は住宅の種類と入居年で変わる", draw=d1,
         sfx=[(0.0, "whoosh"), (0.25, "swish"), ("f0.4", "pop"), ("f0.4+0.35", "ding"), ("f0.7", "pop")]),
    dict(narr=["省エネ基準に合う新築などは、最長13年つづきます。"], cap="最長13年", note="※令和4〜9年に入居した場合", draw=d2,
         sfx=[(0.0, "whoosh")] + [(f"f{0.6*k/13:.3f}+0.3", "tick") for k in range(0, 13, 2)] + [("f0.6+0.3", "ding")]),
    dict(narr=["ただし、返済10年以上などの条件あり。", "省エネ基準に合わない新築は、原則、対象外です。"], cap="条件をチェック", note="※令和6年以降に入居する新築の場合", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.15", "pop"), ("f0.28", "pop"), ("f0.41", "pop"), ("f0.6", "drop")]),
    dict(narr=["1年目は確定申告。", "2年目からは、年末調整でできます。"], cap="2年目からは会社で", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.4+0.2", "pop"), ("f0.5", "tick"), ("f0.65", "ding")]),
    dict(narr=["年末調整の書類、出し忘れに注意。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v042_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v042_jutaku.mp4")
