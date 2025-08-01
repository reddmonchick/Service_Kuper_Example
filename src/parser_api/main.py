from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from dishka import make_async_container
from parser_api.infrastructure.dishka import AppProvider, ConfigProvider, DatabaseProvider, RepositoriesProvider
from parser_api.api.parser_router import router
from contextlib import asynccontextmanager
from parser_api.core.logging.logging_config import configure_logging

configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Initializing Dishka container...")
    yield

    print("Application shutdown: Closing Dishka container...")
    await app.state.dishka_container.close()

app = FastAPI(title="Parser API", lifespan=lifespan)
app.include_router(router)


container = make_async_container(
    AppProvider(),
    ConfigProvider(),
    DatabaseProvider(),
    RepositoriesProvider(),
    FastapiProvider()
)
setup_dishka(container=container, app=app)
