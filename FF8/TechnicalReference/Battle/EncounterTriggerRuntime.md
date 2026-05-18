---
layout: default
parent: Battle
title: Encounter Trigger Runtime
permalink: /technical-reference/battle/encounter-trigger-runtime/
---

This page documents how field and world-map encounter systems select a scene id and hand it to the battle module.

1. TOC
{:toc}

## Summary

Both field and world-map random encounter systems ultimately select a battle scene id, request module `3` (battle), and let `FFModuleHandler_main_loop` launch the battle module. The battle module then reads `COMBAT_SCENE_ID` and loads the corresponding 128-byte entry from [scene.out](../battle-structure-sceneout/).

| Source | Scene id storage | Module request | Main selector |
|--------|------------------|----------------|---------------|
| Field random battle | `MenuState_opcode_menu_id` (`0x1CE4762`) | `globalFieldNextModuleID = 3` | `Field_Encounter_RollAndSelectScene` (`0x47CA90`) |
| Field scripted battle | `MenuState_opcode_menu_id` (`0x1CE4762`) | `globalFieldNextModuleID = 3` | `SCRIPT_BATTLE` (`0x523294`) |
| World map random battle | `WM_PENDING_SCENE_LO/HI` (`0x2036B4E/0x2036B4F`) | `WM_PENDING_MODULE_ID = 3` | `WM_Encounter_RollAndSelectScene` (`0x541C80`) |

## Field random encounters

`Field_Encounter_RollAndSelectScene` (`0x47CA90`) is called each frame from the field state machine (`Field_MainStateMachineTick`, `0x4789A0`).

### Guard conditions

Before danger processing, field random encounters are blocked when:

| Condition | Meaning |
|-----------|---------|
| `globalFieldNextModuleID == 1` or `7` | Already transitioning |
| `Field_IsCutsceneActive()` returns non-zero | Event/cutscene active |
| `VAR_MAP_ADDRESS->unused8[3] != 0` | Field disables encounters |
| `FIELD_STATE_MODE` is `2`, `3` or `4` | Menu / transition states |
| `FIELD_ENC_DISABLED == 1` | Temporary encounter disable flag |
| `RARE_ITEM_ABILITY_IN_IT & 0x08` | Enc-None active |

### Danger meter

The field encounter meter is a fractional accumulator. It increments by the current field's encounter rate, or half that rate with Enc-Half.

```c
if (RARE_ITEM_ABILITY_IN_IT & 0x04)
    FIELD_ENC_METER += (*FIELD_ENC_RATE_PTR) >> 1;
else
    FIELD_ENC_METER += *FIELD_ENC_RATE_PTR;
```

When the meter exceeds `0x100`, a "step" is processed and the meter keeps its fractional remainder.

### Danger rating and threshold

Each step adds a danger amount from field region data. The accumulated danger rating is compared against a shuffled 256-byte threshold table.

| Address | Name | Description |
|---------|------|-------------|
| `0x1CDC740` | `FIELD_ENC_METER` | Fractional encounter meter |
| `0x1CDC74A` | `FIELD_DANGER_RATING` | Accumulated danger |
| `0x1CD2FB8` | `FIELD_STEP_COUNTER` | Step counter, wraps at 256 |
| `0x1CDC748` | `FIELD_CYCLE_BONUS` | Increases by 13 every 256 steps |
| `0xB80A18` | `DANGER_LIMIT_TABLE` | 256-entry shuffled threshold table |
| `0x1CF3D48` | `FIELD_ENC_RATE_PTR` | Pointer to field encounter rate byte |

The threshold is:

```
threshold = FIELD_CYCLE_BONUS + DANGER_LIMIT_TABLE[FIELD_STEP_COUNTER]
```

An encounter triggers when `threshold < FIELD_DANGER_RATING`.

### Formation selection

When an encounter triggers, the field system selects from a 4-entry formation table at `FIELD_FORMATION_TABLE_PTR` (`0x1CF3D78`). The roll is based on `DANGER_LIMIT_TABLE[(TOTAL_ENCOUNTER + 1) & 0xFF]`.

| Roll range | Slot | Nominal probability |
|------------|------|---------------------|
| `< 0x80` | formation 0 | 50% |
| `< 0xC0` | formation 1 | 25% |
| `< 0xF0` | formation 2 | 18.75% |
| otherwise | formation 3 | 6.25% |

If the selected formation matches `FIELD_LAST_FORMATION_ID`, selection falls through to the next formation to avoid immediate repeats.

## Field scripted battles

Field scripts can force battles through the `BATTLE` opcode. `SCRIPT_BATTLE` (`0x523294`) pops the battle flag byte and scene id from the script stack:

