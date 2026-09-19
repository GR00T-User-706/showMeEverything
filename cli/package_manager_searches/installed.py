import subprocess
from .detection import get_package_manager
from ..output.filtering import filter_results
def search_installed_packages(pattern=''):
    pm=get_package_manager()
    if pm=='pacman': cmd=['pacman','-Q']
    elif pm=='apt': cmd=['dpkg-query','-W']
    else: return
    r=subprocess.run(cmd,capture_output=True,text=True,check=False)
    yield from filter_results(r.stdout.splitlines(),pattern)
