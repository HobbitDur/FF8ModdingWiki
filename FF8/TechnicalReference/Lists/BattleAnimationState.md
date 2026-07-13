---
layout: default
title: Battle animation state
parent: List
permalink: /technical-reference/list/battle-animation-state/
---

1. TOC
{:toc}

Reference for the per-entity animation state used by the [animation sequences]({{site.baseurl}}/technical-reference/battle/model-sections/animation-sequences/) (readable/writable via the C3/E5 special variables).

# Entity animation status flags (anim_status)

32-bit flag field on each battle entity, readable from a sequence via `C3 0x1F`. Most bits are refreshed from the entity's [statuses]({{site.baseurl}}/technical-reference/list/status-flags/) through a lookup table (`getAnimMaskFromStatus` at `0x509BA0` in FF8_EN.exe); the engine-controlled bits (marked *engine*) survive that refresh.

| bit | Flag       | Meaning                              | Source                 |
|-----|------------|--------------------------------------|------------------------|
| 0   | 0x00000001 | Weakened (HP < 25%)                  | Status 1 bit 8         |
| 1   | 0x00000002 | Death                                | Status 1 bit 0         |
| 2   | 0x00000004 | Back attack                          | Status 2 bit 23        |
| 3   | 0x00000008 | Stop                                 | Status 2 bit 3         |
| 4   | 0x00000010 | Petrify                              | Status 1 bit 2         |
| 5   | 0x00000020 | Poison                               | Status 1 bit 1         |
| 6   | 0x00000040 | Darkness                             | Status 1 bit 3         |
| 7   | 0x00000080 | Silence                              | Status 1 bit 4         |
| 8   | 0x00000100 | Berserk                              | Status 1 bit 5         |
| 9   | 0x00000200 | Float                                | Status 2 bit 13        |
| 10  | 0x00000400 | Zombie                               | Status 1 bit 6         |
| 11  | 0x00000800 | Confusion                            | Status 2 bit 14        |
| 12  | 0x00001000 | Sleep                                | Status 2 bit 0         |
| 13  | 0x00002000 | Gradual petrify                      | Status 2 bit 12        |
| 14  | 0x00004000 | Haste                                | Status 2 bit 1         |
| 15  | 0x00008000 | Slow                                 | Status 2 bit 2         |
| 16  | 0x00010000 | Unknown                              | -                      |
| 17  | 0x00020000 | Aura                                 | Status 2 bit 8         |
| 18  | 0x00040000 | Curse                                | Status 2 bit 9         |
| 19  | 0x00080000 | Doom                                 | Status 2 bit 10        |
| 20  | 0x00100000 | Invincible                           | Status 2 bit 11        |
| 21  | 0x00200000 | Defend                               | Status 2 bit 19        |
| 22  | 0x00400000 | Eject                                | Status 2 bit 16        |
| 23  | 0x00800000 | Preparing attack                     | *engine*               |
| 24  | 0x01000000 | Running / moving to target           | *engine*               |
| 25  | 0x02000000 | Vit0                                 | Status 2 bit 24        |

The "weakened look" group tested by the engine is `0x41021` (weakened, poison, sleep, curse).

# Battle state controller flags (some_flag)

16-bit flag field on the per-entity sequence state (offset +0x2C of the state controller struct), readable/writable from a sequence via `C3 0x08` / `E5 0x08`.

| Flag  | Meaning |
|-------|---------|
| 0x001 | Sequence (re)start pending: set when a new sequence is queued; the per-frame driver clears it and runs the interpreter from the sequence start immediately |
| 0x002 | An animation was queued by the sequence (opcode &lt; 0x80 or A0); when it ends the driver re-queues it (loop) |
| 0x004 | Current animation finished (set automatically at the animation's last frame, cleared while playing). Opcode A0 only re-triggers an already-playing animation when this is set; opcode A4 sets it manually |
| 0x008 | Waiting for the animation to finish: set (together with 0x002) by opcode &lt; 0x80; the driver does not advance the sequence while it is set, and clears it when the animation completes |
| 0x040 | Sequence chain finished / entity idle-interruptible: set by A3 when no follow-up sequence is pending, cleared when a sequence is queued. Externally triggered sequences (hit reactions BF, status changes) are only accepted when 0x040 or 0x100 is set |
| 0x100 | Taking damage / hit reaction in progress (same gate as 0x040 for external triggers) |

Other bits (e.g. 0x080, written by some vanilla sequences through `E5 08`) have no identified engine use.

# Default sequence IDs

At battle start every entity plays **sequence 8** (battle entrance) and the idle fallback (`basedAnimSeq`) defaults to **1**.

When a sequence ends (`A2`) with nothing queued, **monsters** return to `basedAnimSeq`; **characters** (com_id &lt; 0x10) pick by animation status (`analyse_animation_status` at `0x509C10`), in this priority order:

| Sequence | Played when |
|----------|-------------|
| 3        | Dead |
| 2        | Sleeping, or weakened look (HP &lt; 25%, poison, curse) |
| 16 (0x10)| Running / moving |
| 19 (0x13)| Preparing attack |
| 29 (0x1D)| Defending |
| 1        | Normal standing (default) |
