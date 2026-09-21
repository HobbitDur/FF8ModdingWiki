---
layout: default
title: Ability id space (and how to add abilities)
nav_order: 40
parent: Kernel
permalink: /technical-reference/main/kernel/ability-id-space/
---

1. TOC
{:toc}

# Ability id space — and how to add abilities

Sections 12 to 18 look like seven independent ability lists. To the game they are **one array**.
Everything a mod needs to know before trying to add an ability follows from that single fact.

All addresses on this page are from **FF8_EN.exe, 2013 Steam re-release, image base 0x400000**.
Other languages and the 2000 release have the same structure at different addresses.
Everything here is static analysis of the exe — none of the patch recipes below has been run in-game yet.

## One array, seven groups

The seven ability sections are contiguous in kernel.bin, all with 8-byte entries, and the exe treats
them as a single array indexed by a **unified ability id, 0 to 115**:

| Group | Ids | Count | Kernel section | Offset in kernel.bin | Address in the exe |
|-------|-----|-------|----------------|----------------------|--------------------|
| 0 Junction  | 0–19   | 20 | [12](../junction-abilities/) | 0x40E0 | `K_JUNCTION_ABILITY` 0x1CF7F28 |
| 1 Command   | 20–38  | 19 | [13](../command-abilities-gf/) | 0x4180 | 0x1CF7FC8 |
| 2 Stat %    | 39–57  | 19 | [14](../stat-percentage-increasing-abilities/) | 0x4218 | 0x1CF8060 |
| 3 Character | 58–77  | 20 | [15](../characters-abilities/) | 0x42B0 | 0x1CF80F8 |
| 4 Party     | 78–82  | 5  | [16](../party-abilities/) | 0x4350 | 0x1CF8198 |
| 5 GF        | 83–91  | 9  | [17](../gf-abilities/) | 0x4378 | 0x1CF81C0 |
| 6 Menu      | 92–115 | 24 | [18](../menu-abilities/) | 0x43C0 | 0x1CF8208 |

`getAbilityName` (0x47E710) and `getAbilityDescription` (0x47E840) index `K_JUNCTION_ABILITY[id]`
for **every** id, whatever the group. The group is used for one thing only: choosing which kernel
**text** section the entry's name/description offset is relative to. The same is true of the three
flag bytes at entry+5: `Menu_BuildGFJunctionSummary` (0x4E2C20) and the junction handlers read them
through the same base.

So an ability id is just an index into a 116-entry array, and the "sections" are ranges inside it.

## Where the layout is hardcoded

### Data section addresses are baked into the exe

`readFilesKernelNamedicIconSysfnt` (0x47D2A0) reads kernel.bin **whole** into the static buffer at
`KERNEL_HEADER` (0x1CF3E48), so every section's address is `0x1CF3E48 + its offset in the file` —
and those addresses are assembled into the instructions that use them.

The header's **data** offsets (`offsetMagicData`, `offsetGFAbilities`, …) have **zero cross-references**:
the game never reads them. Only the **text** offsets are read from the header, which is why text
sections move freely when a mod rewrites the header, while data sections cannot move at all.

Vanilla kernel.bin is 37992 bytes and the next named global after the buffer is at 0x1CFDC50, so about
**2.4 KB of slack** follows the loaded file. A bigger kernel.bin fits in memory; what does not survive
is the *addressing*.

### The group boundaries

The chain `20 / 39 / 58 / 78 / 83 / 92` is duplicated, inlined, in five places:

| Address | Function | What it decides |
|---------|----------|-----------------|
| 0x47E710 | `getAbilityName` | which text section the name offset belongs to |
| 0x47E840 | `getAbilityDescription` | same, for the description |
| 0x4ACB20 | `getAbilityGroupFromId` | the helper other code calls |
| 0x4ACB70 | `BuildGFAbilityList` | field [3] of each list record |
| 0x4A62E0 | `Menu_DrawAbilityLearnedPopup` | the icon sprite id (216 + group) |

Individual boundaries also appear on their own: the equippable-passive range `[39, 83)` in
`Menu_ValidateCharaPassiveAbilities` (0x4DA6AF, 0x4DA6B4) and `Menu_BuildCharaAbilityMaskAndLists`
(0x4E01C8, 0x4E0224), and "is this a junction ability" (`< 20`) in `Menu_BuildGFJunctionSummary` (0x4E2C94).

### The group table at 0xB877C0

Seven records of 4 bytes, `{u16 section offset in kernel.bin, u8 first ability id, u8 entry size}`:

```
40E0 00 08   junction      4180 14 08   command      4218 27 08   stat %
42B0 3A 08   character     4350 4E 08   party        4378 53 08   GF
43C0 5C 08   menu
```

