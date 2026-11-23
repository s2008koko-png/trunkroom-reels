"""#037 預貯金の利子の税金 — 利子は受け取るときに20.315%（所得税等15.315%＋住民税5%）が源泉徴収される・
源泉分離課税で納税が完結し確定申告はしない・計算例 利子1,000円→税金203円（153円＋50円）→797円・
障害者等の少額貯蓄非課税制度（マル優）は元本350万円までの利子が非課税。
Sources (fetched 2026-11-23): 国税庁 No.1310 利息を受け取ったとき（利子所得）（令和8年4月1日現在法令等） / 暮らしの税情報 株式・配当・利子と税"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def bank(cx, cy, label="銀行", s=1.0, col="#EDEDED"):
    """Original bank building: roof triangle + 4 columns, ~260 wide, centred on (cx, cy)."""
    b = f'<polygon points="{cx-140},{cy-70} {cx},{cy-160} {cx+140},{cy-70}" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
    b += f'<rect x="{cx-130}" y="{cy-70}" width="260" height="34" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
    for k in range(4):
        b += f'<rect x="{cx-112+k*66}" y="{cy-36}" width="34" height="130" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
    b += f'<rect x="{cx-145}" y="{cy+94}" width="290" height="34" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
    b += txt(cx, cy - 84, label, 40)
    return grp(cx, cy, s, b)


def passbook(cx, cy, w=230, h=280):
    x, y = cx - w / 2, cy - h / 2
    p = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{GRN}" stroke="{BLK}" stroke-width="8"/>'
    p += f'<rect x="{x+28}" y="{y+46}" width="{w-56}" height="80" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="5"/>' + txt(cx, y + 104, "通帳", 48)
    p += f'<rect x="{x+20}" y="{y+h-80}" width="{w-40}" height="26" fill="{BLK}"/>'
    return p


def check(cx, cy, r=70):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GRN}" stroke="{BLK}" stroke-width="8"/>'
            f'<path d="M{cx-r*0.45} {cy} L{cx-r*0.1} {cy+r*0.35} L{cx+r*0.5} {cy-r*0.35}" fill="none" stroke="{WHT}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>')


def d0(t, T):
    out = head(t, "銀行の利子は もらう前に", 76, "約2割 引かれてる", 100)
    out += bank(230, 760, s=pop(t, 0.1))
    t0 = 0.5 * T
    p = prog(t, t0, 0.8)
    for k in range(5):
        x = 440 + k * 118
        if k == 4:
            out += grp(x, 760, pop(t, 0.3 + k * 0.12), coin(x, 760 - 170 * p, 50, PNK, WHT), op=1.0)
        else:
            out += grp(x, 760, pop(t, 0.3 + k * 0.12), coin(x, 760 - 8 * abs(math.sin(t * 5 + k)), 50))
    out += grp(912, 590, pop(t, t0 + 0.5), txt(790, 606, "税金", 46, PNK))
    out += grp(700, 930, pop(t, t0 + 0.7), pill(700, 930, "利子の約2割が税金", 44, 480))
    return out


def d1(t, T):
    out = head(t, "利子の税率は", 90, "20.315%", 150)
    x0, y0, h = 120, 700, 130
    wa, wb = 600, 196  # 15.315 : 5
    pa, pb = prog(t, 0.3 * T, 0.7), prog(t, 0.6 * T, 0.5)
    if pa > 0:
        out += f'<rect x="{x0}" y="{y0}" width="{wa*pa:.1f}" height="{h}" fill="{RED}" stroke="{BLK}" stroke-width="8"/>'
    if pb > 0:
        out += f'<rect x="{x0+wa}" y="{y0}" width="{wb*pb:.1f}" height="{h}" fill="{BLU}" stroke="{BLK}" stroke-width="8"/>'
    out += grp(x0 + wa / 2, 640, pop(t, 0.3 * T + 0.3), txt(x0 + wa / 2, 660, "国へ 15.315%", 56))
    out += grp(x0 + wa + wb / 2, 900, pop(t, 0.6 * T + 0.3), txt(x0 + wa + wb / 2, 900, "地方へ 5%", 50))
    out += grp(x0 + wa / 2, 900, pop(t, 0.6 * T + 0.6), pill(x0 + wa / 2, 950, "合わせて 20.315%", 46, 480, PNK))
    return out


def d2(t, T):
    out = head(t, "利子が1,000円なら", 86, "手元に797円", 124)
    t0 = 0.4 * T
    p = prog(t, t0, 1.0)
    val = int(round(1000 - 203 * p))
    out += grp(380, 720, pop(t, 0.15), card(120, 590, 520, 260, txt(380, 770, f"{val:,}円", 120, PNK if p >= 1 else BLK)))
    out += monster(830, 730, RED, t, 0.75 * pop(t, 0.3), chomp=p > 0)
    if 0 < p < 1:
        out += coin(640 + 130 * p, 720 - 60 * math.sin(math.pi * p), 36)
    out += grp(380, 940, pop(t, t0 + 1.0), pill(380, 940, "税金 203円", 50, 360, PNK))
    return out


def d3(t, T):
    out = head(t, "銀行が先に納めるから", 84, "確定申告はしない", 110)
    out += bank(220, 760, s=pop(t, 0.1))
    out += bank(860, 760, "国・地方", s=pop(t, 0.2), col="#DDE6F5")
    p = prog(t, 0.3 * T, 0.9)
    if 0 < p < 1:
        out += coin(380 + 320 * p, 740 - 120 * math.sin(math.pi * p), 44, PNK, WHT)
    out += grp(540, 720, pop(t, 0.3 * T + 0.9), check(540, 720))
    out += grp(540, 950, pop(t, 0.3 * T + 1.2), pill(540, 950, "これで納税は終わり", 44, 500))
    return out


def d4(t, T):
    out = head(t, "障害のある人などは", 86, "非課税の制度あり", 110)
    for k in range(6):
        out += grp(260 + (k % 3) * 100, 800 - (k // 3) * 60, pop(t, 0.2 + k * 0.08), coin(260 + (k % 3) * 100, 800 - (k // 3) * 60, 46))
    s = pop(t, 0.4 * T)
    sh = (f'<path d="M700 580 L860 630 L860 760 Q860 870 700 930 Q540 870 540 760 L540 630 Z" fill="{GRN}" stroke="{BLK}" stroke-width="9" stroke-linejoin="round"/>'
          + txt(700, 740, "利子に", 50, WHT) + txt(700, 810, "税なし", 56, WHT))
    out += grp(700, 760, s, sh)
    out += grp(360, 950, pop(t, 0.4 * T + 0.5), pill(360, 950, "元本350万円まで", 46, 460, PNK))
    return out


def d5(t, T):
    out = head(t, "通帳の利子を", 90, "見てみよう", 130)
    out += grp(300, 700, pop(t, 0.2), passbook(300, 700 - 12 * abs(math.sin(t * 5)), 200, 240), rot=-5)
    out += grp(560, 700, pop(t, 0.35), coin(560, 700 - 12 * abs(math.sin(t * 5 + 1)), 60))
    out += bank(820, 720 - 10 * abs(math.sin(t * 5 + 2)), s=0.7 * pop(t, 0.5))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["銀行の利子は、受け取る前に、約2割が税金で引かれています。"], cap="利子にも税金がかかる", draw=d0,
         sfx=[(0.0, "whoosh"), (0.1, "pop"), ("f0.5", "drop"), ("f0.5+0.7", "ding")]),
    dict(narr=["税率は、20.315パーセント。", "国に15.315、地方に5パーセントです。"], cap="国15.315%＋地方5%", note="※所得税等15.315%・住民税5%", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.3", "tick"), ("f0.6", "tick"), ("f0.6+0.6", "pop")]),
    dict(narr=["利子が1000円なら、税金は203円。", "手元にのこるのは、797円です。"], cap="1,000円→797円", note="※預貯金の利子1,000円の計算例", draw=d2,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.4", "chomp"), ("f0.4+1.0", "ding")]),
    dict(narr=["銀行が先に引いて、納めてくれます。", "だから、確定申告はしません。"], cap="引かれて納税は完了", note="※預貯金の利子は源泉分離課税", draw=d3,
         sfx=[(0.0, "whoosh"), (0.1, "pop"), ("f0.3", "swish"), ("f0.3+0.9", "ding")]),
    dict(narr=["ただし、障害のある人などは、元本350万円まで、利子が非課税になる制度があります。"], cap="350万円まで非課税", note="※障害者等の少額貯蓄非課税制度", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.4", "pop"), ("f0.4+0.5", "ding")]),
    dict(narr=["通帳の利子を、見てみよう。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v037_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v037_rishi.mp4")
