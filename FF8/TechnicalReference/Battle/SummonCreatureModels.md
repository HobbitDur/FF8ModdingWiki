---
layout: default
parent: Battle
title: Summon Creature Models
permalink: /technical-reference/battle/summon-creature-models/
---

Timeline-family summon and effect creatures (see [GF Summon Runtime](../gf-summon-runtime/)) are drawn from **standard 4-section battle-model containers** — the exact same layout as sections 1–3 of a `c0mXXX.dat` monster: `[nb_sections=4][offsets][file_size]` followed by skeleton, geometry, animation and a (usually empty) trailer section. They animate through `Battle_ReadAnimation`, the same keyframe machinery as monsters and characters. This page is the census of where every such creature model and its texture live.

The shared-cinematic GFs (Ifrit, Bahamut, Cerberus, Alexander, Brothers, Eden, Leviathan) are **not** covered here: their `MAGxxx_B.00/.01` packs use the custom opcode-VM format with no keyframe animation data (see the runtime page).

1. TOC
{:toc}

## Two storage locations

- **In magic.fs group files.** The container ships as one file of the effect's mag group (file number = `effect_id − 1`). Sibling files of the group are raw TIM textures the summon uploads to VRAM.
- **Embedded in FF8_EN.exe `.data`.** The container (and often the body TIM) is baked into the executable. The effect code passes its address to one of two shared binders (`Effect_BindModelContainerSections` / `Effect_BindModelContainerSetAnim`), which resolve the four section pointers, then hand the model to `Battle_ReadAnimation`.

A third helper, `Battle_QueueTIMUpload_GetEOF`, uploads a TIM (from a loaded file buffer or an embedded address) to the VRAM coordinates stored in the TIM's own header.

## File-based creature models

| Creature | Effect | Model file | Bones | Animations | Textures |
|---|---|---|---|---|---|
| Shiva | 185 | `mag184_e.dat` | 69 | 1 / 86 / 6 frames | `mag184_d.dat` (body atlas, tpage 13), `mag184_h.dat` |
| Quezacotl | 116 | `mag115_h.07` | 47 | 8 / 122 / 24 | `mag115_h.*` TIMs |
| Siren | 95 | `mag094_b.2e0` | 63 | 1 / 58 / 66 | `mag094_b.*` TIMs |
| Pandemona | 291 | `mag290_h.03` | 55 | 217 | `mag290_h.*` TIMs |
| Doomtrain | 191 | `mag190_b.dat` | 14 | 30 / 120 | `mag190_a.dat`, `mag190_c.dat` |
| Diablos | 325 | `mag324_h.02` | 69 | 7 anims | `mag324_h.01`/`.t00` |
| Odin | 187 | `mag186_b.dat` | 60 | 7 anims | `mag186_a.dat`, `mag186_d.dat` |
| Odin (Zantetsuken Reverse) | 326 | `mag325_b.dat` | 60 | 6 anims | `mag325_a.dat`, `mag325_d.dat`, `mag325_f.dat` |
| Gilgamesh | 327–330 | `mag326_g.dat` | 69 | 50 | `mag326_a.dat`, `mag326_c.dat`, `mag326_d.dat` |
| Gilgamesh (second copy, richer anim set) | 218 | `mag217_b.dat` | 69 | 6 anims | `mag217_a.dat`, `mag217_c.dat`, `mag217_d.dat` |
| Small chocobo (identity unverified) | ~100 | `mag099_b.4e0` | 17 | 1 / 28 / 1 | `mag099_b.*` TIMs |

`mag324_h.02` has a quirk: its `file_size` header field equals the section-4 offset, and 11,704 extra bytes (a nested container) follow the declared end. Sections 1–3 parse normally.

## EXE-embedded creature models

Addresses are IDA virtual addresses (the IDB maps the image without the 0x400000 base). File offset in `FF8_EN.exe` = `0x76D000 + (address − 0xB6D000)`.

