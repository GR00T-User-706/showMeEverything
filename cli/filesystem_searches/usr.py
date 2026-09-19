import os
from ..output.filtering import filter_results
def search_usr(pattern=''):
    if not os.path.isdir('/usr'): return
    for d,dirs,files in os.walk('/usr'):
        dirs[:]=[x for x in dirs if x!='.cache']
        for n in files: yield from filter_results([os.path.join(d,n)],pattern)
