from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio
from environs import Env

# Добавьте импорт вашего Base и моделей
from src.parser_api.infrastructure.db.models import Base

config = context.config
fileConfig(config.config_file_name)

# Укажите target_metadata из вашего Base
target_metadata = Base.metadata

def get_url_from_env() -> str:
    """
    Builds the database connection URL from environment variables.
    This ensures alembic uses the same configuration source as the app.
    """
    env = Env()
    env.read_env()
    # For local runs, you might want to switch DB_HOST to localhost in your .env file
    return (
        f"postgresql+asyncpg://{env.str('DB_USER')}:{env.str('DB_PASSWORD')}"
        f"@{env.str('DB_HOST')}:{env.int('DB_PORT')}/{env.str('DB_PATH')}"
    )

def run_migrations_offline():
    """Миграции без подключения к БД"""
    url = get_url_from_env()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations(connection):
    """Запуск миграций через синхронное соединение"""
    context.configure(
        connection=connection, 
        target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    """Асинхронный запуск миграций"""
    url = get_url_from_env()
    connectable = create_async_engine(url)
    async with connectable.connect() as connection:
        await connection.run_sync(run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
