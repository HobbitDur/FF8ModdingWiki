---
layout: default
parent: Battle
title: Element System
permalink: /technical-reference/battle/element-system/
---

This page documents how FF8's eight elements are represented, stored, consumed and displayed
end to end — kernel data, battle runtime, enemy AI, junction and UI — and records where the
hard limits sit for anyone considering adding a ninth element.

Function and field names used here are the real names in the IDA database (verified 2026-09,
FF8_EN.exe 2013). An address table is at the [bottom of this page](#function-address-reference).

1. TOC
{:toc}

## Representation

An element is a **bit in a 1-byte bitfield** (`ElementType`). All eight bits are assigned;
there is no spare bit.

| Bit | Mask | Element | Index |
|-----|------|---------|-------|
| 0 | 0x01 | Fire    | 0 |
| 1 | 0x02 | Ice     | 1 |
| 2 | 0x04 | Thunder | 2 |
| 3 | 0x08 | Earth   | 3 |
| 4 | 0x10 | Poison  | 4 |
| 5 | 0x20 | Wind    | 5 |
| 6 | 0x40 | Water   | 6 |
| 7 | 0x80 | Holy    | 7 |

`0x00` means non-elemental. The **index** column is what the runtime actually uses: the
bitfield is converted to a list of set-bit indices by `GetFlaggedBitIndexList`, and every
resistance lookup is indexed, not masked.

> `GetFlaggedBitIndexList` was previously named `GetElementFlagged`. It is **not**
> element-specific — two of its four callers pass `BATTLE_SLOT_DATA.target_info_mask` and
> use the result as a list of target slot indices. That is why its loop is 16 bits wide.

### Only the first element counts

Both damage paths read `list[0]` only — the **lowest set bit**. A spell flagged
`Fire|Ice` behaves as pure Fire. Multi-element attacks are not implemented, even though
the data format allows the bits to be combined.

## Where the element byte lives in data

`Battle_applyDamage` loads the attack element into `HIT_ELEMENT` from **twelve** kernel
sections, one store per command source. Each offset below was read from its store site and
checked against that section's page:

| Kernel section | Element offset | Record size | Retail values seen |
|----------------|----------------|-------------|--------------------|
| §2 Magic | `0x0E` | 60 | all eight, and 0 |
| §3 Junctionable GFs | `0x0D` | 132 | all eight, and 0 |
| §4 Enemy attacks | `0x0A` | 20 | all eight, and 0 |
| §6 Renzokuken finishers | `0x0D` | 24 | 0 only |
| §8 Battle items | `0x17` | 24 | 0, Holy |
| §10 Non-junctionable GF attacks | `0x0B` | 20 | 0, Fire |
| §11 Command abilities in battle | `0x08` | 16 | 0 only |
| §19 Temporary character limit breaks | `0x0D` | 24 | 0 only |
| §20 Blue magic | `0x0C` | 16 | 0, Fire, Thunder, Water |
| §22 Shot | `0x0D` | 24 | 0, Fire |
| §23 Duel | `0x0D` | 32 | 0 only |
| §26 Rinoa limit breaks (part 2) | `0x0B` | 20 | 0 only |

A thirteenth field reaches it indirectly: magic `jElemAttack` (`0x20`) becomes a character's
attack element through the junction (`get_elem_attack` → `hitElement` → `hit_element`).

**Across all 566 records of these fields, and every `jElemAttack`, no retail value has more
than one bit set.** Combined with the damage paths reading only the lowest set bit, the
attack element is an index in everything but encoding.

The junction defence mask is different: magic `jElemDefense` (`0x22`) **is** multi-bit in
retail — 8 of 57 spells, including `0xFF` — and it is the only element field that is.

Blue magic's element is at `0x0C`; the load at `0x0D` right beside it in the code is the
status accuracy, which is easy to mistake for it.

Free space in the magic record: `0x0F` (after the element byte) and `0x3A`–`0x3B` at the end
of the record have no readers.

Per-target resistance is stored per element, not as a bitfield:

| Source | Offset | Layout |
|--------|--------|--------|
| Monster `.dat` info section | `+0x160` | `ElemRes[8]`, one byte per element |
| `FF8FieldCharData` (party) | `+0x194` | `elemDefInfo[8]`, one **word** per element |
| `FF8BattleSlotData` (runtime) | `+0x44` | `elem_def[8]`, one word per element |

## Runtime resistance array

`FF8BattleSlotData.elem_def` is a `uint16[8]` at `+0x44`, immediately followed by
`timer[16]` at `+0x54`. The scale is:

- **800** = neutral
- **< 800** = weak (more damage)
- **900** = immune
- **> 900** = absorb (damage goes negative, `HIT_TYPE_RESTORATIVE` is set)
- cap 1000 from the junction path

Two producers fill it:

- **Monsters** — `setMonsterInfoFromDatInfoSection`: `elem_def[i] = 10 * ElemRes[i]` for `i` in 0..7.
- **Party** — `setBattleSlotData`: straight 8-word copy of `FF8FieldCharData.elemDefInfo`,
  which `Stat_RefreshCharaBattleStats` computes from junctions via `getMagicElemDefValue`
  (base 800, `+= jElemDefenseValue * stock / 100` over 4 junction slots, capped at 1000).

Two consumers read it:

- `Damage_ApplyPhysicalModifiers`: `dmg += dmg * HIT_ELEMENT_PERCENT * (800 - elem_def[i]) / 10000`
- `Damage_ComputeMagicAndGF`: `dmg = dmg * (900 - elem_def[i]) / 100`

A Zombie target hit by Holy uses a forced value of **700** (double damage) instead of the
stored resistance, in both paths.

### The Aura / Charged drain reads Thunder

In `Damage_ApplyPhysicalModifiers`, the Charged-status melee drain bonus is computed as
`attacker_maxHP / 10 * (900 - elem_def[2]) / 100` — i.e. scaled by the **attacker's Thunder
resistance**. Verified at byte level: `66 8B 88 58 7B D2 01` = `mov cx, [eax+1D27B58h]`, and
`0x1D27B58 - BATTLE_SLOT_DATA(0x1D27B10) = 0x48` = `elem_def[2]`. The same read appears at
`0x491622`. This looks like an original-code quirk rather than a deliberate design.

## Enemy AI

### Opcode 0x2D (45) `elemDmgMod`

Writes a monster's own elemental resistance at runtime. Parameters: `elem_index` (1 byte),
then a 16-bit little-endian value.

Effective address: `BATTLE_SLOT_DATA + 0x44 + 208*slot + 2*elem_index`, encoded as
`lea edx, [eax+edx*8]` with `edx = 13*slot`, then `[BATTLE_SLOT_DATA.elem_def + edx*2]`.

**There is no bounds check on `elem_index`.** It is a raw bytecode byte (0–255), so the
opcode can write a word anywhere from `+0x44` to `+0x242` relative to the slot base —
across `timer`, coordinates, `flag_data`, `status_1`, `mental_res`, and into following
slots. Index 8 currently lands in `timer[0]`.

The value is stored raw; readers apply `800 - v` or `900 - v`, which is consistent with
IfritAI encoding an authored percentage as `900 - percent`.

### Element-resistance targeting

`checkIfSlotIDHasStatus` implements "highest/lowest *X* resistance" predicates through
`StatusAI` values **221–236**:

| Range | Meaning | Index math |
|-------|---------|------------|
| 221–228 | highest Fire…Holy resistance | `p_status - 221` |
| 229–236 | lowest Fire…Holy resistance  | `p_status - 229` |

The lookup base constant `30571348` is `0x1D27B54` = `BATTLE_SLOT_DATA + 0x44`, with a
stride of 104 words (208 bytes). No upper bound check. Note the two ranges are **adjacent**,
so neither can be extended without colliding with the other.

## User interface

### Junction / status menu

Two pages draw elements, both table-driven and both hard-coded to 8 rows:

- `Menu_DrawElemAttackPage` — elemental attack, loop bound `cmp eax, 8` at `0x4E13E3`
- `Menu_DrawElemDefensePage` — elemental defense, loop bound `mov [esp+34h+var_1C], 8` at `0x4E1496`

They share one **8-record table at `0xB88758`**, 8 bytes per record:

| Offset | Size | Meaning |
|--------|------|---------|
| `+0` | 1 | grid X cell |
| `+1` | 1 | grid Y cell |
| `+2` | 2 | byte offset of `elemDefInfo[i]` inside `FF8FieldCharData` (`0x0194 + 2i`) |
| `+4` | 2 | `icon.sp1` sprite id (`0x0120 + i`) |
| `+6` | 2 | padding (always 0) |

The attack page's pointer starts at the `+4` field (`0xB8875C`), the defense page's at the
`+2` field (`0xB8875A`). Unrelated data begins at `0xB88798`, so the table cannot be
extended in place. `STATUS_MENU_TABLE` at `0xB886F0` is the same shape with 13 records for
the mental statuses.

Both pages compare the new value against a pre-junction snapshot and draw sprite 109 or 110
(down/up arrow) when they differ.

### Preview panel geometry

All four junction preview drawers share one geometry, driven by
`JUNCTION_PREVIEW_DRAWER_TABLE` (10 bytes at `0x4E0F90`: `00 01 02 02 02 02 03 03 03 03`),
indexed by `JUNCTION_CURSOR_TO_TARGET_ID[cursor] - 9`:

| Value | Drawer | Rows |
|-------|--------|------|
| 0 | `Menu_DrawElemAttackPage` | 8 |
| 1 | inline status-attack block | 13 |
| 2 | `Menu_DrawElemDefensePage` | 8 |
| 3 | `Menu_DrawStatusDefensePage` | 13 |

Junction target ids: 9 = Elem-Atk, 10 = Status-Atk, **11–14 = the four Elem-Def slots** (all
four show the same elemental page), 15–18 = the four Status-Def slots.

- Column pitch **105 px** (`21*gridX + 84*gridX`)
- Row pitch **13 px** (`13*gridY`)
- `MENU_WINDOW_POS` (`0x1D76A80`) = x in the low word, y in the high word
- `MENU_WINDOW_SIZE` (`0x1D76A84`) = width low, height high

The two globals are contiguous and are read as a `short[4]` rect by
`Menu_ComputeWindowOpenScaleRect`, which is what establishes the field order. All four
panels are **218 px wide**. Heights: element pages 67 (4 rows), status attack 89, status
defense 96.

Panels are **bottom-aligned at y ≈ 215**: the element pages start at `a4+147` with height 67
(147 + 67 = 214); `Menu_DrawStatusDefensePage` starts at `a4+120` with height 96
(120 + 96 = 216).

Two consequences for any layout change:

- **A third column does not fit.** Two columns already span x ≈ 146–318 on a 320 px screen.
- **More rows do fit.** Eight rows need height `67 + 4*13 = 119`, so the y-origin immediate
  moves `147 → 96` (96 + 119 = 215, preserving the bottom alignment). The status pages
  already render a taller block in this same panel, so this is within proven bounds.

### There is no element picker

Worth stating plainly, because it removes a whole category of expected work:
**FF8 has no UI where the player selects an element.** `Elem-Atk-J` and `Elem-Def-J`
junction a *magic*, and the element is whatever that magic's kernel `jElemAttack` /
`jElemDefense` byte says.

`StatusJunctionMenuHandler` (0x4DA9B0) — the 21KB state machine behind the whole junction
screen — has no element loop of its own. It reaches element data in one place:
`Junction_GetMagicValueForTarget` (0x4C2E50), called at four sites to decide which held
spells are offered for the current junction slot (nonzero = offered). That getter returns,
per junction target:

| Target | Returns |
|--------|---------|
| 0–8 | HP..LCK junction value, read as a **signed** byte |
| 9 | `jElemAttack` |
| 10 | `jStatusesAttack` (16-bit) |
| 11–14 | `jElemDefense`, **as a byte** — the four Elem-Def slots |
| 15–18 | `jStatusesDefend` (16-bit) — the four Status-Def slots |

`Menu_UnjunctionGFAndCompactDefSlots` (0x4E02C0, from 0x4DC843 and 0x4DF49A) operates on
the **4 Elem-Def-J slots**, not on the elements, and all element drawing is delegated through
`Menu_DrawStatusJunctionWindow` (0x4E04F0) to the two pages above.

The preview's "before" column comes from `JUNCTION_PREVIEW_CHAR_SNAPSHOT` (0x1D8B3B0), a
464-byte copy of `F_CHAR_DATA[0]` that the handler takes and restores with the generic copy
helper `Menu_CopyBytes` (0x49A7B0) at about twenty sites.

The same holds for `Menu_DrawJunctionElemSummaryRows` (0x4E1E40, the Elem-Atk / Elem-Def
summary rows with icons 298/299) and `Junction_AutoPickForStatMultiSlot` (0x4DFDE0) — both
are driven by the 4-slot count, not the element count.

One exception: **auto-junction scoring truncates**. `Junction_AutoPickBestSpellForStat`
scores a candidate spell as `PopCount32(mask) * junction_value`, and the element cases pass
the mask through a byte cast:

| Stat | Expression |
|------|------------|
| 9 — Elem-Atk-J  | `PopCount32((unsigned __int8)K_MAGIC[s].jElemAttack)  * jElemAttackValue` |
| 11 — Elem-Def-J | `PopCount32((unsigned __int8)K_MAGIC[s].jElemDefense) * jElemDefenseValue` |

`PopCount32` itself is 32-bit clean, so the ceiling is purely those two casts. Left
unpatched, the Auto command would silently ignore elements 8–15 when choosing spells.

### Scan screen

`manageScanText` builds the affinity lines. For each of five categories it calls
`ScanText_CollectElementsByAffinity`, which buckets `elem_def[i]` for `i` in 0..7:

| Category | Condition | Label (misc text) |
|----------|-----------|-------------------|
| 0 | `v <= 600` | 37 — very weak against |
| 1 | `600 < v < 800` | 38 — weak against |
| 2 | `800 < v < 900` | 39 — strong against |
| 3 | `v == 900` | 40 — has no effect |
| 4 | `v > 900` | 41 — absorbs |

Matching indices are appended to `SCAN_ELEMENT_INDEX_LIST` and each is rendered as misc text
`index + 101`.

`manageScanText_Dup` (`0xB68390`, previously `getSomeText0`) and
`ScanText_CollectElementsByAffinity_Dup` (`0xB686D0`) are an identical second copy with their
own arrays, used by the other Scan effect variant.

Two limits bound what a scan can show, neither checked by the code:

- **Line length.** Lines are built in `BUFFER_CONCATENATE_TEXT` (48 bytes) and copied by
  `addToQueueMessageToPrint` into a 48-byte `PrintMessage`. A verdict line is the label plus
  eight name slots, each preceded by a separator; with the longest English label (17 bytes)
  that is 42 bytes.
- **Line count.** `SCAN_TEXT_LINES` holds exactly 8 pointers, with `SCAN_TEXT_LINE_COUNT`
  directly behind it. Retail's maximum is exactly 8: level/HP, monster type, five verdicts,
  and the monster's own scan text. `ScanText_GetLine` (0xB68370) is the reader.

### Element names are icon tokens, not words

Kernel **misc-text entries 101–108** are each exactly two bytes — `05 5D` through `05 64` —
i.e. FF8 text special codes **0x055D–0x0564**, one per element, rendered as icon glyphs.
Verified by decoding `main/kernel.bin` directly. No `push 65h` (=101) immediate exists
anywhere else in the executable, so the two scan builders are their only consumers.

`Text_RenderGlyphs` settles what such a code draws. For `0x05 NN` with `NN >= 0x40` it draws
`icon.sp1` sprite `TEXT_ICON_CODE_TO_SPRITE[NN]` (0xB86D84); `NN` 0x20–0x2F are controller
buttons through the key config, and 0x30–0x3F draw sprite `NN + 80`. The table:

| Codes | Sprites |
|-------|---------|
| `0x0553`–`0x0559` | status icons `0x110`–`0x116` (`0x5A`–`0x5C` repeat `0x110`) |
| `0x055D`–`0x0564` | **element icons `0x120`–`0x127`** |
| `0x0565`–`0x0571` | status icons `0x110`–`0x11C` |
| `0x0572`–`0x0575` | `0x128`–`0x12B` |
| `0x0576`–`0x057E` | `0x130`–`0x138` |

Valid entries stop at `0x7E` and unrelated strings follow, so the table cannot grow in place.
Its four readers — `Text_IconCodeToSpriteId` (0x49F930), `calculateTextDimension`,
`sub_4A1200` and `Text_RenderGlyphs` — only check `NN >= 0x40` and index with a
zero-extended byte; there is no upper bound.

### Icon sprite ids

`Menu_DrawSp1SpriteById` (0x4B7210) gates sprite ids with `if (id >= *AICON_SP1_DATA) return;`
— the ceiling is the sprite count stored in `icon.sp1`'s **own header** (329 in retail EN,
checked in the file), not a constant in the executable. Adding sprites to `icon.sp1` raises
the cap with no exe patch. Ids 128–139 are diverted to the sysfnt path. Element icons occupy
288–295 (`0x0120`–`0x0127`), mental-status icons 272–284.

