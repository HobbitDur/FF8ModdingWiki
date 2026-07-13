---
layout: default
title: Battle formulas (from code)
parent: Battle
permalink: /technical-reference/battle/formulas/
---

1. TOC
{:toc}

# Battle formulas — decompiled from FF8_EN.exe

Exact integer arithmetic as compiled in the PC executable (function addresses given; image base 0x400000). Where the code differs from commonly circulated formulas, the difference is flagged. Notation: `rand255` = uniform 0..255, `randVar = rand%33 + 240` (the ±6% damage variance factor, applied as `dmg × randVar / 256`).

## Character stats (`Stat_ComputeCharaStat` 0x496440)

Kernel growth curve bytes A, B, C, D per stat; `J_val` = junctioned magic's junction value, `count` = magic quantity (0–100):

* **STR/VIT/MAG/SPR**: `stat = weaponBonus(STR only) + (C + lvl·A/10 + lvl/B − (lvl²/D)/2)/4 + savedBonus + J_val·count/100`, capped 255
* **SPD/LUCK**: `stat = bonus + lvl·A + lvl/B − lvl/D + savedBonus + J_val·count/100` (no /10, no level², no /4)
* **Max HP** (0x496310): `HP = savedBonus + C + lvl·A − 10·lvl²/B + hpJ_val·count` — ⚠ the HP junction term has **no /100 divisor**
* **HIT** (0x4967C0): `weapon.attackParameter + hitJ·count/100`; **EVA** (0x4968A0): `SPD/4 + evaJ·count/100`
* All stats are then scaled by the Stat+X% ability multiplier (`× mult/100`, base 100); HP caps at 9999.

## Monster stats (0x48C1C0 / 0x48C3F0 / 0x48C500)

From the .dat info_stat 4-byte curves: **STR/MAG** `= (C + lvl·A/10 + lvl/B − (lvl²/D)/2)/4`; **VIT/SPR/SPD/EVA** `= C + lvl·A + lvl/B − lvl/D`; each is then scaled by the AI-controllable stat variable (`× var/10`), capped 255. **HP** `= HP1·lvl²/20 + (HP1 + 100·HP3)·lvl + 10·HP2 + 1000·HP4`.

## Physical damage (`Damage_ComputePhysicalCore` 0x492C40)

```
dmg = [ P × ((265 − VIT) × (STR + STR²/16) / 256) / 16 ] × randVar / 256
```

Vit 0 sets VIT = 0. Hit roll (0x492BA0): `255×(HIT + LUCK_atk/2 − EVA_tgt − LUCK_tgt)/100 ≥ rand255` (attacker Darkness quarters HIT); Sleep/Stop on target or accuracy 255 = auto-hit. Crit roll (0x492B30): `LUCK + critBonus ≥ rand255` → damage ×2. Modifiers (0x48F600): Protect ÷2, back attack ×2, zombie target ÷2, Defend ÷2; attack element: `dmg += dmg × elem% × (800 − elemDef)/10000`.

**Gunblade** (0x48F480): `dmg = [(CRIT_BONUS/20 + 2) × 4·P × ((265−VIT)×(STR + STR²/16)/256) / 128] × randVar/256`; the trigger gives a flat ×1.5-style boost via that leading term and **no crit roll happens**.

## Magic damage (`Damage_ComputeMagicAndGF` 0x491AD0)

```
dmg = [ P × ((265 − SPR) × (P + MAG) / 4) / 256 ] × randVar / 256
```

⚠ **Enemy-cast magic is halved**: if the caster slot is ≥ 3 (a monster), `dmg >>= 1` — confirmed in the PC code. Shell ÷2, Defend ÷2. Element: `dmg × (900 − elemDef)/100` where 800 = neutral (so 100 % absorb → negative); a zombie target treats Holy at 700 (×2). Drain spells heal `dmg × (acc − drainResist)/100`, inverted on zombies. Cap 9999.

## GF damage (same function)

```
dmg = [ (SumMag+100)/100 × Boost/100 × P × ((265−SPR) × (LvlMod·GFLvl/10 + P + PwrMod) / 8) / 256 ] × randVar/256
```

`SumMag` = SumMag+% ability, `Boost` = boost value (up to 250). Diablos instead does `GFLvl × maxHP / (PwrMod − LvlMod + 100)`; Demi does `P × curHP/16`.

## Healing

Cure line (0x493280): `heal = P × randVar × ((P + MAG)/2) / 256`. Item in battle: `50 × P`. White Wind: caster's `maxHP − curHP`. Revive: target `maxHP/8` (from item Med data: `maxHP/4`). Angelo Recover: `P × maxHP/16`.

## Status attacks (`Battle_ApplyStatusWithResistRoll` 0x48F9F0)

`chance = accuracy + atkStat/4 − tgtStat/4 − mentalResist` (must be > 0; resist ≥ 100 = immune). Accuracy < 250: succeed when `255·chance/100 ≥ rand255`; accuracy 250–254: automatic unless resist zeroes it; accuracy 255: **bypasses the resist check entirely** (rarely documented).

