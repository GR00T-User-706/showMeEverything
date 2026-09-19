import subprocess
from .detection import get_package_manager
def search_package_files_db(pattern=''):
    pm=get_package_manager()
    if pm=='pacman': yield from subprocess.run(['pacman','-F',pattern],capture_output=True,text=True,check=False).stdout.splitlines()
    elif pm=='apt': yield from subprocess.run(['dpkg','-S','*'+pattern+'*'],capture_output=True,text=True,check=False).stdout.splitlines()
