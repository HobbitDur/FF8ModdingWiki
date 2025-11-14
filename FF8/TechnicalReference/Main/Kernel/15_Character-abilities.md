---
layout: default
title: Characters abilities
nav_order: 16
parent: Kernel
permalink: /technical-reference/main/kernel/characters-abilities/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x42B0 | 20       | 8 bytes      |

## Sections

| Offset | Ability       |
|--------|---------------|
| 0x42B0 | Mug           |
| 0x42B8 | Med Data      |
| 0x42C0 | Counter       |
| 0x42C8 | Return Damage |
| 0x42D0 | Cover         |
| 0x42D8 | Initiative    |
| 0x42E0 | Move-HP Up    |
| 0x42E8 | HP Bonus      |
| 0x42F0 | Str Bonus     |
| 0x42F8 | Vit Bonus     |
| 0x4300 | Mag Bonus     |
| 0x4308 | Spr Bonus     |
| 0x4310 | Auto-Protect  |
| 0x4318 | Auto-Shell    |
| 0x4320 | Auto-Reflect  |
| 0x4328 | Auto-Haste    |
| 0x4330 | Auto-Potion   |
| 0x4338 | Expendx2-1    |
| 0x4340 | Expendx3-1    |
| 0x4348 | Ribbon        |

## Section Structure

| Offset | Length  | Description                                                                                                                                    |
|--------|---------|------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to ability name                                                                                                                         |
| 0x0002 | 2 bytes | Offset to ability description                                                                                                                  |
| 0x0004 | 1 byte  | AP Required to learn ability                                                                                                                   |
| 0x0005 | 3 byte  | The [Chara abilities flag]({{site.baseurl}}/technical-reference/list/ability-list#chara-abilities) that define the flag value for this ability |