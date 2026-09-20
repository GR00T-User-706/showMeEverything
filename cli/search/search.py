from ..output.sorting import sort_results
from .actions import action_names
from ..shell_searches import path,commands,builtins,aliases,functions,manpages,systemd,processes,kernel_modules
from ..filesystem_searches import home,system,usr,etc,sys,var,opt,boot,lib,bin,sbin
from ..package_manager_searches import repository,installed,not_installed,files
from ..environment_searches import search_environment
A={'environment':search_environment,'path':path.search_path,'command':commands.search_loaded_commands,'builtins':builtins.search_shell_builtins,'aliases':aliases.search_aliases,'functions':functions.search_shell_functions,'manpages':manpages.search_manpages,'systemd':systemd.search_systemd_units,'process':processes.search_running_processes,'modules':kernel_modules.loaded_kernel_modules,'packages':repository.search_package_repo,'installed':installed.search_installed_packages,'files':files.search_package_files_db,'not_installed':not_installed.search_packages_not_installed,'home':home.search_home_directory,'system':system.search_system_dirs,'usr':usr.search_usr,'etc':etc.search_etc,'sys':sys.search_sys,'var':var.search_var,'opt':opt.search_opt,'boot':boot.search_boot,'lib':lib.search_lib,'bin':bin.search_bin,'sbin':sbin.search_sbin}
def execute(actions,pattern):
    for name in actions: yield name,sort_results(A[name](pattern))
