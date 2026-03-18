# showMeEverything

## A full systemwide probe for Linux distros. A little more useful than tree /.

Once I wanted to type search <string> and have the system show me everything.
This is that tool.

## What it does
showMeEverything searches everything:

  - Your $PATH (every file, every directory)
  - Loaded Zsh commands, aliases, functions, and builtins
  - manpage descriptions
  - systemd unit files
  - Running processes
  - Loaded kernel modules
  - System directories (/usr, /etc, /sys, /var, ...)
  - Your home directory
  - Package databases (currently Arch Linux)

## Philosophy

  - Zero dependencies – pure Zsh + coreutils
  - Raw output – no filtering, no pretty tables
  - Full system interrogation – online or offline
  - --all "" dumps everything. Yes, really.

## Current Support

  - Package manager: Arch Linux (pacman) – APT detection planned
  - Filesystem searches (--path, --system, --home): Any Linux distribution
  - Shell: Zsh – bash/sh support planned

## Installation

This script is provided as showMeEverything, but you can name it anything you want.
(The author keeps it as search on their own system because... laziness.)

Two ways to use it:

   ### 1. Drop it in your $PATH

      -  Run echo $PATH to see where you can put it
      -  Copy the file to one of those directories (e.g., ~/.local/bin/)
      -  Make sure it's executable: chmod +x ~/.local/bin/showMeEverything

   ### 2. Source it from your shell config

      -  Add this line to ~/.zshrc, ~/.profile, or similar:
      -  ```source /path/to/showMeEverything```
      -  Note: ~/.bashrc is not recommended – this is a Zsh script (for now)

Pick one method. Don't do both.

## Usage: Once installed, use it like this:

```
showMeEverything --all systemd        # everything related to systemd
showMeEverything --command git        # just commands named git
showMeEverything --system "conf"      # system files with "conf" in the name
showMeEverything --home "" > home.txt # entire home directory listing
showMeEverything --help               # shows all options
```
## If you renamed the script (e.g., to search), just use that name instead.

# Final thoughts 
- I always welcome constructive critisism
- if you have any ideas on ways to improve this please make a pull request 
- the ultimate goal is always to spread and share the knowledge for the betterment of all
