import datetime
from typing import NoReturn, Optional

from injector import singleton, inject

from application.outfit.command import CreateOutfitCommand, UpdateOutfitCommand
from application.outfit.dpo import ListOutfitDpo, OutfitDpo
from domain.model.image import Image
from domain.model.outfit import OutfitRepository, Outfit, OutfitId, Gender
from domain.model.url import URL


@singleton
class OutfitApplicationService:
    @inject
    def __init__(self, outfit_repository: OutfitRepository):
        self.__outfit_repository = outfit_repository

    def create(self, command: CreateOutfitCommand) -> NoReturn:
        outfit = Outfit(
            self.__outfit_repository.next_identity(),
            Gender[command.gender],
            [Image(image_url) for image_url in command.images],
            command.description,
            command.posted_at if command.posted_at is not None else datetime.date.today(),
            URL(command.url)
        )
        self.__outfit_repository.save(outfit)

    def update(self, command: UpdateOutfitCommand) -> NoReturn:
        outfit_id = OutfitId(command.id)
        outfit = self.__outfit_repository.outfit_of_id(outfit_id)

        outfit.gender = Gender[command.gender]
        outfit.images = [Image(image_url) for image_url in command.images]
        outfit.description = command.description
        outfit.posted_at = command.posted_at if command.posted_at is not None else datetime.date.today()
        outfit.url = URL(command.url)

        self.__outfit_repository.save(outfit)

    def list(self, start: int = 0, size: int = 30, gender: Optional[str] = None) -> ListOutfitDpo:
        return ListOutfitDpo(
            self.__outfit_repository.total(),
            self.__outfit_repository.outfits(start, size, None if gender is None else Gender[gender])
        )

    def get(self, outfit_id: str) -> OutfitDpo:
        outfit_id = OutfitId(outfit_id)
        outfit = self.__outfit_repository.outfit_of_id(outfit_id)
        if outfit is None:
            raise Exception(f'該当コーディネート {outfit_id} が見つかりませんでした')
        return OutfitDpo(outfit)

    def delete(self, outfit_id: str) -> NoReturn:
        outfit_id = OutfitId(outfit_id)
        outfit = self.__outfit_repository.outfit_of_id(outfit_id)
        self.__outfit_repository.remove(outfit)
