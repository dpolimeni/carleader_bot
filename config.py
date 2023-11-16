from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    openai_key: str

    model_config = SettingsConfigDict(env_file=".env")


configuration = Configuration()
