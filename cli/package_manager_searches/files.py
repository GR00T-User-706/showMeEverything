from .detection import get_package_managers
from . import apt, pacman, dnf, zypper, apk

def search_package_files_db(pattern=''):
    modules={'apt':apt.files,'pacman':pacman.files,'dnf':dnf.files,'zypper':zypper.files,'apk':apk.files}
    for manager in get_package_managers():
        yield from modules[manager].search_package_files_db(pattern)
