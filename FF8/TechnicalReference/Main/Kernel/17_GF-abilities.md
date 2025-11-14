---
layout: default
title: GF abilities
nav_order: 18
parent: Kernel
permalink: /technical-reference/main/kernel/gf-abilities/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4378 | 9        | 8 bytes      |

## Sections

| Offset | Ability    |
|--------|------------|
| 0x4378 | SumMag+10% |
| 0x4380 | SumMag+20% |
| 0x4388 | SumMag+30% |
| 0x4390 | SumMag+40% |
| 0x4398 | GFHP+10%   |
| 0x43A0 | GFHP+20%   |
| 0x43A8 | GFHP+30%   |
| 0x43B0 | GFHP+40%   |
| 0x43B8 | Boost      |

## Section Structure

| Offset | Length  | Description                   |
|--------|---------|-------------------------------|
| 0x0000 | 2 bytes | Offset to ability name        |
| 0x0002 | 2 bytes | Offset to ability description |
| 0x0004 | 1 byte  | AP Required to learn ability  |
| 0x0005 | 1 byte  | Enable Boost                  |
| 0x0006 | 1 byte  | Stat to increase              |
| 0x0007 | 1 byte  | Increase value                |


