# -*- coding: utf-8 -*-

"""Console script for qutemap."""
import os
import sys
from functools import partial

import click

from . import __version__
from .customtypes import COORDINATE_TYPE, JSON_TYPE


app = None


@click.version_option(version=__version__)
@click.command(
    context_settings={"ignore_unknown_options": True},
    options_metavar="<options>",
)
@click.option(
    "--center",
    "-c",
    type=COORDINATE_TYPE,
    help="Center of map, format: 'LAT,LNG'",
    required=True,
)
@click.option("--zoom", "-z", default=14, show_default=True, help="Map zoom")
@click.option("--parameters", type=JSON_TYPE, help="Extra parameters")
@click.option(
    "--plugin", default="google", show_default=True, help="Name of plugin"
)
@click.option(
    "--markers",
    type=click.Path(exists=True, readable=True),
    metavar="<markers>",
    help="Filename of json with information about the markers",
)
@click.option(
    "--binding",
    default="PyQt5",
    type=click.Choice(["PyQt5", "PySide2"]),
    show_default=True,
    help="Qt bindings",
)
@click.option(
    "--log",
    default=False,
    is_flag=True,
    show_default=True,
    help="Enable logging",
)
def main(center, markers, zoom, parameters, plugin, binding, log):
    """Console script for qutemap.
    """
    from .plugin import Plugin

    if Plugin.getPlugin(plugin) is None:
        click.echo(f"The plugin {plugin!r} was not found")
        return -1

    last_binding = os.environ.get("QT_PREFERRED_BINDING")
    os.environ["QT_PREFERRED_BINDING"] = binding

    from .vendor.Qt import QtWidgets, QtWebEngineWidgets, QtPositioning
    from .QuteMap import MapPage

    def on_load_finished(handler, ok):
        click.echo(f"load finished: {ok}")
        if ok:
            handler.center = QtPositioning.QGeoCoordinate(*center)

    # print(center, markers, zoom, parameters, plugin, binding, log)

    global app
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    view = QtWebEngineWidgets.QWebEngineView()
    view.setWindowTitle(f"{__name__} {__version__}")
    page = MapPage(
        plugin, parent=view, parameters=parameters, connect_default_logger=log
    )
    view.setPage(page)
    view.loadFinished.connect(partial(on_load_finished, page.handler))
    view.resize(640, 480)
    view.show()
    res = app.exec_()
    if last_binding:
        os.environ["QT_PREFERRED_BINDING"] = last_binding
    else:
        del os.environ["QT_PREFERRED_BINDING"]
    return res


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
