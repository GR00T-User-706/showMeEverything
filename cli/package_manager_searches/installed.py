from .detection import get_package_managers
from . import apt, pacman, dnf, zypper, apk

def search_installed_packages(pattern=''):
    modules={'apt':apt.installed,'pacman':pacman.installed,'dnf':dnf.installed,'zypper':zypper.installed,'apk':apk.installed}
    for manager in get_package_managers():
        yield from modules[manager].search_installed_packages(pattern)
