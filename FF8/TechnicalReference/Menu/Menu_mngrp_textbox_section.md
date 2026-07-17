---
layout: default
parent: Menu
title: Mngrp Textbox Section
permalink: /technical-reference/menu/mngrp-textbox-section/
---

# TextBox

<img src="https://github.com/user-attachments/assets/6f73a84e-9cf3-4721-8d95-854a524f3270" width="300">

TextBox are mainly found in the menu, for example for the tutorial.
They can be composed of:

* An ID
* A title
* A parent TextBox ID (the one we used to get to the current TextBox)
* Often different [cursor location id]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8Char#cursor-location-id)
* Button info
* And sometimes a left box id and/or a right box id to be able to move with the left or right cross.

These pages power the **Information menu** (main menu → Information): a hypertext browser (menu program 21)
with links, a parent page per entry and a 127-deep navigation history.

There are 6 sections with string info in it (raw files 128-133 of [mngrp.bin](../mngrpbin-file-format/)), and before those a
"Seek map" section (raw file 127) which indicates the position of every String Entry.

## Seek Map

The seek map (raw file 127, loaded to its own buffer at menu start of the Information browser) is composed of
4 bytes containing the number of seek locations, then 4 bytes per seek location. So the total size of the seek
map is 4 + 4*(Number seek). The seek index is the **page id** used by links and by the parent/left/right fields.

### Number seek

| Type   | Size | Value | Description               |
|--------|------|-------|---------------------------|
| UInt32 | 4    | Count | Number of seek locations. |

### Seek location info

| Type   | Size | Value           | Description                                        |
|--------|------|-----------------|----------------------------------------------------|
| UInt16 | 2    | Seek\_Location  | From beginning of section to start of String Entry |
| UInt16 | 2    | Section\_Number | 0-5                                                |

## String Entry

Then each string complex section is composed of the following data:

| Type                                                                               | Size                           | Value             | Description                                                                                                      |
|------------------------------------------------------------------------------------|--------------------------------|-------------------|------------------------------------------------------------------------------------------------------------------|
| UInt16                                                                             | 2                              | Parent TextBox ID | **0xFFFF** for the first TextBox                                                                                 |
| UInt16                                                                             | 2                              | Left TextBox ID   | **0xFFFF** if no TextBox linked                                                                                  |
| UInt16                                                                             | 2                              | Right TextBox ID  | **0xFFFF** if no TextBox linked                                                                                  |
| UInt16                                                                             | 2                              | Entry\_Length     | Exact length of the entry in bytes, from the start of the entry, terminators included.                          |
| [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String) | Depends                        | Title             | The title of the TextBox, no offset specified to know the end. <br/>The **0x00** determines the end of the title |
| [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String) | Entry\_Length - 8 - Title_size | TextBox content   | The text in the TextBox, ends with **0x00**                                                                     |

Entries start on a **4-byte boundary**: the next entry begins at `align4(entry_start + Entry_Length)`, so 0 to 3
padding bytes (0x00) can follow an entry.

## How the engine reads an entry

The in-game information browser locates an entry through the Seek Map, then:

* reads the three link IDs at +0/+2/+4 (Parent is followed with the Square button, the two others with the
  page-navigation buttons; **0xFFFF** disables the button),
* **ignores Entry_Length entirely**,
* copies the title from +8 up to its **0x00** terminator,
* takes the content as the string starting right after the title terminator.

So Entry_Length and the 4-byte alignment are storage conventions of the original files rather than something the
browser depends on, but tools should preserve them.

## Content control codes

Besides the normal [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String) codes, the
Information browser interprets two extra codes inside the TextBox content:

* **0x0A n** — visibility / dynamic value:
  * n = 0x3F: the following text is always visible;
  * n = 0x40-0xBF: the following text is only visible if bit (n - 0x40) of the savemap tutorial-info
    bitfield is set (topics unlocked as the story progresses);
  * n ≥ 0xC0: inserts a live counter as digits: (n - 0xC0) = 0 steps walked, 1 total battles, 2 battles won,
    3 battles escaped, 16-23 kill count of character 0-7, 24-31 KO count of character 0-7, 32-47 kill count
    of GF 0-15, 48-63 KO count of GF 0-15.
* **0x0B a b** — link hotspot: places a selectable cursor position at the current text location, jumping to
  page id (a << 7) + b - 4128 on confirm.

## Engine addresses (FF8 PC 2000, FF8_EN.exe)

| Address  | Name       | Role                                                                     |
|----------|------------|--------------------------------------------------------------------------|
| 0x4D5F10 | Menu_InfoBrowser_Update | Loads TextBox sections (mngrphd entry 128 + section number) and resolves entries via the map |
| 0x4D6B20 | Menu_InfoBrowser_ParseContent | Parses a page content: control codes above, link hotspots, text metrics |
| 0x4D5E00 | (program 21 init) | Builds the topic list (EXE table 0xB88578 filtered by unlocked topics) and loads the seek map (raw 127) |
| 0x1D82E48 | (loaded Seek Map)    | RAM copy of the map; entries from +4: per page {LOWORD: entry offset, HIWORD: section number} |
