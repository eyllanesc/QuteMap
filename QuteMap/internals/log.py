import os
import logging.config
import yaml
from .Qt import QtCore

DEFAULT_LOGGER_CREATED = False

qutemap = logging.getLogger("qutemap")
scheme = logging.getLogger("scheme")
js = logging.getLogger("js")
qt = logging.getLogger("qt")

DEFAULT_LOGGER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "logging.yaml")
)


def init_log(log_path=DEFAULT_LOGGER_PATH, log_level=logging.INFO):
    global DEFAULT_LOGGER_CREATED

    if not DEFAULT_LOGGER_CREATED:
        if os.path.exists(log_path):
            with open(log_path, "rt") as f:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=log_level)
        DEFAULT_LOGGER_CREATED = True


def qt_message_handler(msg_type, context, msg):
    qt_to_logging = {
        QtCore.QtInfoMsg: logging.INFO,
        QtCore.QtDebugMsg: logging.DEBUG,
        QtCore.QtWarningMsg: logging.WARNING,
        QtCore.QtCriticalMsg: logging.ERROR,
        QtCore.QtFatalMsg: logging.CRITICAL,
    }
    if context.category is None or context.category == "default":
        name = "qt"
    else:
        name = "qt-" + context.category

    if context.function is None:
        func = "none"
    elif ":" in context.function:
        func = '"{}"'.format(context.function)
    else:
        func = context.function
    level = qt_to_logging[msg_type]
    record = qt.makeRecord(
        name, level, context.file, context.line, msg, (), None, func
    )
    qt.handle(record)
