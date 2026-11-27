"""Reel 05: 衣替え（夏物の服・季節家電を預ける）."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_lib import *
import reel_lib as M
GREY = (90, 100, 120)
SKY = (205, 228, 245)
PALE = (255, 200, 150)


def shirt(d, cx, ty, s, col):
    """hanger + T-shirt, top of hook at ty."""
    d.arc((cx - s * 0.12, ty, cx + s * 0.12, ty + s * 0.24), 180, 90, fill=GREY, width=max(4, int(s * 0.04)))
    y = ty + s * 0.3
    d.polygon([(cx - s * 0.2, y), (cx + s * 0.2, y), (cx + s * 0.55, y + s * 0.22), (cx + s * 0.42, y + s * 0.42),
               (cx + s * 0.3, y + s * 0.34), (cx + s * 0.3, y + s * 1.0), (cx - s * 0.3, y + s * 1.0),
               (cx - s * 0.3, y + s * 0.34), (cx - s * 0.42, y + s * 0.42), (cx - s * 0.55, y + s * 0.22)], fill=col)
    d.pieslice((cx - s * 0.13, y - s * 0.12, cx + s * 0.13, y + s * 0.12), 0, 180, fill=CREAM)


def fan(d, cx, cy, s, t=0.0):
    d.line((cx, cy, cx, cy + s * 1.1), fill=WHITE, width=int(s * 0.1))
    d.rounded_rectangle((cx - s * 0.5, cy + s * 1.05, cx + s * 0.5, cy + s * 1.2), radius=8, fill=WHITE)
    d.ellipse((cx - s * 0.75, cy - s * 0.75, cx + s * 0.75, cy + s * 0.75), outline=WHITE, width=int(s * 0.08))
    for k in range(3):
        a = t * 3 + k * 2.094
        d.pieslice((cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6), math.degrees(a), math.degrees(a) + 60, fill=ORANGE)
    d.ellipse((cx - s * 0.12, cy - s * 0.12, cx + s * 0.12, cy + s * 0.12), fill=WHITE)


def s1(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    pill(img, "衣替えの季節", 340, 64, NAVY, WHITE, t, 0.0)
    text(img, "夏物の服、", 530, 140, NAVY, t, 0.25)
    text(img, "クローゼットに", 710, 118, NAVY, t, 0.5)
    text(img, "入りきらない？", 880, 124, ORANGE, t, 0.75)
    # crowded rail
    d.rounded_rectangle((70, 1050, 1010, 1074), radius=12, fill=NAVY)
    cols = [ORANGE, NAVY, PALE, (70, 110, 170), ORANGE, BOX, NAVY, PALE, ORANGE]
    for i, c in enumerate(cols):
        p = prog(t, 0.9 + i * 0.12, 0.35)
        if p > 0:
            sw = 12 * math.sin(t * 3 + i)
            shirt(d, 130 + i * 102 + sw * 0.3, 1050 - int((1 - p) * 60), 300, c)
    return img


def s2(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    text(img, "冬のあいだ", 330, 88, WHITE, t, 0.0, black=False)
    text(img, "使わないモノ", 470, 124, ORANGE, t, 0.2)
    rows = [("shirt", "夏物の服"), ("fan", "扇風機"), ("box", "夏用の寝具")]
    for i, (k, name) in enumerate(rows):
        p = prog(t, 0.6 + i * 0.4)
        if p <= 0:
            continue
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        y = 640 + i * 290
        off = int((1 - p) * 140) * (1 if i % 2 else -1)
        d.rounded_rectangle((90 + off, y, 990 + off, y + 250), radius=125, fill=CREAM)
        cx = 855 + off
        d.ellipse((cx - 105, y + 20, cx + 105, y + 230), fill=NAVY)
        if k == "shirt":
            shirt(d, cx, y + 40, 125, ORANGE)
        elif k == "fan":
            fan(d, cx, y + 100, 62, t)
        else:
            box(d, cx - 62, y + 70, 124, 110)
        d.text((170 + off, y + 125), name, font=font(86), fill=NAVY, anchor="lm")
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * p)))
        img.alpha_composite(layer)
    return img


def s3(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    text(img, "まとめて預けて", 340, 100, NAVY, t, 0.0)
    # closet
    x, y, w, h = 160, 520, 760, 640
    d.rounded_rectangle((x, y, x + w, y + h), radius=30, fill=WHITE, outline=NAVY, width=10)
    d.rounded_rectangle((x + 40, y + 70, x + w - 40, y + 90), radius=10, fill=NAVY)
    q = prog(t, 0.8, 0.9)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    for i, c in enumerate([ORANGE, PALE, BOX, ORANGE, PALE]):
        shirt(dl, x + 250 + i * 95 + int(q * 600), y + 68, 250, c)
    a = int(255 * (1 - q))
    layer.putalpha(layer.getchannel("A").point(lambda v: v * a // 255))
    img.alpha_composite(layer)
    for i, c in enumerate([NAVY, (70, 110, 170)]):
        shirt(d, x + 120 + i * int(95 + q * 200), y + 68, 250, c)
    d.line((x + 10, y + h - 150, x + w - 10, y + h - 150), fill=NAVY, width=8)
    box(d, x + 60, y + h - 130, 180, 110)
    text(img, "クローゼット", 1290, 110, NAVY, t, 1.5)
    text(img, "すっきり", 1440, 130, ORANGE, t, 1.7)
    return img


def s4(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    text(img, "季節の変わり目に", 340, 84, WHITE, t, 0.0, black=False)
    text(img, "サッと入れ替え", 480, 120, WHITE, t, 0.2)
    p = prog(t, 0.6)
    if p > 0:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        off = int((1 - p) * 100)
        dl.rounded_rectangle((90, 660 + off, 990, 1180 + off), radius=60, fill=ORANGE)
        dl.text((540, 770 + off), "池ノ上駅から", font=font(84), fill=WHITE, anchor="mm")
        dl.text((300, 980 + off), "徒歩", font=font(110), fill=NAVY, anchor="mm")
        dl.text((610, 960 + off), "30", font=font(300), fill=WHITE, anchor="mm")
        dl.text((860, 1000 + off), "秒", font=font(130), fill=NAVY, anchor="mm")
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * p)))
        img.alpha_composite(layer)
    # arrows: summer <-> winter swap
    p2 = prog(t, 1.3)
    if p2 > 0:
        shirt(d, 300, 1250, 170, PALE)
        d.rounded_rectangle((690, 1330, 870, 1470), radius=20, fill=CREAM)
        d.rectangle((690, 1330, 870, 1362), fill=BOX)
        k = math.sin(t * 5) * 10
        d.polygon([(470 + k, 1340), (560 + k, 1340), (560 + k, 1315), (610 + k, 1360), (560 + k, 1405), (560 + k, 1380), (470 + k, 1380)], fill=ORANGE)
        d.polygon([(610 - k, 1440), (520 - k, 1440), (520 - k, 1415), (470 - k, 1460), (520 - k, 1505), (520 - k, 1480), (610 - k, 1480)], fill=WHITE)
    return img


def s5(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    text(img, "クローゼットに、", 360, 104, NAVY, t, 0.0)
    text(img, "ゆとりを。", 530, 150, ORANGE, t, 0.3)
    q = prog(t, 0.6)
    if q > 0:
        d.rounded_rectangle((300, 690, 780, 706), radius=8, fill=NAVY)
        shirt(d, 450, 690, int(200 * q), NAVY)
        shirt(d, 640, 690, int(200 * q), ORANGE)
    p = prog(t, 0.9)
    if p > 0:
        d.rounded_rectangle((90, 1020, 990, 1500), radius=44, fill=NAVY)
    text(img, "まずは内覧から", 1110, 84, WHITE, t, 0.95)
    pill(img, "24時間WEB内覧予約", 1265, 70, ORANGE, WHITE, t, 1.15, padx=40)
    text(img, "DSトランクルーム代沢", 1415, 76, WHITE, t, 1.4)
    return img


M.SCENES = [(s1, 3.6), (s2, 3.6), (s3, 3.6), (s4, 4.0), (s5, 4.0)]
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "test":
        ims = [fn(dur - 0.4).convert("RGB").resize((360, 640)) for fn, dur in M.SCENES]
        s = Image.new("RGB", (1800, 640))
        for i, im in enumerate(ims):
            s.paste(im, (360 * i, 0))
        s.save("sheet.jpg", quality=88)
    else:
        i = int(mode)
        M.render(i, f"s{i}.mp4")
