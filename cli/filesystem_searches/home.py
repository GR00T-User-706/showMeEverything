import os
from .. import config
from ..output.filtering import filter_results
def search_home_directory(pattern=''):
    home=os.path.expanduser('~')
    for root,dirs,files in os.walk(home):
        dirs[:]=[d for d in dirs if d!='.cache' and not(config.EXCLUDE_DOTFILES and d.startswith('.'))]
        for name in files:
            if config.EXCLUDE_DOTFILES and name.startswith('.'): continue
            yield from filter_results([os.path.join(root,name)],pattern)
