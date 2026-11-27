# Style DNA — Layered Cut-Paper Diorama (Myth)

The locked visual system. Read this fully before writing a prompt — the
specificity **is** the craft, and this style is a **specification, not a vibe**:
its palette, exposure and pacing are all measurable, and every failure is a number
drifting off target. State targets as numbers; adjectives don't survive the trip
to the model, percentages do.

Contents: the locked slots · the AI-default betrayal + its negative · paper logic
(including creatures, water, fire, wounds and transformation) · the palette
(pointer) · exposure · the wipe wording · **the style-key prompt** · hero-frame
template · **the block-prompt template + a worked mythic example** ·
reference-sheet formats · style-specific failure rows · the per-block checklist.

A note on units: a **block** is one 10-second `create_video` generation and one
story beat. Everything below is written per block.

---

## The locked slots (never vary within a film; only their contents change)

**1. Medium & texture.** A **layered cut-paper diorama rendered in 3D** — every
object built from **stacked sheets of matte cardstock** with **visible cut edges**
and **soft contact shadows** between the layers. Not real stop-motion, not a photo,
not a flat illustration: a physical-looking paper set photographed as a tabletop
miniature. Fine paper-fibre grain, very light vignette. The signature is the cut
edge and the contact shadow between stacked layers — their absence is what makes AI
output look like clean CGI or a flat vector.

**2. Palette — three colours and no others.** Ground / accent / void at fixed luma
(197 / 77 / 38), roughly 45% / 35% / 20% of the frame **time-averaged across the
film**. No fourth hue anywhere, no pure white, no pure black. This replaces any
"one accent colour" thinking — the whole colour system is these three. Full maths,
the five tested palettes, and how to write it three ways: **`palette.md`**.

**3. Composition & scale.** **Hard vertical symmetry**, a **tiny figure dead
centre** of a **huge symmetrical world**, the set receding around them. Head-on
wide for the establish; the world resolving into **concentric rings** for the
top-down hero shot. The format's signature is one small protagonist dwarfed by an
enormous concentric set.

**4. Camera.** 24mm equivalent, **deep focus throughout** so every cut edge stays
crisp front to back. Locked-off (but alive) for the establish; **handheld only
through the action beat**, bouncing on physical events (every step, every plank
seam), not wandering; a stable crane climb to the top-down; a smooth push into the
face. **Pin every move to a timecode and forbid it pausing** — unpinned moves
stall or arrive late.

**5. Lighting.** Broad soft key with generous bounce; shadows soft, short and
open, **never black**. Fully matte surfaces — **no specular, no gloss, no lens
flare**. The darkest value is a soft void colour, the brightest a warm off-ground;
nothing crushes to pure black or blows to pure white.

**6. Exposure — it swings, hard.** See below. Lock the palette ratio on the hero
frame; let the film swing luma ~150 around it. Never lock exposure per-frame.

**7. Motion grammar.** Native **24fps** (don't ask for 30, don't step-print).
Something moves every second that isn't a wipe — but **never write "hold"**, the
model freezes on a full-detail frame. Give micro-motion (drifting punched dust, a
trembling paper fringe, an idling shiver, fluttering exhaust). The action beat is
where the incident lives: blows land, heads erupt, shards blow at the lens.

**8. Audio grammar.** In the *video* prompt: **`No music. No voice.`** — any
narration is a separate track laid on in post, and the score (if any) is a separate
Unsora `create_music` bed added in the mix. What the clip generates natively is
**anime-fight impact SFX + dry paper foley**, boxed close: a sharp whoosh on every
fast camera move and paper wipe, a metallic ring on a draw, a heavy bass-boosted
impact on each strike, a rising charge-up swell before the big hit, a low boom on
the eruption — every sound short and performed as if on real paper (stiff card
sliding and snapping, flat card slaps, punch-out confetti scattering, pages
riffling). Sync the SFX to the beats: whoosh into each wipe, biggest impact on the
eruption or overhead reveal, one resonant hit on the final push into the face, then
a short tail. **Ban the drone's *sustain*, not its frequency** — paper impacts
carry legitimate low body ("heavy card dropped flat"); "no sub bass" strips that and
leaves the foley thin. Use "no sustained tone, no cinematic drone, no continuous
hum".

