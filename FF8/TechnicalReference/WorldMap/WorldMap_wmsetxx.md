---
layout: default
parent: WorldMap
title: WorldMap wmsetxx File Format
permalink: /technical-reference/worldmap/worldmap-wmsetxx-file-format/
---

## Info

`wmsetxx.obj` (where `xx` is `gr`, `us`, `it`, `fr`, or `sp`) is the world-map data bundle. A single file packs everything the world map needs: scripts, dialog text, location names, models, textures, palette/texture animations, AKAO audio, and various lookup tables. Localised builds differ only in their text sections; binary layouts and offsets above the first text section are identical.

`wmset.obj` (no language suffix) appears to be a leftover; it is not loaded in-game. `lang-en/wmset.obj` carries English text but its layout differs from `wmsetus.obj`.

This document reflects the format as parsed by our addon (`src/sections/section_*.py`) against `wmsetus.obj`. Where this disagrees with prior notes, our parser is the source of truth.

### Conventions

- **Endianness:** all multi-byte integers are little-endian.
- **Indexing:** sections are 0-indexed throughout this document, matching our source code (Section N is parsed by `section_N.py`). Older notes you may find online are 1-indexed — subtract 1 to translate.
- **Relative offsets:** "relative offset" always means "from the start of the section's bytes".
- **Offset lists:** many sections begin with a list of `uint32` offsets terminated by a sentinel `0x00000000`.

## General structure

`wmsetxx.obj` contains 48 sections, numbered 0 through 47. The file begins with a fixed-size header of 48 × 4-byte absolute offsets (192 bytes total), one offset per section, in order.

| Offset    | Length  | Description                              |
|-----------|---------|------------------------------------------|
| 0         | 4 bytes | Absolute offset to Section 0's data      |
| N × 4     | 4 bytes | Absolute offset to Section N's data      |
| 188       | 4 bytes | Absolute offset to Section 47's data     |

Each section's data runs from its offset up to the next section's offset (or end of file for Section 47).

---

## Section 0: Encounter ID supplier

Maps `(region_id, ground_id)` pairs to an `esi` multiplier used to look up encounters in Section 3.

| Offset             | Length  | Description                              |
|--------------------|---------|------------------------------------------|
| 0                  | 4 bytes | `entries_size` (total bytes of entries; entry count = `entries_size / 4`) |
| 4 + entryID × 4    | 4 bytes | `EncounterIdSupplierEntry`               |

**EncounterIdSupplierEntry** (4 bytes):

| Offset | Length  | Type   | Field      |
|--------|---------|--------|------------|
| 0      | 1 byte  | uint8  | `region_id` |
| 1      | 1 byte  | uint8  | `ground_id` |
| 2      | 2 bytes | uint16 | `esi`       |

`esi` is the row index Section 3 uses to find the matching encounter group. Stepping on a tile whose `(region, ground)` matches an entry selects that entry's `esi`.

---

## Section 1: World map regions grid

A 32 × 24 byte grid (768 bytes, no header). Each byte is the region ID at that grid cell. The grid is row-major: `region_id = grid[grid_y * 32 + grid_x]`. Dumping the section as a raw 32 × 24 grayscale image produces a recognisable minimap of regions.

---

## Section 2: World map encounter flags

One `uint8` per encounter group in Section 3. Common observed values:

| Value | Meaning (observed)                          |
|-------|---------------------------------------------|
| 0     | Roads, railways                             |
| 2     | Default                                     |
| 3     | Galbadia desert (day and night)             |
| 12    | Forests                                     |
| 128   | Island Closest to Heaven / Hell             |

The count of groups in Section 3 equals the byte count of Section 2.

---

## Section 3: World map encounters

Each encounter group is 16 bytes: eight `uint16` encounter (scene) IDs. The conventional split per group is:

- 4 common encounters (`uint16[4]`)
- 2 medium encounters (`uint16[2]`)
- 2 rare encounters (`uint16[2]`)

Group N occupies bytes `N × 16 .. N × 16 + 15`. The runtime looks up a group via `esi` from Section 0 and picks one encounter ID from the appropriate rarity slot.

---

## Section 4: Lunar Cry encounter flags

Same shape as Section 2 but for post-Lunar-Cry encounters. Always `0x08` in the original release.

---

## Section 5: Lunar Cry encounters

Same shape as Section 3 (16-byte groups of 8 × `uint16`), but for Lunar Cry encounters. To find the post-Lunar-Cry group at a given location, look up Section 0 with `region == 10` (Esthar) and subtract `80` from the resulting `esi` — that is the index into Section 5.

---

## Section 6: Polygon texture lookup

Maps a polygon's CLUT slot to a real `(tex_page, clut_id)` pair. Used while drawing land polygons from `wmx.obj`.

| Offset         | Length  | Description                              |
|----------------|---------|------------------------------------------|
| 0              | 4 bytes | `entries_size` (total bytes of entries; entry count = `(entries_size − 4) / 4`) |
| 4 + entryID × 4 | 4 bytes | `TextureLookup`                         |

**TextureLookup** (4 bytes):

| Offset | Length  | Type   | Field   |
|--------|---------|--------|---------|
| 0      | 2 bytes | uint16 | `tpage` |
| 2      | 2 bytes | uint16 | `clut`  |

(Earlier notes labeled this section as roads/train track/bridge. That is the texture archive in Section 38 — this section is the polygon texture lookup.)

---

## Section 7: Player-location scripts

Generic script section (see "Script format" below). One script per offset entry. These scripts run when the player crosses into a new region or tile and decide things like text triggers and event activations.

---

## Section 8: Field landing positions

Where Squall (and his vehicle, if any) spawns when transitioning from a field map back to the world map.

| Offset           | Length   | Description                          |
|------------------|----------|--------------------------------------|
| 0                | 4 bytes  | `entries_size` (entry count = `(entries_size − 4) / 12`) |
| 4 + N × 12       | 12 bytes | `FieldLandingPosition`               |

