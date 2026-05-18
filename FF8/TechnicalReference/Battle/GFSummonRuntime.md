---
layout: default
parent: Battle
title: GF Summon Runtime
permalink: /technical-reference/battle/gf-summon-runtime/
---

This page documents the runtime dispatch for Guardian Force summon effects, special GF-style auto-actions and the shared `MagicList_Logic` effect table.

1. TOC
{:toc}

## MagicList_Logic

`MagicList_Logic` at `0xC81774` is a 400-entry array of battle effect callbacks. Magic spells, GF summon cinematics, enemy attacks, item animations and boss cinematics all share this table.

| Address | Name | Type | Role |
|---------|------|------|------|
| `0xC81774` | `MagicList_Logic` | `int(*)(int)[400]` | Effect logic callbacks |
| `0xC81DB8` | `MagicList_TextureLoad` | `void(*)(void)[400]` | Matching texture-loading callbacks |
| `0x50AF20` | `BattleGF_LoadCallbackByMagicID` | function | Loads texture callback and writes active logic callback |
| `0x21DFEC4` | `GF_CALLBACK_PTR` | function pointer | Currently active GF/effect callback |

The `magicID` parameter passed to `BattleGF_LoadCallbackByMagicID` is a 1-based `effect_id`, not a GF kernel id and not a command argument.

```c
int idx = magicID - 1;
MagicList_TextureLoad[idx]();
*callback_out = MagicList_Logic[idx];
```

## Junctionable GF dispatch

The player command path identifies a GF with `command_id=0x03` and `command_arg=0x40..0x4F`. The command argument indexes the kernel GF table:

```
gf_index = command_arg - 0x40
effect_id = K_GF_JUNCTIONABLE[gf_index].magicID
```

The effect id is written to the action context at offset `+6`. `BattleActionSequence_Tick_GF_Cinematic` (`0x50B2A0`) later reads it and calls `BattleGF_LoadCallbackByMagicID`.

| Context offset | Size | Field | Description |
|----------------|------|-------|-------------|
| `+0` | 1 | `attacker_slot` | Attacker slot id |
| `+1` | 1 | `command_type` | `0xFE` for GF summon, other values for magic/special |
| `+2` | 1 | `anim_state` | Animation state byte |
| `+4` | 2 | `cmd_arg` | Ability / GF kernel id |
| `+6` | 2 | `effect_id` | 1-based `MagicList_Logic` id |
| `+12` | 4 | `damage_ctx_ptr` | Damage context pointer |
| `+16` | 1 | `flags` | Additional flags |

## Junctionable GF catalog

Runtime evidence quality varies by GF. Keep the Confidence and Runtime fields when using this table for modding work.

| GF | cmd_arg | effect_id | Entry | Init | Tick | Counter | Completion | Family | Confidence | Runtime |
|----|---------|-----------|-------|------|------|---------|------------|--------|------------|---------|
| Quezacotl | `0x40` | 116 | `0x6C3550` | `0x6C3640` | `0x6C3760` / `0x6C6660` | `0x6C3932` / `0x6C51F2` / `0x6C671D` | `0x6C3931` / `0x6C51F0` / `0x6C675D` | FamilyA | 96 (static) | Pending |
| Shiva | `0x41` | 185 | `0x5C0D50` | inline | `0x5C7F50` | `0x5C7F8B` | Unknown | FamilyA | 92 (static) | Pending |
| Ifrit | `0x42` | 201 | `0xB25780` | `0xB257E0` | `0xB25DF0` | `0xB25DFA` | `0xB26004` | FamilyB | 100 | PASS |
| Siren | `0x43` | 95 | `0x739DA0` | `0x8DC540` shared | `0x739F40` | Unknown | Unknown | SharedInit | 95 (static) | Pending |
| Brothers | `0x44` | 205 | `0xAF4520` | inline | `0xAF4B90` | `0xAF4B9A` | `0xAF4DA1` | Atypical | 75 | Tier-3 partial |
| Diablos | `0x45` | 325 | `0x654210` | Unknown | `0x654350` driver | `0x65459D` | `0x654595` | Unknown | 90 | PASS |
| Carbuncle | `0x46` | 278 | `0x680C50` | `0x680C80` | `0x680DF0` | `0x6811C8` | `0x6811BE` | FamilyA | 95 (static) | Pending |
| Leviathan | `0x47` | 6 | `0xB58080` | inline | `0xB586F0` | `0xB586FA` | `0xB58901` | Atypical | 75 | Tier-3 partial |
| Pandemona | `0x48` | 291 | `0x6ED250` | `0x6ED260` | `0x6ED350` | `0x6ED755` | `0x6ED749` | FamilyA | 95 | PASS |
| Cerberus | `0x49` | 203 | `0xB0C1A0` | inline | `0xB0C820` | `0xB0C82A` | `0xB0CA31` | FamilyB | High | PASS |
| Alexander | `0x4A` | 204 | `0xAFFCA0` | inline | `0xB00310` | `0xB0031A` | `0xB00521` | Atypical | 72 | Tier-3 partial |
| Doomtrain | `0x4B` | 191 | `0x63E730` | inline | `0x6472C0` | `0x6472D1` | Unknown | FamilyA | 80 | Tier-3 partial |
| Bahamut | `0x4C` | 202 | `0xB189A0` | inline | `0xB19010` | `0xB1901A` | `0xB19221` | Atypical | 72 | Tier-3 partial |
| Cactuar | `0x4D` | 199 | `0x5A8750` | inline | `0x5AA3A0` | `0x5AA3B1` | Unknown | Atypical | 75 | Tier-3 partial |
| Tonberry | `0x4E` | 90 | `0x762360` | `0x8DC540` shared | `0x7624D0` | `0x7625F9` | `0x762611` | SharedInit | 95 | PASS |
| Eden | `0x4F` | 206 | `0xAE2DD0` | inline | `0xAE3470` | `0xAE347A` | `0xAE3681` | Atypical | 70 | Tier-3 partial |

