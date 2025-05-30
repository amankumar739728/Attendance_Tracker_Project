from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Todo App"
    app_version: str = "1.0.0"
    jwt_secret: str
    database_url: str
    secret_key: str
    password_secret_key: str
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    ch_pool_min_size: int
    ch_pool_max_size: int

    algorithm: str


    class Config:
        env_file = ".env.development"

def get_settings():
    return Settings()



import os
from pathlib import Path

from dotenv import load_dotenv

env = os.environ.get("PY_ENV") or "development"
env_path = os.path.join(Path(__file__).parent.parent.parent, f".env.{env}")
load_dotenv(dotenv_path=env_path)

#ENV CONFIGURATION
SECRET_KEY = os.environ.get('SECRET_KEY')
REFRESH_SECRET_KEY = os.environ.get('REFRESH_SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get('REFRESH_TOKEN_EXPIRE_DAYS'))
ALGORITHM= os.environ.get('ALGORITHM')


JWT_EXCLUDE_PATH = [
    '/docs',
    '/swaggerapi/docs',
    '/health',
    'openapi.json'
]

ENABLE_JWT = True