**FieldLandingPosition** (12 bytes):

| Offset | Length  | Type  | Field         |
|--------|---------|-------|---------------|
| 0      | 4 bytes | int32 | `x`           |
| 4      | 4 bytes | int32 | `y`           |
| 8      | 2 bytes | int16 | `z`           |
| 10     | 1 byte  | uint8 | `player_yaw`  |
| 11     | 1 byte  | uint8 | `vehicle_yaw` |

`player_yaw` and `vehicle_yaw` are 0–255 (full turn = 256).

---

## Section 9: Entity-spawn scripts

Generic script section. Each script controls the spawn / despawn of one or more entities (party characters, NPCs, vehicles, landmarks). The script's `ADD_ENTITY` (`0xFF13`) and `ADD_ENTITY_ALT` (`0xFF14`) opcodes register entities into the active list for the current world-map state.

---

## Section 10: Entity-spawn positions

Starting positions and orientation for the entities that the Section 9 scripts spawn. No header — records pack back-to-back at 16 bytes each.

**EntityPosition** (16 bytes):

| Offset | Length  | Type  | Field   |
|--------|---------|-------|---------|
| 0      | 4 bytes | int32 | `x`     |
| 4      | 4 bytes | int32 | `y`     |
| 8      | 4 bytes | int32 | `z`     |
| 12     | 2 bytes | int16 | `yaw`   |
| 14     | 2 bytes | int16 | `pitch` |

Entry count = `section_size / 16`.

---

## Section 11: Vehicle warp scripts

Generic script section. Triggered when the player boards or rides a vehicle (Ragnarok, Balamb Garden, Shumi train). Scripts here use `SET_RETURN_VALUE` (`0xFF15`) to communicate the destination back to the caller — the value `3` triggers a special return path (`sub_5484B0`).

---

## Section 12: Train exit positions

Where the player exits the Shumi train onto the world map.

| Offset           | Length   | Description                          |
|------------------|----------|--------------------------------------|
| 0                | 4 bytes  | `entries_size` (entry count = `(entries_size − 4) / 12`) |
| 4 + N × 12       | 12 bytes | `TrainExitPosition`                  |

**TrainExitPosition** (12 bytes):

| Offset | Length  | Type  | Field       |
|--------|---------|-------|-------------|
| 0      | 4 bytes | int32 | `x`         |
| 4      | 4 bytes | int32 | `y`         |
| 8      | 2 bytes | int16 | `z`         |
| 10     | 1 byte  | uint8 | `unknown_a` |
| 11     | 1 byte  | uint8 | `unknown_b` |

---

## Section 13: Dialog texts (side quests)

World-map dialog strings used by side-quest scripts.

| Offset           | Length  | Description                                    |
|------------------|---------|------------------------------------------------|
| 0 + N × 4        | 4 bytes | Relative offset to a string (terminator: `0x00000000`) |
| (after sentinel) | varies  | Concatenated FF8-encoded string data           |

Each string spans from its offset up to the next string's offset (or end of section). Decoding uses the FF8 character table (see `utils/char_table.py`): single-byte glyph codes plus multi-byte control codes (`0x00` end, `0x01` new page, `0x02` newline, `0x03 N` character name, `0x04 N` variable, `0x06 N` colour, `0x09 N` wait, `0x0E N` location name, `0x19–0x1C` Japanese tables).

Strings here are referenced by ID from the script opcodes `SHOW_TEXT_BOX` (`0xFF1F`) and `SHOW_CHOICE_BOX` (`0xFF23`).

---

## Section 14: Unused

Present in the file but unused by the runtime. Our parser keeps the raw bytes for round-tripping.

---

## Section 15: World-map object models

