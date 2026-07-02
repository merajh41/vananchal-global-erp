from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Vananchal Global ERP"
    VERSION: str = "0.1.0"
    COMPANY_NAME: str = "Vananchal Global"

    class Config:
        env_file = ".env"


settings = Settings()