"""#016 生命保険料控除 — 生命保険・介護医療保険・個人年金保険の保険料は所得控除（新契約：各区分 年8万円超で一律4万円、合計上限12万円）、
令和8年分以降は23歳未満の扶養親族がいる人の新生命保険料の控除が最高6万円、所得から引く控除、年末調整は保険料控除申告書。
Sources (fetched 2026-11-16): 国税庁 No.1140 生命保険料控除（令和8年4月1日現在法令等） / 令和8年分 年末調整Q&A"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def umbrella(cx, cy, s=1.0, rot=0.0):
    """Original umbrella ~300x300 centred at (cx, cy)."""
    g = (f'<path d="M{cx-150} {cy} Q{cx-150} {cy-150} {cx} {cy-150} Q{cx+150} {cy-150} {cx+150} {cy} Q{cx+100} {cy-40} {cx+50} {cy} Q{cx} {cy-40} {cx-50} {cy} Q{cx-100} {cy-40} {cx-150} {cy} Z" fill="{PNK}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<path d="M{cx} {cy-20} L{cx} {cy+110} Q{cx} {cy+150} {cx-36} {cy+150} Q{cx-66} {cy+150} {cx-66} {cy+118}" fill="none" stroke="{BLK}" stroke-width="12" stroke-linecap="round"/>'
         f'<line x1="{cx}" y1="{cy-150}" x2="{cx}" y2="{cy-176}" stroke="{BLK}" stroke-width="12" stroke-linecap="round"/>')
    return grp(cx, cy, s, g, rot=rot)


def heart(cx, cy, r=50):
    return (f'<path d="M{cx} {cy+r} Q{cx-r*1.5} {cy} {cx-r*1.1} {cy-r*0.6} Q{cx-r*0.55} {cy-r*1.2} {cx} {cy-r*0.45} Q{cx+r*0.55} {cy-r*1.2} {cx+r*1.1} {cy-r*0.6} Q{cx+r*1.5} {cy} {cx} {cy+r} Z" '
            f'fill="{PNK}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>')


def kid(cx, cy, s=1.0):
    g = (f'<circle cx="{cx}" cy="{cy}" r="70" fill="#FFD9B0" stroke="{BLK}" stroke-width="7"/>'
         f'<path d="M{cx-66} {cy-22} Q{cx} {cy-110} {cx+66} {cy-22} Q{cx} {cy-58} {cx-66} {cy-22} Z" fill="{BLK}"/>'
         f'<circle cx="{cx-24}" cy="{cy+4}" r="7" fill="{BLK}"/><circle cx="{cx+24}" cy="{cy+4}" r="7" fill="{BLK}"/>'
         f'<path d="M{cx-22} {cy+30} Q{cx} {cy+50} {cx+22} {cy+30}" fill="none" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>')
    return grp(cx, cy, s, g)


def d0(t, T):
    out = head(t, "生命保険に入ってる人", 80, "最高12万円 引ける", 96)
    out += umbrella(235, 790 + 8 * math.sin(t * 5), 1.0, rot=4 * math.sin(t * 3))
    p = prog(t, 0.3 * T, 1.0)
    out += txt(710, 790, f"{int(round(12 * p))}万円", 150, PNK if p >= 1 else BLK)
    out += grp(700, 900, pop(t, 0.3 * T + 1.0), pill(700, 900, "所得から引ける", 46, 420))
    return out


def d1(t, T):
    out = head(t, "対象になる保険は", 84, "この3種類", 130)
    items = [("生命保険", 0.25 * T), ("介護医療保険", 0.5 * T), ("個人年金保険", 0.72 * T)]
    for k, (lab, t0) in enumerate(items):
        x = 100 + k * 305
        cx = x + 135
        ic = heart(cx, 720, 62) if k == 0 else icon("hospital" if k == 1 else "old", cx - 65, 650)
        out += grp(cx, 760 - 10 * abs(math.sin(t * 5 + k)), pop(t, t0), card(x, 580, 270, 380, ic + txt(cx, 900, lab, 40)))
    return out


def d2(t, T):
    out = head(t, "年8万円こえて払うと", 80, "それぞれ4万円", 120)
    for k, lab in enumerate(("生命保険", "介護医療保険", "個人年金保険")):
        y, t0 = 545 + k * 105, 0.08 * T + k * 0.5
        out += grp(250, y + 45, pop(t, t0, 0.3), txt(120, y + 62, lab, 44, BLK, "start"))
        out += hbar(430, y + 14, 300 * prog(t, t0 + 0.1, 0.5), (PNK, BLU, GRN)[k], 70)
        out += grp(820, y + 45, pop(t, t0 + 0.5, 0.3), txt(750, y + 68, "4万円", 54, BLK, "start"))
    out += grp(540, 925, pop(t, 0.62 * T), pill(540, 925, "合計の上限は12万円", 52, 620, PNK))
    return out


def d3(t, T):
    out = head(t, "23歳未満を扶養する人", 80, "生命保険は6万円に", 96)
    out += kid(210, 700 + 8 * math.sin(t * 5), pop(t, 0.2))
    p = prog(t, 0.5 * T, 0.9)
    w = 100 * (4 + 2 * p)
    out += hbar(340, 640, 400, PNK, 110)
    if p > 0.01:
        out += hbar(340, 640, w, PNK, 110) + f'<rect x="{740}" y="646" width="{w-400-6:.1f}" height="98" rx="6" fill="{GLD}"/>'
    for k in range(1, 6):
        out += f'<line x1="{340+100*k}" y1="646" x2="{340+100*k}" y2="744" stroke="{BLK}" stroke-width="3" opacity="0.35"/>'
    out += txt(660, 900, f"{4 + 2 * p:.0f}万円" if p in (0, 1) else f"{4 + 2 * p:.1f}万円", 130, PNK if p >= 1 else BLK)
    out += grp(210, 880, pop(t, 0.35), pill(210, 880, "扶養", 44, 180, BLU))
    return out


def d4(t, T):
    out = head(t, "税金が12万円", 90, "へるわけではない", 104)
    p = prog(t, 0.3 * T, 0.9)
    x, y, w = 110, 600, 860
    cut = 130
    out += f'<rect x="{x}" y="{y}" width="{w}" height="110" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="{x+4}" y="{y+4}" width="{w-cut-8}" height="102" rx="10" fill="{GLD}"/>'
    out += f'<rect x="{x+w-cut-4}" y="{y+4}" width="{cut}" height="102" rx="10" fill="{PNK}" opacity="{1-0.8*p:.2f}"/>'
    out += txt(x + (w - cut) / 2, y + 74, "税金を計算するもとの金額", 46)
    out += grp(x + w - cut / 2, y - 40 - 30 * p, pop(t, 0.3 * T), txt(x + w - 20, y + 170, "−12万円", 56, PNK, "end"))
    out += monster(250, 880, RED, t, 0.5 * pop(t, 0.55 * T))
    out += grp(640, 900, pop(t, 0.55 * T + 0.3), pill(640, 900, "ここに税率をかける", 46, 520))
    return out


def d5(t, T):
    out = head(t, "年末調整で", 90, "申告書を会社に出す", 96)
    q = prog(t, 0.2, 1.2)
    sx = 200 + 330 * q
    sheet = card(sx - 80, 590, 160, 200) + f'<rect x="{sx-76}" y="594" width="152" height="46" rx="12" fill="{BLK}"/>' + txt(sx, 628, "申告書", 32, YEL)
    for k in range(3):
        sheet += f'<rect x="{sx-56}" y="{662+k*40}" width="112" height="16" rx="6" fill="#BBB"/>'
    bld = f'<rect x="700" y="570" width="220" height="260" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    for r in range(3):
        for c in range(3):
            bld += f'<rect x="{724+c*64}" y="{594+r*62}" width="44" height="40" fill="{BLU}" stroke="{BLK}" stroke-width="4"/>'
    bld += f'<rect x="786" y="776" width="48" height="54" fill="{BLK}"/>'
    out += bld + grp(sx, 690, 1.0, sheet, rot=-6 + 5 * math.sin(t * 5))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["生命保険に入っている人。", "所得から、最高12万円を引けます。"], cap="所得から最高12万円", note="※生命保険料控除（国税庁 No.1140）", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.3", "drop"), ("f0.3+1.0", "ding")]),
    dict(narr=["対象は、生命保険、介護医療保険、個人年金保険の3種類。"], cap="対象の保険は3種類", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.25", "pop"), ("f0.5", "pop"), ("f0.72", "pop")]),
    dict(narr=["1年に8万円をこえて払うと、それぞれ4万円。", "合計の上限は12万円。"], cap="3つ合わせて最高12万円", note="※平成24年以後に契約した保険の場合", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.08", "tick"), ("f0.08+0.5", "tick"), ("f0.08+1.0", "tick"), ("f0.62", "ding")]),
    dict(narr=["今年から、23歳未満を扶養する人は、生命保険のわくが6万円に。"], cap="生命保険のわくが6万円", note="※令和8年分以降・年12万円をこえて払った場合", draw=d3,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.5", "drop"), ("f0.5+0.9", "ding")]),
    dict(narr=["ただし、税金が12万円へるわけではなく、計算のもとの金額がへります。"], cap="引くのは所得から", note="※所得控除＝所得から差し引くしくみ", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.3", "swish"), ("f0.55", "pop")]),
    dict(narr=["年末調整で、申告書を会社にだそう。", "フォローしてね。"], cap="フォローして学ぼう", note="※給与所得者の保険料控除申告書", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v016_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v016_seimeihoken.mp4")
