"""#049 労災保険 — 業務災害・通勤災害による傷病が対象。労災指定医療機関等で原則として無償で治療（療養の給付）。
休業（補償）等給付は、療養のため働けず賃金を受けていないとき、休業4日目から1日につき給付基礎日額の60%＋
休業特別支給金20%＝80%（金額等は令和8年4月1日現在）。休業の初日から3日目までは労災保険から支給されず、
業務災害の場合は事業主が休業補償（1日につき平均賃金の60%）。費用は原則として事業主の負担する保険料（全額事業主負担）。
Sources (fetched 2026-11-27): 厚生労働省 労災保険給付の支給事由と内容 / 請求(申請)のできる保険給付等 / 労災保険制度の概要"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

GRY, SKIN, HEL = "#BDBDBD", "#FFD9B0", "#3D8BFF"


def worker(cx, cy, s=1.0, hurt=True):
    """Original worker with a helmet (~220x300 at s=1) centred on (cx, cy)."""
    w = (f'<path d="M{cx-95} {cy+150} V{cy+70} Q{cx-95} {cy+20} {cx} {cy+16} Q{cx+95} {cy+20} {cx+95} {cy+70} V{cy+150} Z" fill="{GRN}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<circle cx="{cx}" cy="{cy-40}" r="78" fill="{SKIN}" stroke="{BLK}" stroke-width="8"/>'
         f'<path d="M{cx-88} {cy-62} Q{cx-84} {cy-150} {cx} {cy-150} Q{cx+84} {cy-150} {cx+88} {cy-62} Z" fill="{HEL}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<rect x="{cx-104}" y="{cy-74}" width="208" height="20" rx="10" fill="{HEL}" stroke="{BLK}" stroke-width="7"/>'
         f'<circle cx="{cx-28}" cy="{cy-28}" r="8" fill="{BLK}"/><circle cx="{cx+28}" cy="{cy-28}" r="8" fill="{BLK}"/>')
    if hurt:
        w += (f'<path d="M{cx-24} {cy+12} Q{cx} {cy-2} {cx+24} {cy+12}" fill="none" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>'
              f'<g transform="rotate(-25 {cx+48} {cy-2})"><rect x="{cx+22}" y="{cy-14}" width="52" height="24" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="5"/>'
              f'<line x1="{cx+48}" y1="{cy-10}" x2="{cx+48}" y2="{cy+6}" stroke="{PNK}" stroke-width="5"/></g>')
    else:
        w += f'<path d="M{cx-24} {cy} Q{cx} {cy+20} {cx+24} {cy}" fill="none" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>'
    return grp(cx, cy, s, w)


def office(cx, cy, label="会社"):
    """Original office building ~200x280 centred on (cx, cy)."""
    out = f'<rect x="{cx-100}" y="{cy-140}" width="200" height="280" rx="10" fill="#555" stroke="{BLK}" stroke-width="8"/>'
    for r in range(3):
        for c in range(3):
            out += f'<rect x="{cx-72+c*54}" y="{cy-112+r*52}" width="36" height="32" fill="{YEL}"/>'
    out += f'<rect x="{cx-70}" y="{cy+60}" width="140" height="62" rx="8" fill="{WHT}"/>' + txt(cx, cy + 108, label, 46)
    return out


def daybox(x, y, w, label, col, fg=BLK):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{w}" rx="16" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="12" fill="{BLK}"/>' + txt(x + w / 2, y + w * 0.5 + 40, label, 44, fg))


def d0(t, T):
    out = head(t, "仕事中のケガ", 110, "治療費は原則0円", 104)
    out += worker(260, 800 - 8 * abs(math.sin(t * 5)), 0.95)
    out += card(520, 570, 420, 410, icon("hospital", 665, 590))
    pulse = 1 if t < 0.4 else 1 + 0.06 * math.sin(t * 7)
    out += grp(730, 870, pulse, txt(730, 930, "0円", 170, PNK))
    return out


def d1(t, T):
    out = head(t, "通勤中のケガも", 100, "対象になる", 130)
    out += grp(185, 660, pop(t, 0.15), icon("house", 120, 590))
    out += grp(850, 700, pop(t, 0.25), office(850, 700))
    out += f'<line x1="270" y1="800" x2="730" y2="800" stroke="{BLK}" stroke-width="10" stroke-dasharray="26 22" stroke-linecap="round"/>'
    x = 300 + 400 * (0.5 - 0.5 * math.cos(t * 1.6))
    out += worker(x, 700 - 10 * abs(math.sin(t * 9)), 0.42, hurt=False)
    out += grp(850, 925, pop(t, 0.5), pill(850, 925, "仕事中", 46, 250))
    out += grp(480, 925, pop(t, 0.45 * T), pill(480, 925, "通勤中", 46, 250, PNK))
    return out


def d2(t, T):
    out = head(t, "休んだら4日目から", 90, "日額の80%", 130)
    for k in range(4):
        x, t0 = 135 + k * 210, 0.1 * T + k * 0.3
        last = k == 3
        s = pop(t, t0) * ((1 + 0.06 * math.sin(t * 8)) if last and t > t0 + 0.4 else 1)
        out += grp(x + 90, 640, s, daybox(x, 550, 180, f"{k+1}日目", GLD if last else GRY, PNK if last else BLK))
    t1 = 0.5 * T
    out += hbar(130, 790, 480 * prog(t, t1, 0.5), BLU, 100)
    out += grp(370, 840, pop(t, t1 + 0.4), txt(370, 862, "60%", 60, WHT))
    out += hbar(610, 790, 160 * prog(t, t1 + 0.6, 0.4), PNK, 100)
    out += grp(690, 840, pop(t, t1 + 0.9), txt(690, 860, "20%", 54, WHT))
    out += grp(885, 840, pop(t, t1 + 1.2), txt(885, 866, "80%", 76, PNK))
    out += grp(370, 950, pop(t, t1 + 0.4), txt(370, 962, "保険給付", 40))
    out += grp(690, 950, pop(t, t1 + 0.9), txt(690, 962, "特別支給金", 40))
    return out


def d3(t, T):
    out = head(t, "最初の3日間は", 100, "会社が補償する", 110)
    out += grp(850, 700, pop(t, 0.15), office(850, 700))
    for k in range(3):
        x = 110 + k * 190
        out += grp(x + 80, 680, pop(t, 0.2 + k * 0.12), daybox(x, 600, 160, f"{k+1}日目", GRY))
        t0 = 0.45 * T + k * 0.35
        p = prog(t, t0, 0.5)
        if p > 0:
            cx = 750 + (x + 80 - 750) * p
            cy = 640 - 130 * math.sin(math.pi * p) + (590 - 640) * p
            out += coin(cx, cy, 40)
    out += grp(380, 925, pop(t, 0.45 * T + 1.2), pill(380, 925, "平均賃金の60%", 48, 480, PNK))
    return out


def d4(t, T):
    out = head(t, "保険料は", 110, "全額 会社が払う", 104)
    out += grp(230, 700, pop(t, 0.15), office(230, 700))
    box = (card(560, 660, 380, 220, txt(750, 800, "労災保険", 70))
           + f'<rect x="670" y="648" width="160" height="24" rx="12" fill="{BLK}"/>')
    out += grp(750, 770, pop(t, 0.25), box)
    for k in range(3):
        ph = (t * 0.7 + k / 3) % 1
        if t > 0.5:
            cx = 340 + (750 - 340) * ph
            cy = 640 - 110 * math.sin(math.pi * ph) + 10 * ph
            out += grp(cx, cy, 1, coin(cx, cy, 36), op=clamp((1 - ph) * 5))
    out += grp(540, 950, pop(t, 0.55 * T), pill(540, 950, "働く人の負担は0円", 46, 520, PNK))
    return out


def d5(t, T):
    out = head(t, "仕事や通勤のケガは", 90, "労災保険を確認", 110)
    out += worker(540, 700 - 16 * abs(math.sin(t * 6)), 0.78 * pop(t, 0.2), hurt=False)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["仕事中のケガは、労災保険で、原則無料で治療できます。"], cap="労災保険で原則無料",
         note="※労災指定医療機関等で治療を受ける場合", draw=d0, sfx=[(0.0, "whoosh"), (0.4, "pop"), ("f0.5", "ding")]),
    dict(narr=["仕事中だけでなく、通勤中のケガも対象です。"], cap="仕事中も通勤中も対象", draw=d1,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), (0.25, "pop"), ("f0.45", "ding")]),
    dict(narr=["ケガで働けず給料が出ないときは、4日目から給付。", "もとになる日額の80パーセントです。"], cap="4日目から80%",
         note="※給付基礎日額の60%＋特別支給金20%", draw=d2,
         sfx=[(0.0, "whoosh")] + [(f"f0.1+{k*0.3:.2f}", "tick") for k in range(4)] + [("f0.5", "swish"), ("f0.5+1.2", "ding")]),
    dict(narr=["最初の3日間は、労災保険から出ません。", "仕事中のケガなら、会社が平均賃金の60パーセントを補償。"], cap="3日間は会社が60%",
         note="※業務災害（仕事中のケガなど）の場合", draw=d3, sfx=[(0.0, "whoosh"), (0.15, "pop")] + [(f"f0.45+{k*0.35:.2f}", "tick") for k in range(3)] + [("f0.45+1.2", "ding")]),
    dict(narr=["保険料は、全額、会社の負担です。", "給料からは引かれません。"], cap="保険料は全額会社負担", draw=d4,
         sfx=[(0.0, "whoosh"), (0.15, "pop"), (0.25, "pop"), ("f0.55", "ding")]),
    dict(narr=["仕事や通勤のケガは、労災保険。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v049_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v049_rosai.mp4")
