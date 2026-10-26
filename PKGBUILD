# SME_SIGNATURE=gr00t-user-706
# Build from a clean repository checkout with:
#   makepkg -si
#
# VERSION is the source of truth. Keep pkgver synchronized with VERSION.

pkgbase=showmeeverything
pkgname=('showmeeverything-cli' 'showmeeverything-gui')
pkgver=3.2.1
pkgrel=2
pkgdesc='System-wide search tools: Zsh/Python CLIs and desktop interfaces'
arch=('x86_64')
url='https://github.com/GR00T-User-706/showMeEverything'
license=('GPL3')

depends_cli=('zsh' 'python')
depends_gui=('qt5-base' 'qt5-declarative' 'qt5-quickcontrols2')
optdepends_gui=(
    'showmeeverything-cli: command-line search engine used by the GUI'
    'tk: Python Tkinter GUI fallback'
)

makedepends=('qt5-base' 'qt5-declarative' 'qt5-quickcontrols2')

# This PKGBUILD builds the checked-out working tree directly. Do not clone the
# repository into $srcdir: makepkg's $srcdir is already named "src" and would
# collide with this project's real src/ directory.
source=()
sha256sums=()

prepare() {
    local repo_dir="$startdir"
    local source_version
    source_version="$(<"$repo_dir/VERSION")"

    if [[ "$source_version" != "$pkgver" ]]; then
        error "VERSION mismatch: PKGBUILD pkgver is $pkgver but VERSION is $source_version"
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
        cli/smecli.py \
        cli/config.py \
        cli/search/arguments.py \
        cli/search/actions.py \
        cli/search/search.py \
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
        if [[ ! -f "$repo_dir/$required_file" ]]; then
            error "Required source file is missing: $required_file"
            return 1
        fi
    done
}

build() {
    local repo_dir="$startdir"
    local build_dir="$srcdir/build-qml"

    mkdir -p "$build_dir"
    cd "$build_dir"

    qmake-qt5 "$repo_dir/showmeeverything_gui/showmeeverything_gui.pro"
    make
}

package_showmeeverything-cli() {
    depends=('zsh' 'python')
    local repo_dir="$startdir"
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

    install -d "$pkgdir/usr/bin"
    sed 's|__SME_ENTRYPOINT__|/usr/lib/showMeEverything/showMeEverything.zsh|' \
        "$repo_dir/src/showMeEverything.launcher" \
        > "$pkgdir/usr/bin/showMeEverything"
    chmod 755 "$pkgdir/usr/bin/showMeEverything"
    ln -s showMeEverything "$pkgdir/usr/bin/smecli"

    # Install the complete Python CLI package, preserving its module layout.
    install -d "$pkgdir/usr/lib/showmeeverything-python"
    cp -a "$repo_dir/cli" "$pkgdir/usr/lib/showmeeverything-python/"
    install -Dm644 "$repo_dir/VERSION" \
        "$pkgdir/usr/lib/showmeeverything-python/VERSION"

    cat > "$pkgdir/usr/bin/smecli2" <<'EOF'
#!/usr/bin/env python3
import sys

sys.path.insert(0, "/usr/lib/showmeeverything-python")

from cli.smecli import main

raise SystemExit(main())
EOF
    chmod 755 "$pkgdir/usr/bin/smecli2"

    install -Dm644 "$repo_dir/LICENSE" \
        "$pkgdir/usr/share/licenses/showmeeverything-cli/LICENSE"
}

package_showmeeverything-gui() {
    depends=('qt5-base' 'qt5-declarative' 'qt5-quickcontrols2')
    optdepends=(
        'showmeeverything-cli: command-line search engine used by the GUI'
        'tk: Python Tkinter GUI fallback'
    )
    local repo_dir="$startdir"

    # Install the Qt/QML GUI.
    install -Dm755 "$srcdir/build-qml/showmeeverything_qml" \
        "$pkgdir/usr/bin/showmeeverything_qml"
    ln -s showmeeverything_qml "$pkgdir/usr/bin/smegui"

    # Install the optional Python Tkinter GUI fallback.
    install -Dm755 "$repo_dir/showmeeverything_gui/showmeeverything_tk.py" \
        "$pkgdir/usr/bin/showmeeverything_tk"
    ln -s showmeeverything_tk "$pkgdir/usr/bin/smegpy"

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
        "$pkgdir/usr/share/licenses/showmeeverything-gui/LICENSE"
}