## Specials

| Formula | Code |
|---------|------|
| Kamikaze | `5 × attacker maxHP` |
| Everyone's Grudge | `P × character NumKills` |
| LV Up/Down | `newLvl = clamp(P×lvl/8, 1, 100)`, gated by `acc > rand255` |
| Devour | success when `atkHP ≥ tgtHP` and `rand255 ≤ 255×(atkHP−tgtHP)/atkHP`; heal `HPHeal × maxHP/16` |
| Card | success when `256 − 255×curHP/maxHP ≥ rand255` (≈1/256 at full HP, never 0 below max); rare card when `rand255 < 16` |
| Draw quantity | `((atkLvl − tgtLvl + 10)/2 − drawResist + rand(1..32) + MAG)/5 − stockAmount`, clamp 0–9 |
| Draw-cast damage | `dmg × (rand255 + 10)/150` |
| Mug | success when `rand255 ≤ MugRate + SPD/2` |
| Drop/Mug slots | weights **178/51/15/12** (community docs often say /1 — the last slot spans rand 244–255) |
| Rare Item bug | with Rare Item, the 4th-slot compare compiles to `rand ≥ 261` — **impossible for a byte**, so weights become 128/114/14/**0** |
| EXP | `(damage share of HP) × (5·Exp·enemyLvl/avgPartyLvl − Exp)`, clamp 1..60000; killer gets the same with own level; Card/Devour/Doom kills give 0 |
| GF XP | character XP / number of junctioned GFs; compatibility per cast: `+= tableByte − 100`, clamped 1000..6000 |
| Multipliers | Darkside ×3, Angel Wing ×5, Berserk ×1.5, Cover ÷2; damage cap 9999 (60000 with Break Damage Limit flag) |

## Notable code-vs-community differences

1. **Enemy magic ÷2** is real and unconditional for caster slots ≥ 3.
2. **Drop/mug fourth slot weight is 12, not 1**.
3. **Rare Item makes the rarest slot unreachable** (`rand ≥ 261` bug).
4. **HP junction is `hpJ × count`** with no /100.
5. Crit chance is exactly `(LUCK + bonus)/256` — the compiled `255·x/255` is a no-op.
6. Status accuracy 250–254 vs 255 behave differently (auto-success vs full resist bypass).

Key functions: `Damage_DispatchByAttackType` 0x4922B0 · `Damage_ComputePhysicalWithHitCritRoll` 0x492E10 · `Damage_ApplyPhysicalModifiers` 0x48F600 · `Battle_RollDropItem` 0x486650 · `Battle_RollMugItem` 0x4867C0 · `Battle_ComputeDrawQuantity` 0x48FD20 · `Battle_RollCardCommand` 0x48FBA0 · `Battle_ComputeExpDistribution` 0x494D40 · `Stat_RefreshCharaBattleStats` 0x495960.

## Two ID spaces: command type vs attack type

An action carries two independent IDs, easy to confuse:

* **Command type** (`commandType`, byte +1 of each [`BattleTask68Data`]({{ site.baseurl }}/technical-reference/battle/tasks-effects/) action slot; the live copy is `CURRENT_COMMAND_TYPE_ID` at 0x1D27AD9). This is the *command* — Attack, Magic, GF, Item, Mug, Darkside, and the synthetic gunblade/Renzokuken variants. It selects animation, on-hit text and recoil behaviour, **not** the damage formula. (This field was mislabelled `commandTypeWIthGunblade` in an earlier pass — it holds the plain command type; the gunblade logic only *reads* it.)
* **Attack type** (`p_attack_type`, from the kernel Attack Type field of the magic/ability). This is what `Damage_DispatchByAttackType` (0x4922B0) switches on to pick the damage formula.

### Attack-type → formula dispatch (`Damage_DispatchByAttackType`, 0x4922B0)

| Attack type | Damage function | Notes |
|-------------|-----------------|-------|
| Physical attack | `Damage_ComputePhysicalCore(…,0)` | hit + crit roll first |
| Magic attack | `Damage_ComputeMagicAndGF` (unmissable) | |
| Magic ignoring target SPR | `Damage_ComputeMagicAndGF` (ignore SPR) | |
| GF | `Damage_ComputeMagicAndGF` (GF) | |
| GF ignoring target SPR | `Damage_ComputeMagicAndGF` (GF, ignore SPR) | |
| Percent magic damage | `Damage_ComputeMagicAndGF` (% current HP) | Demi |
| Percent GF damage | `Damage_ComputeMagicAndGF` (Diablos) | |
| Squall gunblade attack | `Damage_ComputeGunblade` | |
| Renzokuken finisher | `Damage_ComputePhysicalCore(…,0)` | |
| Percent physical damage | `Damage_ComputePhysicalCore(…,1)` | |
| Kamikaze | `Damage_ComputePhysicalCore(…,3)` | 5 × attacker maxHP |
| Everyone's Grudge | `Damage_ComputePhysicalWithHitCritRoll(…,16)` | × NumKills |
| Physical, ignore VIT | `Damage_ComputePhysicalWithHitCritRoll(…,19)` | |
| Curative magic | `Damage_ComputeCurativeMagic(…,7)` | |
| Curative item | `Damage_ComputeCurativeItemSpecial(…,14)` | |
| White Wind | `Damage_ComputeCurativeItemSpecial(…,9)` | |
| Angelo Recover | `Damage_ComputeCurativeItemSpecial(…,15)` | give % HP |
| Revive / Revive at full HP | `Damage_ComputeReviveHP` / resurrection | |
| Fixed / target HP−1 / GF-level fixed / 1 HP | `Damage_ComputeFixedSpecial(…,11/12/13/18)` | |
| LV Down / LV Up | `computeLvlUpDown(…,0/1)` | LV Up also restores HP |
| Scan | scan flag + text | sets abbreviated-repeat flag |
| Card | eject + card-obtained text | miss if no card |
| Devour | HP-ratio success roll | |
| Angelo Search | random item find | |
| Moogle Dance (Moomba) | GF revive | |

Before the switch, sleep/confusion are cleared on the target (unless the attack is a medicine item or shelled magic); after it, back-attack status is cleared.

### The command-type ID space (complete)

`Battle_applyDamage` (0x48FE20) dispatches on `commandType` twice via two-level jump tables (`cmp id, 0xFE; ja default`): stage 1 (0x48FF2F, damage-formula fields) through `BATTLE_COMMAND_SWITCH_REMAP1` (0x491250), stage 2 (0x49043B, semantic handler) through `BATTLE_COMMAND_SWITCH_REMAP2` (0x4913B8). The IDs fall into two disjoint bands.

**Real kernel battle commands (0x00–0x26)** — indices into the kernel battle-command ability list:

| ID | Command | ID | Command | ID | Command |
|----|---------|----|---------|----|---------|
| 0x00 | none / Kamikaze / Phoenix Pinion (fail sentinel) | 0x0E | Shot (Irvine) | 0x1A | Recover |
| 0x01 | Attack | 0x0F | Blue Magic (Quistis) | 0x1B | Revive |
| 0x02 | Magic | 0x10 | Slot (Selphie) | 0x1C | **Darkside** |
| 0x04 | Item | 0x11 | No Mercy (Seifer) | 0x1D | Card |
| 0x05 | Renzokuken launch, no finisher | 0x12 | Sorcery (Edea) | 0x1E | Doom |
| 0x06 | Draw | 0x13 | Combine (Selphie "The End") | 0x1F | (unknown 0x1F) |
| 0x07 | Devour | 0x14–0x16 | Slot/No-Mercy/Sorcery **item variants** (base \| 0x04) | 0x20 | Absorb |
| 0x08 | Monster attack | 0x17 | Defend | 0x21 | LV Down |
| 0x0B | Zell Duel link (launch) | 0x18 | Mad Rush | 0x22 | LV Up |
| 0x0C | **Mug** | 0x19 | Treatment | 0x26 | MiniMog |
| 0x0D | Item sub-link | | | | |

**Synthetic pseudo-commands (0xEC–0xFE)** — injected at runtime for the multi-stage limit and gunblade sequences (0x27–0xEB, 0xF2, and 0xFF are unused and route to the generic handler):

| ID | Command | Character / mechanic |
|----|---------|----------------------|
| 0xEC | Seifer link | Seifer |
| 0xED / 0xEE | Shot on-hit / expire | Irvine |
| 0xEF | Zell Duel link (secondary) | Zell |
| 0xF0 | Angelo auto-move | Rinoa |
| 0xF1 | Duel (main) | Zell |
| 0xF3 | Darkside + gunblade trigger | Squall/Seifer |
| 0xF4 | Angelo / Chocobo (Invincible Moon…) | Rinoa |
| 0xF5 | Odin / Gilgamesh | GF |
| 0xF6 | Doom countdown reached 0 | — |
| 0xF7 | Reflected-spell variant | — |
| 0xF8 | Mug + gunblade trigger | Squall |
| 0xF9 | Renzokuken finisher (Rough Divide … Lion Heart) | Squall |
| 0xFA | Renzokuken launch / sequence marker | Squall |
| 0xFB | Renzokuken on-hit (each initial hit) | Squall |
| 0xFC | Special action (generic) | — |
| 0xFD | Gunblade on-hit (Attack + trigger) | Squall |
| 0xFE | G-Force (GF summon) | GF |

The gunblade variants (0xF3/0xF8/0xFD) and the Renzokuken launch pair (0x05/0xFA) collapse to shared handlers in stage 2; the gunblade forms are produced by `Battle_ApplyGunbladeTriggerHit` (0x485160) from the base command in `commandType`. `computeDamageEndOfAction` (0x484180) then queues Darkside's self-damage recoil after a Darkside hit (0x1C or its gunblade form 0xF3) via the internal command 0 — the same path as the poison end-of-turn tick.
