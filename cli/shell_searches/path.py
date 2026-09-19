import os
from ..output.filtering import matches
def search_path(pattern=''):
    for d in os.environ.get('PATH','').split(os.pathsep):
        if not os.path.isdir(d): continue
        for root,dirs,files in os.walk(d):
            dirs[:]=[x for x in dirs if x!='.cache']
            for name in files:
                p=os.path.join(root,name)
                if matches(p,pattern): yield p
