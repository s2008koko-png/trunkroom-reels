import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narration import build
build(lines=[
    (0.3, 3.1, "キャンプ道具、部屋のどこに置いてますか？"),
    (3.9, 3.1, "趣味の道具は、場所をとりますよね。"),
    (7.5, 3.1, "使わない季節は預けて、お部屋ひろびろ。"),
    (11.1, 3.6, "池ノ上駅、徒歩三十秒。二十四時間、出し入れ自由。"),
    (15.1, 3.5, "ディーエストランクルーム代沢。ウェブで内覧予約できます。"),
], total=18.8, bgm="bgm.wav", out="audio.wav")
