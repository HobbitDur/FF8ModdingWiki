---
title: Dynamic texture data
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/dynamic-texture-data/
nav_order: 4
author: HobbitDur
---

## Dynamic texture data

Optional section (monster section 4, character section 4, Edea section 4). It holds the parts of
the model's texture that the game repaints during the battle: the **eye blink** of every playable
character, and the faces, eyes or patterns that change on 37 monsters (PuPu...).

### How it works

Nothing on the model moves: the polygons always sample the same spot of the texture, the
**destination**. To change what they show, the game copies another rectangle of the same texture,
a **sprite**, onto the destination in VRAM (a VRAM-to-VRAM copy). Sprite 0 is the resting picture,
the other sprites are the alternatives.

Squall (`d0c000.dat`): the destination is his right painted eye on the face texture, and both eye
sockets of his mesh are mapped onto it (mirrored), so one copy blinks both eyes. Sprite 0 (the open
eye) and sprite 1 (the closed eye) are stored in a strip at the bottom of the texture. The left
painted eye of the texture is not used by the mesh.

| Squall `d0c000` | Pixels (texture 1) | Picture                         |
|-----------------|--------------------|---------------------------------|
| Destination     | 64, 29 (12 x 6)    | Right painted eye, both eyes    |
| Sprite 0        | 44, 90             | Open eye                        |
| Sprite 1        | 58, 90             | Closed eye                      |

### Format

The section starts with a table of 2-byte offsets (from the start of the section), one per entry,
up to the first entry's data. The **position** in this table is the entry id the sequences use: an
offset of 0 means "no entry with this id" (many monsters have no entry 0, their first entry is 1).

Each entry:

| Offset | Size     | Name            | Description                                                                         |
|--------|----------|-----------------|-------------------------------------------------------------------------------------|
| 0x00   | 1        | texture_num     | Which of the model's texture slots (= its textures in file order, 128 x 128 each)   |
| 0x01   | 1        | destination_u   | X of the destination, in VRAM halfwords (x 2 = pixel of an 8-bit texture)           |
| 0x02   | 1        | destination_v   | Y of the destination, in pixels                                                     |
| 0x03   | 1        | width           | Width of the destination and of every sprite, in VRAM halfwords (x 2 = pixels)      |
| 0x04   | 1        | height          | Height of the destination and of every sprite, in pixels                            |
| 0x05   | 1        | nb_extra_sprite | Number of sprites after sprite 0                                                    |
| 0x06   | 1        | anim_speed      | Speed for opcode `80` (see below), 0 = scroll mode                                  |
| 0x07   | 1        | frame_counter   | Runtime accumulator of opcode `80`, 0 in the file                                   |
| 0x08   | 2        | sprite 0        | u (halfwords), v of the resting sprite                                              |
| 0x0A   | 2 x n    | sprites 1..n    | u, v of each other sprite (n = nb_extra_sprite)                                     |

All x values and the width are VRAM halfwords: an 8-bit texture holds 2 pixels per halfword (every
texture with a dynamic texture section is 8-bit). The coordinates are relative to the texture slot
(`texture_num`), whose VRAM place the loader assigns:

| Slots       | VRAM x                  | VRAM y                  | Used by                                  |
|-------------|-------------------------|-------------------------|------------------------------------------|
| 0-5         | 640 + 64 x (slot / 2)   | 128 x (slot & 1)        | Party bodies (slots 2s and 2s + 1)       |
| 6-11        | 640 + 64 x (slot / 2)   | 128 x (slot & 1)        | Monsters                                 |
| 12-14       | 64 x (slot - 2)         | 128 + (y & 0x7F)        | Weapons                                  |

### What copies a sprite

