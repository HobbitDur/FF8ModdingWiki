---
layout: default
parent: Battle
title: GF Summon Runtime
permalink: /technical-reference/battle/gf-summon-runtime/
---

This page documents the runtime dispatch for Guardian Force summon effects, special GF-style auto-actions and the shared `MagicList_Logic` effect table.

1. TOC
{:toc}

## MagicList_Logic

`MagicList_Logic` is a 400-entry array of battle effect callbacks. Magic spells, GF summon cinematics, enemy attacks, item animations and boss cinematics all share this table.

| Address | Name | Type | Role |
|---------|------|------|------|
| `0xC81774` | `MagicList_Logic` | `int(*)(int)[400]` | Effect logic callbacks |
| `0xC81DB8` | `MagicList_TextureLoad` | `void(*)(void)[400]` | Matching texture-loading callbacks |
| `0x50AF20` | `BattleGF_LoadCallbackByMagicID` | function | Loads texture callback and writes active logic callback |
| `0x21DFEC4` | `GF_CALLBACK_PTR` | function pointer | Currently active GF/effect callback |

The `magicID` parameter passed to `BattleGF_LoadCallbackByMagicID` is a 1-based `effect_id`, not a GF kernel id and not a command argument.

```c
int idx = magicID - 1;
MagicList_TextureLoad[idx]();
*callback_out = MagicList_Logic[idx];
```

## Junctionable GF dispatch

The player command path identifies a GF with `command_id=0x03` and `command_arg=0x40..0x4F`. The command argument indexes the kernel GF table:

```
gf_index = command_arg - 0x40
effect_id = K_GF_JUNCTIONABLE[gf_index].magicID
```

The effect id is written to the action context at offset `+6`. `BattleActionSequence_Tick_GF_Cinematic` later reads it and calls `BattleGF_LoadCallbackByMagicID`.

| Context offset | Size | Field | Description |
|----------------|------|-------|-------------|
| `+0` | 1 | `attacker_slot` | Attacker slot id |
| `+1` | 1 | `command_type` | `0xFE` for GF summon, other values for magic/special |
| `+2` | 1 | `anim_state` | Animation state byte |
| `+4` | 2 | `cmd_arg` | Ability / GF kernel id |
| `+6` | 2 | `effect_id` | 1-based `MagicList_Logic` id |
| `+12` | 4 | `damage_ctx_ptr` | Damage context pointer |
| `+16` | 1 | `flags` | Additional flags |

## Junctionable GF catalog

Runtime evidence quality varies by GF. Keep the Confidence and Runtime fields when using this table for modding work.

