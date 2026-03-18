# showMeEverything
full systemwide probe for linux distros a little more useful then ```tree /``` 


# showMeEverything – system interrogation tool

Once I wanted to type `search <string>` and have the system show me everything.
This is that tool.

## What it does

`showMeEverything` searches **everything**:
- Your PATH (every file, every directory)
- Loaded Zsh commands, aliases, functions, builtins
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
- `--all ""` dumps everything. Yes, really.

## Current Support

- **Package manager**: Arch Linux (`pacman`) – APT detection planned
- **Filesystem searches** (`--path`, `--system`, `--home`): Any Linux distribution
- **Shell**: Zsh – bash/sh support planned

## Usage

- originally i named the script search bc ultimately i am lazy and hate typing excessive amounts
- so copy and save this file under what ever name you wish 
- or keep the reponame and alias it 
- for ease of use in whatever terminal emulator you choose run ```echo $PATH``` and either save this file in one of those locations 
- alternatively find your run command file and add a line sourcing this file both options should work just dont do both  pick one 

```zsh
search --all systemd        # everything related to systemd
search --command git        # just commands named git
search --system "conf"      # system files with "conf" in the name
search --home "" > home.txt # entire home directory listing
search --help               # tells you how to use it

```
