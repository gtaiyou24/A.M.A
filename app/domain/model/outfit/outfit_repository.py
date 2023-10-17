import abc
from typing import NoReturn, Optional

from domain.model.outfit import OutfitId, Outfit, Gender


class OutfitRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> OutfitId:
        pass

    @abc.abstractmethod
    def total(self) -> int:
        pass

    @abc.abstractmethod
    def outfit_of_id(self, an_outfit_id: OutfitId) -> Optional[Outfit]:
        pass

    @abc.abstractmethod
    def outfits(self, start: int, size: int, gender: Optional[Gender] = None) -> list[Outfit]:
        pass

    @abc.abstractmethod
    def save(self, outfit: Outfit) -> NoReturn:
        pass

    @abc.abstractmethod
    def remove(self, outfit: Outfit) -> NoReturn:
        pass
