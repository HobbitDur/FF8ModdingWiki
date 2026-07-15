---
layout: default
parent: Miscellaneous
title: String_Encoding
permalink: /technical-reference/miscellaneous/string-encoding/
---
 For String encoding, you can  find the info on the wiki of the [ShumiTranslator](https://github.com/HobbitDur/ShumiTranslator/wiki/FF8_char) tool done by HobbitDur which detail the following file (link is kept here to the old wiki for archive purpose):

# String Encoding

FF8 strings are converted to byte arrays.[Char Table](https://sourceforge.net/p/ifrit/code-0/HEAD/tree/trunk%20ifrit-code-0/Resources/textformat.ifr) Some of which aligns to the grid of text in the texture if you -32 from the value. Some values are 1 byte = 2 characters, most are 1 byte = 1 character. There are also special bytes that use up 1-3 bytes.

## Special Bytes

These bytes are points where things are inserted or a change in formatting. Some just say to ignore this string unless the player unlocked something.

The full, up-to-date opcode map (including the recovered meanings of `0x07`, `0x08`, `0x0A`, `0x0D`
and `0x0F`) lives in [FF8 Char - Control opcode overview]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8Char#control-opcode-overview).
A summary follows.

| Starting byte | Size | Name | Description |
|---------------|------|------|-------------|
| 0x00 | 1 | NULL | End of string. |
| 0x01 | 1 | NewPage | Ends the page: wait for input, clear the window, show the next page. |
| 0x02 | 1 | `\n` | New line. Some areas ignore it. |
| 0x03 | 2 | Name | Inserts a character name (`0x03 ??`). |
| 0x04 | 2 | Var | Inserts a numeric variable from the active text layer. |
| 0x05 | 2 | Icon | Draws a symbol from `icon.tex` (controller buttons; on PC the assigned keyboard keys). |
| 0x06 | 2 | Color | Changes text color / blink. |
| 0x07 | 1 | NewPage (variant) | Page break; handled the same as `0x01`. |
| 0x08 | 2 | *(unused)* | Reserved; consumes a param byte, no visible output. |
| 0x09 | 2 | Wait | Pause for N frames. |
| 0x0A | 2 | Value (context) | Inserts a number or string filled in by the active screen; meaning depends on the screen. |
| 0x0B | 2-3 | Cursor location | Cursor stop / choice position. 2 bytes for Yes/No, 3 bytes for multi-choice lists. |
| 0x0C | 2 | GF name | Inserts a Guardian Force name. |
| 0x0D | 2 | *(unused)* | Reserved; consumes a param byte, no visible output. |
| 0x0E | 2 | Location/Word | Inserts a location or generic (language-dependent) word. |
| 0x0F | 2 | *(unused)* | Reserved; consumes a param byte, no visible output. |
| 0x19-0x1F | 2 | Extended glyph | Japanese / extended two-byte glyph pages. |
