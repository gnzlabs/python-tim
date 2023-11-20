from .info import FileInfo
from pathlib import Path
from typing import Union


def get_file_info(file_path: Union[Path, str]) -> dict:
    if type(file_path) is not Path:
        file_path = Path(file_path)
    return FileInfo(file_path, file_path.stat()).__dict__
