---
title: Animation frame-rate conversion (30/60 fps)
layout: default
parent: Battle
author: HobbitDur
permalink: /technical-reference/battle/animation-frame-rate-conversion/
nav_order: 4
---

Battle model animations hold one pose per battle tick, at 15 poses per second. A mod that
wants smoother models either **inserts interpolated frames in the animation data** or
**uses the engine's own half-step player** ([Battle Model Animation Timing](../battle-model-animation-timing/)).
This page covers the first approach: what the engine allows, which animations do not fit,
and how to cut the ones that do not.

1. TOC
{:toc}

## Converting by inserting frames

Inserting `factor - 1` interpolated poses between each pair of frames turns a 15 fps
animation into a 30 fps one (`factor = 2`) or a 60 fps one (`factor = 4`). The frame count
of the result depends on whether the animation loops:

| Animation | Frame count after conversion |
|---|---|
| played once | `(n - 1) * factor + 1` |
| looping | `n * factor` (the wrap from the last frame back to the first one is interpolated too) |

Whether an animation loops is not stored in the animation data: it depends on how the
[animation sequences](../model-sections/animation-sequences/) play it — see
[Animation Sequences](../model-sections/animation-sequences/) for the op codes and
`FF8GameData/dat/animloopdetector.py` in FF8UltimateEditor for the detection.

## The two limits

### 255 frames — the storage limit

An animation stores its frame count on **one byte**, and `BattleAnimCmd.current_frame` /
`total_frames` are bytes as well, so no animation can be longer than 255 frames.

### 128 frames — the Slow limit

When an animation starts while the entity is slowed, `pre_Battle_ReadAnimation` sets
`total_frames = 2 * nbFrames - 1` **in an 8 bit register**:

```
0x509482  shl cl, 1     ; cl is a byte
0x509484  dec cl
0x509486  mov [eax+7], cl
```

Over 128 frames that count wraps: a 137 frame animation gets `2*137-1 = 273 & 0xFF = 17`
and stops after 17 calls instead of 273. So an animation Slow can reach must stay
**≤ 128 frames**.

Slow (and Haste) are only applied while `currentAnimSeqId == basedAnimSeq`
(`Battle_QueueAnimation`), and the `A3` op code marks the running sequence as the base
one. **Only the animations played by a base sequence — the idle stance in practice — are
concerned.** A loop inside an attack sequence is never slowed and uses the full 255.

This is why the limit is per animation:

| Animation | Limit |
|---|---|
| played by a base sequence (`A3`) | 128 frames |
| every other one | 255 frames |

## Splitting an animation that does not fit

An animation that goes over its limit once converted is cut into parts played one after
the other. **Interpolate first, cut after**: the animation is converted whole, then the
resulting frame stream is cut in contiguous slices of at most the limit. The parts are
then slices of the very stream an unsplit conversion would produce — no frame is repeated
at the cut, no interpolated frame is missing, and the parts chained play exactly the
unsplit animation. Elvoret's animation 27 at 30 fps: 140 frames → 279 converted →
`140 + 139`, and 140 + 139 = 279.

(Cutting the 15 fps frames *before* interpolating would instead force each part to end on
the frame the next one starts with — one repeated frame per cut, and one tick too many.)

The chaining is seamless because of how the engine counts ticks: an animation of N frames
occupies exactly N ticks, and the tick where it completes **draws nothing** —
`Battle_ReadAnimation` returns COMPLETE before rebuilding the geometry, the sequence VM
runs in that same tick, reaches the op code of the next part, and
`pre_Battle_ReadAnimation` displays *its* frame 0. Part 1's last frame and part 2's first
frame are therefore consecutive ticks, exactly as they would be inside a single animation.

The original animation keeps the first part and the other parts are appended at the end of
the section, so existing animation ids stay valid. A bare op code names the animation
directly, so ids stop at **0x7F**.

### Rewriting the sequences

| Played by | Rewritable | Why |
|---|---|---|
| a bare op code (`XX`) | yes → `XX Z1 Z2` | The op code pauses the sequence until the animation ends, so the parts play in a row |
| `A0 XX` | **no** | `A0` does not pause the sequence: `A0 XX A0 Z1` replaces part 1 with part 2 on the same frame |

Inserting bytes moves every following op code, so **every relative jump of the sequence has
to be recomputed**. Gerogero's idle loop shows both:

```
before:  A3 00 E6 FF        E6 FF jumps -1, onto the op code playing animation 0
after:   A3 00 0C E6 FE     animation 0 then 12, and the jump becomes -2 to cover both
```

Two vanilla sequences (`c0m005` seq 12, `c0m060` seq 3) jump to their own end, i.e. into
the next sequence: their size cannot change, so they are refused too.

### Why `A0` cannot be chained

`A0` exists precisely because the sequence keeps running while the animation plays.
Geezard's attack (`c0m004` sequence 12):

