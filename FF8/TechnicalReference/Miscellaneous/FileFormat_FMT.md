---
layout: default
parent: Miscellaneous
title: Audio (audio.dat/audio.fmt)
permalink: /technical-reference/miscellaneous/audio-audiodataudiofmt/
---

1. TOC
{:toc}

Final Fantasy VIII's sound effects live in two files under `Data/Sound/`. **audio.dat** holds the actual waveforms (MS-ADPCM, 4-bit), and **audio.fmt** is the locator/format table describing each sound's position and format inside the dat.

## audio.fmt structure

All values little-endian.

| Offset | Size    | Description                                              |
|--------|---------|----------------------------------------------------------|
| 0x00   | 2 bytes | `soundCount`                                             |
| 0x02   | varies  | `soundCount + 1` sound entries (see below)               |

The number of entries is `soundCount + 1`. **Entry 0 is a blank placeholder** (a 38-byte all-zero entry), so the first real sound is entry 1 at offset `0x28`. Reading `soundCount` as a 4-byte value yields the same number because the high two bytes fall inside that zero entry.

Each entry is variable-length: **70 bytes** for an ADPCM sound (`cbSize` = 32) or **38 bytes** for a blank/PCM entry (`cbSize` = 0). Fields:

| Offset | Size     | Description                                                                                  |
|--------|----------|----------------------------------------------------------------------------------------------|
| 0x00   | 4 bytes  | `dataLength` — size of the waveform in audio.dat                                             |
| 0x04   | 4 bytes  | `dataOffset` — offset of the waveform in audio.dat                                           |
| 0x08   | 1 byte   | `bufferFlags` — DirectSound buffer flag; **1 = looping**, 0 = one-shot                       |
| 0x09   | 3 bytes  | Padding (0)                                                                                   |
| 0x0C   | 4 bytes  | `bufferReadCursor` (DirectSound buffer state, normally 0)                                     |
| 0x10   | 4 bytes  | `bufferWriteCursor` (DirectSound buffer state, normally 0)                                    |
| 0x14   | 18 bytes | Microsoft `WAVEFORMATEX` (`wFormatTag`, `nChannels`, `nSamplesPerSec`, `nAvgBytesPerSec`, `nBlockAlign`, `wBitsPerSample`, `cbSize`) |
| 0x26   | `cbSize` bytes | Extra format bytes. For MS-ADPCM (`wFormatTag` = 2, `cbSize` = 32): samples-per-block (2), coefficient count (2, always 7), then the 28-byte standard ADPCM coefficient set |

The first 20 bytes (`0x00`–`0x14`) are the game's own locator/buffer record; the rest is a standard `WAVEFORMATEX` (+ ADPCM tail) that can be copied verbatim into a WAV `fmt ` chunk.

## audio.dat structure

`audio.dat` is a raw concatenation of the waveform bodies. Sound *i* occupies `[dataOffset, dataOffset + dataLength)`. There is no per-sound header in the dat — the engine locates every sound purely from audio.fmt's offset/length, so on a rebuild the waveforms may be packed in any order/alignment as long as audio.fmt matches.

## Retail archive facts

The shipped `audio.fmt` holds **2791 entries** (`soundCount` = 2790), of which **1544 are valid sounds** (the rest are blank placeholders). Every valid sound is **MS-ADPCM, 44100 Hz, mono**. The valid entries' `dataOffset + dataLength` values tile audio.dat exactly up to its full size (~105 MB), confirming the layout.

Sound entries are addressed by their **index** (0-based) in audio.fmt. That index is the "sound id" used elsewhere in the engine — e.g. the [battle actor sound table](../../battle/battle-actor-sounds/) stores, per battle actor, the indices of the sounds it plays.

## Exporting a sound to WAV

A standalone WAV is built by wrapping the entry's format and its audio.dat bytes:

```
"RIFF" + u32(dataLength + 38 + cbSize) + "WAVE"
"fmt " + u32(18 + cbSize) + WAVEFORMATEX(18) + extra(cbSize)
"data" + u32(dataLength) + <dataLength bytes from audio.dat>
```

Both PCM and MS-ADPCM WAVs round-trip this way. (Note: FF8SND/ff8-sound-remixed use `dataLength + 36` for the RIFF size, which is two bytes short because they still emit the full 18-byte `WAVEFORMATEX`; `+ 38` is the correct size for strict WAV parsers.)

## Editing

The **Julia** sound editor in FF8UltimateEditor reads audio.fmt/audio.dat, plays and exports sounds to WAV, replaces a sound from a WAV (PCM or MS-ADPCM), and rebuilds both files (repacking audio.dat and rewriting audio.fmt offsets). It also shows which battle actor uses each sound via the [battle actor sound table](../../battle/battle-actor-sounds/).

## Reference (names & addresses)

FF8_EN.exe:

| Name                  | Address  | Role                                                        |
|-----------------------|----------|-------------------------------------------------------------|
| `GetSoundID_ForWorld` | 0x46B120 | Maps a world-sound id to an audio.fmt index                 |
| `PlaySound`           | 0x4699A0 | Plays an audio.fmt entry through DirectSound                |
