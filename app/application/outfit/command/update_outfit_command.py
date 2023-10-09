from dataclasses import dataclass

from application.outfit.command import CreateOutfitCommand


@dataclass(init=True, unsafe_hash=True, frozen=True)
class UpdateOutfitCommand(CreateOutfitCommand):
    id: str
