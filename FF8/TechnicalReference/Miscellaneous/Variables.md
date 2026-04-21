---
layout: default
parent: Miscellaneous
title: Variables
permalink: /technical-reference/miscellaneous/variables/
---

By [Shard](../User:Shard).

Game variables can be accessed using the PSHM family of script functions, and can be written to by using the POPM family of functions. Which one you use depends on the size of the variable. The variables are all stored in save files, with the save block starting at address 0xD10 on uncompressed PC saves. The parameter to access a variable in the game scripts is basically the offset from this point in the variable block. For example, getting main story progress (word 256, which is word 0x100 in hex) just gets the two bytes starting at address 0xD10 + 0x100 = 0xE10. The varmap is continuous in memory while the game is running as well. In the en-US version of the original and SE releases (and likely most other versions), the varblock begins at 0x18fe9b8. You can use this [Cheat Engine Table](https://www.mediafire.com/?ucolf65ewq1yoty) to track them as you play.

Items in grey are unused by field scripts (some of them may be used in battle scripts).

| Var type    | Var Number  | Description                                                                                                                                                             |
|-------------|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Byte        | 0-3         | unused in fields (always "FF-8")                                                                                                                                        |
| Long        | 4           | Steps (used to generate random encounters)                                                                                                                              |
| Long        | 8           | Payslip                                                                                                                                                                 |
| Byte        | 12-15       | unused in fields                                                                                                                                                        |
| Signed Word | 16          | SeeD rank points?                                                                                                                                                       |
| Byte        | 18-19       | unused in fields                                                                                                                                                        |
| Long        | 20          | Battles won. (Fun fact: this affects the basketball shot in Trabia.)                                                                                                    |
| Byte        | 24-25       | unused in fields                                                                                                                                                        |
| Word        | 26          | Battles escaped.                                                                                                                                                        |
| Word        | 28          | Enemies killed by Squall                                                                                                                                                |
| Word        | 30          | Enemies killed by Zell                                                                                                                                                  |
| Word        | 32          | Enemies killed by Irvine                                                                                                                                                |
| Word        | 34          | Enemies killed by Quistis                                                                                                                                               |
| Word        | 36          | Enemies killed by Rinoa                                                                                                                                                 |
| Word        | 38          | Enemies killed by Selphie                                                                                                                                               |
| Word        | 40          | Enemies killed by Seifer                                                                                                                                                |
| Word        | 42          | Enemies killed by Edea                                                                                                                                                  |
| Word        | 44          | Squall death count                                                                                                                                                      |
| Word        | 46          | Zell death count                                                                                                                                                        |
| Word        | 48          | Irvine death count                                                                                                                                                      |
| Word        | 50          | Quistis death count                                                                                                                                                     |
| Word        | 52          | Rinoa death count                                                                                                                                                       |
| Word        | 54          | Selphie death count                                                                                                                                                     |
| Word        | 56          | Seifer death count                                                                                                                                                      |
| Word        | 58          | Edea death count                                                                                                                                                        |
| Byte        | 60-67       | unused in fields                                                                                                                                                        |
| Long        | 68          | Enemies killed                                                                                                                                                          |
| Long        | 72          | Amount of Gil the party currently has                                                                                                                                   |
| Long        | 76          | Amount of Gil Laguna's party has                                                                                                                                        |
| Long        | 80          | Counts the number of frames since the current movie started playing.                                                                                                    |
| Word        | 84          | Last area visited.                                                                                                                                                      |
| Signed Byte | 86          | Current car rent.                                                                                                                                                       |
| Signed Byte | 87          | Built-in engine variable. No idea what it does. Scripts always check if it's equal to 0 or 10. Related to music.                                                        |
| Signed Byte | 88          | Built-in engine variable. Used exclusively on save points. Never written to with field scripts. Related to Siren's Move-Find ability.                                   |
| Byte        | 89-103      | unused in fields                                                                                                                                                        |
| Long        | 104         | Seems related to SARALYDISPON/SARALYON/MUSICLOAD/PHSPOWER opcodes                                                                                                       |
| Long        | 108         | Music related                                                                                                                                                           |
| Long        | 112         | unused in fields                                                                                                                                                        |
| Byte        | 116-147     | Draw points in field                                                                                                                                                    |
| Byte        | 148-179     | Draw points in worldmap                                                                                                                                    | Byte | 180-243 | unused in fields |
| Byte | 244 | Worldmap variant extra flags. Bit 3 (normal path) or bit 4 (Disc 4 path) OR-ins bit 6 (`0x40`) into the `word_2036BB6` variant bitmask. Likely Balamb Garden mobile/stationary toggle. |
| Byte | 245 | Copied into worldmap state block (`+103`) by `sub_544860`, purpose not yet verified. Read only, not investigated. |
| Byte | 246 | Worldmap variant index. Bits 0-4 select the base tile-variant bitmask via a 5-case switch: `0→0x011D`, `1→0x010D`, `2→0x0101`, `3→0x0100`, `4→0x0180`. Each bit corresponds to one entry in the trigger-rect table at `.rdata:0xC763D2`/`0xC763EE` that overrides grid segments (0-767) with alternate segments (768-834). |
| Byte | 247 | Disc 4 worldmap sub-variant. Bits 0-1 select among three Disc 4 bitmasks (`0x003E`, `0x023E`, `0x003F`). Only used when Disc 4 code path is active (`dword_203FD60 != 0`). |
| Byte | 248-255 | unused in fields |
| Word | 256 | Main Story quest progress. |
| Byte | 258 | not investigated |
| Byte | 259-260 | unused in fields |
| Byte | 261 | not investigated |
| Byte | 262-263 | unused in fields |
| Byte | 264 | not investigated |
| Byte | 265 | not investigated |
| Byte | 266 | World map version? (3=Esthar locations unlocked) |
| Word        | 256         | Main Story quest progress.                                                                                                                                              |
| Byte        | 258         | not investigated                                                                                                                                                        |
| Byte        | 259-260     | unused in fields                                                                                                                                                        |
| Byte        | 261         | not investigated                                                                                                                                                        |
| Byte        | 262-263     | unused in fields                                                                                                                                                        |
| Byte        | 264         | not investigated                                                                                                                                                        |
| Byte        | 265         | not investigated                                                                                                                                                        |
| Byte        | 266         | World map version? (3=Esthar locations unlocked)                                                                                                                        |
| Byte        | 267         | unused in fields                                                                                                                                                        |
| Byte        | 268         | not investigated                                                                                                                                                        |
| Byte        | 269         | not investigated                                                                                                                                                        |
| Byte        | 270         | not investigated                                                                                                                                                        |
| Byte        | 271         | unused in fields                                                                                                                                                        |
| Byte        | 272-299     | SO MANY F\*\*\*ING CARD GAME VARIABLES                                                                                                                                  |
| Byte        | 300         | Card Queen re-cards.                                                                                                                                                    |
| Byte        | 301-303     | unused in fields                                                                                                                                                        |
| Byte        | 304-305     | Timber Maniacs issues found.                                                                                                                                            |
| Byte        | 306-319     | Reserved for Hacktuar / FF8Voice                                                                                                                                        |
| Byte        | 320-332     | Ultimecia Gallery related (pictures viewed?)                                                                                                                            |
| Byte        | 333         | Ultimecia Armory chest flags                                                                                                                                            |
| Byte        | 334         | Ultimecia Castle seals. See [SEALEDOFF](../Field/Field%20Opcodes/159_SEALEDOFF) for details.                                                                 |
| Byte        | 335         | Card related                                                                                                                                                            |
| Byte        | 336         | Deling City bus related                                                                                                                                                 |
| Byte        | 338-340     | Deling Sewer gates opened                                                                                                                                               |
| Byte        | 341         | Does lots of things.<sub>5</sub>                                                                                                                                        |
| Byte        | 342         | Deling City bus system                                                                                                                                                  |
| Byte        | 343         | G-Garden door/event flags.                                                                                                                                              |
| Byte        | 344         | B-Garden / G-Garden event flags (during GvG)                                                                                                                            |
| Byte        | 345         | G-Garden door/event flags.                                                                                                                                              |
| Byte        | 346-349     | FH Instrument (346 Zell, 347 Irvine, 348 Selphie, 349 Quistis)                                                                                                          |
| Word        | 350-356     | Health Bars (Garden mech fight)                                                                                                                                         |
| Byte        | 358         | Space station talk flags, Centra ruins related (beat odin?).                                                                                                            |
| Byte        | 359         | Centra ruins related (beat odin?).                                                                                                                                      |
| Long        | 360         | Choice of FH music.                                                                                                                                                     |
| Byte        | 364-368     | Randomly generated code for Centra Ruins.                                                                                                                               |
| Byte        | 369-370     | Ultimecia Castle flags                                                                                                                                                  |
| Byte        | 371         | unused in fields                                                                                                                                                        |
| Byte        | 372-376     | Ultimecia boss/timer/item flags                                                                                                                                         |
| Byte        | 377         | Ultimecia organ note controller                                                                                                                                         |
| Byte        | 378         | Centra Ruins timer (controls blackout messages from Odin)                                                                                                               |
| Byte        | 379         | unused in fields                                                                                                                                                        |
| Word        | 380         | Squall health during mech fight.                                                                                                                                        |
| Byte        | 382-383     | unused in fields                                                                                                                                                        |
| Byte        | 384         | Something about Laguna's time periods and GFs.                                                                                                                          |
| Byte        | 385         | Laguna dialogue in pub. Only the +2 bit is ever set. Don't change the +1 bit.                                                                                           |
| Byte        | 387         | Winhill progress?                                                                                                                                                       |
| Byte        | 388         | Timber Maniacs HQ talk flags (main lobby)                                                                                                                               |
| Byte        | 389         | Timber Maniacs HQ talk flags (office room)                                                                                                                              |
| Byte        | 390         | Edea talk flags at her house                                                                                                                                            |
| Byte        | 391         | Laguna talk flags (in his office, disc 3)                                                                                                                               |
| Byte        | 392         | unknown (used in Edea's house and in the Balamb Garden computer system)                                                                                                 |
| Byte        | 393-399     | unused in fields                                                                                                                                                        |
| Long        | 400 and 404 | Related to monsters killed in Winhill, but I don't think it actually does anything. Will investigate.                                                                   |
| Byte        | 408         | unused in fields                                                                                                                                                        |
| Byte        | 409         | Balamb Garden computer system                                                                                                                                           |
| Byte        | 410-431     | unused in fields                                                                                                                                                        |
| Byte        | 432         | BG Main hall flags                                                                                                                                                      |
| Byte        | 433         | Flags. Switches are assigned all over BG. No idea what any of them control.                                                                                             |
| Byte        | 434         | Flags. Switches are assigned all over BG. No idea what any of them control.                                                                                             |
| Byte        | 435         | Flags. Switches are assigned all over BG. No idea what any of them control.                                                                                             |
| Byte        | 436         | Moomba friendship level in the prison? Some actions cause these flags to be set.                                                                                        |
| Byte        | 437         | In BG on Disc 2, keeps track of who's in your party. In the prison, it's the current floor you're on.                                                                   |
| Byte        | 438         | Cid vs Norg event flags                                                                                                                                                 |
| Byte        | 439         | Cid vs Norg event flags                                                                                                                                                 |
| Byte        | 440         | Event flags. (+1 Quad ambush, +2 quad item giver, +4/+8 Infirmary helped, +16 Nida, +64 Kadowaki Elixir, +128 Training center)                                          |
| Byte        | 441         | Cid vs Norg event flags                                                                                                                                                 |
| Byte        | 442         | Rinoa Garden tour flags                                                                                                                                                 |
| Word        | 443         | Zell Health in Prison (Hacktuar)                                                                                                                                        |
| Byte        | 445-447     | Propagator defeated flags                                                                                                                                               |
| Word        | 448         | Unknown                                                                                                                                                                 |
| Byte        | 450-451     | Various magazine/talk flags                                                                                                                                             |
| Byte        | 452         | Lunatic Pandora areas visited?                                                                                                                                          |
| Byte        | 453-455     | Moomba teleport variables                                                                                                                                               |
| Byte        | 456-457     | unused in fields                                                                                                                                                        |
| Byte        | 458-459     | Used with MUSICSKIP in some Balamb Garden areas                                                                                                                         |
| Byte        | 460         | Random flags (some used for Card Club)                                                                                                                                  |
| Byte        | 461-473     | unused in fields                                                                                                                                                        |
| Byte        | 474         | Random flags (some used for Card Club)                                                                                                                                  |
| Byte        | 475-478     | CC Group variables                                                                                                                                                      |
| Byte        | 479         | If set to 0, disables all random battles during area loading.                                                                                                           |
| Byte        | 480         | State of students in classroom (what they're doing).                                                                                                                    |
| Byte        | 481         | Controls a conversation in the cafeteria.                                                                                                                               |
| Signed Word | 482         | Error ratio of missiles                                                                                                                                                 |
| Byte        | 484         | Missile Base progression?                                                                                                                                               |
| Byte        | 485         | ToUK Progression (initially 0b111010101, +2 on finish quest. No other pops)                                                                                             |
| Byte        | 486         | ToUK room? (used to control map jumps in the maze)                                                                                                                      |
| Byte        | 487         | Missile base progression (also does something in BG2F classroom)                                                                                                        |
| Byte        | 488         | Alternate Party Flags. Irvine +1/+16, Quistis +2/+32, Rinoa +4/+64, Zell +8/+128.<sub>1</sub>                                                                           |
| Byte        | 489         | Random talk flags?                                                                                                                                                      |
| Byte        | 490         | Cafeteria cutscene                                                                                                                                                      |
| Byte        | 491         | ToUK stuff                                                                                                                                                              |
| Byte        | 492         | I think this is a door opener for the missile base if you choose a short time limit.                                                                                    |
| Byte        | 493         | Missile base timer related?                                                                                                                                             |
| Byte        | 494-527     | unused in fields                                                                                                                                                        |
| Signed Word | 528         | Sub-story progression (it's a progression variable for individual segments of the game)                                                                                 |
| Byte        | 530         | X-ATM related (defeated it in battle?)                                                                                                                                  |
| Byte        | 531         | Functionally unused. Read from at dollet, only manipulated in debug rooms.                                                                                              |
| Byte        | 532         | Controls footstep sounds at dollet (sand to concrete)                                                                                                                   |
| Byte        | 533         | not investigated                                                                                                                                                        |
| Byte        | 534         | not investigated                                                                                                                                                        |
| Byte        | 535         | not investigated                                                                                                                                                        |
| Byte        | 536         | not investigated                                                                                                                                                        |
| Byte        | 537         | not investigated                                                                                                                                                        |
| Byte        | 538         | not investigated                                                                                                                                                        |
| Byte        | 539         | not investigated                                                                                                                                                        |
| Byte        | 540-591     | unused in fields                                                                                                                                                        |
| Byte        | 592-593     | Seems to control angles and character facing.                                                                                                                           |
| Byte        | 594         | unused in fields                                                                                                                                                        |
| Byte        | 595         | not investigated                                                                                                                                                        |
| Byte        | 596         | not investigated                                                                                                                                                        |
| Byte        | 597         | not investigated                                                                                                                                                        |
| Byte        | 598         | not investigated                                                                                                                                                        |
| Byte        | 599         | not investigated                                                                                                                                                        |
| Byte        | 600         | not investigated                                                                                                                                                        |
| Byte        | 601         | not investigated                                                                                                                                                        |
| Byte        | 602         | not investigated                                                                                                                                                        |
| Byte        | 603         | not investigated                                                                                                                                                        |
| Byte        | 604         | not investigated                                                                                                                                                        |
| Byte        | 605         | not investigated                                                                                                                                                        |
| Byte        | 606         | not investigated                                                                                                                                                        |
| Byte        | 607         | not investigated                                                                                                                                                        |
| Byte        | 608         | not investigated                                                                                                                                                        |
| Byte        | 609         | not investigated                                                                                                                                                        |
| Byte        | 610         | not investigated                                                                                                                                                        |
| Byte        | 611         | not investigated                                                                                                                                                        |
| Byte        | 612         | not investigated                                                                                                                                                        |
| Byte        | 613         | not investigated                                                                                                                                                        |
| Byte        | 614         | not investigated                                                                                                                                                        |
| Byte        | 615         | not investigated                                                                                                                                                        |
| Byte        | 616         | not investigated                                                                                                                                                        |
| Byte        | 617         | not investigated                                                                                                                                                        |
| Byte        | 618         | not investigated                                                                                                                                                        |
| Byte        | 619         | not investigated                                                                                                                                                        |
| Byte        | 620         | not investigated                                                                                                                                                        |
| Byte        | 621         | not investigated                                                                                                                                                        |
| Byte        | 622         | not investigated                                                                                                                                                        |
| Byte        | 623         | not investigated                                                                                                                                                        |
| Byte        | 624         | not investigated                                                                                                                                                        |
| Byte        | 625         | Balamb visited flags (+8 Zell's room)                                                                                                                                   |
| Byte        | 626         | not investigated                                                                                                                                                        |
| Byte        | 627         | not investigated                                                                                                                                                        |
| Byte        | 628         | unused in fields                                                                                                                                                        |
| Byte        | 629         | not investigated                                                                                                                                                        |
| Byte        | 630         | not investigated                                                                                                                                                        |
| Byte        | 631         | not investigated                                                                                                                                                        |
| Byte        | 632         | not investigated                                                                                                                                                        |
| Byte        | 633         | not investigated                                                                                                                                                        |
| Word        | 634         | not investigated                                                                                                                                                        |
| Byte        | 636         | not investigated                                                                                                                                                        |
| Byte        | 637         | unused in fields                                                                                                                                                        |
| Byte        | 638         | not investigated                                                                                                                                                        |
| Byte        | 639         | unused in fields                                                                                                                                                        |
| Byte        | 640         | not investigated                                                                                                                                                        |
| Byte        | 641         | not investigated                                                                                                                                                        |
| Byte        | 642         | not investigated                                                                                                                                                        |
| Byte        | 643         | not investigated                                                                                                                                                        |
| Byte        | 644         | not investigated                                                                                                                                                        |
| Byte        | 645         | not investigated                                                                                                                                                        |
| Byte        | 646         | not investigated                                                                                                                                                        |
| Byte        | 647         | not investigated                                                                                                                                                        |
| Byte        | 648         | not investigated                                                                                                                                                        |
| Byte        | 649         | not investigated                                                                                                                                                        |
| Byte        | 650-655     | unused in fields                                                                                                                                                        |
| Word        | 656         | not investigated                                                                                                                                                        |
| Byte        | 658         | not investigated                                                                                                                                                        |
| Byte        | 659         | not investigated                                                                                                                                                        |
| Byte        | 660         | not investigated                                                                                                                                                        |
| Byte        | 661         | not investigated                                                                                                                                                        |
| Byte        | 662         | not investigated                                                                                                                                                        |
| Byte        | 663         | not investigated                                                                                                                                                        |
| Byte        | 664         | not investigated                                                                                                                                                        |
| Byte        | 665         | not investigated                                                                                                                                                        |
| Word        | 666         | not investigated                                                                                                                                                        |
| Byte        | 668         | not investigated                                                                                                                                                        |
| Byte        | 669-671     | unused in fields                                                                                                                                                        |
| Word        | 672         | not investigated                                                                                                                                                        |
| Byte        | 674         | unused in fields                                                                                                                                                        |
| Byte        | 675         | not investigated                                                                                                                                                        |
| Byte        | 676         | unused in fields                                                                                                                                                        |
| Byte        | 677         | not investigated                                                                                                                                                        |
| Byte        | 678         | not investigated                                                                                                                                                        |
| Byte        | 679         | unused in fields                                                                                                                                                        |
| Byte        | 680         | not investigated                                                                                                                                                        |
| Byte        | 681         | not investigated                                                                                                                                                        |
| Byte        | 682         | not investigated                                                                                                                                                        |
| Byte        | 683         | not investigated                                                                                                                                                        |
| Byte        | 684         | not investigated                                                                                                                                                        |
| Byte        | 685         | not investigated                                                                                                                                                        |
| Byte        | 686         | not investigated                                                                                                                                                        |
| Byte        | 687         | not investigated                                                                                                                                                        |
| Byte        | 688         | not investigated                                                                                                                                                        |
| Byte        | 689         | not investigated                                                                                                                                                        |
| Byte        | 690         | not investigated                                                                                                                                                        |
| Byte        | 691         | not investigated                                                                                                                                                        |
| Byte        | 692-719     | unused in fields                                                                                                                                                        |
| Byte        | 720         | Squall's costume (0=normal, 1=student, 2=SeeD, 3=Bandage on forehead)                                                                                                   |
| Byte        | 721         | Zell's Costume (0=normal, 1=student, 2=SeeD)                                                                                                                            |
| Byte        | 722         | Selphie's costume (0=normal, 1=student, 2=SeeD)                                                                                                                         |
| Byte        | 723         | Quistis' Costume (0=normal, 1=SeeD)                                                                                                                                     |
| Word        | 724         | Dollet mission time                                                                                                                                                     |
| Word        | 726         | not investigated                                                                                                                                                        |
| Byte        | 728         | Does lots of things.<sub>3</sub>                                                                                                                                        |
| Byte        | 729         | not investigated                                                                                                                                                        |
| Byte        | 730         | Flags (+1 Joined Garden Festival Committee, +4 Gave Selphie tour of BG, +16 Kadowaki asks for Cid, +32 and +64 Tomb of Unknown Kind hints?, +128 Beat all card people?) |
| Byte        | 731         | unused in fields                                                                                                                                                        |
| Word        | 732         | not investigated                                                                                                                                                        |
| Byte        | 734         | Split Party Flags (+1 Zell, +2 Irvine, +4 Rinoa, +8 Quistis, +16 Selphie).<sub>2</sub>                                                                                  |
| Byte        | 735         | not investigated                                                                                                                                                        |
| Byte        | 736-751     | unused in fields                                                                                                                                                        |
| Byte        | 752         | not investigated                                                                                                                                                        |
| Byte        | 753-1023    | unused in fields                                                                                                                                                        |
| Byte        | Above 1023  | Temporary variables used pretty much everywhere.                                                                                                                        |

# Notes

1.  When the party splits in disc 2, each party member in the inactive party except Selphie has one of the eight bits changed for this variable. One member has a flag in the 4 most significant bits, and the other has a flag in the 4 least significant bits. It's done this way so that when the characters appear, they animate towards different locations in the field, rather than stacking on top of each other.
2.  This byte contains flags for which characters are in Squall's party when the party splits in disc 2.
3.  List of everything that 728 holds throughout the game:
    1.  SeeD field exam "Conduct" score (lose points when you do something wrong at Dollet).
    2.  Train job attempts (Timber)
    3.  Tomb of the Unknown King student ID.
    4.  Who you took to space in disc 3.
4.  The field controlling restriction unlocking in Ultimecia's Castle uses this to figure out where to jump the party after they've broken a seal. It's unknown how SETPLACE actually sets this, it's not always related to the field ID or the SETPLACE parameter. This variable is also set at Balamb Garden's front gate manually.:5. List of everything that 341 holds throughout the game:
    1.  First flashback team
    2.  Selphie's current action when escaping from Deling's mansion (changes the dialogue)
    3.  FH Concert Crappiness
    4.  Something in B-Garden classroom during the paratrooper attack.


struct GameVariables
{
    // 0x00 - 0x03: Unused in fields (always "FF-8")
    __int8 unused1[4];

    // 0x04: Steps (used to generate random encounters)
    __int32 Steps;

    // 0x08: Payslip
    __int32 Payslip;

    // 0x0C - 0x0F: Unused in fields
    __int8 unused2[4];

    // 0x10: SeeD rank points?
    __int16 SeeDRankPoints;

    // 0x12 - 0x13: Unused in fields
    __int8 unused3[2];

    // 0x14: Battles won (affects the basketball shot in Trabia)
    __int32 BattlesWon;

    // 0x18 - 0x19: Unused in fields
    __int8 unused4[2];

    // 0x1A: Battles escaped
    __int16 BattlesEscaped;

    // 0x1C: Enemies killed by Squall
    __int16 SquallKills;

    // 0x1E: Enemies killed by Zell
    __int16 ZellKills;

    // 0x20: Enemies killed by Irvine
    __int16 IrvineKills;

    // 0x22: Enemies killed by Quistis
    __int16 QuistisKills;

    // 0x24: Enemies killed by Rinoa
    __int16 RinoaKills;

    // 0x26: Enemies killed by Selphie
    __int16 SelphieKills;

    // 0x28: Enemies killed by Seifer
    __int16 SeiferKills;

    // 0x2A: Enemies killed by Edea
    __int16 EdeaKills;

    // 0x2C: Squall death count
    __int16 SquallDeaths;

    // 0x2E: Zell death count
    __int16 ZellDeaths;

    // 0x30: Irvine death count
    __int16 IrvineDeaths;

    // 0x32: Quistis death count
    __int16 QuistisDeaths;

    // 0x34: Rinoa death count
    __int16 RinoaDeaths;

    // 0x36: Selphie death count
    __int16 SelphieDeaths;

    // 0x38: Seifer death count
    __int16 SeiferDeaths;

    // 0x3A: Edea death count
    __int16 EdeaDeaths;

    // 0x3C - 0x43: Unused in fields
    __int8 unused5[8];

    // 0x44: Enemies killed
    __int32 TotalEnemiesKilled;

    // 0x48: Amount of Gil the party currently has
    __int32 PartyGil;

    // 0x4C: Amount of Gil Laguna's party has
    __int32 LagunaPartyGil;

    // 0x50: Number of frames since the current movie started playing
    __int32 MovieFrameCount;

    // 0x54: Last area visited
    __int16 LastAreaVisited;

    // 0x56: Current car rent
    __int8 CurrentCarRent;

    // 0x57: Built-in engine variable (related to music)
    __int8 EngineVar1;

    // 0x58: Built-in engine variable (used on save points)
    __int8 EngineVar2;

    // 0x59 - 0x67: Unused in fields
    __int8 unused6[15];

    // 0x68: Related to SARALYDISPON/SARALYON/MUSICLOAD/PHSPOWER opcodes
    __int32 OpcodeRelated1;

    // 0x6C: Music related
    __int32 MusicRelated;

    // 0x70: Unused in fields
    __int32 unused7;

    // 0x74 - 0x93: Draw points in field
    __int8 FieldDrawPoints[44];

    // 0x94 - 0xB3: Draw points in worldmap
    __int8 WorldmapDrawPoints[44];

    // 0xB4 - 0xFF: Unused in fields
    __int8 unused8[76];

    // 0x100: Main Story quest progress
    __int16 MainStoryProgress;

    // 0x102: Not investigated
    __int8 Unknown1;

    // 0x103 - 0x104: Unused in fields
    __int8 unused9[2];

    // 0x105: Not investigated
    __int8 Unknown2;

    // 0x106 - 0x107: Unused in fields
    __int8 unused10[2];

    // 0x108: Not investigated
    __int8 Unknown3;

    // 0x109: Not investigated
    __int8 Unknown4;

    // 0x10A: World map version? (3 = Esthar locations unlocked)
    __int8 WorldMapVersion;

    // 0x10B: Unused in fields
    __int8 unused11;

    // 0x10C: Not investigated
    __int8 Unknown5;

    // 0x10D: Not investigated
    __int8 Unknown6;

    // 0x10E: Not investigated
    __int8 Unknown7;

    // 0x10F: Unused in fields
    __int8 unused12;

    // 0x110 - 0x12B: Card game variables
    __int8 CardGameVars[28];

    // 0x12C: Card Queen re-cards
    __int8 CardQueenRecards;

    // 0x12D - 0x12F: Unused in fields
    __int8 unused13[3];

    // 0x130 - 0x131: Timber Maniacs issues found
    __int8 TimberManiacsIssues[2];

    // 0x132 - 0x13F: Reserved for Hacktuar / FF8Voice
    __int8 Reserved1[14];

    // 0x140 - 0x14C: Ultimecia Gallery related (pictures viewed?)
    __int8 UltimeciaGallery[13];

    // 0x14D: Ultimecia Armory chest flags
    __int8 UltimeciaArmory;

    // 0x14E: Ultimecia Castle seals
    __int8 UltimeciaSeals;

    // 0x14F: Card related
    __int8 CardRelated;

    // 0x150: Deling City bus related
    __int8 DelingBus;

    // 0x152 - 0x154: Deling Sewer gates opened
    __int8 DelingSewerGates[3];

    // 0x155: Does lots of things
    __int8 MultiPurposeVar1;

    // 0x156: Deling City bus system
    __int8 DelingBusSystem;

    // 0x157: G-Garden door/event flags
    __int8 GGardenFlags1;

    // 0x158: B-Garden / G-Garden event flags (during GvG)
    __int8 GGardenFlags2;

    // 0x159: G-Garden door/event flags
    __int8 GGardenFlags3;

    // 0x15A - 0x15D: FH Instrument (Zell, Irvine, Selphie, Quistis)
    __int8 FHInstruments[4];

    // 0x15E - 0x164: Health Bars (Garden mech fight)
    __int16 HealthBars[4];

    // 0x166: Space station talk flags, Centra ruins related (beat Odin?)
    __int8 SpaceStationFlags;

    // 0x167: Centra ruins related (beat Odin?)
    __int8 CentraRuinsFlags;

    // 0x168: Choice of FH music
    __int32 FHMusicChoice;

    // 0x16C - 0x170: Randomly generated code for Centra Ruins
    __int8 CentraRuinsCode[5];

    // 0x171 - 0x172: Ultimecia Castle flags
    __int8 UltimeciaCastleFlags[2];

    // 0x173: Unused in fields
    __int8 unused14;

    // 0x174 - 0x178: Ultimecia boss/timer/item flags
    __int8 UltimeciaBossFlags[5];

    // 0x179: Ultimecia organ note controller
    __int8 UltimeciaOrgan;

    // 0x17A: Centra Ruins timer (controls blackout messages from Odin)
    __int8 CentraRuinsTimer;

    // 0x17B: Unused in fields
    __int8 unused15;

    // 0x17C: Squall health during mech fight
    __int16 SquallMechHealth;

    // 0x17E - 0x17F: Unused in fields
    __int8 unused16[2];

    // 0x180: Something about Laguna's time periods and GFs
    __int8 LagunaTimePeriods;

    // 0x181: Laguna dialogue in pub
    __int8 LagunaPubDialogue;

    // 0x183: Winhill progress?
    __int8 WinhillProgress;

    // 0x184: Timber Maniacs HQ talk flags (main lobby)
    __int8 TimberManiacsLobby;

    // 0x185: Timber Maniacs HQ talk flags (office room)
    __int8 TimberManiacsOffice;

    // 0x186: Edea talk flags at her house
    __int8 EdeaHouseFlags;

    // 0x187: Laguna talk flags (in his office, disc 3)
    __int8 LagunaOfficeFlags;

    // 0x188: Unknown (used in Edea's house and Balamb Garden computer system)
    __int8 Unknown8;

    // 0x189 - 0x18F: Unused in fields
    __int8 unused17[7];

    // 0x190 - 0x193: Related to monsters killed in Winhill
    __int32 WinhillMonsters;

    // 0x194: Unused in fields
    __int8 unused18;

    // 0x195: Balamb Garden computer system
    __int8 BalambComputer;

    // 0x196 - 0x1AF: Unused in fields
    __int8 unused19[26];

    // 0x1B0: BG Main hall flags
    __int8 BGHallFlags;

    // 0x1B1 - 0x1B3: Flags (switches assigned all over BG)
    __int8 BGFlags[3];

    // 0x1B4: Moomba friendship level in the prison
    __int8 MoombaFriendship;

    // 0x1B5: In BG on Disc 2, keeps track of who's in your party
    __int8 PartyTracking;

    // 0x1B6 - 0x1B7: Cid vs Norg event flags
    __int8 CidNorgFlags[2];

    // 0x1B8: Event flags
    __int8 EventFlags;

    // 0x1B9: Cid vs Norg event flags
    __int8 CidNorgFlags2;

    // 0x1BA: Rinoa Garden tour flags
    __int8 RinoaTourFlags;

    // 0x1BB: Zell Health in Prison (Hacktuar)
    __int16 ZellPrisonHealth;

    // 0x1BD - 0x1BF: Propagator defeated flags
    __int8 PropagatorFlags[3];

    // 0x1C0: Unknown
    __int16 Unknown9;

    // 0x1C2 - 0x1C3: Various magazine/talk flags
    __int8 MagazineFlags[2];

    // 0x1C4: Lunatic Pandora areas visited?
    __int8 LunaticPandora;

    // 0x1C5 - 0x1C7: Moomba teleport variables
    __int8 MoombaTeleport[3];

    // 0x1C8 - 0x1C9: Unused in fields
    __int8 unused20[2];

    // 0x1CA - 0x1CB: Used with MUSICSKIP in some Balamb Garden areas
    __int8 MusicSkipFlags[2];

    // 0x1CC: Random flags (some used for Card Club)
    __int8 RandomFlags1;

    // 0x1CD - 0x1DF: Unused in fields
    __int8 unused21[19];

    // 0x1E0: Random flags (some used for Card Club)
    __int8 RandomFlags2;

    // 0x1E1 - 0x1E4: CC Group variables
    __int8 CCGroupVars[4];

    // 0x1E5: If set to 0, disables all random battles during area loading
    __int8 DisableRandomBattles;

    // 0x1E6: State of students in classroom
    __int8 ClassroomState;

    // 0x1E7: Controls a conversation in the cafeteria
    __int8 CafeteriaConversation;

    // 0x1E8: Error ratio of missiles
    __int16 MissileErrorRatio;

    // 0x1EA: Missile Base progression?
    __int8 MissileBaseProgress;

    // 0x1EB: ToUK Progression
    __int8 ToUKProgress;

    // 0x1EC: ToUK room? (used to control map jumps in the maze)
    __int8 ToUKRoom;

    // 0x1ED: Missile base progression
    __int8 MissileBaseProgress2;

    // 0x1EE: Alternate Party Flags
    __int8 AlternatePartyFlags;

    // 0x1EF: Random talk flags?
    __int8 RandomTalkFlags;

    // 0x1F0: Cafeteria cutscene
    __int8 CafeteriaCutscene;

    // 0x1F1: ToUK stuff
    __int8 ToUKStuff;

    // 0x1F2: Door opener for the missile base
    __int8 MissileBaseDoor;

    // 0x1F3: Missile base timer related?
    __int8 MissileBaseTimer;

    // 0x1F4 - 0x20F: Unused in fields
    __int8 unused22[28];

    // 0x210: Sub-story progression
    __int16 SubStoryProgress;

    // 0x212: X-ATM related (defeated it in battle?)
    __int8 XATMDefeated;

    // 0x213: Functionally unused
    __int8 UnusedVar1;

    // 0x214: Controls footstep sounds at Dollet
    __int8 DolletFootsteps;

    // 0x215 - 0x21B: Not investigated
    __int8 Unknown10[7];

    // 0x21C - 0x24F: Unused in fields
    __int8 unused23[52];

    // 0x250 - 0x251: Controls angles and character facing
    __int8 AngleControl[2];

    // 0x252: Unused in fields
    __int8 unused24;

    // 0x253 - 0x267: Not investigated
    __int8 Unknown11[21];

    // 0x268: Balamb visited flags
    __int8 BalambVisitedFlags;

    // 0x269 - 0x26F: Not investigated
    __int8 Unknown12[7];

    // 0x270: Unused in fields
    __int8 unused25;

    // 0x271 - 0x27F: Not investigated
    __int8 Unknown13[15];

    // 0x280: Squall's costume
    __int8 SquallCostume;

    // 0x281: Zell's Costume
    __int8 ZellCostume;

    // 0x282: Selphie's costume
    __int8 SelphieCostume;

    // 0x283: Quistis' Costume
    __int8 QuistisCostume;

    // 0x284: Dollet mission time
    __int16 DolletMissionTime;

    // 0x286: Not investigated
    __int16 Unknown14;

    // 0x288: Does lots of things
    __int8 MultiPurposeVar2;

    // 0x289: Not investigated
    __int8 Unknown15;

    // 0x28A: Flags
    __int8 Flags1;

    // 0x28B: Unused in fields
    __int8 unused26;

    // 0x28C: Not investigated
    __int16 Unknown16;

    // 0x28E: Split Party Flags
    __int8 SplitPartyFlags;

    // 0x28F: Not investigated
    __int8 Unknown17;

    // 0x290 - 0x2FF: Unused in fields
    __int8 unused27[112];

    // 0x300: Not investigated
    __int8 Unknown18;

    // 0x301 - 0x3FF: Unused in fields
    __int8 unused28[255];
};
