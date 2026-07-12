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

## Section dispatch

`MonsterAI_DispatchSection` routes execution by section index.

| Section | Name | Trigger | Description |
|---------|------|---------|-------------|
| 0 | Init | Monster appears | Runs once when the enemy enters battle. Calls `MonsterAI` on the Init code. |
| 1 | Turn | Enemy ATB ready | Runs each enemy turn and increments `number_turn`. Calls `MonsterAI` on the Turn code. |
| 2 | Counter | After being hit | **Monsters** (slot ≥ 3): gated on Death/Petrify/Berserk/Sleep/Stop/Linked-Escape, then calls `MonsterAI` on the Counter code. **Playable characters** (slot 0-2): does **not** run AI bytecode at all — instead it directly resolves the character's auto-counterattack (`Counter` ability, targets the last attacker), triggers Angelo's automatic response after Rinoa is hit, and runs Auto-Potion (uses Potion → Hi-Potion → Potion+ → Hi-Potion+ → X-Potion → Elixir depending on HP lost, only once HP lost exceeds 200). A separate function, `ReturnDamage_ApplyAccumulated`, accumulates and triggers "Return Damage"/reflect-style effects outside of this dispatch. |
| 3 | Death | HP reaches 0 | **Monsters**: calls `MonsterAI` on the Death code (can summon replacements, drop items, trigger events). **Playable characters**: triggers an Angelo auto-revive action instead of running any script. |
| 4 | Pre-hit | Before hit resolves | Calls `MonsterAI` on the Pre-hit code. Last-moment effects before damage commits. |
| 5 | Doom | Doom counter reaches 0 | Not AI bytecode — directly queues the `DOOM_FINISHED` command that kills the actor. |
| 6 | Kamikaze/revive | Fixed trigger | Not AI bytecode — directly queues the `KAMIKAZE_PHOENIX_PINION_OR_FAIL` command (Phoenix Pinion / kamikaze-style auto-revive path). |
| 7 | Odin / Gilgamesh | Auto-trigger | Special GF summon handler — queues the Odin/Gilgamesh/Phoenix summon command directly. |
| 8 | Angelo | Auto-trigger | Angelo auto-action handler — queues an Angelo automove command directly. |

For party slots (`0..2`), only sections 0, 1 and 4 run through the normal `MonsterAI` bytecode path; sections 2 and 3 are hardcoded character behavior as described above.

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
