---
title: Character & weapon files (dXcYYY.dat / dXwYYY.dat)
layout: default
parent: Battle
permalink: /technical-reference/battle/character-weapon-files/
nav_order: 3
author: HobbitDur
---

1. TOC
{:toc}

## Overview

Playable characters and their weapons are battle models stored in the same
`battle.fs` archive as the monsters, using the **same container format and the
same section building blocks** as [monster files (c0mxxx.dat)](../monster-file/).
They differ only in *which* sections they carry and in how those sections are
split at load time.

A character in battle is a **composite of two files**: a body model
(`dXcYYY.dat`) and a weapon model (`dXwYYY.dat`). The engine loads both, binds
them into a single animated entity, and drives them from **one** animation-sequence
program — which, notably, lives in the **weapon** file, not the body file.

### com id

Every battle actor has a `com_id`. The value decides which loader runs
(`sub_507080`):

| com id      | Actor                          | Loader                                     |
|-------------|--------------------------------|--------------------------------------------|
| 0 – 15      | **Character** body             | `Battle_isLoadSquallEtc` (Edea: dedicated) |
| + `0x1000`  | **Weapon** for that character  | `Battle_LoadWeaponry` / `BS_LoadWeaponry_2`|
| 16 – 126    | Monster                        | `battle_monster_dat_loader`                |
| 127 (`0x8F`)| c0m127 garbage / final form    | dedicated stub                             |

When a character is spawned the loader queues the body with com id `N`, then
(unless the character is unarmed) queues the weapon with com id `N + 0x1000`.

The 11 character ids follow the standard FF8 party order:

| com id | Character | Body file(s)          | Notes                                             |
|--------|-----------|-----------------------|---------------------------------------------------|
| 0      | Squall    | `d0c000`, `d0c001`    |                                                   |
| 1      | Zell      | `d1c003`, `d1c004`    | unarmed — reduced weapon file (`BS_LoadWeaponry_2`)|
| 2      | Irvine    | `d2c006`              |                                                   |
| 3      | Quistis   | `d3c007`              |                                                   |
| 4      | Rinoa     | `d4c009`              |                                                   |
| 5      | Selphie   | `d5c011`, `d5c012`    |                                                   |
| 6      | Seifer    | `d6c014`              |                                                   |
| 7      | Edea      | `d7c016`              | dedicated loader (`linked_edea_sub_5079B0`); **10-section self-contained body, no weapon file** |
| 8      | Laguna    | `d8c017`, `d8c018`    |                                                   |
| 9      | Kiros     | `d9c019`, `d9c020`    | reduced weapon file (`BS_LoadWeaponry_2`)          |
| 10 (a) | Ward      | `dac021`, `dac022`    |                                                   |

The file-name digits are `dXcYYY` where **`X`** is the character id in hex
(`0`–`a`) and **`YYY`** is a global, sequential model index (the same number used
in the [battle file list](../battle-files/), e.g. `D0C000.DAT` = file 310).

### Body variants (alt model)

Some characters ship two body files (e.g. `d0c000` / `d0c001` for Squall). The
extra file is a **variant** used to differentiate specific battles — most often a
second texture/costume set (for instance the SeeD-exam dress uniforms). The
loader picks the variant through a per-entity *alt-model* byte
(`getCharDataByte_1CFF1B9`), which indexes the character's entry in the party
model table before loading.

## Container header

