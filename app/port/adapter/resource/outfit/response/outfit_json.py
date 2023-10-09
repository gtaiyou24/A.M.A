from __future__ import annotations

from typing import List
from uuid import UUID

from pydantic.fields import Field

from application.outfit.dpo import OutfitDpo
from port.adapter.resource.outfit.definition import OutfitDefinition


class OutfitJson(OutfitDefinition):
    id: UUID = Field(title='コーディネートID')

    @staticmethod
    def of(dpo: OutfitDpo) -> OutfitJson:
        return OutfitJson(
            id=UUID(dpo.outfit.outfit_id.id),
            gender=dpo.outfit.gender.name,
            images=[image.address for image in dpo.outfit.images],
            description=dpo.outfit.description,
            posted_at=dpo.outfit.posted_at,
            url=dpo.outfit.url.address
        )
