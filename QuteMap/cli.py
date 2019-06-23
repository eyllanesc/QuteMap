# -*- coding: utf-8 -*-

"""Console script for qutemap."""
import os
import sys
from functools import partial

import click

from . import __version__
from .customtypes import COORDINATE_TYPE, JSON_TYPE, ChoiceOptional
from . import Plugin

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
@click.option(
    "--plugin",
    default="google",
    type=ChoiceOptional(Plugin.getPluginNames()),
    show_default=True,
    help="Plugin name of map",
)
@click.option("--zoom", "-z", default=14, show_default=True, help="Map zoom")
@click.option("--parameters", type=JSON_TYPE, help="Extra parameters")
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
@click.argument("extra_args", nargs=-1, type=click.UNPROCESSED)
def main(center, plugin, zoom, parameters, markers, binding, log, extra_args):
    """Console script for qutemap.
    """
    if Plugin.getPlugin(plugin) is None:
        click.echo(f"The plugin {plugin!r} was not found")
        return -1

    last_binding = os.environ.get("QT_PREFERRED_BINDING")
    os.environ["QT_PREFERRED_BINDING"] = binding

    import QuteMap
    from .internals.Qt import (
        QtCore,
        QtWidgets,
        QtWebEngineWidgets,
        QtPositioning,
    )
    from .QuteMap import MapPage

    def on_load_finished(handler, ok):
        click.echo(f"load finished: {ok}")
        if ok:
            c = QtPositioning.QGeoCoordinate(*center)
            QtCore.QTimer.singleShot(500, lambda: setattr(handler, "center", c))
            handler.zoom = zoom
            # handler.center = c
            click.echo(
                f"center: {c.toString(QtPositioning.QGeoCoordinate.DegreesMinutesSeconds)}"
            )
            click.echo(f"zoom: {zoom}")

    QuteMap.init()
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    global app
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv + list(extra_args))
    view = QtWebEngineWidgets.QWebEngineView()
    view.setWindowTitle(f"{__name__} {__version__}: {plugin}")
    page = MapPage("cli", plugin, parameters=parameters, log_enabled=log)
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
