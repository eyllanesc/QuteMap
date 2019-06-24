import os

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtPositioning

# from PySide2 import QtWidgets, QtWebEngineWidgets, QtPositioning

os.environ["QT_PREFERRED_BINDING"] = "PyQt5"  # "PySide2"

import QuteMap


if __name__ == "__main__":
    import sys

    from dotenv import load_dotenv

    load_dotenv(verbose=True)

    QuteMap.init(log_enabled=True)

    app = QtWidgets.QApplication(sys.argv)

    log_enabled = False
    view1 = QtWebEngineWidgets.QWebEngineView()
    page1 = QuteMap.MapPage(
        "google1",
        "googlemaps",
        parameters={"API_KEY": os.getenv("GOOGLE_API_KEY")},
        log_enabled=log_enabled,
    )
    view1.setPage(page1)

    view2 = QtWebEngineWidgets.QWebEngineView()
    page2 = QuteMap.MapPage("osm1", "osm")
    view2.setPage(page2)

    w = QtWidgets.QMainWindow()
    splitter = QtWidgets.QSplitter()
    splitter.addWidget(view1)
    splitter.addWidget(view2)
    w.setCentralWidget(splitter)
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())