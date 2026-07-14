---
layout: default
parent: Menu
title: mngrp.bin File Format
permalink: /technical-reference/menu/mngrpbin-file-format/
---

This file is an archive which contains 118 files, that will be called section in this wiki.

It is important to note that the independent files like tkmnmes, m00x.bin or m00x.msg are not used by the game even tho
they exist (they are loaded in memory by MenuReadFiles but never read). Only the data in mngrp is taken into account.
The standalone tkmnmes2.bin is even a stale copy: its text differs from the mngrp copy the game displays.

Some sections are pure data that are irrelevant for ShumiTranslator, they are just mention for archive purpose.

This section list is for the english version. Others language should have the same sections but not the same size or offset.

The definition of this file with the different offset and size is determine by [Mngrphd.bin](../mngrphdbin-file-format/).

The **Pos** column below is the position among valid sections (the order tools like ShumiTranslator use). The
**Header entry** column is the raw mngrphd.bin entry index, which is what the engine uses to load a section
(see [Mngrphd.bin](../mngrphdbin-file-format/)). For example the refine menu asks for entries 188-192 (m00X.bin)
and 196-200 (m00X.msg), the SeeD written test for entry 96 + test number, and the Card Album pages for entry 48 + page.

If the file is modified, all sections keep a size multiple of 0x800 (2048, the PSX CD sector size) in the retail file,
padded with 0. The engine itself only trusts the offset/size pairs of mngrphd.bin; the practical limit is the fixed
capacity of the destination buffer each section is loaded into, so avoid growing a section beyond its original
0x800-multiple size.

## Mapped Data

