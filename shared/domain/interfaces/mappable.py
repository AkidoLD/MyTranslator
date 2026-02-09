from abc import ABC, abstractmethod
from typing import Self


class Mappable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        """Convert this object to a dictionary structure"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> Self:
        pass