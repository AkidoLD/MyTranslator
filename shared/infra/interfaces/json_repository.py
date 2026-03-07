import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from shared.infra.exceptions.json_repository_exception import JsonRepositoryException


class JsonRepository:
    def __init__(self, path: str):
        self.path = path

    @property
    def path(self):
        return str(self._file_path.absolute())

    @path.setter
    def path(self, path : str):
        f = Path(path)
        if not f.exists() : f.touch()
        self._file_path = f

    def load(self) -> Any:
        try:
            content = self._file_path.read_text().strip()
            return json.loads(content) if content else content
        except (RuntimeError, ValueError, JSONDecodeError) as e:
            raise JsonRepositoryException(f"Failed to load data : {e}")

    def save(self, data: Any):
        try :
            with self._file_path.open("w") as file :
                json.dump(data, file, indent=2)
        #
        except (RuntimeError, ValueError, JSONDecodeError, TypeError) as e:
            raise JsonRepositoryException(f"Failed to save data : {e}")