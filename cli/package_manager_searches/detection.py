import shutil
def get_package_manager():
    if shutil.which('pacman'): return 'pacman'
    if shutil.which('apt-cache') and shutil.which('dpkg-query'): return 'apt'
    if shutil.which('dnf'): return 'dnf'
    if shutil.which('zypper'): return 'zypper'
    if shutil.which('apk'): return 'apk'
    return None
