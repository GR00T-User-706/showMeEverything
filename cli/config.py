import os, socket
from datetime import datetime
SME_SIGNATURE='gr00t-user-706'
SME_VERSION='v3.0.0'
PIPE_MODE=False
COLOR_MODE=True
REGEX=True
SORT_MODE=False
EXCLUDE_DOTFILES=False
CURRENT_SHELL=os.path.basename(os.environ.get('SHELL','')) or 'sh'
def terminal_info():
    return '{} {} {} {}'.format(datetime.now().strftime('%c'),os.environ.get('SHELL',''),os.environ.get('USER',''),socket.gethostname())
