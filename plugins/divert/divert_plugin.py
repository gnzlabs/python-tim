import os

from .._base import Plugin
from .diverter import Diverter


class Divert(Plugin):

    def __init__(self, configuration):
        super().__init__(configuration)
        self._diverter: Diverter = None

    def _cmd_start(self, filter="true", **kwargs):
        if self._diverter is not None:
            if self._diverter.is_running:
                raise RuntimeError("Already started")
        else:
            self._diverter = Diverter(kwargs.get("storage_directory"))
        self._diverter.start(filter)
        return {"diverter_active": self._diverter.is_running}
    
    def _cmd_stop(self, **kwargs):
        if self._diverter is None:
            raise RuntimeError("Not started")
        self._diverter.stop()
        running = self._diverter.is_running
        self._diverter = None
        return {"diverter_active": running}
        
    
    def handle(self, directive: str, *args, **kwargs) -> dict:
        kwargs["storage_directory"] = kwargs.get("storage_directory", 
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "diverted_packets")
        )
        return super().handle(directive, *args, **kwargs)