from ..backend import run_backend
def search_package_files_db(pattern=''):
    out=run_backend('pacman','file_database_search',pattern,['pacman','-F',pattern])
    yield from out.splitlines()
