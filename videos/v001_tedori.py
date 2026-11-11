"""#001 給料の22%は最初から消えてる — the reference video. Copy this file's shape for new videos."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

NOTE = "※年収450万円・独身の会社員の目安"


def d0(t, T):
    out = head(t, "あなたの給料の22%は", 76, "最初から消えてる", 104)
    g, p = gauge(t, 0.45 * T, 0.78)
    out += grp(540, 655, pop(t, 0.2), g)
    val = int(round(100 - 22 * p))
    shake = 10 * math.sin(t * 40) * (1 - clamp((t - 0.45 * T - 1.0) / 0.5)) if t > 0.45 * T + 1.0 else 0
    return out + grp(540, 860, pop(t, 0.35), txt(540 + shake, 930, f"{val}円", 190, PNK if p >= 1 else BLK))


def d1(t, T):
    out = head(t, "犯人は", 76, "この3匹", 130)
    for k, (cx, col, name) in enumerate(((230, RED, "所得税"), (540, BLU, "住民税"), (850, GRN, "社会保険料"))):
        t0 = 0.3 + k * 0.35
        out += monster(cx, 720 - 14 * abs(math.sin(t * 5 + k)), col, t + k * 0.3, 0.85 * pop(t, t0))
        out += grp(cx, 947, pop(t, t0 + 0.25), pill(cx, 947, name))
    return out


def d2(t, T):
    out = head(t, "いちばん重いのは", 80, "社会保険料", 130, tb=0.5 * T)
    rows = [("所得税", 2, RED, "約2円", 0.06 * T), ("住民税", 5, BLU, "約5円", 0.24 * T), ("社会保険料", 15, GRN, "約15円", 0.6 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 555 + k * 140
        out += grp(250, y + 20, pop(t, t0, 0.3), txt(130, y + 36, lab, 46, BLK, "start"))
        out += hbar(130, y + 52, v * 30 * prog(t, t0 + 0.15, 0.6), col)
        out += grp(130 + v * 30 + 90, y + 84, pop(t, t0 + 0.6, 0.3), txt(130 + v * 30 + 22, y + 102, val, 52, BLK, "start"))
    out += monster(880, 760 - 10 * abs(math.sin(t * 5)), GRN, t, 0.62 * pop(t, 0.5 * T))
    return out + grp(835, 600, pop(t, 0.2), pill(835, 600, "100円あたり", 40, 290))


def d3(t, T):
    out = head(t, "しかも所得税は", 80, "稼ぐほど上がる", 110)
    out += monster(240, 770, RED, t, 0.85 * pop(t, 0.2))
    r = [5, 10, 20, 23, 33, 40, 45]
    return out + vbars(t, r, [f"{v}%" for v in r], step=(0.75 * T - 0.5) / 7)


def d4(t, T):
    out = head(t, "ただしムダじゃない", 80, "みんなのために使う", 92)
    for k, (kind, lab, x, y) in enumerate([("hospital", "病院", 100, 545), ("old", "年金", 560, 545), ("school", "学校", 100, 775), ("road", "道路", 560, 775)]):
        out += grp(x + 210, y + 102, pop(t, 0.42 * T + k * 0.3), card(x, y, 420, 205, icon(kind, x + 30, y + 30) + txt(x + 290, y + 128, lab, 76)))
    return out


def d5(t, T):
    out = head(t, "仕組みを知ってる人が", 76, "得をする", 130)
    for k, (cx, col) in enumerate(((270, RED), (540, BLU), (810, GRN))):
        out += monster(cx, 690 - 24 * abs(math.sin(t * 6 + k * 0.8)), col, t + k * 0.2, 0.62 * pop(t, 0.3 + k * 0.15))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["あなたの給料、22パーセントは最初から消えてます。", "100円もらっても、使えるのは78円。"], cap="100円もらっても78円", note=NOTE, draw=d0,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.45", "drop"), ("f0.45+1.0", "ding")]),
    dict(narr=["犯人は、この3匹。"], cap="給料から引かれる3つ", draw=d1, sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.65, "pop"), (1.0, "pop")]),
    dict(narr=["所得税が約2円、住民税が約5円。", "いちばん大きいのが社会保険料、約15円。"], cap="給料100円あたりの目安", note=NOTE, draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.06", "tick"), ("f0.24", "tick"), ("f0.6", "tick"), ("f0.5", "pop"), ("f0.6+0.6", "chomp")]),
    dict(narr=["しかも所得税は、稼ぐほど税率が上がる。", "5パーセントから、最大45パーセント。"], cap="5%から最大45%", draw=d3, sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.75", "ding")]),
    dict(narr=["ただし、ムダじゃない。", "病院、年金、学校、道路に使われてる。"], cap="ムダに消えてはいない", draw=d4,
         sfx=[(0.0, "whoosh")] + [(f"f0.42+{k*0.3:.2f}", "pop") for k in range(4)]),
    dict(narr=["知ってる人だけが、とくをする。", "フォローして、お金の仕組みを学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.45, "pop"), (0.6, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v001_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v001_tedori.mp4")