The ids right after the element icons are **not** free: `0x128`–`0x12B` and `0x130`–`0x138`
are drawn by text icon codes `0x72`–`0x7E` (above). New sprites have to go after the last
retail one, from 329.

## Inventory of element-carrying storage

Every place an element bitfield is stored, and whether it has room to become 16 bits:

| # | Location | Size | Adjacent free space? |
|---|----------|------|----------------------|
| 1 | `HIT_ELEMENT` @ 0x1D2A244 | 4-byte global, low byte used | **Yes** — spare width, but ~17 byte-store access sites |
| 2 | `FF8BattleSlotData.hit_element` +0xC5 | 1 | No — `charaStat[8]` below, `hit_element_percent` above |
| 3 | `FF8BattleSlotData.last_attacker_attack_element` +0x8C | 1 | No — `last_attacker_command_type` below, `last_attacker_com_id` above |
| 4 | `FF8FieldCharData.hitElement` +0x1C4 | 1 | No — `comId` below, `hitElementPercent` above |
| 5 | Kernel §2 magic element `0x0E` | 1 | **Yes** — `0x0F` is unused padding |
| 6 | Kernel §2 `jElemAttack` `0x20` / `jElemDefense` `0x22` | 1 each | No (value bytes follow); `0x3A`–`0x3B` free at record end |
| 7 | Kernel §4 enemy attack element `0x0A` | 1 | No — 20-byte record fully packed |
| 8 | Kernel §8 item element `0x17` | 1 | Padding at `0x0C`, not adjacent |

