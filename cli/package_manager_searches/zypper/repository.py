from ..backend import run_backend
from ...output.filtering import filter_results
def search_package_repo(pattern=''):
    out=run_backend('zypper','repository_search',pattern,['zypper','search'])
    yield from filter_results(out.splitlines(),pattern)
