# DOSKEY_Manager

DOSKEY_Manager is an app for managing aliases in CMD / Windows Terminal.

# Setup
Just run setup.cmd and it will localize the app's path to your current directory.
You can always re-run it if you want to move to another directory.

# Features
+ Adds an ever changing customizable background when using the Windows Terminal. The installation directory contains a 'backgrounds' folder in which you can add / remove any backgrounds (both images and gifs) as you want (if you want, leave it empty for a blank background).
+ Ability to change the background via the 'bg' command to a random one. It also detects all folders created inside the 'backgrounds' folder so that you may use 'bg -type \<name of folder>' to choose a random background inside that specific folder.
+ Automatic backup to the Windows Terminal settings.json when changing a background.
+ Adds a customizable welcome text when opening the terminal. The installation directory contains a 'welcome_screens' folder with some premade texts. Whatever welcome screen you want applied, add the *.txt file to the 'active' folder located inside the 'welcome_screens' folder (I left a few premades that I like in there). Syntax also supports randomness - use %_random_\<mode>_\<count>_%, where mode represents what is displayed:
- 'd' digits
- 'sc' small characters
- 'bc' big characters'
- 'mc' mixed characters (small + big)
- 'dsc' digits + small characters
- 'dbc' digits + big characters
- 'dmc' digits + big characters + small characters
+ Enables you to easily add any and as many aliases to scripts or commands of whatever nature you want. Some default ones have been provided.

# Known issues
It seems to interfere with postgres's activation of its database server for some reason.
To quickly disable DOSKEY_Manager, just rename the 'DOSKEY_Loader.bat' file to anything else and try running postgres again and it should work (for example, you can add '_' before the name). If for some reason it doesn't, you'll have to manually go to "HKLM\SOFTWARE\Microsoft\Command Processor" in the registry editor and delete the entry called 'AutoRun'. You can always restore it later by running the setup.bat again.


|![](https://i.imgur.com/LryZzs7.png)   |  ![](https://i.imgur.com/S3UXR9S.png)|
|-------------------------------------|------------------------------------|

# Changelog
## v2.3
+ Added support for displaying  a random title

## v2.2
+ Added a config for a custom Windows Store (ergo WinTerminal) path.
* Completely rewrote file loading methods for a more robust and less error prone functionality.

## v2.1
+ Added detection for all folders created inside the 'backgrounds' folder so that the user may use 'bg -type \<name of folder>' to choose a random background inside that specific folder.

## v2.0
+ Added 'version' command
+ Added a bunch of linux-like aliases for existing windows commands
+ Added a background changing script for the Windows Terminal
+ Streamlined installation process

## v1.2
+ Added a couple more linux aliases
+ Added welcome text every time a terminal is opened
+ Added colored help section - 'helpcfg'
  
## v1.1
+ Added notepad++ detection
  
## v1.0
- Initial upload
