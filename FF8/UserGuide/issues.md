---
layout: default
title: Known Issues and fixes
parent: User Guide
permalink: /user-guide/issues/
---


This is a collection of known issues, and fixes to those issues.

1. TOC
{:toc}

# __Known issues, crashes, bugs or Problems and How to fix them__


## __When I press play Final Fantasy 8 wont load__
   - **Make sure you have the latest version of both Junction 8 and FFnx.
   - Go to Junction 8 / SETTINGS / GENERAL SETTINGS
   - At the bottom left side is CHANNEL SETTINGS. Here you can check FFnX, Junction8 and Reshader to see if there is any updates.
   - It is very important to have newest version of Junction 8 as updates include VC+ and .NET windows redistributables needed.

## __Was using Echo-S 8 and game ended on disk 1?__
   - **Disable Echo-S 8 mod in Junction 8 and keep on playing the same save file.**

## __Poly-Up and any mod that replaces character models can crash__
   - **Having more than 3 enhcanced character models active at a time can and will cause crashes on scenes where more than 3 main characters on screen at once.
   - Poly up has options to turn on and off characters enchanced models individually. Try to only have 2 characters enchanced at a time.

## __Chrono's WIP Save anywhere causes Crashes__
   - **The option in Chrono's WIP mod to save anywhere is bugged and crashes the game. If your game is crashing make sure this option is off.

## __Background field textures have character textures on them__
   - **Known bug with ANGELWING ULTIMA field texture pack (maybe other field texture packs too) Just exit area and re enter**

## __Game Crashes at DISK 3 when entering Lunatic Pandora after going up elevator and FMV's play__
   - **Known bug with Battlefield Pack mod. Disable Battlefield Pack mod, do the fight, then re-enable the mod**

## __Game Crashes at Tonberry King Fight__
   - **Known bug with Battlefield Pack mod. Disable Battlefield Pack mod, do the fight, then re-enable the mod**

## __When starting Battles, casting magic and GF's game lags a little bit__
   - **Known bug with Hit-J. If the stutter/ lag bothers you, disable this mod**

## __Game Crashes when using EDEN GF__
   - When the game is using DirectX11 or 12, and the game is set to 16:9 or 16:10 aspect ratio it can crash the game during the GF animation
   - This crash happens even when no mods are being used.
   - **There is 2 fixes for this issue. You can change your renderer in Junction 8 / Settings / Game Driver from DX11 or DX12 to VULKAN**
   - **OR you can not use 16:9 or 16:10 and instead use FILL SCREEN, or 4:3**

## __Cannot figure out how to quit the game__
   - **Control+Q WHILE NOT IN A MENU. A lot of people try quiting the game while inside menus, that will not work, you must be on the field, or in a battle.**

## __Music is too loud, how to lower music volume?__
   - **This is not done in game, and must be done from the Junction8 launcher. Open Junction8, go SETTINGS, GAME LAUNCHER.**
   - in here is volume controls to edit volumes of sfx, music, voice, ambient and movie. You can also select sound device you want sound to come out of.

## __How to play Junction8 in non english languages?__
   - **To play junction8 in other languages, you must first install the ENGLISH version of the game, then inside Junction8 change the language.
   - to change the Junction8 language Open junction8 go SETTINGS, LANGUAGE and select which one you want.
   - Then go Browse Catalog tab, and find the mod called FF* ILP (International Language Patch) 
   - Then go to My Mods tab, find FF8 ILP, select it and click CONFIGURE MOD.
   - In here select which language you want to use and click SAVE.

## __When playing 16:9 or 16:10 Move names, and scan information gets cut off__
   - **Widescreen 16:9 and 16:10 is still in alpha stages of development and is not perfect. 
   - This issue is known, and there is no way yet to prevent this from happening other than not using 16:9 or 16:10.
   - another issue caused by widescreen is when the game shows fmv with in game assets on top of them. There will be ghosting effects on the sides of the screen.
   - Such as when Squall and Quistis are walking around balamb dorms at start of game, or when dollet Radio tower opens up

## __Why does Seifer have a hole in head?__
   - **Thats the game itself and nothing to do with Junction8 or ffnx.**

## __When I load a save game, Im put into some DEBUG room__
   - **You must have activated the DEBUG mod. This mod will load you into the DEBUG ROOM when loading save files. Disable DEBUG ROOM mod**

# __Issue is not listed, please help!__

   - **If your issue is not listed in this list, what you need to do is check the log file for the errors**
   - ** or share the log file on tsunamods ff8 mod support page.**

   - To find log file go to FINAL FANTASY VIII game directory. To find the directory you can check in Junction8, go SETTINGS, GENERAL SETTINGS.
   - At the top will be PATHS: FF8 EXE: - This will show you the directory you need.
   - In the FINAL FANTASY VIII directory look for a file called FFNX.LOG
   - inside this log file press CONTROL+F (find) and look for the word ERROR
   - in the log the places where it says ERROR will give info on what file caused the crash. If a texture, or sound, its most likely from a mod.
   - Figure out which mod would have that file, and disable it.
   - Also MAKE SURE FFnX and Junction 8 are up to date. Go SETTINGS, GENERAL SETTINGS and click CHECK FOR UPDATES a at the lower left side
   - Other things to try are disable all mods and see if it crashes. 
   - If game still crashing, try different RENDER options in Junction 8 / SETTINGS / GAME DRIVER
   - All else fails, share the log file in Tsunamods ff8 mod support channel!



 **Guide written by Slimebucket**
