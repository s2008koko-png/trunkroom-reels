"""#017 たばこ税の引上げ — 国のたばこ税を令和9年4月・10年4月・11年4月に1本あたり0.5円ずつ3段階で引上げ（引上げは国税のみ）、
1箱20本なら税額は10円ずつ・合計30円（計算）、加熱式たばこは令和8年4月と10月の2段階で紙巻たばことの税負担差を解消する課税方式の適正化、
防衛力強化に係る財源確保のための税制措置、たばこ税等の税収（国・地方の合計）は概ね2兆円程度で推移。
Sources (fetched 2026-11-16): 財務省 たばこ税等に関する資料（令和8年4月現在） https://www.mof.go.jp/tax_policy/summary/consumption/d09.htm"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

GRY = "#9AA0A6"


def box(cx, cy, s=1.0, rot=0.0):
    """Original plain cigarette box ~200x300 centred at (cx, cy), three sticks poking out. No brand marks."""
    g = ""
    for k, dx in enumerate((-52, 0, 52)):
        g += (f'<rect x="{cx+dx-20}" y="{cy-190-12*k}" width="40" height="120" rx="6" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
              f'<rect x="{cx+dx-20}" y="{cy-190-12*k}" width="40" height="34" rx="6" fill="#E8A657" stroke="{BLK}" stroke-width="6"/>')
    g += (f'<rect x="{cx-100}" y="{cy-110}" width="200" height="260" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
          f'<rect x="{cx-96}" y="{cy-106}" width="192" height="70" rx="10" fill="{GRY}"/>'
          f'<rect x="{cx-60}" y="{cy+10}" width="120" height="90" rx="10" fill="{BLK}"/>' + txt(cx, cy + 76, "20", 60, YEL))
    return grp(cx, cy, s, g, rot=rot)


def up(cx, cy, s=1.0, col=PNK):
    g = f'<polygon points="{cx},{cy-90} {cx+70},{cy-10} {cx+28},{cy-10} {cx+28},{cy+90} {cx-28},{cy+90} {cx-28},{cy-10} {cx-70},{cy-10}" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
    return grp(cx, cy, s, g)


def shield(cx, cy, s=1.0):
    g = (f'<path d="M{cx-100} {cy-100} L{cx+100} {cy-100} L{cx+100} {cy+10} Q{cx+100} {cy+90} {cx} {cy+135} Q{cx-100} {cy+90} {cx-100} {cy+10} Z" fill="{BLU}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         + txt(cx, cy + 22, "防衛", 68, WHT))
    return grp(cx, cy, s, g)


def d0(t, T):
    out = head(t, "たばこの税金", 96, "3年連続で上がる", 110)
    out += box(260, 800, 1.0, rot=3 * math.sin(t * 4))
    for k, cx in enumerate((520, 700, 880)):
        t0 = 0.25 * T + k * 0.4
        out += up(cx, 780 - 26 * k - 12 * abs(math.sin(t * 6 + k)), pop(t, t0))
    return out


def d1(t, T):
    out = head(t, "1本あたり", 90, "0.5円ずつ×3回", 110)
    out += f'<line x1="110" y1="984" x2="970" y2="984" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k, yr in enumerate(("2027年4月", "2028年4月", "2029年4月")):
        t0 = 0.12 * T + k * 0.22 * T
        p = prog(t, t0, 0.4)
        if p <= 0:
            continue
        x, h = 130 + k * 280, (110 + 100 * k) * p
        out += f'<rect x="{x}" y="{980-h:.1f}" width="260" height="{h:.1f}" rx="8" fill="{(BLK, BLK, PNK)[k]}"/>'
        out += grp(x + 130, 950, pop(t, t0 + 0.3, 0.25), txt(x + 130, 962, yr, 38, WHT))
        out += grp(x + 130, 980 - h - 40, pop(t, t0 + 0.3, 0.25), txt(x + 130, 980 - h - 22, "+0.5円", 58, PNK))
    return out


def d2(t, T):
    out = head(t, "1箱20本なら", 90, "税が合計30円ふえる", 96)
    out += box(230, 800, 0.9)
    for k in range(3):
        t0 = 0.15 * T + k * 0.5
        out += grp(470, 610 + k * 100, pop(t, t0), pill(470, 610 + k * 100, "＋10円", 50, 250))
    n = sum(1 for k in range(3) if t >= 0.15 * T + k * 0.5 + 0.2)
    out += txt(805, 800, f"{n * 10}円", 140, PNK if n == 3 else BLK)
    out += grp(815, 900, pop(t, 0.15 * T + 1.3), pill(815, 900, "合計", 46, 200, PNK))
    return out


def d3(t, T):
    out = head(t, "加熱式たばこは", 90, "税の差をなくす見直し", 88)
    base, full = 960, 330
    p1, p2 = prog(t, 0.3 * T, 0.5), prog(t, 0.6 * T, 0.5)
    h2 = full * (0.6 + 0.2 * p1 + 0.2 * p2)
    out += f'<line x1="140" y1="{base+4}" x2="700" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    out += f'<rect x="180" y="{base-full}" width="200" height="{full}" rx="8" fill="{BLK}"/>' + txt(280, base - 30, "紙巻き", 46, WHT)
    out += f'<rect x="460" y="{base-h2:.1f}" width="200" height="{h2:.1f}" rx="8" fill="{PNK}"/>' + txt(560, base - 30, "加熱式", 46, WHT)
    out += f'<line x1="150" y1="{base-full}" x2="700" y2="{base-full}" stroke="{BLK}" stroke-width="5" stroke-dasharray="16 12"/>'
    out += grp(850, 700, pop(t, 0.3 * T), pill(850, 700, "4月", 54, 220))
    out += grp(850, 830, pop(t, 0.6 * T), pill(850, 830, "10月", 54, 220, PNK))
    return out


def d4(t, T):
    out = head(t, "引き上げの目的は", 84, "防衛力の強化", 120)
    out += shield(760, 740, pop(t, 0.2))
    for k in range(3):
        q = ((t - 0.4 - k * 0.45) / 1.35) % 1.0 if t > 0.4 + k * 0.45 else -1
        if q >= 0:
            out += coin(160 + 470 * q, 760 - 110 * math.sin(math.pi * q), 38)
    out += grp(540, 940, pop(t, 0.55 * T), pill(540, 940, "上がるのは国の税だけ", 48, 600))
    return out


def d5(t, T):
    out = head(t, "たばこ税の税収は", 84, "年およそ2兆円", 120)
    for k, cx in enumerate((250, 540, 830)):
        out += box(cx, 730 - 22 * abs(math.sin(t * 6 + k * 0.8)), 0.5 * pop(t, 0.3 + k * 0.15))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["たばこの税金。", "来年から、3年連続で上がります。"], cap="来年から3年連続", note="※国のたばこ税（財務省・令和8年4月現在）", draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.25", "pop"), ("f0.25+0.4", "pop"), ("f0.25+0.8", "pop")]),
    dict(narr=["2027年、28年、29年の4月に、1本あたり0.5円ずつ。"], cap="1本0.5円ずつ×3回", note="※令和9年・10年・11年の各4月", draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.12", "tick"), ("f0.34", "tick"), ("f0.56", "ding")]),
    dict(narr=["1箱20本なら、税金が合計30円ふえる計算です。"], cap="1箱で税が合計30円", note="※1箱20本として計算した税額", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.15", "pop"), ("f0.15+0.5", "pop"), ("f0.15+1.0", "pop"), ("f0.15+1.3", "ding")]),
    dict(narr=["加熱式たばこは、今年の4月と10月に、紙巻きとの税の差をなくす見直しがありました。"], cap="加熱式は今年2段階で", note="※イメージ図・令和8年4月と10月", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.3", "tick"), ("f0.6", "ding")]),
    dict(narr=["目的は、国の防衛力を強くするお金を集めること。", "上がるのは国の税だけ。"], cap="防衛力強化の財源", note="※防衛力強化に係る財源確保のための税制措置", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.55", "pop")]),
    dict(narr=["たばこ税は、国と地方あわせて、1年でおよそ2兆円。", "フォローしてね。"], cap="フォローして学ぼう", note="※税収は概ね2兆円程度で推移（財務省）", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), (0.6, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v017_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v017_tabako.mp4")
