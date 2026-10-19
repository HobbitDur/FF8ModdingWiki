---
layout: default
title: Scan (camera and text)
parent: ExeData
author: HobbitDur
permalink: /technical-reference/exedata/scan/
---

1. TOC
{:toc}

# Scan

Scan shows a target's name, description and stats. Two things it uses live in the exe, not in
the battle files: the **camera framing** of each target and the **scan text** of each monster.
Both are indexed by the target's com_id (a monster's com_id is its c0m number + 16).

FFNx lets modders replace both from `direct/exe/` (or `direct/<language>/exe/`), see
[FFNx files](#ffnx-files).

## Full scan and short scan

The Scan magic effect (magic effect 39) plays one of two versions:

| Version    | When                                                                                         | What the player sees                                               |
|------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Full scan  | first scan of a species, or the Config **Scan** option set to full                           | zoom-in on the target, then the info screen with the turning model |
| Short scan | the species bit is already in `SG_ENEMY_SCANNED_ONCE` and the Config Scan option is on short | zoom-in on the target and the text box, the camera circling it     |

`Damage_DispatchByAttackType` decides it in its `ATTACK_TYPE_SCAN` case: when
`SG_SETTING.scan` bit 0 is clear and the target's species is already marked scanned, it sets bit
2 of the action result. `MAG_040_SCAN_Emitter_State0_SpawnScanner` then spawns the short
scanner instead of the full one. Magic effect 67 is a second copy of the Scan code that only has
the short version; it uses its own, identical copy of the camera table.

## Camera table

The table holds one 16-byte row per target. The vanilla table has 166 rows, and both copies
(effects 39 and 67) are byte-identical in all seven PC releases (EN, FR, DE, IT, ES, JP, JP NV).

| Offset | Type  | Name             | Description                                                                            |
|--------|-------|------------------|----------------------------------------------------------------------------------------|
| 0x00   | int16 | distance         | Camera distance from the aim point, negative = in front of the target                  |
| 0x02   | int16 | offset_x         | Side offset of the aim point in the info screen: it moves the model away from the text |
| 0x04   | int16 | offset_y         | Height of the aim point above the floor (negative = up)                                |
| 0x06   | int16 | model_offset_y   | Height of the point the model turns around when the player tilts it                    |
| 0x08   | int16 | aim_at_model     | 0 = aim at the target's position on the floor, otherwise at its centre bone            |
| 0x0A   | int16 | view_offset_y    | Height offset used while the player moves a target whose aim_at_model is 0             |
| 0x0C   | uint8 | can_pitch        | 1 = the player can tilt the model in the info screen                                   |
| 0x0D   | uint8 | can_yaw          | 1 = the model turns on its own in the info screen, and the player can turn it          |
| 0x0E   | uint8 | short_scan_orbit | 1 = the camera circles the target during the short scan                                |
| 0x0F   | uint8 | padding          | Always 0                                                                               |

Most monsters share the same framing, the one of G-Soldier (row 87): distance -4608, offset_x 512,
offset_y -640, model_offset_y 640, aim_at_model 1, view_offset_y 0, flags 1, 1, 1.

### Row selection

`MAG_040_SCAN_GetCameraRowIndex` returns the target's com_id, except for six monster states that
have a framing of their own:

| Row | Monster (com_id)                      | Condition                   |
|-----|---------------------------------------|-----------------------------|
| 160 | Fastitocalon, Fastitocalon-F (36, 37) | the entity flag word is -1  |
| 161 | Armadodo (43)                         | not in animation sequence 1 |
| 162 | Abadon (119)                          | not in animation sequence 1 |
| 163 | Bomb (59)                             | size scale 0x1800 (1.5x)    |
| 164 | Bomb (59)                             | size scale 0x2000 (2x)      |
| 165 | Imp (75)                              | not in animation sequence 1 |

The row index is also stored in the scan state (word at +0x4C). Rows 0-159 cover com_id 0-159,
so a monster loaded through FFNx from c0m144 (com_id 160 and up) reads one of the alternate rows
above, or past the end of the table, unless FFNx extends it.

### Camera placement

`MAG_040_SCAN_Camera_Setup` builds a target camera, which `MAG_040_SCAN_CameraBlendStep` reaches
over a few ticks and `MAG_040_SCAN_CameraApply` turns into the battle camera:
`eye = look-at + RotY(yaw) * (0, height, distance)`, with the lens (projection H) set to 576.

The aim point P is the model's centre: `GetEffectSpawnPosition` with bone selector 0xF1, which
reads byte 5 of the skeleton section header (bit 0x80 = the end of the bone, otherwise its start).
When aim_at_model is 0, P is the target's position instead. P's height is then forced to 0 (the
floor). R is the rotation of the target's facing.

| Camera mode | Used by                                        | Look-at                      | Distance       | Height     | Blend speed |
|-------------|------------------------------------------------|------------------------------|----------------|------------|-------------|
| 0           | zoom-in while the reticle locks on, short scan | P + R(0, offset_y, 0)        | 3/4 × distance | distance/2 | 256         |
| 1           | full scan info screen                          | P + R(offset_x, offset_y, 0) | distance       | 0          | 682         |

In the info screen, the model turns by 64/4096 of a turn per tick when can_yaw is 1, around a
pivot raised by model_offset_y.

### Player controls in the info screen

`MAG_040_SCAN_ReadViewInput` reads the pad (and the analog sticks, scaled the same way) and
`MAG_040_SCAN_Viewer_Update` applies it every tick:

| Input              | Effect                                | Per tick (full input) | Condition      |
|--------------------|---------------------------------------|-----------------------|----------------|
| Left / Right       | turn the model                        | ±128/4096 of a turn   | can_yaw is 1   |
| Up / Down          | tilt the model                        | ±128/4096 of a turn   | can_pitch is 1 |
| L1 or R1 + Up/Down | zoom, scale 2048 to 8192 (0.5x to 2x) | ±128                  |                |
| L2 or R2 + pad     | move the model in the screen plane    | ±64 units             |                |
| L1 + L2 together   | back to the starting pose             |                       |                |

The model's orientation is RotY(turn) × RotX(tilt), scaled by the zoom, turning around the point
model_offset_y above its origin; a move is applied along the target's starting facing. Any input
stops the automatic turn. After 75 ticks without input, `MAG_040_SCAN_Viewer_Reset` puts back the
starting rotation, scale 4096 and no move, and the automatic turn starts again.

During the short scan (`MAG_040_SCAN_ShortScanner_State3_CircleUntilTextClosed`), each tick:

- when short_scan_orbit is 1, the camera yaw turns by 64/4096 of a turn, so the camera circles
  the target;
- when offset_y is below -384 (a tall target), the camera height moves by -height/32 toward the
  aim level, stopping at 0.

## Scan text

The scan text table holds one string per com_id (160 strings in the vanilla exe), read by
`Scan_GetText` with the target's `com_file_id`. The info screen draws three text layers:

| Layer | Content                                | Rectangle (x, y, width, height) |
|-------|----------------------------------------|---------------------------------|
| 2     | monster name (from the monster's .dat) | 170, 30, 136, 28                |
| 0     | scan text (the description)            | 170, 52, 136, 128               |
| 1     | info bar, one line at a time           | 16, 180, 296, 28                |

`setTextPosition` draws a layer's text 6 pixels inside its rectangle, one line every 16 pixels,
with room for (height - 12) / 16 lines: one line for the name and the info bar, 7 lines for the
description.

### The description has a single page

The description is set once and never scrolled or paged. Only its first 7 lines fit in the box,
and `Text_RenderGlyphs` stops at a page break (`0x01` or `0x07`), so the text after a page break
is never shown. Lines are broken with `0x02` only: the game does not wrap long lines.

### Info bar pages

The "pages" of the Scan screen are the lines of the info bar under the model and the description.
`MAG_040_SCAN_TextPager_State0_TextOpen` builds them with `manageScanText_Dup`, in this order:

| Line                    | Content                                                                                     | When                                       |
|-------------------------|---------------------------------------------------------------------------------------------|--------------------------------------------|
| Level and HP            | "Lv" level, "HP" current HP / max HP                                                        | always; HP shows "?????" for a target with flag 0x2000 set |
| Undead / Flying monster | "Undead", "Fly" and "monster" kernel texts                                                  | monsters with the undead or flying flag    |
| Very weak against       | the elements with an element defence of 600 or less                                         | at least one such element (no HP-hiding flag) |
| Weak against            | element defence 601 to 799                                                                   | same                                       |
| Strong against          | element defence 801 to 899                                                                   | same                                       |
| Has no effect           | element defence 900                                                                          | same                                       |
| Absorbs                 | element defence above 900                                                                    | same                                       |
| Extra scan text         | the battle text set by the monster's AI with `setScanText` ([AI opcode 0x25](../../battle/battle-scripts/#opcode-0x25-37---setscantext)) | the monster's AI set one              |

Every line comes from the kernel's battle texts and the target's battle stats, except the extra
scan text, which the AI copies from the monster's own battle texts (24 bytes at most, including
the end byte; text id 0xFF clears it).

How the lines are put together:

- The texts are kernel.bin misc texts (misc text section, by index): 0x21 "LEVEL", 0x22 "HP",
  0x24 "Monster", 0x25-0x29 the five group texts, 0x63 "Fly", 0x65-0x6C the element names,
  0x71 "?????", 0x72 "Undead". The level/HP line reads, in English, "LEVEL 20 HP 600/600".
- The parts are joined with a separator byte taken from misc text 0x0B (the number and symbol
  text): its character 0 (a space) between parts and its character 18 ("/") between the HP values.
  Numbers use its characters 1 to 10 as the digits, without leading zeros. Each HP value shows
  "?????" when it is above 99999, and both do when the HP is hidden.
- The undead/flying line always joins four parts and an element line nine (the group text and
  eight element slots), so empty slots leave trailing spaces, which draw nothing.
- The element names are not letters: each one is a text icon (code 0x05 followed by 0x5D-0x64).
  An icon code of 0x40 or more is looked up in a table of the exe that gives the icon.sp1 sprite,
  here sprites 288-295 (Fire to Holy); codes 0x30-0x3F are sprite code + 80, and 0x20-0x2F are pad
  buttons that follow the key config. After an icon the text goes on at the sprite's width
  (largest quad offset + width) plus 1 pixel.
- The battle slot values come from the monster's .dat info section when the monster is set up:
  the level is capped at 100, the HP is the HP curve at that level, the element defence of an
  element is 10 × its .dat byte (so 800 is normal damage and is in no group), and "HP hidden"
  (bit 0x10 of the flag byte at 0xF7) sets the slot flag 0x2000.
- Only monsters get the undead/flying line and the extra scan text. Characters (battle slots 0-2)
  get the level/HP line and element lines from their own element defence.

`MAG_040_SCAN_TextPager_State1_TextShowLine` shows one line and starts a 45-tick timer (3
seconds). Then `MAG_040_SCAN_TextPager_State2_PageInput`:

- turns to the next line when the button in the Circle slot of the button config is newly
  pressed, or when the timer runs out;
- goes back to the first line after the last one;
- closes the Scan screen when the button in the Cross slot (confirm) is held.

To add a page to a monster's Scan screen, give its AI a `setScanText` call with one of its battle
texts. The other lines follow the monster's stats, and the description cannot have more pages.

## Screen graphics

While the camera zooms in, the Dimmer task darkens the other entities and the battle stage, then
hides them. In their place, `MAG_040_SCAN_DrawScanBars` fills the whole screen from the zoom-in
until the Scan screen is closed: 5 rows of 3 opaque textured quads of 128 × 64 pixels, showing the
blue scan lines of the Scan texture (`mag039-067.tim`, texture page 0xBA, CLUT 0x3C94, u from 128
down to 0, v 0 to 64). The rows start at (frame counter & 63) − 64, so the lines scroll down one
pixel a tick, and their black texels are transparent. The tiles fade in during the zoom (colour
+8 a tick up to 128).

Over them come four effect models stored in the exe's data and drawn in view space (no camera) by
`MAG_040_SCAN_DrawHudModel`:

| Part       | Model                              | Position (x, y, z)    | Behaviour                                                                  |
|------------|------------------------------------|-----------------------|----------------------------------------------------------------------------|
| Backdrop   | 84 vertices, 16 + 56 Gouraud faces | -3968, 3840, 32767    | scale 4608; the blue "spotlight" behind the model; fades in from black by 512/4096 a tick |
| Spinner    | 24 vertices, 16 + 12 flat faces    | -128, -160, 1152      | turns 192/4096 a tick about Y and 96/4096 about Z; fades in by 256 a tick |
| Stat board | 1 textured quad (48 × 32)          | -64, -88, 576         | the labels HP, STR., DEF., INT., SPI., DEX., EVA. from the Scan texture (`mag039-067.tim`) |
| Stat bars  | 6 vertices, 2 Gouraud quads each   | board + table / 2     | 8 bars from a table: x, y, Z turn (0 or 180°), delay, pulse phase           |

The bars are, in table order: 0 and 1 HP (to the left and to the right of the board), then STR,
VIT, MAG, SPR, SPD and EVA, on alternating sides. Each bar appears after its delay (1 to 13 ticks),
grows by 768/4096 a tick up to its length and pulses: its colour is faded towards black by
(sin(phase) + 4096) / 6, the phase moving 256 a tick. The full length (scale 16384, 64 pixels) is
reached at 999 HP, 127 for STR to SPD and 25 for EVA; higher values are capped.

The drawing matrix is RotZ × RotX × RotY, scaled per axis, translated by the position. With the
Scan screen's projection (576), a model at z 576 is drawn one unit per pixel around the screen
centre. All faces are two-sided and depth-cued towards black by the part's fade value (4096 =
black). Every primitive of the models is semi-transparent; the texture page sets additive
blending, so the backdrop adds its blue light over the scan lines and the other parts add light
over the model.

