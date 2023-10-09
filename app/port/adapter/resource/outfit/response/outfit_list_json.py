from __future__ import annotations

from typing import List

from pydantic.fields import Field
from pydantic.main import BaseModel

from application.outfit.dpo import ListOutfitDpo, OutfitDpo
from port.adapter.resource.outfit.response import OutfitJson


class OutfitListJson(BaseModel):
    total: int = Field(title='件数')
    items: List[OutfitJson] = Field(title='コーディネート一覧')

    @staticmethod
    def of(dpo: ListOutfitDpo) -> OutfitListJson:
        return OutfitListJson(
            total=dpo.total,
            items=[OutfitJson.of(OutfitDpo(outfit)) for outfit in dpo.outfits]
        )
