QT += quick widgets core

SOURCES = src/main.cpp \
          src/searchbackend.cpp

HEADERS = src/searchbackend.h

RESOURCES = resources.qrc

# Optional: Add deployment settings
target.path = /usr/local/bin
INSTALLS += target
