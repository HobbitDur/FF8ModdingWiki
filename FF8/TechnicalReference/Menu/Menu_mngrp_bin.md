---
layout: default
parent: Menu
title: mngrp.bin File Format
permalink: /technical-reference/menu/mngrpbin-file-format/
---

This file is an archive which contains 117 files, that will be called section in this wiki.

It is important to note that the independent files like tkmnmes, m00x.bin or m00x.msg are not used by the game even tho
they exist. Only the data in mngrp is taken into account.

Some sections are pure data that are irrelevant for ShumiTranslator, they are just mention for archive purpose.

This section list is for the english version. Others language should have the same sections but not the same size or offset.

The definition of this file with the different offset and size is determine by [Mngrphd.bin](../mngrphdbin-file-format/).

If the file is modified, it is important to note that all sections need a size multiple of 256. You can fill it with 0 if needed.

## Mapped Data

| Pos | Seek     | Size    | Filename                                                 | Content of the section                                                                  | Present in <br/>ShumiTranslator | 
|-----|----------|---------|----------------------------------------------------------|-----------------------------------------------------------------------------------------|---------------------------------|
| 0   | 0x0      | 0x800   | [tkmnmes1.bin](../tknmnesxbin-file-format/)                          | Menu text                                                                               | Yes                             |
| 1   | 0x800    | 0x1800  | [tkmnmes2.bin](../tknmnesxbin-file-format/)                          | Menu text                                                                               | Yes                             |
| 2   | 0x2000   | 0x2000  | [tkmnmes3.bin](../tknmnesxbin-file-format/)                          | Menu text                                                                               | Yes                             |
| 3   | 0x4000   | 0xE000  |                                                          |                                                                                         | No                              |
| 4   | 0x12000  | 0x1000  |                                                          |                                                                                         | No                              |
| 5   | 0x13000  | 0x6800  | face1.bin                                                | Character portraits                                                                     | No                              |
| 6   | 0x19800  | 0x6800  | face2.bin                                                | GF portraits                                                                            | No                              |
| 7   | 0x20000  | 0x800   | magita.tim                                               | Tutorial/magazine background texture                                                    | No                              |
| 8   | 0x20800  | 0xE000  | start00_and_start01.tim                                  | Title screen logo                                                                       | No                              |
| 9   | 0x2E800  | 0xC800  | mag00.tim                                                | Weapons Monthly, 1st Issue                                                              | No                              |
| 10  | 0x3B000  | 0xC800  | mag07.tim                                                | Pet Pals                                                                                | No                              |
| 11  | 0x47800  | 0xC800  | mag00.tim                                                | Weapons Monthly, 1st Issue duplicate of 0x2E800                                         | No                              |
| 12  | 0x54000  | 0xC800  | mag01.tim                                                | Weapons Monthly, March Issue                                                            | No                              |
| 13  | 0x60800  | 0xC800  | mag02.tim                                                | Weapons Monthly, April Issue                                                            | No                              |
| 14  | 0x6D000  | 0xC800  | mag03.tim                                                | Weapons Monthly, May Issue                                                              | No                              |
| 15  | 0x79800  | 0xC800  | mag04.tim                                                | Weapons Monthly, June Issue                                                             | No                              |
| 16  | 0x86000  | 0xC800  | mag05.tim                                                | Weapons Monthly, July Issue                                                             | No                              |
| 17  | 0x92800  | 0xC800  | mag06.tim                                                | Weapons Monthly, August Issue                                                           | No                              |
| 18  | 0x9F000  | 0xC800  | mag08.tim                                                | Occult Fan I & II                                                                       | No                              |
| 19  | 0xAB800  | 0xC800  | mag09.tim                                                | Occult Fan III & IV                                                                     | No                              |
| 20  | 0xB8000  | 0xC800  | mc00.tim                                                 | Card textures for menus                                                                 | No                              |
| 21  | 0xC4800  | 0xC800  | mc01.tim                                                 | Card textures for menus                                                                 | No                              |
| 22  | 0xD1000  | 0xC800  | mc02.tim                                                 | Card textures for menus                                                                 | No                              |
| 23  | 0xDD800  | 0xC800  | mc03.tim                                                 | Card textures for menus                                                                 | No                              |
| 24  | 0xEA000  | 0xC800  | mc04.tim                                                 | Card textures for menus                                                                 | No                              |
| 25  | 0xF6800  | 0xC800  | mc05.tim                                                 | Card textures for menus                                                                 | No                              |
| 26  | 0x103000 | 0xC800  | mc06.tim                                                 | Card textures for menus                                                                 | No                              |
| 27  | 0x10F800 | 0xC800  | mc07.tim                                                 | Card textures for menus                                                                 | No                              |
| 28  | 0x11C000 | 0xC800  | mc08.tim                                                 | Card textures for menus                                                                 | No                              |
| 29  | 0x128800 | 0xC800  | mc09.tim                                                 | Card textures for menus                                                                 | No                              |
| 30  | 0x135000 | 0x11800 | PSX_Controller00.tim                                     | Field controls tutorial image                                                           | No                              |
| 31  | 0x146800 | 0x11800 | PSX_Controller01.tim                                     | World map controls tutorial image                                                       | No                              |
| 32  | 0x158000 | 0x11800 | PSX_Controller02.tim                                     | Battle controls tutorial image                                                          | No                              |
| 33  | 0x169800 | 0xC800  | mag10.tim                                                | Triple Triad tutorial                                                                   | No                              |
| 34  | 0x176000 | 0xC800  | mag11.tim                                                | Triple Triad tutorial                                                                   | No                              |
| 35  | 0x182800 | 0xC800  | mag12.tim                                                | Triple Triad tutorial                                                                   | No                              |
| 36  | 0x18F000 | 0xC800  | mag13.tim                                                | Battle tutorial                                                                         | No                              |
| 37  | 0x19B800 | 0xC800  | mag14.tim                                                | Battle tutorial                                                                         | No                              |
| 38  | 0x1A8000 | 0x3000  | [Mngrp_string_section00](../mngrp-string-section/)  | Book text                                                                               | Yes                             |
| 39  | 0x1AB000 | 0x800   | [Mngrp_string_section01](../mngrp-string-section/)  | Battle tutorial                                                                         | Yes                             |
| 40  | 0x1AB800 | 0x1000  | [Mngrp_string_section02](../mngrp-string-section/)  | Card rules + Icon                                                                       | Yes                             |
| 41  | 0x1AC800 | 0x1000  | [Mngrp_string_section03](../mngrp-string-section/)  | Chocobo tutorial                                                                        | Yes                             |
| 42  | 0x1AD800 | 0x800   | [Mngrp_string_section04](../mngrp-string-section/)  | Test seed generic text (congrats, fail,...)                                             | Yes                             |
| 43  | 0x1AE000 | 0x800   | [Mngrp_string_section05](../mngrp-string-section/)  | Test seed 1                                                                             | Yes                             |
| 44  | 0x1AE800 | 0x800   | [Mngrp_string_section06](../mngrp-string-section/)  | Test seed 2                                                                             | Yes                             |
| 45  | 0x1AF000 | 0x800   | [Mngrp_string_section07](../mngrp-string-section/)  | Test seed 3                                                                             | Yes                             |
| 46  | 0x1AF800 | 0x800   | [Mngrp_string_section08](../mngrp-string-section/)  | Test seed 4                                                                             | Yes                             |
| 47  | 0x1B0000 | 0x800   | [Mngrp_string_section09](../mngrp-string-section/)  | Test seed 5                                                                             | Yes                             |
| 48  | 0x1B0800 | 0x800   | [Mngrp_string_section10](../mngrp-string-section/)  | Test seed 6                                                                             | Yes                             |
| 49  | 0x1B1000 | 0x800   | [Mngrp_string_section11](../mngrp-string-section/)  | Test seed 7                                                                             | Yes                             |
| 50  | 0x1B1800 | 0x800   | [Mngrp_string_section12](../mngrp-string-section/)  | Test seed 8                                                                             | Yes                             |
| 51  | 0x1B2000 | 0x800   | [Mngrp_string_section13](../mngrp-string-section/)  | Test seed 9                                                                             | Yes                             |
| 52  | 0x1B2800 | 0x800   | [Mngrp_string_section14](../mngrp-string-section/)  | Test seed 10                                                                            | Yes                             |
| 53  | 0x1B3000 | 0x800   | [Mngrp_string_section15](../mngrp-string-section/)  | Test seed 11                                                                            | Yes                             |
| 54  | 0x1B3800 | 0x800   | [Mngrp_string_section16](../mngrp-string-section/)  | Test seed 12                                                                            | Yes                             |
| 55  | 0x1B4000 | 0x800   | [Mngrp_string_section17](../mngrp-string-section/)  | Test seed 13                                                                            | Yes                             |
| 56  | 0x1B4800 | 0x800   | [Mngrp_string_section18](../mngrp-string-section/)  | Test seed 14                                                                            | Yes                             |
| 57  | 0x1B5000 | 0x800   | [Mngrp_string_section19](../mngrp-string-section/)  | Test seed 15                                                                            | Yes                             |
| 58  | 0x1B5800 | 0x800   | [Mngrp_string_section20](../mngrp-string-section/)  | Test seed 16                                                                            | Yes                             |
| 59  | 0x1B6000 | 0x800   | [Mngrp_string_section21](../mngrp-string-section/)  | Test seed 17                                                                            | Yes                             |
| 60  | 0x1B6800 | 0x800   | [Mngrp_string_section22](../mngrp-string-section/)  | Test seed 18                                                                            | Yes                             |
| 61  | 0x1B7000 | 0x800   | [Mngrp_string_section23](../mngrp-string-section/)  | Test seed 19                                                                            | Yes                             |
| 62  | 0x1B7800 | 0x800   | [Mngrp_string_section24](../mngrp-string-section/)  | Test seed 20                                                                            | Yes                             |
| 63  | 0x1B8000 | 0x800   | [Mngrp_string_section25](../mngrp-string-section/)  | Test seed 21                                                                            | Yes                             |
| 64  | 0x1B8800 | 0x800   | [Mngrp_string_section26](../mngrp-string-section/)  | Test seed 22                                                                            | Yes                             |
| 65  | 0x1B9000 | 0x800   | [Mngrp_string_section27](../mngrp-string-section/)  | Test seed 23                                                                            | Yes                             |
| 66  | 0x1B9800 | 0x800   | [Mngrp_string_section28](../mngrp-string-section/)  | Test seed 24                                                                            | Yes                             |
| 67  | 0x1BA000 | 0x800   | [Mngrp_string_section29](../mngrp-string-section/)  | Test seed 25                                                                            | Yes                             |
| 68  | 0x1BA800 | 0x800   | [Mngrp_string_section30](../mngrp-string-section/)  | Test seed 26                                                                            | Yes                             |
| 69  | 0x1BB000 | 0x800   | [Mngrp_string_section31](../mngrp-string-section/)  | Test seed 27                                                                            | Yes                             |
| 70  | 0x1BB800 | 0x800   | [Mngrp_string_section32](../mngrp-string-section/)  | Test seed 28                                                                            | Yes                             |
| 71  | 0x1BC000 | 0x800   | [Mngrp_string_section33](../mngrp-string-section/)  | Test seed 29                                                                            | Yes                             |
| 72  | 0x1BC800 | 0x800   | [Mngrp_string_section34](../mngrp-string-section/)  | Test seed 30                                                                            | Yes                             |
| 73  | 0x1BD000 | 0x800   | [Mngrp_string_section35](../mngrp-string-section/)  | Test seed 31                                                                            | Yes                             |
| 74  | 0x1BD800 | 0x800   | [Mngrp_TextBox_map](../mngrp-textbox-section/)       | Map for Complex Strings 00-05                                                           | Yes                             |
| 75  | 0x1BE000 | 0x4800  | [Mngrp_TextBox_section00](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 76  | 0x1C2800 | 0x4000  | [Mngrp_TextBox_section01](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 77  | 0x1C6800 | 0x4800  | [Mngrp_TextBox_section02](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 78  | 0x1CB000 | 0x4000  | [Mngrp_TextBox_section03](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 79  | 0x1CF000 | 0x2800  | [Mngrp_TextBox_section04](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 80  | 0x1D1800 | 0x4800  | [Mngrp_TextBox_section05](../mngrp-textbox-section/) | TextBox                                                                                 | Yes                             |
| 81  | 0x1D6000 | 0x1000  | [Mngrp_string_section36](../mngrp-string-section/)  | Junction tutorial                                                                       | Yes                             |
| 82  | 0x1D7000 | 0x800   | [Mngrp_string_section37](../mngrp-string-section/)  | Magic junction tutorial                                                                 | Yes                             |
| 83  | 0x1D7800 | 0x800   | [Mngrp_string_section38](../mngrp-string-section/)  | Elemental junction tutorial                                                             | Yes                             |
| 84  | 0x1D8000 | 0x800   | [Mngrp_string_section39](../mngrp-string-section/)  | Status junction tutorial                                                                | Yes                             |
| 85  | 0x1D8800 | 0x800   | [Mngrp_string_section40](../mngrp-string-section/)  | GF tutorial                                                                             | Yes                             |
| 86  | 0x1D9000 | 0x800   | [Mngrp_string_section41](../mngrp-string-section/)  | Squall limit break tutorial                                                             | Yes                             |
| 87  | 0x1D9800 | 0x800   | [Mngrp_string_section42](../mngrp-string-section/)  | Zell limit break tutorial                                                               | Yes                             |
| 88  | 0x1DA000 | 0x800   | [Mngrp_string_section43](../mngrp-string-section/)  | Rinoa limit break tutorial                                                              | Yes                             |
| 89  | 0x1DA800 | 0x800   |                                                          |                                                                                         | No                              |
| 90  | 0x1DB000 | 0x800   |                                                          |                                                                                         | No                              |
| 91  | 0x1DB800 | 0x800   |                                                          |                                                                                         | No                              |
| 92  | 0x1DC000 | 0x800   |                                                          |                                                                                         | No                              |
| 93  | 0x1DC800 | 0x800   |                                                          |                                                                                         | No                              |
| 94  | 0x1DD000 | 0x800   |                                                          |                                                                                         | No                              |
| 95  | 0x1DD800 | 0x800   |                                                          |                                                                                         | No                              |
| 96  | 0x1DE000 | 0x800   |                                                          |                                                                                         | No                              |
| 97  | 0x1DE800 | 0x800   |                                                          |                                                                                         | No                              |
| 98  | 0x1DF000 | 0x800   |                                                          | text with binary data GF names some misspelled/truncated                                | No                              |
| 99  | 0x1DF800 | 0x800   |                                                          |                                                                                         | No                              |
| 100 | 0x1E0000 | 0x800   |                                                          | text with binary data GF names some misspelled/truncated.<br/> Very similar to 0x1DF000 | No                              |
| 101 | 0x1E0800 | 0xC800  | mag15.tim                                                | Chocobo world cartoon                                                                   | No                              |
| 102 | 0x1ED000 | 0xC800  | mag16.tim                                                | Tutorial image                                                                          | No                              |
| 103 | 0x1F9800 | 0xC800  | mag17.tim                                                | Tutorial image                                                                          | No                              |
| 104 | 0x206000 | 0xC800  | mag18.tim                                                | Chocobo world sketch cartoon                                                            | No                              |
| 105 | 0x212800 | 0xC800  | mag19.tim                                                | Chocobo world sketch cartoon.<br/> Duplicate of 0x206000                                | No                              |
| 106 | 0x21F000 | 0x800   | [m000.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 107 | 0x21F800 | 0x800   | [m001.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 108 | 0x220000 | 0x800   | [m002.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 109 | 0x220800 | 0x800   | [m003.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 110 | 0x221000 | 0x800   | [m004.bin](../gf-refinement/refine-abilities/)              | Locations for msg file and Refine values.                                               | Yes                             |
| 111 | 0x221800 | 0x1800  | [m000.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 112 | 0x223000 | 0x2000  | [m001.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 113 | 0x225000 | 0x800   | [m002.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 114 | 0x225800 | 0x800   | [m003.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 115 | 0x226000 | 0x1800  | [m004.msg](../gf-refinement/refine-abilities/)              |                                                                                         | Yes                             |
| 116 | 0x227800 | 0x800   | [Mngrp_string_section44](../mngrp-string-section/)  | Character switch tutorial                                                               | Yes                             |
| 117 | 0x228000 | 0x800   |                                                          |                                                                                         | No                              |
