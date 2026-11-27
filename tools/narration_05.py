import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narration import build
build(lines=[
    (0.3, 3.1, "夏物の服、クローゼットに入りきらない？"),
    (3.9, 3.1, "冬のあいだ使わない、夏服や扇風機。"),
    (7.5, 3.1, "まとめて預けて、クローゼットすっきり。"),
    (11.1, 3.6, "池ノ上駅から徒歩三十秒。サッと入れ替え。"),
    (15.1, 3.5, "ディーエストランクルーム代沢。ウェブで内覧予約できます。"),
], total=18.8, bgm="bgm.wav", out="audio.wav")
