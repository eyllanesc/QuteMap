# -*- coding: utf-8 -*-

"""Main module."""
import os
import sys
import logging
from typing import Dict

import jinja2

from .vendor.Qt import (
    QtCore,
    QtWidgets,
    QtWebEngineWidgets,
    QtWebChannel,
    QtPositioning,
)

from . import utils
from .plugin import Plugin


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
            self.m_map.logger.debug(
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
            self.m_map.logger.debug(f"set zoom to map: {zoom}")
            self.m_map.runJavaScript(f"setZoom({zoom})")

    zoom = QtCore.Property(int, fget=zoom, fset=setZoom, notify=zoomChanged)

    # Methods that allow to update the properties from js.

    @QtCore.Slot(float, float)
    def updateCenterFromMap(self, latitude, longitude):
        """Update the :attr:`.center` property from the map."""
        self.m_center = QtPositioning.QGeoCoordinate(latitude, longitude)
        self.centerChanged.emit(self.m_center)
        self.m_map.logger.debug(
            f"update center from map : {self.m_center.toString(QtPositioning.QGeoCoordinate.DegreesMinutesSeconds)}"
        )

    @QtCore.Slot(int)
    def updateZoomFromMap(self, zoom):
        """Update the :attr:`.zoom` property from the map."""
        self.m_zoom = zoom
        self.m_map.logger.debug(f"update zoom from map: {zoom}")
        self.zoomChanged.emit(self.m_zoom)


class MapPage(QtWebEngineWidgets.QWebEnginePage):
    """Class showing the maps

        :param plugin: name of plugin
        :type plugin: str 
        :param parameters: additional parameters of the map
        :type parameters: dict, None
        :param parent: Constructs an object with parent object parent.
        :type parent: `QObject <https://doc.qt.io/qt-5/qobject.html>`_
        :param logger: An optional logger.
        :type logger: :class:`logging.Logger` instance
        :param connect_default_logger: If true, connects a default logger to the class.
        :type connect_default_logger: :class:`bool`
        :rtype: :class:`.MapPage` instance
    """

    def __init__(
        self,
        plugin,
        parameters=None,
        parent=None,
        logger=None,
        connect_default_logger=False,
    ):
        super().__init__(parent)
        if logger:
            self.m_logger = logger
        elif connect_default_logger:
            self.m_logger = utils.defaultLogger()
        else:
            self.m_logger = utils.DummyLogger()
        channel = QtWebChannel.QWebChannel(self)
        self.setWebChannel(channel)
        self.m_handler = MapHandler(self)
        channel.registerObject("map_handler", self.m_handler)
        if parameters is None:
            parameters = dict()
        p = Plugin.getPlugin(plugin)
        if p is not None:
            self.loadPlugin(p, parameters)
        else:
            self.logger.debug(f"not found plugin: {plugin}")

    @property
    def handler(self):
        """handler of map and markers

            :getter: Returns this handler
            :type: :class:`.MapHandler`
        """
        return self.m_handler

    @property
    def logger(self):
        """logger of class

            :getter: Returns this logger
            :type: :class:`.logging.Logger`
        """
        return self.m_logger

    def loadPlugin(self, plugin: Plugin, parameters: Dict[str, str]):
        """Function that loads the .html and .js files by passing the additional parameters.
    	"""
        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(plugin.path)
        )
        for js in plugin.javascripts:
            js_script = environment.get_template(js).render(parameters)
            script = QtWebEngineWidgets.QWebEngineScript()
            script.setName(js)
            script.setInjectionPoint(
                QtWebEngineWidgets.QWebEngineScript.DocumentReady
            )
            script.setRunsOnSubFrames(True)
            script.setWorldId(
                QtWebEngineWidgets.QWebEngineScript.ApplicationWorld
            )
            script.setSourceCode(js_script)
            self.profile().scripts().insert(script)
        parameters["_"] = lambda x: x
        html = environment.get_template(plugin.html).render(parameters)
        self.setHtml(
            html,
            QtCore.QUrl.fromLocalFile(
                os.path.join(plugin.path, f"{plugin.name}.html")
            ),
        )

    def javaScriptConsoleMessage(self, level, msg, line, source):
        logstring = f"[{source}:{line}] {msg}"
        level_map = {
            QtWebEngineWidgets.QWebEnginePage.InfoMessageLevel: self.logger.info,
            QtWebEngineWidgets.QWebEnginePage.WarningMessageLevel: self.logger.warning,
            QtWebEngineWidgets.QWebEnginePage.ErrorMessageLevel: self.logger.error,
        }
        level_map[level](logstring)
