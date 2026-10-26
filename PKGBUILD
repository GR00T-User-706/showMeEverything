# SME_SIGNATURE=gr00t-user-706
# Build from the repository checkout with:
#   makepkg -si
#
# VERSION is the source of truth. SemVer Forge synchronizes this pkgver field
# from VERSION before release/package builds.

pkgname=showmeeverything-cli
pkgver=3.2.1
pkgrel=1
pkgdesc="System-wide Linux search CLI with Qt and Tk desktop interfaces"
arch=('x86_64')
url="https://github.com/GR00T-User-706/showMeEverything"
license=('GPL3')
depends=(
    'zsh'
    'qt5-base'
    'qt5-declarative'
    'qt5-quickcontrols2'
)
optdepends=(
    'python: Python Tkinter GUI fallback'
    'tk: Python Tkinter GUI fallback'
)
makedepends=(
    'git'
    'qt5-base'
)
source=("showmeeverything::git+https://github.com/GR00T-User-706/showMeEverything.git#branch=main")
sha256sums=('SKIP')

prepare() {
    local source_version
    source_version="$(<"$srcdir/showmeeverything/VERSION")"

    if [[ "$source_version" != "$pkgver" ]]; then
        error "VERSION mismatch: PKGBUILD pkgver is $pkgver but fetched VERSION is $source_version"
        return 1
    fi

    local required_file
    for required_file in \
        src/showMeEverything.launcher \
        src/showMeEverything.zsh \
        src/config.zsh \
        src/shell_searches.zsh \
        src/package_manager_searches.zsh \
        src/filesystem_searches.zsh \
        src/help.zsh \
        showmeeverything_gui/showmeeverything_gui.pro \
        showmeeverything_gui/resources.qrc \
        showmeeverything_gui/src/main.cpp \
        showmeeverything_gui/src/searchbackend.cpp \
        showmeeverything_gui/src/searchbackend.h \
        showmeeverything_gui/src/qml/main.qml \
        showmeeverything_gui/showmeeverything_tk.py \
        showmeeverything_gui/assets/com.github.gr00t-user-706.showmeeverything-gui-qml.desktop \
        showmeeverything_gui/assets/com.github.gr00t-user-706.showmeeverything-gui-python.desktop \
        LICENSE
    do
        if [[ ! -f "$srcdir/showmeeverything/$required_file" ]]; then
            error "Required source file is missing: $required_file"
            return 1
        fi
    done
}

build() {
    local repo_dir="$srcdir/showmeeverything"
    local build_dir="$srcdir/build-qml"

    mkdir -p "$build_dir"
    cd "$build_dir"

    qmake "$repo_dir/showmeeverything_gui/showmeeverything_gui.pro"
    make
}

package() {
    local repo_dir="$srcdir/showmeeverything"
    local module

    # Install the modular Zsh CLI.
    install -d "$pkgdir/usr/lib/showMeEverything"

    for module in \
        showMeEverything.zsh \
        config.zsh \
        shell_searches.zsh \
        package_manager_searches.zsh \
        filesystem_searches.zsh \
        help.zsh
    do
        if [[ "$module" == "showMeEverything.zsh" ]]; then
            install -Dm755 "$repo_dir/src/$module" \
                "$pkgdir/usr/lib/showMeEverything/$module"
        else
            install -Dm644 "$repo_dir/src/$module" \
                "$pkgdir/usr/lib/showMeEverything/$module"
        fi
    done

    # Generate the installed launcher with the package-owned module path.
    install -d "$pkgdir/usr/bin"
    sed 's|__SME_ENTRYPOINT__|/usr/lib/showMeEverything/showMeEverything.zsh|' \
        "$repo_dir/src/showMeEverything.launcher" \
        > "$pkgdir/usr/bin/showMeEverything"
    chmod 755 "$pkgdir/usr/bin/showMeEverything"
    ln -s showMeEverything "$pkgdir/usr/bin/smecli"

    # Install the Qt/QML GUI built above.
    install -Dm755 "$srcdir/build-qml/showmeeverything_qml" \
        "$pkgdir/usr/bin/showmeeverything_qml"
    ln -s showmeeverything_qml "$pkgdir/usr/bin/smegui"

    # Install the optional Python Tkinter fallback and its compatibility name.
    install -Dm755 "$repo_dir/showmeeverything_gui/showmeeverything_tk.py" \
        "$pkgdir/usr/bin/showmeeverything_tk"
    ln -s showmeeverything_tk "$pkgdir/usr/bin/smegpy"

    # Desktop launchers use pacman-managed paths and a theme icon.
    install -Dm644 \
        "$repo_dir/showmeeverything_gui/assets/com.github.gr00t-user-706.showmeeverything-gui-qml.desktop" \
        "$pkgdir/usr/share/applications/com.github.gr00t-user-706.showmeeverything-gui-qml.desktop"
    sed -i \
        -e 's|^Exec=.*|Exec=/usr/bin/showmeeverything_qml|' \
        -e 's|^Icon=.*|Icon=system-search|' \
        "$pkgdir/usr/share/applications/com.github.gr00t-user-706.showmeeverything-gui-qml.desktop"

    install -Dm644 \
        "$repo_dir/showmeeverything_gui/assets/com.github.gr00t-user-706.showmeeverything-gui-python.desktop" \
        "$pkgdir/usr/share/applications/com.github.gr00t-user-706.showmeeverything-gui-python.desktop"
    sed -i \
        -e 's|^Exec=.*|Exec=/usr/bin/showmeeverything_tk|' \
        -e 's|^Icon=.*|Icon=system-search|' \
        "$pkgdir/usr/share/applications/com.github.gr00t-user-706.showmeeverything-gui-python.desktop"

    install -Dm644 "$repo_dir/LICENSE" \
        "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
