from abc import ABC, abstractmethod



class TranslationProviderRepository(ABC):
    @abstractmethod
    def load(self) -> list[dict]:
        pass
    @abstractmethod
    def save(self, data : list[dict]):
        pass

    @abstractmethod
    def len(self) -> int:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def delete(self, provider_id: str):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def exist(self, provider_id: str):
        pass