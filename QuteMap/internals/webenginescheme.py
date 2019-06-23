import jinja2

from .Qt import QtCore, QtWebEngineCore
from .plugin import Plugin
from . import log


class WebEngineUrlSchemeHandler(QtWebEngineCore.QWebEngineUrlSchemeHandler):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_parameters = {}

    @property
    def parameters(self):
        return self.m_parameters

    def requestStarted(self, request):
        url = request.requestUrl()
        plugin_name = url.host()
        p = Plugin.getPlugin(plugin_name)
        if p is not None:
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(p.path))
            _, *paths = url.path().split("/")
            if len(paths) == 2:
                name, html = paths
                if html in [p.html] + p.javascripts:
                    res = env.get_template(html).render(
                        self.parameters.get(name, {})
                    )
                    log.scheme.debug(res)
                    buf = QtCore.QBuffer(parent=self)
                    request.destroyed.connect(buf.deleteLater)
                    buf.open(QtCore.QIODevice.WriteOnly)
                    buf.write(res.encode())
                    buf.seek(0)
                    buf.close()
                    request.reply(b"text/html", buf)
                    return
        request.fail(QtWebEngineCore.QWebEngineUrlRequestJob.UrlNotFound)
