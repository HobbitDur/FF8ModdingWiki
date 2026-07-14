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

| ID   | Meaning          |
|------|------------------|
| 0x03 | Damage-type pair (bits 0-1) — see below |
| 0x04 | Unused — no reader anywhere (also set on nothing in retail) |
| 0x08 | Break damage limit (dmg cap 9999 → 60000) |
| 0x10 | Reflectable — the spell can be bounced by Reflect status (`handleSpellReflection`) |
| 0x20 | Read **only for battle items** — `updateBattleItemData` (`test byte, 20h`) drives the item's battle-menu selectability/greyed state. On magic / GF / Blue Magic / limits this bit is **inert**, even though it is set on virtually every player ability (an authoring convention: set on all player abilities, clear on all 384 enemy attacks) |
| 0x40 | Unused — no reader anywhere. It is deliberately set on the curative/beneficial magics (Cure family, Life, Esuna, Dispel, Float, and — oddly — Fire) and on every curative item, but nothing in the engine tests it. The actual "beneficial → default-target allies / revive" behaviour is driven by `0x80` (Revive) plus the separate [TargetInfo]({{site.baseurl}}/technical-reference/list/kernel#target-info) byte, not this bit |
| 0x80 | Revive — classifies the action as revival; drives the field/battle menu revive handling and the ally-default targeting (`ATTACK_FLAG_REVIVE`) |

### Damage-type pair (bits 0-1)

The low two bits form a damage-type pair, stored per hit as the target's
`last_attacker_attack_flag` (`ATTACK_FLAG & 3`). It is **not** a free bitfield — it's one of four
mutually-exclusive values. The kernel `attackFlags` byte holds the "resting" value; the runtime
overrides some (Gunblade/Renzokuken force `3`; on a Gunblade *hit* the value becomes the source's
own type).

| Pair | Name | Set by |
|------|------|--------|
| 0 | Physical | Attack, most physical commands |
| 1 | Magical | Magic, GF, most offensive spells |
| 2 | Item/Medicine | Battle items |
| 3 | (special) | Forced by Renzokuken finishers / Gunblade |

**What pair = 0 (Physical) uniquely enables** — pure-physical hits are the *only* ones that:
trigger the target's **Counter** ability, **wake** a Sleeping/Confused target, **remove Back
Attack** status, and mark the **kill result** on a killing blow. Magical, Item and special hits do
none of these. The monster-AI condition `LAST ACTION DAMAGE TYPE` also compares this pair against
Physical/Magical, so an attack's type decides which AI branches fire.

**What pair = 1 (Magical) does** — the target's **Shell** status halves the damage *or heal*
(`ATTACK_FLAG_MAGICAL_SHELLED`). This is unconditional in `computeCurativeMagic`, so **curative
magic is always Shell-halved** — a penalty spells cannot avoid.

**What pair = 2 (Item/Medicine) does** — it is the gate for the **Med Data** doubling in
`Damage_ComputeCurativeItemSpecial`:

```
if ((ATTACK_FLAG & 3) == 2 && attacker is a player character && attacker knows Med Data)
    heal *= 2;
```

Curative-item heals use `50 × power` (Potion, power 4 → 200 HP; doubled to 400 with Med Data). But
the *implications of the pair value* matter just as much as the doubling:

- **Fun fact — items dodge Shell.** Because a curative item is pair 2 (not 1/Magical), a target's
  Shell status does **not** halve its healing (`Damage_ComputeCurativeItemSpecial` has no Shell
  check). The Shell penalty that hits a Cure *spell* (pair 1, halved unconditionally in
  `computeCurativeMagic`) simply never applies to a Potion.
- **Fun fact — Med Data never provokes a counter.** Med Data doubling only exists on the Item path
  (pair 2), which is non-Physical, so a doubled heal can never trigger the target's Counter — you get
  the boost with none of the physical-hit side effects.
- **Fun fact — Phoenix Down ignores this flag entirely.** Its Med Data boost (maxHP/8 → maxHP/4
  revive) lives in `GetReviveHP` and checks `command == Item` **directly**, not `ATTACK_FLAG & 3`. So
  the flag governs *curative-item HP restore*, while revival amount is gated separately by the command
  type.