Only one of the eight has adjacent free space, so **the element type cannot be widened in
place**. It does not have to be: every attack-side value in retail is a single bit and only
the lowest bit is ever used, so a byte holding an *index* (0 = none, 1–16) says everything
the bitfield ever did, in the same byte. Only the junction defence mask needs more bits, and
the magic record has free bytes for it.

## Notes for extending past eight elements

These are observations about the shipped code, recorded for anyone evaluating the idea —
not a recommended design.

1. **The 8-element cap is load-bearing for stack safety.** In both damage functions the
   `GetFlaggedBitIndexList` output buffer is exactly 8 bytes and sits directly beneath the
   saved return address (`[esp+18h]` vs `[esp+20h]` in `Damage_ApplyPhysicalModifiers`;
   `[esp+14h]` vs `[esp+1Ch]` in `Damage_ComputeMagicAndGF`). The helper writes one byte per
   set bit, so a ninth set element bit overwrites the return address. Simply widening the
   element bitfield without enlarging these buffers is a stack smash.
2. **`FF8BattleSlotData` cannot grow.** `elem_def` is boxed in by `timer` at `+0x54`, and the
   208-byte stride is a hardcoded immediate throughout the executable
   (`index_slot_data = 208 * target_slot_id`).
3. **`FF8FieldCharData` cannot grow.** `elemDefInfo` is followed by `mentalRes` at `+0x1A4`.
4. **`getMagicElemDefValue` truncates.** It builds `1 << elem_id` in a DWORD but compares
   `(unsigned __int8)mask & K_MAGIC[].jElemDefense`, so any index ≥ 8 yields neutral 800.
