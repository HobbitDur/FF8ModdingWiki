---
layout: default
parent: Battle
title: Command and Action Pipeline
permalink: /technical-reference/battle/command-and-action-pipeline/
---

This page documents the runtime path from a player or AI command to action resolution, damage, status application and draw/stock handling.

1. TOC
{:toc}

## Overview

The battle action path is:

```
Input / AI -> PendingAction -> ExecQueue -> Arbitration -> Resolve -> Damage / Status -> Presentation
```

| Stage | Main function | Address |
|-------|---------------|---------|
| Input / command menu | `BattleUI_InputPollAndMenuState` | `0x4A8772` |
| Pending write | `BattlePendingAction_Write` | `0x484D20` |
| Pending to execution queue | `BattlePendingAction_TransferToExecQueue` | `0x4847F0` |
| Arbitration | `BattleArbitration_SelectNextAction` | `0x485460` |
| Action resolve | `BattleAction_ResolveSpecialActionAndUpdateDamage` | `0x485160` |
| Damage / HP write | `BattleAction_ResolveAndApplyDamage` / `Battle_ApplyDamageOrHeal` | `0x48FE20` / `0x494410` |
| Damage event output | `Battle_UpdateDamage` | `0x48EF80` |

## Command menu builder

The command availability builder runs through the following chain:

| Function | Address | Role |
|----------|---------|------|
| `BattleCommandMenu_MainState` | `0x4BB9E0` | Per-character command menu state machine |
| `BattleCommandMenu_InitCommandSetAndLimitState` | `0x4BB910` | Rebuild command metadata and Limit Break availability |
| `BattleLimit_ComputeCrisisAndToggleAttackSlot` | `0x4941F0` | Compute crisis level and toggle the attack slot |
| `BattleCommandMenu_OpenSelectedCommand` | `0x4BC770` | Open submenu or accept a direct action |

On command confirmation, the staged command is flushed to `BattlePendingAction_Write`. The write happens on target confirmation, not when the player only highlights a command.

| Command type | Runtime notes |
|--------------|---------------|
| Magic | Requires a command entry in the 4-command set and stocked magic availability |
| GF | Uses `command_id=0x03`; `command_arg` is the kernel GF id (`0x40..0x4F`) |
| Draw | Uses a dedicated menu/target state machine; target draw list is refreshed from the enemy slot |
| Item | Opens through the generic battle submenu dispatch path |

## Pending action entry

Pending actions are stored at `BATTLE_PENDING_ACTION_BUFFER`. There are three entries, each 8 bytes.

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| `+0x0` | 2 | `target_mask` | Target selection bitmask |
| `+0x2` | 1 | `attacker_slot` | Attacker slot index |
| `+0x3` | 1 | `command_id` | Command category |
| `+0x4` | 1 | `command_arg` | Spell id, GF kernel id, item id, etc. |
| `+0x5` | 1 | padding | Always 0 |
| `+0x6` | 1 | padding | Always 0 |
| `+0x7` | 1 | `active` | 1 = entry is live |

Example command bytes:

| Command | Raw bytes | Notes |
|---------|-----------|-------|
| Attack, slot 1 to enemy | `10 00 01 01 00 00 00 01` | `target_mask=0x10`, `cmd_id=0x01` |
| GF Ifrit, slot 0 | `08 80 00 03 42 00 00 01` | `cmd_arg=0x42` |
| GF Diablos, slot 0 | `08 80 00 03 45 00 00 01` | `cmd_arg=0x45` |
| GF Cerberus, slot 0 | `08 80 00 03 49 00 00 01` | Support GF, Double/Triple |

`BattlePendingAction_TransferToExecQueue` copies live entries into:

| Address | Name | Description |
|---------|------|-------------|
| `0x1D288E8` | `BATTLE_EXEC_QUEUE_BYTES` | Attacker, command and auxiliary byte lanes |
| `0x1D288EE` | `BATTLE_EXEC_QUEUE_TARGET_MASKS` | Target mask array |

