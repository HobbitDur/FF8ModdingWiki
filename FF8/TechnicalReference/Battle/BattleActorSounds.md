---
layout: default
parent: Battle
title: Battle actor sound table
permalink: /technical-reference/battle/battle-actor-sounds/
---

1. TOC
{:toc}

## Battle actor sound table

The sound effects an actor makes in battle (a monster's growl, an attack impact, a character's weapon swing) are **not** stored in the monster `.dat` file. The `.dat` [Section 9](../model-sections/sounds/) and [Section 10](../model-sections/sound-sample-bank/) hold AKAO sound data that the PC engine parses but never plays.

Instead, the sounds come from a table baked into `FF8_EN.exe`, `BattleActorSoundTable`, indexed by the actor's **`com_id`** (the same enemy id stored in each [scene.out](../battle-structure-sceneout/) encounter, offset `0x38`). Each `com_id` owns up to **7 sound slots**; the battle animation picks a slot by number, and the table turns that into a global sound.

### Lookup chain

An actor sound plays through this chain:

1. The [animation-sequence VM (Section 5)](../model-sections/animation-sequences/) runs a sound opcode (`0xB5`/`0xB6` for an actor-local sound, `0xB8` for a global one). The opcode carries a **slot number** (`0`–`6`) and a flags byte.
2. `BdPlayActorSE` takes the running actor's `com_id` and the slot number and reads `BattleActorSoundTable[com_id][slot]`. That value is a **world-sound id**.
3. `PlayWorldSound` passes the world-sound id to `GetSoundID_ForWorld`, which decodes it into an **[audio archive](../../miscellaneous/audio-audiodataudiofmt/) sound id** (an index into audio.fmt).
4. `PlaySound` plays that id through DirectSound.

So the answer to "how does the game know which sound to play" is: the **actor's `com_id` selects the row**, and the **animation's slot number selects the column**. The `.dat` file only decides *when* to fire a slot, not *what* the slot sounds like.

### World-sound id encoding

The values stored in the table are "world-sound ids". `GetSoundID_ForWorld` splits each id into a **category** (`id / 10000`) and an **index** (`id % 10000`), then adds a per-category base:

| Category (`id / 10000`) | Base | Used for                                   |
|:-----------------------:|:----:|--------------------------------------------|
| 1                       | 2150 | —                                          |
| 21                      | 150  | Character (party) battle sounds            |
| 22                      | 180  | Monster battle sounds (the common case)    |
| 24                      | 370  | —                                          |
| 30                      | 710  | —                                          |
| 35                      | 980  | —                                          |
| 40                      | 1230 | Shared battle-effect sounds                |
| 41                      | 1510 | Shared battle-effect sounds                |
| 42                      | 1920 | Shared battle-effect sounds                |
| 50                      | 2784 | —                                          |
| 69                      | —    | Special case: `690000` → `2060`, otherwise `id − 688040` |
| any other               | 0    | `index` used directly                      |

Final audio id = `base[category] + index`.

**Worked example:** world-sound id `220037` → category `22`, index `37` → `180 + 37` = audio id **217** (the first slot of `com_id 0x11`).

The decoded audio id is the entry index into the [audio archive](../../miscellaneous/audio-audiodataudiofmt/) (`audio.fmt` / `audio.dat`). This is verified against the retail archive: e.g. index `217` is `com_id 0x11` (GIM52A) and indices `158`/`159` are Squall's — each an MS-ADPCM, 44100 Hz mono sound. The table below lists the **decoded audio ids** directly.

### The table (`BattleActorSoundTable`)

160 rows (`com_id` `0x00`–`0x9F`), 7 slots each. Empty cells are unused slots (value `0`). Rows with no entries are silent actors.

- **`0x00`–`0x0A`** are the playable characters — in `com_id` order: Squall, Zell, Irvine, Quistis, Rinoa, Selphie, Seifer, Edea, Laguna, Kiros, Ward. Their sounds are category-21 movement/weapon effects.
- **`0x0B`–`0x10`** are silent (unused actor slots).
- **`0x11`–`0x9F`** are monsters. For most, slots 0 and 1 are the actor's own voice pair (category 22) and any further slots are shared battle-effect sounds (category 40+) such as impacts or elemental hits.

