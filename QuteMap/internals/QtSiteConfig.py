def update_members(members):
    other_modules = {
        "QtWebEngineCore": [
            "QWebEngineUrlScheme",
            "QWebEngineUrlSchemeHandler",
            "QWebEngineUrlRequestJob",
        ],
        "QtWebEngineWidgets": [
            "QWebEngineView",
            "QWebEnginePage",
            "QWebEngineScript",
            "QWebEngineProfile",
        ],
        "QtWebChannel": ["QWebChannel"],
        "QtPositioning": ["QGeoCoordinate"],
    }
    members.update(other_modules)
    members["QtCore"].extend(
        [
            "QUrlQuery",
            "QtInfoMsg",
            "QtDebugMsg",
            "QtWarningMsg",
            "QtCriticalMsg",
            "QtFatalMsg",
        ]
    )
