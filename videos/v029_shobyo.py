"""#029 傷病手当金 — 業務外の病気やケガで働けず給与が出ないとき健康保険から支給・連続3日間の待期のあと4日目から・1日あたり 直近12か月の標準報酬月額の平均÷30×2/3・同一の傷病について通算1年6か月・給与が出るとその分減額・業務上や通勤中は労災保険。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

NOTE = "※健康保険の被保険者が対象"


def bed(x, y, t):
    """Original simple bed with a sleeping round person (x,y = top-left of a ~380x220 box). 'Z's float up."""
    out = f'<rect x="{x}" y="{y+120}" width="380" height="60" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="{x}" y="{y+50}" width="26" height="170" rx="8" fill="{BLK}"/><rect x="{x+354}" y="{y+150}" width="26" height="70" rx="8" fill="{BLK}"/>'
    out += f'<circle cx="{x+90}" cy="{y+92}" r="44" fill="#FFD9B0" stroke="{BLK}" stroke-width="7"/>'
    out += f'<path d="M{x+72} {y+92} q10 10 20 0" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/><path d="M{x+98} {y+92} q10 10 20 0" fill="none" stroke="{BLK}" stroke-width="5" stroke-linecap="round"/>'
    out += f'<rect x="{x+130}" y="{y+70}" width="230" height="{70+4*math.sin(t*3):.0f}" rx="24" fill="{BLU}" stroke="{BLK}" stroke-width="8"/>'
    for k in range(3):
        ph = (t * 0.5 + k / 3) % 1.0
        out += f'<text x="{x+150+60*ph:.0f}" y="{y+40-90*ph:.0f}" {F} font-size="{30+26*ph:.0f}" fill="{BLK}" opacity="{1-ph:.2f}">Z</text>'
    return out


def hcard(cx, cy):
    """Original health-insurance style card (no real design): white card, pink cross."""
    return (f'<rect x="{cx-170}" y="{cy-105}" width="340" height="210" rx="22" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="{cx-170}" y="{cy-105}" width="340" height="56" rx="22" fill="{GRN}" stroke="{BLK}" stroke-width="8"/>'
            + txt(cx, cy - 64, "健康保険", 38, WHT)
            + f'<rect x="{cx-22}" y="{cy-28}" width="44" height="116" fill="{PNK}"/><rect x="{cx-58}" y="{cy+8}" width="116" height="44" fill="{PNK}"/>')


def d0(t, T):
    out = head(t, "病気で会社を休んでも", 84, "給料の約3分の2が出る", 84)
    out += bed(110, 560, t)
    p = prog(t, 0.45 * T, 1.0)
    # three money blocks; the third fades away
    for k in range(3):
        x = 560 + k * 130
        op = 1 - 0.85 * p if k == 2 else 1
        out += grp(0, 0, 1, f'<rect x="{x}" y="590" width="116" height="170" rx="16" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>' + txt(x + 58, 700, "¥", 80), op=op)
    return out + grp(540, 900, pop(t, 0.45 * T + 0.9) * (1 + 0.04 * math.sin(t * 8)), pill(540, 900, "およそ 3分の2", 64, 560, PNK))


def d1(t, T):
    out = head(t, "名前は", 84, "傷病手当金", 140)
    out += grp(300, 720, pop(t, 0.2), hcard(300, 720 - 8 * abs(math.sin(t * 4))))
    for k in range(4):
        ph = (t * 0.6 + k / 4) % 1.0
        if t > 0.6:
            out += grp(0, 0, 1, coin(480 + 300 * ph, 720 - 110 * math.sin(math.pi * ph), 30), op=min(1, 4 * ph) * (1 - ph ** 4))
    out += grp(815, 720, pop(t, 0.5), icon("wallet", 750, 650))
    return out + grp(540, 930, pop(t, 0.4 * T), pill(540, 930, "健康保険から出る", 50, 480))


def d2(t, T):
    out = head(t, "もらえるのは", 84, "休んで4日目から", 116)
    for k in range(5):
        t0 = 0.3 + k * 0.45
        x = 110 + k * 176
        on = k >= 3
        box = f'<rect x="{x}" y="600" width="156" height="200" rx="18" fill="{GLD if on else WHT}" stroke="{BLK}" stroke-width="8"/>'
        box += f'<rect x="{x}" y="600" width="156" height="50" rx="18" fill="{PNK if on else BLK}"/>' + txt(x + 78, 638, f"{k+1}日目", 32, WHT)
        box += txt(x + 78, 752, "¥" if on else "休", 84, BLK if on else "#999")
        out += grp(x + 78, 700, pop(t, t0, 0.3), box)
    out += grp(365, 890, pop(t, 0.3 + 2 * 0.45 + 0.2), pill(365, 890, "連続3日は待つ", 44, 500))
    return out + grp(815, 890, pop(t, 0.3 + 3 * 0.45 + 0.2), pill(815, 890, "ここから", 44, 300, PNK))


def d3(t, T):
    out = head(t, "もらえる期間は", 84, "通算1年6か月まで", 104)
    p = prog(t, 0.15 * T, 1.8)
    out += f'<rect x="120" y="640" width="840" height="100" rx="20" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="126" y="646" width="{828*p:.0f}" height="88" rx="14" fill="{GRN}"/>'
    for k in range(1, 18):
        x = 120 + 840 / 18 * k
        out += f'<line x1="{x:.0f}" y1="{646 if k % 6 else 620}" x2="{x:.0f}" y2="734" stroke="{BLK}" stroke-width="{3 if k % 6 else 6}" opacity="{0.35 if k % 6 else 1}"/>'
    out += txt(120, 800, "スタート", 40, BLK, "start") + txt(960, 800, "1年6か月", 40, BLK, "end")
    return out + grp(540, 910, pop(t, 0.15 * T + 1.8), txt(540, 950, f"{int(round(18 * p))}か月", 130, PNK))


def d4(t, T):
    out = head(t, "ただし 給料が出ると", 84, "その分 へる", 130)
    p = prog(t, 0.3 * T, 1.2)
    # seesaw: 給料 goes up, 手当金 goes down
    ang = -14 * p + 1.5 * math.sin(t * 5)
    plank = f'<rect x="170" y="748" width="740" height="24" rx="12" fill="{BLK}"/>' + pill(280, 690, "給料", 56, 260, GLD, BLK) + pill(790, 690, "手当金", 56, 280, PNK)
    out += f'<polygon points="540,772 480,900 600,900" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
    out += grp(540, 760, 1, plank, rot=-ang)
    return out + grp(540, 950, pop(t, 0.3 * T + 1.0), pill(540, 950, "差額が支給される", 44, 480))


def d5(t, T):
    out = head(t, "休むときは", 90, "健康保険に相談", 116)
    out += grp(300, 700, pop(t, 0.2), hcard(300, 700 - 10 * abs(math.sin(t * 5))))
    out += grp(760, 640, pop(t, 0.4), pill(760, 640, "本人", 44, 300))
    out += grp(760, 730, pop(t, 0.55), pill(760, 730, "会社", 44, 300, BLU))
    out += grp(760, 820, pop(t, 0.7), pill(760, 820, "医師", 44, 300, GRN))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["病気で会社を休んでも、給料のおよそ3分の2が出る制度があります。"], cap="休んでもお金が出る", note=NOTE, draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.45", "drop"), ("f0.45+0.9", "ding")]),
    dict(narr=["名前は、しょうびょうてあてきん。", "加入している健康保険から出ます。"], cap="健康保険から出るお金", note=NOTE, draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "pop"), ("f0.4", "ding")]),
    dict(narr=["仕事以外の病気やケガで、働けないときが対象。", "連続3日休んだあと、4日目から出ます。"], cap="休んで4日目から対象", note="※最初の連続3日間は待期期間", draw=d2,
         sfx=[(0.0, "whoosh")] + [(0.3 + k * 0.45, "tick") for k in range(3)] + [(0.3 + 3 * 0.45, "ding"), (0.3 + 4 * 0.45, "pop")]),
    dict(narr=["もらえる期間は、通算で1年6か月までです。"], cap="通算1年6か月まで", note="※同じ病気やケガについて", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.15", "swish"), ("f0.15+1.8", "ding")]),
    dict(narr=["ただし、休んでいる間に給料が出ると、その分へります。", "仕事中のケガは、労災保険の対象です。"], cap="給料が出ると減る", note="※業務上・通勤中の病気やケガは労災保険", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.3", "drop"), ("f0.3+1.0", "pop")]),
    dict(narr=["もしものときは、健康保険に相談。", "フォローして学ぼう。"], cap="フォローして学ぼう", note="※申請書は本人・会社・医師が記入", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.4, "tick"), (0.55, "tick"), (0.7, "tick"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v029_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v029_shobyo.mp4")