Read by `BuildGFAbilityList` and `DrawGFAbilityLearnStatus` as
`*(&KERNEL_HEADER.offsetBattleCommands + offset + size * (id - first_id))` — the `+4` of that base is
what makes the read land on the entry's **AP required** field.

### The GF group is delimited by addresses, not ids

`computeGFBattleStats` (0x495D80) tests the entry pointer against two absolute addresses,
`K_GF_ABILITY[0].stat_to_increase` (0x495DF5) and `K_MENU_ABILITY[0].start_offset` (0x495DFC),
and its outer loop only walks learned bits 64 to 127.

## What an entry can actually do

Abilities are data, not code. Per group, the bytes after AP are:

| Group | entry+5 … +7 | Applied by |
|-------|--------------|-----------|
| Junction  | 3 flag bytes — which junction slots the ability grants | `ResetAndParseBattleAndFieldCharacter`, `Menu_BuildGFJunctionSummary` |
| Command   | battle command index | command menu build |
| Stat %    | stat id, percent | `GetCharaStatPercentBonus` (0x4962C0) |
| Character | 3 flag bytes (Counter, Cover, Auto-Haste…) | `ResetAndParseBattleAndFieldCharacter` |
| Party     | one flag (Move-Find, Enc-None…) | field code |
| GF        | boost flag, stat id, value | `computeGFBattleStats` |
| Menu      | refine table index, start/end offsets | refine menus |

For **GF abilities** specifically, `computeGFBattleStats` does exactly three things:

* `flag |= entry[5]` — bit 0x01 is "Boost enabled" (0x80 is the runtime "HP below 25%" bit)
* `entry[6] == 0` → `percentDamageBonus += entry[7]` (the `SumMag+x%` family)
* `entry[6] == 1` → `percentHPBonus += entry[7]` (the `GFHP+x%` family)

Any other value of `entry[6]` does nothing. A new GF ability that raises summon damage, raises GF HP or
enables Boost is **pure data**. A new *kind* of effect needs new code in that function.

## The limits

| Limit | Value | Where it comes from |
|-------|-------|---------------------|
| Ability ids | **128** | `SG_GFData.CompleteAbilities` is a 16-byte learned mask, one bit per ability per GF |
| Ids used by vanilla | 116 | leaves **12 spare** (116–127) |
| Abilities offered by one GF | **21** | section [3](../junctionable-gfs/) has 21 `{unlocker, level/prereq, alt prereq, ability}` records |
| Entries in a displayed list | 22 | the `>= 22` checks in `BuildGFAbilityList` / `GFAbilityLearnComplete` |
| Menu abilities | **32** | `RebuildLearnedMenuAbilityMask` (0x4C2B40) packs ids 92–115 into one dword |
| Equippable passive ids | 39–82 | `Menu_ValidateCharaPassiveAbilities` rejects anything outside |
| Absolute id ceiling | 254 | the id is a byte everywhere; 0xFF is the "none" sentinel |

The per-GF limit of 21 is the one people hit first in practice: across 16 GFs that is 336 teachable
slots, but no single GF can ever offer a 22nd ability.

## Adding abilities

### Route A — redistribute, no size change

The 116 ids are just where the array happens to end. Moving the GF/menu boundary up by N grows the GF
group at the menu group's expense, with kernel.bin keeping its **exact size**. For N = 4
(GF becomes 83–95, menu 96–115), the complete patch is nine edits:

| Address | Vanilla | Patched | Why |
|---------|---------|---------|-----|
| 0x47E7F0 | `cmp eax, 5Ch` | `60h` | boundary in `getAbilityName` |
| 0x47E920 | `cmp eax, 5Ch` | `60h` | boundary in `getAbilityDescription` |
| 0x4A6386 | `cmp esi, 5Ch` | `60h` | boundary in `Menu_DrawAbilityLearnedPopup` |
| 0x4ACB5A | `cmp eax, 5Ch` | `60h` | boundary in `getAbilityGroupFromId` |
| 0x4ACDD6 | `cmp edx, 5Ch` | `60h` | boundary in `BuildGFAbilityList` |
| 0x4C2B80 | `cmp eax, 5Ch` | `60h` | first menu ability |
| 0x495DFC | `offset 0x1CF820E` | `0x1CF822E` | GF range upper bound (+8N) |
| 0xB877D8 | `word 43C0` | `43E0` | menu row of the group table (+8N) |
| 0xB877DA | `byte 5C` | `60` | menu row first id (+N) |

The four entries change group, so their names and descriptions must move from the menu ability text
section to the GF ability text section. `0x4C2B85` (`cmp eax, 74h`, one past the last ability) stays,
because the total is still 116.

### Route B — grow the array in place

