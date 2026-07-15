---
layout: default
parent: Menu
title: Items metadata (mitem.bin file format)
permalink: /technical-reference/menu/mitem/
author: hobbitdur
---

`mitem.bin` is the **field-menu item table**. It defines what each item does when used from the Item menu, who it can target, and how much of an effect it has.

- **Location:** `ff8/data/eng/menu/mitem.bin`
- **Size:** 796 bytes
- **Layout:** 199 entries × 4 bytes, indexed directly by item ID (`0x00`–`0xC6`)

> Entry `0x00` ("Nothing") is a valid entry and is never used as a real item; the inventory treats ID 0 as an empty slot.

This file governs **field-menu behaviour only**. Battle-side item behaviour lives elsewhere, which is why several item types here are indistinguishable from one another (
see [Unused / duplicate types](#unused--duplicate-types)).

---

## Entry format

Each entry is 4 bytes, with no padding or alignment.

| Offset | Name     | Description                                                                                       |
|--------|----------|---------------------------------------------------------------------------------------------------|
| `0`    | `type`   | Item category. Drives dispatch. See [Item types](#item-types).                                    |
| `1`    | `flags`  | Targeting and usability bitfield, read through `Mitem_GetEffectiveFlags`, which overrides it for types 9/12/13/14/15/19. See [Flags](#flags). |
| `2`    | `param1` | Type-dependent. Heal amount, GF id, ability id, magazine start page, …                            |
| `3`    | `param2` | Type-dependent. Status mask, stat mask, compatibility amount, magazine end page, …                |

The meaning of `param1` and `param2` **depends entirely on `type`**. See the per-type sections below.

---

## Flags

`flags` is a bitfield. The item menu tests individual bits.

| Bit | Value  | Name               | Meaning                                                                                           |
|-----|--------|--------------------|---------------------------------------------------------------------------------------------------|
| 0   | `0x01` | `USABLE_IN_MENU`   | Item can be used from the field Item menu. If clear, selecting it shows the "cannot use" message. |
| 1   | `0x02` | `TARGET_CHARA`     | Can target party characters (target mask bits 0–15).                                              |
| 2   | `0x04` | `TARGET_GF`        | Can target GFs (target mask bits 16–31).                                                          |
| 3   | `0x08` | `TARGET_ALL`       | Hits every valid target on one side; no cursor.                                                   |
| 4   | `0x10` | `TARGET_ALL_BOTH`  | Hits characters **and** GFs together. Only Cottage uses this.                                     |
| 5   | `0x20` | `TARGET_DEAD`      | Valid on KO'd targets; the cursor auto-selects a dead target on open.                             |
| 6   | `0x40` | `QUISTIS_ONLY`     | Target mask is forced to party slot 3 (Quistis). Used by all limit-break items.                   |
| 7   | `0x80` | `GF_COMPAT_OTHERS` | *(type 16 only)* Also applies `param2 / 2` as a penalty to every non-target GF.                   |

**Exception:** for `type == 9` (magazines), byte `flags` is **dead data**. An exhaustive sweep of the engine
(all three in-memory copies of mitem.bin — items, shop, status/demo modules — every accessor function and every
direct read) shows the byte is never read for magazine rows: `Mitem_GetEffectiveFlags` returns the constant
`0x11` for types 9, 13 and 15 without touching the file, and the raw-flags getter has no callers at all.

The stored values themselves are decoded, though: they are the **magazine series id** (1 = Weapons Monthly,
2 = Combat King, 3 = Pet Pals, 4 = Occult Fan) — but computed from `param1 - 1` (the previous
[mmag.bin](../mmag/) entry) instead of `param1`, an off-by-one artifact of whatever tool generated the file.
The formula `series(param1 - 1)` matches all 22 magazine rows exactly, while the correct series only matches
19. So the byte was probably meant as a series tag and was never fixed because nothing consumes it (possibly a
PSX-era leftover).

---

## Item types in code

Byte `type` is dispatched in two places.

**Layer 1** — `case 5` of the state machine, on confirm, *before* target selection. Types `9, 12, 13, 14, 15, 16` are intercepted here (16 only for a precondition check).

**Layer 2** — `case 17`, *after* target selection. Types `11, 18, 19` branch to dedicated sub-menus; everything else indexes the action LUT `K_ITEM_TYPE_TO_ACTION` (`byte_B88AC4` in the community IDB,
28 bytes):

```
type   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21
LUT    1  2  3  1  2  3  4  0  0  0  0  0  0  0  0  0  5  6  0  0  8  9
```

LUT value `0` (and the unused `7`) mean *no effect* — the item cannot be consumed from the field menu.

| LUT | Function                     | Effect                               |
|-----|------------------------------|--------------------------------------|
| 1   | `sub_4FC1F0(target, p1, p2)` | Restore HP, optionally cure status   |
| 2   | *(inline in `case 17`)*      | Revive at `maxHP / 8`                |
| 3   | `sub_4FC350(target)`         | Revive at full HP                    |
| 4   | `sub_4FC650(target)`         | Restore full HP and clear all status |
| 5   | `sub_4FC3A0(target, itemId)` | Modify GF compatibility              |
| 6   | `sub_4FC6C0(target, p1)`     | Teach GF ability                     |
| 8   | `sub_4FC8C0(target, p1, p2)` | Permanent stat increase              |
| 9   | `sub_4FC2A0(target, p1, p2)` | Cure status                          |

### Type reference

| Type | Name                | LUT | `param1`              | `param2`             | Notes                                                               |
|------|---------------------|-----|-----------------------|----------------------|---------------------------------------------------------------------|
| 0    | `HEAL_CHARA`        | 1   | heal amount           | status mask to cure  | Amount is `param1 × 50`, clamped to max HP                          |
| 1    | `REVIVE_CHARA`      | 2   | —                     | status mask (`0x01`) | Revives to `maxHP / 8`                                              |
| 2    | `REVIVE_FULL_CHARA` | 3   | —                     | —                    | **No items use this type**                                          |
| 3    | `HEAL_GF`           | 1   | heal amount           | —                    | Identical action to type 0                                          |
| 4    | `REVIVE_GF`         | 2   | —                     | —                    | Identical action to type 1                                          |
| 5    | `REVIVE_FULL_GF`    | 3   | —                     | —                    | **No items use this type**                                          |
| 6    | `FULL_RESTORE`      | 4   | —                     | `0x7F`               | Blocked unless `sub_4B2D50() & 1` (world map / save point)          |
| 7    | `BATTLE_ONLY`       | 0   | —                     | —                    | Usable in battle only                                               |
| 8    | `AMMO`              | 0   | —                     | —                    | Irvine's ammunition                                                 |
| 9    | `MAGAZINE`          | —   | first page            | last page            | Opens the magazine reader (states 80–93). Pages are [mmag.bin](../mmag/) entry indices; the reader uses the items module's own mmag.bin copy (`mmagbuffer`) |
| 10   | `REFINE_ONLY`       | 0   | —                     | —                    | Inert; exists only as refine input                                  |
| 11   | `RENAME_CARD`       | —   | —                     | —                    | Queues field event `(gfIndex + 3) \| 0x80`                          |
| 12   | `PET_NAMETAG`       | —   | —                     | —                    | Queues field event `130`; blocked by `MAP_SEAL_RESURRECTION_LOCKED` |
| 13   | `CHOCOBO_TAG`       | —   | —                     | —                    | Requires `sub_4AD350()->FlagInfo & 1`; queues field event `147`     |
| 14   | `MAGICAL_LAMP`      | —   | —                     | —                    | Grants GF 5 (Diablos); consumes the item immediately                |
| 15   | `SOLOMON_RING`      | —   | —                     | —                    | Checks `mthomasbuffer` recipe, grants GF 11 (Doomtrain)             |
| 16   | `GF_COMPATIBILITY`  | 5   | GF id, or `255` = all | amount               | `flags & 0x80` also penalizes other GFs by `amount / 2`             |
| 17   | `TEACH_GF_ABILITY`  | 6   | ability id            | —                    | 59 items                                                            |
| 18   | `FORGET_ABILITY`    | —   | —                     | —                    | Opens the ability-forget sub-menu (state 66)                        |
| 19   | `QUISTIS_LIMIT`     | —   | limit break id        | —                    | Learns a Blue Magic limit (state 107)                               |
| 20   | `STAT_UP`           | 8   | amount                | stat mask            | Permanent stat increase                                             |
| 21   | `CURE_STATUS`       | 9   | —                     | status mask          | Cures the listed statuses                                           |

---

## Status masks

Used by `param2` on types 0, 1, 6 and 21. These bits match the low byte of [Status1Flag]({{site.baseurl}}/technical-reference/list/status-flags/).

| Bit | Value  | Status   | Curing item        |
|-----|--------|----------|--------------------|
| 0   | `0x01` | Death    | Phoenix Down       |
| 1   | `0x02` | Poison   | Antidote           |
| 2   | `0x04` | Petrify  | Soft               |
| 3   | `0x08` | Darkness | Eye Drops          |
| 4   | `0x10` | Silence  | Echo Screen        |
| 5   | `0x20` | Berserk  | *(Elixir, Remedy)* |
| 6   | `0x40` | Zombie   | Holy Water         |
| 7   | `0x80` | —        | Never curable      |

Common combinations:

| Value  | Statuses                                    | Items                    |
|--------|---------------------------------------------|--------------------------|
| `0x3E` | Poison, Petrify, Darkness, Silence, Berserk | Elixir, Megalixir        |
| `0x7E` | All except Death                            | Remedy, Remedy&          |
| `0x7F` | All except bit 7                            | Tent, Pet House, Cottage |

Bit 7 is deliberately excluded everywhere. `sub_4FC650` hardcodes `status & 0x80` as the bits to preserve — exactly the complement of `0x7F`.

---

## Stat masks

Used by `param2` on type 20. `param1` is the amount added.

| Value  | Stat |
|--------|------|
| `0x01` | HP   |
| `0x02` | Str  |
| `0x04` | Vit  |
| `0x08` | Mag  |
| `0x10` | Spr  |
| `0x20` | Spd  |
| `0x40` | Luck |

The item menu previews which stat will be raised: `case 11` reads `param2` and takes its first set bit.

---

## GF ids

Used by `param1` on type 16.

[GF ids]({{site.baseurl}}/technical-reference/list/gf/)

`255` means "all GFs". No item modifies Eden's compatibility.

**Compatibility is inverted: lower is better.** The value is clamped to `[1000, 6000]`. The target GF receives `compat - param2`; if `flags & 0x80`, every other GF receives
`compat + param2 / 2`. The number shown to the player is `param2 / 5`.

---

## Unused / duplicate types

Types **2** and **5** (full revive, `sub_4FC350`) are referenced by the action LUT but no item in `mitem.bin` uses them. The function is unreachable from this table.

Types **0/3**, **1/4** and **2/5** are pairwise identical from the field menu's perspective: same LUT entry, and the character-vs-GF distinction is already carried by `flags` bits
1 and 2. The split must be meaningful to the **battle-side** item handler, which reads the same table.

---

## Full item table

`type` and `flags` are shown as raw byte then decoded. `param1` / `param2` are decimal.

| ID   | Item              | `type` |                  | `flags` |                          | `p1` | `p2` | Meaning                                                             |
|------|-------------------|--------|------------------|---------|--------------------------|------|------|---------------------------------------------------------------------|
| 0x00 | Nothing           | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x01 | Potion            | 0      | HEAL_CHARA       | 0x03    | MENU+CHR                 | 4    | 0    | heal 4x50 HP                                                        |
| 0x02 | Potion+           | 0      | HEAL_CHARA       | 0x03    | MENU+CHR                 | 8    | 0    | heal 8x50 HP                                                        |
| 0x03 | Hi-Potion         | 0      | HEAL_CHARA       | 0x03    | MENU+CHR                 | 20   | 0    | heal 20x50 HP                                                       |
| 0x04 | Hi-Potion+        | 0      | HEAL_CHARA       | 0x03    | MENU+CHR                 | 40   | 0    | heal 40x50 HP                                                       |
| 0x05 | X-Potion          | 0      | HEAL_CHARA       | 0x03    | MENU+CHR                 | 255  | 0    | heal 255x50 HP                                                      |
| 0x06 | Mega-Potion       | 0      | HEAL_CHARA       | 0x0B    | MENU+CHR+ALL             | 20   | 0    | heal 20x50 HP                                                       |
| 0x07 | Phoenix Down      | 1      | REVIVE_CHARA     | 0x23    | MENU+CHR+DEAD            | 0    | 1    | revive @ maxHP/8                                                    |
| 0x08 | Mega Phoenix      | 1      | REVIVE_CHARA     | 0x2B    | MENU+CHR+ALL+DEAD        | 0    | 1    | revive @ maxHP/8                                                    |
| 0x09 | Elixir            | 0      | HEAL_CHARA       | 0x03    | MENU+CHR                 | 255  | 62   | heal 255x50 HP; cure Poison,Petrify,Darkness,Silence,Berserk        |
| 0x0A | Megalixir         | 0      | HEAL_CHARA       | 0x0B    | MENU+CHR+ALL             | 255  | 62   | heal 255x50 HP; cure Poison,Petrify,Darkness,Silence,Berserk        |
| 0x0B | Antidote          | 21     | CURE_STATUS      | 0x03    | MENU+CHR                 | 0    | 2    | cure Poison                                                         |
| 0x0C | Soft              | 21     | CURE_STATUS      | 0x03    | MENU+CHR                 | 0    | 4    | cure Petrify                                                        |
| 0x0D | Eye Drops         | 21     | CURE_STATUS      | 0x03    | MENU+CHR                 | 0    | 8    | cure Darkness                                                       |
| 0x0E | Echo Screen       | 21     | CURE_STATUS      | 0x03    | MENU+CHR                 | 0    | 16   | cure Silence                                                        |
| 0x0F | Holy Water        | 21     | CURE_STATUS      | 0x03    | MENU+CHR                 | 0    | 64   | cure Zombie                                                         |
| 0x10 | Remedy            | 21     | CURE_STATUS      | 0x03    | MENU+CHR                 | 0    | 126  | cure Poison,Petrify,Darkness,Silence,Berserk,Zombie                 |
| 0x11 | Remedy&           | 21     | CURE_STATUS      | 0x03    | MENU+CHR                 | 0    | 126  | cure Poison,Petrify,Darkness,Silence,Berserk,Zombie                 |
| 0x12 | Hero-trial        | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x13 | Hero              | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x14 | Holy War-trial    | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x15 | Holy War          | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x16 | Shell Stone       | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x17 | Protect Stone     | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x18 | Aura Stone        | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x19 | Death Stone       | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x1A | Holy Stone        | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x1B | Flare Stone       | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x1C | Meteor Stone      | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x1D | Ultima Stone      | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x1E | Gysahl Greens     | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x1F | Phoenix Pinion    | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x20 | Friendship        | 7      | BATTLE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x21 | Tent              | 6      | FULL_RESTORE     | 0x2B    | MENU+CHR+ALL+DEAD        | 0    | 127  | full HP + cure Death,Poison,Petrify,Darkness,Silence,Berserk,Zombie |
| 0x22 | Pet House         | 6      | FULL_RESTORE     | 0x2D    | MENU+GF+ALL+DEAD         | 0    | 127  | full HP + cure Death,Poison,Petrify,Darkness,Silence,Berserk,Zombie |
| 0x23 | Cottage           | 6      | FULL_RESTORE     | 0x37    | MENU+CHR+GF+ALLBOTH+DEAD | 0    | 127  | full HP + cure Death,Poison,Petrify,Darkness,Silence,Berserk,Zombie |
| 0x24 | G-Potion          | 3      | HEAL_GF          | 0x05    | MENU+GF                  | 4    | 0    | heal 4x50 HP (GF)                                                   |
| 0x25 | G-Hi-Potion       | 3      | HEAL_GF          | 0x05    | MENU+GF                  | 20   | 0    | heal 20x50 HP (GF)                                                  |
| 0x26 | G-Mega-Potion     | 3      | HEAL_GF          | 0x0D    | MENU+GF+ALL              | 20   | 0    | heal 20x50 HP (GF)                                                  |
| 0x27 | G-Returner        | 4      | REVIVE_GF        | 0x25    | MENU+GF+DEAD             | 0    | 0    | revive @ maxHP/8                                                    |
| 0x28 | Rename Card       | 11     | RENAME_CARD      | 0x05    | MENU+GF                  | 0    | 0    |                                                                     |
| 0x29 | Amnesia Greens    | 18     | FORGET_ABILITY   | 0x05    | MENU+GF                  | 0    | 0    |                                                                     |
| 0x2A | HP-J Scroll       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 1    | 0    | ability 1                                                           |
| 0x2B | Str-J Scroll      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 2    | 0    | ability 2                                                           |
| 0x2C | Vit-J Scroll      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 3    | 0    | ability 3                                                           |
| 0x2D | Mag-J Scroll      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 4    | 0    | ability 4                                                           |
| 0x2E | Spr-J Scroll      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 5    | 0    | ability 5                                                           |
| 0x2F | Spd-J Scroll      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 6    | 0    | ability 6                                                           |
| 0x30 | Luck-J Scroll     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 9    | 0    | ability 9                                                           |
| 0x31 | Aegis Amulet      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 7    | 0    | ability 7                                                           |
| 0x32 | Elem Atk          | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 10   | 0    | ability 10                                                          |
| 0x33 | Elem Guard        | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 15   | 0    | ability 15                                                          |
| 0x34 | Status Atk        | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 11   | 0    | ability 11                                                          |
| 0x35 | Status Guard      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 17   | 0    | ability 17                                                          |
| 0x36 | Rosetta Stone     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 19   | 0    | ability 19                                                          |
| 0x37 | Magic Scroll      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 20   | 0    | ability 20                                                          |
| 0x38 | GF Scroll         | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 21   | 0    | ability 21                                                          |
| 0x39 | Draw Scroll       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 22   | 0    | ability 22                                                          |
| 0x3A | Item Scroll       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 23   | 0    | ability 23                                                          |
| 0x3B | Gambler Spirit    | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 25   | 0    | ability 25                                                          |
| 0x3C | Healing Ring      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 31   | 0    | ability 31                                                          |
| 0x3D | Phoenix Spirit    | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 33   | 0    | ability 33                                                          |
| 0x3E | Med Kit           | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 28   | 0    | ability 28                                                          |
| 0x3F | Bomb Spirit       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 36   | 0    | ability 36                                                          |
| 0x40 | Hungry Cookpot    | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 37   | 0    | ability 37                                                          |
| 0x41 | Mog`s Amulet      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 38   | 0    | ability 38                                                          |
| 0x42 | Steel Pipe        | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 83   | 0    | ability 83                                                          |
| 0x43 | Star Fragment     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 84   | 0    | ability 84                                                          |
| 0x44 | Energy Crystal    | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 85   | 0    | ability 85                                                          |
| 0x45 | Samantha Soul     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 86   | 0    | ability 86                                                          |
| 0x46 | Healing Mail      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 87   | 0    | ability 87                                                          |
| 0x47 | Silver Mail       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 88   | 0    | ability 88                                                          |
| 0x48 | Gold Armor        | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 89   | 0    | ability 89                                                          |
| 0x49 | Diamond Armor     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 90   | 0    | ability 90                                                          |
| 0x4A | Regen Ring        | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 39   | 0    | ability 39                                                          |
| 0x4B | Giant`s Ring      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 40   | 0    | ability 40                                                          |
| 0x4C | Gaea`s Ring       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 41   | 0    | ability 41                                                          |
| 0x4D | Strength Love     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 42   | 0    | ability 42                                                          |
| 0x4E | Power Wrist       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 43   | 0    | ability 43                                                          |
| 0x4F | Hyper Wrist       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 44   | 0    | ability 44                                                          |
| 0x50 | Turtle Shell      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 45   | 0    | ability 45                                                          |
| 0x51 | Orihalcon         | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 46   | 0    | ability 46                                                          |
| 0x52 | Adamantine        | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 47   | 0    | ability 47                                                          |
| 0x53 | Rune Armlet       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 51   | 0    | ability 51                                                          |
| 0x54 | Force Armlet      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 52   | 0    | ability 52                                                          |
| 0x55 | Magic Armlet      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 53   | 0    | ability 53                                                          |
| 0x56 | Circlet           | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 48   | 0    | ability 48                                                          |
| 0x57 | Hypno Crown       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 49   | 0    | ability 49                                                          |
| 0x58 | Royal Crown       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 50   | 0    | ability 50                                                          |
| 0x59 | Jet Engine        | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 54   | 0    | ability 54                                                          |
| 0x5A | Rocket Engine     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 55   | 0    | ability 55                                                          |
| 0x5B | Moon Curtain      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 71   | 0    | ability 71                                                          |
| 0x5C | Steel Curtain     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 70   | 0    | ability 70                                                          |
| 0x5D | Glow Curtain      | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 72   | 0    | ability 72                                                          |
| 0x5E | Accelerator       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 73   | 0    | ability 73                                                          |
| 0x5F | Monk`s Code       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 60   | 0    | ability 60                                                          |
| 0x60 | Knight`s Code     | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 62   | 0    | ability 62                                                          |
| 0x61 | Doc`s Code        | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 59   | 0    | ability 59                                                          |
| 0x62 | Hundred Needles   | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 61   | 0    | ability 61                                                          |
| 0x63 | Three Stars       | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 76   | 0    | ability 76                                                          |
| 0x64 | Ribbon            | 17     | TEACH_GF_ABILITY | 0x05    | MENU+GF                  | 77   | 0    | ability 77                                                          |
| 0x65 | Normal Ammo       | 8      | AMMO             | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x66 | Shotgun Ammo      | 8      | AMMO             | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x67 | Dark Ammo         | 8      | AMMO             | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x68 | Fire Ammo         | 8      | AMMO             | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x69 | Demolition Ammo   | 8      | AMMO             | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x6A | Fast Ammo         | 8      | AMMO             | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x6B | AP Ammo           | 8      | AMMO             | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x6C | Pulse Ammo        | 8      | AMMO             | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x6D | M-Stone Piece     | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x6E | Magic Stone       | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x6F | Wizard Stone      | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x70 | Ochu Tentacle     | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x71 | Healing Water     | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x72 | Cockatrice Pinion | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x73 | Zombie Powder     | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x74 | Lightweight       | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x75 | Sharp Spike       | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x76 | Screw             | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x77 | Saw Blade         | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x78 | Mesmerize Blade   | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x79 | Vampire Fang      | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x7A | Fury Fragment     | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x7B | Betrayal Sword    | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x7C | Sleep Powder      | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x7D | Life Ring         | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x7E | Dragon Fang       | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x7F | Spider Web        | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 1    | 0    | limit 1                                                             |
| 0x80 | Coral Fragment    | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 2    | 0    | limit 2                                                             |
| 0x81 | Curse Spike       | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 3    | 0    | limit 3                                                             |
| 0x82 | Black Hole        | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 4    | 0    | limit 4                                                             |
| 0x83 | Water Crystal     | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 5    | 0    | limit 5                                                             |
| 0x84 | Missile           | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 6    | 0    | limit 6                                                             |
| 0x85 | Mystery Fluid     | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 7    | 0    | limit 7                                                             |
| 0x86 | Running Fire      | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 8    | 0    | limit 8                                                             |
| 0x87 | Inferno Fang      | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 9    | 0    | limit 9                                                             |
| 0x88 | Malboro Tentacle  | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 10   | 0    | limit 10                                                            |
| 0x89 | Whisper           | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 11   | 0    | limit 11                                                            |
| 0x8A | Laser Cannon      | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 12   | 0    | limit 12                                                            |
| 0x8B | Barrier           | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 13   | 0    | limit 13                                                            |
| 0x8C | Power Generator   | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 14   | 0    | limit 14                                                            |
| 0x8D | Dark Matter       | 19     | QUISTIS_LIMIT    | 0x43    | MENU+CHR+QUIS            | 15   | 0    | limit 15                                                            |
| 0x8E | Bomb Fragment     | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 2    | 8    | Ifrit +8                                                            |
| 0x8F | Red Fang          | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 2    | 16   | Ifrit +16                                                           |
| 0x90 | Arctic Wind       | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 1    | 8    | Shiva +8                                                            |
| 0x91 | North Wind        | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 1    | 16   | Shiva +16                                                           |
| 0x92 | Dynamo Stone      | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 0    | 16   | Quezacotl +16                                                       |
| 0x93 | Shear Feather     | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 8    | 8    | Pandemona +8                                                        |
| 0x94 | Venom Fang        | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 11   | 16   | Doomtrain +16                                                       |
| 0x95 | Steel Orb         | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 5    | 16   | Diablos +16                                                         |
| 0x96 | Moon Stone        | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 10   | 16   | Alexander +16                                                       |
| 0x97 | Dino Bone         | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 4    | 16   | Brothers +16                                                        |
| 0x98 | Windmill          | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 8    | 16   | Pandemona +16                                                       |
| 0x99 | Dragon Skin       | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 6    | 16   | Carbuncle +16                                                       |
| 0x9A | Fish Fin          | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 7    | 10   | Leviathan +10                                                       |
| 0x9B | Dragon Fin        | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 9    | 16   | Cerberus +16                                                        |
| 0x9C | Silence Powder    | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 3    | 16   | Siren +16                                                           |
| 0x9D | Poison Powder     | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 11   | 8    | Doomtrain +8                                                        |
| 0x9E | Dead Spirit       | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0x9F | Chef`s Knife      | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 14   | 16   | Tonberry +16                                                        |
| 0xA0 | Cactus Thorn      | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 13   | 16   | Cactuar +16                                                         |
| 0xA1 | Shaman Stone      | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 12   | 16   | Bahamut +16                                                         |
| 0xA2 | Fuel              | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0xA3 | Girl Next Door    | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0xA4 | Sorceress` Letter | 10     | REFINE_ONLY      | 0x00    | -                        | 0    | 0    |                                                                     |
| 0xA5 | Chocobo`s Tag     | 13     | CHOCOBO_TAG      | 0x01    | MENU                     | 0    | 0    |                                                                     |
| 0xA6 | Pet Nametag       | 12     | PET_NAMETAG      | 0x01    | MENU                     | 0    | 0    |                                                                     |
| 0xA7 | Solomon Ring      | 15     | SOLOMON_RING     | 0x01    | MENU                     | 0    | 0    | grants GF 11 (Doomtrain)                                            |
| 0xA8 | Magical Lamp      | 14     | MAGICAL_LAMP     | 0x01    | MENU                     | 43   | 3    | grants GF 5 (Diablos)                                               |
| 0xA9 | HP Up             | 20     | STAT_UP          | 0x03    | MENU+CHR                 | 10   | 1    | HP +10                                                              |
| 0xAA | Str Up            | 20     | STAT_UP          | 0x03    | MENU+CHR                 | 1    | 2    | STR +1                                                              |
| 0xAB | Vit Up            | 20     | STAT_UP          | 0x03    | MENU+CHR                 | 1    | 4    | VIT +1                                                              |
| 0xAC | Mag Up            | 20     | STAT_UP          | 0x03    | MENU+CHR                 | 1    | 8    | MAG +1                                                              |
| 0xAD | Spr Up            | 20     | STAT_UP          | 0x03    | MENU+CHR                 | 1    | 16   | SPR +1                                                              |
| 0xAE | Spd Up            | 20     | STAT_UP          | 0x03    | MENU+CHR                 | 1    | 32   | SPD +1                                                              |
| 0xAF | Luck Up           | 20     | STAT_UP          | 0x03    | MENU+CHR                 | 1    | 64   | Luck +1                                                             |
| 0xB0 | LuvLuv G          | 16     | GF_COMPATIBILITY | 0x83    | MENU+CHR+OTHERGF         | 255  | 101  | all GFs + 101                                                       |
| 0xB1 | Weapons Mon 1st   | 9      | MAGAZINE         | 0x01    | MENU                     | 0    | 3    | pages 0-3                                                           |
| 0xB2 | Weapons Mon Mar   | 9      | MAGAZINE         | 0x01    | MENU                     | 4    | 7    | pages 4-7                                                           |
| 0xB3 | Weapons Mon Apr   | 9      | MAGAZINE         | 0x01    | MENU                     | 8    | 11   | pages 8-11                                                          |
| 0xB4 | Weapons Mon May   | 9      | MAGAZINE         | 0x01    | MENU                     | 12   | 15   | pages 12-15                                                         |
| 0xB5 | Weapons Mon Jun   | 9      | MAGAZINE         | 0x01    | MENU                     | 16   | 19   | pages 16-19                                                         |
| 0xB6 | Weapons Mon Jul   | 9      | MAGAZINE         | 0x01    | MENU                     | 20   | 23   | pages 20-23                                                         |
| 0xB7 | Weapons Mon Aug   | 9      | MAGAZINE         | 0x01    | MENU                     | 24   | 27   | pages 24-27                                                         |
| 0xB8 | Combat King 001   | 9      | MAGAZINE         | 0x01    | MENU                     | 28   | 28   | pages 28-28                                                         |
| 0xB9 | Combat King 002   | 9      | MAGAZINE         | 0x02    | CHR                      | 29   | 29   | pages 29-29                                                         |
| 0xBA | Combat King 003   | 9      | MAGAZINE         | 0x02    | CHR                      | 30   | 30   | pages 30-30                                                         |
| 0xBB | Combat King 004   | 9      | MAGAZINE         | 0x02    | CHR                      | 31   | 31   | pages 31-31                                                         |
| 0xBC | Combat King 005   | 9      | MAGAZINE         | 0x02    | CHR                      | 32   | 32   | pages 32-32                                                         |
| 0xBD | Pet Pals Vol.1    | 9      | MAGAZINE         | 0x02    | CHR                      | 33   | 33   | pages 33-33                                                         |
| 0xBE | Pet Pals Vol.2    | 9      | MAGAZINE         | 0x03    | MENU+CHR                 | 34   | 34   | pages 34-34                                                         |
| 0xBF | Pet Pals Vol.3    | 9      | MAGAZINE         | 0x03    | MENU+CHR                 | 35   | 35   | pages 35-35                                                         |
| 0xC0 | Pet Pals Vol.4    | 9      | MAGAZINE         | 0x03    | MENU+CHR                 | 36   | 36   | pages 36-36                                                         |
| 0xC1 | Pet Pals Vol.5    | 9      | MAGAZINE         | 0x03    | MENU+CHR                 | 37   | 37   | pages 37-37                                                         |
| 0xC2 | Pet Pals Vol.6    | 9      | MAGAZINE         | 0x03    | MENU+CHR                 | 38   | 38   | pages 38-38                                                         |
| 0xC3 | Occult Fan I      | 9      | MAGAZINE         | 0x03    | MENU+CHR                 | 39   | 39   | pages 39-39                                                         |
| 0xC4 | Occult Fan II     | 9      | MAGAZINE         | 0x04    | GF                       | 40   | 40   | pages 40-40                                                         |
| 0xC5 | Occult Fan III    | 9      | MAGAZINE         | 0x04    | GF                       | 41   | 41   | pages 41-41                                                         |
| 0xC6 | Occult Fan IV     | 9      | MAGAZINE         | 0x04    | GF                       | 42   | 42   | pages 42-42                                                         |

## Function addresses

| Function | Address | Description |
|---|---|---|
| `Mitem_GetEffectiveFlags` | 0x4F7530 | Computes the effective `flags` byte, overriding it for types 9/12/13/14/15/19 |
| `K_ITEM_TYPE_TO_ACTION` | 0xB88AC4 | 28-byte item-type → action LUT (global variable/data, not a function; named `byte_B88AC4` in the community IDB) |