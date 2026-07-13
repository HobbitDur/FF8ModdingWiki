---
layout: default
parent: Battle
title: Encounters data (scene.out)
author: JeMaCheHi, HobbitDur, Nihil
permalink: /technical-reference/battle/battle-structure-sceneout/
---

Scene.out contains all the data for each encounter in the game, this includes enemy IDs, positions, flags and more.  

See the corresponding thread: <http://forums.qhimm.com/index.php?topic=15816.0>

Runtime loading and field/world-map handoff are documented in [Encounter Trigger Runtime](../encounter-trigger-runtime/) and [Battle Runtime](../battle-runtime/).

## File Structure

Scene.out contains no header. It is a raw list of 1024 encounters. Each encounter block consists of 128 bytes and has the following structure:

| Offset | Length | Description                                                                                                                                                                                                                                                                                                               |
|--------|--------|---------------------------------------------------------------------------------------------------|
| 0x00   | 1      | Battle Stage ID (See [.x files](../battle-stage-x))                                               |
| 0x01   | 1      | [Battle Flags](#battle-flags)                                                                     |
| 0x02   | 1      | Main [camera data](#camera-data)                                                                  |
| 0x03   | 1      | Secondary [camera data](#camera-data)                                                             |
| 0x04   | 1      | "NOT Visible" [enemy flags](#enemy-flags)                                                         |
| 0x05   | 1      | "Not Loaded" [enemy flags](#enemy-flags)                                                          |
| 0x06   | 1      | "NOT Targetable" [enemy flags](#enemy-flags)                                                      |
| 0x07   | 1      | "Enabled" [enemy flags](#enemy-flags)                                                             |
| 0x08   | 48     | [Enemy Coordinates](#enemy-coordinates)                                                           |
| 0x38   | 8      | [Enemy IDs](#enemy-ids)                                                                           |
| 0x40   | 16     | [Unused 1](#unused)                                                                               |
| 0x50   | 16     | [Unused 2](#unused)                                                                               |
| 0x60   | 16     | [Unused 3](#unused)                                                                               |
| 0x70   | 8      | [Unused 4](#unused)                                                                               |
| 0x78   | 8      | [Enemy Levels](#enemy-level)                                                                      |

## Battle Flags

Similarly to [enemy flags](#enemy-flags), it's a byte and each bit determines whether a specific flag is on or off.  

| Flag value | Name                       | Description                                                                      |
|------------|----------------------------|----------------------------------------------------------------------------------|
| 0x01       | Disable Escape             | Prevents escaping, AI opcode re-enable escaping                                  |
| 0x02       | Disable Victory Fanfare    | Disables the fanfare                                                             |
| 0x04       | Show Timer                 | Shows active timer                                                               |
| 0x08       | Disable EXP Gain           | Prevents EXP from being gained                                                   |
| 0x10       | Disable Post-Battle Screen | Doesn't show the post-battle screens (return to field instead)                   |
| 0x20       | Surprise Attack            | Monster's ATBs start full                                                        |
| 0x40       | Back Attack                | Monster's ATBs start full + all party members afflicted with _Back Attack_       |
| 0x80       | Force Standard Battle      | Normal ATB starting positions for everyone, no _Back Attack_ status applications |

## Camera Data

This byte selects the **battle-intro camera animation**: the camera sweep played when the battle starts, before ATB time starts. It is an index into the camera animation collection stored in the loaded battle stage's [.x file](../battle-stage-x/#camera-data), so the meaning of a given value depends entirely on which stage the encounter uses.

| Bits               | Description                                                                |
|--------------------|----------------------------------------------------------------------------|
| 7-4 (Upper nibble) | Camera animation **set** index (into the stage's camera animation collection) |
| 3                  | **Unused** (masked off by the engine)                                      |
| 2-0                | Camera animation index within the set (0-7)                                |

Each stage's camera animation collection declares its own number of sets (`NumOfSets`, first uint16 of the collection), and each set holds 8 animation pointers. If the set index is **out of range** for the stage (`set >= NumOfSets`), the engine silently does nothing: no intro animation plays and the camera stays at its default position. Values are therefore stage-dependent; for example `a0stg000.x` (Balamb Garden Quad) has 2 sets, so only `0x00`-`0x07` and `0x10`-`0x17` select an animation.

### Main vs Secondary camera

Every encounter holds two of these bytes; we'll call the first one (offset 0x02) _Main Camera_ and the second one (offset 0x03) _Secondary Camera_.

At battle load, `BS_CameraInit` (`0x500F70`) picks one of the two with a **fair 50/50 coin flip** (`pnrg_lcg_algo() & 1` — the LCG bit used is well mixed, so there is no bias toward the main camera; earlier observations of ~80% main were sample bias).

There is exactly one hardcoded exception: **encounter ID 33** (2× G-Soldier, Dollet elevator) always uses the _Main Camera_, presumably to keep that scripted Dollet sequence consistent.

### Runtime pipeline (PC 2000, FF8_EN.exe)

1. `FFBattleDirector_battleLoop` (`0x47CCB0`) loads the 128-byte encounter record into `CURRENT_ENCOUNTER_DATA_SCENE_OUT` (`0x1D287DC`) via `ReadSceneOutFileForSpecificEncounter` (`0x48D0E0`).
2. During stage init, the per-stage handler (`BS_StageXXX`) receives the *load camera* command and calls `BS_CameraInit` (`0x500F70`), which picks main/secondary as described above and stores the byte into **camera-VM variable 0** (`CURRENT_CAMERA_ANIMATION`, `0x1D97728`). It then resolves the stage .x camera section pointers (camera settings + animation collection) via `BS_GetCameraAnimPointers` (`0x509970`).
3. Every frame, `updateBattleCamera` (`0x504060`) → `BS_UpdateCameraSequence` (`0x509610`) executes the stage's *camera settings* byte-code with the shared animation-sequence VM (`computeAnimationSequence`, `0x50DB40` — the same VM used by [monster animation sequences](../monster-files-c0mxxxdat/) and [camera sequences](../model-sections/camera-sequence/)). Stage camera scripts start with camera opcode `05 00` = "play the camera animation whose ID is read from camera variable 0" — i.e. the scene.out byte.
4. `BS_GetCameraAnimationPointer` (`0x503520`) decodes the byte: `set = (id >> 4) & 0xF` (bounds-checked against `NumOfSets`), `anim = id & 7`, resolves the animation's relative pointer inside the stage file and spawns the `ProcessCameraAnimation` task that plays it.

After the intro animation ends, this byte has no further effect: mid-battle cameras are chosen per action by `cameraWhenDoingAction` (`0x506190`), which overwrites camera variable 0 with its own animation choices.  

## Enemy Coordinates 

Each encounter stores 8 enemy coordinate blocks, one for each monster slot.  
Each block is 6 bytes, containing 3 signed 16-bit values that represent the X, Y, Y positions.  

| Offset           | Size | Description |
|------------------|------|-------------|
| Slot ID \* 6 + 0 | 2    | X Position  |
| Slot ID \* 6 + 2 | 2    | Y Position  |
| Slot ID \* 6 + 4 | 2    | Z Position  |

## Enemy Flags

Enemy flags are one byte each, and each bit determines whether a specific monster's flag is on or off, starting from the leftmost bit (MSB) for Monster 1, down to the rightmost bit (LSB) for Monster 8.

| Flag value | Monster   |
|------------|-----------|
| 0x80       | Monster 1 |
| 0x40       | Monster 2 |
| 0x20       | Monster 3 |
| 0x10       | Monster 4 |
| 0x08       | Monster 5 |
| 0x04       | Monster 6 |
| 0x02       | Monster 7 |
| 0x01       | Monster 8 |

**NOT Visible** stops the monster from rendering.  
**NOT Targetable** removes the monster from the list of targetable enemies.  
**NOT Loaded** means the monster's AI isn't being evaluated.  
**Enabled** needs to be *true* for the monster to exist in the fight, even if it's not tagged as **NOT Visible** or **NOT Loaded**, it won't appear or do anything until it's **Enabled**.  

## Enemy IDs

Encounters hold 8 monster IDs.  
IDs are the last 3 digits of the monster's [c0mxxx.dat file](../monster-files-c0mxxxdat/)) + 0x10.  

| Offset     | Size | Monster      |
|------------|------|--------------|
| 0x00       | 1    | Monster 1 ID |
| 0x01       | 1    | Monster 2 ID |
| 0x02       | 1    | Monster 3 ID |
| 0x03       | 1    | Monster 4 ID |
| 0x04       | 1    | Monster 5 ID |
| 0x05       | 1    | Monster 6 ID |
| 0x06       | 1    | Monster 7 ID |
| 0x07       | 1    | Monster 8 ID |

## Unused

**Unused 1, 2, and 3** each contain 2 bytes per monster, making them 16 bytes long (8 monsters \* 2 bytes).  
**Unused 4** contains 1 byte per monster, for a total of 8 bytes.  

The data is laid out sequentially, from _Monster 1_ through _Monster 8_, and each monster has its own set of values, though some values are shared between monsters.  

**Confirmed unused (PC 2000, FF8_EN.exe):** disassembly analysis shows that no code ever reads offsets `0x40`-`0x77` of the encounter record:

- The loaded record lives at `CURRENT_ENCOUNTER_DATA_SCENE_OUT` (`0x1D287DC`) and is the game's only live copy (`ReadSceneOutFileForSpecificEncounter` at `0x48D0E0` is its only writer, and its staging buffer is not read anywhere else).
- Every other field of the record has cross-references (camera bytes → `BS_CameraInit`, enemy flags/IDs → `setEnemyVisibility` / `setAllMonsterInfoFromDatSection` / `linkedToMonsterVisibility`, coordinates → `getZCoordinateEnemyBattleTask67`, levels → `setAllMonsterInfoFromDatSection`), but the four unused blocks at `+0x40`, `+0x50`, `+0x60`, `+0x70` have **zero** cross-references, and all neighbouring array accesses are bounded to the 8 monster slots.

They are therefore remnants of a scrapped feature (their 2/2/2/1 bytes-per-monster layout suggests planned per-monster attributes that were never hooked up), and can be repurposed freely by mods targeting the PC version. (This has only been verified against the PC executable; the PSX build has not been checked.)  

## Enemy Level

Enemy levels are represented by 1 byte.

| Offset     | Size | Level         |
|------------|------|---------------|
| 0x00       | 1    | Monster 1 LVL |
| 0x01       | 1    | Monster 2 LVL |
| 0x02       | 1    | Monster 3 LVL |
| 0x03       | 1    | Monster 4 LVL |
| 0x04       | 1    | Monster 5 LVL |
| 0x05       | 1    | Monster 6 LVL |
| 0x06       | 1    | Monster 7 LVL |
| 0x07       | 1    | Monster 8 LVL |

By default, the enemy level is determined by the average level of the current team `team level`, and the game adds or substracts `team level / 5`.

- Numbers from 0 to 100 are fixed levels `N +- (N / 5)`. 
- From 101 to 200 are max levels fixed `min(team level +- (team level / 5), N)`
- From 201 to 250 are added values `team level + (N - 200)  +- ((team level + (N - 200)) / 5)`
- 251 is level between 1 to 65, but the game exceptionnaly doesn't divide the result by +-5, it adds or substracts a random value between 0 and 3 `min(team level +- rand(0, 3), 65)`
- 252 is completely random `rand(1, 100)`
- 253 is not used in the game, but the formula is random with a constraint `rand(1, team level +- (team level / 5))`
- 254 is the average team level, period, no division per 5 `team level`
- 255 is the standard formula `team level +- (team level / 5)`


## Notes

No more than 4 enemies can be **Enabled** at any given time.  
Using a value lower than 0x10 for an enemy ID will crash the game on battle start, as the first 16 IDs are reserved for playable characters.  