from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expiration_time: int

    model_config = ConfigDict(env_file=".env")  # Fixed: use model_config + correct syntax

settings = Settings()
