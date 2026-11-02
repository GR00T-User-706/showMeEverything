from ..backend import run_backend
from ...output.filtering import filter_results
def search_package_repo(pattern=''):
    out=run_backend('pacman','repository_search',pattern,['pacman','-Sl'])
    yield from filter_results(out.splitlines(),pattern)
