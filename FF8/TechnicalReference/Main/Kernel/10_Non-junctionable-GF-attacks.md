---
layout: default
title: Non junctionable GF attacks
nav_order: 11
parent: Kernel
permalink: /technical-reference/main/kernel/non-junctionable-gf-attacks/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x3EE0 | 16       | 20 bytes     |

## Sections

| Offset | Attack          |
|--------|-----------------|
| 0x3EE0 | Zantetsuken (O) |
| 0x3EF4 | Rebirth Flame   |
| 0x3F08 | ChocoFire       |
| 0x3F1C | ChocoFlare      |
| 0x3F30 | ChocoMeteor     |
| 0x3F44 | ChocoBocle      |
| 0x3F58 | Moogle Dance    |
| 0x3F6C | Excaliber       |
| 0x3F80 | Excalipoor      |
| 0x3F94 | Masamune        |
| 0x3FA8 | Zantetsuken (G) |
| 0x3FBC | Angelo Rush     |
| 0x3FD0 | Angelo Recover  |
| 0x3FE4 | Angelo Reverse  |
| 0x3FF8 | Angelo Search   |
| 0x400C | Friendship      |

## Section Structure

| Offset | Length  | Description                                                                                                                                                                                  |
|--------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to GF attack name                                                                                                                                                                     |
| 0x0002 | 2 bytes | special Action ID (decides what animation to play)                                                                                                                                                    |
| 0x0004 | 1 byte  | Attack type                                                                                                                                                                                  |
| 0x0005 | 1 byte  | GF power (used in damage formula)                                                                                                                                                            |
| 0x0006 | 1 byte  | Status attack enabler                                                                                                                                                                        |
| 0x0007 | 1 byte  | Unknown                                                                                                                                                                                      |
| 0x0008 | 1 byte  | Status flags                                                                                                                                                                                 |
| 0x0009 | 1 byte | Unknown                                                                                                                                                                                  |
| 0x0009 | 1 byte | Hit Count                                                                                                                                                                                      |
| 0x000B | 1 byte  | Element<br/><br/> *0x00 - Non-Elemental<br/> 0x01 - Fire<br/> 0x02 - Ice<br/> 0x04 - Thunder<br/> 0x08 - Earth<br/> 0x10 - Poison<br/> 0x20 - Wind<br/> 0x40 - Water<br/> 0x80 - Holy*       |
| 0x000C | 1 byte  | Status 1<br/><br/> *0x00 - None<br/> 0x01 - Sleep<br/> 0x02 - Haste<br/> 0x04 - Slow<br/> 0x08 - Stop<br/> 0x10 - Regen<br/> 0x20 - Protect<br/> 0x40 - Shell<br/> 0x80 - Reflect*           |
| 0x000D | 1 byte  | Status 2<br/><br/> *0x00 - None<br/> 0x01 - Aura<br/> 0x02 - Curse<br/> 0x04 - Doom<br/> 0x08 - Invincible<br/> 0x10 - Petrifying<br/> 0x20 - Float<br/> 0x40 - Confusion<br/> 0x80 - Drain* |
| 0x000E | 1 byte  | Status 3<br/><br/> *0x00 - None<br/> 0x01 - Eject<br/> 0x02 - Double<br/> 0x04 - Triple<br/> 0x08 - Defend<br/> 0x10 - ???<br/> 0x20 - ???<br/> 0x40 - ???<br/> 0x80 - ???*                  |
| 0x000F | 1 byte  | Status 4<br/><br/> *0x00 - None<br/> 0x01 - Vit0<br/> 0x02 - ???<br/> 0x04 - ???<br/> 0x08 - ???<br/> 0x10 - ???<br/> 0x20 - ???<br/> 0x40 - ???<br/> 0x80 - ???*                            |
| 0x0010 | 1 byte  | Status 5<br/><br/> *0x00 - None<br/> 0x01 - Death<br/> 0x02 - Poison<br/> 0x04 - Petrify<br/> 0x08 - Darkness<br/> 0x10 - Silence<br/> 0x20 - Berserk<br/> 0x40 - Zombie<br/> 0x80 - ???*    |
| 0x0011 | 1 byte  | Unknown                                                                                                                                                                                      |
| 0x0012 | 1 byte  | Power Mod (used in damage formula)                                                                                                                                                           |
| 0x0013 | 1 byte  | Level Mod (used in damage formula)                                                                                                                                                           |
