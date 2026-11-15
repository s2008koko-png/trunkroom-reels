"""#013 副業と確定申告 — 会社員は年末調整で終わるが、給料以外の所得が年20万円をこえると確定申告が必要。
20万円は売上ではなく「もうけ」（収入−必要経費）。副業がアルバイト（給与2か所）のときは給料の金額で数える。
Sources (fetched 2026-11-15): 国税庁 No.1900 給与所得者で確定申告が必要な人 / No.1500 雑所得（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

PUR = "#8E5BFF"


def jar(cx, base, fill, t, line=0.5, w=300, h=380):
    """Original glass jar filling with gold; a dashed pink line marks the 20万円 level."""
    x, y = cx - w / 2, base - h
    fh = (h - 16) * clamp(fill)
    j = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    if fh > 4:
        j += f'<rect x="{x+8}" y="{base-8-fh:.1f}" width="{w-16}" height="{fh:.1f}" rx="24" fill="{GLD}"/>'
        for k in range(4):
            j += f'<circle cx="{x+50+k*66+8*math.sin(t*3+k):.1f}" cy="{base-8-fh+6:.1f}" r="16" fill="{YEL}" stroke="{BLK}" stroke-width="4"/>'
    ly = base - 8 - (h - 16) * line
    j += f'<line x1="{x-30}" y1="{ly}" x2="{x+w+30}" y2="{ly}" stroke="{PNK}" stroke-width="8" stroke-dasharray="20 12"/>'
    j += f'<rect x="{cx-70}" y="{y-34}" width="140" height="40" rx="10" fill="{BLK}"/>'
    return j, ly


def laptop(cx, cy, s=1.0):
    g = (f'<rect x="{cx-90}" y="{cy-70}" width="180" height="120" rx="12" fill="{BLK}"/>'
         f'<rect x="{cx-76}" y="{cy-58}" width="152" height="96" rx="6" fill="{BLU}"/>'
         f'<polygon points="{cx-120},{cy+78} {cx+120},{cy+78} {cx+98},{cy+50} {cx-98},{cy+50}" fill="#999" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>')
    return grp(cx, cy, s, g)


def office(cx, cy, s=1.0, col="#B9C4D6"):
    g = f'<rect x="{cx-75}" y="{cy-110}" width="150" height="220" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
    for r in range(3):
        for c in range(2):
            g += f'<rect x="{cx-48+c*58}" y="{cy-86+r*58}" width="38" height="36" fill="{WHT}" stroke="{BLK}" stroke-width="5"/>'
    return grp(cx, cy, s, g)


def d0(t, T):
    out = head(t, "副業のもうけが", 84, "年20万円をこえたら？", 88)
    p = prog(t, 0.25 * T, 0.5 * T)
    j, ly = jar(330, 990, 0.66 * p, t)
    out += j
    if 0 < p < 1:
        q = (t * 2.2) % 1.0
        out += coin(330 + 40 * math.sin(t * 7), 500 + 110 * q, 34)
    val = int(round(26 * p))
    over = val > 20
    out += grp(755, 690, 1 + (0.06 * math.sin(t * 12) if over else 0), txt(755, 725, f"{val}万円", 124, PNK if over else BLK))
    out += grp(735, 905, pop(t, 0.25 * T + 0.5 * T * 0.72), pill(735, 940, "確定申告が必要", 50, 440, PNK))
    return out + txt(520, ly + 46, "20万円", 44, PNK, "start")


def d1(t, T):
    out = head(t, "会社員はふつう", 84, "年末調整でおわり", 104)
    out += office(240, 760, pop(t, 0.15))
    sheet = card(450, 590, 330, 360) + f'<rect x="454" y="594" width="322" height="76" rx="14" fill="{BLK}"/>' + txt(615, 648, "年末調整", 50, YEL)
    for k in range(3):
        sheet += f'<rect x="490" y="{710+k*62}" width="{250*prog(t, 0.5+k*0.2, 0.4):.0f}" height="22" rx="8" fill="#BBB"/>'
    out += grp(615, 770, pop(t, 0.3), sheet)
    st = 0.55 * T
    stamp = f'<circle cx="850" cy="880" r="92" fill="{WHT}" stroke="{PNK}" stroke-width="12"/>' + txt(850, 866, "申告", 52, PNK) + txt(850, 924, "不要", 52, PNK)
    return out + grp(850, 880, pop(t, st, 0.3), stamp, rot=-14)


def d2(t, T):
    out = head(t, "給料以外のもうけが", 80, "年20万円がライン", 100)
    out += laptop(200, 640, 0.8 * pop(t, 0.15)) + grp(200, 740, pop(t, 0.3), pill(200, 750, "副業", 44, 180, PUR))
    x0, w, y = 330, 620, 610
    lim = x0 + w * 0.62
    out += f'<rect x="{x0}" y="{y}" width="{w}" height="96" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    p = prog(t, 0.3 * T, 0.45 * T)
    ww = (w - 8) * p
    out += f'<rect x="{x0+4}" y="{y+4}" width="{min(ww, lim-x0-4):.1f}" height="88" rx="10" fill="{GLD}"/>' if ww > 2 else ""
    if x0 + 4 + ww > lim:
        out += f'<rect x="{lim}" y="{y+4}" width="{x0+4+ww-lim:.1f}" height="88" rx="10" fill="{PNK}"/>'
    out += f'<line x1="{lim}" y1="{y-30}" x2="{lim}" y2="{y+126}" stroke="{BLK}" stroke-width="8" stroke-dasharray="14 10"/>' + txt(lim, y + 170, "20万円", 48, BLK)
    hit = 0.3 * T + 0.45 * T * 0.5
    out += grp(480, 890, pop(t, 0.4), txt(lim - 20, 905, "申告不要", 50, BLK, "end")) if t < hit else ""
    out += grp(800, 900, pop(t, hit) * (1 + 0.05 * math.sin(t * 9)), pill(770, 900, "こえたら確定申告", 46, 430, PNK))
    return out


def d3(t, T):
    out = head(t, "20万円は売上じゃない", 80, "経費を引いたもうけ", 96)
    rows = [("売上", 50, GLD, "50万円", 0.1 * T), ("経費", 35, "#999", "−35万円", 0.38 * T), ("もうけ", 15, PNK, "15万円", 0.66 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 560 + k * 145
        out += grp(200, y + 60, pop(t, t0, 0.3), txt(130, y + 78, lab, 56, BLK, "start"))
        out += hbar(330, y + 22, v * 9.6 * prog(t, t0 + 0.1, 0.6), col, 78)
        out += grp(330 + v * 9.6 + 110, y + 60, pop(t, t0 + 0.6, 0.3), txt(330 + v * 9.6 + 20, y + 80, val, 52, PNK if k == 2 else BLK, "start"))
    out += f'<line x1="120" y1="838" x2="960" y2="838" stroke="{BLK}" stroke-width="6" opacity="{clamp((t-0.6*T)*4):.2f}"/>'
    return out


def d4(t, T):
    out = head(t, "副業がアルバイトなら", 80, "給料の金額で数える", 96)
    out += office(250, 740, pop(t, 0.15)) + grp(250, 910, pop(t, 0.3), pill(250, 910, "本業", 46, 200))
    out += office(790, 740, pop(t, 0.3 * T), "#FFC6DA") + grp(790, 910, pop(t, 0.3 * T + 0.15), pill(790, 910, "バイト", 46, 220, PNK))
    if t > 0.3 * T + 0.4:
        for k in range(3):
            q = ((t - 0.3 * T - 0.4) / 1.0 + k / 3) % 1.0
            out += coin(680 - 160 * q, 760 - 90 * math.sin(math.pi * q), 30)
    out += grp(520, 610, pop(t, 0.55 * T), pill(520, 610, "経費は引かない", 44, 380, BLK, YEL))
    return out


def d5(t, T):
    out = head(t, "副業をしたら", 84, "もうけを記録しよう", 96)
    note = card(390, 560, 300, 270)
    for k in range(3):
        note += f'<rect x="430" y="{610+k*62}" width="{220*prog(t, 0.3+k*0.25, 0.4):.0f}" height="24" rx="8" fill="{[GLD, "#999", PNK][k]}"/>'
    out += grp(540, 695, pop(t, 0.15), note, rot=-4 + 3 * math.sin(t * 4))
    out += coin(250, 700 - 22 * abs(math.sin(t * 6)), 50) + coin(830, 700 - 22 * abs(math.sin(t * 6 + 1)), 50)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["副業のもうけが、年20万円をこえたら。", "会社員でも、確定申告が必要です。"], cap="20万円こえたら確定申告", csize=58, note="※給与が1か所の会社員の場合", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.25", "tick"), ("f0.4", "tick"), ("f0.5", "tick"), ("f0.61", "ding")]),
    dict(narr=["会社員の税金は、ふつう年末調整でおわり。", "自分で申告はしません。"], cap="ふつうは申告いらない", draw=d1,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.55", "pop")]),
    dict(narr=["でも、給料以外のもうけが年20万円をこえると、確定申告が必要になります。"], cap="ラインは年20万円", note="※給与所得・退職所得以外の所得の合計", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.3", "drop"), ("f0.52", "ding")]),
    dict(narr=["20万円は、売上ではありません。", "売上から経費を引いた、もうけです。"], cap="売上−経費＝もうけ", note="※例：売上50万円・経費35万円のとき", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.1", "tick"), ("f0.38", "tick"), ("f0.66", "ding")]),
    dict(narr=["副業がアルバイトなら、もらった給料の金額で数えます。"], cap="バイトは給料の金額", note="※2か所から給与をもらう場合", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.3", "pop"), ("f0.55", "pop")]),
    dict(narr=["副業をしたら、もうけを記録しておこう。", "フォローして、お金を学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v013_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v013_fukugyo.mp4")
