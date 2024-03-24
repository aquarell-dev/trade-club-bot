import redis.asyncio as redis

from settings import get_env

env = get_env()

client = redis.Redis(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    password=env.REDIS_PASSWORD
)
