# -*- coding: utf-8 -*-

"""Main module."""
from typing import Dict

from .internals.Qt import (
    QtCore,
    QtWebEngineWidgets,
    QtWebChannel,
    QtPositioning,
)

from .internals import log, webenginescheme
from .internals.plugin import Plugin


class MapHandler(QtCore.QObject):
    """Class that handles the map and the markers

        :param page: Page where the map and markers that it handles are displayed
        :type page: :class:`.MapPage` instance
        :rtype: :class:`.MapHandler` instance

    **Signals:**
        centerChanged(center): This signal is sent when the center of the map changes position.
        zoomChanged(zoom): This signal is sent when the zoom of map change.

    **Slots:**
        :meth:`.updateCenterFromMap` : Update the :attr:`.center` property from the map.
        :meth:`.updateZoomFromMap` : Update the :attr:`.zoom` property from the map.
    """

    centerChanged = QtCore.Signal(QtPositioning.QGeoCoordinate)
    zoomChanged = QtCore.Signal(int)

    def __init__(self, page):
        super().__init__(page)
        self.m_map = page
        self.m_center = QtPositioning.QGeoCoordinate()
        self.m_zoom = 1
        self.m_markers = []

    def center(self):
        """Center of the map

            :getter: Returns the position of the center of the map 
            :setter: Set the new position of the center of the map
            :type: `QGeoCoordinate <https://doc.qt.io/qt-5/qgeocoordinate.html>`_
        """
        return self.m_center

    def setCenter(self, position):
        if self.m_center != position and position.isValid():
            log.qutemap.debug(
                f"set center to map: {position.toString(QtPositioning.QGeoCoordinate.DegreesMinutesSeconds)}"
            )
            self.m_map.runJavaScript(
                f"setCenter({position.latitude()}, {position.longitude()});"
            )

    center = QtCore.Property(
        QtPositioning.QGeoCoordinate,
        fget=center,
        fset=setCenter,
        notify=centerChanged,
    )

    def zoom(self):
        """Zoom map

            :getter: Returns the zoom of the map 
            :setter: Set the new zoom of the map
            :type: int
        """
        return self.m_zoom

    def setZoom(self, zoom):
        if self.m_zoom != zoom and zoom >= 1:
            log.qutemap.debug(f"set zoom to map: {zoom}")
            self.m_map.runJavaScript(f"setZoom({zoom})")

    zoom = QtCore.Property(int, fget=zoom, fset=setZoom, notify=zoomChanged)

    # Methods that allow to update the properties from js.

    @QtCore.Slot(float, float)
    def updateCenterFromMap(self, latitude, longitude):
        """Update the :attr:`.center` property from the map."""
        self.m_center = QtPositioning.QGeoCoordinate(latitude, longitude)
        self.centerChanged.emit(self.m_center)
        log.qutemap.debug(
            f"update center from map : {self.m_center.toString(QtPositioning.QGeoCoordinate.DegreesMinutesSeconds)}"
        )

    @QtCore.Slot(int)
    def updateZoomFromMap(self, zoom):
        """Update the :attr:`.zoom` property from the map."""
        self.m_zoom = zoom
        log.qutemap.debug(f"update zoom from map: {zoom}")
        self.zoomChanged.emit(self.m_zoom)


class MapPage(QtWebEngineWidgets.QWebEnginePage):
    """Class showing the maps

        :param name: name of map
        :type name: str 
        :param plugin: name of plugin
        :type plugin: str 
        :param parameters: additional parameters of the map
        :type parameters: dict, None
        :param parent: Constructs an object with parent object parent.
        :type parent: `QObject <https://doc.qt.io/qt-5/qobject.html>`_
        :rtype: :class:`.MapPage` instance
    """

    def __init__(
        self, name, plugin, parameters=None, parent=None, log_enabled=False
    ):
        super().__init__(parent)
        self.m_name = name

        channel = QtWebChannel.QWebChannel(self)
        self.setWebChannel(channel)
        self.m_handler = MapHandler(self)
        channel.registerObject("qutemap_handler", self.m_handler)

        handler = QtWebEngineWidgets.QWebEngineProfile.defaultProfile().urlSchemeHandler(
            b"qutemap"
        )
        if handler is None:
            handler = webenginescheme.WebEngineUrlSchemeHandler(
                QtCore.QCoreApplication.instance()
            )
            QtWebEngineWidgets.QWebEngineProfile.defaultProfile().installUrlSchemeHandler(
                b"qutemap", handler
            )

        if parameters is None:
            parameters = {}

        p = Plugin.getPlugin(plugin)
        if p is not None:
            parameters["root"] = f"qutemap://{p.name}/{self.name}"
            handler.parameters[name] = parameters
            self.load(QtCore.QUrl(f"qutemap://{p.name}/{self.name}/{p.html}"))
            log.qutemap.debug(f"found plugin: {p}")
        else:
            log.qutemap.debug(f"not found plugin: {p}")

    @property
    def name(self):
        """name of map

            :getter: Returns the name of map
            :type: str
        """
        return self.m_name

    @property
    def handler(self):
        """handler of map and markers

            :getter: Returns this handler
            :type: :class:`.MapHandler`
        """
        return self.m_handler

    def javaScriptConsoleMessage(self, level, msg, line, source):
        logstring = f"[{source}:{line}] {msg}"
        level_map = {
            QtWebEngineWidgets.QWebEnginePage.InfoMessageLevel: log.js.info,
            QtWebEngineWidgets.QWebEnginePage.WarningMessageLevel: log.js.warning,
            QtWebEngineWidgets.QWebEnginePage.ErrorMessageLevel: log.js.error,
        }
        level_map[level](logstring)
