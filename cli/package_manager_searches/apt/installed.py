from ..backend import run_backend
from ...output.filtering import filter_results
def search_installed_packages(pattern=''):
    out=run_backend('apt','installed_search',pattern,['dpkg-query','-W'])
    yield from filter_results(out.splitlines(),pattern)
