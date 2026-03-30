#!/bin/bash
# Install the CLI
sudo cp showMeEverything /usr/local/bin/search
sudo chmod +x /usr/local/bin/search

# Build and install the GUI
cd showmeeverything_gui
qmake
make
sudo cp showmeeverything_gui /usr/local/bin/search-gui
cd ..

# (Optional) Install the Python fallback if you want
# sudo cp showmeeverything_tk.py /usr/local/bin/search-gui-fallback

# Install desktop files
sudo cp *.desktop /usr/local/share/applications/
sudo update-desktop-database

echo "Installation complete."
