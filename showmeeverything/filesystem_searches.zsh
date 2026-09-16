# SME MODULE: FILESYSTEM SEARCHES
# The functions below are preserved from the original showMeEverything source.
search_home_directory() {
    local info="Searching the home directory $HOME for $1 (excluding .cache)..."
    local exclude_dirs="$HOME/.cache"
    local dotfiles="$HOME/.*"

    header0 "$info"

    if [ "$exclude_dotfiles" = true ]; then
        if [ "$REGEX" -eq 1 ]; then
            find "$HOME" -not -path "$exclude_dirs/*" -not -path "$HOME/.*" -type f 2>/dev/null | sme_grep "$1" | sme_sort
        else
            find "$HOME" -not -path "$exclude_dirs/*" -not -path "$HOME/.*" -iname "*$1*" 2>/dev/null | sme_sort
        fi
    else
        if [ "$REGEX" -eq 1 ]; then
            find "$HOME" -not -path "$exclude_dirs/*" -type f 2>/dev/null | sme_grep "$1" | sme_sort
        else
            find "$HOME" -not -path "$exclude_dirs/*" -iname "*$1*" 2>/dev/null | sme_sort
        fi
    fi
}
search_system_dirs() {
    local info="Searching system directories (/usr, /etc, /sys, /var, /opt, /boot, /lib, /bin, /sbin) for $1..."
    local dirs=(/usr /etc /sys /dev /var /opt /boot /lib /bin /sbin)
    local d

    header0 "$info"

    for d in "${dirs[@]}"; do
        [ -d "$d" ] || continue

        if [ "$REGEX" -eq 1 ]; then
            find "$d" -type f 2>/dev/null | sme_grep "$1" | sme_sort
        else
            find "$d" -iname "*$1*" 2>/dev/null | sme_sort
        fi
    done
}
search_usr() {
    local info="Searching /dir for $1..."
    header0 "$info"

    [ -d /usr ] || return
    find /usr -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

search_etc() {
    local info="Searching /etc for $1..."
    header0 "$info"

    [ -d /etc ] || return
    find /etc -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

search_sys() {
    local info="Searching /sys for $1..."
    header0 "$info"

    [ -d /sys ] || return
    find /sys -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

search_var() {
    local info="Searching /var for $1..."
    header0 "$info"

    [ -d /var ] || return
    find /var -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

search_opt() {
    local info="Searching /opt for $1..."
    header0 "$info"

    [ -d /opt ] || return
    find /opt -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

search_boot() {
    local info="Searching /boot for $1..."
    header0 "$info"
    [ -d /boot ] || return
    find /boot -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

search_lib() {
    local info="Searching /lib for $1..."
    header0 "$info"
    [ -d /lib ] || return
    find /lib -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

search_bin() {
    local info="Searching /bin for $1..."
    header0 "$info"
    [ -d /bin ] || return
    find /bin -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

search_sbin() {
    local info="Searching /sbin for $1..."
    header0 "$info"
    [ -d /sbin ] || return
    find /sbin -iname "*$1*" "${EXCLUDES[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
}

