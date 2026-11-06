---
layout: default
parent: Miscellaneous
title: Variables
permalink: /technical-reference/miscellaneous/variables/
---

By Shard.

Game variables can be accessed using the PSHM family of script functions, and can be written to by using the POPM family of functions. Which one you use depends
on the size of the variable. The variables are all stored in save files, with the save block starting at address 0xD10 on uncompressed PC saves. The parameter
to access a variable in the game scripts is basically the offset from this point in the variable block. For example, getting main story progress (word 256,
which is word 0x100 in hex) just gets the two bytes starting at address 0xD10 + 0x100 = 0xE10. The varmap is continuous in memory while the game is running as
well. In the en-US version of the original and SE releases (and likely most other versions), the varblock begins at the address given for `VARMAP_START` below. You can use
this [Cheat Engine Table](https://www.mediafire.com/?ucolf65ewq1yoty) to track them as you play.

Items in grey are unused by field scripts (some of them may be used in battle scripts).

> **IDA verification (FF8_EN.exe).** The variable block is the global `VARMAP_START` (typed as the packed struct `SavemapVariables`). The
> `SCRIPT_PSHM_*` / `SCRIPT_POPM_*` opcode handlers read/write `*(&VARMAP_START + var_number)`, which confirms that **the "Var Number" in this table is exactly the
> byte offset into the block** — variable N lives at offset N. Rows annotated with a function name / address below have been verified against engine code; most of
> the remaining entries are used only by field or battle scripts and are not touched by the EXE, so they cannot be verified from the binary.
>
> **Multi-use variables** are shown in one of two ways: variables reused for *different things at different points in the game* carry a numbered footnote (e.g. 341,
> 728); variables reused for the *same role across different maps* get one row per context (e.g. 1024).

> **Studied row by row.** Rows starting *Likely* rest on the dialogue and actions around the variable without being conclusive; rows starting *Unclear* only say where it is used. Everything else is shown by the dialogue or by the engine code. The bytes are read by the 882 field scripts and by `FF8_EN.exe` through `VAR_MAP_ADDRESS`.
>
> **Maps named `test*` are not all debug rooms.** `testbl1`, `testbl2`, `testbl3`, `testbl6` and `testbl9` are real: the game jumps to them, with `MAPJUMP0` for most (`testbl9` is the "Release which seal?" screen, `testbl6` handles a lost fight or Odin's time running out). A value only set in the other `test*` maps isn't set in normal play.

| Var type    | Var Number  | Description                                                                                                                                                                                                                                                                                                                |
|-------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Byte        | 0-3         | unused in fields (always "FF-8")                                                                                                                                                                                                                                                                                           |
| Long        | 4           | Steps (used to generate random encounters)                                                                                                                                                                                                                                                                                 |
| Long        | 8           | Payslip                                                                                                                                                                                                                                                                                                                    |
| Long        | 12          | Move-HP step counter: grows with the steps walked on the field and the world map. At 8 it resets and the party heals. |
| Signed Word | 16          | SeeD rank points. The SeeD rank shown in the menu = `clamp(points, 100, 3100) / 100` (rank 1–31), computed by `GetSeeDRankFromPoints`.                                                                                                                                                                            |
| Word        | 18          | Total kills of the party at the last SeeD payday. The new SeeD points are the old ones plus the kills since then, minus 10. |
| Long        | 20          | Battles won. (Fun fact: this affects the basketball shot in Trabia.)                                                                                                                                                                                                                                                       |
| Word        | 24          | Battles lost: copy of the save's counter, which goes up when a battle ends in defeat or runs out of time. The copy is made on every field start. Nothing reads the copy; the game adds the save's counter to battles won and escaped for a total. |
| Word        | 26          | Battles escaped.                                                                                                                                                                                                                                                                                                           |
| Word        | 28          | Enemies killed by Squall                                                                                                                                                                                                                                                                                                   |
| Word        | 30          | Enemies killed by Zell                                                                                                                                                                                                                                                                                                     |
| Word        | 32          | Enemies killed by Irvine                                                                                                                                                                                                                                                                                                   |
| Word        | 34          | Enemies killed by Quistis                                                                                                                                                                                                                                                                                                  |
| Word        | 36          | Enemies killed by Rinoa                                                                                                                                                                                                                                                                                                    |
| Word        | 38          | Enemies killed by Selphie                                                                                                                                                                                                                                                                                                  |
| Word        | 40          | Enemies killed by Seifer                                                                                                                                                                                                                                                                                                   |
| Word        | 42          | Enemies killed by Edea                                                                                                                                                                                                                                                                                                     |
| Word        | 44          | Squall death count                                                                                                                                                                                                                                                                                                         |
| Word        | 46          | Zell death count                                                                                                                                                                                                                                                                                                           |
| Word        | 48          | Irvine death count                                                                                                                                                                                                                                                                                                         |
| Word        | 50          | Quistis death count                                                                                                                                                                                                                                                                                                        |
| Word        | 52          | Rinoa death count                                                                                                                                                                                                                                                                                                          |
| Word        | 54          | Selphie death count                                                                                                                                                                                                                                                                                                        |
| Word        | 56          | Seifer death count                                                                                                                                                                                                                                                                                                         |
| Word        | 58          | Edea death count                                                                                                                                                                                                                                                                                                           |
| Byte        | 60-67       | unused in fields                                                                                                                                                                                                                                                                                                           |
| Long        | 68          | Enemies killed                                                                                                                                                                                                                                                                                                             |
| Long        | 72          | Amount of Gil the party currently has                                                                                                                                                                                                                                                                                      |
| Long        | 76          | Amount of Gil Laguna's party has                                                                                                                                                                                                                                                                                           |
| Long        | 80          | Counts the number of frames since the current movie started playing.                                                                                                                                                                                                                                                       |
| Word        | 84          | Last area visited.                                                                                                                                                                                                                                                                                                         |
| Signed Byte | 86          | The vehicle the party was on when it last left the world map, as the world map's vehicle code. The world map sets it on leaving and it is copied on every field start. Field scripts read it to show the arrival car and let the Missile Base guards react to it. Values: 0 = On foot (0-9 and 128 are all on foot), 16 = Train (16-22), 32 = Car; Missile Base guards let it pass, 33 = Bike, 34 = Balamb rental: sky blue van, 35 = Balamb rental: classic car, 38 = Deling City rental car, 40 = Esthar car, 48 = Balamb Garden (mobile), 49 = Chocobo, 50 = Ragnarok, 64 = Boat (64-66), 128 = On foot. |
| Signed Byte | 87          | Where the engine was just before this field started. Copied on every field start. Scripts load their own field music only when it is 0 or 10, since other arrivals keep the music already playing. Values: 0 = New game or a save just loaded, 1 = Another field, 2 = The world map, 3 = A battle or card game, 6 = A menu, 10 = A menu whose result asks for a reload. |
| Signed Byte | 88          | 1 when the party has Siren's Move-Find. Refreshed from the abilities on each field entry; save points and draw points read it to show themselves when hidden. Values: 0 = No Move-Find, 1 = Has Move-Find. |
| Byte        | 89-99       | unused in fields |
| Word        | 100         | Unused: only the opening logo script clears it, and nothing reads it. |
| Byte        | 102-103     | unused in fields |
| Long        | 104         | Engine switches. 8: no SeeD salary (SALARYOFF). 16: salary not shown (SALARYDISPOFF). 64: on-screen timer shown. 1024: random battles were on before a music load. |
| Signed Long | 108         | Handle of the music playing. -1 means there is no field music to carry over, so the music stops after a battle. |
| Signed Long | 112         | Handle of the second music channel, the one DUALMUSIC fills, -1 for none. MUSICLOAD only starts loading a track while it is -1. |
| Byte        | 116-147     | Draw points in field                                                                                                                                                                                                                                                                                                       |
| Byte        | 148-179     | Draw points in worldmap                                                                                                                                                                                                                                                                                                    |
| Word        | 180         | Draw point refill counter: grows with steps. At 10240 it resets and each used draw point may refill. |
| Word        | 182         | Flags of the BATTLEMODE opcode for this field. +2 no victory fanfare, the music keeps playing. +4 the countdown carries into battle; DISPTIMER and KILLTIMER switch it. +8 no EXP or items (no vanilla script uses it). +16 the battle uses the music already playing. +128 set in Dollet, Timber and Fisherman's Horizon, no game code tests it. +256 the timer reaching 0 doesn't end the game. |
| Signed Word | 184         | Frames the SeeD salary message stays on screen after a payday. It counts down; 0 or less means no message, and most saves hold -1. A movie or a card game closes the message at once. |
| Signed Word | 186         | SeeD points before the last payday, used to tell whether the rank changed. |
| Byte        | 188         | Field party, first member: character id, 255 for nobody. SETPARTY and SWAP change it. |
| Byte        | 189         | Field party, second member: character id, 255 for nobody. |
| Byte        | 190         | Field party, third member: character id, 255 for nobody. |
| Byte        | 191         | Second copy of the field party, first member. |
| Byte        | 192         | Second copy of the field party, second member. |
| Byte        | 193         | Second copy of the field party, third member. |
| Byte        | 194         | Field entity walking as the first party member, 255 for none. |
| Byte        | 195         | Field entity walking as the second party member, 255 for none. |
| Byte        | 196         | Field entity walking as the third party member, 255 for none. |
| Byte        | 197         | Volume of music channel 0, set by MUSICVOL. 127 is full. |
| Byte        | 198         | Volume of music channel 1, set by MUSICVOL. 127 is full. |
| Signed Byte | 199         | Track playing, -1 for none. MUSICCHANGE copies it from the track loaded. The world map sets it to its own: 41, 24, 81, 35, 59 or 89 depending on the vehicle. |
| Signed Byte | 200         | Second track of DUALMUSIC, -1 for none. |
| Byte        | 201         | Which of the two music buffers is in use, 0 or 1. Battles and the world map flip it. |
| Signed Byte | 202         | Last sound effect set loaded by EFFECTLOAD, -1 for none. Reloaded when a save is loaded. |
| Byte        | 203         | Battle music chosen by SETBATTLEMUSIC. |
| Byte        | 204         | Unused in fields. This region holds engine-only display/timer state rather than script variables: on-screen timer visibility (182) and X/Y position (205/206), a battle-disable flag (207), a "can save here" flag (209), and a battle-music A/B toggle (~201/203, toggled by `Battle_KeepMusicAfterBattle`). |
| Byte        | 205         | Horizontal position of the on-screen timer. |
| Byte        | 206         | Vertical position of the on-screen timer. |
| Byte        | 207         | 1 when random battles are off, from BATTLEOFF. Music opcodes also set it for the time a track loads. Values: 0 = Random battles on, 1 = Random battles off. |
| Byte        | 208         | Unused in fields. This region holds engine-only display/timer state rather than script variables: on-screen timer visibility (182) and X/Y position (205/206), a battle-disable flag (207), a "can save here" flag (209), and a battle-music A/B toggle (~201/203, toggled by `Battle_KeepMusicAfterBattle`). |
| Byte        | 209         | Field switches kept by the engine. Bits: +1 Can save here, +2 PHS party switch enabled. |
| Byte        | 210         | Message window channels with a question open, one bit per channel. |
| Byte        | 211         | Message window channels with any text window open, one bit per channel. |
| Byte        | 212         | Message window channels with a plain message open, one bit per channel. |
| Signed Byte | 213         | Track loaded by the last MUSICLOAD, waiting for MUSICCHANGE or another music opcode. |
| Byte        | 214         | 1 while a music track is loading. MUSICLOAD waits on it. Values: 0 = Idle, 1 = Loading. |
| Byte        | 215         | Unused in fields. This region holds engine-only display/timer state rather than script variables: on-screen timer visibility (182) and X/Y position (205/206), a battle-disable flag (207), a "can save here" flag (209), and a battle-music A/B toggle (~201/203, toggled by `Battle_KeepMusicAfterBattle`). |
| Word        | 216         | Screen fade in progress, so a loaded save resumes it: its type (2 is FADEIN). The fade opcodes write 216 to 239 together. |
| Word        | 218         | Screen fade: frames elapsed. It climbs to the duration in variable 220. |
| Word        | 220         | Screen fade: duration in frames. |
| Word        | 222         | Screen fade: current red. |
| Word        | 224         | Screen fade: current green. |
| Word        | 226         | Screen fade: current blue. |
| Word        | 228         | Screen fade: start red. |
| Word        | 230         | Screen fade: start green. |
| Word        | 232         | Screen fade: start blue. |
| Word        | 234         | Screen fade: end red. |
| Word        | 236         | Screen fade: end green. |
| Word        | 238         | Screen fade: end blue. |
| Byte        | 240         | 1 when this field has a draw point set by SETDRAWPOINT, so a loaded save sets it again. |
| Byte        | 241         | Whether that draw point is visible, the value SETDRAWPOINT got. |
| Byte        | 242         | Number of the draw point of this field, from SETDRAWPOINTID. |
| Byte        | 243         | Abilities sealed by SEALEDOFF. A sealed ability's bit is set; 255 seals all. The game copies it to the map seal of the config. Bits: +1 Items sealed, +2 Magic sealed, +4 GF sealed, +8 Draw sealed, +16 Command abilities sealed, +32 Limit breaks sealed, +64 Resurrection sealed, +128 Saving sealed. |
| Long        | 244         | Angelo step counter: grows with steps. At 592 it resets and Angelo gets points, unless Angelo is disabled. |
| Byte        | 248-255     | Not investigated. **Note:** the worldmap-variant descriptions historically listed here (as 244–247) actually belong to offsets **264–267** — see below. These 12 bytes are `unk5` in the struct and their purpose is unverified. |
| Word        | 256         | Main Story quest progress. Both bytes are also copied into the worldmap state block (`+110`/`+111`) by `World_BuildObjectInstanceList` (renamed from `Wmset_SetupWorldmapVariant` in the community IDB), so the worldmap appearance can depend on story progress.                                                                                                                     |
| Byte        | 258         | Bit 1 would make Zell add the lines about Laguna coming to get Ward when he recounts his dream in the D-District Prison start; it is only ever set by the debug room, so in normal play the shorter version is told. Bits: +1 Zell tells Laguna-rescues-Ward part. |
| Byte        | 259-260     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 261         | Save point state shared by every field with a save point: bit 1 is on while the party stands on the save point, and bit 2 blocks the party-switch (PHS) menu there. Bits: +1 Standing on a save point, +2 Party switching disabled at save point. |
| Byte        | 262-263     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 264         | World map switches. Bits 1, 2 and 4 stand Galbadia Garden, with its upright ring, at one of three spots. Bit 8 chooses D-District Prison's height. The rest is about parking Balamb Garden or the Ragnarok. Bits: +1 Galbadia Garden beside Balamb Town, +2 Unused: Galbadia Garden on the north Galbadia coast, no script sets it, +4 Galbadia Garden at the far west of Centra, set at Trabia Garden and cleared on disc 3, +8 D-District Prison stands at full height. Clear: only the tops of its three towers show above the sand. Set on the Galbadia Garden ticket and after the escape, and it stays set, +16 Unused: it would swap the same cell on a world map mode the game never switches on, +32 Garden or Ragnarok has no room to set down at the entrance just used, +64 Lands Garden or the Ragnarok on the next world map frame, +128 Unused. |
| Byte        | 265         | World map train and car switches, set at story turns. Bits: +1 No train runs on the rails, +64 A train you ride drops you at the second station without asking, +128 You can't get out of the car. |
| Byte        | 266         | World map story phase. It picks which places stand on the map, and the world map reads it when it starts. Values: 0 = Start: Missile Base, Galbadia Garden and Balamb Garden stand, Esthar hidden, 1 = Missile Base is rubble (story 482), 2 = Both Gardens have left their sites (story 570), 3 = Esthar shows (story 1750, crossing into Esthar), 4 = From Rinoa's rescue in space. Same places as 3. |
| Byte        | 267         | Unused: it only picks tile sets for a world map mode the game never switches on, and no field script writes it. |
| Byte        | 268         | Which music the world map plays. Field scripts set it at story turns. Chocobo and Ragnarok have their own themes on top. Values: 0 = No music, 24 = SeeD theme, 41 = Blue Fields, except on a chocobo or the Ragnarok, 42 = No track of its own: the music stops, 89 = Blue Fields, only on foot or in Balamb Garden. |
| Byte        | 269         | One-time request: puts Balamb Garden or the Ragnarok at a fixed spot the next time the world map loads, then returns to 0. Values: 0 = No request, 1 = Balamb Garden on Balamb island, 2 = Unused: Balamb Garden on the north Galbadia coast, 3 = Unused: Balamb Garden on the south Galbadia coast, 4 = Ragnarok in Centra, 5 = Ragnarok above the Horizon Bridge, 6 = Ragnarok in Esthar City, 7 = Balamb Garden in the sea at Fisherman's Horizon. |
| Byte        | 270         | Second one-time request of the same kind as variable 269. Only used once, for the Ragnarok in Esthar City. Values: 0 = No request, 6 = Ragnarok in Esthar City. |
| Byte        | 271         | Unused: copied when the world map starts, and nothing reads the copy. |
| Byte        | 272         | Card rules in force in Balamb. The card master script copies them into variable 292 for each match there, adding rules Squall carries in (see 288). After a match the region can gain or lose a rule. New game: Open. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 273         | Card rules in force in Galbadia. The card master script copies them into variable 292 for each match there, adding rules Squall carries in (see 288). After a match the region can gain or lose a rule. New game: Same. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 274         | Card rules in force in Trabia. The card master script copies them into variable 292 for each match there, adding rules Squall carries in (see 288). After a match the region can gain or lose a rule. New game: Plus and Random. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 275         | Card rules in force in Centra. The card master script copies them into variable 292 for each match there, adding rules Squall carries in (see 288). After a match the region can gain or lose a rule. New game: Same, Plus and Random. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 276         | Card rules in force in Dollet. The card master script copies them into variable 292 for each match there, adding rules Squall carries in (see 288). After a match the region can gain or lose a rule. New game: Random and Elemental. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 277         | Card rules in force in Fisherman's Horizon. The card master script copies them into variable 292 for each match there, adding rules Squall carries in (see 288). After a match the region can gain or lose a rule. New game: Sudden Death and Elemental. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 278         | Card rules in force in Lunar Gate. The card master script copies them into variable 292 for each match there, adding rules Squall carries in (see 288). After a match the region can gain or lose a rule. New game: every rule but Retry. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 279         | Card rules in force in Esthar. The card master script copies them into variable 292 for each match there, adding rules Squall carries in (see 288). After a match the region can gain or lose a rule. New game: Same Wall and Elemental. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 280         | Trade rule of Balamb, copied into variable 293 for each match there. After a match it can take the rule of the region in 296 (see 297), or fall back to One (see 298). If the Queen of Cards is in the region, each match has about 1 chance in 3 of giving it her rule (see 299). New game: One. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 281         | Trade rule of Galbadia, copied into variable 293 for each match there. After a match it can take the rule of the region in 296 (see 297), or fall back to One (see 298). If the Queen of Cards is in the region, each match has about 1 chance in 3 of giving it her rule (see 299). New game: One. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 282         | Trade rule of Trabia, copied into variable 293 for each match there. After a match it can take the rule of the region in 296 (see 297), or fall back to One (see 298). If the Queen of Cards is in the region, each match has about 1 chance in 3 of giving it her rule (see 299). New game: One. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 283         | Trade rule of Centra, copied into variable 293 for each match there. After a match it can take the rule of the region in 296 (see 297), or fall back to One (see 298). If the Queen of Cards is in the region, each match has about 1 chance in 3 of giving it her rule (see 299). New game: One. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 284         | Trade rule of Dollet, copied into variable 293 for each match there. After a match it can take the rule of the region in 296 (see 297), or fall back to One (see 298). If the Queen of Cards is in the region, each match has about 1 chance in 3 of giving it her rule (see 299). New game: One. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 285         | Trade rule of Fisherman's Horizon, copied into variable 293 for each match there. After a match it can take the rule of the region in 296 (see 297), or fall back to One (see 298). If the Queen of Cards is in the region, each match has about 1 chance in 3 of giving it her rule (see 299). New game: One. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 286         | Trade rule of Lunar Gate, copied into variable 293 for each match there. After a match it can take the rule of the region in 296 (see 297), or fall back to One (see 298). If the Queen of Cards is in the region, each match has about 1 chance in 3 of giving it her rule (see 299). New game: One. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 287         | Trade rule of Esthar, copied into variable 293 for each match there. After a match it can take the rule of the region in 296 (see 297), or fall back to One (see 298). If the Queen of Cards is in the region, each match has about 1 chance in 3 of giving it her rule (see 299). New game: One. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 288         | Rules Squall carries, latest set: a copy of the rules of the region in 290. At the start of a match 1 time in 4, and after any match outside region 290, the current region's rules go here and this set moves to 289. When a carried set holds a rule the region lacks, the player says "Heard you know rules unfamiliar to this region" and the match adds the rules of the set's region. After such a match the region picks a rule at random, up to three times, and adopts the first one it lacks from the carried set; if none fits, it can drop the rule last picked (1 in 2). A region holding all 7 rules drops one, 1 time in 4, after any match. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 289         | Rules Squall carries, older set: the set 288 held before. See 288. Bits: +1 Open, +2 Same, +4 Plus, +8 Random, +16 Sudden Death, +32 Retry (no script adds it), +64 Same Wall, +128 Elemental. |
| Byte        | 290         | Region whose rules are in 288. Values: 0 = None, 1 = Balamb, 2 = Galbadia, 3 = Trabia, 4 = Centra, 5 = Dollet, 6 = Fisherman's Horizon, 7 = Lunar Gate, 8 = Esthar. |
| Byte        | 291         | Region whose rules are in 289. Values: 0 = None, 1 = Balamb, 2 = Galbadia, 3 = Trabia, 4 = Centra, 5 = Dollet, 6 = Fisherman's Horizon, 7 = Lunar Gate, 8 = Esthar. |
| Byte        | 292         | Scratch byte holding the card game rules for the match about to start: the card master script copies the current region's rules into it, adds any rules carried in from another region, and the NPC passes it to the card game. It is cleared to 0 afterwards. |
| Byte        | 293         | Scratch byte holding the card trade rule for the match about to start (0 none, 1 one, 2 difference, 3 direct, 4 all); the card master script copies it from the region's trade rule and the NPC passes it to the card game. Values: 0 = None, 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 294         | Holds the card rule the Queen of Cards offers to pass on to the current region for 30,000 Gil, stored as the rule bit (1 Open, 2 Same, 4 Plus, 8 Random, 16 Sudden Death, 64 Same Wall, 128 Elemental). It is zeroed at game start and merged into the region's rules when the player pays. Values: 1 = Open, 2 = Same, 4 = Plus, 8 = Random, 16 = Sudden Death, 64 = Same Wall, 128 = Elemental. |
| Byte        | 295         | Region the Queen of Cards is in. She leaves when a match against her changes how many rare cards Squall has; the next region is drawn at random from a list that depends on where she is (from Balamb: Dollet 3 times in 8, otherwise Galbadia). Talking to her in the old place then only gives where she went. New game: Balamb. Values: 1 = Balamb, 2 = Galbadia, 3 = Trabia, 4 = Centra, 5 = Dollet, 6 = Fisherman's Horizon, 7 = Lunar Gate, 8 = Esthar. |
| Byte        | 296         | Region where card trading is busiest, the one the Queen of Cards names; its trade rule is the one that spreads. A match there raises 297; a match elsewhere lowers 297, and at 0 that match's region takes over. New game: Balamb. Values: 1 = Balamb, 2 = Galbadia, 3 = Trabia, 4 = Centra, 5 = Dollet, 6 = Fisherman's Horizon, 7 = Lunar Gate, 8 = Esthar. |
| Byte        | 297         | How busy trading is in the region in 296, 0 to 10. After each match the trade rule of 296 is copied to one region drawn at random, with a chance of about this value in 10. The Queen of Cards reads it: under 3 "little trading", 3 to 5 "much trading", 6 and more "some trading". New game: 0. |
| Byte        | 298         | Pull of the trade rules back to One. After each match it grows by 0 to 7, and goes back to 0 once past 240; then, with a chance of this value in 256, one region drawn at random gets trade rule One. From 128 the Queen of Cards says everybody is avoiding risky trades, instead of naming the rule that spreads. New game: 0. |
| Byte        | 299         | Trade rule of the Queen of Cards, used in matches against her. Each time she is challenged it usually moves one step up or down (from 1 to 2, from 4 to 3, otherwise either way). It also spreads to the region she is in (see 280-287). New game: One. Values: 1 = One, 2 = Difference, 3 = Direct, 4 = All. |
| Byte        | 300         | Cards the Queen of Cards' father has painted. In the Dollet pub, once she holds the card he wants, she passes it on to her son and the next card appears elsewhere (the variable's value tells which step is done). Each step waits for the one before. Values: 0 = None yet, 1 = MiniMog made Kiros (Deling City), 2 = Sacred made Irvine (FH), 3 = Chicobo made Chubby Chocobo (Balamb Garden), 4 = Alexander made Doomtrain (Timber), 5 = Doomtrain made Phoenix (aide in Esthar). |
| Byte        | 301-303     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 304-305     | Timber Maniacs issues found.                                                                                                                                                                                                                                                                                               |
| Byte        | 306-319     | Reserved for Hacktuar / FF8Voice                                                                                                                                                                                                                                                                                           |
| Byte        | 320         | Number (1 to 12) of the painting in Ultimecia Castle's art gallery that the party last stepped up to; the painting room then shows that picture's title and sends the party to its scene. Values: 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 321         | Art gallery record in Ultimecia Castle: the number of the painting visited first (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 322         | Art gallery record in Ultimecia Castle: the number of the painting visited second (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 323         | Art gallery record in Ultimecia Castle: the number of the painting visited third (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 324         | Art gallery record in Ultimecia Castle: the number of the painting visited fourth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 325         | Art gallery record in Ultimecia Castle: the number of the painting visited fifth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 326         | Art gallery record in Ultimecia Castle: the number of the painting visited sixth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 327         | Art gallery record in Ultimecia Castle: the number of the painting visited seventh (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 328         | Art gallery record in Ultimecia Castle: the number of the painting visited eighth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 329         | Art gallery record in Ultimecia Castle: the number of the painting visited ninth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 330         | Art gallery record in Ultimecia Castle: the number of the painting visited tenth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 331         | Art gallery record in Ultimecia Castle: the number of the painting visited eleventh (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 332         | Art gallery record in Ultimecia Castle: the number of the painting visited twelfth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 333         | Treasure Room in Ultimecia Castle: which of the four boxes are open. It is set to 9 (boxes 1 and 4 open) on first arrival at the castle. Pressing a box toggles it and the boxes beside it in the row; all four open (15) calls Catoblepas and the boxes lock. Bits: +1 Box 1 open, +2 Box 2 open, +4 Box 3 open, +8 Box 4 open. Values: 9 = Starting state: boxes 1 and 4 open, 15 = All four open; Catoblepas appears. |
| Byte        | 334         | Ultimecia Castle seals released: after beating a guardian the party picks one seal to release, and its bit is set. All eight set (255) changes the party's lines before Ultimecia's chamber. Values: 255 = Everything unsealed. Bits: +1 Item unsealed, +2 Magic unsealed, +4 GF unsealed, +8 Draw unsealed, +16 Command abilities unsealed, +32 Limit Break unsealed, +64 Resurrection unsealed, +128 Save unsealed. |
| Byte        | 335         | One-time flag set on the first visit, from story 3860 (start of Disc 4), to the escape pod site on the south Esthar peninsula, where the Queen of Cards waits. She then takes back Chubby Chocobo, Phoenix, Doomtrain, Kiros and Irvine cards you don't hold, except ones with seven other card players if var 475 bit 32 is set. Values: 0 = Not done yet, 1 = Done. |
| Byte        | 336         | Deling City bus and driveway state. Bits 1 to 32 are the buses you ride: prompt to get off is showing, and Circle was pressed. Bit 64 means Rinoa asked not to be left in the house at the mansion gate. Bit 128 means a car you drove in is parked at the rental office. Bits: +1 First bus route: get-off prompt showing, +2 First bus route: Circle pressed, +4 Second bus route: get-off prompt showing, +8 Second bus route: Circle pressed, +16 Third bus route: get-off prompt showing, +32 Third bus route: Circle pressed, +64 Rinoa's talk at the mansion gate played, +128 Your car parked at the rental office. |
| Byte        | 337         | Deling City one-time events. Bit 1: Quistis takes the cup in the locked room of Caraway's Mansion, which lets her open the secret way out next door. Bit 2: the hatch in the Presidential Residence corridor is open. Bits 4, 32, 64 and 128: sewer levers pulled, each removing a grate. Bits: +1 Quistis took the cup (Caraway's Mansion), +2 Presidential Residence corridor hatch open, +4 Sewer lever pulled: third map, left, +32 Sewer lever pulled: fourth map, lower left, +64 Sewer lever pulled: fourth map, upper left, +128 Sewer lever pulled: third map, right. |
| Byte        | 338         | Deling City Sewer levers, second set. Bits 1, 2, 32 and 64 are levers in the fourth sewer map, bits 4, 8 and 16 in the fifth; each removes a grate, some of them seen again in other sewer maps. Bit 128 is checked by a grate in the third map but nothing sets it. Bits: +1 Sewer lever: fourth map, lower right, +2 Sewer lever: fourth map, upper right, +4 Sewer lever: fifth map, lower right (one section), +8 Sewer lever: fifth map, upper right, +16 Sewer lever: fifth map, lower right (other section), +32 Sewer lever: fourth map, second lower right, +64 Sewer lever: fourth map, centre left upper, +128 Never set; its grate in the third map stays shut. |
| Byte        | 339         | Reused byte. Deling City Sewer: bits 1, 2 and 4 are levers in the third map and bit 64 means Weapons Monthly May Issue is taken. Centra Ruins tower: bits 16 and 32 mean the party is mid-climb on the left or right ladder between floors. Bit 128: Caraway took your Ifrit card. Bit 8 is only cleared. Bits: +1 Sewer lever: third map, centre right, +2 Sewer lever: third map, upper right, +4 Sewer lever: third map, left (other section), +8 Only ever cleared, +16 Centra tower: mid-climb on left ladder, +32 Centra tower: mid-climb on right ladder, +64 Weapons Monthly May Issue taken (sewer), +128 Caraway took your Ifrit card. |
| Byte        | 340         | Reused byte. Battle of the Gardens: SeeD sent to the front gate (1 Quistis, 2 Selphie, 3 Irvine). Garden fistfight: blocks in a row (3 unlocks Deathblow). Concert: member choosing an instrument (1 to 4). Caraway's Mansion: Zell's search step (1 to 12). Deling sewer: section (0 to 25). Timber Forest: second party member. Values: 0 = Not set. |
| Byte        | 341         | Reused byte. Caraway's Mansion: Selphie's search step (1 to 9, skipping 8). Concert: band lineup, read on the Sun Panel to choose the scene (1 sax, piano, electric guitar, bass; 2 guitar, violin, flute, tap; 3 any other with sax; 0 the rest). Timber Forest: third party member. Values: 0 = Not set. |
| Byte        | 342         | Deling City bus route in progress: the number of the stop-to-stop leg the bus is travelling (1 to 16), set when the player boards and cleared to 0 when the bus arrives. It tells each stop's scene where the bus comes from. |
| Byte        | 343         | Galbadia Garden events. Bit 1 is set after the Reception Room wait and starts the Raijin and Fujin meeting in the hall, which clears it and sets bit 2 until the hall is re-entered. Bit 4: Irvine's Front Gate talk. Bits 16, 32, 64: Card Keys 1, 2, 3 received. Bit 128: Athletic Track door unlocked. Bits: +1 Reception Room wait done (cleared after the hall scene), +2 Raijin and Fujin scene in the hall (cleared on re-entry), +4 Irvine's Front Gate talk done, +16 Card Key 1 received, +32 Card Key 2 received, +64 Card Key 3 received, +128 Athletic Track door unlocked. |
| Byte        | 344         | Battle of the Gardens events. Balamb Garden 2F Hallway: bits 1, 2 and 8 remove trainees and staff once met, bit 4 is the Cottage received; speaking to Zell at his post sets all four. Galbadia Garden: bit 32 Lock 3 door opened, bit 64 elevator unlocked, bit 16 elevator arrival walk, bit 128 Cerberus fought. Bits: +1 Trainee on 2F questioned, +2 Trainee group on 2F met, +4 Cottage received from classman, +8 Provisions staff on 2F passed, +16 Elevator arrival walk pending (cleared in Master Room), +32 Lock 3 door opened, +64 Elevator lock opened, +128 Cerberus fought. |
| Byte        | 345         | Mixed bits. Bit 1: first camera pan in the Mayor's Residence at Fisherman's Horizon played. Bit 4: Solomon Ring taken at Tears' Point. Bit 8: Odin's timer is running in the Centra Ruins. Bits 16, 32, 64, 128: Galbadia Garden Lock 1, Lock 2 (two doors) and Lock 3 doors opened. Bits: +1 Mayor's Residence pan played (FH), +4 Solomon Ring taken, +8 Odin timer running (Centra Ruins), +16 G-Garden: Lock 1 door opened, +32 G-Garden: Lock 2 door opened (first door), +64 G-Garden: Lock 2 door opened (second door), +128 G-Garden: Lock 3 door opened. |
| Byte        | 346         | Instrument chosen for Zell in the Fisherman's Horizon concert band, picked from a list of eight; the same instrument cannot be given to two members, and the lineup decides how the concert goes. Values: 0 = None chosen, 1 = Guitar, 2 = Sax, 3 = Electric Guitar, 4 = Piano, 5 = Violin, 6 = Flute, 7 = Bass Guitar, 8 = Tap (dance). |
| Byte        | 347         | Instrument chosen for Irvine in the Fisherman's Horizon concert band, picked from a list of eight; the same instrument cannot be given to two members, and the lineup decides how the concert goes. Values: 0 = None chosen, 1 = Guitar, 2 = Sax, 3 = Electric Guitar, 4 = Piano, 5 = Violin, 6 = Flute, 7 = Bass Guitar, 8 = Tap (dance). |
| Byte        | 348         | Instrument chosen for Selphie in the Fisherman's Horizon concert band, picked from a list of eight; the same instrument cannot be given to two members, and the lineup decides how the concert goes. Values: 0 = None chosen, 1 = Guitar, 2 = Sax, 3 = Electric Guitar, 4 = Piano, 5 = Violin, 6 = Flute, 7 = Bass Guitar, 8 = Tap (dance). |
| Byte        | 349         | Instrument chosen for Quistis in the Fisherman's Horizon concert band, picked from a list of eight; the same instrument cannot be given to two members, and the lineup decides how the concert goes. Values: 0 = None chosen, 1 = Guitar, 2 = Sax, 3 = Electric Guitar, 4 = Piano, 5 = Violin, 6 = Flute, 7 = Bass Guitar, 8 = Tap (dance). |
| Word        | 350         | Squall's starting health in the Balamb Garden fistfight: 600 plus the bonus in variable 380. It is written once and nothing reads it; the health bar takes its scale from variable 354. |
| Word        | 352         | The Galbadian soldier's starting health in the Balamb Garden fistfight, set to 600. It is written once and nothing reads it; the health bar takes its scale from variable 356. |
| Signed Word | 354         | Squall's current health in the Balamb Garden fistfight; it starts at 600 plus variable 380, drops when he is hit (less when blocking), and 0 or below loses the fight. When time runs out, whoever has less health is dropped to 0. |
| Signed Word | 356         | The Galbadian soldier's current health in the Balamb Garden fistfight; it starts at 600, drops when Squall hits him and can go below 0. When time runs out, whoever has less health is dropped to 0. At 0 or below he is gone from the second part of the fight. |
| Byte        | 358         | Mixed bits. Lunar Base: bit 1 Squall looked through the moonscope, bit 4 Ellone said she can't send him to Rinoa, bit 8 Ellone is out walking the base. Bit 16: Selphie, in SeeD uniform, stands once in the Quad up to story 65. Bit 32: Odin beaten. Bit 64: Raijin's talk on Disc 2. Bit 128: Odin's fight or timer just ended. Bits: +1 Moonscope used (Lunar Base), +2 Read by Ellone but never set, +4 Ellone refused to send Squall to Rinoa, +8 Ellone out walking the Lunar Base, +16 Selphie in SeeD uniform seen once in the Quad (up to story 65), +32 Odin beaten, +64 Raijin's talk done (G-Garden Hallway), +128 Odin fight or timer just ended (cleared at once). |
| Byte        | 359         | Centra Ruins puzzle. The left and right eyes move between two statues: bits 1, 2 tower statue, bits 4, 8 roof statue. Both eyes in the roof statue show the code, both in the tower statue let you enter it; bit 32 is Code Accepted. Bit 128 power switch, bit 64 tower console (lights and stairs). Bit 16: first arrival. Bits: +1 Tower statue has left eye, +2 Tower statue has right eye, +4 Roof statue has left eye, +8 Roof statue has right eye, +16 First arrival done, eyes placed, +32 Code accepted, +64 Tower console used, +128 Power switch pulled. |
| Long        | 360         | Music-part mask for the Fisherman's Horizon concert: each of the four instrument choices (variables 346-349) switches on its bits, and the mask goes to the music as the show starts and in the field outside. It is never reset, so it stays set after the concert. bit 0 Always on, bit 1 Tap, bit 2 Flute, bit 3 Violin, bits 4-11 Guitar, bit 12 Sax, bits 13-18 Piano, bits 19-21 Electric Guitar, bit 22 Bass. |
| Byte        | 364         | The first digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 365         | The second digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 366         | The third digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 367         | The fourth digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 368         | The fifth digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 369         | Unrelated bits. Bits 1, 2, 4: sewer ladders lowered in Deling City. Bit 8: Lunar Base crew member's Adel story seen. Bit 16: Wilderness gate scene played. Bits 32, 64, 128: set in the Ultimecia Castle Elevator Hall on a party switch to place the lifts and arriving party, then cleared on arrival. Bits: +1 Sewer ladder lowered (third map), +2 Sewer ladder lowered (second map, section 16), +4 Sewer ladder lowered (second map, section 25), +8 Crew member's Adel story seen, +16 Wilderness gate scene played, +32 Elevator Hall: left lift up, right lift down on arrival, +64 Elevator Hall: switched from right lift to left (until arrival), +128 Elevator Hall: switched from upper left to right (until arrival). |
| Byte        | 370         | In Ultimecia's Castle, where the party you aren't controlling waits. Switch points jump there and store the room just left. Value 8 also keeps the Grand Hall lever held down by that party. It becomes 1 on entering the castle and 0 when you leave over the bridge. Values: 0 = Together (no split, or at the bridge), 1 = Hall, 2 = Stairway Hall (felfst1), 3 = Elevator Hall, left lift, 4 = Elevator Hall, right lift, 5 = Stairway Hall (ferrst1), 6 = Stairway Hall (ferfst1), 7 = Courtyard, 8 = Grand Hall, holding the lever down, 9 = Elevator Hall, after you stepped off the left lift. |
| Byte        | 371         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 372         | Ultimecia's Castle guardians. Most bits are set when that guardian is beaten, removing it. The Art Gallery and Prison Cell bits work the other way: set to make the guardian appear (after solving the painting title or taking the Prison Key) and cleared when it is beaten. Bits: +1 Hall: Sphinxara beaten, +2 Terrace: Krysta beaten, +4 Treasure Room: Catoblepas beaten, +8 Wine Cellar: Tri-Point beaten, +16 Art Gallery: Trauma is present, +32 Armory: Vysage, Lefty and Righty beaten, +64 Prison Cell: Red Giant is present, +128 Clock Tower: Tiamat beaten. |
| Byte        | 373         | Ultimecia's Castle key and hatch flags: one bit per key picked up, plus a hatch in the Grand Hall. Bits: +1 Floodgate Key obtained, +2 Treasure Vault Key obtained, +4 Armory Key obtained, +8 Prison Key obtained, +16 Grand Hall floor hatch broken open. |
| Byte        | 374         | Ultimecia's Castle doors and the bell. Treasure Room and Armory doors opened with their keys; Prison Cell doors; the 60-second countdown started by ringing the bell, during which Omega Weapon stands in the Chapel; and Omega Weapon beaten, after which the bell only rings. Bits: +1 Treasure Room door unlocked, +2 Prison Cell door opened with the key, +4 Prison Cell door shut by the auto-lock, +8 Armory door unlocked, +32 Prison Cell auto-lock disengaged, +64 Bell countdown running, +128 Omega Weapon beaten. |
| Byte        | 375         | Ultimecia's Castle puzzles. Bit 1: Floodgate Key used. Bit 2: water stopped at the Flood Gate, draining the Waterway; clear means it flows. Bit 8: Art Gallery painting named correctly. Bit 16: Catoblepas called, Treasure Room boxes locked. Bit 32: Rosetta Stone taken. Bits: +1 Floodgate unlocked with the key, +2 Water stopped at the Flood Gate, +8 Art Gallery painting named correctly, +16 Catoblepas called, boxes locked, +32 Rosetta Stone taken. |
| Byte        | 376         | Where the Armory Key is until picked up. Running on the Clock Tower bridge shakes it loose: it drops into the Waterway if the water is stopped, otherwise it washes to the Flood Gate. Restarting the water also carries it from the Waterway to the Flood Gate. Values: 0 = On the Clock Tower bridge, 1 = In the Waterway, 2 = At the Flood Gate. |
| Byte        | 377         | Notes held on the Chapel organ in Ultimecia's Castle: one bit per note. Only the last chord counts: after all buttons are released the next note starts over. In the Passageway each note clears a pair of grates, and only all four at once (15) lets you walk through. Bits: +1 DO in last chord, +2 RE in last chord, +4 MI in last chord, +8 FA in last chord. Values: 15 = All four held together: Passageway open. |
| Byte        | 378         | Stage of Odin's countdown in the Centra Ruins. It starts at 0 and rises as the timer runs down, making Odin speak a new taunt each stage; when the time is up he kills the party, and the next screen offers a retry or the game over. Values: 0 = Countdown not started, 1 = Odin: 'I am Odin...', 2 = Odin: 'To him who doth vanquish me...', 3 = Odin: 'Come hither, knight-errant...', 4 = Odin: 'Two knights, but one victor.', 5 = Odin: 'Thou must use thy wits...', 6 = Odin: 'Behold, thy doom is near.'. |
| Byte        | 379         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 380         | Bonus health for Squall in the Balamb Garden fistfight: each lost try adds 200, up to 5000, so the fight gets easier. His bar starts at 600 plus this; the soldier's stays at 600. |
| Byte        | 382-383     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 384         | Early Garden flags: Squall's Study Panel at his classroom desk being on, and his first GFs, Quetzalcoatl and Shiva. He receives and names them on first logging in at the panel; if he never did, Quistis hands them over at the front gate. Bit 4 is only used in a test room. Bits: +1 Study Panel switched on, +2 Quetzalcoatl and Shiva received. |
| Byte        | 385         | Laguna's first dream, the Galbadia Hotel bar: the grey third answer to the waiter's greeting. Bit 1: Laguna picked '(Huh? Excuse me?)'; the menu then changes. Bit 2: he picked '(What is this?)' and the three admit their heads buzz. Picking it again gets 'Just shut up, PU-LEASE!!!'. Bits: +1 Picked grey '(Huh? Excuse me?)', +2 Picked grey '(What is this?)', head-buzz talk heard. |
| Byte        | 387         | Progress of Laguna's day in Winhill, from Ellone fetching him to the patrol report. It decides which scene each map plays, and the bed: from 26 on, choosing to rest gives Laguna's 'I get scared sometimes' talk and ends the dream. Values: 0 = Not started, 2 = Ellone says a visitor is at the pub, 4 = Ellone: 'I waited! Am I a good girl?', 6 = 'Ellone! Now's your chance!' in the square, 8 = Kiros turns up at the pub, 10 = Talked with Kiros; he joins Laguna, 12 = Back in the pub, ready to go out, 16 = Laguna explains he's Winhill's Monster Hunter, 18 = First patrol complete at the town entrance, 20 = Kiros mentions Timber Maniacs, 22 = Laguna wants to stay in Winhill, 23 = Walks back through the square, 24 = Patrol report starts at the pub, 26 = Raine: wait in your room; bed ends the dream. |
| Byte        | 388         | Talk flags in the Timber Maniacs lobby: the receptionist and the magazine pile. Bits: +1 Receptionist greeted, +2 Receptionist visit repeated, +4 Girl Next Door magazine taken. |
| Byte        | 389         | Which topic Squall picked when talking to the Timber Maniacs editor-in-chief; the following room plays a scene according to it. It is reset to 0 at the start of each chat. Values: 0 = No topic yet, 2 = About Timber Maniacs, 4 = The dream with Laguna, 6 = About Timber's situation. |
| Byte        | 390         | How far Squall has got in talking with Edea in her house's backyard: 0 until she has told him where the White SeeD ship may be and handed him her letter. Values: 0 = White SeeD ship not asked about, 1 = Edea gave the letter and the ship hint. |
| Byte        | 391         | Laguna's Presidential Palace office in Esthar: his greeting, the long 'Where's Ellone?' answer and the 'What are you doing here?' story with its flashback. Bit 16 only lasts through the flashback. Bits: +1 Laguna's greeting heard, +4 Laguna explained where Ellone is, +8 Laguna finished his story, +16 Flashback in progress. |
| Byte        | 392         | Reused. At Edea's House backyard bits 1, 2 and 4 record Edea's speeches. Bit 8 is unrelated: it only lasts while coming back from Selphie's page to the Study Panel menu, which then plays its return screen. Bits: +1 Edea told about Sorceress Adel, +2 Edea apologized to Rinoa, +4 Edea told Rinoa to find a knight, +8 Returning from Selphie's page. |
| Byte        | 393-399     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Long        | 400         | Number of enemies killed (variable 68) as it stood when the Winhill patrol began; the report to Raine later subtracts it from the count at the end. |
| Long        | 404         | Number of enemies killed (variable 68) as it stood when Laguna returns from his Winhill patrol; the difference with variable 400 is the 'monsters exterminated' count in his report. |
| Byte        | 408         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 409         | NEW marks on Selphie's Garden Festival page, reached from the Study Panel. A bit is set once that section has been read, which removes its mark. Nothing ever clears these, so a mark never comes back even when new entries appear later. Bits: +1 Notices read, +2 Pals messages read, +4 Diary read. |
| Byte        | 410-431     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 432         | Balamb Garden after the Dollet field exam, while waiting for results: one-time scenes in the front hall. Xu's report to Cid plays on arrival, Xu praises Squall, Cid asks about the battlefield, and two students discuss the tower before they can be spoken to. Bits: +4 Xu reported to Cid, +8 Xu praised Squall, Quistis replied, +32 Cid asked about the battlefield, +64 Students' tower talk heard. |
| Byte        | 433         | Exam-day and SeeD-night story flags in Garden. Bit 2 is night: from the SeeD ceremony until Selphie announces the first mission, staff say only the training center is open, and the dorm leads to night maps. Bit 1 is never set in play. Bits: +1 Never set in play, +2 Night in Garden, +4 Cid's speech before the exam heard, +8 Back from Dollet at the front gate, +16 Selphie showed off her SeeD uniform, +128 Left for the exam (movie played). |
| Byte        | 434         | Early Garden flags: running into Selphie on 2F and her tour, students' 2F hallway exam gossip, a classmate's Fire Cavern line, two students on the ring corridor, and later Xu's greeting on the Garden bridge. Bit 16 drops briefly during the tour. Bits: +1 Second hallway exam talk heard, +2 Classmate's Fire Cavern line heard, +4 First hallway exam talk heard, +8 Students came back along the corridor, +16 Selphie met on 2F, +32 Tour in progress, +128 Xu's greeting on the bridge heard. |
| Byte        | 435         | Garden student talks, mostly on 2F: the gunblade classmate, the boy at the 'Do Not Open' door, the brother and sister with the cold, Cid in bed, the magic request that brings Mr. Aki, and the card story about the boy who ran laps. Bits: +1 Classmate's gunblade chat done, +2 Boy at 'Do Not Open' door spoke, +4 Cid spoke in the infirmary, +8 Brother and sister: first talk, +16 Sister has a cold, +32 Sister recovered, +64 Student's magic request, Mr. Aki shouted, +128 Hall boy's playing-card story heard. |
| Byte        | 436         | D-District Prison choices and scenes. Bit 2 is Squall's torture answer, not a Warden fight: '...I'll lie...' sets it. It decides who wakes him, whether two Moombas stay, and in Laguna's Esthar dream whether he catches the falling Moomba. Bit 32 is also read at the training center. Bits: +1 Zell stopped the guard, Moomba saved, +2 Squall chose '...I'll lie...' under torture, +4 Zell's group reached Squall's floor, +8 Moombas shouted 'Laguna!', Zell follows them, +16 Moombas seen running off, +32 Joker introduced himself, +64 Moomba gave the Cottage, +128 Moomba gave the Rename Card. |
| Byte        | 437         | Reused. In D-District Prison it is the current stage of the prison tower (0 to 13), shown on the elevator panel as 'Floor N'. On Disc 2 in Balamb Garden it is a bitmask of the party members who join Squall (bit 1 Zell, 2 Irvine, 4 Rinoa, 8 Quistis). On the Ragnarok it counts fights with the alien monsters, ending past 24. Bits: +1 Zell joins (Garden, Disc 2), +2 Irvine joins (Garden, Disc 2), +4 Rinoa joins (Garden, Disc 2), +8 Quistis joins (Garden, Disc 2). |
| Byte        | 438         | Cid vs NORG fight in Balamb Garden (Disc 2): faculty beaten at each spot, the Mega Potion at the gate, the first 'headmaster isn't here' scene, Xu's hall scene, and whether Squall has openly sided with Cid. Faculty talk politely until bit 128 is on. Bits: +1 Faculty beaten on the tree-lined road, +2 Faculty beaten at the Garden entrance, +4 Mega Potion from the student at the gate, +8 Xu scene in the hall played, +16 Faculty beaten on the dorm corridor, +32 Faculty beaten on the library corridor, +64 First 'headmaster isn't here' scene seen, +128 Squall openly sided with Cid. |
| Byte        | 439         | More Cid vs NORG flags (Disc 2): faculty fights, students' gifts, Cid's hologram and the hot dog joke. The library, parking lot and cafeteria gifts count toward Xu's appearance in the hall, together with var 440 bits 1 and 4 and var 441 bit 1: three of the six are needed. Bits: +1 Mega Phoenix from the library student, +2 Faculty beaten on the parking lot corridor, +4 Cid's hologram seen, +8 Tent from the parking lot student, +16 Faculty beaten on the cafeteria corridor, +32 Gysahl Greens from the cafeteria student, +64 Hot dog joke with Zell heard, +128 Faculty beaten in the Quad. |
| Byte        | 440         | Cid vs NORG scenes (Disc 2) at the Quad, the infirmary corridor, the infirmary and the training center. Choosing 'Help them' on the corridor puts the wounded man in the infirmary. Bits 1 and 4 count toward Xu's appearance in the hall. Bits: +1 Quad scene: students ask whose side you're on, +2 X-Potion from the Quad student, +4 Corridor fight outside the infirmary seen, +8 Chose 'Help them' in that fight, +16 Nida talked to, +32 Dr. Kadowaki's infirmary talk heard, +64 Dr. Kadowaki gave the Elixir, +128 Training center entrance chase seen. |
| Byte        | 441         | Garden flags: training center rescue, gifts and Xu's hall scene (Disc 2), and bit 128, Garden under way: the front gate won't let you out, and the deck shows another view, until you tell Nida to go. Bit 64 is checked but never set. Bits: +1 Training center stop over, +2 Junior classmen saved (or the boy won back at cards), +4 Training center SeeD gave a Remedy, +8 Xu scene in the hall played, +16 Library student spoke, +64 Never set, +128 Garden under way, gate closed. |
| Byte        | 442         | Rinoa's Garden tour on Disc 2. It starts in the dorm only if she came back with Squall (var 734 bit 4). If she didn't, the hall scene never plays. Bits: +1 Tour with Rinoa started, +2 Rinoa's 'This place is huge' line seen, +4 'What's over here?' stop at the hall seen. |
| Word        | 443         | Unused: no script or game code touches it. |
| Byte        | 445         | Ragnarok during the Propagator chase. Bit 1: security lock released. Bit 2: Squall tried the locked door in the aisle ('It's no use'). Bit 4: one Propagator of a colour is beaten and its partner is next; if the next fight is another colour, the last one comes back. Bits: +1 Security lock released, +2 Squall's locked-door line played, +4 Waiting for the partner of the last Propagator. |
| Byte        | 446         | One bit per Propagator on the Ragnarok, set when it is fought. Beat two of a colour in a row to keep them gone: fighting another colour instead clears the previous bit, and that one returns. 255 means all gone and the cockpit lift works; more than 24 fights forces 255. Bits: +1 Air Room (yellow) fought, +2 Aisle rgroad1 (green) fought, +4 Aisle rgroad2 (red) fought, +8 Aisle rgroad3 (red) fought, +16 Hangar rghang1 (purple) fought, +32 Hangar rghang2 (green) fought, +64 Entrance rgexit1 (purple) fought, +128 Passenger Seat (yellow) fought. Values: 255 = All Propagators gone. |
| Byte        | 447         | The Propagator fought last on the Ragnarok, as a single bit (same order as variable 446). The next fight checks it against its partner of the same colour; if it isn't the partner, this one comes back. Bits: +1 Last fight: Air Room (yellow), +2 Last fight: Aisle rgroad1 (green), +4 Last fight: Aisle rgroad2 (red), +8 Last fight: Aisle rgroad3 (red), +16 Last fight: Hangar rghang1 (purple), +32 Last fight: Hangar rghang2 (green), +64 Last fight: Entrance rgexit1 (purple), +128 Last fight: Passenger Seat (yellow). |
| Signed Word | 448         | Main story progress (variable 256) at the brother and sister's latest talk in the 2F hallway, the one where she has a cold. Their next talk waits until the story has moved past this value. |
| Byte        | 450         | Records which one-time pickups have been taken: the Magical Lamp from Headmaster Cid, two Weapons Monthly issues in Balamb Garden, and several items in the D-District Prison area. A set bit stops the item from being given again. Bits: +1 Magical Lamp from Cid taken, +2 Weapons Monthly, April taken, +4 Weapons Monthly, July taken, +8 Tent taken (prison), +16 Pet House taken (prison), +64 HP Up taken (prison), +128 Luck Up taken (prison). |
| Byte        | 451         | Records which one-time pickups have been taken in the D-District Prison area and in the Esthar road areas visited as Laguna. A set bit stops the item from being given again. Bits: +1 Combat King 001 taken (prison), +2 Combat King 005 taken (Esthar), +4 Pet Nametag taken (prison), +8 Strength Up taken (prison), +16 Power Generator taken (Esthar), +32 Phoenix Pinion taken (Esthar), +64 LuvLuv G taken (Esthar), +128 Spd-J Scroll taken (Esthar). |
| Byte        | 452         | Lunatic Pandora flags in Squall's party's visits (not Laguna's). Bit 8 is set by boarding at the 1st Contact Point and stops the machine in the lower hall from throwing the party out on the way back from the upper corridor lift. Bits: +1 Biggs and Wedge quit scene seen; they are gone after it (ebinto3, boarding from the Ragnarok), +2 First arrival in Adel's chamber; nothing reads this bit, +8 Boarded at the 1st Contact Point (Esthar City run): no machine trap in the lower hall. |
| Byte        | 453         | Floor chosen with the top Moomba lift in the D-District Prison, stored as the floor number minus one. 0 means no choice; the prison floor maps check it against the current floor to open the shortcut. Values: 0 = No floor chosen, 9 = Floor 10, 10 = Floor 11, 11 = Floor 12. |
| Byte        | 454         | Floor chosen with the middle Moomba lift in the D-District Prison, stored as the floor number minus one. 0 means no choice. Values: 0 = No floor chosen, 4 = Floor 5, 5 = Floor 6, 8 = Floor 9. |
| Byte        | 455         | Floor chosen with the bottom Moomba lift in the D-District Prison, stored as the floor number minus one. 0 means no choice. Values: 0 = No floor chosen, 1 = Floor 2, 2 = Floor 3, 3 = Floor 4. |
| Byte        | 456-457     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 458         | Holds the playing music's position, saved just before leaving a map so the next map can resume the track with the music-skip instruction. It is saved in the Garden hallways and the Fisherman's Horizon deck; the PC version always stores 0. |
| Byte        | 459         | Holds the playing music's position, saved just before leaving a Balamb Garden map so the next map can resume the track with the music-skip instruction. The PC version always stores 0. |
| Byte        | 460         | Battle Meter and Garden flags. Cid gives the Battle Meter, a prison card player and Joker each upgrade it after a card win, and Mr. Aki's rebuke costs SeeD points. Bit 128 marks the Garden as ready to leave Fisherman's Horizon. Bits: +1 Battle Meter received from Cid, +2 Prison man upgraded Battle Meter, +4 Joker upgraded Battle Meter (GFs), +8 Prison man offered an upgrade, +16 Joker offered an upgrade, +32 Ship monster report read (Ragnarok), +64 Mr. Aki caught Squall; -100 SeeD, +128 Garden ready to leave FH. |
| Byte        | 461-473     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 474         | Card-related one-time flags: the Garden boy gives Squall 7 cards, and later on the Ragnarok Xu, Joker and Quistis have been met. Bits: +1 Garden boy gave 7 cards, +2 Xu met on the Ragnarok, +4 Joker met on the Ragnarok, +8 Quistis (King) met on the Ragnarok. |
| Byte        | 475         | Card game talk flags in Balamb Garden and with Joker. Bit 1 records that Squall did not win his last match against Dr. Kadowaki: she then plays low-level cards with a chance of rare ones, and after a win high-level cards without any. Bit 2 raises the levels of both. Bit 32 is set at random (1 in 3) when resting in the dorm from story 750 once bit 2 is on, and starts the scene where Quistis is the CC Group's King. Bits: +1 Dr. Kadowaki: last match not won, +2 Dr. Kadowaki denied being in the CC Group, +4 Joker met in the prison, +8 Joker met in Garden, +16 Joker introduced himself, +32 Quistis revealed as King, +64 Zell talked about his cards, +128 Member No. 109 talked about his cards. |
| Byte        | 476         | Progress of the CC Group card challenges in Balamb Garden. Each member appears and challenges Squall in turn: Jack, Club, the Diamond duo, Spade, then Xu as Heart. Bit 128 marks the missing running boy as found alive. Bits: +1 Jack has challenged Squall, +2 Jack has been beaten, +4 Club has challenged Squall, +8 Diamond duo has challenged Squall, +16 Spade has challenged Squall, +32 Xu revealed as Heart, +64 Nida remarked on Xu being a CC suit, +128 Running boy found alive. |
| Byte        | 477         | CC Group members beaten. The game's debug menu names them all, but only that menu sets King and Joker: no script does. Bits: +1 Jack beaten, +2 Club beaten, +4 Spade beaten, +8 Heart (Xu) beaten, +16 Diamond duo beaten, +32 King beaten (debug menu only), +64 Joker beaten (debug menu only). |
| Byte        | 478         | Card games won against Balamb Garden students. Jack challenges Squall from 15 wins on. |
| Byte        | 479         | Controls random battles on the current field: 0 turns them off when a field loads, 1 turns them on. Most fields check it at load, and scripts set it to match their battle on or off command. Values: 0 = Random battles off, 1 = Random battles on. |
| Byte        | 480         | First classroom scene before the SeeD exam, story 14 and 15: 2 once Quistis has walked in and said 'Good morning, class', 4 once the classmate in the aisle has stepped aside for Squall. The students' other checks accept every value up to 4. Values: 0 = Before class, 2 = Quistis began the class, 4 = Classmate stepped aside for Squall. |
| Byte        | 481         | Complaining students in the cafeteria: each bit marks the last line of their talk heard at one story stage. With all five set, from story 1200 on, they appear in SeeD uniform and thank Squall for hearing them out. Bits: +1 'Sad people' talk heard, +2 'Paper Test Boy' talk heard, +4 'Never expected this' talk heard, +8 'We are SaaaaaaD' talk heard, +16 'Sometimes I enjoy it' talk heard. |
| Signed Word | 482         | Error ratio of the missiles, set at the Missile Base monitor room. It starts at 0, goes down by 6 per press up to -150, which is the maximum error ratio. Values: -150 = Maximum error ratio, 0 = No error. |
| Byte        | 484         | Missile Base mission progress. The monitor-room bits record the error ratio and data upload, the alarm bit rings when the party is caught or the self-destruct starts, and several bits feed the SeeD points of the mission. Bits: +1 Error ratio set to maximum, +2 Equipment check/data upload done, +4 Alarm sounding, +8 Cover blown (disguises dropped), +32 Launcher pushed into position, +128 Control room entered. |
| Byte        | 485         | Tomb of the Unknown King flags. Bits 1, 4, 16, 64 and 128 are set together by the 'F-Float!' scene at the viewing spot, which removes the students there. Bit 2 is set by the fight with Sacred and Minotaur in the central room, which removes them. Bits: +1 Students scene played, +2 Sacred and Minotaur beaten, +4 Students scene played, +16 Students scene played, +64 Students scene played, +128 Students scene played. |
| Byte        | 486         | Current position in the Tomb of the Unknown King maze, used to decide where each passage leads. 0 is the entrance and 73 to 76 mark rooms 1 to 4. Values: 0 = Tomb entrance, 73 = Room 1, 74 = Room 2, 75 = Room 3, 76 = Room 4. |
| Byte        | 487         | Balamb Garden classroom bit 1 and Missile Base penalties. Bit 1 is set while Squall sits at his classroom seat; bits 16 and 32 each reduce the SeeD points paid after the Missile Base mission. Bit 64 is set by the control room soldier scene. Bits: +1 Squall seated in classroom, +16 Gave maintenance man the wrong message, +32 Party caught as intruders. |
| Byte        | 488         | Marks which inactive party members stand where after the party splits (the Missile Base group on one side, the others in Fisherman's Horizon and the cafeteria). Each of Irvine, Quistis, Rinoa and Zell has a low and a high bit, so two members do not stack in the same place. Bits: +1 Irvine, first place, +2 Quistis, first place, +4 Rinoa, first place, +8 Zell, first place, +16 Irvine, second place, +32 Quistis, second place, +64 Rinoa, second place, +128 Zell, second place.<sub>1</sub> |
| Byte        | 489         | One-time flags: Fishermans Horizon talks with Rinoa and Mayor Dobe, the cafeteria lady's lost son, and the Esthar display panel where Color check and Camouflage each set their own bit. With both set, the party says something new. Bits: +1 Rinoa left after her FH talk, +2 Mayor Dobe talk finished, +4 Panel: Color check tried, +8 Panel: Camouflage tried, +32 Irvine told the son about Garden, +64 Squall recognized the cafeteria lady's son, +128 Cafeteria lady told of her son. |
| Byte        | 490         | Disciplinary committee in the Garden cafeteria. Bit 1 plays on first seeing them: Raijin asks for water and Fujin answers '...IGNORE.' Bit 2 is Raijin whispering to Squall about Fujin, after which she snaps at him and they stand apart. Bits: +1 Fujin ignored Raijin ('...IGNORE.'), +2 Raijin whispered to Squall. |
| Byte        | 491         | Tomb of the Unknown King progress. Bit 2: Sacred driven off in the first room; the save point and passages open. Bits 4 and 8: water channel opened and gearwheel turned; both open the way to the central room. Bits 16 and 32: Brothers beaten and the sealed one freed; nothing reads these two. Bits: +2 Sacred driven off (first room), +4 Water channel opened, +8 Gearwheel turned, +16 Sacred and Minotaur beaten, +32 Sealed one in the arc freed. |
| Byte        | 492         | Missile Base self-destruct and ID card flags. Bits 1, 2, 4 and 8 record the chosen countdown (10, 20, 30 or 40 minutes); the higher bits track the control room exit door, the missile-fired scene and the wounded soldier. Bits: +1 10-minute countdown chosen, +2 20-minute countdown chosen, +4 30-minute countdown chosen, +8 40-minute countdown chosen, +16 Control room exit door opened, +32 Missile-fired scene played, +64 ID Card taken from soldier, +128 Wounded soldier talked to. |
| Byte        | 493         | Set to 15 when the Missile Base self-destruct countdown starts; maps combine it with the countdown bits of the previous variable to tell that a timer is running and blow the base when it ends. Values: 0 = No countdown running, 15 = Countdown running. |
| Byte        | 494-527     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 528         | Progress counter reused by separate story segments: Dollet exam (2-12), first Laguna patrol dream (500-510), Timber missions (100-206), Laguna in the Esthar lab (1000-1120), White SeeD ship (700-740). Each segment overwrites the last. Values: 2 = Dollet: first stair in town gate climbed, Seifer moves up, 4 = Dollet: second stair, Seifer moves up, 6 = Dollet: third stair, waiting at the top, 8 = Dollet: Seifer has run off from the Central Square, 12 = Dollet: Selphie has joined on the mountain path, 100 = Timber: arrived at the Forest Owls' train, 102 = Timber: Rinoa reunion done, she joins, 104 = Timber: Rinoa has met Zell and Selphie, everyone leaves for the strategy talk next door, 108 = Timber: abduction plan explained, 112 = Timber: party chosen, ready; Watts starts the plan when asked, 128 = Abduction: jumped from the roof onto the president's car, 132 = Abduction: first set of cars uncoupled, 150 = Abduction: moved to the train after Watts says go, and again when plan succeeds; rank change given back at base, 154 = Timber: before going to the fake president, 170 = Timber: fake president beaten, plan failed; Squall explains the Dollet tower at base, 172 = Timber: Cid's contract letter read, 174 = Timber: free to go to the TV station, 178 = Timber: Rinoa has gone ahead, train leaves, 180 = Timber: soldiers fought in town, Buel Card from them, 182 = Timber pub: entry scene done, the Drifter complains about the resistance and Rinoa snaps at him, 184 = Timber pub: the Drifter has been moved aside, back alley opens, 190 = Escape 1: out of the TV station, 192 = Escape 2: back alley, 194 = Escape 3: pub, 196 = Escape 4: town street (titown52), 198 = Escape 5: town street (titown51), 200 = Escape 6: talked to Quistis in the house (timin22), 202 = Escape 7: house (timin21), Remedy received, 204 = Escape 8: Watts comes, 206 = Escape 9: Zone comes; go to the station, 500 = Laguna patrol: arrived, 'bad feeling' talk done (cdfield1), 510 = Laguna patrol: Esthar soldier ambush fought (cdfield2), 700 = White SeeD ship: boarded, leader sends you off, 710 = White SeeD ship: met Watts and Zone, 730 = White SeeD ship: Edea's letter given, leader's story told, 740 = White SeeD ship: left the ship, 1000 = Esthar lab: Kiros and Ward sent to Lunatic Pandora, Laguna stays to work, 1001 = Esthar lab: "It's only been 3 days" scolding done, second work scene next, 1002 = Esthar lab: Laguna stood up for the Moomba at meal time (passing, no control), 1004 = Esthar lab: guards gone, free to walk around while working, 1010 = Esthar lab: talked to the Moomba, 1012 = Esthar lab: heard Dr. Odine's failed experiment upstairs, the other worker comments, 1014 = Esthar lab: Moomba rescue and worker's resistance offer done, guard fought; Kiros and Ward arrive, 1020 = Esthar lab: second fight won, 1030 = Esthar lab: overheard Dr. Odine upstairs, 1050 = Esthar lab: told about Ellone by Odine's assistant, 1060 = Esthar lab: nobody in the lab now, fight line on, 1100 = Esthar lab: third fight won, 1120 = Esthar lab: asked Odine about Ellone, go to her. |
| Byte        | 530         | Dollet exam flags. The SeeD rank screen gives +150 for bit 64 unless bit 128 is set. Bit 64 is set by beating the crab (X-ATM092) and also by the pub shortcut, which lets it pass. Bit 8 is tested but never set. Bits: +2 Seifer and the soldier on the mountain path scene seen, +4 Tower lift has arrived; cleared when boarding so arrival plays again, +16 Came back in from the mountain side; tower door scene plays once, then cleared, +32 Squall jumped off the cliff; Selphie comments when you meet her, +64 Crab out of the chase (beaten, or passed at the pub), +128 Let the crab pass by through the pub: no +150, crab shows up on the beach instead. |
| Byte        | 531         | Read only at the Dollet seaside, where a value of 1 changes the opening scene. Only the debug rooms ever set it, so in normal play it stays 0. Values: 0 = Normal, 1 = Alternate seaside opening (debug only). |
| Byte        | 532         | Footstep sound in Dollet's gate area and beach: 0 sand, 1 normal. Lines across dogate_1 switch it as you cross, and the save point and the town set it to 1. Only dogate_1 reads it, to restore the sound on entry. Values: 0 = Sand footsteps, 1 = Normal footsteps. |
| Byte        | 533         | Dollet revisit flags: the road guard, the pub owner's cards, the hotel clerk and the painter's grandfather. Bit 64 flips with the bone treasure hunt and says where the grandfather is. Bits: +2 Squall forced past the road guard; cleared when he returns and the guard wakes, +4 Road guard's leg cramp chance has come up (only once), +8 Pub owner beaten at cards; upstairs room opens, he moves there, +16 Pub owner gave the prize: 5 Geezard, 4 Red Bat, 3 Buel, 2 Anacondaur, 1 Cactuar cards, +32 Hotel clerk uses her accent ('y'all'): told it is just an accent; cleared if you say it sounds strange, +64 Grandfather is at the beach, not home, +128 Squall said 'There used to be a dog here...' in the town. |
| Byte        | 534         | Dollet bone treasure hunt. Each painting shows a dog's spot with a bone; digging gives the next painting. Items become the better one from story 900. Bits 1 and 128 are separate: a boy who runs off, and the guard on the mountain road. Bits: +1 Boy in the street has run off (dotown1a), +2 Saw painting 1: dog appears at the Central Square, +4 Dug at the Central Square: Potion (X-Potion late), +8 Saw painting 2: dog moves to the town street by the pub, +16 Dug there: Phoenix Down (Mega-Potion late), +32 Saw painting 3: dog moves to the street by the painter, +64 Dug in town: Soft (Elixir late); the boy gives up pranks, +128 Beat the two robots and chased off the Galbadian on the mountain road (domt5_1). |
| Byte        | 535         | Timber flags: Watts's password, the TV station party, the journalist boy and whether disguised Watts still waits on the street during the escape. Bit 2 only holds while the Dollet tower talk plays. Bits: +1 Gave Watts a wrong password reply; he then meets you differently, +2 Dollet tower talk with Zone in progress (off again on return), +4 Fought the Galbadian guards at the Timber gate; they are gone, +8 Soldiers' talk in the town (titown2) seen, +16 Zell is with Squall at the TV station, not Selphie, +32 Told the boy not to give up on journalism, +64 Boy gave the Pet Nametag, +128 Disguised Watts is not due on the street (titown51): on when the escape reaches the town, off in the house so he can come, on again after his talk or on leaving Timber. |
| Byte        | 536         | One-time flags from Timber plus one magazine from Dollet's pub. Bits 8 and 16 are set but nothing reads them. Bits: +1 Big Brother's speech heard in the back alley; boys and draw point appear there, +2 First scene in the house (timin22) during the escape, +4 Helped the girl who fell on the Timber bridge; she thanks you at the hotel and the boy mopes, +8 Told Watts 'You be careful, too' at the farewell; nothing reads it, +16 Took the last train out of Timber; nothing reads it, +32 Took 500 Gil 'secret savings' from the cupboard (timin1), +64 Took Pet Pals Vol. 2 (tiagit4), +128 Took Occult Fan II (dopub_3). |
| Byte        | 537         | Laguna's Centra excavation escape: Old Keys and traps. Each finished trap (4, 16, 64, 128) removes one soldier fight at the exit; a fifth fight always happens. Red switch needs the blue boulder not fired yet. Bits: +1 Lost the Old Key found in ebexit1; path in ebroad6 opens (Combat King 005), +2 Lost the Old Key found in ebexit2; path in ebroad7 opens (LuvLuv G), +4 Hatch trap set: tampered lever 1 and crossed; the shutter to an empty room below is gone (ebroad12), +8 Red switch pressed, far boulder falling; cleared on return, +16 Far (small) boulder has fallen, +32 Blue switch pressed, near boulder falling; cleared on return, +64 Near (large) boulder has fallen, +128 Pushed the boulder about to fall on the soldiers (ebroad41). |
| Byte        | 538         | Mixed one-time flags: Laguna's first patrol and Centra excavation (hatch levers, detonator) and the Esthar lab. Tampering with lever 2 springs its hatch on soldiers in the red boulder chase and opens the way to the Phoenix Pinion below. Bits: +1 Leg cramp scene seen (cdfield3), +2 Hatch lever 1 explained ('The lever on the hatch is loose'); not the tampering, +4 Detonator explained (ebroad31), +8 Hatch lever 2 tampered with, +16 Hatch 2 sprung during the red boulder chase; the shutter to the Phoenix Pinion room below is gone (ebroad12), +32 Went down or up the cdfield ladder; 'It's a ladder' not repeated, +64 Esthar lab: talked with the assistant about Ellone (edview1), +128 Took Weapons Monthly, First Issue (edlabo1). |
| Byte        | 539         | Mixed flags: Laguna's excavation hatch 3, the White SeeD ship, and the Adel sealing flashback, where bits 1 and 2 hold the part reached and are cleared before the Sealing movie. Bits: +1 Adel flashback: Esthar lab part done (temporary), +2 Adel flashback: lab view part done (temporary), +8 Hatch lever 3 tampered with, +16 Hatch 3 sprung during the blue boulder chase; the shutter to the Power Generator room below is gone (ebroad12), +32 Gave Zone 'The Girl Next Door' (free: Rename Card and Shiva Card; or for 25,500 Gil); refusing leaves it clear, +64 Watts told you Ellone left with Esthar soldiers, +128 White SeeD's 'meat' joke heard. |
| Byte        | 540-591     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 592         | Stage of the three SeeD train rides in the bvtr maps. Below 100 is the ride to Timber, 100 the ride to East Academy, 102 up the ride to Deling. Read as a word it adds 256 once byte 593 is set on the Ragnarok; that part is not this flag. Values: 0 = Before any ride, 2 = Timber ride: corridor talk done ("This train is awesome!", Zell shows the ticket door, Selphie heads for the front), 4 = Timber ride: Zell runs into the SeeD cabin, 6 = Timber ride: Zell's Timber talk under way, 22 = Timber ride: asleep, Laguna's first dream starts (story 22 set too), 24 = Timber ride: awake, arrival announcement, 28 = Not held in play: overwritten at once; Selphie's door scene that also sets it is in a car nothing leads to, 50 = Timber ride over: after the arrival announcement Squall walks out and the ride ends at Timber station, 100 = East Academy ride: reached the SeeD cabin (story 290), 102 = Deling ride: Zell asks 'what do we do about HIM?', 104 = Deling ride: Irvine has left the cabin after flirting, 106 = Deling ride: after the dream, 'no damage to the train'. |
| Byte        | 594         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 595         | Tells the next map how the party is arriving by lift, so it plays the ride. In Fisherman's Horizon it covers the lift between the bridge and the roof; the Master Fisherman's send-off at the docks also uses it. In the Deep Sea tower it covers the lift between levels 5 and 6. Values: 1 = No ride pending (arrival finished), 2 = Riding down to the FH bridge, 4 = Riding up to the FH roof, 8 = Riding the lift between Deep Sea levels 5 and 6. |
| Byte        | 596         | Set to 1 after Quistis has explained the GF junction tutorial at the Balamb Garden gate, so the explanation is not repeated. Values: 1 = Junction tutorial shown. |
| Byte        | 597         | Set to 1 when the party pays at the Fisherman's Horizon hotel counter and goes to sleep, and back to 0 when Squall wakes in the room. Values: 0 = Not resting, 1 = Resting at hotel. |
| Byte        | 598         | Fisherman's Horizon side story at the docks. It follows the viewpoint movie, the Fisherkid's disastrous casts at the Shopkeeper's stall, then the Master Fisherman's invitation to the inn. At 128 the draw point at his fishing spot appears; at 1 after a refusal he is gone for good. Values: 1 = Arrived on the deck, or refused the Master Fisherman at the inn, 2 = Viewpoint movie seen; Fisherkid's first cast is next, 4 = Fisherkid's cast broke the shop window, 8 = Fisherkid's next cast smashed up the shop, 16 = Fisherkid's hook caught the Shopkeeper, 32 = Fisherkid finally got his cast right, 64 = Master Fisherman invited Squall to the inn, 128 = Accepted at the inn; Master Fisherman says 'Follow me'. |
| Byte        | 599         | Two unrelated uses. In Fisherman's Horizon it records talks with the lift brothers. In the Chocobo Forests it records the first catch: entering a forest with no forest started sets 32, and riding the chocobo out plays Chocoboy's 'first catch' scene and sets 64. A forest entered first stops the lift talks; a first forest entered later overwrites them. Values: 1 = Rode the roof lift and heard its operator's Esthar chat, 2 = Bottom lift operator said 'Don't we look alike?', 32 = First Chocobo Forest entered; no chocobo ridden out yet, 64 = Rode out on the first chocobo; Chocoboy's congratulations seen. |
| Byte        | 600         | Fisherman's Horizon sequence while the Garden is repaired, with Irvine and the technicians. Until the roof scenes reach 8 the roof lift refuses to run ('Hold on a sec...'). It then follows Irvine's reaction on deck 6 and his scene back in town. Values: 1 = Rode the lift up for the first time, 2 = Reached the roof; Irvine reports the technicians are in the Garden, 4 = Irvine asked Squall about getting things fixed, 8 = Roof scenes done; lift works again, 16 = Irvine's reaction to the machinery on deck 6, 32 = Irvine's 'What the...?' scene in town. |
| Byte        | 601         | Master Fisherman's tour of Fisherman's Horizon after accepting at the inn, up to his send-off with a Megalixir. Later Kazu's talks with Irvine and the Fisherkid's practice overwrite it. Any value above 0 puts the Master Fisherman in Shumi Village; at 16 or more he also adds lines about the name FH there. Values: 1 = Accepted; Master Fisherman says 'Follow me', 2 = He left the inn room; town walk is next, 4 = Town walk done; he heads for the shop, 8 = He met the Shopkeeper at the docks, 16 = Shopkeeper told the 'Engineer' story, 32 = Kazu questioned Irvine on the bridge, 64 = Kazu told Irvine he is going to do something, 128 = Squall told the Fisherkid 'You've gotten better'. |
| Byte        | 602         | Deep Sea tower level 3: the room variant, set from the Reserve Steam Pressure on arrival (12, 14 or 15). Only the 14 variant allows the Steam Room; once level 4 is entered, it reports an over-flow instead. The reset at level 1 returns it to 1. Values: 1 = Reset at level 1; variant chosen on next arrival, 2 = Arrived with pressure 12, 4 = Arrived with pressure 14; Steam Room can be opened, 8 = Arrived with pressure 15, 16 = Steam Room door opened (4 pressure spent), 32 = Steam Room refill used (+7 pressure). |
| Byte        | 603         | Deep Sea tower level 4: the room variant, set from the Reserve Steam Pressure on arrival. Any value of 2 or more also means level 4 has been reached, which closes the Steam Room. With pressure 10 or 13 at level 5, this decides whether that terminal spends 2 or 1. Values: 1 = Reset at level 1; variant chosen on next arrival, 2 = Arrived with pressure 8, without opening the Steam Room, 4 = Arrived with pressure 10, 12 or 15, 8 = Arrived with pressure 11, 13, 14 or 16. |
| Byte        | 604         | Deep Sea tower level 5: the room variant, set from the Reserve Steam Pressure on arrival and, at pressure 10 or 13, from level 4's variant. Any value of 2 or more means level 5 has been reached, which changes how level 4 looks on the way back. Values: 1 = Reset at level 1; variant chosen on next arrival, 2 = Arrived with pressure 4, 4 = Arrived with pressure 6 or 8, or 10 or 13 with level 4 at 4, 8 = Arrived with pressure 7, 9, 11, 12, 14 or 15, or 10 or 13 with level 4 at 8. |
| Byte        | 605         | Progress at the bottom of the Deep Sea tower. The door to the ocean deposit opens either by paying 4 pressure or by letting Zell force it, which keeps the pressure but adds battles in the ruins. It ends with the operation at the ruins and the final battle; from 32 on, encounters there are off. Values: 1 = Level 1 reset done, 2 = Zell forced the door; line-triggered battles in the ruins, 4 = Door opened with 4 steam pressure, 8 = Operation at the ruins confirmed (10 or more pressure), 16 = Excavation scene played; final battle next, 32 = Final battle won. |
| Byte        | 606         | One-time gift flags, one bit per gift, in Fisherman's Horizon and once in Shumi Village. The Occult Fan III write replaces the whole byte, but it comes before every other gift. Having the Megalixir also adds Irvine's 'not the Mega type' line when Grease Monkey gives the Phoenix Down. Bits: +1 Master Fisherman gave Occult Fan III, +2 Master Fisherman gave a Megalixir, +4 Grease Monkey gave a Mega Phoenix, +8 Grease Monkey gave a Phoenix Down, +16 Galbadian Officer gave 5 Fast, 5 AP and 5 Pulse Ammo, +64 Shumi Elder gave a Status Guard. |
| Byte        | 607         | Finishing the Laguna statue in Shumi Village: the Attendant starts work, the Elder and Attendant say one more craftsman is needed, Grease Monkey's Moomba doll wins over Artisan, and the statue is finished when the party returns to the village late in the game (story above 3100). Values: 1 = Attendant agreed and has started helping, 2 = Elder explained the Attendant's wish; one more helper needed, 4 = Attendant named Artisan; Squall must win him over, 8 = Grease Monkey gave the Moomba doll, 16 = Artisan heard Grease Monkey's message from the doll, 32 = Artisan agreed at the pond, 64 = Statue finished, 128 = Attendant says it can be shown to the Elder. |
| Byte        | 608         | Squall's dealings with the Sculptor and the Elder in Shumi Village, up to the Elder's reward. Refusing the Sculptor's request sets 16, and he can be asked again. Before 2 the Moomba blocks the way at the village entrance. Values: 1 = Saw the Laguna statue in the workshop, 2 = Sculptor's Moomba speech; told to go see the Elder, 4 = Elder's welcome scene seen, 8 = Elder gave the assignment to help finish the statue, 16 = Refused the Sculptor's request for now, 32 = Agreed; stone search under way, 64 = Stone search complete, 128 = Elder gave the Phoenix Pinion. |
| Byte        | 609         | Two stages in Shumi Village. Values 1, 2 and 4 mark the first arrival: the sand pit, the elevator and the hotel. From 8 on it is the stone the Sculptor is asking for, which also sets the Specialist's hint and which stone can be picked up. While at 4 or less, he is asking for the blue or wind stone. Values: 1 = First arrival in the sand pit, 2 = First elevator ride done, 4 = First hotel scene done; asking for blue, then wind, 8 = Asking for the life stone, 16 = Asking for the shadow stone, 32 = Asking for the water stone, 64 = Pond stone refused; water stone still needed, 128 = All stones delivered. |
| Byte        | 610         | Shumi Village stone search: the stone Squall has just found and takes to the Sculptor, who checks it against his request. Values: 1 = Blue stone, 2 = Wind stone, 4 = Life stone, 8 = Shadow stone, 16 = Stone by the pond (wrong one), 32 = Water stone from Artisan's house, 64 = Job complete; stones not needed, 128 = Sculptor explained the stones' purpose. |
| Byte        | 611         | Short-term 'already said it' flag reused by several scenes. For the stones, 0 means a new stone hasn't been shown to the Sculptor and 1 means he has commented. It also marks the Specialist's first greeting and Kazu's first talk with Irvine in Fisherman's Horizon. Nothing long-term depends on it. Values: 0 = Next line not played yet, 1 = Line already played. |
| Byte        | 612         | Shumi Village story of the Elder's Attendant after the Phoenix Pinion: the Elder orders him to help with the statue, he refuses to work seriously, and the Moomba outside is sent to make him. At 128 the Attendant is really working, and var 607 takes over. Values: 1 = Phoenix Pinion received with Zell, Irvine, Quistis, Rinoa or Selphie in the party; they talk outside about the Elder, 2 = The cry from the Elder's house is due, after 'Explain' and the Elder's order to the Attendant. It would also follow the reward with none of the five in the party, which a normal game can't reach, 4 = 'NNNNOOOOOO!!!' heard from the Elder's house, or 'why bother' chosen in the talk, 8 = Left through the sand pit; Attendant now assigned, 16 = Attendant complains about the 'silly statue', 32 = Elder asks Squall to get the Moomba outside, 64 = Moomba outside has been talked to, 128 = Attendant is working on the statue. |
| Byte        | 613         | Fisherman's Horizon repair shop events, plus Artisan's first talk in Shumi Village. Walking out on the Galbadian Officer, twice, sets the first two flags and leads to Grease Monkey's gifts. Hearing Artisan out sets the third, and the doll scene that follows is what lets Grease Monkey hand it over. Bits: +1 Left the shop during the officer's first confrontation (story 655), +2 Left the shop during the second confrontation, +4 Heard Artisan's talk about the artisans in Shumi Village, +8 Moomba doll reacted in the repair shop; Grease Monkey explained. |
| Byte        | 614         | One progress line through the Deep Sea Research Center. On the island (Zell's 'Battleship Island') it tracks arrival, the core and beating Bahamut. In the tower it records the last terminal used, each one opening the way down; a terminal only works at the value before it. The level 1 reset returns it to 8. Values: 1 = Arrived on the island, 2 = Reached the core; 'The blue light leads all to death', 4 = Bahamut beaten; tower not started, 8 = Level 1 terminal used; door to level 2 open, 16 = Level 2 terminal used; door to level 3 open, 32 = Level 3 terminal used; door to level 4 open, 64 = Level 4 terminal used; door to level 5 open, 128 = Level 5 terminal used; door to level 6 open. |
| Byte        | 615         | Reserve Steam Pressure left in the Deep Sea Research Center puzzle, from 0 to 20. Each terminal subtracts the amount the player picks and the Steam Room adds some back. |
| Byte        | 616         | State of Chocobo Forest 1 (Beginner level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Aura Stone) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 617         | State of Chocobo Forest 2 (Beginner level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Flare Stone) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 618         | State of Chocobo Forest 3 (Intermediate level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Shell Stone and Holy Stone) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 619         | Chocobo holy ground, the seventh forest. Once all six other forests are cleared, crossing into the clearing plays the gathering of chocobos, and a chicobo then gives the Chocobo Card. After that, Chocoboy offers his last 'Help me' and is gone on the next visit. Values: 2 = Chocoboy's first talk here, 32 = All six forests cleared; gathering not yet seen, 64 = Gathering scene played, 128 = Chocobo Card received. |
| Byte        | 620         | State of Chocobo Forest 5 (Expert level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Meteor, Holy and Ultima Stones) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 621         | State of Chocobo Forest 6 (Intermediate level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Protect and Meteor Stones) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 622         | State of Chocobo Forest 7 (Expert level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Meteor, Flare and Ultima Stones) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 623         | Shumi Village scenes after the statue is finished (story 3150 or later for the Elder). The Elder comes to the workshop, thanks the group and asks for a private talk. The party overhears it: he asks if the Attendant wants to go see Laguna, and the Attendant says he shouldn't. At 32 the village settles. Values: 1 = Attendant says the statue is finished, 2 = Elder arrived: 'It's finally finished', 4 = Thanks given; Elder asks to speak in private, 8 = Party goes back to the workshop to overhear, 16 = Private talk seen; the Attendant's wish replays, 32 = Scenes over; village back to normal. |
| Byte        | 624         | Progress of scripted scenes in two story trips plus one subplot: Balamb Town on the SeeD exam day (4 to 18), Trabia Garden (100 to 122) and the pigtail girl's Balamb Hotel scenes (144, 146). Values: 0 = Nothing yet, 2 = Passing state during Irvine's orphanage story at the Trabia court (the script writes 770 here; only the low byte is stored), 4 = Exam day: the car reached the port ("So that's the vessel...?"); the party can walk, 6 = Exam day: the car scene at the town entrance has played and the car is parked there, 8 = Exam day: the driver's complaint at the entrance heard ("Piece of crap!"), 10 = Never set in play; only the debug rooms write it. The car at the Balamb entrance is hidden from 10 up, 12 = Back from Dollet: getting off the boat scene done, 14 = Back from Dollet: Seifer's car has left ("Might as well walk it"), 16 = Back from Dollet: reached the hotel street on foot, 18 = Back from Dollet: passed the hotel street line, town music returns, 100 = Trabia Garden approach scene done, 102 = Trabia front gate arrival done, 106 = Reached the Trabia garage, 108 = Selphie's cemetery scene done, 120 = Basketball court arrival done, 122 = Orphanage memories over, the party leaves the Trabia court, 144 = Pigtail girl: Balamb Hotel room scene done, 146 = Pigtail girl: Balamb Hotel lobby scene done. |
| Byte        | 625         | Balamb Town flags, some reset each time the party arrives in town from outside. They do not mark areas as visited: they track the chase, an inn payment, Zell's room and the hotel owner's slogan. Bits: +1 The Big Bad Rascal chase in the square is over for this visit (you left the square during it), +2 First entry to the square this visit is done; also stops the Garden student's first chat in the port plaza, +4 Balamb Hotel room paid; the rest scene plays in the room, then this clears, +8 Companion's scene in Zell's room seen during the occupation; also set when the town is freed, so it never plays later, +16 Never set in play, +32 Never set in play (would remove the platform travellers), +64 Never set in play, only cleared, +128 Zell's insult gave the hotel owner his slogan ("blow you away"). |
| Byte        | 626         | Balamb Town flags for the mechanic and the Big Bad Rascal. Bits 2, 16, 32 and 128 last one town visit and reset when the party arrives from outside; bits 4, 8 and 64 stay. Bits: +2 Mechanic and his helpers are out at the town entrance this visit (even odds when you arrive by the gate), +4 Zell freed the mechanic's machine and heard "I really need a guy like you"; the mechanic now mentions Zell's mother, +8 New assistant met Zell and called him a legend, +16 The Rascal and his mother chase each other in the square this visit (1 in 4), +32 Rascal's mother complained during the chase; she then only sighs, +64 The man in the square greeted Zell; without Zell he later asks "That rowdy punk Zell isn't here today?", +128 The Rascal is at Zell's house this visit; Ma Dincht says so. |
| Byte        | 627         | Balamb Town flags: where the Big Bad Rascal and the next-door girl are this visit. All reset when the party arrives from outside except bit 64. Bits: +1 Zell and the Rascal greeted each other at the house this visit, +2 Just arrived in town: the next entry to the square rolls where the Rascal is, +4 Next door this visit: a visitor sits with the girl (1 in 3), +8 Next door this visit: the girl is out drawing on the hotel street (1 in 3), +16 This visit the Rascal runs through the hotel street, +32 This visit the Rascal and his mother are in the port plaza, +64 The Rascal's mother caught him in the port plaza. Permanent; this unlocks the Spd Up in Zell's room, +128 The Rascal has already run through the hotel street this visit. |
| Byte        | 628         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 629         | Random mask rolled each time the party arrives in Balamb Town from outside. It decides who is out in the port plaza this visit; each bit has a 3 in 4 chance. Bits: +1 Garden student on the plaza bench, +2 Rolled but nothing reads it, +4 Townsperson gossiping in the plaza, +8 Dog owner and dog in the plaza. |
| Byte        | 630         | Big Bad Rascal flags, plus one station passer-by. Bits 8 and 16 stay for good, recording his pranks; the rest reset when the party arrives from outside. Bits: +1 The Rascal scared the girl on the hotel street this visit (she says "I hate him"); makes that scene rarer, +2 The Rascal's mother is at Zell's house this visit and he behaves upstairs, +4 Her talk with Zell played; nothing reads this, +8 He told Zell about the frog; the frog is now in the house, +16 He told Zell about signing the painting; the signature can now be read, +32 Never set in play (would give his "Top Secret" line), +64 He has told today's prank this visit, +128 The businessman has already walked through the station this visit. |
| Byte        | 631         | Flags for Balamb Hotel guests, the station photographer, the fish cook and one Garden library scene with Ellone. Bits: +1 Photographer is at the station this visit (even odds; resets on arrival), +2 Never set in play, +4 Ellone's library scene ("You're my only hope") played, +8 Galbadian guest is at the hotel (1 in 3); clears when you rest, +16 That guest has left for good, once you walk back to the square, +32 Never set in play, +64 Never set in play, +128 With Selphie in the party, the fish cook heard her dessert idea and now plans a Badamb fish cake. |
| Byte        | 632         | Flags rolled per visit: Balamb Town NPCs (reset when arriving from outside) and two Garden library students (rerolled on entering the library). Bits: +2 This visit the Galbadian guest is not at the hotel, +4 Picks which of two routines the port plaza dog owner and dog use this visit, +8 The dog owner's walk-on already played this visit, +16 Library: first of two students is out (even odds), +32 Library: second of two students is out, +128 The girl is drawing on the hotel street this visit. |
| Byte        | 633         | Mixed event flags: the Balamb harbor draw point, Zell's room, the Garden library and the Trabia Garden approach. Bits: +1 Took the extra Gil at the harbor draw point this visit (needs the soldier to have dropped his Gil); resets on arrival, +2 Ellone's first library meeting ("Hi", "Try to remember") played, +4 Spd Up taken in Zell's room, +8 Library: conceited SeeD and committee group are out (rerolled on entry), +16 Library: other committee layout (rerolled on entry), +32 Conceited SeeD spoke to the committee member ("He spoke to me!!!"); resets on entry, +64 Selphie was in your party and ran ahead into Trabia Garden; otherwise the party just says she ran off, +128 Hyne's legend told next door; early in the story it resets on arrival. |
| Word        | 634         | Main story progress when the pigtail library girl subplot last moved on. Her next scene with Zell stays locked until the story has passed this value. |
| Byte        | 636         | Times the Winhill chocobo has been pushed. After the first push it no longer sits on the vase piece, so the piece can be taken. The fifth push makes it run off: the value jumps to 6 and a second chocobo takes over. Values: 0 = Not pushed; the vase piece is out of reach, 1 = Pushed once, 2 = Pushed twice, 3 = Pushed three times, 4 = Pushed four times, 6 = Fifth push: the chocobo has run off. |
| Byte        | 637         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 638         | Steps of the scene with NORG in the Master's Room, which alternates between two views. It jumps by uneven amounts, from the arrival through Squall's report to the battle and what follows. Values: 0 = Not started, 4 = NORG: '3-SECONDS-ARE-UP'; arrival played, 6 = NORG revealed, 8 = NORG asks for the report, 10 = 'YOU-WERE-FOOLED!' report done, 16 = Faculty explain the Galbadia deal, 18 = 'QUIT-YOUR-WHINING!' exchange played, 26 = NORG on Cid and Edea played, 28 = NORG attacks, 30 = Scene after the NORG battle. |
| Byte        | 639         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 640         | Trabia Garden approach: a bit is set for each of the four SeeDs who is not in Squall's party and so stands waiting at the front gate and on the basketball court. Bits: +1 Zell waits, +2 Quistis waits, +4 Rinoa waits, +8 Irvine waits. |
| Byte        | 641         | Trabia Garden encounters, plus the occupied Balamb gate. Bits 1, 2 and 128 each raise the chance that the tech squad's computer brings up Selphie's personal data when she is not in the party. Bits: +1 Student woke the dreamer in the garage ("Fight yourself back to reality!"); raises the chance by 60, +2 Patrol Squad complained about his late relief at the front gate; raises it by 70, +4 Occupied gate soldier told you the town is under Edea, +8 Zell got past the gate soldier by claiming news of Ellone, +16 You answered the Trabia donation drive; she leaves the gate, +32 Selphie comforted the children about Mr. Bear in the garage, +64 Entered the stage from the garage; nothing reads this, +128 You answered "Good luck" to the donation drive; raises the chance by 50. |
| Byte        | 642         | Occupied Balamb Town scenes at Zell's house and the station, and two Trabia Garden events that nothing reads afterwards. The bit the town entry clears (32) is never set. Bits: +1 Answered "I think so" when the Trabia girl asks if you like Selphie; nothing reads this, +2 Weapons Monthly, August Issue taken at Trabia gate; nothing reads this, +8 The station soldier has gone through to the platform, +16 That soldier has come back and left; the kitchen scene also sets this, +32 Never set in play, +64 Zell's reunion with Ma Dincht upstairs seen, +128 The Rascal showed his special move and left "to check things out". |
| Byte        | 643         | Zell's home and the occupied town, with one Timber train flag and one library flag. Bits: +1 Occupied town: "Ma, I'm home!" entry scene at Zell's house, +2 First boarding of the Timber train done. That ride runs a short stretch, then cuts to the SeeD cabin. Later boardings ride the whole line to Timber station, +4 Zell's first homecoming scene in the free town done; the town's liberation sets it too, +8 Hotel soldiers told you to find the captain; this starts the hunt, +16 Occupied town: the next-door girl cried "I can't take it anymore", +64 The square's townsperson has been placed at her first spot, +128 Pigtail girl's first stage is over (from the Dollet return on, or once she recited the rules). |
| Byte        | 644         | Occupied Balamb Town hunt clues, the Garden student at the port and two library layout bits. Bits: +1 Garden student at the port told you he has nowhere to go (after the Garden left), +2 Never set in play, only cleared, +4 Library: teacher in the back room (rerolled on entry, with bit 16), +8 Rinoa's first look around the library played, +16 Library: back room layout A (rerolled on entry), +32 The harbor soldier dropped his Gil in the sea; the harbor draw point now also gives Gil, +64 The Rascal came to the next-door girl; next the gate distraction can play, +128 Harbor soldier told you the captain went fishing. |
| Byte        | 645         | Zell's answers to the library love-compatibility quiz: bits 1, 2 and 4 hold the colour he picked and bits 8, 16 and 32 the food. The library girls and the compatibility book read them back. Bits: +1 Colour: red, +2 Colour: blue, +4 Colour: pink, +8 Food: beef, +16 Food: fish, +32 Food: hot dogs. |
| Byte        | 646         | Occupied Balamb Town captain hunt: kitchen and fish route, tabloid guy's paid tips, and the search dog. Bits: +1 The fish smoke scene at Zell's house has started; the platform soldiers are now poisoned, +2 The Rascal distracted the gate guard and told the hotel owner his daughter is safe, +4 Paid the tabloid guy 30,000 Gil: captain went fishing at the harbor, +8 Station Staff explained the poison was Badamb fish; the townsperson now says the captain went into the station, +16 Paid the tabloid guy again: think of where you could cook the fish, +32 Harbor soldier's line by the dog heard; nothing reads this, +64 After Ma's reunion and the fishing clue you came back to the square from elsewhere: the captain now cooks while you are away, +128 The search dog is running and the chase is on. |
| Byte        | 647         | Times the party has walked from the square into the occupied hotel street, up to 8. It is the hunt's real time limit. From 3 the hotel soldiers change their talk; at 8 the kitchen route closes, the dog handler goes off shift, and talking to both soldiers forces the Raijin fight. |
| Byte        | 648         | How the search for Raijin ended in occupied Balamb Town, the state of the dog chase, and the fight at the hotel. The route picks your SeeD level gain before the Fujin battle. Bits: +1 The dog reached the platform and drove Raijin out; meet him at the hotel. Clears after that fight, +2 Beat Raijin after the dog route; 100 SeeD level gain, +4 Fujin scene at the hotel reached; nothing reads this, +8 Beat Raijin after finding him on the train; 60 SeeD level gain, +32 The chase countdown has ended or was never started, +64 Dog chase running: the menu is locked until it is wrapped up, +128 Never set in play. |
| Byte        | 649         | Occupied Balamb Town story flags: the gate, Zell's house and the hunt. Bits: +1 Walked past the gate soldier into town, +2 The party reeks of the fish after the smoke scene; a townsperson says so, and the search dog can now be chased. Clears when the time limit hits, +4 Zell gave in: "Let's just go to my room and rest." The stairs open. His "It's sacred" line sets nothing, +16 Found Raijin in the freight train, +32 Hotel soldiers' second talk heard; nothing reads this, +64 Time ran out: Raijin forced into a fight (40 SeeD level gain), +128 The platform officer gave his orders and left; the fish scene also sets this. Soldiers are only poisoned with 646 bit 1. |
| Byte        | 650-655     | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Word        | 656         | Length in seconds (200) of the countdown timer for the Raijin hunt in occupied Balamb Town. It is set when the harbor map is entered and loaded into the timer when the player talks to the soldier with the search dog. |
| Byte        | 658         | Seconds used on the search dog chase (200 at the start minus the time left), recomputed on entering each occupied Balamb map. Each map has a limit: harbor path 35, hotel street 55, square 95, station 125. Over it, or out of order, the chase ends. |
| Byte        | 659         | Stages of the pigtail library girl's crush on Zell, set as each scene plays. The Garden library copies them into 660 on your next entry. Bits: +1 She recited the library rules at the counter, +2 Zell asked her about "Good-bye Pururun", +4 The Conceited SeeD talks to the committee member (Zell not in party); magazine scene and card option follow, +8 Never set in play; 660 bit 8 is set directly, +16 "Let's Find Out More About Zell" committee quiz stopped Zell in the library, +32 The fortune book scene: "You began to understand her feelings!", +64 She gave Zell a book in the Balamb Hotel lobby, +128 Never set in play. |
| Byte        | 660         | Stages of the pigtail girl subplot as recorded, which decide her next scene. On library entry the highest stage of 659 is copied here and the story moment noted, so the next scene needs later story. Bit 8 and bit 64 are set directly. Bits: +1 Counter stage over; also set automatically once back from Dollet, +2 Good-bye Pururun stage recorded, +4 Conceited SeeD stage recorded, +8 Without Zell, she asked "How is... Zell doing...?" in the back room; adds a line at the hotel, +16 Zell quiz stage recorded, +32 Fortune book stage recorded, +64 Combat King 003 taken at the Balamb Hotel; ends the subplot, +128 Never set in play. |
| Byte        | 661         | One-time and per-visit flags shared by unrelated places: Garden library, Master Room, Balamb station, Winhill and Trabia Garden. Bits: +1 Library: back room layout B (rerolled on entry), +2 Occult Fan I taken (Garden library), +4 The villager at the Winhill crossroads went home as you came near; resets on arriving at Winhill, +8 Never set in play, only cleared, +16 Headmaster scene seen at the Master Room ("Please! Listen to me!"), +32 Timber train ticket bought for 3,000 Gil; clears when you board or next arrive in town, +64 Heard the voice in the Winhill mansion ("I'm looking for my feet...") with Quistis or Irvine in the party, +128 Weapons Monthly, August Issue taken (Trabia Garden gate). |
| Byte        | 662         | Winhill flags for the mansion's ghost story, the inn and Raine's house, which unlock each other in turn. Bits: +1 The armor in the mansion fell apart; the vase piece there can now be found, +2 Paid 100 Gil at the inn; clears on reaching the room, +4 The rich man told you his vase is missing, +8 The woman upstairs at Raine's house said spirits lurk in these walls, +16 The cat upstairs talked ("Cyats cyan tyalk, too"), +32 She mentioned the white flowers downstairs; the ghost and cat appear there, +64 Second look at the flowers ("What is that...?"), +128 She first threw you out ("Who do you think you are?"). |
| Byte        | 663         | Winhill vase quest and Raine's house. Four bits are the vase pieces; finding all four and telling the rich man gives the Holy Stone. Bit 4 is a library flag. Bits: +1 Vase piece from the cat at Raine's house, +2 Saw the ghost among the flowers at Raine's house ("Raine...?"); the cat appears and the woman upstairs changes her talk, +4 Rinoa is looking around the Garden library until you leave, +8 Vase piece from behind the fallen armor, +16 Vase piece in the village, once the chocobo moved, +32 Vase piece in the flower field, +64 Answered yes to "Do you like flowers?"; opens the flower field piece, +128 Rich man will say "You found some more!"; only the cat's and the armor's pieces set it. |
| Byte        | 664         | Used in two places. In occupied Balamb Town it records which of the tabloid man's paid tips has been bought. In Winhill it records the rich man's Holy Stone reward and two hidden items. Bits: +1 Holy Stone reward received (Winhill), +2 Bought the 5,000 Gil tip, +4 Bought the 15,000 Gil tip, +8 Bought the 30,000 Gil tip, +16 Left town via the rascal kid's route, +32 Rascal kid distracted guard, +64 Hidden vegetable taken (Winhill), +128 Hidden item taken (Winhill). |
| Byte        | 665         | Pigtail girl and Rascal's mother flags in the free town, plus the occupied town's tabloid guy. Bits: +1 Zell was told a girl with a pigtail was asking for him, +2 Zell asked Ma Dincht about her, +4 The Balamb Hotel room scene played; the lobby scene and Combat King 003 follow, +8 Met the tabloid guy (occupied town), +16 Rascal's mother scolded Zell at his house once; she repeats it once more, +32 The pigtail messenger stands at the town entrance this visit; nothing reads this, +64 The pigtail messenger stands on the platform this visit, so not at the entrance, +128 Reached the occupied hotel street after the soldier dropped his Gil; nothing reads this. |
| Word        | 666         | Number of times the party has walked into the Balamb Garden library from outside. The Love Meter book shows 1 to 5 hearts depending on whether it exceeds 0, 20, 30, 40 or 50. |
| Byte        | 668         | One-time dialogue flags in Balamb Town and Winhill. Bits: +1 Rascal's mother scolded Zell a second time; the scene no longer plays, +2 Ma Dincht told you about the man who cooked fish, +4 Heard the captain once slept behind the car; the new assistant now waits by it, +8 First vase piece given to the rich man (Winhill). |
| Byte        | 669-671     | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Word        | 672         | Story stage from the Fisherman's Horizon tracks to the Esthar City run. 19 runs the 20-minute countdown and 23 ends it, either by time out or by boarding Lunatic Pandora at a Contact Point. 2, 12 and 14 are tested but never set. Values: 0 = Not reached yet, 1 = Squall carrying Rinoa on the FH tracks, 3 = Station at the end of the tracks: Edea's group catches up, 4 = Station: Edea says she must see Dr. Odine, 5 = Station: Selphie and Irvine scouted, 'try East', 6 = Laguna's dream: fight in the magic lab lobby (battle 249), 7 = In the Esthar car to the Presidential Palace, 9 = Palace: meeting with Dr. Odine and the aide, 15 = Zell's party reaches the central platform (ecenter2); lab assistant lets them in, 18 = Zell's party in Dr. Odine's lab, Lunatic Pandora explained, 19 = Outside the lab: countdown of 1201 seconds runs, 23 = Run over: Contact Point boarded or 'MAN! We're not gonna make it!'. |
| Byte        | 674         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 675         | Never set in normal play. The test room's 'Julia and Laguna, Hotel lobby (can drink)' jump sets it to 1, so that talking to Julia no longer ends Laguna's free walk around the Galbadia Hotel lobby. Values: 0 = Normal, 1 = Debug: Julia does not end the scene. |
| Byte        | 676         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 677         | 1 while riding an Esthar City skyway lifter between stops, 0 otherwise. On entering a stop while 1, the game asks whether to get off or keep going. A save cannot normally catch it at 1. Values: 0 = Not riding, 1 = Riding a lifter. |
| Byte        | 678         | Contact Point fights tried in the Esthar City run; each can be tried once. 1st Contact Pt works at about 900-720 seconds left, 2nd at 600-300, 3rd at 180-1. Winning in time boards Lunatic Pandora; fleeing or a late win leaves you on the road. Bits: +1 1st Contact Pt fight started; Zell says 'not gonna miss it this time' at the 2nd, +2 2nd Contact Pt fight started, +4 3rd Contact Pt failed; nothing reads this bit. |
| Byte        | 679         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 680         | A running gag in Esthar City: a man and a woman meant to meet get separated. Talk to him on the skyway and he dashes off; he then runs past on other maps until both end up in the same place. Values: 0 = He is waiting at the skyway (eccway12), 1 = You spoke to him; he ran off, 2 = He ran past at ecopen2, 3 = He got back: both at the skyway, 'This place is so confusing'. |
| Byte        | 681         | Free gifts given once by shops in the Esthar shopping mall (each shop gives two on successive visits), plus the Occult Fan IV magazine from the presidential palace secretary. Bits: +1 Cloud's Shop: Hi-Potion given, +2 Johnny's Shop: Hi-Potion given, +4 Karen's Store: Hi-Potion given, +8 Cloud's Shop: X-Potion given, +16 Johnny's Shop: Mega-Potion given, +32 Karen's Store: Mega Phoenix given, +64 Occult Fan IV taken (palace), +128 Cheryl's Store: Rosetta Stone given. |
| Byte        | 682         | Esthar City NPC flags: the Presidential Aide on break, the woman and the mother on the skyway, and Riki the runaway dog. Bits: +2 Presidential Aide spoken to on break as Squall; the aide leaves the palace meeting room and the secretary with the president's books appears in the hall, +4 Skyway map eccway31 visited: set on every load, so its first-visit branch never runs, +8 Squall's party: woman and mother walked to their spot (eccway11), +16 Zell's party: woman walked off (eccway11), +32 Talked to Riki the dog; he returns to his owner, +64 Owner thanked you; soldier beside him moves. |
| Byte        | 683         | Skyway soldier with the magazine. Talk to him with Squall leading, later with someone else leading: he hands over Combat King 004 and leaves. Skip the Squall talk and he only says he is still reading it, leaves, and you lose the item. Bits: +1 Talked to him with Squall leading, +4 Talked to him with another leader; he walks away for good. |
| Byte        | 684         | Laguna at the magic lab console (emlabo1b). The soldier is fought first. The right panel unlocks the door to Ellone in the lobby below; the other shows an error and Kiros doubts him. You can switch between 2 and 3; only 2 opens the door. Values: 0 = Soldier not fought, 1 = Soldier beaten, 2 = Blue lamp, [Unlocked]: lobby door opens, 3 = Red lamp, error: 'do you know what you're doing?'; door stays shut. |
| Byte        | 685         | One-time placement flags for Esthar City NPCs, mostly: they have done their walk and now stand or are gone. Bit 128 opens the lab: the research assistant lets you in and leaves. Bits 32 and 64 are unused. Bits: +1 ecoway3: aide woman and scientist in their place (forced on when Zell leads), +2 eccway31: soldier finished patrol walk; says he must patrol outside, +4 ecoway3: man's one-time walk done (talked to, or Zell leads), +8 eciway11: soldiers spoken to after 1st Contact Pt passed; they have gone, +16 eccway41: searching soldiers spoken to in the run; they have gone, +128 Research assistant let you into the lab and walked off. |
| Byte        | 686         | Esthar City run comments about Lunatic Pandora, plus Squall's first look at the city. Each bit makes one moment play only once. Bits: +1 Zell: 'Where is it?' 'There it is!' (ecmway1), +2 Zell: 'It's heading for the center!' or 'Man we better hurry', +4 Lunatic Pandora starts across the view at the center (under 720 seconds left), +128 Squall: '(What an incredible city.)', camera pan on first walk into the center. |
| Byte        | 687         | Contact Point window in the Esthar City run: 1 while it is open. The Card button toggles it, and it stays set across maps so the next map reopens it. The window shows the current Contact Point, blinking red while it is active. Values: 0 = Window closed, 1 = Window open. |
| Byte        | 688         | Palace meeting room sofa. The first time Squall sits down both bits are set. The Presidential Aide then has one extra line about Dr. Odine, which clears bit 2. Bit 1 stops the sit scene repeating. Bits: +1 Squall has sat on the sofa, +2 Aide's next talk gives the Odine line. |
| Byte        | 689         | Dr. Odine's lines in his lab during the run ('It will not attack us...') have played, so they play once only. Values: 1 = Scene played. |
| Byte        | 690         | Talk to the bored sentry near the Airstation four times outside the run and he asks for a stand-in. From then on an Eliminator, a card player, stands in that spot unless Squall leads. Values: 1 = Eliminator relieves the sentry. |
| Byte        | 691         | Set to 1 the first time the MD Level 4 maps of Balamb Garden start their special music, so it is not started again. Values: 0 = Music not started yet, 1 = Music already started. |
| Byte        | 692-719     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 720         | Squall's current outfit as shown on the field: it picks his model in every map. The Garden dorm lets the player change between uniforms and street clothes. A debug room also offers a bandage outfit (3). Values: 0 = Own clothes, 1 = Student uniform, 2 = SeeD uniform. |
| Byte        | 721         | Zell's outfit on the field; it picks his model. He is in uniform for the SeeD exam, from the car to Balamb through Dollet, until he's back at the Garden gate; the first mission call also sets own clothes. Value 2 is only reachable from a test room. Values: 0 = Own clothes, 1 = Student uniform, 2 = Test room only: hides him in some maps. |
| Byte        | 722         | Selphie's outfit on the field. Uniform during her tour and at the exam. From story 760, entering the classroom without her in the party gives her a random outfit of the three at her seat; leaving the classroom resets it to own clothes. Values: 0 = Own clothes, 1 = Student uniform, 2 = SeeD uniform (classroom random only). |
| Byte        | 723         | Quistis' outfit on the field. She changes into the dark uniform on the way to Balamb for the SeeD exam and keeps it, unlike Zell and Selphie, until Selphie announces the first mission. Values: 0 = Own clothes (model d018), 1 = Dark uniform (model d020). |
| Word        | 724         | Shared word. Dollet: seconds left on reaching the beach, read for the rank's Conduct: under 180 -100, under 360 -50, under 600 -30, 900+ +10 rising to +80 at 1500+. Timber: Rinoa's plan topic in the briefing, then seconds left in the abduction roof and uncoupling parts. Values: 0 = Briefing: order of events, 1 = Briefing: sensor, 2 = Briefing: uncoupling, 3 = Briefing: everything. |
| Word        | 726         | During the Dollet mission, the number of enemies killed (the kill counter at the end minus its value at the start); the SeeD field exam turns it into the 'Attack' score. In Timber it is reused as a flag set to 1 once Rinoa has explained everything about the plan. |
| Byte        | 728         | Reused many times. In Dollet it counts mistakes during the field exam (+1 to +20 each) and feeds the 'Attitude' score. In Timber it counts abduction-plan attempts. In Deling City it holds a random code number that the Tomb of the Unknown King guard asks for. In disc 3 it holds which character went to space with Squall. Values: 2 = Irvine (space party), 3 = Quistis (space party), 5 = Selphie (space party).<sub>3</sub> |
| Byte        | 729         | During the Dollet mission, the number of battles escaped (counter at the end minus counter at the start), used for the 'Spirit' score of the SeeD field exam. In Deling City it counts the 3,000 Gil hints bought from Caraway's guard (0 to 2). In Timber it counts failures of the abduction plan. Values: 0 = No hint bought (Deling City), 1 = First hint bought (Deling City), 2 = Both hints bought (Deling City). |
| Byte        | 730         | Mixed flags: Garden Festival committee, Selphie's tour, the library reshuffle marker, Dr. Kadowaki's message to Cid, the Tomb of the Unknown King map and location displayer, and the CC Group King event pending after the 4-Suits. Bit 4 is cleared when the tour ends and nothing reads it. Bits: +1 Joined Garden Festival committee, +2 Selphie's tour finished, +4 Tour in progress (never read), +8 Left the library area; its NPCs reroll, +16 Kadowaki asked you to send Cid, +32 Given the Tomb of Unknown King map, +64 Bought the Tomb location displayer, +128 4-Suits beaten, King event still to come. |
| Byte        | 731         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 732         | Seconds left on the Fire Cavern countdown when Ifrit is beaten; read for the rank's Judgment. Under 8 +100, under 30 +80, under 60 +70, under 120 +50, under 180 +30, 600+ -50 falling to -100 at 900+, otherwise 0. |
| Byte        | 734         | Who is with Squall when he gets back to Balamb Garden's front gate from the Disc 2 split (Selphie's group is elsewhere). It decides Cid's orders at FH, Squall's dorm thoughts, Rinoa's tour and who appears at Cid's bedside. Bits: +1 Zell, +2 Irvine, +4 Rinoa, +8 Quistis. |
| Byte        | 735         | Stops on Rinoa's Garden tour (story 571), plus a few markers nothing reads. Each stop plays once. Dr. Kadowaki also waits in the hall until the infirmary stop. Bits: +1 Tour started (never read), +2 Tour: parking lot stop, +4 Tour: cafeteria stop, +8 Quad entered after tour start (never read), +16 Tour: infirmary stop, +32 Tour: training center stop, +64 Library girl's 'try to remember' scene (never read). |
| Byte        | 736-751     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 752         | Remembers where the Ragnarok was entered, so its exit door returns the party there; the exit clears the bit. Bit 8 also makes the cockpit lift use the Lunatic Pandora cockpit. Entering Esthar City's lookout from outside the city sets the whole byte to 32, drawing the parked Ragnarok. Take-off clears all. Bits: +1 Entered at Fisherman's Horizon (Sun Panel), +2 Entered at Esthar City, +4 Entered at Spaceship Landing Zone, +8 Entered at Lunatic Pandora, +32 Ragnarok parked at the Esthar City lookout, +64 Entered at Deep Sea Research Center. |
| Byte        | 753-1023    | **Verified free** (271 bytes) — see note <sub>6</sub>. Unused by every field script, by the EXE, and zero in all real saves; a home for mod-added persistent data from 817 on, FFNx can use 753-816.                                                                                                                                                     |
| Byte        | 1024        | Card level mask of Joker in the training center (`bgmon_4`): `RND`, then `(random & 31) \| 22` before story progress 750, `(random & 127) \| 22` after. Scratch variable reused by many other maps.                                                                                                                        |
| Byte        | 1025        | Card level mask of Joker on the Ragnarok (`rgroad11`): `(random & 127) \| 70`.                                                                                                                                                                                                                                             |
| Byte        | 1040        | Card level mask of the SeeDs in the Balamb Garden hall (`bghall1b`): random roll mapped to 7, 11, 13, 14 or 15 (+16 later in the story).                                                                                                                                                                                   |
| Byte        | 1041        | Card level mask of the students in the Balamb Garden hall (`bghall_1`): random roll mapped to 7, 11, 13, 14 or 15.                                                                                                                                                                                                         |
| Byte        | Above 1023  | Temporary variables used pretty much everywhere.                                                                                                                                                                                                                                                                           |

# Notes

1. When the party splits in disc 2, each party member in the inactive party except Selphie has one of the eight bits changed for this variable. One member has a
   flag in the 4 most significant bits, and the other has a flag in the 4 least significant bits. It's done this way so that when the characters appear, they
   animate towards different locations in the field, rather than stacking on top of each other.
2. This byte contains flags for which characters are in Squall's party when the party splits in disc 2.
3. List of everything that 728 holds throughout the game:
    1. SeeD field exam "Conduct" score (lose points when you do something wrong at Dollet).
    2. Train job attempts (Timber)
    3. Tomb of the Unknown King student ID.
    4. Who you took to space in disc 3.
4. The field controlling restriction unlocking in Ultimecia's Castle uses this to figure out where to jump the party after they've broken a seal. It's unknown
   how SETPLACE actually sets this, it's not always related to the field ID or the SETPLACE parameter. This variable is also set at Balamb Garden's front gate
   manually.
5. List of everything that 341 holds throughout the game:
    1. First flashback team
    2. Selphie's current action when escaping from Deling's mansion (changes the dialogue)
    3. FH Concert Crappiness
    4. Something in B-Garden classroom during the paratrooper attack.
6. **Vars 753–1023 — verified unused, usable as free persistent storage for mods.** Confirmed on three independent axes: (a) referenced by **no field script** (all 882 `*.jsm` re-scanned for every PSHM/POPM/PSHSM opcode), (b) referenced by **no EXE code** (full binary scan for any instruction embedding an address in that range), and (c) **zero in every real save** (28 Steam `.ff8` saves decoded). The region's save-image offset is `464 + 3344 + var = 3808 + var`, so vars 753–1023 occupy image bytes **4561–4831**, which lie **inside** the save CRC span (bytes 80–5023); the game recomputes that CRC on every save, so values written here at runtime persist through a normal save/load with no extra hooking. Unlike the temporary variables at ≥1024, these bytes are never cleared on field entry. Runtime address of a given var = `0x1CFE9B8 + var` (e.g. var 753 = `0x1CFECA9`). **FFNx takes two parts of it:** 753-784 hold the magic drawn-once list when the kernel has more than 96 magic entries, and 785-816 hold the monster scanned-once list when `scene.out` uses a monster id of 160 or more. A mod that needs free storage starts at var **817**.

# Field-script usage (JSM bytecode scan)

The table below is generated by scanning **every field script** in the game — all 882 `*.jsm` files under `field/mapdata/`. Field scripts read and write variables
through nine bytecode opcodes; each instruction is a little-endian dword whose high byte is the opcode and whose low 24 bits are the operand. For these opcodes the
operand **is the byte offset** (= variable number):

| Opcode | Mnemonic | Access | Opcode | Mnemonic | Access |
|--------|----------|--------|--------|----------|--------|
| 10 | `PSHM_B` | read (u8) | 11 | `POPM_B` | write (u8) |
| 12 | `PSHM_W` | read (u16) | 13 | `POPM_W` | write (u16) |
| 14 | `PSHM_L` | read (u32) | 15 | `POPM_L` | write (u32) |
| 16 | `PSHSM_B` | read (s8) | 17 | `PSHSM_W` | read (s16) |
| 18 | `PSHSM_L` | read (s32) |    |          |        |

(Opcode numbers verified from the interpreter dispatch table `funcs_52A647` (see address table below); the JSM code array begins at file offset `u16@6`.) A variable that appears
here is genuinely used by field scripts; one that is absent (e.g. everything in the 410–431, 461–473, 494–527, 540–591 "unused" gaps) is **not** touched by any field
script, which is a strong independent confirmation of the "unused in fields" rows above.

The **field-name prefix** identifies the location, which usually reveals what a variable is for. Legend for the prefixes seen below:

`bg`=Balamb Garden · `bc`=Balamb Town · `bd`=Fire Cavern · `bv`=Balamb (boat/train) · `cr`=Centra Ruins (Odin) · `cw`=Chocobo Forest · `dd`=Deep Sea Research ·
`do`=Dollet · `ea`=Esthar Airstation · `eb`=Esthar streets · `ec`=Esthar City · `ed`=Edea's House · `em`=Esthar Lab (Odine) · `ep`=Esthar Palace · `es`/`et`/`eh`/`ew`/`el`/`ee`=Esthar (misc) ·
`fe`/`ff`=Ultimecia Castle · `fh`=Fisherman's Horizon · `gf`=Winhill · `gg`=Galbadia Garden · `gl`=Deling City · `gm`=Galbadia Missile Base · `gn`=Tomb of the Unknown King ·
`gp`=D-District Prison · `lo`=Intro/Logo · `rg`=Ragnarok · `ss`=Space station/Lunar · `tg`/`ti`=Timber · `tm`=Shumi Village · `te`=test/debug maps.

A few results worth calling out:

- **var 261** — heavily used (82 fields, all over the world map): a real, active general-purpose flag, previously "not investigated".
- **vars 264–270** (worldmap-variant cluster) are written by field scripts too, confirming they are ordinary savemap variables and not engine scratch.
- The location-coded blocks confirm many guesses: **387/400/404** are all Winhill (`gf`), **436/437** are the D-District Prison (`gp`), **358/359** Centra Ruins + space, **484/487/492/493** the Missile Base (`gm`), **485/486/491** the Tomb of the Unknown King (`gn`), **320–334/369–377** Ultimecia Castle (`fe`/`ff`), and **752** is Ragnarok (`rg`).
- The scan also resolved several bytes previously marked "not investigated"/"Unknown": **337** = Deling City event bits (`gl`), **448** = a BG 2F classroom panel (`bg2f_22` only), **533–539 / 595–624 / 626–691** = large per-town/city local-flag clusters (Dollet/Timber/Esthar, FH/D-District, Balamb-city/BG-library/Esthar-city — the Esthar walkway gates **672/673** are the single busiest bytes in the whole block), and **726/729/732** are all read by `bgrank1` (the SeeD-rank field), i.e. town-conduct inputs — **732** is written *only* by the Fire Cavern field `bdifrit1`.
- Temporary/scratch variables (offsets **1024–1074** observed) are used everywhere, as expected.
- **Vars 753–1023 (271 bytes) are verified free for modding** — see note <sub>6</sub>.

### Who accesses the variable block

The block is shared savemap state. Besides the field scripts (`*.jsm`) scanned above, it is read/written by several other EXE modules — there is **no separate
scripting language** for it apart from the field JSM. The consumers found in the binary (via the `VAR_MAP_ADDRESS` pointer) are:

- **Field script-command handlers** — the `SCRIPT_*` engine functions behind field opcodes (e.g. `SCRIPT_ADDGIL`, `SCRIPT_CARDGAME`, `SCRIPT_DRAWPOINT`, `SCRIPT_JOIN`/`SCRIPT_SPLIT`, `SCRIPT_JUNCTION`, `SCRIPT_SEALEDOFF`, `SCRIPT_ADDSEEDLEVEL`) read/write vars on a script's behalf.
- **Field per-frame update** (`sub_529FF0`) and **world-map per-frame update** (`sub_6519D0`, via `FFWorldDirector`) — both tick Steps, SeeD pay, SeeD rank, walking HP-regen and Angelo points directly in the block.
- **World-map module** — `FFWorldInit`, `jumpFromFieldToWorldmap` / `jumpFromWorldmapToField`, `World_BuildObjectInstanceList`, `World_MusicChanger` (worldmap variant, field↔worldmap transitions, music).
- **Battle module** — reads a few entries (e.g. `Battle_KeepMusicAfterBattle` for music retention); battle *results* (kills, deaths, gil, battles-won) are written back to the block after combat.
- **Menu / save-data code** and **new-game init** (`newgame_startgame`) — display values (gil, SeeD rank) and set the block's starting state.

The monster **battle AI** and world-map encounter logic use their own separate variable spaces and do not address this block directly (apart from boss-fight HP mirror
values such as vars 350–357 / 380 / 443, which the special-battle setup reads from here).

| Var | Reads | Writes | #Fields | Areas | Example field folders |
|-----|-------|--------|---------|-------|-----------------------|
| 16 | 26 | 24 | 8 | bg(1) dd(1) fh(1) | bgrank1, ddruins6, fhwater1 |
| 20 | 2 | 0 | 1 | tg(1) | tgcourt1 |
| 26 | 3 | 0 | 2 | do(2) | dosea_2, dotown_1 |
| 28 | 1 | 0 | 1 | bg(1) | bgroom_1 |
| 34 | 1 | 0 | 1 | bg(1) | bgroom_1 |
| 44 | 1 | 0 | 1 | bg(1) | bgroom_1 |
| 50 | 1 | 0 | 1 | bg(1) | bgroom_1 |
| 68 | 5 | 0 | 4 | do(2) gf(2) | dosea_2, dotown_1, gfelone2 |
| 72 | 108 | 0 | 36 | cw(7) ti(6) bc(4) | bcgate_1, bchtl_1, bcport1b |
| 76 | 4 | 0 | 3 | gl(2) bg(1) | bg2f_1a, glhtl1, glyagu2 |
| 80 | 159 | 2 | 48 | bg(12) gl(9) do(4) | bg2f_11, bg2f_21, bg2f_31 |
| 84 | 721 | 5 | 218 | bg(41) ec(23) gl(15) | bccent1a, bccent_1, bcform_1 |
| 86 | 41 | 2 | 7 | bc(1) do(1) ec(1) | bcgate_1, dogate_2, ecenter2 |
| 87 | 25 | 0 | 17 | eb(4) bg(3) gl(3) | bgryo2_1, bgsido_2, bgsido_5 |
| 88 | 86 | 0 | 15 | eb(2) gn(2) gp(2) | ddruins6, dopub_2, ebadele2 |
| 100 | 0 | 2 | 1 | lo(1) | logo |
| 256 | 5868 | 1072 | 517 | bg(100) gl(53) fh(37) | bccent_1, bcform_1, bcgate_1 |
| 258 | 4 | 2 | 2 | gp(1) te(1) | gpbigin2 |
| 261 | 423 | 187 | 82 | bg(10) gl(8) do(6) | bchtr_1, bcmin22a, bghall2a |
| 264 | 14 | 9 | 8 | bg(2) gp(2) bc(1) | bchtl1a, bggate_6, bgsido_7 |
| 265 | 13 | 13 | 10 | gp(2) ti(2) bc(1) | bcgate_1, bgsido_7, bvcar_1 |
| 266 | 26 | 52 | 18 | te(6) ep(4) bg(2) | bgmast_6, bgsido_8, eaplane1 |
| 268 | 0 | 11 | 10 | bv(3) bc(2) rg(2) | bcform_1, bcport_2, bgmast_6 |
| 269 | 0 | 6 | 6 | bg(2) ea(1) eb(1) | bghoke_2, bgsido_7, eaplane1 |
| 270 | 0 | 1 | 1 | ec(1) | ecpview2 |
| 272 | 1115 | 233 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 273 | 1113 | 233 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 274 | 1113 | 233 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 275 | 1113 | 233 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 276 | 1113 | 233 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 277 | 1113 | 233 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 278 | 1130 | 234 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 279 | 1113 | 233 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 280 | 2111 | 2273 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 281 | 2111 | 2273 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 282 | 2111 | 2273 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 283 | 2111 | 2273 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 284 | 2111 | 2273 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 285 | 2111 | 2273 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 286 | 2111 | 2273 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 287 | 2111 | 2273 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 288 | 454 | 228 | 170 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 289 | 907 | 228 | 170 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 290 | 916 | 228 | 170 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 291 | 235 | 228 | 170 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 292 | 2103 | 5711 | 170 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 293 | 287 | 3649 | 170 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 294 | 17 | 121 | 11 | es(2) bc(1) do(1) | bcsta_1, dopub_2, ephall1 |
| 295 | 1978 | 149 | 172 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 296 | 3768 | 1818 | 171 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 297 | 9579 | 3634 | 171 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 298 | 817 | 456 | 171 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 299 | 3717 | 121 | 171 | bg(29) ec(21) ti(15) | bcform_1, bcgate_1, bcmin11a |
| 300 | 35 | 25 | 2 | do(1) te(1) | dopub_2 |
| 304 | 47 | 18 | 14 | gl(3) te(3) bc(2) | bcform_1, bchtr_1, bgroom_6 |
| 305 | 36 | 13 | 12 | bg(2) te(2) tv(2) | bghoke_2, bgroom_6, crview1 |
| 320 | 24 | 12 | 5 | fe(5) | feart1f1, feart1f2, feart2f1 |
| 321 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 322 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 323 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 324 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 325 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 326 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 327 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 328 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 329 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 330 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 331 | 40 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 332 | 28 | 12 | 4 | fe(4) | feart1f1, feart1f2, feart2f1 |
| 333 | 29 | 17 | 2 | fe(1) ff(1) | fetre1, ffbrdg1 |
| 334 | 28 | 8 | 2 | fe(1) te(1) | feroad1 |
| 335 | 1 | 1 | 1 | ea(1) | eapod1 |
| 336 | 110 | 79 | 12 | gl(11) lo(1) | glfurin4, glfury1, glgate1 |
| 337 | 25 | 6 | 6 | gl(6) | glfurin1, glfurin3, glprein1 |
| 338 | 36 | 7 | 6 | gl(4) bc(2) | bccent12, bccent15, glwater1 |
| 339 | 104 | 74 | 7 | gl(5) cr(2) | crtower1, crtower2, glfurin1 |
| 340 | 230 | 102 | 24 | gl(11) bg(9) fh(2) | bg2f_31, bgbtl_1, bggate6a |
| 341 | 24 | 24 | 7 | fh(2) gl(2) bg(1) | bgroom_3, fhpanel1, fhwise13 |
| 342 | 40 | 44 | 8 | gl(8) | glgate1, glgate3, glmall1 |
| 343 | 42 | 11 | 17 | gg(16) te(1) | ggele1, gggro1, gggroen2 |
| 344 | 35 | 18 | 9 | gg(5) bg(3) te(1) | bg2f_11, bg2f_21, bgkote_5 |
| 345 | 41 | 14 | 20 | cr(11) gg(4) ee(3) | crenter1, crodin1, cropen1 |
| 346 | 76 | 2 | 3 | fh(3) | fhwise12, fhwise13, fhwise15 |
| 347 | 76 | 2 | 2 | fh(2) | fhwise12, fhwise13 |
| 348 | 77 | 2 | 2 | fh(2) | fhwise12, fhwise13 |
| 349 | 77 | 2 | 2 | fh(2) | fhwise12, fhwise13 |
| 350 | 0 | 2 | 2 | bg(1) te(1) | bg2f_31 |
| 352 | 0 | 2 | 2 | bg(1) te(1) | bg2f_31 |
| 354 | 15 | 5 | 3 | bg(2) te(1) | bg2f_31, bgbtl_1 |
| 356 | 13 | 5 | 3 | bg(2) te(1) | bg2f_31, bgbtl_1 |
| 358 | 54 | 27 | 21 | cr(11) ss(6) te(2) | bgkote_3, crenter1, crodin1 |
| 359 | 45 | 18 | 8 | cr(6) te(2) | crpower1, crroof1, crtower1 |
| 360 | 38 | 33 | 2 | fh(2) | fhedge11, fhwise13 |
| 364 | 2 | 1 | 3 | cr(3) | crroof1, crsphi1, crtower3 |
| 365 | 2 | 1 | 3 | cr(3) | crroof1, crsphi1, crtower3 |
| 366 | 2 | 1 | 3 | cr(3) | crroof1, crsphi1, crtower3 |
| 367 | 2 | 1 | 3 | cr(3) | crroof1, crsphi1, crtower3 |
| 368 | 2 | 1 | 3 | cr(3) | crroof1, crsphi1, crtower3 |
| 369 | 36 | 13 | 6 | ff(2) gl(2) fe(1) | felrele1, ffhole1, ffhole1a |
| 370 | 161 | 88 | 10 | fe(8) ff(1) te(1) | fehall1, felfst1, felrele1 |
| 372 | 21 | 11 | 11 | fe(11) | feart1f1, feart2f1, febarac1 |
| 373 | 25 | 7 | 9 | fe(8) te(1) | febrdg1, fegate1, fejail1 |
| 374 | 136 | 49 | 38 | fe(38) | fe2f1, feart1f1, feart1f2 |
| 375 | 25 | 6 | 7 | fe(7) | febrdg1, fegate1, fepic1 |
| 376 | 7 | 3 | 3 | fe(3) | febrdg1, fegate1, fewater2 |
| 377 | 9 | 8 | 2 | fe(2) | fewater1, fewor2 |
| 378 | 66 | 70 | 12 | cr(11) te(1) | crenter1, crodin1, cropen1 |
| 380 | 4 | 2 | 2 | bg(1) te(1) | bg2f_31 |
| 384 | 27 | 10 | 4 | bg(3) te(1) | bggate_1, bgroom_4, bgroom_5 |
| 385 | 4 | 2 | 1 | gl(1) | glclub1 |
| 387 | 37 | 13 | 10 | gf(10) | gfcross1, gfelone1, gfelone2 |
| 388 | 6 | 3 | 1 | ti(1) | timania5 |
| 389 | 6 | 4 | 3 | ti(3) | timania1, timania2, timania3 |
| 390 | 1 | 1 | 1 | eh(1) | ehback2 |
| 391 | 9 | 5 | 1 | ep(1) | epwork3 |
| 392 | 12 | 7 | 3 | bg(2) eh(1) | bgroom_5, bgroom_6, ehback2 |
| 400 | 1 | 1 | 2 | gf(2) | gfelone2, gflain2 |
| 404 | 1 | 1 | 1 | gf(1) | gflain2 |
| 409 | 48 | 25 | 1 | bg(1) | bgroom_6 |
| 432 | 11 | 5 | 2 | bg(2) | bghall_1, bghall_6 |
| 433 | 97 | 33 | 24 | bg(22) te(2) | bg2f_4, bggate_1, bggate_6 |
| 434 | 53 | 24 | 9 | bg(7) te(2) | bg2f_2, bg2f_4, bghall_1 |
| 435 | 31 | 13 | 6 | bg(5) te(1) | bg2f_2, bg2f_22, bg2f_3 |
| 436 | 101 | 13 | 16 | gp(12) te(2) bg(1) | bgmon_4, edmoor1, gpbig1 |
| 437 | 100 | 68 | 22 | gp(10) rg(8) bg(3) | bggate_1, bgryo2_1, bgsido_5 |
| 438 | 61 | 34 | 16 | bg(15) te(1) | bgbook1a, bgeat1a, bggate_2 |
| 439 | 30 | 17 | 8 | bg(7) te(1) | bgbook1a, bgeat1a, bghall1b |
| 440 | 41 | 10 | 8 | bg(7) te(1) | bghall1b, bghoke_1, bgkote1a |
| 441 | 40 | 17 | 15 | bg(14) te(1) | bg2f_22, bg2f_3, bgbook1a |
| 442 | 28 | 5 | 3 | bg(2) te(1) | bghall_5, bgryo2_1 |
| 445 | 34 | 22 | 9 | rg(8) te(1) | rgair1, rgexit1, rgguest2 |
| 446 | 86 | 58 | 9 | rg(8) te(1) | rgair1, rgexit1, rgguest2 |
| 447 | 16 | 24 | 8 | rg(8) | rgair1, rgexit1, rgguest2 |
| 448 | 2 | 3 | 1 | bg(1) | bg2f_22 |
| 450 | 19 | 10 | 6 | bg(5) gp(1) | bggate_5, bgmon_2, bgryo2_1 |
| 451 | 30 | 13 | 9 | eb(8) gp(1) | ebroad12, ebroad13, ebroad42 |
| 452 | 8 | 3 | 4 | eb(4) | ebadele1, ebgate3, ebinlow1 |
| 453 | 2 | 3 | 2 | gp(2) | gpbig1a, gpgmn1a |
| 454 | 2 | 3 | 2 | gp(2) | gpbig1a, gpgmn1a |
| 455 | 2 | 3 | 2 | gp(2) | gpbig1a, gpgmn1a |
| 458 | 10 | 5 | 5 | bg(4) fh(1) | bg2f_3, bghall3a, bghall_3 |
| 459 | 3 | 2 | 2 | bg(2) | bgmon_1, bgmon_6 |
| 460 | 23 | 11 | 8 | bg(5) gp(1) rg(1) | bg2f_2, bgmon_4, bgrank1 |
| 474 | 11 | 4 | 4 | rg(3) bg(1) | bg2f_1, rgair2, rgexit2 |
| 475 | 90 | 17 | 17 | bg(7) rg(7) ea(1) | bg2f_1, bghall3a, bghoke_1 |
| 476 | 23 | 10 | 6 | bg(5) te(1) | bg2f_1, bghall1b, bghall3a |
| 477 | 38 | 20 | 7 | bg(6) te(1) | bg2f_1, bghall1b, bghall_5 |
| 478 | 51 | 52 | 22 | bg(19) te(2) fh(1) | bg2f_1, bg2f_2, bg2f_22 |
| 479 | 159 | 42 | 162 | bg(65) eb(46) gp(24) | bg2f_1, bg2f_2, bg2f_22 |
| 480 | 9 | 3 | 1 | bg(1) | bgroom_1 |
| 481 | 27 | 6 | 2 | bg(1) te(1) | bgeat_2 |
| 482 | 17 | 3 | 1 | gm(1) | gmmoni1 |
| 484 | 264 | 57 | 16 | gm(13) te(2) bg(1) | bgmast_6, gmcont1, gmcont2 |
| 485 | 13 | 2 | 2 | gn(2) | gnroom4, gnview1 |
| 486 | 566 | 255 | 10 | gn(10) | gnroad1, gnroad2, gnroad3 |
| 487 | 27 | 18 | 8 | gm(6) bg(1) te(1) | bgroom_1, gmcont1, gmcont2 |
| 488 | 81 | 26 | 5 | fh(2) bg(1) gm(1) | bgeat_1, fhtown23, fhtown24 |
| 489 | 48 | 17 | 5 | fh(2) bg(1) ew(1) | bgeat_1, ewpanel2, fhtown22 |
| 490 | 10 | 2 | 1 | bg(1) | bgeat_1 |
| 491 | 34 | 6 | 7 | gn(7) | gnroad1, gnroad2, gnroad5 |
| 492 | 40 | 8 | 11 | gm(11) | gmcont1, gmcont2, gmden1 |
| 493 | 16 | 1 | 11 | gm(11) | gmcont1, gmcont2, gmden1 |
| 528 | 463 | 147 | 49 | ti(25) se(10) do(5) | bgmast_6, cdfield1, cdfield2 |
| 530 | 206 | 65 | 24 | do(22) bg(1) te(1) | bgrank1, doan1_1, doan1_2 |
| 531 | 1 | 2 | 2 | do(1) te(1) | dosea_2 |
| 532 | 2 | 18 | 4 | do(3) te(1) | dogate_1, dosea_2, dotown_1 |
| 533 | 42 | 23 | 10 | do(9) te(1) | dohtl_1, domin2_1, domt1_1 |
| 534 | 55 | 14 | 7 | do(6) te(1) | domin2_1, domt5_1, doopen1a |
| 535 | 53 | 18 | 11 | ti(10) te(1) | tiagit2, tigate1, timin21 |
| 536 | 28 | 8 | 9 | ti(8) do(1) | dopub_3, tiagit4, tiback1 |
| 537 | 112 | 23 | 22 | eb(20) te(2) | ebexit1, ebexit2, ebexit3 |
| 538 | 29 | 10 | 10 | eb(5) cd(2) ed(2) | cdfield2, cdfield3, ebroad11 |
| 539 | 56 | 21 | 10 | eb(4) ef(2) se(2) | ebexit3, ebroad11, ebroad12 |
| 592 | 79 | 22 | 6 | bv(5) te(1) | bvtr_1, bvtr_2, bvtr_3 |
| 593 | 4 | 3 | 3 | rg(1) sd(1) te(1) | rgcock2, sdcore2 |
| 595 | 14 | 17 | 6 | fh(3) dd(2) te(1) | ddtower5, ddtower6, fhbrdg1 |
| 596 | 2 | 4 | 1 | bg(1) | bggate_1 |
| 597 | 10 | 5 | 3 | fh(3) | fhhtl1, fhhtr1, fhtown1 |
| 598 | 32 | 17 | 7 | fh(6) te(1) | fhdeck1, fhfish1, fhhtr1 |
| 599 | 32 | 14 | 8 | cw(6) fh(2) | cwwood1, cwwood2, cwwood3 |
| 600 | 12 | 9 | 5 | fh(4) te(1) | fhbrdg1, fhdeck6, fhroof1 |
| 601 | 52 | 11 | 9 | fh(5) tm(3) te(1) | fhbrdg1, fhhtl1, fhhtr1 |
| 602 | 10 | 14 | 5 | dd(4) te(1) | ddsteam1, ddtower1, ddtower3 |
| 603 | 17 | 13 | 5 | dd(4) te(1) | ddtower1, ddtower3, ddtower4 |
| 604 | 7 | 17 | 4 | dd(3) te(1) | ddtower1, ddtower4, ddtower5 |
| 605 | 42 | 20 | 13 | dd(11) ec(1) te(1) | ddruins1, ddruins2, ddruins3 |
| 606 | 14 | 8 | 4 | fh(3) tm(1) | fhfish1, fhmin1, fhwater1 |
| 607 | 64 | 10 | 9 | tm(7) fh(1) te(1) | fhmin1, tmdome1, tmelder1 |
| 608 | 36 | 20 | 5 | tm(4) te(1) | tmelder1, tmgate1, tmkobo2 |
| 609 | 13 | 13 | 9 | tm(8) te(1) | tmele1, tmgate1, tmhtl1 |
| 610 | 27 | 11 | 7 | tm(6) te(1) | tmgate1, tmkobo2, tmmin1 |
| 611 | 6 | 15 | 8 | tm(6) fh(2) | fhbrdg1, fhdeck6, tmgate1 |
| 612 | 46 | 18 | 8 | tm(7) te(1) | tmelder1, tmgate1, tmkobo1 |
| 613 | 33 | 5 | 3 | fh(1) te(1) tm(1) | fhmin1, tmmin1 |
| 614 | 44 | 57 | 11 | dd(6) sd(3) rg(1) | ddtower1, ddtower2, ddtower3 |
| 615 | 77 | 81 | 9 | dd(8) te(1) | ddruins6, ddsteam1, ddtower1 |
| 616 | 49 | 31 | 8 | cw(7) te(1) | cwwood1, cwwood2, cwwood3 |
| 617 | 54 | 31 | 8 | cw(7) te(1) | cwwood1, cwwood2, cwwood3 |
| 618 | 53 | 31 | 8 | cw(7) te(1) | cwwood1, cwwood2, cwwood3 |
| 619 | 27 | 4 | 1 | cw(1) | cwwood4 |
| 620 | 53 | 31 | 8 | cw(7) te(1) | cwwood1, cwwood2, cwwood3 |
| 621 | 56 | 30 | 8 | cw(7) te(1) | cwwood1, cwwood2, cwwood3 |
| 622 | 54 | 31 | 8 | cw(7) te(1) | cwwood1, cwwood2, cwwood3 |
| 623 | 66 | 10 | 8 | tm(8) | tmelder1, tmele1, tmgate1 |
| 624 | 136 | 43 | 20 | bc(9) tg(7) bg(2) | bccent_1, bcgate_1, bchtl_1 |
| 625 | 61 | 33 | 15 | bc(14) te(1) | bccent_1, bcform_1, bcgate_1 |
| 626 | 64 | 38 | 11 | bc(10) te(1) | bccent_1, bcform_1, bcgate_1 |
| 627 | 78 | 43 | 11 | bc(10) te(1) | bccent_1, bcform_1, bcgate_1 |
| 629 | 3 | 6 | 4 | bc(3) te(1) | bcform_1, bcgate_1, bcport1a |
| 630 | 60 | 43 | 10 | bc(9) te(1) | bccent_1, bcform_1, bcgate_1 |
| 631 | 26 | 15 | 10 | bc(8) bg(1) te(1) | bccent_1, bcform_1, bcgate_1 |
| 632 | 45 | 31 | 10 | bc(7) bg(3) | bcform_1, bcgate_1, bchtl_1 |
| 633 | 65 | 29 | 12 | bc(6) bg(3) tg(2) | bcform_1, bcgate_1, bcmin1_1 |
| 634 | 5 | 14 | 5 | bg(5) | bgbook1b, bgbook_1, bgbook_2 |
| 636 | 12 | 2 | 1 | gf(1) | gfvill1a |
| 638 | 37 | 18 | 4 | bg(3) te(1) | bgmast_1, bgmast_3, bgmast_5 |
| 640 | 35 | 12 | 3 | tg(2) te(1) | tgcourt1, tgfront1 |
| 641 | 34 | 12 | 8 | tg(6) bc(1) te(1) | bcgate1a, tgfront1, tggara1 |
| 642 | 41 | 24 | 12 | bc(9) tg(2) te(1) | bccent1a, bccent_1, bcgate_1 |
| 643 | 83 | 47 | 15 | bc(12) bg(2) te(1) | bccent1a, bcform1a, bcform_1 |
| 644 | 54 | 32 | 17 | bc(13) bg(3) te(1) | bccent1a, bcform_1, bcgate1a |
| 645 | 36 | 12 | 3 | bg(2) te(1) | bgbook1b, bgbook_2 |
| 646 | 85 | 38 | 12 | bc(11) te(1) | bccent1a, bcform1a, bcgate1a |
| 647 | 17 | 4 | 8 | bc(7) te(1) | bccent1a, bcform1a, bcmin21a |
| 648 | 78 | 43 | 14 | bc(13) te(1) | bccent1a, bcform1a, bcgate1a |
| 649 | 62 | 23 | 12 | bc(11) te(1) | bccent1a, bcform1a, bcgate1a |
| 656 | 5 | 1 | 5 | bc(5) | bccent1a, bcport1b, bcport2a |
| 658 | 4 | 5 | 5 | bc(5) | bccent1a, bcport1b, bcport2a |
| 659 | 57 | 15 | 8 | bg(5) bc(2) te(1) | bchtl_1, bchtr_1, bgbook1b |
| 660 | 125 | 44 | 13 | bc(6) bg(6) te(1) | bcform_1, bcgate_1, bchtl_1 |
| 661 | 38 | 20 | 12 | bg(4) gf(4) bc(3) | bcform_1, bcgate_1, bcsta_1 |
| 662 | 50 | 14 | 6 | gf(5) te(1) | gfhtl1a, gfhtr1a, gflain1a |
| 663 | 44 | 16 | 6 | gf(5) bg(1) | bgbook_1, gflain1a, gflain2a |
| 664 | 21 | 10 | 5 | bc(3) gf(2) | bccent1a, bcgate1a, bcport1b |
| 665 | 47 | 19 | 12 | bc(7) bg(4) te(1) | bcform_1, bcgate_1, bchtl_1 |
| 666 | 6 | 2 | 3 | bg(3) | bgbook1b, bgbook_1, bgbook_2 |
| 668 | 15 | 7 | 7 | bc(5) gf(1) te(1) | bcmin21a, bcmin2_1, bcport1b |
| 672 | 336 | 58 | 38 | ec(28) em(5) fh(2) | eccway11, eccway12, eccway21 |
| 675 | 1 | 2 | 2 | gl(1) te(1) | glhtr1 |
| 677 | 36 | 22 | 18 | ec(14) em(4) | eccway11, eccway12, eccway21 |
| 678 | 21 | 4 | 8 | ec(8) | eccway11, eccway12, eccway21 |
| 680 | 10 | 5 | 5 | ec(4) te(1) | eccway11, eccway12, eccway41 |
| 681 | 34 | 17 | 3 | ec(2) ep(1) | ecmall1, ecmall1a, ephall2 |
| 682 | 26 | 7 | 5 | ec(3) ep(2) | eccway11, eccway31, ecpway1 |
| 683 | 7 | 3 | 2 | ec(1) te(1) | eccway21 |
| 684 | 5 | 3 | 2 | em(2) | emlabo1b, emlobby3 |
| 685 | 32 | 17 | 6 | ec(5) te(1) | eccway31, eccway41, eciway11 |
| 686 | 12 | 5 | 3 | ec(3) | ecenter1, ecmway1, ecoway1 |
| 687 | 20 | 40 | 20 | ec(20) | eccway11, eccway12, eccway21 |
| 688 | 5 | 3 | 1 | ep(1) | epmeet1 |
| 689 | 6 | 5 | 2 | em(1) te(1) | emlabo1 |
| 690 | 2 | 1 | 1 | ec(1) | ecpview1 |
| 691 | 4 | 2 | 2 | bg(2) | bgmd4_1, bgmd4_2 |
| 720 | 361 | 69 | 91 | bg(56) bc(14) bd(8) | bccent_1, bcform_1, bcgate_1 |
| 721 | 173 | 39 | 85 | bg(52) bc(14) bd(8) | bccent_1, bcform_1, bcgate_1 |
| 722 | 177 | 34 | 77 | bg(48) bc(14) bd(8) | bccent_1, bcform_1, bcgate_1 |
| 723 | 43 | 19 | 32 | bc(14) bg(8) tg(5) | bccent_1, bcform_1, bcgate_1 |
| 724 | 31 | 33 | 10 | ti(6) do(2) bg(1) | bgrank1, dosea_2, dotown_1 |
| 726 | 12 | 7 | 8 | ti(4) do(2) bg(1) | bgrank1, dosea_2, dotown_1 |
| 728 | 104 | 46 | 29 | do(9) ss(4) te(4) | bgrank1, bgroom_6, doani3_2 |
| 729 | 14 | 10 | 9 | ti(3) do(2) te(2) | bgrank1, dosea_2, dotown_1 |
| 730 | 65 | 27 | 33 | bg(15) gn(9) te(4) | bg2f_2, bgbook1b, bgbook_1 |
| 732 | 11 | 1 | 2 | bd(1) bg(1) | bdifrit1, bgrank1 |
| 734 | 60 | 35 | 6 | bg(4) te(2) | bggate_1, bgmast_4, bgryo2_1 |
| 735 | 28 | 12 | 10 | bg(9) te(1) | bgbook_3, bgeat_1, bghall3a |
| 752 | 31 | 22 | 7 | rg(6) ec(1) | ecpview2, rgcock2, rgcock4 |

*(Temporary/scratch variables at offsets 1024–1074 are also used across many fields; they are volatile per-map scratch and are omitted from this table.)*

# Struct (IDA `SavemapVariables`)

This is the layout applied to `VARMAP_START` in the FF8_EN.exe database. It is a **packed** struct (no padding), so every field's offset equals its
variable number in the table above. `MapSeal`, `VarMiscFlag` and `SomeVarFlag` are the game's own enum types; `unused*`/`unk*`/`notInvestigated*` bytes are gaps.

```c
#pragma pack(push, 1)
struct SavemapVariables
{
    // 0x00: Unused in fields (always "FF-8")
    __int32 literally_ff8_text;
    __int32 Steps;                  // 0x04  Steps (random encounter counter)
    __int32 SeedPay;                // 0x08  Payslip
    __int32 linked_healing_move_up; // 0x0C  (unused in fields)
    __int16 SeeDRankPoints;         // 0x10  SeeD rank points (rank = clamp(v,100,3100)/100)
    __int8  unused3[2];             // 0x12
    __int32 BattlesWon;             // 0x14
    __int8  unused4[2];             // 0x18
    __int16 BattlesEscaped;         // 0x1A
    __int16 SquallKills;            // 0x1C
    __int16 ZellKills;              // 0x1E
    __int16 IrvineKills;            // 0x20
    __int16 QuistisKills;           // 0x22
    __int16 RinoaKills;             // 0x24
    __int16 SelphieKills;           // 0x26
    __int16 SeiferKills;            // 0x28
    __int16 EdeaKills;              // 0x2A
    __int16 SquallDeaths;           // 0x2C
    __int16 ZellDeaths;             // 0x2E
    __int16 IrvineDeaths;           // 0x30
    __int16 QuistisDeaths;          // 0x32
    __int16 RinoaDeaths;            // 0x34
    __int16 SelphieDeaths;          // 0x36
    __int16 SeiferDeaths;           // 0x38
    __int16 EdeaDeaths;             // 0x3A
    __int8  unused5[8];             // 0x3C
    __int32 TotalEnemiesKilled;     // 0x44
    __int32 PartyGil;               // 0x48
    __int32 LagunaPartyGil;         // 0x4C
    __int32 MovieFrameCount;        // 0x50
    __int16 LastAreaVisited;        // 0x54
    __int8  CurrentCarRent;         // 0x56
    __int8  EngineVar1;             // 0x57  (music-related engine var)
    __int8  EngineVar2;             // 0x58  (save-point / Siren Move-Find engine var)
    __int8  unused6[15];            // 0x59
    VarMiscFlag miscFlag;           // 0x68  SALARYDISPON/MUSICLOAD/PHSPOWER related
    __int32 MusicRelated;           // 0x6C  Music retention (-1 = stop after battle)
    __int32 unused7;                // 0x70
    __int8  FieldDrawPoints[44];    // 0x74
    __int8  WorldmapDrawPoints[20]; // 0xA0
    // 0xB4..0xF3: engine-only display/timer state (unused by field scripts)
    __int8  unk7777;                // 0xB4
    __int8  unk7778;                // 0xB5
    __int8  showTimer;              // 0xB6
    __int8  unk7770;                // 0xB7
    __int8  unk777[20];             // 0xB8  (battle-music A/B toggle at ~0xC9/0xCB)
    __int8  unk11;                  // 0xCC
    __int8  timer_x_position;       // 0xCD
    __int8  timer_y_position;       // 0xCE
    __int8  battleOff;              // 0xCF
    __int8  unk15;                  // 0xD0
    SomeVarFlag canSaveHere;        // 0xD1
    __int8  unk[30];                // 0xD2
    __int8  unk1;                   // 0xF0
    __int8  unk2;                   // 0xF1
    __int8  unk3;                   // 0xF2
    MapSeal map_seal;               // 0xF3
    __int8  unk5[12];               // 0xF4  (vars 244-255, not investigated)
    __int16 MainStoryProgress;      // 0x100 var 256
    __int8  var258;                 // 0x102
    __int8  unused259[2];           // 0x103
    __int8  var261;                 // 0x105
    __int8  unused262[2];           // 0x106
    __int8  WorldmapVariantFlags;   // 0x108 var 264  (bit3/bit4 -> 0x40)
    __int8  WorldmapVar265;         // 0x109 var 265  (-> wm state +103)
    __int8  WorldmapVariantIndex;   // 0x10A var 266  (5-case variant selector)
    __int8  WorldmapDisc4SubVariant;// 0x10B var 267  (disc-4 sub-variant)
    __int8  WorldmapVar268;         // 0x10C var 268  (-> wm state +106)
    __int8  WorldmapVar269;         // 0x10D var 269  (-> wm state +107)
    __int8  WorldmapVar270;         // 0x10E var 270  (-> wm state +108)
    __int8  WorldmapVar271;         // 0x10F var 271  (-> wm state +109)
    __int8  CardGameVars[28];       // 0x110 vars 272-299 (292 rules, 293 trade rule)
    __int8  CardQueenRecards;       // 0x12C var 300
    __int8  unused301[3];           // 0x12D
    __int8  TimberManiacsIssues[2]; // 0x130
    __int8  ReservedHacktuarFF8Voice[14]; // 0x132
    __int8  UltimeciaGallery[13];   // 0x140
    __int8  UltimeciaArmory;        // 0x14D
    MapSeal UltimeciaSeals;         // 0x14E var 334 (SEALEDOFF)
    __int8  CardRelated;            // 0x14F
    __int8  DelingBus;              // 0x150
    __int8  GGardenWaterFlags337;   // 0x151 var 337 (Galbadia Garden water/fountain, gl*)
    __int8  DelingSewerGates[3];    // 0x152
    __int8  MultiPurposeVar1;       // 0x155 var 341 (multi-use, note 5)
    __int8  DelingBusSystem;        // 0x156
    __int8  GGardenDoorFlags1;      // 0x157
    __int8  GGardenEventDuringGGFlags2; // 0x158
    __int8  GGardenDoorFlags3;      // 0x159
    __int8  FHInstruments[4];       // 0x15A
    __int16 HealthBars[4];          // 0x15E var 350-357 (Garden mech fight)
    __int8  SpaceStationFlags;      // 0x166
    __int8  CentraRuinsFlags;       // 0x167
    __int32 FHMusicChoice;          // 0x168
    __int8  CentraRuinsCode[5];     // 0x16C
    __int8  UltimeciaCastleFlags[2];// 0x171
    __int8  unused371;              // 0x173
    __int8  UltimeciaBossFlags[5];  // 0x174
    __int8  UltimeciaOrgan;         // 0x179
    __int8  CentraRuinsTimer;       // 0x17A
    __int8  unused379;              // 0x17B
    __int16 SquallMechHealth;       // 0x17C
    __int8  unused382[2];           // 0x17E
    __int8  LagunaTimePeriods;      // 0x180
    __int8  LagunaPubDialogue;      // 0x181
    __int8  unused386;              // 0x182
    __int8  WinhillProgress;        // 0x183
    __int8  TimberManiacsLobby;     // 0x184
    __int8  TimberManiacsOffice;    // 0x185
    __int8  EdeaHouseFlags;         // 0x186
    __int8  LagunaOfficeFlags;      // 0x187
    __int8  EdeaBGComputerVar;      // 0x188 var 392
    __int8  unused393[7];           // 0x189
    __int32 WinhillMonsters;        // 0x190
    __int32 WinhillMonsters2;       // 0x194
    __int8  unused408;              // 0x198
    __int8  BalambComputer;         // 0x199
    __int8  unused410[22];          // 0x19A
    __int8  BGHallFlags;            // 0x1B0
    __int8  BGFlags[3];             // 0x1B1
    __int8  MoombaFriendship;       // 0x1B4
    __int8  PartyTracking;          // 0x1B5
    __int8  CidNorgFlags[2];        // 0x1B6
    __int8  EventFlags;             // 0x1B8 var 440
    __int8  CidNorgFlags2;          // 0x1B9
    __int8  RinoaTourFlags;         // 0x1BA
    __int16 ZellPrisonHealth;       // 0x1BB var 443
    __int8  PropagatorFlags[3];     // 0x1BD
    __int16 BG2FClassroomVar448;    // 0x1C0 var 448 (Balamb Garden 2F classroom study panel, bg2f_22)
    __int8  MagazineFlags[2];       // 0x1C2
    __int8  LunaticPandora;         // 0x1C4
    __int8  MoombaTeleport[3];      // 0x1C5
    __int8  unused456[2];           // 0x1C8
    __int8  MusicSkipFlags[2];      // 0x1CA
    __int8  RandomFlags1;           // 0x1CC
    __int8  unused461[13];          // 0x1CD
    __int8  RandomFlags2;           // 0x1DA
    __int8  CCGroupVars[4];         // 0x1DB
    __int8  DisableRandomBattles;   // 0x1DF var 479
    __int8  ClassroomState;         // 0x1E0
    __int8  CafeteriaConversation;  // 0x1E1
    __int16 MissileErrorRatio;      // 0x1E2
    __int8  MissileBaseProgress;    // 0x1E4
    __int8  ToUKProgress;           // 0x1E5
    __int8  ToUKRoom;               // 0x1E6
    __int8  MissileBaseProgress2;   // 0x1E7
    __int8  AlternatePartyFlags;    // 0x1E8 var 488 (note 1)
    __int8  RandomTalkFlags;        // 0x1E9
    __int8  CafeteriaCutscene;      // 0x1EA
    __int8  ToUKStuff;              // 0x1EB
    __int8  MissileBaseDoor;        // 0x1EC
    __int8  MissileBaseTimer;       // 0x1ED
    __int8  unused494[34];          // 0x1EE
    __int16 SubStoryProgress;       // 0x210 var 528
    __int8  XATMDefeated;           // 0x212
    __int8  UnusedVar1_Dollet;      // 0x213
    __int8  DolletFootsteps;        // 0x214
    __int8  TownLocalVars533[7];    // 0x215 vars 533-539 (Dollet/Timber/Esthar road+field flags)
    __int8  unused540[52];          // 0x21C
    __int8  AngleCharacterFacingControl[2]; // 0x250
    __int8  unused594;              // 0x252
    __int8  TownLocalVars595[30];   // 0x253 vars 595-624 (FH / D-District / Timber-Moomba; 614-615 hottest)
    __int8  BalambVisitedFlags;     // 0x271 var 625
    __int8  CityLocalVars626[66];   // 0x272 vars 626-691 (Balamb city / BG library / Winhill / Esthar city; 672-673 hottest)
    __int8  unused692[28];          // 0x2B4
    __int8  SquallCostume;          // 0x2D0 var 720
    __int8  ZellCostume;            // 0x2D1
    __int8  SelphieCostume;         // 0x2D2
    __int8  QuistisCostume;         // 0x2D3
    __int16 DolletMissionTime;      // 0x2D4
    __int16 TownVar726_SeedRankInput; // 0x2D6 var 726 (town conduct, read by bgrank1 SeeD-rank field)
    __int8  MultiPurposeVar2;       // 0x2D8 var 728 (multi-use, note 3)
    __int8  TownVar729_SeedRankInput; // 0x2D9 var 729 (town conduct, read by bgrank1)
    __int8  Flags1;                 // 0x2DA var 730
    __int8  unused731;              // 0x2DB
    __int16 FireCavernVar732_SeedRankInput; // 0x2DC var 732 (Fire Cavern time, written only by bdifrit1, read by bgrank1)
    __int8  SplitPartyFlags;        // 0x2DE var 734 (note 2)
    __int8  BGardenNPCVar735;       // 0x2DF var 735 (Balamb Garden interior NPC/state)
    __int8  unused736[16];          // 0x2E0
    __int8  RagnarokVar752;         // 0x2F0 var 752 (Ragnarok interior state, rg*)
    __int8  unused753[271];         // 0x2F1  (vars 753-1023, VERIFIED FREE - see note 6)
    __int8  tempVars[256];          // 0x400  (vars >=1024, temporary/scratch)
};
#pragma pack(pop)
```

## Function addresses

| Function | Address | Description |
|---|---|---|
| `VARMAP_START` | 0x1cfe9b8 | Global variable/data, not a function — base of the savemap variable block, typed `SavemapVariables` |
| `GetSeeDRankFromPoints` | 0x4C3090 | Converts SeeD rank points to displayed rank |
| `Battle_KeepMusicAfterBattle` | 0x52CE30 | Reads var 108 to decide whether to carry over field BGM after battle |
| `World_BuildObjectInstanceList` | 0x544860 | Renamed from `Wmset_SetupWorldmapVariant` in the community IDB; copies worldmap-variant vars into the worldmap state block |
| `funcs_52A647` | 0xb8de94 | Global variable/data, not a function — field script interpreter opcode dispatch table |
| `VAR_MAP_ADDRESS` | 0xb8ee90 | Global variable/data, not a function — pointer to the savemap variable block, used by non-script EXE consumers |
| Trigger-rect table | 0xC763D2 / 0xC763EE | Global variable/data, not a function — per-variant table overriding worldmap grid segments (0-767) with alternates (768-834) |
