# Unsora reference — calls · polling · manifest · ffmpeg assembly

Exact mechanics for Phases 1 → 6. The defining split: **everything generated runs
on Unsora** (`create_image`, `create_video`, `create_voiceover`, optionally
`create_music`); **the cut, the narration placement and the mix are ffmpeg**, run
locally. If a call returns an auth error, surface it and let the user
re-authenticate — don't silently switch generator.

Contents:
1. Workspace layout
2. The job model
3. Style key — `create_image`
4. Reference sheets — `create_image`
5. Optional hero-frame lock
6. Blocks — `create_video` (+ QC)
7. Narration — `create_voiceover`
8. Music — `create_music` (optional)
9. Manifest schema
10. ffmpeg — concat
11. ffmpeg — VO placement and mix
12. Optional burned subtitles
13. Verification
14. Resume after failure
15. Moderation and IP
16. Cost
17. Optional posting

---

## 1. Workspace layout

```
<agent-workspace>/diorama-myth/
├── blocks.json          # manifest — source of truth for resume
├── style_key.png        # the cardstock style key (Phase 1)
├── sheets/              # character / creature / place / talisman sheets
├── frames/              # only for hero-frame-locked blocks
├── clips/               # block_01.mp4 … (10s each)
├── vo/                  # vo_01.mp3 … (voiced blocks only)
├── music.mp3            # only if a bed was requested
├── concat_list.txt
├── cut.mp4              # stitched picture, native SFX only
└── final.mp4            # narration + [music] mixed — the deliverable
```

Copy the skill's `scripts/` next to the workspace (or call them by absolute path).
Copy only `final.mp4` to the outputs directory at the end.

---

## 2. The job model

Every `create_*` is asynchronous and returns a `generation.id`. Poll the matching
waiter, then take the **result URL** off the completed job:

| Create | Poll | Sensible polling |
|---|---|---|
| `create_image` | `wait_for_image` | `intervalSeconds: 5`, `maxAttempts: 60` |
| `create_video` | `wait_for_video` | `intervalSeconds: 10`, `maxAttempts: 90` (Seedance 2.0 runs several minutes a clip) |
| `create_voiceover` | `wait_for_voiceover` | `intervalSeconds: 5`, `maxAttempts: 60` |
| `create_music` | `wait_for_music` | `intervalSeconds: 5`, `maxAttempts: 60` |

**The URL is the currency, not the id.** A result URL is what goes into `image` and
`referenceImages` on later calls, and what you `curl` for the local copy. Record
both id and URL in the manifest — the id is for resume, the URL is for work.

Submitting the N block jobs back to back and polling them afterwards is much faster
than serialising, but keep a strict id → block mapping so a failure is retried alone.

---

## 3. Style key — `create_image`

| Param | Value |
|---|---|
| `prompt` | The STYLE KEY prompt from `style-dna.md` §Style key, palette hexes substituted |
| `model` | `"nano-banana-pro"` |
| `aspectRatio` | The run's ratio — `"16:9"` by default |

`wait_for_image` → `curl -L -o style_key.png "<URL>"` → QC it:

```bash
python scripts/qc.py frame style_key.png --ground '#DCC0A0' --accent '#A02D19' --void '#1B2740'
```

Ground share near 45%, all three colours strongly present, nothing crushed or
blown, cut edges legible. Re-roll here rather than discovering the problem across
N clips — the key rides in `referenceImages` on every block, so its faults become
the film's faults.

---

## 4. Reference sheets — `create_image`

One call per sheet, **before any block**, using the sheet formats in
`style-dna.md` §Reference sheets.

| Param | Value |
|---|---|
| `prompt` | The sheet prompt, verbatim |
| `model` | `"nano-banana-pro"` |
| `aspectRatio` | `"16:9"` for figures, creatures and places; `"1:1"` for the talisman prop — regardless of the film's ratio |
| `referenceImages` | `[style_key_url]` — the key holds the sheet on-palette |

QC each sheet and show them all in the plan message. A flawed sheet propagates into
every block that references it, and this is the cheapest moment to re-roll.

---

## 5. Optional hero-frame lock

For the two blocks that carry the film — the **ring shot** and the **final face** —
you can generate the opening frame first and animate from it:

1. `create_image` with that block's hero-frame prompt (`style-dna.md` §Hero-frame
   template), `referenceImages: [style_key_url, …sheet_urls]`.
2. QC the frame; generate 2–3 variants and pick on numbers if it matters.
3. `create_video` with `image: <chosen frame URL>` and the same
   `referenceImages`.

`aspectRatio` **must be identical** in both calls or the frame gets cropped. The
lock costs one extra image and buys precision on composition and palette; skip it
on routine blocks, where a text-only `create_video` with the style key attached is
enough.

---

## 6. Blocks — `create_video` (+ QC)

