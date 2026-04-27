#!/usr/bin/env bash
# SME_SIGNATURE=gr00t-user-706
set -e

echo "Removing Show Me Everything..."

rm -f /usr/local/bin/showMeEverything
rm -f /usr/local/bin/smecli

rm -f /usr/local/bin/showmeeverything_tk
rm -f /usr/local/bin/smegpy

rm -f /usr/local/bin/showmeeverything_gui
rm -f /usr/local/bin/smegui

rm -f /usr/local/share/applications/com.github.gr00t-user-706.showmeeverything-*.desktop
rm -f /usr/local/share/icons/showMeEverything.png

update-desktop-database

echo "Uninstall complete."
