from .arguments import FLAGS
AGGRESSIVE=['environment','path','command','builtins','aliases','functions','manpages','systemd','process','modules','packages','installed','files','not_installed','home','system']
BROAD=['environment','path','command','builtins','aliases','functions','manpages','process','packages','installed','files','not_installed','home']
def action_names(argv):
    # Arguments after -- are search terms, never flags.
    flag_argv = argv[:argv.index('--')] if '--' in argv else argv
    if '--ALL' in flag_argv or '-A' in flag_argv: return AGGRESSIVE[:]
    if '--all' in flag_argv: return BROAD[:]
    out=[]
    for arg in flag_argv:
        if arg in FLAGS and FLAGS[arg] not in out: out.append(FLAGS[arg])
    return out
