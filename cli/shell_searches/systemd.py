import shutil,subprocess
from ..output.filtering import filter_results
def search_systemd_units(pattern=''):
    if not shutil.which('systemctl'): return
    r=subprocess.run(['systemctl','list-unit-files'],capture_output=True,text=True,check=False)
    yield from filter_results(r.stdout.splitlines(),pattern)
