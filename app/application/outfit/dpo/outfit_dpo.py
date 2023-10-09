from dataclasses import dataclass

from domain.model.outfit import Outfit


@dataclass
class OutfitDpo:
    outfit: Outfit
