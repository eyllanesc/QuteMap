# -*- coding: utf-8 -*-
import logging
import json
from dataclasses import dataclass
from typing import List


DEFAULT_LOGGER_CREATED = False


def defaultLogger() -> logging.Logger:
    """
    Creates a debugging logger that prints to console.
    
    :rtype: :class:`logging.Logger` instance
    """
    global DEFAULT_LOGGER_CREATED

    log = logging.getLogger("qutemap")

    if not DEFAULT_LOGGER_CREATED:
        log.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(
            logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        )
        log.addHandler(console)
        DEFAULT_LOGGER_CREATED = True
    return log


class DummyLogger(object):
    """
    A dummy logger. You can call `debug()`, `warning()`, etc on this object, and nothing will happen.
    """

    def __init__(self):
        pass

    def dummy_func(self, *args, **kargs):
        pass

    def __getattr__(self, name):
        if name.startswith("__"):
            return object.__getattr__(name)
        return self.dummy_func
