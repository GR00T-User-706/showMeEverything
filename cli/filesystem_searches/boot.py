import os
from ..output.filtering import filter_results
def search_boot(pattern=''):
    if not os.path.isdir('/boot'): return
    for d,dirs,files in os.walk('/boot'):
        dirs[:]=[x for x in dirs if x!='.cache']
        for n in files: yield from filter_results([os.path.join(d,n)],pattern)
