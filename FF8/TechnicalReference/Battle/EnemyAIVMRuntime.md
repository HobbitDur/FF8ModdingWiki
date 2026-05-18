---
layout: default
parent: Battle
title: Enemy AI VM Runtime
permalink: /technical-reference/battle/enemy-ai-vm-runtime/
---

This page documents the runtime interpreter used for enemy behavior scripts in c0mxxx.dat section 8. For per-opcode authoring details, see [Battle Scripts](../battle-scripts/).

1. TOC
{:toc}

## Architecture

Enemy AI is executed through three layers when a monster becomes active:

```
BattleArbitration_SelectNextAction (0x485460)
  -> EnemyAI_PrepareTurnAction (0x485610)
     -> EnemyAI_DispatchSection (0x4877F0)
        -> EnemyAI_VM_ExecuteScript (0x487DF0)
```

Damage application also routes back into AI for counter/death behavior:

```
Battle_ApplyDamageOrHeal (0x494410)
  -> EnemyAI_DispatchSection(section=2 COUNTER)
  -> EnemyAI_DispatchSection(section=3 DEATH)
```

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

`EnemyAI_DispatchSection` (`0x4877F0`) routes execution by section index.

| Section | Name | Trigger | Description |
|---------|------|---------|-------------|
| 0 | Init | Monster appears | Runs once when the enemy enters battle |
| 1 | Turn | Enemy ATB ready | Runs each enemy turn and increments `number_turn` |
| 2 | Counter | After being hit | Checks death/petrify/berserk/sleep/stop gates first |
| 3 | Death | HP reaches 0 | Can summon replacements, drop items, trigger events |
| 4 | Pre-hit | Before hit resolves | Last-moment effects before damage commits |
| 5-6 | Special | Fixed actions | Queues predefined commands |
| 7 | Odin / Gilgamesh | Auto-trigger | Special GF summon handler |
| 8 | Angelo | Auto-trigger | Angelo auto-action handler |

For party slots (`0..2`), section 2 handles Counter ability, Cover and Return Damage rather than running enemy AI bytecode.

## VM interpreter

`EnemyAI_VM_ExecuteScript` (`0x487DF0`) is the bytecode interpreter. It dispatches a 61-case switch table at `0x487EDC`.

| Behavior | Detail |
|----------|--------|
| Fetch | Reads one opcode byte from the current bytecode pointer |
| Valid range | Opcodes `0x01..0x3D` plus `0x00` stop |
| Stop | Opcode `0x00` ends script execution |
| Default / NOP | Opcodes `0x0A`, `0x10`, `0x14`, `0x21` fall through to default |
| Branching | Opcode `0x23` reads a 16-bit jump; opcode `0x02` conditionally skips by byte count |

Observed interpreter signature:

```c
unsigned __int8 __usercall EnemyAI_VM_ExecuteScript@<al>(
    unsigned int p_ai_subsection_init_code@<ebp>,
    int          p_monster_slot_id,
    uint8_t*     p_ai_current_subcode,
    int          p_text_subsection,
    int          p_text_offset_section
);
```

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

The complete authoring reference remains [Battle Scripts](../battle-scripts/). Runtime grouping observed in the interpreter:

| Group | Opcodes |
|-------|---------|
| Control flow | `0x00` STOP, `0x02` IF_CONDITION, `0x23` JUMP |
| Attack setup | Magic, item, monster ability, ability info, drawn magic, execute action |
| Targeting | Direct target, status target, target mask, random ability target |
| Text / display | Display text, display and wait, text after attack, scan text |
| Variables | Local/global variable set/add operations |
| Monster management | Enter/leave, targetable/untargetable, enable/disable |
| Status / stat modification | Stat changes, status tests, elemental defense writes |
| Rewards / special | Drop/steal/reward and story-special behavior |

Note: wiki opcode names and byte labels should be reconciled against [Battle Scripts](../battle-scripts/) before editing individual opcode sections. Do not assume that a decompiler label maps directly to the existing IfritAI name.

## Important function addresses

| Address | Name | Role |
|---------|------|------|
| `0x487DF0` | `EnemyAI_VM_ExecuteScript` | Bytecode interpreter |
| `0x4877F0` | `EnemyAI_DispatchSection` | Section router |
| `0x485610` | `EnemyAI_PrepareTurnAction` | Turn preparation, context setup |
| `0x48A680` | `EnemyAI_CompareValues` | Comparison operator implementation |
| `0x482C90` | `EnemyAI_LookupAbilityByIndex` | `.dat` section 7 ability lookup |
| `0x48A830` | `EnemyAI_TargetHasStatus` | Target status predicate |
| `0x4838C0` | `EnemyAI_GetTargetMaskFromMask` | Raw mask to target bitmask |
| `0x483EF0` | `EnemyAI_SyncAIVarsToSlot` | Sync AI vars to battle slot data |
| `0x487590` | `EnemyAI_GetTargetMemberCount` | Count members in target mask |
| `0x4860A0` | `EnemyAI_CountAlivePartyMembers` | Count alive party members |
| `0x4860D0` | `EnemyAI_CountAliveMonsters` | Count alive monsters |

## Special GF-related sections

Section 7 is used for Odin / Gilgamesh auto-actions and section 8 for Angelo auto-actions. These paths queue direct actions instead of reading normal monster bytecode. See [GF Summon Runtime](../gf-summon-runtime/) for the dispatch path into `MagicList_Logic`.
