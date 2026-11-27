# Palette

The colour system is the spine of this style. Lock ONE palette at the front door
and hold it across the whole film. State it three ways in every hero-frame prompt
and restate it in every animation prompt.

## The structure

| role | hex | luma | hue | sat |
|---|---|---|---|---|
| ground | `#DCC0A0` kraft cream | 196.7 | 32° | 46% |
| accent | `#A02D19` brick vermilion | 77.1 | 9° | 73% |
| void | `#1B2740` midnight navy | 38.3 | 221° | 41% |

Three facts that matter more than the hexes:

1. **Ground and accent are the same hue family** — 32° and 9°, only 23° apart. The
   vermilion is the cream's own hue, saturated and dropped 120 in value. That unity
   is why the frame reads as one material rather than three colours sitting next to
   each other.
2. **The void is the outsider** — 221°, a full 148° across from the accent. It is
   depth, not shadow.
3. **Accent and void are both dark** — 77 and 38, only 39 apart. They separate by
   *hue*, not value. All the light lives in the ground.

## Why this palette and not another

At full chroma, each hue sits at a fixed luma. This is fixed by the eye, not taste:

| hue | luma at full chroma | slot |
|---|---|---|
| yellow | 225.9 | ground (desaturate → cream) |
| cyan | 178.8 | ground |
| orange | 151.4 | — none |
| green | 149.7 | — none |
| magenta | 105.3 | accent (a little bright) |
| **red** | **76.2** | **accent — target is 77.1** |
| violet | 67.3 | accent |
| **blue** | **29.1** | **void — target is 38.3** |

Pure red lands at 76.2. The accent slot is 77.1. **Red is the only hue that is
simultaneously at full chroma and at the accent's value.** Every other warm hue is
too bright, and darkening it to 77 destroys its chroma — a saturated dark yellow is
brown sludge, not an accent.

So cream/vermilion/navy is roughly what falls out of the luma geometry when you
demand three tiers at maximum chroma. **Your freedom is in the ground and the void.
The accent is nearly locked to red** (violet at 67 is the only real alternative).

## The five palettes

All measured on the same subject with the same prompt, palette only swapped. Share
is ground/accent/void against a 45/35/20 target. Offer these by name and feel — the
user doesn't need the hexes to choose.

| name | ground | accent | void | measured | reads as |
|---|---|---|---|---|---|
| **Reference** | `#DCC0A0` cream | `#A02D19` vermilion | `#1B2740` navy | 43/43/15 | cosmic, stage, the original |
| **Sable** | `#D5B7E4` lilac | `#981898` violet | `#232B12` moss | **44/35/21** | dusk, fairytale, no red or blue at all |
| **Cobalt** | `#DCC0A0` cream | `#A02D19` vermilion | `#152C31` deep teal | **48/32/20** | oceanic, harbour, storm |
| **Iris** | `#DCC0A0` cream | `#6B3389` violet | `#16301C` forest | 44/35/22 | nocturne, woodland |
| **Glacier** | `#B8CCD6` ice | `#A02D19` vermilion | `#33230F` bitumen | 38/41/21 | arctic; inverts the temperature axis |

**Sable is the strongest result in testing** and the most surprising, because it
contains none of the original colours. It works because it is the reference's
*exact* geometry — ground and accent 20° apart, void opposing at 140° —
transplanted wholesale onto the violet/green axis. That's the best evidence that
the structure, not the hues, is the style.

**Cobalt** is the reference with the void rotated from navy to teal: 179° of
opposition, the strongest of any palette here.

**Glacier** is the odd one out and worth understanding. Its void (bitumen, 28°)
sits only 19° from its accent — almost no opposition. It still works because its
*ground* opposes the accent instead (ice at 205° vs red at 9°). So the rule isn't
"the void must oppose the accent" — it's **something must**. Reference and Sable use
the void; Glacier uses the ground.

### The failure case

| Foxglove | `#DCC0A0` cream | `#A02D19` vermilion | `#16301C` forest | 33/50/17 | **fails** |

