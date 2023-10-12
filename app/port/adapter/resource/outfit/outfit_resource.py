from typing import Optional
from uuid import UUID

from di import DIContainer
from fastapi import APIRouter

from application.outfit import OutfitApplicationService
from application.outfit.command import CreateOutfitCommand, UpdateOutfitCommand
from port.adapter.resource.outfit.request import SaveOutfitRequest
from port.adapter.resource.outfit.response import OutfitListJson, OutfitJson

router = APIRouter(
    prefix='/outfits',
    tags=['コーディネート']
)


@router.post('', name='新規作成')
def create(request: SaveOutfitRequest):
    application_service: OutfitApplicationService = DIContainer.instance().resolve(OutfitApplicationService)
    application_service.create(CreateOutfitCommand(
        images=request.images,
        gender=request.gender,
        description=request.description,
        posted_at=request.posted_at,
        url=request.url
    ))


@router.put('/{outfit_id}', name='更新')
def update(outfit_id: UUID, request: SaveOutfitRequest):
    application_service: OutfitApplicationService = DIContainer.instance().resolve(OutfitApplicationService)
    application_service.update(UpdateOutfitCommand(
        id=str(outfit_id),
        images=request.images,
        gender=request.gender,
        description=request.description,
        posted_at=request.posted_at,
        url=request.url
    ))


@router.get('', name='一覧取得', response_model=OutfitListJson)
def list(start: int = 0, size: int = 30, gender: Optional[str] = 'MEN') -> OutfitListJson:
    application_service: OutfitApplicationService = DIContainer.instance().resolve(OutfitApplicationService)
    dpo = application_service.list(start, size, gender)
    return OutfitListJson.of(dpo)


@router.get('/{outfit_id}', name='詳細取得', response_model=OutfitJson)
def get(outfit_id: UUID) -> OutfitJson:
    application_service: OutfitApplicationService = DIContainer.instance().resolve(OutfitApplicationService)
    dpo = application_service.get(str(outfit_id))
    return OutfitJson.of(dpo)


@router.delete('/{outfit_id}', name='削除')
def get(outfit_id: UUID):
    application_service: OutfitApplicationService = DIContainer.instance().resolve(OutfitApplicationService)
    application_service.delete(str(outfit_id))
