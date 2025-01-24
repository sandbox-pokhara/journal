from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DISCORD_BOT_TOKEN: str = ""
    BACKEND_URI: str = "http://127.0.0.1:8000/"


ENV = Environment()
