"""#032 還付申告 — 納めすぎた所得税は、その年の翌年1月1日から5年間、申告で取り戻せる（令和3年分は令和8年12月31日まで）。
Sources (fetched 2026-11-21): 国税庁 No.2030 還付申告（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

YEARS = ["令和3年", "令和4年", "令和5年", "令和6年", "令和7年"]


def cal(cx, cy, label, col=PNK, sub="分"):
    """Small calendar page ~150x170 centred on (cx, cy)."""
    return (f'<rect x="{cx-75}" y="{cy-85}" width="150" height="170" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
            f'<path d="M{cx-75} {cy-45} L{cx-75} {cy-71} Q{cx-75} {cy-85} {cx-61} {cy-85} L{cx+61} {cy-85} Q{cx+75} {cy-85} {cx+75} {cy-71} L{cx+75} {cy-45} Z" fill="{col}" stroke="{BLK}" stroke-width="7"/>'
            f'<circle cx="{cx-36}" cy="{cy-86}" r="9" fill="{BLK}"/><circle cx="{cx+36}" cy="{cy-86}" r="9" fill="{BLK}"/>'
            + txt(cx, cy + 14, label, 34) + txt(cx, cy + 62, sub, 34))


def d0(t, T):
    out = head(t, "払いすぎた税金は", 84, "5年前まで取り戻せる", 90)
    for k in range(5):
        cx = 170 + k * 185
        out += grp(cx, 660, pop(t, 0.2 + k * 0.12), cal(cx, 660, YEARS[k]))
        # a coin comes back from each year
        p = prog(t, 0.4 * T + k * 0.18, 0.6)
        if p > 0:
            out += coin(cx, 780 + 130 * p, 44)
    return out


def d1(t, T):
    out = head(t, "申告の義務がない", 80, "会社員でもできる", 104)
    out += monster(760, 740, RED, t, 0.8 * pop(t, 0.2))
    out += grp(250, 800, pop(t, 0.3), icon("wallet", 150, 720) + txt(215, 930, "あなた", 44))
    for k in range(4):
        p = clamp((t - 0.35 * T - k * 0.3) / 0.8)
        if 0 < p:
            q = 1 - (1 - p) ** 3
            x = 640 - 330 * q
            y = 780 - 110 * math.sin(math.pi * q)
            out += coin(x, y, 40) if p < 1 else ""
    out += grp(480, 600, pop(t, 0.35 * T), pill(480, 600, "納めすぎた分", 42, 330, PNK))
    return out


def d2(t, T):
    out = head(t, "たとえば", 80, "こんな年", 130)
    heart = lambda x, y: f'<path d="M{x+65} {y+125} C{x-30} {y+60} {x+20} {y-10} {x+65} {y+40} C{x+110} {y-10} {x+160} {y+60} {x+65} {y+125} Z" fill="{PNK}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
    door = lambda x, y: (f'<rect x="{x+20}" y="{y+5}" width="90" height="135" fill="{BLU}" stroke="{BLK}" stroke-width="7"/><circle cx="{x+92}" cy="{y+76}" r="8" fill="{GLD}" stroke="{BLK}" stroke-width="4"/>')
    rows = [(icon("hospital", 130, 548), "医療費が多かった", 0.08 * T), (heart(130, 700), "寄付をした", 0.3 * T), (door(130, 852), "途中で退職した", 0.55 * T)]
    for k, (ic, lab, t0) in enumerate(rows):
        y = 540 + k * 152
        out += grp(540, y + 70, pop(t, t0), card(100, y, 880, 140) + grp(195, y + 70, 0.72, ic) + txt(300, y + 92, lab, 62, BLK, "start"))
    return out


def d3(t, T):
    out = head(t, "期限は 翌年1月1日から", 76, "5年間", 140)
    for k in range(5):
        cx = 170 + k * 185
        gone = k == 0 and t > 0.5 * T
        blink = gone and int(t * 5) % 2 == 0
        out += grp(cx, 660, pop(t, 0.2 + k * 0.1), cal(cx, 660, YEARS[k], PNK if (k == 0 and blink) else (GLD if k == 0 else BLU)))
    out += grp(170, 800, pop(t, 0.5 * T), f'<polygon points="170,770 130,830 210,830" fill="{PNK}" stroke="{BLK}" stroke-width="6" stroke-linejoin="round"/>')
    out += grp(540, 910, pop(t, 0.5 * T + 0.2), card(110, 840, 860, 140, txt(540, 934, "令和3年分は 12月31日まで", 60, PNK)))
    return out


def d4(t, T):
    out = head(t, "ただし 必ずもどる", 80, "わけじゃない", 120)
    sl = f'<rect x="130" y="560" width="560" height="410" rx="16" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>' + txt(410, 625, "源泉徴収票", 46)
    for r in range(3):
        sl += f'<rect x="160" y="{660+r*56}" width="{500 - r*90}" height="26" rx="8" fill="#CCC"/>'
    out += grp(410, 760, pop(t, 0.2), sl)
    out += grp(410, 890, pop(t, 0.4 * T), f'<rect x="160" y="835" width="500" height="110" rx="12" fill="{YEL}" stroke="{PNK}" stroke-width="8"/>'
               + txt(180, 905, "源泉徴収税額", 38, BLK, "start") + txt(640, 912, "0円", 64, PNK, "end"))
    k = pop(t, 0.4 * T + 0.5)
    out += grp(840, 740, k, coin(840, 740, 80) + f'<line x1="760" y1="660" x2="920" y2="820" stroke="{PNK}" stroke-width="22" stroke-linecap="round"/>'
               f'<line x1="920" y1="660" x2="760" y2="820" stroke="{PNK}" stroke-width="22" stroke-linecap="round"/>')
    out += grp(840, 890, pop(t, 0.4 * T + 0.7), pill(840, 890, "もどらない", 40, 260))
    return out


def d5(t, T):
    out = head(t, "昔の源泉徴収票を", 84, "見直そう", 130)
    for k in range(3):
        cx = 300 + k * 240
        out += grp(cx, 690, pop(t, 0.2 + k * 0.15), f'<rect x="{cx-85}" y="{590 - 14*abs(math.sin(t*5+k)):.1f}" width="170" height="210" rx="12" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
                   + "".join(f'<rect x="{cx-60}" y="{630 + r*42 - 14*abs(math.sin(t*5+k)):.1f}" width="{120 - r*22}" height="18" rx="6" fill="{PNK if r == 3 else "#BBB"}"/>' for r in range(4)))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["払いすぎた所得税は、5年さかのぼって取り戻せます。"], cap="還付申告は5年間できる", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.4", "tick"), ("f0.4+0.4", "tick"), ("f0.4+0.8", "ding")]),
    dict(narr=["これを還付申告といいます。", "確定申告の義務がない会社員でも、できます。"], cap="納めすぎた分がもどる", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.35", "swish"), ("f0.35+0.9", "ding")]),
    dict(narr=["たとえば、医療費が多かった年、寄付をした年。", "途中で退職して、年末調整を受けていない年。"], cap="こんな年は確認しよう", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.08", "pop"), ("f0.3", "pop"), ("f0.55", "pop")]),
    dict(narr=["期限は、翌年1月1日から5年間。", "令和3年分は、今年の12月31日まで。"], cap="令和3年分は年内まで", note="※令和8年11月時点", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "tick"), (0.4, "tick"), ("f0.5", "ding")]),
    dict(narr=["ただし、源泉徴収税額が0円なら、戻る税金はありません。"], cap="税額0円ならもどらない", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.4", "tick"), ("f0.4+0.5", "drop")]),
    dict(narr=["昔の源泉徴収票を見直そう。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v032_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v032_kanpu.mp4")
