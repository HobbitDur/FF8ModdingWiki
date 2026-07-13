---
layout: default
title: Kernel
parent: List
permalink: /technical-reference/list/kernel/
---

# Target info

Bits decoded by `getTargetMaskFromInfo` / `computeTargetMaskDeadUnknown1` when the engine
auto-resolves a target mask (AI attacks, auto-summons, item randomization).

| ID     | Description          |
|--------|----------------------|
| 0x0000 | None                 |
| 0x0001 | Dead — targets KO'd units (adds the revive bit 0x4000 to the target mask) |
| 0x0002 | Multi-target spread — adds mask bit 0x2000 (`TARGET_MASK32_TARGET_SEVERAL`; IDA `TARGET_INFO_SEVERAL_HIT_SPREAD`) |
| 0x0004 | Unused — skipped by both target-mask decoders; no consumer found |
| 0x0008 | Single Side          |
| 0x0010 | Single — auto-resolves to one random target of the chosen side |
| 0x0020 | Everyone on one side — auto-resolves to the whole side |
| 0x0040 | Enemy — selects the enemy side (otherwise the character side) |
| 0x0080 | Unused — skipped by both target-mask decoders; no consumer found |


# Attack Type

| ID | Hex  | Description                          |
|----|------|--------------------------------------|
| 1  | 0x00 | None                                 |
| 2  | 0x01 | Physical Attack                      |
| 3  | 0x02 | Magic Attack                         |
| 4  | 0x03 | Curative Magic                       |
| 5  | 0x04 | Curative Item                        |
| 6  | 0x05 | Revive                               |
| 7  | 0x06 | Revive At Full HP                    |
| 8  | 0x07 | % Physical Damage                    |
| 9  | 0x08 | % Magic Damage                       |
| 10 | 0x09 | Renzokuken Finisher                  |
| 11 | 0x0A | Squall Gunblade Attack               |
| 12 | 0x0B | GF                                   |
| 13 | 0x0C | Scan                                 |
| 14 | 0x0D | LV Down                              |
| 15 | 0x0E | Summon Item?                         |
| 16 | 0x0F | GF (Ignore Target SPR)               |
| 17 | 0x10 | LV Up                                |
| 18 | 0x11 | Card                                 |
| 19 | 0x12 | Kamikaze                             |
| 20 | 0x13 | Devour                               |
| 21 | 0x14 | % GF Damage                          |
| 22 | 0x15 | Unknown 1                            |
| 23 | 0x16 | Magic Attack (Ignore Target SPR)     |
| 24 | 0x17 | Angelo Search                        |
| 25 | 0x18 | Moogle Dance                         |
| 26 | 0x19 | White Wind (Quistis)                 |
| 27 | 0x1A | LV? Attack                           |
| 28 | 0x1B | Fixed Damage                         |
| 29 | 0x1C | Target Current HP - 1                |
| 30 | 0x1D | Fixed Magic Damage Based on GF Level |
| 31 | 0x1E | Unknown 2                            |
| 32 | 0x1F | Unknown 3                            |
| 33 | 0x20 | Give Percentage HP                   |
| 34 | 0x21 | Unknown 4                            |
| 35 | 0x22 | Everyone's Grudge                    |
| 36 | 0x23 | 1 HP Damage                          |
| 37 | 0x24 | Physical Attack (Ignore Target VIT)  |


## Attack flag

The low two bits form a damage-type pair stored as the target's `last_attacker_attack_flag`
(`ATTACK_FLAG & 3`): 0 = Physical, 1 = Magical, 2 = Item/Medicine (Renzokuken finishers force 3).
Only pure-physical hits (pair = 0) trigger the Counter ability, wake Sleep/Confusion, remove
Back Attack, and mark the kill result on death; the AI condition `LAST ACTION DAMAGE TYPE`
compares this pair against Physical/Magical.

| ID   | Meaning          |
|------|------------------|
| 0x01 | Magical — Shell halves the damage/heal (`ATTACK_FLAG_MAGICAL_SHELLED`) |
| 0x02 | Item/Medicine — healing doubled by the MedData ability (`ATTACK_FLAG_ITEM_MEDICINE`) |
| 0x04 | Unused — never tested by any consumer of the attack flags |
| 0x08 | Break damage limit |
| 0x10 | Reflectable — the spell can be bounced by Reflect status (`handleSpellReflection`) |
| 0x20 | Unused — never tested by any consumer of the attack flags |
| 0x40 | Unused — never tested by any consumer of the attack flags |
| 0x80 | Revive — classifies the action as revival (menu revive handling, `ATTACK_FLAG_REVIVE`) |

