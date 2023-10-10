import abc
from typing import NoReturn

from domain.model.outfit import OutfitId, Outfit


class OutfitRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> OutfitId:
        pass

    @abc.abstractmethod
    def total(self) -> int:
        pass

    @abc.abstractmethod
    def outfit_of_id(self, an_outfit_id: OutfitId) -> Outfit:
        pass

    @abc.abstractmethod
    def outfits(self, start: int, size: int) -> list[Outfit]:
        pass

    @abc.abstractmethod
    def save(self, outfit: Outfit) -> NoReturn:
        pass

    @abc.abstractmethod
    def remove(self, outfit: Outfit) -> NoReturn:
        pass