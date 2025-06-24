---
layout: default
title: Battle items
nav_order: 9
parent: Kernel
permalink: /technical-reference/main/kernel/battle-items/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x3930 | 33       | 24 bytes     |

## Sections

| Offset | Ability        |
|--------|----------------|
| 0x3930 | Dummy/Unused   |
| 0x3948 | Potion         |
| 0x3960 | Potion+        |
| 0x3978 | Hi-Potion      |
| 0x3990 | Hi-Potion+     |
| 0x39A8 | X-Potion       |
| 0x39C0 | Mega-Potion    |
| 0x39D8 | Phoenix Down   |
| 0x39F0 | Mega Phoenix   |
| 0x3A08 | Elixir         |
| 0x3A20 | Megalixir      |
| 0x3A38 | Antidote       |
| 0x3A50 | Soft           |
| 0x3A68 | Eye Drops      |
| 0x3A80 | Echo Screen    |
| 0x3A98 | Holy Water     |
| 0x3AB0 | Remedy         |
| 0x3AC8 | Remedy+        |
| 0x3AE0 | Hero-trial     |
| 0x3AF8 | Hero           |
| 0x3B10 | Holy War-trial |
| 0x3B28 | Holy War       |
| 0x3B40 | Shell Stone    |
| 0x3B58 | Protect Stone  |
| 0x3B70 | Aura Stone     |
| 0x3B88 | Death Stone    |
| 0x3BA0 | Holy Stone     |
| 0x3BB8 | Flare Stone    |
| 0x3BD0 | Meteor Stone   |
| 0x3BE8 | Ultima Stone   |
| 0x3C00 | Gysahl Greens  |
| 0x3C18 | Phoenix Pinion |
| 0x3C30 | Friendship     |

## Section Structure

| Offset | Length  | Description                 |
|--------|---------|-----------------------------|
| 0x0000 | 2 bytes | Offset to item  name        |
| 0x0002 | 2 bytes | Offset to item  description |
| 0x0004 | 2 bytes | Magic ID                    |
| 0x0006 | 1 byte  | Attack type                 |
| 0x0007 | 1 byte  | Attack power                |
| 0x0008 | 1 byte  | Battle flag                 |
| 0x0009 | 1 byte  | Target info                 |
| 0x000A | 1 byte  | Unknown                     |
| 0x000B | 1 byte  | Attack flags                |
| 0x000C | 1 bytes | Unknown                     |
| 0x000D | 1 byte  | Status Attack Enabler       |
| 0x000E | 2 bytes | status_0; //statuses 0-7    |
| 0x0010 | 4 bytes | status_1; //statuses 8-39   |
| 0x0014 | 1 byte  | Attack Param                |
| 0x0015 | 1 byte  | Unknown                     |
| 0x0016 | 1 bytes | Hit Count                   |
| 0x0017 | 1 bytes | Element                     |
