from pydantic import (
    BaseModel, 
    model_validator, 
    SecretStr,
    RedisDsn,
    PostgresDsn,
    NatsDsn
)


class DatabaseConfig(BaseModel):
    user: str
    password: str
    path: str
    host: str = "db"
    port: int = 5432
    driver: str = "asyncpg"
    system: str = "postgresql"


    def build_connection_url(self) -> str:
        dsn: PostgresDsn = PostgresDsn.build(
            scheme=f"{self.system}+{self.driver}",
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            path=self.path
        )
        return dsn.unicode_string()