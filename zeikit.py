"""Zeikin channel video kit: black-cat host, tax monsters, VOICEVOX voice, SFX, renderer.

A video is a list of scenes. Each scene is a dict:
  narr : list[str]   sentences spoken (Japanese; use hiragana where the reading is risky)
  cap  : str         bottom caption (<= 14 full-width chars)
  note : str | None  small footnote under the caption (sources / assumptions)
  draw : fn(t, T)    returns SVG for the header + stage; t = seconds in scene, T = scene length
  sfx  : list[(when, kind)]  when = seconds (float) or "f0.5" / "f0.5+0.3" (fraction of T + seconds)
                             kind = pop | tick | ding | drop | whoosh | swish | chomp
Call build(scenes, "name.mp4"). Use preview(scenes, "sheet.png") first and LOOK at the sheet.
"""
import glob, io, json, math, os, subprocess
from multiprocessing import Pool
import numpy as np
import soundfile as sf

W, H, FPS, SR = 1080, 1920, 30, 48000
F = 'font-family="Noto Sans CJK JP" font-weight="900"'
YEL, YEL2, BLK, PNK, PNK2, GLD, WHT = "#FFE433", "#FFD400", "#151515", "#FF3D7F", "#D92A66", "#F2B705", "#FFFFFF"
RED, BLU, GRN = "#FF6B35", "#3D8BFF", "#2EC27E"   # 所得税 / 住民税 / 社会保険料 monsters
VV = os.environ.get("ZVV", os.path.expanduser("~/zvv"))
SPEAKER = 3  # VOICEVOX:ずんだもん (ノーマル), in 0.vvm


# ---------- animation helpers ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, t0, d):
    """0→1 ease-out progress starting at t0 lasting d seconds."""
    x = clamp((t - t0) / d)
    return 1 - (1 - x) ** 3


def pop(t, t0, d=0.35):
    """Scale factor for a bouncy pop-in at t0 (0 before t0, overshoots, settles at 1)."""
    x = clamp((t - t0) / d)
    if x <= 0:
        return 0.0
    return 1 + 2.70158 * (x - 1) ** 3 + 1.70158 * (x - 1) ** 2


def grp(cx, cy, s, inner, rot=0.0, op=1.0):
    """Wrap SVG so it scales/rotates around (cx, cy). Returns '' when invisible."""
    if s <= 0.001 or op <= 0.001 or not inner:
        return ""
    return f'<g opacity="{op:.3f}" transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.2f}) scale({s:.4f}) translate({-cx:.1f},{-cy:.1f})">{inner}</g>'


def txt(x, y, s, size, fill=BLK, anchor="middle"):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}">{s}</text>'


# ---------- fixed parts ----------
def head(t, a, asize, b, bsize, tb=0.2):
    """Top header: black strip `a` (yellow text) + white panel `b` (pink text). Width budget ~900px:
    full-width chars * size must stay under ~900."""
    A = f'<rect x="70" y="170" width="940" height="110" rx="14" fill="{BLK}"/>' + txt(540, 225 + asize * 0.36, a, asize, YEL)
    B = f'<rect x="60" y="292" width="960" height="180" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>' + txt(540, 382 + bsize * 0.36, b, bsize, PNK)
    if _COVER:  # scene 1: header is already on screen at frame 0, so the TikTok cover shows the hook
        return A + B
    return grp(540, 225, pop(t, 0.0), A) + grp(540, 382, pop(t, tb), B)


