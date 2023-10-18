import os
from contextlib import asynccontextmanager

from di import DIContainer, DI
from fastapi import FastAPI
from sqlalchemy import create_engine, Engine

from application import UnitOfWork
from domain.model.outfit import OutfitRepository
from port.adapter.persistence.repository.mysql import DataBase, MySQLUnitOfWork
from port.adapter.persistence.repository.mysql.outfit import MySQLOutfitRepository
from port.adapter.resource.outfit import outfit_resource
from port.adapter.standalone.inmemory import InMemOutfitRepository
from port.adapter.resource.health import health_resource

engine: Engine = create_engine(
    'mysql://{username}:{password}@{host}:{port}/{database}?ssl_mode=VERIFY_IDENTITY&charset=utf8mb4'.format(
        username=os.getenv('DATABASE_USERNAME'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=3306,
        database=os.getenv('DATABASE')
    )
)
DI_LIST = [
    DI.of(Engine, {}, engine),
    DI.of(OutfitRepository, {'MySQL': MySQLOutfitRepository, 'InMem': InMemOutfitRepository}, InMemOutfitRepository),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    DataBase.metadata.create_all(bind=engine)
    [DIContainer.instance().register(di) for di in DI_LIST]
    yield


app = FastAPI(title="A.M.A", root_path=os.getenv('OPENAPI_PREFIX'), lifespan=lifespan)

app.include_router(health_resource.router)
app.include_router(outfit_resource.router)
