from __future__ import print_function

import os
from Qt import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel, QtNetwork, QtCompat

import jinja2
import json

script_path = os.path.dirname(os.path.abspath(__file__))
environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
BASE_FILE = "base.html"
JS_GMAP = "qgmap.js"


class GeoCoder(QtNetwork.QNetworkAccessManager):
    class NotFoundError(Exception):
        pass

    def geocode(self, location, api_key):
        url = QtCore.QUrl("https://maps.googleapis.com/maps/api/geocode/xml")

        query = QtCore.QUrlQuery()
        query.addQueryItem("key", api_key)
        query.addQueryItem("address", location)
        url.setQuery(query)
        request = QtNetwork.QNetworkRequest(url)
        reply = self.get(request)
        loop = QtCore.QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
        reply.deleteLater()
        self.deleteLater()
        return self._parseResult(reply)

    def _parseResult(self, reply):
        xml = reply.readAll()
        reader = QtCore.QXmlStreamReader(xml)
        while not reader.atEnd():
            reader.readNext()
            if reader.name() != "geometry":
                continue
            reader.readNextStartElement()
            if reader.name() != "location":
                continue
            reader.readNextStartElement()
            if reader.name() != "lat":
                continue
            latitude = float(reader.readElementText())
            reader.readNextStartElement()
            if reader.name() != "lng":
                continue
            longitude = float(reader.readElementText())
            return latitude, longitude
        raise GeoCoder.NotFoundError


class MapView(QtWebEngineWidgets.QWebEngineView):

    mapMoved = QtCore.Signal(float, float)
    mapClicked = QtCore.Signal(float, float)
    mapRightClicked = QtCore.Signal(float, float)
    mapDoubleClicked = QtCore.Signal(float, float)

    markerMoved = QtCore.Signal(str, float, float)
    markerClicked = QtCore.Signal(str, float, float)
    markerDoubleClicked = QtCore.Signal(str, float, float)
    markerRightClicked = QtCore.Signal(str, float, float)

    def __init__(self, source="googlemap", api_key=None, parent=None):
        super(MapView, self).__init__(parent)
        channel = QtWebChannel.QWebChannel(self)
        self.page().setWebChannel(channel)
        channel.registerObject("qGoogleMap", self)
        js = environment.get_template(JS_GMAP).render()
        self.page().runJavaScript(js)
        self._api_key = api_key

        if source == "googlemap":
            html = environment.get_template(BASE_FILE).render(
                {"_": lambda x: x, "API_KEY": self._api_key}
            )
            self.setHtml(html)
        self.loadFinished.connect(self.on_loadFinished)
        self.initialized = False
        self._manager = QtNetwork.QNetworkAccessManager(self)

    @QtCore.Slot()
    def on_loadFinished(self):
        self.initialized = True

    def waitUntilReady(self):
        if not self.initialized:
            loop = QtCore.QEventLoop()
            self.loadFinished.connect(loop.quit)
            loop.exec_()

    def geocode(self, location):
        return GeoCoder(self).geocode(location, self._api_key)

    def centerAtAddress(self, location):
        try:
            latitude, longitude = self.geocode(location)
        except GeoCoder.NotFoundError:
            print("Not found {}".format(location))
            return None, None
        self.centerAt(latitude, longitude)
        return latitude, longitude

    def addMarkerAtAddress(self, location, **extra):
        if "title" not in extra:
            extra["title"] = location
        try:
            latitude, longitude = self.geocode(location)
        except GeoCoder.NotFoundError:
            return None
        return self.addMarker(location, latitude, longitude, **extra)

    @QtCore.Slot(float, float)
    def mapIsMoved(self, lat, lng):
        self.mapMoved.emit(lat, lng)

    @QtCore.Slot(float, float)
    def mapIsClicked(self, lat, lng):
        self.mapClicked.emit(lat, lng)

    @QtCore.Slot(float, float)
    def mapIsRightClicked(self, lat, lng):
        self.mapRightClicked.emit(lat, lng)

    @QtCore.Slot(float, float)
    def mapIsDoubleClicked(self, lat, lng):
        self.mapDoubleClicked.emit(lat, lng)

    # markers
    @QtCore.Slot(str, float, float)
    def markerIsMoved(self, key, lat, lng):
        self.markerMoved.emit(key, lat, lng)

    @QtCore.Slot(str, float, float)
    def markerIsClicked(self, key, lat, lng):
        self.markerClicked.emit(key, lat, lng)

    @QtCore.Slot(str, float, float)
    def markerIsRightClicked(self, key, lat, lng):
        self.markerRightClicked.emit(key, lat, lng)

    @QtCore.Slot(str, float, float)
    def markerIsDoubleClicked(self, key, lat, lng):
        self.markerDoubleClicked.emit(key, lat, lng)

    def runScript(self, script, callback=None):
        if callback is None:
            self.page().runJavaScript(script)
        else:
            self.page().runJavaScript(script, callback)

    def centerAt(self, latitude, longitude):
        self.runScript("gmap_setCenter({},{})".format(latitude, longitude))

    def center(self):
        self._center = {}
        loop = QtCore.QEventLoop()

        def callback(*args):
            self._center = tuple(args[0])
            loop.quit()

        self.runScript("gmap_getCenter()", callback)
        loop.exec_()
        return self._center

    def setZoom(self, zoom):
        self.runScript("gmap_setZoom({})".format(zoom))

    def addMarker(self, key, latitude, longitude, **extra):
        return self.runScript(
            "gmap_addMarker("
            "key={!r}, "
            "latitude={}, "
            "longitude={}, "
            "{}"
            "); ".format(key, latitude, longitude, json.dumps(extra))
        )

    def moveMarker(self, key, latitude, longitude):
        return self.runScript(
            "gmap_moveMarker({!r}, {}, {});".format(key, latitude, longitude)
        )

    def setMarkerOptions(self, keys, **extra):
        return self.runScript(
            "gmap_changeMarker("
            "key={!r}, "
            "{}"
            "); ".format(keys, json.dumps(extra))
        )

    def deleteMarker(self, key):
        return self.runScript(
            "gmap_deleteMarker(" "key={!r} " "); ".format(key)
        )


if __name__ == "__main__":
    import sys

    API_KEY = ""
    app = QtWidgets.QApplication(sys.argv)
    w = MapView(api_key=API_KEY)
    w.resize(640, 480)
    w.show()
    w.waitUntilReady()
    w.setZoom(14)
    lat, lng = w.centerAtAddress("Lima Peru")
    if lat is None and lng is None:
        lat, lng = -12.0463731, -77.042754
        w.centerAt(lat, lng)

    w.addMarker(
        "MyDragableMark",
        lat,
        lng,
        **dict(
            icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
            draggable=True,
            title="Move me!",
        )
    )

    for place in ["Plaza Ramon Castilla", "Plaza San Martin"]:
        w.addMarkerAtAddress(
            place,
            icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
        )
    w.mapMoved.connect(print)
    w.mapClicked.connect(print)
    w.mapRightClicked.connect(print)
    w.mapDoubleClicked.connect(print)
    sys.exit(app.exec_())
