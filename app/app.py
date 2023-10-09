import os
from contextlib import asynccontextmanager

from di import DIContainer, DI
from fastapi import FastAPI

from domain.model.outfit import OutfitRepository
from port.adapter.resource.outfit import outfit_resource
from port.adapter.standalone.inmemory import InMemOutfitRepository
from port.adapter.resource.health import health_resource

DI_LIST = [
    DI.of(OutfitRepository, {}, InMemOutfitRepository),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    [DIContainer.instance().register(di) for di in DI_LIST]
    yield


app = FastAPI(title="A.M.A", openapi_prefix=os.getenv('OPENAPI_PREFIX'), lifespan=lifespan)

app.include_router(health_resource.router)
app.include_router(outfit_resource.router)