5. **`StatusAI` 221–228 and 229–236 are adjacent**, so the AI's highest/lowest resistance
   ranges cannot both be extended in place.
6. **The scan screen's local pointer array is `char *v58[9]`** — one label plus exactly eight
   element names, with an unrolled 7-iteration concatenation. A ninth name overflows it.
7. **The misc-text pointer table is a fixed 128 entries** with only four spares (122–125,
   the `DUMMY` entries).
8. **The junction menu table at `0xB88758` cannot grow in place**, and its 2×4 grid layout has
   no room for more rows without a redesign.
9. **`last_attacker_attack_element` (+0x8C) is boxed in** with no adjacent free byte, and the
   AI's "last attack element" condition (opcode `0x0A` sub-type `0x05`) reads it as a byte at
   `0x4888FA`.
10. **Auto-junction scoring truncates** at the two `(unsigned __int8)` casts in
    `Junction_AutoPickBestSpellForStat` (see above).

11. **`Junction_GetMagicValueForTarget` truncates** `jElemDefense` to a byte, so a spell
    whose defence covered only new elements would be hidden from the Elem-Def spell list.
12. **The scan screen's text icon table ends at code `0x7E`**, and its line and message
    buffers (48 bytes each, 8 lines) are unchecked — see *Scan screen*.

