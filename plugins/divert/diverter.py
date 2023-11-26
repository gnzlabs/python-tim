import json
import pydivert
import queue
import threading
import time

from pathlib import Path
from typing import Union


class Diverter(object):

    def __init__(self, storage_path: Union[Path, str]):
        self._active = False
        self._capture_queue = queue.Queue()
        self._capture_thread: threading.Thread = None
        self._write_thread: threading.Thread = None
        if type(storage_path) is str:
            storage_path = Path(storage_path)
        self.storage_path = storage_path

    def _capture_worker(self, filter: str):
        with pydivert.WinDivert(filter) as diverter:
            while self._active:
                for packet in diverter:
                    if not self._active:
                        return
                    self._capture_queue.put(packet)
                    diverter.send(packet)
    
    def _write_worker(self):
        while self._active:
            if not self._capture_queue.empty():
                packet: pydivert.Packet = self._capture_queue.get()
                with open(self.storage_path.joinpath(Path(f"{time.time_ns()}.pkt")), "w") as outfile:
                    outfile.write(str(packet))
            else:
                time.sleep(0.1)

    @property
    def is_running(self):
        return self._active

    def start(self, filter: str):
        if self._active:
            raise RuntimeError("Diverter already active")
        if not self.storage_path.exists():
            self.storage_path.mkdir(parents=True)
        if not pydivert.WinDivert.check_filter(filter):
            raise ValueError(f"Invalid filter: {filter}")
        self._active = True
        self._capture_thread = threading.Thread(target=self._capture_worker, args=(filter,))
        self._write_thread = threading.Thread(target=self._write_worker)
        for thread in [self._capture_thread, self._write_thread]:
            thread.start()

    def stop(self):
        self._active = False
        for thread in [self._capture_thread, self._write_thread]:
            thread.join()
