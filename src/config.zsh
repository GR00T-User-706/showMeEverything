# SME MODULE: CONFIG
# The statements below are preserved from the original showMeEverything source.
readonly SME_SIGNATURE="gr00t-user-706"
readonly SME_VERSION="v2.3.5"
# GLOBAL CONFIG DEFAULT STATE
# VALID STATES:
# PIPE_MODE=0 COLOR_MODE=1  -> human readable ANSI output
# PIPE_MODE=1 COLOR_MODE=0  -> machine parseable output
# any other combination is invalid and fatal
#==========================================================================#
# PROJECT_ORIGIN="search()"
#search() {
#  { echo $path | tr ' ' '\n' | xargs -I{} ls {} | sort -u | grep "$1" } && { print -rl -- ${(k)commands} | grep "$1" }
#}
#==========================================================================#
RED="\e[31m"
GRN="\e[32m"
YLW="\e[33m"
BLU="\e[34m"
NC="\e[0m"

PIPE_MODE=0 # 0=off 1=on for MACHINE parse-able output formatting

COLOR_MODE=1
HEADER=1
FOOTER=1
REGEX=1
SORT_MODE=0
if [ -n "${ZSH_VERSION:-}" ]; then
    current_shell="zsh"
elif [ -n "${BASH_VERSION:-}" ]; then
    current_shell="bash"
else
    current_shell="$(basename "$SHELL")"
    echo "${RED}FATAL${NC}:  Detecting an Un-Supported Shell: $current_shell"
    echo "BASH or ZSH Are the only supported Shells"
    echo "Exiting with Exit Code 1"; sleep 5
    exit 1
fi
# setting for human readable / machine parseable
EXCLUDES=(
    -not -path "*/.cache/*"
)


[ "$current_shell" = "bash" ] && shopt -s expand_aliases 2>/dev/null
#==========================================#
