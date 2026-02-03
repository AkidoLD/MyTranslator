import json
from pathlib import Path
from typing import List

from translation.domain.base.translation_api import TranslationApi
from translation.domain.repositories.translation_api_repository import TranslationApiRepository
from translation.infra.factory import get_translation_provider


class JsonTranslationApiRepository(TranslationApiRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path
        pass

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self,  path : str):
        try :
            f = Path(path)
            if not f.exists() : f.touch()
            self._file_path = f
        except Exception as e:
            raise RuntimeError("Failed to set the file path in JsonTranslationApiRepository : ", e)

    def load(self) -> list[TranslationApi]:
        try :
            with self.file_path.open("r") as file :
                data = json.load(file)
                if not isinstance(data, list) :
                    raise TypeError("Invalid JSON content. The type of the api list must be type of `list`")
                #
                l : List[TranslationApi]= []
                for value in data :
                    #Retrieve the type of the API
                    t = value.get("type")

                    #If not found, crash 😼
                    if not t :
                        raise TypeError("Invalid JSON content. The type of the api is not found")

                    #Get the corresponded api provider
                    cls = get_translation_provider(t)
                    api = cls.from_dict(value)
                    l.append(api)
                #
                return l
        except Exception as e :
            raise RuntimeError("Failed to load data in JsonTranslationApiRepository : ", e)

    def save(self, data: list[TranslationApi]):
        try :
            with self.file_path.open("w") as file :
                l = []
                for api in data : l.append(api.to_dict())
                json.dump(l, file, indent=2)
        #
        except Exception as e :
            raise RuntimeError("Failed to save data in JsonTranslationApiRepository : ", e)

    def len(self) -> int:
        return len(self.load())

    def is_empty(self) -> bool:
        return self.len() == 0