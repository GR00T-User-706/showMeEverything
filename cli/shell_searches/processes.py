import subprocess
from ..output.filtering import filter_results
def search_running_processes(pattern=''):
    r=subprocess.run(['ps','aux'],capture_output=True,text=True,check=False)
    yield from filter_results(r.stdout.splitlines(),pattern)
