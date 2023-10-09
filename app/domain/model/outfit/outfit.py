from dataclasses import dataclass
from datetime import date
from typing import Optional

from domain.model.image import Image
from domain.model.outfit import OutfitId, Gender
from domain.model.url import URL


@dataclass(init=True)
class Outfit:
    """コーディネート"""
    outfit_id: OutfitId
    gender: Gender
    images: list[Image]
    description: Optional[str]
    posted_at: date
    url: URL
