#!/data/data/com.termux/files/usr/bin/zsh
set_ver() {
	svf sync --discover || return
	svf next || return
}
build_pkg() {
	if command -v termux-create-package; then
		termux-create-package ./showmeeverything-termux.yaml || TCP_BUILD="failed"
		TCP_BUILD="success"
	fi
	if command -v makepkg; then
		makepkg ./packaging/arch/{cli,gui}/PKGBUILD || ARCH_BUILD="failed"
		ARCH_BUILD="success"
	fi
	if [[ "$ARCH_BUILD" == "failed" ]] && [[ "$TCP_BUILD" == "failed" ]]; then
		echo "both builds failed exit code 1" && exit 1
	fi
}

update_repo() {
	
	git pull || return
	git add . || return
	git commit -m "build: generated new packages" || return
	git push || return
}

install_sme() {
	ver="$(cat ./VERSION)
	apt install -y "./showmeeverything-cli_${ver}_all.deb" || return
}
set_ver
build_pkg
update_repo
install_sme