```
A0 0F     play animation 15 (100 frames) without pausing
B9 5F     wait 94 frames
C1 05 ..  rotation loop, one A1 (yield) per frame
E7 D5     jump back while the counter is not 0
A2        end of sequence
```

The rotation choreography runs **in parallel** with the animation, and the wait is tuned to
the animation length (94 ≈ 100 frames). Chaining a second part would mean starting it at
the exact frame part 1 ends, i.e. in the middle of that wait/rotation loop — the timing is
hand-written, so it is left to the modder.

## Which monsters do not fit

Counts over the 199 readable `c0m` files (4779 animations):

| Target | Animations over their limit | Splittable | Refused | Monsters affected |
|---|---|---|---|---|
| 30 fps | 7 | 4 | 3 | 7 |
| 60 fps | 117 | 53 | 64 | 85 |

60 fps is where the limits bite: most refusals are idle stances looped by `A0` that go over
the 128 frame Slow limit. **30 fps converts the whole roster with 7 exceptions.**

Reading the table: `27 (140f→3)` means animation 27, 140 frames, needs 3 parts.
`15 (100f, A0)` means animation 15, 100 frames, refused because a sequence plays it with
`A0` (`jump` = a sequence jumping outside itself, `size` = cannot be cut small enough).
Monsters absent from the table convert as-is at both frame rates.