def cat(t, talking):
    mo = talking and int(t / 0.16) % 2 == 1
    dy = -10 * abs(math.sin(t * math.pi / 0.32)) if talking else 0
    s, tx, ty = 1.6, 210 - 190 * 1.6, 751 + dy
    mouth = (f'<ellipse cx="194" cy="340" rx="20" ry="13" fill="{PNK}" stroke="{WHT}" stroke-width="4"/>' if mo else
             f'<path d="M168 336 Q194 352 222 330" fill="none" stroke="{WHT}" stroke-width="4" stroke-linecap="round"/>')
    return f'''<rect x="{210-98*1.6:.1f}" y="{1560+dy:.1f}" width="{196*1.6:.1f}" height="420" fill="{PNK}"/>
<g transform="translate({tx:.1f},{ty:.1f}) scale({s})">
<path d="M92 540 L92 440 Q92 372 190 366 Q288 372 288 440 L288 540 Z" fill="{PNK}"/>
<path d="M140 372 Q190 420 240 372 L240 360 L140 360 Z" fill="{PNK2}"/>
<polygon points="118,250 124,168 184,216" fill="{BLK}"/><polygon points="262,250 256,168 196,216" fill="{BLK}"/>
<polygon points="132,232 135,190 166,216" fill="{PNK}"/><polygon points="248,232 245,190 214,216" fill="{PNK}"/>
<circle cx="190" cy="290" r="84" fill="{BLK}"/>
<rect x="118" y="262" width="62" height="38" rx="10" fill="{PNK}" stroke="{WHT}" stroke-width="4"/>
<rect x="200" y="262" width="62" height="38" rx="10" fill="{PNK}" stroke="{WHT}" stroke-width="4"/>
<line x1="180" y1="276" x2="200" y2="276" stroke="{WHT}" stroke-width="4"/>
<line x1="130" y1="290" x2="150" y2="272" stroke="{WHT}" stroke-width="4" stroke-linecap="round"/>
<line x1="212" y1="290" x2="232" y2="272" stroke="{WHT}" stroke-width="4" stroke-linecap="round"/>
<polygon points="190,312 183,320 197,320" fill="{PNK}"/>
{mouth}
<line x1="112" y1="318" x2="146" y2="322" stroke="{WHT}" stroke-width="2"/><line x1="112" y1="334" x2="146" y2="330" stroke="{WHT}" stroke-width="2"/>
<line x1="268" y1="318" x2="234" y2="322" stroke="{WHT}" stroke-width="2"/><line x1="268" y1="334" x2="234" y2="330" stroke="{WHT}" stroke-width="2"/>
<path d="M146 378 Q190 436 234 378" fill="none" stroke="{GLD}" stroke-width="7" stroke-linecap="round"/>
<circle cx="190" cy="430" r="20" fill="{GLD}" stroke="{BLK}" stroke-width="3"/>
<text x="190" y="438" text-anchor="middle" {F} font-size="22" fill="{BLK}">¥</text>
</g>'''


def bg(tg):
    off = (tg * 70) % 520
    out = [f'<rect width="{W}" height="{H}" fill="{YEL}"/>']
    for k in range(-1, 6):
        y = k * 520 - off + 400
        out.append(f'<polygon points="0,{y+360:.0f} 1080,{y:.0f} 1080,{y+170:.0f} 0,{y+530:.0f}" fill="{YEL2}"/>')
    return "".join(out)


# ---------- stage parts (stage area: x 90..990, y 530..1000; the cat owns x<350, y>1020) ----------
def monster(cx, cy, col, t, s=1.0, chomp=True, rot=0.0):
    """Round tax monster ~240px wide at s=1. col: RED 所得税, BLU 住民税, GRN 社会保険料 (or any colour)."""
    o = abs(math.sin(t * 9)) if chomp else 0.25
    my = cy + 40
    m = (f'<ellipse cx="{cx-70}" cy="{cy+118}" rx="34" ry="18" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
         f'<ellipse cx="{cx+70}" cy="{cy+118}" rx="34" ry="18" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
         f'<polygon points="{cx-78},{cy-88} {cx-58},{cy-150} {cx-28},{cy-104}" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<polygon points="{cx+78},{cy-88} {cx+58},{cy-150} {cx+28},{cy-104}" fill="{WHT}" stroke="{BLK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<ellipse cx="{cx}" cy="{cy}" rx="118" ry="122" fill="{col}" stroke="{BLK}" stroke-width="8"/>'
         f'<circle cx="{cx-42}" cy="{cy-48}" r="28" fill="{WHT}" stroke="{BLK}" stroke-width="6"/><circle cx="{cx+42}" cy="{cy-48}" r="28" fill="{WHT}" stroke="{BLK}" stroke-width="6"/>'
         f'<circle cx="{cx-36}" cy="{cy-44}" r="12" fill="{BLK}"/><circle cx="{cx+48}" cy="{cy-44}" r="12" fill="{BLK}"/>'
         f'<ellipse cx="{cx}" cy="{my}" rx="74" ry="{12+40*o:.1f}" fill="#2B0A0A" stroke="{BLK}" stroke-width="6"/>')
    ty = my - (12 + 40 * o) + 3
    for dx in (-36, 0, 36):
        m += f'<polygon points="{cx+dx-15},{ty:.1f} {cx+dx+15},{ty:.1f} {cx+dx},{ty+22:.1f}" fill="{WHT}"/>'
    return grp(cx, cy, s, m, rot=rot)


def coin(cx, cy, r=48, col=GLD, fg=BLK):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{col}" stroke="{BLK}" stroke-width="7"/>' + txt(cx, cy + r * 0.36, "¥", r * 1.05, fg)


