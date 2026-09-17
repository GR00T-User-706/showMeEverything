readonly SME_SIGNATURE="gr00t-user-706"
# SME MODULE: PACKAGE MANAGER SEARCHES
# The functions below are preserved from the original showMeEverything source.
{
    #===============================#
    #===PACKAGE MANAGER DETECTION===#
    #===============================#
    {
        get_package_manager() {
            if command -v pacman >/dev/null 2>&1; then
                echo "pacman"
            elif command -v apt-cache >/dev/null 2>&1 && command -v dpkg-query >/dev/null 2>&1; then
                echo "apt"
            elif command -v dnf >/dev/null 2>&1; then
                echo "dnf"
            elif command -v zypper >/dev/null 2>&1; then
                echo "zypper"
            elif command -v apk >/dev/null 2>&1; then
                echo "apk"
            fi
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
                pacman -Sl 2>/dev/null | sme_grep "$1" | sme_sort
            }

            # -------- installed ---------- #
            pacman_installed_packages_search() {
                local info="Searching installed Pacman packages for $1..."
                header0 "$info"
                pacman -Q 2>/dev/null | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            pacman_search_not_installed() (
                local PIPE_MODE=1
                local COLOR_MODE=0
                local info="Searching Pacman for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(pacman -Slq 2>/dev/null | sme_grep "$1" | sme_sort | sort -u) \
                    <(pacman -Qq 2>/dev/null | sort -u) | sme_sort
            )

            # --------- files DB ---------- #
            pacman_files_db_search() {
                local info="Searching Pacman file database for $1..."
                header0 "$info"
                pacman -F "$1" 2>/dev/null | sme_sort
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
                    apt list 2>/dev/null | sme_sort
                else
                    apt list 2>/dev/null | sme_sort | sme_grep "$1" | sme_sort
                fi
            }

            # -------- installed ---------- #
            apt_installed_packages_search() {
                local info="Searching installed APT packages for $1..."
                header0 "$info"
                dpkg-query -W 2>/dev/null | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            apt_search_not_installed() {
                local info="Searching APT for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(apt-cache pkgnames 2>/dev/null | sme_grep "$1" | sme_sort | sort -u) \
                    <(dpkg-query -W -f='${binary:Package}\n' 2>/dev/null | sort -u) | sme_sort
            }

            # --------- files DB ---------- #
            apt_files_db_search() {
                local info="Searching installed APT/DPKG file ownership for $1..."
                header0 "$info"
                dpkg -S "*$1*" 2>/dev/null | sme_sort
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
                dnf list available 2>/dev/null | sme_grep "$1" | sme_sort
            }

            # -------- installed ---------- #
            dnf_installed_packages_search() {
                local info="Searching installed DNF packages for $1..."
                header0 "$info"
                dnf list installed 2>/dev/null | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            dnf_search_not_installed() {
                local info="Searching DNF for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(dnf list available 2>/dev/null | awk 'NR > 1 {print $1}' | sed 's/\.[^.[:space:]]*$//' | sme_grep "$1" | sme_sort | sort -u) \
                    <(dnf list installed 2>/dev/null | awk 'NR > 1 {print $1}' | sed 's/\.[^.[:space:]]*$//' | sort -u) | sme_sort
            }

            # --------- files DB ---------- #
            dnf_files_db_search() {
                local info="Searching DNF/RPM file ownership for $1..."
                header0 "$info"
                repoquery -f "*$1*" 2>/dev/null | sme_sort
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
                zypper search 2>/dev/null | sme_grep "$1" | sme_sort
            }

            # -------- installed ---------- #
            zypper_installed_packages_search() {
                local info="Searching installed Zypper packages for $1..."
                header0 "$info"
                rpm -qa --qf '%{NAME} %{VERSION}-%{RELEASE}\n' 2>/dev/null | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            zypper_search_not_installed() {
                local info="Searching Zypper for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(zypper search 2>/dev/null | awk 'NR > 4 {print $3}' | sme_grep "$1" | sme_sort | sort -u) \
                    <(rpm -qa --qf '%{NAME}\n' 2>/dev/null | sort -u) | sme_sort
            }

            # --------- files DB ---------- #
            zypper_files_db_search() {
                local info="Searching Zypper/RPM file ownership for $1..."
                header0 "$info"
                rpm -qal 2>/dev/null | sme_grep "$1" | sme_sort
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
                apk search 2>/dev/null | sme_grep "$1" | sme_sort
            }

            # -------- installed ---------- #
            apk_installed_packages_search() {
                local info="Searching installed APK packages for $1..."
                header0 "$info"
                apk info 2>/dev/null | sme_grep "$1" | sme_sort
            }

            #--------not installed----------#
            apk_search_not_installed() {
                local info="Searching APK for packages not installed: $1..."
                header0 "$info"
                comm -23 \
                    <(apk search 2>/dev/null | sed 's/-[0-9].*$//' | sme_grep "$1" | sme_sort | sort -u) \
                    <(apk info 2>/dev/null | sort -u) | sme_sort
            }

            # --------- files DB ---------- #
            apk_files_db_search() {
                local info="Searching APK file ownership for $1..."
                header0 "$info"
                apk info -L 2>/dev/null | sme_grep "$1" | sme_sort
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
                case "$(get_package_manager)" in
                pacman) pacman_full_repo_search "$1" ;;
                apt) apt_full_repo_search "$1" ;;
                dnf) dnf_full_repo_search "$1" ;;
                zypper) zypper_full_repo_search "$1" ;;
                apk) apk_full_repo_search "$1" ;;
                esac
            }

            # ----- NOT INSTALLED --- #
            search_packages_not_installed() {
                case "$(get_package_manager)" in
                pacman) pacman_search_not_installed "$1" ;;
                apt) apt_search_not_installed "$1" ;;
                dnf) dnf_search_not_installed "$1" ;;
                zypper) zypper_search_not_installed "$1" ;;
                apk) apk_search_not_installed "$1" ;;
                esac
            }

            # ------- INSTALLED ----- #
            search_installed_packages() {
                case "$(get_package_manager)" in
                pacman) pacman_installed_packages_search "$1" ;;
                apt) apt_installed_packages_search "$1" ;;
                dnf) dnf_installed_packages_search "$1" ;;
                zypper) zypper_installed_packages_search "$1" ;;
                apk) apk_installed_packages_search "$1" ;;
                esac
            }

            # --- pkg mngr file DB --- #
            search_package_files_db() {
                case "$(get_package_manager)" in
                pacman) pacman_files_db_search "$1" ;;
                apt) apt_files_db_search "$1" ;;
                dnf) dnf_files_db_search "$1" ;;
                zypper) zypper_files_db_search "$1" ;;
                apk) apk_files_db_search "$1" ;;
                esac
            }
        }
    }
}
