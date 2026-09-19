import subprocess
from .. import config
from ..output.filtering import filter_results
def search_aliases(pattern=''):
    r=subprocess.run([config.CURRENT_SHELL,'-ic','alias'],capture_output=True,text=True,check=False)
    yield from filter_results((x.strip() for x in r.stdout.splitlines() if x.strip()),pattern)