| Pos | Header entry | Seek     | Size    | Filename                                                 | Content of the section                                                                  | Present in <br/>ShumiTranslator |
|-----|--------------|----------|---------|----------------------------------------------------------|-----------------------------------------------------------------------------------------|---------------------------------|
| 0   | 0           | 0x0      | 0x800   | [tkmnmes1.bin](../tknmnesxbin-file-format/)                          | Menu text                                                                               | Yes                             |
| 1   | 1           | 0x800    | 0x1800  | [tkmnmes2.bin](../tknmnesxbin-file-format/)                          | Menu text                                                                               | Yes                             |
| 2   | 2           | 0x2000   | 0x2000  | [tkmnmes3.bin](../tknmnesxbin-file-format/)                          | Menu text                                                                               | Yes                             |
| 3   | 3           | 0x4000   | 0xE000  |                                                          | Chocobo World PocketStation image: a complete 7-block PS1 save file ("SC" magic, MCX app marker, SJIS title "ＦＦ８／Ｃｈｏｃｏｂｏ　Ｗｏｒｌｄ") installed on the emulated memory card by the save screen | No                              |
| 4   | 7           | 0x12000  | 0x1000  |                                                          | Background tile descriptors for magita.tim (always loaded together with it): string-section-shaped, 79 offset slots (39 used), 16-byte records {UInt32 quad count, quadrant x/y, texture location, width 128, height 96/104, CLUT}. Exact renderer not identified yet | No                              |
| 5   | 9           | 0x13000  | 0x6800  | face1.bin                                                | Character portraits (main menu UI texture, reloaded on every sub-screen exit)           | No                              |
| 6   | 10          | 0x19800  | 0x6800  | face2.bin                                                | GF portraits (main menu UI texture, reloaded on every sub-screen exit)                  | No                              |
| 7   | 12          | 0x20000  | 0x800   | magita.tim                                               | Tutorial/magazine background texture                                                    | No                              |
| 8   | 16          | 0x20800  | 0xE000  | start00_and_start01.tim                                  | Title screen logo                                                                       | No                              |
| 9   | 20          | 0x2E800  | 0xC800  | mag00.tim                                                | Weapons Monthly, 1st Issue                                                              | No                              |
| 10  | 24          | 0x3B000  | 0xC800  | mag07.tim                                                | Pet Pals                                                                                | No                              |
| 11  | 28          | 0x47800  | 0xC800  | mag00.tim                                                | Weapons Monthly, 1st Issue duplicate of 0x2E800                                         | No                              |
| 12  | 29          | 0x54000  | 0xC800  | mag01.tim                                                | Weapons Monthly, March Issue                                                            | No                              |
| 13  | 30          | 0x60800  | 0xC800  | mag02.tim                                                | Weapons Monthly, April Issue                                                            | No                              |
| 14  | 31          | 0x6D000  | 0xC800  | mag03.tim                                                | Weapons Monthly, May Issue                                                              | No                              |
| 15  | 32          | 0x79800  | 0xC800  | mag04.tim                                                | Weapons Monthly, June Issue                                                             | No                              |
| 16  | 33          | 0x86000  | 0xC800  | mag05.tim                                                | Weapons Monthly, July Issue                                                             | No                              |
| 17  | 34          | 0x92800  | 0xC800  | mag06.tim                                                | Weapons Monthly, August Issue                                                           | No                              |
| 18  | 44          | 0x9F000  | 0xC800  | mag08.tim                                                | Occult Fan I & II                                                                       | No                              |
| 19  | 45          | 0xAB800  | 0xC800  | mag09.tim                                                | Occult Fan III & IV                                                                     | No                              |
| 20  | 48          | 0xB8000  | 0xC800  | mc00.tim                                                 | Card textures for menus (Card Album page N loads header entry 48 + N)                  | No                              |
| 21  | 49          | 0xC4800  | 0xC800  | mc01.tim                                                 | Card textures for menus                                                                 | No                              |
| 22  | 50          | 0xD1000  | 0xC800  | mc02.tim                                                 | Card textures for menus                                                                 | No                              |
| 23  | 51          | 0xDD800  | 0xC800  | mc03.tim                                                 | Card textures for menus                                                                 | No                              |
| 24  | 52          | 0xEA000  | 0xC800  | mc04.tim                                                 | Card textures for menus                                                                 | No                              |
| 25  | 53          | 0xF6800  | 0xC800  | mc05.tim                                                 | Card textures for menus                                                                 | No                              |
| 26  | 54          | 0x103000 | 0xC800  | mc06.tim                                                 | Card textures for menus                                                                 | No                              |
| 27  | 55          | 0x10F800 | 0xC800  | mc07.tim                                                 | Card textures for menus                                                                 | No                              |
| 28  | 56          | 0x11C000 | 0xC800  | mc08.tim                                                 | Card textures for menus                                                                 | No                              |
| 29  | 57          | 0x128800 | 0xC800  | mc09.tim                                                 | Card textures for menus                                                                 | No                              |
| 30  | 63          | 0x135000 | 0x11800 | PSX_Controller00.tim                                     | Field controls tutorial image                                                           | No                              |
| 31  | 64          | 0x146800 | 0x11800 | PSX_Controller01.tim                                     | World map controls tutorial image                                                       | No                              |
| 32  | 65          | 0x158000 | 0x11800 | PSX_Controller02.tim                                     | Battle controls tutorial image                                                          | No                              |
| 33  | 71          | 0x169800 | 0xC800  | mag10.tim                                                | Triple Triad tutorial                                                                   | No                              |
| 34  | 72          | 0x176000 | 0xC800  | mag11.tim                                                | Triple Triad tutorial                                                                   | No                              |
| 35  | 73          | 0x182800 | 0xC800  | mag12.tim                                                | Triple Triad tutorial                                                                   | No                              |
| 36  | 74          | 0x18F000 | 0xC800  | mag13.tim                                                | Battle tutorial                                                                         | No                              |
| 37  | 75          | 0x19B800 | 0xC800  | mag14.tim                                                | Battle tutorial                                                                         | No                              |
| 38  | 87          | 0x1A8000 | 0x3000  | [Mngrp_string_section00](../mngrp-string-section/)  | Book text                                                                               | Yes                             |
| 39  | 88          | 0x1AB000 | 0x800   | [Mngrp_string_section01](../mngrp-string-section/)  | Battle tutorial                                                                         | Yes                             |
| 40  | 89          | 0x1AB800 | 0x1000  | [Mngrp_string_section02](../mngrp-string-section/)  | Card rules + Icon                                                                       | Yes                             |
| 41  | 90          | 0x1AC800 | 0x1000  | [Mngrp_string_section03](../mngrp-string-section/)  | Chocobo World intro story, shown by the save-point Chocobo World screen                | Yes                             |
| 42  | 95          | 0x1AD800 | 0x800   | [Mngrp_string_section04](../mngrp-string-section/)  | Test seed generic text (congrats, fail,...)                                             | Yes                             |
| 43  | 96          | 0x1AE000 | 0x800   | [Mngrp_string_section05](../mngrp-string-section/)  | Test seed 1                                                                             | Yes                             |
| 44  | 97          | 0x1AE800 | 0x800   | [Mngrp_string_section06](../mngrp-string-section/)  | Test seed 2                                                                             | Yes                             |
| 45  | 98          | 0x1AF000 | 0x800   | [Mngrp_string_section07](../mngrp-string-section/)  | Test seed 3                                                                             | Yes                             |
| 46  | 99          | 0x1AF800 | 0x800   | [Mngrp_string_section08](../mngrp-string-section/)  | Test seed 4                                                                             | Yes                             |
| 47  | 100         | 0x1B0000 | 0x800   | [Mngrp_string_section09](../mngrp-string-section/)  | Test seed 5                                                                             | Yes                             |
| 48  | 101         | 0x1B0800 | 0x800   | [Mngrp_string_section10](../mngrp-string-section/)  | Test seed 6                                                                             | Yes                             |
| 49  | 102         | 0x1B1000 | 0x800   | [Mngrp_string_section11](../mngrp-string-section/)  | Test seed 7                                                                             | Yes                             |
| 50  | 103         | 0x1B1800 | 0x800   | [Mngrp_string_section12](../mngrp-string-section/)  | Test seed 8                                                                             | Yes                             |
| 51  | 104         | 0x1B2000 | 0x800   | [Mngrp_string_section13](../mngrp-string-section/)  | Test seed 9                                                                             | Yes                             |
| 52  | 105         | 0x1B2800 | 0x800   | [Mngrp_string_section14](../mngrp-string-section/)  | Test seed 10                                                                            | Yes                             |
| 53  | 106         | 0x1B3000 | 0x800   | [Mngrp_string_section15](../mngrp-string-section/)  | Test seed 11                                                                            | Yes                             |
| 54  | 107         | 0x1B3800 | 0x800   | [Mngrp_string_section16](../mngrp-string-section/)  | Test seed 12                                                                            | Yes                             |
| 55  | 108         | 0x1B4000 | 0x800   | [Mngrp_string_section17](../mngrp-string-section/)  | Test seed 13                                                                            | Yes                             |
| 56  | 109         | 0x1B4800 | 0x800   | [Mngrp_string_section18](../mngrp-string-section/)  | Test seed 14                                                                            | Yes                             |
| 57  | 110         | 0x1B5000 | 0x800   | [Mngrp_string_section19](../mngrp-string-section/)  | Test seed 15                                                                            | Yes                             |
| 58  | 111         | 0x1B5800 | 0x800   | [Mngrp_string_section20](../mngrp-string-section/)  | Test seed 16                                                                            | Yes                             |
| 59  | 112         | 0x1B6000 | 0x800   | [Mngrp_string_section21](../mngrp-string-section/)  | Test seed 17                                                                            | Yes                             |
| 60  | 113         | 0x1B6800 | 0x800   | [Mngrp_string_section22](../mngrp-string-section/)  | Test seed 18                                                                            | Yes                             |
| 61  | 114         | 0x1B7000 | 0x800   | [Mngrp_string_section23](../mngrp-string-section/)  | Test seed 19                                                                            | Yes                             |
| 62  | 115         | 0x1B7800 | 0x800   | [Mngrp_string_section24](../mngrp-string-section/)  | Test seed 20                                                                            | Yes                             |
| 63  | 116         | 0x1B8000 | 0x800   | [Mngrp_string_section25](../mngrp-string-section/)  | Test seed 21                                                                            | Yes                             |
| 64  | 117         | 0x1B8800 | 0x800   | [Mngrp_string_section26](../mngrp-string-section/)  | Test seed 22                                                                            | Yes                             |
| 65  | 118         | 0x1B9000 | 0x800   | [Mngrp_string_section27](../mngrp-string-section/)  | Test seed 23                                                                            | Yes                             |
| 66  | 119         | 0x1B9800 | 0x800   | [Mngrp_string_section28](../mngrp-string-section/)  | Test seed 24                                                                            | Yes                             |
| 67  | 120         | 0x1BA000 | 0x800   | [Mngrp_string_section29](../mngrp-string-section/)  | Test seed 25                                                                            | Yes                             |
| 68  | 121         | 0x1BA800 | 0x800   | [Mngrp_string_section30](../mngrp-string-section/)  | Test seed 26                                                                            | Yes                             |
| 69  | 122         | 0x1BB000 | 0x800   | [Mngrp_string_section31](../mngrp-string-section/)  | Test seed 27                                                                            | Yes                             |
| 70  | 123         | 0x1BB800 | 0x800   | [Mngrp_string_section32](../mngrp-string-section/)  | Test seed 28                                                                            | Yes                             |
| 71  | 124         | 0x1BC000 | 0x800   | [Mngrp_string_section33](../mngrp-string-section/)  | Test seed 29                                                                            | Yes                             |
| 72  | 125         | 0x1BC800 | 0x800   | [Mngrp_string_section34](../mngrp-string-section/)  | Test seed 30                                                                            | Yes                             |
| 73  | 126         | 0x1BD000 | 0x800   | [Mngrp_string_section35](../mngrp-string-section/)  | Test seed 31: unused (the engine caps the test number at 30) and a byte-exact duplicate of Test seed 30 | Yes                             |
| 74  | 127         | 0x1BD800 | 0x800   | [Mngrp_TextBox_map](../mngrp-textbox-section/)       | Map for Complex Strings 00-05                                                           | Yes                             |
| 75  | 128         | 0x1BE000 | 0x4800  | [Mngrp_TextBox_section00](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 76  | 129         | 0x1C2800 | 0x4000  | [Mngrp_TextBox_section01](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 77  | 130         | 0x1C6800 | 0x4800  | [Mngrp_TextBox_section02](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 78  | 131         | 0x1CB000 | 0x4000  | [Mngrp_TextBox_section03](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 79  | 132         | 0x1CF000 | 0x2800  | [Mngrp_TextBox_section04](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 80  | 133         | 0x1D1800 | 0x4800  | [Mngrp_TextBox_section05](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 81  | 160         | 0x1D6000 | 0x1000  | [Mngrp_string_section36](../mngrp-string-section/)  | Junction tutorial                                                                       | Yes                             |
| 82  | 161         | 0x1D7000 | 0x800   | [Mngrp_string_section37](../mngrp-string-section/)  | Magic junction tutorial                                                                 | Yes                             |
| 83  | 162         | 0x1D7800 | 0x800   | [Mngrp_string_section38](../mngrp-string-section/)  | Elemental junction tutorial                                                             | Yes                             |
| 84  | 163         | 0x1D8000 | 0x800   | [Mngrp_string_section39](../mngrp-string-section/)  | Status junction tutorial                                                                | Yes                             |
| 85  | 164         | 0x1D8800 | 0x800   | [Mngrp_string_section40](../mngrp-string-section/)  | GF tutorial                                                                             | Yes                             |
| 86  | 165         | 0x1D9000 | 0x800   | [Mngrp_string_section41](../mngrp-string-section/)  | Squall limit break tutorial                                                             | Yes                             |
| 87  | 166         | 0x1D9800 | 0x800   | [Mngrp_string_section42](../mngrp-string-section/)  | Zell limit break tutorial                                                               | Yes                             |
| 88  | 167         | 0x1DA000 | 0x800   | [Mngrp_string_section43](../mngrp-string-section/)  | Rinoa limit break tutorial                                                              | Yes                             |
| 89  | 168         | 0x1DA800 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): Junction demo                                                     | No                              |
| 90  | 169         | 0x1DB000 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): Magic junction demo                                               | No                              |
| 91  | 170         | 0x1DB800 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): Elemental junction demo                                           | No                              |
| 92  | 171         | 0x1DC000 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): Status junction demo                                              | No                              |
| 93  | 172         | 0x1DC800 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): GF demo                                                           | No                              |
| 94  | 173         | 0x1DD000 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): Squall limit break demo                                           | No                              |
| 95  | 174         | 0x1DD800 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): Zell limit break demo                                             | No                              |
| 96  | 175         | 0x1DE000 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): Rinoa limit break demo                                            | No                              |
| 97  | 176         | 0x1DE800 | 0x800   |                                                          | [Tutorial demo](../mngrp-demo-script/) mock characters A (8 × 152-byte savemap character records)               | No                              |
| 98  | 177         | 0x1DF000 | 0x800   |                                                          | [Tutorial demo](../mngrp-demo-script/) mock GF records A (16 × 68-byte savemap GF records; names misspelled, e.g. "Quetcoatl", replaced by the real save's names in game) | No                              |
| 99  | 178         | 0x1DF800 | 0x800   |                                                          | [Tutorial demo](../mngrp-demo-script/) mock characters B (variant used by elemental/status junction and character switch demos) | No                              |
| 100 | 179         | 0x1E0000 | 0x800   |                                                          | [Tutorial demo](../mngrp-demo-script/) mock GF records B.<br/> Very similar to 0x1DF000                          | No                              |
| 101 | 180         | 0x1E0800 | 0xC800  | mag15.tim                                                | Chocobo world cartoon                                                                   | No                              |
| 102 | 181         | 0x1ED000 | 0xC800  | mag16.tim                                                | Tutorial image                                                                          | No                              |
| 103 | 182         | 0x1F9800 | 0xC800  | mag17.tim                                                | Tutorial image                                                                          | No                              |
| 104 | 183         | 0x206000 | 0xC800  | mag18.tim                                                | Chocobo world sketch cartoon                                                            | No                              |
| 105 | 184         | 0x212800 | 0xC800  | mag19.tim                                                | Chocobo world sketch cartoon.<br/> Duplicate of 0x206000                                | No                              |
| 106 | 188         | 0x21F000 | 0x800   | [m000.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 107 | 189         | 0x21F800 | 0x800   | [m001.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 108 | 190         | 0x220000 | 0x800   | [m002.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 109 | 191         | 0x220800 | 0x800   | [m003.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 110 | 192         | 0x221000 | 0x800   | [m004.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 111 | 196         | 0x221800 | 0x1800  | [m000.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 112 | 197         | 0x223000 | 0x2000  | [m001.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 113 | 198         | 0x225000 | 0x800   | [m002.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 114 | 199         | 0x225800 | 0x800   | [m003.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 115 | 200         | 0x226000 | 0x1800  | [m004.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 116 | 204         | 0x227800 | 0x800   | [Mngrp_string_section44](../mngrp-string-section/)  | Character switch tutorial                                                               | Yes                             |
| 117 | 205         | 0x228000 | 0x800   |                                                          | [Tutorial demo script](../mngrp-demo-script/): Character switch demo                                             | No                              |

## The Chocobo World PocketStation image (Pos 3)

Section 3 is a complete PlayStation memory-card save file holding the Chocobo World PocketStation application:

| Offset | Size   | Description                                                                                  |
|--------|--------|------------------------------------------------------------------------------------------------|
| 0x00   | 2      | "SC" title-frame magic                                                                       |
| 0x02   | 1      | Icon display flag 0x11 (one icon frame)                                                     |
| 0x03   | 1      | Block count: 7 (7 × 8192 = 0xE000, the exact section size)                                  |
| 0x04   | 64     | Shift-JIS title "ＦＦ８／Ｃｈｏｃｏｂｏ　Ｗｏｒｌｄ"                                            |
| 0x50   | 16     | PocketStation fields, including the "MCX0" application marker at 0x52                        |
| 0x60   | 32     | Icon CLUT (16 colors)                                                                       |
| 0x80   | 128    | Icon frame (16×16, 4bpp)                                                                    |
| 0x100  | -      | PocketStation application code and data (438 of 448 128-byte frames are used)                |

The save screen's Chocobo World feature installs this image on the emulated memory card. Prepending a 128-byte
memory-card directory frame turns it into a standard `.mcs` save usable in PS1/PocketStation emulators (the PC
executable embeds no product-code filename, so any name can be used in the directory frame).
