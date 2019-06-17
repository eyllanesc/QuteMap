# -*- coding: utf-8 -*-

"""Top-level package for QuteMap."""

__author__ = """Edwin Christian Yllanes Cucho"""
__email__ = "e.yllanescucho@gmail.com"

from .QuteMap import MapHandler, MapPage
from . import utils
from .plugin import Plugin

__version_major__ = 0
__version_minor__ = 0
__version_micro__ = 1
__version__ = "{}.{}.{}".format(
    __version_major__, __version_minor__, __version_micro__
)

__all__ = ["QuteMap", "utils", "Plugin"]
