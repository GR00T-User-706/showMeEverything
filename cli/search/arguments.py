import argparse
FLAGS={'--ALL':'all_aggressive','-A':'all_aggressive','--all':'all','--aliases':'aliases','-a':'aliases','--bin':'bin','--boot':'boot','-B':'boot','--builtins':'builtins','-b':'builtins','--command':'command','-c':'command','--etc':'etc','-E':'etc','--files':'files','-F':'files','--functions':'functions','-f':'functions','--home':'home','-H':'home','--installed':'installed','-i':'installed','--lib':'lib','-L':'lib','--manpages':'manpages','--man':'manpages','-M':'manpages','--modules':'modules','-m':'modules','--not-installed':'not_installed','-n':'not_installed','--process':'process','-x':'process','--packages':'packages','-p':'packages','--pkg':'packages','--path':'path','-P':'path','--sbin':'sbin','--systemd':'systemd','-s':'systemd','--system':'system','-R':'system','--usr':'usr','-U':'usr','--var':'var','-V':'var','--opt':'opt','-O':'opt'}
def parse_arguments(argv):
    p=argparse.ArgumentParser(add_help=False,allow_abbrev=False)
    p.add_argument('-h','--help',action='store_true'); p.add_argument('-v','--version',action='store_true')
    p.add_argument('--less',action='store_true'); p.add_argument('--sort',action='store_true'); p.add_argument('--pipe',action='store_true'); p.add_argument('--glob',action='store_true')
    p.add_argument('--excludeDotFiles','--nodot',dest='exclude_dotfiles',action='store_true')
    for flag,dest in FLAGS.items(): p.add_argument(flag,dest=dest,action='store_true')
    p.add_argument('search_terms',nargs=argparse.REMAINDER)
    return p.parse_known_args(argv)
