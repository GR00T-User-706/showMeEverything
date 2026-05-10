```
This Doc Is AI Generated
```

**User:** @GR00T-User-706
**Thread URL:** https://github.com/copilot/c/75af76cd-6414-44b0-99b8-f82712f08bdd

## @GR00T-User-706

@pasted.txt

## Copilot

---

# **Show Me Everything – Technical Documentation**

## 1. Overview

### Purpose
Show Me Everything (`smecli` / `showMeEverything`) is a comprehensive Linux system introspection and search tool designed to emit multi-layer search results across system state domains. It functions as a system-wide probe that unifies searches across the filesystem, shell runtime, package databases, kernel interfaces, and process state into a single coherent interface.

### Core Functionality
- **Unified search interface**: Single command searches multiple system domains simultaneously or individually
- **Multi-subsystem probing**: Shell introspection (aliases, functions, builtins, commands), package management (pacman, apt, dnf, zypper, apk), filesystem traversal, systemd units, running processes, kernel modules, manpages
- **Multiple output modalities**: Human-readable formatted output (with headers/footers) or machine-parseable pipe mode
- **Dual-GUI support**: QML/C++ native GUI (primary) with Python Tkinter fallback for older systems
- **Pattern-based filtering**: Regex or glob-based matching with case-insensitive search

