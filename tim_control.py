#! /usr/bin/python3

import base64
import json
import socket

from dataclasses import dataclass


@dataclass
class Command(object):

    plugin: str
    directive: str
    arguments: dict


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 40960))
    while True:
        plugin = input("Plugin > ")
        directive = input("Directive > ")
        arguments = json.loads(input("Arguments > "))
        command = Command(plugin, directive, arguments)
        s.sendall(
            base64.b64encode(
                bytes(json.dumps(command.__dict__), 'utf-8')
            )
        )
        response = json.loads(base64.b64decode(s.recv(204800)))
        print(json.dumps(response, indent=4))