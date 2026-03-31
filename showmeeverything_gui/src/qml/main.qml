import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import Qt.labs.platform 1.1

ApplicationWindow {
    id: mainWindow
    title: "Show Me Everything - System Search Tool"
    width: 1000
    height: 700
    visible: true

    // Colors
    property color backgroundColor: "#2a2e32"
    property color foregroundColor: "#eff0f1"
    property color accentColor: "#3daee9"
    property color buttonColor: "#31363b"
    property color inputColor: "#31363b"

    // Friendly flag mapping
    property var flagMap: ({
        "all": "--all",
        "aliases": "--aliases",
        "builtins": "--builtins",
        "command": "--command",
        "files": "--files",
        "functions": "--functions",
        "help": "--help",
        "home": "--home",
        "installed": "--installed",
        "manpages": "--manpages",
        "modules": "--modules",
        "process": "--process",
        "packages": "--packages",
        "path": "--path",
        "systemd": "--systemd",
        "system": "--system"
    })

    // Model for output lines
    ListModel {
        id: outputModel
    }

    // Connect to backend signals (new syntax)
    Connections {
        target: searchBackend
        function onOutputLine(line) {
            outputModel.append({"modelData": line})
            outputListView.positionViewAtEnd() // auto-sctoll
        }
        function onOutputCleared() { outputModel.clear() }
    }

    // Helper functions
    function convertToFlag(userInput) {
        var trimmed = userInput.trim().toLowerCase()
        if (flagMap[trimmed]) return flagMap[trimmed]
            return userInput
    }

    function performSearch() {
        var rawInput = argumentInput.text.trim()
        if (rawInput === "") {
            outputModel.append({"modelData": "Please enter a valid argument"})
            outputModel.append({"modelData": "Examples:"})
            outputModel.append({"modelData": "  --all firefox"})
            outputModel.append({"modelData": "  --packages vim"})
            outputModel.append({"modelData": "  --help"})
            return
        }
        var convertedInput = convertToFlag(rawInput)
        argumentInput.text = convertedInput
        searchBackend.runSearch(convertedInput)
    }

    function clearSearch() {
        searchBackend.clearOutput()
        argumentInput.clear()
        argumentInput.forceActiveFocus()
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
                background: Rectangle {
                    color: inputColor
                    radius: 3
                }
                onAccepted: performSearch()
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
                model: ["all", "packages", "installed", "files", "system", "home"]
                Button {
                    text: modelData
                    flat: true
                    onClicked: {
                        argumentInput.text = flagMap[modelData]
                        performSearch()
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
                ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
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
            Item { Layout.fillWidth: true }

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
                        searchBackend.stopSearch()
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
        fileMode: FileDialog.SaveFile   // This makes it a "Save As" dialog
        onAccepted: {
            searchBackend.saveToFile(fileDialog.fileUrl.toString())
        }
    }
}
