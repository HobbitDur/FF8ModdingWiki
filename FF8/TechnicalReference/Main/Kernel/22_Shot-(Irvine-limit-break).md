---
layout: default
title: Shot (irvine limit breaks)
nav_order: 23
parent: Kernel
permalink: /technical-reference/main/kernel/shot-irvine-limit-breaks/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x47F8 | 8        | 24 bytes     |

## Sections

| Offset | Ability       |
|--------|---------------|
| 0x47F8 | Normal Shot   |
| 0x4810 | Scatter Shot  |
| 0x4828 | Dark Shot     |
| 0x4840 | Flame Shot    |
| 0x4858 | Canister Shot |
| 0x4870 | Quick Shot    |
| 0x4888 | Armor Shot    |
| 0x48A0 | Hyper Shot    |

## Section Structure

| Offset | Length  | Description                 |
|--------|---------|-----------------------------|
| 0x0000 | 2 bytes | Offset to limit name        |
| 0x0002 | 2 bytes | Offset to limit description |
| 0x0004 | 2 bytes | Magic ID                    |
| 0x0006 | 1 byte  | Attack Type                 |
| 0x0007 | 1 byte  | Attack Power                |
| 0x0008 | 2 bytes | Target hit/reaction animation ID (`HIT_TYPE_TARGET_ANIMATION_TO_PLAY`) played on the target when the ability lands |
| 0x000A | 1 byte  | Target Info                 |
| 0x000B | 1 byte  | Attack Flags                |
| 0x000C | 1 byte  | Hit Count                   |
| 0x000D | 1 byte  | Element Attack              |
| 0x000E | 1 byte  | Element Attack %            |
| 0x000F | 1 byte  | Status Attack Enabler       |
| 0x0010 | 2 bytes | status_0; //statuses 0-7    |
| 0x0012 | 1 byte  | Used item index             |
| 0x0013 | 1 byte  | Crit increase               |
| 0x0014 | 4 bytes | status_1; //statuses 8-39   |
