"""Reel 04: 趣味の道具（キャンプ・ゴルフ・スノーボード）."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_lib import *
import reel_lib as M
GREY = (90, 100, 120)
SKY = (205, 228, 245)


def tent(d, cx, by, s, col=ORANGE, door=NAVY):
    d.polygon([(cx, by - int(1.5 * s)), (cx + int(1.7 * s), by), (cx - int(1.7 * s), by)], fill=col)
    d.polygon([(cx, by - int(0.8 * s)), (cx + int(0.45 * s), by), (cx - int(0.45 * s), by)], fill=door)
    d.line((cx, by - int(1.5 * s), cx, by - int(1.75 * s)), fill=door, width=max(4, s // 14))


def s1(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    # stars
    for i, (sx, sy) in enumerate([(140, 300), (930, 340), (820, 250), (260, 880), (900, 900), (90, 620), (990, 640)]):
        r = 7 + 4 * math.sin(t * 4 + i)
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=CREAM)
    # ground + tent rising
    d.ellipse((-200, 1380, W + 200, 2100), fill=(30, 55, 95))
    q = prog(t, 0.9, 0.6)
    if q > 0:
        tent(d, 540, 1470 + int((1 - q) * 500), 190)
    pill(img, "キャンプ好きの方へ", 360, 62, ORANGE, WHITE, t, 0.0)
    text(img, "その道具、", 560, 140, WHITE, t, 0.25)
    text(img, "部屋のどこに", 740, 124, WHITE, t, 0.5)
    text(img, "置いてますか？", 910, 124, ORANGE, t, 0.75)
    return img


def ic(d, kind, cx, cy):
    d.rounded_rectangle((cx - 110, cy - 110, cx + 110, cy + 110), radius=40, fill=NAVY)
    if kind == "tent":
        tent(d, cx, cy + 60, 55, ORANGE, NAVY)
    elif kind == "golf":
        d.line((cx - 40, cy - 70, cx - 40, cy + 70), fill=WHITE, width=10)
        d.polygon([(cx - 36, cy - 70), (cx + 46, cy - 44), (cx - 36, cy - 14)], fill=ORANGE)
        d.ellipse((cx + 14, cy + 34, cx + 58, cy + 78), fill=WHITE)
    elif kind == "board":
        layer = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        dl.rounded_rectangle((92, 20, 148, 220), radius=28, fill=ORANGE)
        dl.rectangle((92, 86, 148, 100), fill=WHITE)
        dl.rectangle((92, 140, 148, 154), fill=WHITE)
        layer = layer.rotate(-28, resample=Image.BICUBIC)
        d._image.paste(layer, (cx - 120, cy - 120), layer)


def s2(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    text(img, "趣味の道具は", 340, 96, NAVY, t, 0.0)
    text(img, "場所をとる…", 480, 116, ORANGE, t, 0.25)
    rows = [("tent", "キャンプ用品"), ("golf", "ゴルフバッグ"), ("board", "スノーボード")]
    for i, (k, name) in enumerate(rows):
        p = prog(t, 0.6 + i * 0.4)
        if p <= 0:
            continue
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        y = 640 + i * 290 + int((1 - p) * 80)
        d.rounded_rectangle((90, y, 990, y + 250), radius=48, fill=WHITE, outline=NAVY, width=6)
        ic(d, k, 225, y + 125)
        d.text((380, y + 125), name, font=font(80), fill=NAVY, anchor="lm")
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * p)))
        img.alpha_composite(layer)
    return img


def s3(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    text(img, "使わない季節は", 350, 96, WHITE, t, 0.0, black=False)
    text(img, "預けて", 520, 150, ORANGE, t, 0.25)
    # room: boxes slide out to the right, room becomes empty
    x, y, w, h = 140, 680, 800, 520
    d.rounded_rectangle((x, y, x + w, y + h), radius=30, fill=CREAM)
    d.rectangle((x + 560, y + 60, x + 720, y + 220), fill=SKY, outline=NAVY, width=6)
    d.line((x, y + h - 90, x + w, y + h - 90), fill=BOXD, width=6)
    d.rounded_rectangle((x + 60, y + h - 210, x + 330, y + h - 90), radius=22, fill=ORANGE)
    d.rounded_rectangle((x + 60, y + h - 280, x + 330, y + h - 190), radius=22, fill=(255, 170, 90))
    q = prog(t, 0.9, 0.9)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    off = int(q * 700)
    for bx, by, bw, bh in [(380, 290, 150, 140), (540, 310, 130, 120), (440, 160, 140, 130), (660, 250, 110, 180)]:
        box(dl, x + bx + off, y + by, bw, bh)
    a = int(255 * (1 - q))
    layer.putalpha(layer.getchannel("A").point(lambda v: v * a // 255))
    img.alpha_composite(layer)
    text(img, "お部屋ひろびろ", 1350, 124, WHITE, t, 1.6)
    return img


def s4(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    text(img, "週末の前にサッと", 330, 84, NAVY, t, 0.0, black=False)
    text(img, "取り出せる", 470, 128, NAVY, t, 0.2)
    items = [("池ノ上駅", "徒歩30秒", ORANGE, WHITE, WHITE), ("24時間365日", "出し入れ自由", NAVY, WHITE, ORANGE),
             ("冷暖房・除湿機", "完備", NAVY, WHITE, ORANGE)]
    pos = [(90, 620, 990, 900), (90, 940, 990, 1180), (90, 1220, 990, 1460)]
    for i, ((a, b, bg, fa, fb), (l, tp, r, bt)) in enumerate(zip(items, pos)):
        p = prog(t, 0.55 + i * 0.45)
        if p <= 0:
            continue
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        off = int((1 - p) * 150) * (-1 if i % 2 else 1)
        d.rounded_rectangle((l + off, tp, r + off, bt), radius=50, fill=bg)
        cy = (tp + bt) // 2
        if i == 0:
            d.text((540 + off, cy - 62), a, font=font(84), fill=fa, anchor="mm")
            d.text((540 + off, cy + 58), b, font=font(112), fill=NAVY, anchor="mm")
        else:
            d.text((540 + off, cy - 48), a, font=font(84), fill=fa, anchor="mm")
            d.text((540 + off, cy + 56), b, font=font(64), fill=fb, anchor="mm")
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * p)))
        img.alpha_composite(layer)
    return img


def s5(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    text(img, "趣味を、", 380, 120, WHITE, t, 0.0)
    text(img, "もっと身軽に。", 560, 138, ORANGE, t, 0.3)
    q = prog(t, 0.6)
    if q > 0:
        tent(d, 540, 900, int(110 * q), ORANGE, NAVY)
    p = prog(t, 0.9)
    if p > 0:
        d.rounded_rectangle((90, 980, 990, 1500), radius=44, fill=CREAM)
    text(img, "まずは内覧から", 1080, 84, NAVY, t, 0.95)
    pill(img, "24時間WEB内覧予約", 1250, 70, ORANGE, WHITE, t, 1.15, padx=40)
    text(img, "DSトランクルーム代沢", 1410, 76, NAVY, t, 1.4)
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