**9. Style references.** Paper-craft animation photographed as a tabletop
miniature — Kubo and the Two Strings-style stop-motion craft (Frank Passingham),
Robert Yeoman centred symmetry, a Busby Berkeley overhead kaleidoscope for the
top-down, Barry Ackroyd / Hurt Locker handheld **only** through the action beat.
Never lead with a live-action or photoreal reference — it pulls the model toward
depth and gloss.

**10. Text / titles.** This style is **image-led, not type-led** — default to
**no on-screen text at all** (any explanation lives in the VO). If the user asks
for a title card, set it as a **physical cut-paper word** built from the same
cardstock and palette, laid flat on the set — never a clean vector overlay.

---

## The AI-default betrayal (put the negative in EVERY hero-frame prompt)

The betrayal: the model renders this as a **glossy CGI or photoreal scene** with
**specular highlights, real smoke/volumetrics, lens flare, and depth-of-field**,
or as a **flat vector illustration** — losing the stacked matte cardstock and the
cut edges. Two secondary betrayals: it **floods the frame with the ground colour**
(so the accent and void vanish) and it **drifts dark** on interiors and close-ups.

The negatives that beat it — in every hero-frame prompt:

> *Layered cut-paper diorama rendered in 3D — every object built from stacked
> sheets of matte cardstock with visible cut edges and soft contact shadows between
> the layers. Fully matte, no specular, no gloss, no lens flare. No smoke, no
> volumetrics, no fog — an explosion is flat paper shards, not a cloud. No
> photoreal materials, no depth-of-field. No text, no watermark, no logos. No pure
> white, no crushed blacks, no colours outside the three.*

If a block still drifts glossy or dark, add "fully matte cardstock, broad soft key,
nothing crushes to black" and re-state the exposure block.

---

## Paper logic (everything in frame obeys it, or the illusion dies)

- Sky is **horizontal bands of stacked card**, not a gradient.
- Stars, dust and debris are **punched shapes**.
- The sun, a lamp, a moon: **a flat disc**.
- Craters, rings, drums, stairwells: **stacked concentric rings of cut plank**.
- An explosion is **flat shards**, never smoke or volumetrics.
- Sparks are **punch-out confetti**.
- Surfaces are fully matte — no specular, no gloss, no lens flare.
- When a **new element enters mid-block**, say explicitly that it too is built from
  the same stacked cardstock in the same three colours — otherwise the model
  introduces a photoreal object or a fourth hue.

### Myth's own vocabulary (name these, every time one appears)

Myth asks for five things an explainer never does. Each has one correct paper
translation, and stating it is what keeps the film in the medium:

- **Creatures** are built from **overlapping cut scales, plates or fringes of
  card** — a serpent is a chain of stacked crescents, a wolf a silhouette of
  layered fur-cut edges, a giant a stack of slab shapes. Say *how the creature is
  cut*, not what animal it resembles. Silhouette is everything: cut paper reads at
  a glance or not at all, so give the creature one unmistakable outline and keep it.
- **Water** is **stacked wavy cards in overlapping ranks**, each rank a flat
  cut-out with a visible edge — a wave is card sliding over card, a flood is ranks
  advancing, never a fluid sim, never foam, never spray.
- **Fire** is **layered flame-shaped cut-outs in the accent**, stepping in size,
  with punched-confetti sparks. Never glow, never volumetric light, never smoke.
- **Wounds and death** are **a vermilion paper shard** at the point of the blow and
  a **scatter of punched confetti** — abstract by construction. This is the whole
  moderation strategy and the whole aesthetic strategy at once. Never anatomical.
