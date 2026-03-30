# showMeEverything

## A full systemwide probe for Linux distros. A little more useful than tree /.

Once I wanted to type search <string> and have the system show me everything.
This is that tool.

## What it does
showMeEverything searches everything:

  - Your $PATH (every file, every directory)
  - Loaded shell commands, aliases, functions, and builtins
  - manpage descriptions
  - systemd unit files
  - Running processes
  - Loaded kernel modules
  - System directories (/usr, /etc, /sys, /var, ...)
  - Your home directory
  - Package databases on supported Linux distributions

## Philosophy

  - Zero dependencies – shell + coreutils + whatever your distro already uses to manage packages
  - Raw output – no filtering, no pretty tables
  - Full system interrogation – online or offline
  - --all "" dumps everything. Yes, really.
  - One function per job so every probe stays separated and obvious

## Current Support

  - Package managers: pacman, APT/dpkg, dnf, zypper, and apk
  - Filesystem searches (--path, --system, --home): Any Linux distribution
  - Shell execution: Zsh first, with Bash as the compatibility path
  - Shell sourcing: Supported in both Bash and Zsh with Zsh-native probes kept first

## Installation

This script is provided as showMeEverything, but you can name it anything you want.
(The author keeps it as search on their own system because... laziness.)

Two ways to use it:

   ### 1. Drop it in your $PATH

      -  Run echo $PATH to see where you can put it
      -  Copy the file to one of those directories (e.g., ~/.local/bin/)
      -  Make sure it's executable: chmod +x ~/.local/bin/showMeEverything

   ### 2. Source it from your shell config

      -  Add this line to ~/.bashrc, ~/.zshrc, ~/.profile, or similar:
      -  ```source /path/to/showMeEverything```
      -  Note: executable mode is the most portable option because the script runs under Bash either way

Pick one method. Don't do both.

## Usage: Once installed, use it like this:

```
showMeEverything --all systemd        # everything related to systemd
showMeEverything --command git        # just commands named git
showMeEverything --system "conf"      # system files with "conf" in the name
showMeEverything --home "" > home.txt # entire home directory listing
showMeEverything --packages bash      # package manager aware package search
showMeEverything --help               # shows all options
```
## If you renamed the script (e.g., to search), just use that name instead.

# Final thoughts 
- I always welcome constructive critisism
- if you have any ideas on ways to improve this please make a pull request 
- the ultimate goal is always to spread and share the knowledge for the betterment of all
