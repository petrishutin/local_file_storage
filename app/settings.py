import os

from pydantic import BaseSettings


class Config(BaseSettings):
    """Config of microservice"""
    STORAGE_USER: str = 'admin'
    PASSWORD: str = 'admin'
    SECRET_KEY: str = 'replace_this_with_your_string'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    DB: str = f'database.db'
    DB_URL: str = f'sqlite:///{BASE_DIR}/{DB}'
    LOG_LEVEL: str = 'INFO'

    class Config:
        case_sensitive = True
        env_file = '.env'


config = Config()
