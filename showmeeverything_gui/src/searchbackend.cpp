#include "searchbackend.h"
#include <QDebug>
#include <QUrl>
#include <QTimer>
// SME_SIGNATURE=gr00t-user-706
SearchBackend::SearchBackend(QObject* parent)
    : QObject(parent)
    , m_process(nullptr)
    , m_running(false)
{
    m_allowedArgs = QStringList()
    << "--ALL" << "-A" << "ALL" << "A"
    << "--all" << "all"
    << "--pipe" << "pipe"
    << "--aliases" << "-a" << "aliases" << "a"
    << "--builtins" << "-b" << "builtins" << "b"
    << "--command" << "-c" << "command" << "c"
    << "--files" << "-F" << "files" << "F"
    << "--functions" << "-f" << "functions" << "f"

    << "--help" << "-h" << "help" << "h"

    << "--home" << "-H" << "home" << "H"
    << "--installed" << "-i" << "installed" << "i"

    << "--manpages" << "--man" << "-M" << "manpages" << "man" << "M"

    << "--modules" << "-m" << "modules" << "m"

    << "--process" << "-x" << "process" << "x"

    << "--packages" << "-p" << "--pkg" << "packages" << "pkg" << "p"

    << "--path" << "-P" << "path" << "P"

    << "--systemd" << "-s" << "systemd" << "s"

    << "--system" << "-R" << "system" << "R"

    << "--excludeDotFiles" << "--nodot" << "excludeDotFiles" << "nodot"

    // refined system search flags
    << "--usr" << "-U" << "usr" << "U"
    << "--etc" << "-E" << "etc" << "E"
    << "--var" << "-V" << "var" << "V"
    << "--opt" << "-O" << "opt" << "O"
    << "--boot" << "-B" << "boot" << "B"
    << "--lib" << "-L" << "lib" << "L"
    << "--bin" << "bin"
    << "--sbin" << "sbin";
}
void SearchBackend::runSearch(const QString& args)
{
    clearOutput();
    QStringList argList = args.split(' ', Qt::KeepEmptyParts);

    // validate that the first argument is an allowed flag
    if (!argList.isEmpty() && !m_allowedArgs.contains(argList.first())) {
        appendOutput("Error: Invalid argument. Use --help for available flags\n");
        appendOutput("You entered: " + argList.first() + "\n");
        return;
    }

    if (m_process && m_running) {
        m_process->terminate();
        m_process->waitForFinished(1000);
        delete m_process;
    }

    m_process = new QProcess(this);
    m_process->setProgram("/usr/local/bin/showMeEverything");
    m_process->setArguments(argList);

    connect(m_process, &QProcess::readyReadStandardOutput, this,
        &SearchBackend::onReadyReadStandardOutput);
    connect(m_process,
        QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
        &SearchBackend::onProcessFinished);

    setRunning(true);
    m_process->start();
}

void SearchBackend::runHelp() { runSearch("--help"); }

void SearchBackend::clearOutput()
{
    m_output.clear();
    emit outputChanged();
    emit outputCleared();
}

void SearchBackend::onProcessFinished(int exitCode,
    QProcess::ExitStatus exitStatus)
{
    setRunning(false);
    if (exitStatus == QProcess::CrashExit) {
        appendOutput("\n\n--- Process crashed ---\n");
    } else if (exitCode != 0) {
        appendOutput("\n\n--- Process finished with exit code: " + QString::number(exitCode) + " ---\n");
    }
}
void SearchBackend::onReadyReadStandardOutput()
{
    if (m_process) {
        QString data = QString::fromUtf8(m_process->readAllStandardOutput());
        // Split into lines and emit each line
        QStringList lines = data.split('\n', Qt::KeepEmptyParts);
        for (const QString& line : lines) {
            emit outputLine(line);
        }
        // Also accumulate full output for save/copy
        m_output += data;
        emit outputChanged();
    }
}
void SearchBackend::appendOutput(const QString& text)
{
    m_output += text;
    emit outputChanged();
    emit outputLine(text);
}

void SearchBackend::setRunning(bool running)
{
    if (m_running != running) {
        m_running = running;
        emit runningChanged();
    }
}
void SearchBackend::saveToFile(const QString& fileUrlString)
{
    QUrl url = QUrl::fromUserInput(fileUrlString);
    QString localPath = url.toLocalFile();
    if (localPath.isEmpty()) {
        appendOutput("Error: Invalid file path.\n");
        return;
    }

    QFile file(localPath);
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QTextStream out(&file);
        out << m_output;
        file.close();
        appendOutput("Saved to " + localPath + "\n");
    } else {
        appendOutput("Error: Could not save to " + localPath + "\nReason: " + file.errorString() + "\n");
    }
}

QString SearchBackend::getFullOutput() const { return m_output; }
void SearchBackend::copyToClipboard()
{
    QClipboard* clipboard = QGuiApplication::clipboard();
    clipboard->setText(m_output);
    appendOutput("--- Copied to clipboard ---\n");
}
void SearchBackend::stopSearch() {
        if (m_process && m_running){
            m_process->terminate();  //SIGTERM
            // If SIGTERM doesn't work after 2 seconds, kill it
            QTimer::singleShot(2000, this, [this]() {
                if (m_running && m_process)
                    m_process->kill();
            });
            appendOutput("\n--- Search interrupted by user ---\n");
        }
}
