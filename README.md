# zeikin — 30秒でわかる税金 (TikTok channel kit)

Short vertical explainer videos (1080x1920, ~30s) about Japanese tax and money rules.
Style: so simple a primary-school child could follow, but spoken to adults.
Host: an original black cat in pink sunglasses. Helpers: three round "tax monsters"
(RED 所得税, BLU 住民税, GRN 社会保険料). Voice: VOICEVOX ずんだもん. Posting is done by hand by the owner.

## Files
- `setup.sh` — run once per session (downloads the voice engine, installs Python packages).
- `zeikit.py` — the kit: drawing parts, animation helpers, voice, sound effects, renderer. Read its docstrings.
- `videos/v001_tedori.py` — the reference video. New videos copy its shape.
- `TOPICS_LOG.md` — every video made so far. Never repeat a topic or a hook.

## Make a video
```bash
bash setup.sh
python3 videos/vNNN_slug.py readings   # how each sentence will be READ — fix wrong readings by writing hiragana
python3 videos/vNNN_slug.py preview    # contact sheet -> out/vNNN_sheet.png — LOOK at it, fix overlaps/overflow
python3 videos/vNNN_slug.py            # full build -> out/vNNN_slug.mp4 (about 2 minutes)
```

## Format rules (what makes a video belong to this channel)
- 5–6 scenes, 28–35 seconds total. Scene 1 is the hook: a number or a loss the viewer feels in the first second.
  Last scene: a one-line takeaway + `follow()` button. Second-to-last: the fair "other side" when the topic has one.
- Every scene has something MOVING on the stage that shows the point (bars growing, coins leaving, a gauge shrinking,
  cards popping in). Never a scene with only text. Build new stage drawings from simple shapes when the kit has none.
- Words: short, plain, no jargon without a 3-word explanation. One idea per scene. Narration ≤ 2 short sentences per scene.
- Layout: header via `head()` (text width: full-width chars × font size ≤ ~900px). Stage is x 90..990, y 530..1000.
  The cat owns the bottom-left (x<350, y>1020). Caption ≤ 14 full-width chars. Nothing below y=1640 (TikTok UI).
- Original shapes only: no photos, logos, third-party characters, or copyrighted music.

## Fact rules (non-negotiable)
- Every number comes from an official page fetched today: nta.go.jp, mof.go.jp, soumu.go.jp, mhlw.go.jp,
  nenkin.go.jp, kyoukaikenpo.or.jp, cao.go.jp, e-gov. If today's official figure cannot be confirmed, drop the claim
  or choose another topic. Rules change every April/January — never reuse numbers from an old script without re-checking.
- Estimates (take-home pay etc.) must state the assumption in the scene `note` (e.g. `※年収450万円・独身の会社員の目安`).
- Explain how the rules work. Only lawful, ordinary options (控除, ふるさと納税, iDeCo, NISA as rules, not as advice to buy).
  Never: tax evasion or "won't get caught" tips, promises of savings, investment recommendations, political blame.
- No fake urgency, no invented statistics, no "〜しないと大損" unless the number is shown and sourced.

## Posting notes (for the owner)
- Credit required in the TikTok caption: `VOICEVOX:ずんだもん`
- Add a trending sound at low volume inside the TikTok app when posting.
