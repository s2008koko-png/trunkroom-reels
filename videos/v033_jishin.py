"""#033 地震保険料控除 — 地震保険料は年5万円まで全額を所得から引ける（5万円超は一律5万円）。所得控除。年末調整でOK。
Sources (fetched 2026-11-22): 国税庁 No.1145 地震保険料控除（令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def house(cx, cy, s=1.0, rot=0.0, col=BLU):
    """Simple original house ~260 wide, 250 tall, centred on (cx, cy)."""
    h = (f'<rect x="{cx-105}" y="{cy-20}" width="210" height="145" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<polygon points="{cx-140},{cy-14} {cx},{cy-125} {cx+140},{cy-14}" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<rect x="{cx-28}" y="{cy+45}" width="56" height="80" fill="{BLK}"/>'
         f'<rect x="{cx+45}" y="{cy+15}" width="40" height="40" fill="{YEL}" stroke="{BLK}" stroke-width="6"/>'
         f'<rect x="{cx-85}" y="{cy+15}" width="40" height="40" fill="{YEL}" stroke="{BLK}" stroke-width="6"/>')
    return grp(cx, cy + 125, s, h, rot=rot)


def paper(cx, cy, label="", w=150, h=190, col=PNK):
    p = f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="10" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
    p += f'<rect x="{cx-w/2+18}" y="{cy-h/2+18}" width="{w-36}" height="26" rx="6" fill="{col}"/>'
    for r in range(3):
        p += f'<rect x="{cx-w/2+18}" y="{cy-h/2+64+r*34}" width="{w-36-r*24}" height="16" rx="6" fill="#BBB"/>'
    if label:
        p += txt(cx, cy + h / 2 + 52, label, 40)
    return p


def d0(t, T):
    out = head(t, "地震保険の保険料", 84, "5万円まで全額引ける", 88)
    shake = 7 * math.sin(t * 22) * (0.4 + 0.6 * abs(math.sin(t * 1.7)))
    # ground cracks
    out += f'<path d="M110 985 L300 985 L330 965 L370 992 L420 978 L470 985 L960 985" fill="none" stroke="{BLK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    out += house(290, 855, pop(t, 0.15), rot=shake * 0.5)
    # shield with yen = the insurance
    sh = (f'<path d="M700 600 L850 640 L850 770 Q850 880 700 940 Q550 880 550 770 L550 640 Z" fill="{GRN}" stroke="{BLK}" stroke-width="9" stroke-linejoin="round"/>'
          + txt(700, 800, "5万円", 82, WHT) + txt(700, 700, "年", 50, WHT))
    out += grp(700, 770, pop(t, 0.3) * (1 + 0.04 * math.sin(t * 6)), sh)
    out += grp(900, 590, pop(t, 0.45 * T), pill(900, 590, "全額", 44, 170, PNK))
    return out


def d1(t, T):
    out = head(t, "名前は", 80, "地震保険料控除", 116)
    # income bar; a chunk is cut off
    p = prog(t, 0.45 * T, 0.8)
    x, y, w, h = 130, 640, 820, 120
    cut = 170
    out += grp(540, 600, pop(t, 0.2), txt(130, 612, "所得（税金を計算するもと）", 44, BLK, "start"))
    out += grp(540, 700, pop(t, 0.25), f'<rect x="{x}" y="{y}" width="{w-cut}" height="{h}" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>')
    out += grp(540, 700, pop(t, 0.25), f'<rect x="{x+w-cut}" y="{y + 190*p:.1f}" width="{cut}" height="{h}" fill="{GRN}" stroke="{BLK}" stroke-width="8" transform="rotate({12*p:.1f} {x+w-cut/2} {y+h/2+190*p:.1f})"/>'
               + txt(x + w - cut / 2, y + 78 + 190 * p, "保険料", 42, WHT))
    out += grp(380, 890, pop(t, 0.45 * T + 0.5), pill(380, 890, "小さくなる", 46, 330, PNK))
    return out


def d2(t, T):
    out = head(t, "引けるのは", 80, "年5万円まで", 130)
    base, cap_y = 985, 985 - 250
    out += f'<line x1="110" y1="{base}" x2="970" y2="{base}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k, (lab, paid, t0) in enumerate((("3万円 払った", 150, 0.3), ("8万円 払った", 400, 0.5 * T))):
        x = 170 + k * 420
        hh = paid * prog(t, t0, 0.7)
        if hh <= 0:
            continue
        ded = min(hh, 250)
        if hh > 250:
            out += f'<rect x="{x}" y="{base-hh:.1f}" width="220" height="{hh-250:.1f}" fill="#CCC" stroke="{BLK}" stroke-width="7"/>'
        out += f'<rect x="{x}" y="{base-ded:.1f}" width="220" height="{ded:.1f}" fill="{GRN}" stroke="{BLK}" stroke-width="7"/>'
        out += grp(x + 110, base - 60, pop(t, t0 + 0.6), txt(x + 110, base - 50, "3万円" if k == 0 else "5万円", 60, WHT) + txt(x + 110, base - 115, "引ける", 38, WHT))
        out += grp(x + 110, base - paid - 34, pop(t, t0 + 0.2), txt(x + 110, base - paid - 20, lab, 40, BLK))
    out += f'<line x1="110" y1="{cap_y}" x2="970" y2="{cap_y}" stroke="{PNK}" stroke-width="12" stroke-dasharray="34 20"/>'
    out += grp(455, cap_y - 40, pop(t, 0.2), pill(455, cap_y - 40, "上限", 38, 150, PNK))
    return out


def d3(t, T):
    out = head(t, "会社員は", 80, "年末調整でOK", 120)
    p = prog(t, 0.35 * T, 1.0)
    x, y = 250 + 380 * p, 740 - 110 * math.sin(math.pi * p)
    bx = 760
    out += grp(bx + 90, 760, pop(t, 0.2), f'<rect x="{bx}" y="640" width="180" height="250" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
               f'<rect x="{bx-14}" y="618" width="208" height="32" fill="{BLU}" stroke="{BLK}" stroke-width="7"/>'
               + "".join(f'<rect x="{bx+24+c*56}" y="{674+r*58}" width="34" height="34" fill="{BLU}"/>' for c in range(3) for r in range(2))
               + f'<rect x="{bx+68}" y="826" width="44" height="64" fill="{BLK}"/>' + txt(bx + 90, 950, "会社", 46))
    out += grp(x, y, pop(t, 0.3) * (1 - 0.45 * p), paper(x, y), rot=-10 + 20 * p)
    out += grp(250, 930, pop(t, 0.4), pill(250, 930, "控除証明書", 42, 290))
    out += grp(850, 590, pop(t, 0.35 * T + 1.0), txt(850, 600, "OK!", 70, PNK))
    return out


def d4(t, T):
    out = head(t, "ただし 税金が5万円", 80, "へるわけじゃない", 104)
    out += grp(250, 700, pop(t, 0.2), card(110, 600, 280, 200, txt(250, 670, "所得", 46) + txt(250, 760, "−5万円", 66, GRN)))
    out += grp(455, 700, pop(t, 0.35 * T), txt(455, 725, "×", 80))
    out += grp(590, 700, pop(t, 0.35 * T + 0.2), card(520, 600, 150, 200, txt(595, 670, "税率", 40) + txt(595, 760, "10%", 58, RED)))
    out += grp(715, 700, pop(t, 0.6 * T), txt(715, 725, "＝", 70))
    out += grp(865, 700, pop(t, 0.6 * T + 0.2) * (1 + 0.04 * math.sin(t * 7)), card(765, 600, 210, 200, txt(870, 670, "税金", 44) + txt(870, 760, "−5千円", 54, PNK)))
    out += monster(540, 915, RED, t, 0.42 * pop(t, 0.6 * T + 0.3))
    return out


def d5(t, T):
    out = head(t, "保険の証明書は", 84, "捨てないで", 130)
    for k in range(3):
        cx = 300 + k * 240
        dy = -14 * abs(math.sin(t * 5 + k))
        out += grp(cx, 700, pop(t, 0.2 + k * 0.15), paper(cx, 700 + dy, w=150, h=180, col=(GRN, PNK, BLU)[k]))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["地震保険の保険料は、ねん5万円まで、全額を所得から引けます。"], cap="地震保険料は引ける", draw=d0,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), (0.3, "pop"), ("f0.45", "ding")]),
    dict(narr=["これを、地震保険料控除といいます。", "税金を計算するもとの所得が、小さくなります。"], cap="所得から引く控除", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "drop"), ("f0.45+0.5", "pop")]),
    dict(narr=["3万円払ったら、3万円。", "8万円払っても、引けるのは5万円まで。"], cap="5万円超は一律5万円", draw=d2,
         sfx=[(0.0, "whoosh"), (0.3, "tick"), ("f0.5", "tick"), ("f0.5+0.6", "pop")]),
    dict(narr=["会社員は、年末調整で、控除証明書を出せばOK。"], cap="証明書を会社に出す", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.35", "swish"), ("f0.35+1.0", "ding")]),
    dict(narr=["ただし、税金が5万円へるわけではありません。", "税率10パーセントの人なら、へるのは5,000円。"], cap="へるのは一部だけ",
         note="※所得税の税率10%の人が5万円引く例", draw=d4, sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.35", "tick"), ("f0.6", "tick"), ("f0.6+0.2", "pop")]),
    dict(narr=["保険会社から届く証明書は、捨てないで。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v033_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v033_jishin.mp4")
