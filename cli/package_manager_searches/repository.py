from .detection import get_package_managers
from . import apt, pacman, dnf, zypper, apk

def search_package_repo(pattern=''):
    modules={'apt':apt.repository,'pacman':pacman.repository,'dnf':dnf.repository,'zypper':zypper.repository,'apk':apk.repository}
    for manager in get_package_managers():
        yield from modules[manager].search_package_repo(pattern)