- **Transformation** — the thing this style does better than any other — is **one
  stack of card replaced by another, layer by layer, in frame**: the figure's
  sheets peel, slide out of the silhouette and reassemble into the new shape. Say
  the layers do the changing. Never a morph, never a dissolve, never a glow.

The **talisman** — the one object that travels the whole film — is a cut-paper prop
with a fixed silhouette and its own sheet. Name it in every block by its shape, and
name what state it is in: intact, cracked, lit, taken, given.

---

## Exposure — the swing is the style

| | luma range | swing |
|---|---|---|
| reference | 40 → 191 | **~150** |
| a flat, dead clip | 108 → 164 | ~56 |

The 45/35/20 palette ratio is a **time-average, not a per-frame lock**. The film
earns that average by swinging: void-heavy in one beat (62% void), ground-flooded
in another (99% ground). **Lock the ratio on the hero frame; let the film swing.**
Instructing "hold the balance every frame" bans the swing and produces the flat
clip. Interiors (stairwell, drum, vault) and close-ups drift two stops under unless
the exposure block is in from the first attempt and the close-up is pinned "as
bright as the opening".

---

## The paper wipe (the wording)

Describe the **physical event, not the edit**: the camera flies into a sheet of
cardstock that fills the frame; for ~0.4–0.5s there is nothing but flat paper; then
it pulls back into the new scene. Give the colour and the duration explicitly.
**Cream/ground wipes into bright scenes, vermilion/accent wipes into dark ones.**

Within a block:

> At 0:06 the camera rushes straight into a blank sheet of cream cardstock that
> fills the entire frame — for 0.5 seconds the screen is nothing but flat cream
> paper, no detail — then it pulls back out into: [next scene in the same block].

Between blocks (the bookend join — how the concat cut is hidden):

- **Tail of the outgoing clip:** the clip ENDS by rushing into a flat field —
  > The final 0.4 seconds: the camera rushes straight into a blank sheet of
  > [join-colour] cardstock filling the entire frame; the clip ends on flat
  > [join-colour] paper, no detail at all.
