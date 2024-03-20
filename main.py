import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from redis_client import client
from routers import join_team_router, start_router
from settings import get_env

env = get_env()


async def main() -> None:
    bot = Bot(env.BOT_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=RedisStorage(client))

    dp.include_routers(start_router, join_team_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    await client.aclose()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    asyncio.run(main())
