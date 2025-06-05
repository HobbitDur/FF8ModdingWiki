---
layout: default
title: Magic
nav_order: 3
parent: Kernel
permalink: /technical-reference/main/kernel/magic/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x021C | 57       | 60 bytes     |

## Sections

| Offset | Magic          |
|--------|----------------|
| 0x021C | Unknown/Dummy? |
| 0x0258 | Fire           |
| 0x0294 | Fira           |
| 0x02D0 | Firaga         |
| 0x030C | Blizzard       |
| 0x0348 | Blizzara       |
| 0x0384 | Blizzaga       |
| 0x03C0 | Thunder        |
| 0x03FC | Thundara       |
| 0x0438 | Thundaga       |
| 0x0474 | Water          |
| 0x04B0 | Aero           |
| 0x04EC | Bio            |
| 0x0528 | Demi           |
| 0x0564 | Holy           |
| 0x05A0 | Flare          |
| 0x05DC | Meteor         |
| 0x0618 | Quake          |
| 0x0654 | Tornado        |
| 0x0690 | Ultima         |
| 0x06CC | Apocalypse     |
| 0x0708 | Cure           |
| 0x0744 | Cura           |
| 0x0780 | Curaga         |
| 0x07BC | Life           |
| 0x07F8 | Full-Life      |
| 0x0834 | Regen          |
| 0x0870 | Esuna          |
| 0x08AC | Dispel         |
| 0x08E8 | Protect        |
| 0x0924 | Shell          |
| 0x0960 | Reflect        |
| 0x099C | Aura           |
| 0x09D8 | Double         |
| 0x0A14 | Triple         |
| 0x0A50 | Haste          |
| 0x0A8C | Slow           |
| 0x0AC8 | Stop           |
| 0x0B04 | Blind          |
| 0x0B40 | Confuse        |
| 0x0B7C | Sleep          |
| 0x0BB8 | Silence        |
| 0x0BF4 | Break          |
| 0x0C30 | Death          |
| 0x0C6C | Drain          |
| 0x0CA8 | Pain           |
| 0x0CE4 | Berserk        |
| 0x0D20 | Float          |
| 0x0D5C | Zombie         |
| 0x0D98 | Meltdown       |
| 0x0DD4 | Scan           |
| 0x0E10 | Full Cure      |
| 0x0E4C | Wall           |
| 0x0E88 | Rapture        |
| 0x0EC4 | Percent        |
| 0x0F00 | Catastrophe    |
| 0x0F3C | The End        |

## Section Structure

| Offset | Length  | Description                                                    |
|--------|---------|----------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to spell name                                           |
| 0x0002 | 2 bytes | Offset to spell description                                    |
| 0x0004 | 2 bytes | Magic ID                                                        |
| 0x0006 | 1 byte  | Animation triggered                                            |
| 0x0007 | 1 byte  | Attack type                                                    |
| 0x0008 | 1 byte  | Spell power (used in damage formula)                           |
| 0x0009 | 1 byte  | Unknown                                                        |
| 0x000A | 1 byte  | [Target info](../../list/kernel/#target-info)                                                 |
| 0x000B | 1 byte  | Attack Flags                                                   |
| 0x000C | 1 byte  | Draw resist (how hard is the magic to draw)                    |
| 0x000D | 1 byte  | Hit count (works with meteor animation, not sure about others) |
| 0x000E | 1 byte  | Element                                                        |
| 0x000F | 1 byte  | Unknown                                                        |
| 0x0010 | 4 bytes | Statuses 1                                                   |
| 0x0014 | 2 bytes | Statuses 0                                                   |
| 0x0016 | 1 byte  | Status attack enabler                                          |
| 0x0017 | 1 byte  | Characters HP junction value                                   |
| 0x0018 | 1 byte  | Characters STR junction value                                  |
| 0x0019 | 1 byte  | Characters VIT junction value                                  |
| 0x001A | 1 byte  | Characters MAG junction value                                  |
| 0x001B | 1 byte  | Characters SPR junction value                                  |
| 0x001C | 1 byte  | Characters SPD junction value                                  |
| 0x001D | 1 byte  | Characters EVA junction value                                  |
| 0x001E | 1 byte  | Characters HIT junction value                                  |
| 0x001F | 1 byte  | Characters LUCK junction value                                 |
| 0x0020 | 1 byte  | Characters J-Elem attack                                      |
| 0x0021 | 1 byte  | Characters J-Elem attack value                                 |
| 0x0022 | 1 byte  | Characters J-Elem defense                                    |
| 0x0023 | 1 byte  | Characters J-Elem defense value                                |
| 0x0024 | 1 byte  | Characters J-Status attack value                               |
| 0x0025 | 1 byte  | Characters J-Status defense value                              |
| 0x0026 | 2 bytes | Characters J-Statuses Attack                                 |
| 0x0028 | 2 bytes | Characters J-Statuses Defend                               |
| 0x002A | 1 byte  | Quezacolt compatibility                                        |
| 0x002B | 1 byte  | Shiva compatibility                                            |
| 0x002C | 1 byte  | Ifrit compatibility                                            |
| 0x002D | 1 byte  | Siren compatibility                                            |
| 0x002E | 1 byte  | Brothers compatibility                                         |
| 0x002F | 1 byte  | Diablos compatibility                                          |
| 0x0030 | 1 byte  | Carbuncle compatibility                                        |
| 0x0031 | 1 byte  | Leviathan compatibility                                        |
| 0x0032 | 1 byte  | Pandemona compatibility                                        |
| 0x0033 | 1 byte  | Cerberus compatibility                                         |
| 0x0034 | 1 byte  | Alexander compatibility                                        |
| 0x0035 | 1 byte  | Doomtrain compatibility                                        |
| 0x0036 | 1 byte  | Bahamut compatibility                                          |
| 0x0037 | 1 byte  | Cactuar compatibility                                          |
| 0x0038 | 1 byte  | Tonberry compatibility                                         |
| 0x0039 | 1 byte  | Eden compatibility                                             |
| 0x003A | 2 bytes | Unknown                                                        |
