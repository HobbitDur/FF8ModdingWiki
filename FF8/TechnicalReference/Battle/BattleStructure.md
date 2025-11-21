---
layout: default
parent: Battle
title: Encounters data (scene.out)
author: JeMaCheHi, HobbitDur, Nihil
permalink: /technical-reference/battle/battle-structure-sceneout/
---

Scene.out contains all the data for each encounter in the game, this includes enemy IDs, positions, flags and more.  

See the corresponding thread: <http://forums.qhimm.com/index.php?topic=15816.0>

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
| 0x40   | 16     | [Unknown 1](#unknowns)                                                                            |
| 0x50   | 16     | [Unknown 2](#unknowns)                                                                            |
| 0x60   | 16     | [Unknown 3](#unknowns)                                                                            |
| 0x70   | 8      | [Unknown 4](#unknowns)                                                                            |
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

This is likely the data for the camera thats used at the start of the fight, before ATB time starts.  

| Bits               | Description  |
|--------------------|--------------|
| 7-4 (Upper nibble) | Camera ID    |
| 3-0 (Lower nibble) | Animation ID |

Note that every encounter holds data for 2 cameras, we'll call the first one _Main Camera_ and the second one _Secondary Camera_.  
The games chooses which one to use when loading the battle, and it appears to pick the _Main Camera_ about 80% of the time.  

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

## Unknowns

**Unknown 1, 2, and 3** each contain 2 bytes per monster, making them 16 bytes long (8 monsters \* 2 bytes).  
**Unknown 4** contains 1 byte per monster, for a total of 8 bytes.  

The data is laid out sequentially, from _Monster 1_ through _Monster 8_, and each monster has its own set of values, though some values are shared between monsters.  
It appears that the game doesn't read these fields' data, suggesting they may be remnants of a scrapped feature.  

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