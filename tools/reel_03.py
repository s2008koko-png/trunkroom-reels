"""Reel 03: 年末の大掃除 (year-end cleaning)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_lib import *
import reel_lib as M
GREY = (90, 100, 120)


def sparkle(d, cx, cy, r, col):
    d.polygon([(cx, cy - r), (cx + r * 0.25, cy - r * 0.25), (cx + r, cy), (cx + r * 0.25, cy + r * 0.25),
               (cx, cy + r), (cx - r * 0.25, cy + r * 0.25), (cx - r, cy), (cx - r * 0.25, cy - r * 0.25)], fill=col)


def s1(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 1500, W, H), fill=NAVY)
    # pile of boxes rising from the floor
    spec = [(90, 1290, 260, 210, 0.3), (370, 1300, 240, 200, 0.45), (630, 1280, 250, 220, 0.6),
            (200, 1090, 240, 200, 0.8), (470, 1100, 250, 200, 0.95), (330, 910, 230, 190, 1.15)]
    for x, y, w, h, st in spec:
        q = prog(t, st, 0.45)
        if q > 0:
            box(d, x, int(y + (1 - q) * 700), w, h)
    # broom swinging
    q = prog(t, 1.3, 0.5)
    if q > 0:
        sw = math.sin(t * 5) * 18
        bx = 930 + sw
        d.line((bx - 60, 900, bx, 1400), fill=BOXD, width=18)
        d.polygon([(bx - 50, 1390), (bx + 50, 1390), (bx + 80, 1500), (bx - 80, 1500)], fill=ORANGE)
    pill(img, "12月の前に", 330, 64, NAVY, WHITE, t, 0.0)
    text(img, "年末の大掃除", 520, 132, NAVY, t, 0.25)
    text(img, "しまう場所ない！", 700, 112, ORANGE, t, 0.6)
    return img


def ic(d, kind, cx, cy):
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=ORANGE)
    if kind == "shirt":
        d.polygon([(cx - 44, cy - 30), (cx - 18, cy - 42), (cx, cy - 30), (cx + 18, cy - 42), (cx + 44, cy - 30),
                   (cx + 31, cy - 6), (cx + 22, cy - 12), (cx + 22, cy + 42), (cx - 22, cy + 42), (cx - 22, cy - 12),
                   (cx - 31, cy - 6)], fill=WHITE)
    elif kind == "fan":
        d.ellipse((cx - 36, cy - 46, cx + 36, cy + 26), outline=WHITE, width=8)
        d.ellipse((cx - 9, cy - 19, cx + 9, cy - 1), fill=WHITE)
        d.line((cx, cy + 26, cx, cy + 44), fill=WHITE, width=8)
        d.line((cx - 26, cy + 46, cx + 26, cy + 46), fill=WHITE, width=8)
    elif kind == "tent":
        d.polygon([(cx, cy - 40), (cx + 48, cy + 36), (cx - 48, cy + 36)], fill=WHITE)
        d.polygon([(cx, cy - 4), (cx + 15, cy + 36), (cx - 15, cy + 36)], fill=ORANGE)
    elif kind == "book":
        for i, (w, h) in enumerate([(20, 72), (20, 58), (20, 78)]):
            x = cx - 36 + i * 26
            d.rounded_rectangle((x, cy + 40 - h, x + w, cy + 40), radius=4, fill=WHITE)


def s2(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    text(img, "今つかわないモノは", 340, 84, WHITE, t, 0.0, black=False)
    text(img, "外に預けよう", 480, 128, ORANGE, t, 0.25)
    rows = [("shirt", "夏の服"), ("fan", "扇風機"), ("tent", "レジャー用品"), ("book", "本・思い出の品")]
    for i, (k, name) in enumerate(rows):
        p = prog(t, 0.6 + i * 0.3)
        if p <= 0:
            continue
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        y = 640 + i * 215
        off = int((1 - p) * 140) * (1 if i % 2 == 0 else -1)
        d.rounded_rectangle((110 + off, y, 970 + off, y + 180), radius=90, fill=CREAM)
        ic(d, k, 210 + off, y + 90)
        d.text((330 + off, y + 90), name, font=font(74), fill=NAVY, anchor="lm")
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * p)))
        img.alpha_composite(layer)
    return img


def room(d, x, y, w, h, full, p=1.0):
    d.rounded_rectangle((x, y, x + w, y + h), radius=28, fill=WHITE, outline=NAVY, width=8)
    d.line((x + 8, y + h - 90, x + w - 8, y + h - 90), fill=NAVY, width=6)
    # window
    d.rectangle((x + w - 150, y + 50, x + w - 50, y + 170), fill=(190, 222, 245), outline=NAVY, width=6)
    if full:
        for bx, by, bw, bh in [(30, 250, 130, 110), (170, 270, 120, 90), (60, 150, 120, 100), (300, 260, 110, 100)]:
            box(d, x + bx, y + h - 90 - (h - 90 - by) + 0, bw, bh) if False else box(d, x + bx, y + by, bw, bh)
    else:
        # sofa
        d.rounded_rectangle((x + 50, y + h - 190, x + 260, y + h - 90), radius=20, fill=ORANGE)
        d.rounded_rectangle((x + 50, y + h - 250, x + 260, y + h - 170), radius=20, fill=(255, 170, 90))
        for sx, sy, r in [(200, 110, 30), (80, 200, 22), (380, 240, 20)]:
            sparkle(d, x + sx, y + sy, int(r * p), ORANGE)


def s3(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    text(img, "モノが減ると…", 340, 88, NAVY, t, 0.0, black=False)
    p = prog(t, 0.3)
    if p > 0:
        room(d, 70, 520, 430, 460, True)
    q = prog(t, 0.9, 0.4)
    if q > 0:
        d.polygon([(520, 720), (520, 780), (548, 780), (548, 800), (584, 750), (548, 700), (548, 720)], fill=ORANGE)
    r = prog(t, 1.2)
    if r > 0:
        room(d, 600, 520, 430, 460, False, r)
    text(img, "Before", 1040, 50, GREY, t, 0.3, cx=285)
    text(img, "After", 1040, 50, ORANGE, t, 1.2, cx=815)
    text(img, "お部屋すっきり", 1230, 124, NAVY, t, 1.5)
    text(img, "掃除もラクに", 1400, 104, ORANGE, t, 1.8)
    return img


def s4(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    text(img, "預けたあとも安心", 340, 96, WHITE, t, 0.0)
    cards = [("冷暖房・除湿機", "完備の屋内型"), ("24時間365日", "出し入れ自由"), ("池ノ上駅", "徒歩30秒")]
    for i, (a, b) in enumerate(cards):
        p = prog(t, 0.4 + i * 0.45)
        if p <= 0:
            continue
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        y = 520 + i * 320 + int((1 - p) * 70)
        d.rounded_rectangle((110, y, 970, y + 270), radius=40, fill=WHITE)
        d.rounded_rectangle((110, y, 140, y + 270), radius=14, fill=ORANGE)
        d.text((560, y + 95), a, font=font(84), fill=NAVY, anchor="mm")
        d.text((560, y + 195), b, font=font(64), fill=ORANGE, anchor="mm")
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * p)))
        img.alpha_composite(layer)
    return img


def s5(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    for sx, sy, r, st in [(170, 330, 40, 0.2), (930, 300, 30, 0.4), (860, 760, 26, 0.6), (200, 800, 24, 0.8)]:
        q = prog(t, st)
        if q > 0:
            sparkle(d, sx, sy, int(r * q * (1 + 0.15 * math.sin(t * 6))), ORANGE)
    text(img, "すっきりした部屋で", 450, 92, NAVY, t, 0.0)
    text(img, "新年を。", 640, 170, ORANGE, t, 0.3)
    p = prog(t, 0.9)
    if p > 0:
        d.rounded_rectangle((90, 920, 990, 1500), radius=44, fill=NAVY)
    text(img, "まずは内覧から", 1030, 84, WHITE, t, 0.95)
    pill(img, "WEB内覧予約 24時間受付", 1210, 62, ORANGE, WHITE, t, 1.15, padx=40)
    text(img, "DSトランクルーム代沢", 1390, 78, WHITE, t, 1.4)
    return img


M.SCENES = [(s1, 3.4), (s2, 3.8), (s3, 3.6), (s4, 4.0), (s5, 4.2)]
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
