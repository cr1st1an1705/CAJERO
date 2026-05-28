from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NOMBRE: str = "Backend Cajero ATM"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    BACKEND_CORS_ORIGINS: str = ""

    JWT_SECRET: str = "CAMBIA_ESTE_SECRETO"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_MINUTES: int = 60

    SESSION_IDLE_MINUTES: int = 3
    MAX_INTENTOS_PIN: int = 4
    MINUTOS_BLOQUEO: int = 1

    DATABASE_URL: str | None = None
    DB_PRIMARY_URL: str | None = None
    DB_SECONDARY_URL: str | None = None
    ENABLE_DB_FAILOVER: bool = False
    AUTO_INIT_SCHEMA: bool = False

    DB_PRIMARY_HOST: str = "127.0.0.1"
    DB_PRIMARY_PORT: int = 3307
    DB_PRIMARY_NAME: str = "cajero_atm"
    DB_PRIMARY_USER: str = "cajero_user"
    DB_PRIMARY_PASSWORD: str = "cajero_pass"

    DB_SECONDARY_HOST: str = "127.0.0.1"
    DB_SECONDARY_PORT: int = 3308
    DB_SECONDARY_NAME: str = "cajero_atm"
    DB_SECONDARY_USER: str = "cajero_user"
    DB_SECONDARY_PASSWORD: str = "cajero_pass"

    @staticmethod
    def _normalize_db_url(url: str) -> str:
        if url.startswith("mysql://"):
            return "mysql+pymysql://" + url.removeprefix("mysql://")
        return url

    @property
    def ALLOWED_CORS_ORIGINS(self) -> list[str]:
        return [x.strip() for x in self.BACKEND_CORS_ORIGINS.split(",") if x.strip()]

    @property
    def PRIMARY_DB_URL(self) -> str:
        explicit_url = self.DB_PRIMARY_URL or self.DATABASE_URL
        if explicit_url:
            return self._normalize_db_url(explicit_url)
        return (
            f"mysql+pymysql://{self.DB_PRIMARY_USER}:{self.DB_PRIMARY_PASSWORD}"
            f"@{self.DB_PRIMARY_HOST}:{self.DB_PRIMARY_PORT}/{self.DB_PRIMARY_NAME}"
        )

    @property
    def SECONDARY_DB_URL(self) -> str | None:
        if self.DB_SECONDARY_URL:
            return self._normalize_db_url(self.DB_SECONDARY_URL)

        if not self.ENABLE_DB_FAILOVER:
            return None

        return (
            f"mysql+pymysql://{self.DB_SECONDARY_USER}:{self.DB_SECONDARY_PASSWORD}"
            f"@{self.DB_SECONDARY_HOST}:{self.DB_SECONDARY_PORT}/{self.DB_SECONDARY_NAME}"
        )

settings = Settings()