Swapping only the void from navy to forest looked like the safest possible change
and was the worst: cream collapsed to 33% while vermilion ran to 50%. Cream sits at
32°, forest at 95°, red at 9° — *nothing* opposes the accent, so it floods. Compare
Iris, which uses the same forest void successfully because its violet accent (300°)
is 155° away from it.

**Whatever you build, check that one thing opposes the accent by roughly 140°+.**

## What the reference actually averages

Before treating 45/35/20 as sacred — the two reference films disagree:

| film | ground | accent | void |
|---|---|---|---|
| Astronaut | 45.0 | 27.1 | 28.0 |
| Kabuki | 41.6 | 51.2 | 7.2 |

The **ground is the constant** — 42–45% in both. The accent/void split is wildly
free: Astronaut is void-heavy, Kabuki is accent-heavy by seven to one. So 45/35/20
is a useful prompt target that produces balanced frames, not a law. If a film wants
to be accent-red or void-blue, let it — just hold the ground near 45%.

## Picking a palette for a myth

Lock one and hold it for the whole film. The choice is a reading of the myth's
**world and its cost**, not of its nationality — pick for what the story is made of.

| The myth's world | Palette | Why |
|---|---|---|
| Fire, forge, blood-debt, siege, war, the underworld's heat | **Reference** (cream / vermilion / navy) | The vermilion is the story's own violence; navy gives it somewhere to fall |
| Dusk, enchantment, trickster tales, curses, the fairytale register | **Sable** (lilac / violet / moss) | No red and no blue anywhere — it reads as *other* before anything happens |
| Sea, storm, flood, harbour, a serpent in deep water | **Cobalt** (cream / vermilion / teal) | The teal void is depth with a floor to it |
| Forest, night, the hunt, the grove, a descent into the dark | **Iris** (cream / violet / forest) | Violet accent keeps blood off the palette when the story isn't about blood |
| Ice, mountain, exile, binding, the long cold ending | **Glacier** (ice / vermilion / bitumen) | Inverts the temperature axis: the light is cold, the wound is warm |

Three tie-breakers when two fit:

1. **What is the wound?** If something bleeds, breaks or burns on screen, the accent
   is that event's colour and wants to be vermilion. If the cost is grief, exile or
   transformation rather than injury, violet carries it better.
2. **What is the dark?** The void is where the myth's threat lives — water, night,
   earth, tar. Pick the void for the threat, then check it still opposes the accent
   by roughly 140°.
3. **Does the transformation need to read?** A body becoming a tree, a woman becoming
   a spider — the new form has to separate from the old at a glance, so favour the
   palette where ground and accent sit furthest apart in value (Glacier, Sable).

Whatever you pick, say the name and the three hexes in the plan message, then never
revisit it: a palette change mid-film is a re-roll of every block.

## Building a new palette

`scripts/palette.py` solves for hexes at the right values:

```bash
python scripts/palette.py --ground-hue 150 --accent-hue 168 --void-hue 18
```

It takes hue angles and returns hexes that hit 197/77/38 at the reference
saturations, and warns if the void doesn't oppose the accent or the accent hue is
out of the red/violet region. Sanity-check the result against the three facts above.

## Writing it into a prompt

State the palette **three ways** in the same hero-frame prompt. Each catches a
different failure:

1. **The hexes with their ranges** — `kraft cream (base #DCC0A0, highlights to
   #F9E9C5, shadows to #8C5B44)`.
2. **The colour budget as percentages** — `roughly 45% cream, 35% vermilion, 20%
   navy. All three must be strongly present.`
3. **The exclusion** — `no other hue anywhere in frame; no pure white; no pure
   black.` When swapping palettes, name the colour you removed: `NO BLUE ANYWHERE —
   the dark colour here is green, not navy.` Without that, the model reaches for
   navy out of habit.

Restate at least the percentages and the exclusion in the **animation** prompt too
— the hero image constrains the first frame far more than the last, so the palette
drifts across the clip if the video prompt doesn't hold it.
