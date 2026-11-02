from ..backend import run_backend
from ...output.filtering import filter_results
def _names(text):
    return [line.split()[0].rsplit('.',1)[0] for line in text.splitlines()[1:] if line.split()]
def search_packages_not_installed(pattern=''):
    available=run_backend('dnf','not_installed_available',pattern,['dnf','list','available'])
    installed=set(_names(run_backend('dnf','not_installed_installed',pattern,['dnf','list','installed'])))
    yield from filter_results((x for x in _names(available) if x not in installed),pattern)