Note: Diablos has a thunk wrapper at `0x6541E0` in `MagicList_Logic`; it forwards to the real entry at `0x654210`.

## GF families

| Family | Shape | Examples |
|--------|-------|----------|
| FamilyA | Entry -> Init -> SequenceTick -> secondary SequenceTaskDriver | Pandemona, Doomtrain, Shiva, Odin |
| FamilyB | Entry -> SequenceTick; the tick is the driver | Cerberus, Brothers, Leviathan, Alexander, Bahamut, Eden |
| SharedInit | Entry -> `BdLinkTask_CreateAndInitContext` -> SequenceTick | Siren, Tonberry |
| Atypical | Partially resolved or not clearly classified | Several low-confidence chains |

All families use the same completion return pattern:

```c
return ((unsigned int)~*(WORD*)(statePtr + 10) >> 14) & 2;
```

## Shared GF infrastructure

`BdLinkTask_CreateAndInitContext` (`0x8DC540`) is a shared task constructor used by multiple GFs.

```c
int __cdecl BdLinkTask_CreateAndInitContext(
    _DWORD *dst_ctx,
    int tick_fn,
    int ctx_size,
    int parent_ctx
);
```

The second argument is the per-frame tick function, which is how the tick can be recovered from entries that use the shared constructor.

Shared cinematic globals are reused across all GFs; only one GF cinematic runs at a time.

| Address | Name | Description |
|---------|------|-------------|
| `0x27973EC` | `g_GfCinematic_SequenceCtxPtr` | Active GF sequence context |
| `0x27973B8` | `g_GfCinematic_RuntimeSlotPtr` | Active GF runtime slot |
| `0x27973BC` | `g_GfCinematic_RenderCtxPtr` | Active GF render context |
| `0x27973C0` | `g_GfCinematic_SequenceStatePtr` | Active GF state pointer |
| `0x2797624` | `g_GfCinematic_OffsetStack` | Active GF stack frame |

## Special / non-junctionable GFs

| Effect | effect_id | Entry | Mechanism | Notes |
|--------|-----------|-------|-----------|-------|
| Odin | 187 | `0x6472E0` | Battle-start auto-trigger | Crashes on direct injection; use caveat |
| Griever | 69 | `0x6FE040` / thunk `0x6FE050` | Boss-only cinematic | Corrected from a former mid-function address |
| Gilgamesh Zantetsuken | 329 | `0x58DB10` | Special action `0xF5` | Variant selected randomly |
| Gilgamesh Masamune | 330 | `0x58DCF0` | Special action `0xF5` | Variant selected randomly |
| Gilgamesh Excalibur | 328 | `0x58D930` | Special action `0xF5` | Variant selected randomly |
| Gilgamesh Excalipoor | 327 | `0x58D760` | Special action `0xF5` | Variant selected randomly |
| Phoenix | 140 | `0x6A6430` | Party-wipe auto-trigger | 64/255 trigger check |
| Angelo Rush | 91 | via MagicList | Auto/counter | Rinoa action |
| Angelo Recover | 93 | via MagicList | Auto/counter heal | Rinoa action |
| Angelo Reverse | 94 | via MagicList | Counter revive | Rinoa action |
| Angelo Search | 92 | via MagicList | Auto item find | Rinoa action |
| ChocoFire | 97 | `0x729A60` | Chocobo/Boko variant | Entry mapped through table |
| ChocoFlare | 98 | `0x721860` | Chocobo/Boko variant | Entry mapped through table |
| ChocoMeteor | 99 | `0x717D30` | Chocobo/Boko variant | Entry mapped through table |
| ChocoBocle | 100 | `0x70D390` | Chocobo/Boko variant | SharedInit-like pattern |