- **Head of the incoming clip:** the clip OPENS on the same flat field —
  > The clip opens on ~0.25 seconds of flat [join-colour] paper filling the entire
  > frame, no detail, then pulls back out into: [this block's tableau].

Because both sides of the concat cut are the same flat colour, the cut is
invisible; the two halves read as one continuous ~0.5s wipe. **The join colour is
set by the incoming beat and must match on both sides.** The first block cold-opens
(no leading wipe); the last block lands on the face and ends on it (no trailing wipe).

---

## Style key (Unsora `create_image`, `nano-banana-pro`) — Phase 1

The style key is **one image that encodes the whole visual system**, generated
before anything else and passed in `referenceImages` on every block. Its job is not
to be a shot from the film: it is a palette-and-material swatch with enough scene in
it that the model reads construction, exposure and colour off it at once. Generate
it at the run's aspect ratio, QC it, and re-roll it rather than living with it.

Substitute the palette hexes and generate as-is:

```
A layered cut-paper diorama rendered in 3D — a small symmetrical world built
entirely from stacked sheets of matte cardstock, photographed as a tabletop
miniature. A tiny cut-paper figure stands dead centre, back to camera, dwarfed by
concentric stacked-card terraces receding around and behind them; a flat disc sun
low in a sky of horizontal stacked card bands; punched-shape dust drifting in the
air; a scatter of flat paper shards frozen mid-air at the left edge.

COLOUR BUDGET — hit these proportions closely: roughly 45% of the frame is
[GROUND NAME], roughly 35% is [ACCENT NAME], roughly 20% is [VOID NAME]. All three
must be strongly present. Do NOT let [GROUND] flood the frame — the [ACCENT] wash
and the [VOID] elements have to carry real area.

EXPOSURE: mid-key, evenly lit, target average brightness around 60% — bright enough
that every cut edge is legible, never washed out. Nothing crushes to pure black and
nothing blows to pure white: the darkest value is a soft [VOID], the brightest a
warm off-[GROUND]. No hot white highlights anywhere.

Strict three-colour palette and nothing else:
[GROUND] (base #XXXXXX, highlights to #XXXXXX, shadows to #XXXXXX),
[VOID] (base #XXXXXX, never below #XXXXXX),
[ACCENT] (base #XXXXXX, shadows to #XXXXXX).
[IF SWAPPED: NO [REMOVED COLOUR] ANYWHERE — the dark colour here is X, not Y.]
No other hue anywhere in frame.

Every object is built from stacked sheets of matte cardstock with visible cut edges
and soft contact shadows between the layers. Fully matte surfaces, no specular, no
gloss, no lens flare. Fine paper-fibre grain, very light vignette. 24mm equivalent,
deep focus so every cut edge stays crisp front to back. Broad soft key with generous
bounce; shadows soft, short and open, never black.

This is the master style reference for a paper-craft short film.

No text, no watermark, no logos, no smoke or volumetrics, no depth-of-field, no
crushed blacks, no blown white highlights, no colours outside the three.
Aspect ratio [16:9 / 9:16 / 1:1].
```

Then measure it before spending on anything else:
`python scripts/qc.py frame style_key.png --ground '#…' --accent '#…' --void '#…'`

---

## Hero-frame prompt template (Unsora `create_image`, `nano-banana-pro`)

Used for the **optional hero-frame lock** on the two blocks that carry the film —
the ring shot and the final face — and for nothing else. Everywhere else the block
prompt plus the style key is enough.

Order: Subject → Colour budget → Exposure → Medium/paper-logic → Composition →
Lighting → Constraints. Adapt; don't paste.

```
[If a sheet is bound: Match the design and identity of @Image1 exactly — the sheet
is the design source for this figure/place, not the composition; pose ONE instance
as described below.]

[SUBJECT: one or two sentences. The world, built of stacked cardstock. The figure
(tiny, dead centre, back to camera for a wide; or filling frame for a face). The
concentric geometry receding around them. The accent light source and what it
washes. The single frozen event this frame shows.]

COLOUR BUDGET — hit these proportions closely: roughly 45% of the frame is
[GROUND NAME], roughly 35% is [ACCENT NAME], roughly 20% is [VOID NAME]. All three
must be strongly present. Do NOT let [GROUND] flood the frame — the [ACCENT] wash
and the [VOID] elements have to carry real area.

EXPOSURE: mid-key, evenly lit, target average brightness around 60% — bright
enough that every cut edge is legible, never washed out. Nothing crushes to pure
black and nothing blows to pure white: the darkest value is a soft [VOID], the
brightest a warm off-[GROUND]. No hot white highlights anywhere.

Layered cut-paper diorama rendered in 3D — every object built from stacked sheets
of matte cardstock with visible cut edges and soft contact shadows between the
layers. Strict three-colour palette and nothing else:
[GROUND] (base #XXXXXX, highlights to #XXXXXX, shadows to #XXXXXX),
[VOID] (base #XXXXXX, never below #XXXXXX),
[ACCENT] (base #XXXXXX, shadows to #XXXXXX).
[IF SWAPPED FROM REFERENCE: NO [REMOVED COLOUR] ANYWHERE — the dark colour here is
X, not Y.] No other hue anywhere in frame. Everything obeys paper logic — [name the
specific translations: the wall is stacked concentric rings of cut plank, the crowd
is punched shapes, the lamp is a flat disc, the blast is flat shards not smoke].
Fully matte surfaces, no specular, no gloss, no lens flare. Fine paper-fibre grain,
very light vignette.

Composition: [symmetrical head-on wide, figure on the exact centre, rings receding
around them] / [extreme close-up on the face, flat paper features, accent across
the eyes]. 24mm equivalent, deep focus so every cut edge stays crisp front to back.

Lighting: broad soft key with generous bounce, shadows soft, short and open — never
black.

This is one frame of a paper-craft short film.

No text, no watermark, no logos, no lens flare, no gloss, no smoke or volumetrics,
no depth-of-field, no crushed blacks, no blown white highlights, no colours outside
the three. Aspect ratio [16:9 / 9:16 / 1:1].
```

**Interior sets go dark** — put the exposure block in from attempt one, don't wait
to see it fail. **Then measure before animating:**
`python scripts/qc.py frame v1.png v2.png v3.png --ground '#…' --accent '#…' --void '#…'`

---

## Block prompt template (Unsora `create_video`, `seedance-2.0`, 10s)

One per block. This is the workhorse — every block gets one, with or without a hero
frame. **Structure a 10s block as event → wipe → event → wipe → event**, plus its
join bookends: three nameable things happen, and no single camera move is asked to
carry the window. Restate the palette (a reference image constrains the opening far
more than the ending). Pin camera moves to timecodes. Name both wipe bookends.
Adapt; don't paste.

```
Paper-craft animation photographed as a tabletop miniature — Kubo and the Two
Strings-style stop-motion, Robert Yeoman centred symmetry[, a Busby Berkeley
overhead kaleidoscope]. Native 24fps.

The reference images are the style and design source. The block matches their
palette, paper construction, cut-edge layering and lighting precisely — every new
element that enters frame must be built
from the same stacked matte cardstock in the same three colours ([GROUND],
[ACCENT], [VOID]). Roughly [45% GROUND / 35% ACCENT / 20% VOID]; the exposure may
swing but no fourth hue, no pure white, no crushed black.

[Sheet binding, one line per sheet, by slot: @ImageN is the [figure / creature /
place / talisman]; keep its identity, design and silhouette exactly, and pose ONE
instance as described below. Never re-describe its design.]

Camera: 24mm wide, deep focus throughout. [Locked-off but alive] / [handheld riding
the action close with organic bounce, Barry Ackroyd / Hurt Locker-style, ONLY
through the action] / [a stable crane climb — the crane starts at 0:0X and does not
pause or slow] / [a smooth push into the close-up].

[HEAD WIPE, only if this block bookends an incoming join: The clip opens on ~0.25
seconds of flat [JOIN-COLOUR] paper filling the entire frame, no detail, then pulls
back out into the scene.]

[0:00–0:03] EVENT ONE. [The nameable thing that happens. Micro-motion from frame
one — punched dust drifting, a paper fringe trembling, the talisman swinging on its
cord. NEVER the word "hold".]

[INTERNAL PAPER WIPE at 0:03: the camera rushes straight into a blank sheet of
[COLOUR] cardstock filling the entire frame — for 0.4 seconds nothing but flat
paper, no detail — then pulls back out into:]

[0:03–0:06] EVENT TWO. [The escalation, at a different scale from event one —
whiplash it: giant face → ant-sized figure → colossal creature.]

[INTERNAL PAPER WIPE at 0:06, same wording, [COLOUR].]

[0:06–0:10] EVENT THREE. [The pay-off of the block. The biggest impact sits here
unless the tail wipe takes it.]

[TAIL WIPE, only if this block bookends an outgoing join: The final 0.4 seconds —
the camera rushes straight into a blank sheet of [JOIN-COLOUR] cardstock that fills
the entire frame; the clip ends on flat [JOIN-COLOUR] paper, no detail at all.]

Audio: NO MUSIC of any kind, no dialogue, no sustained tone, no cinematic drone, no
continuous hum. Every sound is short, dry paper foley and anime-style impact SFX
performed on real paper, boxed close — [name each object and gesture: stiff card
sliding and snapping for the draw, flat card slaps for the blows, punch-out confetti
scattering for sparks, a heavy card dropped flat for each impact, pages riffling far
above]. A sharp whoosh into each paper wipe and fast camera move; the biggest impact
on [the eruption / the overhead reveal]; one clean hit on the final push-in, then a
short tail.
```

**Do NOT add a global exposure lock** — it reads as sensible and kills the film.
The swing is the style. **Then QC:**
`python scripts/qc.py video clips/block_NN.mp4 --ground '#…' --accent '#…' --void '#…'`

**Never** put a VO line inside the block prompt. `No voice.` is load-bearing — the
narration and the score are separate tracks added in the mix.

---

### Worked example — Fenrir, block 5 of 8 (the third binding)

Palette **Glacier**: ground ice `#DDE6EC`, accent vermilion `#A02D19`, void bitumen
`#241F1B`. Sheets bound: `[style_key, fenrir_sheet, chain_sheet]` with no `image`,
so **@Image1 = style key, @Image2 = Fenrir, @Image3 = the chain**. Wipes: in on
vermilion (a dark beat), out on vermilion. Narration for this block: *"The third
chain was thin as breath. That was how they knew it would hold."* (6.1s, centred at
41.95s.)

