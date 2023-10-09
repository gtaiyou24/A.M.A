from dataclasses import dataclass

from domain.model.outfit import Outfit


@dataclass
class ListOutfitDpo:
    total: int
    outfits: list[Outfit]
