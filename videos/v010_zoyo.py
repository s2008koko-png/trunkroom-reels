"""#010 贈与税の基本 — もらったお金にも税金。年110万円までは0円、払うのはもらった人、翌年2/1〜3/15に申告。
Sources (fetched 2026-11-14): 国税庁 No.4402 贈与税がかかる場合 / No.4405 贈与税がかからない場合（ともに令和8年4月1日現在法令等）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

PUR = "#8E5CFF"  # 贈与税 monster


def gift(cx, cy, s=1.0, lid=0.0, col=PNK, rot=0.0):
    """Original gift box ~220x190 centred at (cx, cy). `lid` 0..1 lifts and tilts the lid."""
    b = (f'<rect x="{cx-100}" y="{cy-50}" width="200" height="140" rx="12" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{cx-18}" y="{cy-50}" width="36" height="140" fill="{GLD}" stroke="{BLK}" stroke-width="6"/>')
    l = (f'<rect x="{cx-114}" y="{cy-96}" width="228" height="50" rx="12" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{cx-18}" y="{cy-96}" width="36" height="50" fill="{GLD}" stroke="{BLK}" stroke-width="6"/>'
         f'<path d="M{cx} {cy-96} q-50 -60 -70 -20 q10 30 70 20 q50 -60 70 -20 q-10 30 -70 20" fill="{GLD}" stroke="{BLK}" stroke-width="6" stroke-linejoin="round"/>')
    return grp(cx, cy, s, b + grp(cx - 110, cy - 50, 1, f'<g transform="translate(0,{-20*lid:.1f})">{l}</g>', rot=-32 * lid), rot=rot)


def person(cx, cy, col, s=1.0, bob=0.0):
    """Simple original person ~150x260: round head + body."""
    p = (f'<path d="M{cx-75} {cy+130} L{cx-75} {cy+40} Q{cx-75} {cy-20} {cx} {cy-24} Q{cx+75} {cy-20} {cx+75} {cy+40} L{cx+75} {cy+130} Z" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-80}" r="56" fill="#FFD9B0" stroke="{BLK}" stroke-width="8"/>'
         f'<circle cx="{cx-20}" cy="{cy-84}" r="7" fill="{BLK}"/><circle cx="{cx+20}" cy="{cy-84}" r="7" fill="{BLK}"/>'
         f'<path d="M{cx-18} {cy-60} Q{cx} {cy-46} {cx+18} {cy-60}" fill="none" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>')
    return grp(cx, cy, s, f'<g transform="translate(0,{bob:.1f})">{p}</g>')


def d0(t, T):
    out = head(t, "親からもらったお金にも", 76, "税金がかかる？", 110)
    lid = prog(t, 0.25 * T, 0.6)
    cy = 800 - 170 * prog(t, 0.25 * T + 0.2, 0.8)
    out += coin(320, cy, 52) if t > 0.25 * T + 0.2 else ""
    out += gift(300, 870 + 5 * math.sin(t * 6), 1.15, lid)
    p = prog(t, 0.5 * T, 0.8)
    out += grp(730, 700, pop(t, 0.5 * T), txt(730, 745, f"{int(round(110 * p))}万円", 120, PNK if p >= 1 else BLK))
    return out + grp(730, 890, pop(t, 0.5 * T + 0.9) * (1 + 0.04 * math.sin(t * 8)), pill(730, 890, "ここまで 0円", 54, 420, BLK, YEL))


def d1(t, T):
    out = head(t, "この税金は贈与税", 84, "払うのはもらった人", 96)
    out += person(220, 760, BLK, pop(t, 0.15)) + grp(220, 950, pop(t, 0.3), pill(220, 950, "あげた人", 42, 250))
    arrive = 0.2 * T + 1.0
    out += person(600, 760, BLU, pop(t, 0.3), bob=-16 * abs(math.sin(t * 6)) if t > arrive else 0)
    out += grp(600, 950, pop(t, 0.45), pill(600, 950, "もらった人", 42, 280, PNK))
    p = clamp((t - 0.2 * T) / 1.0)
    if 0 < p < 1:
        out += coin(220 + 380 * p, 640 - 150 * math.sin(math.pi * p), 46)
    out += monster(865, 730 - 12 * abs(math.sin(t * 5)), PUR, t, 0.52 * pop(t, arrive + 0.2))
    return out + grp(865, 905, pop(t, arrive + 0.45), pill(865, 905, "贈与税", 42, 210, PUR))


def d2(t, T):
    out = head(t, "1月1日〜12月31日の", 80, "合計で見る", 120)
    x0, w, y, h = 130, 820, 700, 120
    xl = x0 + w * 0.55                      # 110万円 line (bar full width = 200万円)
    f = 0.8 * prog(t, 0.3, 0.6 * T)         # fills to 160万円 (example)
    out += f'<rect x="{x0}" y="{y}" width="{w}" height="{h}" rx="18" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="{x0+4}" y="{y+4}" width="{max(0, min(f, 0.55)*w-4):.1f}" height="{h-8}" rx="14" fill="{GLD}"/>'
    if f > 0.55:
        out += f'<rect x="{xl:.1f}" y="{y+4}" width="{(f-0.55)*w:.1f}" height="{h-8}" fill="{PNK}"/>'
    out += f'<line x1="{xl:.1f}" y1="{y-40}" x2="{xl:.1f}" y2="{y+h+30}" stroke="{BLK}" stroke-width="8" stroke-dasharray="16 10"/>'
    out += grp(xl, 610, pop(t, 0.2), pill(xl, 610, "110万円", 50, 290))
    out += txt(x0, y + h + 60, "1月", 44, BLK, "start") + txt(x0 + w, y + h + 60, "12月", 44, BLK, "end")
    out += grp(350, 925, pop(t, 0.3 + 0.35 * T), pill(350, 925, "ここまで0円", 44, 320, GLD, BLK))
    return out + grp(745, 925, pop(t, 0.3 + 0.62 * T) * (1 + 0.05 * math.sin(t * 9)), pill(745, 925, "こえた分に税金", 44, 380, PNK))


def mark(cx, cy, ok):
    if ok:
        return f'<circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="{GRN}" stroke-width="20"/>'
    return (f'<line x1="{cx-46}" y1="{cy-46}" x2="{cx+46}" y2="{cy+46}" stroke="{PNK}" stroke-width="22" stroke-linecap="round"/>'
            f'<line x1="{cx+46}" y1="{cy-46}" x2="{cx-46}" y2="{cy+46}" stroke="{PNK}" stroke-width="22" stroke-linecap="round"/>')


def d3(t, T):
    out = head(t, "生活費や学費は", 84, "そのつど使えば0円", 96)
    rows = [("生活費", True, 100, 545, 0.1 * T), ("学費", True, 560, 545, 0.1 * T + 0.3), ("貯金する", False, 100, 775, 0.55 * T), ("株を買う", False, 560, 775, 0.55 * T + 0.3)]
    for lab, ok, x, y, t0 in rows:
        wob = 0 if ok else 3 * math.sin(t * 14) * (t > t0 + 0.4)
        out += grp(x + 210, y + 102, pop(t, t0), card(x, y, 420, 205, txt(x + 140, y + 124, lab, 58) + grp(x + 335, y + 102, pop(t, t0 + 0.3), mark(x + 340, y + 102, ok))), rot=wob)
    return out


def d4(t, T):
    out = head(t, "110万円をこえたら", 84, "次の年に申告", 120)
    x1, x2, y = 250, 830, 760
    out += f'<line x1="130" y1="{y}" x2="950" y2="{y}" stroke="{BLK}" stroke-width="10" stroke-linecap="round"/>'
    p = prog(t, 0.25 * T, 1.2)
    out += f'<rect x="{x1}" y="{y-24}" width="{(x2-x1)*p:.1f}" height="48" rx="10" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>' if p > 0 else ""
    for x, lab, t0 in ((x1, "2/1", 0.2), (x2, "3/15", 0.25 * T + 1.0)):
        out += grp(x, y, pop(t, t0), f'<circle cx="{x}" cy="{y}" r="26" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>' + txt(x, y - 60, lab, 84))
    dx = x1 + (x2 - x1) * p
    doc = (f'<rect x="{dx-45}" y="{y+50}" width="90" height="116" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
           + "".join(f'<line x1="{dx-26}" y1="{y+80+k*24}" x2="{dx+26}" y2="{y+80+k*24}" stroke="{BLK}" stroke-width="6"/>' for k in range(3)))
    out += grp(dx, y + 108, pop(t, 0.25 * T), doc, rot=6 * math.sin(t * 7))
    out += grp(540, 585, pop(t, 0.1), pill(540, 585, "もらった次の年", 46, 400))
    return out + grp(690, 950, pop(t, 0.62 * T), pill(690, 950, "110万円以下は申告なし", 44, 560, BLK, YEL))


def d5(t, T):
    out = head(t, "もらう前に", 84, "ルールを知ろう", 110)
    for k, (cx, col) in enumerate(((250, PNK), (540, BLU), (830, GRN))):
        out += gift(cx, 720 - 26 * abs(math.sin(t * 6 + k * 0.8)), 0.72 * pop(t, 0.3 + k * 0.15), 0, col)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["親からお金をもらっても、税金がかかることも。", "でも、1年に110万円までは0円。"], cap="年110万円までは0円", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.25", "pop"), ("f0.5", "tick"), ("f0.5+0.9", "ding")]),
    dict(narr=["これが、ぞうよ税。", "払うのは、もらった人。"], cap="払うのはもらった人", draw=d1,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), (0.3, "pop"), ("f0.2", "swish"), ("f0.2+1.2", "chomp")]),
    dict(narr=["見るのは、1年間にもらった合計。", "110万円をこえた分に、税金がかかります。"], cap="こえた分にだけかかる", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.35+0.3", "tick"), ("f0.62+0.3", "ding")]),
    dict(narr=["必要な生活費や学費は、そのつど使うなら0円。", "貯金や株にまわすと、対象です。"], cap="貯金にまわすと対象", note="※扶養義務者からの通常必要な分",
         draw=d3, sfx=[(0.0, "whoosh"), ("f0.1", "pop"), ("f0.1+0.3", "pop"), ("f0.55", "drop"), ("f0.55+0.3", "pop")]),
    dict(narr=["こえたら、次の年の2月から3月に申告。", "110万円以下なら、不要です。"], cap="翌年2/1〜3/15に申告", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.25", "swish"), ("f0.25+1.0", "pop"), ("f0.62", "ding")]),
    dict(narr=["もらう前に、ルールを知ろう。", "フォローして、お金を学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), (0.6, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v010_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v010_zoyo.mp4")
