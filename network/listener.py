import base64
import json
import socketserver
import os

from command import CommandHandler
from configuration import Configuration


class TimServer(socketserver.ThreadingTCPServer):

    def __init__(self, *args, **kwargs):
        self.config: Configuration = kwargs.get("configuration")
        self.commands = CommandHandler(kwargs.get("plugins"))
        for keyword_arg in ["configuration", "plugins"]:
            del kwargs[keyword_arg]
        super().__init__(*args, **kwargs)


class TimRequestHandler(socketserver.StreamRequestHandler):

    def unpack_command(self, packed_command: str) -> dict:
        print(f"Packed command: {str(packed_command, 'utf-8')}")
        return json.loads(base64.b64decode(packed_command.strip()))
    
    def pack_response(self, response: dict) -> bytes:
        return base64.b64encode(bytes(json.dumps(response), 'utf-8'))

    def handle(self):
        command = self.unpack_command(self.rfile.readline())
        print(f"== Command =={os.linesep}{json.dumps(command, indent=4)}")
        if not command["arguments"]:
            command["arguments"] = {}
        response = self.server.commands.handle(command["plugin"], command["directive"], **command["arguments"])
        print(f"== Response =={os.linesep}{json.dumps(response, indent=4)}{os.linesep}====")
        self.wfile.write(self.pack_response(response))