Identical to the [monster header](../monster-file/#header): a section
count, a table of per-section byte offsets, and a trailing end offset equal to
the file size. `len(section i) = position[i+1] − position[i]`.

Characters carry **7** sections; standard weapons **8**; the reduced weapons of
the unarmed fighters (Zell, Kiros) **5**.

## Character sections (dXcYYY.dat)

| # | Character section        | Shared building block                                             | Notes                                                                                   |
|---|--------------------------|-------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| 1 | Skeleton                 | [Skeleton](../model-sections/skeleton/)          | Identical format (bone count + bones).                                                   |
| 2 | Model geometry           | [Model geometry](../model-sections/model-geometry/)    | Identical format. The body mesh.                                                         |
| 3 | Model animation          | [Model animation](../model-sections/model-animation/)   | Identical format. The body's animation pool (idle, walk, hit, cast poses…).              |
| 4 | Dynamic texture data     | [Dynamic texture data](../model-sections/dynamic-texture-data/) | Identical format, present in every character — this is the **eye-blink** animation.   |
| 5 | **Camera sequence**      | [Camera sequence](../model-sections/camera-sequence/)   | Same byte-code VM and camera-collection layout as the monster camera section.            |
| 6 | Textures                 | [Textures](../model-sections/textures/)        | Identical format (PlayStation TIMs). The body texture pages.                             |
| 7 | Extra animation block    | [Model animation](../model-sections/model-animation/)   | A single extra animation (model-animation format) used to bind body + weapon (see below).      |

What a character file **does not** carry, compared to a monster: no animation
**sequences**, no information/stats, no AI, and no sound sections. Those are
either supplied elsewhere or handled by the weapon:

- **Stats / AI** — a playable character's stats come from the save data and the
  [kernel]({{site.baseurl}}/technical-reference/main/kernel/), and it is driven
  by the player's commands, so there is nothing to store per model.
- **Animation sequences** — the sequence program that decides *which* animation
  plays for each action lives in the **weapon** file (section below). This is why
  a character always needs a weapon loaded, and why the unarmed fighters still
  have a (reduced) weapon file.

### Section 7 — the composite bind

At battle start (`initAnimationSequenceAtStartBattle`), for characters only, the
body's section 7 and the weapon's last section are merged into a per-slot com-file
record and bound into **both** the body's and the weapon's animation headers with
`setComFileData`. The result is that the body and the held weapon behave as one
model driven by a single animation clock.

For how that single clock actually drives the two models at runtime — the
lockstep same-index playback, the render order and how the weapon is positioned —
see [Composite character + weapon animation (runtime)](../composite-character-weapon-animation/).

## Weapon sections (dXwYYY.dat)

Each character has one weapon file per equippable weapon (`dXwYYY`, where `YYY`
is again the global model index; e.g. Squall's `d0w000`–`d0w006` are the seven
gunblades). An empty/placeholder slot can exist (`d0w007` is a 0-byte file).

The weapon carries the **animation-sequence VM** and the battle **sound** data
for the whole character+weapon entity.

### Standard weapon — 8 sections

Used by every armed character (`Battle_LoadWeaponry`):

| # | Weapon section            | Shared building block                                                | Notes                                                                             |
|---|---------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| 1 | Skeleton                  | [Skeleton](../model-sections/skeleton/)             | Weapon's own (small) skeleton.                                                     |
| 2 | Model geometry            | [Model geometry](../model-sections/model-geometry/)       | The weapon mesh. This is the only section that changes between weapons of a tier.  |
| 3 | Model animation           | [Model animation](../model-sections/model-animation/)      | Weapon animation pool.                                                             |
| 4 | **Animation sequences**   | [Animation sequences](../model-sections/animation-sequences/)  | The byte-code VM that orchestrates the composite entity's attack/idle animations.  |
| 5 | Sounds                    | [Sounds](../model-sections/sounds/)              | AKAO sequence — the attack SFX triggers.                                           |
| 6 | Sound sample bank         | [Sound sample bank](../model-sections/sound-sample-bank/)     | AKAO ADPCM sample bank (vestigial on PC, as for monsters).                          |
| 7 | Textures                  | [Textures](../model-sections/textures/)           | Weapon TIMs.                                                                       |
| 8 | Extra animation block     | [Model animation](../model-sections/model-animation/)      | Single extra animation, merged with the body's section 7 at bind time.             |

### Reduced weapon — 5 sections

The unarmed fighters — **Zell** (`d1w`) and **Kiros** (`d9w`) — use a shorter
weapon file loaded by `BS_LoadWeaponry_2`. It drops the separate weapon skeleton
and the extra-animation block, keeping only the parts needed to hold the sequence
VM, sounds and (minimal) textures:

| # | Weapon section          | Shared building block                                              |
|---|-------------------------|-------------------------------------------------------------------|
| 1 | Model geometry          | [Model geometry](../model-sections/model-geometry/)     |
| 2 | Animation sequences     | [Animation sequences](../model-sections/animation-sequences/)|
| 3 | Sounds                  | [Sounds](../model-sections/sounds/)            |
| 4 | Sound sample bank       | [Sound sample bank](../model-sections/sound-sample-bank/)   |
| 5 | Textures                | [Textures](../model-sections/textures/)         |

Because these reduced files carry **no skeleton, geometry animation, or renderable
weapon model**, Zell and Kiros draw **no second model** in battle
(`weaponAnimHeader = NULL`); the file exists only to supply the sequence VM and the
attack sounds. See [Composite character + weapon animation](../composite-character-weapon-animation/).

## Edea — self-contained 10-section body

Edea is the exception to the two-file rule: `initWeaponAnim` loads **no weapon
file** for her, and her body `d7c016.dat` instead carries **10 sections** — a
normal 7-section character body with the weapon's three "service" sections
(sequence VM + sounds + bank) spliced in ahead of the textures. Verified against
the extracted file:

| # | Edea section              | Shared building block                                          | Comes from |
|---|---------------------------|----------------------------------------------------------------|------------|
| 1 | Skeleton                  | [Skeleton](../model-sections/skeleton/)                        | body |
| 2 | Model geometry            | [Model geometry](../model-sections/model-geometry/)            | body |
| 3 | Model animation (30)      | [Model animation](../model-sections/model-animation/)          | body |
| 4 | Dynamic texture (eye-blink)| [Dynamic texture data](../model-sections/dynamic-texture-data/)| body |
| 5 | Camera sequence           | [Camera sequence](../model-sections/camera-sequence/)          | body |
| 6 | **Animation sequences**   | [Animation sequences](../model-sections/animation-sequences/)  | *weapon's role* |
| 7 | **Sounds**                | [Sounds](../model-sections/sounds/)                            | *weapon's role* |
| 8 | **Sound sample bank**     | [Sound sample bank](../model-sections/sound-sample-bank/)      | *weapon's role* |
| 9 | Textures                  | [Textures](../model-sections/textures/)                        | body |
| 10| Extra animation block     | [Model animation](../model-sections/model-animation/)          | body |

Section 6 is byte-for-byte the same sequence-VM header format as a standard
weapon's section 4, and sections 7–8 are the same `AKAO` sounds/bank as a weapon's
sections 5–6 — Edea simply *is* a character and her "weapon" fused into one file,
so she needs no separate weapon and renders a single model.

## Summary: who carries what

| Building block                | Monster (c0m) | Character (dXc) | Weapon (dXw)          |
|-------------------------------|:-------------:|:---------------:|:---------------------:|
| Skeleton                      | ✔ (s1)        | ✔ (s1)          | ✔ (s1, standard only) |
| Model geometry                | ✔ (s2)        | ✔ (s2)          | ✔ (s2 / s1)           |
| Model animation               | ✔ (s3)        | ✔ (s3)          | ✔ (s3 / —)            |
| Dynamic texture (eye-blink)   | ✔ (s4)        | ✔ (s4)          | —                     |
| Animation sequences (VM)      | ✔ (s5)        | —               | ✔ (s4 / s2)           |
| Camera sequence               | ✔ (s6)        | ✔ (s5)          | —                     |
| Information & stats           | ✔ (s7)        | —               | —                     |
| Battle scripts / AI           | ✔ (s8)        | —               | —                     |
| Sounds (AKAO seq)             | ✔ (s9)        | —               | ✔ (s5 / s3)           |
| Sound sample bank (AKAO)      | ✔ (s10)       | —               | ✔ (s6 / s4)           |
| Textures                      | ✔ (s11)       | ✔ (s6)          | ✔ (s7 / s5)           |
| Extra animation (bind block)  | —             | ✔ (s7)          | ✔ (s8, standard only) |

## Reference — key addresses (FF8_EN.exe)

| Address    | Symbol                            | Role                                                        |
|------------|-----------------------------------|-------------------------------------------------------------|
| `0x507080` | `sub_507080`                      | Model-load dispatch (picks loader from com id)              |
| `0x5077B0` | `Battle_isLoadSquallEtc`          | Character body loader (splits the 7 sections)               |
| `0x5079B0` | `linked_edea_sub_5079B0`          | Edea body loader                                            |
| `0x507BF0` | `Battle_LoadWeaponry`             | Standard weapon loader (8 sections)                         |
| `0x507E20` | `BS_LoadWeaponry_2`               | Reduced weapon loader for Zell/Kiros (5 sections)           |
| `0x508480` | `BattleFile_CharacterLoad`        | Kicks off the actual file read into the battle file buffer  |
| `0x507400` | `sub_507400`                      | Texture VRAM allocation (TPage/CLUT patching)               |
| `0x5022C0` | `BS_BindEntityModelFromComData`   | Binds section pointers into the entity com-file data        |
| `0x5027D0` | `initAnimationSequenceAtStartBattle` | Merges body s7 + weapon last section; queues entrance seq |
