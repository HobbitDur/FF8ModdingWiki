---
title: Information & stats
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/information-stats/
nav_order: 7
author: HobbitDur
---

1. TOC
{:toc}

## Informations & stats

| Offset | Length     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|--------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | 24 bytes   | Monster name in [FF8 String]({{site.baseurl}}/technical-reference/Miscellaneous/FF8String)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 24     | 4 bytes    | HP values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 28     | 4 bytes    | Str values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 32     | 4 bytes    | Vit values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 36     | 4 bytes    | Mag values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 40     | 4 bytes    | Spr values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 44     | 4 bytes    | Spd values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 48     | 4 bytes    | Eva values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 52     | 16*4 bytes | [Abilities](#abilities), low level                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 116    | 16*4 bytes | [Abilities](#abilities), med level                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 180    | 16*4 bytes | [Abilities](#abilities), high level                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 244    | 1 byte     | Med level start                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 245    | 1 byte     | High level start                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 246    | 1 byte     | [Camera category](#byte-246-camera-category) — a small integer selecting how camera sequences frame this monster. See details below                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 247    | 1 byte     | [LSB] Zombie / Fly / unused / LvUp-Down Immunity / HP Hidden / Auto-Reflect / Auto-Shell / Auto-Protect [MSB]. Bit `0x04` (third from LSB) is never read by the loader — it has no effect                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 248    | 3 bytes    | [Card]({{site.baseurl}}/technical-reference/Lists/Card_list#card-info) (drop/mod/rare mod)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 251    | 3 bytes    | [Devour]({{site.baseurl}}/technical-reference/Lists/Devour_list#devour-effects) (low/med/high)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 254    | 1 byte     | [LSB] <span id="increase-surprise-rng">[IncreaseSurpriseRNG]({{site.baseurl}}/technical-reference/battle/surprise-attack)</span> / <span id="decrease-surprise-rng">[DecreaseSurpriseRNG]({{site.baseurl}}/technical-reference/battle/surprise-attack)</span>  / <span id="surprise-attack-immunity">[SurpriseAttackImmunity]({{site.baseurl}}/technical-reference/battle/surprise-attack)</span> / <span id="increase-change-escape">[IncreaseChanceEscape]({{site.baseurl}}/technical-reference/battle/escape)</span>  / <span id="decrease-change-escape">[DecreaseChanceEscape]({{site.baseurl}}/technical-reference/battle/escape)</span> / unused / Gravity Immunity / Always obtains card [MSB] |
| 255    | 1 byte     | [DevourCategory](#byte-255-devour-category). Consumed by the Devour code, which returns it as the "damage" of the devour hit — technically real but invisible in practice, so likely vestigial.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 256    | 2 bytes    | Extra EXP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 258    | 2 bytes    | EXP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 260    | 8 bytes    | [Draw](#draw-mug-drop) (low)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 268    | 8 bytes    | [Draw](#draw-mug-drop) (med)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 276    | 8 bytes    | [Draw](#draw-mug-drop) (high)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 284    | 8 bytes    | [Mug](#draw-mug-drop)(low)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 292    | 8 bytes    | [Mug](#draw-mug-drop)(med)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 300    | 8 bytes    | [Mug](#draw-mug-drop)(high)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 308    | 8 bytes    | [Drop](#draw-mug-drop) (low)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 316    | 8 bytes    | [Drop](#draw-mug-drop) (med)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 324    | 8 bytes    | [Drop](#draw-mug-drop) (high)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 332    | 1 byte     | [Mug rate](#rate-value)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 333    | 1 byte     | [Drop rate](#rate-value)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 334    | 1 byte     | Padding (0x00)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 335    | 1 byte     | APs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 336    | 16 bytes   | [Renzokuken data](#renzokuken-data)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                         
| 352    | 8 bytes    | [Elemental resistance](#elemental-resistance) (Fire, Ice, Thunder, Earth, Poison, Wind, Water, Holy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 360    | 20 bytes   | [Status resistance](#Status-resistance) (Death, Poison, Petrify, Darkness, Silence, Berserk, Zombie, Sleep,<br> Haste, Slow, Stop, Regen, Reflect, Doom, Slow Petrify, Float, Drain, Confuse , Expulsion, VIT0(but unused by the game))                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

### Abilities

Abilities are composed of:

| Length | Description                                                                             |
|--------|-----------------------------------------------------------------------------------------|
| 1 byte | [AbilityTypeID]({{site.baseurl}}/technical-reference/list/ability-list/#abilities-type) |
| 1 byte | [AnimationSequenceID](#animationsequenceid)                                             |
| 2 byte | [AbilityID]({{site.baseurl}}/technical-reference//list/ability-list/#monster_ability)   |

#### AnimationSequenceID

Refer to a sequence in [Animation sequences](../animation-sequences/)

### Renzokuken data

The data is 8*2 bytes, each 2 bytes corresponding to an ID on the [Special Action list]({{site.baseurl}}/technical-reference/list/special-action-list/)

### Draw Mug Drop

Each section is composed of 8 bytes corresponding to 4 id ([magic]({{site.baseurl}}/technical-reference/list/magic-list) for
draw, [Item]({{site.baseurl}}/technical-reference/list/item) for mug & drop) and 4 quantity.
Quantity is not used for draw (always 0 but no impact on game when changing it)

| Length | Description |
|--------|-------------|
| 1 byte | ID 1        |
| 1 byte | Quantity 1  |
| 1 byte | ID 2        |
| 1 byte | Quantity 2  |
| 1 byte | ID 3        |
| 1 byte | Quantity 3  |
| 1 byte | ID 4        |
| 1 byte | Quantity 4  |

### Elemental resistance

The % def value follow the formula:
value% = 900 - value_hex * 10

and to revert back:
value_hex = floor((900 - value%) / 10))

### Status resistance

The % def value follow the formula:
value% = value_hex - 100

and to revert back:
value_hex = value% + 100

### Rate value

The mug rate (byte 332) and drop rate (byte 333) are raw bytes (0–255), **not** stored as a percentage. The engine compares them directly against a
uniform battle random number in the range 0–255 (`GetRandomInt` at `0x48F020`), so the true probability is out of 256, with a `+1` from the `<=` comparison.

**Drop** — `ComputeProbabilityGetItemMug` (`0x486650`), rolled on kill inside `applyDamageAndHandleDeath`:

```
the drop succeeds when  GetRandomInt() <= DropRate      // GetRandomInt() ∈ [0, 255]
=> P(drop) = (DropRate + 1) / 256
```

There is no zero-guard on the drop, so `DropRate = 0` still yields a 1/256 (≈0.39%) chance, and `DropRate = 255` is a guaranteed drop.

**Mug** — `getMugObjectIdAndQuantity` (`0x4867C0`), used by the steal/Mug path:

```
if MugRate == 0            => never steal
the mug succeeds when  GetRandomInt() <= MugRate + attacker_SPD / 2
=> P(mug) = (MugRate + min(attacker_SPD/2, ...) + 1) / 256
```

Unlike the drop, the mug has a hard `MugRate == 0 => never` guard and adds half the attacker's SPD to the threshold, so a faster stealer succeeds more often.

A convenient approximation for display is `% ≈ (value_hex + 1) / 256 * 100` (e.g. `128 ≈ 50.4%`, `255 = 100%`). The older `value_hex * 100 / 255`
formula is close but slightly off (wrong denominator, and it ignores the `+1`).

The battle module also has generic probability helpers used by the auto-summon / escape / card rolls — `isRandomProbaNumDen255` (`0x48F0F0`) and
`isRandomNumeratorDenominator` (`0x48F0C0`) — which compute `255 * numerator / denominator` and succeed when that value `>= GetRandomInt()`. This is the same
0–255 convention (a roll quoted as "32/255" means a threshold of 32 against the 0–255 random).

### Byte 246: Camera category

This byte is a small per-monster integer that tells the battle camera how to frame the monster (roughly, a size/distance class — it is what makes the camera
pull back further for large enemies when a spell is cast on them, etc.). It is not a bitfield in the usual sense; it is read once per entity at battle start and
converted into a camera value on the entity, which the camera-sequence VM then reads back.

**How the engine uses it:**

1. At battle start, `initAnimationSequenceAtStartBattle` reads this byte through `getMonsterCameraCategory` and converts it into the entity's
   `cameraDataRelated` field using the mapping below. Playable characters (com id &lt; 0x10) always get `cameraDataRelated = 0`; only monsters use the byte.
2. During a fight, the [camera-sequence VM](../camera-sequence/) can read a target's `cameraDataRelated` back via C3 special variable `0x15` (21),
   letting a camera sequence branch on the target's category to pick a framing.

Conversion from byte 246 to `cameraDataRelated`:

| Byte 246 value                | `cameraDataRelated` | Notes                                    |
|-------------------------------|---------------------|------------------------------------------|
| bit `0x8` set                 | 5                   | Not used by any vanilla monster          |
| bit `0x4` set (and not `0x8`) | 4                   | i.e. value `4`                           |
| 3                             | 0                   | `3 − value` for the remaining low values |
| 2                             | 1                   |                                          |
| 1                             | 2                   |                                          |
| 0                             | 3                   | Default / closest framing                |

Vanilla monsters only use values `0`–`4`, so the effective camera value ranges `0`–`4` (the `0x8 → 5` branch exists but is never triggered by shipped data).

### Byte 255: Devour category

It is an integer, a per-monster *category* consumed by the Devour system:

**What the engine does with it (PC version):**

1. When a Devour command resolves, `computeDevour` picks the devour effect ID from bytes 251–253 (by level tier). If the ID is 255 (Immune) the devour fails
   immediately. Otherwise it stores the effect ID (`DEVOUR_EFFECT_ID`) **and this byte** (`DEVOUR_CATEGORY_OR_SWAP_COM_ID`) into a pending-devour block.
2. `Battle_DamageGettingRelated`'s `ATTACK_TYPE_DEVOUR` case then rolls the devour: it succeeds only if the devourer's **current HP ≥ the target's current HP**,
   with probability `(attacker_hp − target_hp) / attacker_hp` (so devouring gets more reliable the more the target is weakened — a previously undocumented
   formula). On success the target gets the *Eject* status (this is how Devour removes a monster without death rewards) and the devour message is printed; on
   failure the miss flag is set and the byte is overwritten with **8**.
3. Either way, the function **returns this byte as the "damage" value of the devour hit**. So on PC its gameplay effect is real but essentially invisible: a
   successful devour deals 0–7 damage to a monster that is being ejected anyway, and on a failure the miss flag suppresses the 8. In practice you cannot see it
   in game — which is why it stayed unidentified so long. The categorized values strongly suggest it originally had a richer purpose (flavor text or
   per-category outcome).
4. Side note: the effect ID meanwhile drives everything visible — statuses and heal/damage quantities from the kernel devour table, and the
   Str/Vit/Mag/Spr/Spd/HP permanent bonuses via `relatedToDevour`.

**The data itself is a deliberate classification.** No name for the categories survives in the engine or the reference data — the names in the `Name` column
below are proposed based on which monsters use each value, not something extracted from code. Monster lists come from scanning all vanilla c0m files (144–199
are garbage filler):

| Value | Name                            | Monsters                                                                                                                                                        | Reading                                                                                                                                                          |
|-------|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0     | `DEVOUR_CATEGORY_PRIME_BEAST`   | Thrustaevis, Mesmerize, Blue Dragon, Adamantoise, Chimera, Behemoth, T-Rexaur, Ruby Dragon, Cactuar, Tonberry, Torama                                           | Notably includes every stat-bonus devour (Str/Vit/Mag/HP +1)                                                                                                     |
| 1     | `DEVOUR_CATEGORY_STANDARD`      | SAM08G, Snow Lion, Caterchipillar, Fastitocalon, Hexadragon, Armadodo, Turtapod, Wendigo, Gayla, Death Claw, Grand Mantis, Grendel, PuPu, Lefty, Righty, Vysage | Mostly Full HP Recovery devours                                                                                                                                  |
| 2     | `DEVOUR_CATEGORY_SMALL_CRITTER` | Glacial Eye, Buel, Red Bat, Blitz, Fastitocalon-F, Jelleye, Imp, Anacondaur, Cockatrice, Tri-Face, Bomb, Abyss Worm                                             | Small / flying / venomous critters                                                                                                                               |
| 3     | `DEVOUR_CATEGORY_PLANT`         | Grat, Ochu, Malboro, Funguar                                                                                                                                    | Plants                                                                                                                                                           |
| 4     | `DEVOUR_CATEGORY_AMORPHOUS`     | Blobra, Gesper, Blood Soul                                                                                                                                      | Amorphous / spirits                                                                                                                                              |
| 5     | `DEVOUR_CATEGORY_UNDEAD`        | Forbidden                                                                                                                                                       | Undead                                                                                                                                                           |
| 6     | `DEVOUR_CATEGORY_PEST`          | Geezard, Bite Bug                                                                                                                                               | Small pest group                                                                                                                                                 |
| 7     | `DEVOUR_CATEGORY_MACHINE`       | GIM52A, GIM47N, Elastoid, Iron Giant, Belhelmel                                                                                                                 | Machines / inorganic                                                                                                                                             |
| 8     | `DEVOUR_CATEGORY_INEDIBLE`      | Every boss/story monster (c0m061+) and early bosses                                                                                                             | Bosses / story monsters. Matches the engine forcing this value on a failed devour; these monsters are all Devour-immune anyway, so it's never even read for them |

Note the consistency: `DEVOUR_CATEGORY_INEDIBLE` (8) is the failure code the engine itself writes, and it is exactly the value stored on every non-devourable
monster. Modders can effectively treat this byte as free space (its only vanilla effect is 0–7 phantom damage on a successful devour), or repurpose the
already-wired data path: monster byte 255 → `DEVOUR_CATEGORY_OR_SWAP_COM_ID` → returned as the devour hit's damage.

### Function/address reference

For readers following along in IDA / a disassembler. Names above are the ones set in the shared IDA database.

| Name                                 | Address     | Role                                                                                                                                  |
|--------------------------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `initAnimationSequenceAtStartBattle` | `0x5027D0`  | Per-entity battle-start init; converts byte 246 into the entity's `cameraDataRelated`                                                 |
| `getMonsterCameraCategory`           | `0x48B9F0`  | Reads byte 246 (`camera_category`) from a monster's info section                                                            |
| `a3ParamAnimSeqForCamera`            | `0x509640`  | Camera-sequence VM special-variable reader; C3 var `0x15` returns a target's `cameraDataRelated`                                      |
| `ComputeProbabilityGetItemMug`       | `0x486650`  | On-kill item drop: reads byte 333 (`DropRate`), drop succeeds when `GetRandomInt() <= DropRate`                                       |
| `getMugObjectIdAndQuantity`          | `0x4867C0`  | Mug/steal: reads byte 332 (`MugRate`); 0 = never, else succeeds when `GetRandomInt() <= MugRate + attacker_SPD/2`                     |
| `GetRandomInt`                       | `0x48F020`  | Battle random byte generator, returns a value in `[0, 255]`                                                                           |
| `computeDevour`                      | `0x48FC60`  | Picks the devour effect ID by level tier, stores it and byte 255 into the pending-devour block                                        |
| `Battle_DamageGettingRelated`        | `0x4922B0`  | Resolves attack-type-specific damage; `ATTACK_TYPE_DEVOUR` case at `0x4926BC` rolls the devour and returns byte 255 as the hit damage |
| `relatedToDevour`                    | `0x492220`  | Applies the devour effect's permanent Str/Vit/Mag/Spr/Spd/HP bonuses from the kernel devour table                                     |
| `DEVOUR_EFFECT_ID`                   | `0x1D28E27` | Pending devour effect ID (from bytes 251–253)                                                                               |
| `DEVOUR_CATEGORY_OR_SWAP_COM_ID`     | `0x1D28E28` | Pending devour category (byte 255); reused as a scratch com-id by the unrelated party-swap flow                             |