The pending `active` flag is cleared after transfer.

## command_id and resolver values

| command_id | Command | Evidence |
|------------|---------|----------|
| `0x01` | Attack | Runtime capture |
| `0x02` | Magic | Runtime injection / cast |
| `0x03` | GF | Runtime capture |
| `0x04` | Draw | Inferred from menu path |
| `0x05` | Item | Inferred from menu path |

At damage resolve time, `COMMAND_TYPE_ID` selects which kernel/runtime table supplies metadata:

| COMMAND_TYPE_ID | Category | Metadata source |
|-----------------|----------|-----------------|
| `1` | Physical / Attack | `BATTLE_SLOT_DATA[attacker]` |
| `2` | Magic | `K_MAGIC[action_id]` |
| `4` | Item | `K_ITEM[action_id]` |
| `6` | Draw | `K_MAGIC[action_id]` |
| `7`, `23..27`, `29..34`, `38` | Command ability | `K_BATTLE_COMMAND_ABILITY[action_id]` |
| `8` | Enemy attack | `K_ENEMY_ATTACK[action_id]` |
| `16` | Slot / Selphie | `K_MAGIC[action_id]` |
| `236` | Enemy attack variant | `K_ENEMY_ATTACK[action_id]` |
| `247` | Magic variant | `K_MAGIC[action_id]` |
| `254` (`0xFE`) | GF | `K_GF_JUNCTIONABLE[action_id - 64]` |

## GF command_arg values

GF `command_arg` values are kernel GF IDs, not zero-based indices. The resolver computes `gf_index = command_arg - 64`.

| command_arg | GF | gf_index | Evidence |
|-------------|----|----------|----------|
| `0x40` | Quezacotl | 0 | Kernel order |
| `0x41` | Shiva | 1 | Kernel order |
| `0x42` | Ifrit | 2 | Runtime capture |
| `0x43` | Siren | 3 | Kernel order |
| `0x44` | Brothers | 4 | Kernel order |
| `0x45` | Diablos | 5 | Runtime action globals |
| `0x46` | Carbuncle | 6 | Kernel order |
| `0x47` | Leviathan | 7 | Kernel order |
| `0x48` | Pandemona | 8 | Runtime action globals |
| `0x49` | Cerberus | 9 | Runtime action globals |
| `0x4A` | Alexander | 10 | Kernel order |
| `0x4B` | Doomtrain | 11 | Kernel order |
| `0x4C` | Bahamut | 12 | Kernel order |
| `0x4D` | Cactuar | 13 | Kernel order |
| `0x4E` | Tonberry | 14 | Kernel order |
| `0x4F` | Eden | 15 | Kernel order |

## Damage pipeline

`Battle_applyDamage` (renamed from `BattleAction_ResolveAndApplyDamage`) first resolves metadata into hit globals:

| Global | Source |
|--------|--------|
| `HIT_ELEMENT` | Kernel table `.element` |
| `HIT_ATTACK_ENABLER` | Kernel table `.statusAttackEnabler` |
| `HIT_STATUS_1` | Kernel table `.statuses0` |
| `HIT_STATUS_2` | Kernel table `.statuses1` |
| `HIT_ATTACK_HITPERCENT` | Kernel table `.hitPercent` |
| `ATTACK_FLAG` | Kernel table `.attackFlags` |

`Damage_DispatchByAttackType` (renamed from `Damage_ComputeRawDeltaFromAttackType`) then dispatches by `attackType`:

| Attack type path | Function |
|------------------|----------|
| Magic / GF | `ComputeMagicAndGFDamage` (`0x491AD0`) |
| Curative | `computeCurativeMagic` (`0x493280`) / `computeCurativeGFMagicItem` |
| Physical | Physical formula path |

