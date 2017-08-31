from qOSM.config import config

doTrace = False

import json
import os

import decorator

backend = config['backend']

if backend == "PyQt5":
        from PyQt5.QtCore import pyqtSignal, QUrl
        from PyQt5.QtGui import QDesktopServices
        from PyQt5.QtNetwork import QNetworkDiskCache
        from PyQt5.QtWebKit import QWebSettings
        from PyQt5.QtWebKitWidgets import QWebPage, QWebView
        from PyQt5.QtWidgets import QApplication

elif backend == "PyQt4":
    from PyQt4.QtCore import pyqtSignal, QUrl
    from PyQt4.QtGui import QDesktopServices, QApplication
    from PyQt4.QtNetwork import QNetworkDiskCache
    from PyQt4.QtWebKit import QWebPage, QWebView, QWebSettings

@decorator.decorator
def trace(function, *args, **k):
    """Decorates a function by tracing the begining and
    end of the function execution, if doTrace global is True"""

    if doTrace: print("> " + function.__name__, args, k)
    result = function(*args, **k)
    if doTrace: print("< " + function.__name__, args, k, "->", result)
    return result


class _LoggedPage(QWebPage):
    @trace
    def javaScriptConsoleMessage(self, msg, line, source):
        print('JS: %s line %d: %s' % (source, line, msg))


class QOSM(QWebView):
    mapMoved = pyqtSignal(float, float)
    mapClicked = pyqtSignal(float, float)
    mapRightClicked = pyqtSignal(float, float)
    mapDoubleClicked = pyqtSignal(float, float)

    markerMoved = pyqtSignal(str, float, float)
    markerClicked = pyqtSignal(str, float, float)
    markerDoubleClicked = pyqtSignal(str, float, float)
    markerRightClicked = pyqtSignal(str, float, float)

    def __init__(self, parent=None, debug=True):
        QWebView.__init__(self, parent=parent)

        cache = QNetworkDiskCache()
        cache.setCacheDirectory("cache")
        self.page().networkAccessManager().setCache(cache)
        self.page().networkAccessManager()

        if debug:
            QWebSettings.globalSettings().setAttribute(
                QWebSettings.DeveloperExtrasEnabled, True
            )

        self.initialized = False

        self.page().mainFrame().addToJavaScriptWindowObject("qtWidget", self)

        basePath = os.path.abspath(os.path.dirname(__file__))
        url = 'file://' + basePath + '/qOSM.html'
        self.load(QUrl(url))

        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

        self.loadFinished.connect(self.onLoadFinished)
        self.linkClicked.connect(QDesktopServices.openUrl)

    def onLoadFinished(self, ok):
        if self.initialized:
            return

        if not ok:
            print("Error initializing OpenStreetMap")

        self.initialized = True
        self.centerAt(0, 0)
        self.setZoom(10)

    def waitUntilReady(self):
        while not self.initialized:
            QApplication.processEvents()

    def runScript(self, script):
        return self.page().mainFrame().evaluateJavaScript(script)

    def centerAt(self, latitude, longitude):
        self.runScript("osm_setCenter({}, {})".format(latitude, longitude))

    def setZoom(self, zoom):
        self.runScript("osm_setZoom({})".format(zoom))

    def center(self):
        center = self.runScript("osm_getCenter()")
        return center['lat'], center['lng']

    def addMarker(self, key, latitude, longitude, **extra):
        return self.runScript("osm_addMarker(key={!r},"
                              "latitude= {}, "
                              "longitude= {}, {});".format(key, latitude, longitude, json.dumps(extra)))

    def moveMarker(self, key, latitude, longitude):
        self.runScript("osm_moveMarker(key={!r},"
                       "latitude= {}, "
                       "longitude= {});".format(key, latitude, longitude))

    def positionMarker(self, key):
        return tuple(self.runScript("osm_posMarker(key={!r});".format(key)))
