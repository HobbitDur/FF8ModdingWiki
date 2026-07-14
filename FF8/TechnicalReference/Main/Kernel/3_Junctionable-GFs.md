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

| Offset | Length  | Description                                                                                      |
|--------|---------|--------------------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to GF attack name                                                                         |
| 0x0002 | 2 bytes | Offset to GF attack description                                                                  |
| 0x0004 | 2 bytes | Attack animation — id of the effect / animation dispatched at runtime (the engine "special action")  |
| 0x0006 | 1 byte  | Attack type                                                                                      |
| 0x0007 | 1 byte  | GF power (used in damage formula)                                                                |
| 0x0008 | 1 byte  | [Status window flags]({{site.baseurl}}/technical-reference/list/battle/#status-window-flags) — all 16 GFs use `0x80` (ally status panel hidden while targeting) |
| 0x0009 | 1 byte  | Target info — target mask for the GF attack, via `getTargetMaskFromInfo` |                                                                                       
| 0x000A | 1 byte  | Attack Flags                                                                                     |
| 0x000B | 1 bytes | HIT_TYPE_TARGET_ANIMATION_TO_PLAY                                                                |
| 0x000C | 1 bytes | Hit count                                                                                        |
| 0x000D | 1 byte  | [Element]({{site.baseurl}}/technical-reference/list/magic-list#element)                          |
| 0x000E | 2 bytes | [Status1]({{site.baseurl}}/technical-reference/list/status-flags#status-1)                       |
| 0x0010 | 4 bytes | [Status2]({{site.baseurl}}/technical-reference/list/status-flags#status-2)                       |
| 0x0014 | 1 byte  | GF HP Modifier 1(GF_LVLxGF_HP_MODIFIER_1)                                                        |
| 0x0015 | 1 byte  | GF HP Modifier 2(10xGF_LVLxGF_LVL/GF_HP_MODIFIER_2)                                              |
| 0x0016 | 1 byte  | GF HP Modifier 3(GF_HP_MODIFIER_3)                                                               |
| 0x0017 | 1 bytes | Padding (always 0x00)                                                                            |
| 0x0018 | 1 bytes | GF Next level modifier 1(10xGF_LVLxGF_LVL_MODIFIER_1)                                            |
| 0x0019 | 1 bytes | GF Next level modifier 2(GF_LVLxGF_LVLxGF_LVL_MODIFIER_2/256)                                    |
| 0x001A | 1 byte  | Status attack accuracy — **unused** (dead byte). Deep-audited in IDA: 0 field xrefs, 0 direct-address xrefs, and all *register-relative* accesses checked too (the base-pointer case that hides menu reads) — the only 3 functions holding a GF-entry pointer (`getAddressGfAttackName`, `GFAbilityLearnComplete`, the ~15 KB GF/junction menu `sub_4F81F0`) read only offset 0 or 0x1B, never 0x1A; no aliases or bulk copies read it either. The GF summon's real status-attack accuracy is the next byte, 0x1B |
| 0x001B | 1 byte  | **GF summon status-attack accuracy** — structurally the first ability slot's byte+0 (`abilityData[0].abilityUnlocker`), but `Battle_applyDamage`'s GF case reads it as `HIT_ATTACK_ACCURACY` for the summon's status roll (the dedicated 0x1A byte above is dead). `0` = the summon inflicts no status (e.g. Ifrit). `BuildGFAbilityList` never reads this byte for ability learning |
| 0x001C | 1 byte  | Ability 1 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x001D | 1 byte  | Ability 1 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x001E | 1 byte  | [Ability 1]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x001F | 1 byte  | Ability 2 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 2 level/prereq'). Always `0` in retail |
| 0x0020 | 1 byte  | Ability 2 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0021 | 1 byte  | Ability 2 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0022 | 1 byte  | [Ability 2]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0023 | 1 byte  | Ability 3 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 3 level/prereq'). Always `0` in retail |
| 0x0024 | 1 byte  | Ability 3 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0025 | 1 byte  | Ability 3 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0026 | 1 byte  | [Ability 3]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0027 | 1 byte  | Ability 4 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 4 level/prereq'). Always `0` in retail |
| 0x0028 | 1 byte  | Ability 4 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0029 | 1 byte  | Ability 4 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x002A | 1 byte  | [Ability 4]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x002B | 1 byte  | Ability 5 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 5 level/prereq'). Always `0` in retail |
| 0x002C | 1 byte  | Ability 5 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x002D | 1 byte  | Ability 5 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x002E | 1 byte  | [Ability 5]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x002F | 1 byte  | Ability 6 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 6 level/prereq'). Always `0` in retail |
| 0x0030 | 1 byte  | Ability 6 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0031 | 1 byte  | Ability 6 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0032 | 1 byte  | [Ability 6]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0033 | 1 byte  | Ability 7 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 7 level/prereq'). Always `0` in retail |
| 0x0034 | 1 byte  | Ability 7 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0035 | 1 byte  | Ability 7 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0036 | 1 byte  | [Ability 7]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0037 | 1 byte  | Ability 8 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 8 level/prereq'). Always `0` in retail |
| 0x0038 | 1 byte  | Ability 8 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0039 | 1 byte  | Ability 8 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x003A | 1 byte  | [Ability 8]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x003B | 1 byte  | Ability 9 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 9 level/prereq'). Always `0` in retail |
| 0x003C | 1 byte  | Ability 9 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x003D | 1 byte  | Ability 9 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x003E | 1 byte  | [Ability 9]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x003F | 1 byte  | Ability 10 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 10 level/prereq'). Always `0` in retail |
| 0x0040 | 1 byte  | Ability 10 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0041 | 1 byte  | Ability 10 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0042 | 1 byte  | [Ability 10]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0043 | 1 byte  | Ability 11 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 11 level/prereq'). Always `0` in retail |
| 0x0044 | 1 byte  | Ability 11 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0045 | 1 byte  | Ability 11 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0046 | 1 byte  | [Ability 11]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0047 | 1 byte  | Ability 12 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 12 level/prereq'). Always `0` in retail |
| 0x0048 | 1 byte  | Ability 12 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0049 | 1 byte  | Ability 12 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x004A | 1 byte  | [Ability 12]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x004B | 1 byte  | Ability 13 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 13 level/prereq'). Always `0` in retail |
| 0x004C | 1 byte  | Ability 13 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x004D | 1 byte  | Ability 13 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x004E | 1 byte  | [Ability 13]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x004F | 1 byte  | Ability 14 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 14 level/prereq'). Always `0` in retail |
| 0x0050 | 1 byte  | Ability 14 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0051 | 1 byte  | Ability 14 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0052 | 1 byte  | [Ability 14]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0053 | 1 byte  | Ability 15 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 15 level/prereq'). Always `0` in retail |
| 0x0054 | 1 byte  | Ability 15 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0055 | 1 byte  | Ability 15 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0056 | 1 byte  | [Ability 15]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0057 | 1 byte  | Ability 16 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 16 level/prereq'). Always `0` in retail |
| 0x0058 | 1 byte  | Ability 16 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0059 | 1 byte  | Ability 16 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x005A | 1 byte  | [Ability 16]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x005B | 1 byte  | Ability 17 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 17 level/prereq'). Always `0` in retail |
| 0x005C | 1 byte  | Ability 17 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x005D | 1 byte  | Ability 17 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x005E | 1 byte  | [Ability 17]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x005F | 1 byte  | Ability 18 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 18 level/prereq'). Always `0` in retail |
| 0x0060 | 1 byte  | Ability 18 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0061 | 1 byte  | Ability 18 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0062 | 1 byte  | [Ability 18]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0063 | 1 byte  | Ability 19 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 19 level/prereq'). Always `0` in retail |
| 0x0064 | 1 byte  | Ability 19 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0065 | 1 byte  | Ability 19 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x0066 | 1 byte  | [Ability 19]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x0067 | 1 byte  | Ability 20 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 20 level/prereq'). Always `0` in retail |
| 0x0068 | 1 byte  | Ability 20 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x0069 | 1 byte  | Ability 20 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x006A | 1 byte  | [Ability 20]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x006B | 1 byte  | Ability 21 — **unused** (byte+0 of the ability slot); `BuildGFAbilityList` never reads it (real unlock = the next byte, 'Ability 21 level/prereq'). Always `0` in retail |
| 0x006C | 1 byte  | Ability 21 level/prereq — 1-100 = the GF must be at least this level; 101-121 = instead of a level, ability slot (value-101) on this same GF must already be fully learned first (a same-GF unlock chain), via `BuildGFAbilityList` |
| 0x006D | 1 byte  | Ability 21 alt prereq slot — points at another ability slot (0-20) on this GF and makes the two mutually exclusive until one is done: this ability keeps being offered only while the other slot's ability is still unfinished, and gets cut off once that other ability is completed. `0xFF` = no such restriction (always `0xFF` in retail - a working `BuildGFAbilityList` feature the shipped data never uses) |
| 0x006E | 1 byte  | [Ability 21]({{site.baseurl}}/technical-reference/list/junctionable-abilities) |
| 0x006F | 1 byte  | Padding                                                                                          |
| 0x0070 | 1 byte  | Quezacolt compatibility                                                                          |
| 0x0071 | 1 byte  | Shiva compatibility                                                                              |
| 0x0072 | 1 byte  | Ifrit compatibility                                                                              |
| 0x0073 | 1 byte  | Siren compatibility                                                                              |
| 0x0074 | 1 byte  | Brothers compatibility                                                                           |
| 0x0075 | 1 byte  | Diablos compatibility                                                                            |
| 0x0076 | 1 byte  | Carbuncle compatibility                                                                          |
| 0x0077 | 1 byte  | Leviathan compatibility                                                                          |
| 0x0078 | 1 byte  | Pandemona compatibility                                                                          |
| 0x0079 | 1 byte  | Cerberus compatibility                                                                           |
| 0x007A | 1 byte  | Alexander compatibility                                                                          |
| 0x007B | 1 byte  | Doomtrain compatibility                                                                          |
| 0x007C | 1 byte  | Bahamut compatibility                                                                            |
| 0x007D | 1 byte  | Cactuar compatibility                                                                            |
| 0x007E | 1 byte  | Tonberry compatibility                                                                           |
| 0x007F | 1 byte  | Eden compatibility                                                                               |
| 0x0080 | 2 bytes | GF Boost timing params — **not** a min/max. Low byte ×15 = initial length (ticks) of the first "safe" Boost phase (press □ to raise Boost); high byte ×15 = initial length of the overall input window (`pre_computeGFBoost`/`computeGFBoost`). The Boost value itself runs 75–250 (100 if untouched); damage = damage × Boost/100. Later phases re-roll to `15×(1..3 + 1..3)` |
| 0x0082 | 1 byte  | Power Mod (used in damage formula)                                                               |
| 0x0083 | 1 byte  | Level Mod (used in damage formula)                                                               |

### GF compatibility block (0x70–0x7F)

The 16 compatibility bytes are **not** a GF-vs-GF matrix. They are a *per-summon delta table*:
when **this** GF is summoned in battle, each byte is how much the casting character's stored
compatibility with the corresponding GF (Quezacotl … Eden) changes. `BattleAction_ExecuteCommand`
applies `SG_ARRAY_CHARA_DATA[char].GFCompatibility[gf] += byte − 100` for every GF the player owns
(player slots 0–2 only), so **100 = no change**, **>100 raises** and **<100 lowers** compatibility;
the running total is clamped to **[1000, 6000]**. Casting a spell does the same via the identical
block in the [Magic]({{site.baseurl}}/technical-reference/main/kernel/magic/) section. Higher stored
compatibility fills that GF's summon (Boost) gauge faster — `gf_atb += 4 × (battleSpeed+1) × compat / 35`
in `computeCommandAction` — so the GF appears sooner.