| GF | cmd_arg | effect_id | Entry | Init | Tick | Counter | Completion | Family | Confidence | Runtime |
|----|---------|-----------|-------|------|------|---------|------------|--------|------------|---------|
| Quezacotl | `0x40` | 116 | `0x6C3550` | `0x6C3640` | `0x6C3760` / `0x6C6660` | `0x6C3932` / `0x6C51F2` / `0x6C671D` | `0x6C3931` / `0x6C51F0` / `0x6C675D` | FamilyA | 96 (static) | Pending |
| Shiva | `0x41` | 185 | `0x5C0D50` | inline | `0x5C7F50` | `0x5C7F8B` | Unknown | FamilyA | 92 (static) | Pending |
| Ifrit | `0x42` | 201 | `0xB25780` | `0xB257E0` | `0xB25DF0` | `0xB25DFA` | `0xB26004` | FamilyB | 100 | PASS |
| Siren | `0x43` | 95 | `0x739DA0` | `0x8DC540` shared | `0x739F40` | Unknown | Unknown | SharedInit | 95 (static) | Pending |
| Brothers | `0x44` | 205 | `0xAF4520` | inline | `0xAF4B90` | `0xAF4B9A` | `0xAF4DA1` | Atypical | 75 | Tier-3 partial |
| Diablos | `0x45` | 325 | `0x654210` | Unknown | `0x654350` driver | `0x65459D` | `0x654595` | Unknown | 90 | PASS |
| Carbuncle | `0x46` | 278 | `0x680C50` | `0x680C80` | `0x680DF0` | `0x6811C8` | `0x6811BE` | FamilyA | 95 (static) | Pending |
| Leviathan | `0x47` | 6 | `0xB58080` | inline | `0xB586F0` | `0xB586FA` | `0xB58901` | Atypical | 75 | Tier-3 partial |
| Pandemona | `0x48` | 291 | `0x6ED250` | `0x6ED260` | `0x6ED350` | `0x6ED755` | `0x6ED749` | FamilyA | 95 | PASS |
| Cerberus | `0x49` | 203 | `0xB0C1A0` | inline | `0xB0C820` | `0xB0C82A` | `0xB0CA31` | FamilyB | High | PASS |
| Alexander | `0x4A` | 204 | `0xAFFCA0` | inline | `0xB00310` | `0xB0031A` | `0xB00521` | Atypical | 72 | Tier-3 partial |
| Doomtrain | `0x4B` | 191 | `0x63E730` | inline | `0x6472C0` | `0x6472D1` | Unknown | FamilyA | 80 | Tier-3 partial |
| Bahamut | `0x4C` | 202 | `0xB189A0` | inline | `0xB19010` | `0xB1901A` | `0xB19221` | Atypical | 72 | Tier-3 partial |
| Cactuar | `0x4D` | 199 | `0x5A8750` | inline | `0x5AA3A0` | `0x5AA3B1` | Unknown | Atypical | 75 | Tier-3 partial |
| Tonberry | `0x4E` | 90 | `0x762360` | `0x8DC540` shared | `0x7624D0` | `0x7625F9` | `0x762611` | SharedInit | 95 | PASS |
| Eden | `0x4F` | 206 | `0xAE2DD0` | inline | `0xAE3470` | `0xAE347A` | `0xAE3681` | Atypical | 70 | Tier-3 partial |

