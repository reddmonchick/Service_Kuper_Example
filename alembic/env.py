from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio

# Добавьте импорт вашего Base и моделей
from parser_api.infrastructure.db.models import Base

config = context.config
fileConfig(config.config_file_name)

# Укажите target_metadata из вашего Base
target_metadata = Base.metadata

def run_migrations_offline():
    """Миграции без подключения к БД"""
    url = config.get_main_option("sqlalchemy.url")
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
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))
    async with connectable.connect() as connection:
        # Исправленная строка: передаем run_migrations как колбэк
        await connection.run_sync(run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    # Исправленный запуск асинхронных миграций
    asyncio.run(run_async_migrations())