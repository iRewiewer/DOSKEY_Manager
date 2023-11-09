# DOSKEY_Manager

DOSKEY_Manager is an app for managing aliases in CMD / New Windows Terminal.

# Setup
Just run setup.cmd and it will localize the app's path to your current directory.
You can always re-run it if you want to move to another directory.

# Features
+ Adds an ever changing customizable background when using the Windows Terminal. The installation directory contains a 'backgrounds' folder in which you can add / remove any backgrounds (both images and gifs) as you want.
+ Ability to change the background via the 'bg' command to a random one. It also detects all folders created inside the 'backgrounds' folder so that you may use 'bg -type \<name of folder>' to choose a random background inside that specific folder.
+ Automatic backup to the Windows Terminal settings.json when changing a background.
+ Adds a customizable welcome text when opening the terminal. The installation directory contains a 'welcomeScreens' folder with some premade texts. The only text file read is welcome.txt located in the root directory.
+ Enables you to easily add any and as many aliases to scripts or commands of whatever nature you want. Some default ones have been provided.


|![](https://i.imgur.com/LryZzs7.png)   |  ![](https://i.imgur.com/S3UXR9S.png)|
|-------------------------------------|------------------------------------|

# Changelog
## v2.2.38.5
+ Added a config for a custom Windows Store (ergo WinTerminal) path.
* Completely rewrote file loading methods for a more robust and less error prone functionality.
## v2.14
+ Added detection for all folders created inside the 'backgrounds' folder so that the user may use 'bg -type \<name of folder>' to choose a random background inside that specific folder.

## v2.09
+ Added 'version' command
+ Added a bunch of linux-like aliases for existing windows commands
+ Added a background changing script for the Windows Terminal
+ Streamlined installation process

## v1.0.4.3.6
+ Added a couple more linux aliases
+ Added welcome text every time a terminal is opened
+ Added colored help section - 'helpcfg'
  
## v1.0.1.23
+ Added notepad++ detection
  
## v1.0.0.0
- Initial upload