| Param | Value |
|---|---|
| `prompt` | This block's animation prompt, verbatim |
| `model` | `"seedance-2.0"` (not `-fast`, not `-mini`; the prompts are written for full) |
| `aspectRatio` | The run's ratio, identical on every block |
| `duration` | `10` — one beat, one block. (Range is 1–20; the whole story engine and the centring maths assume 10) |
| `resolution` | `"720p"` on every call, held across the film |
| `generateAudio` | `true` — the native paper foley and impact SFX are the clip's audio bed |
| `referenceImages` | `[style_key_url, …this block's sheet URLs]`, max 9 |
| `image` | Only on hero-frame-locked blocks. Otherwise omit |
| `lastImage` | **Always omit.** Never chain block → block; the wipe bookends are the join |
| `negativePrompt` | Optional; the AI-default negative already lives in the prompt body |

**Slot maths for binding sheets in the prompt:** `image` is @Image1 when present, so
the first `referenceImages` entry is @Image2 (and @Image1 when `image` is omitted).
Count the slots for each block and write the prompt against those numbers — a prompt
that says "@Image2" when the sheet actually landed in @Image1 binds nothing.

`wait_for_video` → `curl -L -o clips/block_04.mp4 "<VIDEO_URL>"` → QC:

```bash
python scripts/qc.py video clips/block_04.mp4 --ground '#DCC0A0' --accent '#A02D19' --void '#1B2740'
```

It reports specs (warns off 24fps), the exposure swing (flags a flat clip under 80 —
usually a global exposure lock in the prompt), the wipes it detects with colour and
duration, per-second motion (a frozen full-detail second is the "hold" bug; a flat
field is a legitimate wipe), the time-averaged palette share, and whether the audio
carries a sustained drone versus legitimate paper-impact body. For a block that
bookends a join, confirm the first ~0.25s and/or last ~0.4s read as a flat field.

Report the numbers honestly, failures included, and name the prompt line that caused
any drift.

---

## 7. Narration — `create_voiceover`

`list_voiceover_voices` first. In app-capable hosts it renders a picker with
tap-to-play previews — if the user is choosing, show it and say nothing more; don't
repeat the twenty voices as a list. If you are choosing (the default), pick a
storyteller and note the `voice_id`.

| Param | Value |
|---|---|
| `text` | One block's narration line. Plain spoken text — no stage directions, no parentheticals, numbers spelled out |
| `voice_id` | One of the twenty Eleven v3 voices. **The same one on every block** |
| `stability` | `0.6` — steady narrator. Lower drifts theatrical, higher goes flat |
| `similarity` | Leave default |

One call per **voiced** block; generate nothing for a wordless block.
`wait_for_voiceover` → `curl -L -o vo/vo_04.mp3 "<AUDIO_URL>"`, then measure:

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 vo/vo_04.mp3
```

Record `vo_dur` per block. **5–8s is the target, ≈9.5s the ceiling** inside a 10s
window. Over the ceiling: cut a clause or merge two sentences and re-voice that
block, or speed-fit it in the mix (§11).

`<#0.5#>` between two words inserts a half-second pause — useful at a threshold
line, but it spends the same window the end silences do.

---

## 8. Music — `create_music` (optional)

Off by default: the native foley carries this style. If a bed is wanted:

| Param | Value |
|---|---|
| `prompt` | Named instruments, tempo, and an arc — e.g. "low frame drum and a single bowed string, slow, building to one struck hit"; add "instrumental, no vocals" |
| `model` | `"mureka-7.5"` — the instrumental BGM model. Omit `lyrics` |
| `output_format` | `"mp3"` |

`wait_for_music` → `curl -L -o music.mp3 "<URL>"`. Vague "epic music" comes back as
formless drone; name the instruments and the arc. The song models (`mureka-9`, `-8`,
`-o2`, `-7.6`, `auto`) require lyrics and add vocals — never use them for a bed. The
bed rarely matches runtime: loop (`-stream_loop -1`) or trim (`-t`) it in the mix.

---

## 9. Manifest schema

