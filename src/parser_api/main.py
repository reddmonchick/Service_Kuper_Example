from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from dishka import make_container
from parser_api.core.di import AppProvider 
from parser_api.api.parser_router import router
from contextlib import asynccontextmanager
from parser_api.core.config.logging_config import configure_logging

configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()

app = FastAPI(title="Parser API", lifespan=lifespan)
app.include_router(router)
container = make_container(AppProvider(), FastapiProvider())
setup_dishka(container=container, app=app)