```
Paper-craft animation photographed as a tabletop miniature — Kubo and the Two
Strings-style stop-motion, Robert Yeoman centred symmetry. Native 24fps.

The reference images are the style and design source. The block matches their
palette, paper construction, cut-edge layering and lighting precisely — every new
element that enters frame must be built from the same stacked matte cardstock in
the same three colours (ice, vermilion, bitumen). Roughly 45% ice, 35% vermilion,
20% bitumen; the exposure may swing but no fourth hue, no pure white, no crushed
black. NO BLUE ANYWHERE — the dark colour here is bitumen brown, not navy.

@Image2 is the wolf: keep its identity, its layered fur-cut silhouette and its
scale exactly as built, and pose ONE instance as described. @Image3 is the chain —
a single hair-thin ribbon of cut card with a visible edge; keep its silhouette.

Camera: 24mm wide, deep focus throughout. Locked-off but alive for the ring, then
handheld riding the action close with organic bounce, Barry Ackroyd / Hurt
Locker-style, ONLY from 0:06.

The clip opens on ~0.25 seconds of flat vermilion paper filling the entire frame,
no detail, then pulls back out into: a ring of stacked-card gods, each a flat
silhouette, standing on concentric ice-coloured terraces around the wolf at dead
centre.

[0:00–0:03] EVENT ONE. The god steps forward and offers the hair-thin chain across
his open palms. Punched-shape snow drifts continuously through the frame; the
wolf's fur-cut fringe trembles; the ring of silhouettes shifts its weight.

At 0:03 the camera rushes straight into a blank sheet of vermilion cardstock
filling the entire frame — for 0.4 seconds nothing but flat paper, no detail —
then pulls back out into:

[0:03–0:06] EVENT TWO. Extreme scale flip: the wolf's open jaw fills the entire
frame, built of layered cut teeth, and one small god's hand — a flat cut shape —
lays itself between them. The jaw's layers slide closed one rank at a time.

At 0:06 the camera rushes straight into a blank sheet of vermilion cardstock
filling the entire frame for 0.4 seconds, no detail, then pulls back out into:

[0:06–0:10] EVENT THREE. Wide again, handheld. The wolf hauls against the chain;
the terraces judder; a single vermilion paper shard flicks out where the hand was
and a scatter of punch-out confetti blows toward the lens. The chain does not
break.

The final 0.4 seconds: the camera rushes straight into a blank sheet of vermilion
cardstock that fills the entire frame; the clip ends on flat vermilion paper, no
detail at all.

Audio: NO MUSIC of any kind, no dialogue, no sustained tone, no cinematic drone, no
continuous hum. Every sound is short, dry paper foley and anime-style impact SFX
performed on real paper, boxed close — stiff card sliding and snapping as the chain
is offered, a light card flutter for the drifting snow, a heavy card dropped flat as
the jaw closes, punch-out confetti scattering on the shard, a deep flat card slam as
the wolf hauls. A sharp whoosh into each paper wipe; the biggest impact on the jaw
closing at 0:06, then a short tail.
```

