---
title: Sound sample bank
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/sound-sample-bank/
nav_order: 10
author: HobbitDur
---

1. TOC
{:toc}

## Sound sample bank

This section is a single **AKAO ADPCM sample / instrument bank** — the waveform data referenced by the [Sounds](../sounds/) sequences. It can be empty.

Unlike the [sounds](../sounds/) section (which holds several small sequence blocks), this section is **exactly one** large AKAO block, typically **8–18 KB**. It begins directly with the `"AKAO"` magic — there is no per-section position table.

### AKAO bank header

| Offset | Length  | Description                                                                                 |
|--------|---------|---------------------------------------------------------------------------------------------|
| 0x00   | 4 bytes | Magic `"AKAO"`                                                                               |
| 0x04   | 2 bytes | Bank id (`301`, `302`, `303`… — increments per monster file; matches the `bank id` field of the file's category-1 [Sounds](../sounds/) blocks) |
| 0x06   | 2 bytes | `0`                                                                                          |
| 0x08   | 4 bytes | `0`                                                                                          |
| 0x0C   | 4 bytes | `0`                                                                                          |
| 0x10   | 4 bytes | `0x0006B000` — **constant in every file**. SPU-RAM destination address for the sample upload (≈ 428 KB into SPU RAM, above the reserved music/stream area) |
| 0x14   | 4 bytes | Size of the ADPCM sample body to transfer                                                    |
| 0x18   | 4 bytes | `0xD0` (208) — **constant**. Size of the header / instrument-table region that precedes the sample body |
| 0x1C   | 4 bytes | `0x10` (16) — **constant**. Instrument / region count in the header block                    |
| 0x20   | ...     | Instrument headers, then ADPCM sample data                                                   |

The field values `0x10`, `0x18`, `0x1C` are constant across all monster files. Their meanings follow the AKAO sample-bank transfer-header layout: the header describes a DMA of the ADPCM body to SPU RAM at address `0x6B000`. They are marked "inferred" because the PC executable never dereferences them (its consumer is a stub — see below).

### Section length

There is no length field inside the section for the reader to trust; the engine computes it from the section table:

```
len(this section) = offset[10] - offset[9]
```

If `offset[9] == offset[10]` the section is empty (no bank).

### How the PC engine handles this section

At battle-load time, `battle_monster_dat_loader` processes this section in its load phase:

```c
sec10 = &file[ offset[9] ];                 // this section start
sec11 = &file[ offset[10] ];                // textures section start
if (sec11 == sec10)                          // empty bank -> skip
    goto next_phase;

// find a free sound-bank slot (0..2) in the 3-bit allocation mask
slot = first_clear_bit(SoundBankSlotAllocMask);   // max 3 concurrent banks
if (slot >= 3) goto next_phase;
entity->command_queue.sound_bank_slot = slot;
SoundBankSlotAllocMask |= (1 << slot);

BankUpload_Stub();                           // no-op on PC
```

The final call — the sample-bank-to-SPU DMA slot — is `return_0`, a 2-instruction null stub (`xor eax, eax` / `retn`). Its effects on the PC release:

- This section is **not copied into battle work RAM** (the model-blob copy stops at `offset[9]`) and its bytes are **not uploaded** to the (software) SPU.
- Only bookkeeping happens: a slot bit in `SoundBankSlotAllocMask` is reserved on load and cleared on entity unload; the mask is reset when a battle location is set up. Nothing reads a slot back to fetch sample data.
- The header fields at `0x10`/`0x14`/`0x18`/`0x1C` are consequently never read by the PC executable — their interpretation above comes from the AKAO bank-header layout.

The section is therefore inert on the PC release: retained in the files and slot-allocated, but its sample upload is a no-op. Monster SFX on PC are played through the global DirectSound engine keyed by a hardcoded executable table — see [Sounds → The SFX path](../sounds/#the-sfx-path).

### Presence statistics (199 eleven-section c0m files)

| Combination                         | Count |
|-------------------------------------|-------|
| Both section 9 and 10 present       | 113   |
| Section 9 only (no embedded bank)   | 24    |
| Section 10 only                     | 0     |
| Neither (silent / non-combat entry) | 62    |

A bank (section 10) never appears without sequences (section 9). The 24 "section 9 only" monsters reference a shared/global sample bank rather than an embedded one. `c0m127.dat` is the special case with only 2 sections (7 and 8) and therefore no sound sections.

### Modding implications

- Editing or replacing this section has **no audible effect** on the PC release (its upload is stubbed).
- Keep the section structurally consistent with the header table: the loader relies on `offset[10] - offset[9]` to detect an empty bank and to place `offset[10]` (the textures section) correctly.
- The bank id at `0x04` is informational on the PC release.

### Reference (names & addresses)

FF8_EN.exe:

| Name                     | Address    | Role                                                             |
|--------------------------|------------|-----------------------------------------------------------------|
| `battle_monster_dat_loader` | 0x507120 | Parses the monster `.dat`; reserves the bank slot     |
| `return_0`               | 0x46C040   | Null stub (`xor eax,eax; retn`) at the bank upload site    |
| `BS_SetLocation1`        | 0x508260   | Resets the sound-bank slot mask at battle-location setup         |
| `SoundBankSlotAllocMask`   | 0x1D98B38  | 3-bit allocation mask (≤ 3 concurrent monster banks)             |
| Bank SPU dest addr       | 0x0006B000 | Constant `0x10` header field value (SPU-RAM upload address)      |
