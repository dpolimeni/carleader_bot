from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Configuration(BaseSettings):
    openai_key: str
    chat_model_version: str
    # emb_model_version: str

    model_config = SettingsConfigDict(env_file=".env")


configuration = Configuration()
