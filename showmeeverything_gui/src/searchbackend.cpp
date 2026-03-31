#include "searchbackend.h"
#include <QDebug>

SearchBackend::SearchBackend(QObject* parent)
    : QObject(parent)
    , m_process(nullptr)
    , m_running(false)
{
    m_allowedArgs = QStringList() << "--all" << "-A"
                                  << "--aliases" << "-a"
                                  << "--builtins" << "-B"
                                  << "--command" << "-c"
                                  << "--files" << "-F"
                                  << "--functions" << "-f"
                                  << "--help" << "-h"
                                  << "--home" << "-H"
                                  << "--installed" << "-i"
                                  << "--manpages" << "--man"
                                  << "--modules" << "-m"
                                  << "--not-installed" << "-n"
                                  << "--process" << "-x"
                                  << "--packages" << "-p" << "--pkg"
                                  << "--path" << "-P"
                                  << "--systemd" << "-s"
                                  << "--system" << "-R";
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
    QUrl url(fileUrlString);
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