Using the 12 spare ids means the array really gets longer, so the 13 sections that follow it
(temporary limit breaks through misc text pointers) all shift. Those sections **are** addressed
absolutely: **110 instruction operands** in 0x401000–0x570000 reference them — `Battle_applyDamage`
alone has about 40, plus `computeCommandAction`, `BuildLimitCommandMenu`, `relatedToDevour`,
`getAddressTextMisc`, `Damage_DispatchByAttackType`. Add the nine edits above (with `0x4C2B85` now
also moving) and it is roughly 120 patched operands.

Every one is mechanical — `+8N` over a known address list — so this is a generated patch, not hand
work. Two caveats: it is locked to one exe build, and it is **incompatible with FFNx's AddMoreMagic**,
which deliberately hands the exe a vanilla-layout kernel image so that every baked address stays valid.

### Route C — redirect the array (FFNx)

The approach [AddMoreMagic](https://github.com/julianxhokaxhiu/FFNx/pull/956) uses for spells applies to
abilities and is much smaller here: point the array at a mod-side table instead of moving anything.
The ability array is reached from only **26 displacement operands** (all through the
`K_JUNCTION_ABILITY` base: the two text getters, `ResetAndParseBattleAndFieldCharacter`,
`StatusJunctionMenuHandler`, `GetCharaStatPercentBonus`, `GF_AddApToLearningAbility`,
`Menu_BuildGFJunctionSummary`, `Menu_DrawAbilityListRow`), plus `computeGFBattleStats`' loop pointer and
its two range bounds, plus the two AP-fetch bases in `BuildGFAbilityList` / `DrawGFAbilityLearnStatus`,
plus the seven boundary constants and the group table.

About **37 rewrites**, nothing in the kernel buffer moves, the 110 references above stay valid, and the
array can then be any length. The ceiling becomes the save mask, not the layout.

### Beyond 128 ids

Only the savegame stands in the way, and it is a separate job:

* `SG_GFData.APs` is 24 bytes for 21 used slots — 24 spare bits per GF, already saved, but not
  contiguous with the mask, so each of the **23** `CompleteAbilities` access sites needs a branch.
* Cleaner: replace those 23 accesses with one accessor pair against a wider mod-side mask, and persist
  it in the save file's unused tail. `Save_BuildSaveFileImage` (0x4E2EF0) copies **5028** bytes from
  `SG_CHECKSUM` into an **8192**-byte image at offset 384, and the CRC16-CCITT covers savemap+80 for
  4944 bytes — so image bytes **5412–8191 are unused, zeroed and outside the CRC**. A block there does
  not disturb the vanilla save format, the checksum, or Hyne.
* Note that two of the 23 sites (`Menu_BuildJunctionedGFAbilityMask` 0x4E0090,
  `Menu_BuildCharaAbilityMaskAndLists` 0x4E0110) *iterate* the mask as four dwords against a hardcoded
  end pointer, so the union scratch buffer at 0x1D8B580 widens too.

## Function reference

| Address | Name | Role |
|---------|------|------|
| 0x47D2A0 | `readFilesKernelNamedicIconSysfnt` | loads kernel.bin whole at 0x1CF3E48 |
| 0x47E710 | `getAbilityName` | id → name, unified array |
| 0x47E840 | `getAbilityDescription` | id → description |
| 0x4ACB20 | `getAbilityGroupFromId` | id → group 0–6 |
| 0x4ACB70 | `BuildGFAbilityList` | a GF's learnable/learned list, 8-byte records |
| 0x4A62E0 | `Menu_DrawAbilityLearnedPopup` | the "Learned X!" window |
| 0x4D45D0 | `DrawGFAbilityLearnStatus` | AP progress line in the GF menu |
| 0x4FC6C0 | `GFAbilityLearnComplete` | sets the learned bit |
| 0x497010 | `GF_AddApToLearningAbility` | adds AP, compares against AP required |
| 0x495D80 | `computeGFBattleStats` | applies GF ability effects |
| 0x4962C0 | `GetCharaStatPercentBonus` | sums stat % abilities on a character |
| 0x4C2B40 | `RebuildLearnedMenuAbilityMask` | the 32-bit menu ability mask |
| 0x4DA660 | `Menu_ValidateCharaPassiveAbilities` | keeps only ids 39–82 equipped |
| 0x4E0090 | `Menu_BuildJunctionedGFAbilityMask` | union of the junctioned GFs' learned masks |
| 0x4E0110 | `Menu_BuildCharaAbilityMaskAndLists` | same union + the menu candidate lists |
| 0x4E2C20 | `Menu_BuildGFJunctionSummary` | per-GF junction slots / level / owner table |
| 0x4E2EF0 | `Save_BuildSaveFileImage` | savemap → save file image |
