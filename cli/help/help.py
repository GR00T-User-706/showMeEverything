SHORT_HELP = '''smecli — Show Me Everything CLI
Author:  Zenrich Shadowstep / GR00T-User-706
Version: v3.0.0

USAGE:
  smecli [OPTIONS] [SEARCH_TERM]
  smecli [SEARCH_FLAGS...] [OPTIONS] [SEARCH_TERM]

HELP:
  -h, --help              Show this quick help.
      --full-help        Show detailed help.

OUTPUT OPTIONS:
  --less                 Internal interactive pager.
  --sort                 Sort results alphabetically, case-insensitive.
  --pipe                 Machine-friendly output: disables color, headers, footer.
  --glob                 Literal/fixed-string matching.
  --excludeDotFiles,
  --nodot                Exclude dotfiles from HOME searches.
  -v, --version          Print SME version/signature.

SEARCH FLAGS:
  --ALL, -A              Aggressive full scan.
  --all                  Broad scan without system-directory sweep.\n  --environment, --env, -e\n                         Search environment, shell variables, process\n                         environments, environment configuration, and\n                         application-defined environment variables.
  --aliases, -a          Search aliases.
  --builtins, -b         Search shell builtins.
  --command, -c          Search loaded commands.
  --functions, -f        Search shell functions.
  --path, -P             Search PATH.
  --manpages, --man, -M  Search manpage descriptions.
  --process, -x          Search running processes.
  --systemd, -s          Search systemd units.
  --modules, -m          Search loaded kernel modules.
  --packages, -p, --pkg  Search package repository/database.
  --installed, -i        Search installed packages.
  --not-installed, -n    Search packages not installed.
  --files, -F            Search package file database.
  --home, -H             Search HOME.
  --system, -R           Search major system directories.
  --usr, -U              Search /usr.
  --etc, -E              Search /etc.
  --var, -V              Search /var.
  --opt, -O              Search /opt.
  --boot, -B             Search /boot.
  --lib, -L              Search /lib.
  --bin                  Search /bin.
  --sbin                 Search /sbin.

Use --full-help for detailed descriptions, examples, conflict rules, and
large-output guidance.
'''

FULL_HELP = '''smecli — Show Me Everything CLI
Author:  Zenrich Shadowstep / GR00T-User-706
Contact: crypto_code_weaver_syndicate@proton.me
Version: v3.0.0

USAGE:
  smecli [OPTIONS] [SEARCH_TERM]
  smecli [SEARCH_FLAGS...] [OPTIONS] [SEARCH_TERM]

BASIC EXAMPLES:
  smecli --path python
  smecli --installed firefox
  smecli --home notes
  smecli --all network
  smecli --ALL usb --less
  smecli --systemd ssh
  smecli --packages nmap
  smecli --not-installed python

IMPORTANT:
  At least one search flag is required.
  SEARCH_TERM is optional for most flags.
  Empty searches can produce huge output.
  Use --less or redirect output when running broad scans.

HELP:
  -h, --help
      Show the quick help.

  --full-help
      Show this detailed help.

OUTPUT OPTIONS:
  --less
      Internal interactive pager.

  --sort
      Sort search results alphabetically, case-insensitive.

  --pipe
      Machine-friendly output:
      disables ANSI color, headers, and footer.

  --glob
      Use literal/glob-style matching instead of regex mode.

  --excludeDotFiles, --nodot
      Exclude dotfiles from HOME-based searches.

  -v, --version
      Print SME version/signature.

SEARCH GROUPS:
  --ALL, -A
      Aggressive full scan:
      PATH, commands, builtins, aliases, functions, manpages,
      systemd units, running processes, kernel modules,
      package repository, installed packages, package file DB,
      not-installed packages, HOME, and system directories.

      WARNING:
      Very large output, especially without SEARCH_TERM.

  --all
      Broad user/system scan without the full system directory sweep:
      PATH, commands, builtins, aliases, functions, manpages,
      running processes, package searches, and HOME.

      Safer than --ALL, but still potentially large.

SHELL SEARCH FLAGS:
  --aliases, -a
      Search loaded shell aliases.

  --builtins, -b
      Search shell builtins.

  --command, -c
      Search loaded shell command list.

  --functions, -f
      Search loaded shell functions.

  --path, -P
      Search executable files in $PATH.

DOCUMENTATION / PROCESS FLAGS:
  --manpages, --man, -M
      Search manpage descriptions with apropos.

  --process, -x
      Search running processes.

  --systemd, -s
      Search systemd unit files.

  --modules, -m
      Search loaded kernel modules.

PACKAGE SEARCH FLAGS:
  --packages, -p, --pkg
      Search detected package manager repository/database.

  --installed, -i
      Search installed packages.

  --not-installed, -n
      Search packages available in repositories but not installed.

  --files, -F
      Search package-managed file database / file ownership.

FILESYSTEM SEARCH FLAGS:
  --home, -H
      Search $HOME.

  --system, -R
      Search major system directories:
      /usr, /etc, /sys, /dev, /var, /opt, /boot, /lib, /bin, /sbin

  --usr, -U
      Search /usr.

  --etc, -E
      Search /etc.

  --var, -V
      Search /var.

  --opt, -O
      Search /opt.

  --boot, -B
      Search /boot.

  --lib, -L
      Search /lib.

  --bin
      Search /bin.

  --sbin
      Search /sbin.

MUTUALLY EXCLUSIVE MODES:
  Do not combine:
    --ALL
    --all
    --system

  Pick one broad scan mode at a time. The script will reject conflicting
  combinations because even search tools need boundaries.

COMMON USE:
  Find commands:
    smecli --command ssh

  Find aliases:
    smecli --aliases git

  Find installed packages:
    smecli --installed python

  Find package files:
    smecli --files libssl

  Search home directory:
    smecli --home project

  Search system directories:
    smecli --system firmware

  Big search with pager:
    smecli --all docker --less

  Full aggressive scan:
    smecli --ALL firmware --less

  Sort search results:
    smecli --path python --sort

  Use glob-style matching:
    smecli --home '*.conf' --glob

  Pipe machine-friendly output:
    smecli --installed python --pipe

  Exclude dotfiles from HOME searches:
    smecli --home config --excludeDotFiles

NOTES:
  - Regex mode is enabled by default.
  - Use --glob for literal/glob-style matching.
  - Use --sort for case-insensitive alphabetical output.
  - Use --pipe when feeding output into another script.
  - Use --less for interactive pagination.
  - Broad scans can produce a truly unreasonable amount of text.
'''

def show_help():
    print(SHORT_HELP)

def show_full_help():
    print(FULL_HELP)
