from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(init=True, unsafe_hash=True, frozen=True)
class CreateOutfitCommand:
    images: list[str]
    gender: str
    description: Optional[str]
    posted_at: Optional[date]
    url: str