3D polygon data for world-map objects (Balamb Garden, Galbadia Garden, Ragnarok, Lunatic Pandora, cactuar statue, halo ring, etc.). Researched by Vehek ([qhimm.com forum](http://forums.qhimm.com/index.php?topic=13799.msg193791#msg193791)).

| Offset           | Length  | Description                                      |
|------------------|---------|--------------------------------------------------|
| 0 + N × 4        | 4 bytes | Per-model entry: `uint16 offset`, `uint16 padding` |
| (after sentinel) | varies  | Model data, packed back-to-back                  |

Each entry pairs a `uint16` relative offset with a `uint16` padding word. Padding is normally `0`; a padding value of `0x000F` flags a legacy/non-parseable model and is skipped by our parser. The list ends when `offset == 0`.

**Model header** (8 bytes):

| Offset | Length  | Type   | Field            |
|--------|---------|--------|------------------|
| 0      | 2 bytes | uint16 | `triangle_count` |
| 2      | 2 bytes | uint16 | `quad_count`     |
| 4      | 2 bytes | uint16 | `texture_page`   |
| 6      | 2 bytes | uint16 | `vertex_count`   |

Followed by `triangle_count` triangles (12 bytes each), then `quad_count` quads (16 bytes each), then `vertex_count` vertices (8 bytes each).

**Triangle** (12 bytes):

| Offset | Length  | Type    | Field                       |
|--------|---------|---------|-----------------------------|
| 0      | 3 bytes | uint8×3 | `vertex_indices[0..2]`      |
| 3      | 1 byte  | uint8   | `semitransp` (bit `0x01` = semi-transparent) |
| 4      | 2 bytes | uint8×2 | `uv0` (u, v for vertex 0)   |
| 6      | 2 bytes | uint8×2 | `uv1` (u, v for vertex 1)   |
| 8      | 2 bytes | uint8×2 | `uv2` (u, v for vertex 2)   |
| 10     | 2 bytes | uint16  | `clut_id`                   |

**Quad** (16 bytes):

| Offset | Length  | Type    | Field                       |
|--------|---------|---------|-----------------------------|
| 0      | 4 bytes | uint8×4 | `vertex_indices[0..3]`      |
| 4      | 2 bytes | uint8×2 | `uv0`                       |
| 6      | 2 bytes | uint8×2 | `uv1`                       |
| 8      | 2 bytes | uint8×2 | `uv2`                       |
| 10     | 2 bytes | uint8×2 | `uv3`                       |
| 12     | 2 bytes | uint16  | `clut_id`                   |
| 14     | 1 byte  | uint8   | `semitransp` (bit `0x01`)   |
| 15     | 1 byte  | uint8   | unknown                     |

**Vertex** (8 bytes):

| Offset | Length  | Type   | Field      |
|--------|---------|--------|------------|
| 0      | 2 bytes | int16  | `x`        |
| 2      | 2 bytes | int16  | `y`        |
| 4      | 2 bytes | int16  | `z`        |
| 6      | 2 bytes | uint16 | unknown (likely padding) |

Texturing uses the model's `texture_page` together with the per-polygon `clut_id`. Quad winding on PSX is `0, 1, 3, 2` (the third and fourth indices swap relative to standard OBJ winding).

---

## Section 16: Animated texture descriptors (image-frame animations)

Drives per-frame indexed-pixel swaps for VRAM-resident world textures (the moving parts of the sea/water, primarily). Each descriptor describes one animated rectangle in VRAM and lists the offsets of its frame payloads. Payloads live inside the same section, after the descriptor block.

| Offset           | Length  | Description                              |
|------------------|---------|------------------------------------------|
| 0 + N × 4        | 4 bytes | Relative offset to descriptor (sentinel: `0x00000000`) |
| (after sentinel) | varies  | Descriptor records, then frame payloads  |

**Descriptor** (8 bytes + 4 × frame count):

| Offset | Length  | Type   | Field              |
|--------|---------|--------|--------------------|
| 0      | 1 byte  | uint8  | `phase_offset`     |
| 1      | 1 byte  | uint8  | `period`           |
| 2      | 1 byte  | uint8  | `half_frame_count` |
| 3      | 1 byte  | uint8  | `flags`            |
| 4      | 2 bytes | uint16 | `tex_page`         |
| 6      | 2 bytes | uint16 | `v_coord`          |
| 8      | 4 × F   | uint32 | `frame_offsets[F]` |

`F = half_frame_count` (or `1` when `half_frame_count == 0`). `(tex_page, v_coord)` is a VRAM destination: `tex_page` is in 16-bit word columns (same unit as TIM `img_x`); `v_coord` is in pixel rows.

**Frame payload** (at `descriptor_offset + 8 + frame_offset`): a small VRAM-transfer block. Layout (observed):

| Offset | Length  | Type   | Field                                |
|--------|---------|--------|--------------------------------------|
| 0      | 4 bytes | uint32 | marker `0x12` (decimal 18)           |
| 4      | 4 bytes | uint32 | marker `0x01`                        |
| 8      | 4 bytes | uint32 | `size` (includes 12-byte rect header) |
| 12     | 2 bytes | uint16 | `dest_x`                             |
| 14     | 2 bytes | uint16 | `dest_y`                             |
| 16     | 2 bytes | uint16 | `width_words`                        |
| 18     | 2 bytes | uint16 | `height`                             |
| 20     | size−12 | bytes  | 8-bit palette indices (paste at dest) |

In `wmsetus.obj` this section animates the sea: world TIM 21 (full 64×64) and world TIM 22 (two independent 64×32 halves). Each has four frames played ping-pong (`0, 1, 2, 3, 2, 1` — six display slots per cycle).

---

## Section 17: Encounter formation table

A 16-entry header pointing into 16 formation groups. Each group is itself an offset list of formation entries.

| Offset    | Length     | Description                              |
|-----------|------------|------------------------------------------|
| 0         | 16 × 4     | 16 × `uint32` group offsets              |
| (group N) | varies     | `uint32` formation offsets, sentinel `0x00000000` |

Used to organise encounter formations by type/tier.

At runtime, `WM_Encounter_RollAndSelectScene` (`0x541C80`) selects from the wmset encounter tables by region/terrain. There are 8 formations per terrain; if the selected formation matches `WM_LAST_FORMATION_ID` (`0x20400A0`), the game can re-roll up to two times before handing the scene id to the battle module. See [World Map Encounters](worldmap_encounters) and [Encounter Trigger Runtime](../../battle/encounter-trigger-runtime/).

---

## Section 18: Region location IDs

Raw `uint8` array of length = section size. Each byte assigns a location ID to a region cell (parallel to the region grid in Section 1).

---

## Section 19: AKAO frame headers

Six AKAO sub-streams packed back-to-back, with a small index header.

| Offset | Length  | Type   | Field              |
|--------|---------|--------|--------------------|
| 0      | 4 bytes | uint32 | `akao_count`       |
| 4      | 4 bytes | uint32 | `akao_header_size` |
| 8      | 6 × 4   | uint32 | `offsets[0..5]` (relative to section start) |
| 32+    | varies  | bytes  | Concatenated AKAO blocks                    |

Each block must start with the magic `"AKAO"` (`0x4F414B41`). Block `i` spans `offsets[i] .. offsets[i+1]`; the final block runs from `offsets[5]` to end of section.

---

## Section 20: AKAO

A single AKAO audio stream. The section starts with the magic `"AKAO"` and contains the full block to the end of the section.

---

## Sections 21 – 27: Unused (null padding)

Each is a 4-byte null section, present for header alignment. Our parser reads and discards them.

---

## Section 28: World-map "water block"

A duplicate of one water-mesh segment from `wmx.obj`. Used as a fallback when the engine cannot load the real `wmx.obj` segments fast enough to fill the frame — for example during a Ragnarok landing transition where the camera rotates and reveals areas before their segments have streamed in. Visible as a uniform sea fill in those moments.

The section is opaque to our parser; we keep the raw bytes.

---

## Section 29: Animation frame data

Opaque animation/keyframe data. Our parser preserves raw bytes; the structure is not yet known.

---

## Section 30: Animation descriptors (location records)

Records describing per-location animation hooks (12 bytes each), addressed via an initial total-size word.

| Offset           | Length   | Description                              |
|------------------|----------|------------------------------------------|
| 0                | 4 bytes  | `end_offset` (record count = `(end_offset − 4) / 12`) |
| 4 + N × 12       | 12 bytes | `LocationRecord`                         |

**LocationRecord** (12 bytes):

| Offset | Length  | Type  | Field         |
|--------|---------|-------|---------------|
| 0      | 1 byte  | uint8 | `x`           |
| 1      | 1 byte  | uint8 | `y`           |
| 2      | 1 byte  | uint8 | `location_id` |
| 3      | 1 byte  | uint8 | unknown       |
| 4      | 4 bytes | int32 | `value1`      |
| 8      | 4 bytes | int32 | `value2`      |

---

## Section 31: Location names

Text strings for world-map location names (Garden buildings, towns, special places like "Sorceress Memorial" and "Tears' Point"). Same layout as Section 13: offset list ending in `0x00000000`, followed by FF8-encoded string data. Referenced from scripts and from the Ragnarok landing UI.

---

## Section 32: Sky / fog colour zones

Per-zone lighting and atmospheric parameters. Each zone has a position, fade range, two light colours, three fog colours, and nine 16-bit atmosphere parameters.

| Offset           | Length  | Description                          |
|------------------|---------|--------------------------------------|
| 0 + N × 4        | 4 bytes | Relative offset to zone (sentinel: `0x00000000`) |
| (after sentinel) | 84 each | `SkyColorZone` records               |

**SkyColorZone** (84 bytes):

| Offset | Length   | Type    | Field              |
|--------|----------|---------|--------------------|
| 0      | 4 bytes  | int32   | `x`                |
| 4      | 4 bytes  | int32   | `y`                |
| 8      | 4 bytes  | int32   | `transition_range` |
| 12     | 4 bytes  | RGB+pad | `light_color_1`    |
| 16     | 4 bytes  | RGB+pad | `light_color_2`    |
| 20     | 4 bytes  | RGB+pad | `fog_color_1`      |
| 24     | 4 bytes  | RGB+pad | `fog_color_2`      |
| 28     | 4 bytes  | RGB+pad | `fog_color_3`      |
| 32     | 18 bytes | int16×9 | `atmosphere[0..8]` |

Each `RGB+pad` is `uint8 r, g, b` followed by 1 byte of padding.

---

## Section 33: Text templates (dialog composer)

Compact token streams used to assemble dynamic dialog. Each template is a sequence of bytes terminated by the two-byte sequence `0x0A 0xFF`.

| Offset           | Length  | Description                          |
|------------------|---------|--------------------------------------|
| 0 + N × 4        | 4 bytes | Relative offset to template (sentinel: `0x00000000`) |
| (after sentinel) | varies  | Template token streams               |

**Token rules**:

- `0x0A` then a byte `≥ 0x20`: argument substitution. `arg_index = byte − 0x20`.
- `0x0A 0xFF`: end of template.
- Any other byte `B`: dictionary word at index `B`.

---

## Section 34: World-map draw points (positions / trigger table)

The world-map draw-point table. It holds the **trigger position** of each world draw point — **not** its magic. When the player presses the action button near a draw point, the world map uses this section to work out *which* draw-point index the player is standing on, then reads that index's magic / refill / high-yield byte from the EXE `DrawPointData` table (see [Draw point]({{site.baseurl}}/technical-reference/exedata/draw-point/)). So this section answers "*where* is world draw point N", while the EXE answers "*what* does it give".

> **Correction:** earlier notes described byte 2 of each record as a `magic_id` (with a `+0x80` offset) and reproduced a magic table. That is wrong. Byte 2 is a location discriminator, and world draw-point magic is stored in the EXE, not here. The old magic table is dropped.

### Layout

| Offset       | Length   | Description                    |
|--------------|----------|--------------------------------|
| 0x00         | 40 bytes | Block table: 5 × `BlockRange`  |
| 0x28         | 4 bytes  | `records_base` (always `0x2C`) |
| 0x2C + N × 4 | 4 bytes  | `DrawPoint` record (128 total) |

The section is `0x2C` (44) bytes of header followed by exactly **128** four-byte records (index `N = 0..127`). The record count is fixed; records are stored in draw-ID order.

**BlockRange** (8 bytes) — one per world-map draw-point block:

| Offset | Length  | Type   | Field        |
|--------|---------|--------|--------------|
| 0      | 4 bytes | uint32 | `start_off`  |
| 4      | 4 bytes | uint32 | `end_off`    |

`start_off` / `end_off` are byte offsets (relative to the section start) delimiting that block's slice of the record array. In `wmsetus.obj` the five blocks are `[0x2C,0x200)`, `[0x200,0x204)`, `[0x204,0x208)`, `[0x208,0x210)`, `[0x210,0x228)` — i.e. record ranges `0..116`, `117`, `118`, `119..120`, `121..126`. The runtime picks a block per world region through a small EXE lookup table (`0xC76E70`, indexed by `region & 0x1F`), so only the draw points in the player's current region are scanned. Because records never move, the block table stays valid when records are edited in place.

**DrawPoint** (4 bytes):

| Offset | Length  | Type   | Field    |
|--------|---------|--------|----------|
| 0      | 1 byte  | uint8  | `x`      |
| 1      | 1 byte  | uint8  | `y`      |
| 2      | 1 byte  | uint8  | `sub_id` |
| 3      | 1 byte  | uint8  | padding (always `0`) |

- `x`, `y` together form the 16-bit world-map **block id** (`x | y << 8`) that the draw point is anchored to. `x` is the block column, `y` the block row. (Per legacy notes, `x` spans `0x00..0xFF` with the high bit selecting the lower of two stacked rows within a segment; `y` is the segment/row index.)
- `sub_id` is a **location discriminator**: several draw points can share the same `(x, y)` block, and `sub_id` tells them apart. On the islands (Closest to Heaven / Hell) many records share a block and differ only by `sub_id` — e.g. block `(113, 10)` carries three draw points with `sub_id` `15`, `27`, `33`.

### How a draw is resolved (runtime)

`WorldMap_DrawPointsParsing_wmset35` (`0x54F920`) scans the block for the record whose `(x,y)` equals the current block id **and** whose `sub_id` equals the current location index, and returns the **record index** `N` (0..127). `World_Interaction_Draw_SubQuest` (`0x54E9B0`) then:

1. adds `128` → EXE `DrawPointData` index (`128..255`);
2. calls `GetDrawMagic` (`0x52D1E0`) → reads the magic / refill / high-yield byte from the EXE table at `0xB92328`;
3. decodes it exactly like a field draw point (`magic = byte & 0x3F`, `refill = byte & 0x40`, `high_yield = byte & 0x80`).

### Mapping to the EXE draw table

Record index `N` (0..127) is world draw point `N`; its magic/refill/high-yield lives at EXE `DrawPointData[128 + N]`, i.e. **Draw ID `129 + N`** in the 1-based numbering used by [Draw point]({{site.baseurl}}/technical-reference/exedata/draw-point/). Record 127 is the unused final entry (`x=y=sub_id=0`, Draw ID 256). The section is parsed by `Wmset_ParseSections` (`0x542DA0`) into the global `dword_2040124`.

---

## Section 35: Special locations (save / GF / warp points)

Point-of-interest markers used by world-map UI: save points, GF battles, warp targets, etc. No header; records pack back-to-back at 12 bytes each (`record_count = section_size / 12`).

**SpecialLocation** (12 bytes):

| Offset | Length  | Type   | Field        |
|--------|---------|--------|--------------|
| 0      | 4 bytes | int32  | `x`          |
| 4      | 4 bytes | int32  | `z`          |
| 8      | 2 bytes | int16  | `y`          |
| 10     | 1 byte  | uint8  | `type_code`  |
| 11     | 1 byte  | int8   | `extra`      |

Note the field order: `x`, `z`, `y` — not `x`, `y`, `z`.

---

## Section 36: Event scripts

Generic script section. Top-level event scripts that run while the world map is active. Drives world-map state transitions (`SET_WORLD_MAP_STATE`, `0xFF26`), global event triggers (`SET_GLOBAL_EVENT_TRIGGERED`, `0xFF36`) and per-region UI.

---

## Section 37: World-map textures (TIM archive)

The main texture archive for terrain. Contains the world tileset, beach/coast tiles, sky/cloud strip, and special-effect textures. Around 36 entries in the original release (with some entries unused / replaced by `texl.obj`).

| Offset           | Length  | Description                              |
|------------------|---------|------------------------------------------|
| 0 + N × 4        | 4 bytes | Relative offset to TIM (sentinel: `0x00000000`) |
| (after sentinel) | varies  | TIM textures (`10 00 00 00 ..`)          |

See the **TIM texture format** appendix below for the per-TIM layout.

**Atlas conventions** (from our renderer):

- The land tileset is rendered as a 4 × 5 atlas of 256 × 256 tiles (1024 × 1280 px). TIM index `i` is placed at column `i // 5`, row `i % 5`.
- Each land TIM has 16 CLUTs; rendered as a 4 × 4 grid of 64 × 64 sub-tiles where sub-tile `(col, row)` uses palette `row × 4 + col` (this mirrors Deling's `TextureFile::gridImage(4, 4)`).
- Sea, beach, road and similar composites are built like Deling's `Map::composeTextureImage`: each TIM is pasted at its VRAM pixel position relative to the union's top-left. Sea composite is 256 × 128 (world TIMs 16..23); road composite is 192 × 64 (full road archive).

**FF8 transparency rule** (important): a texel is transparent if and only if the entire 16-bit colour word is `0x0000`. The PSX STP bit (bit 15) is **not** alpha — palettes with STP set on every entry still render opaque. Stock `TIM.save_png` uses STP as alpha, which is wrong for FF8 content; our renderer applies the FF8 rule, mirroring `FF8Color::fromPsColor` in [Deling](https://github.com/myst6re/deling).

---

## Section 38: Road / train track / bridge textures (TIM archive)

Same layout as Section 37 (offset list ending in `0x00000000`, then TIM data). Holds road tiles, train track tiles, and the bridge segment near Fisherman's Horizon (~52 entries in the original release).

---

## Section 39: One world-map texture (PSX disk-read fallback)

A single TIM, archive-style (one offset followed by `0x00000000`, then the TIM blob). Holds the first texture from Section 37 / `texl.obj`. Appears to be a PSX-specific disk-read fallback, mirroring the role of Section 28 for textures.

| Offset    | Length  | Description                          |
|-----------|---------|--------------------------------------|
| 0         | 4 bytes | Relative offset to TIM               |
| 4         | 4 bytes | `0x00000000`                         |
| 8         | varies  | TIM texture                          |

---

## Section 40: Palette (CLUT) animations

Animated palettes. The TIM's indexed pixel data stays put; only the 256-colour CLUT is rewritten per frame. In `wmsetus.obj` this section animates world TIMs 16, 17, 18, 19 (six frames each, forward loop) — driving the rippling sea/coastal hues.

| Offset           | Length  | Description                              |
|------------------|---------|------------------------------------------|
| 0 + N × 4        | 4 bytes | Relative offset to animation (sentinel: `0x00000000`) |
| (after sentinel) | varies  | Animation records                        |

**PaletteAnimation** (12-byte header + 4 × frame_count):

| Offset | Length  | Type   | Field         |
|--------|---------|--------|---------------|
| 0      | 1 byte  | uint8  | `flags`       |
| 1      | 1 byte  | uint8  | unknown       |
| 2      | 1 byte  | uint8  | `frame_count` |
| 3      | 1 byte  | uint8  | unknown       |
| 4      | 2 bytes | uint16 | `value_a` (palette dest VRAM x) |
| 6      | 2 bytes | uint16 | `value_b` (palette dest VRAM y) |
| 8      | 2 bytes | uint16 | `vram_x`      |
| 10     | 2 bytes | uint16 | `vram_y`      |
| 12     | 4 × F   | uint32 | `frame_rel_offsets[F]` (relative to `record_offset + 12`) |

Each frame occupies `20 + 512` bytes at `record_offset + 12 + frame_rel_offset`:

| Offset | Length    | Field                                |
|--------|-----------|--------------------------------------|
| 0      | 20 bytes  | Frame header (purpose not fully decoded) |
| 20     | 512 bytes | Palette data (256 × `uint16` BGR555+STP) |

`(value_a, value_b)` is the destination palette position in VRAM and is the easiest way to match an animation to its target TIM (the rectangle that contains `(value_a, value_b)` in `pal_x..pal_x+pal_w, pal_y..pal_y+pal_h` is the target).

---

## Section 41: Vehicle and object textures (TIM archive)

Same layout as Section 37. Holds textures for world-map objects — Balamb Garden, Galbadia Garden ("Galbadia mobile"), Balamb halo ring, cactuar statue, Lunatic Pandora, etc. ~132 entries in the original release.

---

## Sections 42 – 47: AKAO music and sound

Six adjacent AKAO sections. Each begins with the magic `"AKAO"` and contains one music or sound stream to the end of the section.

| Section | Notes                                |
|---------|--------------------------------------|
| 42      | AKAO (sound / music)                 |
| 43      | AKAO (music)                         |
| 44 – 47 | AKAO (sound / music)                 |

---

## Appendix A — Script format

Sections 7, 9, 11 and 36 share a "generic script" container.

### Container

| Offset           | Length  | Description                              |
|------------------|---------|------------------------------------------|
| 0 + N × 4        | 4 bytes | Relative offset to a script (sentinel: `0x00000000`) |
| (after sentinel) | varies  | Script bytecode for each entry           |

Each script's bytecode runs from its offset up to the next script's offset (or end of section). Scripts always terminate with `RETURN` (`0xFF16`, code id `−234`).

### Opcode

Each opcode is exactly 4 bytes:

| Offset | Length  | Type   | Field          |
|--------|---------|--------|----------------|
| 0      | 2 bytes | int16  | `code_id`      |
| 2      | 1 byte  | uint8  | `param1`       |
| 3      | 1 byte  | uint8  | `param2`       |

A 16-bit parameter is recovered as `param1 + param2 × 256`.

### Control flow

| ID   | Hex     | Name                | Notes |
|------|---------|---------------------|-------|
| −255 | `0xFF01` | `IF`                | Begin condition block (interpreter state v6 = 1). |
| −252 | `0xFF04` | `EXEC`              | Begin action block; runs when previous condition passed (v6 = 2, v4 = 3). |
| −251 | `0xFF05` | `ENDIF`             | End of IF/EXEC/ELSE; in exec mode this terminates the script (`sub_54D7E0` returns 0). |
| −246 | `0xFF0A` | `IFBLOCK`           | Explicitly begin an IF structure (v4 = 1). |
| −245 | `0xFF0B` | `ELSE`              | ELSE clause; from IF-true (v4 = 1) → exec-true (v4 = 2); from nested-true (v4 = 4) → nested exec (v4 = 3). |
| −244 | `0xFF0C` | `NESTEDIF`          | Nested IF inside an ELSE (valid from v4 = 2 or v4 = 5; sets v4 = 4). |
| −243 | `0xFF0D` | `NESTEDELSE`        | Nested ELSE inside an ELSE (valid from v4 = 2 or v4 = 5; sets v4 = 6). |
| −242 | `0xFF0E` | `GOTO`              | Unconditional jump to absolute byte offset = `param1 + param2 × 256` from the start of the current script. |
| −234 | `0xFF16` | `RETURN`            | End the script entry-point. |
| −235 | `0xFF15` | `SET_RETURN_VALUE`  | Set output value without stopping; `3` triggers a special return path (used in Section 11). |
| −248 | `0xFF08` | `RETURN_WITH_VALUE` | Terminate the script and return code `1` with `param` as output. |
| −213 | `0xFF2B` | `RETURN_WITH_CODE_3`| Terminate the script and return code `3` with `param` as output. |

### Conditions (used inside IF / IFBLOCK / NESTEDIF)

All return `1` (pass) or `−1` (fail). On fail the interpreter skips to the matching ELSE / ENDIF.

| ID   | Hex     | Name                          | Notes |
|------|---------|-------------------------------|-------|
| −254 | `0xFF02` | `LTEQ_THAN`                   | `param ≤ word_2036BDE` (persistent scenario phase, save-game offset 0x100, `SavemapVariables.unk5[12:13]`). |
| −253 | `0xFF03` | `GREATER_THAN`                | `param > word_2036BDE`. |
| −250 | `0xFF06` | `CHECK_REGION_NUMBER`         | `param == wm_GetRegionNumber(WORLD_MAP_COORD_X, Y)` (or tile-grid region in tile mode). |
| −249 | `0xFF07` | `CHECK_TILE_POSITION`         | `param == tile_x + 128 × tile_y` (wrapping). |
| −247 | `0xFF09` | `CHECK_VEHICLE_TYPE`          | Current vehicle equals `param`. Known values: 33 = bike, 48 = Balamb Garden, 49 = Shumi train, 50 = Ragnarok, 128 = on foot, 129 = any vehicle, 130 = Galbadia aircraft, 131 = mobile Garden, 132 = special. Fails if `dword_2040A2C` (override) is set. |
| −241 | `0xFF0F` | `X_GREATER_THAN`              | `param > (WORLD_MAP_COORD_X & 0x1FFF)`; tile mode uses `(dword_2040A24 % 4) << 11`. |
| −240 | `0xFF10` | `Y_GREATER_THAN`              | `param > (WORLD_MAP_COORD_Y & 0x1FFF)`; tile mode similar. |
| −239 | `0xFF11` | `X_LESS_THAN`                 | `param < (WORLD_MAP_COORD_X & 0x1FFF)`. |
| −238 | `0xFF12` | `Y_LESS_THAN`                 | `param < (WORLD_MAP_COORD_Y & 0x1FFF)`. |
| −233 | `0xFF17` | `CHECK_ENTITY_PROXIMITY`      | Nearest entity matching `param` is within camera-space sight range. |
| −232 | `0xFF18` | `CHECK_VEHICLE_ENTERING`      | Vehicle `param` in approaching/boarding state. Ragnarok: `byte_2036B70 == 6`. Balamb Garden: `byte_2036B70 == 9`. |
| −231 | `0xFF19` | `CHECK_VEHICLE_BOARDED`       | Vehicle `param` fully boarded. Ragnarok: 5. Balamb Garden: 8. |
| −230 | `0xFF1A` | `CHECK_CHARACTER_LOCATION`    | Nearest NPC has location code `param` (entity table `byte_20426D0`). |
| −229 | `0xFF1B` | `CHECK_CHARACTER_LOCATION_EX` | As above but excludes the 7 party/vehicle entity slots. |
| −228 | `0xFF1C` | `CHECK_CHARACTER_LOCATION_2`  | Secondary tracked entity `dword_C75D10` has location code `param`. |
| −227 | `0xFF1D` | `CHECK_CHARACTER_DISTANCE`    | Same as above plus camera-space angle ≤ 512 (~11°), excluding party slots. |
| −226 | `0xFF1E` | `FAIL`                        | Always fails — placeholder / force-ELSE. |
| −224 | `0xFF20` | `CHECK_BUTTON_INPUT`          | Button / stick edge detection. `param = 0xFFFF` checks any analogue dead-zone edge; otherwise `param` is a button bitmask. Fails if `dword_2040A38` (battle/cutscene lock) is set. |
| −223 | `0xFF21` | `CHECK_BATTLE_STATE`          | Battle just won/lost: `(dword_2040A34 != 0) || ((party_save[109] & 1) == param)`. |
| −222 | `0xFF22` | `CHECK_LOCATION_DRAW_REGISTER`| Which location-block is currently rendered (computed from `Worldmap_weirdregister0_LocationDRAW`). |
| −219 | `0xFF25` | `CHECK_WORLD_MAP_STATE`       | `byte_2036B70 == param`. Known: 0 = normal, 5 = Ragnarok active, 6 = Ragnarok approaching, 7 = Shumi, 8 = BG active, 9 = BG approaching, 10 = draw-point active, 13 = exiting to field, 14 = vehicle transition. |
| −217 | `0xFF27` | `CHECK_BIT_FLAG`              | Save-game bit `param1` (0..63) equals `param2` (0 or 1). Bits 0..31 → `dword_20403A4+116`; 32..63 → `dword_20403A4+120`. |
| −215 | `0xFF29` | `CHECK_DIALOG_STATE`          | Evaluates dialog slot `param`; stores active state / choice index in `dword_20402D8`. Passes if state ≥ 0. |
| −214 | `0xFF2A` | `COMPARE_DIALOG_RESPONSE`     | `dword_20402D8 == param` — branches on the dialog choice. |
| −212 | `0xFF2C` | `CHECK_DIALOG_CONFIRMED`      | `sub_543AE0(param1) == param2` — slot active and player confirmed. |
| −211 | `0xFF2D` | `COMPARE_SCRIPT_VAR`          | Script byte `[param1] == param2` (`param1` ∈ {0, 1}). Stored at `dword_20403A4+124`. |
| −209 | `0xFF2F` | `CHECK_RANDOM_NUMBER`         | Random uint16 < `param`. 0 = never, 65535 = always. |
| −208 | `0xFF30` | `COMPARE_SCRIPT_VAR_GT`       | `param2 > script_byte[param1]`. |
| −207 | `0xFF31` | `COMPARE_SCRIPT_VAR_LT`       | `param2 < script_byte[param1]`. |
| −206 | `0xFF32` | `CHECK_LOCATION_FLAG`         | Inverted bit-3 check on location-block flags byte (offset +14). |
| −205 | `0xFF33` | `COMPARE_LOCATION_BYTE`       | Per-location byte at offset +13 equals `param1`. |
| −204 | `0xFF34` | `CHECK_COMBAT_SCENE_ID`       | `param == COMBAT_SCENE_ID`. |
| −203 | `0xFF35` | `CHECK_BATTLE_RESULT`         | `byte_1CFF6E7 == 4`. No parameter is read. |
| −200 | `0xFF38` | `CHECK_MOVEMENT`              | `(isStateOfMovement != 0) == param` (1 = moving, 0 = standing still). |
| −199 | `0xFF39` | `CHECK_BATTLEVAR`             | `param == SG_UNKNOWN_BATTLE_VAR`. |

### Actions (used inside EXEC blocks)

| ID   | Hex     | Name                       | Notes |
|------|---------|----------------------------|-------|
| −237 | `0xFF13` | `ADD_ENTITY`               | Register entity. `param1` = entity type (0 = Squall, 1 = Seifer, 3 = Chocobo, 33 = bike, 48 = Balamb Garden, 50 = Ragnarok, 64..66 = Galbadia vehicles, 80 = SeeD ship, 94 = Lunatic Pandora …). `param2` = slot override or `0xFF` for default. Used only in Section 9. |
| −236 | `0xFF14` | `ADD_ENTITY_ALT`           | Same layout as `ADD_ENTITY`; identical handling in `sub_544860`. |
| −225 | `0xFF1F` | `SHOW_TEXT_BOX`            | Open text dialog (no choices) in slot `param1`. `param2` = string ID in Section 13. |
| −221 | `0xFF23` | `SHOW_CHOICE_BOX`          | Open choice dialog. `param1` = slot, `param2` = string ID. Choice-option IDs are hard-coded per call site. |
| −220 | `0xFF24` | `CLOSE_TEXT_BOX`           | Close dialog slot `param` (sets state −1, calls `sub_4A0660`). |
| −218 | `0xFF26` | `SET_WORLD_MAP_STATE`      | `byte_2036B70 = param1`. See `CHECK_WORLD_MAP_STATE` for values. |
| −216 | `0xFF28` | `SET_BIT_FLAG`             | Save-game bit `param1` set to `param2` (0 / 1). |
| −210 | `0xFF2E` | `SET_SCRIPT_VAR`           | `script_byte[param1] = param2` (`param1` ∈ {0, 1}). |
| −202 | `0xFF36` | `SET_GLOBAL_EVENT_TRIGGERED`| `dword_2040A40 = 1` — suppresses further global event checks this frame (params ignored). |
| −201 | `0xFF37` | `ADD_ITEM`                 | `AddItemToInventory(param1, param2)` (item id, quantity). |

(Opcodes documented here are the ones implemented in `src/sections/opcodes.py`. Anything not listed is currently unrecognised in this build.)

---

## Appendix B — TIM texture format

Each texture entry in Sections 37, 38, 39 and 41 is a PSX TIM blob.

**Header** (8 bytes minimum):

| Offset | Length  | Field                                |
|--------|---------|--------------------------------------|
| 0      | 4 bytes | Magic `10 00 00 00`                  |
| 4      | 1 byte  | Flags (bits 0–1 = BPP, bit 3 = has palette) |
| 5      | 3 bytes | Padding                              |

**BPP values**: `0` = 4-bit indexed (16 colours), `1` = 8-bit indexed (256 colours), `2`/`3` = 16-bit direct. Indexed BPP requires a CLUT block; direct BPP must not.

**If indexed**, a CLUT block follows immediately:

| Offset | Length  | Type   | Field                |
|--------|---------|--------|----------------------|
| 0      | 4 bytes | uint32 | `pal_size` (includes the 12-byte header that follows) |
| 4      | 2 bytes | uint16 | `pal_x` (VRAM word column) |
| 6      | 2 bytes | uint16 | `pal_y` (VRAM row)   |
| 8      | 2 bytes | uint16 | `pal_w` (colours per CLUT) |
| 10     | 2 bytes | uint16 | `pal_h` (number of CLUTs) |
| 12     | `pal_size − 12` | uint16 | Palette entries (BGR555 + STP) |

Number of CLUTs in this TIM:

```
one_pal_size = 16 if BPP == 0 else 256
nb_pal = (pal_size − 12) / (one_pal_size × 2)
```

**Image block** (always present, follows the CLUT):

| Offset | Length  | Type   | Field                |
|--------|---------|--------|----------------------|
| 0      | 4 bytes | uint32 | `img_size` (includes the 12-byte header that follows) |
| 4      | 2 bytes | uint16 | `img_x` (VRAM word column) |
| 6      | 2 bytes | uint16 | `img_y` (VRAM row)   |
| 8      | 2 bytes | uint16 | `img_w` (in 16-bit words) |
| 10     | 2 bytes | uint16 | `img_h` (in pixels)  |
| 12     | `img_size − 12` | bytes | Pixel data |

**Pixel-width conversion** (logical width in pixels):

- BPP 0 (4 bpp): `pixels_w = img_w × 4`
- BPP 1 (8 bpp): `pixels_w = img_w × 2`
- BPP 2/3 (16 bpp): `pixels_w = img_w`

**Pixel encoding**:

- BPP 0: two 4-bit CLUT indices per byte (low nibble = first pixel, high nibble = second).
- BPP 1: one 8-bit CLUT index per byte.
- BPP 2/3: one 16-bit BGR555 + STP colour per pixel.

**Colour word** (16-bit, little-endian):

| Bits  | Field |
|-------|-------|
| 0–4   | R (5-bit) |
| 5–9   | G (5-bit) |
| 10–14 | B (5-bit) |
| 15    | STP (PSX semi-transparency) |

**FF8 alpha rule**: a texel is transparent iff the 16-bit colour word is exactly `0x0000`. The STP bit alone is not alpha — many FF8 palettes have STP set on every entry yet render opaque. See `wmx/atlas.py:_palette_rgba` and Deling's `FF8Color::fromPsColor` for the reference implementation.

**VRAM positioning**: `img_x` is in 16-bit-word columns, so the pixel column of the TIM's top-left corner is `img_x × 4` (4 bpp), `img_x × 2` (8 bpp), or `img_x × 1` (16 bpp). `img_y` is already in pixel rows. This is what our composite builders use to lay sea / road / beach tiles out exactly as the original artwork dictates.

---

## Appendix C — Related files

- `wmx.obj` — the world-map geometry stream (segment grid). Section 28 in `wmsetxx.obj` is a duplicate of one of its water segments. See addon source `src/wmx/` for parsing details (32 × 24 segments, 16 blocks per segment, polygons reference `wmsetxx.obj` textures via `(tex_page, clut_id)`).
- `texl.obj` — paged world textures. 20 slots of `0x12800` bytes each; each slot is a TIM identical in layout to the ones in Section 37.