| Trigger                     | Effect                                                                                                         |
|-----------------------------|----------------------------------------------------------------------------------------------------------------|
| Idle blink                  | While the entity's idle-blink flag is on: closed sprite 1, then sprite 0 again, every 15-59 ticks (random)     |
| Sleep (characters)          | Falling asleep copies sprite 1 (eyes closed), waking up sprite 0                                               |
| KO cured (characters)       | Copies sprite 0 and switches the idle blink back on                                                            |
| Opcode `BE XX`              | Copies sprite 0 of entry 0; `XX` != 0 switches the idle blink on, `XX` == 0 off                                |
| Opcode `BD XX YY`           | Copies sprite `YY` of entry `XX`                                                                               |
| Opcode `9B XX YY`           | Copies a sprite of entry `XX`, read from special variable `YY`                                                 |
| Opcode `9F` timeline        | Blink timeline on entry 0 (idle blink off meanwhile, on again at the end)                                      |
| Opcode `80 XX`              | Steps entry `XX` through its sprites with `anim_speed`                                                         |

The idle blink is off when an entity spawns; opcode `BE 01` and a cured KO switch it on. A
character's sequences are in its weapon file (`d?w`; Edea's own file), so its blink is driven by the
weapon file plus the section 4 of its body. Squall's `d0w000.dat`: sequence 3 runs `BE 00` then
`BD 00 01` (blink off, eyes closed), sequence 22 runs `BE 01` (blink on), sequences 23-27 play `9F`
timelines.

### Opcode `80` (`anim_speed` / `frame_counter`)

[Animation sequences](../animation-sequences/) opcode `80 XX` advances entry `XX`; only
`anim_speed` comes from the file, `frame_counter` is runtime state (0 on disk):

- **`anim_speed` == 0**: *scroll mode*, the destination region is scrolled in VRAM rather than
  swapped (`nb_extra_sprite` is 0 in this case).
- **`anim_speed` == 8**: one sprite per tick; `frame_counter` cycles `0 .. nb_extra_sprite`.
- **any other value**: `anim_speed` is a speed in **1/8-sprite units**: each tick adds it to
  `frame_counter` (which runs `0 .. 8 x (nb_extra_sprite + 1)`), and the sprite copied is
  `frame_counter / 8`. Smaller values play slower, `8` is one sprite per tick.

### Reference (names & addresses)

| Name                                      | FF8_EN.exe | Role                                                                    |
|-------------------------------------------|------------|-------------------------------------------------------------------------|
| `QueueTextureAnimation`                   | 0x50C780   | Copies sprite N of an entry onto its destination (VRAM blit)            |
| `AnimSeq80_StepDynamicTextureAnim`        | 0x50C950   | Opcode `80`                                                             |
| `AnimSeq80_ScrollDynamicTexture`          | 0x50C860   | Opcode `80`, scroll mode                                                |
| `AnimSeq9F_UpdateTextureToggleTimeline`   | 0x5057D0   | Opcode `9F` timeline task                                               |
| `pre_pre_linkedToAnimationSequence`       | 0x502AB0   | Per-entity task: idle blink                                             |
| `initAnimationSequenceAtStartBattle`      | 0x5027D0   | Spawn: arms the blink timer (15-59), blink flag off                     |
| `updateEntityStatusFlags`                 | 0x509D10   | Sleep / KO sprites of a character                                       |
| `BS_RelocateTimsToTexSlots`               | 0x507400   | Assigns the texture slots                                               |
| `Battle_isLoadSquallEtc`                  | 0x5077B0   | Character loader: binds section 4 (`texture_anim_data`)                 |
| `battle_monster_dat_loader`               | 0x507120   | Monster loader: binds section 4 (`texture_anim_data`)                   |
| `BattleComModelData.texture_anim_data`    | +0x30      | The bound section 4                                                     |
| `FF8BattleEntitySlotData.idle_blink_timer`| +0x90      | Ticks left before the next blink step                                   |
| `BATTLE_ENTITY_STATUS_FLAG_IDLE_BLINK`    | 0x04       | Status flag (entity +0x01): idle blink on                               |