def pill(cx, cy, text, size=44, w=270, bg_=BLK, fg=WHT):
    h = size * 1.9
    return f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{h/2}" fill="{bg_}"/>' + txt(cx, cy + size * 0.36, text, size, fg)


def card(x, y, w, h, inner=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>' + inner


def hbar(x, y, w, col, h=62):
    return f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="8" fill="{col}" stroke="{BLK}" stroke-width="6"/>' if w > 0 else ""


def gauge(t, t0, frac_left, x=120, y=590, w=840, h=130):
    """A 10-segment money bar that shrinks from 100% to frac_left starting at t0 (1s)."""
    p = prog(t, t0, 1.0)
    ww = w * (1 - (1 - frac_left) * p)
    g = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{WHT}" stroke="{BLK}" stroke-width="8"/>'
         f'<rect x="{x+4}" y="{y+4}" width="{ww-8:.1f}" height="{h-8}" rx="16" fill="{GLD}"/>')
    if 0 < p < 1:
        g += f'<rect x="{x+ww:.1f}" y="{y+4}" width="{w-ww-4:.1f}" height="{h-8}" rx="10" fill="{PNK}" opacity="{1-p:.2f}"/>'
    for k in range(1, 10):
        g += f'<line x1="{x+w/10*k}" y1="{y+4}" x2="{x+w/10*k}" y2="{y+h-4}" stroke="{BLK}" stroke-width="3" opacity="0.35"/>'
    return g, p


def vbars(t, values, labels, x0=440, base=980, bw=62, gap=12, unit=8.4, t0=0.5, step=0.33, hi=RED):
    """Vertical bars growing one by one; last bar highlighted."""
    n = len(values)
    out = f'<line x1="{x0-15}" y1="{base+4}" x2="{x0+n*(bw+gap)+5}" y2="{base+4}" stroke="{BLK}" stroke-width="8" stroke-linecap="round"/>'
    for k, v in enumerate(values):
        tk = t0 + k * step
        p = prog(t, tk, 0.35)
        if p <= 0:
            continue
        h, x = v * unit * p, x0 + k * (bw + gap)
        col = hi if k == n - 1 else BLK
        out += f'<rect x="{x}" y="{base-h:.1f}" width="{bw}" height="{h:.1f}" rx="6" fill="{col}"/>'
        out += grp(x + bw / 2, base - h - 24, pop(t, tk + 0.2, 0.25), txt(x + bw / 2, base - h - 12, labels[k], 30, col))
    return out


def icon(kind, x, y):
    """130x140 icons: school | hospital | road | old (pensioner) | house | wallet."""
    if kind == "school":
        return (f'<rect x="{x}" y="{y+50}" width="130" height="90" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
                f'<polygon points="{x-12},{y+54} {x+65},{y} {x+142},{y+54}" fill="{RED}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
                f'<rect x="{x+50}" y="{y+90}" width="30" height="50" fill="{BLK}"/><circle cx="{x+65}" cy="{y+40}" r="12" fill="{WHT}" stroke="{BLK}" stroke-width="5"/>')
    if kind == "hospital":
        return (f'<rect x="{x}" y="{y+5}" width="130" height="135" rx="14" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
                f'<rect x="{x+50}" y="{y+30}" width="30" height="86" fill="{PNK}"/><rect x="{x+22}" y="{y+58}" width="86" height="30" fill="{PNK}"/>')
    if kind == "road":
        return (f'<polygon points="{x+40},{y+5} {x+90},{y+5} {x+135},{y+140} {x-5},{y+140}" fill="#444" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
                f'<line x1="{x+65}" y1="{y+20}" x2="{x+65}" y2="{y+130}" stroke="{WHT}" stroke-width="8" stroke-dasharray="22 16"/>')
    if kind == "house":
        return (f'<rect x="{x+10}" y="{y+60}" width="110" height="80" fill="{WHT}" stroke="{BLK}" stroke-width="7"/>'
                f'<polygon points="{x-8},{y+64} {x+65},{y+4} {x+138},{y+64}" fill="{BLU}" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
                f'<rect x="{x+52}" y="{y+92}" width="28" height="48" fill="{BLK}"/>')
    if kind == "wallet":
        return (f'<rect x="{x}" y="{y+30}" width="130" height="100" rx="16" fill="#8B5A2B" stroke="{BLK}" stroke-width="7"/>'
                f'<rect x="{x+70}" y="{y+62}" width="66" height="38" rx="12" fill="{GLD}" stroke="{BLK}" stroke-width="6"/><circle cx="{x+92}" cy="{y+81}" r="7" fill="{BLK}"/>')
    return (f'<circle cx="{x+65}" cy="{y+78}" r="60" fill="#FFD9B0" stroke="{BLK}" stroke-width="7"/>'
            f'<path d="M{x+8} {y+62} Q{x+65} {y-30} {x+122} {y+62} Q{x+65} {y+22} {x+8} {y+62} Z" fill="#DDD" stroke="{BLK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<circle cx="{x+45}" cy="{y+80}" r="6" fill="{BLK}"/><circle cx="{x+85}" cy="{y+80}" r="6" fill="{BLK}"/>'
            f'<path d="M{x+42} {y+104} Q{x+65} {y+124} {x+88} {y+104}" fill="none" stroke="{BLK}" stroke-width="6" stroke-linecap="round"/>')


