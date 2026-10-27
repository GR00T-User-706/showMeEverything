from .. import config

SHORT_HELP = '''smecli2 — Show Me Everything CLI
Author:  Zenrich Shadowstep / GR00T-User-706
Version: @SME_VERSION@

USAGE:
  smecli2 [OPTIONS] [SEARCH_TERM ...]
  smecli2 [SEARCH_FLAGS...] [OPTIONS] [SEARCH_TERM ...]

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
      --includeMounts     Include mounted filesystems beneath HOME.
  -v, --version          Print SME version/signature.

SEARCH FLAGS:
  --ALL, -A              Aggressive full scan.
  --all                  Broad scan without system-directory sweep.
  --environment, --env, -e
                         Search environment and shell variables.
  --environment, --env, -e\n                         Search environment, shell variables, process\n                         environments, environment configuration, and\n                         application-defined environment variables.
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

FULL_HELP = '''smecli2 — Show Me Everything CLI
Author:  Zenrich Shadowstep / GR00T-User-706
Contact: crypto_code_weaver_syndicate@proton.me
Version: @SME_VERSION@

USAGE:
  smecli2 [OPTIONS] [SEARCH_TERM]
  smecli2 [SEARCH_FLAGS...] [OPTIONS] [SEARCH_TERM]

BASIC EXAMPLES:
  smecli2 --path python
  smecli2 --installed firefox
  smecli2 --home notes
  smecli2 --all network
  smecli2 --ALL usb --less
  smecli2 --systemd ssh
  smecli2 --packages nmap
  smecli2 --not-installed python
  smecli2 -c python ssh git

IMPORTANT:
  At least one search flag is required.
  Multiple SEARCH_TERM arguments are searched independently. SEARCH_TERM is optional for most flags.
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

  --includeMounts
      Include mounted filesystems beneath HOME, including FUSE/ADBFS.
      By default HOME searches stay on HOME's filesystem.

  -v, --version
      Print SME version/signature.

SEARCH GROUPS:
  --ALL, -A
      Aggressive full scan:
      environment, shell variables, PATH, commands, builtins, aliases,
      functions, manpages, systemd units, running processes, kernel modules,
      package repository, installed packages, package file DB,
      not-installed packages, HOME, and system directories.

      WARNING:
      Very large output, especially without SEARCH_TERM.

  --all
      Broad user/system scan without the full system directory sweep:
      environment, shell variables, PATH, commands, builtins, aliases,
      functions, manpages, running processes, package searches, and HOME.

      Safer than --ALL, but still potentially large.

ENVIRONMENT SEARCH FLAGS:
  --environment, --env, -e
      Search exported environment variables, shell variables discoverable
      from startup files, system environment configuration, systemd
      environments, readable process environments, and documented or
      configured application environment-variable names.

      Results include the source where the variable was discovered.
      Application variables may be reported even when they are not
      currently exported by the shell.

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
    smecli2 --command ssh

  Find environment and application variables:
    smecli2 --environment ollama

  Search Ollama-related environment variables:
    smecli2 --environment OLLAMA_

  Find aliases:
    smecli2 --aliases git

  Find installed packages:
    smecli2 --installed python

  Find package files:
    smecli2 --files libssl

  Search home directory:
    smecli2 --home project

  Search system directories:
    smecli2 --system firmware

  Big search with pager:
    smecli2 --all docker --less

  Full aggressive scan:
    smecli2 --ALL firmware --less

  Sort search results:
    smecli2 --path python --sort

  Use glob-style matching:
    smecli2 --home '*.conf' --glob

  Pipe machine-friendly output:
    smecli2 --installed python --pipe

  Exclude dotfiles from HOME searches:
    smecli2 --home config --excludeDotFiles

NOTES:
  - Regex mode is enabled by default.
  - Use --glob for literal/glob-style matching.
  - Use --sort for case-insensitive alphabetical output.
  - Use --pipe when feeding output into another script.
  - Use --less for interactive pagination.
  - Broad scans can produce a truly unreasonable amount of text.
'''

def show_help():
    print(SHORT_HELP.replace('@SME_VERSION@', config.SME_VERSION))

def show_full_help():
    print(FULL_HELP.replace('@SME_VERSION@', config.SME_VERSION))
