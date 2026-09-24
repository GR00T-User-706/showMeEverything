readonly SME_SIG_SHELL="gr00t-user--706"
# SME MODULE: SHELL SEARCHES
# The functions below are preserved from the original showMeEverything source.
#==== SHELL SPECIFIC  SEARCH FUNCTIONS ====#
#==========================================#
search_path() {
    local info="Searching \$PATH for $1..."
    local dir
    header0 "$info"

    while IFS=: read -r dir; do
        [ -d "$dir" ] || continue

        if [ "$REGEX" -eq 1 ]; then
            find "$dir" "${EXCLUDES[@]}" -type f 2>/dev/null | sme_grep "$1" | sme_sort
        else
            find "$dir" "${EXCLUDES[@]}" -iname "*$1*" 2>/dev/null | sme_grep "$1" | sme_sort
        fi
    done <<< "$PATH"
}
search_loaded_commands() {
    local info="Searching loaded shell commands for $1..."
    header0 "$info"

    if [ "$current_shell" = "zsh" ]; then
        eval 'print -rl -- ${(k)commands}' | sme_grep "$1" | sme_sort
    elif [ "$current_shell" = "bash" ]; then
        compgen -c | sme_grep "$1" | sme_sort
    fi
}

search_builtins() {
    local info="Searching shell builtins for $1..."
    header0 "$info"

    if [ "$current_shell" = "zsh" ]; then
        eval 'print -rl -- ${(k)builtins}' | sme_grep "$1" | sme_sort
    elif [ "$current_shell" = "bash" ]; then
        compgen -b | sme_grep "$1" | sme_sort
    fi
}

search_shell_functions() {
    local info="Searching loaded shell functions for $1..."
    header0 "$info"

    if [ "$current_shell" = "zsh" ]; then
        eval 'print -rl -- ${(k)functions}' | sme_grep "$1" | sme_sort
    elif [ "$current_shell" = "bash" ]; then
        compgen -A function | sme_grep "$1" | sme_sort
    fi
}

search_aliases() {
    local info="Searching shell aliases for $1..."
    header0 "$info"
    alias | sme_grep "$1" | sme_sort
}


search_manpages() {
    local info="Searching manpage descriptions for $1..."
    local wcs="*$1*"
    header0 "$info"

    if command -v apropos >/dev/null 2>&1; then
        apropos -w "$wcs" | sme_grep "$1" | sme_sort
    fi
}

search_systemd_units() {
    local info="Searching systemd unit files for $1..."
    header0 "$info"

    if command -v systemctl >/dev/null 2>&1; then
        systemctl list-unit-files 2>/dev/null | sme_grep "$1" | sme_sort
    fi
}

search_running_processes() {
    local info="Searching running processes for $1..."
    header0 "$info"
    ps aux 2>/dev/null | sme_grep "$1" | sme_sort
}

loaded_kernel_modules() {
    local info="Searching loaded kernel modules for $1..."
    header0 "$info"

    if command -v lsmod >/dev/null 2>&1; then
        lsmod 2>/dev/null | sme_grep "$1" | sme_sort
    fi
}
