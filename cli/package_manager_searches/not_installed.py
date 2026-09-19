import subprocess
from .detection import get_package_manager
from ..output.filtering import filter_results
def search_packages_not_installed(pattern=''):
    pm=get_package_manager()
    if pm=='pacman':
        available=subprocess.run(['pacman','-Slq'],capture_output=True,text=True,check=False).stdout.splitlines()
        installed=set(subprocess.run(['pacman','-Qq'],capture_output=True,text=True,check=False).stdout.splitlines())
    elif pm=='apt':
        available=subprocess.run(['apt-cache','pkgnames'],capture_output=True,text=True,check=False).stdout.splitlines()
        installed=set(subprocess.run(['dpkg-query','-W','-f='+chr(36)+'{binary:Package}\\n'],capture_output=True,text=True,check=False).stdout.splitlines())
    else: return
    yield from filter_results((x for x in available if x not in installed),pattern)
