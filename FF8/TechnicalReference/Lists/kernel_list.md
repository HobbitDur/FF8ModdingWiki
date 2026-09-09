---
layout: default
title: Kernel
parent: List
permalink: /technical-reference/list/kernel/
---

# Target info

This byte is read by two independent paths, and a bit inert in one can still matter in the
other. `getTargetMaskFromInfo` / `computeTargetMaskDeadUnknown1` decode it when the engine
**auto-resolves** a target mask (AI attacks, auto-summons, item randomization); `sub_4AB190`
and the cursor engine `sub_4AA1D0` decode it when a **player** aims a command by hand. `0x04`
is the case that bites: no reader at all on the auto-resolve side, the cursor's side switch
on the player side.

| ID     | Description          |
|--------|----------------------|
| 0x0000 | None                 |
| 0x0001 | Dead — targets KO'd units (adds the revive bit 0x4000 to the target mask). In the player battle menu this only takes effect when the entry also has [Attack flag]({{site.baseurl}}/technical-reference/list/kernel#attack-flag) `0x80` set, which is what opens the cursor to KO'd units in the first place |
| 0x0002 | Multi-target spread — adds mask bit 0x2000 (`TARGET_MASK32_TARGET_SEVERAL`; IDA `TARGET_INFO_SEVERAL_HIT_SPREAD`) |
| 0x0004 | **Side switch** — lets the player move the target cursor to the other side. Suppressed by `0x0008`; see below. Skipped by the AI target-mask decoders, which is why it looks unused from that path |
| 0x0008 | Single Side — locks the cursor to one side; overrides `0x0004` |
| 0x0010 | Scope pair with `0x0020` — see below. Alone: one unit of the chosen side |
| 0x0020 | Scope pair with `0x0010` — see below. Alone: **everyone on BOTH sides** |
| 0x0040 | Enemy — selects the side **opposing the actor**, and it alone decides which side is targeted; `0x04`/`0x08` only govern whether the player may leave it. See below |
| 0x0080 | **Skip target selection** — the command takes no target at all; the engine picks one and commits immediately. See below |


### 0x0004 is the cursor's side switch, not an unused bit

`0x0004` has no reader in `getMagicTargetMask` / `computeTargetMaskDeadUnknown1`, which is why
it was previously recorded as unused — but those only cover the **AI / auto-resolve** path. The
**player target cursor** reads it, twice.

`sub_4AB190` (`0x4AB190`), which sets the cursor up, turns it into the set of target name
windows to open:

```c
if ( ((a2 >> 2) & 3) == 1 )          // a2 = TargetInfo: 0x04 set AND 0x08 clear
    v10 = 3;                         // both windows
else
    v10 = 2 - ((a2 & 0x40) != 0);    // one side only, picked by 0x40 Enemy
*(_BYTE *)(v9 + 11) = v10;
```

`v9 + 11` is consumed in `sub_4AB4F0` (`0x4AB4F0`), where bit 1 opens the party window (fixed
width 92, height from `ctx+22` = party row count) and bit 0 opens the enemy window (width from
`ctx+16`, the value `sub_4AA920` computes from the monster-slot name widths). The `0x40` branch
above confirms the assignment: Enemy set gives `1` = the enemy window, clear gives `2` = the
party window.

The cursor engine `sub_4AA1D0` (`0x4AA1D0`) then gates the actual side swap on the same
expression, at `0x4AA644`:

```asm
and  al, 0Ch
cmp  al, 4          ; TargetInfo & 0x0C == 0x04
jnz  ...            ; otherwise no switch is possible
```

Inside that branch, a direction press swaps the current-side mask `a1[7]` between `7` (party)
and `78h` (monsters), saving and restoring a remembered cursor slot per side in `a1[16]` /
`a1[17]` and playing cursor sound 1. That is the player pressing left/right to cross sides.

### Bits 2-3 are one 2-bit field, not two flags

`0x04` and `0x08` are never read independently — every reader tests the **pair**
`TargetInfo & 0x0C`, and only the value `0x04` does anything:

