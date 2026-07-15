---
layout: default
parent: Menu
title: mmagic.bin file format
permalink: /technical-reference/menu/mmagic/
author: hobbitdur, Nihil
---

# mmagic.bin

`menu/mmagic.bin` controls which spells the player can cast from the field **Magic** menu (outside of battle). It is a flat array of 4-byte records with no header.

The file is 228 bytes long: `228 / 4 = 57` records. This matches the kernel magic-data section exactly (57 sections, ID 0 being an unused/dummy entry), so a record's position **is** the magic ID:

| Record index | Magic ID | Spell |
|--------------|----------|-------|
| 0            | 0        | Unused / dummy |
| 1            | 1        | Fire  |
| ...          | ...      | ...   |
| 21           | 21       | Cure  |
| 24           | 24       | Life  |
| 25           | 25       | Full-life |
| ...          | ...      | ...   |
| 56           | 56       | (last magic) |

See the [Magic list](../../list/magic-list/) for the full ID → spell mapping.

## Record layout

Each 4-byte record has the structure below (IDA type `mmmagicData`):

| Offset | Field             | Typical value | Meaning |
|--------|-------------------|---------------|---------|
| 0x00   | `menuUsableFlags` | `00`/`03`/`23` | Field-menu usability + intended target. See below. |
| 0x01   | `constFF_1`       | `FF`          | Unused, always `0xFF`. |
| 0x02   | `constFF_2`       | `FF`          | Unused, always `0xFF`. |
| 0x03   | `pad_00`          | `00`          | Padding, always `0x00`. |

Only byte `0x00` carries information; the remaining three bytes are constant (`FF FF 00`) for every record.

## Byte 0 — `menuUsableFlags`

Observed values across the retail file:

| Value | Bits set        | Meaning |
|-------|-----------------|---------|
| `0x00`| —               | Spell is hidden from the field Magic menu. |
| `0x03`| bit0 + bit1     | Usable in the menu, targets a **living** ally. |
| `0x23`| bit0 + bit1 + bit5 | Usable in the menu, targets a **KO'd** ally (revive spells). |

**Important — what the PC executable actually reads:** the magic-menu code touches this buffer at only two places, and both mask it with `& 1`:

- Drawing a magic-list row (`sub_4F7140`) — `menuUsableFlags & 1` picks the text colour: bit clear → the spell is drawn greyed-out/disabled; bit set → normal, selectable.
- The main field magic menu (`linked_menu_magic_sub_4F02F0`) — same `& 1` test to decide whether the entry is enabled.

So on the PC port **only bit 0 (`0x01`) is consulted** — `0x03` and `0x23` are treated identically (both "usable"). The higher bits (`0x02`, `0x20`) are never read.

The living-vs-KO'd distinction that the `0x23` value seems to encode is instead derived at runtime from the spell's **kernel `AttackType`**: the game recognises revive spells (Life / Full-life) through the `ATTACK_TYPE_REVIVE … ATTACK_TYPE_REVIVE_AT_FULL_HP` range, not through this byte. This can be seen in the same draw routine, where revive spells are greyed out when the Resurrection map-seal is active (`checkMapSeal(MAP_SEAL_RESURRECTION_LOCKED)` + `K_MAGIC[id].attackType`). Bits `0x02`/`0x20` therefore appear to be legacy/informational data carried over from the PSX version and have no effect on the retail PC EXE.

## Menu-usable spells in the retail file

Every record is `00 FF FF 00` except the curative/support block:

| Magic ID | Spell     | Byte 0 | Menu target |
|----------|-----------|--------|-------------|
| 21       | Cure      | `0x03` | Living ally |
| 22       | Cura      | `0x03` | Living ally |
| 23       | Curaga    | `0x03` | Living ally |
| 24       | Life      | `0x23` | KO'd ally   |
| 25       | Full-life | `0x23` | KO'd ally   |
| 26       | Regen     | `0x00` | *(not usable in menu)* |
| 27       | Esuna     | `0x03` | Living ally |
| 28       | Dispel    | `0x03` | Living ally |

All other magic (offensive spells, buffs like Protect/Shell, Regen, etc.) have byte 0 = `0x00` and cannot be selected from the field Magic menu.

## Loading

The file is read into a fixed buffer at menu init (`MenuReadFiles`) and re-read when the battle-command magic list is built (`sub_4C0B30`), both via `au_re_SmPcRead`. It is released by `free_all_files`.

## Relevant executable addresses (FF8_EN.exe)

| Symbol | Address | Role |
|--------|---------|------|
| `mmagicbinbuffer`             | `0x1D2BB10` | Loaded file buffer: `mmmagicData[57]`, indexed by magic ID. |
| `MenuReadFiles`               | `0x4A1C7A`  | Loads `mmagic.bin` into the buffer. |
| `linked_menu_magic_sub_4F02F0`| `0x4F02F0`  | Field magic menu; tests `menuUsableFlags & 1` at `0x4F0625`. |
| `sub_4F7140`                  | `0x4F7140`  | Draws a magic-list row; tests `menuUsableFlags & 1` at `0x4F71E9`. |
| `sub_4C0B30`                  | `0x4C0B30`  | Rebuilds the magic list (re-reads the file). |
| `free_all_files`              | `0x4A1EC0`  | Frees the buffer. |
