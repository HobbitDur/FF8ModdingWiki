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
| 0x01   | 1      | [Battle flags](#battle-flags)                                                                     |
| 0x02   | 1      | Main Camera data (the upper nibble is the camera's ID, the lower nibble is the animation ID)      |
| 0x03   | 1      | Secondary camera data (the upper nibble is the camera's ID, the lower nibble is the animation ID) |
| 0x04   | 1      | "NOT Visible" [enemy flags](#enemy-flags)                                                         |
| 0x05   | 1      | "Not Loaded" [enemy flags](#enemy-flags)                                                          |
| 0x06   | 1      | "NOT Targetable" [enemy flags](#enemy-flags)                                                      |
| 0x07   | 1      | "Enabled" [enemy flags](#enemy-flags)                                                             |
| 0x08   | 48     | Enemy coordinates, 6 bytes per monster (2 bytes each for X, Y, and Z positions)                   |
| 0x38   | 8      | Enemy IDs (used for [c0mxxx.dat files](../monster-files-c0mxxxdat/)) + 0x10                       |
| 0x40   | 16     | [Unknown 1](#unknowns)                                                                            |
| 0x50   | 16     | [Unknown 2](#unknowns)                                                                            |
| 0x60   | 16     | [Unknown 3](#unknowns)                                                                            |
| 0x70   | 8      | [Unknown 4](#unknowns)                                                                            |
| 0x78   | 8      | [Enemy levels](#enemy-level)                                                                      |

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

## Battle flags

Similarly to [enemy flags](#enemy-flags), it's a byte and each bit determines whether a specific flag is on or off.  

| Flag value | Description                |
|------------|----------------------------|
| 0x01       | Disable Escape             |
| 0x02       | Disable Victory Fanfare    |
| 0x04       | Show Timer                 |
| 0x08       | Disable EXP Gain           |
| 0x10       | Disable Post-Battle Screen |
| 0x20       | Surprise Attack            |
| 0x40       | Back Attack                |
| 0x80       | Scripted Battle            |

## Unknowns

**Unknown 1, 2, and 3** each contain 2 bytes per monster, making them 16 bytes long (8 monsters \* 2 bytes).  
**Unknown 4** contains 1 byte per monster, for a total of 8 bytes.  

The data is laid out sequentially, from _Monster 1_ through _Monster 8_, and each monster has its own set of values, though some values are shared between monsters.  
It appears that the game doesn't read these fields' data, suggesting they may be remnants of a scrapped feature.  

## Enemy level

Each ennemy level is 1 byte.<br>
By default, the ennemy level is determined by the average level of the current team `team level`, and the game adds or substracts `team level / 5`.

- Numbers from 0 to 100 are fixed levels `N +- (N / 5)`. 
- From 101 to 200 are max levels fixed `min(team level +- (team level / 5), N)`
- From 201 to 250 are added values `team level + (N - 200)  +- ((team level + (N - 200)) / 5)`
- 251 is level between 1 to 65, but the game exceptionnaly doesn't divide the result by +-5, it adds or substracts a random value between 0 and 3 `min(team level +- rand(0, 3), 65)`
- 252 is completely random `rand(1, 100)`
- 253 is not used in the game, but the formula is random with a constraint `rand(1, team level +- (team level / 5))`
- 254 is the average team level, period, no division per 5 `team level`
- 255 is the standard formula `team level +- (team level / 5)`

## Notes

Only a maximum of 4 enemies can be loaded at the same time.  
Using a value lower than 0x10 for an enemy ID will crash the game on battle start.  