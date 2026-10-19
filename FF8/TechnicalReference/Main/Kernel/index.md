---
layout: default
title: Kernel
parent: Main
nav_order: 1
permalink: /technical-reference/main/kernel/
---

**Kernel.bin** documentation was originally held on external wiki of [Doomtrain github](https://github.com/alexfilth/doomtrain/wiki/Kernel.bin)

As we are not able anymore to update it, it has been copied here and edited with latest knowledge.

## Naming and offsets

Section numbers in these pages and SolomonRing are **1-based** (the header is section
0). A field offset is relative to the start of one record; section offsets in the
header are relative to the start of `kernel.bin`. Absolute offsets in the General
tables describe the vanilla layout; an edited file's header is authoritative.

| Term in SolomonRing and this wiki | IDA convention | Meaning |
|---|---|---|
| Attack animation | `attackAnimationID`, type `AttackAnimationID` | 16-bit visual-effect ID dispatched by the engine; not an entry ID in the Magic section |
| Target hit animation | `targetHitAnimation` | Reaction/impact animation played by the target; distinct from the acting entity's Seq anim and camera animation |
| Status attack accuracy | `statusAttackAccuracy` | Accuracy input for the status roll; an accuracy value, not an on/off flag |
| Command ability data (section 11) | `FF8KernelCommandAbilityData`, `K_COMMAND_ABILITY_DATA` | Fixed effect records referenced by Battle Commands |
| Command abilities (section 13) | `FF8KernelCommandAbilityGF` | GF-learned abilities that grant a Battle Command |
| Padding / unused | `padding` or an explicit `unused…` member | Bytes retained in the binary layout; do not treat them as unknown editable effects |

New IDA member names use camelCase; existing snake_case members, including the Misc
table, remain stable. Labels use the terms above. SolomonRing retains historical internal keys such as `magic_id`,
`animation`, and `ability1_unlocker` for compatibility; its labels and help describe
the actual field. `FF8KernelBattleCommandAbility` and `FF8KernelCommandBattleAbility`
are compatibility aliases of `FF8KernelCommandAbilityData`, not separate layouts.

## IDA field types

Use the existing enum when its meaning **and stored width** match the field:

| Field | IDA type | Stored width |
|---|---|---|
| Status 1 mask | `Status1Flag` | 2 bytes |
| Status 2 mask | `Status2Flag` | 4 bytes |
| Damage calculation | `AttackType` | 1 byte |
| Attack flags | `AttackFlags` | 1 byte |
| Target info | `TargetInfo` | 1 byte |
| Element mask | `ElementType` | 1 byte |
| Attack animation | `AttackAnimationID` | 2 bytes |
| Weapon character | `CharacterID` | 1 byte |
| Granted Battle Command | `KernelBattleCommandId` | 1 byte |
| Stat-percentage ability's stat | `FF8KernelStatIndex` | 1 byte |

Legacy IDA names `status0`/`Status0` for the 16-bit mask and `status1`/`Status1` for
the 32-bit mask are normalized to **`status1`** and **`status2`** respectively. This
does not change their order in records: some families store Status 2 before Status 1.

The non-junctionable GF record stores **four Status 2 bytes followed by the low
Status 1 byte**, rather than two full masks. Its fields use `Status2FlagLowByte`,
`Status2Byte1Flags`, `Status2Byte2Flags`, `Status2Byte3Flags`, then `Status1FlagLowByte`.
The byte enums expose the same bit positions within each byte as SolomonRing.

The Junction/Character ability masks are **three bytes**, so a four-byte runtime
enum cannot be assigned directly. `FF8KernelJunctionFlags` and
`FF8KernelCharacterFlags` preserve that size with three byte-sized enum members
(`low`, `middle`, `high`). Their flags match SolomonRing's existing lookups.
Other kernel-only byte enums cover GF stat selection, Refine table selection,
gender, Renzokuken finisher flags, status-window flags and command-menu flags.
Numeric powers, accuracies, durations, offsets and padding retain numeric types.
