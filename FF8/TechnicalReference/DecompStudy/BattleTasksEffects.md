---
layout: default
title: Battle tasks and action effects
parent: Battle
permalink: /technical-reference/battle/tasks-effects/
---

1. TOC
{:toc}

# Battle tasks and action effects

The battle module's internal scheduler — the task system that sequences windows, captions, stage loads, action animations, magic effects and damage popups — and the full pipeline from an executed command to the numbers on screen. Complements [Battle module runtime]({{ site.baseurl }}/technical-reference/battle/module-runtime/) and [Battle UI]({{ site.baseurl }}/technical-reference/battle/battle-ui/). Addresses for FF8_EN.exe, image base 0x400000.

## Task system

30 task slots of 12 bytes at `BATTLE_TASK_SLOT`, linked-list managed by `BATTLE_TASK_MANAGER`:

```
+0  u8   list index
+1  u8   priority (high nibble) | state (low nibble: 0 pending, 8 deferred, 0xF done)
+2  u16  task id
+4  ptr  callback (or data pointer, per task)
+8  u32  packed parameters
```

Tasks enter through `addElementBattleStack(id, priority, data)` and run each frame in `BattleTaskMainHandler`, gated by a priority threshold. Special id 0x6B purges pending action tasks below a given priority. A separate small **UI queue** (3 slots, `BattleTask_UI_Enqueue`) carries window requests.

### Task id table

| Id | Effect | Id | Effect |
|----|--------|----|--------|
| 1 | camera reset | 0x68 | **execute action sequence** |
| 3/4 | fade/transition helpers | 0x69 | hide selection triangle |
| 8 | print caption text | 0x6A | AI death (transform) |
| 9 | load b0wave.dat | 0x6C/0x6D | set/unset RUNNING anim (all) |
| 0xA | execute callback | 0x6E/0x72 | set/unset PREPARING_ATTACK |
| 0x11 / 0x12 | open command window / next character (UI queue) | 0x6F | chain transformation |
| 0x40 / 0x41 | HUD show / hide (UI queue) | 0x70 | enable AI |
| 1002 | load battle stage file | 0x71 | callback when anim unlocked |
| 1003 | stage post-load | 0x73 | victory pose (R0WIN) |
| | | 0x74–0x77 | wait-ready / status→anim / anim status bits |

## Action execution pipeline

1. Director (FIGHTING) → `BattleTurn_ProcessActionQueue` → `BattleAction_ExecuteCommand` — handles Triple/Double casts, Berserk/Confuse retargeting, Angel Wing.
2. `computeCommandAction` runs the [damage formulas]({{ site.baseurl }}/technical-reference/battle/formulas/); `computeTargetData` fills `TARGET_DATA[]` (damage dealt, hit type, statuses) and `BATTLE_TASK_68_DATA` (magic effect id, command type, target list). Reflected spells re-queue as bounced casts here.
3. Task **0x68** is enqueued with that data (plus a task 8 caption). Next frame, `BattleTask68_DispatchActionSequence` picks the per-command tick: physical, GF cinematic, or default magic.
4. The magic tick loads the effect (`Magic_GetIDLoad`, effect id = kernel magic id + 4), waits, then runs the procedural `MAGIC_EFFECT_LOGIC_CALLBACK` — which also selects the battle camera sequence (the camera VM shares the AnimSeq byte-code VM).
5. Attacker/target animations run in the AnimSeq VM; its opcodes **B2/B7** call `ApplyActionResultToTarget`: status→animation, hit reaction, crit flash — and the **damage popup spawn**, plus drain-back application to the attacker.
6. Effect-end wait → cleanup → the task completes; victory/turn-end checks happen back in the director.

## Damage number popups

`BattleFx_DamageNumbers_Spawn` — one per target (and a second for drain-back on the attacker), suppressed when the result is reported as text (LV Up/Down…) unless it's a MISS.

* **Glyphs** come from the AICON.SP1 sprite atlas: digits = glyph 56+digit (up to 4, leading zeros trimmed), MISS = glyphs 70+69 stacked, reflected = wide glyph 16; 8 px x-advance, centered by 4 px per digit.
* **Colors**: white modulate (0x808080) for damage, green (0x408040) for healing; frames 8–9 fade out with a palette scaler + semi-transparency.
* **Animation**: 10 frames, y-offsets from the animation table — damage **bounces** (−12,−16,−17,−17,−16,−12,−13,−13,−12,−12), healing **rises steadily** (−12…−21).
* **Position**: projected **once** at spawn — an anchor 0xF0 above the target model (`GetEffectSpawnPosition`) through the battle camera (`TransformWorldCoordinateToProjectedSpace`), clamped to x∈[32,288], y∈[32,152]. The popup does not track the target afterwards.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `BattleTask_InitManager` | 0x500C00 | Initializes the task manager |
| `BattleTaskMainHandler` | 0x500CC0 | Per-frame task-list runner |
| `addElementBattleStack` | 0x500DF0 | Enqueues a task |
| `BattleTask_UI_Enqueue` | 0x4AD620 | Enqueues a UI window request |
| `BattleTurn_ProcessActionQueue` | 0x485460 | Executes the queued player/AI actions |
| `BattleAction_ExecuteCommand` | 0x485610 | Handles Triple/Double, Berserk/Confuse retargeting, Angel Wing |
| `computeCommandAction` | 0x48D200 | Runs the damage/heal formulas for the executed command |
| `computeTargetData` | 0x48EF80 | Fills per-target result data (damage, hit type, statuses) |
| `BattleTask68_DispatchActionSequence` | 0x50A790 | Picks the per-command action-sequence tick |
| `BattleTask68_LoadActionContext` | 0x50BF90 | Loads context for task 0x68 |
| `ApplyActionResultToTarget` | 0x506690 | AnimSeq opcode handler for hit reaction/status/damage popup |
| `BattleFx_DamageNumbers_Spawn` | 0x5068B0 | Spawns a damage/heal number popup |
| `BattleFx_DamageNumbers_TaskTick` | 0x5069B0 | Per-frame tick of an active damage popup |
| `BattleFx_DrawGlyphString_AICON_SP1` | 0x4A93D0 | Draws the digit/MISS glyphs from the AICON.SP1 atlas |
| `BATTLE_TASK_SLOT` | 0x1D96AB8 | Global variable/data, not a function — 30×12 B task slot array |
| `BATTLE_TASK_MANAGER` | 0x1D96D68 | Global variable/data, not a function — linked-list task manager state |
| `TARGET_DATA[]` | 0x1D28344 | Global variable/data, not a function — per-target result buffer |
| `BATTLE_TASK_68_DATA` | 0x1D280C4 | Global variable/data, not a function — action-sequence task data |
| `BattleFx_DamageNumbers_AnimTable` | 0xB8B830 | Global variable/data, not a function — popup y-offset animation table |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
