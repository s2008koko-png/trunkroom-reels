# How the reels are made
- `reel_lib.py`: drawing helpers (1080x1920, 30fps, PIL frames piped to ffmpeg). `text()`, `pill()`, `box()`, `render(i, out)`; scenes are functions `scene(t) -> RGBA image` listed in `SCENES = [(fn, seconds), ...]`.
- `example_reel_02.py`: a full example reel built on reel_lib (run `python3 example_reel_02.py test` for a contact sheet, then `0..4` to render scenes s0..s4.mp4).
- `bgm.py`: synthesizes an original background track to `bgm.wav` (edit `dur`, `bpm`, `chords`).
- Join: `ffmpeg -f concat -i list.txt -c copy joined.mp4`, then `ffmpeg -i joined.mp4 -i bgm.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest -movflags +faststart out.mp4`.
- Keep text between y=250 and y=1520 (Instagram UI covers top/bottom). Check a contact sheet for overflow before rendering.
