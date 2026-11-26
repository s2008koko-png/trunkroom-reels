"""#045 在職老齢年金 — 厚生年金に加入しながら老齢厚生年金を受ける60歳以上の人は、基本月額（老齢厚生年金〈報酬比例部分〉の月額）と
総報酬月額相当額（標準報酬月額＋1年間の標準賞与額÷12）の合計が支給停止調整額をこえると、こえた金額の半分が支給停止。
支給停止調整額は令和8年4月から月51万円→65万円（令和8年度・毎年度改定）。老齢基礎年金は調整の対象にならず全額支給。
計算例：給料60万円＋年金10万円＝70万円 → (70−65)÷2＝2.5万円が停止 → 年金7.5万円。
Sources (fetched 2026-11-26): 日本年金機構 在職老齢年金制度が改正されました（更新日2026年4月1日）/ 用語集 在職老齢年金 /
厚生労働省 在職老齢年金制度の見直しについて"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from zeikit import *  # noqa: F401,F403

X0, PX = 120, 10.5          # money track: 0..80万円 across x 120..960
LIM = X0 + 65 * PX          # the 65万円 line


def limit_line(y1, y2):
    return f'<line x1="{LIM}" y1="{y1}" x2="{LIM}" y2="{y2}" stroke="{BLK}" stroke-width="8" stroke-dasharray="16 10"/>'


def d0(t, T):
    out = head(t, "働きながら年金", 100, "月65万円が さかいめ", 90)
    p = prog(t, 0.35 * T, 1.2)
    val = 40 + 30 * p
    out += f'<rect x="{X0}" y="650" width="840" height="110" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
    out += f'<rect x="{X0+4}" y="654" width="{min(val, 65)*PX-8:.1f}" height="102" rx="10" fill="{GLD}"/>'
    if val > 65:
        out += f'<rect x="{LIM}" y="654" width="{(val-65)*PX:.1f}" height="102" fill="{PNK}"/>'
    out += limit_line(630, 780) + pill(LIM, 580, "65万円", 50, 240)
    over = val > 65
    wob = 8 * math.sin(t * 30) if over and p < 1 else 0
    out += txt(540 + wob, 930, f"合計 {int(round(val))}万円", 120, PNK if over else BLK)
    return out


def d1(t, T):
    out = head(t, "給料＋厚生年金が", 90, "65万円をこえると", 100)
    out += grp(290, 635, pop(t, 0.2), card(110, 560, 360, 150, txt(290, 664, "給料", 84)))
    out += grp(540, 635, pop(t, 0.2 * T + 0.2), txt(540, 668, "＋", 90))
    out += grp(790, 635, pop(t, 0.2 * T + 0.4), card(610, 560, 360, 150, txt(790, 660, "厚生年金", 72)))
    t0 = 0.6 * T
    blink = PNK if int(t / 0.3) % 2 == 0 else PNK2
    out += grp(540, 860, pop(t, t0), card(170, 760, 740, 210, txt(540, 842, "こえた分の半分が", 62) + txt(540, 940, "ストップ", 86, blink)))
    return out


def d2(t, T):
    out = head(t, "給料60万＋年金10万", 84, "年金は2.5万円へる", 96)
    t1, t2, t3, t4 = 0.08 * T, 0.28 * T, 0.5 * T, 0.75 * T
    w1 = 60 * PX * prog(t, t1, 0.6)
    w2 = 10 * PX * prog(t, t2, 0.4)
    out += hbar(X0, 650, w1, BLU, 110)
    out += grp(X0 + 315, 705, pop(t, t1 + 0.5), txt(X0 + 315, 724, "給料 60万円", 54, WHT))
    if w2 > 0:
        out += hbar(X0 + 630, 650, w2, GLD, 110)
        if t > t3 and w2 > 52:
            out += f'<rect x="{LIM}" y="650" width="52.5" height="110" fill="{PNK}" stroke="{BLK}" stroke-width="6"/>'
    out += grp(LIM, 612, pop(t, t2 + 0.3), txt(LIM, 626, "年金 10万円", 42))
    out += grp(LIM, 790, pop(t, t3 - 0.3), limit_line(640, 772) + txt(LIM, 818, "65万円", 42))
    out += grp(400, 880, pop(t, t3), txt(400, 890, "こえた5万円の半分", 50))
    out += grp(540, 960, pop(t, t4), txt(540, 990, "年金 10万→7.5万円", 84, PNK))
    return out


def d3(t, T):
    out = head(t, "このさかいめ", 100, "51万→65万円に", 110)
    U, base = 5.4, 960
    h1 = 51 * U * prog(t, 0.15, 0.5)
    out += f'<line x1="140" y1="{base+4}" x2="940" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    out += f'<rect x="180" y="{base-h1:.1f}" width="260" height="{h1:.1f}" rx="8" fill="{BLK}"/>'
    out += grp(310, base - 51 * U - 30, pop(t, 0.6), txt(310, base - 51 * U - 16, "51万円", 60))
    out += grp(310, 900, pop(t, 0.6), txt(310, 916, "これまで", 46, WHT))
    t0 = 0.5 * T
    v = 51 + 14 * prog(t, t0, 1.0)
    if t > t0 - 0.4:
        h2 = v * U * prog(t, t0 - 0.4, 0.4)
        out += f'<rect x="640" y="{base-h2:.1f}" width="260" height="{h2:.1f}" rx="8" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>'
        out += txt(770, base - v * U - 16, f"{int(round(v))}万円", 64, PNK)
        out += grp(770, 880, pop(t, t0), txt(770, 860, "2026年", 46, WHT) + txt(770, 920, "4月から", 46, WHT))
    out += grp(540, 800, pop(t, t0 - 0.2), txt(540, 830, "→", 90))
    return out


def d4(t, T):
    out = head(t, "へるのは厚生年金だけ", 84, "基礎年金は全額", 120)
    sq = 1 - 0.06 * abs(math.sin(t * 4))  # the 2nd floor squeezes a little
    out += grp(540, 640, pop(t, 0.2), grp(540, 730, sq, card(230, 550, 620, 180, txt(430, 664, "厚生年金", 64) + pill(710, 640, "調整あり", 40, 220))))
    out += grp(160, 640, pop(t, 0.2), txt(160, 660, "2階", 54))
    t0 = 0.5 * T
    out += grp(540, 850, pop(t, 0.35), card(230, 760, 620, 180, txt(430, 874, "基礎年金", 64)))
    out += grp(160, 850, pop(t, 0.35), txt(160, 870, "1階", 54))
    out += grp(710, 850, pop(t, t0) * (1 + 0.05 * math.sin(t * 8)), pill(710, 850, "全額", 60, 220, PNK))
    return out


def d5(t, T):
    out = head(t, "働く前に", 100, "65万円をチェック", 100)
    for k, cx in enumerate((270, 540, 810)):
        out += grp(cx, 700, pop(t, 0.2 + k * 0.15), coin(cx, 700 - 30 * abs(math.sin(t * 6 + k * 0.9)), 70))
    return out + follow(t, 0.45 * T)


SCENES = [
    dict(narr=["働きながら年金をもらうと、年金がへることも。", "さかいめは、月65万円。"], cap="さかいめは月65万円",
         note="※令和8年度・厚生年金に入って働く60歳以上", draw=d0, sfx=[(0.0, "whoosh"), ("f0.35", "swish"), ("f0.35+1.2", "ding")]),
    dict(narr=["給料と厚生年金の合計が65万円をこえると、こえた分の半分が止まります。"], cap="こえた分の半分が止まる",
         note="※給料はボーナスこみの年収÷12で計算", draw=d1, sfx=[(0.0, "whoosh"), (0.2, "pop"), ("f0.2+0.4", "pop"), ("f0.6", "drop")]),
    dict(narr=["給料60万円、年金10万円なら、合計70万円。", "年金は2万5千円へります。"], cap="5万円こえ→半分へる",
         note="※月の額の例（令和8年度の基準）", draw=d2, sfx=[(0.0, "whoosh"), ("f0.08", "swish"), ("f0.28", "tick"), ("f0.5", "pop"), ("f0.75", "ding")]),
    dict(narr=["2026年4月に、51万円から65万円に上がりました。"], cap="51万円から65万円へ",
         note="※金額は毎年度見直されます", draw=d3, sfx=[(0.0, "whoosh"), (0.15, "tick"), ("f0.5", "swish"), ("f0.5+1.0", "ding")]),
    dict(narr=["へるのは厚生年金だけ。", "基礎年金は、全額もらえます。"], cap="基礎年金はへらない", draw=d4,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), ("f0.5", "ding")]),
    dict(narr=["働く前に、65万円をチェック。", "フォローして学ぼう。"], cap="フォローして学ぼう", draw=d5,
         sfx=[(0.0, "whoosh"), (0.2, "pop"), (0.35, "pop"), (0.5, "pop"), ("f0.45", "ding")]),
]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1:] == ["preview"]:
        print(preview(SCENES, "out/v045_sheet.png"))
    elif sys.argv[1:] == ["readings"]:
        readings(SCENES)
    else:
        build(SCENES, "out/v045_zairo.mp4")
