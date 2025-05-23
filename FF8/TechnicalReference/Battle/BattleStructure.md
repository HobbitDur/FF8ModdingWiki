---
layout: default
parent: Battle
title: Battle encounter data (Scene.out)
author: JeMaCheHi, HobbitDur
permalink: /technical-reference/battle/battle-structure-sceneout/
---

Scene.out contains enemy placement data and flags for each of the game's battle encounters.

See the corresponding thread: <http://forums.qhimm.com/index.php?topic=15816.0>

## File Structure

Scene.out contains no header. It is a raw list of 1024 encounters. Each encounter block consists of 128 bytes and has the following structure:

| Offset | Length | Description                                                                                                                                                                                                                                                                                                               |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x00   | 1      | Battle scenario. The value here corresponds to the number in the a0stg???.x files (into battle.fs file). You have to convert it to hex                                                                                                                                                                                    |
| 0x01   | 1      | [Battle flag 1](#battle-flag-1)                                                                                                                                                                                                                                                                                           |
| 0x02   | 1      | MainCam If you set it to 0xFF camera will always be fixed                                                                                                                                                                                                                                                                 |
| 0x03   | 1      | Sec cam                                                                                                                                                                                                                                                                                                                   |
| 0x04   | 1      | Visible enemies. Shows an enemy for each bit in the byte. (see below for "enemy switches")                                                                                                                                                                                                                                |
| 0x05   | 1      | Loaded enemies. Show the enemies that are been actually fought. Loaded enemies will attack you.                                                                                                                                                                                                                           |
| 0x06   | 1      | Targetable enemies. Show the enemies which will appear in the target window. Careful with this, if you put untargetable enemies battle will never end. (see "enemy switches" too)                                                                                                                                         |
| 0x07   | 1      | Enabled enemies. Also works like eight binary switches. See below                                                                                                                                                                                                                                                         |
| 0x08   | 48     | Enemy coordinates. Its a set of 6x8 bytes which describes each enemy's coordinate in (x,y,z) format. So, first 6 bytes would be enemy 1's coords, next 6 enemy 2's ones, and so on.                                                                                                                                       |
| 0x38   | 8      | Enemies. Each byte represents an enemy. To know what enemy you're working with, you can check the c0m???.dat files in battle.fs. You just have to convert it to hex and add 0x10. Be careful, if you put numbers under 0x10 as enemies, battle will crush.                                                                |
| 0x40   | 16     | unknown                                                                                                                                                                                                                                                                                                                   |
| 0x50   | 16     | Still under research, but this is usually the same as the previous field's value.                                                                                                                                                                                                                                         |
| 0x60   | 16     | unknown                                                                                                                                                                                                                                                                                                                   |
| 0x70   | 8      | unknown                                                                                                                                                                                                                                                                                                                   |
| 0x78   | 8      | [Ennemy level](#ennemy-level) |

## Notes

Each 128block can have up to 8 enemies, but if more than 4 are shown at the same time, the game will crash. This could seem stupid, but it's not. If you think about some battles, like the final battle (where we have 8 enemies), all the monsters are present, but only one or two are shown at any given time. The rest appear through scripting.

Some byte fields are just 8 switches. Here's what I've found:

In 0x01:

In 0x04, 0x05, 0x06, and 0x07

  
+128: 1st enemy relative

+64: 2nd enemy relative

+32: 3rd enemy relative

+16: 4th enemy relative

+8: 5th enemy relative

+4: 6th enemy relative

+2: 7th enemy relative

+1: 8th enemy relative

An important note: If you put an enemy that "summons" another one (Ultimecia summoning Griever, Sphinxara summoning jelleye...) it will summon the enemy from certain slot. This means that if you put that enemy in another battle, it will still summon that slot, because (I think) that summoning is scripted in its AI (in c9m???.dat)


## Battle flag 1

| Flag Value | Description         |
|------------|---------------------|
| 0x01       | No Escape           |
| 0x02       | No Victory          |
| 0x04       | Show Timer          |
| 0x08       | No EXP Gain         |
| 0x10       | No EXP Screen       |
| 0x20       | Surprise Attack     |
| 0x40       | Back Attack         |
| 0x80       | Scripted Battle     |

## Ennemy level

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
