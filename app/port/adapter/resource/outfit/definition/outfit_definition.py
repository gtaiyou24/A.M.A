from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel


class OutfitDefinition(BaseModel):
    class Gender(str, Enum):
        WOMEN = 'WOMEN'
        MEN = 'MEN'
        KIDS = 'KIDS'
        UNKNOWN = 'UNKNOWN'

    images: List[str] = Field(title='画像URLの一覧')
    gender: OutfitDefinition.Gender = Field(title='性別', default='UNKOWN')
    description: Optional[str] = Field(title='説明文')
    posted_at: Optional[date] = Field(title='投稿日')
    url: str = Field(title='URL')