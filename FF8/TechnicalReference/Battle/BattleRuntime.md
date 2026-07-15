---
layout: default
parent: Battle
title: Battle Runtime
permalink: /technical-reference/battle/battle-runtime/
---

The following information documents the PC 2000 battle runtime state machine and the main per-frame flow. It complements the file format pages by showing how loaded encounter data becomes an active battle.

1. TOC
{:toc}

## Module entry

The battle module is entered through `FFModuleHandler_main_loop`. Field and world-map modules write a pending battle scene id, then the module handler stores it in `COMBAT_SCENE_ID` before launching the battle module.

| Address | Name | Role |
|---------|------|------|
| `0x4706B0` | `FFModuleHandler_main_loop` | Top-level module dispatcher |
| `0x46FEE0` | `FFFieldModule_field_main_loop` | Field module loop |
| `0x53F0F0` | `FFWorldModule_worldmap_main_loop` | World-map module loop |
| `0x47CCB0` | `FFBattleDirector_battleLoop` | Battle state machine and per-frame tick |
| `0x1CFF6E0` | `COMBAT_SCENE_ID` | Active battle scene id |

The battle director reaches the active battle tick when:

| State field | Required value | Meaning |
|-------------|----------------|---------|
| `mode_StateGlobal` | `3` | Battle module active |
| `mode3_subsub_step` | `3` | Battle init has reached the active substage |
| `mode_3_subsubsubstep` | `4` | Active per-frame battle tick |

## Initialization phases

Before the per-frame tick begins, `FFBattleDirector_battleLoop` runs the battle module through a set of initialization substates:

| Step | Description |
|------|-------------|
| 1 | Load `COMBAT_SCENE_ID` and the 128-byte scene.out encounter block (`scene_id << 7`) |
| 2 | Clear all 11 battle slots, parse party members, junction stats, commands, auto-statuses and items |
| 3 | Async-load battle stage geometry |
| 4 | Initialize enemy slots from c0mxxx.dat data: level scaling, HP/stat formulas and innate statuses |
| 5 | Resolve preemptive / back-attack outcome and ATB overrides |
| 6 | Async-load enemy textures |
| 7 | Run pre-battle checks such as Odin, Gilgamesh, dead timer and target visibility |
| 8 | Enter active tick (`mode_3_subsubsubstep == 4`) |

See [Encounters data (scene.out)](../battle-structure-sceneout/) for the encounter block layout loaded in step 1.

## Active tick flow

Within the active tick, the engine processes player input, ATB, pending actions, arbitration, damage/status resolution and presentation tasks in a fixed order.

| Order | Function | Address | Role |
|-------|----------|---------|------|
| 1 | `BattleUI_InputPollAndMenuState` | `0x4A8772` | Poll input and drive command menu state |
| 2 | `BattleATB_TickAndReady` | `0x4842B0` | Advance ATB and enqueue ready commands |
| 3 | `BattlePendingAction_TransferToExecQueue` | `0x4847F0` | Move pending actions into the execution queue |
| 4 | `BattleArbitration_SelectNextAction` | `0x485460` | Pick the next queued action; monster slots enter the AI VM |
| 5 | `BattleAction_ResolveSpecialActionAndUpdateDamage` | `0x485160` | Resolve the action and bridge to damage/status handling |
| 6 | `BattleTaskQueue_Tick` | `0x500CC0` | Dispatch presentation tasks |

## Preemptive / back attack

`computeBattleSurpriseAttack` (renamed from `Battle_InitPreemptiveBackAttackStatus`) runs during battle initialization after scene data has been loaded. Scripted battle flags can force or suppress specific outcomes.

| Flag | Value | Effect |
|------|-------|--------|
| bit 7 | `0x80` | Suppress preemptive/back-attack; force normal start |
| bit 5 | `0x20` | Force preemptive attack |
| bit 6 | `0x40` | Force back attack |
| bit 2 | `0x04` | Enable inherited battle countdown timer |
| bit 1 | `0x02` | Suppress normal battle music handling |
| bit 0 | `0x01` | Set cannot-run state |

Random encounters normally use `ENCOUTER_BATTLE_FLAG == 0`. When no flag forces the result, the engine rolls `GetRandomInt()` and applies modifiers from enemy death immunity, party abilities and Initiative.

| Result value | Outcome | Effect |
|--------------|---------|--------|
| `0` | Normal | Normal starting positions |
| `1` | Preemptive | Party starts forward |
| `2` | Back Attack | Party receives back-attack status |
| `3` | Pincer | Known value, details not confirmed here |
| `4` | Side Attack | Enemy side receives back-attack status |

The result is stored in `BACK_PREEMTIVE_INFO`.

## Battle end

Battle end detection is part of the battle initialization/state machine family, not a separate module. `BATTLE_RESULT_CODE` stores the final result code used by the end transition and post-battle handling.

| Value | Meaning |
|-------|---------|
| `0` | Battle still active / no final result |
| `1` | Victory |
| `2` | Defeat or game-over path |
| `3` | Escape |

Note: Phoenix can intercept party wipe before game-over is committed. See [GF Summon Runtime](../gf-summon-runtime/) for the Phoenix auto-trigger path.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `FFModuleHandler_main_loop` | 0x4706B0 | Top-level module dispatcher (verified IDA function) |
| `computeBattleSurpriseAttack` (formerly documented as `Battle_InitPreemptiveBackAttackStatus`) | 0x48AFD0 | Preemptive/back-attack resolution (verified IDA function) |
| `BACK_PREEMTIVE_INFO` | 0x1D28E08 | Global variable/data, not a function |
| `BATTLE_RESULT_CODE` | 0x1CFF6E7 | Global variable/data, not a function (also documented as `battle_result_byte` on [Battle transition and module entry](../battle-transition-module/)) |
