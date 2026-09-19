import os
from ..output.filtering import filter_results
ROOTS=('/usr','/etc','/sys','/dev','/var','/opt','/boot','/lib','/bin','/sbin')
def search_system_dirs(pattern=''):
    for root in ROOTS:
        if not os.path.isdir(root): continue
        for d,dirs,files in os.walk(root):
            for name in files: yield from filter_results([os.path.join(d,name)],pattern)
