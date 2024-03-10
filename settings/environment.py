from functools import lru_cache

from pydantic.v1 import BaseSettings


class Environment(BaseSettings):
    BOT_KEY: str
    BYBIT_API_PUBLIC_KEY: str
    BYBIT_API_SECRET_KEY: str
    BYBIT_BASE_API_URL: str
    REGISTER_URL: str
    GROUP_ID: str
    MIN_TRADE_VOLUME: int
    MIN_DEPOSIT: int

    class Config:
        env_file = ".env"


@lru_cache
def get_env() -> Environment:
    return Environment()
