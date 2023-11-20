import mimetypes

from pathlib import Path


class FileInfo(object):

    def __init__(self, file_path: Path, file_stats):
        self.file_name = file_path.name
        self.file_parent = str(file_path.parent)
        self.file_extension = file_path.suffix
        self.reported_mime_type = mimetypes.guess_type(file_path)
        self.permissions = getattr(file_stats, "st_mode", 0)
        self.inode = getattr(file_stats, "st_ino", 0)
        self.device_id = getattr(file_stats, "st_dev", 0)
        self.link_count = getattr(file_stats, "st_nlink", 0)
        self.owner_id = getattr(file_stats, "st_uid", 0)
        self.group_id = getattr(file_stats, "st_gid", 0)
        self.size_bytes = getattr(file_stats, "st_size", 0)
        self.time_last_accessed = getattr(file_stats, "st_atime", 0)
        self.time_last_modified = getattr(file_stats, "st_mtime", 0)
        self.time_created = getattr(file_stats, "st_ctime", 0)
