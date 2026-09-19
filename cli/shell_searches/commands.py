import subprocess
from .. import config
from ..output.filtering import filter_results
def search_loaded_commands(pattern=''):
    if config.CURRENT_SHELL=='zsh': cmd=[config.CURRENT_SHELL,'-ic','print -rl -- '+'$'+'{(k)commands}']
    elif config.CURRENT_SHELL=='bash': cmd=[config.CURRENT_SHELL,'-ic','compgen -c']
    else: return
    r=subprocess.run(cmd,capture_output=True,text=True,check=False)
    yield from filter_results((x.strip() for x in r.stdout.splitlines() if x.strip()),pattern)
