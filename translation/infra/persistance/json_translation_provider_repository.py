import json
from pathlib import Path
from translation.domain.repositories.translation_provider_repository import TranslationProviderRepository


class JsonTranslationProviderRepository(TranslationProviderRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path
        pass

    @property
    def file_path(self):
        return str(self._file_path.absolute())

    @file_path.setter
    def file_path(self,  path : str):
        try :
            f = Path(path)
            if not f.exists() : f.touch()
            self._file_path = f
        except Exception as e:
            raise RuntimeError("Failed to set the file path in JsonTranslationProviderRepository : ", e)

    def load(self) -> list[dict]:
        try :
            with self._file_path.open("r") as file :
                data = json.load(file)
                if not isinstance(data, list) :
                    raise TypeError("Invalid JSON content. The _type of the api list must be _type of `list`")
                #
                return data
        except Exception as e :
            raise RuntimeError("Failed to load data in JsonTranslationProviderRepository : ", e)

    def save(self, data: list[dict]):
        try :
            with self._file_path.open("w") as file :
                json.dump(data, file, indent=2)
        #
        except Exception as e :
            raise RuntimeError("Failed to save data in JsonTranslationProviderRepository : ", e)

    def delete(self, provider_id : str):
        providers = [provider for provider in self.load() if provider.get("id", "") != provider_id]
        self.save(providers)

    def exist(self, provider_id : str):
        return any(p.get("id", "") == provider_id for p in self.load())

    def len(self) -> int:
        return len(self.load())

    def is_empty(self) -> bool:
        return any(p for p in self.load()) == False

    def clear(self):
        self.save([])