A note on what is *not* in the way: the false-positive `elemDefInfo` xref in
`BattleMenu_DrawWindow_Update` at `0x4ADEAA` — that instruction reads `status_1` (+0x1B2),
not elemental defense.

Two things that are **not** blockers:

- **The save format.** It stores junctioned *magic IDs* (`0x65` elem attack, `0x67` four
  elem-defense slots), never element bitfields.
- **The monster `.dat` info section length.** `battle_monster_dat_loader` is entirely
  offset-table driven: every section destination is computed as
  `next_offset - this_offset` from the header table (`many[4]`…`many[44]`), and the info
  section's length is only ever derived as `many[32] - many[28]`. Growing it past 380 bytes
  works provided the later header offsets are bumped and the file still fits the
  `BS_FILE_MEMORY_ADDR` arena. Appending after `StatusRes[20]` keeps every existing field
  offset intact.

`HIT_ELEMENT` (`0x1D2A244`) is worth noting: it is declared as a 4-byte global but only its
low byte is ever read, and the next symbol starts at `+4`.

## Function address reference

| Name | Address | Role |
|------|---------|------|
| `GetFlaggedBitIndexList` | 0x48EF50 | Bitmask → list of set-bit indices (elements *and* target masks) |
| `Damage_ApplyPhysicalModifiers` | 0x48F600 | Physical path; applies `elem_def` and the Aura drain |
| `Damage_ComputeMagicAndGF` | 0x491AD0 | Magic/GF path; applies `elem_def` |
| `setMonsterInfoFromDatInfoSection` | 0x48BBD0 | Fills `elem_def` from `.dat` `ElemRes[8]` |
| `setBattleSlotData` | 0x48B310 | Fills `elem_def` from `elemDefInfo[8]` |
| `Stat_RefreshCharaBattleStats` | 0x495960 | Recomputes `elemDefInfo` / `hitElement` from junctions |
| `get_elem_attack` | 0x496930 | Junctioned elemental attack bitfield |
| `get_elem_attack_value` | 0x496960 | Junctioned elemental attack percentage |
| `getMagicElemDefValue` | 0x4969E0 | Per-element junction defense (base 800, cap 1000) |
| `checkIfSlotIDHasStatus` | 0x486E70 | AI predicates incl. highest/lowest elemental resistance |
| `MonsterAI` | 0x487DF0 | AI interpreter; opcode 0x2D at 0x488744 |
| `Menu_DrawElemAttackPage` | 0x4E1210 | Junction/status menu, elemental attack page |
| `Menu_DrawElemDefensePage` | 0x4E1460 | Junction/status menu, elemental defense page |
| `manageScanText` | 0xB67EF0 | Scan screen text builder |
| `ScanText_CollectElementsByAffinity` | 0xB68230 | Buckets `elem_def` into the five affinity categories |
| `Menu_DrawSp1SpriteById` | 0x4B7210 | `icon.sp1` sprite renderer (data-driven id cap) |
| `battle_monster_dat_loader` | 0x507120 | Offset-table-driven `.dat` section placement |
| `Menu_DrawStatusDefensePage` | 0x4E0FF0 | Status-defense preview page (13 rows) |
| `Menu_DrawWindowFrame` | 0x4B2740 | Common tail call of every preview page; draws frame + header icon |
| `Menu_ComputeWindowOpenScaleRect` | 0x4A35A0 | Window open/close scale animation over the POS/SIZE rect |
| `Menu_ElemDefToPercent` | 0x4BFAC0 | Raw `elem_def` → displayed percent (800→0, 900→100, >900 absorb) |
| `Menu_ElemDefIsAbsorb` | 0x4BFAF0 | `v > 900`; gates the absorb icon (175) on the defense page |
| `Menu_StatusResToPercent` | 0x4BFAB0 | Status resistance → displayed percent (`v - 100`) |
| `Menu_GetMenuContextId` | 0x4BD060 | Selects between the two window header-icon sets |
| `StatusJunctionMenuHandler` | 0x4DA9B0 | Junction screen state machine; no element loop of its own |
| `Menu_DrawStatusJunctionWindow` | 0x4E04F0 | Status/junction window drawer; dispatches the element pages |
| `Menu_UnjunctionGFAndCompactDefSlots` | 0x4E02C0 | GF removal; compacts the 4 Elem-Def-J slots |
| `Menu_DrawJunctionElemSummaryRows` | 0x4E1E40 | Elem-Atk / Elem-Def summary rows (icons 298/299) |
| `Junction_AutoPickBestSpellForStat` | 0x4DFE90 | Auto-junction scoring; truncates the element mask to 8 bits |
| `Junction_AutoPickForStatMultiSlot` | 0x4DFDE0 | Repeats the above once per available defense slot |
| `PopCount32` | 0x4ABC20 | 32-bit set-bit count used by auto-junction scoring |
| `Battle_applyDamage` | 0x48FE20 | Loads `HIT_ELEMENT` / `HIT_ELEMENT_PERCENT` (byte stores) |
| `applyDamageAndHandleDeath` | 0x494410 | Stamps `last_attacker_attack_element` |
| `Junction_GetMagicValueForTarget` | 0x4C2E50 | What a magic gives a junction target; truncates `jElemDefense` to a byte |
| `Menu_CopyBytes` | 0x49A7B0 | Generic forward copy; takes and restores the preview snapshot |
| `Text_IconCodeToSpriteId` | 0x49F930 | Text icon code → `icon.sp1` sprite id |
| `manageScanText_Dup` | 0xB68390 | Second scan text builder (other Scan effect variant) |
| `ScanText_GetLine` | 0xB68370 | Reads a built scan line |