def follow(t, t0):
    pulse = 1 + 0.06 * math.sin(t * 9)
    btn = f'<rect x="270" y="870" width="540" height="124" rx="62" fill="{PNK}" stroke="{BLK}" stroke-width="8"/>' + txt(540, 958, "＋ フォロー", 70, WHT)
    return grp(540, 932, pop(t, t0) * pulse, btn)


# ---------- frame / render ----------
_SC, _DURS = [], []
_COVER = False  # True while drawing scene 1 (header + caption shown from the very first frame)


def frame(i, t):
    global _COVER
    sc, T = _SC[i], _DURS[i]
    _COVER = i == 0
    capbox = f'<rect x="70" y="1400" width="860" height="150" rx="14" fill="{BLK}"/>' + txt(500, 1498, sc["cap"], sc.get("csize", 62), WHT)
    notebox = ""
    if sc.get("note"):
        notebox = (f'<rect x="150" y="1562" width="700" height="60" rx="10" fill="{BLK}"/>'
                   f'<text x="500" y="1603" text-anchor="middle" font-family="Noto Sans CJK JP" font-weight="700" font-size="30" fill="{WHT}">{sc["note"]}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + bg(sum(_DURS[:i]) + t) + sc["draw"](t, T) + cat(t, 0.15 < t < T - 0.3)
            + grp(500, 1475, 1 if i == 0 else pop(t, 0.1, 0.3), capbox) + grp(500, 1592, pop(t, 0.5, 0.3), notebox) + '</svg>')


def _png(i, t):
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H)], input=frame(i, t).encode(), stdout=subprocess.PIPE, check=True).stdout


def _render(args):
    i, work = args
    tmp, fin = os.path.join(work, f"s{i}.tmp.mp4"), os.path.join(work, f"s{i}.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                           "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(int(round(_DURS[i] * FPS))):
        ff.stdin.write(_png(i, k / FPS))
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"scene {i} failed")
    os.replace(tmp, fin)
    return fin


# ---------- audio ----------
def _sfx(kind):
    rng = np.random.default_rng(7)

    def env(n, d):
        tt = np.arange(n) / SR
        return np.minimum(1, tt / 0.005) * np.exp(-d * tt)
    if kind == "pop":
        n = int(0.12 * SR); tt = np.arange(n) / SR
        return np.sin(2 * np.pi * (900 * tt - 2200 * tt ** 2)) * env(n, 30)
    if kind == "tick":
        n = int(0.08 * SR); tt = np.arange(n) / SR
        return np.sin(2 * np.pi * 1400 * tt) * env(n, 50) * 0.7
    if kind == "ding":
        n = int(0.9 * SR); tt = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1318.5 * tt) + 0.6 * np.sin(2 * np.pi * 1975.5 * tt) + 0.3 * np.sin(2 * np.pi * 2637 * tt)) * env(n, 5) * 0.55
    if kind == "drop":
        n = int(1.0 * SR); tt = np.arange(n) / SR
        return np.sin(2 * np.pi * (700 * tt - 250 * tt ** 2)) * np.minimum(1, tt / 0.02) * np.minimum(1, (1.0 - tt) / 0.1) * 0.5
    if kind in ("whoosh", "swish"):
        n = int((0.35 if kind == "whoosh" else 0.6) * SR)
        x = np.convolve(rng.standard_normal(n), np.ones(60) / 60, mode="same")
        return x / np.abs(x).max() * np.sin(np.pi * np.arange(n) / n) ** 2 * 0.6
    if kind == "chomp":
        n = int(0.16 * SR)
        x = np.convolve(rng.standard_normal(n), np.ones(25) / 25, mode="same")
        one = x / np.abs(x).max() * env(n, 28)
        out = np.zeros(int(0.5 * SR))
        for o in (0, 0.2):
            out[int(o * SR):int(o * SR) + n] += one
        return out
    raise ValueError(kind)


