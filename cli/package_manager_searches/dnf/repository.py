from ..backend import run_backend
from ...output.filtering import filter_results
def search_package_repo(pattern=''):
    out=run_backend('dnf','repository_search',pattern,['dnf','list','available'])
    yield from filter_results(out.splitlines(),pattern)
