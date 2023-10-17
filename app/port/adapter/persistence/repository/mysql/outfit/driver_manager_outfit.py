from typing import Optional, NoReturn

from injector import inject

from domain.model.outfit import OutfitId, Outfit, Gender
from port.adapter.persistence.repository.mysql.outfit.driver import OutfitsTableRow, OutfitsCrud, InterestGender, \
    OutfitImagesCrud, OutfitImagesTableRow


class DriverManagerOutfit:
    @inject
    def __init__(self,
                 outfits_crud: OutfitsCrud,
                 outfit_images_crud: OutfitImagesCrud):
        self.__outfits_crud = outfits_crud
        self.__outfit_images_crud = outfit_images_crud

    def count(self) -> int:
        return self.__outfits_crud.count()

    def find_one_by_id(self, id: OutfitId) -> Optional[Outfit]:
        optional = self.__outfits_crud.find_one_by(id=id.id, deleted=False)
        if optional is None:
            return None
        return optional.to_entity(self.__outfit_images_crud.find_all_by(deleted=False))

    def pagination(self, gender: Optional[Gender], start: int, size: int) -> list[Outfit]:
        table_rows = self.__outfits_crud.pagination(
            InterestGender.integer(gender) if gender is not None else None,
            start,
            size
        )
        return [table_row.to_entity(self.__outfit_images_crud.find_all_by(outfit_id=table_row.id, deleted=False)) \
                for table_row in table_rows]

    def upsert(self, outfit: Outfit) -> NoReturn:
        self.__outfits_crud.upsert(OutfitsTableRow.of(outfit))
        # 画像を一旦全て削除する
        self.__outfit_images_crud.delete(outfit_id=outfit.outfit_id.id)
        self.__outfit_images_crud.insert(OutfitImagesTableRow.of(outfit))

    def delete(self, id: OutfitId) -> NoReturn:
        self.__outfits_crud.delete(id.id)
        self.__outfit_images_crud.delete(outfit_id=id.id)
