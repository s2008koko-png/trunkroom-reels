"""#048 確定申告をするとワンストップ特例は無効 — ふるさと納税ワンストップ特例は「確定申告の不要な給与所得者等」で
寄附先が5団体以内の人が使える（総務省）。6団体以上は確定申告が必要（総務省）。確定申告を行う場合はワンストップ特例の
申請が無効となり、申請をした分も含めて寄附金控除額を計算する必要がある（国税庁）。寄附金控除は確定申告書に
寄附金の受領証などを添付または提示（国税庁 No.1150・令和8年4月1日現在法令等）。
Sources (fetched 2026-11-27): 総務省 ふるさと納税の流れ / 国税庁 確定申告をすれば税金が還付される方 / 国税庁 No.1150"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

GRY = "#BDBDBD"


def paper(cx, cy, w, h, title="", size=50, sub="", ssize=70):
    """Original sheet of paper centred on (cx, cy) with a folded corner and ruled lines."""
    x, y = cx - w / 2, cy - h / 2
    out = (f'<path d="M{x} {y} H{x+w-50} L{x+w} {y+50} V{y+h} H{x} Z" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<path d="M{x+w-50} {y} V{y+50} H{x+w}" fill="{GRY}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>')
    if title:
        out += txt(cx - 10, y + 40 + size * 0.8, title, size)
    if sub:
        out += txt(cx, cy + ssize * 0.6, sub, ssize, PNK)
    for k in range(2):
        yy = y + h - 40 - k * 38
        out += f'<line x1="{x+40}" y1="{yy}" x2="{x+w-40}" y2="{yy}" stroke="{GRY}" stroke-width="10" stroke-linecap="round"/>'
    return out


def xmark(cx, cy, r):
    out = ""
    for wd, col in ((54, BLK), (34, PNK)):
        out += (f'<line x1="{cx-r}" y1="{cy-r}" x2="{cx+r}" y2="{cy+r}" stroke="{col}" stroke-width="{wd}" stroke-linecap="round"/>'
                f'<line x1="{cx+r}" y1="{cy-r}" x2="{cx-r}" y2="{cy+r}" stroke="{col}" stroke-width="{wd}" stroke-linecap="round"/>')
    return out


def check(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GRN}" stroke="{BLK}" stroke-width="7"/>'
            f'<path d="M{cx-r*0.45:.1f} {cy:.1f} L{cx-r*0.1:.1f} {cy+r*0.38:.1f} L{cx+r*0.5:.1f} {cy-r*0.35:.1f}" fill="none" stroke="{WHT}" stroke-width="{r*0.24:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def hall(cx, cy, col=BLU):
    """Original small town hall ~130x150 centred on (cx, cy)."""
    return (f'<line x1="{cx}" y1="{cy-75}" x2="{cx}" y2="{cy-30}" stroke="{BLK}" stroke-width="7"/>'
            f'<polygon points="{cx},{cy-78} {cx+40},{cy-64} {cx},{cy-50}" fill="{PNK}" stroke="{BLK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<rect x="{cx-60}" y="{cy-15}" width="120" height="90" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
            f'<polygon points="{cx-72},{cy-12} {cx},{cy-48} {cx+72},{cy-12}" fill="{col}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{cx-14}" y="{cy+30}" width="28" height="45" fill="{BLK}"/>'
            f'<rect x="{cx-44}" y="{cy+8}" width="20" height="20" fill="{col}"/><rect x="{cx+24}" y="{cy+8}" width="20" height="20" fill="{col}"/>')


def d0(t, T):
    out = head(t, "確定申告をすると", 96, "ワンストップは無効", 96)
    t0 = 0.5 * T
    hit = t >= t0
    rot = 3 * math.sin(t * 3) if not hit else 6 * math.sin((t - t0) * 30) * (1 - clamp((t - t0) / 0.5))
    out += grp(540, 740, 1, paper(540, 740, 420, 370, "ワンストップ", 52, "申請書", 96), rot=rot)
    if hit:
        s = 1 + 1.6 * (1 - prog(t, t0, 0.25))
        out += grp(540, 740, s, xmark(540, 740, 130))
        out += grp(540, 958, pop(t, t0 + 0.3), pill(540, 958, "無効", 46, 260, PNK))
    return out


def d1(t, T):
    out = head(t, "ワンストップ特例は", 90, "申請書だけでOK", 104)
    for k, cx in enumerate((170, 355, 540, 725, 910)):
        t0 = 0.3 * T + k * 0.28
        cy = 650 - 10 * abs(math.sin(t * 5 + k))
        out += grp(cx, 650, pop(t, t0), hall(cx, cy, (BLU, GRN, RED, BLU, GRN)[k]))
        out += grp(cx, 770, pop(t, t0 + 0.1), f'<circle cx="{cx}" cy="770" r="30" fill="{BLK}"/>' + txt(cx, 785, str(k + 1), 42, WHT))
    out += grp(540, 870, pop(t, 0.3 * T + 1.5), pill(540, 870, "5団体以内", 50, 380, PNK))
    out += grp(540, 968, pop(t, 0.78 * T), pill(540, 968, "申請書を出すだけ", 42, 460))
    return out


def d2(t, T):
    out = head(t, "でも医療費控除などで", 84, "確定申告をすると…", 96)
    out += grp(290, 700, pop(t, 0.15), card(100, 560, 380, 290, icon("hospital", 225, 580) + txt(290, 815, "医療費控除", 54)))
    out += grp(540, 705, pop(t, 0.25 * T), txt(540, 730, "→", 84))
    sx = 400 * (1 - prog(t, 0.3 * T, 0.5))
    if t > 0.3 * T:
        out += paper(790 + sx, 705, 340, 290, "確定申告書", 50, "提出", 70)
    t0 = 0.62 * T
    op = 1 - 0.55 * prog(t, t0, 0.4)
    out += grp(540, 945, pop(t, 0.2), pill(540, 945, "ワンストップ申請書", 46, 540), op=op)
    if t >= t0:
        out += grp(540, 945, 1 + 1.6 * (1 - prog(t, t0, 0.25)), xmark(540, 945, 52))
    return out


def d3(t, T):
    out = head(t, "ふるさと納税の分も", 90, "申告書に書く", 120)
    out += grp(540, 765, pop(t, 0.15), paper(480, 765, 600, 420, "確定申告書", 54))
    out += grp(480, 730, pop(t, 0.2 * T), txt(250, 750, "医療費控除", 54, BLK, "start") + check(700, 732, 34))
    t0 = 0.42 * T
    w = 520 * prog(t, t0, 0.5)
    if w > 0:
        out += f'<rect x="220" y="790" width="{w:.1f}" height="92" rx="12" fill="{PNK}"/>'
    out += grp(480, 836, pop(t, t0 + 0.3), txt(250, 856, "ふるさと納税", 56, WHT, "start") + check(700, 836, 34))
    p = prog(t, 0.68 * T, 0.5)
    if p > 0:
        rc = card(770, 850, 210, 130, txt(875, 935, "受領証", 52))
        out += grp(875, 915, 1, rc, rot=8 + 40 * (1 - p), op=p).replace("translate(875.0,915.0)", f"translate({875 + 300 * (1 - p):.1f},915.0)", 1)
    return out


def d4(t, T):
    out = head(t, "確定申告をしない人は", 84, "そのままでOK", 110)
    by = 730 - 12 * abs(math.sin(t * 5))
    out += grp(270, 730, pop(t, 0.15), paper(270, by, 290, 300, "申請書", 56) + check(270, by + 30, 62))
    out += grp(270, 950, pop(t, 0.4), pill(270, 950, "そのまま", 46, 300, GRN))
    t0 = 0.5 * T
    for k in range(6):
        cx, cy = 600 + (k % 3) * 135, 620 + (k // 3) * 150
        out += grp(cx, cy, 0.72 * pop(t, t0 + k * 0.12), hall(cx, cy, RED if k == 5 else BLU))
    out += grp(735, 950, pop(t, t0 + 0.9), pill(735, 950, "6団体以上は確定申告", 38, 470))
    return out


def d5(t, T):
    out = head(t, "申告するなら", 100, "寄付も忘れずに", 110)
    for k, cx in enumerate((270, 540, 810)):
        cy = 700 - 22 * abs(math.sin(t * 6 + k * 0.8))
        out += grp(cx, 700, pop(t, 0.2 + k * 0.15), paper(cx, cy, 190, 220) + check(cx, cy - 20, 50))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["確定申告をすると、ふるさと納税のワンストップ特例は無効になります。"], cap="申請が無効になる",
         note="※ふるさと納税ワンストップ特例の申請", draw=d0, sfx=[(0.0, "whoosh"), ("f0.5", "chomp"), ("f0.5+0.3", "ding")]),
    dict(narr=["これは、確定申告のいらない会社員などが、5団体以内で使える制度。"], cap="5団体以内なら申請書だけ",
         note="※確定申告の不要な給与所得者等が対象", draw=d1, csize=58,
         sfx=[(0.0, "whoosh")] + [(f"f0.3+{k*0.28:.2f}", "pop") for k in range(5)] + [("f0.78", "ding")]),
    dict(narr=["でも、医療費控除などで確定申告をすると、申請書は使えません。"], cap="申請書は使えなくなる",
         draw=d2, sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.3", "swish"), ("f0.62", "chomp")]),
    dict(narr=["そのときは、ふるさと納税の分も申告書に書きます。"], cap="寄付の分も申告書に",
         note="※寄附金控除として申告する", draw=d3, sfx=[(0.0, "whoosh"), ("f0.2", "tick"), ("f0.42", "tick"), ("f0.68", "swish")]),
    dict(narr=["確定申告をしない人は、そのままで大丈夫。", "6団体以上なら、確定申告が必要です。"], cap="申告しない人はそのまま",
         draw=d4, sfx=[(0.0, "whoosh"), (0.15, "pop"), ("f0.5", "pop"), ("f0.5+0.9", "ding")]),
    dict(narr=["申告するなら、寄付も忘れずに。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v048_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v048_onestop.mp4")