Read it against the checklist below before generating: medium sentence, negative,
palette three ways including the removed colour, exposure implied by the style key
and never locked, sheets bound by slot and never re-described, three events, two
internal wipes, both bookends in vermilion, camera pinned, no "hold", `No voice.`

---

## The talisman / prop sheet (Unsora `create_image`, `1:1`)

The travelling object needs its own sheet — it appears in every block and must be
recognisable at any scale, so it gets a silhouette lock of its own:

```
Prop reference sheet, 1:1, centred on a plain [GROUND] paper ground. [The object]
built from stacked matte cardstock with visible cut edges, shown three ways: a
straight-on view, a three-quarter view, and a close detail. [Shape, proportion,
the one feature that makes its silhouette unmistakable at small scale.] Strict
three-colour palette — [GROUND], [ACCENT], [VOID], no other hue. Fully matte, soft
contact shadows, fine paper grain. No hand, no figure, no background scene, no
text.
```

If the talisman **changes state** at the crisis — cracked, lit, unravelled, halved —
generate the second state as its own sheet from the same prompt with the change
described, and bind whichever state that block needs. A talisman that changes
without a second sheet drifts into a different object.

---

## Reference-sheet formats (Unsora `create_image`, always 16:9)

For any recurring **character** or **place** flagged by the tally, generate a sheet
**once** before any block, QC it, show it to the user, then pass its URL into every
block that uses it. Sheets are always `16:9` regardless of the film's ratio.

