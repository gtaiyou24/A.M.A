import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from port.adapter.resource.health import health_resource


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('start')
    yield
    print('end')


app = FastAPI(title="A.M.A", openapi_prefix=os.getenv('OPENAPI_PREFIX'), lifespan=lifespan)

app.include_router(health_resource.router)