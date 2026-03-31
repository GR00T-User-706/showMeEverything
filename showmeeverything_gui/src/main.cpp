#include "searchbackend.h"
#include <QApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    app.setOrganizationName("YourName");
    app.setApplicationName("ShowMeEverything");
    app.setApplicationDisplayName("Show Me Everything Search Tool");

    SearchBackend backend;

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("searchBackend", &backend);
    engine.load(QUrl(QStringLiteral("qrc:/src/qml/main.qml")));

    return app.exec();
}
