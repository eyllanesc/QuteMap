# -*- coding: utf-8 -*-

"""Top-level package for QuteMap."""

__author__ = """Edwin Christian Yllanes Cucho"""
__email__ = "e.yllanescucho@gmail.com"

from .QuteMap import MapHandler, MapPage
from .internals.plugin import Plugin
from .internals import log
from .internals.Qt import QtCompat, QtWebEngineCore

__version_major__ = 0
__version_minor__ = 0
__version_micro__ = 1
__version__ = "{}.{}.{}".format(
    __version_major__, __version_minor__, __version_micro__
)

__all__ = ["QuteMap"]


def init(log_enabled: bool =False) -> None:
    """Function used to configure QuteMap, 
    this must be called before creating an instance of `QApplication <https://doc.qt.io/qt-5/qapplication.html>`_.
	
    :param log_enabled: Enable logging
    :type log_enabled: :class:`bool`
    """
    QtCompat.qInstallMessageHandler(log.qt_message_handler)

    scheme = QtWebEngineCore.QWebEngineUrlScheme(b"qutemap")
    scheme.setFlags(
        QtWebEngineCore.QWebEngineUrlScheme.LocalScheme
        | QtWebEngineCore.QWebEngineUrlScheme.LocalAccessAllowed
    )
    QtWebEngineCore.QWebEngineUrlScheme.registerScheme(scheme)
    if log_enabled:
        log.init_log()
