import redis.asyncio as redis

from settings import get_env

env = get_env()

client = redis.from_url(env.REDIS_URL)