**Recurring character (as a cut-paper figure):**

```
Character reference sheet, 16:9, on a plain [GROUND] paper ground. The SAME figure
built from stacked matte cardstock with visible cut edges, shown three ways left to
right: full-body front, full-body back, and a head-and-shoulders close-up. [Age,
build, silhouette, costume, defining features]. Strict three-colour palette —
[GROUND], [ACCENT], [VOID], no other hue. Fully matte, cut edges and soft contact
shadows, fine paper grain. Neutral pose, no background scene, no text.
```

**Recurring place / set:**

```
Location reference sheet, 16:9, on a plain [GROUND] paper ground. [The place] as a
layered cut-paper master set — [key stacked-card elements and their arrangement, the
concentric geometry]. Strict three-colour palette [GROUND] / [ACCENT] / [VOID], no
other hue; fully matte, visible cut edges, soft contact shadows. Flat paper logic
throughout, no text. This is the design source for the place across blocks.
```

Show each finished sheet to the user before proceeding — a flawed sheet propagates
into every block that references it, so this is the cheapest moment to re-roll.

**Binding a sheet in a block:** pass the sheet URL in `referenceImages` on
`create_video` (and on `create_image` too if the block is hero-frame-locked), then
bind it in the prompt **by slot number**: "@ImageN is the [figure]; keep its
identity, design and silhouette exactly, and pose ONE instance as described."

Slot maths, and it is worth counting every time: on `create_video`, `image` is
@Image1 when present, so the first `referenceImages` entry is @Image2 — but with no
`image`, the first entry is @Image1. The style key rides in `referenceImages` on
every block, so it occupies a slot too. Write the prompt against the numbers you
actually sent; a prompt binding "@Image2" when the sheet landed in @Image1 binds
nothing and the figure drifts.

Pass only the sheets a block actually uses — a dangling reference invites drift, and
Seedance caps `referenceImages` at nine.

---

## Style-specific failure rows (in addition to SKILL.md's table)

