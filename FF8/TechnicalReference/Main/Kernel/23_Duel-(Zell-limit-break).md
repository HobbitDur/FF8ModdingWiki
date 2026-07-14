---
layout: default
title: Duel (zell limit break)
nav_order: 25
parent: Kernel
permalink: /technical-reference/main/kernel/duel-zell-limit-break/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x48B8 | 10       | 32 bytes     |

## Sections

| Offset | Ability         |
|--------|-----------------|
| 0x48B8 | Punch Rush      |
| 0x48D8 | Booya           |
| 0x48F8 | Heel Drop       |
| 0x4918 | Mach Kick       |
| 0x4938 | Dolphin Blow    |
| 0x4958 | Meteor Strike   |
| 0x4978 | Burning Rave    |
| 0x4998 | Meteor Barret   |
| 0x49B8 | Different Beat  |
| 0x49D8 | My Final Heaven |

## Section Structure

| Offset | Length  | Description                 |
|--------|---------|-----------------------------|
| 0x0000 | 2 bytes | Offset to limit name        |
| 0x0002 | 2 bytes | Offset to limit description |
| 0x0004 | 2 bytes | Magic ID                    |
| 0x0006 | 1 byte  | Attack type                 |
| 0x0007 | 1 byte  | Attack power                |
| 0x0008 | 1 byte  | Target hit animation — the hit/impact animation byte. Duel swaps the flags/animation byte order vs. Magic/Enemy-attack layouts (`Battle_applyDamage`) |
| 0x0009 | 1 byte  | Padding (unused; IDA: 0 xrefs) |
| 0x000A | 1 byte  | Target Info                 |
| 0x000B | 1 bytes | Attack flags — behavior bitfield (low 2 bits also stored as the last-attacker `ATTACK_FLAG`) |
| 0x000C | 1 byte  | Hit count                   |
| 0x000D | 1 byte  | Element Attack              |
| 0x000E | 1 byte  | Element Attack %            |
| 0x000F | 1 byte  | Status attack accuracy       |
| 0x0010 | 2 bytes | Sequence Button 1           |
| 0x0012 | 2 bytes | Sequence Button 2           |
| 0x0014 | 2 bytes | Sequence Button 3           |
| 0x0016 | 2 bytes | Sequence Button 4           |
| 0x0018 | 2 bytes | Sequence Button 5           |
| 0x001A | 2 bytes | [Status 1]({{site.baseurl}}/technical-reference/list/status-flags#status-1) (statuses 0-15)    |
| 0x001C | 4 bytes | [Status 2]({{site.baseurl}}/technical-reference/list/status-flags#status-2) (statuses 16-47)   |

Buttons
is finisher = 0x0001
up = 0x0010
-> = 0x0020
do = 0x0040
<- = 0x0080
L2 = 0x0100
R2 = 0x0200
L1 = 0x0400
R1 = 0x0800
/\ = 0x1000
O = 0x2000
X = 0x4000
|_|= 0x8000
None = 0xFFFF
