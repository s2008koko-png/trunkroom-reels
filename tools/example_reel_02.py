import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_lib import *
import reel_lib as M
GREY=(90,100,120)

def s1(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    # closet overflowing
    p = prog(t, 0.0, 0.5)
    d.rounded_rectangle((240, 1000, 840, 1560), radius=24, fill=(60, 84, 124))
    d.line((540, 1000, 540, 1560), fill=NAVY, width=8)
    d.ellipse((500, 1260, 524, 1284), fill=ORANGE); d.ellipse((556, 1260, 580, 1284), fill=ORANGE)
    spec=[(180,1380,220,180,0.5),(700,1400,240,170,0.65),(300,1480,200,150,0.8),(600,1500,190,140,0.95),(110,1520,180,130,1.1),(820,1540,170,120,1.25)]
    for x,y,w,h,st in spec:
        q=prog(t,st,0.45)
        if q>0: box(d,x,int(y+(1-q)*500),w,h)
    text(img, "クローゼット、", 440, 130, WHITE, t, 0.2)
    text(img, "もう限界？", 640, 180, ORANGE, t, 0.55)
    return img

def ic(d, kind, cx, cy):
    d.ellipse((cx-95, cy-95, cx+95, cy+95), fill=ORANGE)
    if kind=="shirt":
        d.polygon([(cx-60,cy-40),(cx-25,cy-58),(cx,cy-40),(cx+25,cy-58),(cx+60,cy-40),(cx+42,cy-8),(cx+30,cy-16),(cx+30,cy+56),(cx-30,cy+56),(cx-30,cy-16),(cx-42,cy-8)], fill=WHITE)
    elif kind=="case":
        d.rounded_rectangle((cx-42,cy-36,cx+42,cy+56), radius=12, fill=WHITE)
        d.rounded_rectangle((cx-20,cy-62,cx+20,cy-36), radius=8, outline=WHITE, width=9)
        d.line((cx-14,cy-20,cx-14,cy+40), fill=ORANGE, width=7); d.line((cx+14,cy-20,cx+14,cy+40), fill=ORANGE, width=7)
    elif kind=="tent":
        d.polygon([(cx,cy-54),(cx+66,cy+48),(cx-66,cy+48)], fill=WHITE)
        d.polygon([(cx,cy-6),(cx+20,cy+48),(cx-20,cy+48)], fill=ORANGE)
    elif kind=="book":
        for i,(w,h) in enumerate([(26,96),(26,80),(26,104)]):
            x=cx-48+i*34
            d.rounded_rectangle((x,cy+52-h,x+w,cy+52), radius=5, fill=WHITE)
            d.line((x+5,cy+52-h+18,x+w-5,cy+52-h+18), fill=ORANGE, width=5)

def s2(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    text(img, "こんなモノ、", 360, 96, NAVY, t, 0.0)
    text(img, "預けられます", 500, 120, ORANGE, t, 0.25)
    items=[("shirt","季節の服"),("case","スーツケース"),("tent","キャンプ用品"),("book","本・コレクション")]
    for i,(k,name) in enumerate(items):
        p=prog(t,0.6+i*0.35)
        if p<=0: continue
        layer=Image.new("RGBA", img.size, (0,0,0,0)); d=ImageDraw.Draw(layer)
        col=i%2; row=i//2
        x=90+col*460; y=660+row*440+int((1-p)*80)
        d.rounded_rectangle((x,y,x+440,y+400), radius=40, fill=WHITE)
        ic(d,k,x+220,y+150)
        d.text((x+220,y+320), name, font=font(52 if len(name)<7 else 44), fill=NAVY, anchor="mm")
        layer.putalpha(layer.getchannel("A").point(lambda v:int(v*p)))
        img.alpha_composite(layer)
    return img

def s3(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    text(img, "サイズが選べる", 400, 110, WHITE, t, 0.0)
    # three lockers growing
    sizes=[(170,260,"0.54㎡〜"),(250,400,""),(340,560,"〜2.46㎡")]
    x=140; base=1180
    for i,(w,h,lab) in enumerate(sizes):
        p=prog(t,0.4+i*0.3,0.5)
        if p>0:
            hh=int(h*p)
            d.rounded_rectangle((x,base-hh,x+w,base), radius=16, fill=WHITE if i!=2 else ORANGE)
            d.ellipse((x+w-44,base-hh//2-12,x+w-20,base-hh//2+12), fill=NAVY)
        x+=w+40
    text(img, "0.54㎡", 1260, 60, WHITE, t, 1.0, cx=225)
    text(img, "2.46㎡", 1260, 60, ORANGE, t, 1.3, cx=850)
    text(img, "ロッカータイプは", 1400, 70, WHITE, t, 1.6, black=False)
    text(img, "月額2,980円(税込)〜", 1510, 92, ORANGE, t, 1.8)
    text(img, "※別途管理費がかかります", 1610, 42, (190,200,215), t, 2.0, black=False)
    return img

def s4(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    text(img, "屋内型だから", 430, 100, NAVY, t, 0.0, black=False)
    pill(img, "冷暖房", 660, 130, NAVY, WHITE, t, 0.3, padx=70, pady=34)
    text(img, "＋", 850, 110, ORANGE, t, 0.6)
    pill(img, "除湿機", 1040, 130, NAVY, WHITE, t, 0.8, padx=70, pady=34)
    text(img, "完備", 1280, 190, ORANGE, t, 1.2)
    return img

def s5(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    pill(img, "池ノ上駅 徒歩30秒", 420, 78, ORANGE, WHITE, t, 0.0)
    text(img, "24時間365日", 640, 130, WHITE, t, 0.3)
    text(img, "出し入れ自由", 800, 130, WHITE, t, 0.5)
    p=prog(t,0.9)
    if p>0: d.rounded_rectangle((90,1000,990,1480), radius=44, fill=CREAM)
    text(img, "無料の内覧予約は", 1100, 76, NAVY, t, 0.95, black=False)
    text(img, "WEBで24時間受付", 1230, 86, NAVY, t, 1.15)
    text(img, "DSトランクルーム代沢", 1380, 76, ORANGE, t, 1.35)
    return img

M.SCENES=[(s1,3.2),(s2,4.4),(s3,4.2),(s4,3.2),(s5,4.4)]
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="test":
        ims=[fn(dur-0.4).convert("RGB").resize((360,640)) for fn,dur in M.SCENES]
        s=Image.new("RGB",(1800,640))
        for i,im in enumerate(ims): s.paste(im,(360*i,0))
        s.save("sheet.jpg",quality=88)
    else:
        i=int(mode); M.render(i,f"s{i}.mp4")
