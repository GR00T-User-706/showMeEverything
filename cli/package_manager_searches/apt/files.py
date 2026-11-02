from ..backend import run_backend
def search_package_files_db(pattern=''):
    out=run_backend('apt','file_ownership_search',pattern,['dpkg','-S','*'+pattern+'*'])
    yield from out.splitlines()
