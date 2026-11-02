from ..backend import run_backend
from ...output.filtering import filter_results
def search_installed_packages(pattern=''):
    out=run_backend('apk','installed_search',pattern,['apk','info'])
    yield from filter_results(out.splitlines(),pattern)
