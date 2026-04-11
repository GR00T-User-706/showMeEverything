# showMeEverything

## A full systemwide probe for Linux distros. A little more useful than tree /.

***


*"Once I wanted to type search \<STRING> and have the system show me everything."*
>
> **This** is that tool.
---
## Repository Layout
```

showMeEverything
├── assets
│   ├── com.github.gr00t-user-706.showmeeverything-gui-python.desktop # PY-TK desktop entry fallback
│   ├── com.github.gr00t-user-706.showmeeverything-gui-qml.desktop  # QML/C++ GUI desktop entry
│   └── showMeEverything.png   # icon
├── install                                # Installation script
├── LICENSE
├── README.md
├── showMeEverything     # CLI script this file is the heart of everything without it the rest will faiil
---
├── showMeEverything.cflags    # this
├── showMeEverything.config    # this
├── showMeEverything.creator    # this
├── showMeEverything.cxxflags     # these files are all generated when you compile the
├── showMeEverything.files        #   QML/C++ GUI there  missing from the repo for a reson 
---
├── showmeeverything_gui 
--- 
same with these files they are generated at build time and will not be in the repo 
│   ├── main.o
│   ├── moc_predefs.h
│   ├── moc_searchbackend.cpp
│   ├── moc_searchbackend.o
│   ├── qrc_resources.cpp
│   ├── qrc_resources.o
│   ├── resources.qrc
│   ├── searchbackend.o
---
│   ├── Makefile
│   ├── README                    # GUI build instructions
│   ├── showmeeverything_gui     # compiled QML/C++ GUI executable
│   ├── showmeeverything_gui.pro # qmake project file
│   ├── showmeeverything_tk.py   # optional Python Tkinter fallback GUI
│   └── src
│       ├── main.cpp
│       ├── qml
│       │   └── main.qml
│       ├── searchbackend.cpp
│       └── searchbackend.h
└── showMeEverything.includes
```

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
---
---
## Installation
>- make the install script executable and then us it like 
```
cd /path/to/showMeEverything # whereever you downloaded it to
sudo bash install
```
>- that install script will take care of everything 
>- it first attepts to compile the qml GUI if that fails the script will continue 
>- also if that fails the script will inform you  -thats also why there is a python basic gui
>- then it will install the desktop entry files in /usr/local/share/applications/ creats dir if needed 
>- installs the icon at /usr/local/share/icons
>- and finally installs the cli and the 2 guis to /usr/local/bin/ assuming the QML build was seccessful
>- it also sets all the permissions to 555 leave the cloned repo if u want to edit the files
>- For QoL the cli and the guis get symlinks for shorter names comment them out if you dont want them
>- you can re-run the install script anytime you grap an update off this repo, or anytime you modify the files 
## Usage


### CLI:
>```
>smecli --all systemd        # everything related to systemd
>smecli --command git        # just commands named git
>smecli --system "conf"      # system files with "conf" in the name
>smecli --home "" > home.txt # entire home directory listing
>smecli --packages bash      # package manager aware package search
>smecli --help               # shows all options
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
>- Raw output, full system interrogation
>- --ALL dumps everything
>- One function per probe, easy to reason about
>- Pull requests and constructive criticism welcome
>- Goal: spread knowledge and system awareness  
>- this is a very powerful tool, if you are not a system administrator 
>- you should probably just stop before u get yourself in trouble 