```json
{
  "project": "fenrir-diorama-myth",
  "myth": "The binding of Fenrir — Gylfaginning variant",
  "aspect_ratio": "16:9",
  "resolution": "720p",
  "block_seconds": 10,
  "palette": { "name": "Glacier", "ground": "#DDE6EC", "accent": "#A02D19", "void": "#241F1B" },
  "style_key": { "generation_id": null, "url": null, "path": "style_key.png", "status": "pending" },
  "voice": { "voice_id": "George", "stability": 0.6 },
  "music": { "source": "none | unsora_create_music", "file": null },
  "talisman": "the silk-thin chain",
  "total_seconds": 80,
  "assets": [
    { "name": "fenrir", "kind": "creature", "used_in_blocks": [1,3,4,5,6,7,8],
      "sheet_prompt": "…", "generation_id": null, "url": null,
      "path": "sheets/fenrir.png", "status": "pending" }
  ],
  "blocks": [
    { "n": 1, "beat": "cold open", "event": "the wolf snaps the second chain",
      "assets": ["fenrir", "chain"], "wipe_in": null, "wipe_out": "accent",
      "vo_line": "They told him it was a game. They had told him that twice before.",
      "vo_generation_id": null, "vo_file": "vo/vo_01.mp3", "vo_dur": 6.4,
      "hero_frame": null, "video_prompt": "…",
      "video_generation_id": null, "video_url": null, "clip_path": "clips/block_01.mp4",
      "start_ms": 0, "vo_offset_ms": 1800, "qc": null, "status": "pending" }
  ]
}
```

Block `status`: `pending` → `vo_done` → `video_queued` → `video_done` → `qc_done` →
`done` (or `failed` + `error`). Asset `status`: `pending` → `queued` → `done` /
`failed`. No block generates until the style key and every asset it lists are
`done`. `wipe_in`/`wipe_out` carry the join colour; `null` means block 1's cold open
or block N's final image.

---

## 10. ffmpeg — concat

Blocks share codec, resolution and fps (same model, same ratio, same duration), so
a stream copy works. Order from the manifest, never a directory listing, and
zero-pad the numbers so a glob sorts correctly.

```bash
cd <agent-workspace>/diorama-myth
: > concat_list.txt
for f in clips/block_*.mp4; do printf "file '%s'\n" "$f" >> concat_list.txt; done
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy cut.mp4
```

Each join is wipe-bookended — the outgoing clip ends on a flat join-colour field and
the incoming opens on the same flat colour — so the cut lands between two identical
flat frames and is invisible. **No crossfade**: it would double the wipe and read as
mush. Spot-check every seam afterwards; a hard jump means the bookends didn't land
or the colours mismatched, so re-render the offending block.

Fallback if `-c copy` errors on a mismatch:

```bash
ffmpeg -y -f concat -safe 0 -i concat_list.txt \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 192k -movflags +faststart cut.mp4
```

---

## 11. ffmpeg — VO placement and mix

**The centring maths.** Each block is a fixed 10s window and its take sits in the
middle of it, so the block opens and closes on pure foley:

```
start_ms      = (n - 1) * 10000
vo_offset_ms  = start_ms + (10000 - round(vo_dur * 1000)) / 2
```

A 6.4s take in block 3 lands at `20000 + (10000 - 6400)/2 = 21800 ms`, with 1.8s of
paper foley at each end. Wordless blocks contribute no input at all.

**Normalise every take first** so the duck behaves:

```bash
for f in vo/vo_*.mp3; do
  ffmpeg -y -i "$f" -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 "${f%.mp3}_n.wav"; done
```

**Speed-fit only a take over the ≈9.5s ceiling** (pitch-safe, keep `atempo` ≤ 1.15;
re-voicing shorter is always better):

```bash
ffmpeg -y -i vo/vo_05_n.wav -filter:a "atempo=1.10" vo/vo_05_fit.wav
```

**Mix** — narration on top, native clip SFX under it but still punchy (this style
wants the impacts louder than Vox-style foley: they *are* the action). Example: an
8-block film where blocks 5 and 7 are wordless, no music bed.

```bash
ffmpeg -y -i cut.mp4 \
  -i vo/vo_01_n.wav -i vo/vo_02_n.wav -i vo/vo_03_n.wav -i vo/vo_04_n.wav \
  -i vo/vo_06_n.wav -i vo/vo_08_n.wav \
  -filter_complex "\
    [1:a]adelay=1800|1800[a1];[2:a]adelay=11600|11600[a2];\
    [3:a]adelay=21800|21800[a3];[4:a]adelay=31500|31500[a4];\
    [5:a]adelay=51900|51900[a6];[6:a]adelay=72000|72000[a8];\
    [a1][a2][a3][a4][a6][a8]amix=inputs=6:normalize=0[vo];\
    [0:a]volume=0.45[sfx];\
    [sfx][vo]amix=inputs=2:duration=first:normalize=0[out]" \
  -map 0:v -map "[out]" -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

**With a music bed**, add it as an input, duck it under the narration, and keep it
well below the foley:

```bash
ffmpeg -y -i cut.mp4 -stream_loop -1 -i music.mp3 \
  -i vo/vo_01_n.wav -i vo/vo_02_n.wav \
  -filter_complex "\
    [2:a]adelay=1800|1800[a1];[3:a]adelay=11600|11600[a2];\
    [a1][a2]amix=inputs=2:normalize=0[vo];\
    [1:a]volume=0.35[mus];\
    [mus][vo]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[musd];\
    [0:a]volume=0.45[sfx];\
    [sfx][musd][vo]amix=inputs=3:duration=first:normalize=0[out]" \
  -map 0:v -map "[out]" -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

