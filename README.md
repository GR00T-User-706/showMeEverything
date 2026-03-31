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
│   ├── search_gui.desktop       # QML/C++ GUI desktop entry
│   ├── showmeeverything.desktop # PY-TK desktop entry fallback
│   └── showMeEverything.png    # icon
├── install.sh                   # Installation script
├── LICENSE
├── README.md
├── showMeEverything             # CLI script
└── showmeeverything_gui
    ├── main.o
    ├── Makefile
    ├── README                  # GUI build instructions
    ├── resources.qrc
    ├── showmeeverything_gui     # compiled QML/C++ GUI executable
    ├── showmeeverything_gui.pro # qmake project file
    ├── showmeeverything_tk.py   # optional Python Tkinter fallback GUI
    └── src
        ├── main.cpp
        ├── qml
        │   └── main.qml
        ├── searchbackend.cpp
        └── searchbackend.h
```

---
## What it does
---
### showMeEverything searches everything:

>- Your $PATH (every file, every directory)
>- Loaded shell commands, aliases, functions, and builtins
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
>- QML/C++ GUI (showmeeverything_gui) – requires CLI in $PATH, callable as `search-gui`
>- Python Tkinter fallback (showmeeverything_tk.py) – optional, requires CLI callable as `search-gui-fallback`
>- Desktop files in `assets/` assume executables are in `/usr/local/bin/` or symlinked
---
## **Important:**  
+  All GUIs assume the CLI is installed and callable by its single-word name (search by default).
---
## Installation
>+ these all assume the package root directory are in your home folder   
>+ if you saved them somewhere else make sure you adjust accordingly 
 ### 1. **Install the CLI**  
  
``` 
sudo cp ~/showMeEverything/showMeEverything /usr/local/bin/search
sudo chmod +x /usr/local/bin/search
``` 

### 2. **Build and install the QML/C++ GUI**  
```
cd ~/showMeEverything/showmeeverything_gui/
qmake
make
sudo cp showmeeverything_gui /usr/local/bin/search-gui
cd ..
```
### 3. **Optional**: Python GUI fallback
```
sudo cp showmeeverything_tk.py /usr/local/bin/search-gui-fallback
chmod +x /usr/local/bin/search-gui-fallback
```

### 4. Install desktop files
```  
sudo cp ~/showMeEverything/assets/*.desktop /usr/local/share/applications/
sudo update-desktop-database
```
***
**Note**: Desktop files assume executables live in /usr/local/bin or symlinked there. Adjust paths if installed elsewhere.
***
## Usage

### CLI:
>```
>search --all systemd        # everything related to systemd
>search --command git        # just commands named git
>search --system "conf"      # system files with "conf" in the name
>search --home "" > home.txt # entire home directory listing
>search --packages bash      # package manager aware package search
>search --help               # shows all options
>```

### GUI:
>```
>Run search-gui (QML/C++ GUI) or search-gui-fallback (Python Tkinter)
>Enter any valid CLI argument in the input box
>Press Search or hit Enter
>Press Help to see available flags
>```
***
## **Both GUIs require the CLI to be in $PATH and callable by the name used during**
***
## Philosophy

>- Zero dependencies beyond shell + coreutils
>- Raw output, full system interrogation
>- --all dumps everything
>- One function per probe, easy to reason about
>- Pull requests and constructive criticism welcome
>- Goal: spread knowledge and system awareness  
