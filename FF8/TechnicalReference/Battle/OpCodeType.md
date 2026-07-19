---
layout: default
parent: Battle
title: Opcode Type List
author: nihil, hobbitdur
permalink: /technical-reference/battle/opcode-type-list/
---

# Type list

## int

This type take literally the value of the parameter.
If the parameter is more than 1 byte, the int is in little endian
When speaking of int, we consider an unsigned int, so value are between 0 and 255 except state otherwise

## unused

Means the value is not used and could be changed by any value without any impact on the game

## Comparator

| Opcode dec | Opcode hex | Comparator pretty | Comparator IfritAI |
|------------|------------|-------------------|--------------------|
| 0          | 0x00       | ==                | ==                 |
| 1          | 0x01       | <                 | <                  |
| 2          | 0x02       | \>                | \>                 |
| 3          | 0x03       | ≠                 | !=                 |
| 4          | 0x04       | ≤                 | <=                 |
| 5          | 0x05       | ≥                 | \>=                |

## Target advanced specific

Designates a single combatant. Used by the IF subjects that read one actor (HP OF, STATUS OF, LEVEL OF, varX OF...).

| Opcode dec | Opcode hex | Text          | Comment                                                        |
|------------|------------|---------------|----------------------------------------------------------------|
| 0-15       | 0x00-0x0F  | Character     | Character ID (0=Squall, 1=Zell, ... 10=Ward), see resolution below |
| 16 + N     | 0x10 + N   | Monster       | Monster with com file ID N (c0mNNN), see resolution below      |
| 200        | 0xC8       | SELF          |                                                                |
| 203        | 0xCB       | LAST ATTACKER |                                                                |
| 220-227    | 0xDC-0xE3  | varA-varH     | The local var contains a battle slot ID (0-7)                  |

## Target advanced generic

Designates a whole side of the battle. Used by the team-wide IF subjects (HP IN TEAM, NUMBER OF MEMBER, STATUS OF ALL IN...) and by opcode **_targetStatus_**.

| Opcode dec | Opcode hex | Text       |
|------------|------------|------------|
| 200        | 0xC8       | ENEMY TEAM |
| 201        | 0xC9       | ALLY TEAM  |

## Target basic

