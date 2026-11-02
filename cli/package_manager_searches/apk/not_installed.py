import re
from ..backend import run_backend
from ...output.filtering import filter_results
def search_packages_not_installed(pattern=''):
    available=run_backend('apk','not_installed_available',pattern,['apk','search']).splitlines()
    installed=set(run_backend('apk','not_installed_installed',pattern,['apk','info']).splitlines())
    names=[re.sub(r'-[0-9].*$','',x) for x in available]
    yield from filter_results((x for x in names if x not in installed),pattern)
