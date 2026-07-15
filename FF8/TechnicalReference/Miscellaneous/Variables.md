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

| Var type    | Var Number  | Description                                                                                                                                                                                                                                                                                                                |
|-------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Byte        | 0-3         | unused in fields (always "FF-8")                                                                                                                                                                                                                                                                                           |
| Long        | 4           | Steps (used to generate random encounters)                                                                                                                                                                                                                                                                                 |
| Long        | 8           | Payslip                                                                                                                                                                                                                                                                                                                    |
| Byte        | 12-15       | unused in fields                                                                                                                                                                                                                                                                                                           |
| Signed Word | 16          | SeeD rank points. The SeeD rank shown in the menu = `clamp(points, 100, 3100) / 100` (rank 1–31), computed by `GetSeeDRankFromPoints`.                                                                                                                                                                            |
| Byte        | 18-19       | unused in fields                                                                                                                                                                                                                                                                                                           |
| Long        | 20          | Battles won. (Fun fact: this affects the basketball shot in Trabia.)                                                                                                                                                                                                                                                       |
| Byte        | 24-25       | unused in fields                                                                                                                                                                                                                                                                                                           |
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
| Signed Byte | 86          | Current car rent.                                                                                                                                                                                                                                                                                                          |
| Signed Byte | 87          | Built-in engine variable. No idea what it does. Scripts always check if it's equal to 0 or 10. Related to music.                                                                                                                                                                                                           |
| Signed Byte | 88          | Built-in engine variable. Used exclusively on save points. Never written to with field scripts. Related to Siren's Move-Find ability.                                                                                                                                                                                      |
| Byte        | 89-103      | unused in fields                                                                                                                                                                                                                                                                                                           |
| Long        | 104         | Seems related to SALARYDISPON/SALARYON/MUSICLOAD/PHSPOWER opcodes                                                                                                                                                                                                                                                          |
| Long        | 108         | Music related. Used for battle music retention: a value of `-1` means "no field BGM to carry over", which makes the engine stop music after the fight (checked by `Battle_KeepMusicAfterBattle`).                                                                                                                  |
| Long        | 112         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 116-147     | Draw points in field                                                                                                                                                                                                                                                                                                       |
| Byte        | 148-179     | Draw points in worldmap                                                                                                                                                                                                                                                                                                    |
| Byte        | 180-243     | Unused in fields. This region holds engine-only display/timer state rather than script variables: on-screen timer visibility (182) and X/Y position (205/206), a battle-disable flag (207), a "can save here" flag (209), and a battle-music A/B toggle (~201/203, toggled by `Battle_KeepMusicAfterBattle`).               |
| Byte        | 244-255     | Not investigated. **Note:** the worldmap-variant descriptions historically listed here (as 244–247) actually belong to offsets **264–267** — see below. These 12 bytes are `unk5` in the struct and their purpose is unverified.                                                                                            |
| Word        | 256         | Main Story quest progress. Both bytes are also copied into the worldmap state block (`+110`/`+111`) by `World_BuildObjectInstanceList` (renamed from `Wmset_SetupWorldmapVariant` in the community IDB), so the worldmap appearance can depend on story progress.                                                                                                                     |
| Byte        | 258         | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 259-260     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 261         | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 262-263     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 264         | **Worldmap variant extra flags.** Bit 3 (normal path) or bit 4 (Disc 4 path) OR-ins bit 6 (`0x40`) into the `word_2036BB6` worldmap variant bitmask. Likely the Balamb Garden mobile/stationary toggle. Read by `World_BuildObjectInstanceList`.                                                                     |
| Byte        | 265         | **Worldmap variant state.** Copied into the worldmap state block (`+103`) by `World_BuildObjectInstanceList`. Purpose not yet verified.                                                                                                                                                                                        |
| Byte        | 266         | **Worldmap variant index** (previously guessed "World map version? 3=Esthar"). Bits 0-4 select the base tile-variant bitmask via a 5-case switch: `0→0x011D`, `1→0x010D`, `2→0x0101`, `3→0x0100`, `4→0x0180`. Each bit corresponds to one entry in the trigger-rect table (see address table below) that overrides grid segments (0-767) with alternate segments (768-834). |
| Byte        | 267         | **Disc 4 worldmap sub-variant.** Bits 0-1 select among three Disc 4 bitmasks (`0x003E`, `0x023E`, `0x003F`). Only used when the Disc 4 code path is active (`dword_203FD60 != 0`).                                                                                                                                          |
| Byte        | 268-271     | Worldmap variant state bytes, copied into the worldmap state block (`+106`…`+109`) by `World_BuildObjectInstanceList`. Not yet individually investigated.                                                                                                                                                                       |
| Byte        | 272-299     | SO MANY F\*\*\*ING CARD GAME VARIABLES (292 = current card game rules, 293 = current card trade rule)                                                                                                                                                                                                                       |
| Byte        | 300         | Card Queen re-cards.                                                                                                                                                                                                                                                                                                       |
| Byte        | 301-303     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 304-305     | Timber Maniacs issues found.                                                                                                                                                                                                                                                                                               |
| Byte        | 306-319     | Reserved for Hacktuar / FF8Voice                                                                                                                                                                                                                                                                                           |
| Byte        | 320-332     | Ultimecia Gallery related (pictures viewed?)                                                                                                                                                                                                                                                                               |
| Byte        | 333         | Ultimecia Armory chest flags                                                                                                                                                                                                                                                                                               |
| Byte        | 334         | Ultimecia Castle seals. See [SEALEDOFF](../../field/field-opcodes/159-sealedoff/) for details.                                                                                                                                                                                                                               |
| Byte        | 335         | Card related                                                                                                                                                                                                                                                                                                               |
| Byte        | 336         | Deling City bus related                                                                                                                                                                                                                                                                                                    |
| Byte        | 338-340     | Deling Sewer gates opened                                                                                                                                                                                                                                                                                                  |
| Byte        | 341         | Does lots of things.<sub>5</sub>                                                                                                                                                                                                                                                                                           |
| Byte        | 342         | Deling City bus system                                                                                                                                                                                                                                                                                                     |
| Byte        | 343         | G-Garden door/event flags.                                                                                                                                                                                                                                                                                                 |
| Byte        | 344         | B-Garden / G-Garden event flags (during GvG)                                                                                                                                                                                                                                                                               |
| Byte        | 345         | G-Garden door/event flags.                                                                                                                                                                                                                                                                                                 |
| Byte        | 346-349     | FH Instrument (346 Zell, 347 Irvine, 348 Selphie, 349 Quistis)                                                                                                                                                                                                                                                             |
| Word        | 350-357     | Health Bars (Garden mech fight) — four words (350, 352, 354, 356)                                                                                                                                                                                                                                                          |
| Byte        | 358         | Space station talk flags, Centra ruins related (beat odin?).                                                                                                                                                                                                                                                               |
| Byte        | 359         | Centra ruins related (beat odin?).                                                                                                                                                                                                                                                                                         |
| Long        | 360         | Choice of FH music.                                                                                                                                                                                                                                                                                                        |
| Byte        | 364-368     | Randomly generated code for Centra Ruins.                                                                                                                                                                                                                                                                                  |
| Byte        | 369-370     | Ultimecia Castle flags                                                                                                                                                                                                                                                                                                     |
| Byte        | 371         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 372-376     | Ultimecia boss/timer/item flags                                                                                                                                                                                                                                                                                            |
| Byte        | 377         | Ultimecia organ note controller                                                                                                                                                                                                                                                                                            |
| Byte        | 378         | Centra Ruins timer (controls blackout messages from Odin)                                                                                                                                                                                                                                                                  |
| Byte        | 379         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 380         | Squall health during mech fight.                                                                                                                                                                                                                                                                                           |
| Byte        | 382-383     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 384         | Something about Laguna's time periods and GFs.                                                                                                                                                                                                                                                                             |
| Byte        | 385         | Laguna dialogue in pub. Only the +2 bit is ever set. Don't change the +1 bit.                                                                                                                                                                                                                                              |
| Byte        | 387         | Winhill progress?                                                                                                                                                                                                                                                                                                          |
| Byte        | 388         | Timber Maniacs HQ talk flags (main lobby)                                                                                                                                                                                                                                                                                  |
| Byte        | 389         | Timber Maniacs HQ talk flags (office room)                                                                                                                                                                                                                                                                                 |
| Byte        | 390         | Edea talk flags at her house                                                                                                                                                                                                                                                                                               |
| Byte        | 391         | Laguna talk flags (in his office, disc 3)                                                                                                                                                                                                                                                                                  |
| Byte        | 392         | unknown (used in Edea's house and in the Balamb Garden computer system)                                                                                                                                                                                                                                                    |
| Byte        | 393-399     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Long        | 400 and 404 | Related to monsters killed in Winhill, but I don't think it actually does anything. Will investigate.                                                                                                                                                                                                                      |
| Byte        | 408         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 409         | Balamb Garden computer system                                                                                                                                                                                                                                                                                              |
| Byte        | 410-431     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 432         | BG Main hall flags                                                                                                                                                                                                                                                                                                         |
| Byte        | 433         | Flags. Switches are assigned all over BG. No idea what any of them control.                                                                                                                                                                                                                                                |
| Byte        | 434         | Flags. Switches are assigned all over BG. No idea what any of them control.                                                                                                                                                                                                                                                |
| Byte        | 435         | Flags. Switches are assigned all over BG. No idea what any of them control.                                                                                                                                                                                                                                                |
| Byte        | 436         | Moomba friendship level in the prison? Some actions cause these flags to be set.                                                                                                                                                                                                                                           |
| Byte        | 437         | In BG on Disc 2, keeps track of who's in your party. In the prison, it's the current floor you're on.                                                                                                                                                                                                                      |
| Byte        | 438         | Cid vs Norg event flags                                                                                                                                                                                                                                                                                                    |
| Byte        | 439         | Cid vs Norg event flags                                                                                                                                                                                                                                                                                                    |
| Byte        | 440         | Event flags. (+1 Quad ambush, +2 quad item giver, +4/+8 Infirmary helped, +16 Nida, +64 Kadowaki Elixir, +128 Training center)                                                                                                                                                                                             |
| Byte        | 441         | Cid vs Norg event flags                                                                                                                                                                                                                                                                                                    |
| Byte        | 442         | Rinoa Garden tour flags                                                                                                                                                                                                                                                                                                    |
| Word        | 443         | Zell Health in Prison (Hacktuar)                                                                                                                                                                                                                                                                                           |
| Byte        | 445-447     | Propagator defeated flags                                                                                                                                                                                                                                                                                                  |
| Word        | 448         | Unknown                                                                                                                                                                                                                                                                                                                    |
| Byte        | 450-451     | Various magazine/talk flags                                                                                                                                                                                                                                                                                                |
| Byte        | 452         | Lunatic Pandora areas visited?                                                                                                                                                                                                                                                                                             |
| Byte        | 453-455     | Moomba teleport variables                                                                                                                                                                                                                                                                                                  |
| Byte        | 456-457     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 458-459     | Used with MUSICSKIP in some Balamb Garden areas                                                                                                                                                                                                                                                                            |
| Byte        | 460         | Random flags (some used for Card Club)                                                                                                                                                                                                                                                                                     |
| Byte        | 461-473     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 474         | Random flags (some used for Card Club)                                                                                                                                                                                                                                                                                     |
| Byte        | 475-478     | CC Group variables                                                                                                                                                                                                                                                                                                         |
| Byte        | 479         | If set to 0, disables all random battles during area loading.                                                                                                                                                                                                                                                              |
| Byte        | 480         | State of students in classroom (what they're doing).                                                                                                                                                                                                                                                                       |
| Byte        | 481         | Controls a conversation in the cafeteria.                                                                                                                                                                                                                                                                                  |
| Signed Word | 482         | Error ratio of missiles                                                                                                                                                                                                                                                                                                    |
| Byte        | 484         | Missile Base progression?                                                                                                                                                                                                                                                                                                  |
| Byte        | 485         | ToUK Progression (initially 0b111010101, +2 on finish quest. No other pops)                                                                                                                                                                                                                                                |
| Byte        | 486         | ToUK room? (used to control map jumps in the maze)                                                                                                                                                                                                                                                                         |
| Byte        | 487         | Missile base progression (also does something in BG2F classroom)                                                                                                                                                                                                                                                           |
| Byte        | 488         | Alternate Party Flags. Irvine +1/+16, Quistis +2/+32, Rinoa +4/+64, Zell +8/+128.<sub>1</sub>                                                                                                                                                                                                                              |
| Byte        | 489         | Random talk flags?                                                                                                                                                                                                                                                                                                         |
| Byte        | 490         | Cafeteria cutscene                                                                                                                                                                                                                                                                                                         |
| Byte        | 491         | ToUK stuff                                                                                                                                                                                                                                                                                                                 |
| Byte        | 492         | I think this is a door opener for the missile base if you choose a short time limit.                                                                                                                                                                                                                                       |
| Byte        | 493         | Missile base timer related?                                                                                                                                                                                                                                                                                                |
| Byte        | 494-527     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Signed Word | 528         | Sub-story progression (it's a progression variable for individual segments of the game)                                                                                                                                                                                                                                    |
| Byte        | 530         | X-ATM related (defeated it in battle?)                                                                                                                                                                                                                                                                                     |
| Byte        | 531         | Functionally unused. Read from at dollet, only manipulated in debug rooms.                                                                                                                                                                                                                                                 |
| Byte        | 532         | Controls footstep sounds at dollet (sand to concrete)                                                                                                                                                                                                                                                                      |
| Byte        | 533-539     | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 540-591     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 592-593     | Seems to control angles and character facing.                                                                                                                                                                                                                                                                              |
| Byte        | 594         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 595-624     | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 625         | Balamb visited flags (+8 Zell's room)                                                                                                                                                                                                                                                                                      |
| Byte        | 626-691     | not investigated (words at 634, 656, 666, 672; several sub-bytes unused in fields)                                                                                                                                                                                                                                         |
| Byte        | 692-719     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 720         | Squall's costume (0=normal, 1=student, 2=SeeD, 3=Bandage on forehead)                                                                                                                                                                                                                                                      |
| Byte        | 721         | Zell's Costume (0=normal, 1=student, 2=SeeD)                                                                                                                                                                                                                                                                               |
| Byte        | 722         | Selphie's costume (0=normal, 1=student, 2=SeeD)                                                                                                                                                                                                                                                                            |
| Byte        | 723         | Quistis' Costume (0=normal, 1=SeeD)                                                                                                                                                                                                                                                                                        |
| Word        | 724         | Dollet mission time                                                                                                                                                                                                                                                                                                        |
| Word        | 726         | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 728         | Does lots of things.<sub>3</sub>                                                                                                                                                                                                                                                                                           |
| Byte        | 729         | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 730         | Flags (+1 Joined Garden Festival Committee, +4 Gave Selphie tour of BG, +16 Kadowaki asks for Cid, +32 and +64 Tomb of Unknown Kind hints?, +128 Beat all card people?)                                                                                                                                                    |
| Byte        | 731         | unused in fields                                                                                                                                                                                                                                                                                                           |
| Word        | 732         | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 734         | Split Party Flags (+1 Zell, +2 Irvine, +4 Rinoa, +8 Quistis, +16 Selphie).<sub>2</sub>                                                                                                                                                                                                                                     |
| Byte        | 735         | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 736-751     | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 752         | not investigated                                                                                                                                                                                                                                                                                                           |
| Byte        | 753-1023    | unused in fields                                                                                                                                                                                                                                                                                                           |
| Byte        | 1024        | Escalating deck level for balamb card player (bgmon_4, training center for Joker) -> Linked to CC group quest                                                                                                                                                                                                              |
| Byte        | 1024        | Escalating deck level for balamb card player (rgroad11, ragnarok for Joker) -> Linked to CC group quest                                                                                                                                                                                                                    |
| Byte        | 1040        | Escalating deck level for balamb card player (bghall1b with seed) -> Linked to CC group quest                                                                                                                                                                                                                              |
| Byte        | 1041        | Escalating deck level for balamb card player (bghall_1 with seito) -> Linked to CC group quest                                                                                                                                                                                                                             |
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
- Temporary/scratch variables (offsets **1024–1074** observed) are used everywhere, as expected.

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
    __int8  unused337;              // 0x151
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
    __int16 Unknown9;               // 0x1C0 var 448
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
    __int8  Unknown10[7];           // 0x215
    __int8  unused540[52];          // 0x21C
    __int8  AngleCharacterFacingControl[2]; // 0x250
    __int8  unused594;              // 0x252
    __int8  Unknown11[30];          // 0x253
    __int8  BalambVisitedFlags;     // 0x271 var 625
    __int8  notInvestigated626[66]; // 0x272
    __int8  unused692[28];          // 0x2B4
    __int8  SquallCostume;          // 0x2D0 var 720
    __int8  ZellCostume;            // 0x2D1
    __int8  SelphieCostume;         // 0x2D2
    __int8  QuistisCostume;         // 0x2D3
    __int16 DolletMissionTime;      // 0x2D4
    __int16 Unknown14;              // 0x2D6
    __int8  MultiPurposeVar2;       // 0x2D8 var 728 (multi-use, note 3)
    __int8  Unknown15;              // 0x2D9
    __int8  Flags1;                 // 0x2DA var 730
    __int8  unused731;              // 0x2DB
    __int16 Unknown16;              // 0x2DC
    __int8  SplitPartyFlags;        // 0x2DE var 734 (note 2)
    __int8  Unknown17;              // 0x2DF
    __int8  unused736[16];          // 0x2E0
    __int8  Unknown18;              // 0x2F0 var 752
    __int8  unused753[271];         // 0x2F1  (vars 753-1023, unused in fields)
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
