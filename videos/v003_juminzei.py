"""#003 住民税は後払い — 辞めた次の年に請求が来る理由 (source: 総務省 個人住民税)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def envelope(cx, cy):
    x, y, w, h = cx - 230, cy - 150, 460, 300
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
            f'<polyline points="{x},{y+6} {cx},{cy+10} {x+w},{y+6}" fill="none" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
            + pill(cx, cy + 85, "納税通知書", 50, 330, PNK))


def bin_icon(x, y):
    return (f'<rect x="{x+25}" y="{y+40}" width="80" height="100" rx="8" fill="{BLU}" stroke="{BLK}" stroke-width="7"/>'
            f'<rect x="{x+12}" y="{y+18}" width="106" height="24" rx="8" fill="{BLU}" stroke="{BLK}" stroke-width="7"/>'
            f'<line x1="{x+50}" y1="{y+60}" x2="{x+50}" y2="{y+122}" stroke="{BLK}" stroke-width="6"/><line x1="{x+80}" y1="{y+60}" x2="{x+80}" y2="{y+122}" stroke="{BLK}" stroke-width="6"/>')


def tree_icon(x, y):
    return (f'<rect x="{x+54}" y="{y+84}" width="22" height="56" fill="#8B5A2B" stroke="{BLK}" stroke-width="6"/>'
            f'<circle cx="{x+65}" cy="{y+56}" r="52" fill="{GRN}" stroke="{BLK}" stroke-width="7"/>')


def d0(t, T):
    out = head(t, "会社を辞めた次の年", 80, "税金の請求が来る", 104)
    drop = (1 - prog(t, 0.2, 0.5)) * -300
    out += grp(400, 760 + drop, 1 if t > 0.2 else 0, envelope(400, 760 + drop), rot=4 * math.sin(t * 5))
    out += monster(850, 740 - 16 * abs(math.sin(t * 6)), BLU, t, 0.7 * pop(t, 0.62 * T))
    out += grp(850, 930, pop(t, 0.62 * T + 0.25), pill(850, 930, "住民税", 48, 240))
    return out


def d1(t, T):
    out = head(t, "住民税は", 84, "去年の分を今年払う", 96)
    L = card(110, 560, 360, 300, txt(290, 640, "去年", 64) + coin(210, 740) + coin(290, 740) + coin(370, 740) + txt(290, 840, "稼ぐ", 46))
    R = card(610, 560, 360, 300, txt(790, 640, "今年", 64) + txt(790, 840, "払う", 46, PNK))
    out += grp(290, 710, pop(t, 0.2), L) + grp(790, 710, pop(t, 0.45), R)
    out += grp(540, 710, pop(t, 0.7), txt(540, 740, "→", 110))
    p = prog(t, 0.4 * T, 0.8)
    if p > 0:
        x = 370 + 420 * p
        out += coin(x, 740 - 110 * math.sin(math.pi * p), col=BLU, fg=WHT)
    out += grp(540, 950, pop(t, 0.68 * T), pill(540, 950, "つまり 後払い", 60, 520, PNK))
    return out


def d2(t, T):
    out = head(t, "金額は去年の所得の", 80, "約10%", 150)
    tf = 0.3 * T
    for k in range(10):
        cx, cy = 220 + (k % 5) * 160, 610 + (k // 5) * 130
        s = pop(t, 0.3 + k * 0.06, 0.25)
        if k == 9:
            p = prog(t, tf, 0.7)
            x, y = cx + 60 * p, cy - 120 * math.sin(math.pi * p) + 40 * p
            out += grp(x, y, s * (1 - 0.3 * p), coin(x, y, col=BLU if t > tf - 0.2 else GLD, fg=WHT if t > tf - 0.2 else BLK))
        else:
            out += grp(cx, cy, s, coin(cx, cy))
    out += grp(540, 930, pop(t, 0.6 * T), pill(540, 930, "＋ 年5,000円", 70, 600, BLU))
    return out


def d3(t, T):
    out = head(t, "会社員は毎月の給料から", 70, "6月〜次の5月", 110)
    months = [6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5]
    step = (0.7 * T) / 12
    for k, m in enumerate(months):
        x, y = 115 + (k % 6) * 144, 580 + (k // 6) * 190
        t0 = 0.3 + k * step
        on = t > t0 + 0.15
        box = (f'<rect x="{x}" y="{y}" width="130" height="160" rx="14" fill="{BLU if on else WHT}" stroke="{BLK}" stroke-width="7"/>'
               + txt(x + 65, y + 100, f"{m}月", 46, WHT if on else BLK))
        out += grp(x + 65, y + 80, pop(t, t0, 0.25), box)
    return out


def d4(t, T):
    out = head(t, "住民税は", 84, "町の会費みたいなもの", 88)
    items = [(bin_icon, "ゴミ収集", 100, 545), (lambda x, y: icon("school", x, y), "学校", 560, 545),
             (lambda x, y: icon("road", x, y), "道路", 100, 775), (tree_icon, "公園", 560, 775)]
    for k, (fn, lab, x, y) in enumerate(items):
        out += grp(x + 210, y + 102, pop(t, 0.4 * T + k * 0.3), card(x, y, 420, 205, fn(x + 30, y + 30) + txt(x + 290, y + 124, lab, 56)))
    return out


def d5(t, T):
    out = head(t, "辞める前に", 84, "住民税ぶんを残そう", 96)
    out += grp(300, 700, pop(t, 0.3), card(150, 570, 300, 260, icon("wallet", 235, 600) + txt(300, 800, "とっておく", 46)))
    out += monster(760, 690 - 20 * abs(math.sin(t * 6)), BLU, t, 0.7 * pop(t, 0.5))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["会社を辞めた次の年、収入がなくても、税金の請求が来ます。", "犯人は、住民税。"], cap="犯人は住民税", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "drop"), ("f0.62", "pop"), ("f0.62+0.3", "chomp")]),
    dict(narr=["住民税は、去年の稼ぎに対して、今年払う。", "つまり、後払い。"], cap="住民税は後払い", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.45, "pop"), ("f0.4", "swish"), ("f0.68", "ding")]),
    dict(narr=["金額は、去年の所得の約10パーセント。", "プラス、年に5000円。"], cap="所得の約10%＋年5,000円", csize=58, note="※均等割4,000円＋森林環境税1,000円", draw=d2,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.3", "swish"), ("f0.6", "ding")]),
    dict(narr=["会社員は、6月から次の年の5月まで、毎月の給料から引かれます。"], cap="毎月の給料から天引き", draw=d3,
         sfx=[(0.0, "whoosh")] + [(f"f{0.7*k/12:.3f}+0.3", "tick") for k in range(12)]),
    dict(narr=["住民税は、住んでいる町の会費のようなもの。", "ゴミ収集や学校、道路に使われます。"], cap="住んでいる町のために使う", draw=d4,
         sfx=[(0.0, "whoosh")] + [(f"f0.4+{k*0.3:.2f}", "pop") for k in range(4)]),
    dict(narr=["辞める前に、住民税のぶんを残しておこう。", "フォローして、お金の仕組みを学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v003_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v003_juminzei.mp4")
