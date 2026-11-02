from ..backend import run_backend
def search_package_files_db(pattern=''):
    out=run_backend('zypper','file_database_search',pattern,['rpm','-qal'])
    yield from (x for x in out.splitlines() if pattern.casefold() in x.casefold())
