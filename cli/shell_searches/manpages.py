import shutil,subprocess
from ..output.filtering import filter_results
def search_manpages(pattern=''):
    if not shutil.which('apropos'): return
    r=subprocess.run(['apropos','-w',('*'+pattern+'*' if pattern else '*')],capture_output=True,text=True,check=False)
    yield from filter_results(r.stdout.splitlines(),pattern)