| Creature | Effect(s) | Model (IDA name) | Bones | Animations | Body TIM (IDA name) |
|---|---|---|---|---|---|
| Carbuncle | 278 | `GF278_Carbuncle_ModelContainer` | 30 | 76 / 2 / 31 | 2nd TIM inside `magic/mag277.tim` (offset 172064) |
| Phoenix | 140 | `MAG140_Phoenix_ModelContainer` | 59 | 138 | inside `magic/mag139.tim` |
| Mog | 96 (Moogle Dance = MiniMog command) | `MAG096_Mog_ModelContainer` | 30 | 77 (dance) / 12 / 36 | inside `magic/mag095.tim` |
| Moomba | 338 (Friendship) | `MAG338_Moomba_ModelContainer` | 28 | 4 / 49 / 5 / 4 | `MAG338_Moomba_BodyTIM` |
| Boko | 97 / 98 / 99 / 100 | `MAG097..100_Boko_ModelContainer` (4 copies) | 34 | 20 / 1 / 28 / 2 / 35 / 4 | `MAG097..100_Boko_BodyTIM` (4 copies) |
| Angelo | 86 / 87 / 88 / 89 / 91 / 92 / 93 / 94 | `MAG086..094_Angelo_ModelContainer` (8 copies) | 34 | varies per effect | `MAG086..094_Angelo_BodyTIM` (8 copies) |
| Death reaper | 8 / 14 / 74 / 345 | `MAG008/014/074/345_Reaper_ModelContainer` (4 copies) | 28 | varies | body + wings TIM pairs per effect |
| Tonberry | 90 | `MAG090_Tonberry_ModelContainer` | 26 | 99 / 20 / 44 / 1 | with the Chef's Knife effect data |
| Cactuar | 199 | `MAG199_Cactuar_ModelContainer` | 11 | 1 / 6 / 1 / 3 / 2 | `MAG199_Cactuar_BodyTIM` |
| Cherub | 83 (Absorbed Into Time) | `MAG083_Cherub_ModelContainer` | 27 | 20 / 35 / 21 | `MAG083_Cherub_BodyTIM` |
| Angel wings (prop) | 84 (Angel Wing) | `MAG084_AngelWings_ModelContainer` | 22 | 60 / 103 | `MAG084_AngelWings_TIM` |

Every per-effect copy is byte-identical to its siblings — each effect keeps its own self-contained data blob (model, body TIM, spawn helper), so Wishing Star, the four Angelo counters and the four chocobo spells each embed the same dog / bird again.

Notable identifications settled by this census:

- **Effect 96 "Moogle Dance" is the MiniMog command effect** — its creature is Mog, with the 77-frame dance as the main animation.
- **Wishing Star (89) is Angelo's move**, not Boko's: its creature model and fur TIM are the Angelo set.
- **Effect 218 (unnamed) owns the mag217 group**, whose `mag217_b.dat` is a **second Gilgamesh model** — identical skeleton and geometry to `mag326_g.dat` but with 6 animations instead of 1 (verified in the textured viewer).
- **Griever's summon effect (69) carries no model at all.** Its texture-load callback `MAG_069_GRIEVER_SUMMON_FL` (0x5755F0) is empty, and `GF_069Griever_SetupSummon` renders whichever battle-model instances already occupy `stru_1D9898C[1]` / `[2]`. The summon only ever plays in the final battle, where those slots hold Griever's own boss model — so it reuses that, no separate asset. Griever's model **is a normal monster battle file**: `c0m122.dat`, named `{Griever}`, 70 bones, 22 animations — already a complete `.dat`, no conversion needed. This is why the `mag068` group the id rule predicts is absent.

## Boss models that double as summon creatures

Some GFs are also fought as bosses, so their model already ships as a `c0mXXX.dat` monster file — a self-contained battle model with full stats/AI/animations that needs no conversion:

| GF / creature | Boss file | Bones | Note |
|---|---|---|---|
| Griever | `c0m122.dat` `{Griever}` | 70 | The only source of the Griever model — summon reuses it |
| Diablos | `c0m066.dat` `Diablos` | 69 | Also has the `mag324_h.02` summon model |
| Odin | `c0m070.dat` `Odin` | 60 | Also has the `mag186_b.dat` summon model |

## Texture conventions

Creature geometry stores PSX texture ids: `tex_id_1` is a CLUT id (`vram_x/16 + vram_y*64`), `tex_id_2` a texture-page id. Embedded creatures consistently use **texture page 13** (VRAM x 832, y 256) with CLUT rows at **(320,224)** and (320,225); wings/extras use page 12 (768,256) with CLUT (320,226). The `magic/MagXXX.tim` pack files load through `IO_GetFile_MAGIC` (per-effect `*_FL` texture-load callbacks) and are uploaded to the VRAM coordinates in their TIM headers; some packs concatenate several TIMs (e.g. `mag277.tim` = 640×256 effect atlas + the 128×256 Carbuncle body atlas).

