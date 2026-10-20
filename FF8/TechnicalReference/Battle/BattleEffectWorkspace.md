---
title: Effect sources and native camera parameters
layout: default
parent: Battle
permalink: /technical-reference/battle/effect-sources/
---

# Effect sources and native camera parameters

An effect ID identifies native dispatch, not one storage format. Choreography, camera,
geometry, skeletal animation, textures and sound can have different sources within the same
effect. FF8UltimateEditor's **Fujin** now groups these components around one effect selection;
its MAG/cinematic implementation is provided by the former Laguna components.

## Resource ownership and evidence

| Case | Verified example | Consequence |
|---|---|---|
| Native initializer starts a MAG interpreter | Disease Breath (231), Ifrit (201) | Native dispatch and file scripts coexist |
| Native timeline loads external models | Shiva (185): `mag184_e.dat` | File storage does not imply script-driven choreography |
| Embedded model uses external textures | Carbuncle (278): model `0x10B6F94`, second TIM in `mag277.tim` | A component editor must support mixed sources |
| Existing battle actors reused | Griever (69), battle instances in slots 1/2 | No dedicated `mag068` summon model; Griever is `c0m122.dat` |
| Separate copies contain identical data | Angelo and Boko effect variants | Editing one address must not silently edit siblings |
| Several effect IDs share a resource | Gilgamesh weapon effects 327–330: `mag326_g.dat` | Filename arithmetic alone cannot establish ownership |

Fujin distinguishes loader references, verified runtime resource bindings and filename-family
hints. Partial string extraction does not enumerate all streamed files. A missing `magNNN`
group or empty loader callback does not establish that an effect is unused.

Camera sources are similarly independent: a static executable track, a track embedded in
MAG data, cinematic camera-bone commands, native coordinate writes, or the action's opening
camera. [Battle Cameras](BattleCameras.md) describes the handoff. Disease Breath's normal
track begins at `MAG230_B.00 + 0x870`; a cinematic opcode `0x39`, modifier 8, selects it.
Presence of an unused camera handler alone does not prove a script invokes it.

## Audited executable resource spans

The editor's `effect_resources.json` records 24 standard creature model containers, 26 complete
TIM images and six procedural-camera immediate operands. Addresses are for the audited
English 2013 Steam executable (SHA-256
`064d466b5fe2ba901fd44abf19f37c0fd6a2db40aabd95c9e5959195b6589570`).
In this image, the listed IDA VA maps to file offset `VA - 0x400000`.
Each resource has its own length and fingerprint; each camera operand also has an instruction
guard. Other executable languages require separately verified native resource addresses.
The pre-existing static-track editor has independent per-language camera addresses.

Model sources and IDA names are listed in [Summon Creature Models](SummonCreatureModels.md).
Consecutive TIM packs must be walked by their complete block lengths: the first image's end
does not necessarily mean the file's end. Carbuncle's body TIM begins at file offset 172064
inside `mag277.tim`.

## Carbuncle's procedural camera

Decompilation of `GF_278Carbuncle_CreatureTask` (`0x681630`) shows direct writes to camera globals
and calls to `MAG_278_CameraSwingAboutLookAt` (`0x683D10`). These are not a camera VM track.
The following operand locations were also checked against the x86 instructions in the
extracted executable. All numbers below are signed.

| Meaning | Tick window | Operand VA | Width | Original |
|---|---|---|---|---|
| Initial Y offset from floor | 1 | `0x681D35` | 32 bits | 3000 |
| Initial camera Z | 1 | `0x681D5E` | 16 bits | -4000 |
| Opening orbit radius | 1–36 | `0x681D93` | 32 bits | 4010 |
| Middle orbit radius | 86–109 | `0x681DE2` | 32 bits | 4000 |
| Middle orbit angle step | 86–109 | `0x681DE7` | 8 bits | -32 |
| Late orbit radius | from 247 while the task runs | `0x681F67` | 32 bits | 4150 |

The 8-bit immediate is the sign-extended operand of `push imm8` (`6A E0`), so widening the
stored value would overwrite the next instruction. The bindings own only operand bytes;
the surrounding opcodes and destination addresses are not part of the editable span.
Other camera writes and timing/branch logic in this function remain native research.

## Editing and validation boundaries

Fujin shares one byte image per imported file/native resource across component views.
MAG edits preserve section sizes and write back to imported paths. Executable changes export
as a cumulative Hext patch; resized static tracks export as FFNx `.cam` files. Native code
is never recompiled from its pseudocode. The selected camera-track preview does not reproduce
additional procedural writes, and whole-effect scene playback remains limited to seven
verified cinematic GFs. Unknown sections retain bounded byte editing rather than invented
semantics. See the [MAG format census](FileFormat_magfiles.md) for file coverage and VM profiles.
