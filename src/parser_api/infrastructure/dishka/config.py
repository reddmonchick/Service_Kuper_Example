from dishka import Provider, provide, Scope
from environs import Env

from parser_api.infrastructure.config import DatabaseConfig
from parser_api.infrastructure.config import get_database_config


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self, env: Env) -> DatabaseConfig:
        return get_database_config(env)
    
    @provide
    def get_env(self) -> Env:
        env = Env()
        env.read_env()
        return env
