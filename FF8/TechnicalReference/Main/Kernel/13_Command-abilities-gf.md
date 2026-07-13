---
layout: default
title: Command abilities GF
nav_order: 14
parent: Kernel
permalink: /technical-reference/main/kernel/command-abilities-gf/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4180 | 19       | 8 bytes      |

## Sections

| Offset | Ability   |
|--------|-----------|
| 0x4180 | Magic     |
| 0x4188 | GF        |
| 0x4190 | Draw      |
| 0x4198 | Item      |
| 0x41A0 | Empty     |
| 0x41A8 | Card      |
| 0x41B0 | Doom      |
| 0x41B8 | Mad Rush  |
| 0x41C0 | Treatment |
| 0x41C8 | Defend    |
| 0x41D0 | Darkside  |
| 0x41D8 | Recover   |
| 0x41E0 | Absorb    |
| 0x41E8 | Revive    |
| 0x41F0 | LV Down   |
| 0x41F8 | LV Up     |
| 0x4200 | Kamikaze  |
| 0x4208 | Devour    |
| 0x4210 | MiniMog   |

## Section Structure

| Offset | Length  | Description                   |
|--------|---------|-------------------------------|
| 0x0000 | 2 bytes | Offset to ability name        |
| 0x0002 | 2 bytes | Offset to ability description |
| 0x0004 | 1 byte  | AP Required to learn ability  |
| 0x0005 | 1 byte  | Index to Battle commands      |
| 0x0006 | 2 bytes | Padding (unused; IDA: 0 xrefs) |
