"""Detect every available supported package manager, not just the first."""
import shutil

def get_package_managers():
    managers = []
    if shutil.which("pacman"):
        managers.append("pacman")
    if shutil.which("apt-cache") and shutil.which("dpkg-query"):
        managers.append("apt")
    if shutil.which("dnf"):
        managers.append("dnf")
    if shutil.which("zypper") and shutil.which("rpm"):
        managers.append("zypper")
    if shutil.which("apk"):
        managers.append("apk")
    return managers

def get_package_manager():
    """Compatibility alias; now returns the complete list."""
    return get_package_managers()
