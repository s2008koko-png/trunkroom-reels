"""#027 iDeCoの税金面のしくみ（ルールの説明のみ）— 掛金は全額所得控除・運用益は運用中非課税・上限 月23,000円→令和8年12月から62,000円（企業年金のない会社員）・原則60歳から受給・受取時は公的年金等控除／退職所得控除。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def jar(cx, top, w, h, fill, label="iDeCo", lsize=54):
    """A money jar: body (cx centred, top..top+h), gold level `fill` 0..1, label on the front."""
    x = cx - w / 2
    fh = (h - 20) * clamp(fill)
    out = f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="30" fill="{WHT}" stroke="{BLK}" stroke-width="10"/>'
    if fh > 4:
        out += f'<rect x="{x+10}" y="{top+h-10-fh:.0f}" width="{w-20}" height="{fh:.0f}" rx="20" fill="{GLD}"/>'
    out += f'<rect x="{cx-w*0.3}" y="{top-34}" width="{w*0.6}" height="40" rx="10" fill="{BLK}"/>'
    return out + pill(cx, top + h * 0.5, label, lsize, w - 50, PNK)


def falling(t, cx, top, n=3, r=26, speed=0.9, span=170):
    out = ""
    for k in range(n):
        ph = (t * speed + k / n) % 1.0
        out += grp(0, 0, 1, coin(cx + (k - (n - 1) / 2) * 60, top - span + span * ph, r), op=1 - ph * 0.8)
    return out


def d0(t, T):
    out = head(t, "iDeCoの掛金は", 90, "全額 所得から引ける", 96)
    out += falling(t, 270, 690) + jar(270, 690, 300, 290, 0.25 + 0.6 * prog(t, 0.2, 2.5))
    p = prog(t, 0.45 * T, 1.0)
    out += txt(700, 640, "税金がかかる所得", 44)
    out += f'<rect x="520" y="670" width="400" height="110" rx="16" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="526" y="676" width="{388 - 120 * p:.0f}" height="98" rx="12" fill="{RED}"/>'
    return out + grp(720, 890, pop(t, 0.45 * T + 0.9) * (1 + 0.04 * math.sin(t * 8)), pill(720, 890, "掛金のぶん へる", 48, 440))


def d1(t, T):
    out = head(t, "iDeCoは", 90, "自分でつくる年金", 110)
    for k in range(6):
        t0 = 0.3 + k * 0.28
        q = prog(t, t0, 0.5)
        x, y = 150 + k * 70, 620
        x2, y2 = 760, 700
        if q > 0:
            out += grp(0, 0, 1, coin(x + (x2 - x) * q, y + (y2 - y) * q - 120 * math.sin(math.pi * q), 34), op=1 - q ** 4)
        else:
            out += coin(x, y, 34)
    out += jar(760, 700, 320, 280, 0.15 + 0.12 * sum(prog(t, 0.3 + k * 0.28, 0.5) for k in range(6)))
    return out + grp(330, 850, pop(t, 0.4), pill(330, 850, "毎月 積み立てる", 48, 430))


def d2(t, T):
    out = head(t, "ふえた分も 運用中は", 84, "税金がかからない", 110)
    pts = [(150, 940), (290, 880), (420, 900), (560, 800), (690, 770), (800, 690)]
    p = prog(t, 0.2, 2.0)
    n = len(pts) - 1
    f = p * n
    k = min(int(f), n - 1)
    a, b = pts[k], pts[k + 1]
    tx, ty = a[0] + (b[0] - a[0]) * (f - k), a[1] + (b[1] - a[1]) * (f - k)
    s = " ".join(f"{x},{y}" for x, y in pts[:k + 1]) + f" {tx:.0f},{ty:.0f}"
    out += f'<path d="M130 570 L130 965 L960 965" fill="none" stroke="{BLK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    out += f'<polyline points="{s}" fill="none" stroke="{GRN}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>' + coin(tx, ty, 34)
    # the tax monster bounces off a shield
    bx = 900 - 40 * abs(math.sin(t * 3))
    out += monster(bx, 620, RED, t, 0.42 * pop(t, 0.5), chomp=False)
    out += grp(770, 620, pop(t, 0.7), f'<path d="M740 560 L800 560 L800 630 Q770 690 740 630 Z" fill="{BLU}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>')
    return out + grp(380, 640, pop(t, 0.45 * T), pill(380, 640, "運用益 非課税", 54, 430, PNK))


def d3(t, T):
    out = head(t, "毎月の上限が", 84, "12月から上がる", 120)
    rows = [("いま", 23, BLK, "23,000円", 0.1 * T), ("12月から", 62, PNK, "62,000円", 0.5 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 570 + k * 210
        out += grp(250, y + 30, pop(t, t0, 0.3), txt(130, y + 44, lab, 56, BLK, "start"))
        out += hbar(130, y + 70, v * 8.6 * prog(t, t0 + 0.15, 0.7), col, 90)
        out += grp(130 + v * 8.6 + 140, y + 115, pop(t, t0 + 0.7, 0.3), txt(130 + v * 8.6 + 22, y + 138, val, 60, BLK, "start"))
    return out


def d4(t, T):
    out = head(t, "ただし 受け取りは", 84, "原則60歳から", 130)
    p = prog(t, 0.15 * T, 2.0)
    age = int(round(30 + 30 * p))
    out += jar(280, 600, 300, 250, 0.3 + 0.6 * p, "iDeCo", 50)
    # padlock on the jar: shackle lifts when age reaches 60
    lift = 34 * prog(t, 0.15 * T + 2.0, 0.3)
    out += f'<path d="M240 {900-lift:.0f} L240 {870-lift:.0f} Q280 {820-lift:.0f} 320 {870-lift:.0f} L320 {900-lift:.0f}" fill="none" stroke="{BLK}" stroke-width="14" stroke-linecap="round"/>'
    out += f'<rect x="220" y="895" width="120" height="80" rx="14" fill="{GLD if p >= 1 else BLK}" stroke="{BLK}" stroke-width="8"/>'
    out += txt(700, 760, f"{age}歳", 170, PNK if p >= 1 else BLK)
    return out + grp(700, 890, pop(t, 0.15 * T + 2.1), pill(700, 890, "受け取りスタート", 46, 440))


def d5(t, T):
    out = head(t, "iDeCoは", 90, "老後のための制度", 110)
    b = 10 * abs(math.sin(t * 5))
    out += grp(540, 640, pop(t, 0.2), card(150, 570 - b, 780, 140, txt(540, 664 - b, "掛金は全額 所得から引ける", 56)))
    out += grp(540, 790, pop(t, 0.5), pill(540, 790, "年末調整で申告できる", 42, 520))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["イデコの掛金は、全額が所得から引けます。"], cap="掛金は全額 所得控除", note="※小規模企業共済等掛金控除", draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "tick"), ("f0.45", "drop"), ("f0.45+0.9", "ding")]),
    dict(narr=["イデコは、自分で毎月積み立てる、自分用の年金です。"], cap="自分でつくる年金", note="※個人型確定拠出年金", draw=d1,
         sfx=[(0.0, "whoosh")] + [(0.3 + k * 0.28, "tick") for k in range(6)]),
    dict(narr=["ふえた分にも、運用中は税金がかかりません。"], cap="運用益は運用中 非課税", draw=d2,
         sfx=[(0.0, "whoosh"), (0.2, "swish"), (0.7, "pop"), ("f0.45", "ding")]),
    dict(narr=["毎月の上限は、企業年金がない会社員で2万3000円。", "12月から、6万2000円に上がります。"], cap="毎月の掛金の上限", note="※企業年金のない会社員・令和8年12月から", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.1", "tick"), ("f0.5", "tick"), ("f0.5+0.7", "ding")]),
    dict(narr=["ただし、受け取れるのは原則60歳から。", "受け取るときは、税金の計算の対象です。"], cap="途中で引き出せない", note="※受取時は公的年金等控除・退職所得控除", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.15", "swish"), ("f0.15+2.0", "ding")]),
    dict(narr=["イデコは、老後のための税金のルール。", "フォローして学ぼう。"], cap="フォローして学ぼう", note="※加入するかは自分で決めること", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v027_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v027_ideco.mp4")
