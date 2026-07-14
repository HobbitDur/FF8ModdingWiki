---
layout: default
title: Stat percentage increasing abilities
nav_order: 15
parent: Kernel
permalink: /technical-reference/main/kernel/stat-percentage-increasing-abilities/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4218 | 19       | 8 bytes      |

## Sections

| Offset | Ability  |
|--------|----------|
| 0x4218 | HP+20%   |
| 0x4220 | HP+40%   |
| 0x4228 | HP+80%   |
| 0x4230 | STR+20%  |
| 0x4238 | STR+40%  |
| 0x4240 | STR+60%  |
| 0x4248 | VIT+20%  |
| 0x4250 | VIT+40%  |
| 0x4258 | VIT+60%  |
| 0x4260 | MAG+20%  |
| 0x4268 | MAG+40%  |
| 0x4270 | MAG+60%  |
| 0x4278 | SPR+20%  |
| 0x4280 | SPR+40%  |
| 0x4288 | SPR+60%  |
| 0x4290 | SPD+20%  |
| 0x4298 | SPD+40%  |
| 0x42A0 | EVA+30%  |
| 0x42A8 | LUCK+50% |

## Section Structure

| Offset | Length  | Description                    |
|--------|---------|--------------------------------|
| 0x0000 | 2 bytes | Offset to ability name         |
| 0x0002 | 2 bytes | Offset to ability description  |
| 0x0004 | 1 byte  | AP needed to learn the ability |
| 0x0005 | 1 byte  | Stat to increase — NOT a bitfield; a plain index picking one of the 9 standard stats (`0`=HP, `1`=STR, `2`=VIT, `3`=MAG, `4`=SPR, `5`=SPD, `6`=EVA, `7`=HIT (unused by any retail ability), `8`=LUCK). `sub_4962C0` tests it with a straight equality compare against the stat being computed, once per owned Stat% ability; matching abilities' Increase Value bytes sum onto a 100 base (owning both HP+20% and HP+40% gives 100+20+40=160%). Applied in `Stat_RefreshCharaBattleStats`: `stat = multiplier * baseStat / 100` |
| 0x0006 | 1 byte  | Increase value                 |
| 0x0007 | 1 byte  | Padding (unused; IDA: 0 xrefs) |
