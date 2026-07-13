---
layout: default
title: Command abilities in battle
nav_order: 12
parent: Kernel
permalink: /technical-reference/main/kernel/command-abilities-in-battle/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4020 | 12       | 16 bytes     |

## Sections

| Offset | Ability   |
|--------|-----------|
| 0x4020 | Recover   |
| 0x4030 | Revive    |
| 0x4040 | Treatment |
| 0x4050 | Mad Rush  |
| 0x4060 | Doom      |
| 0x4070 | Absorb    |
| 0x4080 | LV Down   |
| 0x4090 | LV Up     |
| 0x40A0 | Kamikaze  |
| 0x40B0 | Devour    |
| 0x40C0 | Card      |
| 0x40D0 | Defend    |

## Section Structure

| Offset | Length  | Description           |
|--------|---------|-----------------------|
| 0x0000 | 2 bytes | Magic ID              |
| 0x0002 | 1 bytes | Padding (unused; IDA: 0 xrefs) |
| 0x0003 | 1 bytes | Animation triggered   |
| 0x0004 | 1 byte  | Attack type           |
| 0x0005 | 1 byte  | Attack power          |
| 0x0006 | 1 byte  | Attack flags          |
| 0x0007 | 1 byte  | Hit Count             |
| 0x0008 | 1 byte  | Element               |
| 0x0009 | 1 byte  | Status attack enabler |
| 0x000A | 2 bytes | Status1               |
| 0x000C | 4 bytes | Status2               |
