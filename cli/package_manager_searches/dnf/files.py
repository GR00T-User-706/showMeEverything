from ..backend import run_backend
def search_package_files_db(pattern=''):
    out=run_backend('dnf','file_database_search',pattern,['repoquery','-f','*'+pattern+'*'])
    yield from out.splitlines()
