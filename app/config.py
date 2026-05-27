from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    - When this calss is called pydantic runs through all of the them
    - Looks and import all of them 
    - Performs auto validation and ensure proper key transformation.
    - With this validation in place one can easily realise which varible is missing and which is wron, etc.
    """
    database_hostname: str 
    database_port: str 
    data_port: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token: str
    database_password: str
    access_token_expires_minute: int

    class Config:
        env_file = ".env"


settings = Settings()