### Design Philosophy
Inferred from code and README:
- **Completeness over efficiency**: Prioritizes comprehensive results over performance constraints
- **Raw emission over normalized output**: Streams unfiltered results with structured section headers for pipeline integration
- **Transparency over safety smoothing**: Intentionally produces high-volume output as a feature, not a limitation
- **Deterministic system state dumping**: Reproducible introspection for forensic analysis and environment reconstruction
- **Minimal core dependencies**: Shell + coreutils only for CLI; GUI components are optional add-ons
- **Zero lateral traversal**: By design, never crosses user boundaries (searches only executing user's accessible domains)

---

## 2. Architecture

### High-Level Structure

```
showMeEverything (ecosystem)
│
├─ CLI Core (Shell Script: showMeEverything)
│  └─ 15+ search functions (path, packages, processes, fs, etc.)
│  └─ Package manager abstraction layer (5 backends)
│  └─ Shell capability detection (bash/zsh)
│  └─ Output configuration (pipe mode vs. human-readable)
│
├─ QML/C++ GUI (Qt6 wrapper)
│  ├─ SearchBackend (C++ subprocess bridge)
│  ├─ main.qml (QML interface)
│  └─ Calls CLI core via subprocess
│
├─ Python Tk GUI (Fallback)
│  └─ Direct subprocess call to CLI core
│  └─ Flag validation + argument mapping
│
└─ Installation/Deployment
   ├─ install script (smart detection + conditional builds)
   └─ Desktop entry files (.desktop)
```

### Key Modules and Responsibilities

| Module | Responsibility | Language |
|--------|-----------------|----------|
| `showMeEverything` (main) | CLI entry point, argument parsing, search dispatch | Shell (zsh/bash) |
| `searchbackend.cpp/h` | Qt6 process management, output streaming | C++ |
| `main.qml` | UI layout, input handling, output rendering | QML |
| `main.cpp` | Qt application initialization, QML engine setup | C++ |
| `showmeeverything_tk.py` | Fallback GUI, Python subprocess wrapper | Python 3 |
| `install` script | Dependency detection, conditional builds, symlink setup | Bash |

### Data Flow (High-Level)

```
User Input
    ↓
┌─ CLI (showMeEverything)
│  ├─ Parse arguments (flags + search pattern)
│  ├─ Validate flag combinations (mutually exclusive checks)
│  ├─ Dispatch to appropriate search function(s)
│  └─ Configure output format (PIPE_MODE on/off)
│
├─ Search Functions (parallel or sequential)
│  ├─ PATH search (find command)
│  ├─ Shell introspection (compgen, eval builtins)
│  ├─ Package manager queries (abstraction layer)
│  ├─ Filesystem traversal (find + grep)
│  ├─ Process/module listing (ps, lsmod)
│  └─ System state probes (systemctl, apropos)
│
├─ Output Formatting
│  ├─ PIPE_MODE=1: No headers/footers, --color=never grep
│  └─ PIPE_MODE=0: Full headers/footers, --color=always grep
│
└─ Output (stdout/stderr)
    ↓
┌─ GUI (optional wrapper)
│  ├─ QML subprocess → C++ SearchBackend
│  └─ Python Tk subprocess → direct shell exec
│
└─ User (terminal, file redirect, pipe)
```

---

## 3. Components

### 3.1 Core CLI: `showMeEverything`

**Responsibility**: Primary executable; command-line interface to all search subsystems.

**Key Functions**:
- `config_output()` – Switches between PIPE_MODE (machine-readable) and human-readable output
- `header0()` – Emits formatted section headers (suppressed in PIPE_MODE)
- `footer()` – Emits footer with timestamp, shell, user, host (suppressed in PIPE_MODE)
- `search_path()` – Searches $PATH for pattern
- `search_loaded_commands()` – Shell builtins: `compgen -c` (bash), `${(k)commands}` (zsh)
- `search_builtins()` – Shell builtins: `compgen -b` (bash), `${(k)builtins}` (zsh)
- `search_shell_functions()` – Loaded functions: `compgen -A function` (bash), `${(k)functions}` (zsh)
- `search_aliases()` – Shell aliases via `alias` builtin
- Package manager wrappers:
  - `pacman_*()` – Arch Linux (pacman -Sl, pacman -Q, pacman -F)
  - `apt_*()` – Debian/Ubuntu (apt-cache, dpkg-query, dpkg -S)
  - `dnf_*()` – Red Hat/Fedora (dnf list, repoquery)
  - `zypper_*()` – SUSE (zypper search, rpm queries)
  - `apk_*()` – Alpine (apk search, apk info)
- `get_package_manager()` – Auto-detects PM via command presence
- `search_manpages()` – Manpage DB search via `apropos -w`
- `search_systemd_units()` – Unit files via `systemctl list-unit-files`
- `search_running_processes()` – Process list via `ps aux`
- `loaded_kernel_modules()` – Kernel modules via `lsmod`
- `search_home_directory()` – Find in $HOME (respects --excludeDotFiles flag)
- `search_system_dirs()` – Traverses /usr, /etc, /sys, /var, /opt, /boot, /lib, /bin, /sbin
- Refined system searches: `search_usr()`, `search_etc()`, `search_var()`, `search_opt()`, `search_boot()`, `search_lib()`, `search_bin()`, `search_sbin()`
- `search()` – Main dispatcher; parses flags, validates combinations, executes selected functions

**Key Variables**:
- `PIPE_MODE` – 0 (human-readable) or 1 (machine-parseable)
- `HEADER` / `FOOTER` – Output format flags
- `REGEX` – 1 (regex matching), 0 (glob matching)
- `current_shell` – Detected shell (zsh or bash)
- `EXCLUDES` – Common find exclusions (e.g., .cache)
- `GREP_OPTS` – Conditional array: color and case-insensitive opts

**Flag System**:
- **Global modes**: `--ALL` (full system), `--all` (userspace only)
- **Shell introspection**: `--aliases`, `--builtins`, `--command`, `--functions`, `--path`
- **Package management**: `--packages`, `--installed`, `--files`, `--not-installed`
- **System state**: `--systemd`, `--process`, `--modules`, `--manpages`
- **Filesystem**: `--system`, `--home`, `--usr`, `--etc`, `--var`, `--opt`, `--boot`, `--lib`, `--bin`, `--sbin`
- **Output control**: `--pipe`, `--less`, `--excludeDotFiles`, `--nodot`, `--glob`

**Exit Behavior**:
- Returns 1 if conflicting flags detected (ALL + all, ALL + system, all + system)
- Returns 1 if no search flags provided
- Returns 1 if --ALL/--all used with incompatible flags
- Normal completion signals via footer timestamp

**Dependencies**:
- `find`, `grep`, `sed`, `awk`, `sort`, `uniq`, `comm`, `compgen`, `alias`, `ps`, `lsmod`, `systemctl`, `apropos`
- Package manager CLIs (pacman, apt-cache, dpkg-query, dnf, repoquery, zypper, rpm, apk)
- Bash/Zsh builtins

---

### 3.2 Qt6 GUI: C++ Backend (`searchbackend.h`, `searchbackend.cpp`)

**Responsibility**: Subprocess management bridge between QML UI and CLI core.

**Key Classes**:

**`SearchBackend` (QObject)**

**Public Slots**:
- `void runSearch(const QString& args)` – Spawns subprocess with given args; connects stdout/stderr
- `void runHelp()` – Convenience: calls `runSearch("--help")`
- `void stopSearch()` – Sends SIGTERM, escalates to SIGKILL after 2s timeout
- `void clearOutput()` – Purges m_output buffer, emits signals
- `void saveToFile(const QString& filename)` – Writes m_output to filesystem
- `QString getFullOutput() const` – Returns accumulated output
- `void copyToClipboard()` – Copies m_output to X11/Wayland clipboard

**Signals**:
- `outputChanged()` – Emitted when m_output changes
- `runningChanged()` – Emitted when process state toggles
- `outputLine(const QString& line)` – Emitted per line of stdout
- `outputCleared()` – Emitted when output is cleared

**Q_PROPERTY**:
- `QString output` – READ-only, bound to m_output
- `bool running` – READ-only, bound to m_running

**Private Slots**:
- `void onReadyReadStandardOutput()` – Accumulates stdout, emits per-line signals
- `void onProcessFinished(int exitCode, QProcess::ExitStatus)` – Handles process exit

**Member Variables**:
- `QProcess* m_process` – Subprocess handle
- `QString m_output` – Accumulated output buffer
- `bool m_running` – Process state flag
- `QStringList m_allowedArgs` – Whitelist of valid CLI arguments (sandboxing)

**Validation Logic**:
- First arg of parsed input must exist in `m_allowedArgs`; rejects unknown flags preemptively

**Subprocess Setup**:
- Program: `/usr/local/bin/showMeEverything`
- Args: Split input on spaces (preserving empty parts)
- Environment: Inherits parent environment
- stdout/stderr: Connected to readyReadStandardOutput signal

**Environment Variables Set**:
- None explicitly set by backend (CLI respects shell defaults)

---

### 3.3 Qt6 GUI: QML UI (`main.qml`)

**Responsibility**: User interface layout, input handling, output display.

**Key Components**:

| Element | Type | Purpose |
|---------|------|---------|
| `mainWindow` | ApplicationWindow | Top-level container (1000×700) |
| `backgroundColor`, `foregroundColor`, etc. | property color | Theme colors (dark theme) |
| `flagMap` | property var (object) | User-friendly → CLI flag mapping |
| `argumentInput` | TextField | User input field for search args |
| `performSearch()` | function | Entry point: validates input, calls searchBackend.runSearch() |
| `clearSearch()` | function | Clears output and input field |
| `convertToFlag()` | function | Maps friendly names to CLI flags (e.g., "all" → "--all") |
| `outputModel` | ListModel | Data model for output lines |
| `outputListView` | ListView | Scrollable output display |
| `Connections` | QML element | Connects searchBackend signals to model updates |
| Quick buttons | Button | "Search", "Help", "Clear", "Save to File", "Copy to Clipboard", "Stop" |
| Quick flags | Repeater + Flow | Buttons for common flags ["all", "path", "installed", "system", "home"] |
| `fileDialog` | FileDialog | Save output to file (uses StandardPaths.HomeLocation) |

**Signal Connections**:
- `searchBackend.onOutputLine(line)` → `outputModel.append()`; auto-scroll to end
- `searchBackend.onOutputCleared()` → `outputModel.clear()`

**User Input Flow**:
1. User types into `argumentInput`
2. Hits Enter (onAccepted) or clicks "Search" button
3. `performSearch()` called:
   - Validates input (shows examples if empty)
   - Converts friendly flag name via `convertToFlag()`
   - Calls `searchBackend.runSearch(convertedInput)`
4. Output lines arrive via `onOutputLine` signal, appended to model
5. ListView auto-scrolls to end

**Output Display**:
- Monospace font, 10pt, wrapping enabled, dark theme colors
- ScrollBar appears on demand (AsNeeded policy)
- Status bar shows "Searching..." or "Ready", line count

---

### 3.4 Qt6 GUI: Application Entry (`main.cpp`)

**Responsibility**: Qt application initialization and QML engine setup.

**Logic**:
```cpp
1. Create QApplication
2. Set org/app name/display name
3. Create SearchBackend instance
4. Create QQmlApplicationEngine
5. Inject searchBackend into QML context as "searchBackend"
6. Load QML from resource: "qrc:/src/qml/main.qml"
7. Start event loop (app.exec())
```

**Org/App Names**:
- Organization: "GR00T-User-706"
- Application: "ShowMeEverything"
- Display Name: "Show Me Everything Search Tool"

---

### 3.5 Python Tk GUI (`showmeeverything_tk.py`)

**Responsibility**: Fallback GUI for systems without Qt6 or on older hardware.

**Key Components**:

| Element | Purpose |
|---------|---------|
| `SEARCH_SCRIPT` | Path to CLI (`shutil.which("showMeEverything")` or fallback `/usr/local/bin/showMeEverything`) |
| `FLAG_GROUPS` | Dict mapping friendly names to CLI flags (similar to QML flagMap) |
| `ALLOWED_ARGS` | Flattened list of all valid CLI args (derived from FLAG_GROUPS) |
| `ARG_MAP` | Dict: lowercase flag → canonical form mapping |
| `append_text(line)` | Appends line to ScrolledText widget; enables/disables state |
| `run_search_thread(arg)` | Worker thread function: spawns subprocess, streams stdout/stderr |
| `run_search(event=None)` | Main search handler; validates input, starts thread |
| `run_help()` | Calls run_search_thread("--help") in background |

**Process Spawning**:
```python
cmd = [SEARCH_SCRIPT, flag] + [search_term]  # if search_term present
env = os.environ.copy()
env["SMECLI_GUI_MODE"] = "1"  # Signal GUI mode to CLI
process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE, text=True, env=env)
```

**Threading Model**:
- Main thread: Tk event loop (input, button clicks)
- Worker thread (daemon): Subprocess execution, output streaming

**Validation**:
- First arg lowercased, checked against `ARG_MAP`
- Rejects unknown args with error message
- Splits input on first space only (flag + optional search term)

**Output Handling**:
- stdout lines appended to ScrolledText in real-time
- stderr lines prefixed with " --- ERRORS ---\n"
- Exceptions caught and displayed in output

---

### 3.6 Installation Script (`install`)

**Responsibility**: Intelligent installation, dependency detection, conditional builds, cleanup.

**Key Functions**:

| Function | Purpose |
|----------|---------|
| `detect_shell()` | Determines SCRIPT_DIR based on Bash/Zsh |
| `define_paths()` | Sets all installation paths |
| `check_root()` | Enforces sudo requirement |
| `show_header()` | Displays header message |
| `determine_install_mode()` | Detects if GUI source present; offers CLI-only fallback |
| `check_existing_installation()` – Looks for prior binary, verifies signature, compares hash, prompts user |
| `clean_previous_install()` | Removes old binaries, symlinks, desktop files, icon |
| `install_cli()` | Copies showMeEverything to /usr/local/bin, creates symlinks |
| `check_python_gui()` | Tests python3 + tkinter availability |
| `install_python_gui()` | Installs Python GUI binary, creates symlinks |
| `check_qt_gui()` | Tests qmake6 and make availability |
| `build_qt_gui()` | Runs qmake6 + make; sets QT_BUILD_OK flag on success |
| `install_qt_gui()` | Copies built binary to /usr/local/bin, creates symlinks |
| `install_desktop_entries()` | Copies .desktop files, icon; runs update-desktop-database |
| `set_ownership()` | Chown reinstalls back to $SUDO_USER |
| `show_summary()` | Displays final status report |

**Install Modes**:

**CLI-Only Mode** (triggered if `showmeeverything_gui/` missing):
- Installs CLI only
- Asks user confirmation
- Suggests re-running from full repo

**Full Mode** (GUI directory present):
- Installs CLI (always)
- Attempts Python GUI (if python3 + tkinter detected)
- Attempts Qt GUI (if qmake6 + make available, builds, installs if successful)
- Installs desktop entries (if at least one GUI or icon present)

**Ownership**:
- All operations run as root (via sudo)
- Final `set_ownership()` returns repo to $SUDO_USER for future edits

**Path Layout**:
- CLI binary: `/usr/local/bin/showMeEverything`
- CLI symlinks: `/usr/local/bin/smecli`
- Qt binary: `/usr/local/bin/showmeeverything_qml`
- Qt symlink: `/usr/local/bin/smegui`
- Python binary: `/usr/local/bin/showmeeverything_tk`
- Python symlink: `/usr/local/bin/smegpy`
- Icon: `/usr/local/share/icons/showMeEverything.png`
- Desktop entries: `/usr/local/share/applications/com.github.gr00t-user-706.showmeeverything-*.desktop`

---

### 3.7 Uninstall Script (`uninstall.sh`)

**Responsibility**: Clean removal of all installed components.

**Actions**:
- Removes all binaries, symlinks, desktop files, icon
- Runs `update-desktop-database` to refresh

---

### 3.8 Qt Project File (`showmeeverything_gui.pro`)

**Responsibility**: QMake build configuration.

**QT Modules**: quick, widgets, core
**Target**: showmeeverything_qml
**Sources**: main.cpp, searchbackend.cpp
**Headers**: searchbackend.h
**Resources**: resources.qrc
**Install Path**: /usr/local/bin

---

### 3.9 Qt Resources (`resources.qrc`)

**Not provided in code listing.** Must contain reference to `src/qml/main.qml` as `qrc:/src/qml/main.qml` (as loaded in main.cpp).

---

## 4. API / Interfaces

### CLI Public Interface (main executable: `showMeEverything`)

```bash
showMeEverything [MODE] [OPTIONS] <PATTERN>
```

**Argument Syntax**:
- First argument: Search mode flag (required)
- Subsequent arguments: Search pattern (optional; some modes require pattern)
- Flags: Can be long (`--all`), short (`-a`), or friendly (`all`, `a`)

**Return Values**:
- Exit 0: Success (normal completion or help shown)
- Exit 1: Error (missing flags, conflicting flags, help display, no flags)

**Environment Variables**:
- `SMECLI_GUI_MODE`: If set to "1", enables PIPE_MODE automatically
- `SHELL`: Detected for shell capability probing (bash vs. zsh)
- `PATH`: Used for --path search
- `HOME`: Used for --home search

### C++ SearchBackend Public Interface

```cpp
public slots:
  void runSearch(const QString& args);        // args: "FLAG [PATTERN]"
  void runHelp();
  void stopSearch();
  void clearOutput();
  void saveToFile(const QString& filename);   // filename: file:// URL or local path
  QString getFullOutput() const;
  void copyToClipboard();

signals:
  void outputChanged();                        // m_output buffer modified
  void outputLine(const QString& line);        // new line received from subprocess
  void runningChanged();                       // process state toggled
  void outputCleared();                        // output buffer cleared

properties (Q_PROPERTY, read-only):
  QString output;                              // current m_output buffer
  bool running;                                // process state
```

### QML Public Slots/Functions

```qml
function performSearch()
function clearSearch()
function convertToFlag(userInput)
```

### Python Tk Public Functions

```python
def append_text(line)
def run_search(event=None)
def run_help()
def run_search_thread(arg)
```

---

## 5. Data Structures

### CLI Global Variables

```bash
PIPE_MODE (int: 0 or 1)
HEADER (int: 0 or 1)
FOOTER (int: 0 or 1)
REGEX (int: 0 or 1)
VERSION (string: "v1.0.1")
current_shell (string: "bash" or "zsh")
EXCLUDES (array: exclusion patterns for find)
GREP_OPTS (array: conditional grep options)
```

### C++ SearchBackend Member State

```cpp
QProcess* m_process;           // Active subprocess or nullptr
QString m_output;              // Accumulated output buffer (no size limit)
bool m_running;                // Process state
QStringList m_allowedArgs;     // Whitelist of ~55 valid CLI arguments
```

### QML Data Model

```qml
ListModel id: outputModel
  [
    { modelData: "line 1 from stdout" },
    { modelData: "line 2 from stdout" },
    ...
  ]
```

### Python Tk Global State

```python
SEARCH_SCRIPT (str): Path to showMeEverything binary
FLAG_GROUPS (dict): {friendly_name: [list of aliases]}
ALLOWED_ARGS (list): Flattened list of all valid args
ARG_MAP (dict): {lowercase_alias: canonical_form}
root, entry, output_text, run_button, help_button (Tk widgets)
```

---

## 6. Execution Flow

### CLI Startup Sequence

```
1. Shell sources/executes showMeEverything script
2. Detects current shell (bash/zsh) via environment variables
3. Defines EXCLUDES, initializes PIPE_MODE=0, HEADER=1, FOOTER=1, REGEX=1
4. Defines all search functions (15+ function definitions)
5. Parses command-line arguments in search() function:
   a. Loop through args, classify each as flag or pattern
   b. Accumulate flag handlers into actions[] array
   c. Check for mutually exclusive flag combinations
   d. Validate --ALL/--all constraints
6. Call config_output() to set GREP_OPTS based on PIPE_MODE
7. Execute each function in actions[] with pattern as arg
8. For each function output: emit header, execute search, emit footer
9. Exit with status 0 or 1
```

### Qt GUI Startup Sequence

```
1. main.cpp: QApplication constructor
2. Set org/app name/display name
3. Construct SearchBackend instance
4. Construct QQmlApplicationEngine
5. Inject searchBackend into QML context
6. Load main.qml from resource
7. Event loop: app.exec()
   └─ Waits for user input, processes signals
```

### Qt GUI Search Execution

```
User Input (argumentInput.text)
  ↓
performSearch() called
  ├─ Trim + validate input (show examples if empty)
  ├─ Call convertToFlag() on input
  ├─ Call searchBackend.runSearch(convertedInput)
  │
  └─ SearchBackend.runSearch():
     ├─ Validate first arg against m_allowedArgs
     ├─ Terminate any existing process
     ├─ Spawn new QProcess:
     │   └─ /usr/local/bin/showMeEverything [args...]
     ├─ Connect stdout readyRead → onReadyReadStandardOutput()
     ├─ Connect process finished → onProcessFinished()
     ├─ Set m_running = true, emit runningChanged()
     ├─ Process.start()
     │
     └─ While running:
        ├─ onReadyReadStandardOutput() called for each chunk
        ├─ Split chunk by newlines
        ├─ Emit outputLine() per line → QML ListView appends
        └─ Accumulate in m_output
        
        On process finish:
        ├─ onProcessFinished() called
        ├─ Set m_running = false, emit runningChanged()
        └─ Optionally append crash/exit code message
```

### Python Tk GUI Search Execution

```
User Input (entry.get())
  ↓
run_search(event=None) called (main thread)
  ├─ Validate input
  ├─ Clear output_text widget
  ├─ Spawn daemon thread: run_search_thread(arg)
  │
  └─ run_search_thread (worker thread):
     ├─ Parse arg: flag + optional pattern
     ├─ Map flag via ARG_MAP
     ├─ Build cmd: [SEARCH_SCRIPT, flag, pattern]
     ├─ Set env["SMECLI_GUI_MODE"] = "1"
     ├─ subprocess.Popen(cmd, ...)
     │
     └─ Stream output:
        ├─ Read stdout line-by-line
        ├─ Call append_text(line) (thread-safe via Tk queue)
        ├─ Read stderr line-by-line
        ├─ Append with "--- ERRORS ---" prefix
        └─ On exception: append error message
        
Main thread (Tk event loop):
  ├─ append_text() enables widget, inserts, scrolls, disables
  └─ Processes remaining Tk events
```

### Package Manager Detection & Search

```
get_package_manager() detects available PM:
  ├─ Check command presence: pacman, apt-cache/dpkg-query, dnf, zypper, apk
  └─ Return first match (priority order as above)

search_package_repo() dispatches:
  └─ case $(get_package_manager) in
     ├─ pacman) pacman -Sl | grep ...
     ├─ apt) apt list | grep ...
     ├─ dnf) dnf list available | grep ...
     ├─ zypper) zypper search | grep ...
     └─ apk) apk search | grep ...
```

---

## 7. Configuration

### Environment Variables (CLI)

| Variable | Purpose | Default |
|----------|---------|---------|
| `SMECLI_GUI_MODE` | If "1", auto-enables PIPE_MODE | unset |
| `SHELL` | Detected for shell-specific builtins | system default |
| `PATH` | Searched by --path, searched for executable | system default |
| `HOME` | Searched by --home | system default |
| `ZSH_VERSION` | Detected to enable zsh probes | unset if bash |
| `BASH_VERSION` | Detected to enable bash probes | unset if zsh |

### CLI Runtime Flags (Parsed)

```
Global output control:
  --pipe, pipe                    PIPE_MODE = 1
  --less                          Pipe all output to less -R
  --excludeDotFiles, --nodot      exclude_dotfiles = true (legacy)
  --glob, glob                    REGEX = 0 (use glob instead)

Global search modes (mutually exclusive):
  --ALL, -A, ALL, A               Full system (everything)
  --all, all                      Userspace only (no system dirs)
  --system, -R, system, R         System dirs only

Subsystem flags (can stack):
  --aliases, -a, aliases, a
  --builtins, -b, builtins, b
  --command, -c, command, c
  --functions, -f, functions, f
  --path, -P, path, P
  --packages, -p, --pkg, packages, pkg, p
  --installed, -i, installed, i
  --files, -F, files, F
  --not-installed, -n, not-installed, n
  --manpages, --man, -M, manpages, man, M
  --systemd, -s, systemd, s
  --process, -x, process, x
  --modules, -m, modules, m
  --home, -H, home, H
  --usr, -U, usr, U
  --etc, -E, etc, E
  --var, -V, var, V
  --opt, -O, opt, O
  --boot, -B, boot, B
  --lib, -L, lib, L
  --bin, bin
  --sbin, sbin

Help:
  --help, -h, help, h
```

### Qt Configuration (Hardcoded)

```qml
backgroundColor: "#1b1e21"      // Dark background
foregroundColor: "#eff0f1"      // Light text
accentColor: "#3daee9"          // Highlight/border color
buttonColor: "#31363b"          // Button background
inputColor: "#7a7a7a"           // TextField background
mainWindow size: 1000×700
```

### Installation Paths (Configured)

```
/usr/local/bin/showMeEverything          (CLI binary)
/usr/local/bin/smecli                    (CLI symlink)
/usr/local/bin/showmeeverything_qml      (Qt binary)
/usr/local/bin/smegui                    (Qt symlink)
/usr/local/bin/showmeeverything_tk       (Python binary)
/usr/local/bin/smegpy                    (Python symlink)
/usr/local/share/icons/showMeEverything.png
/usr/local/share/applications/com.github.gr00t-user-706.showmeeverything-gui-qml.desktop
/usr/local/share/applications/com.github.gr00t-user-706.showmeeverything-gui-python.desktop
```

---

## 8. Error Handling

### CLI Error Handling

| Error Condition | Behavior | Exit Code |
|-----------------|----------|-----------|
| No flags provided | Print usage hint + help | 1 |
| Conflicting flags (ALL + all, ALL + system, all + system) | Print warning message + return | 1 |
| --ALL/--all used with incompatible flags | Print error + return | 1 |
| Unknown command in find/grep | Suppressed by `2>/dev/null` | (suppressed) |
| Permission denied (e.g., system dirs) | Suppressed by `2>/dev/null` | (suppressed) |
| Package manager not installed | Function returns no output | (none) |
| Shell feature unavailable (bash vs zsh) | Attempts bash fallback; may return empty | (none) |

### C++ Backend Error Handling

| Error Condition | Behavior |
|-----------------|----------|
| Invalid first arg (not in m_allowedArgs) | Append error, return early (no subprocess spawn) |
| QProcess spawn fails | Exception caught in Qt framework |
| Process crashes | Catch on finished signal, append crash message |
| File save fails | Append file error + QFile::errorString() |
| Invalid URL in saveToFile | Append "Invalid file path" |

### Python Tk GUI Error Handling

| Error Condition | Behavior |
|-----------------|----------|
| Unknown first arg (not in ARG_MAP) | Append "Argument 'X' not allowed\n" |
| Subprocess exception (e.g., file not found) | Append "Exception: {e}\n" |
| Subprocess crashes | Captured in try/except, displayed in output |

### Patterns Used

1. **Suppression via stderr redirect**: `command 2>/dev/null` – failures silently ignored
2. **Validation before execution**: CLI validates flags before dispatching; C++ validates before spawn
3. **Output accumulation**: No hard limit on m_output buffer size (potential DoS vector)
4. **Signal chaining**: Qt signals propagate errors to UI via outputLine/outputChanged

### Known Failure Points

1. **Shell detection**: If neither BASH_VERSION nor ZSH_VERSION set, falls back to `basename $SHELL` (may be unreliable)
2. **Package manager detection**: Only detects presence, not availability in current PATH
3. **Output buffer growth**: No memory limit on m_output QString; large searches may exhaust memory
4. **Subprocess timeout**: No timeout on long-running searches; user must click Stop
5. **Thread safety in Tk**: append_text() assumes Tk is thread-safe; may deadlock on certain platforms
6. **Desktop entry validation**: Python Tk install doesn't validate desktop files before installing
7. **Mutually exclusive flag parsing**: Logic checks at end of argument loop; early termination not possible

---

## 9. Security Considerations

### Input Validation

| Input | Validation | Sanitization |
|-------|-----------|--------------|
| CLI search pattern | None (passed to grep/find as-is) | None |
| CLI flags | Whitelist check (C++, Python); no shell check | None |
| Qt/Python input field | Frontend validation only (C++/Python lists) | None |
| File save path | URL parsing (Qt); local path extraction | None |

### External Interactions

| Interaction | Security Posture | Notes |
|-------------|------------------|-------|
| Subprocess spawning | No shell invocation; direct exec | Immune to shell injection if args properly split |
| Package manager queries | Direct CLI calls, no shell | Depends on PM for output validation |
| Filesystem traversal | Recursive find with EXCLUDES | Can traverse symlinks (no -L flag) |
| Process enumeration | Via ps aux (world-readable) | No permission bypass |
| Manpage search | Via apropos (world-readable) | Depends on system mandb index |

### User Isolation

By design, **never traverses other users' home directories**. Search scope is limited to:
- Executing user's $PATH
- Executing user's shell state (aliases, functions)
- Executing user's $HOME
- Global system state (packages, processes, modules, manpages)

### Potential Vulnerabilities

1. **Regex DoS via search pattern**: User can supply complex regex to grep; no timeout
   - **Impact**: CLI hang, GUI frozen (if not in separate thread)
   - **Mitigation**: Python/Qt run searches in worker threads; user can click Stop

2. **Output buffer unbounded growth**: m_output QString has no size limit
   - **Impact**: Full-system --ALL search could exhaust RAM
   - **Mitigation**: User can redirect to file (`smecli ... > file`); Qt users can save to file

3. **Symlink traversal**: find does not use -L; follows symlinks in /usr, /etc, etc.
   - **Impact**: Can traverse to other mount points or restricted areas (if readable)
   - **Mitigation**: Depends on filesystem permissions; no elevation used

4. **Shell injection in flag aliases**: QML/Python accept friendly names, mapped to CLI flags
   - **Status**: No injection; mapping is static whitelist
   - **Impact**: None observed

5. **Desktop file privilege escalation**: .desktop files do NOT set SUID or RunAs
   - **Status**: Safe; files set Terminal=false, no privilege elevation
   - **Impact**: None

6. **Package manager command confusion**: CLI uses `pacman -Sl`, `apt list`, etc.
   - **Status**: Standard commands, no arbitrary args
   - **Impact**: Depends on package manager security

### Assumptions & Trust Model

- User running the tool is assumed to be the owner of processes/files they want to search
- No SUID bit used; executes with user's credentials
- System utilities (find, grep, ps) are assumed to be uncompromised
- Desktop environment assumed to be under user control (for Qt/Tk GUI)

---

## 10. Limitations

### Explicit Design Limitations

1. **Single-threaded package manager detection**: `get_package_manager()` returns first match, not all available PMs
2. **No output pagination**: CLI always streams to stdout; user must use --less or pipe to pager
3. **No incremental filtering**: Cannot refine results mid-stream; must restart search
4. **No saved searches**: State not persisted between invocations
5. **Regex/Glob toggle**: Global REGEX flag affects all searches; cannot mix in one invocation
6. **No custom search functions**: User cannot extend search domains without editing script

### Missing Features (Determinable Gaps)

1. **No timeout mechanism**: Long-running searches cannot be time-limited; user must manually stop
2. **No output caching**: Identical searches re-execute; no memoization
3. **No plugin system**: Search functions hardcoded; no extensibility
4. **No parallel execution**: Package manager searches run sequentially; no parallelization
5. **No differential search**: Cannot highlight changes between two invocations
6. **No search history**: GUIs do not maintain input history (no readline in Tk; QML history unclear)

### Qt GUI Limitations

1. **No desktop environment detection**: assumes Qt6 full support; no graceful fallback for minimal systems
2. **No dark mode toggle**: Theme hardcoded to dark; no user preference
3. **No settings persistence**: Window size/position not saved
4. **No keyboard shortcuts**: Only standard QML shortcuts; no customization
5. **No output filtering UI**: Must re-run with new search; no post-filter

### Python Tk GUI Limitations

1. **Single-threaded Tk assumption**: append_text() may deadlock on multi-threaded platforms
2. **No output syntax highlighting**: All text rendered as monospace plain text
3. **No drag-and-drop**: Cannot drag output to terminal or other apps
4. **No font size adjustment**: Fixed 10pt monospace

### CLI Limitations

1. **Bash/Zsh only**: No support for sh, ksh, fish, tcsh
2. **No recursive --home search flag**: Must use full --system to recurse /home
3. **No output filtering post-execution**: Grep applied during search, not after
4. **No user filtering**: Cannot restrict output to specific UIDs
5. **No permission-aware search**: Errors suppressed; user unaware of skipped directories

### Platform Limitations

1. **Linux only**: No support for macOS (BSD tools differ), Windows, other Unix
2. **Systemd-specific**: --systemd assumes systemctl; non-systemd systems skip this
3. **APT/Dpkg specific**: Debian/Ubuntu only; no cross-distro fallback for Debian derivatives
4. **Package manager specific**: Each PM has different flag semantics; abstractions may leak

### Infrastructure Gaps

1. **No logging**: No audit trail of what was searched or when
2. **No metrics**: No performance stats (execution time, output size)
3. **No configuration file**: All settings hardcoded; no rc file support
4. **No version check**: No self-update mechanism; relies on package manager

### Not Determinable from Code

1. **Qt resource file completeness**: `resources.qrc` not provided; unclear if all assets referenced
2. **Qt build system**: Whether `.pro` file includes all necessary modules/libraries
3. **Python dependency versions**: Which Python 3.x versions supported; which Tk versions
4. **Desktop file validation**: Whether .desktop files are syntactically correct
5. **Filesystem ACL support**: Whether find respects POSIX ACLs or SELinux labels

---

## 11. Suggested Improvements

### Evidence-Based Improvements (High Confidence)

1. **Add subprocess timeout in C++ backend**
   - **Evidence**: No timeout visible in searchbackend.cpp; long searches freeze UI
   - **Recommendation**: Implement QTimer in SearchBackend to kill process after configurable duration (default 30s)
   - **Implementation**: Add `m_timeoutMs` member; set QTimer::singleShot on process start; on timeout, call m_process->kill()

2. **Add output buffer size limit in C++ backend**
   - **Evidence**: m_output QString unbounded; potential DoS via full-system search
   - **Recommendation**: Implement circular buffer or truncation after N MB (e.g., 100 MB)
   - **Implementation**: Check m_output.size() in onReadyReadStandardOutput(); truncate or emit warning if exceeded

3. **Add -L flag to find commands**
   - **Evidence**: `find` without -L traverses symlinks; can escape intended search scope
   - **Recommendation**: Add `-L` to all find invocations in `search_*()` functions for symlink handling
   - **Implementation**: Modify EXCLUDES array or inline in find command: `find -L /path ...`

4. **Parallelize package manager queries**
   - **Evidence**: `search_package_repo()`, `search_installed_packages()`, etc. run sequentially
   - **Recommendation**: Use `&` (background) in shell to run multiple PMs in parallel; wait for all
   - **Implementation**: Wrap PM calls in subshell, append `&`, final `wait` call

5. **Add history to QML input field**
   - **Evidence**: QML TextField resets on each search; no history available
   - **Recommendation**: Maintain history stack in C++; expose prev/next via keyboard (Up/Down arrows)
   - **Implementation**: Add `QStringList m_history`; connect TextField key events to history navigation

6. **Add search result count display**
   - **Evidence**: QML shows line count but not result count; ambiguous for large outputs
   - **Recommendation**: Display "Results: N" separate from "Lines: N" in status bar
   - **Implementation**: Track non-header/footer lines; emit resultCount signal

7. **Add configuration file support**
   - **Evidence**: Colors, paths, all hardcoded; no customization possible
   - **Recommendation**: Support `~/.config/showmeeverything/config` (INI format)
   - **Implementation**: Load on startup; override defaults; reload on SIGHUP

8. **Fix missing newline in Python Tk FILE_GROUPS**
   - **Evidence**: Line 36 in showmeeverything_tk.py missing comma after "not-installed" entry
   - **Recommendation**: Add missing comma to fix syntax error
   - **Implementation**: Change `"not-installed": [...]` to `"not-installed": [...],` before "process" entry

9. **Add shell=False to all subprocess calls (already correct)**
   - **Evidence**: C++ and Python both avoid shell invocation; safe from shell injection
   - **Recommendation**: Document this as security feature; maintain in future versions

10. **Add graceful fallback if CLI not in $PATH**
    - **Evidence**: Both GUIs hard-code `/usr/local/bin/showMeEverything`; fails silently if not found
    - **Recommendation**: Search $PATH, try common locations, show error if not found
    - **Implementation**: In C++/Python, loop through PATH before failing; emit user-facing error

### Lower-Confidence Improvements (Speculative)

11. **Implement search caching with TTL**
    - **Evidence**: No memoization visible; identical rapid searches re-execute
    - **Concern**: Cache invalidation complex; system state changes unpredictably
    - **Recommendation**: Optional in-memory cache with 5-minute TTL; disable by default

12. **Add output post-filtering UI in QML**
    - **Evidence**: All filtering done at search time; cannot refine results
    - **Concern**: Post-filtering on large outputs still requires grep; minor UX improvement
    - **Recommendation**: Add secondary TextField + filter button to grep existing output

13. **Support other shells (fish, tcsh, ksh)**
    - **Evidence**: Only bash/zsh detected; other shells not supported
    - **Concern**: Different builtin syntax across shells; complex fallback logic
    - **Recommendation**: Detect shell; use generic `hash -r` + `set` instead of compgen/eval

14. **Add search bookmarks in GUIs**
    - **Evidence**: No persistent state; frequent searches re-entered manually
    - **Concern**: Minor UX; not critical to core functionality
    - **Recommendation**: Persistent favorites in ~/.config/showmeeverything/bookmarks.json

---

## 12. Summary Table

| Aspect | Status | Notes |
|--------|--------|-------|
| **Purpose** | Clear | System-wide search introspection tool |
| **Architecture** | Well-structured | Modular CLI + Qt/Python GUIs |
| **Dependencies** | Minimal | Shell + coreutils for CLI; Qt6 or Tk for GUIs optional |
| **Error Handling** | Basic | Errors suppressed; some validation present |
| **Security** | Good | No privilege escalation; input validated (whitelist); no shell injection |
| **Extensibility** | Low | Hardcoded search functions; no plugin system |
| **Documentation** | Adequate | README clear; code lacks detailed comments |
| **Testing** | Not determinable | No test suite visible in provided code |
| **Performance** | Acceptable for human use | No parallelization; output buffering unbounded |
| **Maintainability** | Good | Clean code structure; signature comments in key files |

---

**Document Version**: 1.0 (based on commit 1bab516e445a48b60e23ab93d3c8c46982b28aed)  
**Last Updated**: 2026-05-08  
**Author**: Technical analysis tool (system prompt: senior architect)
