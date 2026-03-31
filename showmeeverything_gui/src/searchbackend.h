#ifndef SEARCHBACKEND_H
#define SEARCHBACKEND_H

#include <QClipboard> // Add this
#include <QFile>
#include <QGuiApplication> // Add this
#include <QObject>
#include <QProcess>
#include <QStringList>
#include <QTextStream>

class SearchBackend : public QObject {
    Q_OBJECT
    Q_PROPERTY(QString output READ output NOTIFY outputChanged)
    Q_PROPERTY(bool running READ running NOTIFY runningChanged)

public:
    explicit SearchBackend(QObject* parent = nullptr);

    QString output() const { return m_output; }
    bool running() const { return m_running; }

public slots:
    void runSearch(const QString& args);
    void runHelp();
    void stopSearch();
    void clearOutput();
    void saveToFile(const QString& filename);
    QString getFullOutput() const;
    void copyToClipboard(); // Add this

signals:
    void outputChanged();
    void runningChanged();
    void outputLine(const QString& line);
    void outputCleared();

private slots:
    void onProcessFinished(int exitCode, QProcess::ExitStatus exitStatus);
    void onReadyReadStandardOutput();

private:
    void appendOutput(const QString& text);
    void setRunning(bool running);

    QProcess* m_process;
    QString m_output;
    bool m_running;
    QStringList m_allowedArgs; // For sandboxing
};

#endif // SEARCHBACKEND_H
