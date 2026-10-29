
#!/usr/bin/env bash
# SME_SIGNATURE=gr00t-user-706
set -e

echo "Removing Show Me Everything..."

# Legacy CLI launchers
rm -f /usr/local/bin/showMeEverything
rm -f /usr/local/bin/smecli

# Legacy CLI implementation
rm -rf /usr/local/lib/showMeEverything

# Legacy GUI launchers
rm -f /usr/local/bin/showmeeverything_tk
rm -f /usr/local/bin/showmeeverything_qml
rm -f /usr/local/bin/smegpy
rm -f /usr/local/bin/showmeeverything_gui
rm -f /usr/local/bin/smegui

# Legacy Python cache
rm -f /usr/local/bin/__pycache__/showmeeverything_tk.cpython-314.pyc

# Legacy desktop entries and icon
rm -f /usr/local/share/applications/com.github.gr00t-user-706.showmeeverything-*.desktop
rm -f /usr/local/share/icons/showMeEverything.png

# Refresh desktop database when available
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/local/share/applications
fi

echo "Uninstall complete."

