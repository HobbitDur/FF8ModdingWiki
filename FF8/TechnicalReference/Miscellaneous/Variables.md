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
| Word        | 24          | *Unclear:* Copy of a battle counter stored between battles won and battles escaped, made when the game comes back from the world map. Nothing reads this copy. |
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
| Signed Byte | 86          | *Likely:* The vehicle the party was using on the world map when it entered the current field, as the world map's vehicle code; 0 to 9 means on foot. Field scripts read it to show the arrival car and to let the Missile Base guards react to it, and the world map writes it, not the fields. Values: 0 = On foot (0-9 are all on foot), 32 = Car; Missile Base guards let it pass, 34 = Balamb rental: sky blue van, 35 = Balamb rental: classic car, 38 = Deling City rental car, 40 = Esthar car, 48 = Balamb Garden (mobile). |
| Signed Byte | 87          | *Likely:* Sound state the engine copies when the game comes back from the world map. Scripts only load their field music while it is 0, and also test it for 10. |
| Signed Byte | 88          | *Likely:* 1 when the party has Siren's Move-Find. The engine refreshes it on field entry; save points and draw points read it to show themselves. Values: 0 = No Move-Find, 1 = Move-Find. |
| Byte        | 89-99       | unused in fields |
| Word        | 100         | *Unclear:* Word cleared to 0 by the opening logo script and never read by any field script; its purpose isn't clear. |
| Byte        | 102-103     | unused in fields |
| Long        | 104         | Engine switches. 8: no SeeD salary (SALARYOFF). 16: salary not shown (SALARYDISPOFF). 64: on-screen timer shown. 1024: random battles were on before a music load. |
| Signed Long | 108         | Handle of the music playing. -1 means there is no field music to carry over, so the music stops after a battle. |
| Signed Long | 112         | Handle of the second music channel, the one DUALMUSIC fills, -1 for none. MUSICLOAD only starts loading a track while it is -1. |
| Byte        | 116-147     | Draw points in field                                                                                                                                                                                                                                                                                                       |
| Byte        | 148-179     | Draw points in worldmap                                                                                                                                                                                                                                                                                                    |
| Word        | 180         | Draw point refill counter: grows with steps. At 10240 it resets and each used draw point may refill. |
| Word        | 182         | *Likely:* Flags of the BATTLEMODE opcode for this field. DISPTIMER sets bit 4 and KILLTIMER clears it while the timer shows; bit 256 keeps the timer's end from triggering its action. |
| Signed Word | 184         | *Likely:* Frames the SeeD salary message stays on screen after a payday. It counts down; 0 or less means no message, and most saves hold -1. A movie or a card game closes the message at once. |
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
| Word        | 218         | *Likely:* Screen fade: current value of the fade. |
| Word        | 220         | *Likely:* Screen fade: speed. |
| Word        | 222         | *Likely:* Screen fade: target red. |
| Word        | 224         | *Likely:* Screen fade: target green. |
| Word        | 226         | *Likely:* Screen fade: target blue. |
| Word        | 228         | *Likely:* Screen fade: state kept from the fade engine. |
| Word        | 230         | *Likely:* Screen fade: state kept from the fade engine. |
| Word        | 232         | *Likely:* Screen fade: state kept from the fade engine. |
| Word        | 234         | *Likely:* Screen fade: state kept from the fade engine. |
| Word        | 236         | *Likely:* Screen fade: state kept from the fade engine. |
| Word        | 238         | *Likely:* Screen fade: state kept from the fade engine. |
| Byte        | 240         | 1 when this field has a draw point set by SETDRAWPOINT, so a loaded save sets it again. |
| Byte        | 241         | Whether that draw point is visible, the value SETDRAWPOINT got. |
| Byte        | 242         | Number of the draw point of this field, from SETDRAWPOINTID. |
| Byte        | 243         | Abilities sealed by SEALEDOFF. A sealed ability's bit is set; 255 seals all. The game copies it to the map seal of the config. Bits: +1 Items sealed, +2 Magic sealed, +4 GF sealed, +8 Draw sealed, +16 Command abilities sealed, +32 Limit breaks sealed, +64 Resurrection sealed, +128 Saving sealed. |
| Long        | 244         | *Likely:* Angelo step counter: grows with steps. At 592 it resets and Angelo gets points, unless Angelo is disabled. |
| Byte        | 248-255     | Not investigated. **Note:** the worldmap-variant descriptions historically listed here (as 244–247) actually belong to offsets **264–267** — see below. These 12 bytes are `unk5` in the struct and their purpose is unverified. |
| Word        | 256         | Main Story quest progress. Both bytes are also copied into the worldmap state block (`+110`/`+111`) by `World_BuildObjectInstanceList` (renamed from `Wmset_SetupWorldmapVariant` in the community IDB), so the worldmap appearance can depend on story progress.                                                                                                                     |
| Byte        | 258         | *Likely:* Bit 1 would make Zell add the lines about Laguna coming to get Ward when he recounts his dream in the D-District Prison start; it is only ever set by the debug room, so in normal play the shorter version is told. Bits: +1 Zell tells Laguna-rescues-Ward part. |
| Byte        | 259-260     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 261         | Save point state shared by every field with a save point: bit 1 is on while the party stands on the save point, and bit 2 blocks the party-switch (PHS) menu there. Bits: +1 Standing on a save point, +2 Party switching disabled at save point. |
| Byte        | 262-263     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 264         | *Likely:* World map variant switches. Bit 8 on the normal world map and bit 16 on disc 4 change the map tiles (bit 64 of the mask): Balamb Garden moved. Scripts also set bits 1, 4 and 64 in story scenes. |
| Byte        | 265         | *Unclear:* World map state byte the engine copies on entering the world map. Field scripts set bits 1, 64 and 128 at story turns. |
| Byte        | 266         | World map story phase, 0 to 4. It selects which tile variants the world map shows; phase 4 starts with Rinoa's rescue in space on disc 3. |
| Byte        | 267         | Disc 4 world map variant: bits 1 and 2 select one of three tile sets. No field script writes it. |
| Byte        | 268         | *Likely:* World map state byte set from the story, with values 24, 41, 42 and 89. They match the track numbers the world map plays, so this is likely the world map's music. |
| Byte        | 269         | *Unclear:* World map state byte set to 1, 4, 5 or 7 at story turns, copied on entering the world map. |
| Byte        | 270         | *Unclear:* World map state byte, set to 6 once in ecpview2, copied on entering the world map. |
| Byte        | 271         | *Unclear:* World map state byte copied on entering the world map. No field script writes it. |
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
| Byte        | 321         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited first (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 322         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited second (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 323         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited third (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 324         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited fourth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 325         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited fifth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 326         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited sixth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 327         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited seventh (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 328         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited eighth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 329         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited ninth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 330         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited tenth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 331         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited eleventh (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 332         | *Likely:* Art gallery record in Ultimecia Castle: the number of the painting visited twelfth (0 if fewer paintings were visited). Each painting is added to the first empty slot only once, and the picture hall shows them in that order. Values: 0 = No painting yet, 1 = Ignus (Fire), 2 = Inandantia (Flood), 3 = Iudicium (Judgment), 4 = Intervigilium (Sleep), 5 = Venus (Love), 6 = Viator (Messenger), 7 = Vigil (Watchman), 8 = Vividarium (Garden), 9 = Inaudax (Cowardice), 10 = Xystus (Tree-lined Road), 11 = Xerampelinae (Red Clothes), 12 = Xiphias (Swordfish). |
| Byte        | 333         | *Likely:* Ultimecia Castle treasure room: bits record which of the four boxes (1 to 4) are open; touching a box toggles its bit, and once all four are open (15) the boss appears. It is set to 9 when the party arrives at the castle. Values: 15 = All four open; boss appears. Bits: +1 Box 1 open, +2 Box 2 open, +4 Box 3 open, +8 Box 4 open. |
| Byte        | 334         | Ultimecia Castle seals released: after beating a guardian the party picks one seal to release, and its bit is set. All eight set (255) changes the party's lines before Ultimecia's chamber. Values: 255 = Everything unsealed. Bits: +1 Item unsealed, +2 Magic unsealed, +4 GF unsealed, +8 Draw unsealed, +16 Command abilities unsealed, +32 Limit Break unsealed, +64 Resurrection unsealed, +128 Save unsealed. |
| Byte        | 335         | *Likely:* One-shot flag set to 1 in the Esthar space pod once the story has passed 3860; at that moment rare cards 77, 95, 97, 100 and 104 not owned by the player are moved back to the Queen of Cards. Values: 0 = Not done yet, 1 = Done. |
| Byte        | 336         | *Likely:* Deling City bus and driveway state. Bits 1 to 32 track the three bus lines while the party rides (get-off prompt up, player chose to get off); bit 64 is set at Caraway's Mansion gate event; bit 128 is set when the Deling rental office shows the arrival car. Bits: +1 Bus 0: get-off prompt shown, +2 Bus 0: player chose to get off, +4 Bus 1: get-off prompt shown, +8 Bus 1: player chose to get off, +16 Bus 2: get-off prompt shown, +32 Bus 2: player chose to get off, +64 Mansion gate event done, +128 Arrival car parked at rental office. |
| Byte        | 337         | *Likely:* Deling City one-time event bits. Bit 1 is set when General Caraway locks the party in his mansion (and lets the party move on afterwards), bit 2 when the hatch in the Presidential Residence corridor has been opened, and bits 4, 32, 64 and 128 when the matching switches in the Deling sewers have been used. Bits: +1 Caraway locked party in mansion, +2 Residence corridor hatch opened, +4 Sewer switch used (left), +32 Sewer switch used (lower room), +64 Sewer switch used (upper), +128 Sewer switch used (right). |
| Byte        | 338         | *Likely:* Deling sewer switches, second set: bits 1, 2, 32 and 64 are set by switches in the second sewer room and bits 4, 8 and 16 by switches in the third; the earlier rooms read them to know which gates are open. Two Balamb Town centre fields also test the whole byte as 0 or 1 to choose a movie. Bits: +1 Sewer switch used (room 2), +2 Sewer switch used (room 2), +4 Sewer switch used (room 3), +8 Sewer switch used (room 3), +16 Sewer switch used (room 3), +32 Sewer switch used (room 2), +64 Sewer switch used (room 2). |
| Byte        | 339         | *Likely:* Reused byte. In the Deling sewers bits 1, 2 and 4 mark switches used and bit 64 marks Weapons Monthly (May issue) as already taken; in the Centra Ruins tower bits 16 and 32 mark the left and right ladders used; in Caraway's Mansion bit 128 marks that the Ifrit card was given to Caraway, and bit 8 is only ever cleared. Bits: +1 Sewer switch used, +2 Sewer switch used, +4 Sewer switch used, +16 Centra tower: left ladder used, +32 Centra tower: right ladder used, +64 Weapons Monthly May taken (sewer), +128 Ifrit card given to Caraway. |
| Byte        | 340         | *Likely:* Reused scratch byte. In the Garden Festival fields it holds which SeeD (1 Quistis, 2 Selphie, 3 Irvine) goes with Xu to the front gate; in Squall's fistfight in Balamb Garden it counts punches (Deathblow unlocks at 3); in Fisherman's Horizon's concert fields it is the member being given an instrument (1 Zell, 2 Irvine, 3 Selphie, 4 Quistis); in the Deling sewers (1 to 25) it records which ladder or room the party last used; in Caraway's Mansion (1 to 12) it is Zell's escape-search step; in the desert fields it stores a party member. Values: 0 = Not set. |
| Byte        | 341         | *Likely:* Reused scratch byte. In Caraway's Mansion it is Selphie's escape-search step (1 to 9) that changes her dialogue; at the Fisherman's Horizon concert it is set from the band's instrument lineup (0 to 3) and later read on the roof to vary Rinoa's lines; in the desert road it stores a party member; the Balamb Garden classroom attack resets it to 0. Values: 0 = Not set.<sub>5</sub> |
| Byte        | 342         | Deling City bus route in progress: the number of the stop-to-stop leg the bus is travelling (1 to 16), set when the player boards and cleared to 0 when the bus arrives. It tells each stop's scene where the bus comes from. |
| Byte        | 343         | *Likely:* Galbadia Garden event bits. Bit 1 is set after the waiting scene in the dorm room and starts the Raijin and Fujin meeting in the hall, which then sets bit 2; bits 16, 32 and 64 mean Card Keys 1, 2 and 3 have been received during the later infiltration (they unlock the matching doors and the elevator); bit 128 means a ground-floor door lock has been opened; bit 4 marks Irvine's talk in the viewing area. Bits: +1 Dorm waiting scene done, +2 Raijin and Fujin met in the hall, +4 Irvine talked in the viewing area, +16 Card Key 1 received, +32 Card Key 2 received, +64 Card Key 3 received, +128 Ground-floor door lock opened. |
| Byte        | 344         | *Likely:* Event bits for the two Gardens during the Garden-versus-Garden fight. Bits 1, 2, 4 and 8 are Balamb Garden talks already done (trainees questioned, junior classman's Cottage given, Zell's lines at the gate); bits 16, 32, 64 and 128 are Galbadia Garden progress (elevator door unlocked, Lock 3 door opened, hall monster beaten). Bits: +1 BG: first trainee questioned, +2 BG: second trainee met, +4 BG: Cottage taken from classman, +8 BG: classman at 2F spoken to, +16 GG: elevator unlocked (step 1), +32 GG: Lock 3 door opened, +64 GG: elevator unlocked (step 2), +128 GG: hall monster beaten. |
| Byte        | 345         | *Likely:* Mixed event bits. Bit 8 is on while the Odin timer runs in the Centra Ruins and is cleared when it ends; bits 16, 32, 64 and 128 mean Galbadia Garden's Lock 1, Lock 2 (two doors) and Lock 3 doors have been opened; bit 4 means the Solomon Ring was taken in Esthar; bit 1 marks a one-time scene already played in the Fisherman's Horizon concert area. Bits: +1 FH one-time scene done, +4 Solomon Ring taken, +8 Odin timer running (Centra Ruins), +16 GG: Lock 1 door opened, +32 GG: Lock 2 door opened, +64 GG: Lock 2 door opened, +128 GG: Lock 3 door opened. |
| Byte        | 346         | Instrument chosen for Zell in the Fisherman's Horizon concert band, picked from a list of eight; the same instrument cannot be given to two members, and the lineup decides how the concert goes. Values: 0 = None chosen, 1 = Guitar, 2 = Sax, 3 = Electric Guitar, 4 = Piano, 5 = Violin, 6 = Flute, 7 = Bass Guitar, 8 = Tap (dance). |
| Byte        | 347         | Instrument chosen for Irvine in the Fisherman's Horizon concert band, picked from a list of eight; the same instrument cannot be given to two members, and the lineup decides how the concert goes. Values: 0 = None chosen, 1 = Guitar, 2 = Sax, 3 = Electric Guitar, 4 = Piano, 5 = Violin, 6 = Flute, 7 = Bass Guitar, 8 = Tap (dance). |
| Byte        | 348         | Instrument chosen for Selphie in the Fisherman's Horizon concert band, picked from a list of eight; the same instrument cannot be given to two members, and the lineup decides how the concert goes. Values: 0 = None chosen, 1 = Guitar, 2 = Sax, 3 = Electric Guitar, 4 = Piano, 5 = Violin, 6 = Flute, 7 = Bass Guitar, 8 = Tap (dance). |
| Byte        | 349         | Instrument chosen for Quistis in the Fisherman's Horizon concert band, picked from a list of eight; the same instrument cannot be given to two members, and the lineup decides how the concert goes. Values: 0 = None chosen, 1 = Guitar, 2 = Sax, 3 = Electric Guitar, 4 = Piano, 5 = Violin, 6 = Flute, 7 = Bass Guitar, 8 = Tap (dance). |
| Word        | 350         | *Likely:* Maximum value of Squall's health bar in the Balamb Garden fistfight against a Galbadian soldier (600 plus a bonus read from variable 380). |
| Word        | 352         | *Likely:* Maximum value of the Galbadian soldier's health bar in the Balamb Garden fistfight, set to 600. |
| Signed Word | 354         | *Likely:* Squall's current health in the Balamb Garden fistfight against a Galbadian soldier; it starts at his maximum, drops when he is hit, and the fight is lost when it reaches 0. |
| Signed Word | 356         | *Likely:* The Galbadian soldier's current health in the Balamb Garden fistfight; it starts at 600, drops when Squall hits him, and he is beaten when it reaches 0. |
| Byte        | 358         | *Likely:* Mixed event bits. Bit 128 means the Odin encounter in the Centra Ruins is over (won or run out of time) and bit 32 that Odin was beaten; bits 1, 4 and 8 are Lunar Base progress with Ellone (moonscope used, Ellone says she can't send Squall to Rinoa, Ellone placed in the control room); bit 64 marks Raijin's talk in Galbadia Garden's road; bit 16 marks Selphie's one-time scene in Balamb Garden. Bits: +1 Moonscope used (Lunar Base), +4 Ellone refused to send Squall to Rinoa, +8 Ellone in Lunar Base control room, +16 Selphie scene in Balamb Garden done, +32 Odin defeated, +64 Raijin talk in Galbadia road done, +128 Odin encounter over (win or timeout). |
| Byte        | 359         | *Likely:* Centra Ruins puzzle state. Bits 1 and 2 are the left and right eyes put into the tower statue and bits 4 and 8 the left and right eyes of the roof statue; bit 32 is set once the right eye combination is accepted; bit 64 means the tower console was used and bit 128 the power switch was pulled; bit 16 is set when the Centra Ruins view scene starts. Bits: +1 Tower statue has left eye, +2 Tower statue has right eye, +4 Roof statue has left eye, +8 Roof statue has right eye, +16 Ruins entry scene started, +32 Eye code accepted, +64 Tower console used, +128 Power switch pulled. |
| Long        | 360         | *Likely:* Music-part mask for the Garden Festival concert at Fisherman's Horizon: each of the four music choices (variables 346-349) switches on a set of music channels, and the combined mask is given to the music engine when the show starts. It is reset to 0 when the concert scene is left. |
| Byte        | 364         | The first digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 365         | The second digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 366         | The third digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 367         | The fourth digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 368         | The fifth digit (0-9) of the five-digit code in the Centra Ruins statue puzzle. It is rolled at random when the stone in the Sphinx room is pushed; the roof room shows the code once the statue has both eyes, and the tower room accepts it when the same digits are entered. |
| Byte        | 369         | *Likely:* Several unrelated one-bit events share this byte. Bits 1, 2 and 4 mark sewer ladders already used in Deling City (glwater2, glwater3). Bit 8 marks the Lunar Base passage crew member already spoken to. Bit 16 marks the Wilderness gate scene near Ultimecia's Castle as played. Bits 32, 64 and 128 are short-lived triggers in the Ultimecia Castle Elevator Hall that make the incoming party walk in after a party switch. Bits: +1 Sewer ladder used (glwater3), +2 Sewer ladder used (glwater2), +4 Sewer ladder used (glwater2, 2nd), +8 Lunar Base passage crew talked to, +16 Wilderness gate scene played. |
| Byte        | 370         | *Likely:* In Ultimecia's Castle, where the party that is not being controlled waits when the parties are split. Party switch points use it to jump to that room and then store the room just left; 0 means the parties are not split. Values: 0 = Parties not split, 1 = Hall, 2 = Stairway Hall (felfst1), 3 = Elevator Hall (felrele1), 4 = Elevator Hall (felrele1, 2nd spot), 5 = Stairway Hall (ferrst1), 6 = Stairway Hall (ferfst1), 7 = Courtyard, 8 = Grand Hall, 9 = Elevator Hall (elevator). |
| Byte        | 371         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 372         | *Likely:* Ultimecia's Castle guardian fights. Each bit is set after the guardian of one room has been fought off, and that guardian is then removed from its room. The Art Gallery and Prison Cell bits work the other way round: they are set to make the guardian appear (after reading the painting title, or taking the Prison Key) and cleared after the fight. Bits: +1 Hall guardian beaten, +2 Terrace guardian beaten, +4 Treasure Room guardian beaten, +8 Wine Cellar guardian beaten, +16 Art Gallery guardian appears, +32 Armory guardian beaten, +64 Prison guardian appears (key taken), +128 Clock Tower guardian beaten. |
| Byte        | 373         | Ultimecia's Castle key and hatch flags: one bit per key picked up, plus a hatch in the Grand Hall. Bits: +1 Floodgate Key obtained, +2 Treasure Vault Key obtained, +4 Armory Key obtained, +8 Prison Key obtained, +16 Grand Hall floor hatch broken open. |
| Byte        | 374         | *Likely:* Ultimecia's Castle door and timer flags: doors opened with their keys, the Prison auto-lock, and the countdown started by ringing the bell, which the timer script in every castle room checks. Bits: +1 Treasure Vault door unlocked, +8 Armory door unlocked, +32 Prison auto-lock disengaged, +64 Bell countdown running, +128 Omega Weapon beaten. |
| Byte        | 375         | *Likely:* Ultimecia's Castle puzzle flags: the floodgate and its water release, a picture riddle in the Art Gallery, the Treasure Room guardian's appearance and the Rosetta Stone pickup. Bits: +1 Floodgate unlocked with the key, +2 Flood released into the waterway, +8 Art Gallery picture riddle read, +16 Treasure Room guardian has appeared, +32 Rosetta Stone taken. |
| Byte        | 376         | *Likely:* Where the Armory Key is while it floats in the Ultimecia's Castle waterway: it starts near the Clock Tower bridge and is carried to the Waterway or the Flood Gate depending on whether the flood was released. Values: 0 = At the Clock Tower bridge, 1 = Washed into the Waterway, 2 = At the Flood Gate. |
| Byte        | 377         | *Likely:* Notes played on the organ in the Chapel of Ultimecia's Castle: one bit per note (DO, RE, MI, FA). The Passageway room (fewater1) reacts to each note, and all four together (15) trigger its final effect. Bits: +1 DO played, +2 RE played, +4 MI played, +8 FA played. |
| Byte        | 378         | Stage of Odin's countdown in the Centra Ruins. It starts at 0 and rises as the timer runs down, making Odin speak a new taunt each stage; when the time is up he kills the party and sends it back to Dollet Harbor. Values: 0 = Countdown not started, 1 = Odin: 'I am Odin...', 2 = Odin: 'To him who doth vanquish me...', 3 = Odin: 'Come hither, knight-errant...', 4 = Odin: 'Two knights, but one victor.', 5 = Odin: 'Thou must use thy wits...', 6 = Odin: 'Behold, thy doom is near.'. |
| Byte        | 379         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 380         | Bonus health for Squall in the Balamb Garden fistfight: each lost try adds 200, up to 5000, so the fight gets easier. His bar starts at 600 plus this; the soldier's stays at 600. |
| Byte        | 382-383     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 384         | *Likely:* Early Balamb Garden flags: whether the dorm computer is switched on, and whether Quistis has given Squall his first GFs (Quetzalcoatl and Shiva) and the GF tutorial. Bit 4 is only used in the test7 debug room. Bits: +1 Dorm computer switched on, +2 GFs given and named (GF tutorial done). |
| Byte        | 385         | *Likely:* Progress of Laguna's scenes in the Deling City club. Both bits are set during play, not just bit 2. Bits: +1 Laguna's first club talk done, +2 Laguna's second club talk done. |
| Byte        | 387         | *Likely:* Progress of Laguna's stay in Winhill; it goes up in steps of 2 as scenes are completed, from 0 at the start to 26 at the end of the first day's patrol. Values: 4 = Ellone greets Laguna, 18 = First patrol finished, 20 = Kiros mentions Timber Maniacs, 22 = Laguna wants to stay in Winhill, 26 = Patrol report given to Raine. |
| Byte        | 388         | Talk flags in the Timber Maniacs lobby: the receptionist and the magazine pile. Bits: +1 Receptionist greeted, +2 Receptionist visit repeated, +4 Girl Next Door magazine taken. |
| Byte        | 389         | Which topic Squall picked when talking to the Timber Maniacs editor-in-chief; the following room plays a scene according to it. It is reset to 0 at the start of each chat. Values: 0 = No topic yet, 2 = About Timber Maniacs, 4 = The dream with Laguna, 6 = About Timber's situation. |
| Byte        | 390         | How far Squall has got in talking with Edea in her house's backyard: 0 until she has told him where the White SeeD ship may be and handed him her letter. Values: 0 = White SeeD ship not asked about, 1 = Edea gave the letter and the ship hint. |
| Byte        | 391         | *Likely:* Talk flags for Laguna in his Presidential Palace office (Disc 3), covering his greeting, the story he tells of the past and Ellone's scene. Bits: +1 Laguna's greeting talk done, +8 Laguna finished telling his story, +16 Flashback story just played. |
| Byte        | 392         | *Likely:* Reused: in Edea's house backyard bits 1, 2 and 4 record which of her speeches Squall's party has heard; bit 8 is a short-lived marker set when the dorm computer screen opens in Balamb Garden and cleared by the dorm room afterwards. Bits: +1 Edea spoke about Sorceress Adel, +2 Edea spoke to Rinoa about sorceress, +4 Edea advised Rinoa to find a knight, +8 Just left the dorm computer. |
| Byte        | 393-399     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Long        | 400         | Number of enemies killed (variable 68) as it stood when the Winhill patrol began; the report to Raine later subtracts it from the count at the end. |
| Long        | 404         | Number of enemies killed (variable 68) as it stood when Laguna returns from his Winhill patrol; the difference with variable 400 is the 'monsters exterminated' count in his report. |
| Byte        | 408         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 409         | *Likely:* 'New entry' marks on the Balamb Garden computer. A bit is set once the matching section has been read, which removes its NEW mark. Bits: +1 Notices read, +2 Pals messages read, +4 Diary read. |
| Byte        | 410-431     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 432         | *Likely:* Balamb Garden Hall flags for the scenes after the Dollet SeeD exam: whether Xu has praised Squall and whether Headmaster Cid has asked him about the battlefield. Other bits (4, 64) are also set in the Hall but their purpose isn't clear. Bits: +8 Xu praised the exam result, +32 Cid asked about the battlefield. |
| Byte        | 433         | *Likely:* Balamb Garden story flags for the first disc (the day of the SeeD exam and the evening that follows); several bits are reused later. Bit 2 is read by the Garden staff who say it is after-hours and only the training center is open, and is cleared when Selphie announces the first SeeD mission. Bits: +2 After-hours: Garden facilities closed, +4 Cid gave the SeeD exam briefing, +16 Selphie showed Squall around (dorm). |
| Byte        | 434         | *Likely:* Balamb Garden flags for the SeeD exam day, mostly the meeting with transfer student Selphie and the tour of Garden; bit 128 is reused later for Xu's greeting. Bits: +16 Selphie met (tour offer seen or over), +32 Showing Selphie around Garden, +128 Xu's greeting heard. |
| Byte        | 435         | *Likely:* Balamb Garden talk flags for students and staff in the 2F classroom area, the hallway and the infirmary; each bit remembers that a particular character has spoken. Bits: +1 Classmate's gunblade chat done, +2 Boy at the 'Do Not Open' door spoke, +4 Cid spoke in the infirmary, +128 Hall boy's playing-card story heard. |
| Byte        | 436         | *Likely:* Event flags for D-District Prison and the Moomba who helps there: the rescue of the Moomba, the fight with the Warden, the meeting with Joker, and the two gifts the Moombas give. Joker's bit is also checked in the Garden training center. Bits: +1 Moomba saved in the prison, +2 Warden fought and beaten, +32 Joker introduced himself, +64 Moomba gave the Cottage, +128 Moomba gave the Rename Card. |
| Byte        | 437         | Reused. In D-District Prison it is the current stage of the prison tower (0 to 13), shown on the elevator panel as 'Floor N'. On Disc 2 in Balamb Garden it is a bitmask of the party members who join Squall (bit 1 Zell, 2 Irvine, 4 Rinoa, 8 Quistis). On the Ragnarok it counts fights with the alien monsters, ending past 24. Bits: +1 Zell joins (Garden, Disc 2), +2 Irvine joins (Garden, Disc 2), +4 Rinoa joins (Garden, Disc 2), +8 Quistis joins (Garden, Disc 2). |
| Byte        | 438         | *Likely:* Balamb Garden 'Cid vs Norg' event flags (Disc 2): fights with Garden Faculty at several spots, items handed out, and whether Squall sided with the Headmaster. Bits: +1 Faculty fight at Gate 2, +2 Faculty fight at Gate 5, +4 Item received at Gate 6, +16 Faculty fight on Road 5, +32 Faculty fight on Road 7, +64 'Cid isn't here' event ended, +128 Declared as Cid's follower. |
| Byte        | 439         | *Likely:* More Balamb Garden 'Cid vs Norg' flags (Disc 2): faculty fights, items from students and the sighting of Cid's hologram. Bits: +1 Library student gave items, +2 Faculty fight on Road 2, +4 Cid's hologram seen, +8 Parking student gave a Tent, +16 Faculty fight on Road 1, +32 Cafeteria student gave Gysahl Greens, +128 Faculty fight in bgkote3a. |
| Byte        | 440         | *Likely:* Balamb Garden event flags for the Disc 2 attack: items given by students, the Nida and Kadowaki conversations and the Road 4 incident. Bits 1, 4, 8, 32 and 128 mark scenes at the quad, the infirmary and the training center whose exact purpose isn't clear. Bits: +2 Quad student gave an X-Potion, +16 Nida talked to, +64 Dr. Kadowaki gave the Elixir. |
| Byte        | 441         | *Likely:* Balamb Garden 'Cid vs Norg' flags (Disc 2): student gifts and scenes in the hall and the Quad. A debug menu sets it to 7 for 'complete all'. Bits: +4 Training center student gave a Remedy, +8 Xu scene in the hall played, +16 Library student spoke. |
| Byte        | 442         | *Likely:* Progress of Rinoa's tour of Balamb Garden on Disc 2. Bits: +1 Tour with Rinoa started, +2 Rinoa's 'This place is huge' line seen. |
| Word        | 443         | *Unclear:* No vanilla field script reads or writes it, so it is not set in normal play; its purpose isn't clear. |
| Byte        | 445         | *Likely:* Ragnarok state byte used while the alien monsters are hunted through its rooms. Bit 1 is set when the security lock is released, bit 2 by a trigger in rgroad3, and bit 4 flips during the chase. Bits: +1 Ragnarok security lock released. |
| Byte        | 446         | *Likely:* One bit per Ragnarok room, set when the alien monster of that room has been fought off, so it cannot be fought again until it is cleared by a later fight. 255 means all of them are finished. Bit order: 1 rgair1, 2 rgroad1, 4 rgroad2, 8 rgroad3, 16 rghang1, 32 rghang2, 64 rgexit1, 128 rgguest2. Bits: +1 rgair1 alien fought off, +2 rgroad1 alien fought off, +4 rgroad2 alien fought off, +8 rgroad3 alien fought off, +16 rghang1 alien fought off, +32 rghang2 alien fought off, +64 rgexit1 alien fought off, +128 rgguest2 alien fought off. |
| Byte        | 447         | *Likely:* The Ragnarok room where the alien monster was last fought, as a single bit (same bit order as variable 446). Bits: +1 Last fight in rgair1, +2 Last fight in rgroad1, +4 Last fight in rgroad2, +8 Last fight in rgroad3, +16 Last fight in rghang1, +32 Last fight in rghang2, +64 Last fight in rgexit1, +128 Last fight in rgguest2. |
| Signed Word | 448         | *Likely:* Copy of the main story progress (variable 256) saved when the Balamb Garden 2F classroom conversation about the girl with a cold is played; the girl's script compares it with the current progress to know whether the story has moved on. |
| Byte        | 450         | Records which one-time pickups have been taken: the Magical Lamp from Headmaster Cid, two Weapons Monthly issues in Balamb Garden, and several items in the D-District Prison area. A set bit stops the item from being given again. Bits: +1 Magical Lamp from Cid taken, +2 Weapons Monthly, April taken, +4 Weapons Monthly, July taken, +8 Tent taken (prison), +16 Pet House taken (prison), +64 HP Up taken (prison), +128 Luck Up taken (prison). |
| Byte        | 451         | Records which one-time pickups have been taken in the D-District Prison area and in the Esthar road areas visited as Laguna. A set bit stops the item from being given again. Bits: +1 Combat King 001 taken (prison), +2 Combat King 005 taken (Esthar), +4 Pet Nametag taken (prison), +8 Strength Up taken (prison), +16 Power Generator taken (Esthar), +32 Phoenix Pinion taken (Esthar), +64 LuvLuv G taken (Esthar), +128 Spd-J Scroll taken (Esthar). |
| Byte        | 452         | *Likely:* Event flags for the Lunatic Pandora approach in Laguna's Esthar sequence: the Biggs and Wedge scene inside, the first visit to Adel's chamber, and the scene at the Pandora gate. Bits: +1 Biggs and Wedge scene seen, +2 Adel's chamber first-visit scene seen, +8 Pandora gate scene played. |
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
| Byte        | 480         | *Likely:* Stage of the Balamb Garden classroom scene before the SeeD exam: 2 once Quistis has begun the class and 4 once the students have moved to their study-hall places. The students' positions follow it. Values: 2 = Class begun, 4 = Students in study-hall places. |
| Byte        | 481         | *Likely:* Tracks which story stage's complaining-students conversation in the Garden cafeteria has been heard. Each bit is set when the student's line for that stage is read, so the other students react accordingly. Bits: +1 Heard 'Sad people' talk (earliest), +2 Heard 'Paper Test Boy' talk, +4 Heard 'Never expected this' talk, +8 Heard 'We are SaaaaaaD' talk, +16 Heard 'Sometimes I enjoy it' talk. |
| Signed Word | 482         | Error ratio of the missiles, set at the Missile Base monitor room. It starts at 0, goes down by 6 per press up to -150, which is the maximum error ratio. Values: -150 = Maximum error ratio, 0 = No error. |
| Byte        | 484         | Missile Base mission progress. The monitor-room bits record the error ratio and data upload, the alarm bit rings when the party is caught or the self-destruct starts, and several bits feed the SeeD points of the mission. Bits: +1 Error ratio set to maximum, +2 Equipment check/data upload done, +4 Alarm sounding, +8 Cover blown (disguises dropped), +32 Launcher pushed into position, +128 Control room entered. |
| Byte        | 485         | *Likely:* Tomb of the Unknown King flags. Bits 1, 4, 16, 64 and 128 are set together by the 'Float!' scene at the viewing spot, which removes the students there. Bit 2 is set by the Sacred and Minotaur fight in room 4, which removes those monsters from the room. Bits: +2 Sacred and Minotaur fight done. |
| Byte        | 486         | Current position in the Tomb of the Unknown King maze, used to decide where each passage leads. 0 is the entrance and 73 to 76 mark rooms 1 to 4. Values: 0 = Tomb entrance, 73 = Room 1, 74 = Room 2, 75 = Room 3, 76 = Room 4. |
| Byte        | 487         | Balamb Garden classroom bit 1 and Missile Base penalties. Bit 1 is set while Squall sits at his classroom seat; bits 16 and 32 each reduce the SeeD points paid after the Missile Base mission. Bit 64 is set by the control room soldier scene. Bits: +1 Squall seated in classroom, +16 Gave maintenance man the wrong message, +32 Party caught as intruders. |
| Byte        | 488         | Marks which inactive party members stand where after the party splits (the Missile Base group on one side, the others in Fisherman's Horizon and the cafeteria). Each of Irvine, Quistis, Rinoa and Zell has a low and a high bit, so two members do not stack in the same place. Bits: +1 Irvine, first place, +2 Quistis, first place, +4 Rinoa, first place, +8 Zell, first place, +16 Irvine, second place, +32 Quistis, second place, +64 Rinoa, second place, +128 Zell, second place.<sub>1</sub> |
| Byte        | 489         | *Likely:* One-time conversation flags: the Fisherman's Horizon talk with Mayor Dobe and the cafeteria lady's lost son, Rinoa's goodbye, and the camouflage panel test in Esthar (bits 4 and 8 set together). Bits: +1 Rinoa left after FH talk, +2 Mayor Dobe talk finished, +32 Told the son the Garden is here, +64 Son identified as cafeteria lady's, +128 Cafeteria lady told of her son. |
| Byte        | 490         | *Likely:* State of the disciplinary committee scene in the Balamb Garden cafeteria with Seifer, Fujin and Raijin. Bits: +1 Fujin dismissed Squall ('Ignore'), +2 Raijin whispered to Squall. |
| Byte        | 491         | *Likely:* Tomb of the Unknown King room progress: one bit per room puzzle or fight, tested by the maze passages and rooms to reopen or change the routes. Bits: +2 Room 1 event done, +4 Room 2 puzzle done, +8 Room 3 gearwheel turned, +16 Room 4 fight started, +32 Room 4 arc opened. |
| Byte        | 492         | Missile Base self-destruct and ID card flags. Bits 1, 2, 4 and 8 record the chosen countdown (10, 20, 30 or 40 minutes); the higher bits track the control room exit door, the missile-fired scene and the wounded soldier. Bits: +1 10-minute countdown chosen, +2 20-minute countdown chosen, +4 30-minute countdown chosen, +8 40-minute countdown chosen, +16 Control room exit door opened, +32 Missile-fired scene played, +64 ID Card taken from soldier, +128 Wounded soldier talked to. |
| Byte        | 493         | Set to 15 when the Missile Base self-destruct countdown starts; maps combine it with the countdown bits of the previous variable to tell that a timer is running and blow the base when it ends. Values: 0 = No countdown running, 15 = Countdown running. |
| Byte        | 494-527     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 528         | *Likely:* Progress counter for separate story segments, reused by each: the Dollet SeeD exam (2 to 12), Laguna's patrol (500, 510), the Timber missions (100 to 206), the White SeeD ship (700 to 740) and Laguna's Esthar prison and lab (1000 to 1120). Values: 8 = Dollet exam: in town, 12 = Dollet exam: mountain, 100 = Timber hideout: first scene done, 102 = Timber: Rinoa reunion done, 108 = Timber: abduction plan explained, 150 = Timber: before fake president fight, 170 = Timber: abduction plan failed, 174 = Timber: ready for TV station, 500 = Laguna's patrol begun, 700 = White SeeD ship reached, 730 = White SeeD leader's story told, 1014 = Laguna in Esthar prison. |
| Byte        | 530         | *Likely:* Event flags for the Dollet SeeD exam, read when the SeeD rank is worked out. The crab fight adds points unless the pub escape bit is set. Bits: +32 Squall jumped off the cliff, +64 Crab beaten, +128 Escaped through the pub. |
| Byte        | 531         | Read only at the Dollet seaside, where a value of 1 changes the opening scene. Only the debug rooms ever set it, so in normal play it stays 0. Values: 0 = Normal, 1 = Alternate seaside opening (debug only). |
| Byte        | 532         | *Likely:* Selects the footstep sound set used in Dollet: 0 on the beach side and 1 in the town. It is switched on a line across the town gate and set when the town loads. Values: 0 = Beach footsteps, 1 = Town footsteps. |
| Byte        | 533         | *Likely:* Dollet event flags: forcing past the guard, the pub card player, the pub owner's cards, and the hotel clerk's accent chat. Bit 64 is toggled during the painter's boy and dog events. Bits: +2 Forced way past Dollet guard, +8 Pub card player beaten, +16 Pub owner gave cards, +32 Hotel clerk accent talk done. |
| Byte        | 534         | *Likely:* Dollet painting and buried-treasure hunt flags. After seeing each of three paintings in the painter's house, a dog at the matching spot digs up an item. Bits: +2 Saw painting 1, +4 Dog's treasure 1 received, +8 Saw painting 2, +16 Dog's treasure 2 received, +32 Saw painting 3, +64 Dog's treasure 3 received. |
| Byte        | 535         | *Likely:* Timber one-time event flags. The boy who asks whether to give up uses bits 32 and 64; other bits mark Timber scenes at the gate, TV station and houses. Bits: +32 Boy asked whether to give up, +64 Boy gave Pet Nametag. |
| Byte        | 536         | *Likely:* Timber and Dollet one-time event flags: Big Brother's speech, the secret savings in a cupboard, and two magazines. Bits: +1 Big Brother's talk heard, +32 Took 500 Gil from cupboard, +64 Pet Pals Vol. 2 taken, +128 Occult Fan II taken (Dollet). |
| Byte        | 537         | *Likely:* Laguna's Esthar road escape: records the lost keys and the traps Laguna sets (hatch, small boulder, big boulder, about-to-fall boulder). The fights near the exit depend on which traps were prepared. Bits: +1 Key 1 event, +2 Key 2 event, +4 Hatch trap set, +8 Small boulder trap used, +16 Big boulder trap used, +32 Boulder about to fall. |
| Byte        | 538         | *Likely:* Event flags of Laguna's Esthar sequence and the Esthar lab: tampering with the hatch levers, ladders in the Laguna field maps and one magazine pickup. Bits: +2 Hatch lever 1 tampered with, +8 Hatch lever 2 tampered with, +128 Weapons Monthly first issue taken. |
| Byte        | 539         | *Likely:* Event flags from Laguna's Esthar sequence and the White SeeD ship. Bit 8 marks the third hatch lever; the ship bits mark Zone's book, Watts's news about Ellone and a joke heard. Bits: +8 Hatch lever 3 tampered with, +32 Gave Zone 'The Girl Next Door', +64 Watts told about Ellone leaving, +128 White SeeD meat joke heard. |
| Byte        | 540-591     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 592         | *Likely:* Stage counter for the train scenes (Timber-bound train and the other trains) in the bvtr maps. The values rise through the ride and set the cast positions; 50 is the arrival announcement for Timber. Values: 50 = Arrival announcement for Timber, 100 = Train scene start. |
| Byte        | 594         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 595         | *Likely:* Remembers which way the party left the last Fisherman's Horizon bridge, roof or fishing area, or Deep Sea tower floor, so the next map puts them at the matching entrance. Values: 1 = Went down, 8 = Moved between Deep Sea tower floors. |
| Byte        | 596         | *Likely:* Set to 1 after Quistis has explained the GF junction tutorial at the Balamb Garden gate, so the explanation is not repeated. Values: 1 = Junction tutorial shown. |
| Byte        | 597         | Set to 1 when the party pays at the Fisherman's Horizon hotel counter and goes to sleep, and back to 0 when Squall wakes in the room. Values: 0 = Not resting, 1 = Resting at hotel. |
| Byte        | 598         | *Unclear:* Single-value stage marker (1, 2, 4, 8, 16, 32, 64 or 128) set in different Fisherman's Horizon scenes around the Master Fisherman and the fishing shop and tested for equality; its exact purpose isn't clear. |
| Byte        | 599         | *Likely:* Two uses. At Fisherman's Horizon it records which of the two lift-operator brothers Squall has talked to (1 top, 2 bottom). In the Chocobo Forest it records the chocobo state: 32 once a chocobo is found and 64 once Squall rode it out. Values: 1 = Talked to top lift brother, 2 = Talked to bottom lift brother, 32 = Chocobo found (forest), 64 = Rode chocobo out (forest). |
| Byte        | 600         | *Likely:* Fisherman's Horizon sequence about the Garden repair and Irvine with the technicians, advancing one step each time: the lift ride, the roof, the technicians' 'It's working!' and the deck reaction. Values: 1 = Lift ride up, 2 = On the roof, 4 = Irvine meets technicians, 8 = 'It's working!' scene, 16 = Deck 6 reaction scene, 32 = Back in FH town. |
| Byte        | 601         | *Likely:* Progress through a chain of scenes in Fisherman's Horizon with the Master Fisherman, the Shopkeeper, the Fisherkid and Kazu. The Shumi Village workshop also reads it and shows the Master Fisherman once it reaches 16 or more. Values: 1 = Master Fisherman says "Follow me", 8 = Master Fisherman meets the Shopkeeper, 16 = Shopkeeper scene played, 32 = Kazu talks to Irvine on the bridge, 64 = Kazu says he will do something, 128 = Fisherkid practice scene played. |
| Byte        | 602         | *Likely:* Deep Sea Research Center puzzle: layout of tower level 3. It is 1 after the reset at level 1, then the level sets 2, 4 or 8 from the Reserve Steam Pressure the player arrives with (12, 14 or 15). Later values record the Steam Room. Values: 1 = Not chosen yet (after reset), 2 = Chosen when pressure was 12, 4 = Chosen when pressure was 14, 8 = Chosen when pressure was 15, 16 = Steam Room door opened, 32 = Steam Room already used to refill. |
| Byte        | 603         | *Likely:* Deep Sea Research Center puzzle: layout of tower level 4. It is 1 after the reset at level 1, then the level sets 2, 4 or 8 from the Reserve Steam Pressure the player arrives with. Values: 1 = Not chosen yet (after reset). |
| Byte        | 604         | *Likely:* Deep Sea Research Center puzzle: layout of tower level 5. It is 1 after the reset at level 1, then the level sets 2, 4 or 8 from the Reserve Steam Pressure and layout of the level above. Values: 1 = Not chosen yet (after reset). |
| Byte        | 605         | *Likely:* Progress through the end of the Deep Sea Research Center: reset at level 1, opening the door to the ocean deposit, the ruins, and the final battle. From 32 on, random battles in the tower and ruins are switched off. Values: 1 = Level 1 reset done, 2 = Zell forced door; ruins have battles, 4 = Door opened with 4 steam pressure, 8 = Operation at the ruins confirmed, 16 = Excavation resuming, 32 = Final battle won. |
| Byte        | 606         | *Likely:* One-time gift flags: a bit is set when an NPC has handed over its item. Used in Fisherman's Horizon and once in Shumi Village; a few scripts overwrite the whole byte, so bits can be lost. Bits: +1 Master Fisherman gave Occult Fan III, +2 Master Fisherman gave a Megalixir, +4 Grease Monkey gave a Mega Phoenix, +8 Grease Monkey gave a Phoenix Down, +16 Galbadian officer gave 5 Fast Ammo, +64 Shumi Elder gave a Status Guard. |
| Byte        | 607         | *Likely:* Progress of the Shumi Village job of finishing the Laguna statue (Sculptor, Elder's Attendant, Artisan). Fisherman's Horizon mechanic Genba also uses it, because he provides the Moomba doll that wins Artisan over. Values: 1 = Attendant has started helping, 2 = Elder says one more helper is needed, 4 = Squall must win over Artisan, 8 = Genba gave the Moomba doll, 16 = Artisan heard Genba's message, 32 = Artisan agreed to help, 64 = Statue finished, 128 = Attendant ready to show it to Elder. |
| Byte        | 608         | *Likely:* Progress of Squall's dealings with the Sculptor and the Elder in Shumi Village, ending with the five-stone search and the Elder's reward. Values: 1 = Saw the Laguna statue in the workshop, 4 = Met the Elder, 16 = Sculptor asked for the five stones, 32 = Stone search under way, 64 = Stone search complete, 128 = Elder gave the Phoenix Pinion. |
| Byte        | 609         | *Likely:* Shumi Village stone search: the stone the Sculptor is currently asking for. The Specialist at the gate gives hints according to it. Values: 8 = Asking for the life stone, 16 = Asking for the shadow stone, 32 = Asking for the water stone, 64 = Pond stone refused; water stone needed, 128 = All stones delivered. |
| Byte        | 610         | *Likely:* Shumi Village stone search: the stone Squall has just found and takes to the Sculptor, who checks it against his request. Values: 1 = Blue stone, 2 = Wind stone, 4 = Life stone, 8 = Shadow stone, 16 = Stone by the pond (wrong one), 32 = Water stone from Artisan's house, 64 = Job complete; stones not needed, 128 = Sculptor explained the stones' purpose. |
| Byte        | 611         | *Unclear:* Temporary 0/1 flag reused by several scripts: the Shumi Specialist's greeting, the Sculptor's stone check, and Kazu's talk on the Fisherman's Horizon bridge. It is cleared to 0 when a stone is picked up; its purpose isn't clear. |
| Byte        | 612         | *Likely:* Progress of the Shumi Village story about the Elder's Attendant, who first refuses to make the statue and later agrees to work. Squall asks the Moomba outside for help along the way. Values: 64 = Moomba outside has been talked to, 128 = Attendant is working on the statue. |
| Byte        | 613         | *Unclear:* Small event flags for two unrelated places: bits 1, 2 and 8 are set as Squall passes through the Fisherman's Horizon repair shop, and bit 4 is set in Artisan's house in Shumi Village after Artisan's "great honor" line. Their purpose isn't clear. |
| Byte        | 614         | *Likely:* Two uses. On Battleship Island it records the visit and, at 4, that the island is finished; the Deep Sea tower's opening scene plays only at 4. Inside the Deep Sea tower it records which level terminal has been used. Values: 1 = Arrived on Battleship Island, 2 = Reached the island core, 4 = Island finished; tower not started, 8 = Tower level 1 explained, 16 = Tower level 2 terminal used, 32 = Tower level 3 terminal used, 64 = Tower level 4 terminal used, 128 = Tower level 5 terminal used. |
| Byte        | 615         | Reserve Steam Pressure left in the Deep Sea Research Center puzzle, from 0 to 20. Each terminal subtracts the amount the player picks and the Steam Room adds some back. |
| Byte        | 616         | State of Chocobo Forest 1 (Beginner level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Aura Stone) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 617         | State of Chocobo Forest 2 (Beginner level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Flare Stone) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 618         | State of Chocobo Forest 3 (Intermediate level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Shell Stone and Holy Stone) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 619         | *Likely:* State of the Chocobo holy ground, the seventh forest, in the order of the Chocoboy's scenes there: first talk, mother chocobos gathering, and the Chocobo Card. Values: 2 = Chocoboy's first talk here, 32 = Mother chocobos have gathered, 64 = Gathering scene triggered, 128 = Chocobo Card received. |
| Byte        | 620         | State of Chocobo Forest 5 (Expert level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Meteor, Holy and Ultima Stones) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 621         | State of Chocobo Forest 6 (Intermediate level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Protect and Meteor Stones) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 622         | State of Chocobo Forest 7 (Expert level). Values 1 and 2 are the ChocoWhis state shared by all six forests; 128 belongs to this forest and means its reward (Meteor, Flare and Ultima Stones) was collected. Values: 0 = Whistle not obtained yet, 1 = ChocoWhis stolen, 2 = Player has the ChocoWhis, 32 = Chocobo caught with Help Me, 64 = Chocobo caught by the player, 128 = Reward collected; forest done. |
| Byte        | 623         | *Likely:* Progress of the Shumi Village scenes after the statue is finished: the Attendant reports it, the Elder thanks the group and speaks with his Attendant, then offers the Attendant a visit to Laguna. Values: 1 = Attendant says the statue is finished, 4 = Elder thanked the group; private talk, 16 = Elder lets the Attendant go see Laguna. |
| Byte        | 624         | *Likely:* Progress counter for the scripted events of the game's Balamb Town section, which moves in steps of two, and for the Trabia Garden visit, which uses values from 100 up. Debug menu labels tie the Balamb values to getting out of a car, parking it, leaving a boat and Seifer's car leaving. Values: 4 = Event of getting out of the car done, 6 = Car parked at the Balamb entrance, 12 = Event of getting off the boat done, 14 = Seifer's car has left, 100 = Approaching Trabia Garden, 102 = At Trabia Garden's front gate, 106 = Trabia garage scene, 108 = At the Trabia cemetery, 120 = At the Trabia basketball court. |
| Byte        | 625         | *Likely:* Flags for Balamb Town: several maps set bit 1 or 2 on entry to mark the area as visited, and a few bits track conversations. The town setup script clears bits 1, 2 and 64. Bits: +8 Zell's room entered, +128 Hotel owner has come up with his slogan. |
| Byte        | 626         | *Likely:* Balamb Town conversation flags for Zell's visit with his mother, the mechanic and the Big Bad Rascal. The town setup script clears most bits. Bits: +4 Mechanic made his job offer, +8 New assistant spoke of Zell's legend. |
| Byte        | 627         | *Likely:* Balamb Town conversation flags, mostly about the Big Bad Rascal and the townspeople who talk about him. The town setup script clears most bits. Bits: +1 Zell and the Rascal greeted each other. |
| Byte        | 628         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 629         | *Unclear:* Balamb Town flag byte reset when the town setup script starts. Bits 1, 4 and 8 are tested when the port plaza NPCs are placed; their purpose isn't clear. |
| Byte        | 630         | *Unclear:* Balamb Town flag byte set during the Big Bad Rascal's talk about hiding something in Zell's room, by the station and the Zell's house maps, and cleared by the town setup script. Its bits are not clearly tied to single events. |
| Byte        | 631         | *Unclear:* Flag byte used by Balamb Town maps (hotel, station, port) and the Garden library. Bit 128 is set after the fish cook's talk at the port. Its other bits are not clearly tied to events. |
| Byte        | 632         | *Unclear:* Flag byte used by Balamb Town maps (hotel, port plaza dog, hotel street) and the Garden library. Its bits are not clearly tied to single events. |
| Byte        | 633         | *Likely:* Event flags for Balamb Town, the Garden library and the Trabia Garden approach. Bits: +4 Spd Up item taken in Balamb, +64 Selphie went ahead into Trabia Garden, +128 Hyne legend told to the children. |
| Word        | 634         | *Likely:* Value of the main story progress counter at the time the Balamb Garden library flags were last set. Later maps compare it with the current story progress to tell that the story has moved on. |
| Byte        | 636         | *Likely:* Counts how many times the player has pushed the chocobo in Winhill (0 to 5); it becomes 6 when the chocobo runs off and its other copy appears. |
| Byte        | 637         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 638         | *Likely:* Progress of the scenes in the Balamb Garden master's room with NORG. The values rise in steps of two, up to the battle against NORG and the scene after it. Values: 8 = Squall reports the failed assassination, 28 = NORG attacks Squall's group, 30 = Scene after the NORG battle. |
| Byte        | 639         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 640         | *Likely:* Trabia Garden approach: a bit is set for each of the four SeeDs who is not in Squall's party and so stands waiting at the front gate and in the courtyard. Bits: +1 Zell waits at the gate, +2 Quistis waits at the gate, +4 Rinoa waits at the gate, +8 Irvine waits at the gate. |
| Byte        | 641         | *Likely:* Flags for the Trabia Garden scenes (the donation drive at the gate and the student who scolds the dreamer) and for the occupied Balamb Town gate. Bits: +4 Gate soldier: town is under Edea. |
| Byte        | 642         | *Unclear:* Flag byte for the occupied Balamb Town (the hunt for the Galbadian captain) and a Trabia Garden girl's question about Selphie. The town's scenes set bits 8, 16, 64 and 128 as the party passes through; their exact purpose isn't clear. |
| Byte        | 643         | *Unclear:* Flag byte used by occupied Balamb Town maps, the Garden library and the library's Zell quiz setup. Bits 8 and 64 are tested in many town maps; their exact purpose isn't clear. |
| Byte        | 644         | *Likely:* Flag byte for the occupied Balamb Town captain hunt, also used in the Garden library. Bits: +128 Learned the captain went fishing. |
| Byte        | 645         | Zell's answers to the library love-compatibility quiz: bits 1, 2 and 4 hold the colour he picked and bits 8, 16 and 32 the food. The library girls and the compatibility book read them back. Bits: +1 Colour: red, +2 Colour: blue, +4 Colour: pink, +8 Food: beef, +16 Food: fish, +32 Food: hot dogs. |
| Byte        | 646         | *Likely:* Event flags for the occupied Balamb Town captain hunt: clues from townspeople and the soldiers' search dog. Bits: +2 Hotel owner told his daughter is safe, +4 Told the captain is at the harbor's end, +8 Captain seen heading for the station, +128 The search dog has run off. |
| Byte        | 647         | *Likely:* Counts the entries into the occupied Balamb Town hotel street while the captain is hunted, up to 8. At 2 the hotel street townsfolk ask why the captain is wanted, and at 8 the soldiers say their shift is nearly over. |
| Byte        | 648         | *Likely:* Progress flags for the hunt for Raijin in occupied Balamb Town (the Galbadian soldiers' 'captain'). They record how the search was resolved, whether the countdown is over, and the fight at the hotel. Bits: +1 Search dog has set off (2nd route), +2 Raijin beaten after the dog route, +4 Fujin and Raijin hotel battle done, +8 Raijin beaten after the train route, +32 Search countdown stopped or expired, +64 Search countdown running. |
| Byte        | 649         | *Likely:* Story progress flags for the occupied Balamb Town sequence (Zell's hometown, the Galbadian soldiers and Raijin). Each bit marks a cutscene or scene already seen. Bits: +1 Passed the town gate scene, +2 Zell's house scene (smoky kitchen) seen, +4 Zell's room 'it's sacred' scene seen, +16 Raijin found on the train, +32 Hotel soldier asked about the captain, +64 Search ran out of time, forced fight, +128 Soldiers poisoned by the fish. |
| Byte        | 650-655     | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Word        | 656         | Length in seconds (200) of the countdown timer for the Raijin hunt in occupied Balamb Town. It is set when the harbor map is entered and loaded into the timer when the player talks to the soldier with the search dog. |
| Byte        | 658         | *Likely:* Seconds elapsed on the Raijin hunt countdown (656 minus the time left), recomputed when entering each Balamb Town map. Each map compares it with its own limit (about 35 to 125 s) to decide whether the hunt carries on there. |
| Byte        | 659         | *Likely:* Progress flags for the library-girl-with-a-pigtail romance subplot (Zell, Balamb Garden library and Balamb Hotel). A bit is set when its scene has been triggered; the library entry script then plays the pending scene once and records it in 660. Bits: +1 Library girl's rules speech heard, +2 Zell asked about 'Good-bye Pururun', +4 'SeeD' library scene triggered, +16 Library back-room scene triggered, +32 Fortune-telling book scene seen, +64 Pigtail girl met at Balamb Hotel. |
| Byte        | 660         | *Likely:* Companion of 659 for the pigtail library girl subplot: bits 1 to 32 are set by the Garden library when the matching scene of 659 has been played. Bit 64 is set when Zell picks up Combat King 003 in the Balamb Hotel. Bits: +64 Combat King 003 taken (Balamb Hotel). |
| Byte        | 661         | *Likely:* A byte of one-time event flags shared by several unrelated places: the Balamb Garden library, the Timber gate, the Balamb Town station and Winhill. Each bit is set once an item is taken or a scene has been seen. Bits: +2 Occult Fan I taken (Garden library), +64 Rich man's chocobo spoken to (Winhill), +128 Weapons Monthly Aug. taken (Timber). |
| Byte        | 662         | *Likely:* Winhill event flags used for the inn, the rich man's mansion (vase and ghost story) and Lain's house. Each bit marks a conversation or scene already seen, so that the dialogue changes afterwards. Bits: +1 Rich man's mansion entered, +2 Inn room offered upstairs, +4 Rich man's missing vase story heard. |
| Byte        | 663         | *Likely:* Winhill flags for the rich man's broken vase quest: four bits record which vase pieces have been found, and bit 128 means a new piece has not yet been shown to him. Bit 4 is also used in the Balamb Garden library. Bits: +1 Vase piece found (Lain's house), +8 Vase piece found (rich man's house), +16 Vase piece found (village), +32 Vase piece found (flower field), +128 New piece not yet shown to rich man. |
| Byte        | 664         | Used in two places. In occupied Balamb Town it records which of the tabloid man's paid tips has been bought. In Winhill it records the rich man's Holy Stone reward and two hidden items. Bits: +1 Holy Stone reward received (Winhill), +2 Bought the 5,000 Gil tip, +4 Bought the 15,000 Gil tip, +8 Bought the 30,000 Gil tip, +16 Left town via the rascal kid's route, +32 Rascal kid distracted guard, +64 Hidden vegetable taken (Winhill), +128 Hidden item taken (Winhill). |
| Byte        | 665         | *Likely:* Small scene flags for the normal Balamb Town maps (station, gate, hotel, Zell's home) and for the tabloid man in occupied Balamb Town. Most bits are one-time markers that a scene or NPC dialogue was seen. Bits: +1 Told about the pigtail girl's visit, +8 Met the tabloid man (occupied town). |
| Word        | 666         | Number of times the party has walked into the Balamb Garden library from outside. The Love Meter book shows 1 to 5 hearts depending on whether it exceeds 0, 20, 30, 40 or 50. |
| Byte        | 668         | *Likely:* One-time dialogue flags. In Balamb Town they record the clues about the Galbadian 'captain', and in Winhill that the rich man has received his first vase piece. Bits: +2 Zell's mother told about fish smell, +4 Clue: captain slept behind the car, +8 First vase piece given (Winhill). |
| Byte        | 669-671     | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Word        | 672         | *Likely:* Story stage counter for the Esthar part of the game. Scripts raise it as the party goes from the Fisherman's Horizon railway to Esthar station, the presidential palace, the magic research lab and the timed run through Esthar City; it becomes 23 when that timer runs out. Values: 1 = On the Fisherman's Horizon railway, 3 = Arrived at Esthar station, 4 = Esthar station, later scene, 5 = Leaving Esthar station, 6 = Magic lab lobby battle scene, 7 = Taking the car to the palace, 9 = Presidential palace meeting, 15 = Esthar capital entrance reached, 18 = Magic research lab entered, 19 = Timed run through Esthar City, 23 = Time limit expired. |
| Byte        | 674         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 675         | *Unclear:* Only written by a debug room (test14) and read once in the Deling hotel by Julia's script, where the test has no effect. Its purpose isn't clear and it is not set in normal play. |
| Byte        | 676         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 677         | *Likely:* Set to 1 while the party is riding the Esthar inner skyway (moving walkway) and 0 otherwise. When it is 1 on entering a map, the game asks whether to get off or keep going. Values: 0 = Not on the skyway, 1 = Riding the skyway. |
| Byte        | 678         | *Likely:* Records which of the three forced Esthar encounter battles have been fought during the timed run through Esthar City; later maps use it to open or block paths. Bits: +1 First encounter battle fought, +2 Second encounter battle fought, +4 Third encounter battle fought. |
| Byte        | 679         | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields) |
| Byte        | 680         | *Unclear:* A 0 to 3 state shared by several Esthar City maps and changed by talking to a man in them (set to 1 in eccway12, 2 in ecopen2 and 3 in eccway11); the man's lines depend on it. Its exact purpose isn't clear. |
| Byte        | 681         | Free gifts given once by shops in the Esthar shopping mall (each shop gives two on successive visits), plus the Occult Fan IV magazine from the presidential palace secretary. Bits: +1 Cloud's Shop: Hi-Potion given, +2 Johnny's Shop: Hi-Potion given, +4 Karen's Store: Hi-Potion given, +8 Cloud's Shop: X-Potion given, +16 Johnny's Shop: Mega-Potion given, +32 Karen's Store: Mega Phoenix given, +64 Occult Fan IV taken (palace), +128 Cheryl's Store: Rosetta Stone given. |
| Byte        | 682         | *Likely:* Dialogue flags for NPCs in Esthar City and the presidential palace: the dog owner and his dog, a presidential aide, and a woman near the skyway. Each bit marks a conversation that has happened. Bits: +2 Aide reported the major problem, +32 Dog spoken to, +64 Dog owner thanked you. |
| Byte        | 683         | *Likely:* Progress of the conversation with a soldier in the Esthar capital: after two talks he leaves and the Combat King 004 magazine is handed over. Bits: +1 Soldier's first conversation held, +4 Soldier's second talk done, he leaves. |
| Byte        | 684         | *Likely:* State of the Laguna and Kiros scene in the Esthar magic research lab: the soldier fight, the unlocked door and Kiros asking if he knows what he is doing. Values: 1 = Soldier fight fought, 2 = Door unlocked, 3 = Kiros questions Laguna. |
| Byte        | 685         | *Likely:* Dialogue flags for NPCs in Esthar City maps during the timed run (soldiers searching, residents, the research assistant at the lab). Each bit marks a conversation that has taken place. Bits: +128 Research assistant refused entry. |
| Byte        | 686         | *Likely:* Checkpoint flags for the timed run through Esthar City, in which Zell tracks something crossing the city. Bits: +1 Spotted it at the moving way, +2 Told it is heading for the center, +4 Ran out of time at the center, +128 Center scroll line crossed. |
| Byte        | 687         | *Likely:* Set to 1 while the contact-point information window is shown during the timed run through Esthar City, and back to 0 when it is closed. The player toggles it with a button. Values: 0 = Display hidden, 1 = Display shown. |
| Byte        | 688         | *Unclear:* Aide and sofa dialogue state in the presidential palace meeting room: sitting on the sofa sets bits 1 and 2, and the aide's lines change accordingly (one of them mentions Dr. Odine). Bits: +1 Sofa used first time, +2 Sofa used again, aide mentions Odine. |
| Byte        | 689         | *Likely:* Set to 1 after Dr. Odine's lines in the Esthar magic research lab lobby ('It will not attack us...') have played, so they are not repeated. Values: 1 = Odine's lab-lobby scene played. |
| Byte        | 690         | *Unclear:* Set to 1 when the sentry in the Esthar presidential-view map has been spoken to, which changes the second soldier there. Its purpose beyond that isn't clear. Values: 1 = Sentry spoken to. |
| Byte        | 691         | *Likely:* Set to 1 the first time the MD Level 4 maps of Balamb Garden start their special music, so it is not started again. Values: 0 = Music not started yet, 1 = Music already started. |
| Byte        | 692-719     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 720         | Squall's current outfit as shown on the field: it picks his model in every map. The Garden dorm lets the player change between uniforms and street clothes. A debug room also offers a bandage outfit (3). Values: 0 = Own clothes, 1 = Student uniform, 2 = SeeD uniform. |
| Byte        | 721         | *Likely:* Zell's current outfit on the field; it picks his model in every map and follows the same scheme as Squall's. Values: 0 = Own clothes, 1 = Student uniform, 2 = SeeD uniform. |
| Byte        | 722         | *Likely:* Selphie's current outfit on the field; it picks her model in the maps. The Balamb Garden classroom map assigns her a random outfit from the three when entered under certain conditions. Values: 0 = Own clothes, 1 = Student uniform, 2 = SeeD uniform. |
| Byte        | 723         | *Likely:* Quistis' current outfit on the field. Values: 0 = Own clothes, 1 = Uniform. |
| Word        | 724         | *Likely:* A shared timer value. At the end of the Dollet mission it stores the countdown reading, which the SeeD field exam turns into its 'Conduct' score (under 180 gives -100, over 1499 gives +80). In the Timber TV-station cable section it is the remaining time in seconds, and in Timber's plan briefing it holds the explanation topic Rinoa is giving (0 to 3). |
| Word        | 726         | During the Dollet mission, the number of enemies killed (the kill counter at the end minus its value at the start); the SeeD field exam turns it into the 'Attack' score. In Timber it is reused as a flag set to 1 once Rinoa has explained everything about the plan. |
| Byte        | 728         | Reused many times. In Dollet it counts mistakes during the field exam (+1 to +20 each) and feeds the 'Attitude' score. In Timber it counts abduction-plan attempts. In Deling City it holds a random code number that the Tomb of the Unknown King guard asks for. In disc 3 it holds which character went to space with Squall. Values: 2 = Irvine (space party), 3 = Quistis (space party), 5 = Selphie (space party).<sub>3</sub> |
| Byte        | 729         | During the Dollet mission, the number of battles escaped (counter at the end minus counter at the start), used for the 'Spirit' score of the SeeD field exam. In Deling City it counts the 3,000 Gil hints bought from Caraway's guard (0 to 2). In Timber it counts failures of the abduction plan. Values: 0 = No hint bought (Deling City), 1 = First hint bought (Deling City), 2 = Both hints bought (Deling City). |
| Byte        | 730         | *Likely:* Garden story flags. They record the Garden Festival committee, meeting and touring Selphie, Dr. Kadowaki's request for Cid, the Tomb of the Unknown King maps bought from Caraway's guard in Deling City and the 4-Suits card challenge. Bits: +1 Joined Garden Festival committee, +2 Met Selphie in the Garden hall, +4 Gave Selphie a tour of the Garden, +16 Kadowaki asked you to send Cid, +32 Given the Tomb of Unknown King map, +64 Bought the Tomb location displayer, +128 Defeated the four card suits. |
| Byte        | 731         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 732         | *Likely:* The countdown reading taken when the fight against Ifrit in the Fire Cavern ends. The SeeD field exam gives its 'Judgment' score from it (under 8 gives +100, over 899 gives -100). |
| Byte        | 734         | *Likely:* Records which characters were in the party at Balamb Garden's gate when the groups were split in disc 2. Later Garden scenes test these bits to know who is in each group. Bits: +1 Zell, +2 Irvine, +4 Rinoa, +8 Quistis.<sub>2</sub> |
| Byte        | 735         | *Likely:* One-time scene flags for Balamb Garden maps, set when a scene starts and tested to change later behaviour. Bits: +2 Garden defence scene (bgpark_1) started, +4 Cafeteria Zell scene seen, +8 Student scene (bgkote_1) started, +16 Cid's announcement (bghoke_1) seen, +32 Garden defence scene (bgmon_1) started, +64 Library back room (bgbook_3) entered. |
| Byte        | 736-751     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 752         | *Likely:* Remembers which place the Ragnarok was last boarded from, so that its exit door returns the party there. Bits are set from the previous map (fhparar1, ecpview2, eaplane1, ebinto1, sdisle1). Bits: +1 Boarded at fhparar1, +2 Boarded at ecpview2, +4 Boarded at eaplane1, +8 Boarded at ebinto1, +64 Boarded at sdisle1. |
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