## Odin and Gilgamesh

`SG_ODIN_ANGEL_GILGA_FLAG` (`0x1CFE97A`) controls Odin, Phoenix, Gilgamesh, Angelo suppression and Witch-related state.

| Bit | Value | Meaning | Set by |
|-----|-------|---------|--------|
| 1 | `0x02` | Has Odin | `SETODIN` field opcode |
| 2 | `0x04` | Phoenix enabled | Phoenix Pinion use in battle |
| 3 | `0x08` | Has Gilgamesh | Monster AI opcode 54; clears Odin simultaneously |
| 4 | `0x10` | Suppress Angelo | Field script opcode |
| 5 | `0x20` | Witch | `SETWITCH` field opcode |

Odin is checked only at battle init (`mode_3_subsubsubstep == 3`). `ZANTETSUKEN_sub_482DF0` (`0x482E00`) requires the Odin flag and skips if any enemy has death immunity. The RNG is `32/255`, about 12.5%.

Gilgamesh can trigger during battle init (`8/255`, about 3.1%) or during the active tick through `AngeloOdin_SpecialActionTick` (`0x482F80`) at `12/255` per checked tick. `GILGAMESH_ONESHOT_FLAG` prevents more than one Gilgamesh action in the same battle.

In the Seifer disc-3 battle, monster AI opcode 54 clears Odin and sets Gilgamesh:

```c
SG_ODIN_ANGEL_GILGA_FLAG &= 0xFD;
SG_ODIN_ANGEL_GILGA_FLAG |= 0x08;
```

## Phoenix

Phoenix auto-triggers on party wipe only. It does not have a spontaneous per-frame trigger like Gilgamesh.

`BattleFrame_PartyWipeCheck` (`0x486450`) scans party slots each active battle frame. If all party members are dead or petrified, it calls `Phoenix_BattleFrame_TriggerCheck` (`0x483270`).

| Condition | Required value |
|-----------|----------------|
| At least one enemy alive | true |
| At least one party member exists and is not petrified | true |
| `SG_ODIN_ANGEL_GILGA_FLAG & 0x04` | Phoenix enabled |
| `COMBAT_SCENE_ID != 317` | Not excluded scene |
| RNG | `64/255`, about 25.1% |

The result is `RELATED_ODIN_SUMMONED = 1`, which maps to `effect_id=140`.

## Angelo variants

Angelo requires Rinoa in the party (`com_file_id == 4`) and bit `0x10` of `SG_ODIN_ANGEL_GILGA_FLAG` clear.

| Path | Function | Behavior |
|------|----------|----------|
| Per-frame auto-trigger | `AngeloOdin_SpecialActionTick` (`0x482F80`) | Recover, Reverse, Rush-like or Search priority cascade |
| Turn counter | `Angelo_TurnCounter_TriggerCheck` (`0x482E80`) | Rinoa turn: Recover or Rush |
| Damage counter | `Angelo_DamageCounter_ReverseCheck` (`0x482F10`) | Enemy attacks Rinoa: Angelo Reverse |

| Variant index | effect_id | Ability | Command type |
|---------------|-----------|---------|--------------|
| 11 | 91 | Angelo Rush | `0xF0` |
| 12 | 93 | Angelo Recover | `0xF0` |
| 13 | 94 | Angelo Reverse | `0xF0` |
| 14 | 92 | Angelo Search | `0xF0` |

## Runtime evidence summary

| GF | Test id | Key confirmations |
|----|---------|-------------------|
| Ifrit | GF_IFRIT_001 | cmd_arg `0x42`, callback pointer, tick and counter |
| Diablos | GF_DIABLOS_001 | cmd_arg `0x45`, gravity HP reduction, `COMMAND_TYPE_ID=0xFE` |
| Cerberus | GF_CERBERUS_001 | cmd_arg `0x49`, Double+Triple, support GF with 0 damage |
| Doomtrain | GF_DOOMTRAIN_001 | Multi-status and damage pipeline |
| Siren | GF_SIREN_001/002 | Silence infliction |
| Pandemona | GF_PANDEMONA_001 | cmd_arg `0x48`, pending transfer, enemy HP decrease |
| Tonberry | GF_TONBERRY_002 | Tick, counter and completion confirmed |
