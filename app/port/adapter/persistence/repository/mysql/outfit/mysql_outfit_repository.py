import uuid
from typing import NoReturn, Optional

from injector import inject

from domain.model.outfit import OutfitRepository, Outfit, Gender, OutfitId
from port.adapter.persistence.repository.mysql.outfit import DriverManagerOutfit


class MySQLOutfitRepository(OutfitRepository):
    @inject
    def __init__(self, driver_manager_outfit: DriverManagerOutfit):
        self.__driver_manager_outfit = driver_manager_outfit

    def next_identity(self) -> OutfitId:
        return OutfitId(str(uuid.uuid4()))

    def total(self) -> int:
        return self.__driver_manager_outfit.count()

    def outfit_of_id(self, an_outfit_id: OutfitId) -> Optional[Outfit]:
        return self.__driver_manager_outfit.find_one_by_id(an_outfit_id)

    def outfits(self, start: int, size: int, gender: Optional[Gender] = None) -> list[Outfit]:
        return self.__driver_manager_outfit.pagination(gender, start, size)

    def add(self, outfit: Outfit) -> NoReturn:
        self.__driver_manager_outfit.upsert(outfit)

    def remove(self, outfit: Outfit) -> NoReturn:
        self.__driver_manager_outfit.delete(outfit.outfit_id)