Finally, `applyDamageAndHandleDeath` (renamed from `Battle_ApplyDamageOrHeal`) writes HP, clamps it to `[0, max_hp]`, sets KO when HP reaches 0, and performs attacker/target bookkeeping. `Battle_UpdateDamage` writes a 24-byte event record to `BATTLE_DAMAGE_RESULT_BUFFER` (base + `24 * ATTACK_HIT_COUNT_1`) for the presentation layer.

## Status pipeline

Status application is split into a gating layer and an execution layer.

| Step | Function | Address | Role |
|------|----------|---------|------|
| Payload | `BattleAction_ResolveAndApplyDamage` | `0x48FE20` | Populate `HIT_STATUS_1`, `HIT_STATUS_2`, `HIT_ATTACK_ENABLER` |
| Gate | `BattleStatus_CanApplyHitStatus` | `0x492AC0` | Pure predicate: can this status land? |
| Resolve | `BattleStatus_ApplyHitStatus` | `0x4914E0` | Mutual exclusion, double-apply prevention, clear/set bits |
| Commit | `BattleStatus_ApplyAndSyncSlot` | `0x493840` | Write `status_1/2`, sync mirror, handle side effects |
| Post-action | `BattleAction_ResolveAndApplyStatusResult` | `0x493D80` | HP-threshold status bits and final sync |

`BattleStatus_CanApplyHitStatus` blocks all status application when the target is petrified (`status_1 & 0x04`) or has invulnerability flags (`status_2 & 0x180800`). Whether beneficial statuses bypass this gate through a separate path is not confirmed.

## Draw system

`Battle_ComputeDrawQuantity` (renamed from `Draw_ComputeStealCount`) computes draw quantity (0-9) from attacker level, target level, attacker magic stat, `K_MAGIC[magic_id].drawResist`, and randomness.

`computeCommandAction` (the `getText` name and `0x48D554` previously cited here were an interior offset of this function) has two draw paths:

| Parameter | Path |
|-----------|------|
| `9` | Draw -> Cast; validates draw quantity, then casts the spell |
| `10` | Draw -> Stock; computes quantity and loops stock increments |

`updateCharaMagicInventory` (renamed from `Battle_MutateMagicStock`) adds one unit at a time to the magic stock for a slot and caps each stocked spell at 100.

## Open questions

- Exact formula inside `ComputeMagicAndGFDamage`.
- How `ATTACK_FLAG` and `HIT_TYPE_2` modify edge cases such as misses and drain.
- Whether support status applications bypass `BattleStatus_CanApplyHitStatus`.
- Whether `updateCharaMagicInventory` is the only stock mutation path outside battle.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `BATTLE_PENDING_ACTION_BUFFER` | 0x1D28D44 | Global variable/data, not a function |
| `Battle_applyDamage` (formerly documented as `BattleAction_ResolveAndApplyDamage`) | 0x48FE20 | Per-hit damage resolution entry point (verified IDA function) |
| `Damage_DispatchByAttackType` (formerly documented as `Damage_ComputeRawDeltaFromAttackType`) | 0x4922B0 | Dispatches the raw damage formula by attack type (verified IDA function) |
| `applyDamageAndHandleDeath` (formerly documented as `Battle_ApplyDamageOrHeal`) | 0x494410 | Writes HP, clamps, sets KO, attacker/target bookkeeping (verified IDA function) |
| `BATTLE_DAMAGE_RESULT_BUFFER` | 0x1D28344 | Global variable/data, not a function |
| `Battle_ComputeDrawQuantity` (formerly documented as `Draw_ComputeStealCount`) | 0x48FD20 | Computes draw quantity 0-9 (verified IDA function) |
| `computeCommandAction` | 0x48D200 | Command menu action handler; the `getText` name and `0x48D554` previously cited on this page were an interior offset of this function (verified IDA function) |
| `updateCharaMagicInventory` (formerly documented as `Battle_MutateMagicStock`) | 0x486A10 | Adds stock units, caps at 100 (verified IDA function) |
