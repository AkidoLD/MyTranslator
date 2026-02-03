from abc import ABC, abstractmethod

from translation.domain.base.translation_api import TranslationApi


class TranslationApiRepository(ABC):
    @abstractmethod
    def load(self) -> list[TranslationApi]:
        pass
    @abstractmethod
    def save(self, data : list[TranslationApi]):
        pass

    @abstractmethod
    def len(self) -> int:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass