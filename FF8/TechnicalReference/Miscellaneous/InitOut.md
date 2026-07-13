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
| 0x0900 | 20\*20    | [Shops](#shops)                                             |
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
| 0x03   | 1 byte   | Unused padding (high byte of the 32-bit party word; never a member) |
| 0x04   | 4 bytes  | [Unlocked weapons](#unlocked-weapons) (u32 bitmask)              |
| 0x08   | 12 bytes | Griever name (FF8 text format)                                    |
| 0x14   | 1 byte   | Weapon ID Laguna                                                 |
| 0x15   | 1 byte   | Weapon ID Kiros                                                  |
| 0x16   | 1 byte   | Weapon ID Ward                                                   |
| 0x17   | 1 byte   | Status-menu selection index (persisted menu cursor; used, not padding) |
| 0x18   | 4 bytes  | Amount of Gil                                                    |
| 0x1C   | 4 bytes  | Amount of Gil (Laguna squad)                                     |
| 0x20   | 2 bytes  | Limit Break Quistis                                              |
| 0x22   | 2 bytes  | Limit Break Zell                                                 |
| 0x24   | 1 byte   | Limit Break Irvine                                               |
| 0x25   | 1 byte   | Limit Break Selphie                                              |
| 0x26   | 1 byte   | Limit Break Angelo completed                                     |
| 0x27   | 1 byte   | Limit Break Angelo known                                         |
| 0x28   | 8 bytes  | Limit Break Angelo points                                        |
| 0x30   | 32 bytes | [Items battle order](#items-battle-order)                        |

Party member bytes hold a character id (`FF8ComId`): 0 Squall, 1 Zell, 2 Irvine, 3 Quistis,
4 Rinoa, 5 Selphie, 6 Seifer, 7 Edea, 8 Laguna, 9 Kiros, 10 Ward, 0xFF empty.

### Unlocked weapons

Offset 0x04 is a single 32-bit bitmask (not four separate bytes), read and written by the
Junk Shop: bit *i* = weapon-upgrade recipe *i* has been built/owned. The bit index is a
direct 1:1 with the kernel [weapon](../../list/weapon/) id — bit 0 Revolver, bit 1 Shear
Trigger, … up to **bit 27** (Strange Vision). Only bits 0-27 are used (the 28 upgradeable
party weapons); the game never touches bits 28-31, and kernel weapon ids 28-32 (the fixed
Laguna-party weapons) have no bit because they are not upgradeable.

### Limit breaks

Every limit-break field except the Angelo points is a bitfield of individually-unlockable
moves (structure confirmed from code; each bit indexes a kernel table). The move *names*
live in the game message files, so only the anchoring entries are certain.

| Offset | Field                   | Type            | Bits | Meaning                                                              |
|--------|-------------------------|-----------------|------|---------------------------------------------------------------------|
| 0x20   | Quistis (Blue Magic)     | 16-bit bitfield | 0-15 | Learned Blue Magic (bit *i* = `K_BLUE_MAGIC[i]`; bit 0 Laser Eye … bit 15 Shockwave Pulse) |
| 0x22   | Zell (Duel)              | 16-bit bitfield | 0-9  | Known Duel moves (bit 0 Punch Rush … bit 9 My Final Heaven; bits 10-15 unused) |
| 0x24   | Irvine (Shot)            | 8-bit bitfield  | 0-7  | Unlocked Shot ammo (bit *i* = item id 101+*i*: Normal Ammo … Pulse Ammo) |
| 0x25   | Selphie (Slot)           | 8-bit bitfield  | 0-5  | Unlocked Slot special spells (magic-text ids 51-56; names not in the exe) |
| 0x26   | Angelo completed         | 8-bit bitfield  | 0-7  | Angelo commands fully learned (bit 0 Angelo Rush … bit 7 Wishing Star) |
| 0x27   | Angelo known             | 8-bit bitfield  | 0-7  | Angelo commands known / in learning (same bit order)                 |
| 0x28   | Angelo points            | 8 counters      | —    | Per-command remaining points to learn (counts down to 0), **not** a bitfield |

### Items battle order

The 32-byte block at Misc offset 0x30 is an ordering/index array (not a bitmask or id
list): entry `n` corresponds to battle-usable item id `n + 1` (ids 1-32) and holds that
item's display slot (0-31) in the in-battle Item menu. The game keeps it compact — on
picking up an item it assigns the lowest free slot and shifts entries — so the battle Item
list stays in a stable order across pickups.

## Shops

The 400-byte block at 0x0900 is **20 shop records of 20 bytes each**:

| Offset | Size     | Data                                                              |
|--------|----------|------------------------------------------------------------------|
| 0x00   | 16 bytes | Per-slot availability cache (one boolean byte per shop slot: 0 hidden, 1 buyable) |
| 0x10   | 2 bytes  | Visited flag (set to 1 on first entry; no reader found — cosmetic) |
| 0x12   | 2 bytes  | Padding                                                          |

The 16 availability bytes are a **recomputed cache, not authoritative state**. On every shop
entry the game rebuilds them from the static `shop.bin` (each slot's item id + a per-item
unlock threshold) and a story-progress flag — `available = ((storyFlag << 8) + threshold) >
128` — and writes the result back over these bytes. Editing them (in `init.out` or a save)
therefore has **no lasting effect**; to change what a shop sells or when items unlock, edit
`shop.bin`, not this block. A new game zeroes the whole block, and no code seeds it from the
`init.out` template. Prices come from
[`price.bin`](../../menu/price/), also outside this file.

## Guardian Forces — learned abilities & AP

A GF's "Complete abilities" field (record offset 0x14, 16 bytes = 128 bits) is a single
bitfield shared by every GF: bit *i* set means the GF has learned ability id *i*, stored at
byte `i / 8`, bit `i % 8`. The ability ids are the standard
[Junctionable Abilities]({{site.baseurl}}/technical-reference/list/junctionable-abilities/)
list (0x00 None … 0x73 Card Mod); ids 0x53-0x5B (SumMag+10%..40%, GFHP+10%..40%, Boost)
cross-check exactly against the
[kernel.bin GF-abilities section](../../main/kernel/gf-abilities/).

The AP field (record offset 0x24, 24 bytes: 22 used slots + 2 unused) holds, per ability
slot, how much AP has been invested. The slots are **not** indexed by global ability id —
slot *N* is the *N*-th entry in that GF's own learnable-ability list, whose id/AP-cost order
is defined in the [kernel Junctionable-GFs section](../../main/kernel/junctionable-gfs/) and
is not part of `init.out`.

The **Learning ability** byte (record offset 0x40) is the ability id the GF is currently
learning toward (same id space as the ability bitfield); earned AP is applied to it. It is
an ability id, not an AP amount.

The **Exists** byte (record offset 0x11) is a plain boolean: the GF has been obtained
(junctioned/acquired at least once). At a fresh new game every GF except Quezacotl reads 0.

Record offset 0x10 is unused padding (no game code reads it).

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

### Unused bytes

Offsets 0x5A (after `JunctionedGFs`), 0x6F (the junction sub-struct's trailing pad, after
`JunctionMentalDefense`) and 0x95 (after `Exists`) are reserved padding — no game code reads
them.

## Configuration notes

The 20-byte [Configuration](../game-save-format/#configuration) record is shared with saves.
Points relevant when editing `init.out`:

- Battle speed, battle-message speed, field-message speed and camera speed are 0-4 sliders
  (0 = slowest, 4 = fastest); battle speed drives the ATB fill rate (`4000 * (value + 1)`).
- The `flag` byte (0x04) is a controller/config bitfield: bit0 battle-vibration trigger,
  bit4 vibration hardware present (auto), bit5 use custom button config, bit6 no controller
  detected (auto), bit7 controls modified from default.
- The `scan` byte (0x05) is a real option (reached as the high byte of the `flag`+`scan`
  word, mask 0x0100 in the options menu). Bit 0 is the **Scan detail** setting: cleared =
  a repeat Scan on an already-scanned enemy shows an abbreviated result; set = always show
  the full Scan info window. Only bit 0 is used.
- Offset 0x07 is the **map-seal** bitfield (`MapSeal`): bit0 Item, bit1 Magic, bit2 GF,
  bit3 Draw, bit4 Command ability, bit5 Limit break, bit6 Resurrection, bit7 Save — each
  bit locks that menu action when a story event seals the map.
- The 12 button bytes (0x08-0x13) are a remap table: each physical slot (L2, R2, L1, R1,
  Triangle, Circle, Cross, Square, Select, unk1, unk2, Start) stores the 1-based id of the
  logical action it triggers (default = its own slot + 1). Actions identified from code:
  1+2 = Flee-battle hold combo, 3 = menu page / previous character, 4 = Renzokuken
  critical-timing (battle) / next character (menus), 5 = Cancel/Back, 6 = Menu,
  7 = Confirm/Talk, 8 = Examine, 9 = Reset controls, 12 = Pause. Ids 10 and 11 are unused
  filler slots (a PSX pad exposes only 10 configurable buttons; nothing maps to or consumes
  them).
