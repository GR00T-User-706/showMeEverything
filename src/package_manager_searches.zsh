readonly SME_SIG_PKGMAN="gr00t-user--706"

# Persist package-manager errors outside the result stream.
typeset -g SME_PACKAGE_ERRORS_LOGGED=0
typeset -g SME_PACKAGE_ERROR_LOG=""
typeset -g SME_PACKAGE_ERROR_MARKER="${TMPDIR:-/tmp}/sme-pm-errors-$$"
sme_pm_run() {
    local manager="$1" operation="$2" term="$3"; shift 3
    local tmp condition log_path
    tmp="$(mktemp "${TMPDIR:-/tmp}/sme-pm.XXXXXX")" || return 1
    "$@" 2>"$tmp"
    condition=$?
    if (( condition != 0 )) || [[ -s "$tmp" ]]; then
        log_path="${SME_ERROR_LOG:-${XDG_STATE_HOME:-$HOME/.local/state}/showmeeverything/errors.log}"
        SME_PACKAGE_ERRORS_LOGGED=1
        SME_PACKAGE_ERROR_LOG="$log_path"
        : > "$SME_PACKAGE_ERROR_MARKER"
        mkdir -p -- "${log_path:h}" 2>/dev/null || true
        { print -r -- "[$(date '+%Y-%m-%d %H:%M:%S')]"; print -r -- "MANAGER: $manager"; print -r -- "OPERATION: $operation"; print -r -- "SEARCH_TERM: $term"; print -r -- "COMMAND: $*"; print -r -- "EXIT_STATUS: $condition"; print -r -- "STDERR:"; cat "$tmp"; print -r -- "----------------------------------------"; } >> "$log_path" 2>/dev/null
    fi
    rm -f -- "$tmp"
    return 0
}
# SME MODULE: PACKAGE MANAGER SEARCHES
# The functions below are preserved from the original showMeEverything source.
{
    #===============================#
    #===PACKAGE MANAGER DETECTION===#
    #===============================#
    {
        get_package_manager() {
            local -a managers=()
            command -v pacman >/dev/null 2>&1 && managers+=(pacman)
            command -v apt-cache >/dev/null 2>&1 && command -v dpkg-query >/dev/null 2>&1 && managers+=(apt)
            command -v dnf >/dev/null 2>&1 && managers+=(dnf)
            command -v zypper >/dev/null 2>&1 && command -v rpm >/dev/null 2>&1 && managers+=(zypper)
            command -v apk >/dev/null 2>&1 && managers+=(apk)
            if [[ -n "${SME_PACKAGE_MANAGER_FILTER:-}" ]]; then
                local selected=()
                for manager in "${managers[@]}"; do
                    [[ "$manager" == "$SME_PACKAGE_MANAGER_FILTER" ]] && selected+=("$manager")
                done
                managers=("${selected[@]}")
            fi
            print -rl -- "${managers[@]}"
        }
    }

    {
        #===============================#
        #=======PACMAN FUNCTIONS========#
        #===============================#
        {
            # -------- full repo ---------- #
            pacman_full_repo_search() {
                local info="Searching Pacman repo for $1..."
                header0 "$info"
                sme_pm_run pacman repository_search "$1" pacman -Sl | sme_grep "$1" | sme_sort
            }

            # -------- installed ---------- #
            pacman_installed_packages_search() {
                local info="Searching installed Pacman packages for $1..."
                header0 "$info"
                sme_pm_run pacman installed_search "$1" pacman -Q | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            pacman_search_not_installed() (
                local PIPE_MODE=1
                local COLOR_MODE=0
                local info="Searching Pacman for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(sme_pm_run pacman not_installed_available "$1" pacman -Slq | sme_grep "$1" | sme_sort | sort -u) \
                    <(sme_pm_run pacman not_installed_installed "$1" pacman -Qq | sort -u) | sme_sort
            )

            # --------- files DB ---------- #
            pacman_files_db_search() {
                local info="Searching Pacman file database for $1..."
                header0 "$info"
                sme_pm_run pacman file_database_search "$1" pacman -F "$1" | sme_sort
            }
        }
    }

    {
        #===============================#
        #=========APT FUNCTIONS=========#
        #===============================#
        {
            # -------- full repo ---------- #
            apt_full_repo_search() {
                local info="Searching APT repo for $1..."
                header0 "$info"
                if [ -z "$1" ]; then
                    sme_pm_run apt repository_search "$1" apt list | sme_sort
                else
                    sme_pm_run apt repository_search "$1" apt list | sme_sort | sme_grep "$1" | sme_sort
                fi
            }

            # -------- installed ---------- #
            apt_installed_packages_search() {
                local info="Searching installed APT packages for $1..."
                header0 "$info"
                sme_pm_run apt installed_search "$1" dpkg-query -W | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            apt_search_not_installed() {
                local info="Searching APT for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(sme_pm_run apt not_installed_available "$1" apt-cache pkgnames | sme_grep "$1" | sme_sort | sort -u) \
                    <(sme_pm_run apt not_installed_installed "$1" dpkg-query -W -f='${binary:Package}\n' | sort -u) | sme_sort
            }

            # --------- files DB ---------- #
            apt_files_db_search() {
                local info="Searching installed APT/DPKG file ownership for $1..."
                header0 "$info"
                sme_pm_run apt file_ownership_search "$1" dpkg -S "*$1*" | sme_sort
            }
        }
    }

    {
        #===============================#
        #=========DNF FUNCTIONS=========#
        #===============================#
        {
            # -------- full repo ---------- #
            dnf_full_repo_search() {
                local info="Searching DNF repo for $1..."
                header0 "$info"
                sme_pm_run dnf repository_search "$1" dnf list available | sme_grep "$1" | sme_sort
            }

            # -------- installed ---------- #
            dnf_installed_packages_search() {
                local info="Searching installed DNF packages for $1..."
                header0 "$info"
                sme_pm_run dnf installed_search "$1" dnf list installed | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            dnf_search_not_installed() {
                local info="Searching DNF for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(sme_pm_run dnf not_installed_available "$1" dnf list available | awk 'NR > 1 {print $1}' | sed 's/\.[^.[:space:]]*$//' | sme_grep "$1" | sme_sort | sort -u) \
                    <(sme_pm_run dnf not_installed_installed "$1" dnf list installed | awk 'NR > 1 {print $1}' | sed 's/\.[^.[:space:]]*$//' | sort -u) | sme_sort
            }

            # --------- files DB ---------- #
            dnf_files_db_search() {
                local info="Searching DNF/RPM file ownership for $1..."
                header0 "$info"
                sme_pm_run dnf file_database_search "$1" repoquery -f "*$1*" | sme_sort
            }
        }
    }

    {
        #===============================#
        #=======ZYPPER FUNCTIONS========#
        #===============================#
        {
            # -------- full repo ---------- #
            zypper_full_repo_search() {
                local info="Searching Zypper repo for $1..."
                header0 "$info"
                sme_pm_run zypper repository_search "$1" zypper search | sme_grep "$1" | sme_sort
            }

            # -------- installed ---------- #
            zypper_installed_packages_search() {
                local info="Searching installed Zypper packages for $1..."
                header0 "$info"
                sme_pm_run zypper installed_search "$1" rpm -qa --qf '%{NAME} %{VERSION}-%{RELEASE}\n' | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            zypper_search_not_installed() {
                local info="Searching Zypper for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(sme_pm_run zypper not_installed_available "$1" zypper search | awk 'NR > 4 {print $3}' | sme_grep "$1" | sme_sort | sort -u) \
                    <(sme_pm_run zypper not_installed_installed "$1" rpm -qa --qf '%{NAME}\n' | sort -u) | sme_sort
            }

            # --------- files DB ---------- #
            zypper_files_db_search() {
                local info="Searching Zypper/RPM file ownership for $1..."
                header0 "$info"
                sme_pm_run zypper file_database_search "$1" rpm -qal | sme_grep "$1" | sme_sort
            }
        }
    }

    {
        #===============================#
        #=========APK FUNCTIONS=========#
        #===============================#
        {
            # -------- full repo ---------- #
            apk_full_repo_search() {
                local info="Searching APK repo for $1..."
                header0 "$info"
                sme_pm_run apk repository_search "$1" apk search | sme_grep "$1" | sme_sort
            }

            # -------- installed ---------- #
            apk_installed_packages_search() {
                local info="Searching installed APK packages for $1..."
                header0 "$info"
                sme_pm_run apk installed_search "$1" apk info | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            apk_search_not_installed() {
                local info="Searching APK for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(sme_pm_run apk not_installed_available "$1" apk search | sed 's/-[0-9].*$//' | sme_grep "$1" | sme_sort | sort -u) \
                    <(sme_pm_run apk not_installed_installed "$1" apk info | sort -u) | sme_sort
            }

            # --------- files DB ---------- #
            apk_files_db_search() {
                local info="Searching APK file ownership for $1..."
                header0 "$info"
                sme_pm_run apk file_database_search "$1" apk info -L | sme_grep "$1" | sme_sort
            }
        }
    }

    {
        #===============================#
        #== PACKAGE MANAGER MANAGMENT ==#
        #===============================#
        {
            #  ---- FULL REPO  ------ #
            search_package_repo() {
                local manager
                while IFS= read -r manager; do
                    case "$manager" in
                        pacman) pacman_full_repo_search "$1" ;;
                        apt) apt_full_repo_search "$1" ;;
                        dnf) dnf_full_repo_search "$1" ;;
                        zypper) zypper_full_repo_search "$1" ;;
                        apk) apk_full_repo_search "$1" ;;
                    esac
                done < <(get_package_manager)
            }

            # ----- NOT INSTALLED --- #
            search_packages_not_installed() {
                local manager
                while IFS= read -r manager; do
                    case "$manager" in
                        pacman) pacman_search_not_installed "$1" ;;
                        apt) apt_search_not_installed "$1" ;;
                        dnf) dnf_search_not_installed "$1" ;;
                        zypper) zypper_search_not_installed "$1" ;;
                        apk) apk_search_not_installed "$1" ;;
                    esac
                done < <(get_package_manager)
            }

            # ------- INSTALLED ----- #
            search_installed_packages() {
                local manager
                while IFS= read -r manager; do
                    case "$manager" in
                        pacman) pacman_installed_packages_search "$1" ;;
                        apt) apt_installed_packages_search "$1" ;;
                        dnf) dnf_installed_packages_search "$1" ;;
                        zypper) zypper_installed_packages_search "$1" ;;
                        apk) apk_installed_packages_search "$1" ;;
                    esac
                done < <(get_package_manager)
            }

            # --- pkg mngr file DB --- #
            search_package_files_db() {
                local manager
                while IFS= read -r manager; do
                    case "$manager" in
                        pacman) pacman_files_db_search "$1" ;;
                        apt) apt_files_db_search "$1" ;;
                        dnf) dnf_files_db_search "$1" ;;
                        zypper) zypper_files_db_search "$1" ;;
                        apk) apk_files_db_search "$1" ;;
                    esac
                done < <(get_package_manager)
            }
        }
    }
}
