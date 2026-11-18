"""#023 失業したときの基本手当（雇用保険）— 賃金日額の約50〜80%・2年間で12か月以上・90〜360日・自己都合は7日＋原則1か月。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def d0(t, T):
    out = head(t, "会社を辞めたら", 90, "給料の5〜8割もらえる", 84)
    # an umbrella (safety net) with coins dropping under it
    out += f'<path d="M300 760 Q540 480 780 760 Z" fill="{GRN}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
    out += f'<path d="M540 760 L540 930 Q540 975 495 975" fill="none" stroke="{BLK}" stroke-width="12" stroke-linecap="round"/>'
    for k in range(5):
        ph = (t * 0.7 + k * 0.2) % 1.0
        out += grp(0, 0, 1, coin(360 + k * 90, 780 + 190 * ph, 30), op=1 - ph ** 3)
    out += grp(170, 700, pop(t, 0.3), pill(170, 700, "5割", 60, 200, WHT, BLK))
    return out + grp(910, 700, pop(t, 0.5), pill(910, 700, "8割", 60, 200, PNK))


def d1(t, T):
    out = head(t, "条件は2年間で", 90, "12か月以上", 130)
    for k in range(24):
        x, y = 126 + (k % 12) * 70, 640 + (k // 12) * 110
        on = k >= 12 and t > 0.3 * T + (k - 12) * 0.12
        out += grp(x + 30, y + 40, pop(t, 0.1 + k * 0.02, 0.2),
                   f'<rect x="{x}" y="{y}" width="60" height="80" rx="10" fill="{GRN if on else WHT}" stroke="{BLK}" stroke-width="6"/>')
    out += grp(540, 590, pop(t, 0.2), txt(540, 605, "辞める前の24か月", 44))
    n = int(clamp((t - 0.3 * T) / 0.12, 0, 12))
    return out + grp(540, 930, pop(t, 0.3 * T), pill(540, 930, f"雇用保険に {n}か月", 50, 520, BLK, YEL))


def d2(t, T):
    out = head(t, "給料が低い人ほど", 84, "割合は高い", 130)
    rows = [("給料が低い人", 80, PNK, "約80%", 0.15 * T), ("給料が高い人", 50, BLU, "約50%", 0.5 * T)]
    for k, (lab, v, col, val, t0) in enumerate(rows):
        y = 560 + k * 210
        out += grp(300, y + 30, pop(t, t0, 0.3), txt(130, y + 44, lab, 50, BLK, "start"))
        out += f'<rect x="130" y="{y+66}" width="600" height="90" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
        out += hbar(130, y + 66, v * 6 * prog(t, t0 + 0.15, 0.7), col, 90)
        out += grp(850, y + 111, pop(t, t0 + 0.7, 0.3), txt(760, y + 132, val, 62, BLK, "start"))
    return out


def d3(t, T):
    out = head(t, "もらえる日数は", 90, "90日〜360日", 124)
    p = prog(t, 0.2 * T, 1.6)
    n = int(round(90 + 270 * p))
    cx, cy, r = 300, 770, 190
    a = -math.pi / 2 + 2 * math.pi * n / 360
    out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WHT}" stroke="{BLK}" stroke-width="10"/>'
    for k in range(12):
        b = k * math.pi / 6
        out += f'<line x1="{cx+math.cos(b)*(r-26):.0f}" y1="{cy+math.sin(b)*(r-26):.0f}" x2="{cx+math.cos(b)*(r-8):.0f}" y2="{cy+math.sin(b)*(r-8):.0f}" stroke="{BLK}" stroke-width="6"/>'
    out += f'<line x1="{cx}" y1="{cy}" x2="{cx+math.cos(a)*(r-50):.0f}" y2="{cy+math.sin(a)*(r-50):.0f}" stroke="{PNK}" stroke-width="16" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="16" fill="{BLK}"/>'
    out += txt(740, 720, f"{n}日", 130, PNK if p >= 1 else BLK)
    for k, lab in enumerate(("年齢", "加入期間", "辞めた理由")):
        out += grp(740, 800 + k * 70, pop(t, 0.55 * T + k * 0.25, 0.25), pill(740, 800 + k * 70, lab, 36, 330))
    return out


def d4(t, T):
    out = head(t, "自分の都合で辞めると", 80, "すぐにはもらえない", 96)
    p = prog(t, 0.25 * T, 2.2)
    out += f'<rect x="120" y="720" width="840" height="110" rx="12" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += hbar(120, 720, min(840 * p, 150), "#999", 110)
    out += hbar(270, 720, clamp(840 * p - 150, 0, 520), BLU, 110)
    out += grp(195, 660, pop(t, 0.25 * T + 0.2, 0.25), txt(195, 690, "7日", 50))
    out += grp(530, 660, pop(t, 0.25 * T + 0.8, 0.25), txt(530, 690, "原則1か月", 50))
    out += txt(120, 890, "手続き", 40, BLK, "start")
    out += f'<circle cx="{120+840*p:.0f}" cy="775" r="20" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>'
    done = pop(t, 0.25 * T + 2.2)
    out += grp(875, 775, done, coin(875, 775, 44))
    return out + grp(875, 890, done, txt(875, 900, "スタート", 40))


def d5(t, T):
    out = head(t, "手続きは", 90, "ハローワークで", 124)
    b = 12 * abs(math.sin(t * 5))
    inner = (f'<rect x="400" y="{640-b:.0f}" width="280" height="190" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
             f'<rect x="380" y="{600-b:.0f}" width="320" height="50" rx="8" fill="{GRN}" stroke="{BLK}" stroke-width="8"/>'
             f'<rect x="510" y="{740-b:.0f}" width="60" height="90" fill="{BLK}"/>'
             f'<rect x="425" y="{680-b:.0f}" width="55" height="50" fill="{BLU}" stroke="{BLK}" stroke-width="5"/><rect x="600" y="{680-b:.0f}" width="55" height="50" fill="{BLU}" stroke="{BLK}" stroke-width="5"/>')
    return out + grp(540, 720, pop(t, 0.25), inner) + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["会社を辞めたら、給料のおよそ5割から8割がもらえます。", "雇用保険の基本手当です。"], cap="雇用保険の基本手当", note="※賃金日額の約50〜80%・上限あり", draw=d0,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), (0.5, "pop")]),
    dict(narr=["条件は、辞める前の2年間で、12か月以上の加入。"], cap="2年間で12か月以上", note="※倒産・解雇などは1年間で6か月", draw=d1,
         sfx=[(0.0, "whoosh")] + [(f"f0.3+{k*0.12:.2f}", "tick") for k in range(0, 12, 2)] + [("f0.3+1.5", "ding")]),
    dict(narr=["金額は、直前6か月の給料がもと。", "給料が低い人ほど、割合は高め。"], cap="6か月の給料÷180が元", note="※ボーナスはのぞく・60〜64歳は45〜80%", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.15", "tick"), ("f0.5", "tick")]),
    dict(narr=["日数は、90日から360日。", "年齢や加入期間、辞めた理由で変わります。"], cap="人によって日数がちがう", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.2", "swish"), ("f0.2+1.6", "ding")]),
    dict(narr=["ただし自己都合だと、すぐにはもらえません。", "7日間と、原則1か月待ちます。"], cap="自己都合は待ち時間あり", note="※令和7年4月以降の退職の場合", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.25", "swish"), ("f0.25+2.2", "ding")]),
    dict(narr=["手続きはハローワークで。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.25, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v023_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v023_shitsugyo.mp4")