| com_id | Slot 0 | Slot 1 | Slot 2 | Slot 3 | Slot 4 | Slot 5 | Slot 6 |
|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| 0x00 | 158 | 159 |  |  |  |  |  |
| 0x01 | 151 | 152 | 153 | 154 |  |  |  |
| 0x02 | 168 |  |  |  |  |  |  |
| 0x03 | 160 | 161 | 162 |  |  |  |  |
| 0x04 | 155 | 156 | 157 |  |  |  |  |
| 0x05 | 165 | 166 | 167 |  |  |  |  |
| 0x06 | 163 | 164 |  |  |  |  |  |
| 0x07 | 176 | 179 | 1783 |  |  |  |  |
| 0x08 | 174 | 175 |  |  |  |  |  |
| 0x09 | 169 | 172 |  |  |  |  |  |
| 0x0A | 170 | 171 | 173 |  |  |  |  |
| 0x0B |  |  |  |  |  |  |  |
| 0x0C |  |  |  |  |  |  |  |
| 0x0D |  |  |  |  |  |  |  |
| 0x0E |  |  |  |  |  |  |  |
| 0x0F |  |  |  |  |  |  |  |
| 0x10 |  |  |  |  |  |  |  |
| 0x11 | 217 | 218 | 1691 |  |  |  |  |
| 0x12 | 288 | 289 | 1395 |  |  |  |  |
| 0x13 | 211 | 212 | 1346 |  |  |  |  |
| 0x14 | 191 | 192 | 1346 | 1356 |  |  |  |
| 0x15 | 213 | 214 | 1346 | 1350 |  |  |  |
| 0x16 | 207 | 208 | 1285 | 1348 |  |  |  |
| 0x17 | 229 | 230 | 1356 |  |  |  |  |
| 0x18 | 255 | 256 |  |  |  |  |  |
| 0x19 | 185 | 186 | 1250 | 1259 | 1277 |  |  |
| 0x1A | 181 | 182 | 1257 |  |  |  |  |
| 0x1B | 253 | 254 |  |  |  |  |  |
| 0x1C | 253 | 254 |  |  |  |  |  |
| 0x1D | 193 | 194 | 1309 | 1453 |  |  |  |
| 0x1E | 187 | 188 | 1233 |  |  |  |  |
| 0x1F | 195 | 196 | 1423 |  |  |  |  |
| 0x20 | 197 | 198 | 1328 |  |  |  |  |
| 0x21 | 215 | 216 | 1346 |  |  |  |  |
| 0x22 | 199 | 200 | 1346 | 1376 |  |  |  |
| 0x23 | 267 | 268 | 1230 |  |  |  |  |
| 0x24 | 203 | 204 | 1346 | 1799 |  |  |  |
| 0x25 | 231 | 232 | 1346 | 1425 |  |  |  |
| 0x26 | 205 | 206 | 1325 |  |  |  |  |
| 0x27 | 209 | 210 | 1311 |  |  |  |  |
| 0x28 | 201 | 202 | 1294 | 1311 | 1476 |  |  |
| 0x29 | 251 | 252 | 1346 |  |  |  |  |
| 0x2A | 219 | 220 |  |  |  |  |  |
| 0x2B | 225 | 226 | 1356 | 1401 |  |  |  |
| 0x2C | 249 | 250 | 1346 | 1348 |  |  |  |
| 0x2D | 247 | 248 | 1346 |  |  |  |  |
| 0x2E | 243 | 244 | 1356 |  |  |  |  |
| 0x2F | 304 | 305 |  |  |  |  |  |
| 0x30 | 221 | 222 | 1261 | 1401 | 1407 |  |  |
| 0x31 | 233 | 234 | 356 |  |  |  |  |
| 0x32 | 306 | 307 |  |  |  |  |  |
| 0x33 | 223 | 224 | 1559 | 1561 |  |  |  |
| 0x34 | 269 | 270 | 1303 |  |  |  |  |
| 0x35 | 245 | 246 |  |  |  |  |  |
| 0x36 | 273 | 274 | 1844 | 1850 |  |  |  |
| 0x37 | 265 | 266 |  |  |  |  |  |
| 0x38 | 265 | 266 | 1409 | 1411 |  |  |  |
| 0x39 | 227 | 228 | 1394 |  |  |  |  |
| 0x3A | 263 | 264 | 1230 | 1348 |  |  |  |
| 0x3B | 271 | 272 |  |  |  |  |  |
| 0x3C | 235 | 236 | 2011 |  |  |  |  |
| 0x3D | 237 | 238 |  |  |  |  |  |
| 0x3E | 290 | 291 | 1303 | 1311 | 1500 |  |  |
| 0x3F | 308 | 309 | 1346 |  |  |  |  |
| 0x40 | 296 | 297 |  |  |  |  |  |
| 0x41 | 239 | 240 | 1532 | 1699 |  |  |  |
| 0x42 | 302 | 303 | 1679 | 1682 |  |  |  |
| 0x43 | 275 | 276 | 1366 | 1367 | 1370 |  |  |
| 0x44 | 241 | 242 | 1356 | 1682 |  |  |  |
| 0x45 | 292 | 293 | 1356 | 1393 | 1701 |  |  |
| 0x46 | 265 | 266 | 1384 |  |  |  |  |
| 0x47 | 278 | 279 |  |  |  |  |  |
| 0x48 | 282 | 283 | 1713 | 1786 |  |  |  |
| 0x49 | 310 | 311 | 1346 |  |  |  |  |
| 0x4A | 286 | 287 |  |  |  |  |  |
| 0x4B | 314 | 315 | 1356 |  |  |  |  |
| 0x4C | 358 | 360 | 361 |  |  |  |  |
| 0x4D | 277 | 1385 |  |  |  |  |  |
| 0x4E | 335 | 365 | 1532 | 1684 |  |  |  |
| 0x4F | 336 | 366 | 1684 |  |  |  |  |
| 0x50 | 1255 | 1261 |  |  |  |  |  |
| 0x51 | 332 | 1572 |  |  |  |  |  |
| 0x52 | 343 | 1682 |  |  |  |  |  |
| 0x53 | 300 | 301 | 1682 | 1703 |  |  |  |
| 0x54 | 1686 |  |  |  |  |  |  |
| 0x55 |  |  |  |  |  |  |  |
| 0x56 | 344 |  |  |  |  |  |  |
| 0x57 | 1230 |  |  |  |  |  |  |
| 0x58 | 1255 | 1261 |  |  |  |  |  |
| 0x59 | 1230 |  |  |  |  |  |  |
| 0x5A | 1255 | 1261 |  |  |  |  |  |
| 0x5B | 345 | 1346 |  |  |  |  |  |
| 0x5C | 1230 |  |  |  |  |  |  |
| 0x5D | 341 | 342 |  |  |  |  |  |
| 0x5E | 1230 |  |  |  |  |  |  |
| 0x5F | 339 | 340 | 1230 | 1723 |  |  |  |
| 0x60 | 1796 |  |  |  |  |  |  |
| 0x61 | 1796 |  |  |  |  |  |  |
| 0x62 | 334 |  |  |  |  |  |  |
| 0x63 | 324 | 325 | 1713 | 1714 |  |  |  |
| 0x64 | 280 | 281 | 1710 |  |  |  |  |
| 0x65 | 334 |  |  |  |  |  |  |
| 0x66 |  |  |  |  |  |  |  |
| 0x67 |  |  |  |  |  |  |  |
| 0x68 | 346 | 1783 | 1783 |  |  |  |  |
| 0x69 | 257 | 258 | 1230 | 1255 | 1261 | 1691 | 1693 |
| 0x6A | 352 | 1900 |  |  |  |  |  |
| 0x6B | 183 | 184 | 1348 | 1356 |  |  |  |
| 0x6C | 189 | 190 | 1245 | 1381 |  |  |  |
| 0x6D | 261 | 262 | 1356 |  |  |  |  |
| 0x6E | 312 | 313 | 1689 |  |  |  |  |
| 0x6F | 316 | 317 | 355 | 1356 | 1706 | 1708 |  |
| 0x70 | 318 | 319 | 1356 |  |  |  |  |
| 0x71 | 257 | 258 | 1230 | 1255 | 1261 | 1691 | 1693 |
| 0x72 | 257 | 258 | 1230 | 1255 | 1261 | 1691 | 1693 |
| 0x73 | 259 | 260 | 1964 |  |  |  |  |
| 0x74 | 346 |  |  |  |  |  |  |
| 0x75 | 294 | 295 |  |  |  |  |  |
| 0x76 | 294 | 295 |  |  |  |  |  |
| 0x77 | 320 | 321 | 1348 | 1691 |  |  |  |
| 0x78 |  |  |  |  |  |  |  |
| 0x79 | 322 | 323 | 1794 | 1957 | 1959 |  |  |
| 0x7A | 1792 |  |  |  |  |  |  |
| 0x7B | 1792 |  |  |  |  |  |  |
| 0x7C | 1230 |  |  |  |  |  |  |
| 0x7D | 298 | 299 |  |  |  |  |  |
| 0x7E | 326 | 327 |  |  |  |  |  |
| 0x7F | 257 | 258 | 1230 | 1255 | 1261 | 1691 | 1693 |
| 0x80 | 354 |  |  |  |  |  |  |
| 0x81 |  |  |  |  |  |  |  |
| 0x82 | 353 | 1897 |  |  |  |  |  |
| 0x83 | 348 | 349 | 1894 |  |  |  |  |
| 0x84 | 350 | 351 | 1894 |  |  |  |  |
| 0x85 | 347 | 1914 |  |  |  |  |  |
| 0x86 | 359 |  |  |  |  |  |  |
| 0x87 | 1230 | 1697 |  |  |  |  |  |
| 0x88 | 1789 |  |  |  |  |  |  |
| 0x89 | 357 | 1691 |  |  |  |  |  |
| 0x8A | 2038 |  |  |  |  |  |  |
| 0x8B |  |  |  |  |  |  |  |
| 0x8C | 362 | 363 | 2041 |  |  |  |  |
| 0x8D | 2036 |  |  |  |  |  |  |
| 0x8E | 367 | 2044 |  |  |  |  |  |
| 0x8F |  |  |  |  |  |  |  |
| 0x90 |  |  |  |  |  |  |  |
| 0x91 |  |  |  |  |  |  |  |
| 0x92 | 284 | 285 | 1532 | 1699 | 1701 | 1967 |  |
| 0x93 | 337 | 338 | 1691 | 1792 |  |  |  |
| 0x94 | 328 | 329 | 1682 | 1703 |  |  |  |
| 0x95 | 330 | 331 | 1679 | 1682 |  |  |  |
| 0x96 | 1230 |  |  |  |  |  |  |
| 0x97 | 1255 | 1261 |  |  |  |  |  |
| 0x98 | 1230 | 1697 |  |  |  |  |  |
| 0x99 | 1789 |  |  |  |  |  |  |
| 0x9A | 364 |  |  |  |  |  |  |
| 0x9B | 364 |  |  |  |  |  |  |
| 0x9C | 364 |  |  |  |  |  |  |
| 0x9D | 364 |  |  |  |  |  |  |
| 0x9E | 334 |  |  |  |  |  |  |
| 0x9F | 1230 |  |  |  |  |  |  |

