---
layout: default
title: Field Opcodes
parent: Field
nav_order: 2
author: Aali, myst6re, Shard
permalink: /technical-reference/field/field-opcodes/
toc: false
---

## The language

The field script language in ff8 is a simple assembly language with a stack. Here is an example:

```
stack =  []

PSHM_W   1024 # push  var1024  onto  the  stack  (stack =  [var1024])  
PSHN_L   6 # push  number  6  onto  the  stack  (stack =  [6Â ; var1024])  
CAL      EQ # compare  the  two  numbers  at  the  top  of  the  stack, pop  this  numbers, and  push  the  result  (1  or  0)  into  the  stack  (stack =  [1  or  0])    
JPF      LABEL1 # if  the  popped  top  of  the  stack  is  0, jump  to  LABEL1  (stack =  [])  
PSHN_L   0 # push  0  at  the  top  of  the  stack  (stack =  [0])  
POPM_W   1024 # pop  the  top  of  the  stack  into  var1024  (stack =  [])  
JMP      LABEL2 # goto  LABEL2  
LABEL1          
PSHN_L   1 # push  1  at  the  top  of  the  stack  (stack =  [1])  
POPM_W   1024 # pop  the  top  of  the  stack  into  var1024  (stack =  [])  
LABEL2  
...
```

In standard code, it's equivalent to:

```
if(var1024 == 6)  {  
        var1024 = 0;  
} else {  
        var1024 = 1;  
}
```

## Reading Documentation

Each Opcode's page lists all the parameters for that function in the order you would put them on the stack before the function call. The inline argument is
listed separately, if the function requires one. For example, on the page for [SET3](01E-set3), the parameters are listed like this:

*XCoord*

*YCoord*

*ZCoord*

**SET3**

Which means when you call **SET3**, the ZCoord is the top item on the stack, YCoord is under it, and XCoord is under that, for example

```
PSHN_L            402      (XCoord)
PSHN_L -381    (YCoord)  
PSHN_L            20        (ZCoord)  
SET3                17        (walkmesh  triangle  ID)
```

## Opcode list

