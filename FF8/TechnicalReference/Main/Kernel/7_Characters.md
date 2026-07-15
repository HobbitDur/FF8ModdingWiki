---
layout: default
title: Characters
nav_order: 8
parent: Kernel
permalink: /technical-reference/main/kernel/characters/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x37A4 | 11       | 36 bytes     |

## Sections

| Offset | Character |
|--------|-----------|
| 0x37A4 | Squall    |
| 0x37C8 | Zell      |
| 0x37EC | Irvine    |
| 0x3810 | Quistis   |
| 0x3834 | Rinoa     |
| 0x3858 | Selphie   |
| 0x387C | Seifer    |
| 0x38A0 | Edea      |
| 0x38C4 | Laguna    |
| 0x38E8 | Kiros     |
| 0x390C | Ward      |

## Section Structure

| Offset | Length  | Description                                                                                                                                            |
|--------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to character name<br/><br/>  _Squall and Rinoa have name offsets of 0xFFFF because their name is in the save game data rather than kernel.bin._ |
| 0x0002 | 1 byte  | Crisis level hp multiplier                                                                                                                             |
| 0x0003 | 1 byte  | Gender<br/><br/> 0x00 - Male<br/> 0x01 - Female                                                                                                        |
| 0x0004 | 1 byte  | Limit Break ID                                                                                                                                         |
| 0x0005 | 1 byte  | Limit Break Param<br/><br/> _used for the power of each renzokuken hit before finisher_                                                                |
| 0x0006 | 1 byte  | EXP curve — linear factor (low byte): EXP/level ×10. Retail 100 → 1000 EXP/level. See [Character level-up curve]({{site.baseurl}}/technical-reference/list/formula/#character-level-up-curve) |
| 0x0007 | 1 byte  | EXP curve — quadratic factor (high byte): acceleration ÷256. Retail 0 (flat curve)                                                                     |
| 0x0008 | 4 bytes | HP curve — 4 coefficients c1..c4 (see [Stat curves](#stat-curves))                                                                                     |
| 0x000C | 4 bytes | STR curve — 4 coefficients c1..c4                                                                                                                      |
| 0x0010 | 4 bytes | VIT curve — 4 coefficients c1..c4                                                                                                                      |
| 0x0014 | 4 bytes | MAG curve — 4 coefficients c1..c4                                                                                                                      |
| 0x0018 | 4 bytes | SPR curve — 4 coefficients c1..c4                                                                                                                      |
| 0x001C | 4 bytes | SPD curve — 4 coefficients c1..c4                                                                                                                      |
| 0x0020 | 4 bytes | LUCK curve — 4 coefficients c1..c4                                                                                                                     |

## Stat curves

Each stat stores **4 coefficient bytes** (`c1, c2, c3, c4`, in that byte order) that define
the character's **base** value of that stat at a given level `L` (1–100), before junctions,
equipped-weapon bonuses, and permanent stat-up bonuses are added. There are three distinct
curve shapes, verified against the engine:

| Stat(s) | Base formula | Coefficients | Function |
|---------|-------------|--------------|----------|
| **HP** | `L·c1 − 10·L² / c2 + c3` | c1, c2, c3 (**c4 unused**) | `Stat_ComputeCharaMaxHP` |
| **STR, VIT, MAG, SPR** | `( L·c1/10 + L/c2 − L² / (2·c4) + c3 ) / 4` | all 4 | `Stat_ComputeCharaStat` |
| **SPD, LUCK** | `L·c1 + L/c2 − L/c4 + c3` | all 4 | `Stat_ComputeCharaStat` (separate branch) |

All divisions are integer/truncating. HP has no cap in the base function (the final battle
max-HP is `junctionMultiplier% × base`, capped at 9999). STR/VIT/MAG/SPR and SPD/LUCK are
clamped to a maximum of **255** by `CapTo255` after base + bonus + junction are
summed.

> **Note:** SPD and LUCK use the plain **linear** shape (no quadratic term, no `/4`), *not*
> the STR-family formula. The doomtrain editor charts SPD/LUCK with the STR-family formula,
> which is incorrect.

Worked example — Squall's base **STR** at level 100 (coefficients `30, 5, 2, 38`):
`(100·30/10 + 100/5 − 100²/(2·38) + 2) / 4 = (300 + 20 − 131 + 2) / 4 = 47`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `Stat_ComputeCharaMaxHP` | 0x496310 | HP base-stat curve |
| `Stat_ComputeCharaStat` | 0x496440 | STR/VIT/MAG/SPR and SPD/LUCK base-stat curves |
| `CapTo255` | 0x495930 | Clamps a stat to 0–255 |