The models use the format of the effect primitive models (`Effect_RenderPrimModel`): a u32 offset
of the primitive sections, a u32 vertex count, the vertices (x, y, z, padding: 4 × s16), then eight
sections, each a u32 count followed by its entries. Vertex numbers are stored doubled (4-byte units).

| Section | Primitive                      | Entry size | Entry                                                                         |
|---------|--------------------------------|------------|-------------------------------------------------------------------------------|
| 0       | flat triangle                  | 12         | colour + GPU code, 3 vertex numbers, padding                                  |
| 1       | flat quad                      | 12         | colour + GPU code, 4 vertex numbers                                           |
| 2       | flat textured triangle         | 20         | colour + code, 3 vertex numbers, uv2, uv0 + CLUT, uv1 + texture page          |
| 3       | flat textured quad             | 24         | colour + code, 4 vertex numbers, uv0 + CLUT, uv1 + texture page, uv2, uv3     |
| 4       | Gouraud triangle               | 20         | colour 0 + code, 3 vertex numbers, padding, colours 1-2                        |
| 5       | Gouraud quad                   | 24         | colour 0 + code, 4 vertex numbers, colours 1-3                                 |
| 6       | Gouraud textured triangle      | 28         | as section 2 with colours 1-2 after the vertex numbers                         |
| 7       | Gouraud textured quad          | 36         | as section 3 with colours 1-3 after the vertex numbers                         |

