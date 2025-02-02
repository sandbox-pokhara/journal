from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DISCORD_BOT_TOKEN: str = "bot-token"
    BACKEND_URI: str = "http://127.0.0.1:8000/"
    BACKEND_AUTH_TOKEN: str = "auth-token"
    CHECKIN_CHANNEL_ID: str = "channel-id"
    ABSENCE_CHANNEL_ID: str = "channel-id"
    HOLIDAY_CHANNEL_ID: str = "channel-id"


ENV = Environment()