def _when(spec, T):
    if isinstance(spec, (int, float)):
        return float(spec)
    f, _, plus = spec[1:].partition("+")
    return float(f) * T + (float(plus) if plus else 0.0)


def _synth():
    from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
    import pyopenjtalk
    pyopenjtalk.g2p("あ")  # makes sure the dictionary is downloaded
    d = pyopenjtalk.OPEN_JTALK_DICT_DIR
    ort = Onnxruntime.load_once(filename=glob.glob(f"{VV}/voicevox_onnxruntime-*/lib/libvoicevox_onnxruntime.so.*")[0])
    syn = Synthesizer(ort, OpenJtalk(d.decode() if isinstance(d, bytes) else d))
    with VoiceModelFile.open(f"{VV}/0.vvm") as m:
        syn.load_voice_model(m)
    return syn


def readings(scenes):
    """Print how every sentence will be READ. Check this before building; fix kanji that read wrong by writing hiragana."""
    syn = _synth()
    for i, sc in enumerate(scenes):
        for s in sc["narr"]:
            print(i, s, "→", syn.create_audio_query(s, SPEAKER).kana)


def _audio(scenes, speed, work):
    syn = _synth()
    durs, chunks = [], []
    for i, sc in enumerate(scenes):
        parts = [np.zeros(int(0.15 * SR))]
        for s in sc["narr"]:
            q = syn.create_audio_query(s, SPEAKER)
            print(i, q.kana)
            q.speed_scale, q.intonation_scale, q.output_sampling_rate = speed, 1.5, SR
            q.pre_phoneme_length, q.post_phoneme_length = 0.03, 0.03
            x, _ = sf.read(io.BytesIO(syn.synthesis(q, SPEAKER)))
            parts += [x, np.zeros(int(0.16 * SR))]
        x = np.concatenate(parts)
        dur = round(math.ceil((len(x) / SR + 0.3) / 0.2) * 0.2, 2)
        buf = np.zeros(int(round(dur * SR)))
        buf[:len(x)] = x
        durs.append(dur)
        chunks.append(buf)
    v = np.concatenate(chunks)
    v = v / np.abs(v).max() * 0.9
    fx, start = np.zeros(len(v) + 2 * SR), 0.0
    for sc, T in zip(scenes, durs):
        for spec, kind in sc.get("sfx", [(0.0, "whoosh")]):
            s = _sfx(kind)
            o = int((start + _when(spec, T)) * SR)
            fx[o:o + len(s)] += s
        start += T
    mix = v + 0.22 * fx[:len(v)]
    mix = mix / max(1.0, np.abs(mix).max() / 0.97)
    wav = os.path.join(work, "audio.wav")
    sf.write(wav, mix, SR)
    return durs, wav


def preview(scenes, sheet="sheet.png", frac=0.9, durs=None):
    """Render one frame per scene (at frac of each scene) side by side. Always look at this before build()."""
    global _SC, _DURS
    _SC, _DURS = scenes, durs or [6.0] * len(scenes)
    work = os.path.splitext(sheet)[0] + "_work"
    os.makedirs(work, exist_ok=True)
    ins = []
    for i in range(len(scenes)):
        p = os.path.join(work, f"p{i}.png")
        open(p, "wb").write(_png(i, _DURS[i] * frac))
        ins += ["-i", p]
    n = len(scenes)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex",
                    "".join(f"[{i}]" for i in range(n)) + f"hstack=inputs={n},scale={min(1900, 475*n)}:-1", sheet], check=True)
    return sheet


def build(scenes, out, speed=1.3):
    """Voice + SFX → scene lengths → render every scene → join → mux. Returns (path, total_seconds)."""
    global _SC, _DURS
    work = os.path.splitext(out)[0] + "_work"
    os.makedirs(work, exist_ok=True)
    durs, wav = _audio(scenes, speed, work)
    _SC, _DURS = scenes, durs
    json.dump(durs, open(os.path.join(work, "durs.json"), "w"))
    with Pool(min(4, os.cpu_count() or 2)) as p:
        files = p.map(_render, [(i, work) for i in range(len(scenes))])
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
    joined = os.path.join(work, "joined.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", joined, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, durs, sum(durs))
    return out, sum(durs)
