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
| 0x0004 | 2 bytes | SpecialAction ID            |
| 0x0006 | 1 byte  | Unknown                     |
| 0x0007 | 1 byte  | Attack Type                 |
| 0x0008 | 2 bytes | Unknown                     |
| 0x000A | 1 byte  | Attack Flags                |
| 0x000B | 1 byte  | Hit Count                   |
| 0x000C | 1 byte  | Element                     |
| 0x000D | 1 byte  | Status Attack               |
| 0x000E | 1 byte  | Crit Bonus                  |
| 0x000F | 1 byte  | Unknown                     |