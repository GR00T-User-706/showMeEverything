#!/usr/bin/env zsh
readonly SME_SIGNATURE="gr00t-user-706"
# SME_SIGNATURE=gr00t-user-706
# SME MODULAR MAIN / SEARCH ENGINE

SME_MODULE_DIR="${0:A:h}"

source "$SME_MODULE_DIR/config.zsh"
source "$SME_MODULE_DIR/shell_searches.zsh"
source "$SME_MODULE_DIR/package_manager_searches.zsh"
source "$SME_MODULE_DIR/filesystem_searches.zsh"
source "$SME_MODULE_DIR/help.zsh"

sme_grep() {
    local gropts=(-i)
    # Regex mode vs glob/literal mode
    if  [ "$REGEX" = 1 ]; then
        gropts+=(-E)
    else
        gropts+=(-F)
    fi

    # blank pattern = match everything
    local pattern="${1:-}"

    # output mode only controls color
    if [ "$PIPE_MODE" = 0 ] && [ "$COLOR_MODE" = 1 ] ; then
        grep "${gropts[@]}" --color=always -- "$pattern"
    elif  [ "$PIPE_MODE" = 1 ] && [ "$COLOR_MODE" = 0 ]; then
        grep "${gropts[@]}" --color=never -- "$pattern"
    else
        echo "${RED}FATAL${NC}: invalid PIPE_MODE/COLOR_MODE state" >&2
        exit 2
    fi
}

sme_sort() {
    if [ "$SORT_MODE" = 1 ]; then
        sort -f
    else
        cat
    fi
}


#header and footer functions for global use
header0() {
    [ "$PIPE_MODE" -eq 1 ] && return
    echo "#=========================================================#"
    echo "$1"
    echo "$2"
    echo "#=========================================================#"
}
footer() {
    [ "$PIPE_MODE" -eq 1 ] && return
    local TODAY="$(date +%c)"
    local info="$(echo "${TODAY} ${SHELL} ${USER} ${HOST}")"
    header0 "$info"
}

# --- Common exclude rules ---
search() {
    local -a search_terms=()
    local stop_parse=false
    local pattern=""
    local -a actions=()
    local use_less=false
    local exclude_dotfiles=false
    local has_ALL=false
    local has_all=false
    local has_system=false
    local original_args=("$@")
    if [ "${SMECLI_GUI_MODE:-0}" -eq 1 ]; then
        PIPE_MODE=1
    COLOR_MODE=0
    HEADER=0
    FOOTER=0
    fi

    while [ $# -gt 0 ]; do
        if [ "$stop_parse" = true ]; then
            search_terms+=("$1")
            shift
            continue
        fi

        if [ "$1" = "--" ]; then
            stop_parse=true
            shift
            continue
        fi



        case "$1" in
           --excludeDotFiles|--nodot) EXCLUDE_DOTFILES=true ;;
            --less) use_less=true ;;
            --sort) SORT_MODE=1 ;;
            --pipe)
                PIPE_MODE=1
                COLOR_MODE=0
                HEADER=0
                FOOTER=0
            ;;
            --glob) REGEX=0 ;;
            -v|--version)
                echo "SME_VERSION: $SME_VERSION"
                echo "SME_SIGNATURE: $SME_SIGNATURE$"
                return 0
            ;;

            --ALL | -A )
                actions+=(
                    search_path
                    search_loaded_commands
                    search_builtins
                    search_aliases
                    search_shell_functions
                    search_manpages
                    search_systemd_units
                    search_running_processes
                    loaded_kernel_modules
                    search_package_repo
                    search_installed_packages
                    search_package_files_db
                    search_packages_not_installed
                    search_home_directory
                    search_system_dirs
                )
            ;;
            --all )
                actions+=(
                    search_path
                    search_loaded_commands
                    search_builtins
                    search_aliases
                    search_shell_functions
                    search_manpages
                    search_running_processes
                    search_package_repo
                    search_installed_packages
                    search_package_files_db
                    search_packages_not_installed
                    search_home_directory
                )
            ;;

            --aliases  | -a ) actions+=(search_aliases) ;;
            --bin ) actions+=(search_bin) ;;
            --boot | -B ) actions+=(search_boot) ;;
            --builtins | -b ) actions+=(search_builtins) ;;
            --command |  -c) actions+=(search_loaded_commands) ;;
            --etc  | -E ) actions+=(search_etc) ;;
            --files | -F  ) actions+=(search_package_files_db) ;;
            --functions | -f ) actions+=(search_shell_functions) ;;
            --home | -H ) actions+=(search_home_directory) ;;
            --installed | -i  ) actions+=(search_installed_packages) ;;
            --lib | -L ) actions+=(search_lib) ;;
            --manpages | --man | -M ) actions+=(search_manpages) ;;
            --modules | -m ) actions+=(loaded_kernel_modules) ;;
            --not-installed | -n ) actions+=(search_packages_not_installed) ;;
            --process | -x ) actions+=(search_running_processes) ;;
            --packages | -p | --pkg ) actions+=(search_package_repo) ;;
            --path | -P  ) actions+=(search_path) ;;
            --sbin  ) actions+=(search_sbin) ;;
            --systemd | -s ) actions+=(search_systemd_units) ;;
            --system | -R ) actions+=(search_system_dirs) ;;
            --usr | -U ) actions+=(search_usr) ;;
            --var | -V ) actions+=(search_var) ;;
            --opt |  -O ) actions+=(search_opt) ;;

            --help | -h ) show_help; return ;;
            *)
                search_terms+=("$1")
            ;;
        esac
        shift
    done

    for arg in "${original_args[@]}"; do
        case "$arg" in
            --ALL|ALL|-A|A) has_ALL=true ;;
            --all|all) has_all=true ;;
            --system|system|-R|R) has_system=true ;;
        esac
    done
    if { [ "$has_ALL" = true ] && [ "$has_all" = true ]; } || \
       { [ "$has_ALL" = true ] && [ "$has_system" = true ]; } || \
       { [  "$has_all" = true ] && [ "$has_system" = true ]; }; then
        echo "WARNING: conflicting flags detected: ALL|all|system are mutually exclusive."
        echo "$0: For more info try [$0 --help]: returning. with exit code 1"
        return 1
    fi
    if [ "$has_ALL" = true ] || [ "$has_all" = true ]; then
        for fn in "${actions[@]}"; do
            case "$fn" in
                search_path|search_loaded_commands|search_builtins|search_aliases|search_shell_functions|search_manpages|search_systemd_units|search_running_processes|loaded_kernel_modules|search_package_repo|search_installed_packages|search_package_files_db|search_packages_not_installed|search_home_directory|search_system_dirs)
                    # allowed (part of ALL/all)
                    ;;
                *)
                    echo "$0: when using ALL/all, only --less, --sort, --pipe, --glob --excludeDotFiles are allowed alongside"
                    return 1
                    ;;
            esac
        done
    fi


    [ ${#actions[@]} -eq 0 ] && {
        echo "$0: No search flags given"
        echo "$0: for more information try [$0 --help]"
        return 1
    }
    pattern="${search_terms[*]}"
    if [ "$use_less" = true ]; then
        {
            for fn in "${actions[@]}"; do
                "$fn" "$pattern"
            done
        } | less -R
    else
        for fn in "${actions[@]}"; do
            "$fn" "$pattern"
        done
    fi

    footer
}

search "$@"

