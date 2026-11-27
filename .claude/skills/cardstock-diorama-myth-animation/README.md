# Cardstock Diorama Myth Animation

<p align="center">
  <img src="https://raw.githubusercontent.com/sadekxD/cardstock-diorama-myth/d4e46cf801a179cb736f21a45507a0fd7fe72404/assets/demo.gif" alt="Cut-paper diorama myth short film demo" width="360">
</p>

A Claude Code / Claude.ai **skill** that turns a single request — a myth, a premise, or nothing at all — into a finished, narrated mythic short film in a layered **cut-paper diorama** style: stacked matte cardstock worlds, a strict three-colour palette, exposure that swings, paper-wipe transitions hiding every seam, a storyteller's voiceover, and one assembled MP4.

Built for the **[Unsora](https://tryunsora.com) MCP** — all generation runs on Unsora (`create_image`, `create_video`, `create_voiceover`), and assembly runs locally with **ffmpeg**, giving full control over block windows, voiceover placement, and the mix.

## What it makes

Animation-movie storytelling, not an explainer: gods, monsters, heroes, folklore, origin myths and transformations, told in ten-second story beats. The signature look:

- Flat matte cardstock worlds with visible cut edges and soft contact shadows
- A strict **three-colour palette and no others**, with deliberate exposure swings
- A tiny figure dead-centre of a huge symmetrical set; a top-down concentric "ring" hero shot
- Scenes joined by invisible **paper wipes**, native paper foley and impact SFX
- A mythic narrator (~12–18 words per block, some blocks deliberately silent)
- Ends by landing on a face

The look is treated as a **specification, not a vibe** — palette, exposure and pacing are numbers, stated in the prompt and then measured against the output with the bundled QC script.

## When to use it

Ask for a myth, legend, fable, folktale or fairy-tale short; a cut-paper / papercraft animated story; "tell the story of X" as a video; or say **"run the cardstock diorama myth animation"** — the skill can propose myths itself.

Not for fact-driven explainers with charts and statistics.

## Pipeline

| Phase | What happens | Tools |
|---|---|---|
| S — Story | Use the given myth, or propose 4–6 and wait for a pick | reasoning + web search |
| L — Lore | Research the actual tradition: variants, names, iconography, the ending | web search |
| P — Palette | Lock one three-colour palette for the whole film | free |
| 1 — Style key | Generate the cardstock style key at the run's aspect ratio | `create_image` (`nano-banana-pro`) |
| 1b — Casting | Sheets for the protagonist, creatures, recurring places, the talisman | `create_image` (`nano-banana-pro`) |
| 2 — Beat sheet | N beats on the mythic arc, ~12–18 words each, 1–2 wordless | free |
| 3 — Block prompts | N prompts in the diorama language, wipe-bookended, sheets bound | free |
| 4 — Clips | N × 10s clips, style key + sheets on every one | `create_video` (`seedance-2.0`) |
| 5 — Voice | One storyteller (ElevenLabs Eleven v3), one take per voiced block | `create_voiceover` |
| 6 — Assemble | Concat clips, place + mix the takes, deliver one MP4 | **ffmpeg (local)** |

Defaults: 16:9, 1 minute (6 blocks; 8–12 recommended for a real arc), 720p, English narration, no subtitles, no music — seedance's native paper foley carries the sound.

## Requirements

- **Unsora MCP** connected and authenticated (`create_image`, `create_video`, `create_voiceover`, `list_voiceover_voices`, and the matching `wait_for_*` pollers)
- **Local `ffmpeg` and `ffprobe`** — not optional; they are the assembler
- **Web search** for the lore pass on real traditions
- Recommended: `python3` with `numpy`, `pillow`, `scikit-learn` and `curl` for the automated QC pass

## Install

Place the skill folder in your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/sadekxD/cardstock-diorama-myth.git ~/.claude/skills/cardstock-diorama-myth-animation
```

Then invoke it from Claude Code, e.g. *"Tell the story of Icarus as a cut-paper short"* or *"run the cardstock diorama myth animation"*.

## Repository contents

- [SKILL.md](SKILL.md) — the complete skill definition: operating mode, story engine, narration rules, paper-wipe joins, the full phase-by-phase pipeline, failure handling, and delivery format
- [references/style-dna.md](references/style-dna.md) — the full cardstock visual system: paper logic, exposure swing, camera and motion vocabulary, the style-key prompt, the block-prompt template, and the per-block checklist
- [references/palette.md](references/palette.md) — the palette maths, five tested palettes plus one documented failure, and palette-by-myth-world guidance
- [references/unsora.md](references/unsora.md) — exact Unsora call templates for every phase, the job/polling model, moderation and IP map, cost arithmetic, and every ffmpeg command for the assembly
- [scripts/qc.py](scripts/qc.py) — measures frames and clips against the palette, exposure and wipe targets
- [scripts/palette.py](scripts/palette.py) — solves a new three-colour palette at the right luma values
