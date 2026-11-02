from .detection import get_package_managers
from . import apt, pacman, dnf, zypper, apk

def search_packages_not_installed(pattern=''):
    modules={'apt':apt.not_installed,'pacman':pacman.not_installed,'dnf':dnf.not_installed,'zypper':zypper.not_installed,'apk':apk.not_installed}
    for manager in get_package_managers():
        yield from modules[manager].search_packages_not_installed(pattern)
