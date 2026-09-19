HELP_TEXT='''smecli — Show Me Everything CLI
Version: v3.0.0

USAGE:
  smecli [OPTIONS] [SEARCH_TERM]
  smecli [SEARCH_FLAGS...] [OPTIONS] [SEARCH_TERM]

OUTPUT OPTIONS:
  --less                 Internal interactive pager.
  --sort                 Sort results alphabetically, case-insensitive.
  --pipe                 Machine-friendly output: disables color, headers, footer.
  --glob                 Literal/fixed-string matching.
  --excludeDotFiles, --nodot
                         Exclude dotfiles from HOME searches.
  -v, --version         Print SME version/signature.
  -h, --help            Show this help.

SEARCH FLAGS:
  --ALL, -A             Aggressive full scan.
  --all                 Broad scan without system-directory sweep.
  --aliases, -a         Search aliases.
  --builtins, -b        Search shell builtins.
  --command, -c         Search loaded commands.
  --functions, -f       Search shell functions.
  --path, -P            Search PATH.
  --manpages, --man, -M Search manpage descriptions.
  --process, -x         Search running processes.
  --systemd, -s         Search systemd units.
  --modules, -m         Search loaded kernel modules.
  --packages, -p, --pkg Search package repository.
  --installed, -i       Search installed packages.
  --not-installed, -n   Search packages not installed.
  --files, -F           Search package file database.
  --home, -H            Search HOME.
  --system, -R          Search major system directories.
  --usr, -U             Search /usr.
  --etc, -E             Search /etc.
  --var, -V             Search /var.
  --opt, -O             Search /opt.
  --boot, -B            Search /boot.
  --lib, -L             Search /lib.
  --bin                 Search /bin.
  --sbin                Search /sbin.

Empty search patterns are valid and match everything in the selected domain.
Use -- to terminate option parsing. Large output is intentional; results are
not globally deduplicated and no arbitrary result limit is imposed.
'''
def show_help(): print(HELP_TEXT)