Note: Diablos has a thunk wrapper (`MAG_325_UNKNOWN` in IDA) in `MagicList_Logic`; it forwards to the real entry (unnamed in IDA, shown as `sub_654210`). See [Function addresses](#function-addresses).

## GF families

| Family | Shape | Examples |
|--------|-------|----------|
| FamilyA | Entry -> Init -> SequenceTick -> secondary SequenceTaskDriver | Pandemona, Doomtrain, Shiva, Odin |
| FamilyB | Entry -> SequenceTick; the tick is the driver | Cerberus, Brothers, Leviathan, Alexander, Bahamut, Eden |
| SharedInit | Entry -> `BdLinkTask_CreateAndInitContext` -> SequenceTick | Siren, Tonberry |
| Atypical | Partially resolved or not clearly classified | Several low-confidence chains |

All families use the same completion return pattern:

```c
return ((unsigned int)~*(WORD*)(statePtr + 10) >> 14) & 2;
```

## Shared GF infrastructure

`Effect_AddTaskAndInitFromCtx` (renamed from `BdLinkTask_CreateAndInitContext`) is a shared task constructor used by multiple GFs.

```c
int __cdecl Effect_AddTaskAndInitFromCtx(
    _DWORD *dst_ctx,
    int tick_fn,
    int ctx_size,
    int parent_ctx
);
```

The second argument is the per-frame tick function, which is how the tick can be recovered from entries that use the shared constructor.

Shared cinematic globals are reused across all GFs; only one GF cinematic runs at a time.

| Address | Name | Description |
|---------|------|-------------|
| `0x27973EC` | `g_GfCinematic_SequenceCtxPtr` | Active GF sequence context |
| `0x27973B8` | `g_GfCinematic_RuntimeSlotPtr` | Active GF runtime slot |
| `0x27973BC` | `g_GfCinematic_RenderCtxPtr` | Active GF render context |
| `0x27973C0` | `g_GfCinematic_SequenceStatePtr` | Active GF state pointer |
| `0x2797624` | `g_GfCinematic_OffsetStack` | Active GF stack frame |

## Special / non-junctionable GFs

| Effect | effect_id | Entry | Mechanism | Notes |
|--------|-----------|-------|-----------|-------|
| Odin | 187 | `0x6472E0` | Battle-start auto-trigger | Crashes on direct injection; use caveat |
| Griever | 69 | `0x6FE040` / thunk `0x6FE050` | Boss-only cinematic | Corrected from a former mid-function address |
| Gilgamesh Zantetsuken | 329 | `0x58DB10` | Special action `0xF5` | Variant selected randomly |
| Gilgamesh Masamune | 330 | `0x58DCF0` | Special action `0xF5` | Variant selected randomly |
| Gilgamesh Excalibur | 328 | `0x58D930` | Special action `0xF5` | Variant selected randomly |
| Gilgamesh Excalipoor | 327 | `0x58D760` | Special action `0xF5` | Variant selected randomly |
| Phoenix | 140 | `0x6A6430` | Party-wipe auto-trigger | 64/255 trigger check |
| Angelo Rush | 91 | via MagicList | Auto/counter | Rinoa action |
| Angelo Recover | 93 | via MagicList | Auto/counter heal | Rinoa action |
| Angelo Reverse | 94 | via MagicList | Counter revive | Rinoa action |
| Angelo Search | 92 | via MagicList | Auto item find | Rinoa action |
| ChocoFire | 97 | `0x729A60` | Chocobo/Boko variant | Entry mapped through table |
| ChocoFlare | 98 | `0x721860` | Chocobo/Boko variant | Entry mapped through table |
| ChocoMeteor | 99 | `0x717D30` | Chocobo/Boko variant | Entry mapped through table |
| ChocoBocle | 100 | `0x70D390` | Chocobo/Boko variant | SharedInit-like pattern |

## Odin and Gilgamesh

`SG_ODIN_ANGEL_GILGA_FLAG` controls Odin, Phoenix, Gilgamesh, Angelo suppression and Witch-related state.

| Bit | Value | Meaning | Set by |
|-----|-------|---------|--------|
| 1 | `0x02` | Has Odin | `SETODIN` field opcode |
| 2 | `0x04` | Phoenix enabled | Phoenix Pinion use in battle |
| 3 | `0x08` | Has Gilgamesh | Monster AI opcode 54; clears Odin simultaneously |
| 4 | `0x10` | Suppress Angelo | Field script opcode |
| 5 | `0x20` | Witch | `SETWITCH` field opcode |

Odin is checked only at battle init (`mode_3_subsubsubstep == 3`). `rollOdinAutoSummon` (renamed from `ZANTETSUKEN_sub_482DF0`) requires the Odin flag and skips if any enemy has death immunity. The RNG is `32/255`, about 12.5%.

Gilgamesh can trigger during battle init (`8/255`, about 3.1%) or during the active tick through `summonGilgaAngelStartFight` (renamed from `AngeloOdin_SpecialActionTick`) at `12/255` per checked tick. `GILGAMESH_ONESHOT_FLAG` prevents more than one Gilgamesh action in the same battle.

In the Seifer disc-3 battle, monster AI opcode 54 clears Odin and sets Gilgamesh:

```c
SG_ODIN_ANGEL_GILGA_FLAG &= 0xFD;
SG_ODIN_ANGEL_GILGA_FLAG |= 0x08;
```

## Phoenix

Phoenix auto-triggers on party wipe only. It does not have a spontaneous per-frame trigger like Gilgamesh.

`managePhoenixInvocWhenGameOver` (renamed from `BattleFrame_PartyWipeCheck`) scans party slots each active battle frame. If all party members are dead or petrified, it calls `computePhoenixInvoc` (renamed from `Phoenix_BattleFrame_TriggerCheck`; same function documented on [Enemy AI VM Runtime](../enemy-ai-vm-runtime/#function-address-reference)).

| Condition | Required value |
|-----------|----------------|
| At least one enemy alive | true |
| At least one party member exists and is not petrified | true |
| `SG_ODIN_ANGEL_GILGA_FLAG & 0x04` | Phoenix enabled |
| `COMBAT_SCENE_ID != 317` | Not excluded scene |
| RNG | `64/255`, about 25.1% |

The result is `RELATED_ODIN_SUMMONED = 1`, which maps to `effect_id=140`.

## Angelo variants

Angelo requires Rinoa in the party (`com_file_id == 4`) and bit `0x10` of `SG_ODIN_ANGEL_GILGA_FLAG` clear.

| Path | Function | Behavior |
|------|----------|----------|
| Per-frame auto-trigger | `summonGilgaAngelStartFight` (renamed from `AngeloOdin_SpecialActionTick`) | Recover, Reverse, Rush-like or Search priority cascade |
| Turn counter | `Angelo_TurnCounter_TriggerCheck` (`0x482E80`) | Rinoa turn: Recover or Rush |
| Damage counter | `Angelo_DamageCounter_ReverseCheck` (`0x482F10`) | Enemy attacks Rinoa: Angelo Reverse |

| Variant index | effect_id | Ability | Command type |
|---------------|-----------|---------|--------------|
| 11 | 91 | Angelo Rush | `0xF0` |
| 12 | 93 | Angelo Recover | `0xF0` |
| 13 | 94 | Angelo Reverse | `0xF0` |
| 14 | 92 | Angelo Search | `0xF0` |

## Model animation & 60 fps

Each GF draws an animated **creature model** loaded from the magic-effect files. Ifrit loads
`MAG200_B.00` (→ `Magic_b_00`, 69,608 B, geometry + animation opcodes) and `MAG200_B.01`
(→ `Magic_b_01`, 229,804 B, textures **+ a zeroed runtime scratch region**) via
`MagicList_TextureLoad[200]` (`MAG_201_IFRIT_SUMMON_HELL_FIRE_FL` in IDA). Both use an 11-entry u32 offset-table header
(`.00` = `[0, 0xFC, 0x8C, 0x281C, 0x1D48, 0x30, 0xE8, 0xFC, 0, 0x2540, 0]`). This is a **custom
magic-effect format**, not the monster/character skeletal `.dat`.

### The creature animation is a byte-code VM, not keyframes — *in the cinematic family*

> **Scope.** Everything in this subsection was decoded from **Ifrit**, and holds for the
> **shared-cinematic family** (the 10 slots at `0xAE`–`0xB5` that drive ctx `*0x27973EC`). It is
> **not** how every GF animates — see [Quezacotl](#quezacotl-a-timeline-family-gf-animates-like-an-ordinary-battle-model)
> below, which uses the standard battle-model system instead. Do not generalise the VM to all GFs.

Decoded from the Ifrit render tree: there is **no `pose[frame][bone]` table to interpolate**.
The animation is a **data-driven per-bone/per-axis opcode VM** (the AnimSeq VM, shared in form
with battle `.dat` and the summon camera track) that writes **rotation velocities and
accelerations** into each bone; a **per-frame integrator** turns those into the pose:

```
per frame, per bone:  velocity    += acceleration
                      accumulator += velocity
                      output Euler angle = accumulator >> 16      (4096 = 360°)
```

Bone runtime array = 8 bones × 256 B at `dword_27973EC+144` (= `Magic_b_01 + 0xFC`, zeroed
scratch). Per-bone fields: pose accumulators `+80..+100`, velocities `+104..+124`,
accelerations `+128..+138`, **output angles `+140/142/144` & `+148/150/152`**, per-axis
sequence pointers `+0/+4/+8`, hold timers `+12/14/16`, frame duration `+200`. The opcode
stream (`.00 @ 0xFC`) encodes *set velocity / add delta / randomize / wait N frames / loop*
per channel; there is **no fixed frame count** (playback length is opcode-driven; loop count
from GF data `caster+17`).

| Function | Addr | Role |
|---|---|---|
| `GF_Ifrit_seqBDlink` | `0xB25DF0` | per-frame tick (advance channels → integrate → draw); tick ctr `state+50` |
| `GF_Ifrit_AnimIntegrator` | `0xB26110` | pose integrator (`vel+=accel; accum+=vel; angle=accum>>16`) |
| `GF_Ifrit_AdvanceAnimChannels_Neg` / `_Pos` | `0xB2FCF0` / `0xB30110` | advance opcode channels per bone/axis |
| `GF_Ifrit_AnimVM_GenericOpcode` | `0xB2C480` | bulk opcode → writes stream data into bone vel/accel/target (descriptor `byte_1874EF0`) |
| `GF_Ifrit_AnimVM_Op0_FrameYield` / `_Op1_SubSeqLoop` | `0xB2FEB0` / `0xB2FB20` | wait-N-frames / sub-sequence loop |
| `GF_Ifrit_BuildMatricesAndDraw` | `0xB2ABE0` | build per-bone matrices from output angles + draw |
| `GF_Ifrit_SetupSectionPtrs` / `_InitBones` | `0xB258D0` / `0xB2F8F0` | section-pointer + bone-array init |

Each GF has its **own copy** of this VM/integrator (Ifrit's at `0xB2xxxx`), hence the
`GF_Ifrit_*` names.

### 60 fps options

Frame-holding `GF_Ifrit_seqBDlink` freezes the creature (halts both opcode advance and the
integrator) — confirmed in-game, and why the naive GF hold looked choppy and desynced. With no
stored keyframes to bake, two clean paths remain:

1. **Output-pose interpolation (recommended, least invasive):** let the VM run at native rate;
   cache each bone's output angles (`+140..+152`) + translation each native frame and render a
   lerp/slerp pose on the 3 in-between 60 fps frames. Motion is velocity-integrated
   (C1-continuous) so interpolation is visually correct. No VM/timing change.
2. **Half-rate integration:** halve the velocity contribution in `GF_Ifrit_AnimIntegrator` and
   double every wait/hold (`bone+200`, yield count `state+62`) → native 60 fps, but this
   touches the timing model (audio/camera sync).

Because this VM shape is shared with battle `.dat` model animation, output-pose interpolation
is a candidate **unified** fix for GF creatures *and* characters/enemies. (`mag184` **Shiva**
is documented as having a frame-count header, so some chains may store data differently —
verify per GF.)

### Quezacotl: a timeline-family GF animates like an ordinary battle model

Quezacotl (effect **116**) was read specifically to test whether the Ifrit VM generalises. **It does
not.** Quezacotl is a *timeline* GF reached through a 14-byte thunk (`MAG_116_QUEZACOTL` 0x6C3550
→ `GF_116Quezacotl_SetupSummon` 0x6C3640, offset +0xF0), and **nothing in the summon ever touches
`*0x27973EC`**. Its creature animates through the **standard battle-model path**:

```c
au_re_Battle_ReadAnimation_6(&node[3].next, 0..2)     // 0x6574D0
  -> pre_Battle_ReadAnimation (0x509440)
    -> Battle_ReadAnimation (0x508F90)                // the same leaf the model gate hooks
BS_ComputeBonesWorldMatrices((BattleAnimHeader *)(modelBuffer + 136), ...);
ProcessFieldEntitiesTransformation((BattleAnimHeader *)(modelBuffer + 136));
```

So there is no opcode VM and no velocity integrator here — it is a `BattleAnimHeader` skeleton, the
same machinery characters and monsters use. Five other GFs sit behind thunks in the same timeline
region (Griever, Phoenix, Carbuncle, Pandemona, Diablos), so **FF8's GFs are split across two
unrelated animation implementations** — see the [census](../../list/magic-effect-census/).

**Why a ctx-windowed frame-hold cannot work on it.** `GF116_QUEZACOTL_modelBuffer` is
`Magic_TextureOFF_ToEAX1()` — the **magic texture buffer** (~`0x20DFAB8`), filled in `SetupSummon`
by `qmemcpy`ing `0x109FC` + `0x4D9C` bytes out of `.data`. The creature's skeleton and animation
state therefore live at `modelBuffer + 136`, roughly **4.4 MB away** from the effect's own globals
(`0x25216D8`…`0x25217B0`) and from the root queue it returns (`0x2521748`). A snapshot/restore hold
windowed on the returned context (e.g. `ctx − 0x2000`, size `0x8000`) simply **does not contain the
state it is trying to freeze**. That is a concrete, address-level reason the generic frame-hold left
Quezacotl at 4× — separate from the `*0x27973EC` cine-path question.

The summon's own timeline is `++task_node[1].flags_and_priority` in
**`GF_116Quezacotl_SequenceTask` (0x6C3760)**, once per tick — that single task also flips the
double-buffered packet arena, spawns the creature at counter `== 2`
(`GF_116Quezacotl_CreatureTask`, a 0x8D0-byte node), and drives every particle queue. It is
therefore the natural 1-in-4 gate point for this GF. **Untested in-game** — this is a code-reading
conclusion, not a confirmed fix.

### Creature model storage (timeline family)

Every timeline-family creature — GF summons (Quezacotl, Shiva, Siren, Pandemona, Doomtrain,
Diablos, Carbuncle, Odin, Gilgamesh, Phoenix, Cactuar, Tonberry) and effect companions
(Angelo, Boko, Mog/MiniMog, Moomba, the Death reaper, the Absorbed-Into-Time cherub) — is a
**standard 4-section battle-model container** (same layout as `c0mXXX.dat` sections 1–3), either
shipped as a file of its mag group or embedded in `FF8_EN.exe` `.data` and resolved by
`Effect_BindModelContainerSections` (0x6EC060) / `Effect_BindModelContainerSetAnim` (0x8DD0F0)
before entering `Battle_ReadAnimation`. The complete census of model and texture locations,
with all addresses, is on [Summon Creature Models](../summon-creature-models/).

## Runtime evidence summary

| GF | Test id | Key confirmations |
|----|---------|-------------------|
| Ifrit | GF_IFRIT_001 | cmd_arg `0x42`, callback pointer, tick and counter |
| Diablos | GF_DIABLOS_001 | cmd_arg `0x45`, gravity HP reduction, `COMMAND_TYPE_ID=0xFE` |
| Cerberus | GF_CERBERUS_001 | cmd_arg `0x49`, Double+Triple, support GF with 0 damage |
| Doomtrain | GF_DOOMTRAIN_001 | Multi-status and damage pipeline |
| Siren | GF_SIREN_001/002 | Silence infliction |
| Pandemona | GF_PANDEMONA_001 | cmd_arg `0x48`, pending transfer, enemy HP decrease |
| Tonberry | GF_TONBERRY_002 | Tick, counter and completion confirmed |

## Function addresses

| Function | Address | Description |
|---|---|---|
| `MagicList_Logic` | 0xC81774 | Global variable/data, not a function |
| `SG_ODIN_ANGEL_GILGA_FLAG` | 0x1CFE97A | Global variable/data, not a function |
| `BattleActionSequence_Tick_GF_Cinematic` | 0x50B2A0 | Reads the GF effect id and dispatches to `MagicList_Logic` (verified IDA function) |
| `MAG_325_UNKNOWN` (Diablos `MagicList_Logic` thunk) | 0x6541E0 | Thunk that forwards to the real Diablos entry (verified IDA function) |
| Diablos real entry (`sub_654210` in IDA) | 0x654210 | Diablos GF entry point (verified IDA function, not yet named in IDA) |
| `Effect_AddTaskAndInitFromCtx` (formerly documented as `BdLinkTask_CreateAndInitContext`) | 0x8DC540 | Shared task constructor used by multiple GFs (verified IDA function) |
| `rollOdinAutoSummon` (formerly documented as `ZANTETSUKEN_sub_482DF0`) | 0x482E00 | Battle-start Odin roll (verified IDA function) |
| `summonGilgaAngelStartFight` (formerly documented as `AngeloOdin_SpecialActionTick`) | 0x482F80 | Per-frame Gilgamesh/Angelo auto-action tick (verified IDA function) |
| `managePhoenixInvocWhenGameOver` (formerly documented as `BattleFrame_PartyWipeCheck`) | 0x486450 | Scans party slots for a wipe each active battle frame (verified IDA function) |
| `computePhoenixInvoc` (formerly documented as `Phoenix_BattleFrame_TriggerCheck`) | 0x483270 | Phoenix trigger roll; same function as on Enemy AI VM Runtime (verified IDA function) |
| `MAG_201_IFRIT_SUMMON_HELL_FIRE_FL` (`MagicList_TextureLoad[200]`) | 0xB25750 | Ifrit's texture loader entry (verified IDA function) |
