import os
import pathlib

from .._base import Plugin


class FileSystem(Plugin):

    def _cmd_chdir(self, path) -> dict:
        os.chdir(path)
        return self._getcwd()

    def _cmd_getcwd(self, **kwargs) -> dict:
        return {"current_directory": os.getcwd()}
    
    def _cmd_listdir(self, path, pattern="*") -> dict:
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
        return super().handle(directive, *args, **kwargs)
