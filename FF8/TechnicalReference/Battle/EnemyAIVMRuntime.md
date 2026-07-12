---
layout: default
parent: Battle
title: Enemy AI VM Runtime
permalink: /technical-reference/battle/enemy-ai-vm-runtime/
---

This page documents the runtime interpreter used for enemy behavior scripts in c0mxxx.dat section 8. For per-opcode authoring details, see [Battle Scripts](../battle-scripts/).

Note: the function names used in this page are the real names in the IDA database (verified 2026-07), not placeholders. An address lookup table is at the [bottom of this page](#function-address-reference) for anyone following along in a disassembler.

1. TOC
{:toc}

## Architecture

Enemy AI is executed through a chain of four layers:

```
BattleTurn_ProcessActionQueue
  -> BattleAction_ExecuteCommand
     -> MonsterAI_DispatchSection
        -> MonsterAI
```

- **BattleTurn_ProcessActionQueue** is the top-level per-turn scheduler. It walks the queued battle-action linked list, skips actors that are Petrified/Asleep/Stopped, and loops `BattleAction_ExecuteCommand` once per sub-hit (used for multi-hit sequences like Renzokuken) until it fails or the alive-count sentinel (`255`) is hit.
- **BattleAction_ExecuteCommand** is *not* AI-specific. It is the generic command executor for every queued action, player or monster: it resolves multi-target magic (Triple/Double), confusion/berserk auto-targeting, Angel Wing effects, GF compatibility updates, item consumption, and Renzokuken/Duel/Limit-break paths (Zell, Irvine, Lionheart). It only calls into `MonsterAI_DispatchSection` when the queued action's command type is `COMMAND_NO_COMMAND` — i.e. when nothing has decided what this monster is doing yet and the AI script needs to run.
- **MonsterAI_DispatchSection** routes to one of the AI script sections (see table below) and, for the sections backed by actual bytecode, calls `MonsterAI` with a pointer into the right code sub-section.
- **MonsterAI** is the bytecode interpreter itself — it reads and executes the opcodes documented in [Battle Scripts](../battle-scripts/).

Damage application also routes back into AI. The Pre-hit section (4) is dispatched **synchronously, inside the damage-application call itself** — after the engine computed damage and picked the default hit/death reaction animation, but before the hit data is committed:

```
Battle_applyDamage (per target)
  -> applyDamageAndHandleDeath
       -> MonsterAI_DispatchSection(section=4 PRE-HIT)   // runs inline, mid-hit
  -> computeTargetData                                   // commits hit data (incl. reaction animation)
```

This inline timing is what allows the `setHitAnim` opcode to override the reaction animation of the very hit being processed (see [Battle Scripts](../battle-scripts/)), and why launching attacks from the Pre-hit section crashes: the engine is still resolving the current action. Counter (2) and Death (3) behavior is queued as battle tasks and runs after the hit resolves.

## Data source

Enemy scripts are stored in `.dat` section 8.

| Offset | Length | Description |
|--------|--------|-------------|
| 0 | 4 bytes | Number of sub-sections (normally 3) |
| 4 | 4 bytes | Offset to AI sub-section, relative to section start |
| 8 | 4 bytes | Offset to text offsets |
| 12 | 4 bytes | Offset to text sub-section |

The AI sub-section contains offsets to code sub-sections:

| Offset | Length | Description |
|--------|--------|-------------|
| 0 | 4 bytes | Offset to Init code |
| 4 | 4 bytes | Offset to Turn code |
| 8 | 4 bytes | Offset to Counter code |
| 12 | 4 bytes | Offset to Death code |
| 16 | 4 bytes | Offset to Pre-hit code |

The bytecode pointer for a sub-section is:

```
ai_subsection_base + offset[section_index]
```

## How sections get scheduled: the AI action queue

With one exception (Pre-counter, see below), AI sections are never executed on the spot. Instead, `queueAISectionAction(slot, section, list)` inserts a pseudo-action into the battle action queue: `command_type = 0xFF` (NO_COMMAND) and `task_type = section index`. When the turn scheduler (`BattleTurn_ProcessActionQueue` → `BattleAction_ExecuteCommand`) later pops an action whose command type is `0xFF`, it calls `MonsterAI_DispatchSection(slot, task_type)`. This is how Init, Turn, Counter, Death, Doom, Regen, Odin/Gilgamesh/Phoenix and Angelo behavior all reach the dispatcher.

Who queues what:

| Queued section | Queued by | When |
|----------------|-----------|------|
| 0 Init | `setMonsterPresence` | Every time a monster becomes present — at battle start and whenever a monster is brought in by `enter`/`assignSlot`/`enterWithAnim`. This is why a re-entering monster re-runs its Init code. |
| 1 Turn | ATB system | When an enemy's ATB bar fills. |
| 2 Counter / 3 Death | End-of-action processors (`processBattleActionCompletion` and two variants) | During damage application, each victim is stamped with a *pending reaction section* (field `value_is_2_when_targeted` in the battle slot: 2 = was hit and survived, 3 = died with scripted death) plus an `inAction` order number. When the attacker's action fully completes, the processor walks all stamped slots **in the order they were hit** and queues each one's Counter (if alive) or Death section. This deferred, ordered mechanism is why Counter always runs after the attack fully resolves. |
| 5 Doom | `computeTimerStatus` | The per-slot Doom timer expired. |
| 6 Regen | `computeTimerStatus` | Regen HP tick — queued every 60/speed frames, where speed is 2 normally, 3 under Haste, 1 under Slow, 0 under Stop (and Sleep pauses the timers). |
| 7 Odin / Gilgamesh / Phoenix | `rollOdinAutoSummon`, `rollGilgameshAutoSummon`, `computePhoenixInvoc` | Battle-start (or condition-based) random rolls, queued **on the first enabled character slot** — the auto-summon acts through a party slot, not a monster slot. See details below. |
| 8 Angelo | `queueAngeloAutoAction(action, target_mask)` | Angelo auto-actions outside the hit-reaction path. |

Section 4 (Pre-counter) is the sole exception: it is dispatched **synchronously** from inside `applyDamageAndHandleDeath`, mid-hit (see below). It never goes through the queue.

## Section dispatch

`MonsterAI_DispatchSection` routes execution by section index.

| Section | Name | Trigger | Description |
|---------|------|---------|-------------|
| 0 | Init | Monster becomes present | Runs when the monster enters battle (including scripted reinforcements). Calls `MonsterAI` on the Init code. |
| 1 | Turn | Enemy ATB ready | Runs each enemy turn and increments `number_turn`. On a monster's *first* turn it also clears the Back-Attack status. Calls `MonsterAI` on the Turn code. |
| 2 | Counter | Queued after each resolved action that hit this actor | **Monsters** (slot ≥ 3): gated on Death/Petrify/Berserk/Sleep/Stop/Linked-Escape, then calls `MonsterAI` on the Counter code. **Playable characters** (slot 0-2): does **not** run AI bytecode at all — instead it directly resolves the character's auto-counterattack (`Counter` ability, targets the last attacker), triggers Angelo's automatic response after Rinoa is hit, and runs Auto-Potion (uses Potion → Hi-Potion → Potion+ → Hi-Potion+ → X-Potion → Elixir depending on HP lost, only once HP lost exceeds 200). A separate function, `ReturnDamage_ApplyAccumulated`, accumulates and triggers "Return Damage"/reflect-style effects outside of this dispatch. |
| 3 | Death | Queued when a scripted-death monster dies | **Monsters**: calls `MonsterAI` on the Death code (can summon replacements, drop items, trigger events). Note the death-deferral mechanic described in the Pre-counter section below. **Playable characters**: triggers an Angelo auto-revive action instead of running any script. |
| 4 | Pre-counter (pre-hit) | Synchronous, mid-hit | Calls `MonsterAI` on the Pre-counter code, from *inside* the damage-application code. See the dedicated section below — this one behaves like no other. |
| 5 | Doom expiry | Doom timer reached 0 | Not AI bytecode — directly issues the self-targeted `DOOM_FINISHED` command that kills the actor. Skipped if the actor is already dead. |
| 6 | Regen tick | Regen timer tick | Not AI bytecode — directly issues the self-targeted Regen heal-tick command (internally the same multi-purpose "system effect" command family as the Phoenix-Pinion/kamikaze effects, sub-type 4). Skipped if the actor is already dead. |
| 7 | Odin / Gilgamesh / Phoenix | Auto-summon roll succeeded | Issues the `ODIN_GILGAMESH` cinematic command using a variant ID chosen by the roll: 0 = Odin, 1 = Phoenix (also fires a party-wide revive wave alongside), 7–10 = Gilgamesh with one of his four random weapons (Zantetsuken / Masamune / Excaliber / Excalipoor). Rolls: Odin 32/255 at battle start if owned and every enemy passes the eject-susceptibility check (this is what keeps Odin out of boss fights); Gilgamesh 8/255 if owned (replaces Odin); Phoenix 64/255 when a party member is down, once a Phoenix Pinion has been used at least once before. |
| 8 | Angelo | Angelo auto-action queued | Issues the `ANGELO_AUTOMOVE` command with the action ID and target mask that were stored by `queueAngeloAutoAction`. |

For party slots (`0..2`), only sections 0 and 1 run through the normal `MonsterAI` bytecode path; sections 2 and 3 are hardcoded character behavior as described above, and section 4 is only ever dispatched for monsters.

## Pre-counter (section 4) in depth

Pre-counter is unique among the sections; every property below is verified from the decompiled engine (2026-07).

**When exactly it runs.** For each individual hit of an action, the engine resolves damage in this order:

```
Battle_applyDamage(target)
  1. compute damage, pick default hit/death reaction animation from kernel data
  2. applyDamageAndHandleDeath(target, ...)
       - apply HP change, update statuses
       - stamp last-attacker info (slot, command, ability, element) on the target
       - >>> MonsterAI_DispatchSection(target, 4)   <<< pre-counter runs HERE
  3. computeTargetData(target)  — commits the hit data (incl. reaction animation)
```

Because it runs between steps 1 and 3, pre-counter is the only place where the **_setHitAnim_** opcode can override the reaction animation of the very hit being resolved — and because the engine is mid-action, queuing a new attack from here crashes the game.

**Gating flag.** Both pre-counter dispatch sites are gated on a per-slot flag (`0x10`, labelled `BATTLE_FLAG_DEATH_AI` in the IDA database). This single flag explains the long-standing empirical note that "pre-counter only runs on a killing blow if the monster's death section has code in it": the same flag gates both scripted death handling and pre-counter execution. (What exactly sets the flag at load time — death section content, pre-counter content, or both — has not been traced yet; the empirical evidence points at the death section.)

**On a surviving hit** (monster took damage but lives): pre-counter runs only if the hit came from a real attack (not a system effect), and only when no further hits of the same action are pending — i.e. for a multi-hit attack it runs once, on the final hit. The target is then stamped with pending-reaction = 2 so its Counter section gets queued when the action completes.

**On a killing hit** (monster with the death-AI flag): pre-counter runs, and then the engine **removes the Death status it just applied**. The monster is technically alive again; it is stamped with pending-reaction = 3 so its Death section gets queued instead. Death is thereby *deferred to the script*: the queued Death section must eventually execute the **_die_** opcode (or the monster fights on at 0 HP — the classic softlock documented in [Battle Scripts](../battle-scripts/)). Monsters *without* the flag skip all of this and die immediately with the standard death handling (drops, cards, AP, reaction animation 3).

**Execution order for one hit** therefore is: pre-counter (mid-hit, synchronous) → death (queued, if killed) → counter (queued, if survived) — matching the empirically documented order, and explaining *why* it holds.

**What is safe inside pre-counter:** ifs, variable writes, stat/status changes, `setHitAnim`. **What is not:** anything that launches an action (attack, magic, item) — the action pipeline is busy resolving the current hit.

## VM interpreter

`MonsterAI` is the bytecode interpreter. It dispatches a switch table keyed on the opcode byte.

| Behavior | Detail |
|----------|--------|
| Fetch | Reads one opcode byte from the current bytecode pointer |
| Valid range | Opcodes `0x01..0x3D` (1-61) plus `0x00` (`stop`) |
| Stop | Opcode `0x00` (`stop`, shown as `return` in [Battle Scripts](../battle-scripts/)) ends script execution |
| Unused / no-op | Opcodes `0x0A`, `0x10`, `0x14`, `0x21` (10, 16, 20, 33) have no assigned meaning and fall through to a default no-op case |
| Branching | Opcode `0x23` (35, `jump`) reads a 16-bit jump; opcode `0x02` (`if`) conditionally skips by byte count |
| Berserk override | When the Turn section is requested for a monster with the Berserk status, its script is **skipped entirely**: the interpreter instead runs a small hardcoded fallback that picks a random alive player character as target and uses ability line 0. This is why Berserk-ed monsters lose all scripted behavior |

## Runtime variables

| Variable | Purpose |
|----------|---------|
| `op_id` | Current opcode byte |
| `opcode_param_1` | First inline parameter |
| `op_param_2`, `op_param_3` | Additional inline parameters |
| `command_type` | Prepared action command type |
| `section_position` | Prepared ability / spell id |
| `jump_value` | Branch offset for IF/JUMP |
| `monster_difficulty` | Difficulty tier (`0` low, `1` medium, `2` high) |
| `ai_scratch_var` | General-purpose scratch variable |

## Opcode groups

The complete authoring reference remains [Battle Scripts](../battle-scripts/), which lists all 59 opcodes with their exact numeric IDs. Runtime grouping observed in the interpreter:

| Group | Opcodes |
|-------|---------|
| Control flow | `stop`, `if`, `jump` |
| Attack setup | Magic, item, monster ability, ability info, drawn magic, execute action |
| Targeting | Direct target, status target, target mask, random ability target |
| Text / display | Display text, display and wait, text after attack, scan text |
| Variables | Local/global/savemap variable set/add operations |
| Monster management | Enter/leave, targetable/untargetable, enable/disable |
| Status / stat modification | Stat changes, status tests, elemental defense writes |
| Rewards / special | Give GF/Card/Item, Proof of Omega, Game Over, and other story-special behavior |

## Special GF-related sections

Section 7 is used for Odin / Gilgamesh auto-actions and section 8 for Angelo auto-actions. These paths queue direct actions instead of reading normal monster bytecode. See [GF Summon Runtime](../gf-summon-runtime/) for the dispatch path into `MagicList_Logic`.

## Function address reference

For readers following along in IDA / a disassembler. Names above are the ones actually set in the shared IDA database.

| Name | Address | Role |
|------|---------|------|
| `BattleTurn_ProcessActionQueue` | `0x485460` | Top-level per-turn scheduler, walks the queued action list |
| `BattleAction_ExecuteCommand` | `0x485610` | Generic command executor for player and monster actions; calls into AI dispatch only when no command is queued yet |
| `MonsterAI_DispatchSection` | `0x4877F0` | Routes to the correct AI section (Init/Turn/Counter/Death/Pre-hit/Doom/Kamikaze/Odin/Angelo) |
| `MonsterAI` | `0x487DF0` | Bytecode interpreter for the opcodes in [Battle Scripts](../battle-scripts/) |
| `applyDamageAndHandleDeath` | `0x494410` | Applies damage/healing, routes back into `MonsterAI_DispatchSection` for Counter/Death |
| `monsterAICompareValue` | `0x48A680` | Comparison operator implementation for `if` |
| `GenericTargetHasStatus` | `0x48A830` | Target status predicate |
| `getMagicTargetMask` | `0x4838C0` | Raw mask to target bitmask |
| `ReturnDamage_ApplyAccumulated` | `0x483EF0` | Accumulates and triggers "Return Damage" (reflect-style) effects |
| `GetNbMemberTargetGeneric` | `0x487590` | Count members in target mask |
| `howManyCharaNotDeadOrPetrify` | `0x4860A0` | Count alive party members |
| `howManyMonsterNotDeadOrPetrify` | `0x4860D0` | Count alive monsters |
| `queueAISectionAction` | `0x484720` | Inserts the NO_COMMAND (0xFF) pseudo-action that schedules an AI section for a slot |
| `processBattleActionCompletion` | `0x47DE70` | End-of-action processor: queues each hit victim's Counter/Death section in hit order (two near-identical variants exist at `0x47DDA0` and `0x47E120`) |
| `computeTimerStatus` | `0x483470` | Per-slot timer subsystem: Doom expiry (queues section 5), Regen ticks (queues section 6), Petrifying countdown, Shell/Protect/Reflect wear-off |
| `rollOdinAutoSummon` | `0x482E00` | Battle-start Odin roll (32/255, eject-susceptibility gate) → queues section 7 |
| `rollGilgameshAutoSummon` | `0x4831F0` | Gilgamesh roll (8/255, random weapon variant 7–10) → queues section 7 |
| `computePhoenixInvoc` | `0x483270` | Phoenix roll (64/255, needs a downed party member + prior Pinion use) → queues section 7 |
| `queueAngeloAutoAction` | `0x4831C0` | Stores an Angelo action ID + target mask → queues section 8 |
| `Battle_applyDamage` | `0x48FE20` | Per-hit damage resolution; hosts the synchronous pre-counter dispatch via `applyDamageAndHandleDeath` |
