import uuid
from typing import NoReturn

from domain.model.outfit import OutfitRepository, Outfit, OutfitId


class InMemOutfitRepository(OutfitRepository):
    def __init__(self, outfits: list[Outfit] = []):
        self.__outfits = outfits

    def next_identity(self) -> OutfitId:
        return OutfitId(str(uuid.uuid4()))

    def total(self) -> int:
        return len(self.__outfits)

    def outfit_of_id(self, an_outfit_id: OutfitId) -> Outfit:
        for outfit in self.__outfits:
            if outfit.outfit_id == an_outfit_id:
                return outfit
        raise ValueError()

    def outfits(self, start: int, size: int) -> list[Outfit]:
        return self.__outfits[start:start+size]

    def save(self, outfit: Outfit) -> NoReturn:
        self.__outfits.append(outfit)

    def remove(self, outfit: Outfit) -> NoReturn:
        self.__outfits.remove(outfit)
