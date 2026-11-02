from ..backend import run_backend
from ...output.filtering import filter_results
def search_packages_not_installed(pattern=''):
    available=run_backend('pacman','not_installed_available',pattern,['pacman','-Slq']).splitlines()
    installed=set(run_backend('pacman','not_installed_installed',pattern,['pacman','-Qq']).splitlines())
    yield from filter_results((x for x in available if x not in installed),pattern)
