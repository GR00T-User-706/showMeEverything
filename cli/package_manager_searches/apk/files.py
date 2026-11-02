from ..backend import run_backend
def search_package_files_db(pattern=''):
    out=run_backend('apk','file_database_search',pattern,['apk','info','-L'])
    yield from (x for x in out.splitlines() if pattern.casefold() in x.casefold())
