from ..backend import run_backend
from ...output.filtering import filter_results
def search_packages_not_installed(pattern=''):
    available=run_backend('apt','not_installed_available',pattern,['apt-cache','pkgnames']).splitlines()
    installed=set(run_backend('apt','not_installed_installed',pattern,['dpkg-query','-W','-f=${binary:Package}\\n']).splitlines())
    yield from filter_results((x for x in available if x not in installed),pattern)