## Converting a creature to a battle monster

Because the containers are the standard battle-model format, a creature converts into a playable `c0mXXX`-style `.dat`: place its sections 1–3 into an 11-section monster container, rebuild section 11 TIMs from the source textures at the monster VRAM convention (image (640,0)/(640,128)…, CLUT rows (0,224+i)) while remapping every face's tex ids, then fill sections 5/6/9 with the battle-ready shape (idle at animation 0, all 13 sequence slots, camera and non-empty AKAO from donor monsters, every section offset 4-byte aligned). The `GFtoDat/gf_to_dat.py` tool in FF8UltimateEditor implements this end to end; converted dats exist for Shiva, Quezacotl, Siren, Pandemona, Doomtrain, Odin, Gilgamesh, Griever, Carbuncle, Phoenix, Moomba, MiniMog and Boko.

## Function and data addresses

| Name | Address | Description |
|---|---|---|
| `Effect_BindModelContainerSections` | 0x6EC060 | Resolves a 4-section container's absolute section pointers into a creature task |
| `Effect_BindModelContainerSetAnim` | 0x8DD0F0 | Same, plus initial animation id and scale 4096 |
| `Battle_QueueTIMUpload_GetEOF` | 0x505E30 | Queues a TIM upload to the VRAM coords in its header, returns end pointer |
| `au_re_Battle_ReadAnimation_6` | 0x6574D0 | Standard keyframe animation reader used by all these creatures |
| `GF278_Carbuncle_ModelContainer` | 0x10B6F94 | 24,324 B |
| `MAG140_Phoenix_ModelContainer` | 0x11B537C | 71,896 B |
| `MAG338_Moomba_ModelContainer` | 0x136BB30 | 19,920 B |
| `MAG089_Angelo_ModelContainer` | 0x14913FC | Wishing Star copy; others at 0x153407C (94), 0x1538B38 (93), 0x153D59C (92), 0x1543880 (91), 0x154F91C (88), 0x1565EF4 (86), 0x155B1E4 (87) |
| `MAG096_Mog_ModelContainer` | 0x152BC04 | 28,768 B |
| `MAG345_Reaper_ModelContainer` | 0x1525754 | others at 0x158233C (74), 0x162C95C (14), 0x1636CE8 (8) |
| `MAG090_Tonberry_ModelContainer` | 0x1547514 | 29,692 B |
| `MAG083_Cherub_ModelContainer` | 0x15786D4 | 10,252 B |
| `MAG084_AngelWings_ModelContainer` | 0x1572BB0 | 12,848 B |
| `MAG100_Boko_ModelContainer` | 0x1656DE4 | others at 0x1665B08 (99), 0x167482C (98), 0x168354C (97) |
| `MAG199_Cactuar_ModelContainer` | 0xE94918 | 8,680 B |
| `MAG100_Boko_BodyTIM` | 0x165BCCC | others at 0x16704DC (99), 0x1679714 (98), 0x1688434 (97) |
| `MAG338_Moomba_BodyTIM` | 0x1376698 | effect atlases at 0x137A8B8, 0x139B8D8 |
| `MAG345_Reaper_BodyTIM` / `_WingsTIM` | 0x164A678 / 0x1652A98 | per-effect pairs: 0x1778F3C/0x178135C (74), 0x1808FB0/0x18113D0 (14), 0x181CFAC/0x18253CC (8) |
| `MAG089_Angelo_BodyTIM` | 0x14AF700 | others at 0x16ADE90 (94), 0x16B8990 (93), 0x16C12C8 (92), 0x16CF8B0 (91), 0x16F3000 (88), 0x16FDF78 (87), 0x170CDCC (86) |
| `MAG084_AngelWings_TIM` | 0x17243F8 | |
| `MAG083_Cherub_BodyTIM` | 0x1738C08 | |
| `MAG199_Cactuar_BodyTIM` | 0xE96B00 | |
| `MAG278_CARBUNCLE_RUBY_LIGHT_FL` | 0x680C60 | Texture loader: `IO_GetFile_MAGIC("mag277.tim")` |
| `MAG_096_SpawnMogCreature` | 0x733E90 | Analogous `MAG_xxx_Spawn*Creature` / `MAG_xxx_Upload*TIM` helpers exist per effect (see IDB) |
| `GF_291Pandemona_TimelineTask` | 0x6ED900 | Pandemona timeline driver (formerly `SomeTimFileLoadAndCameraWork`) |
