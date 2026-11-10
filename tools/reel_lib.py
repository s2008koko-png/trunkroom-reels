import subprocess, sys, os, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
NAVY = (18, 35, 63)
ORANGE = (255, 138, 31)
CREAM = (255, 247, 234)
WHITE = (255, 255, 255)
BOX = (214, 165, 104)
BOXD = (176, 128, 72)
BLACK_F = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
MED_F = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
_fc = {}


def font(size, black=True):
    k = (size, black)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(BLACK_F if black else MED_F, size, index=0)
    return _fc[k]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def prog(t, start, dur=0.45):
    return ease((t - start) / dur)


def text(img, s, cy, size, color, t, start, black=True, cx=W // 2, slide=50):
    p = prog(t, start)
    if p <= 0:
        return
    f = font(size, black)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text((cx, cy + int((1 - p) * slide)), s, font=f, fill=color + (int(255 * p),), anchor="mm")
    img.alpha_composite(layer)


def pill(img, s, cy, size, bg, fg, t, start, padx=50, pady=26):
    p = prog(t, start)
    if p <= 0:
        return
    f = font(size)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    l, tp, r, b = d.textbbox((W // 2, cy), s, font=f, anchor="mm")
    off = int((1 - p) * 50)
    a = int(255 * p)
    d.rounded_rectangle((l - padx, tp - pady + off, r + padx, b + pady + off), radius=40, fill=bg + (a,))
    d.text((W // 2, cy + off), s, font=f, fill=fg + (a,), anchor="mm")
    img.alpha_composite(layer)


def box(d, x, y, w, h):
    d.rounded_rectangle((x, y, x + w, y + h), radius=14, fill=BOX, outline=BOXD, width=6)
    d.rectangle((x + w // 2 - 22, y, x + w // 2 + 22, y + h), fill=(236, 206, 160))
    d.line((x, y + h // 3, x + w, y + h // 3), fill=BOXD, width=4)


def scene1(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    # falling boxes
    spec = [(150, 1380, 300, 240, 0.0), (470, 1400, 260, 220, 0.15), (750, 1360, 240, 260, 0.3),
            (230, 1150, 280, 230, 0.5), (540, 1180, 300, 220, 0.65), (380, 950, 270, 210, 0.9),
            (680, 960, 230, 220, 1.05), (160, 930, 200, 200, 1.2)]
    for x, y, w, h, st in spec:
        p = prog(t, st, 0.5)
        if p > 0:
            box(d, x, int(y - (1 - p) * 1500), w, h)
    d.rectangle((0, 1620, W, H), fill=NAVY)
    text(img, "部屋、", 430, 150, NAVY, t, 0.2)
    text(img, "モノであふれて", 600, 130, NAVY, t, 0.5)
    text(img, "ませんか？", 770, 150, ORANGE, t, 0.8)
    return img


def scene2(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    text(img, "世田谷・池ノ上に", 400, 84, WHITE, t, 0.0, black=False)
    text(img, "駅から徒歩", 560, 120, WHITE, t, 0.25)
    p = prog(t, 0.6, 0.6)
    if p > 0:
        n = max(1, int(round(30 * p)))
        f = font(360)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        dl.text((W // 2 - 90, 860), str(n), font=f, fill=ORANGE + (int(255 * p),), anchor="mm")
        dl.text((W // 2 + 250, 920), "秒", font=font(170), fill=ORANGE + (int(255 * p),), anchor="mm")
        img.alpha_composite(layer)
    # route illustration: station -> dots -> building
    y = 1250
    p = prog(t, 1.2, 0.8)
    if p > 0:
        d.rounded_rectangle((120, y - 80, 400, y + 80), radius=24, fill=WHITE)
        d.text((260, y), "池ノ上駅", font=font(54), fill=NAVY, anchor="mm")
        x0, x1 = 430, 660
        k = int(6 * p)
        for i in range(k):
            cx = x0 + (x1 - x0) * i / 5
            d.ellipse((cx - 12, y - 12, cx + 12, y + 12), fill=ORANGE)
    p2 = prog(t, 1.9, 0.4)
    if p2 > 0:
        d.rounded_rectangle((690, y - 150, 960, y + 80), radius=20, fill=ORANGE)
        for r in range(2):
            for c in range(3):
                d.rectangle((722 + c * 78, y - 118 + r * 86, 778 + c * 78, y - 58 + r * 86), fill=WHITE)
    pill(img, "DSトランクルーム代沢", 1470, 70, WHITE, NAVY, t, 2.0)
    return img


def scene3(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    text(img, "気になるお値段は…", 420, 84, NAVY, t, 0.0, black=False)
    text(img, "月額", 620, 120, NAVY, t, 0.3)
    p = prog(t, 0.6, 0.7)
    if p > 0:
        n = int(round(2980 * p / 10) * 10)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        a = int(255 * p)
        dl.text((W // 2 - 70, 880), f"{n:,}", font=font(230), fill=ORANGE + (a,), anchor="mm")
        dl.text((W // 2 + 340, 925), "円", font=font(110), fill=ORANGE + (a,), anchor="mm")
        img.alpha_composite(layer)
    text(img, "（税込）から", 1090, 90, NAVY, t, 1.3)
    text(img, "※別途管理費がかかります", 1230, 46, (90, 100, 120), t, 1.5, black=False)
    pill(img, "更新料 0円", 1420, 84, NAVY, WHITE, t, 1.9)
    return img


def icon(d, kind, cx, cy):
    d.ellipse((cx - 80, cy - 80, cx + 80, cy + 80), fill=ORANGE)
    if kind == "clock":
        d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), outline=WHITE, width=9)
        d.line((cx, cy, cx, cy - 32), fill=WHITE, width=9)
        d.line((cx, cy, cx + 24, cy + 10), fill=WHITE, width=9)
    elif kind == "air":
        for i in range(3):
            yy = cy - 32 + i * 32
            d.arc((cx - 55, yy - 18, cx - 5, yy + 18), 180, 360, fill=WHITE, width=9)
            d.arc((cx - 5, yy - 18, cx + 45, yy + 18), 0, 180, fill=WHITE, width=9)
    elif kind == "cam":
        d.rounded_rectangle((cx - 52, cy - 30, cx + 20, cy + 30), radius=8, fill=WHITE)
        d.polygon([(cx + 20, cy - 8), (cx + 56, cy - 30), (cx + 56, cy + 30), (cx + 20, cy + 8)], fill=WHITE)
    elif kind == "card":
        d.rounded_rectangle((cx - 52, cy - 34, cx + 52, cy + 34), radius=10, fill=WHITE)
        d.rectangle((cx - 52, cy - 16, cx + 52, cy - 2), fill=ORANGE)


def scene4(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    text(img, "安心・快適の屋内型", 380, 92, WHITE, t, 0.0)
    rows = [("clock", "24時間365日", "出し入れ自由"), ("air", "冷暖房・除湿機", "完備"),
            ("cam", "防犯カメラ", "SECOM導入"), ("card", "ICカードキー", "利用者だけ入室")]
    for i, (k, a, b) in enumerate(rows):
        st = 0.35 + i * 0.4
        p = prog(t, st)
        if p <= 0:
            continue
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        y = 560 + i * 250
        off = int((1 - p) * 120)
        d.rounded_rectangle((90 + off, y, 990 + off, y + 210), radius=36, fill=WHITE)
        icon(d, k, 210 + off, y + 105)
        d.text((330 + off, y + 72), a, font=font(72), fill=NAVY, anchor="lm")
        d.text((330 + off, y + 152), b, font=font(48, False), fill=(90, 100, 120), anchor="lm")
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * p)))
        img.alpha_composite(layer)
    return img


def scene5(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    pill(img, "キャンペーン実施中", 400, 70, ORANGE, WHITE, t, 0.0)
    text(img, "賃料 最大", 590, 110, NAVY, t, 0.3)
    text(img, "2ヶ月無料", 790, 168, ORANGE, t, 0.55)
    text(img, "※条件があります", 930, 44, (90, 100, 120), t, 0.8, black=False)
    p = prog(t, 1.1)
    if p > 0:
        d.rounded_rectangle((90, 1040, 990, 1500), radius=44, fill=NAVY)
    text(img, "まずは無料で内覧", 1130, 84, WHITE, t, 1.15)
    text(img, "WEB予約は24時間受付", 1250, 62, WHITE, t, 1.35, black=False)
    text(img, "DSトランクルーム代沢", 1400, 76, ORANGE, t, 1.55)
    return img


SCENES = [(scene1, 3.2), (scene2, 3.6), (scene3, 3.6), (scene4, 4.2), (scene5, 4.4)]


def fade(img, t, dur):
    # quick fade in/out to white-ish between scenes
    a = min(prog(t, 0, 0.2), 1.0)
    out = 1 - ease((t - (dur - 0.2)) / 0.2) if t > dur - 0.2 else 1.0
    k = a * out
    if k >= 0.999:
        return img
    bg = Image.new("RGBA", img.size, WHITE + (255,))
    return Image.blend(bg, img, k)


def render(i, out):
    fn, dur = SCENES[i]
    tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                          "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for f in range(n):
        t = f / FPS
        last = (i == len(SCENES) - 1)
        img = fn(t)
        img = fade(img, t, dur if not last else dur + 9)
        p.stdin.write(img.convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() != 0:
        sys.exit("ffmpeg failed")
    os.rename(tmp, out)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "test":
        for i, (fn, dur) in enumerate(SCENES):
            fn(dur - 0.4).convert("RGB").resize((540, 960)).save(f"t{i}.jpg", quality=85)
    else:
        i = int(mode)
        render(i, f"s{i}.mp4")
