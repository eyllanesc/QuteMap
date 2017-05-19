import json
import os

from PyQt5 import QtCore, QtGui, QtWebKit, QtNetwork, QtWebKitWidgets, QtWidgets


class _LoggedPage(QtWebKitWidgets.QWebPage):
    def javaScriptConsoleMessage(self, msg, line, source):
        print('JS: %s line %d: %s' % (source, line, msg))


class QOSM(QtWebKitWidgets.QWebView):
    mapMoved = QtCore.pyqtSignal(float, float)
    mapClicked = QtCore.pyqtSignal(float, float)
    mapRightClicked = QtCore.pyqtSignal(float, float)
    mapDoubleClicked = QtCore.pyqtSignal(float, float)

    markerMoved = QtCore.pyqtSignal(str, float, float)
    markerClicked = QtCore.pyqtSignal(str, float, float)
    markerDoubleClicked = QtCore.pyqtSignal(str, float, float)
    markerRightClicked = QtCore.pyqtSignal(str, float, float)

    def __init__(self, parent=None, debug=True):
        QtWebKitWidgets.QWebView.__init__(self, parent=parent)

        cache = QtNetwork.QNetworkDiskCache()
        cache.setCacheDirectory("cache")
        self.page().networkAccessManager().setCache(cache)
        self.page().networkAccessManager()

        if debug:
            QtWebKit.QWebSettings.globalSettings().setAttribute(
                QtWebKit.QWebSettings.DeveloperExtrasEnabled, True
            )
        self.setPage(_LoggedPage())

        self.initialized = False

        self.page().mainFrame().addToJavaScriptWindowObject("qtWidget", self)

        basePath = os.path.abspath(os.path.dirname(__file__))
        url = 'file://' + basePath + '/qOSM.html'
        self.load(QtCore.QUrl(url))

        self.page().setLinkDelegationPolicy(QtWebKitWidgets.QWebPage.DelegateAllLinks)

        self.loadFinished.connect(self.onLoadFinished)
        self.linkClicked.connect(QtGui.QDesktopServices.openUrl)

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
            QtWidgets.QApplication.processEvents()

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
