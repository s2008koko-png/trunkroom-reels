"""#039 通勤手当の非課税 — 電車・バス通勤の通勤手当は月15万円まで非課税・こえた分は給与として課税・
最も経済的かつ合理的な経路が条件でグリーン料金は含まれない・車や自転車は片道の距離で限度額が決まる
（2km未満は全額課税／2km以上10km未満 4,200円／95km以上 66,400円〈令和8年4月1日以後に支払われるべき通勤手当〉）。
Sources (fetched 2026-11-24): 国税庁 No.2582 電車・バス通勤者の通勤手当（令和8年4月1日現在法令等） /
通勤手当の非課税限度額の改正について（令和8年4月）"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403


def traincar(x, y, col=BLU, label=""):
    """Original train car, 240x130, top-left at (x, y)."""
    c = f'<rect x="{x:.1f}" y="{y:.1f}" width="240" height="130" rx="22" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
    for k in range(3):
        c += f'<rect x="{x+22+k*70:.1f}" y="{y+22:.1f}" width="54" height="46" rx="8" fill="{WHT}" stroke="{BLK}" stroke-width="5"/>'
    c += f'<rect x="{x:.1f}" y="{y+86:.1f}" width="240" height="14" fill="{BLK}"/>'
    for k in (55, 185):
        c += f'<circle cx="{x+k:.1f}" cy="{y+136:.1f}" r="20" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
    if label:
        c += txt(x + 120, y - 16, label, 40)
    return c


def rail(y):
    r = f'<line x1="90" y1="{y}" x2="990" y2="{y}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k in range(12):
        r += f'<line x1="{120+k*75}" y1="{y}" x2="{120+k*75}" y2="{y+18}" stroke="{BLK}" stroke-width="6"/>'
    return r


def car(x, y, col=RED):
    """Original small car, ~170 wide, top-left at (x, y)."""
    return (f'<path d="M{x+35:.1f} {y+30:.1f} L{x+55:.1f} {y:.1f} L{x+115:.1f} {y:.1f} L{x+135:.1f} {y+30:.1f} Z" fill="{WHT}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{x:.1f}" y="{y+30:.1f}" width="170" height="44" rx="14" fill="{col}" stroke="{BLK}" stroke-width="7"/>'
            f'<circle cx="{x+42:.1f}" cy="{y+78:.1f}" r="17" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
            f'<circle cx="{x+128:.1f}" cy="{y+78:.1f}" r="17" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>')


def check(cx, cy, r=60):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GRN}" stroke="{BLK}" stroke-width="8"/>'
            f'<path d="M{cx-r*0.45} {cy} L{cx-r*0.1} {cy+r*0.35} L{cx+r*0.5} {cy-r*0.35}" fill="none" stroke="{WHT}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(cx, cy, r=70):
    return (f'<line x1="{cx-r}" y1="{cy-r}" x2="{cx+r}" y2="{cy+r}" stroke="{PNK}" stroke-width="30" stroke-linecap="round"/>'
            f'<line x1="{cx-r}" y1="{cy+r}" x2="{cx+r}" y2="{cy-r}" stroke="{PNK}" stroke-width="30" stroke-linecap="round"/>')


def d0(t, T):
    out = head(t, "通勤手当は 月15万円まで", 76, "税金 0円", 140)
    out += rail(770)
    x = 110 + 60 * t
    dy = 3 * math.sin(t * 14)
    out += traincar(x, 610 + dy) + traincar(x + 252, 610 + dy)
    out += grp(300, 910, pop(t, 0.3), pill(300, 910, "電車・バス通勤", 44, 380))
    out += grp(760, 910, pop(t, 0.5 * T), pill(760, 910, "税金 0円", 54, 340, PNK))
    return out


def d1(t, T):
    out = head(t, "ふつうの給料とは", 86, "べつあつかい", 124)
    out += grp(300, 725, pop(t, 0.15), card(100, 560, 400, 330, txt(300, 640, "給料", 64)))
    out += monster(300, 770, RED, t, 0.55 * pop(t, 0.35))
    out += grp(300, 950, pop(t, 0.6), pill(300, 950, "所得税がかかる", 40, 380))
    t0 = 0.5 * T
    out += grp(780, 725, pop(t, t0), card(580, 560, 400, 330, txt(780, 640, "通勤手当", 64) + check(780, 770, 70)))
    out += grp(780, 950, pop(t, t0 + 0.4), pill(780, 950, "かからない", 44, 340, PNK))
    return out


def d2(t, T):
    out = head(t, "15万円をこえたら", 86, "こえた分に税金", 112)
    x0, y0, h = 120, 660, 110
    w = 680 * prog(t, 0.3, 0.45 * T)
    out += f'<rect x="{x0}" y="{y0}" width="840" height="{h}" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    if w > 0:
        out += f'<rect x="{x0}" y="{y0}" width="{min(w, 600):.1f}" height="{h}" fill="{GLD}" stroke="{BLK}" stroke-width="8"/>'
    if w > 600:
        out += f'<rect x="{x0+600}" y="{y0}" width="{w-600:.1f}" height="{h}" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<line x1="{x0+600}" y1="{y0-40}" x2="{x0+600}" y2="{y0+h+30}" stroke="{BLK}" stroke-width="8" stroke-dasharray="16 12"/>'
    out += grp(x0 + 600, 590, pop(t, 0.2), txt(x0 + 600, 606, "15万円", 52))
    out += grp(390, 880, pop(t, 0.35 * T), pill(390, 880, "ここまで 0円", 46, 400))
    out += grp(800, 880, pop(t, 0.3 + 0.45 * T), pill(800, 880, "ここだけ課税", 42, 320, PNK))
    return out


def d3(t, T):
    out = head(t, "グリーン車の料金は", 86, "対象外", 140)
    out += rail(790)
    dx = -700 * (1 - prog(t, 0.1, 0.8))
    out += traincar(150 + dx, 630) + traincar(402 + dx, 630, GRN, "グリーン車")
    t0 = 0.55 * T
    out += grp(522, 695, pop(t, t0), cross(522, 705, 52))
    out += grp(840, 690, pop(t, t0 + 0.3), pill(840, 690, "対象外", 50, 250, PNK))
    out += grp(540, 930, pop(t, 0.2 * T), pill(540, 930, "安くて合理的なルート", 44, 540))
    return out


def d4(t, T):
    out = head(t, "車や自転車は", 90, "距離で決まる", 124)
    out += f'<line x1="100" y1="668" x2="980" y2="668" stroke="{BLK}" stroke-width="8" stroke-linecap="round" stroke-dasharray="40 24"/>'
    out += car(110 + 700 * clamp(t / T) , 575 + 3 * math.sin(t * 14))
    rows = [("2km未満", 0, "全額課税", 0.3 * T), ("2〜10km", 24, "4,200円", 0.5 * T), ("95km以上", 330, "66,400円", 0.68 * T)]
    for k, (lab, w, val, t0) in enumerate(rows):
        y = 700 + k * 100
        out += grp(240, y + 30, pop(t, t0, 0.3), txt(120, y + 48, lab, 48, BLK, "start"))
        out += hbar(400, y, w * prog(t, t0 + 0.15, 0.5), GLD, 60)
        out += grp(400 + w + 120, y + 30, pop(t, t0 + 0.4, 0.3), txt(400 + w + 20, y + 48, val, 50, PNK if k == 0 else BLK, "start"))
    out += grp(850, 728, pop(t, 0.2), pill(850, 728, "月の上限", 38, 230))
    return out


def d5(t, T):
    out = head(t, "給与明細の", 90, "通勤手当を見よう", 104)
    slip = card(190, 570, 220, 250, txt(300, 630, "給与明細", 40)
                + "".join(f'<rect x="215" y="{660+k*42}" width="{170 if k != 1 else 110}" height="20" rx="6" fill="{PNK if k == 1 else BLK}"/>' for k in range(3)))
    out += grp(300, 695, pop(t, 0.2), slip, rot=-5 + 3 * math.sin(t * 4))
    out += grp(540, 700, pop(t, 0.35), coin(540, 700 - 14 * abs(math.sin(t * 5 + 1)), 60))
    out += grp(780, 700, 0.75 * pop(t, 0.5), traincar(660, 640 - 10 * abs(math.sin(t * 5 + 2))))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["会社からもらう通勤手当は、月15万円まで、税金がかかりません。"], cap="通勤手当は非課税", note="※電車・バス通勤の場合", draw=d0,
         sfx=[(0.0, "whoosh"), (0.3, "pop"), ("f0.5", "ding")]),
    dict(narr=["給料には、所得税がかかります。", "でも通勤手当は、べつあつかいです。"], cap="給料とは別あつかい", draw=d1,
         sfx=[(0.0, "whoosh"), (0.35, "chomp"), ("f0.5", "pop"), ("f0.5+0.4", "ding")]),
    dict(narr=["ただし、15万円をこえた分は、給料として税金がかかります。"], cap="こえた分は給料あつかい", note="※通勤手当が月17万円の例", draw=d2,
         sfx=[(0.0, "whoosh"), (0.3, "swish"), ("f0.45+0.3", "drop")]),
    dict(narr=["条件は、いちばん安くて合理的なルート。", "グリーン料金は、ふくまれません。"], cap="グリーン料金は対象外", note="※最も経済的かつ合理的な経路が条件", draw=d3,
         sfx=[(0.0, "whoosh"), ("f0.2", "pop"), ("f0.55", "drop"), ("f0.55+0.3", "pop")]),
    dict(narr=["車や自転車は、片道の距離で上限が決まります。", "2キロ未満は、全部に税金がかかります。"], cap="片道2km未満は課税", note="※令和8年4月以後の通勤手当の限度額", draw=d4,
         sfx=[(0.0, "whoosh"), ("f0.3", "tick"), ("f0.5", "tick"), ("f0.68", "tick")]),
    dict(narr=["給与明細を、見てみよう。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v039_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v039_tsukin.mp4")
