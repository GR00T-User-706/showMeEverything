import shutil,subprocess
from ..output.filtering import filter_results
def loaded_kernel_modules(pattern=''):
    if not shutil.which('lsmod'): return
    r=subprocess.run(['lsmod'],capture_output=True,text=True,check=False)
    yield from filter_results(r.stdout.splitlines(),pattern)
