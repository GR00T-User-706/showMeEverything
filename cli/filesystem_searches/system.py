import os
from ..output.filtering import filter_results

ROOTS=(
    '/bin',
    '/boot',
    '/dev',
    '/etc',
    '/home',
    '/lib',
    '/lib64',
    '/mnt',
    '/opt',
    '/proc',
    '/run',
    '/sbin',
    '/srv',
    '/sys',
    '/tmp',
    '/usr',
    '/var',
)

def search_system_dirs(pattern=''):
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for directory, dirs, files in os.walk(root):
            for name in files:
                yield from filter_results(
                    [os.path.join(directory, name)],
                    pattern,
                )
