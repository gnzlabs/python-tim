from typing import Dict
from plugins import Plugin


class CommandHandler(object):

    def __init__(self, plugins: Dict[str, Plugin]):
        self._plugins = plugins

    def handle(self, plugin, directive, **kwargs):
        response = {"error": f"Plugin '{plugin}' not found"}
        if plugin in self._plugins:
            response = self._plugins[plugin].handle(directive, **kwargs)
        return response
