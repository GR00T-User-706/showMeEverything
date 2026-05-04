import Qt.labs.platform 1.1
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15

ApplicationWindow {
    id: mainWindow

    // Colors
    property color backgroundColor: "#1b1e21"
    property color foregroundColor: "#eff0f1"
    property color accentColor: "#3daee9"
    property color buttonColor: "#31363b"
    property color inputColor: "#7a7a7a"
    // Friendly flag mapping
    property var flagMap: ({
        "excludeDotFiles": "--excludeDotFiles",
        "nodot": "--nodot",
        "ALL": "--ALL",
        "A": "--ALL",
        "all": "--all",
        "aliases": "--aliases",
        "a": "--aliases",
        "builtins": "--builtins",
        "b": "--builtins",
        "command": "--command",
        "c": "--command",
        "files": "--files",
        "F": "--files",
        "functions": "--functions",
        "f": "--functions",
        "help": "--help",
        "h": "--help",
        "home": "--home",
        "H": "--home",
        "installed": "--installed",
        "i": "--installed",
        "manpages": "--manpages",
        "man": "--manpages",
        "M": "--manpages",
        "modules": "--modules",
        "m": "--modules",
        "process": "--process",
        "x": "--process",
        "packages": "--packages",
        "pkg": "--packages",
        "p": "--packages",
        "path": "--path",
        "P": "--path",
        "systemd": "--systemd",
        "s": "--systemd",
        "system": "--system",
        "R": "--system",
        // refined system dirs
        "usr": "--usr",
        "U": "--usr",
        "etc": "--etc",
        "E": "--etc",
        "var": "--var",
        "V": "--var",
        "opt": "--opt",
        "O": "--opt",
        "boot": "--boot",
        "B": "--boot",
        "lib": "--lib",
        "L": "--lib",
        "bin": "--bin",
        "sbin": "--sbin"
    })

    // Helper functions
    function convertToFlag(userInput) {
        var trimmed = userInput.trim().toLowerCase();
        if (flagMap[trimmed])
            return flagMap[trimmed];

        return userInput;
    }

    function performSearch() {
        var rawInput = argumentInput.text.trim();
        if (rawInput === "") {
            outputModel.append({
                "modelData": "Please enter a valid argument"
            });
            outputModel.append({
                "modelData": "Examples:"
            });
            outputModel.append({
                "modelData": "  --all firefox"
            });
            outputModel.append({
                "modelData": "  --packages vim"
            });
            outputModel.append({
                "modelData": "  --help"
            });
            return ;
        }
        var convertedInput = convertToFlag(rawInput);
        argumentInput.text = convertedInput;
        searchBackend.runSearch(convertedInput);
    }

    function clearSearch() {
        searchBackend.clearOutput();
        argumentInput.clear();
        argumentInput.forceActiveFocus();
    }

    title: "Show Me Everything - System Search Tool"
    width: 1000
    height: 700
    visible: true

    // Model for output lines
    ListModel {
        id: outputModel
    }

    // Connect to backend signals (new syntax)
    Connections {
        function onOutputLine(line) {
            outputModel.append({
                "modelData": line
            });
            outputListView.positionViewAtEnd(); // auto-scroll
        }

        function onOutputCleared() {
            outputModel.clear();
        }

        target: searchBackend
    }

    // Main layout
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 8

        // Header
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 80
            color: accentColor
            radius: 5

            Text {
                anchors.centerIn: parent
                text: "Show Me Everything\nPowerful System Search Tool"
                font.pointSize: 14
                font.bold: true
                color: "white"
                horizontalAlignment: Text.AlignHCenter
            }

        }

        // Input row
        RowLayout {
            Layout.fillWidth: true

            TextField {
                id: argumentInput

                Layout.fillWidth: true
                placeholderText: "Enter flag (e.g., --all, --packages, help) and optional search term..."
                onAccepted: performSearch()

                background: Rectangle {
                    color: inputColor
                    radius: 3
                }

            }

            Button {
                text: "Search"
                onClicked: performSearch()

                background: Rectangle {
                    color: accentColor
                    radius: 3
                }

            }

            Button {
                text: "Help"
                onClicked: searchBackend.runHelp()
            }

            Button {
                text: "Clear"
                onClicked: clearSearch()
            }

        }

        // Quick flags row
        Flow {
            Layout.fillWidth: true
            spacing: 5

            Repeater {
                model: ["all", "path", "installed", "system", "home"]

                Button {
                    text: modelData
                    flat: true
                    onClicked: {
                        argumentInput.text = flagMap[modelData];
                        performSearch();
                    }
                }

            }

        }

        // Output area (ListView for performance)
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            border.color: accentColor
            border.width: 1
            color: backgroundColor
            clip: true

            ListView {
                id: outputListView

                anchors.fill: parent
                anchors.margins: 2
                model: outputModel

                delegate: Text {
                    text: modelData
                    font.family: "Monospace"
                    font.pointSize: 10
                    wrapMode: Text.Wrap
                    width: ListView.view.width
                    color: foregroundColor
                }

                ScrollBar.vertical: ScrollBar {
                    policy: ScrollBar.AsNeeded
                }

            }

        }

        // Status bar and buttons
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 30
            spacing: 8

            Text {
                text: searchBackend.running ? "Searching..." : "Ready"
                font.pointSize: 9
                color: foregroundColor
            }

            Item {
                Layout.fillWidth: true
            }

            Button {
                text: "Save to File"
                onClicked: fileDialog.open()
            }

            Button {
                text: "Copy to Clipboard"
                onClicked: searchBackend.copyToClipboard()
            }

            Button {
                text: "Scroll to Bottom"
                onClicked: outputListView.positionViewAtEnd()
            }

            Button {
                text: "Stop"
                enabled: searchBackend.running
                onClicked: searchBackend.stopSearch()
            }

            Shortcut {
                sequence: StandardKey.Cancel
                onActivated: {
                    if (searchBackend.running)
                        searchBackend.stopSearch();

                }
            }

            Text {
                text: "Lines: " + outputModel.count
                font.pointSize: 9
                color: foregroundColor
            }

        }

    }

    // File dialog for saving output (uses StandardPaths for home)
    FileDialog {
        id: fileDialog

        title: "Save Output"
        folder: StandardPaths.writableLocation(StandardPaths.HomeLocation)
        fileMode: FileDialog.SaveFile // This makes it a "Save As" dialog
        onAccepted: {
            searchBackend.saveToFile(fileDialog.fileUrl.toString());
        }
    }

}
