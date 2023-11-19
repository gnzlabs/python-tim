#! /usr/bin/python3

import json
import os

from configuration import Configuration
from network import TimServer, TimRequestHandler
from plugins import PluginLoader


if __name__ == "__main__":
    print("Welcome! Configuring Tim server...")
    loaded_config = Configuration(
        plugins=[
            "filesystem"
        ]
    )
    loaded_plugins = PluginLoader(loaded_config).load_plugins()
    print(f"Loaded plugins: {loaded_plugins}")
    tim_server = TimServer(
        ("0.0.0.0", 40960), TimRequestHandler, 
        configuration=loaded_config,
        plugins=loaded_plugins
    )
    print("Tim server is running.")
    tim_server.serve_forever()