| File | Monster | 30 fps split | 30 fps refused | 60 fps split | 60 fps refused |
|---|---|---|---|---|---|
| `c0m004` | Geezard | — | — | — | 15 (100f, A0) |
| `c0m005` | Belhelmel | — | — | — | 0 (35f, A0), 33 (33f, jump) |
| `c0m009` | Mesmerize | — | — | — | 0 (36f, A0) |
| `c0m010` | Buel | — | — | — | 0 (60f, A0) |
| `c0m013` | Snow Lion | — | — | — | 0 (47f, A0), 11 (68f, A0) |
| `c0m014` | Anacondaur | — | — | — | 0 (60f, A0) |
| `c0m016` | Cockatrice | — | — | — | 0 (39f, A0) |
| `c0m017` | Caterchipillar | — | — | 0 (40f→2) | — |
| `c0m020` | Fastitocalon | — | — | — | 22 (35f, A0) |
| `c0m021` | Fastitocalon | — | — | — | 18 (35f, A0) |
| `c0m024` | Hexadragon | — | — | — | 26 (82f, A0) |
| `c0m025` | Blood Soul | — | — | — | 0 (33f, A0) |
| `c0m027` | Armadodo | — | — | 0 (49f→2) | — |
| `c0m029` | Jelleye | — | — | 17 (72f→2) | 0 (36f, A0) |
| `c0m030` | Tri-Point | — | — | — | 0 (40f, A0) |
| `c0m033` | Gayla | — | — | — | 0 (60f, A0) |
| `c0m034` | Gerogero | 0 (70f→2) | — | 0 (70f→3), 3 (88f→2) | — |
| `c0m035` | Death Claw | — | — | 0 (38f→2) | — |
| `c0m037` | Grand Mantis | — | — | 0 (40f→2) | — |
| `c0m038` | Krysta | — | — | 0 (40f→2) | — |
| `c0m041` | Blue Dragon | — | — | 0 (33f→2) | — |
| `c0m043` | Bomb | — | — | — | 0 (38f, A0) |
| `c0m045` | Ochu | — | — | 9 (66f→2) | — |
| `c0m046` | Adamantoise | — | — | 0 (40f→2) | — |
| `c0m047` | Chimera | — | — | 21 (69f→2) | 0 (40f, A0) |
| `c0m049` | Iron Giant | — | — | — | 0 (38f, A0) |
| `c0m050` | Behemoth | — | — | — | 0 (44f, A0) |
| `c0m052` | Ruby Dragon | — | — | 0 (36f→2) | — |
| `c0m056` | Tonberry | — | — | 12 (116f→2) | — |
| `c0m057` | Torama | — | — | — | 0 (41f, A0), 7 (41f, A0) |
| `c0m058` | Funguar | — | — | 0 (36f→2) | — |
| `c0m060` | PuPu | — | 9 (65f, jump) | — | 2 (36f, A0), 9 (65f, jump) |
| `c0m061` | Ifrit | — | — | — | 0 (47f, A0) |
| `c0m062` | Minotaur | — | — | — | 0 (45f, A0) |
| `c0m063` | Sacred | — | — | — | 0 (35f, A0) |
| `c0m067` | Bahamut | — | — | 9 (78f→2) | 0 (46f, A0) |
| `c0m071` | G-Soldier | — | — | — | 0 (35f, A0) |
| `c0m073` | Wedge | — | — | — | 0 (35f, A0) |
| `c0m075` | Fake President | — | — | 3 (53f→2) | — |
| `c0m076` | Guard | — | — | — | 0 (35f, A0) |
| `c0m077` | NORG | — | 3 (89f, A0) | 9 (75f→2), 10 (75f→2), 11 (80f→2), 12 (80f→2) | 0 (50f, A0), 3 (89f, A0) |
| `c0m082` | Gunblade | — | — | 2 (60f→2), 49 (42f→2) | — |
| `c0m083` | Tonberry King | — | 20 (116f, A0) | — | 20 (116f, A0) |
| `c0m084` | Jumbo Cactuar | — | — | 16 (106f→2) | 3 (66f, A0) |
| `c0m087` | Seifer | — | — | 2 (60f→2) | — |
| `c0m088` | Edea | — | — | — | 0 (35f, A0) |
| `c0m089` | Propagator | — | — | 0 (37f→2) | — |
| `c0m090` | Ultima Weapon | — | — | 26 (107f→2) | — |
| `c0m091` | Elvoret | 27 (140f→2) | — | 25 (104f→2), 27 (140f→3) | 0 (50f, A0), 26 (40f, A0) |
| `c0m092` | X-ATM092 | 0 (69f→2) | — | 0 (69f→3) | — |
| `c0m093` | Iguion | — | — | 20 (69f→2) | — |
| `c0m094` | Gargantua | — | — | 0 (45f→2), 26 (108f→2) | — |
| `c0m097` | Propagator | — | — | 0 (37f→2) | — |
| `c0m098` | Propagator | — | — | 0 (37f→2) | — |
| `c0m099` | Oilboyle | — | — | — | 0 (40f, A0) |
| `c0m100` | Edea | — | — | — | 0 (35f, A0) |
| `c0m101` | BGH251F2 | — | — | — | 0 (40f, A0) |
| `c0m102` | BGH251F2 | — | — | 0 (40f→2) | — |
| `c0m108` | Paratrooper | — | — | — | 0 (35f, A0) |
| `c0m110` | Droma | — | — | — | 0 (40f, A0) |
| `c0m111` | Propagator | — | — | 0 (37f→2) | — |
| `c0m112` | Adel | — | — | 18 (100f→2) | 0 (36f, A0), 10 (35f, A0) |
| `c0m113` | {Rinoa} | — | — | 18 (100f→2) | 0 (36f, A0), 10 (35f, A0) |
| `c0m114` | Omega Weapon | — | — | 26 (107f→2), 32 (128f→2) | — |
| `c0m115` | “Sorceress” | — | — | — | 0 (35f, A0), 9 (64f, A0) |
| `c0m116` | “Sorceress” | — | — | — | 0 (38f, A0) |
| `c0m117` | “Sorceress” | — | — | 13 (110f→2) | 0 (35f, A0), 10 (81f, A0) |
| `c0m120` | Raijin | — | — | — | 0 (33f, A0) |
| `c0m121` | Ultimecia | — | — | — | 0 (42f, A0), 10 (108f, A0) |
| `c0m122` | {Griever} | — | — | 17 (88f→2) | — |
| `c0m124` | Ultimecia | — | — | 21 (43f→2) | — |
| `c0m126` | Ultimecia | — | — | — | 0 (40f, A0) |
| `c0m128` | Seifer | — | — | 25 (42f→2) | — |
| `c0m130` | Red Giant | — | — | 0 (38f→2) | — |
| `c0m131` | Elnoyle | 27 (140f→2) | — | 25 (104f→2), 27 (140f→3) | 0 (50f, A0) |
| `c0m132` | Tiamat | — | — | 0 (46f→2), 9 (78f→2) | 17 (34f, A0) |
| `c0m133` | Catoblepas | — | — | 0 (44f→2) | — |
| `c0m134` | Wedge | — | — | 0 (35f→2) | — |
| `c0m137` | Raijin | — | — | — | 0 (33f, A0) |
| `c0m138` | UFO? | — | — | — | 0 (40f, A0) |
| `c0m139` | UFO? | — | — | — | 0 (40f, A0) |
| `c0m140` | UFO? | — | — | — | 0 (40f, A0) |
| `c0m141` | UFO? | — | — | — | 0 (40f, A0) |
| `c0m142` | Gunblade | — | — | 2 (60f→2) | — |
| `c0m143` | Base Soldier | — | — | — | 0 (35f, A0) |

## Function and data addresses

| Name | Address | Description |
|---|---|---|
| `pre_Battle_ReadAnimation` | `0x509440` | Animation start; `total_frames = 2n-1` in a byte when SLOW (`0x509482`) |
| `Battle_ReadAnimation` | `0x508F90` | Per-call delta reader; returns COMPLETE at `current_frame >= total_frames` |
| `Battle_QueueAnimation` | `0x509520` | Applies Slow/Haste only when `currentAnimSeqId == basedAnimSeq` |
| `AnimSeq_DispatchActionOpcode` | `0x504BB0` | Sequence op codes: bare `< 0x80` pauses, `A0` does not, `A3` sets the base sequence |