Used by opcode [**_target_**](../battle-scripts/#opcode-0x04-4---target) (0x04).

| Opcode dec | Opcode hex | Text                  | Comment                                                        |
|------------|------------|-----------------------|----------------------------------------------------------------|
| 0-15       | 0x00-0x0F  | Character             | Character ID (0=Squall, 1=Zell, 2=Irvine, 3=Quistis, 4=Rinoa, 5=Selphie, 6=Seifer, 7=Edea, 8=Laguna, 9=Kiros, 10=Ward) |
| 16 + N     | 0x10 + N   | Monster               | Monster with com file ID N (c0mNNN)                            |
| 200        | 0xC8       | SELF                  |                                                                |
| 201        | 0xC9       | RANDOM ENEMY          | Random alive character (slots 0-2)                             |
| 202        | 0xCA       | RANDOM ALLY           | Random alive monster; falls back to slot 3 if none alive       |
| 203        | 0xCB       | LAST ATTACKER         |                                                                |
| 204        | 0xCC       | ALL ENEMIES           | Slots 0-2                                                      |
| 205        | 0xCD       | ALL ALLIES            | Slots 3-7                                                      |
| 206        | 0xCE       | EVERYONE              | Slots 0-7                                                      |
| 207        | 0xCF       | RANDOM NONSELF ALLY   | Arconada; targets self if it is the only ally left             |
| 208        | 0xD0       | RANDOM ENEMY EACH HIT | Meteor, Omega Weapon with Terra Break                          |
| 209        | 0xD1       | NEW ALLY              | Shiva; the slot of the last monster that entered combat        |
| 220-227    | 0xDC-0xE3  | varA-varH             | The local var contains a battle slot ID (0-7)                  |
| 228-255    | 0xE4-0xFF  | Slot pairs (modded)   | Vanilla: unmatchable, fizzles. With the TargetTwoSlot FFNx patch: fixed battle-slot pairs (see below) |

### Target byte resolution

The interpreter resolves the target byte into a 16-bit battle target mask, where bit N = battle slot N (bit 0-2 = characters, bit 3-7 = monsters), plus flag bits:

| Bit    | Meaning                                            |
|--------|----------------------------------------------------|
| 0x0001-0x0084 | Battle slots 0-7                            |
| 0x2000 | New random target on each hit (set by value 208)   |
| 0x4000 | Can target dead actors (revive)                    |
| 0x8000 | Multi-target (set by values 204, 205, 206 and 208) |

The 0x8000 flag does **not** mean "use these slot bits as a group". When the action executes, `processMultiHitAttackExecution` validates a flagged mask through `expandTargetMaskToValidSide`, which ignores the individual slot bits and returns every valid slot **on the side the mask points to** (mask ≤ 0x0007 = the character side, anything above = the monster side, exactly 0x00FF = everyone). This is invisible in vanilla because the flagged masks are always whole sides already, but it means an exe patch producing an arbitrary subset (e.g. slots 0+2 = 0x0005) must leave 0x8000 **clear**: the unflagged path goes through `getClosestTargetMaskValid`, which intersects the exact bits with the valid-slot mask (its closest-slot fallback only engages when no masked slot is targetable). A multi-bit unflagged mask is processed correctly: every surviving bit gets its own damage computation and result entry.

Resolution rules:

- Values **200-209** and **220-227** follow the comment column above. For the local vars, the mask is computed as `1 << var`: the variable holds a single battle slot ID, so it always resolves to exactly one slot.
- Any **other value** is looked up against the com file ID of each battle slot, in slot order: character slots hold their character ID (0-15 range), monster slots hold their com file ID + 16. The **first** matching slot is taken, so targeting a monster by ID reaches only one instance of it. If no slot matches, a "no target found" flag (bit 31 of the internal 32-bit mask) is set and the action has no target.
- Every value therefore resolves to either a single slot or one of the fixed multi-slot groups (204/205/206/208). There is no encoding for an arbitrary combination of slots (for example slots 0 and 2 only): to hit such a combination a script has to run the action once per slot, using a local var (values 220-227) as the target, or an exe patch has to add a new target value.
- Values **210-219** are dead space: they fall through to the com file ID scan, but monster com file IDs stop at 215 (c0m199 + 16, and only c0m000-143 are reachable in vanilla), so 216-219 can never match anything and always resolve to "no target found". This makes them safe values for mods to repurpose via an exe patch (the switch dispatches through a byte index table at `0x48A61C` indexed by value-200, then a 12-entry jump table at `0x48A5EC` whose base address sits at `0x489B28`). Values **11-15** are equally dead in every possible setup (character IDs stop at 10, monster com file IDs start at 16), and values **228-255** as well; both of these ranges bypass the jump table (the range check `value-200 > 27` at `0x489B17` sends them straight to the com scan), so repurposing them requires detouring that branch rather than extending the jump table.

Vanilla scripts do use the sub-200 value space (scan of all c0m000-143 AI sections, opcode 0x04 + IF specific targets):

| Values | Used by |
|--------|---------|
| 0-5 (Squall-Selphie) | Tri-Point, Seifer 2nd, Edea 1st, Adel, Ultimecia+Griever, Ultimecia final, and character-condition IFs in ~20 monsters |
| 9-10 (Kiros, Ward) | Esthar Soldier (Terminator), Laguna dream logic |
| 28 (Sphinxara) | Sphinxaur, to hand over to its second form |
| 89 (Wedge) | Biggs, to interact with his partner |
| 139-140 (Griever fusion forms) | Griever and the fusion, chaining the final boss forms |
| 17, 23, 55-56, 87-88, 111-112, 124, 143 | IF conditions on partner monsters (GIM52A/SAM08G, Vysage's Lefty/Righty, G-Soldier/Elite Soldier, Granaldo/Raldo, Paratrooper, Ultimecia's check of com ID 143) |

All other sub-200 values (177 of them) are never referenced by any vanilla AI. Within those, values **160-199** deserve a special mention: since only c0m000-143 are loadable in vanilla, com file IDs stop at 159 and this whole range is unmatchable — dead space like 216-219. However, a mod that lifts the c0m144 load cap makes com IDs run up to 215, which reclaims 160-215 as real monster targets; a mod combining such an unlock with repurposed target values should therefore only repurpose 11-15, 216-219 and 228-255, which stay dead under every configuration.

# Monster line ability

In FF8, monster have 3 level of difficulty, by default at level 10, 20 and 30.   
For each level, the ability change.

An ability line correspond to a list of 3 abilities, with the first being at low level, second at medium level and third at high level.

A monster can have theoretically up to 255 ability line, even tho in practise 10 is already a lot.

So the value is the ID of the ability line, starting from 0. The line contains 3 [monster ability]({{site.baseurl}}/technical-reference/list/ability-list/#monster-ability)

# Local var

Local variable of unsigned byte type, used by AIs.    
Here the list of all available local vars and their respective IDs:

| Opcode dec | Opcode hex | IfritAI name |
|------------|------------|--------------|
| 220        | 0xDC       | varA         |
| 221        | 0xDD       | varB         |
| 222        | 0xDE       | varC         |
| 223        | 0xDF       | varD         |
| 224        | 0xE0       | varE         |
| 225        | 0xE1       | varF         |
| 226        | 0xE2       | varG         |
| 227        | 0xE3       | varH         |
| 228        | 0xE4       | varI         |

When used as a parameter for the opcode [**_target_**](../battle-scripts/#opcode-0x04-4---target):

| Value | Resulting target |
|-------|------------------|
| 0     | Battle slot 0    |
| 1     | Battle slot 1    |
| 2     | Battle slot 2    |
| 3     | Battle slot 3    |
| 4     | Battle slot 4    |
| 5     | Battle slot 5    |
| 6     | Battle slot 6    |
| 7     | Battle slot 7    |

_Battle slots_ from 0 to 2 represent the playable characters in menu order, 3 to 7 represent monsters, in [scene.out](../battle-structure-sceneout/) declaration order.  

# Savemap var

Not sure what does it correspond, but this is info that can be re-used between fight

# Global map

This are variable that can be reused anywhere in the game. Here the list known and when it is used for AI

| Opcode dec | Opcode hex | var_name     | Used for                                        |
|------------|------------|--------------|-------------------------------------------------|
| 81         | 0x51       | GlobalVar81  | TonberryDefeated                                |
| 82         | 0x52       | GlobalVar82  | TonberrySrIsDefeated                            |
| 83         | 0x53       | GlobalVar83  | UfoIsDefeated                                   |
| 84         | 0x54       | GlobalVar84  | FirstBugSeen                                    |
| 85         | 0x55       | GlobalVar85  | FirstBombSeen                                   |
| 86         | 0x56       | GlobalVar86  | FirstT-RexaurSeen                               |
| 87         | 0x57       | GlobalVar87  | LimitBreakIrvine                                |
| 96         | 0x60       | GlobalVar96  | WedgeAppeared, omegaWeaponFightedButNotDefeated |
| 97         | 0x61       | GlobalVar97  |                                                 |
| 98         | 0x62       | GlobalVar98  | ElvoretAppeared                                 |
| 102        | 0x66       | GlobalVar102 | FirstBugSeen                                    |

## Stat

| Opcode dec | Opcode hex | Text     |
|------------|------------|----------|
| 0          | 0x00       | Strength |
| 1          | 0x01       | Vitality |
| 2          | 0x02       | Magic    |
| 3          | 0x03       | Spirit   |
| 4          | 0x04       | Speed    |
| 5          | 0x05       | Evade    |

## Engine addresses (FF8 PC 2000 EN)

| Function / location                             | Address    |
|-------------------------------------------------|------------|
| `MonsterAI` (AI byte-code interpreter)          | `0x487DF0` |
| Opcode dispatch jump table (61 entries, index = op_id-1) | `0x48A0B8` |
| Opcode 0x04 target byte resolution switch       | `0x489B01` |
| IF-condition specific-target resolution         | `0x488B83` |
| `processMultiHitAttackExecution` (mask → per-target damage) | `0x48E830` |
| `expandTargetMaskToValidSide` (0x8000 path, side expansion) | `0x48EE50` |
| `getClosestTargetMaskValid` (exact bits + closest fallback) | `0x48EEB0` |

### Target-value pairs 228-255 (TargetTwoSlot patch)

The FFNx **TargetTwoSlot** patch repurposes the 28 unconditionally-free `target`
values 228-255 so each one hits a fixed pair of battle slots in a single action
(each target rolled independently). The value byte is used as-is (opcode 0x04
stays size 1), so IfritAI authors them directly and the tool needs no code
change. Enumeration is `a < b` over slots 0-7; the engine sets
`target_info_mask = (1<<a)|(1<<b)` with the 0x8000 flag clear so the exact two
bits survive validation. Slots 0-2 are the party characters, 3-7 the monsters.

| Val | Slots | Val | Slots | Val | Slots | Val | Slots |
|-----|-------|-----|-------|-----|-------|-----|-------|
| 228 | 0+1 | 235 | 1+2 | 242 | 2+4 | 249 | 3+7 |
| 229 | 0+2 | 236 | 1+3 | 243 | 2+5 | 250 | 4+5 |
| 230 | 0+3 | 237 | 1+4 | 244 | 2+6 | 251 | 4+6 |
| 231 | 0+4 | 238 | 1+5 | 245 | 2+7 | 252 | 4+7 |
| 232 | 0+5 | 239 | 1+6 | 246 | 3+4 | 253 | 5+6 |
| 233 | 0+6 | 240 | 1+7 | 247 | 3+5 | 254 | 5+7 |
| 234 | 0+7 | 241 | 2+3 | 248 | 3+6 | 255 | 6+7 |

Implementation: the target sub-switch range check `cmp edi,0x1B; ja 0x489CD5`
(edi = value-200) at `0x489B17` fires for value 228-255; the patch repoints that
`ja` (rel32 at `0x489B19`) to a stub that looks the value up in a 28-byte
pair-mask table, writes the mask to the interpreter local `target_info_mask`
(`[esp+0x78]`), and rejoins the opcode loop. Values that are not 228-255 fall
through to the untouched com-file-id scan (`dl` = value byte is preserved).

### Adding a mask-target opcode (mod)

The interpreter's main opcode switch is a jump table at `0x48A0B8` indexed by
`op_id - 1`; op_ids above 0x3D and the in-range gaps **0x0A, 0x10, 0x14** all
point at the no-op loop head `0x487EBA`, so those three are free opcode slots.
Repointing one entry (e.g. op 0x10 at `0x48A0F4`) to a stub that reads the next
stream byte and stores it to the interpreter local `target_info_mask`
(`[esp+0x78]`) yields a clean new opcode whose parameter byte is a full 8-bit
slot bitmask — the general form of "attack an arbitrary set of slots". The stub
must leave the 0x8000 flag clear so the exact bits survive validation (see
above). An FFNx implementation of this (`targetMask`, op 0x10) lives in the
community battle-AI patch.

