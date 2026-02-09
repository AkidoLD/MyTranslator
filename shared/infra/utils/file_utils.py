import os
from pathlib import Path


class FileUtils:
    @staticmethod
    def get_real_path(file_path : str) -> str:
        return os.path.join(os.path.dirname(__file__), file_path)

    @staticmethod
    def file_exist(file_path : str) -> bool:
        return Path(file_path).exists()