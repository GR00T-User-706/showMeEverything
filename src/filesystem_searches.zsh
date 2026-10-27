readonly SME_SIG_FILESYSTEM="gr00t-user--706"
# SME MODULE: FILESYSTEM SEARCHES

# HOME scans stay on HOME's filesystem unless --includeMounts is supplied.
# This prevents accidental traversal into FUSE/ADBFS and other mounted trees.
search_home_directory() {
    local info="Searching the home directory $HOME for $1 (excluding .cache; mounted filesystems excluded by default)..."
    local -a find_args
    find_args=("$HOME" -type d -name .cache -prune -o)

    if [ "$EXCLUDE_DOTFILES" = true ]; then
        find_args+=(-type d -name '.*' -prune -o)
    fi
    if [ "$INCLUDE_MOUNTS" != true ]; then
        find_args+=(-xdev)
    fi

    if [ "$REGEX" -eq 1 ]; then
        find_args+=(-type f -print)
    else
        find_args+=(-type f -iname "*$1*" -print)
    fi

    header0 "$info"
    if [ "$REGEX" -eq 1 ]; then
        find "${find_args[@]}" 2>/dev/null | sme_grep "$1" | sme_sort
    else
        find "${find_args[@]}" 2>/dev/null | sme_sort
    fi
}

search_system_dirs() {
    local info="Searching system directories (/usr, /etc, /sys, /dev, /var, /opt, /boot, /lib, /bin, /sbin) for $1..."
    local dirs=(/usr /etc /sys /dev /var /opt /boot /lib /bin /sbin)
    local d
    header0 "$info"
    for d in "${dirs[@]}"; do
        [ -d "$d" ] || continue
        if [ "$REGEX" -eq 1 ]; then
            find "$d" -type f 2>/dev/null | sme_grep "$1" | sme_sort
        else
            find "$d" -type f -iname "*$1*" 2>/dev/null | sme_sort
        fi
    done
}