| Opcode | Name                                     | Function Type      |
|--------|------------------------------------------|--------------------|
| 000    | [000 NOP](000-nop)                       | Script Processing  |
| 001    | [001 CAL](001-cal)                       | Script Processing  |
| 002    | [002 JMP](002-jmp)                       | Script Processing  |
| 003    | [003 JPF](003-jpf)                       | Script Processing  |
| 004    | [004 GJMP](004-gjmp)                     | Script Processing  |
| 005    | [005 LBL](005-lbl)                       | Script Processing  |
| 006    | [006 RET](006-ret)                       | Script Processing  |
| 007    | [007 PSHN_L](007-pshn-l)                 | Memory             |
| 008    | [008 PSHI_L](008-pshi-l)                 | Memory             |
| 009    | [009 POPI_L](009-popi-l)                 | Memory             |
| 00A    | [00A PSHM_B](00a-pshm-b)                 | Memory             |
| 00B    | [00B POPM_B](00b-popm-b)                 | Memory             |
| 00C    | [00C PSHM_W](00c-pshm-w)                 | Memory             |
| 00D    | [00D POPM_W](00d-popm-w)                 | Memory             |
| 00E    | [00E PSHM_L](00e-pshm-l)                 | Memory             |
| 00F    | [00F POPM_L](00f-popm-l)                 | Memory             |
| 010    | [010 PSHSM_B](010-pshsm-b)               | Memory             |
| 011    | [011 PSHSM_W](011-pshsm-w)               | Memory             |
| 012    | [012 PSHSM_L](012-pshsm-l)               | Memory             |
| 013    | [013 PSHAC](013-pshac)                   | Memory             |
| 014    | [014 REQ](014-req)                       | Script Processing  |
| 015    | [015 REQSW](015-reqsw)                   | Script Processing  |
| 016    | [016 REQEW](016-reqew)                   | Script Processing  |
| 017    | [017 PREQ](017-preq)                     | Script Processing  |
| 018    | [018 PREQSW](018-preqsw)                 | Script Processing  |
| 019    | [019 PREQEW](019-preqew)                 | Script Processing  |
| 01A    | [01A UNUSE](01a-unuse)                   | Entity             |
| 01B    | [01B DEBUG](01b-debug)                   |                    |
| 01C    | [01C HALT](01c-halt)                     | Script Processing  |
| 01D    | [01D SET](01d-set)                       | Entity             |
| 01E    | [01E SET3](01e-set3)                     | Entity             |
| 01F    | [01F IDLOCK](01f-idlock)                 | Field related      |
| 020    | [020 IDUNLOCK](020-idunlock)             | Field related      |
| 021    | [021 EFFECTPLAY2](021-effectplay2)       | Music and Sound    |
| 022    | [022 FOOTSTEP](022-footstep)             |                    |
| 023    | [023 JUMP](023-jump)                     | Entity             |
| 024    | [024 JUMP3](024-jump3)                   | Entity             |
| 025    | [025 LADDERUP](025-ladderup)             | Entity             |
| 026    | [026 LADDERDOWN](026-ladderdown)         | Entity             |
| 027    | [027 LADDERUP2](027-ladderup2)           | Entity             |
| 028    | [028 LADDERDOWN2](028-ladderdown2)       | Entity             |
| 029    | [029 MAPJUMP](029-mapjump)               | Field related      |
| 02A    | [02A MAPJUMP3](02a-mapjump3)             | Field related      |
| 02B    | [02B SETMODEL](02b-setmodel)             | Entity             |
| 02C    | [02C BASEANIME](02c-baseanime)           | Animation          |
| 02D    | [02D ANIME](02d-anime)                   | Animation          |
| 02E    | [02E ANIMEKEEP](02e-animekeep)           | Animation          |
| 02F    | [02F CANIME](02f-canime)                 | Animation          |
| 030    | [030 CANIMEKEEP](030-canimekeep)         | Animation          |
| 031    | [031 RANIME](031-ranime)                 | Animation          |
| 032    | [032 RANIMEKEEP](032-ranimekeep)         | Animation          |
| 033    | [033 RCANIME](033-rcanime)               | Animation          |
| 034    | [034 RCANIMEKEEP](034-rcanimekeep)       | Animation          |
| 035    | [035 RANIMELOOP](035-ranimeloop)         | Animation          |
| 036    | [036 RCANIMELOOP](036-rcanimeloop)       | Animation          |
| 037    | [037 LADDERANIME](037-ladderanime)       | Animation          |
| 038    | [038 DISCJUMP](038-discjump)             | Field related      |
| 039    | [039 SETLINE](039-setline)               | Entity             |
| 03A    | [03A LINEON](03a-lineon)                 | Entity             |
| 03B    | [03B LINEOFF](03b-lineoff)               | Entity             |
| 03C    | [03C WAIT](03c-wait)                     | Script Processing  |
| 03D    | [03D MSPEED](03d-mspeed)                 |                    |
| 03E    | [03E MOVE](03e-move)                     | Entity             |
| 03F    | [03F MOVEA](03f-movea)                   |                    |
| 040    | [040 PMOVEA](040-pmovea)                 |                    |
| 041    | [041 CMOVE](041-cmove)                   |                    |
| 042    | [042 FMOVE](042-fmove)                   |                    |
| 043    | [043 PJUMPA](043-pjumpa)                 |                    |
| 044    | [044 ANIMESYNC](044-animesync)           | Script Processing  |
| 045    | [045 ANIMESTOP](045-animestop)           | Animation          |
| 046    | [046 MESW](046-mesw)                     |                    |
| 047    | [047 MES](047-mes)                       | Message            |
| 048    | [048 MESSYNC](048-messync)               | Script Processing  |
| 049    | [049 MESVAR](049-mesvar)                 | Message            |
| 04A    | [04A ASK](04a-ask)                       | Message            |
| 04B    | [04B WINSIZE](04b-winsize)               | Message            |
| 04C    | [04C WINCLOSE](04c-winclose)             | Message            |
| 04D    | [04D UCON](04d-ucon)                     | Misc               |
| 04E    | [04E UCOFF](04e-ucoff)                   | Misc               |
| 04F    | [04F MOVIE](04f-movie)                   | Movie              |
| 050    | [050 MOVIESYNC](050-moviesync)           | Script Processing  |
| 051    | [051 SETPC](051-setpc)                   | Party management   |
| 052    | [052 DIR](052-dir)                       | Entity             |
| 053    | [053 DIRP](053-dirp)                     |                    |
| 054    | [054 DIRA](054-dira)                     |                    |
| 055    | [055 PDIRA](055-pdira)                   |                    |
| 056    | [056 SPUREADY](056-spuready)             | Timer              |
| 057    | [057 TALKON](057-talkon)                 | Entity             |
| 058    | [058 TALKOFF](058-talkoff)               | Entity             |
| 059    | [059 PUSHON](059-pushon)                 | Entity             |
| 05A    | [05A PUSHOFF](05a-pushoff)               | Entity             |
| 05B    | [05B ISTOUCH](05b-istouch)               |                    |
| 05C    | [05C MAPJUMPO](05c-mapjumpo)             | Field related      |
| 05D    | [05D MAPJUMPON](05d-mapjumpon)           | Field related      |
| 05E    | [05E MAPJUMPOFF](05e-mapjumpoff)         | Field related      |
| 05F    | [05F SETMESSPEED](05f-setmesspeed)       | Message            |
| 060    | [060 SHOW](060-show)                     | Entity             |
| 061    | [061 HIDE](061-hide)                     | Entity             |
| 062    | [062 TALKRADIUS](062-talkradius)         | Entity             |
| 063    | [063 PUSHRADIUS](063-pushradius)         | Entity             |
| 064    | [064 AMESW](064-amesw)                   | Message            |
| 065    | [065 AMES](065-ames)                     | Message            |
| 066    | [066 GETINFO](066-getinfo)               |                    |
| 067    | [067 THROUGHON](067-throughon)           | Entity             |
| 068    | [068 THROUGHOFF](068-throughoff)         | Entity             |
| 069    | [069 BATTLE](069-battle)                 | Battle             |
| 06A    | [06A BATTLERESULT](06a-battleresult)     | Battle             |
| 06B    | [06B BATTLEON](06b-battleon)             | Field related      |
| 06C    | [06C BATTLEOFF](06c-battleoff)           | Field related      |
| 06D    | [06D KEYSCAN](06d-keyscan)               | Input              |
| 06E    | [06E KEYON](06e-keyon)                   | Input              |
| 06F    | [06F AASK](06f-aask)                     | Message            |
| 070    | [070 PGETINFO](070-pgetinfo)             |                    |
| 071    | [071 DSCROLL](071-dscroll)               |                    |
| 072    | [072 LSCROLL](072-lscroll)               |                    |
| 073    | [073 CSCROLL](073-cscroll)               |                    |
| 074    | [074 DSCROLLA](074-dscrolla)             |                    |
| 075    | [075 LSCROLLA](075-lscrolla)             |                    |
| 076    | [076 CSCROLLA](076-cscrolla)             |                    |
| 077    | [077 SCROLLSYNC](077-scrollsync)         | Script Processing  |
| 078    | [078 RMOVE](078-rmove)                   |                    |
| 079    | [079 RMOVEA](079-rmovea)                 |                    |
| 07A    | [07A RPMOVEA](07a-rpmovea)               |                    |
| 07B    | [07B RCMOVE](07b-rcmove)                 |                    |
| 07C    | [07C RFMOVE](07c-rfmove)                 |                    |
| 07D    | [07D MOVESYNC](07d-movesync)             | Script Processing  |
| 07E    | [07E CLEAR](07e-clear)                   | Field related      |
| 07F    | [07F DSCROLLP](07f-dscrollp)             |                    |
| 080    | [080 LSCROLLP](080-lscrollp)             |                    |
| 081    | [081 CSCROLLP](081-cscrollp)             |                    |
| 082    | [082 LTURNR](082-lturnr)                 |                    |
| 083    | [083 LTURNL](083-lturnl)                 |                    |
| 084    | [084 CTURNR](084-cturnr)                 |                    |
| 085    | [085 CTURNL](085-cturnl)                 |                    |
| 086    | [086 ADDPARTY](086-addparty)             | Party Management   |
| 087    | [087 SUBPARTY](087-subparty)             | Party Management   |
| 088    | [088 CHANGEPARTY](088-changeparty)       | Party Management   |
| 089    | [089 REFRESHPARTY](089-refreshparty)     | Party Management   |
| 08A    | [08A SETPARTY](08a-setparty)             | Party Management   |
| 08B    | [08B ISPARTY](08b-isparty)               | Party Management   |
| 08C    | [08C ADDMEMBER](08c-addmember)           | Party Management   |
| 08D    | [08D SUBMEMBER](08d-submember)           | Party Management   |
| 08E    | [08E ISMEMBER](08e-ismember)             | Party Management   |
| 08F    | [08F LTURN](08f-lturn)                   |                    |
| 090    | [090 CTURN](090-cturn)                   |                    |
| 091    | [091 PLTURN](091-plturn)                 |                    |
| 092    | [092 PCTURN](092-pcturn)                 |                    |
| 093    | [093 JOIN](093-join)                     | Entity             |
| 094    | [094 MESFORCUS](094-mesforcus)           |                    |
| 095    | [095 BGANIME](095-bganime)               | Field related      |
| 096    | [096 RBGANIME](096-rbganime)             | Field related      |
| 097    | [097 RBGANIMELOOP](097-rbganimeloop)     | Field related      |
| 098    | [098 BGANIMESYNC](098-bganimesync)       | Field related      |
| 099    | [099 BGDRAW](099-bgdraw)                 | Field related      |
| 09A    | [09A BGOFF](09a-bgoff)                   | Field related      |
| 09B    | [09B BGANIMESPEED](09b-bganimespeed)     | Field related      |
| 09C    | [09C SETTIMER](09c-settimer)             | Timer              |
| 09D    | [09D DISPTIMER](09d-disptimer)           | Timer              |
| 09E    | [09E SHADETIMER](09e-shadetimer)         |                    |
| 09F    | [09F SETGETA](09f-setgeta)               |                    |
| 0A0    | [0A0 SETROOTTRANS](0a0-setroottrans)     |                    |
| 0A1    | [0A1 SETVIBRATE](0a1-setvibrate)         |                    |
| 0A2    | [0A2 STOPVIBRATE](0a2-stopvibrate)       |                    |
| 0A3    | [0A3 MOVIEREADY](0a3-movieready)         | Movie              |
| 0A4    | [0A4 GETTIMER](0a4-gettimer)             | Timer              |
| 0A5    | [0A5 FADEIN](0a5-fadein)                 | Field related      |
| 0A6    | [0A6 FADEOUT](0a6-fadeout)               | Field related      |
| 0A7    | [0A7 FADESYNC](0a7-fadesync)             | Script Processing  |
| 0A8    | [0A8 SHAKE](0a8-shake)                   | Field related      |
| 0A9    | [0A9 SHAKEOFF](0a9-shakeoff)             | Field related      |
| 0AA    | [0AA FADEBLACK](0aa-fadeblack)           | Field related      |
| 0AB    | [0AB FOLLOWOFF](0ab-followoff)           |                    |
| 0AC    | [0AC FOLLOWON](0ac-followon)             |                    |
| 0AD    | [0AD GAMEOVER](0ad-gameover)             | Field related      |
| 0AE    | [0AE ENDING](0ae-ending)                 |                    |
| 0AF    | [0AF SHADELEVEL](0af-shadelevel)         |                    |
| 0B0    | [0B0 SHADEFORM](0b0-shadeform)           |                    |
| 0B1    | [0B1 FMOVEA](0b1-fmovea)                 |                    |
| 0B2    | [0B2 FMOVEP](0b2-fmovep)                 |                    |
| 0B3    | [0B3 SHADESET](0b3-shadeset)             |                    |
| 0B4    | [0B4 MUSICCHANGE](0b4-musicchange)       | Music and Sound    |
| 0B5    | [0B5 MUSICLOAD](0b5-musicload)           | Music and Sound    |
| 0B6    | [0B6 FADENONE](0b6-fadenone)             |                    |
| 0B7    | [0B7 POLYCOLOR](0b7-polycolor)           |                    |
| 0B8    | [0B8 POLYCOLORALL](0b8-polycolorall)     |                    |
| 0B9    | [0B9 KILLTIMER](0b9-killtimer)           | Timer              |
| 0BA    | [0BA CROSSMUSIC](0ba-crossmusic)         |                    |
| 0BB    | [0BB DUALMUSIC](0bb-dualmusic)           |                    |
| 0BC    | [0BC EFFECTPLAY](0bc-effectplay)         | Music and Sound    |
| 0BD    | [0BD EFFECTLOAD](0bd-effectload)         | Music and Sound    |
| 0BE    | [0BE LOADSYNC](0be-loadsync)             |                    |
| 0BF    | [0BF MUSICSTOP](0bf-musicstop)           | Music and Sound    |
| 0C0    | [0C0 MUSICVOL](0c0-musicvol)             | Music and Sound    |
| 0C1    | [0C1 MUSICVOLTRANS](0c1-musicvoltrans)   | Music and Sound    |
| 0C2    | [0C2 MUSICVOLFADE](0c2-musicvolfade)     | Music and Sound    |
| 0C3    | [0C3 ALLSEVOL](0c3-allsevol)             | Music and Sound    |
| 0C4    | [0C4 ALLSEVOLTRANS](0c4-allsevoltrans)   | Music and Sound    |
| 0C5    | [0C5 ALLSEPOS](0c5-allsepos)             | Music and Sound    |
| 0C6    | [0C6 ALLSEPOSTRANS](0c6-allsepostrans)   | Music and Sound    |
| 0C7    | [0C7 SEVOL](0c7-sevol)                   | Music and Sound    |
| 0C8    | [0C8 SEVOLTRANS](0c8-sevoltrans)         | Music and Sound    |
| 0C9    | [0C9 SEPOS](0c9-sepos)                   | Music and Sound    |
| 0CA    | [0CA SEPOSTRANS](0ca-sepostrans)         | Music and Sound    |
| 0CB    | [0CB SETBATTLEMUSIC](0cb-setbattlemusic) | Music and Sound    |
| 0CC    | [0CC BATTLEMODE](0cc-battlemode)         | Battle             |
| 0CD    | [0CD SESTOP](0cd-sestop)                 | Music and Sound    |
| 0CE    | [0CE BGANIMEFLAG](0ce-bganimeflag)       |                    |
| 0CF    | [0CF INITSOUND](0cf-initsound)           |                    |
| 0D0    | [0D0 BGSHADE](0d0-bgshade)               |                    |
| 0D1    | [0D1 BGSHADESTOP](0d1-bgshadestop)       |                    |
| 0D2    | [0D2 RBGSHADELOOP](0d2-rbgshadeloop)     |                    |
| 0D3    | [0D3 DSCROLL2](0d3-dscroll2)             |                    |
| 0D4    | [0D4 LSCROLL2](0d4-lscroll2)             |                    |
| 0D5    | [0D5 CSCROLL2](0d5-cscroll2)             |                    |
| 0D6    | [0D6 DSCROLLA2](0d6-dscrolla2)           |                    |
| 0D7    | [0D7 LSCROLLA2](0d7-lscrolla2)           |                    |
| 0D8    | [0D8 CSCROLLA2](0d8-cscrolla2)           |                    |
| 0D9    | [0D9 DSCROLLP2](0d9-dscrollp2)           |                    |
| 0DA    | [0DA LSCROLLP2](0da-lscrollp2)           |                    |
| 0DB    | [0DB CSCROLLP2](0db-cscrollp2)           |                    |
| 0DC    | [0DC SCROLLSYNC2](0dc-scrollsync2)       |                    |
| 0DD    | [0DD SCROLLMODE2](0dd-scrollmode2)       |                    |
| 0DE    | [0DE MENUENABLE](0de-menuenable)         | Menus              |
| 0DF    | [0DF MENUDISABLE](0df-menudisable)       | Menus              |
| 0E0    | [0E0 FOOTSTEPON](0e0-footstepon)         |                    |
| 0E1    | [0E1 FOOTSTEPOFF](0e1-footstepoff)       |                    |
| 0E2    | [0E2 FOOTSTEPOFFALL](0e2-footstepoffall) |                    |
| 0E3    | [0E3 FOOTSTEPCUT](0e3-footstepcut)       |                    |
| 0E4    | [0E4 PREMAPJUMP](0e4-premapjump)         |                    |
| 0E5    | [0E5 USE](0e5-use)                       | Entity             |
| 0E6    | [0E6 SPLIT](0e6-split)                   | Entity             |
| 0E7    | [0E7 ANIMESPEED](0e7-animespeed)         | Animation          |
| 0E8    | [0E8 RND](0e8-rnd)                       |                    |
| 0E9    | [0E9 DCOLADD](0e9-dcoladd)               |                    |
| 0EA    | [0EA DCOLSUB](0ea-dcolsub)               |                    |
| 0EB    | [0EB TCOLADD](0eb-tcoladd)               |                    |
| 0EC    | [0EC TCOLSUB](0ec-tcolsub)               |                    |
| 0ED    | [0ED FCOLADD](0ed-fcoladd)               | Field related      |
| 0EE    | [0EE FCOLSUB](0ee-fcolsub)               | Field related      |
| 0EF    | [0EF COLSYNC](0ef-colsync)               | Script processing  |
| 0F0    | [0F0 DOFFSET](0f0-doffset)               |                    |
| 0F1    | [0F1 LOFFSETS](0f1-loffsets)             |                    |
| 0F2    | [0F2 COFFSETS](0f2-coffsets)             |                    |
| 0F3    | [0F3 LOFFSET](0f3-loffset)               |                    |
| 0F4    | [0F4 COFFSET](0f4-coffset)               |                    |
| 0F5    | [0F5 OFFSETSYNC](0f5-offsetsync)         |                    |
| 0F6    | [0F6 RUNENABLE](0f6-runenable)           | Entity             |
| 0F7    | [0F7 RUNDISABLE](0f7-rundisable)         | Entity             |
| 0F8    | [0F8 MAPFADEOFF](0f8-mapfadeoff)         | Field related      |
| 0F9    | [0F9 MAPFADEON](0f9-mapfadeon)           | Field related      |
| 0FA    | [0FA INITTRACE](0fa-inittrace)           |                    |
| 0FB    | [0FB SETDRESS](0fb-setdress)             | Entity             |
| 0FC    | [0FC GETDRESS](0fc-getdress)             | Entity             |
| 0FD    | [0FD FACEDIR](0fd-facedir)               | Entity             |
| 0FE    | [0FE FACEDIRA](0fe-facedira)             |                    |
| 0FF    | [0FF FACEDIRP](0ff-facedirp)             |                    |
| 100    | [100 FACEDIRLIMIT](100-facedirlimit)     |                    |
| 101    | [101 FACEDIROFF](101-facediroff)         |                    |
| 102    | [102 SARALYOFF](102-saralyoff)           |                    |
| 103    | [103 SARALYON](103-saralyon)             |                    |
| 104    | [104 SARALYDISPOFF](104-saralydispoff)   |                    |
| 105    | [105 SARALYDISPON](105-saralydispon)     |                    |
| 106    | [106 MESMODE](106-mesmode)               | Message            |
| 107    | [107 FACEDIRINIT](107-facedirinit)       |                    |
| 108    | [108 FACEDIRI](108-facediri)             |                    |
| 109    | [109 JUNCTION](109-junction)             | Party Management   |
| 10A    | [10A SETCAMERA](10a-setcamera)           | Field related      |
| 10B    | [10B BATTLECUT](10b-battlecut)           |                    |
| 10C    | [10C FOOTSTEPCOPY](10c-footstepcopy)     |                    |
| 10D    | [10D WORLDMAPJUMP](10d-worldmapjump)     | Field related      |
| 10E    | [10E RFACEDIRI](10e-rfacediri)           |                    |
| 10F    | [10F RFACEDIR](10f-rfacedir)             |                    |
| 110    | [110 RFACEDIRA](110-rfacedira)           |                    |
| 111    | [111 RFACEDIRP](111-rfacedirp)           |                    |
| 112    | [112 RFACEDIROFF](112-rfacediroff)       |                    |
| 113    | [113 FACEDIRSYNC](113-facedirsync)       |                    |
| 114    | [114 COPYINFO](114-copyinfo)             |                    |
| 115    | [115 PCOPYINFO](115-pcopyinfo)           |                    |
| 116    | [116 RAMESW](116-ramesw)                 | Message            |
| 117    | [117 BGSHADEOFF](117-bgshadeoff)         | Field related      |
| 118    | [118 AXIS](118-axis)                     |                    |
| 119    | [119 AXISSYNC](119-axissync)             |                    |
| 11A    | [11A MENUNORMAL](11a-menunormal)         | Menus              |
| 11B    | [11B MENUPHS](11b-menuphs)               | Menus              |
| 11C    | [11C BGCLEAR](11c-bgclear)               |                    |
| 11D    | [11D GETPARTY](11d-getparty)             | Party Management   |
| 11E    | [11E MENUSHOP](11e-menushop)             | Menus              |
| 11F    | [11F DISC](11f-disc)                     | Field related      |
| 120    | [120 DSCROLL3](120-dscroll3)             |                    |
| 121    | [121 LSCROLL3](121-lscroll3)             |                    |
| 122    | [122 CSCROLL3](122-cscroll3)             |                    |
| 123    | [123 MACCEL](123-maccel)                 |                    |
| 124    | [124 MLIMIT](124-mlimit)                 |                    |
| 125    | [125 ADDITEM](125-additem)               | Item/Magic/Card/GF |
| 126    | [126 SETWITCH](126-setwitch)             |                    |
| 127    | [127 SETODIN](127-setodin)               |                    |
| 128    | [128 RESETGF](128-resetgf)               |                    |
| 129    | [129 MENUNAME](129-menuname)             | Menus              |
| 12A    | [12A REST](12a-rest)                     |                    |
| 12B    | [12B MOVECANCEL](12b-movecancel)         |                    |
| 12C    | [12C PMOVECANCEL](12c-pmovecancel)       |                    |
| 12D    | [12D ACTORMODE](12d-actormode)           |                    |
| 12E    | [12E MENUSAVE](12e-menusave)             | Menus              |
| 12F    | [12F SAVEENABLE](12f-saveenable)         | Menus              |
| 130    | [130 PHSENABLE](130-phsenable)           | Menus              |
| 131    | [131 HOLD](131-hold)                     | Party Management   |
| 132    | [132 MOVIECUT](132-moviecut)             |                    |
| 133    | [133 SETPLACE](133-setplace)             |                    |
| 134    | [134 SETDCAMERA](134-setdcamera)         |                    |
| 135    | [135 CHOICEMUSIC](135-choicemusic)       |                    |
| 136    | [136 GETCARD](136-getcard)               |                    |
| 137    | [137 DRAWPOINT](137-drawpoint)           | Menus              |
| 138    | [138 PHSPOWER](138-phspower)             |                    |
| 139    | [139 KEY](139-key)                       |                    |
| 13A    | [13A CARDGAME](13a-cardgame)             | Menus              |
| 13B    | [13B SETBAR](13b-setbar)                 |                    |
| 13C    | [13C DISPBAR](13c-dispbar)               |                    |
| 13D    | [13D KILLBAR](13d-killbar)               |                    |
| 13E    | [13E SCROLLRATIO2](13e-scrollratio2)     |                    |
| 13F    | [13F WHOAMI](13f-whoami)                 |                    |
| 140    | [140 MUSICSTATUS](140-musicstatus)       |                    |
| 141    | [141 MUSICREPLAY](141-musicreplay)       |                    |
| 142    | [142 DOORLINEOFF](142-doorlineoff)       | Entity             |
| 143    | [143 DOORLINEON](143-doorlineon)         | Entity             |
| 144    | [144 MUSICSKIP](144-musicskip)           |                    |
| 145    | [145 DYING](145-dying)                   | Party Management   |
| 146    | [146 SETHP](146-sethp)                   | Party Management   |
| 147    | [147 GETHP](147-gethp)                   | Party Management   |
| 148    | [148 MOVEFLUSH](148-moveflush)           |                    |
| 149    | [149 MUSICVOLSYNC](149-musicvolsync)     |                    |
| 14A    | [14A PUSHANIME](14a-pushanime)           |                    |
| 14B    | [14B POPANIME](14b-popanime)             |                    |
| 14C    | [14C KEYSCAN2](14c-keyscan2)             | Input              |
| 14D    | [14D KEYON2](14d-keyon2)                 | Input              |
| 14E    | [14E PARTICLEON](14e-particleon)         |                    |
| 14F    | [14F PARTICLEOFF](14f-particleoff)       |                    |
| 150    | [150 KEYSIGHNCHANGE](150-keysighnchange) |                    |
| 151    | [151 ADDGIL](151-addgil)                 | Item/Magic/Card/GF |
| 152    | [152 ADDPASTGIL](152-addpastgil)         | Item/Magic/Card/GF |
| 153    | [153 ADDSEEDLEVEL](153-addseedlevel)     | Item/Magic/Card/GF |
| 154    | [154 PARTICLESET](154-particleset)       |                    |
| 155    | [155 SETDRAWPOINT](155-setdrawpoint)     |                    |
| 156    | [156 MENUTIPS](156-menutips)             | Menus              |
| 157    | [157 LASTIN](157-lastin)                 |                    |
| 158    | [158 LASTOUT](158-lastout)               |                    |
| 159    | [159 SEALEDOFF](159-sealedoff)           |                    |
| 15A    | [15A MENUTUTO](15a-menututo)             | Menus              |
| 15B    | [15B OPENEYES](15b-openeyes)             |                    |
| 15C    | [15C CLOSEEYES](15c-closeeyes)           |                    |
| 15D    | [15D BLINKEYES](15d-blinkeyes)           |                    |
| 15E    | [15E SETCARD](15e-setcard)               | Item/Magic/Card/GF |
| 15F    | [15F HOWMANYCARD](15f-howmanycard)       | Item/Magic/Card/GF |
| 160    | [160 WHERECARD](160-wherecard)           | Item/Magic/Card/GF |
| 161    | [161 ADDMAGIC](161-addmagic)             | Item/Magic/Card/GF |
| 162    | [162 SWAP](162-swap)                     |                    |
| 163    | [163 SETPARTY2](163-setparty2)           |                    |
| 164    | [164 SPUSYNC](164-spusync)               | Timer              |
| 165    | [165 BROKEN](165-broken)                 |                    |
| 166    | [166 UNKNOWN1](166-unknown1)             |                    |
| 167    | [167 UNKNOWN2](167-unknown2)             |                    |
| 168    | [168 UNKNOWN3](168-unknown3)             |                    |
| 169    | [169 UNKNOWN4](169-unknown4)             |                    |
| 170    | [170 UNKNOWN5](170-unknown5)             | Item/Magic/Card/GF |
| 171    | [171 UNKNOWN6](171-unknown6)             | Animation          |
| 172    | [172 UNKNOWN7](172-unknown7)             | Animation          |
| 173    | [173 UNKNOWN8](173-unknown8)             | Animation          |
| 174    | [174 UNKNOWN9](174-unknown9)             | Animation          |
| 175    | [175 UNKNOWN10](175-unknown10)           |                    |
| 176    | [176 UNKNOWN11](176-unknown11)           |                    |
| 177    | [177 UNKNOWN12](177-unknown12)           |                    |
| 178    | [178 UNKNOWN13](178-unknown13)           | Music and Sound    |
| 179    | [179 UNKNOWN14](179-unknown14)           | Music and Sound    |
| 180    | [180 UNKNOWN15](180-unknown15)           |                    |
| 181    | [181 UNKNOWN16](181-unknown16)           | Field related      |
| 182    | [182 UNKNOWN17](182-unknown17)           | Field related      |
| 183    | [183 UNKNOWN18](183-unknown18)           | Menus              |