Bit 1 of the GPU code makes a primitive semi-transparent. The layouts of sections 2, 6 and 7 follow
from their sizes; the Scan models do not use them.

## FFNx files

| File                      | Content                                                                             | Size                     |
|---------------------------|-------------------------------------------------------------------------------------|--------------------------|
| `battle_scan_cameras.bin` | the camera table, no header                                                         | exactly 262 × 16 = 4,192 |
| `battle_scans.msd`        | the scan texts: u32 offsets (count = first offset / 4), then 0-terminated FF8 texts | any                      |

`save_exe_data` dumps both from the exe. The same camera rows feed both Scan effects. In the FFNx
camera table, rows 0-165 are the vanilla rows and the monsters from c0m144 use row c0m + 22
(com_id 160 → row 166, up to com_id 255 → row 261); those rows start with G-Soldier's framing.
The scan text of a monster is entry com_id of the msd, so a file used with monsters from c0m144
must reach their com_id.

FF8UltimateEditor's **Xu** tool edits both files and previews them on the monster's model the
way the game frames it, with the name, the description, the info bar lines and the screen graphics.

## Reference (names & addresses)

FF8_EN.exe:

| Name                                                     | Address   |
|----------------------------------------------------------|-----------|
| `MAG_040_SCAN` (magic effect 39)                         | 0x84D030  |
| `MAG_068_SCAN` (magic effect 67)                         | 0x7DC1A0  |
| `MAG_040_SCAN_Emitter_State0_SpawnScanner`               | 0x84D2C0  |
| `MAG_040_SCAN_FindScannedEntities`                       | 0x84D320  |
| `MAG_040_SCAN_GetCameraRowIndex`                         | 0x84D410  |
| `MAG_040_SCAN_Camera_Setup`                              | 0x84E870  |
| `MAG_040_SCAN_GetCameraRow`                              | 0x84EAF0  |
| `MAG_040_SCAN_CameraBlendStep`                           | 0x84EB40  |
| `MAG_040_SCAN_CameraApply`                               | 0x84EC80  |
| `MAG_040_SCAN_Viewer_State0_SpawnTextPager`              | 0x84F8D0  |
| `MAG_040_SCAN_Viewer_Setup`                              | 0x84FCD0  |
| `MAG_040_SCAN_Viewer_Update`                             | 0x84FD90  |
| `MAG_040_SCAN_ReadViewInput`                             | 0x8501F0  |
| `MAG_040_SCAN_Viewer_Reset`                              | 0x850600  |
| `MAG_040_SCAN_TextPager_Tick`                            | 0x84FAF0  |
| `MAG_040_SCAN_TextPager_State0_TextOpen`                 | 0x84FB80  |
| `MAG_040_SCAN_TextPager_State1_TextShowLine`             | 0x84FBB0  |
| `MAG_040_SCAN_TextPager_State2_PageInput`                | 0x84FC30  |
| `MAG_040_SCAN_ShortScanner_State3_CircleUntilTextClosed` | 0x8511A0  |
| `MAG_068_SCAN_GetCameraRowIndex`                         | 0x7DC560  |
| `MAG_068_SCAN_CameraSetup`                               | 0x7DD9B0  |
| `MAG_068_SCAN_GetCameraRow`                              | 0x7DDC30  |
| `MAG_068_SCAN_Scanner_CircleTarget`                      | 0x7DE710  |
| `GetEffectSpawnPosition`                                 | 0x502170  |
| `Damage_DispatchByAttackType` (`ATTACK_TYPE_SCAN`)       | 0x4925A6  |
| `setTextPosition`                                        | 0x4A07A0  |
| `Text_RenderGlyphs`                                      | 0x4A1570  |
| `manageScanText_Dup` (info bar lines)                    | 0xB68390  |
| `ScanText_CollectElementsByAffinity_Dup`                 | 0xB686D0  |
| `concatenateTwoStringWithSpaceOrNext`                    | 0x495210  |
| `getNumberInTextFromKernel`                              | 0x495330  |
| `getAddressTextMisc`                                     | 0x47EC70  |
| `setMonsterInfoFromDatInfoSection`                       | 0x48BBD0  |
| `Text_IconCodeToSpriteId`                                | 0x49F930  |
| `TEXT_ICON_CODE_TO_SPRITE` (u16 per icon code)           | 0xB86D84  |
| `Menu_GetSp1IconSize`                                    | 0x4B73F0  |
| `MAG_040_SCAN_DrawHudModel`                              | 0x84D8B0  |
| `MAG_040_SCAN_DrawScanBars`                              | 0x84F0B0  |
| `MAG_040_SCAN_ScanBars_Tick`                             | 0x84EFF0  |
| `MAG_040_SCAN_Dimmer_State1_FadeIn`                      | 0x84EE70  |
| `MAG_040_SCAN_Dimmer_State2_HideOthers`                  | 0x84EF40  |
| `MAG_040_SCAN_Spinner_Tick` / `_State0_Init`             | 0x84F300 / 0x84F390 |
| `MAG_040_SCAN_StatBoard_State0_Init`                     | 0x84F4A0  |
| `MAG_040_SCAN_StatBar_Tick` / `_State0_Init`             | 0x84F520 / 0x84F5C0 |
| `MAG_040_SCAN_Backdrop_Tick` / `_State0_Init`            | 0x84F9E0 / 0x84FA50 |
| `Effect_RenderPrimModel`                                 | 0x572200  |
| Backdrop / spinner / board models                        | 0x15CEA34 / 0x15CF37C / 0x15CF5B4 |
| Stat bar models (bars 0-1, then 2-7)                     | 0x15CF6FC, 0x15CF784 + 0x88 × n |
| Stat bar table (8 × 10 bytes; short scan's: 0x15D16C8)   | 0x15D1678 |
| `ScanText_CollectElementsByAffinity_Dup`                 | 0xB686D0  |
| `ScanText_GetLine_Dup`                                   | 0xB68810  |
| `Scan_GetText`                                           | 0xB687C0  |
| `g_ScanTextOffsets` (160 u16)                            | 0x1887474 |
| `g_ScanTextData`                                         | 0x18875B4 |
| `g_Scan_CameraRows` (effect 39)                          | 0x15D0B40 |
| `g_Scan2_CameraRows` (effect 67)                         | 0x1594998 |
| `BATTLE_SLOT_DATA[0].com_file_id`                        | 0x1D27BCB |
| `SG_ENEMY_SCANNED_ONCE`                                  | 0x1CFE964 |

Camera table and lookup in every release:

| Release | `GetCameraRow` (39) | `g_Scan_CameraRows` | `GetCameraRow` (67) | `g_Scan2_CameraRows` |
|---------|---------------------|---------------------|---------------------|----------------------|
| EN      | 0x84EAF0            | 0x15D0B40           | 0x7DDC30            | 0x1594998            |
| FR      | 0x84F020            | 0x15D0BF0           | 0x7DE160            | 0x1594A48            |
| DE      | 0x84F120            | 0x15D0D40           | 0x7DE260            | 0x1594B98            |
| IT      | 0x84F0A0            | 0x15D0CA0           | 0x7DE1E0            | 0x1594AF8            |
| ES      | 0x84F110            | 0x15D0CB0           | 0x7DE250            | 0x1594B08            |
| JP      | 0x86C1A0            | 0x17D4DC0           | 0x7FB270            | 0x1798C18            |
| JP NV   | 0x86C3A0            | 0x17D4DC0           | 0x7FB470            | 0x1798C18            |
