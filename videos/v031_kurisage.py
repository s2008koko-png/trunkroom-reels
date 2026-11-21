"""#031 年金の繰下げ・繰上げ — 1か月0.7%増（70歳42%・75歳で最大84%）／繰上げは1か月0.4%減（最大24%）・一生変わらない。
Sources (fetched 2026-11-21): 日本年金機構 年金の繰下げ受給（更新日2026年8月12日） / 年金の繰上げ受給"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def stack(cx, base, n, t, t0, col=GLD):
    """A pile of flat coins growing one by one."""
    out = ""
    for k in range(n):
        s = pop(t, t0 + k * 0.08, 0.2)
        y = base - 18 - k * 26
        out += grp(cx, y, s, f'<ellipse cx="{cx}" cy="{y}" rx="92" ry="22" fill="{col}" stroke="{BLK}" stroke-width="6"/>')
    return out


def d0(t, T):
    out = head(t, "年金を70歳まで待つと", 78, "42%ふえる", 130)
    base = 985
    out += f'<line x1="130" y1="{base}" x2="950" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    p = prog(t, 0.45 * T, 1.0)
    h0, h1 = 240, 240 * (1 + 0.42 * p)
    out += grp(300, base, pop(t, 0.2), f'<rect x="200" y="{base-h0}" width="200" height="{h0}" fill="{BLK}"/>' + txt(300, base - h0 - 20, "65歳から", 46))
    k = pop(t, 0.35)
    out += grp(700, base, k, f'<rect x="600" y="{base-h0:.1f}" width="200" height="{h0:.1f}" fill="{BLK}"/>'
               + (f'<rect x="600" y="{base-h1:.1f}" width="200" height="{h1-h0:.1f}" fill="{PNK}"/>' if p > 0 else "")
               + txt(700, base - h1 - 20, "70歳から", 46))
    out += grp(700, base - 290, pop(t, 0.45 * T + 0.2), txt(700, base - 262, f"+{int(round(42*p))}%", 64, WHT))
    return out


def d1(t, T):
    out = head(t, "1か月 おくらせるごとに", 76, "0.7%ずつ ふえる", 104)
    base, x0, sw = 985, 150, 78
    out += f'<line x1="120" y1="{base}" x2="960" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    n = 10
    for k in range(n):
        tk = 0.4 + k * (0.7 * T - 0.4) / n
        p = prog(t, tk, 0.3)
        if p <= 0:
            continue
        h = (k + 1) * 8.4 * 3.9 * p
        col = PNK if k in (4, 9) else BLK
        out += f'<rect x="{x0+k*sw}" y="{base-h:.1f}" width="{sw-8}" height="{h:.1f}" rx="5" fill="{col}"/>'
    out += grp(x0 + 35, base - 80, pop(t, 0.6), txt(x0 + 35, base - 50, "66", 40, BLK))
    out += grp(x0 + 4 * sw + 35, 760, pop(t, 0.4 + 0.5 * (0.7 * T - 0.4)), txt(x0 + 4 * sw + 35, 800, "70歳", 44, PNK))
    out += grp(x0 + 9 * sw + 20, 610, pop(t, 0.7 * T), txt(x0 + 9 * sw + 20, 635, "75歳", 44, PNK))
    out += grp(330, 610, pop(t, 0.3), pill(330, 610, "ふつうは65歳から", 38, 380))
    return out


def d2(t, T):
    out = head(t, "75歳まで待つと", 84, "最大84%ふえる", 110)
    base = 985
    out += f'<line x1="130" y1="{base}" x2="950" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    out += stack(310, base, 7, t, 0.3) + stack(730, base, 13, t, 0.6, GLD)
    out += grp(310, 760, pop(t, 0.9), txt(310, 770, "65歳から", 46))
    out += grp(730, 610, pop(t, 1.7), txt(730, 620, "75歳から", 46, PNK))
    out += grp(470, 640, pop(t, 0.55 * T), pill(470, 640, "1.84倍", 50, 230, PNK))
    return out


def d3(t, T):
    out = head(t, "逆に60歳からもらうと", 78, "最大24%へる", 120, tb=0.5 * T)
    g, p = gauge(t, 0.5 * T, 0.76)
    out += grp(540, 655, pop(t, 0.2), g)
    out += grp(330, 860, pop(t, 0.4), txt(330, 900, f"−{int(round(24*p))}%", 150, PNK if p >= 1 else BLK))
    out += grp(770, 820, pop(t, 0.6), pill(770, 800, "1か月 0.4%ずつ", 36, 340))
    out += grp(770, 900, pop(t, 0.5 * T + 1.0), pill(770, 900, "へった額も一生", 36, 340, PNK))
    return out


def d4(t, T):
    out = head(t, "注意もある", 84, "待つ間は 0円", 120)
    # hourglass: sand running while the wallet stays empty
    cx, top, bot = 290, 580, 940
    f = clamp(t / max(T - 0.5, 1))
    out += grp(cx, 760, pop(t, 0.2),
               f'<polygon points="{cx-110},{top} {cx+110},{top} {cx+14},{760} {cx+110},{bot} {cx-110},{bot} {cx-14},{760}" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
               f'<polygon points="{cx-80*(1-f):.1f},{top+20+130*f:.1f} {cx+80*(1-f):.1f},{top+20+130*f:.1f} {cx},{750}" fill="{GLD}"/>'
               f'<polygon points="{cx-90},{bot-12} {cx+90},{bot-12} {cx+90*(1-f):.1f},{bot-12-110*f:.1f} {cx-90*(1-f):.1f},{bot-12-110*f:.1f}" fill="{GLD}"/>'
               f'<line x1="{cx}" y1="760" x2="{cx}" y2="{bot-20}" stroke="{GLD}" stroke-width="8" stroke-dasharray="14 12" stroke-dashoffset="{-t*90:.0f}"/>'
               f'<rect x="{cx-130}" y="{top-22}" width="260" height="28" rx="8" fill="{BLK}"/><rect x="{cx-130}" y="{bot-6}" width="260" height="28" rx="8" fill="{BLK}"/>')
    out += grp(720, 660, pop(t, 0.6), card(500, 575, 460, 170, txt(730, 640, "待っている間", 46) + txt(730, 712, "年金は受け取れない", 44, PNK)))
    out += grp(720, 860, pop(t, 0.5 * T), card(500, 775, 460, 170, txt(730, 840, "ふえると 税金や", 44) + txt(730, 908, "保険料に影響も", 46, PNK)))
    return out


def d5(t, T):
    out = head(t, "いつからもらうかは", 80, "自分で選べる", 120)
    x0, x1, y = 150, 930, 690
    out += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{BLK}" stroke-width="16" stroke-linecap="round"/>'
    for a in (60, 65, 70, 75):
        x = x0 + (a - 60) / 15 * (x1 - x0)
        out += f'<circle cx="{x:.0f}" cy="{y}" r="16" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>' + txt(x, y + 80, f"{a}歳", 44)
    age = 67.5 + 7.5 * math.sin(t * 1.6 - 0.6)
    x = x0 + (age - 60) / 15 * (x1 - x0)
    out += grp(x, y, pop(t, 0.2), coin(x, y - 10, 52))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["年金は、70歳まで待つと、42パーセント増えます。"], cap="70歳からなら42%増", note="※昭和27年4月2日以降生まれの場合", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "tick"), ("f0.45+1.0", "ding")]),
    dict(narr=["ふつうは65歳から。", "1か月おくらせるごとに、0.7パーセント増えます。"], cap="1か月ごとに0.7%増", draw=d1,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.6, "tick"), ("f0.7", "ding")]),
    dict(narr=["75歳まで待つと、最大84パーセント増。"], cap="75歳で最大84%増", draw=d2, sfx=[(0.0, "whoosh"), (0.3, "tick"), (0.6, "tick"), ("f0.55", "ding")]),
    dict(narr=["逆に60歳まで早めると、1か月ごとに0.4パーセント減り、最大24パーセント減。"], cap="早めると最大24%減",
         note="※昭和37年4月2日以降生まれの場合", draw=d3, sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.5", "drop"), ("f0.5+1.0", "pop")]),
    dict(narr=["増えた額も減った額も、一生そのまま。", "待っている間は、年金を受け取れません。"], cap="待つ間は受け取れない", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.6, "pop"), ("f0.5", "pop")]),
    dict(narr=["いつから受け取るかは、自分で選べます。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v031_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v031_kurisage.mp4")
