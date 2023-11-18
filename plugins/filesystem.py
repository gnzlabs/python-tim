import os
import pathlib

from ._base import Plugin


class FileSystem(Plugin):

    def _chdir(self, path) -> dict:
        os.chdir(path)
        return self._getcwd()

    def _getcwd(self, **kwargs) -> dict:
        return {"current_directory": os.getcwd()}
    
    def _listdir(self, path, pattern="*") -> dict:
        return_value = {
            "path": str(path),
            "files": [],
            "directories": []
        }
        for child in path.glob(pattern):
            fs_type = "files" if child.is_file() else "directories"
            return_value[fs_type].append(str(child))
        return return_value

    def handle(self, directive: str, *args, **kwargs) -> dict:
        kwargs["path"] = pathlib.Path(kwargs.get("path", ".")).absolute()
        if hasattr(self, f"_{directive}"):
            getattr(self, f"_{directive}")(**kwargs)