| `& 0x0C` | Meaning | Vanilla entries |
|----------|---------|----------------|
| `0x00` | Locked to one side (the side `0x40` names) | 56 |
| `0x04` | Both sides; the player can switch | 100 |
| `0x08` | Locked to one side — indistinguishable from `0x00` in every reader found | 53 |
| `0x0C` | Would behave as locked; never used | 0 |

So "Single Side" (`0x08`) has no effect of its own: its only observable role is to **veto**
`0x04`, and since vanilla never sets both, `0x00` and `0x08` are two spellings of the same
behaviour. Setting `0x08` alone changes nothing; clearing `0x04` is what locks the cursor.

**Reader census — complete.** Every reader of this byte in the binary:
`getMagicTargetMask` (`0x4838C0`), `getTargetMaskFromInfo` (`0x483880`),
`computeTargetMaskDeadUnknown1` (`0x483860`), `sub_483D20`, `sub_483D60`,
`Battle_PickRandomActionConfusedBerserk` (`0x483940`), `sub_4AB190`, `sub_4AA1D0`, plus
`linkedStockFieldCharData` / `setMenuFlagMagicOnCharaData` / `updateBattleItemData`, which only
copy it. `queuePlayerBattleCommand`, `BattleAction_ExecuteCommand` and `MonsterAI` (two sites)
load the raw byte and hand it straight to `computeTargetMaskDeadUnknown1` or
`getTargetMaskFromInfo` without testing anything themselves. Only `sub_4AB190` and `sub_4AA1D0`
touch bits 2-3, and both test the pair. Nothing anywhere tests `0x08` on its own.

The vanilla data agrees exactly. The bit is set on **100 of 209** entries that carry a TargetInfo
byte, and only ever on the three tables a player aims by hand:

| Section | With side switch |
|---------|------------------|
| Battle commands | 25 / 39 |
| Magic | 50 / 57 |
| Battle items | 25 / 33 |
| Junctionable GFs | 0 / 16 |
| Non-junctionable GF attacks | 0 / 16 |
| Renzokuken finishers | 0 / 4 |
| Blue magic (+ params) | 0 / 21 |
| Duel (+ params) | 0 / 18 |
| Rinoa limit part 2 | 0 / 5 |

Every auto-targeted or side-locked table has it clear on every single entry.

### Bits 4-5 are a scope pair, and 0x20 is not "one side"

Like bits 2-3, these are read as one 2-bit value, never as separate flags. Every decoder
switches on `target_info & 0x30` (`getTargetMaskFromInfo`, `getMagicTargetMask`, `sub_483D20`,
`sub_483D60`, `Battle_PickRandomActionConfusedBerserk`) and the cursor code on
`(target_info >> 4) & 3` (`sub_4AB190`, `sub_4AA1D0`):

| `& 0x30` | Resolves to | Vanilla entries |
|----------|-------------|-----------------|
| `0x00` | Every unit of the side `0x40` names — `getTargetMaskAllChara` / `getTargetMaskAllEnemy` | 74 |
| `0x10` | **One** unit of that side (random on the auto-resolve path) | 135 |
| `0x20` | `getMaskEveryone()` — but **broken in practice**, see below | 0 |
| `0x30` | Matches no branch; the raw `0x30` is returned | 0 |

The name "Everyone on one side" was wrong. `getMaskEveryone` returns **all eight slots** — the
three party slots *and* the five monster slots:

```c
TargetMask getMaskEveryone()
{
  return TARGET_MASK_SLOT_0_CHARA|TARGET_MASK_SLOT_1_CHARA|TARGET_MASK_SLOT_2_CHARA
       | TARGET_MASK_SLOT_3_MONSTER|...|TARGET_MASK_SLOT_7_MONSTER
       | TARGET_MASK_TARGET_SEVERAL;
}
```

So `0x20` means *both* sides at once, and it is the one value that ignores `0x40` entirely.
Note also that "whole side" is `0x00`, not `0x20` — clearing both bits is what targets a full
side. Nothing in vanilla ships with `0x20` or `0x30`.

#### Scope 0x20 works for enemy attacks, not for player commands

Set scope `0x20` on something the player uses and the cursor highlights every unit, then the
damage lands on the monsters only. The slot bits are discarded before damage is applied.

