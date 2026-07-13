---
title: Animation sequences
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/animation-sequences/
nav_order: 5
author: HobbitDur
---

1. TOC
{:toc}

## Animation sequences

### Header

| Offset | Length                 | Description         |
|--------|-------------------------|----------------------|
| 0      | 2 bytes                | Number of sequences |
| 2      | nbSequences \* 2 bytes | Sequences Positions |

Contain sequence of animation. They define specific movement/action when using an ability/or just being.
Some old info can be found here: [Qhimm message](https://forums.qhimm.com/index.php?topic=19362.0)

Now how it works. The sequence animation is composed of opcode, followed by parameters (often 1, sometimes 2 or 0). Each op code define an action to do.

### Execution model

The sequences are executed by a small byte-code VM (`computeAnimationSequence` at `0x50DB40` in FF8_EN.exe). The VM itself only implements the arithmetic
opcodes (`C0`-`E5`) and the conditional jumps (`E6`-`F3`); everything below `0xC0` is delegated to a callback. The same VM is reused with different callbacks
for:

- **Entity sequences** (this section): callbacks `AnimSeq_DispatchActionOpcode` (opcodes &lt; 0xC0), `AnimSeq_ReadSpecialVar_C3` (C3-family special reads) and
  `AnimSeq_WriteSpecialVar_E5` (E5 special writes).
- **Camera sequences** ([camera sequence](../camera-sequence/)): same VM with camera-specific callbacks (see that section).

The per-frame driver (`AnimSeq_UpdateEntityPerFrame` at `0x504290`) runs every battle frame:

1. If a *background sequence id* was set (opcode `9A`), that sequence is executed first, every frame.
2. The main sequence resumes at the byte offset saved from the previous frame (`currentSequenceCurrentByte`).
3. The interpreter runs until an opcode *pauses* it: queuing an animation (opcode &lt; 0x80), `A1` (yield), `A9` (terminate), `AC`, or `B9` (frame wait). The
   current byte offset is then saved and execution resumes there the next frame.

All `int16` parameters are **little-endian**.

**Sequences played at battle start:** `initAnimationSequenceAtStartBattle` (`0x5027D0`, run once per entity) queues **sequence 8** as the first sequence (the battle-entrance / scene-in animation). It also sets the idle fallback `basedAnimSeq` to **1** — or to the sequence queued by the entity's initial statuses (e.g. starting dead/asleep), or to an override byte passed by the spawner for scripted mid-battle spawns.

**Base sequence ID (`basedAnimSeq`):** the sequence the entity returns to when nothing else is queued — its "idle". Defaults to 1 at battle start. It can be changed by opcode `A3` (adopts the current sequence as the new base) or via `E5 0x0B`, and read via `C3 0x0B`. When a sequence ends (`A2`) with nothing queued, **monsters** return to `basedAnimSeq`, while **characters** (com_id &lt; 0x10) instead pick a sequence from their [animation status]({{site.baseurl}}/technical-reference/list/battle-animation-state/#default-sequence-ids) (dead → 3, sleeping/weakened → 2, running → 16, preparing attack → 19, defending → 29, else 1).

### Opcode between C0 and E3: set a "current_value"

Those opcode are meant to store and modify a local values (that is then used by later opcodes).  
To analyze it, it is done on two part. First defining how to use the param, then knowing how to modify the local variable (store in what is called the _stack_)

#### How to interpret the params

Do OpCode & 3:

- case 0: 2 param int16 value (C0, C4, D0,...)
- case 1: 1 param sign value (C1, C5, C9, D1, D5, D9, DD,...)
- case 2: 1 param unsigned value (C2, C6, D2, DA,...)
- case 3: 1 param, two cases: (C3, C7, CB, CF, D3...)
    - Param < 0x80: special handle to set param value (cf dedicated chapter).
    - Param >= 0x80: Read from stack value stored at param (from E5 opcode)

#### How to modify the local var

Do opcode & FC:

- case 0xC0u: (C0, C1, C2, C3)
  current_value_computed = param;
- case 0xC4u:// C4, C5, C6, C7
  current_value_computed += param;
- case 0xC8u:
  current_value_computed -= param;
- case 0xCCu:
  current_value_computed *= param;
- case 0xD0u:
  current_value_computed /= param;
- case 0xD4u:
  current_value_computed &= param;
- case 0xD8u:
  current_value_computed |= param;
- case 0xDCu:
  current_value_computed ^= param;
- case 0xE0u:
  current_value_computed %= param;

#### Case 3 param < 0x80:

On each case a specific code is done, often it just read a value in memory that as a specific purpose.
Full list (from `AnimSeq_ReadSpecialVar_C3` at `0x5044B0`):

| Param              | Value read                                                                                                                  |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------|
| 0x00-0x07          | Local variable `e5_data_saved[param]` of the entity (written by E5 0x00-0x07)                                               |
| 0x08               | [Battle state controller flags]({{site.baseurl}}/technical-reference/list/battle-animation-state/#battle-state-controller-flags-some_flag) |
| 0x09               | Current frame of the active animation                                                                                       |
| 0x0A               | Total frames of the active animation                                                                                        |
| 0x0B               | [Base sequence id](#execution-model) (`basedAnimSeq`, the idle the entity returns to)                                       |
| 0x0C               | Random value [0..32767]                                                                                                     |
| 0x0D               | Position Z                                                                                                                  |
| 0x0E               | Position X                                                                                                                  |
| 0x0F               | Position Y                                                                                                                  |
| 0x10               | Speed depending of distance to target. On itself, speed_factor = 1000. On a target, speed_factor = 5000\*distance/4096      |
| 0x11               | Speed from 0x10 adjusted: Speed_0x10 - (2000\*(attacker_speed_factor + target_speed_factor)/4096). Set to 1000 if on itself |
| 0x12               | Stored sine (set via E5 0x12)                                                                                               |
| 0x13               | Stored cosine (set via E5 0x13)                                                                                             |
| 0x14-0x16          | Weapon anim data words at +28/+30/+32 (writable via E5 0x14-0x16), 0 if no weapon                                           |
| 0x17               | Y rotation & 0xFFF                                                                                                           |
| 0x18               | Slot id of the current target                                                                                               |
| 0x19               | Hit flag 2 of the current target (`hitType2 & 2`)                                                                           |
| 0x1A               | Angle between the target and the attacker & 0xFFF                                                                           |
| 0x1B               | Own slot id                                                                                                                 |
| 0x1C               | 2048 if monster; else 0 if (rotY & 0xFFF) <= 2048, else 4096                                                                |
| 0x1F               | [Animation status flags]({{site.baseurl}}/technical-reference/list/battle-animation-state/#entity-animation-status-flags-anim_status) (`anim_status`) |
| 0x22               | Back attack / preemptive strike info                                                                                        |
| 0x23               | Camera flag (shared with camera sequences)                                                                                  |
| 0x24               | Model size scale                                                                                                            |
| 0x25 / 0x26 / 0x27 | Z / Y / X scale                                                                                                             |
| 0x28               | 1 if GF summon data loaded, else 0                                                                                          |
| 0x29               | Number of targets the current action successfully hit (the action-result hit count, prepared when the results are computed) — lets a sequence branch on how many targets were actually affected |
| 0x2A               | Animation speed factor                                                                                                      |
| 0x2C               | Original sceneout position X                                                                                                |
| 0x2E               | 1 if another entity is alive and free (not dead/stopped/petrified), else 0                                                  |
| 0x33               | Combat scene ID                                                                                                             |
| 0x35               | Y offset of target's effect-spawn point 0xF1 above its base Y                                                               |
| 0x36               | Y offset of target's effect-spawn point 0xF0 above its base Y                                                               |
| 0x37               | Invisibility flag                                                                                                           |
| > 0x77             | `current_value = *(E5_7F_save + 2 * (0x7F - param))`; so at 0x7F it's E5_7F_save[0]                                         |

Unlisted values return 0.

### E5 case:

two cases:
Param < 0x80: special handle to save (and use) the current_value
Param >= 0x80: Write to stack current_value at param

#### Param < 0x80

Full list (from `AnimSeq_WriteSpecialVar_E5` at `0x5048E0`):

| Param              | Effect                                                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------|
| 0x00-0x07          | Write local variable `e5_data_saved[param]` (readable via C3 0x00-0x07)                                                  |
| 0x08               | Write the [battle state controller flags]({{site.baseurl}}/technical-reference/list/battle-animation-state/#battle-state-controller-flags-some_flag) |
| 0x0B               | Set the [base sequence id](#execution-model) (`basedAnimSeq`, the idle the entity returns to)                             |
| 0x0D               | Set position Z                                                                                                           |
| 0x0E               | Set position X                                                                                                           |
| 0x0F               | Set position Y                                                                                                           |
| 0x12               | Compute and store sin(current_value) (readable via C3 0x12)                                                              |
| 0x13               | Compute and store cos(current_value) (readable via C3 0x13)                                                              |
| 0x14-0x16          | Write weapon anim data words at +28/+30/+32 (no-op if no weapon)                                                         |
| 0x17               | Rotate the entity (Y rotation, 0-4096)                                                                                   |
| 0x1D               | Move hit particle position (written into skeleton header)                                                                |
| 0x1E               | Move selection cursor position (written into skeleton header)                                                            |
| 0x20               | Hide/show a model part: value > 0 hides geometry object (value-1), value < 0 shows object (-1-value). See opcodes 81/A6 |
| 0x21               | Same as 0x30 (target forwards/backwards rotation)                                                                        |
| 0x24               | Set model scale (4096 is 1x scale)                                                                                       |
| 0x25 / 0x26 / 0x27 | Set Z / Y / X scale                                                                                                      |
| 0x2A               | Set animation speed factor                                                                                               |
| 0x2B               | Set the entity's camera var (readable from camera sequences via camera-C3 0x15)                                          |
| 0x2C               | Set X position (also updates original sceneout X)                                                                        |
| 0x2D               | Set target's Y scale (makes target flat)                                                                                 |
| 0x2F               | Set a global linked to battle stage 137 (Edea's room)                                                                    |
| 0x30               | Set target's rotation (forwards/backwards) (gets reset when target comes back from an attack)                            |
| 0x31               | Set target's rotation (left/right) (gets reset when target comes back from an attack)                                    |
| 0x32               | Set target's rotation (lean to a side) (gets reset when target comes back from an attack)                                |
| 0x34               | Set target's Y position                                                                                                  |
| > 0x77             | `*(E5_7F_save + 2 * (127 - param)) = current_value` (so 0x7F writes E5_7F_save[0])                                       |

### 0xE4: set to zero (BUGGED)

`E4` sets `current_value = 0` but **never advances the instruction pointer**: the interpreter re-reads the same byte forever and the game hangs. Confirmed in
FF8_EN.exe (`xor esi, esi` then jump back to the opcode fetch). Do not use it; use `C1 00` instead.

### 0xE6 to 0xF3: jumps

Those are conditional jumps (if). They check `current_value` and either continue the flow or jump. The jump target is **relative to the address of the jump
opcode itself**: `new_position = opcode_position + offset` (the offset is signed, so backward jumps are possible — offset 0 would hang).

Byte-offset versions (1 signed byte param, opcode size 2):

- E6: Unconditional jump
- E7: jump if current_value > 0
- E8: jump if current_value >= 0
- E9: jump if current_value == 0
- EA: jump if current_value != 0
- EB: jump if current_value <= 0
- EC: jump if current_value < 0

int16 versions (2 bytes little-endian offset, opcode size 3), same conditions:

- ED: Unconditional jump
- EE: current_value > 0
- EF: current_value >= 0
- F0: current_value == 0
- F1: current_value != 0
- F2: current_value <= 0
- F3: current_value < 0

When the condition is not met, execution continues after the parameter (opcode + 2 bytes for E6-EC, opcode + 3 bytes for ED-F3).

### Opcode < 0x80

This queues the animation by the ID defined in [Model animation](../model-animation/) and pauses the sequence until the animation finishes
(sets [state controller flags]({{site.baseurl}}/technical-reference/list/battle-animation-state/#battle-state-controller-flags-some_flag) 0x002 + 0x008 and stops the interpreter for this frame).

## 0x80 <= Opcode < C0

Full opcode list (decoded from `AnimSeq_DispatchActionOpcode` at `0x504BB0` in FF8_EN.exe). Opcodes not listed (87-8F, B3) are no-ops with no parameter.

| Opcode             | Params | Description                                                                                                                                                                                                                                                                                                                                          |
|--------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 80 XX              | 1      | Step **dynamic texture animation** XX ([dynamic texture data](../dynamic-texture-data/)). If `number_destination` > 0: advances the frame counter (data byte 6 = speed in 1/8th frame units, byte 7 = counter) and blits the next dest UV. If `number_destination` == 0: scrolls the texture region in VRAM by byte 6 pixels (UV scroll, e.g. conveyor/water)                               |
| 81 XX              | 1      | Restore hidden model part XX: clears bit XX of the hidden-parts bitmask (set via E5 0x20) and runs a 15-frame re-attach effect                                                                                                                                                                                                                       |
| 82                 | 0      | Set combat flag 0x40. **No reader of this flag has been found in the PC executable** — every located consumer of the combat-flags byte tests other bits — so the opcode appears to have no effect (either vestigial, or read by an untraced raw-offset access)                                                                                        |
| 83 XX              | 1      | Load battle stage camera/geometry (XX = load command bitmask)                                                                                                                                                                                                                                                                                        |
| 84 XX              | 1      | Start a sine-wave vertex animation task (model wobble), XX = wave parameter                                                                                                                                                                                                                                                                          |
| 85                 | 0      | Hide the yellow triangle of chara selection (clears the flag)                                                                                                                                                                                                                                                                                        |
| 86                 | 0      | Show the yellow triangle of chara selection (sets the flag)                                                                                                                                                                                                                                                                                          |
| 90 XX              | 1      | **Multi-part monster link**: XX < 3 unlinks the whole chain; 3 <= XX < 0x10 links self to monster slot XX; XX >= 0x10 links self to the loaded monster whose com_id == XX. Linked entities form a circular chain with two effects: a sequence queued on one of them starts **simultaneously on every part**, and each part **copies the transform matrix of the chain head** every frame so the parts move as one body (used by Ultimecia final form, etc.) |
| 91 XX YY           | 2      | Print monster battle text XX with param YY (urgent text channel)                                                                                                                                                                                                                                                                                     |
| 92 XX              | 1      | **Setup targeting context.** Recomputes everything the attack choreography relies on: the C3 0x10/0x11 speed factors (used to scale walk-in distance/duration by how far the target is), the current target slot (C3 0x18), the attacker→target angle (C3 0x1A), and physically rotates the attacker to face the target. Two modes: XX < 7 → change the target to slot XX (attacker unchanged); XX >= 7 → make *self* the attacker and keep the current target mask (typical at the start of a monster's attack sequence, since the engine already selected the targets). Multi-target actions get the centre point of all targets as the reference |
| 93 XX YY           | 2      | Trigger sequence YY on another entity: XX < 0x10 = slot id; XX >= 0x10 = every loaded entity (except self) with com_id == XX                                                                                                                                                                                                                         |
| 94                 | 0      | Toggle the shadow                                                                                                                                                                                                                                                                                                                                    |
| 95                 | 0      | Reset current position to original position (X and Z)                                                                                                                                                                                                                                                                                                |
| 96 X1 X2 X3        | 3      | **Camera shake** (earthquake): offset interpolated from X1 to X2 over X3 frames, sign alternating every frame                                                                                                                                                                                                                                        |
| 97                 | var    | Play actor sound effect: same encoding as B8 but plays through the actor SE path (`linkedToSoundAnimSeq(addr, 0x80)`)                                                                                                                                                                                                                                |
| 98                 | var    | Same as 97, second variant (`linkedToSoundAnimSeq(addr, 0x81)`)                                                                                                                                                                                                                                                                                      |
| 99 XX YY..FF       | var    | Queue **walk/step effect + sound** timeline on bone XX. Each following byte: bits 0-5 = frames to wait, bit 6 = skip effect, bit 7 = skip sound. List ends with FF                                                                                                                                                                                   |
| 9A XX              | 1      | Set **background sequence id** XX. Every frame, the driver runs sequence XX **from its beginning** (no saved position) before resuming the main sequence. It should therefore only contain per-frame logic (C3/E5 computations, e.g. keep facing the target) and end quickly — it must not queue animations or wait. Cleared by writing 0; skipped while combat flag 0x08 is set |
| 9B XX YY           | 2      | Start texture animation XX with destination index computed through the C3 special-value reader from YY                                                                                                                                                                                                                                               |
| 9C                 | 0      | Turn back (combat_flags  = TURN_BACK)                                                                                                                                                                                                                                                                                                                |
| 9D                 | 0      | Mark self as dead/removed in the battle bookkeeping data (flag 0x40, status bit 0, setMaskEnable)                                                                                                                                                                                                                                                    |
| 9E XX YY           | 2      | Move self smoothly toward entity slot XX, YY = speed/step parameter                                                                                                                                                                                                                                                                                  |
| 9F XX..FF          | var    | **Blink timeline**: each byte = frame delay before toggling texture animation 0 on/off; ends with FF. The task auto-ends when the sequence changes                                                                                                                                                                                                   |
| A0 XX              | 1      | Play animation XX **without pausing the sequence**: unlike opcode &lt; 0x80 (which stops the interpreter until the animation's last frame), A0 switches the animation and the following opcodes keep executing on the same frame (used with A1/B9 loops to script movement during the animation). If XX is already the current animation, it is left running (not restarted) — unless flag 0x004 is set (animation finished, or forced by A4)         |
| A1                 | 0      | **Yield**: pause the sequence for this frame, resume at the next opcode next frame                                                                                                                                                                                                                                                                   |
| A2                 | 0      | **End of sequence (normal)**: reset base rotation, then immediately continue into the next sequence — the queued one if any, else the idle fallback (`basedAnimSeq` for monsters, status-based for characters). Execution of the new sequence starts on the same frame                                                                                |
| A3                 | 0      | Set current sequence as the new base sequence (`basedAnimSeq`); jump to the pending next sequence if it exists, else set the idle-interruptible flag (0x040)                                                                                                                                                                                         |
| A4                 | 0      | Set the "animation finished" flag (0x004). That flag is normally set automatically when the current animation reaches its last frame; setting it manually forces the next `A0 XX` to **restart** animation XX even if it is already playing                                                                                                          |
| A5 XX              | 1      | Trigger magic/limit effect (loads from magic.fs etc.). XX forced to 01 when battle flag 0x40000000 is set: <br>- 00: character/boss magic effect<br>- 01: GF summon<br>- 02: normal limit break<br>- 03: finisher limit break<br>- 04: enemy magic effect<br>- 05: like 04 (placeholder, unused)                                                     |
| A6 X1 + 4×int16    | 9      | **Detach model part** (body parts falling/flying off, e.g. Gerogero). X1 = object index in [model geometry](../model-geometry/) (the model part). The part detaches from the skeleton at its current bone position and flies off with initial velocity (vx, vy, vz) given by the first three int16; each frame the velocity decays by 1/8 (air drag) and +100/frame is added on Y (gravity), so the part follows a ballistic arc for the 15 frames the task runs. The 4th int16 is copied into the task structure but the per-frame update never reads it back, so in practice it has no effect. The part is simultaneously flagged in the hidden-parts bitmask (same bitmask as E5 0x20); opcode 81 restores it later |
| A7 XX              | 1      | **Jump to sequence XX** (a *goto*, not a call: the instruction pointer is set to the start of sequence XX and `currentAnimSeqId` is updated — there is no return; end XX with A2/A9 like any sequence)                                                                                                                                                |
| A8 XX              | 1      | Fade / visibility: <br>- 01: slowly disappear (re-appears suddenly at the end)<br>- 02 or 0C: re-appear<br>- 03: disappear and stay invisible<br>- 06: leave combat by disappearing (no XP gained)                                                                                                                                                   |
| A9                 | 0      | **End of sequence (hard stop)**: unlike A2 (which chains into the next/idle sequence on the same frame), A9 bakes the current animation transforms into the entity (`TerminateSequenceAndUpdateTransforms`, model + weapon) and **stops the interpreter for this frame**; the next sequence is resolved by the driver on the following frame          |
| AA                 | 0      | Apply the pending **action result** to **all targets** at once. "Applying the result" means: show the damage/heal numbers, apply the status changes (with their visual side effects: petrify task, eject fade-out, elemental weakness flash...), queue the target's hit/death animation, and handle the counter-attacker if any. Use AA for single-hit or simultaneous-hit actions; use B2/B7 instead to spread the results over a multi-hit choreography                                                  |
| AB X1 X2 ... A1    | var    | **Renzokuken init** (character weapons only). Reads two bytes, then *pre-scans* the rest of the sequence up to the next A1 without executing it: for every animation opcode (&lt; 0x80) it looks up the animation's frame count in [model animation](../model-animation/) and accumulates it; each A0 closes the current bucket and starts a new one. The resulting list of per-stage durations (in frames) is what drives the R1-trigger timing bar — i.e. the timing windows are computed from the actual animation lengths of the slashes that follow. Execution then resumes normally at the opcodes that were scanned |
| AC XX              | 1      | Restore the base model (undo model swap: comFileData = comFileDataBis, also for the weapon), reset rotation, queue sequence XX \| 0x1000 (auto-pick if XX = 0) and end the sequence                                                                                                                                                                  |
| AD X1 X2X3 X4      | 4      | Shorthand for AE with the midpoint bone forced to FF: `AD X1 X2X3 X4` behaves exactly like `AE X1 FF X2X3 X4` (drag the target to a single attacker bone, no midpoint averaging). See AE for the full explanation                                                                                                                                     |
| AE X1 X2 X3X4 X5   | 5      | **Drag/carry the target** (grab moves, e.g. a monster picking up a character or holding it in its jaws). Starts a per-frame task that, for X5 frames, moves the current target so it sticks to a point on the attacker: X1 = attacker bone id defining that point (X1 = FF uses the target's own base position instead — effectively pinning the target in place; bit 7 of X1 selects which reference point of the target is matched to it, its centre or its base). X2 = optional second attacker bone: when not FF the anchor point is the midpoint between bones X1 and X2 (e.g. between the two jaws). X3X4 = int16 interpolation factor along the bone (0..4096, where to sit between the bone's joint and its tip). While the drag runs the target's shadow is hidden; when the X5 frames elapse the shadow is restored (the target's position is *not* automatically reset — the engine's snap-back reaction handles that on hit) |
| AF XX              | 1      | Trigger sequence XX on the current target                                                                                                                                                                                                                                                                                                            |
| B0 XX FF ..        | var    | **Spawn a hit/impact particle effect on the attacker** (sparks, dust, slash flashes at the moment a blow lands, drawn on the *attacker's* model). First byte = effect id, second byte = flag byte controlling where the effect spawns and how many extra parameter bytes follow (specific bone, random bone, custom 3D position, or default placement — see the flag table below). Unlike B4 it is always shown, even on a miss                                                                            |
| B1 XX YY..FF       | var    | Same as 99 but for the SFX variant (walk sound type 2)                                                                                                                                                                                                                                                                                               |
| B2                 | 0      | Apply the action result (see AA) to the current target, then **advance `CURRENT_TARGET_DATA` to the next target**. This is how a sequence walks through the victims of a multi-target attack one by one: everything that says "current target" (BF, B4, AD/AE, AF, C3 0x18/0x19...) now refers to the next one                                                                                                                                        |
| B4 XX FF ..        | var    | **Impact on the target**: same byte encoding as B0, but the particle effect spawns on the **target's** model, and two extra things happen first: the target's *snap-back reaction* is applied if flagged (a dragged target is teleported back to its owner slot position and plays sequence 22), and the whole visual is **skipped when the attack missed** (the parameter bytes are still consumed — except the bone byte of flag bit 0x08, see the warning in the flag table). B4 is the standard "the blow connects" opcode paired with BF in attack sequences                                          |
| B5 / B6 X1 X2 (X3) | var    | Play local (monster .dat [sounds](../sounds/) AKAO) sound X1. X2 = flag byte (see B8). X1 >= 7 unexpected                                                                                                                                                                                                                                       |
| B7                 | 0      | Apply the action result (see AA) to the **current target only**, without advancing to the next one (contrast with B2). Useful when the sequence wants to show the result mid-choreography and keep acting on the same target afterwards                                                                                                                                                                                                              |
| B8 X1 X2 (X3)      | var    | Play sound X1 from the general audio list. X2 flag byte:<br>- & 0x4: volume = 128<br>- else & 0x1: volume from target's position on screen, else from attacker's position<br>- & 0x2: one more param X3 = channel mask<br>When the attack missed, plays the miss sound instead                                                                       |
| B9 XX              | 1      | **Wait XX - 1 frames** before executing the next opcode (pauses the interpreter)                                                                                                                                                                                                                                                                     |
| BA                 | 0      | Advance the current animation by one frame (manual tick)                                                                                                                                                                                                                                                                                             |
| BB                 | 0      | Print the pending battle text (ability/attack name), if one is flagged                                                                                                                                                                                                                                                                                |
| BC XX              | 1      | Nop (parameter ignored)                                                                                                                                                                                                                                                                                                                              |
| BD XX YY           | 2      | Start texture animation XX with destination index YY                                                                                                                                                                                                                                                                                                |
| BE XX              | 1      | Stop texture animation 0; XX != 0 sets the GF-hidden status flag (model hidden during GF summon), XX == 0 clears it                                                                                                                                                                                                                                  |
| BF XX              | 1      | **Moment of impact — make the target flinch.** Triggers sequence XX on the *current target* (XX is a sequence id in the **target's** .dat, typically its "take a hit" flinch). The engine has already computed the outcome of the attack per target, so BF silently does nothing when the impact should not be shown: attack missed / no hit reaction decided, a snap-back reaction is pending (target was dragged and gets teleported back instead), target is defending or invincible, or target is not interruptible (neither idle nor already in a damage state). Note that BF only plays the reaction *animation* — the damage numbers and statuses are applied by AA/B2/B7. Typical use: right after each hit in a multi-hit attack (see the Bite Bug example: `BF 04` after each bite) |

### B0/B4 flag byte

The second byte of B0/B4 defines the parameter count and the effect placement:

| Bit                    | Meaning                                                                                                                                                                                                                  |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x01                   | One more byte (effect param 1)                                                                                                                                                                                           |
| 0x02                   | One more byte (effect param 2; bit 7 of it is forced from the camera angle)                                                                                                                                              |
| 0x04                   | One more byte (effect param 3)                                                                                                                                                                                           |
| 0x08                   | Spawn the effect at a specific bone → one more byte (bone id). **Warning**: the game consumes this byte only when the attack hits; on a miss (B4) it would be executed as the next opcode. Vanilla data avoids this case |
| 0x10                   | Spawn the effect at a random bone (no extra byte)                                                                                                                                                                        |
| 0x20                   | Flip the effect direction (used with 0x08/0x10)                                                                                                                                                                          |
| 0x40                   | Custom position → three more int16 LE (x, y, z)                                                                                                                                                                          |
| none of 0x08/0x10/0x40 | Spawn the default effect on the entity                                                                                                                                                                                   |

### Example

Normal attack sequence of the Bite Bug, fully annotated:

**Walk toward the target:**

- `C3 11`: current_value = adjusted speed factor (distance-scaled)
- `C5 64`: current_value += 100
- `E5 FF`: stack[0xFF] = current_value
- `C1 00`: current_value = 0
- `CB FF`: current_value -= stack[0xFF] (negate: total distance to cover)
- `E5 02`: local var e5[2] = current_value
- `BB`: print the attack name
- `08`: play animation 08 and wait (attack stance)
- `A0 09`: play animation 09 without waiting (fly forward)
- `C3 0A`: current_value = total frames of the current animation
- `E5 7F`: E5_7F_save[0] = current_value (loop counter = frame count)
- **loop start:**
- `C3 02` `C9 00` `E5 FF`: stack[0xFF] = e5[2]
- `C3 FF` `CF 09` `E5 FE`: stack[0xFE] = e5[2] * current_frame
- `C3 FE` `D3 0A` `E5 FD`: stack[0xFD] = e5[2] * current_frame / total_frames (linear interpolation)
- `C1 00` `C7 FD`: current_value = stack[0xFD]
- `E5 0F`: write the position offset → the model slides toward the target
- `A1`: yield (resume next frame)
- `C3 7F` `C5 FF` `E5 7F`: decrement the loop counter
- `E7 E1`: if counter > 0, jump back 0x100-0xE1 = 31 bytes (loop start)

**Bite three times:**

- `A0 0A`: play animation 0A without waiting (bite)
- `B9 06`: wait 5 frames
- `97 02 01`: play actor sound 02, volume from the target's position
- `BF 04`: if the attack connected, trigger hit sequence 04 on the target
- `B4 1A 00`: apply hit reaction + spawn hit effect 0x1A on the target (default placement)
- `B9 04`: wait 3 frames
- `97 02 01` `BF 04` `B4 1A 00`: second bite
- `B9 04` `97 02 01` `B4 1A 00`: third bite
- `AA`: apply the action result (damage/status) to all targets
- `C3 08` `DA 80` `E5 08`: state flags |= 0x80
- `C3 08` `D9 08` `E5 08`: state flags |= 0x08
- `A1`: yield

**Walk back:**

- `A0 0B`: play animation 0B without waiting (fly back)
- `C3 0A` `E5 7F`: loop counter = total frames
- `C1 00` `CB 02` `E5 FF`: stack[0xFF] = -e5[2] (reverse direction)
- `C3 FF` `CF 09` `E5 FE` `C3 FE` `D3 0A` `E5 FD`: interpolate as before
- `C3 02` `C7 FD` `E5 0F`: position = e5[2] + interpolated value (slides back home)
- `A1`: yield
- `C3 7F` `C5 FF` `E5 7F` `E7 E1`: decrement and loop
- `0C`: play animation 0C and wait (landing)
- `A2`: end of sequence (jump to the next queued/idle sequence)