| Symptom | Cause | Fix |
|---|---|---|
| Renders as glossy CGI / photoreal | Medium & AI-default negative missing | Add "stacked matte cardstock, visible cut edges, soft contact shadows, fully matte, no specular/gloss/lens-flare, no photoreal materials" |
| An explosion is smoke, not shards | Paper logic not stated for the new element | "the blast is flat paper shards, punch-out confetti sparks — no smoke, no volumetrics, no fog" |
| Frame/clip too dark | No exposure block, or interior default | Exposure block from attempt one; "broad soft key, nothing crushes to black"; pin close-ups "as bright as the opening" |
| Ground floods; accent & void vanish | Too many ground cues; ratio not stated | State the colour budget as percentages; "do NOT let ground flood — accent and void must carry real area" |
| A fourth colour / accent floods | Void doesn't oppose accent | Check one colour opposes the accent ~140° (see palette.md); name the removed colour explicitly |
| Camera move stalls / arrives late | Move unpinned | Pin to a timecode, forbid pausing |
| Motion flatlines; a frozen full-detail frame | The word "hold" appeared | Purge "hold"; give named micro-motion every second |
| Low drone under the biggest move | Seedance adds it unasked | Ban the sustain not the frequency: "no sustained tone, no cinematic drone, no continuous hum"; keep "heavy card dropped flat" |
| Foley too thin / weightless | Bass banned wholesale | Don't ban low frequency; ask for "heavy card dropped flat" so impacts keep body |
| Recurring figure/place changes between blocks | No sheet or sheet not bound | Sheet once; URL in `referenceImages` of both calls; bind by slot in both prompts |
| Visible hard cut at a join | Bookends missing / colours mismatched | Same flat join-colour on the outgoing tail and incoming head; verify flat head/tail fields |
| The creature's anatomy changes between blocks | Creature over-described in the prompt | One creature sheet, bound by slot; in the prompt say only what it does, never what it looks like |
| A transformation reads as a morph or dissolve | The layers weren't given the job | "the figure's stacked sheets peel and slide out of the silhouette one rank at a time and reassemble as [the new shape]" — never morph, never glow |
| Water looks like a fluid sim; fire glows | Paper logic not stated for them | Stacked wavy cards in overlapping ranks; layered flame-shaped cut-outs in the accent with punched-confetti sparks |
| The talisman is a different object each block | No prop sheet, or a state change with no second sheet | Its own 1:1 sheet, bound everywhere; a second sheet for its changed state |
| A block flags or fails with no error | Violence written as gore, not as paper | A vermilion shard and punched confetti; silhouette, never anatomy |

## Per-block checklist — before generating

- The block delivers **three** nameable events across its ten seconds, joined by two
  internal wipes. If you can only name one, it is a postcard — pack it or fold it.
- Medium sentence AND the AI-default negative are both in the prompt.
- Palette stated **three ways** (hexes+ranges, percentages, exclusion naming the
  removed colour), and restated in a hero-frame prompt if the block is locked.
- No global exposure lock anywhere; close-ups pinned "as bright as the opening".
- Paper logic named for every element, especially anything entering mid-block, and
  for every creature, wave, flame, wound and transformation.
- The talisman appears, and its state is named.
- Camera moves pinned to timecodes and forbidden to pause; handheld only on the
  action beat.
- If this block bookends a join: head and/or tail wipe written with the correct
  join-colour, matching the neighbouring block. Block 1 has no head wipe; block N has
  no tail wipe.
- Every sheet the block uses is in `referenceImages`, bound by the **slot number
  actually sent**, and the prompt describes only pose and action.
- The word "hold" appears nowhere; micro-motion is named instead.
- Audio block is native SFX + paper foley + **No music. No voice.**; drone sustain
  banned; impacts kept heavy.
- `aspectRatio` identical across the run, `resolution: "720p"`, `duration: 10`,
  `generateAudio: true`, `lastImage` omitted.
