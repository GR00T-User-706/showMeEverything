readonly SME_SIG_ANDROID="gr00t-user-706"
# SME MODULE: ANDROID SYSTEM SEARCHES
search_termux_prefix() {
	local info="Searching the termUX \$PREFIX:[$PREFIX] for $1..."
	header0 "$info"
	if [ "$REGEX" -eq 1 ]; then
		find "$PREFIX" type f | sme_grep "$1" | sme_sort
	else
		find "$PREFIX" -iname "*$1*" | sme_grep "$1" | sme_sort
	fi
}