`normalize=0` is not optional — without it `amix` divides by the input count and the
whole film drops about 6 dB. Keep the narration at unity; tune `[0:a]volume` for how
hard the paper impacts hit.

---

## 12. Optional burned subtitles

Off by default. If the film is headed for silent autoplay, write an ASS file from
the block lines and their offsets and burn it in one pass:

```bash
ffmpeg -y -i final.mp4 -vf "ass=subs.ass" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a copy s.mp4 && mv s.mp4 final.mp4
```

Style them to the film, not to a default: a heavy condensed face, the ground colour
on a flat accent card, no drop shadow, no outline glow. Time each caption to its
take's `vo_offset_ms` and `vo_dur` — the timings are already in the manifest.

---

## 13. Verification

Run before presenting. A concat that silently drops a clip yields a valid file that
is simply short.

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 final.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of default=nw=1 final.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,channels -of default=nw=1 final.mp4
```

Duration should be within ±0.5s of `N × 10`; anything larger means a clip came back
the wrong length. `width,height` must be identical across every clip. Optionally run
`python scripts/qc.py video final.mp4 --ground … --accent … --void …` for a
whole-film read: a good film shows a luma swing well over 80 and one detected wipe
per seam plus the internal ones.

---

## 14. Resume after failure

Read `blocks.json` and regenerate only what isn't `done`.

- Style key or an asset not `done` → do those first; nothing downstream is valid
  without them.
- `vo_done` → skip the voiceover, start at `create_video`.
- `video_queued` with an id → call `wait_for_video` again; the job may still be
  alive.
- `video_done` → skip to QC.
- `qc_done` for every block → just re-run the concat and the mix.
- `failed` → read the error. A content rejection needs a prompt edit, not a retry; a
  timeout needs a retry.

**Never regenerate a `done` block "for consistency".** Each block is an independent
generation, a re-roll comes back different, and it would break the bookend colour
match with its neighbours. Re-verify duration and seams after any repair.

---

## 15. Moderation and IP

The style is the safety margin here: it is abstract by construction, so myth's
violence renders as **paper events** and clears moderation while staying on-style.

| Write this | Not this |
|---|---|
| a vermilion paper shard where the blade fell | blood, a wound, gore |
| a silhouette and a scatter of punched confetti | a decapitation described anatomically |
| stacked wavy card rising over the boat | a realistic drowning |
| a figure of card unfolding into a tree of card | a body described as flesh transforming |
| flat shards blowing outward from the strike | an explosion with smoke and fire |

If a job comes back `FAILED` with no useful error, the first suspect is a line that
described gore rather than paper. Rewrite it as shards and silhouette and resubmit
that block alone.

**IP.** Render every figure from the **tradition's own iconography** — what the myth
and its historical art describe. Never name a studio, a film, or a specific
copyrighted character design, and never describe a character "as they appear in"
one. A generic Norse wolf built of cardstock is fine; a named animated wolf is not.
The style references in `style-dna.md` §9 are craft references for lighting and
camera, and belong in prompts only as they are written there.

---

## 16. Cost

Credits are spent in exactly four places, and Unsora's pricing moves, so **read the
balance rather than quoting a rate you assume**:

- `get_credits` before Phase 4 for the balance in the plan message, and again at the
  end for the actual spend.
- **Video dominates.** N × one 10s Seedance 2.0 clip at 720p is the overwhelming
  majority of any run — an 8-block film is 8 clips. Re-rolls are the thing that
  blows a budget, which is why the style key and the sheets are QC'd first: they are
  one image each and they prevent whole-clip re-rolls.
- **Images are cheap** — the style key, the sheets, and any hero-frame lock.
- **Voiceover is trivial**: 6 credits per started 1,000 characters, and a whole myth
  narration is well under 2,000 characters. Never trade narration quality for
  credits.
- **Music** only if requested.

Phases S, L, P, 2, 3 and the entire ffmpeg assembly are free. If `get_subscription`
shows an inactive plan or the balance won't cover the block count, say so **before**
generating anything rather than stopping half a film in.

---

## 17. Optional posting

Publishing needs its own explicit yes, separate from the yes to generate.

1. `get_subscription` → confirm `isActive`.
2. `get_accounts` → list connected accounts.
3. `create_post` needs a reachable `mediaUrl`; a local MP4 won't do. If there's no
   public URL, say so and ask how they want to host it.
4. `create_post` with `accountIds`, `caption`, `mediaType: "video"`, `mediaUrl`, and
   optional scheduling.
5. Confirm with `list_posts`. Draft the caption; let the user edit it before it goes
   out.
