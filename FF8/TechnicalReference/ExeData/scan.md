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

During the short scan (`MAG_040_SCAN_ShortScanner_State3_CircleUntilTextClosed`), each tick:

- when short_scan_orbit is 1, the camera yaw turns by 64/4096 of a turn, so the camera circles
  the target;
- when offset_y is below -384 (a tall target), the camera height moves by -height/32 toward the
  aim level, stopping at 0.

## Scan text

The scan text table holds one string per com_id (160 strings in the vanilla exe), read by
`Scan_GetText` with the target's `com_file_id`. The info screen draws two text layers:

| Layer | Content                                | Rectangle (x, y, width, height) |
|-------|----------------------------------------|---------------------------------|
| 2     | monster name (from the monster's .dat) | 170, 30, 136, 28                |
| 0     | scan text                              | 170, 52, 136, 128               |

`setTextPosition` draws a layer's text 6 pixels inside its rectangle, one line every 16 pixels,
with (height - 12) / 16 lines per page: one line for the name, 7 lines per page for the scan
text. A longer text is split into pages: `MAG_040_SCAN_TextPager_State2_PageInput` turns the page
when the player presses the page button, or by itself when its timer runs out, and goes back to the
first page after the last one.

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
way the game frames it.

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
| `MAG_040_SCAN_TextPager_State2_PageInput`                | 0x84FC30  |
| `MAG_040_SCAN_ShortScanner_State3_CircleUntilTextClosed` | 0x8511A0  |
| `MAG_068_SCAN_GetCameraRowIndex`                         | 0x7DC560  |
| `MAG_068_SCAN_CameraSetup`                               | 0x7DD9B0  |
| `MAG_068_SCAN_GetCameraRow`                              | 0x7DDC30  |
| `MAG_068_SCAN_Scanner_CircleTarget`                      | 0x7DE710  |
| `GetEffectSpawnPosition`                                 | 0x502170  |
| `Damage_DispatchByAttackType` (`ATTACK_TYPE_SCAN`)       | 0x4925A6  |
| `setTextPosition`                                        | 0x4A07A0  |
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
