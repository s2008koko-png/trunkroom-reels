"""#028 自動車にかかる税金 — 自動車税は毎年4月1日に持っている人に課税（都道府県／軽は市町村）・排気量で決まる（1,000cc以下25,000円・〜1,500cc 30,500円・〜2,000cc 36,000円）・軽は10,800円・車検時に自動車重量税（国税）・環境性能割は令和8年4月1日に廃止。"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def car(cx, cy, t, s=1.0, col=BLU, small=False):
    """Simple original car ~360px wide centred on (cx, cy); wheels spin with t. small=True draws a short boxy kei car."""
    w = 250 if small else 360
    x = cx - w / 2
    cab = (f'<path d="M{x+30} {cy-20} L{x+50} {cy-100} L{x+w-40} {cy-100} L{x+w-20} {cy-20} Z" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>' if small else
           f'<path d="M{x+70} {cy-20} L{x+110} {cy-95} L{x+w-110} {cy-95} L{x+w-60} {cy-20} Z" fill="{col}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>')
    win = (f'<rect x="{x+62}" y="{cy-86}" width="{w-116}" height="52" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>' if small else
           f'<path d="M{x+100} {cy-28} L{x+125} {cy-80} L{x+w-122} {cy-80} L{x+w-88} {cy-28} Z" fill="{WHT}" stroke="{BLK}" stroke-width="6" stroke-linejoin="round"/>')
    body = f'<rect x="{x}" y="{cy-24}" width="{w}" height="78" rx="26" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
    lamp = f'<circle cx="{x+w-18}" cy="{cy+8}" r="12" fill="{YEL}" stroke="{BLK}" stroke-width="5"/>'
    wh = ""
    for wx in (x + 70, x + w - 70):
        a = t * 6
        wh += f'<circle cx="{wx}" cy="{cy+56}" r="38" fill="{BLK}"/><circle cx="{wx}" cy="{cy+56}" r="16" fill="{WHT}"/>'
        wh += f'<line x1="{wx-30*math.cos(a):.1f}" y1="{cy+56-30*math.sin(a):.1f}" x2="{wx+30*math.cos(a):.1f}" y2="{cy+56+30*math.sin(a):.1f}" stroke="{WHT}" stroke-width="6"/>'
    return grp(cx, cy, s, cab + win + body + lamp + wh)


def road(t, y=880):
    out = f'<rect x="90" y="{y}" width="900" height="16" rx="8" fill="{BLK}"/>'
    off = (t * 260) % 120
    for k in range(9):
        x = 990 - k * 120 - off
        if 100 < x < 930:
            out += f'<rect x="{x:.0f}" y="{y+34}" width="60" height="10" rx="5" fill="{BLK}" opacity="0.5"/>'
    return out


def d0(t, T):
    out = head(t, "車を持ってるだけで", 90, "毎年 税金がかかる", 104)
    cx = 330 + 8 * math.sin(t * 3)
    out += road(t) + car(cx, 790 - 4 * abs(math.sin(t * 9)), t, 1.0)
    for k in range(3):
        ph = (t * 0.7 + k / 3) % 1.0
        out += grp(0, 0, 1, coin(480 + 300 * ph, 720 - 140 * math.sin(math.pi * ph), 30), op=1 - ph ** 3)
    return out + monster(850, 700, RED, t, 0.6)


def d1(t, T):
    out = head(t, "払うのは", 84, "4月1日の持ち主", 116)
    # calendar card flips in
    out += grp(300, 760, pop(t, 0.2), f'<rect x="150" y="580" width="300" height="360" rx="24" fill="{WHT}" stroke="{BLK}" stroke-width="10"/>'
               f'<rect x="150" y="580" width="300" height="90" rx="24" fill="{PNK}" stroke="{BLK}" stroke-width="10"/>'
               + txt(300, 648, "4月", 64, WHT) + txt(300, 880, "1", 230, BLK))
    out += car(720, 700 - 6 * abs(math.sin(t * 6)), t, 0.8 * pop(t, 0.5), GRN)
    return out + grp(720, 900, pop(t, 0.4 * T), pill(720, 900, "1年分がかかる", 50, 420))


def d2(t, T):
    out = head(t, "金額は", 84, "エンジンの大きさで決まる", 76)
    rows = [("1,000cc以下", 25, "25,000円", 0.08 * T), ("1,500ccまで", 30.5, "30,500円", 0.4 * T), ("2,000ccまで", 36, "36,000円", 0.62 * T)]
    for k, (lab, v, val, t0) in enumerate(rows):
        y = 545 + k * 150
        out += grp(250, y + 20, pop(t, t0, 0.3), txt(130, y + 40, lab, 46, BLK, "start"))
        out += hbar(130, y + 56, v * 13 * prog(t, t0 + 0.15, 0.6), (BLU, GRN, RED)[k], 66)
        out += grp(130 + v * 13 + 120, y + 90, pop(t, t0 + 0.6, 0.3), txt(130 + v * 13 + 22, y + 108, val, 54, BLK, "start"))
    return out


def d3(t, T):
    out = head(t, "軽自動車は", 90, "年10,800円", 140)
    x = 990 - 720 * prog(t, 0.1, 0.9)
    out += road(t if t < 1.0 else 1.0) + car(x, 800, t if t < 1.0 else 1.0, 1.0, PNK, small=True)
    out += grp(700, 640, pop(t, 1.0), pill(700, 640, "10,800円", 80, 480, BLK, YEL))
    return out + grp(700, 780, pop(t, 0.5 * T), pill(700, 780, "市町村に払う", 44, 360, BLU))


def d4(t, T):
    out = head(t, "車検のときは", 84, "重さで決まる重量税", 96)
    # a weighing scale: the car drops on, the needle swings
    drop = 1 - prog(t, 0.2, 0.5)
    out += car(330, 760 - 220 * drop, 0, 0.8)
    out += f'<rect x="130" y="840" width="400" height="34" rx="10" fill="{BLK}"/><rect x="180" y="874" width="300" height="96" rx="16" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    ang = -60 + 100 * prog(t, 0.7, 0.8) + 4 * math.sin(t * 7)
    out += f'<line x1="330" y1="960" x2="{330+70*math.sin(math.radians(ang)):.1f}" y2="{960-70*math.cos(math.radians(ang)):.1f}" stroke="{PNK}" stroke-width="10" stroke-linecap="round"/><circle cx="330" cy="960" r="10" fill="{BLK}"/>'
    out += grp(770, 620, pop(t, 0.9), pill(770, 620, "国の税金", 50, 320))
    t2 = 0.5 * T
    out += grp(770, 800, pop(t, t2), card(580, 720, 380, 160, txt(770, 790, "環境性能割", 56) + txt(770, 850, "買うときの税", 38)))
    q = prog(t, t2 + 0.5, 0.3)
    if q > 0:
        out += f'<line x1="600" y1="740" x2="{600+340*q:.0f}" y2="{740+120*q:.0f}" stroke="{PNK}" stroke-width="16" stroke-linecap="round"/>'
    return out + grp(770, 940, pop(t, t2 + 0.8), pill(770, 940, "4月に廃止", 48, 320, PNK))


def d5(t, T):
    out = head(t, "車の税金は", 90, "毎年と 車検のとき", 104)
    out += road(t, 760) + car(300 + 10 * math.sin(t * 3), 670 - 4 * abs(math.sin(t * 9)), t, 0.75, BLU)
    out += car(760 + 10 * math.sin(t * 3 + 1), 690 - 4 * abs(math.sin(t * 9 + 1)), t, 0.75 * pop(t, 0.4), PNK, small=True)
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["車は、持っているだけで毎年、税金がかかります。"], cap="自動車税は毎年かかる", draw=d0,
         sfx=[(0.0, "whoosh"), (0.4, "swish"), (1.2, "chomp")]),
    dict(narr=["4月1日に車を持っている人に、1年分がかかります。"], cap="4月1日の持ち主が払う", note="※自動車税は都道府県・軽自動車税は市町村", draw=d1,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.5, "pop"), ("f0.4", "ding")]),
    dict(narr=["金額は、エンジンの大きさで決まります。", "1000シーシー以下で2万5000円、2000シーシーまでなら3万6000円。"], cap="排気量で金額が決まる", note="※2019年10月以降に登録の自家用乗用車", draw=d2,
         sfx=[(0.0, "whoosh"), ("f0.08", "tick"), ("f0.4", "tick"), ("f0.62", "tick")]),
    dict(narr=["軽自動車は、年1万800円です。"], cap="軽自動車は10,800円", note="※自家用の四輪乗用・標準税率", draw=d3,
         sfx=[(0.0, "whoosh"), (0.1, "swish"), (1.0, "ding")]),
    dict(narr=["車検のときは、重さで決まる自動車重量税。", "買うときの環境性能割は、今年4月に廃止されました。"], cap="車検のときは重量税", note="※環境性能割は令和8年4月1日に廃止", draw=d4,
         sfx=[(0.0, "whoosh"), (0.65, "drop"), ("f0.5", "pop"), ("f0.5+0.5", "swish")]),
    dict(narr=["車の税金は、毎年と車検のとき。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.4, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v028_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v028_kuruma.mp4")
