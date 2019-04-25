def update_members(members):
    other_modules = {
        "QtWebEngineWidgets": ["QWebEngineView"],
        "QtWebChannel": ["QWebChannel"],
    }
    members.update(other_modules)
    members["QtCore"].append("QUrlQuery")
