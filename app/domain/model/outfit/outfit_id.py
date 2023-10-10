from dataclasses import dataclass


@dataclass(init=False, frozen=True, unsafe_hash=True)
class OutfitId:
    id: str

    def __init__(self, id: str):
        assert id, 'コーディネートIDは必須です。'
        assert len(id) <= 36, 'コーディネートIDは36文字以内でなければいけません。'
        super().__setattr__('id', id)
