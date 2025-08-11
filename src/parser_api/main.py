from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from dishka import make_async_container, AsyncContainer
from src.parser_api.infrastructure.dishka import AppProvider, ConfigProvider, DatabaseProvider, RepositoriesProvider
from src.parser_api.api.parser_router import router
from contextlib import asynccontextmanager
from src.parser_api.core.logging.logging_config import configure_logging

def create_app(container: AsyncContainer) -> FastAPI:
    """Create the FastAPI app and setup Dishka."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Application startup: Initializing Dishka container...")
        yield
        print("Application shutdown: Closing Dishka container...")
        await container.close()

    app = FastAPI(title="Parser API", lifespan=lifespan)
    app.include_router(router)
    setup_dishka(container=container, app=app)
    return app

# Configure logging once
configure_logging()

# Create the default container and app for production
prod_container = make_async_container(
    AppProvider(),
    ConfigProvider(),
    DatabaseProvider(),
    RepositoriesProvider(),
    FastapiProvider()
)
app = create_app(container=prod_container)