### Notes

- **Bounds.** `BdPlayActorSE` only reads the table when `com_id < 0xA0` and `slot < 7`; anything outside is ignored (no sound).
- **3D variant.** `BdPlayActorSE3D` reads the same table but positions the sound in the battle scene when the 3D-sound capability flag is set; otherwise it falls back to the same stereo path as `BdPlayActorSE`.
- **Global sounds.** The `0xB8` opcode path (`BdPlaySy`) does not use this table; its operand is already a world-sound id and goes straight to `PlayWorldSound`.
- **Shared rows.** Several monster rows are identical (e.g. `0x69`/`0x71`/`0x72`/`0x7F` share the same 7 sounds), so a family of related enemies reuses one sound set.
- **Editing the sounds.** Changing an actor's battle sounds means editing the referenced entries in the [audio archive](../../miscellaneous/audio-audiodataudiofmt/) (e.g. with the Julia tool in FF8UltimateEditor). Changing *which* sound an actor points to means editing `BattleActorSoundTable` in the executable; the `.dat` sound sections have no effect on either.

### Reference (names & addresses)

FF8_EN.exe:

| Name                   | Address   | Role                                                              |
|------------------------|-----------|------------------------------------------------------------------|
| `BattleActorSoundTable` | 0xB8A418 | Actor sound table: 160 × 7 DWORD world-sound ids, indexed `[com_id][slot]` |
| `BdPlayActorSE`        | 0x5015A0  | Reads `BattleActorSoundTable[com_id][slot]`, plays it (stereo)    |
| `BdPlayActorSE3D`      | 0x501640  | Same lookup, positional (3D) playback                            |
| `BdPlaySy`             | 0x501740  | Plays a world-sound id directly (global sounds, no table)        |
| `linkedToSoundAnimSeq` | 0x505AB0  | Section-5 opcode handler that supplies the slot number and flags |
| `PlayWorldSound`       | 0x46B2A0  | World-sound id → channel/panning → `PlaySound`                   |
| `GetSoundID_ForWorld`  | 0x46B120  | Decodes a world-sound id into an audio-archive id                |
| `PlaySound`            | 0x4699A0  | DirectSound / ADPCM playback                                     |
