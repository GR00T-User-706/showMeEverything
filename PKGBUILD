# SME_SIGNATURE=gr00t-user-706
# Build the CLI package from the repository root:
#   makepkg -si
#
# VERSION is the source of truth; pkgver must match it.

pkgname=showmeeverything-cli
pkgver=3.2.1
pkgrel=2
pkgdesc='Show Me Everything command-line tools (Zsh and Python)'
arch=('any')
url='https://github.com/GR00T-User-706/showMeEverything'
license=('GPL3')
depends=('zsh' 'python')
source=()
sha256sums=()

# Intentionally no source clone and no build() function.
# makepkg's default $srcdir is named "src", which is already a real source
# directory in this repository. The CLI package needs no compilation, so it
# must not create build files or clone another checkout there.

check() {
    local repo_dir="$PWD"

    [[ "$(<"$repo_dir/VERSION")" == "$pkgver" ]] || {
        error "PKGBUILD pkgver ($pkgver) does not match VERSION ($( < "$repo_dir/VERSION" ))"
        return 1
    }

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$repo_dir" \
        python -m cli.smecli --version

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$repo_dir" \
        python -m cli.smecli --help >/dev/null

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$repo_dir" \
        python -m cli.smecli --full-help >/dev/null
}

package() {
    local repo_dir="$PWD"
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

    # Install the complete Python CLI module tree.
    install -d "$pkgdir/usr/lib/showmeeverything-python"
    cp -a "$repo_dir/cli" "$pkgdir/usr/lib/showmeeverything-python/"
    install -Dm644 "$repo_dir/VERSION" \
        "$pkgdir/usr/lib/showmeeverything-python/VERSION"

    # Never ship bytecode caches created by local development runs.
    find "$pkgdir/usr/lib/showmeeverything-python/cli" \
        -type d -name __pycache__ -prune -exec rm -rf {} +
    find "$pkgdir/usr/lib/showmeeverything-python/cli" \
        -type f -name '*.py[co]' -delete

    cat > "$pkgdir/usr/bin/smecli2" <<'EOF'
#!/usr/bin/env python3
import sys

sys.path.insert(0, "/usr/lib/showmeeverything-python")

from cli.smecli import main

raise SystemExit(main())
EOF
    chmod 755 "$pkgdir/usr/bin/smecli2"

    install -Dm644 "$repo_dir/LICENSE" \
        "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
