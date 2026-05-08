#  <center> **showMeEverything**

## <center> A full systemwide probe for Linux distros. A little more useful than tree /.

***


*"Once I wanted to type search \<STRING> and have the system show me everything."*
> 
> **This** is that tool.

---
## Repository Layout
```
showMeEverything
├── install
├── LICENSE
├── README.md
├── showMeEverything            # CLI # CORE FILE, dependancy for the guis 
│           # EVERYTHING BELOW IS OPTIONAL 
├── showmeeverything_gui         # QML/C++ + optional Python GUI
│   ├── README                    # GUI build instructions
│   ├── showmeeverything_gui.pro # qmake project file 
│   ├── showmeeverything_tk.py   # optional Python Tkinter GUI fallback
│   │
│   ├── src
│   │   ├── main.cpp
│   │   ├── qml
│   │   │   └── main.qml
│   │   ├── searchbackend.cpp
│   │   └── searchbackend.h
│   │
│   ├── assets  # only needed for the GUI applications 
│   │   ├── com.github.gr00t-user-706.showmeeverything-gui-python.desktop # optional
│   │   ├── com.github.gr00t-user-706.showmeeverything-gui-qml.desktop  #optional
│   │   └── showMeEverything.png
│   └── resources.qrc
```
# <CENTER> For Detailed Documentation go to <br/>[smecli wiki](https://github.com/GR00T-User-706/showMeEverything.wiki.git)

---
## What it does
---
### showMeEverything searches everything:

>- Your $PATH (every file, every directory)
>- Loaded shell commands, aliases, functions, and built-ins
>- manpage descriptions
>- systemd unit files
>- Running processes
>- Loaded kernel modules
>- System directories (/usr, /etc, /sys, /var, ...)
>- Your home directory
>- Package databases on supported Linux distributions
>- Flags can overlap and will stack behavior unless explicitly overridden by mutually exclusive modes.

---
## Current Support

>- Package managers: pacman, APT/dpkg, dnf, zypper, and apk
>- Filesystem searches (--path, --system, --home): Any Linux distribution
>- Shell execution: Zsh first, with Bash compatibility
>- Shell sourcing: Supported in Bash and Zsh, Zsh-native probes first
### GUIs
>- QML/C++ GUI (showmeeverything_gui) – requires CLI in $PATH, callable as 
>- Python Tkinter fallback (showmeeverything_tk.py) – optional, requires CLI callable as 
>- Desktop files in `assets/` assume executables are in `/usr/local/bin/` or symlinked
>- The Install Script should take care of everything
## GUI Support Notes
>- QML GUI requires a modern system with full Qt6 QML runtime support.
>- On older systems (especially pre-2015 hardware), QML may fail due to missing modules or performance constraints.
>- In those cases, use:
```
    smegpy #(Python Tkinter GUI)
```
>- The CLI (smecli) is the primary interface and works on all supported systems. 
---
---
## Installation
>- make the install script executable and then us it like 
```
cd /path/to/showMeEverything # whereever you downloaded it to
sudo bash install
or
sudo ./install 
```
>- that install script will take care of everything 
>- it first detects if there is already a file at the installation path and asks for user aproval if yes 
>- if there are files at the install paths it also checks for a signature to know if the app should proceed
>- it also detects if the cloned repo is missing any parts incase someone only grabbed the cli and installer 
>- if all those go fine the full install will build the qml gui and if that fails continues on to the next stages while  informing of the failure 
>-  then installs the included files in there locations sets permissions and ownership pack to the user installes and registers the desktop entry files 
>- then it will install the desktop entry files in /usr/local/share/applications/ creates dir if needed 
>- the repo is not removed after install in the event you wish to edit the files and all that 
>- each file gets a symlink if installed. smecli, smegpy, smegui
>- you can re-run the install script anytime you grap an update off this repo, or anytime you modify the files 
>- leave the signature at the top of the file its so the install script "
## Usage
>-- i repeat
>-- Flags can overlap and will stack behavior for the time being i recommend not stacking all flags with anything other then --pipe and or --less
>-- the search <STRING> accepts the same formatting as grep to my knowledge like "dat|a|pa|rts"
>-- Im still finding the full usage of this tool 
# <CENTER> **WARNING:** <br/> **UNLESS YOU KNOW EXACTLY WHAT UR DOING <BR/>AND ARE WILLIING TO ACCEPT THE CONSEQUENCES<BR/> NEVER PIPE THIS TOOL INTO CHOWN, CHMOD, OR RM -RF <BR/>THE OUTCOME COULD BE FATAL TO YOUR ENTIRE SYSTEM <BR/>THIS IS YOUR ONLY WARNING** 


### CLI:
>```
>smecli --all systemd        # everything related to systemd
>smecli --command git        # just commands named git
>smecli --system "conf"      # system files with "conf" in the name
>smecli --home "" > home.txt # entire home directory listing
>smecli --packages bash      # package manager aware package search
>smecli --help               # shows all options
>smecli --pipe --home ollama # --pipe = machine parseable formatting on the data stream to stdout
#### You can use this tool with command substitution and get some interesting outcomes
>nano "$(smecli --pipe --home "showmeeverything|ollama")"
>```

### GUI:
>```
>Run smegui (QML/C++ GUI) or smegpy (Python Tkinter)
>Enter any valid CLI argument in the input box
>Press Search or hit Enter
>Press Help to see available flags 
>```
***
### **Both GUIs require the CLI to be in $PATH and callable by the name used during**
>- as long as you use the install script and your system is same this should be true
>-  if not then imma need you to go, do something else, touch grass. smoke grass
>-  but if your $PATH doesn't include /usr/local/bin maybe stop, your gonna break something 
***

## Philosophy

>- Zero dependencies beyond shell + coreutils for the cli
>- The Python GUI needs tkinter and the QML one needs qt6
>- Raw output, full system interrogation 
>- --ALL dumps everything 
>- One function per probe, easy to reason about
>- Pull requests and constructive criticism welcome
>- Goal: spread knowledge and system awareness  
>- this is a very powerful tool, if you are not a system administrator 
>- you should probably just stop before u get yourself in trouble 


## Security/Privacy

>- No matter what unless you modify the code this tool will never traverse any other users home
