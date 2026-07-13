---
layout: default
parent: Miscellaneous
title: New Game Data (init.out)
author: HobbitDur
permalink: /technical-reference/miscellaneous/init-out/
---

`init.out` is the template the game reads when starting a new game: initial GF stats,
character stats, gil, items, and the default game configuration. It uses the same record
layouts as the [Game Save Format](../game-save-format/) (GF/Character/Config/Misc/Items),
but as a template file rather than a save it carries none of a save's checksum/preview
header and none of its field/battle/world-map state: `init.out` is exactly the save
format's structure starting at the Guardian Forces block and ending right after the Items
table, i.e. every offset below equals the save format's offset minus 0x50 (80).

| Offset | Size      | Data                                                      |
|--------|-----------|------------------------------------------------------------|
| 0x0000 | 16\*68    | [Guardian Forces](../game-save-format/#guardian-forces)   |
| 0x0440 | 8\*152    | [Characters](../game-save-format/#characters)              |
| 0x0900 | 400 bytes | Shops (unknown structure)                                   |
| 0x0A90 | 20 bytes  | [Configuration](../game-save-format/#configuration)         |
| 0x0AA4 | 80 bytes  | [Misc](#misc)                                                |
| 0x0AF4 | 396 bytes | Items: 198 \* (Item ID, Quantity)                            |

Total size once every item slot is present: 0x0C80 (3200) bytes. The file as shipped only
reserves the first 4 item slots (2812 bytes); tools that edit the full item table (e.g.
[Quezacotl](../../tools/)) grow it to 3200 bytes on load, zero-filling the new item slots.

## Misc

Same fields as the save format's block between Party and Items Battle Order, renumbered
from this file's own base offset (0x0AA4):

| Offset | Size     | Data                                                          |
|--------|----------|----------------------------------------------------------------|
| 0x00   | 1 byte   | Party member 1                                                  |
| 0x01   | 1 byte   | Party member 2                                                  |
| 0x02   | 1 byte   | Party member 3                                                  |
| 0x03   | 1 byte   | Party member 4 (0xFF terminated)                                 |
| 0x04   | 1 byte   | Known weapons 1                                                  |
| 0x05   | 1 byte   | Known weapons 2                                                  |
| 0x06   | 1 byte   | Known weapons 3                                                  |
| 0x07   | 1 byte   | Known weapons 4                                                  |
| 0x08   | 12 bytes | Griever name (FF8 text format)                                    |
| 0x14   | 1 byte   | Weapon ID Laguna                                                 |
| 0x15   | 1 byte   | Weapon ID Kiros                                                  |
| 0x16   | 1 byte   | Weapon ID Ward                                                   |
| 0x17   | 1 byte   | Unused                                                           |
| 0x18   | 4 bytes  | Amount of Gil                                                    |
| 0x1C   | 4 bytes  | Amount of Gil (Laguna squad)                                     |
| 0x20   | 2 bytes  | Limit Break Quistis                                              |
| 0x22   | 2 bytes  | Limit Break Zell                                                 |
| 0x24   | 1 byte   | Limit Break Irvine                                               |
| 0x25   | 1 byte   | Limit Break Selphie                                              |
| 0x26   | 1 byte   | Limit Break Angelo completed                                     |
| 0x27   | 1 byte   | Limit Break Angelo known                                         |
| 0x28   | 8 bytes  | Limit Break Angelo points                                        |
| 0x30   | 32 bytes | Items battle order                                               |

Party member bytes hold a character id (`FF8ComId`): 0 Squall, 1 Zell, 2 Irvine, 3 Quistis,
4 Rinoa, 5 Selphie, 6 Seifer, 7 Edea, 8 Laguna, 9 Kiros, 10 Ward, 0xFF empty.

## Guardian Forces — learned abilities & AP

A GF's "Complete abilities" field (record offset 0x14, 16 bytes = 128 bits) is a single
bitfield shared by every GF: bit *i* set means the GF has learned ability id *i*, stored at
byte `i / 8`, bit `i % 8`. The ability ids are the standard
[Junctionable Abilities]({{site.baseurl}}/technical-reference/list/junctionable-abilities/)
list (0x00 None … 0x73 Card Mod); ids 0x53-0x5B (SumMag+10%..40%, GFHP+10%..40%, Boost)
cross-check exactly against the
[kernel.bin GF-abilities section](../../main/kernel/gf-abilities/).

The AP field (record offset 0x24, 24 bytes: 22 used slots + 2 unused) holds, per ability
slot, how much AP has been invested learning it.

The **Exists** byte (record offset 0x11) is a plain boolean: the GF has been obtained
(junctioned/acquired at least once). At a fresh new game every GF except Quezacotl reads 0.

## Characters — field notes

These refine the shared [character record](../game-save-format/#characters); offsets are
within one 152-byte record.

### Equipped abilities (0x50-0x57)

Two 4-byte blocks of the same
[ability id space]({{site.baseurl}}/technical-reference/list/junctionable-abilities/), not a
"3 commands + padding + 4 abilities" layout:

| Offset | Field                | Valid ids   | Meaning                                        |
|--------|----------------------|-------------|------------------------------------------------|
| 0x50   | `activeAbilities[4]`  | 0x14-0x26   | Equipped command abilities (Magic, GF, Draw…)  |
| 0x54   | `passifAbilities[4]`  | 0x27-0x39   | Equipped passive abilities (HP+20%, Str+40%…)   |

The game resets any value outside these ranges to 0 (none) on load.

### Junction stat assignments (0x5C-0x6E)

Each junction byte (HP/STR/VIT/MAG/SPR/SPD/EVA/HIT/LCK, elemental & mental attack, the four
elemental-defense and four mental-defense slots) stores a **magic id** — which spell is
junctioned to that stat, `0` = none. The actual stat bonus is that spell's junction value
(from the [kernel magic data](../../main/kernel/magic/)) scaled by the quantity of the
spell stocked, so the byte itself is only the
[magic id]({{site.baseurl}}/technical-reference/list/magic-list/).

### GF compatibility (0x70, 16 × 2 bytes)

One `uint16` per GF. The game clamps compatibility to **1000 (minimum / neutral) … 6000
(maximum)**; higher values summon the GF faster.

### Status (0x96, 2 bytes)

A 16-bit [Status 1]({{site.baseurl}}/technical-reference/list/status-flags/) bitfield (not an
8-bit byte + unknown byte). Only bits 0-6 are real, save-persistent statuses (Death, Poison,
Petrify, Darkness, Silence, Berserk, Zombie). Bit 7 is padding, bits 8-9 (`HP < 25%`,
`HP < 50%`) are synthetic flags the game recomputes from current HP, and bits 10-15 are
unused.

### Exists (0x94)

Plain boolean: the character has joined the party at least once (is recruited and available
in menus / party select).

## Configuration notes

The 20-byte [Configuration](../game-save-format/#configuration) record is shared with saves.
Points relevant when editing `init.out`:

- Battle speed, battle-message speed, field-message speed and camera are 0-4 sliders
  (0 = slowest, 4 = fastest); battle speed drives the ATB fill rate (`4000 * (value + 1)`).
- Offset 0x07 is the **map-seal** bitfield (`MapSeal`): bit0 Item, bit1 Magic, bit2 GF,
  bit3 Draw, bit4 Command ability, bit5 Limit break, bit6 Resurrection, bit7 Save — each
  bit locks that menu action when a story event seals the map.
- The 12 button bytes (0x08-0x13) are a remap permutation table: each byte holds the
  1-based index of the logical button assigned to that physical slot (default = its own
  slot number), not a hardware key code.
- The `scan` byte (0x05) is unused/vestigial in the PC build.