`getMaskEveryone` returns all slot bits **plus `TARGET_MASK_TARGET_SEVERAL` (0x8000)**, and the
player cursor builds the same shape (`sub_4AA1D0`: `BYTE1(v4) |= 0x80` then `v48 = v4 | v47`).
At damage time `processMultiHitAttackExecution` (`0x48E830`) branches on that flag:

```c
if ( special & TARGET_MASK_SPECIAL_BYTE_TARGET_SEVERAL )   // 0x8000 was set
    validated = expandTargetMaskToValidSide(current_hit_mask, revive);   // slot bits DISCARDED
else
    validated = getClosestTargetMaskValid(current_hit_mask, revive);     // exact bits kept
```

and `expandTargetMaskToValidSide` (`0x48EE50`) re-derives a single side:

| slot bits | result |
|-----------|--------|
| `== 0xFF` | every valid slot — both sides |
| `<= 0x07` | the party (slots 0-2) |
| anything else | **the monsters (slots 3-6)** |

**Bit 7 is a phantom slot.** There are only **7** battle slots, not 8:
`getMaskTargetTargetValid` (`0x485FB0`) and `getMaskTargetTargetValidAndAlive` (`0x485F60`) both
loop `i = 1248; i > -208; i -= 208` over `BATTLE_SLOT_DATA` (stride `0xD0`), giving indices 6..0 —
a **7-bit** mask whose maximum value is `0x7F`. Slots 0-2 are the party (the `i < 624` test) and
3-6 the monsters, so **four monsters maximum**. `TARGET_MASK_SLOT_7_MONSTER` (`0x80`) is declared
in the enum but no live-slot builder ever sets it, and the cursor code agrees — `sub_4AA190`
validates with `& 0x7F`, `sub_4AA920` uses `& 7` and `& 0x78`.

That splits the two paths:

- **Enemy / auto-resolved actions work.** `getMaskEveryone` returns the hardcoded constant
  `0x00FF | 0x8000` — phantom bit 7 included — so it matches `== 0xFF` exactly and every valid
  slot is hit.
- **Player commands cannot.** `sub_4AA1D0` builds the mask from the live slot set, which can
  never reach `0xFF`, so it always falls into the last branch. The menu highlights from the
  unexpanded mask, which is why the selection looks correct while the damage is one-sided.

So there is no data-only way to give a *player* action a both-sides hit — not even on a maximally
full battlefield, because the deciding bit is unreachable. It needs a patch at `0x48EE50` (test
"has bits on both sides" rather than `== 0xFF`). Scope `0x00` is immune throughout: its mask is
ANDed with the current side, so it always lands in one of the first two branches correctly.

### 0x0040 — which side, and relative to whom

In the player menu the answer is direct. `sub_4AB190` sets the cursor's starting side from this
bit alone:

```c
*(_BYTE *)(v9 + 14) = (a2 & 0x40) ? 120 : 7;   // 0x78 = monster slots, 7 = party slots
```

So `0x40` set = enemies, clear = allies. **`0x08` "Single Side" does not name a side** — it only
means "one side only", and *which* side is `0x40`'s job.

On the auto-resolve path the bit is **relative to whoever is acting**, which is easy to trip
over. The two decoders read it with opposite polarity:

| Decoder | Called by | `0x40` set resolves to |
|---------|-----------|------------------------|
| `getMagicTargetMask` (`0x4838C0`) | `MonsterAI` only | `getTargetMaskAllChara` — the **party** |
| `getTargetMaskFromInfo` (`0x483880`) | `queuePlayerBattleCommand`, others | `getTargetMaskAllEnemy` — the **monsters** |

