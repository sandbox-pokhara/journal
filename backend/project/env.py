from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DEBUG: bool = True
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "journal"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_PORT: int = 5432
    ALLOWED_HOSTS: str = "*"
    CSRF_TRUSTED_ORIGINS: str = "http://127.0.0.1:8000"
    SECRET_KEY: str = "STRONG_KEY"
    DISCORD_BOT_TOKEN: str = "bot-token"
    ABSENCES_ALLOWED_PER_MONTH: int = 2
    CHECK_IN_DISCORD_CHANNEL_ID: int = 0
    ABSENCE_DISCORD_CHANNEL_ID: int = 0
    JOURNAL_DISCORD_CHANNEL_ID: int = 0
    HOLIDAY_DISCORD_CHANNEL_ID: int = 0


ENV = Environment()
