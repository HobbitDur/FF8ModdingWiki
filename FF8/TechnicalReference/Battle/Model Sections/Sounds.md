---
title: Sounds
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/sounds/
nav_order: 9
author: HobbitDur
---

1. TOC
{:toc}

## Sounds

Contains AKAO sound *sequences* (can be empty). Each sequence is a small block in Square's **AKAO** format (magic `"AKAO"` = `41 4B 41 4F`).

### Header

| Offset             | Length             | Description                                                            |
|--------------------|--------------------|-----------------------------------------------------------------------|
| 0                  | 2 bytes            | Number of AKAOs (`nbAKAO`)                                             |
| 2                  | nbAKAO \* 2 bytes  | AKAO positions (u16 each, **absolute offset from the start of this section**) |
| 2 + nbAKAO \* 2    | 2 bytes            | End offset (= this section's length; gives the length of the last AKAO)     |
| 4 + nbAKAO \* 2    | 0 or 2 bytes       | `0x0000` alignment padding, present only when needed to 4-byte-align the first AKAO |
| (first position)   | Varies \* nbAKAO   | AKAO sequence blocks                                                   |

Details:

- Positions are **absolute** (relative to the section start), so the parser locates each AKAO directly with `positions[i]`; it does not add up lengths.
- The value after the position array (`End offset`) equals the total section length, i.e. one-past-the-last byte, so `len(AKAO[i]) = positions[i+1] - positions[i]` with `positions[nbAKAO]` = End offset.
- The first AKAO block is always **4-byte aligned**. When the header table ends on an unaligned offset, a `0x0000` padding word fills the gap. Example: `c0m001` (nbAKAO=3) → table ends at 0x0A, pad `0000`, first AKAO at 0x0C; `c0m004` (nbAKAO=4) → table ends at 0x0C, no pad.

### AKAO sequence block header

| Offset | Length  | Description                                                                    |
|--------|---------|--------------------------------------------------------------------------------|
| 0x00   | 4 bytes | Magic `"AKAO"`                                                                  |
| 0x04   | 2 bytes | Category / sub-type (observed values `1`, `2`, `3`)                             |
| 0x06   | 2 bytes | `0`                                                                             |
| 0x08   | 4 bytes | Sample-bank id. For category-`1` blocks this equals the [Sound sample bank](../sound-sample-bank/) bank id (e.g. `301`, `302`…); for category `2`/`3` blocks it is `1` |
| 0x0C   | ...     | AKAO sequence body (note/timing command stream)                                |

Typical layout: two category-`1` blocks (referencing the file's embedded sample bank) followed by one or more category-`2`/`3` blocks. Examples:

- `c0m001`: 3 blocks — `(cat 1, len 80, bank 301)`, `(cat 1, len 80, bank 301)`, `(cat 2, len 124, bank 1)`
- `c0m004`: 4 blocks — `(cat 1, 60, 304)`, `(cat 1, 64, 304)`, `(cat 2, 168, 1)`, `(cat 1, 108, 1)`

### How the PC engine handles this section

The section is parsed at battle-load time by `battle_monster_dat_loader`. The whole model blob **plus this section** is copied into battle work RAM in one shot:

```c
BS_CopyGeometry(dest,
    &file[ offset[0] ],                 // first section start
    offset[9] - offset[0]);             // ...up to (not incl.) the sound sample bank
```

Because this section (index 8) sits just before the sound sample bank (index 9), it is included in that copy, and a pointer to the copied sounds data is stored on the entity's command-queue structure (`command_queue + 0x28`).

The PC port does not play sound from these AKAO blocks: no code path reads the stored sounds pointer back into the audio engine. Monster sound effects on PC are played through the global DirectSound engine, driven by the [animation-sequence VM](../animation-sequences/) and keyed by IDs held in the executable — see [The SFX path](#the-sfx-path) below. The embedded AKAO sequences are inert on the PC release.

### The SFX path

The AnimSeq VM (`AnimSeq_DispatchActionOpcode`) triggers battle sound with these opcodes:

| Opcode        | Meaning                    | Call                                              |
|---------------|----------------------------|---------------------------------------------------|
| `0x97`        | revival/miss-aware cue      | `linkedToSoundAnimSeq(addr, 0x80)`                |
| `0x98`        | cue                         | `linkedToSoundAnimSeq(addr, 0x81)`                |
| `0xB5`/`0xB6` | play actor-local sound      | `linkedToSoundAnimSeq(addr, 0)` → `BdPlayActorSE` |
| `0xB8`        | play external/global sound  | `linkedToSoundAnimSeq(addr, 1)` → `BdPlaySy`      |

`linkedToSoundAnimSeq` reads its operands from the sequence stream:

- `sound_id = addr[0]` (byte)
- `flags = addr[1]` (byte): bit0 = pan relative to the current target, bit1 = an explicit channel byte follows, bit2 = fixed volume (128)

Resolution of `sound_id`:

- `BdPlaySy` (external) passes `sound_id` straight to `PlayWorldSound`.
- `BdPlayActorSE` (actor-local): `sound_id` is `0..6` and indexes a hardcoded per-actor table in the executable, `BattleActorSoundTable`:

  ```c
  PlayWorldSound( BattleActorSoundTable[entity->com_id][sound_id], channel_mask, volume, 0x7F );
  ```

  `BattleActorSoundTable` holds **7 DWORD global "world sound" IDs per `com_id`** (monster id) — e.g. entry 0 = `210008`, `210009`, … These world IDs go through `PlayWorldSound` → `GetSoundID_ForWorld` → `PlaySound` (DirectSound / ADPCM, `C:\FF8\Sound\sound.cpp`).

The "sound index" in the animation stream is **not** an index into this section's AKAO array — it is either a global sound id (`0xB8`) or a small slot resolved through the executable's `BattleActorSoundTable` table (`0xB5`/`0xB6`). To change a monster's battle SFX on the PC release, edit `BattleActorSoundTable` in the executable, not this section of the `.dat`.

The full extracted `BattleActorSoundTable` table (every `com_id` and its sound slots) and the world-sound id encoding are documented on the [Battle actor sound table](../../battle-actor-sounds/) page.

### Modding implications

- Editing this section's AKAO blocks has **no audible effect** on the PC release (the data is parsed but never played).
- The section must still be kept structurally valid (correct `nbAKAO`, positions and end offset): `battle_monster_dat_loader` copies it as part of the model blob and computes downstream pointers from `offset[9] - offset[0]`. A wrong length for this section shifts every pointer after it.

### Reference (names & addresses)

FF8_EN.exe:

| Name                          | Address   | Role                                                                    |
|-------------------------------|-----------|-------------------------------------------------------------------------|
| `battle_monster_dat_loader`   | 0x507120  | Parses the monster `.dat`; copies sections 1–9 into work RAM            |
| `BS_CopyGeometry`             | —         | Bulk copy of the model blob + this section                                 |
| `AnimSeq_DispatchActionOpcode`| 0x504BB0  | AnimSeq VM opcode dispatcher; issues the sound opcodes                |
| `linkedToSoundAnimSeq`        | 0x505AB0  | Reads `sound_id`/`flags` from the sequence and routes to the players    |
| `BdPlayActorSE`               | 0x5015A0  | Actor-local SFX; looks up `BattleActorSoundTable[com_id][0..6]`         |
| `BdPlaySy`                    | 0x501740  | External/global SFX                                                      |
| `PlayWorldSound`              | 0x46B2A0  | World-sound id → channel/panning → `PlaySound`                          |
| `PlaySound`                   | 0x4699A0  | DirectSound / ADPCM playback                                            |
| `BattleActorSoundTable`                 | 0xB8A418  | Per-`com_id` table of 7 world-sound IDs (the actual monster SFX)        |
