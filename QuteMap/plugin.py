# -*- coding: utf-8 -*-
import os
import json
from dataclasses import dataclass
from typing import List


base_dir = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIRS = [os.path.join(base_dir, "plugins")]


@dataclass
class Plugin:
    """This is a Plugin class.

        :param name: Name of plugin
        :type name: str
        :param path: Path of plugin
        :type path: str
        :param html: Name of html file
        :type html: str
        :param javascripts: Name of the javascripts files
        :type javascripts: List[str]
        :rtype: :class:`.Plugin` instance
    """

    name: str
    path: str
    html: str
    javascripts: List[str]

    @staticmethod
    def getPlugin(name: str) -> "Plugin":
        """
        method that gets the plugin by name.

        :param name: Name of plugin
        :type name: str
        :rtype: :class:`.Plugin` instance or None if the plugin is not found
        """
        for directory in PLUGIN_DIRS:
            plugin_path = os.path.join(directory, name)
            config_filename = os.path.join(plugin_path, "config.json")
            if os.path.exists(config_filename):
                with open(config_filename) as f:
                    config = json.load(f)
                    plugin = Plugin(
                        name, plugin_path, config["html"], config["javascripts"]
                    )
                    return plugin


def addPluginDirectory(directory: str) -> None:
    """
    Function that adds plugins directories.

    :param directory: Plugin directory
    :type directory: str
    """
    PLUGIN_DIRS.append(directory)
