from parser_api.infrastructure.config.models import DatabaseConfig

from environs import Env

def get_database_config(env: Env) -> DatabaseConfig:
    return DatabaseConfig(
        user=env.str("DB_USER"),
        password=env.str("DB_PASSWORD"),
        host=env.str("DB_HOST", "db"),
        port=env.int("DB_PORT", 5432),
        path=env.str("DB_PATH"),
        driver=env.str("DB_DRIVER", "asyncpg"),
        database_system=env.str("DB_SYSTEM", "postgresql"),
    )