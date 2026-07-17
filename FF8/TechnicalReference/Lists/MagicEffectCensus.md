---
layout: default
parent: List
title: Magic effect census
permalink: /technical-reference/list/magic-effect-census/
---

Every entry of the battle magic-effect dispatch table, classified. This is the map of the effect
system: which of the 345 slots exist, what shape each one's code is, which are free for custom
spells, and — importantly — **which of the community IDB's function names were wrong**.

1. TOC
{:toc}

## Ground truth: the dispatch table, not the names

An effect is selected by the kernel magic entry's **effect_id** (field +0x04), which indexes two
parallel 400-slot function-pointer tables in `.data`:

| Global | Address | Content |
|---|---|---|
| `MagicList_Logic` | 0xC81774 | the effect's init/logic fn — `MagicList_Logic[id-1]` |
| `MagicList_TextureLoad` | 0xC81DB8 | its texture loader (`_FL`) — loads `mag(id-1).tim` |

Three independent facts pin every slot, and they agree:

1. the **dispatch index** (`0xC81774 + 4·(id−1)`);
2. the **`mag(N−1).tim` rule** — effect 23's loader really does open `mag022.tim`;
3. **adjacency** — the `_FL` sits exactly `0x20` before its `_Init` (holds for 164 slots; the
   exceptions are loaders that open several files, e.g. Devour's opens five).

> **Never trust a `MAG_nnn_*` name.** 51 of the 345 init functions carried a *wrong* id (see
> below). The loaders, the block prefixes (`MAG_023_sub_*`) and the table were right; only the
> hand-written init names drifted.

## The mislabelling (fixed 2026-07-16)

**51 of 345 logic/init functions were named with the wrong effect id** — not by a constant shift,
but as **swaps and cycles** (23↔31, 8↔79, and a 29→43→62→34→29 ring), which is the signature of
someone hand-naming from a mis-ordered list. Each fix below is corroborated by the effect's own
texture loader; all are applied in the IDB with an `_Init` suffix.

| id | effect | address | was named | now |
|---|---|---|---|---|
| 8 | Doom | `0x8c4980` | `MAG_079_GRIEVER_DEATH` | `MAG_008_DOOM_Init` |
| 9 | Doom Activation | `0x8c0380` | `MAG_092_ANGELO_SEARCH` | `MAG_009_DOOM_ACTIVATION_Init` |
| 14 | Death/Death Stone | `0x8b68c0` | `MAG_009_DOOM_ACTIVATION` | `MAG_014_DEATH_DEATH_STONE_Init` |
| 23 | Psycho Blast | `0x893020` | `MAG_031_HEARTBREAK` | `MAG_023_PSYCHO_BLAST_Init` |
| 27 | Full-Life | `0x883110` | `MAG_024_ESUNA` | `MAG_027_FULLLIFE_Init` |
| 29 | Wind Blast | `0x8794a0` | `MAG_043_MELTING_BUBBLE` | `MAG_029_WIND_BLAST_Init` |
| 31 | Heartbreak | `0x86c9e0` | `MAG_023_PSYCHO_BLAST` | `MAG_031_HEARTBREAK_Init` |
| 34 | Pain | `0x865600` | `MAG_029_WIND_BLAST` | `MAG_034_PAIN_Init` |
| 41 | Dribble | `0x8465c0` | `MAG_027_FULLLIFE` | `MAG_041_DRIBBLE_Init` |
| 43 | Melting Bubble | `0x839940` | `MAG_062_DEVOUR` | `MAG_043_MELTING_BUBBLE_Init` |
| 47 | Curse | `0x82a7f0` | `MAG_014_DEATH_DEATH_STONE` | `MAG_047_CURSE_Init` |
| 50 | Potion/Potion+ | `0x81fa10` | `MAG_041_DRIBBLE` | `MAG_050_POTION_POTION_Init` |
| 52 | X-Potion | `0x817410` | `MAG_050_POTION_POTION` | `MAG_052_XPOTION_Init` |
| 53 | Mega-Potion | `0x811f70` | `MAG_058_ELIXIR` | `MAG_053_MEGAPOTION_Init` |
| 54 | Everyone's Grudge | `0x80cab0` | `MAG_052_XPOTION` | `MAG_054_EVERYONES_GRUDGE_Init` |
| 57 | Treatment | `0x7fd150` | `MAG_054_EVERYONES_GRUDGE` | `MAG_057_TREATMENT_Init` |
| 58 | Elixir | `0x7f7cb0` | `MAG_059_MEGALIXIR` | `MAG_058_ELIXIR_Init` |
| 59 | Megalixir | `0x7f2810` | `MAG_053_MEGAPOTION` | `MAG_059_MEGALIXIR_Init` |
| 62 | Devour | `0x7e4b00` | `MAG_034_PAIN` | `MAG_062_DEVOUR_Init` |
| 67 | Remedy/Remedy+ | `0x7dea20` | `MAG_057_TREATMENT` | `MAG_067_REMEDY_REMEDY_Init` |
| 73 | Mighty Guard (Quistis) | `0x7cbdb0` | `MAG_067_REMEDY_REMEDY` | `MAG_073_MIGHTY_GUARD_QUISTIS_Init` |
| 74 | LV?Death (Quistis) | `0x7c4460` | `MAG_047_CURSE` | `MAG_074_LVDEATH_QUISTIS_Init` |
| 78 | Mighty Guard | `0x7be2d0` | `MAG_073_MIGHTY_GUARD_QUISTIS` | `MAG_078_MIGHTY_GUARD_Init` |
| 79 | Griever Death | `0x7b4bd0` | `MAG_008_DOOM` | `MAG_079_GRIEVER_DEATH_Init` |
| 80 | Ultimecia Junctioning to Griever | `0x7ab560` | `MAG_085_THE_END` | `MAG_080_ULTIMECIA_JUNCTIONING_TO_GRIEVER_Init` |
| 83 | Absorbed into time... | `0x7976c0` | `MAG_074_LVDEATH_QUISTIS` | `MAG_083_ABSORBED_INTO_TIME_Init` |
| 84 | Angel Wing | `0x78d7b0` | `MAG_096_MOOGLE_DANCE` | `MAG_084_ANGEL_WING_Init` |
| 85 | The End | `0x7844a0` | `MAG_086_ANGELO_CANNON` | `MAG_085_THE_END_Init` |
| 86 | Angelo Cannon | `0x77f250` | `MAG_091_ANGELO_RUSH` | `MAG_086_ANGELO_CANNON_Init` |
| 91 | Angelo Rush | `0x759370` | `MAG_093_ANGELO_RECOVER` | `MAG_091_ANGELO_RUSH_Init` |
| 92 | Angelo Search | `0x755130` | `MAG_083_ABSORBED_INTO_TIME` | `MAG_092_ANGELO_SEARCH_Init` |
| 93 | Angelo Recover | `0x74e390` | `MAG_094_ANGELO_REVERSE` | `MAG_093_ANGELO_RECOVER_Init` |
| 94 | Angelo Reverse | `0x7475f0` | `MAG_080_ULTIMECIA_JUNCTIONING_TO_GRIEVER` | `MAG_094_ANGELO_REVERSE_Init` |
| 96 | Moogle Dance | `0x731de0` | `MAG_084_ANGEL_WING` | `MAG_096_MOOGLE_DANCE_Init` |
| 151 | Cannon Blow | `0x60c9c0` | `MAG_168_SLEEPING_GAS` | `MAG_151_CANNON_BLOW_Init` |
| 152 | Ultrasonic Waves | `0x60afb0` | `MAG_186_BLASTER` | `MAG_152_ULTRASONIC_WAVES_Init` |
| 157 | Breath | `0x603e90` | `MAG_169_GASTRIC_JUICE` | `MAG_157_BREATH_Init` |
| 168 | Sleeping Gas | `0x5e1750` | `MAG_151_CANNON_BLOW` | `MAG_168_SLEEPING_GAS_Init` |
| 169 | Gastric Juice | `0x5dee60` | `MAG_170_ACID` | `MAG_169_GASTRIC_JUICE_Init` |
| 170 | Acid | `0x5dc930` | `MAG_181_KAMIKAZE` | `MAG_170_ACID_Init` |
| 173 | Ice Breath | `0x5d74b0` | `MAG_152_ULTRASONIC_WAVES` | `MAG_173_ICE_BREATH_Init` |
| 174 | Degenerator | `0x5d45a0` | `MAG_173_ICE_BREATH` | `MAG_174_DEGENERATOR_Init` |
| 176 | Sand Storm | `0x5d00f0` | `MAG_174_DEGENERATOR` | `MAG_176_SAND_STORM_Init` |
| 180 | Suicide | `0x5cc840` | `MAG_176_SAND_STORM` | `MAG_180_SUICIDE_Init` |
| 181 | Kamikaze | `0x5cb550` | `MAG_157_BREATH` | `MAG_181_KAMIKAZE_Init` |
| 186 | Blaster | `0x5bf6f0` | `MAG_180_SUICIDE` | `MAG_186_BLASTER_Init` |
| 188 | Shot - Normal Shot | `0x5be340` | `MAG_192_SHOT__SCATTER_SHOT` | `MAG_188_SHOT__NORMAL_SHOT_Init` |
| 192 | Shot - Scatter Shot | `0x5b96f0` | `MAG_193_SHOT__DARK_SHOT` | `MAG_192_SHOT__SCATTER_SHOT_Init` |
| 193 | Shot - Dark Shot | `0x5b7190` | `MAG_196_SHOT__QUICK_SHOT` | `MAG_193_SHOT__DARK_SHOT_Init` |
| 194 | Shot - Flame Shot | `0x5b4c60` | `MAG_197_SHOT__ARMOR_SHOT` | `MAG_194_SHOT__FLAME_SHOT_Init` |
| 196 | Shot - Quick Shot | `0x5b1900` | `MAG_198_SHOT__HYPER_SHOT` | `MAG_196_SHOT__QUICK_SHOT_Init` |

The practical consequence: **any earlier analysis that identified an effect by its IDB name may be
wrong.** The [Cure case study](../../battle/cure-case-study/) caught one instance of this
(`MAG_001_CURE` at 0x88CF70 was really Esuna's init); the census shows it was systemic.

## Archetype census

There are **three** archetypes, not four — and one of them dominates:

| Count | Archetype | Reference |
|---|---|---|
| 296 | **timeline** — frame counter + hardcoded thresholds | [Fire](../../battle/fire-case-study/), [Blizzard](../../battle/blizzard-case-study/), [Thundara](../../battle/thundara-case-study/) |
| 37 | **heal/status framework** — phase jump table, `Effect_AddTaskAndInitFromCtx`, 4 pools | [Cure](../../battle/cure-case-study/), Esuna (24) |
| 10 | **shared cinematic engine** — velocity integrator + byte-code VM on ctx `*0x27973EC` | [GF summons](../../battle/gf-summon-runtime/) |
| 2 | **free** (null dispatch) | ids 224, 225 |

The timeline count includes the **111 slots reached through a thunk**, all of which resolve to
timeline effects (below). **86% of the effect table is one archetype** — so the practical reading is
that FF8 has *one* general effect shape, plus a small heal/status framework and a 10-slot cinematic
engine for the marquee summons.

### "thunk" is not an archetype

An earlier revision of this page listed 111 **thunks** as a fourth family ("→ own-globals effect").
**That was a category error.** A thunk is a one-line forwarder — a calling-convention adapter that
casts its argument and tail-calls the real init:

```c
TaskQueueHeader *__cdecl MAG_102_THUNDARA(int cast_context) {
    return (TaskQueueHeader *)MAG_102_THUNDARA_Init(cast_context);
}
```

It says **nothing** about the effect's shape; the archetype is whatever the *target* is. The 14-byte
init size that the census keyed on is the size of the forwarder, not of the effect.

**All 111 have since been resolved** (2026-07-16) by following each thunk's call edge. Every one of
them lands on a **timeline** effect. The thunk group was never a family — it was a naming artifact.

The resolution is self-checking: **110 of the 111 targets carry a `MAG_nnn` prefix that matches the
dispatch id exactly** (effect 44's thunk calls `MAG_044_sub_6E7B10`, and so on). That is a third
independent confirmation of the dispatch table, alongside the `mag(N−1).tim` rule and `_FL`
adjacency. The single exception was `linkedToPhoenixPinion` — no id prefix at all — now renamed
`MAG_140_PHOENIX_PINION_REBIRTH_FLAME_Init`.

The thunk→target offset is **not** fixed, so the edge must be followed, not computed:

| Offset | Count |
|---|---|
| +0x30 | 94 |
| +0x10 | 14 |
| +0xD0 | 1 (effect 274) |
| +0xF0 | 1 (Quezacotl) |
| +0x130 | 1 (Phoenix) |

Six targets were read in full to check the classification rather than infer it from the address
region: Blizzara, Quezacotl, Diablos, Phoenix, 283 and 285. `MAG_103_BLIZZARA_Init` is
**structurally identical** to [Thundara's init](../../battle/thundara-case-study/) — own globals,
`0x14×1` root pool, `AddTaskToQueue(tick)`, camera track, TIM upload. `GF_116Quezacotl_SetupSummon`
has the same shape and **never touches `*0x27973EC`**, which settles the more interesting question
below.

### The thunked GF summons are timeline, not cinematic

Six of the 111 are GF summons — **Griever (69), Quezacotl (116), Phoenix (140), Carbuncle (278),
Pandemona (291), Diablos (325)**. They are *not* part of the shared cinematic engine: they live in
the `0x65`–`0x70` timeline region, they each drive their own globals and their own
`GF_*_SequenceTask`, and none of them reference the cinematic context `*0x27973EC`. Verified by
reading Quezacotl and Diablos.

> Effects **283 "Magic Summon"** and **285 "Thunder Summon"** are *not* summons despite their names
> in the effect-name list. Their inits (`MAG_283_sub_67C430`, `MAG_285_sub_67A890`) resolve only the
> caster entity and lack the target-centroid idiom below entirely — they are unremarkable timeline
> effects. A reminder that the effect *names*, like the old function names, are not evidence.

So the shared cinematic engine stays at its 10 slots (region `0xAE`–`0xB5`), and FF8's GFs are split
across **two unrelated implementations**. This matters for the 60 fps work: a single gate on the
cinematic context cannot reach the thunked GFs, which is consistent with the observed failure of
exactly that approach on Quezacotl.

Their inits also share a distinctive idiom — the summon **centres itself on the target centroid**:

```c
v3 = *(action_data + 16);                                  // target_count
do { v5 += 24; v2 += BattleEntitySlotData[targetData[i]].based_position_x; } while (--v6);
centroid_x = v2 / v3;                                      // Diablos also averages Z
```

Note this reads `+16` with a 24-byte stride — the Fire pattern, and independent corroboration that
`+16`/`+17` are distinct fields (see the
[Thundara case study](../../battle/thundara-case-study/#3-the-director-iterates-actions-not-targets)).

The archetype column is otherwise assigned by **structural signature** (init size, code region, pool
shape), not by reading each effect — it is a routing hint, not a proof.

## Free slots for custom spells

- **ids 224 and 225** — both dispatch pointers are NULL.
- **ids 346–400** — beyond the 345 used entries; both tables are sized 400.

That is **57 free effect ids**, each needing a logic fn + a loader fn wired into the two tables.

## The full table

`id` — effect_id (kernel magic +0x04). `mag file` = `id − 1`.

| id | effect | init | archetype |
|---|---|---|---|
| 1 | Cure | `0x8d6a00` `MAG_001_CURE_Init` | heal/status framework (Cure archetype) |
| 2 | Fire | `0x6298a0` `MAG_002_FIRE_Init` | timeline (Fire/Blizzard archetype) |
| 3 | Thunder | `0x700c10` `MAG_003_THUNDER` → `MAG_003_THUNDER_Init` | **timeline** (via thunk +0x10) |
| 4 | Double | `0x8d5080` `MAG_004_DOUBLE_Init` | heal/status framework (Cure archetype) |
| 5 | Phoenix Down | `0x8d4450` `—` | heal/status framework (Cure archetype) |
| 6 | Leviathan Summon (Tsunami) | `0xb58080` `MAG_006_LEVIATHAN_SUMMON_TSUNAMI` | shared cinematic engine |
| 7 | Mega Phoenix | `0x8ce3d0` `MAG_007_MEGA_PHOENIX` | heal/status framework (Cure archetype) |
| 8 | Doom | `0x8c4980` `MAG_008_DOOM_Init` | heal/status framework (Cure archetype) |
| 9 | Doom Activation | `0x8c0380` `MAG_009_DOOM_ACTIVATION_Init` | heal/status framework (Cure archetype) |
| 10 | Ray-Bomb | `0x627e60` `MAG_010_RAYBOMB` | timeline (Fire/Blizzard archetype) |
| 11 | Storm Breath | `0x6ea500` `MAG_011_STORM_BREATH` → `MAG_011_sub_6EA530` | **timeline** (via thunk +0x30) |
| 12 | Blade Shot | `0x6e8ae0` `MAG_012_BLADE_SHOT` → `MAG_012_sub_6E8AF0` | **timeline** (via thunk +0x10) |
| 13 | Dark Mist/Poison Mist | `0x8be1f0` `MAG_013_DARK_MIST_POISON_MIST` | timeline (Fire/Blizzard archetype) |
| 14 | Death/Death Stone | `0x8b68c0` `MAG_014_DEATH_DEATH_STONE_Init` | timeline (Fire/Blizzard archetype) |
| 15 | Draw | `0x8b0910` `MAG_015_DRAW` | timeline (Fire/Blizzard archetype) |
| 16 | Recover | `0x8ab140` `MAG_016_RECOVER` | heal/status framework (Cure archetype) |
| 17 | Elvoret Entrance | `0x7003c0` `MAG_017_ELVORET_ENTRANCE` → `MAG_017_sub_7003D0` | **timeline** (via thunk +0x10) |
| 18 | Elvoret Death | `0xb4a530` `MAG_018_ELVORET_DEATH` | shared cinematic engine |
| 19 | Raldo Ball | `0x8a32a0` `MAG_019_UNK0` | heal/status framework (Cure archetype) |
| 20 | NORG Pod Opening | `0x89fbc0` `MAG_020_NORG_POD_OPENING` | heal/status framework (Cure archetype) |
| 21 | Triple | `0x89def0` `MAG_021_TRIPLE` | timeline (Fire/Blizzard archetype) |
| 22 | Bio | `0x89a6b0` `MAG_022_BIO` | timeline (Fire/Blizzard archetype) |
| 23 | Psycho Blast | `0x893020` `MAG_023_PSYCHO_BLAST_Init` | timeline (Fire/Blizzard archetype) |
| 24 | Esuna | `0x88cf70` `MAG_024_ESUNA_Init` | heal/status framework (Cure archetype) |
| 25 | Cura | `0x889d60` `MAG_025_CURA` | heal/status framework (Cure archetype) |
| 26 | Clash | `0x8885d0` `MAG_026_CLASH` | timeline (Fire/Blizzard archetype) |
| 27 | Full-Life | `0x883110` `MAG_027_FULLLIFE_Init` | heal/status framework (Cure archetype) |
| 28 | Curaga | `0x87db10` `MAG_028_CURAGA` | heal/status framework (Cure archetype) |
| 29 | Wind Blast | `0x8794a0` `MAG_029_WIND_BLAST_Init` | heal/status framework (Cure archetype) |
| 30 | Counter Laser-Eye | `0x8735f0` `MAG_030_COUNTER_LASEREYE` | heal/status framework (Cure archetype) |
| 31 | Heartbreak | `0x86c9e0` `MAG_031_HEARTBREAK_Init` | timeline (Fire/Blizzard archetype) |
| 32 | Protect | `0x86b9a0` `MAG_032_PROTECT` | timeline (Fire/Blizzard archetype) |
| 33 | Shell | `0x866010` `MAG_033_SHELL` | timeline (Fire/Blizzard archetype) |
| 34 | Pain | `0x865600` `MAG_034_PAIN_Init` | heal/status framework (Cure archetype) |
| 35 | Life | `0x8649c0` `MAG_035_LIFE` | timeline (Fire/Blizzard archetype) |
| 36 | Confuse | `0x85f4e0` `MAG_036_CONFUSE` | heal/status framework (Cure archetype) |
| 37 | Drink Magic | `0x8569f0` `MAG_037_DRINK_MAGIC` | heal/status framework (Cure archetype) |
| 38 | Quake | `0x8d8510` `MAG_038_QUAKE` | heal/status framework (Cure archetype) |
| 39 | Drain | `0x8513d0` `MAG_039_DRAIN` | heal/status framework (Cure archetype) |
| 40 | Scan | `0x84d030` `MAG_040_SCAN` | heal/status framework (Cure archetype) |
| 41 | Dribble | `0x8465c0` `MAG_041_DRIBBLE_Init` | timeline (Fire/Blizzard archetype) |
| 42 | Shoot | `0x83ecc0` `MAG_042_SHOOT` | timeline (Fire/Blizzard archetype) |
| 43 | Melting Bubble | `0x839940` `MAG_043_MELTING_BUBBLE_Init` | heal/status framework (Cure archetype) |
| 44 | Junk | `0x6e7ae0` `MAG_044_JUNK` → `MAG_044_sub_6E7B10` | **timeline** (via thunk +0x30) |
| 45 | Stare | `0x836590` `MAG_045_STARE` | timeline (Fire/Blizzard archetype) |
| 46 | Sigh | `0x831b50` `MAG_046_SIGH` | timeline (Fire/Blizzard archetype) |
| 47 | Curse | `0x82a7f0` `MAG_047_CURSE_Init` | timeline (Fire/Blizzard archetype) |
| 48 | Magma Breath | `0x824cf0` `MAG_048_MAGMA_BREATH` | timeline (Fire/Blizzard archetype) |
| 49 | Resonance | `0x821540` `MAG_049_RESONANCE` | heal/status framework (Cure archetype) |
| 50 | Potion/Potion+ | `0x81fa10` `MAG_050_POTION_POTION_Init` | heal/status framework (Cure archetype) |
| 51 | Hi-Potion/Hi-Potion+ | `0x81c800` `MAG_051_HIPOTION` | heal/status framework (Cure archetype) |
| 52 | X-Potion | `0x817410` `MAG_052_XPOTION_Init` | heal/status framework (Cure archetype) |
| 53 | Mega-Potion | `0x811f70` `MAG_053_MEGAPOTION_Init` | timeline (Fire/Blizzard archetype) |
| 54 | Everyone's Grudge | `0x80cab0` `MAG_054_EVERYONES_GRUDGE_Init` | heal/status framework (Cure archetype) |
| 55 | Aqua Breath | `0x808820` `MAG_055_AQUA_BREATH` | timeline (Fire/Blizzard archetype) |
| 56 | Absorb | `0x803200` `MAG_056_ABSORB` | heal/status framework (Cure archetype) |
| 57 | Treatment | `0x7fd150` `MAG_057_TREATMENT_Init` | heal/status framework (Cure archetype) |
| 58 | Elixir | `0x7f7cb0` `MAG_058_ELIXIR_Init` | timeline (Fire/Blizzard archetype) |
| 59 | Megalixir | `0x7f2810` `MAG_059_MEGALIXIR_Init` | timeline (Fire/Blizzard archetype) |
| 60 | Unknown | `0x7eb090` `MAG_060_UNK1` | timeline (Fire/Blizzard archetype) |
| 61 | Revive | `0x7e58c0` `MAG_061_REVIVE` | heal/status framework (Cure archetype) |
| 62 | Devour | `0x7e4b00` `MAG_062_DEVOUR_Init` | timeline (Fire/Blizzard archetype) |
| 63 | Unknown | `0x6e6be0` `MAG_063_UNK2` → `MAG_063_sub_6E6C10` | **timeline** (via thunk +0x30) |
| 64 | Griever Tail Falling Off | `0x6e5180` `MAG_064_GRIEVER_TAIL_FALLING_OFF` → `MAG_064_sub_6E51B0` | **timeline** (via thunk +0x30) |
| 65 | Great Attractor | `0x6e0350` `MAG_065_GREAT_ATTRACTOR` → `MAG_065_sub_6E0380` | **timeline** (via thunk +0x30) |
| 66 | Griever + Ultimecia Death | `0x622610` `MAG_066_GRIEVER__ULTIMECIA_DEATH` | timeline (Fire/Blizzard archetype) |
| 67 | Remedy/Remedy+ | `0x7dea20` `MAG_067_REMEDY_REMEDY_Init` | heal/status framework (Cure archetype) |
| 68 | Unknown | `0x7dc1a0` `MAG_068_SCAN` | heal/status framework (Cure archetype) |
| 69 | Griever Summon | `0x6fe040` `MAG_069_GRIEVER_SUMMON` → `GF_069Griever_SetupSummon` | **timeline** (via thunk +0x10) |
| 70 | Shockwave Pulsar | `0x6dd8d0` `MAG_070_SHOCKWAVE_PULSAR` → `MAG_070_sub_6DD900` | **timeline** (via thunk +0x30) |
| 71 | Laser Eye (Quistis) | `0x7d6150` `MAG_071_LASER_EYE_QUISTIS` | heal/status framework (Cure archetype) |
| 72 | Aqua Breath (Quistis) | `0x7d1e80` `MAG_072_AQUA_BREATH_QUISTIS` | timeline (Fire/Blizzard archetype) |
| 73 | Mighty Guard (Quistis) | `0x7cbdb0` `MAG_073_MIGHTY_GUARD_QUISTIS_Init` | heal/status framework (Cure archetype) |
| 74 | LV?Death (Quistis) | `0x7c4460` `MAG_074_LVDEATH_QUISTIS_Init` | timeline (Fire/Blizzard archetype) |
| 75 | Hell's Judgement | `0xb3e8e0` `MAG_075_HELLS_JUDGEMENT` | shared cinematic engine |
| 76 | Ultimecia Final Form Spawn | `0x61f9a0` `MAG_076_ULTIMECIA_FINAL_FORM_SPAWN` | timeline (Fire/Blizzard archetype) |
| 77 | Ultimecia Final Form Death | `0xb302f0` `MAG_077_ULTIMECIA_FINAL_FORM_DEATH` | shared cinematic engine |
| 78 | Mighty Guard | `0x7be2d0` `MAG_078_MIGHTY_GUARD_Init` | heal/status framework (Cure archetype) |
| 79 | Griever Death | `0x7b4bd0` `MAG_079_GRIEVER_DEATH_Init` | timeline (Fire/Blizzard archetype) |
| 80 | Ultimecia Junctioning to Griever | `0x7ab560` `MAG_080_ULTIMECIA_JUNCTIONING_TO_GRIEVER_Init` | timeline (Fire/Blizzard archetype) |
| 81 | Unknown | `0x7a51b0` `MAG_081_UNK4` | heal/status framework (Cure archetype) |
| 82 | Ultimecia Blow Away Magic | `0x79ee30` `MAG_082_ULTIMECIA_BLOW_AWAY_MAGIC` | timeline (Fire/Blizzard archetype) |
| 83 | Absorbed into time... | `0x7976c0` `MAG_083_ABSORBED_INTO_TIME_Init` | timeline (Fire/Blizzard archetype) |
| 84 | Angel Wing | `0x78d7b0` `MAG_084_ANGEL_WING_Init` | timeline (Fire/Blizzard archetype) |
| 85 | The End | `0x7844a0` `MAG_085_THE_END_Init` | timeline (Fire/Blizzard archetype) |
| 86 | Angelo Cannon | `0x77f250` `MAG_086_ANGELO_CANNON_Init` | timeline (Fire/Blizzard archetype) |
| 87 | Angelo Strike | `0x773870` `MAG_087_ANGELO_STRIKE` | timeline (Fire/Blizzard archetype) |
| 88 | Invincible Moon | `0x7684f0` `MAG_088_INVINCIBLE_MOON` | timeline (Fire/Blizzard archetype) |
| 89 | Wishing Star | `0x6f9cf0` `MAG_089_WISHING_STAR` → `MAG_089_sub_6F9D00` | **timeline** (via thunk +0x10) |
| 90 | Tonberry Summon (Chef's Knife) | `0x762360` `MAG_090_TONBERRY_SUMMON_CHEFS_KNIFE` | timeline (Fire/Blizzard archetype) |
| 91 | Angelo Rush | `0x759370` `MAG_091_ANGELO_RUSH_Init` | timeline (Fire/Blizzard archetype) |
| 92 | Angelo Search | `0x755130` `MAG_092_ANGELO_SEARCH_Init` | timeline (Fire/Blizzard archetype) |
| 93 | Angelo Recover | `0x74e390` `MAG_093_ANGELO_RECOVER_Init` | timeline (Fire/Blizzard archetype) |
| 94 | Angelo Reverse | `0x7475f0` `MAG_094_ANGELO_REVERSE_Init` | timeline (Fire/Blizzard archetype) |
| 95 | Siren Summon (Silent Voice) | `0x739da0` `MAG_095_SIREN_SUMMON_SILENT_VOICE` | timeline (Fire/Blizzard archetype) |
| 96 | Moogle Dance | `0x731de0` `MAG_096_MOOGLE_DANCE_Init` | timeline (Fire/Blizzard archetype) |
| 97 | ChocoFire | `0x729a60` `MAG_097_CHOCOFIRE` | timeline (Fire/Blizzard archetype) |
| 98 | ChocoFlare | `0x721860` `MAG_098_CHOCOFLARE` | timeline (Fire/Blizzard archetype) |
| 99 | ChocoMeteor | `0x717d30` `MAG_099_CHOCOMETEOR` | timeline (Fire/Blizzard archetype) |
| 100 | ChocoBocle | `0x70d390` `MAG_100_CHOCOBOCLE` | timeline (Fire/Blizzard archetype) |
| 101 | Unknown | `0x6dd0c0` `MAG_101_UNK5` → `MAG_101_sub_6DD0F0` | **timeline** (via thunk +0x30) |
| 102 | Thundara | `0x6dc2d0` `MAG_102_THUNDARA` → `MAG_102_THUNDARA_Init` | **timeline** (via thunk +0x10) |
| 103 | Blizzara | `0x6da300` `MAG_103_BLIZZARA` → `MAG_103_BLIZZARA_Init` | **timeline** (via thunk +0x10) |
| 104 | Blizzaga | `0x6d6310` `MAG_104_BLIZZAGA` → `MAG_104_BLIZZAGA_Init` | **timeline** (via thunk +0x10) |
| 105 | Thundaga | `0x6d3db0` `MAG_105_THUNDAGA` → `MAG_105_THUNDAGA_Init` | **timeline** (via thunk +0x30) |
| 106 | Reflect | `0x6d2ae0` `MAG_106_REFLECT` → `MAG_106_sub_6D2AF0` | **timeline** (via thunk +0x10) |
| 107 | Demi | `0x6d1310` `MAG_107_DEMI` → `MAG_107_sub_6D1340` | **timeline** (via thunk +0x30) |
| 108 | Berserk | `0x6cfcd0` `MAG_108_BERSERK` → `MAG_108_sub_6CFD00` | **timeline** (via thunk +0x30) |
| 109 | Dispel | `0x6cf4a0` `MAG_109_DISPEL` → `MAG_109_sub_6CF4D0` | **timeline** (via thunk +0x30) |
| 110 | Biggs + Wedge 1st Death | `0x6ce210` `MAG_110_BIGGS__WEDGE_1ST_DEATH` → `MAG_110_sub_6CE240` | **timeline** (via thunk +0x30) |
| 111 | Aura | `0x6cd920` `MAG_111_AURA` → `MAG_111_sub_6CD950` | **timeline** (via thunk +0x30) |
| 112 | Meteor Barret (Zell's Finisher) | `0x6cbbe0` `MAG_112_UNK6` → `MAG_112_sub_6CBC10` | **timeline** (via thunk +0x30) |
| 113 | Bad Breath | `0x6cac20` `MAG_113_BAD_BREATH` → `MAG_113_sub_6CAC50` | **timeline** (via thunk +0x30) |
| 114 | Zombie | `0x6c99c0` `MAG_114_ZOMBIE` → `MAG_114_sub_6C99F0` | **timeline** (via thunk +0x30) |
| 115 | Float | `0x6c9380` `MAG_115_FLOAT` → `MAG_115_sub_6C93B0` | **timeline** (via thunk +0x30) |
| 116 | Quezacotl Summon (Thunder Storm) | `0x6c3550` `MAG_116_QUEZACOTL_SUMMON_THUNDER_STORM` → `GF_116Quezacotl_SetupSummon` | **timeline** (via thunk +0xf0) |
| 117 | Break | `0x6c16a0` `MAG_117_BREAK` → `MAG_117_sub_6C16D0` | **timeline** (via thunk +0x30) |
| 118 | Aero | `0x6c0c80` `MAG_118_AERO` → `MAG_118_sub_6C0CB0` | **timeline** (via thunk +0x30) |
| 119 | Stop | `0x6befd0` `MAG_119_STOP` → `MAG_119_sub_6BF000` | **timeline** (via thunk +0x30) |
| 120 | Petrify Stare | `0x6be960` `MAG_120_PETRIFY_STARE` → `MAG_120_sub_6BE990` | **timeline** (via thunk +0x30) |
| 121 | Blind | `0x6bde80` `MAG_121_BLIND` → `MAG_121_sub_6BDEB0` | **timeline** (via thunk +0x30) |
| 122 | Silence | `0x6bd8e0` `MAG_122_SILENCE` → `MAG_122_sub_6BD910` | **timeline** (via thunk +0x30) |
| 123 | Slow | `0x6bd1c0` `MAG_123_SLOW` → `MAG_123_sub_6BD1F0` | **timeline** (via thunk +0x30) |
| 124 | Flare | `0x6bbda0` `MAG_124_FLARE` → `MAG_124_sub_6BBDD0` | **timeline** (via thunk +0x30) |
| 125 | Haste | `0x6bb6b0` `MAG_125_HASTE` → `MAG_125_sub_6BB6E0` | **timeline** (via thunk +0x30) |
| 126 | Electric Discharge | `0x6b9a10` `MAG_126_ELECTRIC_DISCHARGE` → `MAG_126_sub_6B9A40` | **timeline** (via thunk +0x30) |
| 127 | Petrify Stare | `0x6b93a0` `MAG_127_PETRIFY_STARE` → `MAG_127_sub_6B93D0` | **timeline** (via thunk +0x30) |
| 128 | Gastric Juice | `0x6b7d00` `MAG_128_GASTRIC_JUICE` → `MAG_128_sub_6B7D30` | **timeline** (via thunk +0x30) |
| 129 | Breath | `0x6b4c00` `MAG_129_BREATH` → `MAG_129_sub_6B4C30` | **timeline** (via thunk +0x30) |
| 130 | Eerie Sound Wave | `0x6b4240` `MAG_130_EERIE_SOUND_WAVE` → `MAG_130_sub_6B4270` | **timeline** (via thunk +0x30) |
| 131 | Bad Breath | `0x6b2bd0` `MAG_131_BAD_BREATH` → `MAG_131_sub_6B2C00` | **timeline** (via thunk +0x30) |
| 132 | Disolving Acid | `0x6b19f0` `MAG_132_DISOLVING_ACID` → `MAG_132_sub_6B1A20` | **timeline** (via thunk +0x30) |
| 133 | Hypnotize | `0x6b0fb0` `MAG_133_HYPNOTIZE` → `MAG_133_sub_6B0FE0` | **timeline** (via thunk +0x30) |
| 134 | Beam Laser | `0x6b0070` `MAG_134_BEAM_LASER` → `MAG_134_sub_6B00A0` | **timeline** (via thunk +0x30) |
| 135 | Reflect Beam | `0x6aeea0` `MAG_135_REFLECT_BEAM` → `MAG_135_sub_6AEED0` | **timeline** (via thunk +0x30) |
| 136 | Oil Shot | `0x6ad1a0` `MAG_136_OIL_SHOT` → `MAG_136_sub_6AD1D0` | **timeline** (via thunk +0x30) |
| 137 | Oil Blast | `0x6ab850` `MAG_137_OIL_BLAST` → `MAG_137_sub_6AB880` | **timeline** (via thunk +0x30) |
| 138 | Saliva | `0x6a9f10` `MAG_138_SALIVA` → `MAG_138_sub_6A9F40` | **timeline** (via thunk +0x30) |
| 139 | Sonic Wave | `0x6a8830` `MAG_139_SONIC_WAVE` → `MAG_139_sub_6A8860` | **timeline** (via thunk +0x30) |
| 140 | Phoenix Pinion (Rebirth Flame) | `0x6a6300` `MAG_140_PHOENIX_PINION_REBIRTH_FLAME` → `MAG_140_PHOENIX_PINION_REBIRTH_FLAME_Init` | **timeline** (via thunk +0x130) |
| 141 | Renzokuken - 5 Hits | `0x61de70` `_HITS::MAG_141_RENZOKUKEN(void)` | timeline (Fire/Blizzard archetype) |
| 142 | Fira | `0x61ce10` `MAG_142_FIRA` | timeline (Fire/Blizzard archetype) |
| 143 | Firaga | `0x61bfe0` `MAG_143_FIRAGA` | timeline (Fire/Blizzard archetype) |
| 144 | Blizzard | `0x61aba0` `MAG_144_BLIZZARD` | timeline (Fire/Blizzard archetype) |
| 145 | Sleep | `0x6185d0` `MAG_145_SLEEP` | timeline (Fire/Blizzard archetype) |
| 146 | Tornado | `0x614d70` `MAG_146_TORNADO` | timeline (Fire/Blizzard archetype) |
| 147 | Regen | `0x614290` `MAG_147_REGEN` | timeline (Fire/Blizzard archetype) |
| 148 | Meltdown | `0x6120d0` `MAG_148_MELTDOWN` | timeline (Fire/Blizzard archetype) |
| 149 | Ultima | `0x60f690` `MAG_149_ULTIMA` | timeline (Fire/Blizzard archetype) |
| 150 | Gatling Gun | `0x60e340` `MAG_150_GATLING_GUN` | timeline (Fire/Blizzard archetype) |
| 151 | Cannon Blow | `0x60c9c0` `MAG_151_CANNON_BLOW_Init` | timeline (Fire/Blizzard archetype) |
| 152 | Ultrasonic Waves | `0x60afb0` `MAG_152_ULTRASONIC_WAVES_Init` | timeline (Fire/Blizzard archetype) |
| 153 | Sticky Web | `0x609640` `MAG_153_STICKY_WEB` | timeline (Fire/Blizzard archetype) |
| 154 | Ultra Waves | `0x607c10` `MAG_154_ULTRA_WAVES` | timeline (Fire/Blizzard archetype) |
| 155 | Sand Storm | `0x606cf0` `MAG_155_SAND_STORM` | timeline (Fire/Blizzard archetype) |
| 156 | Wild Cannon Blow | `0x605530` `MAG_156_WILD_CANNON_BLOW` | timeline (Fire/Blizzard archetype) |
| 157 | Breath | `0x603e90` `MAG_157_BREATH_Init` | timeline (Fire/Blizzard archetype) |
| 158 | Melt-Eye | `0x602ed0` `MAG_158_MELTEYE` | timeline (Fire/Blizzard archetype) |
| 159 | Renzokuken (vs X-ATM092) | `0x600bc0` `MAG_159_RENZOKUKEN_VS_XATM092` | timeline (Fire/Blizzard archetype) |
| 160 | Renzokuken - 4 Hits | `0x5ff080` `MAG_160_RENZOKUKEN__4_HITS` | timeline (Fire/Blizzard archetype) |
| 161 | Renzokuken (vs Elnoyle/Elvoret) | `0x5fd100` `MAG_161_RENZOKUKEN_VS_ELNOYLE_ELVORET` | timeline (Fire/Blizzard archetype) |
| 162 | Fated Circle | `0x5f90f0` `MAG_162_FATED_CIRCLE` | timeline (Fire/Blizzard archetype) |
| 163 | Rough Divide | `0x5f5b80` `MAG_163_ROUGH_DIVIDE` | timeline (Fire/Blizzard archetype) |
| 164 | Blasting Zone | `0x5f0260` `MAG_164_BLASTING_ZONE` | timeline (Fire/Blizzard archetype) |
| 165 | Lion Heart | `0x5e9470` `MAG_165_LION_HEART` | timeline (Fire/Blizzard archetype) |
| 166 | Megiddo Flame (Omega Weapon) | `0x5e4e90` `MAG_166_MEGIDO_FLAME` | timeline (Fire/Blizzard archetype) |
| 167 | Zantetsuken | `0x5e2a10` `MAG_167_ZANTETSUKEN` | timeline (Fire/Blizzard archetype) |
| 168 | Sleeping Gas | `0x5e1750` `MAG_168_SLEEPING_GAS_Init` | timeline (Fire/Blizzard archetype) |
| 169 | Gastric Juice | `0x5dee60` `MAG_169_GASTRIC_JUICE_Init` | timeline (Fire/Blizzard archetype) |
| 170 | Acid | `0x5dc930` `MAG_170_ACID_Init` | timeline (Fire/Blizzard archetype) |
| 171 | Poison Gas | `0x5db270` `MAG_171_POISON_GAS` | timeline (Fire/Blizzard archetype) |
| 172 | Morph | `0x5d9cd0` `MAG_172_MORPH` | timeline (Fire/Blizzard archetype) |
| 173 | Ice Breath | `0x5d74b0` `MAG_173_ICE_BREATH_Init` | timeline (Fire/Blizzard archetype) |
| 174 | Degenerator | `0x5d45a0` `MAG_174_DEGENERATOR_Init` | timeline (Fire/Blizzard archetype) |
| 175 | Holy | `0x5d1ad0` `MAG_175_HOLY` | timeline (Fire/Blizzard archetype) |
| 176 | Sand Storm | `0x5d00f0` `MAG_176_SAND_STORM_Init` | timeline (Fire/Blizzard archetype) |
| 177 | 1,000 Needles | `0x5cf760` `MAG_177_1000_NEEDLES` | timeline (Fire/Blizzard archetype) |
| 178 | 10,000 Needles | `0x5cedd0` `MAG_178_10000_NEEDLES` | timeline (Fire/Blizzard archetype) |
| 179 | Unknown | `0x5cdf40` `MAG_179_UNK7` | timeline (Fire/Blizzard archetype) |
| 180 | Suicide | `0x5cc840` `MAG_180_SUICIDE_Init` | timeline (Fire/Blizzard archetype) |
| 181 | Kamikaze | `0x5cb550` `MAG_181_KAMIKAZE_Init` | timeline (Fire/Blizzard archetype) |
| 182 | Card | `0x5c9fe0` `MAG_182_CARD` | timeline (Fire/Blizzard archetype) |
| 183 | Defend | `0x5c9a50` `MAG_183_DEFEND` | timeline (Fire/Blizzard archetype) |
| 184 | Ultra Waves (Quistis) | `0x5c7fc0` `MAG_184_ULTRA_WAVES_QUISTIS` | timeline (Fire/Blizzard archetype) |
| 185 | Shiva Summon (Diamond Dust) | `0x5c0d50` `MAG_185_SHIVA_SUMMON_DIAMOND_DUST` | timeline (Fire/Blizzard archetype) |
| 186 | Blaster | `0x5bf6f0` `MAG_186_BLASTER_Init` | timeline (Fire/Blizzard archetype) |
| 187 | Odin Summon (Zantetsuken) | `0x6472e0` `MAG_187_ODIN_SUMMON_ZANTETSUKEN` | timeline (Fire/Blizzard archetype) |
| 188 | Shot - Normal Shot | `0x5be340` `MAG_188_SHOT__NORMAL_SHOT_Init` | timeline (Fire/Blizzard archetype) |
| 189 | Wall | `0x5bc960` `MAG_189_WALL` | timeline (Fire/Blizzard archetype) |
| 190 | Chain Gun | `0x5bb2c0` `MAG_190_CHAIN_GUN` | timeline (Fire/Blizzard archetype) |
| 191 | Doomtrain Summon (Runaway Train) | `0x63e730` `MAG_191_DOOMTRAIN_SUMMON_RUNAWAY_TRAIN` | timeline (Fire/Blizzard archetype) |
| 192 | Shot - Scatter Shot | `0x5b96f0` `MAG_192_SHOT__SCATTER_SHOT_Init` | timeline (Fire/Blizzard archetype) |
| 193 | Shot - Dark Shot | `0x5b7190` `MAG_193_SHOT__DARK_SHOT_Init` | timeline (Fire/Blizzard archetype) |
| 194 | Shot - Flame Shot | `0x5b4c60` `MAG_194_SHOT__FLAME_SHOT_Init` | timeline (Fire/Blizzard archetype) |
| 195 | Shot - Canister Shot | `0x5b2a40` `MAG_195_SHOT__CANISTER_SHOT` | timeline (Fire/Blizzard archetype) |
| 196 | Shot - Quick Shot | `0x5b1900` `MAG_196_SHOT__QUICK_SHOT_Init` | timeline (Fire/Blizzard archetype) |
| 197 | Shot - Armor Shot | `0x5aed30` `MAG_197_SHOT__ARMOR_SHOT_` | timeline (Fire/Blizzard archetype) |
| 198 | Shot - Hyper Shot | `0x5aa3e0` `MAG_198_SHOT__HYPER_SHOT_` | timeline (Fire/Blizzard archetype) |
| 199 | Cactuar Summon (1,000 Needles) | `0x5a8750` `MAG_199_CACTUAR_SUMMON_1000_NEEDLES` | timeline (Fire/Blizzard archetype) |
| 200 | No Mercy | `0x6391d0` `MAG_200_NO_MERCY` | timeline (Fire/Blizzard archetype) |
| 201 | Ifrit Summon (Hell Fire) | `0xb25780` `MAG_201_IFRIT_SUMMON_HELL_FIRE` | shared cinematic engine |
| 202 | Bahamut Summon (Mega Flare) | `0xb189a0` `MAG_202_BAHAMUT_SUMMON_MEGA_FLARE` | shared cinematic engine |
| 203 | Cerberus Summon (Counter Rockets) | `0xb0c1a0` `MAG_203_CERBERUS_SUMMON_COUNTER_ROCKETS` | shared cinematic engine |
| 204 | Alexander Summon (Holy Judgment) | `0xaffca0` `MAG_204_ALEXANDER_SUMMON_HOLY_JUDGMENT` | shared cinematic engine |
| 205 | Brothers Summon (Brotherly Love) | `0xaf4520` `MAG_205_BROTHERS_SUMMON_BROTHERLY_LOVE` | shared cinematic engine |
| 206 | Eden Summon (Eternal Breath) | `0xae2dd0` `MAG_206_EDEN_SUMMON_ETERNAL_BREATH` | shared cinematic engine |
| 207 | Maelstrom | `0x6a3ab0` `MAG_207_MAELSTROM` → `MAG_207_sub_6A3AE0` | **timeline** (via thunk +0x30) |
| 208 | Final "Sorceress" Death | `0xad7900` `MAG_208_FINAL_SORCERESS_DEATH` | timeline (Fire/Blizzard archetype) |
| 209 | "Sorceress" Spawn | `0x637500` `MAG_209_SORCERESS_SPAWN` | timeline (Fire/Blizzard archetype) |
| 210 | Bloodfest | `0x6f6800` `MAG_210_BLOODFEST` → `MAG_210_sub_6F6810` | **timeline** (via thunk +0x10) |
| 211 | Adel Death | `0xaca120` `MAG_211_ADEL_DEATH` | timeline (Fire/Blizzard archetype) |
| 212 | Burning Rave (Zell's Finisher) | `0x6a0d20` `MAG_212_UNK8` → `MAG_212_sub_6A0D50` | **timeline** (via thunk +0x30) |
| 213 | Storm Breath | `0x69eac0` `MAG_213_STORM_BREATH` → `MAG_213_sub_69EAF0` | **timeline** (via thunk +0x30) |
| 214 | Gravija | `0x69d5b0` `MAG_214_GRAVIJA` → `MAG_214_sub_69D5E0` | **timeline** (via thunk +0x30) |
| 215 | My Final Heaven (Zell's Finisher) | `0x69ab60` `MAG_215_UNK9` → `MAG_215_sub_69AB90` | **timeline** (via thunk +0x30) |
| 216 | Different Beat (Zell's Finisher) | `0x6959e0` `MAG_216_UNK10` → `MAG_216_sub_695A10` | **timeline** (via thunk +0x30) |
| 217 | Energy Bomber | `0x694e60` `MAG_217_ENERGY_BOMBER` → `MAG_217_sub_694E90` | **timeline** (via thunk +0x30) |
| 218 | Unknown | `0x6326d0` `MAG_218_UNK11` | timeline (Fire/Blizzard archetype) |
| 219 | Terra Break | `0xabd420` `MAG_219_TERRA_BREAK` | timeline (Fire/Blizzard archetype) |
| 220 | Light Pillar | `0xab3320` `MAG_220_LIGHT_PILLAR` | timeline (Fire/Blizzard archetype) |
| 221 | Apocalypse | `0xaa5560` `MAG_221_APOCALYPSE` | timeline (Fire/Blizzard archetype) |
| 222 | Water | `0xa9b200` `MAG_222_WATER` | timeline (Fire/Blizzard archetype) |
| 223 | Meteor | `0xa8f890` `MAG_223_METEOR` | timeline (Fire/Blizzard archetype) |
| 224 | Unknown | — `—` | **FREE SLOT** |
| 225 | Unknown | — `—` | **FREE SLOT** |
| 226 | White Wind | `0x694520` `MAG_226_UNKNOWN` → `MAG_226_sub_694550` | **timeline** (via thunk +0x30) |
| 227 | Ultimecia First Death | `0x693790` `MAG_227_UNKNOWN` → `MAG_227_sub_6937C0` | **timeline** (via thunk +0x30) |
| 228 | Ice Strike | `0xa855c0` `MAG_228_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 229 | Homing Laser (Quistis) | `0xa7aa20` `MAG_229_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 230 | Fire Breath (Quistis) | `0xa70b70` `MAG_230_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 231 | Disease Breath | `0xa664a0` `MAG_231_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 232 | Breath of Death | `0xa5c2e0` `MAG_232_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 233 | Earthquake | `0xa51f40` `MAG_233_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 234 | Fart | `0xa488f0` `MAG_234_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 235 | Breath | `0xa3e370` `MAG_235_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 236 | Gas | `0xa34240` `MAG_236_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 237 | Explosion | `0xa29c30` `MAG_237_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 238 | Breath | `0xa1fdc0` `MAG_238_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 239 | Ochu Dance | `0xa15a30` `MAG_239_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 240 | Earthquake | `0xa0b360` `MAG_240_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 241 | BGH251F2 Gatling Gun | `0xa01e10` `MAG_241_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 242 | Beam Cannon | `0x9f7d10` `MAG_242_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 243 | BGH251F2 1st Turret Exploding | `0x9eea90` `MAG_243_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 244 | BGH251F2 2nd Turret Exploding | `0x9e5810` `MAG_244_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 245 | BGH251F2 3rd Turret Exploding | `0x9dc590` `MAG_245_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 246 | BGH251F2 4th Turret Exploding | `0x9d3310` `MAG_246_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 247 | BGH251F2 Death | `0x9c9890` `MAG_247_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 248 | Soldier Entrance After BGH251F2 Death | `0x9c08d0` `MAG_248_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 249 | Unknown | `0x9b7380` `MAG_249_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 250 | Beam Cannon | `0x9abff0` `MAG_250_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 251 | Demon Slice | `0x6f44d0` `MAG_251_UNKNOWN` → `MAG_251_sub_6F44E0` | **timeline** (via thunk +0x10) |
| 252 | Corona | `0x9a2870` `MAG_252_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 253 | Twin Homing Laser | `0x997d10` `MAG_253_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 254 | Homing Laser | `0x98d1b0` `MAG_254_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 255 | Homing Laser | `0x982650` `MAG_255_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 256 | Sand Shake | `0x979400` `MAG_256_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 257 | Mega Flare | `0x96f290` `MAG_257_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 258 | Mad Cow Special | `0x964a00` `MAG_258_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 259 | Renzokuken - 6 Hits | `0x5a6c20` `MAG_259_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 260 | Shockwave Pulsar (Quistis) | `0x690690` `MAG_260_UNKNOWN` → `MAG_260_sub_6906C0` | **timeline** (via thunk +0x30) |
| 261 | Desperado | `0x9598d0` `MAG_261_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 262 | Blood Pain | `0x94f9f0` `MAG_262_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 263 | Massive Anchor | `0x945810` `MAG_263_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 264 | Unknown | `0x937eb0` `MAG_264_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 265 | Unknown | `0x92cbd0` `MAG_265_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 266 | Unknown | `0x91f5e0` `MAG_266_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 267 | Unknown | `0x911ff0` `MAG_267_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 268 | Unknown | `0x904a00` `MAG_268_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 269 | Unknown | `0x8f7220` `MAG_269_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 270 | Ultima Weapon Death | `0x8e9c30` `MAG_270_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 271 | LV Up | `0x68f550` `MAG_271_UNKNOWN` → `MAG_271_sub_68F580` | **timeline** (via thunk +0x30) |
| 272 | LV Down | `0x68dc70` `MAG_272_UNKNOWN` → `MAG_272_sub_68DCA0` | **timeline** (via thunk +0x30) |
| 273 | Mad Rush | `0x68d650` `MAG_273_UNKNOWN` → `MAG_273_sub_68D680` | **timeline** (via thunk +0x30) |
| 274 | Duel | `0x6897e0` `MAG_274_UNKNOWN` → `MAG_274_sub_6898B0` | **timeline** (via thunk +0xd0) |
| 275 | Electrocute (Quistis) | `0x687b40` `MAG_275_UNKNOWN` → `MAG_275_sub_687B70` | **timeline** (via thunk +0x30) |
| 276 | X-ATM092 Death | `0x684ee0` `MAG_276_UNKNOWN` → `MAG_276_sub_684F10` | **timeline** (via thunk +0x30) |
| 277 | Funguar Laser | `0x683f10` `MAG_277_UNKNOWN` → `MAG_277_sub_683F40` | **timeline** (via thunk +0x30) |
| 278 | Carbuncle Summon (Ruby Light) | `0x680c50` `MAG_278_CARBUNCLE_SUMMON_RUBY_LIGHT` → `GF_278Carbuncle_SetupSummon` | **timeline** (via thunk +0x30) |
| 279 | Mega Spark | `0x67efd0` `MAG_279_UNKNOWN` → `MAG_279_sub_67F000` | **timeline** (via thunk +0x30) |
| 280 | Full Cure | `0x67e730` `MAG_280_UNKNOWN` → `MAG_280_sub_67E760` | **timeline** (via thunk +0x30) |
| 281 | Shotgun | `0x67dce0` `MAG_281_UNKNOWN` → `MAG_281_sub_67DD10` | **timeline** (via thunk +0x30) |
| 282 | Evil-Eye | `0x67d400` `MAG_282_UNKNOWN` → `MAG_282_sub_67D430` | **timeline** (via thunk +0x30) |
| 283 | Magic Summon | `0x67c400` `MAG_283_UNKNOWN` → `MAG_283_sub_67C430` | **timeline** (via thunk +0x30) |
| 284 | Micro Missiles | `0x67b7a0` `MAG_284_UNKNOWN` → `MAG_284_sub_67B7D0` | **timeline** (via thunk +0x30) |
| 285 | Thunder Summon | `0x67a860` `MAG_285_UNKNOWN` → `MAG_285_sub_67A890` | **timeline** (via thunk +0x30) |
| 286 | Mini Pulse Cannon | `0x679e10` `MAG_286_UNKNOWN` → `MAG_286_sub_679E40` | **timeline** (via thunk +0x30) |
| 287 | Mega Pulse Cannon | `0x6f2e80` `MAG_287_UNKNOWN` → `MAG_287_sub_6F2E90` | **timeline** (via thunk +0x10) |
| 288 | Rapture | `0x6791f0` `MAG_288_UNKNOWN` → `MAG_288_sub_679220` | **timeline** (via thunk +0x30) |
| 289 | "Brrawghh!" | `0x6777e0` `MAG_289_UNKNOWN` → `MAG_289_sub_677810` | **timeline** (via thunk +0x30) |
| 290 | Unknown | `0x675280` `MAG_290_UNKNOWN` → `MAG_290_sub_6752B0` | **timeline** (via thunk +0x30) |
| 291 | Pandemona Summon (Tornado Zone) | `0x6ed250` `MAG_291_PANDEMONA_SUMMON_TORNADO_ZONE` → `GF_291Pandemona_SetupSummon` | **timeline** (via thunk +0x10) |
| 292 | Soft | `0x674d90` `MAG_292_UNKNOWN` → `MAG_292_sub_674DC0` | **timeline** (via thunk +0x30) |
| 293 | Eye Drops | `0x674870` `MAG_293_UNKNOWN` → `MAG_293_sub_6748A0` | **timeline** (via thunk +0x30) |
| 294 | Antidote | `0x6743f0` `MAG_294_UNKNOWN` → `MAG_294_sub_674420` | **timeline** (via thunk +0x30) |
| 295 | Echo Screen | `0x673e70` `MAG_295_UNKNOWN` → `MAG_295_sub_673EA0` | **timeline** (via thunk +0x30) |
| 296 | Holy Water | `0x673970` `MAG_296_UNKNOWN` → `MAG_296_sub_6739A0` | **timeline** (via thunk +0x30) |
| 297 | White Wind (Quistis) | `0x673000` `MAG_297_UNKNOWN` → `MAG_297_sub_673030` | **timeline** (via thunk +0x30) |
| 298 | Unknown | `0x670970` `MAG_298_UNKNOWN` → `MAG_298_sub_6709A0` | **timeline** (via thunk +0x30) |
| 299 | Micro Missiles (Quistis) | `0x66fcc0` `MAG_299_UNKNOWN` → `MAG_299_sub_66FCF0` | **timeline** (via thunk +0x30) |
| 300 | Bad Breath (Quistis) | `0x66ef00` `MAG_300_UNKNOWN` → `MAG_300_sub_66EF30` | **timeline** (via thunk +0x30) |
| 301 | Unknown | `0x66d8e0` `MAG_301_UNKNOWN` → `MAG_301_sub_66D910` | **timeline** (via thunk +0x30) |
| 302 | Snipe Laser | `0x66ca50` `MAG_302_UNKNOWN` → `MAG_302_sub_66CA80` | **timeline** (via thunk +0x30) |
| 303 | Unknown | `0x66a820` `MAG_303_UNKNOWN` → `MAG_303_sub_66A850` | **timeline** (via thunk +0x30) |
| 304 | Boomerang Sword | `0x669790` `MAG_304_UNKNOWN` → `MAG_304_sub_6697C0` | **timeline** (via thunk +0x30) |
| 305 | Gatling Gun (Quistis) | `0x5a57d0` `MAG_305_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 306 | Degenerator (Quistis) | `0x5a2c90` `MAG_306_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 307 | Ray-Bomb (Quistis) | `0x5a1170` `MAG_307_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 308 | Unknown | `0x667670` `MAG_308_UNKNOWN` → `MAG_308_sub_6676A0` | **timeline** (via thunk +0x30) |
| 309 | Hero-trial/Hero | `0x666dd0` `MAG_309_UNKNOWN` → `MAG_309_sub_666E00` | **timeline** (via thunk +0x30) |
| 310 | Holy War-trial/Holy War | `0x6664a0` `MAG_310_UNKNOWN` → `MAG_310_sub_6664D0` | **timeline** (via thunk +0x30) |
| 311 | Unknown | `0x6652c0` `MAG_311_UNKNOWN` → `MAG_311_sub_6652F0` | **timeline** (via thunk +0x30) |
| 312 | Megiddo Flame (Mobile Type 8) | `0x59cb90` `MAG_312_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 313 | Unknown | `0x59b0d0` `MAG_313_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 314 | Unknown | `0x662890` `MAG_314_UNKNOWN` → `MAG_314_sub_6628C0` | **timeline** (via thunk +0x30) |
| 315 | Fake President Death | `0x598db0` `MAG_315_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 316 | Unknown | `0x6610b0` `MAG_316_UNKNOWN` → `MAG_316_sub_6610E0` | **timeline** (via thunk +0x30) |
| 317 | Acid (Quistis) | `0x65f840` `MAG_317_UNKNOWN` → `MAG_317_sub_65F870` | **timeline** (via thunk +0x30) |
| 318 | Unknown | `0x65e510` `MAG_318_UNKNOWN` → `MAG_318_sub_65E540` | **timeline** (via thunk +0x30) |
| 319 | Unknown | `0x65db30` `MAG_319_UNKNOWN` → `MAG_319_sub_65DB60` | **timeline** (via thunk +0x30) |
| 320 | Dark Flare | `0x65bc10` `MAG_320_UNKNOWN` → `MAG_320_sub_65BC40` | **timeline** (via thunk +0x30) |
| 321 | Ker Plunk | `0x597a00` `MAG_321_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 322 | Zan | `0x65ab70` `MAG_322_UNKNOWN` → `MAG_322_sub_65ABA0` | **timeline** (via thunk +0x30) |
| 323 | Metsu | `0x659a80` `MAG_323_UNKNOWN` → `MAG_323_sub_659AB0` | **timeline** (via thunk +0x30) |
| 324 | Tonberry King Death | `0x596bc0` `MAG_324_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 325 | Diablos Summon (Dark Messenger) | `0x6541e0` `MAG_325_DIABLOS_SUMMON_DARK_MESSENGER` → `GF_325Diablos_SetupSummon` | **timeline** (via thunk +0x30) |
| 326 | Zantetsuken Reverse | `0x62a7e0` `MAG_326_ODIN_ZANTETSUKEN_REVERSE` | timeline (Fire/Blizzard archetype) |
| 327 | Gilgamesh - Zantetsuken | `0x58d760` `MAG_327_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 328 | Gilgamesh - Masamune | `0x58d930` `MAG_328_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 329 | Gilgamesh - Excaliber | `0x58db10` `MAG_329_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 330 | Gilgamesh - Excalipoor | `0x58dcf0` `MAG_330_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 331 | Unknown | `0x8dffa0` `MAG_331_UNKNOWN` | heal/status framework (Cure archetype) |
| 332 | Renzokuken - 7 Hits | `0x58b930` `MAG_332_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 333 | Renzokuken - 8 Hits | `0x589bd0` `MAG_333_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 334 | Renzokuken (vs Bahamut) | `0x587790` `MAG_334_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 335 | Renzokuken (vs NORG) | `0x5856b0` `MAG_335_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 336 | Renzokuken (vs Ultima Weapon) | `0x583040` `MAG_336_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 337 | Renzokuken (vs Final "Sorceress") | `0x580990` `MAG_337_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 338 | Friendship (MoombaMoomba) | `0x6ebd50` `MAG_338_UNKNOWN` → `MAG_338_sub_6EBD60` | **timeline** (via thunk +0x10) |
| 339 | Renzokuken (vs Adel) | `0x57e5d0` `MAG_339_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 340 | Renzokuken (vs Ultimecia Final Form) | `0x57bc00` `MAG_340_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 341 | Renzokuken (vs Jumbo Cactuar) | `0x579a80` `MAG_341_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 342 | Renzokuken (vs Griever + Ultimecia) | `0x5776d0` `MAG_342_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 343 | Renzokuken (vs Griever) | `0x575650` `MAG_343_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 344 | Final Battle Music | `0x62a650` `MAG_344_UNKNOWN` | timeline (Fire/Blizzard archetype) |
| 345 | LV5 Death | `0x705a80` `MAG_345_UNKNOWN` | timeline (Fire/Blizzard archetype) |

## Open

- The 111 thunks are resolved (all timeline), but only **Thundara** has been *read*. The other 110
  are classified by init shape — own globals, `0x14×1` root pool, camera, TIM — not by reading their
  tick functions. That is the same structural argument used for the rest of the table, and it
  carries the same caveat.
- The thunk targets are still named `MAG_nnn_sub_XXXXXX`. The id prefixes are correct (they were the
  evidence above), so this is navigable, but renaming them to `_Init` would make the real entry
  points greppable. Only Thundara, Thundaga, Thunder, Blizzara, Blizzaga and Phoenix carry `_Init`
  names today.
- Ids **60, 63, 68, 81, 101, 179, 218, 224–225, 249, 264–269, 290, 298, 301, 303, 308, 311,
  313–314, 316, 318–319, 331** are named "Unknown" in the effect-name list; 218 is a
  **family-2-shaped GF summon** and a leftover-content candidate.
- The archetype assignment is structural; effects whose behaviour matters should be read.