The helpers themselves are absolute — `getTargetMaskAllChara` returns party slots 0-2,
`getTargetMaskAllEnemy` returns monster slots 3-7 (bit 7 being the phantom slot; only 3-6 ever
exist, see [scope 0x20](#scope-0x20-works-for-enemy-attacks-not-for-player-commands)) — so the
mirroring is deliberate: the kernel bit
means "the opposing side", and each decoder bakes in whose turn it is. The same `target_info`
byte therefore points at different concrete slots depending on whether a character or a monster
is acting.

`MonsterAI_DispatchSection` also calls `getTargetMaskFromInfo` (`0x487C96`, `0x487CE1`), which
looks at first like player polarity in a monster function — but those two calls read
`K_NONJ_GF_ATTACK_NAME_OFFSET.targetInfo`, the **non-junctionable GF attack** table, right
beside `IS_ODIN_GILGA_PHOENIX_SUMMONED_THIS_FIGHT`. They dispatch the *player-side*
auto-summons (Odin, Gilgamesh, Phoenix, Angelo, Boko, MiniMog), so player polarity is
correct there despite the function's name. The data confirms it: under player polarity the
four entries without `0x40` come out as party-targeting, and they are exactly Moogle Dance,
Angelo Recover, Angelo Reverse and Angelo Search — the four that help the party — while every
attacking summon (Zantetsuken, Rebirth Flame, the Choco* series, Excalibur, Masamune, Angelo
Rush, MoombaMoomba) has `0x40` and comes out monster-targeting. Read with monster polarity the
list would be exactly inverted.

### 0x0080 — "this command has no target"

`BattleMenu_ExecuteSelectedCommand` (`0x4BC770`) tests the byte as a **signed char**:

```c
if ( (menuFlags & 0x20) != 0 )      // direct-targeting command
{
  if ( targetInfo >= 0 )            // bit 0x80 CLEAR
    BattleMenu_OpenTargetSelection(...);   // normal interactive cursor
  else                              // bit 0x80 SET
  {
    ...                             // pick a slot: first enemy if 0x40 Enemy, else self
    BattleMenu_PendingSelections[n] = { command, mask, ... };   // commit straight away
  }
}
```

So the command skips target selection entirely, resolves a target itself and pushes the
selection into the pending queue. Two more sites enforce the same thing with the same sign test,
suppressing the cursor UI: `sub_4A9DF0` (`if (*(char *)(ctx + 4) >= 0 && ...)` — otherwise no
cursor finger is drawn) and `sub_4AA1D0` case 0 (`if (*((char *)a1 + 4) < 0) a1[21] = 0` — the
window-open animation counter is zeroed instead of set to 4096).

Vanilla sets it on five battle commands, but it is only *reached* by two of them:

| # | Command | `target_info` | menu bits | Reached? |
|---|---------|---------------|-----------|----------|
| 2 | Magic | `0xD4` | `0x80` | No — takes the sub-list branch |
| 3 | GF | `0xD4` | `0x80` | No — sub-list |
| 4 | Item | `0xD4` | `0x80` | No — sub-list |
| 8 | nomsg | `0xD4` | `0xA0` | **Yes** |
| 10 | Stock | `0xD4` | `0xA0` | **Yes** |

Only commands with menu bit `0x20` (direct targeting) ever reach the test. Magic, GF and Item
open a spell/GF/item list first, and from there the *chosen entry's* own `target_info` drives the
cursor — their command-level copy of `0x80` is dormant data. **Stock** is the case that shows the
intent: stocking a drawn spell onto yourself has no target to pick, so the cursor is skipped.

# Attack Type

| ID | Hex  | Description                          |
|----|------|--------------------------------------|
| 1  | 0x00 | None                                 |
| 2  | 0x01 | Physical Attack                      |
| 3  | 0x02 | Magic Attack                         |
| 4  | 0x03 | Curative Magic                       |
| 5  | 0x04 | Curative Item                        |
| 6  | 0x05 | Revive                               |
| 7  | 0x06 | Revive At Full HP                    |
| 8  | 0x07 | % Physical Damage                    |
| 9  | 0x08 | % Magic Damage                       |
| 10 | 0x09 | Renzokuken Finisher                  |
| 11 | 0x0A | Squall Gunblade Attack               |
| 12 | 0x0B | GF                                   |
| 13 | 0x0C | Scan                                 |
| 14 | 0x0D | LV Down                              |
| 15 | 0x0E | Summon Item?                         |
| 16 | 0x0F | GF (Ignore Target SPR)               |
| 17 | 0x10 | LV Up                                |
| 18 | 0x11 | Card                                 |
| 19 | 0x12 | Kamikaze                             |
| 20 | 0x13 | Devour                               |
| 21 | 0x14 | % GF Damage                          |
| 22 | 0x15 | Unknown 1                            |
| 23 | 0x16 | Magic Attack (Ignore Target SPR)     |
| 24 | 0x17 | Angelo Search                        |
| 25 | 0x18 | Moogle Dance                         |
| 26 | 0x19 | White Wind (Quistis)                 |
| 27 | 0x1A | LV? Attack                           |
| 28 | 0x1B | Fixed Damage                         |
| 29 | 0x1C | Target Current HP - 1                |
| 30 | 0x1D | Fixed Magic Damage Based on GF Level |
| 31 | 0x1E | Unknown 2                            |
| 32 | 0x1F | Unknown 3                            |
| 33 | 0x20 | Give Percentage HP                   |
| 34 | 0x21 | Unknown 4                            |
| 35 | 0x22 | Everyone's Grudge                    |
| 36 | 0x23 | 1 HP Damage                          |
| 37 | 0x24 | Physical Attack (Ignore Target VIT)  |


## Attack flag

| ID   | Meaning          |
|------|------------------|
| 0x03 | Damage-type pair (bits 0-1) — see below |
| 0x04 | Unused — no reader anywhere (also set on nothing in vanilla) |
| 0x08 | Break damage limit (dmg cap 9999 → 60000) |
| 0x10 | Reflectable — the spell can be bounced by Reflect status (`handleSpellReflection`) |
| 0x20 | Read **only for battle items** — CLEAR greys the row out and makes it unselectable (`updateBattleItemData`, `test byte, 20h`); see below. On magic / GF / Blue Magic / limits this bit is **inert**, even though it is set on virtually every player ability (an authoring convention: set on all player abilities, clear on all 384 enemy attacks) |
| 0x40 | Unused — no reader anywhere; an authoring marker for "restores HP or cures an ailment". See the enumeration below |
| 0x80 | "May target KO'd units" (`ATTACK_FLAG_REVIVE`) — a **menu targeting** bit, not a damage-time one; see below. Set on exactly Life and Full-life in the magic table, and on all 32 real battle items |

### 0x80 is menu targeting, not "revive on hit"

The name is misleading and the battle-item table makes it obvious: **32 of the 33 battle
items have `0x80` set**, Potion included — only the blank entry 0 lacks it. If the bit meant
"this action revives", every Potion would be a Phoenix Down. In the magic table it is set on
exactly two of 57 entries (Life, Full-life).

What actually revives is the separate **Attack type** byte — `Damage_ComputeReviveHP`
(`0x491940`) is reached through `Damage_DispatchByAttackType` on attack types 5 (Revive) and
6 (Revive at full HP), and the only flag it tests is `0x10` (Reflect). This matters because
on the Item command path `Battle_applyDamage` copies the item's whole flag byte verbatim
into the global `ATTACK_FLAG` (`0x490C40`), so a Potion does carry `0x80` at damage time and
nothing treats it as revival.

Instead, three parallel "menu status" builders fold `0x80` into bit 0 of a per-entry status
byte, one per list:

| Builder | Table | Effect of `0x80` |
|---------|-------|------------------|
| `setMenuFlagMagicOnCharaData` (`0x4954B0`) | Magic | `magicStatus = MAGIC_MENU_STATUS_REVIVE` (1) |
| `linkedStockFieldCharData` (`0x48CAE0`) | Magic (field/stock) | `unk_8 = 1` |
| `updateBattleItemData` (`0x48C670`) | Battle items | `selectable = 1` |

That status byte rides along in the 5-byte per-row record the shared battle list window
reads (`BattleMenu_ListWindow_Update`, `0x4FDD90`), and reaches target selection in
`sub_4AB190` (`0x4AB190`), which is where it finally does something:

```c
*(_BYTE *)(v9 + 10) = a4 & 1;                    // a4 = the menu status byte
if ( (a4 & 1) != 0 )
    v19 = MASK_MONSTER_CHARA_ENABLE;             // low word
else
    v19 = HIWORD(MASK_MONSTER_CHARA_ENABLE);     // high word
```

`MASK_MONSTER_CHARA_ENABLE` (`0x1D750BC`) is two 16-bit valid-target masks packed in one
dword. The **low word includes KO'd units, the high word is living-only** — provable from
the very next block, which computes the default cursor slot for a revive spell as the
targets present in the low mask but absent from the high one:

```c
if ( *(_BYTE *)(v9 + 10) && (a2 & 1) != 0 )       // a2 = TargetInfo, bit 0 = Dead
    v12 = MASK_MONSTER_CHARA_ENABLE & ~BYTE2(MASK_MONSTER_CHARA_ENABLE) & 7;
```

So `0x80` is the precondition for [TargetInfo]({{site.baseurl}}/technical-reference/list/kernel#target-info)
`0x01` (Dead) to have any effect: the flag opens the cursor to KO'd units, and TargetInfo
`0x01` then parks the cursor on one by default. This is why you cannot point Cure at a KO'd
ally but can point a Potion at one — the Item cursor is always allowed to, so vanilla sets
`0x80` on every item.

### 0x20 on battle items — the greyed row

The same `updateBattleItemData` folds `0x20` into bit 1 of that status byte, inverted:

```c
if ( (K_ITEM[id].attackFlagsAndSelectability & 0x20) == 0 )
    selectable |= 2u;
```

Bit 1 is read in two places, both in the shared list window: the item row draw callback
(`0x4C8680`) swaps the text palette from 7 to 0, and the OK handler (state 22 of
`BattleMenu_ListWindow_Update`) refuses the row with the buzzer alongside the
"quantity <= 0" check. So **clearing `0x20` greys the item out and makes it unselectable**.
Vanilla sets `0x20` on all 32 real items, so only the blank entry 0 is ever greyed. The magic
status byte uses bits 0 and 4 instead of 0 and 1, which is why this bit is inert everywhere
but the item table.

### 0x40 — verified unread, but not random

`0x40` varies meaningfully between entries, which makes "unused" look wrong. It isn't — the
variation is an authoring convention that no code consumes.

**The enumeration.** The byte reaches the engine by two routes, and both were walked exhaustively
rather than pattern-matched:

*Route 1 — the runtime global `ATTACK_FLAG` (`0x1D28E0E`).* It has 26 references. 16 are stores
(`mov [ATTACK_FLAG], cl` / `mov byte ptr [ATTACK_FLAG], imm`, one per command type in
`Battle_applyDamage`). The 10 loads test only three masks:

| Mask | Sites |
|------|-------|
| `0x03` damage-type pair | `0x49466E`, `0x4934F1`, `0x491CCF`, `0x4922B0`, `0x4925D2` |
| `0x08` break damage limit | `0x491124` — `and cl, 8` / `and ecx, 0C351h` / `add ecx, 270Fh`, i.e. cap 9999 → 60000 |
| `0x10` reflectable | `0x491952`, `0x491AE6`, `0x493120`, `0x493291` |

*Route 2 — code reading a kernel table's own `attackFlags` field directly, bypassing the global.*
This is the route that makes `0x20` and `0x80` live, so it cannot be skipped:

| Reader | Table | Mask |
|--------|-------|------|
| `setMenuFlagMagicOnCharaData` (`0x4954B0`) | Magic | `0x80` |
| `linkedStockFieldCharData` (`0x48CAE0`) | Magic | `0x80` |
| `updateBattleItemData` (`0x48C670`) | Battle items | `0x80`, `0x20` |
| `ResetAndParseBattleAndFieldCharacter` (`0x4957AC`) | Battle command abilities | `0x80` |
| `MonsterAI` (`0x489F8A`) | Enemy attacks | `0x80` (adds target-mask bit `0x4000`) |
| `computeCoverTargetSelection` (`0x48EBDA`) | Enemy attacks | `0x03` (Cover needs a pure physical hit) |

Every other field reference is a copy into the global. So the complete set of masks the engine
ever tests on this byte is **`0x03`, `0x08`, `0x10`, `0x20`, `0x80`** — `0x04` and `0x40` appear
in no test anywhere.

**What the bit tracks instead.** It is set on 8 of 57 magics and 17 of 33 battle items:

- Magic: Cure, Cura, Curaga, Life, Full-life, Esuna, Dispel, Float
- Items: the five Potions, Mega-Potion, Phoenix Down, Mega Phoenix, Elixir, Megalixir, Antidote,
  Soft, Eye Drops, Echo Screen, Holy Water, Remedy, Remedy+

Cross-tabulated against the [Attack Type](#attack-type) field it is almost exactly "the attack
type is curative": every Curative Magic, Curative Item, Revive and Revive At Full HP entry has it,
and every non-curative type lacks it, with four exceptions — X-Potion, Elixir and Megalixir (type
*Give Percentage HP*, still heals) and **Float**, the one genuine oddity, a buff marked as
curative. Note it is *not* "beneficial": Regen, Protect, Shell, Reflect, Aura, Haste, Double,
Triple, Hero and Holy War all lack it.

So it duplicates information the Attack type byte already carries, which is presumably why nothing
reads it.

*Caveat:* route 2 relies on those accesses being typed as the struct field in the IDB. Code
reaching the byte through an untyped pointer would not appear in either enumeration.

### Damage-type pair (bits 0-1)

The low two bits form a damage-type pair, stored per hit as the target's
`last_attacker_attack_flag` (`ATTACK_FLAG & 3`). It is **not** a free bitfield — it's one of four
mutually-exclusive values. The kernel `attackFlags` byte holds the "resting" value; the runtime
overrides some (Gunblade/Renzokuken force `3`; on a Gunblade *hit* the value becomes the source's
own type).

| Pair | Name | Set by |
|------|------|--------|
| 0 | Physical | Attack, most physical commands |
| 1 | Magical | Magic, GF, most offensive spells |
| 2 | Item/Medicine | Battle items |
| 3 | (special) | Forced by Renzokuken finishers / Gunblade |

**What pair = 0 (Physical) uniquely enables** — pure-physical hits are the *only* ones that:
trigger the target's **Counter** ability, **wake** a Sleeping/Confused target, **remove Back
Attack** status, and mark the **kill result** on a killing blow. Magical, Item and special hits do
none of these. The monster-AI condition `LAST ACTION DAMAGE TYPE` also compares this pair against
Physical/Magical, so an attack's type decides which AI branches fire.

**What pair = 1 (Magical) does** — the target's **Shell** status halves the damage *or heal*
(`ATTACK_FLAG_MAGICAL_SHELLED`). This is unconditional in `computeCurativeMagic`, so **curative
magic is always Shell-halved** — a penalty spells cannot avoid.

**What pair = 2 (Item/Medicine) does** — it is the gate for the **Med Data** doubling in
`Damage_ComputeCurativeItemSpecial`:

```
if ((ATTACK_FLAG & 3) == 2 && attacker is a player character && attacker knows Med Data)
    heal *= 2;
```

Curative-item heals use `50 × power` (Potion, power 4 → 200 HP; doubled to 400 with Med Data). But
the *implications of the pair value* matter just as much as the doubling:

- **Fun fact — items dodge Shell.** Because a curative item is pair 2 (not 1/Magical), a target's
  Shell status does **not** halve its healing (`Damage_ComputeCurativeItemSpecial` has no Shell
  check). The Shell penalty that hits a Cure *spell* (pair 1, halved unconditionally in
  `computeCurativeMagic`) simply never applies to a Potion.
- **Fun fact — Med Data never provokes a counter.** Med Data doubling only exists on the Item path
  (pair 2), which is non-Physical, so a doubled heal can never trigger the target's Counter — you get
  the boost with none of the physical-hit side effects.
- **Fun fact — Phoenix Down ignores this flag entirely.** Its Med Data boost (maxHP/8 → maxHP/4
  revive) lives in `GetReviveHP` and checks `command == Item` **directly**, not `ATTACK_FLAG & 3`. So
  the flag governs *curative-item HP restore*, while revival amount is gated separately by the command
  type.

