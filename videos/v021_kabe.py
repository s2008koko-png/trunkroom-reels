"""#021 年収の壁（令和8年分）— 扶養控除は136万円・本人の所得税は178万円・社会保険の扶養は別基準。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

BRK = "#C8553D"


def wall(x, top=620, bot=980, w=64, op=1.0):
    """A brick wall: the 'income wall'."""
    out = f'<rect x="{x}" y="{top}" width="{w}" height="{bot-top}" fill="{BRK}" stroke="{BLK}" stroke-width="7"/>'
    k = 0
    y = top + 45
    while y < bot - 5:
        out += f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y}" stroke="{BLK}" stroke-width="4"/>'
        xx = x + (w * 0.33 if k % 2 else w * 0.66)
        out += f'<line x1="{xx:.0f}" y1="{y-45}" x2="{xx:.0f}" y2="{y}" stroke="{BLK}" stroke-width="4"/>'
        y += 45
        k += 1
    return f'<g opacity="{op}">{out}</g>'


def d0(t, T):
    out = head(t, "バイト代が増えると", 76, "親の税金が上がる？", 96)
    p = prog(t, 0.25 * T, 1.6)
    out += wall(800)
    out += pill(832, 575, "136万円", 46, 250, PNK)
    out += txt(120, 760, "子どもの年収", 44, BLK, "start")
    out += hbar(120, 790, 672 * p, GLD, 100)
    hit = t > 0.25 * T + 1.5
    sh = 8 * math.sin(t * 40) * (1 - clamp((t - 0.25 * T - 1.5) / 0.5)) if hit else 0
    out += txt(450 + sh, 690, f"{int(round(136 * p))}万円", 110, PNK if hit else BLK)
    return out + coin(120 + 672 * p - 55, 840, 34)


def d1(t, T):
    out = head(t, "136万円までなら", 84, "親は扶養控除を使える", 88)
    for k, (x, lab, v, col) in enumerate(((100, "16歳以上", 38, BLU), (560, "19〜22歳", 63, RED))):
        t0 = 0.3 * T + k * 0.25 * T
        n = int(round(v * prog(t, t0 + 0.1, 0.7)))
        inner = pill(x + 210, 640, lab, 44, 300, col) + txt(x + 210, 830, f"{n}万円", 104) + txt(x + 210, 915, "を引ける", 46)
        out += grp(x + 210, 760, pop(t, t0), card(x, 570, 420, 390, inner))
    return out


def d2(t, T):
    out = head(t, "19〜22歳は", 90, "すぐゼロにならない", 96)
    steps = [(120, 300, 300), (420, 110, 240), (530, 110, 180), (640, 110, 120), (750, 110, 60)]
    out += f'<line x1="105" y1="984" x2="975" y2="984" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k, (x, w, h) in enumerate(steps):
        p = prog(t, 0.2 * T + k * 0.3, 0.35)
        if p > 0:
            out += f'<rect x="{x}" y="{980-h*p:.1f}" width="{w}" height="{h*p:.1f}" fill="{RED}" stroke="{BLK}" stroke-width="6"/>'
    out += grp(270, 620, pop(t, 0.2 * T + 0.2), pill(270, 620, "最高63万円", 44, 300))
    # a coin hopping down the stairs
    q = clamp((t - 0.2 * T - 1.6) / 2.0)
    idx = min(4, int(q * 5))
    x, w, h = steps[idx]
    fr = q * 5 - idx
    out += coin(x + w / 2, 980 - h - 40 - 60 * abs(math.sin(fr * math.pi)), 34) if t > 0.2 * T + 1.6 else ""
    return out + grp(790, 760, pop(t, 0.55 * T), txt(790, 775, "年収が増えると", 40) + txt(790, 830, "だんだん減る", 40))


def d3(t, T):
    out = head(t, "自分の所得税は", 84, "178万円まで0円", 110)
    p = prog(t, 0.2 * T, 1.6)
    out += wall(608, op=0.35) + wall(860)
    out += pill(640, 575, "136万円", 36, 190, "#777") + pill(880, 575, "178万円", 44, 220, PNK)
    out += txt(120, 760, "自分の年収", 44, BLK, "start")
    out += hbar(120, 790, 732 * p, GLD, 100)
    out += coin(120 + 732 * p - 55, 840, 34)
    return out + grp(330, 655, pop(t, 0.2 * T + 1.6), pill(330, 655, "所得税 0円", 50, 330, GRN, BLK))


def d4(t, T):
    out = head(t, "ただし社会保険は", 84, "別の基準", 130)
    out += monster(250, 770 - 12 * abs(math.sin(t * 5)), GRN, t, 0.9 * pop(t, 0.2))
    inner = txt(680, 690, "扶養に入れるのは", 42) + txt(680, 790, "年収130万円", 76, PNK) + txt(680, 860, "未満", 60, PNK)
    out += grp(680, 740, pop(t, 0.4 * T), card(420, 610, 520, 290, inner))
    return out + grp(680, 950, pop(t, 0.4 * T + 0.5), pill(680, 950, "健康保険・年金", 40, 380))


def d5(t, T):
    out = head(t, "壁は2種類", 90, "税金と社会保険", 116)
    for k, (cx, col, name) in enumerate(((300, RED, "税金の壁"), (780, GRN, "社会保険の壁"))):
        out += monster(cx, 640 - 20 * abs(math.sin(t * 6 + k)), col, t + k * 0.2, 0.55 * pop(t, 0.3 + k * 0.2))
        out += grp(cx, 800, pop(t, 0.5 + k * 0.2), pill(cx, 800, name, 40, 330))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["バイト代が増えると、親の税金が上がる。", "さかいめは、136万円。"], cap="今年の壁は136万円", note="※令和8年分・給与だけの場合", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.25", "swish"), ("f0.25+1.5", "ding")]),
    dict(narr=["子の年収が136万円以下なら、親は38万円か63万円の控除を使えます。"], cap="親の所得から引ける", note="※16歳以上の子の場合",
         draw=d1, sfx=[(0.0, "whoosh"), ("f0.3", "pop"), ("f0.55", "pop")]),
    dict(narr=["19歳から22歳は、こえてもすぐゼロになりません。", "だんだん減るしくみです。"], cap="特定親族特別控除", note="※本人の所得に応じて段階的に減る", draw=d2,
         sfx=[(0.0, "whoosh")] + [(f"f0.2+{k*0.3:.1f}", "tick") for k in range(5)]),
    dict(narr=["自分の所得税は、年収178万円までかかりません。"], cap="本人の所得税は178万円", note="※令和8年分・給与だけの場合", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.2", "swish"), ("f0.2+1.6", "ding")]),
    dict(narr=["ただし、社会保険の扶養は別ルール。", "年収130万円未満などが基準です。"], cap="社会保険は別の基準", note="※19〜22歳は150万円未満", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.4", "pop"), ("f0.4+0.5", "tick")]),
    dict(narr=["かべは、税金と社会保険でべつべつ。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v021_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v021_kabe.mp4")
