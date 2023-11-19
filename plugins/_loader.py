import importlib
import inspect

from typing import List, Dict

from ._base import Plugin
from configuration import Configuration


class PluginLoader(object):

    def __init__(self, configuration: Configuration):
        self._config = configuration

    def _load_modules(self) -> List:
        loaded_modules = []
        for module_name in self._config.plugins:
            try:
                module = importlib.import_module(f"plugins.{module_name}")
                loaded_modules.append(module)
            except ModuleNotFoundError as e:
                # TODO: Logging
                print(e)
        print(loaded_modules)
        return loaded_modules

    def load_plugins(self) -> Dict[str, Plugin]:
        loaded_plugins = {}
        for module in self._load_modules():
            for name, cls in inspect.getmembers(module, lambda x: inspect.isclass(x)):
                if issubclass(cls, Plugin) and cls is not Plugin:
                    print(f"Found plugin {name} at {cls}")
                    if name in loaded_plugins:
                        raise NameError(f"Duplicate plugin name: {name}")
                    loaded_plugins[name] = cls(self._config)
                    loaded_plugins[name].setup()
        return loaded_plugins
