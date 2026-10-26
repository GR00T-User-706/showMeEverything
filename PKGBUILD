pkgname=showmeeverything-cli
pkgver=3.2.1
pkgrel=1
pkgdesc="showMeEverything command-line tools"
arch=('any')
url="https://github.com/GR00T-User-706/showMeEverything"
license=('custom')
depends=('python' 'zsh')
source=()
sha256sums=()

package() {
cd "$srcdir"

```
# Install the Zsh implementation and its modules.
install -d "$pkgdir/usr/lib/showMeEverything"

install -Dm755 src/showMeEverything.zsh \
    "$pkgdir/usr/lib/showMeEverything/showMeEverything.zsh"

install -Dm644 src/config.zsh \
    "$pkgdir/usr/lib/showMeEverything/config.zsh"

install -Dm644 src/shell_searches.zsh \
    "$pkgdir/usr/lib/showMeEverything/shell_searches.zsh"

install -Dm644 src/package_manager_searches.zsh \
    "$pkgdir/usr/lib/showMeEverything/package_manager_searches.zsh"

install -Dm644 src/filesystem_searches.zsh \
    "$pkgdir/usr/lib/showMeEverything/filesystem_searches.zsh"

install -Dm644 src/help.zsh \
    "$pkgdir/usr/lib/showMeEverything/help.zsh"

# Install the Zsh command and its aliases.
install -d "$pkgdir/usr/bin"

ln -s ../lib/showMeEverything/showMeEverything.zsh \
    "$pkgdir/usr/bin/showMeEverything"

ln -s ../lib/showMeEverything/showMeEverything.zsh \
    "$pkgdir/usr/bin/smecli"

# Install the Python CLI launcher.
install -Dm755 packaging/smecli2 \
    "$pkgdir/usr/bin/smecli2"

# Install the Python CLI module.
local pyver
pyver=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

install -d "$pkgdir/usr/lib/python${pyver}/site-packages"

cp -r cli "$pkgdir/usr/lib/python${pyver}/site-packages/cli"
```

}
