from ..backend import run_backend
from ...output.filtering import filter_results
def search_installed_packages(pattern=''):
    out=run_backend('zypper','installed_search',pattern,['rpm','-qa','--qf','%{NAME} %{VERSION}-%{RELEASE}\\n'])
    yield from filter_results(out.splitlines(),pattern)
