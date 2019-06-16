import os

from PyQt5 import QtWidgets, QtWebEngineWidgets, QtPositioning

# from PySide2 import QtWidgets, QtWebEngineWidgets, QtPositioning

os.environ["QT_PREFERRED_BINDING"] = "PyQt5"  # "PySide2"


from QuteMap import MapPage


def print_coordinate(coordinate):
    print(
        coordinate.toString(QtPositioning.QGeoCoordinate.DegreesMinutesSeconds)
    )


if __name__ == "__main__":
    import sys

    from dotenv import load_dotenv

    load_dotenv(verbose=True)

    app = QtWidgets.QApplication(sys.argv)
    w = QtWebEngineWidgets.QWebEngineView()
    page = MapPage("google", parameters={"API_KEY": os.getenv("GOOGLE_API_KEY")})
    w.setPage(page)
    page.handler.centerChanged.connect(print_coordinate)
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
