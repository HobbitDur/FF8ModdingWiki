---
layout: default
title: Junction abilities
nav_order: 13
parent: Kernel
permalink: /technical-reference/main/kernel/junction-abilities/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x40E0 | 20       | 8 bytes      |

## Sections

| Offset | Ability      |
|--------|--------------|
| 0x40E0 | Dummy/Unused |
| 0x40E8 | HP-J         |
| 0x40F0 | Str-J        |
| 0x40F8 | Vit-J        |
| 0x4100 | Mag-J        |
| 0x4108 | Spr-J        |
| 0x4110 | Spd-J        |
| 0x4118 | Eva-J        |
| 0x4120 | Hit-J        |
| 0x4128 | Luck-J       |
| 0x4130 | Elem-Atk-J   |
| 0x4138 | ST-Atk-J     |
| 0x4140 | Elem-Def-J   |
| 0x4148 | ST-Def-J     |
| 0x4150 | Elem-Defx2   |
| 0x4158 | Elem-Defx4   |
| 0x4160 | ST-Def-Jx2   |
| 0x4168 | ST-Def-Jx4   |
| 0x4170 | Abilityx3    |
| 0x4178 | Abilityx4    |

## Section Structure

| Offset | Length  | Description                                                                                                                                        |
|--------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to ability name                                                                                                                             |
| 0x0002 | 2 bytes | Offset to ability description                                                                                                                      |
| 0x0004 | 1 byte  | AP Required to learn ability                                                                                                                       |
| 0x0005 | 3 byte  | The [junction ability flag]({{site.baseurl}}/technical-reference/list/ability-list#junction-abilities) that define the flag value for this ability |
