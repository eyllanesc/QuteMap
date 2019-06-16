def update_members(members):
    other_modules = {
        "QtWebEngineWidgets": [
            "QWebEngineView",
            "QWebEnginePage",
            "QWebEngineScript",
        ],
        "QtWebChannel": ["QWebChannel"],
        "QtPositioning": ["QGeoCoordinate"],
    }
    members.update(other_modules)
    members["QtCore"].append("QUrlQuery")
