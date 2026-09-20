from .arguments import FLAGS
AGGRESSIVE=['environment','path','command','builtins','aliases','functions','manpages','systemd','process','modules','packages','installed','files','not_installed','home','system']
BROAD=['environment','path','command','builtins','aliases','functions','manpages','process','packages','installed','files','not_installed','home']
def action_names(argv):
    if '--ALL' in argv or '-A' in argv: return AGGRESSIVE[:]
    if '--all' in argv: return BROAD[:]
    out=[]
    for arg in argv:
        if arg in FLAGS and FLAGS[arg] not in out: out.append(FLAGS[arg])
    return out
