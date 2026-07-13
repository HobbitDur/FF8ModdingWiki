---
layout: default
title: Sound engine (SFX and music)
parent: Main
permalink: /technical-reference/main/sound-engine/
---

1. TOC
{:toc}

# Sound engine

Runtime documentation of the PC sound engine: DirectSound SFX channels and the DirectMusic/wav music pipeline. Battle-specific vestiges (AKAO sequences inside battle .dat files) are covered in the battle section. Addresses for FF8_EN.exe, image base 0x400000.

## Initialization

`pubintro_init` (engine init callback) calls `Sound_Init` (0x469640) and `Music_Init` (0x46C0B0):

* **Sound** — creates DirectSound (device GUID from registry value `SoundGUID`, HKLM Square Soft key), a 44.1 kHz 16-bit stereo primary buffer, a 3D listener, probes EAX, then `Sound_LoadAudioFmtAndDat` parses **audio.fmt** (38-byte file entries → 24-byte memory records: size, offset in audio.dat, loop mode, loop start/end, `WAVEFORMATEX*`) and opens **audio.dat**. Samples are PCM or MS-ADPCM (decoded through ACM at load time).
* **Music** — creates IDirectMusic, enumerates up to 16 ports, opens the port whose GUID is stored in registry value `MIDIGUID` (there is no "MusicDriver" value — hardware-MIDI vs software synth is simply which port GUID is stored), creates the loader (search directory = music data path) and performance with auto-download. If option bit 0x10 is set and the port is XG-capable, XG mode is enabled and the reset segment `Xgon.sgt` (id 115) is played.

## SFX channels

32 channels of 96 bytes at `dsound_instances` (0x1CD0B00): DSound buffer + optional 3D buffer, a **second buffer holding only the loop region** (how intro-then-loop samples work), sound id, and three transition blocks (volume, pan, frequency — each {active, base, target, current, step/frame}).

* Channel 0 is reserved; explicit plays select channels 1–28 via a mask; mask 0 = round-robin over channels 24–29.
* Volume 0–127 maps to dB through a table (0xB7EB10), scaled by the master SFX volume (0–100); pan 0–127 (64 = center) through its own table; pitch = buffer frequency.
* `Sfx_UpdateChannelTransitions` applies the per-frame ramps; it is wrapped together with the music ramp in `Sound_UpdateTransitions_PerFrame` (0x46BD10), which every module main loop calls once per frame.
* Field script sound opcodes go through a mask-based `Sfx_Set*_Mask` layer (transition time = 10×frames, minimum 50 ms) — the PSX "sd" API heritage.

## Music pipeline

Music requests arrive as **AKAO blobs** (PSX heritage): `Music_PlayFromAKAO` (0x46B530) checks the `AKAO` magic and takes `song_id = byte[4] − 1`, then dispatches:

* **18 ambient track ids** (3, 6, 10, 11, 30–34, 37–40, 44, 74, 87, 94, 95) play as **looping .wav streams** — RIFF parse including the `smpl` chunk for loop points, streamed into a DirectSound buffer refilled by a 75 ms `timeSetEvent` timer.
* Everything else plays as a **DirectMusic segment**: `Music_PlaySegmentById` stops the old segment, loads the shared **ff8.dls** collection once, connects it to the segment and plays. XG mode substitutes filename variants for ids 1/5/13/47.
* The id → filename table is at **0xB7F758**: 117 pointers ("000s-Lose.sgt" … "099-joriku2.sgt", "Chocoworld.sgt"; 115 = Xgon.sgt, 116 = XGdefault.sgt). The Garden Festival concert instrument segments (043a–h.sgt, field opcode CHOICEMUSIC) live in a separate table at 0xB805DC.
* Two logical music channels exist (`MUSIC_CHANNEL_MODE[2]`: 0 stopped / 1 DirectMusic / 2 wav stream) — CROSSMUSIC/DUALMUSIC use the second channel with volume ramps — but only one DirectMusic segment and one wav stream can be active at a time.
* Volume: 0–127 through a 128-entry dB table (0xB7F92C) into `SetGlobalParam(PerfMasterVolume)`, either instant or ramped per frame by `Music_UpdateVolumeRamp`. Wav streams ramp independently and are additionally scaled by the SFX master volume.

## Address table (key functions)

| Function | Address | | Function | Address |
|----------|---------|-|----------|---------|
| `Sound_Init` | 0x469640 | | `Music_Init` | 0x46C0B0 |
| `Sound_LoadAudioFmtAndDat` | 0x46D610 | | `Music_InitDirectMusic` | 0x46EB30 |
| `Sfx_PlaySound` | 0x4699A0 | | `Music_PlayFromAKAO` | 0x46B530 |
| `Sfx_LoadSoundToChannel` | 0x469C60 | | `Music_PlaySegmentById` | 0x46C2A0 |
| `Sfx_CreateLoopRegionBuffer` | 0x46AEF0 | | `Music_GetSegmentFilenameById` | 0x46C850 |
| `Sfx_SetChannelVolume/Pan/Pitch` | 0x46A480/0x46A9E0/0x46AB70 | | `Music_PlayLoopedWav` | 0x46B8E0 |
| `Sfx_GetChannelFromMask` | 0x46B0F0 | | `Music_WavStream_Play` | 0x46CBB0 |
| `Sfx_UpdateChannelTransitions` | 0x46ACA0 | | `Music_DMPerf_SetVolume` | 0x46C6F0 |
| `Sound_UpdateTransitions_PerFrame` | 0x46BD10 | | `Music_UpdateVolumeRamp` | 0x46C780 |
| `dsound_instances` (32×96 B) | 0x1CD0B00 | | `Music_StopChannelOrAll` | 0x46B800 |
| `MUSIC_ID_TO_SGT_FILENAME` (117 ptrs) | 0xB7F758 | | `Music_ChoiceMusic_Concert` | 0x46B990 |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
