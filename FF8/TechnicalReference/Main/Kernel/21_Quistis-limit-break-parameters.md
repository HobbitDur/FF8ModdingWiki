---
layout: default
title: Blue magic parameters
nav_order: 22
parent: Kernel
permalink: /technical-reference/main/kernel/blue-magic-parameters/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x45F8 | 64       | 8 bytes      |

## Sections

| Offset | Ability              |
|--------|----------------------|
| 0x45F8 | Laser Eye CL1        |
| 0x4600 | Laser Eye CL2        |
| 0x4608 | Laser Eye CL3        |
| 0x4610 | Laser Eye CL4        |
| 0x4618 | Ultra Waves CL1      |
| 0x4620 | Ultra Waves CL2      |
| 0x4628 | Ultra Waves CL3      |
| 0x4630 | Ultra Waves CL4      |
| 0x4638 | Electrocute CL1      |
| 0x4640 | Electrocute CL2      |
| 0x4648 | Electrocute CL3      |
| 0x4650 | Electrocute CL4      |
| 0x4658 | LV?Death CL1         |
| 0x4660 | LV?Death CL2         |
| 0x4668 | LV?Death CL3         |
| 0x4670 | LV?Death CL4         |
| 0x4678 | Degenerator CL1      |
| 0x4680 | Degenerator CL2      |
| 0x4688 | Degenerator CL3      |
| 0x4690 | Degenerator CL4      |
| 0x4698 | Aqua Breath CL1      |
| 0x46A0 | Aqua Breath CL2      |
| 0x46A8 | Aqua Breath CL3      |
| 0x46B0 | Aqua Breath CL4      |
| 0x46B8 | Micro Missiles CL1   |
| 0x46C0 | Micro Missiles CL2   |
| 0x46C8 | Micro Missiles CL3   |
| 0x46D0 | Micro Missiles CL4   |
| 0x46D8 | Acid CL1             |
| 0x46E0 | Acid CL2             |
| 0x46E8 | Acid CL3             |
| 0x46F0 | Acid CL4             |
| 0x46F8 | Gatling Gun CL1      |
| 0x4700 | Gatling Gun CL2      |
| 0x4708 | Gatling Gun CL3      |
| 0x4710 | Gatling Gun CL4      |
| 0x4718 | Fire Breath CL1      |
| 0x4720 | Fire Breath CL2      |
| 0x4728 | Fire Breath CL3      |
| 0x4730 | Fire Breath CL4      |
| 0x4738 | Bad Breath CL1       |
| 0x4740 | Bad Breath CL2       |
| 0x4748 | Bad Breath CL3       |
| 0x4750 | Bad Breath CL4       |
| 0x4758 | White Wind CL1       |
| 0x4760 | White Wind CL2       |
| 0x4768 | White Wind CL3       |
| 0x4770 | White Wind CL4       |
| 0x4778 | Homing Laser CL1     |
| 0x4780 | Homing Laser CL2     |
| 0x4788 | Homing Laser CL3     |
| 0x4790 | Homing Laser CL4     |
| 0x4798 | Mighty Guard CL1     |
| 0x47A0 | Mighty Guard CL2     |
| 0x47A8 | Mighty Guard CL3     |
| 0x47B0 | Mighty Guard CL4     |
| 0x47B8 | Ray-Bomb CL1         |
| 0x47C0 | Ray-Bomb CL2         |
| 0x47C8 | Ray-Bomb CL3         |
| 0x47D0 | Ray-Bomb CL4         |
| 0x47D8 | Shockwave Pulsar CL1 |
| 0x47E0 | Shockwave Pulsar CL2 |
| 0x47E8 | Shockwave Pulsar CL3 |
| 0x47F0 | Shockwave Pulsar CL4 |

## Section Structure

| Offset | Length  | Description  |
|--------|---------|--------------|
| 0x0000 | 4 bytes | Status 1     |
| 0x0004 | 2 bytes | Status 0     |
| 0x0006 | 1 bytes | Attack Power |
| 0x0007 | 1 byte  | Hit rate — physical accuracy vs. the target's Evade (`Battle_applyDamage` → `HIT_ATTACK_HITPERCENT`, the Hit%-stat slot); `0xFF` = always hits |