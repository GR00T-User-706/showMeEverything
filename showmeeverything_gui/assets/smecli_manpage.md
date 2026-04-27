# SMECLI(1)

## NAME
smecli - system-wide introspection and recursive search emitter

---

## SYNOPSIS
```bash
smecli [MODE] [OPTIONS] <pattern>
```

---

## DESCRIPTION

`smecli` is a Linux system introspection tool designed to emit raw, multi-layer search results across system state domains including filesystem, shell runtime, package databases, kernel interfaces, and service managers.

It is intentionally designed to prioritize completeness and transparency over output cleanliness or performance constraints.

Output is streamed directly to stdout and is intended for:

- terminal inspection
- piping into `less`, `grep`, `awk`
- forensic system analysis
- full-system dump capture

---

## BEHAVIOR MODEL

### 1. Targeted Mode (low entropy)
Triggered by specific or meaningful patterns:

```bash
smecli showMeEverything
smecli .ollama
smecli ssh
```

Behavior:
- constrained traversal scope
- subsystem filtering applied
- bounded output volume

---

### 2. Entropy Mode (high output / blast mode)
Triggered by broad patterns or global scan flags:

```bash
smecli --ALL a
smecli --ALL 1
smecli --system ctl
```

Behavior:
- full subsystem dispatch
- recursive filesystem traversal
- package + process + kernel enumeration
- system-wide emission flood

Example:
```bash
smecli --ALL a > system_dump.txt
```

---

## OUTPUT FORMAT

Each subsystem emits structured sections:

```
#=========================================================#
<SECTION HEADER>
<SEARCH CONTEXT>
#=========================================================#
<RAW OUTPUT>
```

Sections are separated by headers and optional footer timestamps.

This format is intended for:

- grep-based post filtering
- forensic reconstruction
- log ingestion pipelines

---

## OPTIONS

### GLOBAL MODES

- `--ALL`, `-A`
  Full system scan including:
  `/usr`, `/etc`, `/var`, `/opt`, `/boot`, `/lib`, `/bin`, `/sbin`, `/sys`

- `--all`
  Userspace-only scan (excludes kernel/system-level traversal)

---

### FILTER CONTROLS

- `--less`
  Pipe output into pager

- `--excludeDotFiles`, `--nodot`
  Exclude hidden/cache-like directories in HOME-based scans

---

### SHELL INTROSPECTION

- `--aliases | -a`
- `--builtins | -B`
- `--command | -c`
- `--functions | -f`
- `--path | -P`

---

### PACKAGE SYSTEM INTROSPECTION

Auto-detected backend support:

- pacman
- apt
- dnf
- zypper
- apk

Commands:

- `--packages | --pkg | -p`
- `--installed | -i`
- `--files | -F`
- `--not-installed | -n`

---

### SYSTEM STATE INTROSPECTION

- `--systemd | -s`
- `--process | -x`
- `--modules | -m`
- `--manpages | --man`

---

### FILESYSTEM DOMAIN SCANS

Refined traversal flags:

- `--system`
  Full system directory scan aggregation

- `--usr`
- `--etc`
- `--var`
- `--opt`
- `--boot`
- `--lib`
- `--bin`
- `--sbin`

Each limits traversal scope to a specific filesystem root.

---

## WARNING BEHAVIOR

Low entropy patterns (single characters, digits, or broad substrings) may:

- generate extremely large output volumes
- trigger multi-subsystem traversal cascades
- saturate terminal buffers if not redirected

This behavior is intentional.

---

## RECOMMENDED USAGE

### Precise search
```bash
smecli .ollama
```

### Subsystem scan
```bash
smecli --process ssh
```

### Full system dump
```bash
smecli --ALL a > dump.txt
```

### Post-filtering pipeline
```bash
smecli --ALL a | grep ssh | less
```

---

## DESIGN PHILOSOPHY

`smecli` prioritizes:

1. completeness over efficiency
2. raw emission over normalized output
3. transparency over safety smoothing
4. deterministic system state dumping over UX constraints

It is intended for:

- system introspection
- forensic analysis
- environment reconstruction

Not intended for casual or interactive browsing.

---

## NOTES

This tool intentionally behaves like a controlled system-wide search emitter rather than a traditional CLI utility.

Output volume is a feature, not a side effect.

