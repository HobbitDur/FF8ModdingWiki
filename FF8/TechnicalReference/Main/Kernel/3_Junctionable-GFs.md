---
layout: default
title: Junctionable GFs
nav_order: 4
parent: Kernel
permalink: /technical-reference/main/kernel/junctionable-gfs/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x0F78 | 16       | 132 bytes    |

## Sections

| Offset | G-Force    |
|--------|------------|
| 0x0F78 | Quetzacotl |
| 0x0FFC | Shiva      |
| 0x1080 | Ifrit      |
| 0x1104 | Siren      |
| 0x1188 | Brothers   |
| 0x120C | Diablos    |
| 0x1290 | Carbuncle  |
| 0x1314 | Leviathan  |
| 0x1398 | Pandemona  |
| 0x141C | Cerberus   |
| 0x14A0 | Alexander  |
| 0x1524 | Doomtrain  |
| 0x15A8 | Bahamut    |
| 0x162C | Cactuar    |
| 0x16B0 | Tonberry   |
| 0x1734 | Eden       |

## Section Structure

| Offset | Length  | Description                            |
|--------|---------|----------------------------------------|
| 0x0000 | 2 bytes | Offset to GF attack name               |
| 0x0002 | 2 bytes | Offset to GF attack description        |
| 0x0004 | 2 bytes | [[Magic ID                             |MagicID]] |
| 0x0006 | 1 byte  | Attack type                            |
| 0x0007 | 1 byte  | GF power (used in damage formula)      |
| 0x0008 | 2 bytes | Unknown                                |
| 0x000A | 1 byte  | Attack Flags                           |
| 0x000B | 1 bytes | Unknown                                |
| 0x000B | 1 bytes | Hit count                              |
| 0x000D | 1 byte  | [[Element                              |Elements]] |
| 0x000E | 2 bytes | [[Statuses 0                           |Statuses 0]] |
| 0x0010 | 4 bytes | [[Statuses 1                           |Statuses 1]] |
| 0x0014 | 1 byte  | GF HP Modifier 1(GF_LVLxGF_HP_MODIFIER_1) |
| 0x0015 | 1 byte  | GF HP Modifier 2(10xGF_LVLxGF_LVL/GF_HP_MODIFIER_2) |
| 0x0016 | 1 byte  | GF HP Modifier 3(GF_HP_MODIFIER_3) |
| 0x0017 | 1 bytes | Padding (always 0x00)                                |
| 0x0017 | 1 bytes | GF Next level modifier (10xGF_LVLxGF_LVL_MODIFIER_1)                               |
| 0x0017 | 1 bytes | GF Next level modifier (GF_LVLxGF_LVLxGF_LVL_MODIFIER_2/256)                                     |
| 0x001B | 1 byte  | Status attack enabler                  |
| 0x001C | 1 byte  | [[Ability 1 Unlocker                   |Junctionable Abilities Unlocker]] |
| 0x001D | 1 byte  | Unknown                                |
| 0x001E | 1 byte  | [[Ability 1                            |Junctionable-Abilities]] |
| 0x001F | 1 byte  | Unknown                                |
| 0x0020 | 1 byte  | [[Ability 2 Unlocker                   |Junctionable Abilities Unlocker]]  |
| 0x0021 | 1 byte  | Unknown                                |
| 0x0022 | 1 byte  | [[Ability 2                            |Junctionable-Abilities]]  |
| 0x0023 | 1 byte  | Unknown                                |
| 0x0024 | 1 byte  | [[Ability 3 Unlocker                   |Junctionable Abilities Unlocker]]  |
| 0x0025 | 1 byte  | Unknown                                |
| 0x0026 | 1 byte  | [[Ability 3                            |Junctionable-Abilities]]  |
| 0x0027 | 1 byte  | Unknown                                |
| 0x0028 | 1 byte  | [[Ability 4 Unlocker                   |Junctionable Abilities Unlocker]]  |
| 0x0029 | 1 byte  | Unknown                                |
| 0x002A | 1 byte  | [[Ability 4                            |Junctionable-Abilities]]  |
| 0x002B | 1 byte  | Unknown                                |
| 0x002C | 1 byte  | [[Ability 5 Unlocker                   |Junctionable Abilities Unlocker]]  |
| 0x002D | 1 byte  | Unknown                                |
| 0x002E | 1 byte  | [[Ability 5                            |Junctionable-Abilities]] |
| 0x002F | 1 byte  | Unknown                                |
| 0x0030 | 1 byte  | [[Ability 6 Unlocker                   |Junctionable Abilities Unlocker]]  |
| 0x0031 | 1 byte  | Unknown                                |
| 0x0032 | 1 byte  | [[Ability 6                            |Junctionable-Abilities]] |
| 0x0033 | 1 byte  | Unknown                                |
| 0x0034 | 1 byte  | [[Ability 7 Unlocker                   |Junctionable Abilities Unlocker]] |
| 0x0035 | 1 byte  | Unknown                                |
| 0x0036 | 1 byte  | [[Ability 7                            |Junctionable-Abilities]] |
| 0x0037 | 1 byte  | Unknown                                |
| 0x0038 | 1 byte  | [[Ability 8 Unlocker                   |Junctionable Abilities Unlocker]]  |
| 0x0039 | 1 byte  | Unknown                                |
| 0x003A | 1 byte  | [[Ability 8                            |Junctionable-Abilities]] |
| 0x003B | 1 byte  | Unknown                                |
| 0x003C | 1 byte  | [[Ability 9 Unlocker                   |Junctionable Abilities Unlocker]]  |
| 0x003D | 1 byte  | Unknown                                |
| 0x003E | 1 byte  | [[Ability 9                            |Junctionable-Abilities]] |
| 0x003F | 1 byte  | Unknown                                |
| 0x0040 | 1 byte  | [[Ability 10 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x0041 | 1 byte  | Unknown                                |
| 0x0042 | 1 byte  | [[Ability 10                           |Junctionable-Abilities]] |
| 0x0043 | 1 byte  | Unknown                                |
| 0x0044 | 1 byte  | [[Ability 11 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x0045 | 1 byte  | Unknown                                |
| 0x0046 | 1 byte  | [[Ability 11                           |Junctionable-Abilities]] |
| 0x0047 | 1 byte  | Unknown                                |
| 0x0048 | 1 byte  | [[Ability 12 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x0049 | 1 byte  | Unknown                                |
| 0x004A | 1 byte  | [[Ability 12                           |Junctionable-Abilities]] |
| 0x004B | 1 byte  | Unknown                                |
| 0x004C | 1 byte  | [[Ability 13 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x004D | 1 byte  | Unknown                                |
| 0x004E | 1 byte  | [[Ability 13                           |Junctionable-Abilities]]  |
| 0x004F | 1 byte  | Unknown                                |
| 0x0050 | 1 byte  | [[Ability 14 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x0051 | 1 byte  | Unknown                                |
| 0x0052 | 1 byte  | [[Ability 14                           |Junctionable-Abilities]]  |
| 0x0053 | 1 byte  | Unknown                                |
| 0x0054 | 1 byte  | [[Ability 15 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x0055 | 1 byte  | Unknown                                |
| 0x0056 | 1 byte  | [[Ability 15                           |Junctionable-Abilities]] |
| 0x0057 | 1 byte  | Unknown                                |
| 0x0058 | 1 byte  | [[Ability 16 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x0059 | 1 byte  | Unknown                                |
| 0x005A | 1 byte  | [[Ability 16                           |Junctionable-Abilities]] |
| 0x005B | 1 byte  | Unknown                                |
| 0x005C | 1 byte  | [[Ability 17 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x005D | 1 byte  | Unknown                                |
| 0x005E | 1 byte  | [[Ability 17                           |Junctionable-Abilities]] |
| 0x005F | 1 byte  | Unknown                                |
| 0x0060 | 1 byte  | [[Ability 18 Unlocker                  |Junctionable Abilities Unlocker]] |
| 0x0061 | 1 byte  | Unknown                                |
| 0x0062 | 1 byte  | [[Ability 18                           |Junctionable-Abilities]] |
| 0x0063 | 1 byte  | Unknown                                |
| 0x0064 | 1 byte  | [[Ability 19 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x0065 | 1 byte  | Unknown                                |
| 0x0066 | 1 byte  | [[Ability 19                           |Junctionable-Abilities]] |
| 0x0067 | 1 byte  | Unknown                                |
| 0x0068 | 1 byte  | [[Ability 20 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x0069 | 1 byte  | Unknown                                |
| 0x006A | 1 byte  | [[Ability 20                           |Junctionable-Abilities]] |
| 0x006B | 1 byte  | Unknown                                |
| 0x006C | 1 byte  | [[Ability 21 Unlocker                  |Junctionable Abilities Unlocker]]  |
| 0x006D | 1 byte  | Unknown                                |
| 0x006E | 1 byte  | [[Ability 21                           |Junctionable-Abilities]] |
| 0x006F | 1 byte  | Unknown                                |
| 0x0070 | 1 byte  | Quezacolt compatibility                |
| 0x0071 | 1 byte  | Shiva compatibility                    |
| 0x0072 | 1 byte  | Ifrit compatibility                    |
| 0x0073 | 1 byte  | Siren compatibility                    |
| 0x0074 | 1 byte  | Brothers compatibility                 |
| 0x0075 | 1 byte  | Diablos compatibility                  |
| 0x0076 | 1 byte  | Carbuncle compatibility                |
| 0x0077 | 1 byte  | Leviathan compatibility                |
| 0x0078 | 1 byte  | Pandemona compatibility                |
| 0x0079 | 1 byte  | Cerberus compatibility                 |
| 0x007A | 1 byte  | Alexander compatibility                |
| 0x007B | 1 byte  | Doomtrain compatibility                |
| 0x007C | 1 byte  | Bahamut compatibility                  |
| 0x007D | 1 byte  | Cactuar compatibility                  |
| 0x007E | 1 byte  | Tonberry compatibility                 |
| 0x007F | 1 byte  | Eden compatibility                     |
| 0x0080 | 2 bytes | Unknown                                |
| 0x0082 | 1 byte  | Power Mod (used in damage formula)     |
| 0x0083 | 1 byte  | Level Mod (used in damage formula)     |



