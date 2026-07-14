---
layout: default
title: Blue magic
nav_order: 21
parent: Kernel
permalink: /technical-reference/main/kernel/blue-magic/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x44F8 | 16       | 16 bytes     |

## Sections

| Offset | Ability          |
|--------|------------------|
| 0x44F8 | Laser Eye        |
| 0x4508 | Ultra Waves      |
| 0x4518 | Electrocute      |
| 0x4528 | LV?Death         |
| 0x4538 | Degenerator      |
| 0x4548 | Aqua Breath      |
| 0x4558 | Micro Missiles   |
| 0x4568 | Acid             |
| 0x4578 | Gatling Gun      |
| 0x4588 | Fire Breath      |
| 0x4598 | Bad Breath       |
| 0x45A8 | White Wind       |
| 0x45B8 | Homing Laser     |
| 0x45C8 | Mighty Guard     |
| 0x45D8 | Ray-Bomb         |
| 0x45E8 | Shockwave Pulsar |

## Section Structure

| Offset | Length  | Description                 |
|--------|---------|-----------------------------|
| 0x0000 | 2 bytes | Offset to limit name        |
| 0x0002 | 2 bytes | Offset to limit description |
| 0x0004 | 2 bytes | Attack animation — id of the effect / animation played (the engine "special action") |
| 0x0006 | 1 byte  | Target hit/reaction animation ID (`HIT_TYPE_TARGET_ANIMATION_TO_PLAY`) played on the target when the ability lands |
| 0x0007 | 1 byte  | Attack Type                 |
| 0x0008 | 1 byte  | [Status window flags]({{site.baseurl}}/technical-reference/list/battle/#status-window-flags) — all 16 blue magics use `0x80` (ally status panel hidden while targeting). `BuildLimitCommandMenu` copies it into the Blue Magic list entry's status-window slot |
| 0x0009 | 1 byte  | [TargetInfo]({{site.baseurl}}/technical-reference/list/kernel#target-info) — NOT padding: `BuildLimitCommandMenu` copies it into the list entry's target slot. Retail: `0x40`/`0x50` for the offensive blue magics, `0x00` for the ally-support ones (White Wind, Mighty Guard) |
| 0x000A | 1 byte  | Attack Flags                |
| 0x000B | 1 byte  | Hit Count                   |
| 0x000C | 1 byte  | Element                     |
| 0x000D | 1 byte  | Status attack accuracy — chance to inflict the attached statuses (0 = never; the status flags themselves are in [Quistis limit-break parameters](../quistis-limit-break-parameters/), per crisis level) |
| 0x000E | 1 byte  | Crit Bonus                  |
| 0x000F | 1 byte  | Padding (unused; IDA: 0 xrefs) |