```c
ENCOUTER_BATTLE_FLAG = script_pop();
MenuState_opcode_menu_id = script_pop();
globalFieldNextModuleID = 3;
```

See [069_BATTLE](../../field/field-opcodes/069-battle/) for the field opcode page.

## World-map random encounters

`WM_Encounter_RollAndSelectScene` (`0x541C80`) is called from `FFWorldDirector` (`0x53F4B0`) during the world-map frame tick.

### Guard conditions

| Condition | Meaning |
|-----------|---------|
| `RARE_ITEM_ABILITY_IN_IT & 0x08 == 0` | Enc-None must be inactive |
| `world_currentVehicle < 0x0A || world_currentVehicle == 128` | On foot, chocobo or car |
| `isStateOfMovement != 0` | Party must be moving |

Vehicle ids `>= 10` suppress random encounters except value `128`.

### Terrain and meter

World-map encounters use region and terrain:

```c
uint8_t region = wm_GetRegionNumber(WORLD_MAP_COORD_X, WORLD_MAP_COORD_Y);
uint8_t terrain = *(Worldmap_weirdregister0_LocationDRAW + 13);
```

Terrain types 27 and 28 suppress encounters. Otherwise, the region/terrain pair is matched against wmset encounter data.

The world-map meter increments by 16 each moving frame, or 4 with Enc-Half:

```c
WM_ENC_METER += 16 >> (2 * enc_half);
```

When `WM_ENC_METER > 256`, the meter resets to 0 and the system checks the threshold table.

| Address | Name | Description |
|---------|------|-------------|
| `0x2040A5C` | `WM_ENC_METER` | World-map encounter meter |
| `0x2040A5E` | `LOCOMOTION_METHOD` | Movement accumulator |
| `0x2040A60` | `WM_STEP_AND_BONUS` | Step counter and bonus byte |
| `0x2040A5F` | `WM_CYCLE_BONUS` | World-map cycle bonus |
| `0xC75D20` | `Encounter_RandomRollArray` | World-map copy of the danger threshold table |
| `0x20409E0` | `world_currentVehicle` | Current vehicle id |
| `0x20400A0` | `WM_LAST_FORMATION_ID` | Last world-map encounter id |

### Formation selection and handoff

World-map formations come from wmset encounter tables. There are 8 formations per terrain. If the selected formation matches `WM_LAST_FORMATION_ID`, the system can re-roll up to two times.

When the function returns success:

```c
WM_PENDING_MODULE_ID = 3;
WM_PENDING_SCENE_LO = scene_id;
WM_PENDING_SCENE_HI = scene_id_hi;
ENCOUTER_BATTLE_FLAG = 0;
TOWN_BATTLE_SCENE = 1;
```

Random world-map encounters therefore enter battle with `ENCOUTER_BATTLE_FLAG == 0`.

## Battle module handoff

Both field and world-map paths converge in the module handler.

| Path | Sequence |
|------|----------|
| Field | Field encounter/script writes `MenuState_opcode_menu_id` and `globalFieldNextModuleID = 3`; module handler stores `COMBAT_SCENE_ID` |
| World map | World director writes `WM_PENDING_MODULE_ID = 3` and scene bytes; module handler stores `COMBAT_SCENE_ID` |

The battle module then reads:

```
ReadSceneOutFileForSpecificEncounter(COMBAT_SCENE_ID, &CURRENT_ENCOUNTER_DATA_SCENE_OUT)
```

The loaded scene.out block contributes its own battle flags; scripted `ENCOUTER_BATTLE_FLAG` is merged during initialization.

## Function address summary

| Address | Name | Role |
|---------|------|------|
| `0x47CA90` | `Field_Encounter_RollAndSelectScene` | Field encounter tick: increment, check, select and trigger |
| `0x541C80` | `WM_Encounter_RollAndSelectScene` | World-map encounter tick |
| `0x54A7F0` | `World_Encounter_CheckAndTrigger` | World-map encounter orchestrator |
| `0x523294` | `SCRIPT_BATTLE` | Field script forced battle opcode |
| `0x48AFD0` | `Battle_InitPreemptiveBackAttackStatus` | Preemptive/back-attack resolution |
| `0x48B260` | `Battle_CheckPartyAbilityForPreemptive` | Party ability modifier |
| `0x52B3A0` | `Field_IsCutsceneActive` | Cutscene/event gate |
| `0x53F4B0` | `FFWorldDirector` | World-map state machine |
| `0x4706B0` | `FFModuleHandler_main_loop` | Module dispatcher and battle handoff |
