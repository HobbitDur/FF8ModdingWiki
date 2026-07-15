---
layout: default
parent: Miscellaneous
title: FF8 Char
permalink: /technical-reference/miscellaneous/ff8-char/
---

# Font files

FF8 character are part of a font file. A font file define what are the characters that the game understand, and which
hexa correspond.

There is several different font files for FF8, depending on the language. Mainly known there is:

* 2 japaneses that can be found on [Deling font](https://github.com/myst6re/deling/tree/master/fonts)
* 1 for the west that can be found with the previous link or
  with [FF8GameData font](https://github.com/HobbitDur/FF8GameData/blob/master/Resources/sysfnt.txt)

The [FF8GameData repository](https://github.com/HobbitDur/FF8GameData/) contains lots of data from the game and should
be up-to-date with all new knowledge.

# Char

There is 4 types of char

## TextChar

Correspondant to a letter, number or special character in the alphabet

| Hex value | Char | Size |
|-----------|------|------|
| 0x03      | \n   | 1    |
| 0x21      | 0    | 1    |
| 0x22      | 1    | 1    |
| 0x23      | 2    | 1    |
| 0x24      | 3    | 1    |
| 0x25      | 4    | 1    |
| 0x26      | 5    | 1    |
| 0x27      | 6    | 1    |
| 0x28      | 7    | 1    |
| 0x29      | 8    | 1    |
| 0x2a      | 9    | 1    |
| 0x2b      | %    | 1    |
| 0x2c      | /    | 1    |
| 0x2d      | :    | 1    |
| 0x2e      | !    | 1    |
| 0x2f      | ?    | 1    |
| 0x30      | …    | 1    |
| 0x31      | +    | 1    |
| 0x32      | -    | 1    |
| 0x33      | =    | 1    |
| 0x34      | *    | 1    |
| 0x35      | &    | 1    |
| 0x36      | 「    | 1    |
| 0x37      | 」    | 1    |
| 0x38      | (    | 1    |
| 0x39      | )    | 1    |
| 0x3a      | ·    | 1    |
| 0x3b      | .    | 1    |
| 0x3c      | ,    | 1    |
| 0x3d      | ~    | 1    |
| 0x3e      | ”    | 1    |
| 0x3f      | “    | 1    |
| 0x40      | ‘    | 1    |
| 0x41      | #    | 1    |
| 0x42      | $    | 1    |
| 0x43      | '    | 1    |
| 0x44      | _    | 1    |
| 0x45      | A    | 1    |
| 0x46      | B    | 1    |
| 0x47      | C    | 1    |
| 0x48      | D    | 1    |
| 0x49      | E    | 1    |
| 0x4a      | F    | 1    |
| 0x4b      | G    | 1    |
| 0x4c      | H    | 1    |
| 0x4d      | I    | 1    |
| 0x4e      | J    | 1    |
| 0x4f      | K    | 1    |
| 0x50      | L    | 1    |
| 0x51      | M    | 1    |
| 0x52      | N    | 1    |
| 0x53      | O    | 1    |
| 0x54      | P    | 1    |
| 0x55      | Q    | 1    |
| 0x56      | R    | 1    |
| 0x57      | S    | 1    |
| 0x58      | T    | 1    |
| 0x59      | U    | 1    |
| 0x5a      | V    | 1    |
| 0x5b      | W    | 1    |
| 0x5c      | X    | 1    |
| 0x5d      | Y    | 1    |
| 0x5e      | Z    | 1    |
| 0x5f      | a    | 1    |
| 0x60      | b    | 1    |
| 0x61      | c    | 1    |
| 0x62      | d    | 1    |
| 0x63      | e    | 1    |
| 0x64      | f    | 1    |
| 0x65      | g    | 1    |
| 0x66      | h    | 1    |
| 0x67      | i    | 1    |
| 0x68      | j    | 1    |
| 0x69      | k    | 1    |
| 0x6a      | l    | 1    |
| 0x6b      | m    | 1    |
| 0x6c      | n    | 1    |
| 0x6d      | o    | 1    |
| 0x6e      | p    | 1    |
| 0x6f      | q    | 1    |
| 0x70      | r    | 1    |
| 0x71      | s    | 1    |
| 0x72      | t    | 1    |
| 0x73      | u    | 1    |
| 0x74      | v    | 1    |
| 0x75      | w    | 1    |
| 0x76      | x    | 1    |
| 0x77      | y    | 1    |
| 0x78      | z    | 1    |
| 0x79      | À    | 1    |
| 0x7a      | Á    | 1    |
| 0x7b      | Â    | 1    |
| 0x7c      | Ä    | 1    |
| 0x7d      | Ç    | 1    |
| 0x7e      | È    | 1    |
| 0x7f      | É    | 1    |
| 0x80      | Ê    | 1    |
| 0x81      | Ë    | 1    |
| 0x82      | Ì    | 1    |
| 0x83      | Í    | 1    |
| 0x84      | Î    | 1    |
| 0x85      | Ï    | 1    |
| 0x86      | Ñ    | 1    |
| 0x87      | Ò    | 1    |
| 0x88      | Ó    | 1    |
| 0x89      | Ô    | 1    |
| 0x8a      | Ö    | 1    |
| 0x8b      | Ù    | 1    |
| 0x8c      | Ú    | 1    |
| 0x8d      | Û    | 1    |
| 0x8e      | Ü    | 1    |
| 0x8f      | Œ    | 1    |
| 0x90      | ß    | 1    |
| 0x91      | à    | 1    |
| 0x92      | á    | 1    |
| 0x93      | â    | 1    |
| 0x94      | ä    | 1    |
| 0x95      | ç    | 1    |
| 0x96      | è    | 1    |
| 0x97      | é    | 1    |
| 0x98      | ê    | 1    |
| 0x99      | ë    | 1    |
| 0x9a      | ì    | 1    |
| 0x9b      | í    | 1    |
| 0x9c      | î    | 1    |
| 0x9d      | ï    | 1    |
| 0x9e      | ñ    | 1    |
| 0x9f      | ò    | 1    |
| 0xa0      | ó    | 1    |
| 0xa1      | ô    | 1    |
| 0xa2      | ö    | 1    |
| 0xa3      | ù    | 1    |
| 0xa4      | ú    | 1    |
| 0xa5      | û    | 1    |
| 0xa6      | ü    | 1    |
| 0xa7      | œ    | 1    |
| 0xa9      | \[   | 1    |
| 0xaa      | \]   | 1    |
| 0xab      | ■    | 1    |
| 0xac      | ○    | 1    |
| 0xad      | ♦    | 1    |
| 0xae      | 【    | 1    |
| 0xaf      | 】    | 1    |
| 0xb0      | □    | 1    |
| 0xb2      | 『    | 1    |
| 0xb3      | 』    | 1    |
| 0xb5      | ;    | 1    |
| 0xb7      | ¯    | 1    |
| 0xb8      | ×    | 1    |
| 0xbb      | ↓    | 1    |
| 0xbc      | °    | 1    |
| 0xbd      | ¡    | 1    |
| 0xbe      | ¿    | 1    |
| 0xbf      | ─    | 1    |
| 0xc0      | «    | 1    |
| 0xc1      | »    | 1    |
| 0xc2      | ±    | 1    |
| 0xc3      | ♫    | 1    |
| 0xc5      | ↑    | 1    |
| 0xc9      | ™    | 1    |
| 0xca      | <    | 1    |
| 0xcb      | \>   | 1    |
| 0xe2      | ®    | 1    |

## CompressedTextChar:

To limit the space, some "char" are actually 2 chars. It means that for one hexa value, the corresponding char is 2
chars. To differentiate those one from the previous one, {} are put around

| Hex value | Char | Size |
|-----------|------|------|
| 0xe8      | {in} | 2    |
| 0xe9      | {e } | 2    |
| 0xea      | {ne} | 2    |
| 0xeb      | {to} | 2    |
| 0xec      | {re} | 2    |
| 0xed      | {HP} | 2    |
| 0xee      | {l } | 2    |
| 0xef      | {ll} | 2    |
| 0xf0      | {GF} | 2    |
| 0xf1      | {nt} | 2    |
| 0xf2      | {il} | 2    |
| 0xf3      | {o } | 2    |
| 0xf4      | {ef} | 2    |
| 0xf5      | {on} | 2    |
| 0xf6      | { w} | 2    |
| 0xf7      | { r} | 2    |
| 0xf8      | {wi} | 2    |
| 0xf9      | {fi} | 2    |
| 0xfa      | {EC} | 2    |
| 0xfb      | {s } | 2    |
| 0xfc      | {ar} | 2    |
| 0xfd      | {FE} | 2    |
| 0xfe      | { S} | 2    |
| 0xff      | {ag} | 2    |

## SpecialCommand:

Correspond to 2 hex values that are replaced by a long string. For example, 0x0c60 correspond to "Quezacotl". We also
surround the string in {}.
The list can be found
in [FF8GameData sysfnt info](https://github.com/HobbitDur/FF8GameData/blob/master/Resources/sysfnt_data.json)
In this sub category, there is several subsection (with some not yet discovered)

### Location and generic text (changing depending of languages)

This values are full word that are shorted in just 2 bytes of data to compress.
Location are variable that depends of the language.
Hex value: 0x0e
List of possible values:

| Hex value | Char                    | Size |
|-----------|-------------------------|------|
| 0x0e20    | {Galbadia}              | 2    |
| 0x0e21    | {Esthar}                | 2    |
| 0x0e22    | {Balamb}                | 2    |
| 0x0e23    | {Dollet}                | 2    |
| 0x0e24    | {Timber}                | 2    |
| 0x0e25    | {Trabia}                | 2    |
| 0x0e26    | {Centra}                | 2    |
| 0x0e27    | {Horizon}               | 2    |
| 0x0e28    | {East Academy}          | 2    |
| 0x0e29    | {Desert Prison}         | 2    |
| 0x0e2a    | {Trabia Garden}         | 2    |
| 0x0e2b    | {Lunar Base}            | 2    |
| 0x0e2c    | {Shumi Village}         | 2    |
| 0x0e2d    | {Deling City}           | 2    |
| 0x0e2e    | {Balamb Garden}         | 2    |
| 0x0e2f    | {East Academy Station}  | 2    |
| 0x0e30    | {Dolet Station}         | 2    |
| 0x0e31    | {Desert Prison Station} | 2    |
| 0x0e32    | {Lunar Gate}            | 2    |
| 0x0e33    | {Restores}              | 2    |
| 0x0e34    | {status}                | 2    |
| 0x0e35    | {learns}                | 2    |
| 0x0e36    | {ability}               | 2    |
| 0x0e37    | {Magic}                 | 2    |
| 0x0e38    | {Refine}                | 2    |
| 0x0e39    | {Junctions}             | 2    |
| 0x0e3a    | {Raises}                | 2    |
| 0x0e3b    | {command}               | 2    |
| 0x0e3c    | {Magazine}              | 2    |
| 0x0e3d    | {Ultimecia Castle}      | 2    |
| 0x0e3f    | {Deling}                | 2    |

### Icons

Hex value: 0x0e
List of possible values:

| Hex value | Char                     | Size |
|-----------|--------------------------|------|
| 0x0500    | {Selector}               | 2    |
| 0x0501    | {Selector}               | 2    |
| 0x0502    | {Selector}               | 2    |
| 0x0503    | {Selector}               | 2    |
| 0x0504    | {Selector}               | 2    |
| 0x0505    | {Selector}               | 2    |
| 0x0511    | {Selector}               | 2    |
| 0x0512    | {Selector}               | 2    |
| 0x0513    | {Selector}               | 2    |
| 0x0514    | {Selector}               | 2    |
| 0x0515    | {Selector}               | 2    |
| 0x0516    | {Selector}               | 2    |
| 0x0517    | {Selector}               | 2    |
| 0x0518    | {Selector}               | 2    |
| 0x0519    | {Selector}               | 2    |
| 0x051a    | {Selector}               | 2    |
| 0x051b    | {Selector}               | 2    |
| 0x051c    | {Selector}               | 2    |
| 0x051d    | {Selector}               | 2    |
| 0x051e    | {Selector}               | 2    |
| 0x051f    | {Selector}               | 2    |
| 0x0520    | {L2}                     | 2    |
| 0x0521    | {R2}                     | 2    |
| 0x0522    | {L1}                     | 2    |
| 0x0523    | {R1}                     | 2    |
| 0x0524    | {Circle}                 | 2    |
| 0x0525    | {Triangle}               | 2    |
| 0x0526    | {X}                      | 2    |
| 0x0527    | {Square}                 | 2    |
| 0x0528    | {SELECT}                 | 2    |
| 0x0529    | {0x0529:None}            | 2    |
| 0x052a    | {0x052a:None}            | 2    |
| 0x052b    | {START}                  | 2    |
| 0x052c    | {CrossTop}               | 2    |
| 0x052d    | {CrossRight}             | 2    |
| 0x052e    | {CrossDown}              | 2    |
| 0x052f    | {CrossLeft}              | 2    |
| 0x0530    | {L2}                     | 2    |
| 0x0531    | {R2}                     | 2    |
| 0x0532    | {L1}                     | 2    |
| 0x0533    | {R1}                     | 2    |
| 0x0534    | {Circle}                 | 2    |
| 0x0535    | {Triangle}               | 2    |
| 0x0536    | {X}                      | 2    |
| 0x0537    | {Square}                 | 2    |
| 0x0538    | {SELECT}                 | 2    |
| 0x0539    | {0x0539:None}            | 2    |
| 0x053a    | {0x053a:None}            | 2    |
| 0x053b    | {START}                  | 2    |
| 0x053c    | {CrossTop}               | 2    |
| 0x053d    | {CrossRight}             | 2    |
| 0x053e    | {CrossDown}              | 2    |
| 0x053f    | {CrossLeft}              | 2    |
| 0x0540    | {0x0540:None}            | 2    |
| 0x0541    | {MagicJunctioned}        | 2    |
| 0x0542    | {LimitBreakArrow}        | 2    |
| 0x0543    | {GreenStar}              | 2    |
| 0x0544    | {YellowStar(InMainTeam)} | 2    |
| 0x0545    | {JunctionAbility}        | 2    |
| 0x0546    | {CommandAbility}         | 2    |
| 0x0547    | {CharacterAbility}       | 2    |
| 0x0548    | {CharacterAbility}       | 2    |
| 0x0549    | {PartyAbility}           | 2    |
| 0x054a    | {GFAbility}              | 2    |
| 0x054b    | {MenuAbility}            | 2    |
| 0x054c    | {Potion}                 | 2    |
| 0x054d    | {GFPotion}               | 2    |
| 0x054e    | {TentItem}               | 2    |
| 0x054f    | {MagicStoneItem}         | 2    |
| 0x0550    | {PistolItem}             | 2    |
| 0x0551    | {BookItem}               | 2    |
| 0x0552    | {RockItem}               | 2    |
| 0x0553    | {Dead}                   | 2    |
| 0x0554    | {PoisonStatus}           | 2    |
| 0x0555    | {Petrify}                | 2    |
| 0x0556    | {Darkness}               | 2    |
| 0x0557    | {Silence}                | 2    |
| 0x0558    | {Berserk}                | 2    |
| 0x0559    | {Zombie}                 | 2    |
| 0x055a    | {Death}                  | 2    |
| 0x055b    | {Death}                  | 2    |
| 0x055c    | {Death}                  | 2    |
| 0x055d    | {Fire}                   | 2    |
| 0x055e    | {Ice}                    | 2    |
| 0x055f    | {Thunder}                | 2    |
| 0x0560    | {Earth}                  | 2    |
| 0x0561    | {PoisonType}             | 2    |
| 0x0562    | {Wind}                   | 2    |
| 0x0563    | {Water}                  | 2    |
| 0x0564    | {Holy}                   | 2    |
| 0x0565    | {Death}                  | 2    |
| 0x0566    | {PoisonStatus}           | 2    |
| 0x0567    | {Petrify}                | 2    |
| 0x0568    | {Darkness}               | 2    |
| 0x0569    | {Silence}                | 2    |
| 0x056a    | {Berserk}                | 2    |
| 0x056b    | {Zombie}                 | 2    |
| 0x056c    | {Sleep}                  | 2    |
| 0x056d    | {Slow}                   | 2    |
| 0x056e    | {Stop}                   | 2    |
| 0x056f    | {Curse}                  | 2    |
| 0x0570    | {Confuse}                | 2    |
| 0x0571    | {Drain}                  | 2    |
| 0x0572    | {StatusAttackYellow}     | 2    |
| 0x0573    | {StatusDefenseYellow}    | 2    |
| 0x0574    | {ElementalAttackYellow}  | 2    |
| 0x0575    | {ElementalDefenseYellow} | 2    |
| 0x0576    | {HPYellow}               | 2    |
| 0x0577    | {StrengthYellow}         | 2    |
| 0x0578    | {VitalityYellow}         | 2    |
| 0x0579    | {MagicYellow}            | 2    |
| 0x057a    | {SpiritYellow}           | 2    |
| 0x057b    | {SpeedYellow}            | 2    |
| 0x057c    | {EvadeYellow}            | 2    |
| 0x057d    | {HitYellow}              | 2    |
| 0x057e    | {LuckYellow}             | 2    |
| 0x057f    | {Selector}               | 2    |
| 0x0580    | {LimitBreakArrow}        | 2    |

### Colors

Hex value: 0x06
List of possible values:

| Hex value | Char            | Size |
|-----------|-----------------|------|
| 0x0620    | {Darkgrey}      | 2    |
| 0x0621    | {Grey}          | 2    |
| 0x0622    | {Yellow}        | 2    |
| 0x0623    | {Red}           | 2    |
| 0x0624    | {Green}         | 2    |
| 0x0625    | {Blue}          | 2    |
| 0x0626    | {Purple}        | 2    |
| 0x0627    | {White}         | 2    |
| 0x0628    | {DarkgreyBlink} | 2    |
| 0x0629    | {GreyBlink}     | 2    |
| 0x062a    | {YellowBlink}   | 2    |
| 0x062b    | {RedBlink}      | 2    |
| 0x062c    | {GreenBlink}    | 2    |
| 0x062d    | {BlueBlink}     | 2    |
| 0x062e    | {PurpleBlink}   | 2    |
| 0x062f    | {WhiteBlink}    | 2    |

### Characters

Hex value: 0x03
List of possible values:

| Hex value | Char      | Size |
|-----------|-----------|------|
| 0x0330    | {Squall}  | 2    |
| 0x0331    | {Zell}    | 2    |
| 0x0332    | {Irvine}  | 2    |
| 0x0333    | {Quistis} | 2    |
| 0x0334    | {Rinoa}   | 2    |
| 0x0335    | {Selphie} | 2    |
| 0x0336    | {Seifer}  | 2    |
| 0x0337    | {Edea}    | 2    |
| 0x0338    | {Laguna}  | 2    |
| 0x0339    | {Kiros}   | 2    |
| 0x033a    | {Ward}    | 2    |
| 0x0340    | {Angelo}  | 2    |
| 0x0350    | {Griever} | 2    |
| 0x0360    | {Boko}    | 2    |

### Guardian force

Hex value: 0x0c
List of possible values:

| Hex value | Char        | Size |
|-----------|-------------|------|
| 0x0c60    | {Quezacotl} | 2    |
| 0x0c61    | {Shiva}     | 2    |
| 0x0c62    | {Ifrit}     | 2    |
| 0x0c63    | {Sire}      | 2    |
| 0x0c64    | {Brothers}  | 2    |
| 0x0c65    | {Diablos}   | 2    |
| 0x0c66    | {Carbuncle} | 2    |
| 0x0c67    | {Leviathan} | 2    |
| 0x0c68    | {Pandemona} | 2    |
| 0x0c69    | {Cerberus}  | 2    |
| 0x0c6a    | {Alexander} | 2    |
| 0x0c6b    | {Doomtrain} | 2    |
| 0x0c6c    | {Bahamut}   | 2    |
| 0x0c6d    | {Cactuar}   | 2    |
| 0x0c6e    | {Tonberry}  | 2    |
| 0x0c6f    | {Eden}      | 2    |

## GenericCommand

Correspond to 2 or 3 hexa values that activate a certain code from the game, so that does a specific action.

### Control opcode overview

Every byte in the range `0x00`-`0x1F` is a control opcode rather than a printable glyph. The
game's text engine reads a byte, and if it is below `0x20` it is treated as a command; most
commands consume one following parameter byte (noted "size 2" below). Bytes `0x20` and above are
normal glyphs (see [TextChar](#textchar)).

The table below is the full opcode map as interpreted by the shared battle/menu text engine
(`ProcessBattleTextExpansion` and `Text_FetchNextToken` in the game executable, see the
[Reference addresses](#reference-addresses) table). The field/world text uses the same opcode
numbering.

| Opcode | Size | Name             | Description                                                                                     |
|--------|------|------------------|-------------------------------------------------------------------------------------------------|
| 0x00   | 1    | EndOfString      | Terminates the string.                                                                          |
| 0x01   | 1    | NewPage          | Ends the current page: waits for input, clears the window, then shows the next page.            |
| 0x02   | 1    | NewLine (`\n`)   | Line break. Some windows ignore it.                                                             |
| 0x03   | 2    | CharaName        | Inserts a character name. Param selects which name (see [Characters](#characters)).             |
| 0x04   | 2    | Var              | Inserts a numeric variable read from the active text layer. Param selects slot & format (`{Var0}`,`{Var00}`,`{Varb0}`). |
| 0x05   | 2    | Icon             | Draws a symbol from `icon.tex` (controller button, status icon…). See [Icons](#icons).           |
| 0x06   | 2    | Color            | Changes the text color / blink for the rest of the line. See [Colors](#colors).                 |
| 0x07   | 1    | NewPage (variant)| Handled identically to `0x01` by the engine: a page break / page terminator.                    |
| 0x08   | 2    | *(unused)*       | Consumes a parameter byte but produces no visible output in the known engines.                  |
| 0x09   | 2    | Wait             | Pause. Param = number of frames to wait (`{Wait000}`).                                          |
| 0x0A   | 2    | Value (context)  | Inserts a context-specific value (number or string) filled in by the active screen. See [Context value](#context-value-0x0a). |
| 0x0B   | 2-3  | CursorLocation   | Marks a cursor stop / choice position. See [Cursor location ID](#cursor-location-id).           |
| 0x0C   | 2    | GuardianForce    | Inserts a GF name. See [Guardian force](#guardian-force).                                        |
| 0x0D   | 2    | *(unused)*       | Consumes a parameter byte but produces no visible output in the known engines.                  |
| 0x0E   | 2    | Location/Word    | Inserts a location or generic word (language-dependent). See [Location and generic text](#location-and-generic-text-changing-depending-of-languages). |
| 0x0F   | 2    | *(unused)*       | Consumes a parameter byte but produces no visible output in the known engines.                  |
| 0x19-0x1B | 2 | JP glyph page    | Two-byte Japanese glyph; the lead byte selects font table 1/2/3.                                 |
| 0x1C   | 2    | AddJp            | Japanese text variant (`{Jp000}`).                                                              |
| 0x1D-0x1F | 2 | Extended glyph   | Two-byte extended/Japanese glyph pages (mostly unused on the western build).                     |

> Note on the "unused" opcodes `0x08`, `0x0D`, `0x0F`: the battle and menu text engines still read
> and skip their parameter byte, but no glyph is emitted. They are not referenced by known text and
> should be treated as reserved. If you meet them in real data, keep them untouched.

### End of string, New page

The new page is a special one on himself, I don't know for sure what it does exactly, but should create a "new page"
The end of string is an empty character, but that is stored in hex as 0x00 to tell the game the string is over.
See [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String) for more info

| Hex value | Char      | Size |
|-----------|-----------|------|
| 0x00      |           | 1    |
| 0x01      | {NewPage} | 1    |

### Cursor location ID

In the game the cursor can be placed at many places. There is one ID per different text possibility, considering all game possibilities.
So even though you can see only few in a single page, on each page the different possible position have a unique ID.

The hex value for a cursor location ID is 0x0b, followed by either 1 or 2 bytes depending on the complexity of the ID (there is one byte for the Yes No
question, and 2 when multiples choices)
If used with only 1 byte, the value is not unique (wouldn't have enough value possible),
it is used for example for Yes/No question in the test seed for example. For seed test, it is always id 0x20 and 0x21 for yes/no.

| Hex value | Char                          | Size   |
|-----------|-------------------------------|--------|
| 0x0b      | {cursor_location_id:0x..(..)} | 2 or 3 |

### Context value (0x0a)

The hex value for a context value is 0x0a, followed by one parameter byte (size 2).

It works like the `0x04` Var opcode, but instead of a fixed variable it inserts a value that the
**active screen fills in just before drawing the text**. The parameter byte is a slot number; the
engine converts the slot's value into digit glyphs (for a number) or copies it as a string. Because
each screen loads its own values into these slots, **the same `0x0a` code means different things in
different places** - the meanings below are per-context, not global.

| Hex value | Char         | Size |
|-----------|--------------|------|
| 0x0a      | {0x0a..}     | 2    |

Known values in the **SeeD written test** screen (menu program 23). These are the slots read by
`Menu_SeedTest_ParseCursorStops` and filled by `Menu_SeedTest_Update`:

| Hex value | Char/Signification                  | Filled global (EXE)                    | Size |
|-----------|-------------------------------------|----------------------------------------|------|
| 0x0a20    | {CurrentSeedTestLevel}              | `SeedTest_TextValue_0A20_CurLevelOrAP` | 2    |
| 0x0a21    | {0x0a21}                            | `SeedTest_TextValue_0A21`              | 2    |
| 0x0a22    | {NextSeedTestLevel}                 | `SeedTest_TextValue_0A22_NextLevel`    | 2    |
| 0x0a26    | {SeedRank}                          | `SeedTest_TextValue_0A26_RankStr` (string) | 2 |

For slot `0x0a20` the SeeD test reuses the same slot for two purposes depending on the page: the
current test level/number, or the AP awarded on success (`10 x number of correct answers`).

Known values in **other** screens (the code number is the same, the meaning is not):

| Hex value | Char/Signification | Context                 | Size |
|-----------|--------------------|-------------------------|------|
| 0x0a23    | {CardReceived}     | Card-received popup     | 2    |

### Special characters

Some are mentionned earlier,
here they are mentionned together as the start of image characters instead of normal characters

| Hex value | Char/Signification | Size |
|-----------|--------------------|------|
| 0xc0 | {<<} | 1 |
| 0xc1 | {>>} | 1 |
| 0xc2 | {+-} | 1 |
| 0xc3 | {MusicNote} | 1 |
| 0xc4 | {0xc4:None} | 1 |
| 0xc5 | {TopArrow} | 1 |
| 0xc6 | {VI} | 1 |
| 0xc7 | {II} | 1 |
| 0xc8 | {!Inversed} | 1 |
| 0xc9 | {TM} | 1 |
| 0xca | {<} | 1 |
| 0xcb | {>} | 1 |

# Word divided
Some words are divided in several characters, but need to be used together to correctly form the word (for example the "m" can be trunced between two "characters"

| Hex value | Word | Size |
|-----------|--------------------|------|
| 0xcc 0xcd 0xce 0xcf 0xd0 | {GAMEFOLDER} | 5 |
| 0xd1 0xd2 | {Slot} | 2 |
| 0xd3 | {Ing} | 1 |
| 0xd4 0xd5 0xd6 0xd7 0xd8  | {Steckplatz} | 5 |
| 0xd9 0xda | {Fente} | 2 |
| 0xdb 0xdc 0xdd 0xde | {Ingresso} | 4 |
| 0xdf 0xe0 0xe1 | {Ranura} | 3 |

# Reference addresses

The control-opcode behaviour above was recovered from the 2013 Steam release (`FF8_EN.exe`,
base `0x400000`). Addresses are given for reference only.

| Name                             | Address     | Role                                                                            |
|----------------------------------|-------------|---------------------------------------------------------------------------------|
| `ProcessBattleTextExpansion`     | 0x4B8B30    | Expands a raw string: resolves names/vars/items/GF/location into displayable text. |
| `Text_FetchNextToken`            | 0x4B9170    | Tokenizer: returns the next glyph or `(opcode<<8)\|param` control token.          |
| `Text_RenderGlyphs`              | 0x4A1570    | Main glyph layout/rendering from the tokenized line.                             |
| `someStringWork_4B8E40`          | 0x4B8E40    | Resolves the `0x04` Var opcode (numeric variable slots, decimal/hex formats).    |
| `Menu_SeedTest_ParseCursorStops` | 0x4D4A80    | Parses `0x0B` cursor stops and expands the `0x0A` context values for the SeeD test. |
| `Menu_SeedTest_Update`           | 0x4D4D30    | SeeD written test state machine; fills the `0x0A` value slots below.             |
| `SeedTest_TextValue_0A20_CurLevelOrAP` | 0x1D7DAA8 | Value inserted by `{0x0a20}` (current test level, or AP on success).            |
| `SeedTest_TextValue_0A21`        | 0x1D7DAB0   | Value inserted by `{0x0a21}`.                                                    |
| `SeedTest_TextValue_0A22_NextLevel` | 0x1D7DAAC | Value inserted by `{0x0a22}` (next test level).                                 |
| `SeedTest_TextValue_0A26_RankStr`| 0x1D7EABC   | String inserted by `{0x0a26}` (SeeD rank).                                       |



