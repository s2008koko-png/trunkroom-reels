"""#052 高額療養費制度 — 1か月の医療費の自己負担には上限がある（70歳未満・令和8年8月〜令和9年7月の表）。
月の上限：住民税非課税 36,900円／〜年収約370万円 61,500円／約370〜約770万円 85,800円＋(医療費−286,000円)×1%／
約770〜約1,160万円 179,100円＋(医療費−597,000円)×1%／約1,160万円〜 270,300円＋(医療費−901,000円)×1%。
例：医療費100万円（窓口負担30万円）→ 85,800＋(1,000,000−286,000)×1% ＝ 92,940円（差額207,060円は高額療養費）。
令和8年8月から「年間上限」を新たに導入（約370〜約770万円は年53万円）。
令和9年8月〜は所得区分を細分化する表が示されている（約370〜約510万円 85,800円／約510〜約650万円 98,100円／約650〜約770万円 110,400円、いずれも＋1%部分あり）。
Sources (fetched 2026-11-28): 厚生労働省 高額療養費制度の概要 https://www.mhlw.go.jp/content/001729632.pdf /
高額療養費制度の見直しについて https://www.mhlw.go.jp/content/001726232.pdf"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

GRY = "#BDBDBD"
NOTE = "※70歳未満・年収約370万〜約770万円の例"


def plus(cx, cy, r=60, col=PNK):
    """Original medical cross in a white circle."""
    a = r * 0.3
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
            f'<rect x="{cx-a:.1f}" y="{cy-r*0.62:.1f}" width="{2*a:.1f}" height="{r*1.24:.1f}" fill="{col}"/>'
            f'<rect x="{cx-r*0.62:.1f}" y="{cy-a:.1f}" width="{r*1.24:.1f}" height="{2*a:.1f}" fill="{col}"/>')


def d0(t, T):
    out = head(t, "医療費100万円でも", 90, "払うのは約9万円", 110)
    t0 = 0.45 * T
    p = prog(t, t0, 1.0)
    val = int(round(300000 - 207060 * p))
    out += grp(210, 640, pop(t, 0.15), icon("hospital", 145, 570))
    out += grp(640, 640, pop(t, 0.25), pill(640, 640, "医療費 100万円", 54, 520))
    out += card(120, 740, 840, 230, txt(250, 880, "払う額", 50, BLK) + txt(900, 900, f"{val:,}円", 104, PNK if p >= 1 else BLK, "end"))
    return out


def d1(t, T):
    out = head(t, "上限をこえた分は", 100, "健康保険が払う", 120)
    out += grp(540, 590, pop(t, 0.15), txt(540, 606, "窓口での3割負担 30万円", 50))
    W_ = 820
    a = W_ * 92940 / 300000
    out += f'<rect x="130" y="650" width="{W_}" height="140" rx="12" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
    w = (W_ - a) * prog(t, 0.35 * T, 0.9)
    if w > 8:
        out += f'<rect x="{130+W_-w:.1f}" y="654" width="{w-4:.1f}" height="132" rx="8" fill="{GRN}"/>'
        out += f'<line x1="{130+W_-w:.1f}" y1="650" x2="{130+W_-w:.1f}" y2="790" stroke="{BLK}" stroke-width="6"/>'
    out += grp(130 + a / 2, 720, pop(t, 0.2), txt(130 + a / 2, 738, "自分", 52, WHT))
    out += grp(130 + a + (W_ - a) / 2, 720, pop(t, 0.35 * T + 0.7), txt(130 + a + (W_ - a) / 2, 740, "健康保険から", 58, WHT))
    out += grp(250, 870, pop(t, 0.35 * T + 0.2), txt(130, 886, "92,940円", 56, PNK, "start"))
    out += grp(760, 870, pop(t, 0.35 * T + 0.9), txt(950, 886, "207,060円", 56, "#168A55", "end"))
    out += grp(540, 960, pop(t, 0.7 * T), pill(540, 960, "高額療養費制度", 50, 460))
    return out


def d2(t, T):
    out = head(t, "月の上限は", 100, "年収で決まる", 130)
    rows = [("住民税非課税", 36900, "36,900円"), ("〜約370万円", 61500, "61,500円"), ("約370〜770万円", 85800, "85,800円〜"),
            ("約770〜1,160万円", 179100, "179,100円〜"), ("約1,160万円〜", 270300, "270,300円〜")]
    for k, (lab, v, s) in enumerate(rows):
        y, t0 = 545 + k * 92, 0.1 * T + k * 0.13 * T
        out += grp(250, y + 35, pop(t, t0, 0.3), txt(410, y + 50, lab, 38, BLK, "end"))
        w = v / 270300 * 270
        out += hbar(430, y + 8, w * prog(t, t0 + 0.1, 0.5), PNK if k == 2 else BLK, 58)
        out += grp(430 + w + 100, y + 35, pop(t, t0 + 0.45, 0.3), txt(430 + w + 16, y + 52, s, 40, PNK if k == 2 else BLK, "start"))
    return out


def d3(t, T):
    out = head(t, "2026年8月から", 100, "年間の上限も", 130)
    out += grp(300, 600, pop(t, 0.15), txt(130, 618, "1年間に払った合計", 50, BLK, "start"))
    t0 = 0.25 * T
    p = clamp((t - t0) / (0.4 * T))
    w = 620 * (1 - (1 - p) ** 2)
    hit = p >= 1
    sh = 8 * math.sin(t * 45) * (1 - clamp((t - t0 - 0.4 * T) / 0.4)) if hit else 0
    out += f'<rect x="130" y="660" width="820" height="130" rx="12" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    if w > 8:
        out += f'<rect x="134" y="664" width="{w-4:.1f}" height="122" rx="8" fill="{GLD}"/>'
        for k in range(1, int(w // 62) + 1):
            out += f'<line x1="{134+k*62}" y1="664" x2="{134+k*62}" y2="786" stroke="{BLK}" stroke-width="3" opacity="0.35"/>'
    out += f'<rect x="{750+sh:.1f}" y="630" width="26" height="200" rx="6" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>'
    out += grp(840, 600, pop(t, 0.2), txt(840, 618, "上限", 50, PNK))
    out += grp(540, 955, pop(t, t0 + 0.4 * T), pill(540, 955, "この年収なら 年53万円", 50, 620, PNK))
    return out


def d4(t, T):
    out = head(t, "2027年8月に", 100, "また見直し予定", 120)
    rows = [("約370〜510万円", 85800), ("約510〜650万円", 98100), ("約650〜770万円", 110400)]
    t0 = 0.4 * T
    p = prog(t, t0, 0.8)
    out += grp(540, 580, pop(t, 0.15), pill(540, 580, "年収" + ("　2027年8月〜" if p > 0.5 else "　いま"), 46, 520, PNK if p > 0.5 else BLK))
    for k, (lab, v) in enumerate(rows):
        y = 650 + k * 115
        out += grp(260, y + 40, pop(t, 0.15 + k * 0.12, 0.3), txt(425, y + 58, lab, 40, BLK, "end"))
        cur = 85800 + (v - 85800) * p
        w = cur / 110400 * 270
        up = v > 85800 and p > 0.05
        out += hbar(445, y + 10, w * prog(t, 0.25 + k * 0.12, 0.5), PNK if up else BLK, 66)
        out += grp(445 + w + 110, y + 44, pop(t, 0.6 + k * 0.12, 0.3), txt(445 + w + 16, y + 60, f"{int(round(cur/100)*100):,}円", 44, PNK if up else BLK, "start"))
    return out


def d5(t, T):
    out = head(t, "医療費には", 100, "月の上限がある", 120)
    for k, cx in enumerate((270, 540, 810)):
        cy = 700 - 34 * abs(math.sin(t * 6 + k * 0.9))
        out += grp(cx, cy, pop(t, 0.2 + k * 0.15), plus(cx, cy, 82, (PNK, GRN, BLU)[k]))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["医療費が100万円かかっても、払うのは月およそ9万円。"], cap="1か月の上限がある", note=NOTE, draw=d0,
         sfx=[(0.0, "whoosh"), ("f0.45", "drop"), ("f0.45+1.0", "ding")]),
    dict(narr=["これが高額療養費制度。", "月の上限をこえた分は、健康保険が出します。"], cap="こえた分は保険から", note=NOTE, draw=d1,
         sfx=[(0.0, "whoosh"), ("f0.35", "swish"), ("f0.7", "ding")]),
    dict(narr=["上限は、年収で変わります。", "年収が低いほど、上限も低くなります。"], cap="年収ごとの月の上限",
         note="※70歳未満。〜は医療費により加算あり", draw=d2, sfx=[(0.0, "whoosh")] + [(f"f{0.1+k*0.13:.2f}", "tick") for k in range(5)]),
    dict(narr=["2026年8月からは、1年間の上限もできました。", "この年収なら、ねん53万円です。"], cap="年間上限は53万円", note=NOTE, draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.25", "swish"), ("f0.65", "pop"), ("f0.65+0.1", "ding")]),
    dict(narr=["ただし、2027年8月に、また見直しの予定。", "年収によっては、月の上限が上がります。"], cap="年収により上限が上がる",
         note="※厚労省資料の令和9年8月〜の表・基本額", draw=d4, csize=58, sfx=[(0.0, "whoosh"), ("f0.4", "swish"), ("f0.4+0.8", "pop")]),
    dict(narr=["医療費には、月の上限がある。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v052_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v052_kogaku.mp4")
