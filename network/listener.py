import base64
import json
import socketserver

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
        return json.loads(base64.b64decode(packed_command.strip()))
    
    def pack_response(self, response: dict) -> str:
        return base64.b64encode(json.dumps(response))

    def handle(self):
        command = self.unpack_command(self.rfile.readline())
        response = self.server.commands.handle(command)
        self.wfile.write(self.pack_response(response))
