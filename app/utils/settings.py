from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "Bar API"
    postgres_user: str 
    postgres_password: str 
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str 
    model_config = SettingsConfigDict(env_file=".env")
    redis_host: str = "localhost"
    redis_port: int = 6379

settings = Settings()