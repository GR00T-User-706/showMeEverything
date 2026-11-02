from ..backend import run_backend
from ...output.filtering import filter_results
def _available(text): return [p[2] for line in text.splitlines()[4:] if len(p:=line.split())>=3]
def search_packages_not_installed(pattern=''):
    available=run_backend('zypper','not_installed_available',pattern,['zypper','search'])
    installed=set(run_backend('zypper','not_installed_installed',pattern,['rpm','-qa','--qf','%{NAME}\\n']).splitlines())
    yield from filter_results((x for x in _available(available) if x not in installed),pattern)
